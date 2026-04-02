"""Tests for signal-specific message strategy builder.

Verifies that:
1. _build_signal_strategy() returns correct strategy for each category
2. _build_signal_strategy() returns empty string when no signal context
3. _enrich_trigger_info() prepends signal hook to campaign trigger
4. _format_analysis_section() handles signal_context section
5. build_context_block() includes signal_strategy in output
"""

from __future__ import annotations

from heylead.ai.prompt_loader import (
    _build_signal_strategy,
    _enrich_trigger_info,
    _format_analysis_section,
    _ANGLE_TO_CATEGORY,
    _STRATEGY_TEMPLATES,
    build_context_block,
)


# ── Test Data ──

SIGNAL_CONTEXT_CONGRATS = {
    "signal_type": "company_change",
    "signal_angle": "congrats_new_company",
    "engagement_hook": "Congrats on joining Acme!",
    "signal_summary": "John Doe moved from OldCo to Acme as VP Sales",
    "DO_NOT": "Don't quote their posts directly.",
    "pain_points": [],
    "keywords_matched": ["sales", "leadership"],
}

SIGNAL_CONTEXT_PAIN_POINT = {
    "signal_type": "keyword_mention",
    "signal_angle": "pain_point_alignment",
    "engagement_hook": "Noticed the conversation around outbound — it's a challenge many teams face",
    "signal_summary": "Posted about struggling with cold outreach at scale",
    "DO_NOT": "Don't quote their posts directly.",
    "pain_points": ["outreach scalability", "personalization"],
    "keywords_matched": ["cold outreach", "SDR"],
}

SIGNAL_CONTEXT_COMPETITIVE = {
    "signal_type": "competitor_mention",
    "signal_angle": "competitive_displacement",
    "engagement_hook": "Sounds like you're exploring alternatives to Salesloft",
    "signal_summary": "Mentioned frustration with Salesloft pricing",
    "DO_NOT": "Don't quote their posts directly.",
}

SIGNAL_CONTEXT_ENGAGEMENT = {
    "signal_type": "profile_view",
    "signal_angle": "icp_profile_viewer",
    "engagement_hook": "Noticed you checked us out — Acme seems like a great fit",
    "signal_summary": "Viewed profile, ICP match confirmed",
}

SIGNAL_CONTEXT_GROWTH = {
    "signal_type": "headline_intent",
    "signal_angle": "hiring_partnership",
    "engagement_hook": "Sounds like you're growing the team — exciting times!",
    "signal_summary": "Headline contains 'hiring' and 'growing team'",
}

SIGNAL_CONTEXT_EMPATHY = {
    "signal_type": "news_layoffs",
    "signal_angle": "empathy_restructuring",
    "engagement_hook": "Transitions can be tough — hope things settle well",
    "signal_summary": "Company announced layoffs",
}

ANALYSIS_WITH_SIGNAL = {
    "summary": "VP Sales at a mid-market SaaS company",
    "tone": {"recommended_approach": "direct", "formality_level": 5},
    "pain_points": ["scaling outbound"],
    "signal_context": SIGNAL_CONTEXT_CONGRATS,
}


# ── _build_signal_strategy() ──

def test_build_signal_strategy_congrats():
    analysis = {"signal_context": SIGNAL_CONTEXT_CONGRATS}
    result = _build_signal_strategy(analysis)
    assert "MILESTONE / CONGRATS" in result
    assert "Congrats on joining Acme!" in result
    assert "Don't quote" in result


def test_build_signal_strategy_pain_point():
    analysis = {"signal_context": SIGNAL_CONTEXT_PAIN_POINT}
    result = _build_signal_strategy(analysis)
    assert "PAIN POINT / BUYING INTENT" in result
    assert "outbound" in result


def test_build_signal_strategy_competitive():
    analysis = {"signal_context": SIGNAL_CONTEXT_COMPETITIVE}
    result = _build_signal_strategy(analysis)
    assert "COMPETITIVE DISPLACEMENT" in result
    assert "Salesloft" in result  # engagement hook passed through


