"""
FSM state definitions and base transition cost table
for the highway lane-change behavior planner.
"""

from typing import Dict, List


# All behavior states used by the planner
states: List[str] = [
    "CRUISE",
    "FOLLOW",
    "STOP",
    "LANE_CHANGE_LEFT",
    "LANE_CHANGE_RIGHT",
    "ACCELERATE",
]


# Base (nominal) transition cost table: lower = more preferred
# This mirrors the notebook’s base_transition_cost structure. [file:16]
base_transition_cost: Dict[str, Dict[str, float]] = {s: {} for s in states}


def _set_cost(s_from: str, s_to: str, cost: float) -> None:
    base_transition_cost[s_from][s_to] = cost


# Staying in the same state is usually cheap
for s in states:
    _set_cost(s, s, 1.0)

# Preferences from CRUISE
_set_cost("CRUISE", "FOLLOW", 2.0)
_set_cost("CRUISE", "ACCELERATE", 2.0)
_set_cost("CRUISE", "LANE_CHANGE_LEFT", 3.0)
_set_cost("CRUISE", "LANE_CHANGE_RIGHT", 3.0)
_set_cost("CRUISE", "STOP", 5.0)

# Preferences from FOLLOW
_set_cost("FOLLOW", "CRUISE", 2.0)
_set_cost("FOLLOW", "LANE_CHANGE_LEFT", 2.5)
_set_cost("FOLLOW", "LANE_CHANGE_RIGHT", 2.5)
_set_cost("FOLLOW", "STOP", 4.0)

# Preferences from STOP
_set_cost("STOP", "CRUISE", 2.0)
_set_cost("STOP", "ACCELERATE", 1.5)

# Preferences from lane-change states
_set_cost("LANE_CHANGE_LEFT", "CRUISE", 2.0)
_set_cost("LANE_CHANGE_RIGHT", "CRUISE", 2.0)

# Preferences from ACCELERATE
_set_cost("ACCELERATE", "CRUISE", 1.5)
_set_cost("ACCELERATE", "FOLLOW", 3.0)
