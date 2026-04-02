"""Tests for the ICP match scorer and composite lead scoring.

Verifies that:
1. compute_icp_match() scores prospects correctly against ICP criteria
2. Exclude-list items disqualify prospects (score → 0.0)
3. Unknown/missing data gets neutral scores (not penalized)
4. compute_composite_lead_score() combines all sub-scores correctly
"""

from __future__ import annotations

import json

from heylead.services.icp_match_scorer import (
    compute_icp_match,
    compute_composite_lead_score,
    _score_title_match,
    _score_industry_match,
    _score_seniority_match,
    _score_company_size,
    _score_location_match,
    _score_keyword_overlap,
    _parse_first_icp,
    _segment_to_icp,
    _get_segment_performance_score,
    UNKNOWN_SCORE,
)


# ── Test Data ──

SAMPLE_ICP_JSON = json.dumps({
    "icps": [{
        "name": "SaaS VP Sales",
        "job_titles": {
            "include": ["vp of sales", "head of sales", "sales director"],
            "exclude": ["sales associate", "intern"],
        },
        "industries": {
            "include": ["saas", "technology", "software"],
            "exclude": ["non-profit", "government"],
        },
        "seniority": {
            "include": ["vp", "director", "cxo"],
            "exclude": ["entry", "senior"],
        },
        "company_headcount": {"min": 51, "max": 500},
        "locations": {
            "include": ["united states", "united kingdom", "canada"],
            "exclude": [],
        },
        "keywords": ["b2b", "saas", "revenue", "pipeline", "quota"],
    }],
})


def _make_contact(**overrides) -> dict:
    """Create a test contact with defaults."""
    contact = {
        "id": "test-123",
        "title": "",
        "company": "",
        "location": "",
        "linkedin_id": "",
        "profile_json": "",
        "analysis_json": "",
        "estimated_revenue": 0,
    }
    contact.update(overrides)
    return contact


# ── ICP Parsing ──

def test_parse_first_icp_from_json_string():
    icp = _parse_first_icp(SAMPLE_ICP_JSON)
    assert icp is not None
    assert icp["name"] == "SaaS VP Sales"


def test_parse_first_icp_from_dict():
    data = json.loads(SAMPLE_ICP_JSON)
    icp = _parse_first_icp(data)
    assert icp is not None
    assert icp["name"] == "SaaS VP Sales"


def test_parse_first_icp_returns_none_for_empty():
    assert _parse_first_icp(None) is None
    assert _parse_first_icp("") is None
    assert _parse_first_icp("{}") is None


# ── Title Match ──

def test_title_exact_match():
    icp = _parse_first_icp(SAMPLE_ICP_JSON)
    assert _score_title_match("VP of Sales", icp) == 1.0


def test_title_partial_match():
    icp = _parse_first_icp(SAMPLE_ICP_JSON)
    score = _score_title_match("Regional Sales Manager", icp)
    assert 0.0 < score < 1.0  # "sales" overlaps but not exact


def test_title_exclude_disqualifies():
    icp = _parse_first_icp(SAMPLE_ICP_JSON)
    assert _score_title_match("Sales Associate", icp) == 0.0


def test_title_no_match():
    icp = _parse_first_icp(SAMPLE_ICP_JSON)
    score = _score_title_match("Software Engineer", icp)
    assert score <= 0.2  # Low score for no match


def test_title_unknown():
    icp = _parse_first_icp(SAMPLE_ICP_JSON)
    score = _score_title_match("", icp)
    assert score == UNKNOWN_SCORE


# ── Industry Match ──

def test_industry_exact_match():
    icp = _parse_first_icp(SAMPLE_ICP_JSON)
    contact = _make_contact(analysis_json=json.dumps({"industry": "saas"}))
    score = _score_industry_match(contact, icp, SAMPLE_ICP_JSON)
    assert score == 1.0


def test_industry_exclude_disqualifies():
    icp = _parse_first_icp(SAMPLE_ICP_JSON)
    contact = _make_contact(analysis_json=json.dumps({"industry": "non-profit"}))
    score = _score_industry_match(contact, icp, SAMPLE_ICP_JSON)
    assert score == 0.0


