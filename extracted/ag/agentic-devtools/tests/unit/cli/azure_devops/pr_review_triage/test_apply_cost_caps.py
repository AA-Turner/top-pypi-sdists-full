"""Tests for apply_cost_caps (and the _risk_score helper)."""

from agentic_devtools.cli.azure_devops.pr_review_triage import _risk_score, apply_cost_caps


def _entry(key, depth, reasons, changed):
    return {"fileKey": key, "depth": depth, "reasons": reasons, "changedLines": changed}


_NO_CAPS = {"maxDeepModelCalls": 10_000, "maxDeepTotalChangedLines": 10_000, "maxReviewMinutes": 10_000}


class TestApplyCostCaps:
    def test_no_demotion_within_caps(self):
        entries = [_entry("a", "deep", ["force-deep:glob"], 10)]
        out, demotions = apply_cost_caps(entries, _NO_CAPS)
        assert demotions == []
        assert out[0]["depth"] == "deep"
        # Input is not mutated.
        assert entries[0]["depth"] == "deep"

    def test_demote_on_model_calls(self):
        entries = [_entry(f"f{i}", "deep", ["default:deep"], 1) for i in range(5)]
        config = {**_NO_CAPS, "maxDeepModelCalls": 6}
        out, demotions = apply_cost_caps(entries, config)
        deep = [e for e in out if e["depth"] == "deep"]
        assert len(deep) == 2
        assert len(demotions) == 3
        assert demotions[0]["reason"] == "cost-cap"

    def test_demote_on_changed_lines_lowest_risk_first(self):
        entries = [
            _entry("low", "deep", ["default:deep"], 1500),
            _entry("high", "deep", ["force-deep:glob"], 1500),
        ]
        config = {**_NO_CAPS, "maxDeepTotalChangedLines": 2000}
        out, demotions = apply_cost_caps(entries, config)
        deep = {e["fileKey"] for e in out if e["depth"] == "deep"}
        assert deep == {"high"}
        assert demotions[0]["fileKey"] == "low"

    def test_demote_on_minutes(self):
        entries = [_entry(f"f{i}", "deep", ["default:deep"], 1) for i in range(7)]
        config = {**_NO_CAPS, "maxReviewMinutes": 60}
        out, demotions = apply_cost_caps(entries, config)
        assert len(demotions) == 2

    def test_over_budget_but_no_deep_left(self):
        entries = [_entry("a", "light", ["force-light:glob"], 1)]
        config = {**_NO_CAPS, "maxReviewMinutes": 1}
        out, demotions = apply_cost_caps(entries, config)
        assert demotions == []
        assert out[0]["depth"] == "light"

    def test_demote_marks_reason(self):
        entries = [_entry("a", "deep", ["default:deep"], 1), _entry("b", "deep", ["default:deep"], 1)]
        config = {**_NO_CAPS, "maxDeepModelCalls": 3}
        out, _demotions = apply_cost_caps(entries, config)
        demoted = [e for e in out if e["depth"] == "light"]
        assert demoted[0]["reasons"][-1] == "demoted:cost-cap"


class TestRiskScore:
    def test_known_reason(self):
        assert _risk_score(["force-deep:glob"]) == 100

    def test_unknown_reason(self):
        assert _risk_score(["mystery"]) == 0

    def test_empty_reasons(self):
        assert _risk_score([]) == 0
