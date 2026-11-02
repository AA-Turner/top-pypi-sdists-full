"""Tests for extract_job_id()."""

from agentic_devtools.cli.ci.job_logs import extract_job_id


class TestExtractJobId:
    """Tests for parsing the trailing /job/<id> from a check-run html_url."""

    def test_actions_job_url_returns_job_id(self) -> None:
        url = "https://github.com/owner/repo/actions/runs/28005239943/job/82885697587"
        assert extract_job_id(url) == 82885697587

    def test_codeql_code_scanning_url_returns_none(self) -> None:
        url = "https://github.com/owner/repo/security/code-scanning/42?ref=refs/pull/1/head"
        assert extract_job_id(url) is None

    def test_url_without_job_segment_returns_none(self) -> None:
        url = "https://github.com/owner/repo/actions/runs/28005239943"
        assert extract_job_id(url) is None

    def test_empty_url_returns_none(self) -> None:
        assert extract_job_id("") is None

    def test_single_digit_job_id(self) -> None:
        assert extract_job_id("https://github.com/o/r/actions/runs/1/job/7") == 7
