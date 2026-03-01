"""
Highway world model: vehicles, lane layout, and distance computation
for the FSM-based lane-change behavior planner.
"""

from dataclasses import dataclass
from typing import List, Tuple
import random


@dataclass
class Vehicle:
    lane: int          # lane index: 0, 1, 2
    s: float           # longitudinal position along the road
    speed: float       # speed in m/s (simplified)
    is_ego: bool = False


def create_highway(
    num_vehicles: int = 15,
    length: float = 300.0,
    lanes: int = 3,
) -> Tuple[List[Vehicle], Vehicle]:
    """
    Create a simple 1D highway with:
    - 'lanes' lanes
    - one ego vehicle (middle lane, near start)
    - multiple random vehicles ahead of the ego. [file:16]
    """
    vehicles: List[Vehicle] = []

    # Ego in middle lane near the start
    ego = Vehicle(lane=1, s=10.0, speed=20.0, is_ego=True)
    vehicles.append(ego)

    for _ in range(num_vehicles):
        lane = random.randint(0, lanes - 1)
        s = random.uniform(20.0, length)  # ahead of ego
        speed = random.uniform(10.0, 30.0)
        vehicles.append(Vehicle(lane=lane, s=s, speed=speed))

    return vehicles, ego


def compute_distances(
    vehicles: List[Vehicle],
    ego: Vehicle,
    lanes: int = 3,
    max_dist: float = 1e6,
) -> Tuple[float, float, float]:
    """
    Compute distances to nearest vehicles ahead in:
    - same lane
    - left adjacent lane
    - right adjacent lane. [file:16]
    """
    d_same = max_dist
    d_left = max_dist
    d_right = max_dist

    for v in vehicles:
        if v.is_ego:
            continue
        if v.s <= ego.s:
            continue

        gap = v.s - ego.s

        if v.lane == ego.lane and gap < d_same:
            d_same = gap
        if v.lane == ego.lane - 1 and gap < d_left:
            d_left = gap
        if v.lane == ego.lane + 1 and gap < d_right:
            d_right = gap

    return d_same, d_left, d_right
