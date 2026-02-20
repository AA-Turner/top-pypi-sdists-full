from abstra_internals.entities.agents.action_intelligence import ActionIntelligence


class TestGetPageSignature:
    def test_basic_signature(self):
        ai = ActionIntelligence()
        sig = ai.get_page_signature("https://example.com/dashboard", 100)
        assert isinstance(sig, str)
        assert len(sig) == 12

    def test_same_inputs_same_signature(self):
        ai = ActionIntelligence()
        sig1 = ai.get_page_signature("https://example.com/page", 50)
        sig2 = ai.get_page_signature("https://example.com/page", 50)
        assert sig1 == sig2

    def test_different_urls_different_signature(self):
        ai = ActionIntelligence()
        sig1 = ai.get_page_signature("https://example.com/page1", 50)
        sig2 = ai.get_page_signature("https://example.com/page2", 50)
        assert sig1 != sig2

    def test_numeric_path_segments_normalized(self):
        ai = ActionIntelligence()
        sig1 = ai.get_page_signature("https://example.com/users/123", 50)
        sig2 = ai.get_page_signature("https://example.com/users/456", 50)
        assert sig1 == sig2  # both 123 and 456 become {id}

    def test_element_count_bucketed(self):
        ai = ActionIntelligence()
        sig1 = ai.get_page_signature("https://example.com", 10)
        sig2 = ai.get_page_signature("https://example.com", 40)
        assert sig1 == sig2  # both bucket to 0

        sig3 = ai.get_page_signature("https://example.com", 60)
        assert sig1 != sig3  # 60 buckets to 50


class TestRecordOutcome:
    def test_record_single_outcome(self):
        ai = ActionIntelligence()
        ai.record_outcome("click", "5", "sig1", True, "Clicked button")
        assert len(ai.outcomes) == 1
        assert ai.action_stats["click"]["success"] == 1

    def test_record_failure(self):
        ai = ActionIntelligence()
        ai.record_outcome("click", "5", "sig1", False, "Error: not found")
        assert ai.action_stats["click"]["failure"] == 1
        assert ai.action_stats["click"]["success"] == 0

    def test_successful_sequence_tracking(self):
        ai = ActionIntelligence()
        ai.record_outcome("navigate", "url", "sig1", True, "ok")
        ai.record_outcome("click", "5", "sig1", True, "clicked")
        assert ("navigate", "click") in ai.successful_sequences

    def test_no_sequence_after_failure(self):
        ai = ActionIntelligence()
        ai.record_outcome("navigate", "url", "sig1", False, "error")
        ai.record_outcome("click", "5", "sig1", True, "clicked")
        assert len(ai.successful_sequences) == 0

    def test_element_success_tracking(self):
        ai = ActionIntelligence()
        ai.record_outcome("click", "5", "sig1", True, "ok", element_type="button")
        assert "click" in ai.element_success["button"]

    def test_page_action_stats(self):
        ai = ActionIntelligence()
        ai.record_outcome("click", "5", "page_abc", True, "ok")
        ai.record_outcome("click", "6", "page_abc", False, "error")
        stats = ai.page_action_stats["page_abc"]["click"]
        assert stats["success"] == 1
        assert stats["failure"] == 1


class TestLoopDetection:
    def test_triple_repeat_detected(self):
        ai = ActionIntelligence()
        for _ in range(3):
            ai.record_outcome("click", "5", "sig", True, "ok")
        assert ai.loop_causing_actions["click"] > 0

    def test_alternating_pattern_detected(self):
        ai = ActionIntelligence()
        for _ in range(2):
            ai.record_outcome("click", "5", "sig", True, "ok")
            ai.record_outcome("navigate", "url", "sig", True, "ok")
        assert (
            ai.loop_causing_actions["click"] > 0
            or ai.loop_causing_actions["navigate"] > 0
        )


