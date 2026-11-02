"""Tests for _resolve_repair_skills()."""

from agentic_devtools.cli.ci.github_provider import _resolve_repair_skills


class TestResolveRepairSkills:
    """Tests for mapping a repair type to its (agent, prompt) skill filenames."""

    def test_ci_returns_ci_repair_skills(self) -> None:
        agent, prompt = _resolve_repair_skills("ci")
        assert agent == "agdt.address-copilot-review.ci-repair.agent.md"
        assert prompt == "agdt.address-copilot-review.ci-repair.prompt.md"

    def test_review_returns_evaluate_and_respond_skills(self) -> None:
        agent, prompt = _resolve_repair_skills("review")
        assert agent == "agdt.address-copilot-review.evaluate-and-respond.agent.md"
        assert prompt == "agdt.address-copilot-review.evaluate-and-respond.prompt.md"

    def test_both_returns_evaluate_and_respond_skills(self) -> None:
        agent, prompt = _resolve_repair_skills("both")
        assert agent == "agdt.address-copilot-review.evaluate-and-respond.agent.md"
        assert prompt == "agdt.address-copilot-review.evaluate-and-respond.prompt.md"
