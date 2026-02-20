import hashlib
from typing import Dict, List, Optional, Tuple


class ExplorationState:
    def __init__(self, url: str, element_count: int, depth: int = 0) -> None:
        self.url = url
        self.element_count = element_count
        self.depth = depth
        self.state_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        state_str = f"{self.url}:{self.element_count}"
        return hashlib.md5(state_str.encode()).hexdigest()[:16]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExplorationState):
            return NotImplemented
        return self.state_hash == other.state_hash

    def __hash__(self) -> int:
        return hash(self.state_hash)


class BFSExplorationStrategy:
    def __init__(self, max_depth: int = 5, max_same_state_visits: int = 2) -> None:
        self.max_depth = max_depth
        self.max_same_state_visits = max_same_state_visits
        self.visited_states: Dict[str, int] = {}
        self.action_history: List[Tuple[str, str, str]] = []
        self.consecutive_same_actions = 0
        self.last_action: Optional[Tuple[str, str]] = None
        self.current_depth = 0

    def record_state(self, url: str, element_count: int) -> ExplorationState:
        state = ExplorationState(url, element_count, self.current_depth)
        if state.state_hash not in self.visited_states:
            self.visited_states[state.state_hash] = 0
        self.visited_states[state.state_hash] += 1
        return state

    def record_action(
        self, state: ExplorationState, action: str, action_input: str
    ) -> None:
        self.action_history.append((state.state_hash, action, action_input))
        current_action = (action, action_input)
        if current_action == self.last_action:
            self.consecutive_same_actions += 1
        else:
            self.consecutive_same_actions = 1
            self.last_action = current_action

    def is_loop_detected(self, state: ExplorationState) -> bool:
        if self.visited_states.get(state.state_hash, 0) >= self.max_same_state_visits:
            return True
        if self.consecutive_same_actions >= 3:
            return True
        return False

    def get_unexplored_elements(
        self, state: ExplorationState, available_elements: List[int]
    ) -> List[int]:
        tried_elements = set()
        for hist_state, action, action_input in self.action_history:
            if hist_state == state.state_hash and action == "click":
                try:
                    tried_elements.add(int(action_input))
                except ValueError:
                    pass
        unexplored = [e for e in available_elements if e not in tried_elements]
        explored = [e for e in available_elements if e in tried_elements]
        return unexplored + explored

    def should_try_alternative_approach(self) -> bool:
        if len(self.visited_states) > 10 and self.current_depth == 0:
            return True
        if len(self.action_history) > 15:
            return True
        return False

    def get_exploration_summary(self) -> str:
        unique_states = len(self.visited_states)
        total_actions = len(self.action_history)
        return (
            f"Exploration: {total_actions} actions, "
            f"{unique_states} unique states, "
            f"depth {self.current_depth}/{self.max_depth}"
        )
