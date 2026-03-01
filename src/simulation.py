"""
Simulation wrapper for the highway lane-change FSM behavior planner.
"""

from typing import Dict, List, Tuple

from .highway_world import Vehicle, create_highway, compute_distances
from .behavior_sm import BehaviorSM


def run_simulation(
    steps: int = 30,
    length: float = 300.0,
    lanes: int = 3,
    num_vehicles: int = 20,
) -> Tuple[List[Vehicle], Dict[str, List]]:
    """
    Run a simple simulation of the ego vehicle on the highway.

    Returns:
        vehicles: final list of vehicles (including ego)
        history: dict with time, s, lane, speed, state lists. [file:16]
    """
    vehicles, ego = create_highway(num_vehicles=num_vehicles, length=length, lanes=lanes)

    sm = BehaviorSM()
    sm.start()

    history = {
        "time": [],
        "s": [],
        "lane": [],
        "speed": [],
        "state": [],
    }

    dt = 1.0  # 1 second time step

    for t in range(steps):
        d_same, d_left, d_right = compute_distances(vehicles, ego, lanes=lanes)

        inp = {
            "d_same": d_same,
            "d_left": d_left,
            "d_right": d_right,
            "lane": ego.lane,
            "speed": ego.speed,
        }

        state = sm.step(inp)

        # Simple dynamics based on state (from notebook). [file:16]
        if state == "CRUISE":
            target_speed = 20.0
        elif state == "FOLLOW":
            target_speed = 12.0
        elif state == "STOP":
            target_speed = 0.0
        elif state == "ACCELERATE":
            target_speed = 25.0
        elif state == "LANE_CHANGE_LEFT":
            target_speed = 18.0
            if ego.lane > 0:
                ego.lane -= 1
        elif state == "LANE_CHANGE_RIGHT":
            target_speed = 18.0
            if ego.lane < lanes - 1:
                ego.lane += 1
        else:
            target_speed = ego.speed

        # Relax ego speed toward target
        ego.speed += 0.5 * (target_speed - ego.speed) * dt

        # Update position
        ego.s += ego.speed * dt

        history["time"].append(t)
        history["s"].append(ego.s)
        history["lane"].append(ego.lane)
        history["speed"].append(ego.speed)
        history["state"].append(state)

    return vehicles, history
