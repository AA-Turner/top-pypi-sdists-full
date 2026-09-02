from matrx_scraper.seo_audit import PageEvidence, check_url_design_quality


def test_clean_url_receives_full_score() -> None:
    outcome = check_url_design_quality(PageEvidence(url="https://example.com/guides/seo-basics"))

    assert outcome.status == "pass"
    assert outcome.score == 100
    assert outcome.issue_count == 0


def test_catalogue_deductions_accumulate_once_per_rule() -> None:
    url = "https://example.com/Über_Long_Path/" + "x" * 90 + "?a=1&b=2&c=3&PHPSESSID=abc"

    outcome = check_url_design_quality(PageEvidence(url=url))

    assert outcome.status == "warn"
    assert outcome.score == 15
    assert outcome.issue_count == 6
    assert outcome.evidence == {
        "url_length": len(url),
        "parameter_count": 4,
        "has_uppercase": True,
        "has_underscores": True,
        "has_non_ascii": True,
        "session_params": ["phpsessid"],
    }


def test_repeated_session_parameter_only_takes_one_session_penalty() -> None:
    outcome = check_url_design_quality(PageEvidence(url="https://example.com/page?sid=one&sid=two"))

    assert outcome.score == 75
    assert outcome.issue_count == 1
    assert outcome.evidence["session_params"] == ["sid"]
