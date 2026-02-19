import numpy as np


class metrics(object):
	# Calculate the metrics based on the location of detected sprites
	def __init__(self, frame_size):
		"""
		Args:
		frame_size:
			The observation space of the environment.
			If the observation space size is used to 
			scale the rectangles.
		"""
		self.largest_distance = ((0 - frame_size[1]) ** 2 + (0 - frame_size[0]) ** 2) ** 0.5

	def compute(self, mario_loc, enemy_loc, obstacle_loc, gap_x):
		"""
		Args:
		mario_loc:
			The location of Mario on the frame
		enemy_loc:
			The location of all the enemies in the frame.
		obstacle_loc:
			The location of all the enemies in the frame.
		gap_x:
			The location of all the gaps in the bottom of 
			the frame.
		"""

		# if Mario is not detected on the frame return all zeros
		if len(mario_loc) == 0:
			return 0, 0, 0, 0, 0, 0, 0
		else:
			mario_location = mario_loc[0]
			mario_right = mario_loc[0][0] + 14

			# The number of enemies on screen
			enemy_no = len(enemy_loc)

			# The closest enemy factor
			if enemy_no == 0:
				closest_enemy = 0
			else:
				closest_enemy = 0
				for i in enemy_loc:
					enemy_distance = ((mario_right - i[0]) ** 2 + (mario_loc[0][1] - i[1]) ** 2) ** 0.5
					enemy_distance = 1 - (enemy_distance / self.largest_distance)
					if enemy_distance > closest_enemy:
						closest_enemy = enemy_distance

			# The closest obstacle and its height
			if len(obstacle_loc) == 0:
				closest_obstacle = 0
				obstacle_height = 0
			else:
				obstacle_distance = [(i[0] - mario_right, i[1]) for i in obstacle_loc if i[0] - mario_right > 0]
				if len(obstacle_distance) > 0:
					closest_obstacle = min(obstacle_distance)
					obstacle_height = (mario_loc[0][1] + 16 - closest_obstacle[1]) / 240
					closest_obstacle = 1 - (closest_obstacle[0] / 256)
				else:
					closest_obstacle = 0
					obstacle_height = 0


			# The closest gap to the right of Mario
			if len(gap_x) == 0:
				closest_gap = 0
				gap_length = 0
			else:
				gap_distance = [i - mario_right for i in gap_x if i - mario_right > 0]
				if len(gap_distance) > 0:
					closest_gap = min(gap_distance)
					closest_gap = (1 - (closest_gap / 256))
				else:
					closest_gap = 0

				# The distance of any gap
				gap_length = max(gap_x) - min(gap_x) + 16

			return mario_location, enemy_no, closest_enemy, closest_obstacle, obstacle_height, closest_gap, gap_length