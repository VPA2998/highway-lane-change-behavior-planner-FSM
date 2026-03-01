"""
Visualization utilities for the highway lane-change FSM planner.
"""
import os
import matplotlib.pyplot as plt
from typing import Dict, List
import matplotlib.pyplot as plt
from .highway_world import Vehicle


def plot_highway_snapshot(
    vehicles: List[Vehicle],
    ego: Vehicle,
    length: float = 300.0,
    lanes: int = 3,
    save_path: str | None = "docs/highway_snapshot.png",
) -> None:
    plt.figure(figsize=(10, 4))

    for lane in range(lanes):
        plt.hlines(lane, 0, length, colors="lightgray")

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

    if save_path is not None:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150)

    plt.close()



def plot_behavior_over_time(
    history: Dict[str, List],
    save_path: str | None = "docs/behavior_over_time.png",
) -> None:
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

    if save_path is not None:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150)

    plt.close()