def test_industry_unknown():
    icp = _parse_first_icp(SAMPLE_ICP_JSON)
    contact = _make_contact()  # No industry data
    score = _score_industry_match(contact, icp, None)
    assert score == UNKNOWN_SCORE


# ── Seniority Match ──

def test_seniority_exact_match():
    icp = _parse_first_icp(SAMPLE_ICP_JSON)
    assert _score_seniority_match("VP of Engineering", icp) == 1.0


def test_seniority_adjacent_match():
    icp = _parse_first_icp(SAMPLE_ICP_JSON)
    # "manager" is one level below "director" in the hierarchy
    score = _score_seniority_match("Engineering Manager", icp)
    assert 0.3 < score < 0.8  # Adjacent = partial credit


def test_seniority_exclude_disqualifies():
    icp = _parse_first_icp(SAMPLE_ICP_JSON)
    # "entry" is in the exclude list
    assert _score_seniority_match("Junior Analyst", icp) == 0.0


# ── Company Size ──

def test_company_size_in_range():
    icp = _parse_first_icp(SAMPLE_ICP_JSON)
    contact = _make_contact(analysis_json=json.dumps({"headcount": 200}))
    score = _score_company_size(contact, icp, SAMPLE_ICP_JSON)
    assert score == 1.0


def test_company_size_out_of_range():
    icp = _parse_first_icp(SAMPLE_ICP_JSON)
    contact = _make_contact(analysis_json=json.dumps({"headcount": 50000}))
    score = _score_company_size(contact, icp, SAMPLE_ICP_JSON)
    assert score <= 0.2


def test_company_size_extended_range():
    icp = _parse_first_icp(SAMPLE_ICP_JSON)
    # 600 is outside 51-500 but within 2x (26-1000)
    contact = _make_contact(analysis_json=json.dumps({"headcount": 600}))
    score = _score_company_size(contact, icp, SAMPLE_ICP_JSON)
    assert score == 0.5


def test_company_size_unknown():
    icp = _parse_first_icp(SAMPLE_ICP_JSON)
    contact = _make_contact()  # No headcount data, no ICP fallback
    score = _score_company_size(contact, icp, None)
    assert score == UNKNOWN_SCORE


# ── Location Match ──

def test_location_match():
    icp = _parse_first_icp(SAMPLE_ICP_JSON)
    contact = _make_contact(location="San Francisco, United States")
    score = _score_location_match(contact, icp)
    assert score == 1.0


def test_location_no_match():
    icp = _parse_first_icp(SAMPLE_ICP_JSON)
    contact = _make_contact(location="Tokyo, Japan")
    score = _score_location_match(contact, icp)
    assert score == 0.2  # Has location but doesn't match


# ── Keyword Overlap ──

def test_keyword_full_overlap():
    icp = _parse_first_icp(SAMPLE_ICP_JSON)
    contact = _make_contact(
        title="VP Sales",
        company="B2B SaaS Revenue Platform",
        profile_json=json.dumps({"headline": "Driving pipeline and quota attainment"}),
    )
    score = _score_keyword_overlap(contact, icp)
    assert score >= 0.8  # Most keywords should match


def test_keyword_no_overlap():
    icp = _parse_first_icp(SAMPLE_ICP_JSON)
    contact = _make_contact(
        title="Nurse Practitioner",
        company="St. Joseph's Hospital",
    )
    score = _score_keyword_overlap(contact, icp)
    assert score == 0.0


def test_keyword_from_direct_headline():
    """Keywords should match against headline field directly (not just profile_json)."""
    icp = _parse_first_icp(SAMPLE_ICP_JSON)
    # Simulate a LinkedIn search result: headline at top level, no profile_json
    contact = _make_contact(
        title="CTO",
        company="TechCorp",
    )
    contact["headline"] = "CTO | B2B SaaS revenue pipeline leader"
    score = _score_keyword_overlap(contact, icp)
    assert score >= 0.4, f"Headline keywords should match, got {score}"


# ── Full ICP Match ──

