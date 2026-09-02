"""Unknown-tool did-you-mean hints (executor.build_unknown_tool_hint).

An unregistered tool call used to return "Tool 'X' is not registered." with no
vocabulary — a dead end the model retried blindly. The hint now carries a
fuzzy did-you-mean (over registry + alias + projected names, wire-normalized)
plus a bounded, closest-first list of the active tools.
"""
from __future__ import annotations

from matrx_ai.tools.executor import build_unknown_tool_hint


class TestDidYouMean:
    def test_close_typo_single_confident_match(self) -> None:
        msg, action = build_unknown_tool_hint(
            "databse",
            vocabulary=["database", "web", "shell"],
            active_tools=["database", "web"],
        )
        assert "Tool 'databse' is not registered." in msg
        assert "Did you mean 'database'?" in msg
        assert action == "Retry with tool 'database'."

    def test_wire_called_name_matches_colon_internal(self) -> None:
        # The model only ever saw the wire spelling ('__'); the suggestion must
        # come back in wire form too — the only name the model can call.
        msg, action = build_unknown_tool_hint(
            "bundle__list_supabse",
            vocabulary=["bundle:list_supabase", "database"],
            active_tools=["bundle:list_supabase"],
        )
        assert "Did you mean 'bundle__list_supabase'?" in msg
        assert action == "Retry with tool 'bundle__list_supabase'."
        assert "bundle:list_supabase" not in msg  # never the colon spelling

    def test_no_match_points_at_available_list(self) -> None:
        msg, action = build_unknown_tool_hint(
            "zzzzzz",
            vocabulary=["database", "web", "shell"],
            active_tools=["database", "web", "shell"],
        )
        assert "Did you mean" not in msg
        assert "Available tools:" in msg
        assert action == "Pick a tool from the available list and retry with its exact name."

    def test_no_match_no_active_generic_action(self) -> None:
        msg, action = build_unknown_tool_hint("zzzzzz", vocabulary=[], active_tools=None)
        assert msg == "Tool 'zzzzzz' is not registered."
        assert "Check the tool name" in action


class TestActiveList:
    def test_active_list_is_bounded(self) -> None:
        many = [f"tool_{i:03d}" for i in range(100)]
        msg, _ = build_unknown_tool_hint(
            "tool_x", vocabulary=many, active_tools=many, cap=10
        )
        assert "(+90 more)" in msg
        # Bounded: cap(10) listed + up to 5 did-you-mean names — never all 100.
        assert sum(1 for n in many if n in msg) <= 15

    def test_active_list_closest_first(self) -> None:
        msg, _ = build_unknown_tool_hint(
            "workbok_edit",
            vocabulary=["alpha", "workbook_edit", "zeta"],
            active_tools=["alpha", "workbook_edit", "zeta"],
            cap=1,
        )
        # With cap=1 only the closest name survives the truncation.
        assert "Available tools: workbook_edit" in msg

    def test_active_list_in_wire_form(self) -> None:
        msg, _ = build_unknown_tool_hint(
            "zzzzzz",
            vocabulary=["scraper:scrape_page"],
            active_tools=["scraper:scrape_page"],
        )
        assert "scraper__scrape_page" in msg
        assert "scraper:scrape_page" not in msg

    def test_message_stays_single_line_prose(self) -> None:
        msg, _ = build_unknown_tool_hint(
            "databse", vocabulary=["database"], active_tools=["database"]
        )
        assert "\n" not in msg
