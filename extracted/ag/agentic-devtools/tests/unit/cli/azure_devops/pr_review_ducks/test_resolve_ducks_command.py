"""Tests for resolve_ducks_command."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.azure_devops.pr_review_ducks import resolve_ducks_command
from agentic_devtools.cli.azure_devops.review_reviewer_models import AGENT_PICKS

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_ducks"


def _patches(argv, resolved):
    return (
        patch("sys.argv", argv),
        patch(f"{_MODULE}.load_pull_request_review_config", return_value=object()),
        patch(f"{_MODULE}.get_available_models", return_value=["gpt-5.3-codex", "gemini-3.1-pro-preview"]),
        patch(f"{_MODULE}.resolve_rubber_duck_models", return_value=resolved),
    )


class TestResolveDucksCommand:
    def test_models_to_stdout(self, capsys):
        argv = ["cmd", "--layer", "subagent", "--author-model", "claude-opus-4.6"]
        p = _patches(argv, ["gpt-5.3-codex", "gemini-3.1-pro-preview"])
        with p[0], p[1], p[2], p[3]:
            resolve_ducks_command()
        out = capsys.readouterr().out
        assert "gpt-5.3-codex" in out
        assert "Rubber-duck models for layer 'subagent'" in out

    def test_agent_picks(self, capsys):
        argv = ["cmd", "--layer", "mainAgent"]
        p = _patches(argv, AGENT_PICKS)
        with p[0], p[1], p[2], p[3]:
            resolve_ducks_command()
        assert "agent picks" in capsys.readouterr().out

    def test_writes_output_file(self, tmp_path, capsys):
        out_file = tmp_path / "nested" / "critique.md"
        argv = [
            "cmd",
            "--layer",
            "subagent",
            "--author-model",
            "claude-opus-4.6",
            "--file-key",
            "k",
            "--draft-answer",
            "/tmp/d.json",
            "--output",
            str(out_file),
        ]
        p = _patches(argv, ["gpt-5.3-codex"])
        with p[0], p[1], p[2], p[3]:
            resolve_ducks_command()
        assert out_file.exists()
        assert "Critique prompt written" in capsys.readouterr().out

    def test_json_output(self, capsys):
        argv = ["cmd", "--layer", "subagent", "--json"]
        p = _patches(argv, ["gpt-5.3-codex"])
        with p[0], p[1], p[2], p[3]:
            resolve_ducks_command()
        payload = json.loads(capsys.readouterr().out)
        assert payload["models"] == ["gpt-5.3-codex"]
        assert payload["agentPicks"] is False

    def test_output_write_failure_exits_with_code_2(self, tmp_path, capsys):
        out_file = tmp_path / "nested" / "critique.md"
        argv = ["cmd", "--layer", "subagent", "--output", str(out_file)]
        p = _patches(argv, ["gpt-5.3-codex"])
        with (
            p[0],
            p[1],
            p[2],
            p[3],
            patch(f"{_MODULE}.Path.write_text", side_effect=OSError("read-only fs")),
            pytest.raises(SystemExit) as exc,
        ):
            resolve_ducks_command()
        assert exc.value.code == 2
        assert f"Error: could not write critique prompt to {out_file}" in capsys.readouterr().err