class TestPredictLoopRisk:
    def test_zero_risk_for_new_action(self):
        ai = ActionIntelligence()
        risk = ai.predict_loop_risk("click", "5", "sig1")
        assert risk == 0.0

    def test_high_risk_for_loop_causing_action(self):
        ai = ActionIntelligence()
        for _ in range(3):
            ai.record_outcome("click", "5", "sig1", True, "ok")
        risk = ai.predict_loop_risk("click", "5", "sig1")
        assert risk > 0.3

    def test_higher_risk_for_same_input_repeat(self):
        ai = ActionIntelligence()
        ai.record_outcome("click", "5", "sig1", True, "ok")
        risk = ai.predict_loop_risk("click", "5", "sig1")
        assert risk > 0.3  # same action + same input = high risk

    def test_risk_capped_at_one(self):
        ai = ActionIntelligence()
        # Create many loop-causing entries
        for _ in range(10):
            ai.record_outcome("click", "5", "sig1", True, "ok")
        risk = ai.predict_loop_risk("click", "5", "sig1")
        assert risk <= 1.0


class TestGetRecommendations:
    def test_no_outcomes_gives_exploring_message(self):
        ai = ActionIntelligence()
        advice = ai.get_recommendations("sig1")
        assert "exploring" in advice.reasoning.lower()

    def test_recommends_successful_actions(self):
        ai = ActionIntelligence()
        for _ in range(3):
            ai.record_outcome("extract_text", "{}", "sig1", True, "ok")
        advice = ai.get_recommendations("sig1")
        assert "extract_text" in advice.recommended_actions

    def test_avoids_failing_actions(self):
        ai = ActionIntelligence()
        for _ in range(3):
            ai.record_outcome("click", "5", "sig1", False, "error")
        advice = ai.get_recommendations("sig1")
        assert "click" in advice.actions_to_avoid

    def test_recommends_followup_actions(self):
        ai = ActionIntelligence()
        ai.record_outcome("navigate", "url", "sig1", True, "ok")
        ai.record_outcome("extract_text", "{}", "sig1", True, "ok")
        advice = ai.get_recommendations("sig1", last_action="navigate")
        assert "extract_text" in advice.recommended_actions


class TestWasActionSuccessful:
    def test_success_indicators(self):
        ai = ActionIntelligence()
        assert ai.was_action_successful("Successfully navigated to page")
        assert ai.was_action_successful("Clicked element, page loaded")
        assert ai.was_action_successful("Downloaded file completed")

    def test_failure_indicators(self):
        ai = ActionIntelligence()
        assert not ai.was_action_successful("Error: element not found")
        assert not ai.was_action_successful("Failed to click the button")
        assert not ai.was_action_successful("Timeout waiting for page")

    def test_stagnation_indicators(self):
        ai = ActionIntelligence()
        assert not ai.was_action_successful("same result as before")
        assert not ai.was_action_successful("no change detected")

    def test_code_execution_errors(self):
        ai = ActionIntelligence()
        assert not ai.was_action_successful(
            "Traceback (most recent call last)", action="run_javascript"
        )

    def test_neutral_output_defaults_to_success(self):
        ai = ActionIntelligence()
        # Normal page summary with no success/failure keywords
        assert ai.was_action_successful(
            'Page: "Dashboard" | URL: https://example.com\n'
            "Interactive Elements (25 total):"
        )

    def test_ambiguous_defaults_to_score(self):
        ai = ActionIntelligence()
        # Both success and failure indicators
        result = ai.was_action_successful("Found the element but error occurred")
        assert isinstance(result, bool)


class TestGetContextForPrompt:
    def test_empty_outcomes(self):
        ai = ActionIntelligence()
        assert ai.get_context_for_prompt() == ""

    def test_with_outcomes(self):
        ai = ActionIntelligence()
        ai.record_outcome("click", "5", "sig1", True, "ok")
        ai.record_outcome("navigate", "url", "sig1", False, "error")
        context = ai.get_context_for_prompt()
        assert "Action Intelligence" in context
        assert "1/2" in context  # 1 success out of 2
        assert "FAILED" in context  # last action failed

    def test_shows_working_actions(self):
        ai = ActionIntelligence()
        for _ in range(3):
            ai.record_outcome("extract_text", "{}", "sig1", True, "ok")
        context = ai.get_context_for_prompt()
        assert "Working well" in context
        assert "extract_text" in context

    def test_shows_loop_causing_actions(self):
        ai = ActionIntelligence()
        for _ in range(3):
            ai.record_outcome("click", "5", "sig1", True, "ok")
        context = ai.get_context_for_prompt()
        assert "Avoid" in context
        assert "click" in context
