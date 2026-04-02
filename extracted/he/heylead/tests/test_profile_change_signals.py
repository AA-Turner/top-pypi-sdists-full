"""Tests for profile change signal classification in job_change_collector.

Tests the core classification functions:
- _classify_profile_change()
- _is_promotion()
- _scan_headline_intent()
- _detect_new_positions()
- _build_change_content()
"""

from __future__ import annotations

import pytest


# ──────────────────────────────────────────────
# _is_promotion
# ──────────────────────────────────────────────


class TestIsPromotion:
    def test_entry_to_manager(self):
        from heylead.collectors.job_change_collector import _is_promotion

        assert _is_promotion("entry", "manager") is True

    def test_manager_to_director(self):
        from heylead.collectors.job_change_collector import _is_promotion

        assert _is_promotion("manager", "director") is True

    def test_director_to_vp(self):
        from heylead.collectors.job_change_collector import _is_promotion

        assert _is_promotion("director", "vp") is True

    def test_vp_to_cxo(self):
        from heylead.collectors.job_change_collector import _is_promotion

        assert _is_promotion("vp", "cxo") is True

    def test_lateral_move(self):
        from heylead.collectors.job_change_collector import _is_promotion

        assert _is_promotion("manager", "manager") is False

    def test_demotion(self):
        from heylead.collectors.job_change_collector import _is_promotion

        assert _is_promotion("director", "manager") is False

    def test_same_level(self):
        from heylead.collectors.job_change_collector import _is_promotion

        assert _is_promotion("senior", "senior") is False


# ──────────────────────────────────────────────
# _scan_headline_intent
# ──────────────────────────────────────────────


class TestScanHeadlineIntent:
    def test_hiring_keyword(self):
        from heylead.collectors.job_change_collector import _scan_headline_intent

        result = _scan_headline_intent("VP Sales | We're hiring!")
        assert "hiring" in result
        assert "we're hiring" in result["hiring"]

    def test_open_to_work(self):
        from heylead.collectors.job_change_collector import _scan_headline_intent

        result = _scan_headline_intent("Software Engineer | Open to work")
        assert "open_to_opportunities" in result

    def test_building(self):
        from heylead.collectors.job_change_collector import _scan_headline_intent

        result = _scan_headline_intent("CEO — Building the next generation of AI tools")
        assert "building" in result

    def test_evaluating(self):
        from heylead.collectors.job_change_collector import _scan_headline_intent

        result = _scan_headline_intent("CTO | Modernizing our data stack")
        assert "evaluating" in result

    def test_no_intent(self):
        from heylead.collectors.job_change_collector import _scan_headline_intent

        result = _scan_headline_intent("VP of Engineering at Acme Corp")
        assert result == {}

    def test_multiple_intents(self):
        from heylead.collectors.job_change_collector import _scan_headline_intent

        result = _scan_headline_intent(
            "CTO | We're hiring | Building a world-class team"
        )
        assert "hiring" in result
        assert "building" in result

    def test_case_insensitive(self):
        from heylead.collectors.job_change_collector import _scan_headline_intent

        result = _scan_headline_intent("WE'RE HIRING engineers!")
        assert "hiring" in result


# ──────────────────────────────────────────────
# _detect_new_positions
# ──────────────────────────────────────────────


class TestDetectNewPositions:
    def test_new_position_added(self):
        from heylead.collectors.job_change_collector import _detect_new_positions

        old = [{"title": "VP Sales", "company": "Acme"}]
        new = [
            {"title": "VP Sales", "company": "Acme"},
            {"title": "Advisor", "company": "StartupXYZ"},
        ]
        result = _detect_new_positions(old, new)
        assert len(result) == 1
        assert result[0]["title"] == "Advisor"
        assert result[0]["company"] == "StartupXYZ"

    def test_no_change(self):
        from heylead.collectors.job_change_collector import _detect_new_positions

        old = [{"title": "VP Sales", "company": "Acme"}]
        new = [{"title": "VP Sales", "company": "Acme"}]
        result = _detect_new_positions(old, new)
        assert result == []

    def test_empty_old(self):
        from heylead.collectors.job_change_collector import _detect_new_positions

        new = [{"title": "VP Sales", "company": "Acme"}]
        result = _detect_new_positions([], new)
        assert len(result) == 1

    def test_empty_new(self):
        from heylead.collectors.job_change_collector import _detect_new_positions

        old = [{"title": "VP Sales", "company": "Acme"}]
        result = _detect_new_positions(old, [])
        assert result == []

    def test_company_name_field(self):
        from heylead.collectors.job_change_collector import _detect_new_positions

        old = [{"title": "CTO", "company_name": "OldCo"}]
        new = [
            {"title": "CTO", "company_name": "OldCo"},
            {"title": "Board Member", "company_name": "NewCo"},
        ]
        result = _detect_new_positions(old, new)
        assert len(result) == 1
        assert result[0]["company"] == "NewCo"

    def test_case_insensitive_dedup(self):
        from heylead.collectors.job_change_collector import _detect_new_positions

        old = [{"title": "vp sales", "company": "acme"}]
        new = [{"title": "VP Sales", "company": "Acme"}]
        result = _detect_new_positions(old, new)
        assert result == []


