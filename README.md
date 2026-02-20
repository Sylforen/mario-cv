# Vectorised Epsilon-Greedy RL in Super Mario Bros

<p align="center">
  <img src="./best_run.gif" width="600"/>
</p>

This project demonstrates a lightweight reinforcement learning agent for Super Mario Bros. Instead of using a deep neural network, the agent relies on simple sprite detection and proximity-based features (distance to enemies, obstacles, and gaps) to decide when to move or jump.  

The agent also tracks areas where it repeatedly gets stuck and increases exploration near those points in future episodes. The best-performing episode from a run is saved as `best_run.gif`, displayed above.

---

## Getting Started

### Clone the Project

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install gym gym-super-mario-bros nes-py numpy opencv-python pillow tqdm
```

---

## Running the Agent Locally

Start the agent with default settings:

```bash
python main.py
```

You can also adjust some parameters:

```bash
python main.py --episodes 50 --enemy_factor 0.95 --gap_factor 0.9
```

Press `q` during execution to close the display window at any time.

---

## Using Docker (Optional)

The Docker setup provides a clean, reproducible environment and supports GPU acceleration.

### Build the Docker Image

From the project folder:

```bash
docker build -t mario-ml .
```

### Run the Container

```bash
docker run --gpus all -it --rm \
    -v "$PWD":/app \
    mario-ml
```

**Notes on the command:**

- `--gpus all` → gives the container access to your GPU(s)  
- `-it` → runs interactively  
- `--rm` → automatically removes the container after exiting  
- `-v "$PWD":/app` → mounts the current folder inside the container  

Once inside the container, start the agent:

```bash
python main.py
```

---

## How It Works

- **Sprite Detection:** The agent detects Mario, enemies, obstacles, gaps, bricks, and collectibles in each frame.  
- **Feature Extraction:** Converts positions into simple distance-based metrics.  
- **Action Policy:** Uses a rule-guided epsilon-greedy style to decide when to move, jump, or explore randomly.  
- **Stagnation Handling:** Tracks repeated failure points and encourages exploration nearby.  
- **Output:** Saves the highest-reward run as a GIF for easy viewing.

---

This project shows how reinforcement learning can be applied using interpretable, structured logic and computer vision, without relying on deep learning.
