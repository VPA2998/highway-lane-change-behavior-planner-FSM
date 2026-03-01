"""
Finite State Machine core and behavior planner for highway lane-change.
"""

from typing import Any, Dict, List, Tuple

from .states import states, base_transition_cost


class SM:
    """Simple state machine pattern: start, step, transduce. [file:16]"""

    def __init__(self) -> None:
        self.startstate: Any = None
        self.state: Any = None

    def start(self) -> None:
        self.state = self.startstate

    def step(self, inp: Any) -> Any:
        new_state, output = self.getNextValue(self.state, inp)
        self.state = new_state
        return output

    def transduce(self, inputs: List[Any]) -> List[Any]:
        self.start()
        outputs: List[Any] = []
        for i in inputs:
            outputs.append(self.step(i))
        return outputs


SAFE_FOLLOW_DIST = 25.0
SAFE_LANECHANGE_DIST = 30.0


def traffic_penalty(
    current: str,
    nxt: str,
    d_same: float,
    d_left: float,
    d_right: float,
    lane_index: int | None,
) -> float:
    """
    Traffic-dependent penalty term added on top of the base transition cost. [file:16]
    """
    penalty = 0.0

    # Encourage STOP if extremely close
    if d_same < 5.0 and nxt != "STOP":
        penalty += 50.0

    # FOLLOW is good if there is a car within safe distance ahead
    if nxt == "FOLLOW":
        if d_same < SAFE_FOLLOW_DIST:
            penalty += 0.0
        else:
            penalty += 5.0  # no need to follow if no car ahead

    # CRUISE prefers clear road ahead
    if nxt == "CRUISE":
        if d_same < SAFE_FOLLOW_DIST:
            penalty += 10.0  # cruising too close is bad

    # ACCELERATE requires lots of space ahead
    if nxt == "ACCELERATE":
        if d_same < SAFE_FOLLOW_DIST:
            penalty += 20.0

    # Lane change left
    if nxt == "LANE_CHANGE_LEFT":
        # cannot change left from leftmost lane
        if lane_index is not None and lane_index == 0:
            penalty += 100.0
        # must have enough distance in left lane
        if d_left < SAFE_LANECHANGE_DIST:
            penalty += 30.0

    # Lane change right
    if nxt == "LANE_CHANGE_RIGHT":
        # cannot change right from rightmost lane
        if lane_index is not None and lane_index == 2:
            penalty += 100.0
        if d_right < SAFE_LANECHANGE_DIST:
            penalty += 30.0

    # Slight inertia penalty for changing state too often
    if nxt != current:
        penalty += 0.5

    return penalty


class BehaviorSM(SM):
    """
    Cost-based behavior state machine choosing the next state
    from the FSM state set, given distances and lane index. [file:16]
    """

    def __init__(self) -> None:
        super().__init__()
        self.startstate = "CRUISE"

    def getNextValue(self, state: str, inp: Dict[str, Any]) -> Tuple[str, str]:
        # inp is a dict with distances, lane index, and speed
        d_same = inp["d_same"]
        d_left = inp["d_left"]
        d_right = inp["d_right"]
        lane = inp["lane"]
        # speed is currently unused but kept for future extensions
        _speed = inp.get("speed", 0.0)

        best_state = state
        best_cost = float("inf")

        for nxt in states:
            base = base_transition_cost.get(state, {}).get(nxt, 10.0)
            pen = traffic_penalty(state, nxt, d_same, d_left, d_right, lane_index=lane)
            cost = base + pen
            if cost < best_cost:
                best_cost = cost
                best_state = nxt

        # output is chosen next_state
        return best_state, best_state
