from abstra_internals.entities.agents.tools.click_strategy import ClickStrategyLearner


class TestClickStrategyLearner:
    def test_initial_strategies(self):
        learner = ClickStrategyLearner()
        assert learner.STRATEGIES == ["bbox", "text", "selector", "force", "js"]

    def test_record_result(self):
        learner = ClickStrategyLearner()
        learner.record_result("button", "bbox", True)
        assert learner.stats["button"]["bbox"]["success"] == 1
        assert learner.global_stats["bbox"]["success"] == 1

    def test_record_failure(self):
        learner = ClickStrategyLearner()
        learner.record_result("button", "bbox", False)
        assert learner.stats["button"]["bbox"]["failure"] == 1
        assert learner.global_stats["bbox"]["failure"] == 1

    def test_get_ordered_strategies_default(self):
        learner = ClickStrategyLearner()
        strategies = learner.get_ordered_strategies("button")
        assert len(strategies) == 5
        assert set(strategies) == set(learner.STRATEGIES)

    def test_get_ordered_strategies_by_success_rate(self):
        learner = ClickStrategyLearner()
        # Make "js" very successful for buttons
        for _ in range(5):
            learner.record_result("button", "js", True)
        # Make "bbox" fail for buttons
        for _ in range(5):
            learner.record_result("button", "bbox", False)
        strategies = learner.get_ordered_strategies("button")
        assert strategies[0] == "js"

    def test_filters_out_consistently_failing_strategies(self):
        learner = ClickStrategyLearner()
        # Make "force" fail consistently (>3 tries, <10% success)
        for _ in range(10):
            learner.record_result("button", "force", False)
        strategies = learner.get_ordered_strategies("button")
        assert "force" not in strategies

    def test_keeps_untried_strategies(self):
        learner = ClickStrategyLearner()
        learner.record_result("button", "bbox", True)
        strategies = learner.get_ordered_strategies("button")
        # Untried strategies (total < 3) should still be included
        assert len(strategies) == 5

    def test_per_element_type_tracking(self):
        learner = ClickStrategyLearner()
        for _ in range(5):
            learner.record_result("button", "js", True)
        for _ in range(5):
            learner.record_result("link", "text", True)
        button_order = learner.get_ordered_strategies("button")
        link_order = learner.get_ordered_strategies("link")
        assert button_order[0] == "js"
        assert link_order[0] == "text"

    def test_falls_back_to_global_stats(self):
        learner = ClickStrategyLearner()
        for _ in range(5):
            learner.record_result("button", "selector", True)
        # "div" has no per-element stats, should use global
        strategies = learner.get_ordered_strategies("div")
        assert strategies[0] == "selector"

    def test_returns_all_strategies_if_all_filtered(self):
        learner = ClickStrategyLearner()
        # Make everything fail heavily (> 3 tries, 0% success)
        for strategy in learner.STRATEGIES:
            for _ in range(5):
                learner.record_result("button", strategy, False)
        strategies = learner.get_ordered_strategies("button")
        # Should fall back to full list
        assert strategies == learner.STRATEGIES