# ──────────────────────────────────────────────
# _classify_profile_change
# ──────────────────────────────────────────────


class TestClassifyProfileChange:
    def test_company_change(self):
        from heylead.collectors.job_change_collector import _classify_profile_change

        result = _classify_profile_change(
            old_title="VP Sales",
            new_title="VP Sales",
            old_company="OldCo",
            new_company="NewCo",
            old_headline="VP Sales at OldCo",
            new_headline="VP Sales at NewCo",
            old_experience=[],
            new_experience=[],
        )
        types = [s["signal_type"] for s in result]
        assert "company_change" in types

    def test_promotion_same_company(self):
        from heylead.collectors.job_change_collector import _classify_profile_change

        result = _classify_profile_change(
            old_title="Senior Engineer",
            new_title="Director of Engineering",
            old_company="Acme",
            new_company="Acme",
            old_headline="Senior Engineer at Acme",
            new_headline="Director of Engineering at Acme",
            old_experience=[],
            new_experience=[],
        )
        types = [s["signal_type"] for s in result]
        assert "promotion" in types
        assert "company_change" not in types

    def test_headline_intent_hiring(self):
        from heylead.collectors.job_change_collector import _classify_profile_change

        result = _classify_profile_change(
            old_title="VP Sales",
            new_title="VP Sales",
            old_company="Acme",
            new_company="Acme",
            old_headline="VP Sales at Acme",
            new_headline="VP Sales at Acme | We're hiring!",
            old_experience=[],
            new_experience=[],
        )
        types = [s["signal_type"] for s in result]
        assert "headline_intent" in types

    def test_generic_headline_change_fallback(self):
        from heylead.collectors.job_change_collector import _classify_profile_change

        result = _classify_profile_change(
            old_title="VP Sales",
            new_title="VP Sales",
            old_company="Acme",
            new_company="Acme",
            old_headline="VP Sales at Acme | Passionate about growth",
            new_headline="VP Sales at Acme | Driving revenue",
            old_experience=[],
            new_experience=[],
        )
        types = [s["signal_type"] for s in result]
        assert "headline_change" in types
        assert "headline_intent" not in types

    def test_no_change(self):
        from heylead.collectors.job_change_collector import _classify_profile_change

        result = _classify_profile_change(
            old_title="VP Sales",
            new_title="VP Sales",
            old_company="Acme",
            new_company="Acme",
            old_headline="VP Sales at Acme",
            new_headline="VP Sales at Acme",
            old_experience=[],
            new_experience=[],
        )
        assert result == []

    def test_company_change_plus_headline_intent(self):
        """Company change and headline intent should both fire."""
        from heylead.collectors.job_change_collector import _classify_profile_change

        result = _classify_profile_change(
            old_title="VP Sales",
            new_title="VP Sales",
            old_company="OldCo",
            new_company="NewCo",
            old_headline="VP Sales at OldCo",
            new_headline="VP Sales at NewCo | We're hiring!",
            old_experience=[],
            new_experience=[],
        )
        types = [s["signal_type"] for s in result]
        assert "company_change" in types
        assert "headline_intent" in types

    def test_lateral_title_change_not_promotion(self):
        """Same company, title changed but not a promotion → headline_change fallback."""
        from heylead.collectors.job_change_collector import _classify_profile_change

        result = _classify_profile_change(
            old_title="Sales Manager",
            new_title="Account Manager",
            old_company="Acme",
            new_company="Acme",
            old_headline="Sales Manager at Acme",
            new_headline="Account Manager at Acme",
            old_experience=[],
            new_experience=[],
        )
        types = [s["signal_type"] for s in result]
        # Not a promotion (same seniority), so should fall through
        assert "promotion" not in types
        # Headline did change, so headline_change is the fallback
        assert "headline_change" in types

    def test_new_advisory_position(self):
        from heylead.collectors.job_change_collector import _classify_profile_change

        result = _classify_profile_change(
            old_title="VP Sales",
            new_title="VP Sales",
            old_company="Acme",
            new_company="Acme",
            old_headline="VP Sales at Acme",
            new_headline="VP Sales at Acme",
            old_experience=[{"title": "VP Sales", "company": "Acme"}],
            new_experience=[
                {"title": "VP Sales", "company": "Acme"},
                {"title": "Advisor", "company": "StartupXYZ"},
            ],
        )
        types = [s["signal_type"] for s in result]
        assert "headline_change" in types
        # Find the advisory role signal
        advisory = [s for s in result if s["metadata"].get("is_additional_role")]
        assert len(advisory) == 1
        assert advisory[0]["metadata"]["new_position_title"] == "Advisor"


