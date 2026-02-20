# Vectorised Epsilon-Greedy RL in Super Mario Bros

<p align="center">
  <img src="./best_run.gif" width="600"/>
</p>

This project demonstrates a lightweight reinforcement learning agent for Super Mario Bros. It uses simple sprite detection and proximity-based features (distance to enemies, obstacles, and gaps) for decision-making. The agent also tracks areas of repeated failure and increases exploration near those points. The best-performing episode is saved as `best_run.gif`.

---

## Getting Started

### Clone the Project

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Install Dependencies
pip install -r requirements.txt
```

Or manually:

```bash
pip install gym gym-super-mario-bros nes-py numpy opencv-python pillow tqdm
Running the Agent
```

Start training:

```bash
python main.py --episodes 50 --enemy_factor 0.95 --gap_factor 0.9
```

Press q to close the display window at any time.

## Docker (Optional)
Build the Docker Image
```bash
docker build -t mario-ml .
```
Run the Container
```bash
docker run --gpus all -it --rm -v "$PWD":/app mario-ml
```
