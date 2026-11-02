"""Tests for parsing the zero-findings CCR overview summary."""

from unittest.mock import patch

from agentic_devtools.cli.ci.critique_adjudicator import classify_critique_headline
from agentic_devtools.cli.github.ccr_headline import parse_ccr_overview_summary


def test_parses_critique_headline_and_no_open_issues() -> None:
    body = (
        "<!-- ccr-overview-v2 -->\n\n"
        "### 🔵 Needs a closer look\n\n"
        "Previously reported parser regressions remain unresolved and can lose findings or block promotion.\n\n"
        "**No open issues** 🎉"
    )

    assert parse_ccr_overview_summary(body) == (
        True,
        "Previously reported parser regressions remain unresolved and can lose findings or block promotion.",
    )


def test_parses_overview_marker_with_crlf_line_endings() -> None:
    body = (
        "<!-- ccr-overview-v2 -->\r\n"
        "### Needs a closer look\r\n\r\n"
        "A concrete parser regression remains.\r\n\r\n"
        "0 open findings"
    )

    assert parse_ccr_overview_summary(body) == (True, "A concrete parser regression remains.")


def test_parses_approval_headline_and_zero_open_findings() -> None:
    body = (
        "<!-- ccr-overview-v2 -->\n"
        "### ✅ Ready to approve\n\n"
        "This PR is ready to merge; it only needs human approval.\n\n"
        "0 open findings"
    )

    assert parse_ccr_overview_summary(body) == (True, "This PR is ready to merge; it only needs human approval.")


def test_heading_and_emoji_do_not_change_the_classified_headline() -> None:
    headline = "Broad modernization and limited baseline verification require final human review."
    bodies = (
        f"<!-- ccr-overview-v2 -->\n### 🔵 Needs a closer look\n\n{headline}\n\n0 open findings",
        f"<!-- ccr-overview-v2 -->\n### 🟡 Needs a closer look\n\n{headline}\n\n0 open findings",
    )

    parsed = [parse_ccr_overview_summary(body) for body in bodies]

    assert parsed == [(True, headline), (True, headline)]
    classifications = []
    with patch(
        "agentic_devtools.cli.ci.critique_adjudicator._run_single_adjudication",
        return_value='{"verdict":"approval_worthy"}',
    ) as run_adjudication:
        for result in parsed:
            assert result is not None
            parsed_headline = result[1]
            assert parsed_headline is not None
            classifications.append(classify_critique_headline(parsed_headline).verdict)

    assert classifications == ["approval_worthy", "approval_worthy"]
    assert run_adjudication.call_count == 2
    prompts = [call.args[0] for call in run_adjudication.call_args_list]
    assert prompts[0] == prompts[1]
    assert f'"headline":"{headline}"' in prompts[0]


def test_returns_zero_summary_without_headline_when_unparseable() -> None:
    body = "<!-- ccr-overview-v2 -->\n**No open issues** 🎉"

    assert parse_ccr_overview_summary(body) == (True, None)


def test_reports_nonzero_overview_as_not_zero() -> None:
    body = "<!-- ccr-overview-v2 -->\n### 🔵 Needs a closer look\n\nA concern remains.\n\n1 open finding"

    assert parse_ccr_overview_summary(body) == (False, "A concern remains.")


def test_ignores_bodies_without_overview_marker() -> None:
    assert parse_ccr_overview_summary("### Needs a closer look\n\nA concern remains.\n\n0 open findings") is None


def test_returns_none_for_empty_body() -> None:
    assert parse_ccr_overview_summary("") is None


def test_returns_zero_signal_when_heading_has_no_summary_sentence() -> None:
    assert parse_ccr_overview_summary("<!-- ccr-overview-v2 -->\n### Needs a closer look\n\n0 open findings") == (
        True,
        None,
    )


def test_joins_headline_lines_inside_the_same_paragraph() -> None:
    body = (
        "<!-- ccr-overview-v2 -->\n"
        "### Needs a closer look\n\n"
        "First line describes the work\n"
        "and this line completes the headline.\n\n"
        "0 open findings"
    )

    assert parse_ccr_overview_summary(body) == (
        True,
        "First line describes the work and this line completes the headline.",
    )


def test_removes_bold_wrapping_from_headline() -> None:
    body = (
        "<!-- ccr-overview-v2 -->\n"
        "### Needs a closer look\n\n"
        "**This PR is ready for human approval.**\n\n"
        "0 open findings"
    )

    assert parse_ccr_overview_summary(body) == (True, "This PR is ready for human approval.")


def test_returns_zero_summary_when_bold_headline_is_empty() -> None:
    body = "<!-- ccr-overview-v2 -->\n### Needs a closer look\n\n** **\n\n0 open findings"

    assert parse_ccr_overview_summary(body) == (True, None)


def test_does_not_treat_markup_after_heading_as_headline() -> None:
    body = "<!-- ccr-overview-v2 -->\n### Needs a closer look\n\n<span>summary</span>\n\n0 open findings"

    assert parse_ccr_overview_summary(body) == (True, None)


def test_zero_marker_cannot_become_the_headline() -> None:
    body = "<!-- ccr-overview-v2 -->\n### Needs a closer look\n\n0 open findings"

    assert parse_ccr_overview_summary(body) == (True, None)