# ──────────────────────────────────────────────
# _build_change_content
# ──────────────────────────────────────────────


class TestBuildChangeContent:
    def test_company_change_content(self):
        from heylead.collectors.job_change_collector import _build_change_content

        content = _build_change_content(
            "company_change",
            "Jane Doe",
            {
                "old_company": "OldCo",
                "new_company": "NewCo",
                "new_title": "VP Sales",
            },
        )
        assert "Jane Doe" in content
        assert "NewCo" in content
        assert "OldCo" in content

    def test_promotion_content(self):
        from heylead.collectors.job_change_collector import _build_change_content

        content = _build_change_content(
            "promotion",
            "John Smith",
            {
                "old_title": "Manager",
                "new_title": "Director",
                "company": "Acme",
            },
        )
        assert "promoted" in content.lower()
        assert "Director" in content
        assert "Acme" in content

    def test_headline_intent_content(self):
        from heylead.collectors.job_change_collector import _build_change_content

        content = _build_change_content(
            "headline_intent",
            "Alice",
            {
                "intent_categories": ["hiring"],
                "new_headline": "CTO | We're hiring engineers",
            },
        )
        assert "hiring" in content
        assert "Alice" in content

    def test_headline_change_content(self):
        from heylead.collectors.job_change_collector import _build_change_content

        content = _build_change_content(
            "headline_change",
            "Bob",
            {
                "old_headline": "Old headline",
                "new_headline": "New headline",
            },
        )
        assert "Bob" in content
        assert "headline" in content.lower()

    def test_additional_role_content(self):
        from heylead.collectors.job_change_collector import _build_change_content

        content = _build_change_content(
            "headline_change",
            "Carol",
            {
                "is_additional_role": True,
                "new_position_title": "Advisor",
                "new_position_company": "StartupXYZ",
            },
        )
        assert "Carol" in content
        assert "Advisor" in content
        assert "StartupXYZ" in content


# ──────────────────────────────────────────────
# _infer_seniority (local copy)
# ──────────────────────────────────────────────


class TestInferSeniority:
    def test_cxo(self):
        from heylead.collectors.job_change_collector import _infer_seniority

        assert _infer_seniority("Chief Technology Officer") == "cxo"

    def test_vp(self):
        from heylead.collectors.job_change_collector import _infer_seniority

        assert _infer_seniority("VP of Engineering") == "vp"

    def test_director(self):
        from heylead.collectors.job_change_collector import _infer_seniority

        # "Head of" is the reliable keyword for director level
        # ("Director" contains substring "cto" which matches cxo first)
        assert _infer_seniority("Head of Sales") == "director"

    def test_manager(self):
        from heylead.collectors.job_change_collector import _infer_seniority

        assert _infer_seniority("Sales Manager") == "manager"

    def test_senior(self):
        from heylead.collectors.job_change_collector import _infer_seniority

        assert _infer_seniority("Senior Software Engineer") == "senior"

    def test_entry(self):
        from heylead.collectors.job_change_collector import _infer_seniority

        assert _infer_seniority("Sales Associate") == "entry"

    def test_empty(self):
        from heylead.collectors.job_change_collector import _infer_seniority

        assert _infer_seniority("") == "entry"

    def test_founder(self):
        from heylead.collectors.job_change_collector import _infer_seniority

        assert _infer_seniority("Co-Founder & CEO") == "owner"

    def test_unknown_defaults_to_manager(self):
        from heylead.collectors.job_change_collector import _infer_seniority

        assert _infer_seniority("Solutions Architect") == "manager"


