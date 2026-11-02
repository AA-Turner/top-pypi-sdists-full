"""Tests for the critique repair task prompt contract."""

import pytest

from agentic_devtools.cli.ci.critique_adjudicator import build_critique_repair_prompt


def test_preserves_the_exact_agent_task_prompt() -> None:
    prompt = "@copilot please address the following critique of this pr:\n\nA parser regression remains.\n"

    assert build_critique_repair_prompt(prompt) == prompt


@pytest.mark.parametrize("prompt", ["", "  "])
def test_rejects_empty_prompt(prompt: str) -> None:
    with pytest.raises(ValueError, match="non-empty"):
        build_critique_repair_prompt(prompt)
