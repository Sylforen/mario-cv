import gym
import numpy as np
from PIL import Image
from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import RIGHT_ONLY, SIMPLE_MOVEMENT,  COMPLEX_MOVEMENT
import cv2
from wrappers import MaxAndSkipEnv
from load_sprites import load_images
from detect import detect_cv
from metrics import metrics
import argparse
from collections import deque

try:
	from tqdm.auto import tqdm
except ImportError:  # fallback if tqdm is not installed
	def tqdm(x, *args, **kwargs):
		return x

import mario_patches


if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("--enemy_factor", default=0.95, type=float, help='Maximum enemy closeness before jumping')
	parser.add_argument("--gap_factor", default=0.9, type=float, help='Maximum obstacle closeness before jumping')
	parser.add_argument("--obstacle_factor", default=0.9, type=float, help='Maximum gap closeness before jumping')
	parser.add_argument("--scale", default=2.0, type=float, help="Scale factor for display window")
	parser.add_argument("--stagnation_steps", default=60, type=int, help='Frames without world-distance progress before treating as stagnation')
	parser.add_argument("--explore_steps", default=1000, type=int, help='Frames to favor random actions after stagnation detected')
	parser.add_argument("--stagnation_tolerance", default=32, type=int, help='World x-position tolerance around stagnation points to encourage exploration')
	parser.add_argument("--stagnation_leadup", default=200, type=int, help='World distance before a stagnation point to start random exploration')
	parser.add_argument("--episodes", default=100, type=int, help='Number of episodes to run in this series')
	args = parser.parse_args()

	# Load the envirinment
	env = gym_super_mario_bros.make('SuperMarioBros-1-1-v0')

	env = JoypadSpace(env, RIGHT_ONLY)
	env = MaxAndSkipEnv(env, 1) # only process 1/2 frames

	observation_space = env.observation_space.shape

	# Load the sprites (including collectibles)
	mario_list, enemy_list, obstacle_list, brick_list, rock_list, collectible_list = load_images()

	# Initialise the detection and the 
	detection = detect_cv(observation_space)
	analyse = metrics(observation_space)
	def draw_nearest_lines(frame, mario_loc, target_locs, color, max_items=3, exclude_locs=None):
		"""Draw lines from Mario to the nearest items in a list of sprite detections.

		Args:
		frame: current BGR frame being displayed
		mario_loc: list of detected Mario positions [(x, y), ...]
		target_locs: list of detected sprite positions [(x, y), ...]
		color: BGR tuple for the line color
		max_items: maximum number of nearest items to connect
		exclude_locs: optional list of positions to exclude (e.g., rocks)
		"""
		if not mario_loc or not target_locs:
			return frame

		if exclude_locs is None:
			exclude_locs = []
		exclude_set = set(exclude_locs)

		mario_x, mario_y = mario_loc[0]
		distances = []
		for (x, y) in target_locs:
			# Skip any targets that coincide with excluded locations (e.g., rocks)
			if (x, y) in exclude_set:
				continue
			d = ((x - mario_x) ** 2 + (y - mario_y) ** 2) ** 0.5
			distances.append((d, (x, y)))

		# Sort by distance and draw lines to the closest ones
		distances.sort(key=lambda item: item[0])
		for _, (x, y) in distances[:max_items]:
			cv2.line(frame, (mario_x, mario_y), (x, y), color, 1)

		return frame

	def action_selection(enemy_no, enemy_close, obstacle_close, obstacle_height, gap_close, gap_distance, timesteps, exploring=False, near_stagnation=False):
		"""
		Select an action based on set parameters.
		Args:
		enemy_no: 
			The number of enemies in the frame
		enemy_close: 
			The factor for the closest enemy to mario. The larger 
			the number the closer the enemy.
		obstacle_close:
			The factor for the closest obstacle to mario. The larger 
			the number the closer the obstacle.
		obstacle_height:
			The height of the obstacle. Useful for getting over large 
			pipes.
		gap_close:
			The factor for the closest gap to mario. The larger 
			the number the closer the gap.
		gap_distance:
			The length of the gap.
		timesteps:
			The total number of frames played of the level.
		exploring:
			Whether we are in an exploration phase due to detected stagnation.
		near_stagnation:
			Whether Mario is currently near a previously detected stagnation point.
		"""
		# When we are exploring due to stagnation, bias towards random actions
		# to encourage trying alternative behaviors.
		if exploring or near_stagnation:
			if np.random.rand() < 0.7:
				return env.action_space.sample()

		if enemy_close > args.enemy_factor:
			return 4 # jump right
		elif gap_close > args.gap_factor:
			return 4 # jump right
		elif cnt % 9 == 0:
			return 0 # noop, used to reset the jump
		elif obstacle_close > args.obstacle_factor:
			return 4 # jump right
		else:
			return 1 # walk right

	best_reward_total = None
	best_run_frames = []
	global_stagnation_positions = []  # track problematic world x-positions across episodes
	global_best_x_pos = 0
	stagnation_episode_counter = 0
	best_run_index = None
	best_run_steps = None
	last_runs = deque(maxlen=5)

	for i in tqdm(range(args.episodes), desc="Episodes"):
		state = env.reset()
		avg_loss = 0
		cnt = 0
		reward_total = 0
		reward_counter = 0
		frames_for_episode = []
		best_x = 0
		last_x_pos = None
		episode_max_x = 0
		last_flag_get = False
		exploration_steps_remaining = 0
		while True:
			#env.render()

			# change the state colours to match openCV's imshow
			frame = cv2.cvtColor(state, cv2.COLOR_RGB2BGR)
			frame_grey = cv2.cvtColor(state, cv2.COLOR_RGB2GRAY)

			# Detect sprites in the frame
			frame, mario_loc = detection.detect_mario(frame, frame_grey, mario_list)
			frame, enemy_loc = detection.detect(frame, frame_grey, enemy_list)
			frame, obstacle_loc = detection.detect(frame, frame_grey, obstacle_list)
			frame, brick_loc = detection.detect(frame, frame_grey, brick_list)
			frame, gap_x = detection.detect_gap(frame, frame_grey, rock_list)
			# Detect rocks explicitly so we can exclude them from line drawing
			#frame, rock_loc = detection.detect(frame, frame_grey, rock_list)
			frame, collect_loc = detection.detect(frame, frame_grey, collectible_list)

			# Draw lines from Mario to the nearest three items in each sprite list
			frame = draw_nearest_lines(frame, mario_loc, enemy_loc, (0, 0, 255))                 # enemies - red
			frame = draw_nearest_lines(frame, mario_loc, obstacle_loc, (255, 0, 0))   # obstacles - blue, excluding rocks
			frame = draw_nearest_lines(frame, mario_loc, brick_loc, (255, 255, 0))               # bricks - cyan/yellow
			frame = draw_nearest_lines(frame, mario_loc, collect_loc, (0, 255, 0))               # collectibles - green





			# Calculate the metrics
			mario_location, enemy_no, closest_enemy, closest_obstacle, obstacle_height, closest_gap, gap_length = analyse.compute(mario_loc, enemy_loc, obstacle_loc, gap_x)

			# Place the metrics on the frame
			font = cv2.FONT_HERSHEY_SIMPLEX
			frame = cv2.putText(frame, 'Mario: {}'.format(mario_location), (10, 40), font, 0.3, (0, 0, 0), 1, cv2.LINE_AA)
			frame = cv2.putText(frame, 'Enemy no.: {}'.format(enemy_no), (10, 50), font, 0.3, (0, 0, 0), 1, cv2.LINE_AA)
			frame = cv2.putText(frame, 'Enemy close: {:.2f}'.format(closest_enemy), (10, 60), font, 0.3, (0, 0, 0), 1, cv2.LINE_AA)
			frame = cv2.putText(frame, 'Obstacle close: {:.2f}'.format(closest_obstacle), (10, 70), font, 0.3, (0, 0, 0), 1, cv2.LINE_AA)
			frame = cv2.putText(frame, 'Obstacle height: {:.2f}'.format(obstacle_height), (10, 80), font, 0.3, (0, 0, 0), 1, cv2.LINE_AA)
			frame = cv2.putText(frame, 'Gap close: {:.2f}'.format(closest_gap), (10, 90), font, 0.3, (0, 0, 0), 1, cv2.LINE_AA)
			frame = cv2.putText(frame, 'Gap distance: {}'.format(gap_length), (10, 100), font, 0.3, (0, 0, 0), 1, cv2.LINE_AA)

			# Scale frame for easier human viewing
			display_frame = frame
			if args.scale != 1.0:
				h, w = frame.shape[:2]
				display_frame = cv2.resize(frame, (int(w * args.scale), int(h * args.scale)), interpolation=cv2.INTER_NEAREST)

			# Store frame for potential GIF of best run
			rgb_display = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
			frames_for_episode.append(Image.fromarray(rgb_display))

			# Display the run
			window_name = "Mario Run"
			cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
			cv2.imshow(window_name, display_frame)
			if cv2.waitKey(1)&0xFF == ord('q'):
				break

			# Determine if we're near or approaching any known stagnation point in world coordinates.
			# "Near" means within stagnation_tolerance of the point; "approaching" means we are
			# to the left of the point but within stagnation_leadup world units, which encourages
			# trying alternative actions in the lead-up before we reach the problematic spot.
			near_stagnation_zone = False
			if last_x_pos is not None:
				for pos in global_stagnation_positions:
					if abs(last_x_pos - pos) <= args.stagnation_tolerance:
						near_stagnation_zone = True
						break
					# Approaching from the left: not yet at the stagnation point but close in world distance
					if 0 < (pos - last_x_pos) <= args.stagnation_leadup:
						near_stagnation_zone = True
						break

			# Select the next action using the metrics and stagnation-informed exploration
			exploring = exploration_steps_remaining > 0
			action = action_selection(enemy_no, closest_enemy, closest_obstacle, obstacle_height, closest_gap, gap_length, cnt, exploring=exploring, near_stagnation=near_stagnation_zone)

			# play the next action
			next_state, reward, done, info = env.step(action)

			# Track world x-position for this episode
			x_pos = info.get('x_pos', None)
			if x_pos is not None:
				last_x_pos = x_pos
				if x_pos > episode_max_x:
					episode_max_x = x_pos
			last_flag_get = info.get('flag_get', False) or last_flag_get
			reward_total += reward
			state = next_state
			if done:
				print(cnt, reward_total)
				break
			cnt +=1
			if exploration_steps_remaining > 0:
				exploration_steps_remaining -= 1

		# Episode-level stagnation detection in world coordinates
		# If we repeatedly fail to improve beyond roughly the same best x,
		# add that location as a stagnation point to encourage exploration there.
		if episode_max_x > 0 and not last_flag_get:
			if episode_max_x > global_best_x_pos + args.stagnation_tolerance:
				global_best_x_pos = episode_max_x
				stagnation_episode_counter = 0
			else:
				stagnation_episode_counter += 1
				if stagnation_episode_counter >= 3 and global_best_x_pos > 0:
					global_stagnation_positions.append(global_best_x_pos)
					print(f"Detected repeated failure near world x={global_best_x_pos}. Adding stagnation point.")
					stagnation_episode_counter = 0

		# Track best run by total reward and save frames
		if best_reward_total is None or reward_total > best_reward_total:
			best_reward_total = reward_total
			best_run_frames = frames_for_episode
			best_run_index = i
			best_run_steps = cnt

		# Track last 5 runs (index, reward, steps only; frames not stored)
		last_runs.append({"episode": i, "reward": reward_total, "steps": cnt})

	# Save best run as GIF
	if best_run_frames:
		output_filename = "best_run.gif"
		best_run_frames[0].save(output_filename, save_all=True, append_images=best_run_frames[1:], duration=50, loop=0)
		print(f"Saved best run GIF to {output_filename}")
		if best_run_index is not None and best_run_steps is not None:
			print(f"Best run: episode {best_run_index} | reward={best_reward_total:.2f} | steps={best_run_steps}")
		if last_runs:
			print("Last 5 runs (most recent last):")
			for r in list(last_runs):
				print(f"  Episode {r['episode']}: reward={r['reward']:.2f}, steps={r['steps']}")

	env.close()
	cv2.destroyAllWindows()