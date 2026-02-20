from abstra_internals.entities.agents.exploration_strategy import (
    BFSExplorationStrategy,
    ExplorationState,
)


class TestExplorationState:
    def test_state_hash_deterministic(self):
        s1 = ExplorationState("https://example.com", 50)
        s2 = ExplorationState("https://example.com", 50)
        assert s1.state_hash == s2.state_hash

    def test_different_urls_different_hash(self):
        s1 = ExplorationState("https://example.com/a", 50)
        s2 = ExplorationState("https://example.com/b", 50)
        assert s1.state_hash != s2.state_hash

    def test_different_element_count_different_hash(self):
        s1 = ExplorationState("https://example.com", 50)
        s2 = ExplorationState("https://example.com", 100)
        assert s1.state_hash != s2.state_hash

    def test_equality(self):
        s1 = ExplorationState("https://example.com", 50)
        s2 = ExplorationState("https://example.com", 50)
        assert s1 == s2

    def test_inequality(self):
        s1 = ExplorationState("https://example.com/a", 50)
        s2 = ExplorationState("https://example.com/b", 50)
        assert s1 != s2

    def test_hash_for_sets(self):
        s1 = ExplorationState("https://example.com", 50)
        s2 = ExplorationState("https://example.com", 50)
        assert hash(s1) == hash(s2)
        assert len({s1, s2}) == 1

    def test_not_equal_to_non_state(self):
        s = ExplorationState("https://example.com", 50)
        assert s != "not a state"

    def test_depth_stored(self):
        s = ExplorationState("https://example.com", 50, depth=3)
        assert s.depth == 3


class TestBFSExplorationStrategy:
    def test_initial_state(self):
        strategy = BFSExplorationStrategy()
        assert len(strategy.visited_states) == 0
        assert len(strategy.action_history) == 0
        assert strategy.current_depth == 0

    def test_record_state(self):
        strategy = BFSExplorationStrategy()
        state = strategy.record_state("https://example.com", 50)
        assert isinstance(state, ExplorationState)
        assert strategy.visited_states[state.state_hash] == 1

    def test_record_state_increments_count(self):
        strategy = BFSExplorationStrategy()
        state1 = strategy.record_state("https://example.com", 50)
        strategy.record_state("https://example.com", 50)
        assert strategy.visited_states[state1.state_hash] == 2

    def test_record_action(self):
        strategy = BFSExplorationStrategy()
        state = strategy.record_state("https://example.com", 50)
        strategy.record_action(state, "click", "5")
        assert len(strategy.action_history) == 1

    def test_consecutive_same_actions(self):
        strategy = BFSExplorationStrategy()
        state = strategy.record_state("https://example.com", 50)
        strategy.record_action(state, "click", "5")
        strategy.record_action(state, "click", "5")
        strategy.record_action(state, "click", "5")
        assert strategy.consecutive_same_actions == 3

    def test_consecutive_reset_on_different_action(self):
        strategy = BFSExplorationStrategy()
        state = strategy.record_state("https://example.com", 50)
        strategy.record_action(state, "click", "5")
        strategy.record_action(state, "click", "5")
        strategy.record_action(state, "navigate", "url")
        assert strategy.consecutive_same_actions == 1


class TestLoopDetection:
    def test_no_loop_initially(self):
        strategy = BFSExplorationStrategy()
        state = strategy.record_state("https://example.com", 50)
        assert not strategy.is_loop_detected(state)

    def test_loop_from_too_many_visits(self):
        strategy = BFSExplorationStrategy(max_same_state_visits=2)
        strategy.record_state("https://example.com", 50)
        state = strategy.record_state("https://example.com", 50)
        assert strategy.is_loop_detected(state)

    def test_loop_from_consecutive_actions(self):
        strategy = BFSExplorationStrategy()
        state = strategy.record_state("https://example.com", 50)
        for _ in range(3):
            strategy.record_action(state, "click", "5")
        assert strategy.is_loop_detected(state)


class TestGetUnexploredElements:
    def test_all_unexplored(self):
        strategy = BFSExplorationStrategy()
        state = strategy.record_state("https://example.com", 50)
        result = strategy.get_unexplored_elements(state, [1, 2, 3, 4, 5])
        assert result == [1, 2, 3, 4, 5]

    def test_explored_elements_moved_to_end(self):
        strategy = BFSExplorationStrategy()
        state = strategy.record_state("https://example.com", 50)
        strategy.record_action(state, "click", "2")
        strategy.record_action(state, "click", "4")
        result = strategy.get_unexplored_elements(state, [1, 2, 3, 4, 5])
        assert result == [1, 3, 5, 2, 4]

    def test_non_click_actions_not_counted(self):
        strategy = BFSExplorationStrategy()
        state = strategy.record_state("https://example.com", 50)
        strategy.record_action(state, "navigate", "2")
        result = strategy.get_unexplored_elements(state, [1, 2, 3])
        assert result == [1, 2, 3]


class TestShouldTryAlternativeApproach:
    def test_no_alternative_initially(self):
        strategy = BFSExplorationStrategy()
        assert not strategy.should_try_alternative_approach()

    def test_alternative_after_many_states(self):
        strategy = BFSExplorationStrategy()
        for i in range(11):
            strategy.record_state(f"https://example.com/page{i}", 50)
        assert strategy.should_try_alternative_approach()

    def test_alternative_after_many_actions(self):
        strategy = BFSExplorationStrategy()
        state = strategy.record_state("https://example.com", 50)
        for i in range(16):
            strategy.record_action(state, "click", str(i))
        assert strategy.should_try_alternative_approach()


class TestGetExplorationSummary:
    def test_summary_format(self):
        strategy = BFSExplorationStrategy()
        strategy.record_state("https://example.com", 50)
        state = strategy.record_state("https://other.com", 30)
        strategy.record_action(state, "click", "5")
        summary = strategy.get_exploration_summary()
        assert "1 actions" in summary
        assert "2 unique states" in summary
        assert "depth 0/5" in summary
