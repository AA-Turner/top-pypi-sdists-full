"""Tests for `efterlev.llm.claude_code_client` — subprocess Claude Code backend.

The client subprocesses `claude --print --output-format json` and parses
the JSON envelope. Tests use a fake `claude` binary script under tmp_path
to exercise the subprocess path without depending on the real CLI.
"""

from __future__ import annotations

import json
import os
import stat
from pathlib import Path
from textwrap import dedent

import pytest

from efterlev.errors import AgentError
from efterlev.llm.base import LLMMessage
from efterlev.llm.claude_code_client import ClaudeCodeClient, claude_cli_available


def _make_fake_claude(tmp_path: Path, *, exit_code: int = 0, stdout: str = "{}") -> Path:
    """Write a fake `claude` shell script that exits with `exit_code` and
    prints `stdout`. Used to stand in for the real CLI during tests."""
    script = tmp_path / "claude"
    # Escape single quotes in stdout for safe heredoc embedding.
    safe_stdout = stdout.replace("'", "'\\''")
    script.write_text(
        dedent(
            f"""\
            #!/bin/sh
            cat > /dev/null  # drain stdin (the prompt) so the test doesn't hang
            printf '%s' '{safe_stdout}'
            exit {exit_code}
            """
        ),
        encoding="utf-8",
    )
    script.chmod(script.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return script


def test_success_response_parsed_into_llmresponse(tmp_path: Path) -> None:
    """v0.1.151 / #356: tokens are forced to 0 regardless of what the
    envelope's `usage` block reports. On subscription, the envelope
    fields don't reflect actual Anthropic API counts (customer hit
    180 in / 441k out — clearly bogus), so the previous code computed
    a fake dollar cost. Forcing tokens=0 makes the cost-summary show
    accurate $0 contribution from subscription-backed calls.
    """
    fake_envelope = json.dumps(
        {
            "type": "result",
            "subtype": "success",
            "is_error": False,
            "result": "the model's text response",
            "usage": {"input_tokens": 42, "output_tokens": 17},
            "total_cost_usd": 0,
        }
    )
    fake = _make_fake_claude(tmp_path, exit_code=0, stdout=fake_envelope)
    client = ClaudeCodeClient(binary_path=str(fake))
    response = client.complete(
        system="be helpful",
        messages=[LLMMessage(content="hi")],
        model="claude-sonnet-4-6",
    )
    assert response.text == "the model's text response"
    assert response.model == "claude-sonnet-4-6"
    # tokens forced to 0 (v0.1.151), envelope's 42/17 ignored on purpose.
    assert response.input_tokens == 0
    assert response.output_tokens == 0
    assert response.prompt_hash  # sha256 over system+messages, non-empty


def test_on_chunk_fires_with_final_text(tmp_path: Path) -> None:
    """`claude --print` doesn't true-stream; we surface the final text
    as a single on_chunk callback so progress reporters still trigger."""
    envelope = json.dumps({"type": "result", "is_error": False, "result": "all done", "usage": {}})
    fake = _make_fake_claude(tmp_path, exit_code=0, stdout=envelope)
    client = ClaudeCodeClient(binary_path=str(fake))
    chunks: list[str] = []
    client.complete(
        system="s",
        messages=[LLMMessage(content="m")],
        model="m",
        on_chunk=chunks.append,
    )
    assert chunks == ["all done"]


def test_missing_binary_raises_clear_error(tmp_path: Path) -> None:
    """If the configured binary path doesn't exist, raise an AgentError
    pointing the user at install instructions — not a cryptic OSError."""
    client = ClaudeCodeClient(binary_path=str(tmp_path / "no-such-binary"))
    with pytest.raises(AgentError, match=r"claude.*PATH"):
        client.complete(system="s", messages=[LLMMessage(content="m")], model="m")


def test_non_zero_exit_raises_agent_error(tmp_path: Path) -> None:
    fake = _make_fake_claude(tmp_path, exit_code=42, stdout="")
    # The fake script also writes stderr via shell builtin — extend the
    # script to do so via a small edit. Simpler: use a separate script.
    fake.write_text(
        dedent(
            """\
            #!/bin/sh
            cat > /dev/null
            echo "boom: something broke" >&2
            exit 42
            """
        ),
        encoding="utf-8",
    )
    fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
    client = ClaudeCodeClient(binary_path=str(fake))
    with pytest.raises(AgentError, match="exited 42"):
        client.complete(system="s", messages=[LLMMessage(content="m")], model="m")


def test_malformed_json_response_raises_agent_error(tmp_path: Path) -> None:
    fake = _make_fake_claude(tmp_path, exit_code=0, stdout="this is not json")
    client = ClaudeCodeClient(binary_path=str(fake))
    with pytest.raises(AgentError, match="not valid JSON"):
        client.complete(system="s", messages=[LLMMessage(content="m")], model="m")


def test_envelope_error_with_401_hints_at_stale_subscription(tmp_path: Path) -> None:
    """Post-v0.1.149: API-key env vars are stripped from the subprocess,
    so a 401 usually means the subscription session is stale, not an
    env-var override. The hint should suggest refreshing OAuth."""
    envelope = json.dumps(
        {
            "type": "result",
            "is_error": True,
            "api_error_status": 401,
            "result": "Invalid credentials",
        }
    )
    fake = _make_fake_claude(tmp_path, exit_code=0, stdout=envelope)
    client = ClaudeCodeClient(binary_path=str(fake))
    with pytest.raises(AgentError) as exc_info:
        client.complete(system="s", messages=[LLMMessage(content="m")], model="m")
    msg = str(exc_info.value)
    assert "401" in msg
    assert "subscription" in msg
    assert "claude" in msg  # tells them to run claude interactively


def test_subprocess_env_strips_anthropic_api_key(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """v0.1.149 / #354: ANTHROPIC_API_KEY in the parent env must NOT
    be inherited by `claude --print` — otherwise the user has to unset
    it system-wide just to use the subscription backend.

    Verifies the subprocess sees an empty env for the auth vars by
    writing them out from the fake `claude` script.
    """
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-should-be-stripped")
    monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "auth-should-be-stripped")
    # Fake claude that echoes env-var presence into its JSON response
    # under a custom key the test reads back.
    script = tmp_path / "claude"
    script.write_text(
        "#!/bin/sh\ncat > /dev/null\n"
        'printf \'{"type":"result","is_error":false,"result":"%s|%s","usage":{}}\' '
        '"${ANTHROPIC_API_KEY:-MISSING}" "${ANTHROPIC_AUTH_TOKEN:-MISSING}"\n',
        encoding="utf-8",
    )
    script.chmod(0o755)
    client = ClaudeCodeClient(binary_path=str(script))
    response = client.complete(system="s", messages=[LLMMessage(content="m")], model="m")
    # Both auth vars must read as MISSING inside the subprocess.
    assert response.text == "MISSING|MISSING"


def test_subprocess_env_preserves_unrelated_vars(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Only the auth vars are stripped — everything else (PATH, HOME,
    user customizations) carries through so Claude Code can locate its
    config, keychain, etc."""
    monkeypatch.setenv("EFTERLEV_TEST_MARKER", "should-pass-through")
    script = tmp_path / "claude"
    script.write_text(
        "#!/bin/sh\ncat > /dev/null\n"
        'printf \'{"type":"result","is_error":false,"result":"%s","usage":{}}\' '
        '"${EFTERLEV_TEST_MARKER:-MISSING}"\n',
        encoding="utf-8",
    )
    script.chmod(0o755)
    client = ClaudeCodeClient(binary_path=str(script))
    response = client.complete(system="s", messages=[LLMMessage(content="m")], model="m")
    assert response.text == "should-pass-through"


def test_envelope_missing_result_field_raises(tmp_path: Path) -> None:
    envelope = json.dumps({"type": "result", "is_error": False, "usage": {}})  # no 'result'
    fake = _make_fake_claude(tmp_path, exit_code=0, stdout=envelope)
    client = ClaudeCodeClient(binary_path=str(fake))
    with pytest.raises(AgentError, match="missing 'result'"):
        client.complete(system="s", messages=[LLMMessage(content="m")], model="m")


def test_empty_messages_rejected() -> None:
    client = ClaudeCodeClient()
    with pytest.raises(AgentError, match="messages list cannot be empty"):
        client.complete(system="s", messages=[], model="m")


def test_timeout_defaults_to_600(monkeypatch: pytest.MonkeyPatch) -> None:
    """v0.1.227: default per-call timeout is 600s — a fresh subscription
    gap-batch call's TTFT exceeded the old 300s default and killed the
    2026-06-11 onboarding pipeline; 600 was the operator's working value
    and matches the Bedrock read_timeout precedent."""
    monkeypatch.delenv("EFTERLEV_LLM_TIMEOUT", raising=False)
    assert ClaudeCodeClient().timeout_seconds == 600.0


def test_timeout_configurable_via_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """EFTERLEV_LLM_TIMEOUT overrides the default (defensive depth for slow
    subscription calls / large prompts)."""
    monkeypatch.setenv("EFTERLEV_LLM_TIMEOUT", "900")
    assert ClaudeCodeClient().timeout_seconds == 900.0


def test_timeout_env_invalid_falls_back_to_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A typo'd or non-positive env value falls back to 600, never crashes."""
    monkeypatch.setenv("EFTERLEV_LLM_TIMEOUT", "not-a-number")
    assert ClaudeCodeClient().timeout_seconds == 600.0
    monkeypatch.setenv("EFTERLEV_LLM_TIMEOUT", "-5")
    assert ClaudeCodeClient().timeout_seconds == 600.0


def test_claude_cli_available_reflects_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """`claude_cli_available()` returns True iff `claude` is on PATH."""
    # Put a fake `claude` script at a known location and prepend its dir to PATH.
    fake_dir = tmp_path / "bin"
    fake_dir.mkdir()
    (fake_dir / "claude").write_text("#!/bin/sh\n", encoding="utf-8")
    (fake_dir / "claude").chmod(0o755)
    monkeypatch.setenv("PATH", str(fake_dir) + os.pathsep + os.environ.get("PATH", ""))
    assert claude_cli_available() is True

    monkeypatch.setenv("PATH", "/nonexistent-dir")
    assert claude_cli_available() is False
