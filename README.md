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
