"""
Command-line demo for the highway lane-change behavior planner (FSM).

Run:
    python scripts/demo.py
"""

from src.simulation import run_simulation
from src.visualization import plot_highway_snapshot, plot_behavior_over_time
from src.highway_world import Vehicle


def main() -> None:
    vehicles, history = run_simulation(steps=30)

    ego: Vehicle = next(v for v in vehicles if v.is_ego)

    print("✅ Simulation finished.")
    print(f"Final ego position s={ego.s:.1f} m, lane={ego.lane}, speed={ego.speed:.1f} m/s")
    print(f"Total steps: {len(history['time'])}")

    plot_highway_snapshot(vehicles, ego)
    plot_behavior_over_time(history)


if __name__ == "__main__":
    main()