def test_build_signal_strategy_engagement():
    analysis = {"signal_context": SIGNAL_CONTEXT_ENGAGEMENT}
    result = _build_signal_strategy(analysis)
    assert "SHARED ENGAGEMENT" in result


def test_build_signal_strategy_growth():
    analysis = {"signal_context": SIGNAL_CONTEXT_GROWTH}
    result = _build_signal_strategy(analysis)
    assert "GROWTH / HIRING" in result


def test_build_signal_strategy_empathy():
    analysis = {"signal_context": SIGNAL_CONTEXT_EMPATHY}
    result = _build_signal_strategy(analysis)
    assert "EMPATHY / TRANSITION" in result


def test_build_signal_strategy_no_analysis():
    assert _build_signal_strategy(None) == ""


def test_build_signal_strategy_no_signal_context():
    assert _build_signal_strategy({"tone": {}}) == ""


def test_build_signal_strategy_empty_angle():
    analysis = {"signal_context": {"signal_angle": ""}}
    assert _build_signal_strategy(analysis) == ""


def test_build_signal_strategy_unknown_angle():
    analysis = {"signal_context": {"signal_angle": "some_unknown_angle"}}
    assert _build_signal_strategy(analysis) == ""


# ── Verify all angles map to a category ──

def test_all_categories_have_templates():
    categories = set(_ANGLE_TO_CATEGORY.values())
    for cat in categories:
        assert cat in _STRATEGY_TEMPLATES, f"Category {cat} has no template"


# ── _enrich_trigger_info() ──

def test_enrich_trigger_info_with_signal():
    result = _enrich_trigger_info("Campaign target description", ANALYSIS_WITH_SIGNAL)
    assert "Congrats on joining Acme!" in result
    assert "Campaign context:" in result
    assert "Campaign target description" in result


def test_enrich_trigger_info_no_analysis():
    result = _enrich_trigger_info("Base trigger", None)
    assert result == "Base trigger"


def test_enrich_trigger_info_no_signal_context():
    result = _enrich_trigger_info("Base trigger", {"tone": {}})
    assert result == "Base trigger"


def test_enrich_trigger_info_no_base():
    analysis = {"signal_context": {"engagement_hook": "Great timing!"}}
    result = _enrich_trigger_info("", analysis)
    assert result == "Great timing!"


# ── _format_analysis_section() for signal_context ──

def test_format_analysis_section_signal_context():
    result = _format_analysis_section(ANALYSIS_WITH_SIGNAL, "signal_context")
    assert "Signal: company_change" in result
    assert "Angle: congrats new company" in result
    assert "Hook: Congrats on joining Acme!" in result


def test_format_analysis_section_signal_context_empty():
    result = _format_analysis_section({"signal_context": {}}, "signal_context")
    assert result == ""


# ── build_context_block() integration ──

def test_build_context_block_includes_signal_strategy():
    sender = {"name": "Test User", "title": "Founder", "company": "TestCo"}
    prospect = {"name": "John Doe", "title": "VP Sales", "company": "Acme"}
    campaign_config = {"relevance_hook": "Sales leaders", "target_description": "VP Sales"}
    voice = {"tone": "Direct", "sentence_length": "Short"}

    result = build_context_block(
        sender=sender,
        prospect=prospect,
        campaign_config=campaign_config,
        voice=voice,
        analysis=ANALYSIS_WITH_SIGNAL,
    )

    assert "signal_strategy" in result
    assert "MILESTONE / CONGRATS" in result["signal_strategy"]
    # trigger_info should be enriched with signal hook
    assert "Congrats on joining Acme!" in result["trigger_info"]


def test_build_context_block_no_signal():
    sender = {"name": "Test User", "title": "Founder", "company": "TestCo"}
    prospect = {"name": "John Doe", "title": "VP Sales", "company": "Acme"}
    campaign_config = {"relevance_hook": "Sales leaders"}
    voice = {"tone": "Direct"}

    result = build_context_block(
        sender=sender,
        prospect=prospect,
        campaign_config=campaign_config,
        voice=voice,
        analysis=None,
    )

    assert result["signal_strategy"] == ""
    assert result["trigger_info"] == "Sales leaders"