def test_icp_match_perfect_prospect():
    contact = _make_contact(
        title="VP of Sales",
        company="TechCorp SaaS",
        location="New York, United States",
        analysis_json=json.dumps({"industry": "saas", "headcount": 150}),
        profile_json=json.dumps({"headline": "B2B SaaS revenue pipeline leader"}),
    )
    result = compute_icp_match(contact, SAMPLE_ICP_JSON)
    score = result["icp_match_score"]
    assert score >= 0.7, f"Perfect prospect should score >= 0.7, got {score}"
    assert "breakdown" in result


def test_icp_match_excluded_prospect():
    contact = _make_contact(
        title="Sales Associate",  # In exclude list
        company="Non-profit Foundation",
        analysis_json=json.dumps({"industry": "non-profit"}),  # In exclude list
    )
    result = compute_icp_match(contact, SAMPLE_ICP_JSON)
    score = result["icp_match_score"]
    assert score <= 0.15, f"Excluded prospect should score <= 0.15, got {score}"


def test_icp_match_no_icp_returns_neutral():
    contact = _make_contact(title="VP Sales", company="TechCorp")
    result = compute_icp_match(contact, None)
    assert result["icp_match_score"] == UNKNOWN_SCORE
    assert result["breakdown"] == {}


def test_icp_match_partial_data():
    """A prospect with title match but missing other data should still score decently."""
    contact = _make_contact(title="Head of Sales")  # Title matches
    result = compute_icp_match(contact, SAMPLE_ICP_JSON)
    score = result["icp_match_score"]
    # Should get credit for title match (0.30*1.0) + neutral for unknowns
    assert 0.3 < score < 0.7, f"Partial data prospect should be mid-range, got {score}"


# ── Segment Performance ──

def test_segment_performance_with_matching_pattern():
    contact = _make_contact(title="VP Sales", company="TechCorp")
    patterns = [{
        "pattern_key": "vp+techcorp",
        "confidence": 0.8,
        "sample_size": 30,
        "details_json": json.dumps({"acceptance_rate": 0.35}),
    }]
    score = _get_segment_performance_score(contact, patterns)
    assert score > 0.0
    assert score < 1.0


def test_segment_performance_cold_start():
    contact = _make_contact(title="VP Sales", company="TechCorp")
    score = _get_segment_performance_score(contact, None)
    assert score == 0.5  # Neutral on cold start


def test_segment_performance_no_match():
    contact = _make_contact(title="VP Sales", company="TechCorp")
    patterns = [{
        "pattern_key": "engineering+startup",
        "confidence": 0.8,
        "sample_size": 50,
        "details_json": json.dumps({"acceptance_rate": 0.40}),
    }]
    score = _get_segment_performance_score(contact, patterns)
    assert score == 0.5  # Falls back to neutral


# ── Composite Lead Score ──

def test_composite_score_basic():
    """Composite score should be between 0 and 1."""
    contact = _make_contact(
        title="VP of Sales",
        company="TechCorp SaaS",
        estimated_revenue=50000,
        analysis_json=json.dumps({"industry": "saas", "headcount": 150}),
    )
    score = compute_composite_lead_score(contact, SAMPLE_ICP_JSON)
    assert 0.0 <= score <= 1.0


def test_composite_score_high_revenue_boosts():
    """Higher revenue should produce a higher composite score."""
    low_rev = _make_contact(
        title="VP of Sales",
        estimated_revenue=5000,
        analysis_json=json.dumps({"industry": "saas"}),
    )
    high_rev = _make_contact(
        title="VP of Sales",
        estimated_revenue=80000,
        analysis_json=json.dumps({"industry": "saas"}),
    )
    low_score = compute_composite_lead_score(low_rev, SAMPLE_ICP_JSON)
    high_score = compute_composite_lead_score(high_rev, SAMPLE_ICP_JSON)
    assert high_score > low_score, (
        f"High revenue ({high_score}) should beat low revenue ({low_score})"
    )


def test_composite_score_empty_contact():
    """Empty contact should still produce a valid score."""
    contact = _make_contact()
    score = compute_composite_lead_score(contact, SAMPLE_ICP_JSON)
    assert 0.0 <= score <= 1.0


# ── Segment Format Parsing ──

