"""Tests for Perplexity-style features in sage.

Maps Perplexity's core capabilities to sage primitives:

  Perplexity capability      → Sage primitive
  -----------------------     -----------------------------------------
  Web search w/ citations    → SEARCH_WEB / WEB_FETCH + citation tracker
  Focus modes (academic,     → /focus <mode> selecting prompt + model
    writing, math, code)
  Pro Search (multi-step)    → MultiModelOrchestrator with research plan
  Source attribution         → SourceList collected across the conversation
  Spaces (project context)   → Already covered by .sage/memory/ (D13)
"""

from __future__ import annotations

import pytest


# ── Citation tracking ─────────────────────────────────────────────────


class TestCitationTracker:

    def test_extract_citations_from_response(self):
        from sage.core.perplexity import CitationTracker
        text = (
            "React's hooks were introduced in v16.8 "
            "(https://react.dev/blog/2019/02/06/react-v16.8.0.html). "
            "For accessibility, see https://www.w3.org/WAI/standards-guidelines/wcag/."
        )
        tracker = CitationTracker()
        tracker.ingest(text)
        cites = tracker.citations()
        assert len(cites) == 2
        urls = {c.url for c in cites}
        assert "https://react.dev/blog/2019/02/06/react-v16.8.0.html" in urls
        assert "https://www.w3.org/WAI/standards-guidelines/wcag/" in urls

    def test_render_for_prompt(self):
        from sage.core.perplexity import CitationTracker
        tracker = CitationTracker()
        tracker.ingest("See https://example.org/a and https://example.org/b for details.")
        rendered = tracker.render_for_prompt()
        assert "[1]" in rendered
        assert "[2]" in rendered
        assert "example.org/a" in rendered

    def test_deduplicates_urls(self):
        from sage.core.perplexity import CitationTracker
        tracker = CitationTracker()
        tracker.ingest("See https://x.com/a and https://x.com/a again.")
        assert len(tracker.citations()) == 1


# ── Focus modes ───────────────────────────────────────────────────────


class TestFocusModes:

    def test_default_focus_is_general(self):
        from sage.core.perplexity import FocusMode, get_focus_config
        cfg = get_focus_config(FocusMode.GENERAL)
        assert cfg.name == "general"
        assert len(cfg.system_prompt) > 50

    def test_academic_focus_emphasizes_citations(self):
        from sage.core.perplexity import FocusMode, get_focus_config
        cfg = get_focus_config(FocusMode.ACADEMIC)
        assert "citation" in cfg.system_prompt.lower() or "cite" in cfg.system_prompt.lower()

    def test_code_focus_emphasizes_implementation(self):
        from sage.core.perplexity import FocusMode, get_focus_config
        cfg = get_focus_config(FocusMode.CODE)
        assert "code" in cfg.system_prompt.lower()
        assert "complete" in cfg.system_prompt.lower() or "no placeholder" in cfg.system_prompt.lower()

    def test_math_focus_steps_through_reasoning(self):
        from sage.core.perplexity import FocusMode, get_focus_config
        cfg = get_focus_config(FocusMode.MATH)
        body = cfg.system_prompt.lower()
        assert "step" in body and ("show your work" in body or "reasoning" in body)

    def test_writing_focus_targets_polish(self):
        from sage.core.perplexity import FocusMode, get_focus_config
        cfg = get_focus_config(FocusMode.WRITING)
        body = cfg.system_prompt.lower()
        # Writing mode should emphasize style/tone/clarity
        assert any(k in body for k in ("style", "tone", "voice", "clarity", "concise"))

    def test_each_mode_picks_an_appropriate_model_tier(self):
        from sage.core.perplexity import FocusMode, get_focus_config
        # General + writing → medium models OK
        # Math + academic + code → prefer big
        assert get_focus_config(FocusMode.MATH).preferred_tier in ("big", "medium")
        assert get_focus_config(FocusMode.ACADEMIC).preferred_tier in ("big", "medium")
        assert get_focus_config(FocusMode.CODE).preferred_tier in ("big", "medium")


# ── Pro Search: multi-step research ───────────────────────────────────


class TestProSearch:

    def test_pro_search_returns_research_plan(self):
        from sage.core.perplexity import build_research_plan
        plan = build_research_plan(
            question="What are the tradeoffs of GraphQL vs REST?",
        )
        assert len(plan.steps) >= 3
        # Plan should include at least one search step
        kinds = {s.kind for s in plan.steps}
        assert "search" in kinds

    def test_pro_search_includes_synthesis_step(self):
        from sage.core.perplexity import build_research_plan
        plan = build_research_plan(question="How does WebAssembly compare to JavaScript for performance?")
        kinds = [s.kind for s in plan.steps]
        # Last step should synthesize across earlier findings
        assert kinds[-1] == "synthesis"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
