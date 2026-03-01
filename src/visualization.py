"""
Visualization utilities for the highway lane-change FSM planner.
"""

from typing import Dict, List

import matplotlib.pyplot as plt

from .highway_world import Vehicle


def plot_highway_snapshot(
    vehicles: List[Vehicle],
    ego: Vehicle,
    length: float = 300.0,
    lanes: int = 3,
) -> None:
    """
    Draw a snapshot of the highway:
    - x-axis: s along road
    - y-axis: lane index. [file:16]
    """
    plt.figure(figsize=(10, 4))

    # Draw lane lines
    for lane in range(lanes):
        plt.hlines(lane, 0, length, colors="lightgray")

    # Draw vehicles
    for v in vehicles:
        if v.is_ego:
            plt.scatter(v.s, v.lane, marker="s", s=100, label="ego", color="red")
        else:
            plt.scatter(v.s, v.lane, color="blue")

    plt.xlim(0, length)
    plt.ylim(-0.5, lanes - 0.5)
    plt.xlabel("s along road")
    plt.ylabel("lane")
    plt.title("Highway Snapshot")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_behavior_over_time(history: Dict[str, List]) -> None:
    """
    Plot ego speed and discrete behavior state over time. [file:16]
    """
    times = history["time"]
    speed = history["speed"]
    states = history["state"]

    unique_states = sorted(set(states))
    state_levels = {s: i for i, s in enumerate(unique_states)}
    levels = [state_levels[s] for s in states]

    fig, axs = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

    axs[0].plot(times, speed)
    axs[0].set_ylabel("Speed [m/s]")
    axs[0].set_title("Ego Speed Over Time")
    axs[0].grid(True)

    axs[1].step(times, levels, where="mid")
    axs[1].set_yticks(list(state_levels.values()))
    axs[1].set_yticklabels(unique_states)
    axs[1].set_xlabel("Time step")
    axs[1].set_ylabel("State")
    axs[1].set_title("Behavior State Over Time")
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()
