# Highway Lane-Change Behavior Planner (FSM)

This project implements a cost-based behavior planner for highway lane changes using a Finite State Machine (FSM).
It simulates an ego vehicle on a 3-lane highway with randomly placed vehicles and selects behaviors such as CRUISE, FOLLOW, STOP, LANE_CHANGE_LEFT, LANE_CHANGE_RIGHT, and ACCELERATE based on transition costs and distances to nearby cars.

## How to run (Python)

You can run the FSM simulation and visualize the results from a Python session:

```python
from src.simulation import run_simulation
from src.visualization import plot_highway_snapshot, plot_behavior_over_time

vehicles, history = run_simulation(steps=30)

# Ego is the first vehicle in the list
ego = next(v for v in vehicles if v.is_ego)

plot_highway_snapshot(vehicles, ego)
plot_behavior_over_time(history)
```

## Project overview

This project implements a highway lane-change behavior planner using a cost-based Finite State Machine (FSM). 

An ego vehicle drives on a three-lane highway with randomly placed vehicles and selects behaviors such as CRUISE, FOLLOW, STOP, LANE_CHANGE_LEFT, LANE_CHANGE_RIGHT, and ACCELERATE based on transition costs and traffic-dependent penalties. 

## Key features

- Cost-based FSM with explicit transition costs between behavior states. 
- Simple 3-lane highway world with ego and randomly placed surrounding vehicles. 
- Perception logic that computes distances to nearest vehicles in same and adjacent lanes.
- Behavior selection using base transition costs plus traffic penalties (safety, lane availability, inertia). 
- Modular Python design (`states`, `highway_world`, `behavior_sm`, `simulation`, `visualization`). [file:16]
- CLI demo that runs the simulation and saves plots into `docs/`. 

## Code structure

- `notebooks/Projekt_2_Behavior_Planning_FSM.ipynb` – teaching/demo notebook for the FSM planner.
- `src/states.py` – FSM state set and base transition-cost table. 
- `src/highway_world.py` – `Vehicle` model, highway creation, and distance computation. 
- `src/behavior_sm.py` – generic `SM` class, traffic penalty, and `BehaviorSM` implementation. 
- `src/simulation.py` – `run_simulation()` loop for the ego vehicle. 
- `src/visualization.py` – functions to save highway snapshot and behavior-over-time plots to `docs/`.
- `scripts/demo.py` – command-line entry point to run the planner.

## How to run

Create and activate a virtual environment, then install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install matplotlib
Run the demo:
```

```bash
python3 -m scripts.demo
```

This will run a 30-step simulation and save plots to docs/highway_snapshot.png and docs/behavior_over_time.png.

---

