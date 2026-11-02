"""Tests for build_critique_prompt."""

from agentic_devtools.cli.azure_devops.pr_review_ducks import build_critique_prompt


class TestBuildCritiquePrompt:
    def test_subagent_with_draft(self):
        prompt = build_critique_prompt(
            layer="subagent",
            author_model="claude-opus-4.6",
            file_key="src-a-ts-deadbeef",
            draft_path="/tmp/draft.json",
        )
        assert "layer `subagent`" in prompt
        assert "src-a-ts-deadbeef" in prompt
        assert "claude-opus-4.6" in prompt
        assert "/tmp/draft.json" in prompt
        assert "one of the critics" in prompt
        assert "accept" in prompt and "reject" in prompt and "partial" in prompt
        assert "reviewer.rubberDucks" in prompt
        # Subagent context includes the file prompt line.
        assert "file prompt" in prompt
        # Orchestrator-only instructions must not leak into the duck-facing prompt.
        assert "you (the orchestrator)" not in prompt.lower()
        assert "Spawn one rubber-duck subagent" not in prompt

    def test_main_agent_no_draft_no_key(self):
        prompt = build_critique_prompt(
            layer="mainAgent",
            author_model=None,
            file_key=None,
            draft_path=None,
        )
        assert "layer `mainAgent`" in prompt
        assert "orchestrator's own work" in prompt
        assert "unspecified model" in prompt
        assert "included inline" in prompt
        assert "do **not** spawn" in prompt
        # orchestrator-level work has no file prompt; only cluster context is mentioned.
        assert "file prompt" not in prompt
        assert "cluster context" in prompt
