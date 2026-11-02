"""Tests for finding serialization."""

from typing import Any, cast

import pytest

from agentic_devtools.cli.phase0_review.report import (
    Finding,
    ambiguity,
    malformed_input,
    missing_input,
    structural,
)


def test_all_template_finding_formats_use_json_literals():
    assert structural('expected "x"', "line\nmissing").serialize() == ('- [ ] "expected \\"x\\"": "line\\nmissing"')
    assert missing_input("issue.md", "absent").serialize() == ('- [ ] Missing input: "issue.md": "absent"')
    assert malformed_input("payload", "bad").serialize() == ('- [ ] Malformed input: "payload": "bad"')
    assert ambiguity("labels", "collision").serialize() == ('- [ ] Ambiguous source field "labels": "collision"')


def test_finding_rejects_unknown_section() -> None:
    with pytest.raises(ValueError, match="unsupported finding section"):
        Finding(cast(Any, "other"), "unexpected")