SAMPLE_SEGMENT_ICP_JSON = json.dumps({
    "segments": [{
        "name": "SaaS VP Sales",
        "titles": ["vp of sales", "head of sales", "sales director"],
        "keywords": "b2b, saas, revenue, pipeline, quota",
        "industries": ["saas", "technology", "software"],
        "seniority": ["vp", "director", "cxo"],
        "locations": ["united states", "united kingdom"],
        "company_headcount": {"min": 51, "max": 500},
    }],
    "summary": "Target SaaS VP Sales",
    "campaign_name": "SaaS VP Sales",
})


def test_segment_to_icp_converts_correctly():
    """_segment_to_icp should convert segment fields to ICP dict format."""
    seg = json.loads(SAMPLE_SEGMENT_ICP_JSON)["segments"][0]
    icp = _segment_to_icp(seg)
    assert icp["job_titles"]["include"] == ["vp of sales", "head of sales", "sales director"]
    assert icp["job_titles"]["exclude"] == []
    assert icp["industries"]["include"] == ["saas", "technology", "software"]
    assert icp["seniority"]["include"] == ["vp", "director", "cxo"]
    assert icp["locations"]["include"] == ["united states", "united kingdom"]
    assert icp["keywords"] == ["b2b", "saas", "revenue", "pipeline", "quota"]
    assert icp["company_headcount"] == {"min": 51, "max": 500}


def test_segment_to_icp_handles_keyword_list():
    """_segment_to_icp should handle keywords as list (not just string)."""
    seg = {"titles": [], "keywords": ["b2b", "saas"]}
    icp = _segment_to_icp(seg)
    assert icp["keywords"] == ["b2b", "saas"]


def test_parse_first_icp_from_segments():
    """_parse_first_icp should parse legacy segments format."""
    icp = _parse_first_icp(SAMPLE_SEGMENT_ICP_JSON)
    assert icp is not None
    assert "job_titles" in icp
    assert icp["job_titles"]["include"] == ["vp of sales", "head of sales", "sales director"]


def test_parse_first_icp_from_segments_dict():
    """_parse_first_icp should parse segments format from dict (not just string)."""
    data = json.loads(SAMPLE_SEGMENT_ICP_JSON)
    icp = _parse_first_icp(data)
    assert icp is not None
    assert "job_titles" in icp


def test_icp_match_with_segments_format_matching():
    """compute_icp_match should score well with segments-format ICP for matching prospect."""
    contact = _make_contact(
        title="VP of Sales",
        company="TechCorp SaaS",
        location="New York, United States",
        analysis_json=json.dumps({"industry": "saas", "headcount": 150}),
        profile_json=json.dumps({"headline": "B2B SaaS revenue pipeline leader"}),
    )
    result = compute_icp_match(contact, SAMPLE_SEGMENT_ICP_JSON)
    score = result["icp_match_score"]
    assert score >= 0.7, f"Perfect prospect (segments format) should score >= 0.7, got {score}"


def test_icp_match_with_segments_format_mismatched():
    """compute_icp_match should score low with segments-format ICP for mismatched prospect."""
    contact = _make_contact(
        title="Recruitment Consultant",
        company="Staffing Agency",
    )
    result = compute_icp_match(contact, SAMPLE_SEGMENT_ICP_JSON)
    score = result["icp_match_score"]
    assert score < 0.4, f"Mismatched prospect (segments format) should score < 0.4, got {score}"


def test_icp_match_segments_vs_icps_comparable():
    """Scores from segments format should be comparable to scores from icps format."""
    contact = _make_contact(
        title="VP of Sales",
        company="TechCorp SaaS",
        location="New York, United States",
        analysis_json=json.dumps({"industry": "saas", "headcount": 150}),
        profile_json=json.dumps({"headline": "B2B SaaS revenue pipeline leader"}),
    )
    icps_score = compute_icp_match(contact, SAMPLE_ICP_JSON)["icp_match_score"]
    segments_score = compute_icp_match(contact, SAMPLE_SEGMENT_ICP_JSON)["icp_match_score"]
    # Both should be high for matching prospect; allow some variance since
    # segments format lacks exclude lists
    assert abs(icps_score - segments_score) < 0.2, (
        f"Scores should be comparable: icps={icps_score}, segments={segments_score}"
    )