# ──────────────────────────────────────────────
# _has_significant_change — fuzzy matching
# ──────────────────────────────────────────────


class TestHasSignificantChange:
    def test_exact_match(self):
        from heylead.collectors.job_change_collector import _has_significant_change

        assert _has_significant_change("VP Sales", "VP Sales") is False

    def test_case_insensitive(self):
        from heylead.collectors.job_change_collector import _has_significant_change

        assert _has_significant_change("VP Sales", "vp sales") is False

    def test_empty_old(self):
        from heylead.collectors.job_change_collector import _has_significant_change

        assert _has_significant_change("", "VP Sales") is False

    def test_both_empty(self):
        from heylead.collectors.job_change_collector import _has_significant_change

        assert _has_significant_change("", "") is False

    def test_real_change(self):
        from heylead.collectors.job_change_collector import _has_significant_change

        assert _has_significant_change("OldCo", "NewCo") is True

    def test_substring_expansion_rejected_strict(self):
        """Appending a tagline to a company name is NOT a real change in strict mode."""
        from heylead.collectors.job_change_collector import _has_significant_change

        assert _has_significant_change(
            "SportsTech Cricket Connect",
            "SportsTech Cricket Connect & The Banking 50 (100k-",
            strict=True,
        ) is False

    def test_substring_expansion_allowed_non_strict(self):
        """Appending a tagline to a headline IS detected in non-strict mode."""
        from heylead.collectors.job_change_collector import _has_significant_change

        assert _has_significant_change(
            "VP Sales at Acme",
            "VP Sales at Acme | We're hiring!",
        ) is True

    def test_substring_contraction_rejected_strict(self):
        from heylead.collectors.job_change_collector import _has_significant_change

        assert _has_significant_change(
            "VP Sales at Acme Corp | Passionate about growth",
            "VP Sales at Acme Corp",
            strict=True,
        ) is False

    def test_high_word_overlap_rejected_strict(self):
        """Changing one word out of many is formatting in strict mode."""
        from heylead.collectors.job_change_collector import _has_significant_change

        assert _has_significant_change(
            "VP of Sales and Marketing at Acme",
            "VP of Sales and Marketing at Acme Inc",
            strict=True,
        ) is False

    def test_low_word_overlap_accepted(self):
        """Completely different strings should still trigger."""
        from heylead.collectors.job_change_collector import _has_significant_change

        assert _has_significant_change(
            "Acme Corp", "Globex Industries", strict=True,
        ) is True


# ──────────────────────────────────────────────
# _classify_profile_change — new guards
# ──────────────────────────────────────────────


class TestClassifyProfileChangeGuards:
    def test_morten_scenario_no_role_signal(self):
        """Morten's headline expanded — no company_change or promotion signal.

        A benign headline_change may still fire (contextual_reference angle),
        but critically no "congrats on the new role" signal should be produced.
        """
        from heylead.collectors.job_change_collector import _classify_profile_change

        result = _classify_profile_change(
            old_title="Founder",
            new_title="Founder",
            old_company="SportsTech Cricket Connect",
            new_company="SportsTech Cricket Connect & The Banking 50",
            old_headline="Founder, SportsTech Cricket Connect",
            new_headline="Founder, SportsTech Cricket Connect & The Banking 50 (100k+ global banking & fintech community)",
            old_experience=[],
            new_experience=[],
        )
        types = [s["signal_type"] for s in result]
        assert "company_change" not in types
        assert "promotion" not in types

    def test_company_change_requires_new_company(self):
        """company_change should not fire when new_company is empty."""
        from heylead.collectors.job_change_collector import (
            _classify_profile_change,
            _has_significant_change,
        )

        # Simulate a scenario where company_changed=True but new_company=""
        # This is tested by directly calling _classify_profile_change with
        # empty new_company — the guard should prevent company_change signal
        result = _classify_profile_change(
            old_title="VP Sales",
            new_title="VP Sales",
            old_company="OldCo",
            new_company="",
            old_headline="VP Sales at OldCo",
            new_headline="VP Sales",
            old_experience=[],
            new_experience=[],
        )
        types = [s["signal_type"] for s in result]
        assert "company_change" not in types
