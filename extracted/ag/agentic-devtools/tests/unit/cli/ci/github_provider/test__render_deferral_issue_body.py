"""Tests for _render_deferral_issue_body in the github_provider module."""

import json

import pytest

from agentic_devtools.cli.ci.github_provider import (
    _MAX_COMMENT_BODY_CHARS,
    SUPPRESSED_DEFERRAL_ISSUE_MARKER,
    _render_deferral_issue_body,
)


class TestRenderDeferralIssueBody:
    """Tests for the deferral issue body contract."""

    def test_marker_is_first_line_and_carries_payload(self) -> None:
        body = _render_deferral_issue_body(
            pr_number=11,
            review_id=42,
            base_sha="abc1234",
            findings=[("specs/3672/spec.md", "Ambiguous criteria.")],
        )

        first_line = body.splitlines()[0]
        assert first_line.startswith(SUPPRESSED_DEFERRAL_ISSUE_MARKER)
        payload = json.loads(first_line[len(SUPPRESSED_DEFERRAL_ISSUE_MARKER) :].rsplit(" -->", 1)[0])
        assert payload == {"pr": 11, "review_id": 42, "base_sha": "abc1234", "finding_count": 1}

    def test_renders_one_section_per_finding_in_order(self) -> None:
        body = _render_deferral_issue_body(
            pr_number=11,
            review_id=42,
            base_sha="abc1234",
            findings=[("specs/a.md", "First finding."), ("docs/b.md", "Second finding.")],
        )

        assert body.index("### Finding 1 — `specs/a.md`") < body.index("### Finding 2 — `docs/b.md`")
        assert "First finding." in body
        assert "Second finding." in body

    def test_embedded_fence_does_not_terminate_the_finding_fence(self) -> None:
        comment = "Broken example:\n```python\nprint('x')\n```"
        body = _render_deferral_issue_body(
            pr_number=11,
            review_id=42,
            base_sha="abc1234",
            findings=[("specs/a.md", comment)],
        )

        assert "````" in body
        assert comment in body

    def test_renders_without_findings(self) -> None:
        body = _render_deferral_issue_body(pr_number=11, review_id=42, base_sha="abc1234", findings=[])

        assert "### Finding" not in body
        assert body.endswith("\n")

    def test_raises_when_rendered_body_exceeds_github_limit(self) -> None:
        huge_finding = "x" * _MAX_COMMENT_BODY_CHARS
        with pytest.raises(RuntimeError, match="exceeds GitHub limit"):
            _render_deferral_issue_body(
                pr_number=11,
                review_id=42,
                base_sha="abc1234",
                findings=[("specs/a.md", huge_finding)],
            )
