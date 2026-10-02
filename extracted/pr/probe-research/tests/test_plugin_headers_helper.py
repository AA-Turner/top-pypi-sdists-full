"""The Claude Code headers helper reports plugin metadata without starting the CLI."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


_HELPER = (
    Path(__file__).resolve().parent.parent
    / "plugins"
    / "probe-research"
    / "bin"
    / "probe-mcp-headers"
)


#: Every marker the helper detects. Scrubbed by default so these tests answer the same
#: way wherever they run: the harness inherits os.environ, and a developer running the
#: suite from inside Claude Code would otherwise get real agent headers in the output
#: and fail the exact-match assertions below -- while CI, which has none of these set,
#: stayed green. Tests that WANT an agent set it explicitly through extra_env.
_AGENT_MARKERS = (
    "CLAUDECODE",
    "CLAUDE_CODE_ENTRYPOINT",
    "CLAUDE_CODE_SESSION_ID",
    "CURSOR_TRACE_ID",
    "CODEX_SANDBOX",
    "CODEX_THREAD_ID",
    "PRBE_CODEX_TAP_TOKEN",
    "PRBE_CODEX_TAP_PLUGIN_DIR",
)


@pytest.fixture(autouse=True)
def _no_ambient_agent(monkeypatch):
    for marker in _AGENT_MARKERS:
        monkeypatch.delenv(marker, raising=False)


def _run_helper(
    plugin_root: Path,
    *,
    include_env_token: bool = True,
    extra_env: dict[str, str] | None = None,
) -> dict[str, str]:
    env = {
        **os.environ,
        "CLAUDE_PLUGIN_ROOT": str(plugin_root),
    }
    if include_env_token:
        env["PROBE_MCP_TOKEN"] = "probe_pat_test"
    else:
        env.pop("PROBE_MCP_TOKEN", None)
    env.update(extra_env or {})
    result = subprocess.run(
        [str(_HELPER)],
        env=env,
        check=True,
        capture_output=True,
        text=True,
        timeout=2,
    )
    return json.loads(result.stdout)


@pytest.mark.parametrize("version", ["0.7.0", "1.2.3+linux-01"])
def test_helper_emits_plugin_kind_and_metadata_version(
    tmp_path: Path,
    version: str,
) -> None:
    metadata = tmp_path / ".claude-plugin" / "plugin.json"
    metadata.parent.mkdir()
    metadata.write_text(json.dumps({"name": "probe-research", "version": version}) + "\n")

    assert _run_helper(tmp_path) == {
        "Authorization": "Bearer probe_pat_test",
        "X-Probe-Client": "plugin",
        "X-Probe-Client-Version": version,
    }


def test_helper_keeps_authorization_when_metadata_is_missing(tmp_path: Path) -> None:
    assert _run_helper(tmp_path) == {
        "Authorization": "Bearer probe_pat_test",
    }


@pytest.mark.parametrize("version", ["latest", "0.0.0.dev0", "1.2.3-01"])
def test_helper_drops_malformed_metadata_without_breaking_auth(
    tmp_path: Path,
    version: str,
) -> None:
    metadata = tmp_path / ".claude-plugin" / "plugin.json"
    metadata.parent.mkdir()
    metadata.write_text(json.dumps({"name": "probe-research", "version": version}) + "\n")

    assert _run_helper(tmp_path) == {
        "Authorization": "Bearer probe_pat_test",
    }


# --- the config read ------------------------------------------------------
#
# NO `probe` ON PATH, deliberately, in every test below. The helper falls back to
# shelling out to the CLI when its own read finds nothing, so a test that leaves a
# real `probe` reachable passes whether the read works or not -- which is exactly
# how a read that never once matched the shape the wizard writes stayed green. PATH
# here holds a python3 and nothing else, so the only thing that can answer is the
# config read under test.


def _hermetic_path(tmp_path: Path) -> str:
    """A PATH with an interpreter and no `probe`."""
    bin_dir = tmp_path / "hermetic-bin"
    bin_dir.mkdir()
    (bin_dir / "python3").symlink_to(sys.executable)
    return str(bin_dir)


def _run_helper_against_config(tmp_path: Path, config: dict) -> subprocess.CompletedProcess:
    home = tmp_path / "home"
    config_home = tmp_path / "config"
    (config_home / "probe").mkdir(parents=True)
    (config_home / "probe" / "config.json").write_text(json.dumps(config))
    home.mkdir()
    return subprocess.run(
        [str(_HELPER)],
        env={
            "CLAUDE_PLUGIN_ROOT": str(tmp_path / "plugin"),
            "HOME": str(home),
            "XDG_CONFIG_HOME": str(config_home),
            "PATH": _hermetic_path(tmp_path),
        },
        capture_output=True,
        text=True,
        timeout=10,
    )


def test_helper_reads_the_active_context_of_a_v2_config(tmp_path: Path) -> None:
    """The shape `probe wizard` actually writes.

    This is the whole bug: the read only knew v1's top-level key, so on every
    install the wizard has ever produced the fast path returned nothing. A machine
    where the CLI fallback could not resolve a `probe` then sent an unauthenticated
    request, and the edge's `WWW-Authenticate` challenge put Claude Code into an
    OAuth flow -- `/mcp`, re-authenticate, on a device the installer had just
    authorized.
    """
    result = _run_helper_against_config(
        tmp_path,
        {
            "version": 2,
            "current_context": "default",
            "contexts": {
                "default": {
                    "token": "probe_pat_write",
                    "mcp_token": "probe_pat_read",
                }
            },
        },
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["Authorization"] == "Bearer probe_pat_read"


def test_helper_reads_a_non_default_active_context(tmp_path: Path) -> None:
    """`current_context` decides, not the first or the one named "default"."""
    result = _run_helper_against_config(
        tmp_path,
        {
            "version": 2,
            "current_context": "work",
            "contexts": {
                "default": {"mcp_token": "probe_pat_wrong"},
                "work": {"mcp_token": "probe_pat_right"},
            },
        },
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["Authorization"] == "Bearer probe_pat_right"


def test_helper_still_reads_a_v1_flat_config(tmp_path: Path) -> None:
    """v1 is migrated in memory on read and never rewritten, so a config written
    before named contexts can still be sitting on disk untouched."""
    result = _run_helper_against_config(tmp_path, {"mcp_token": "probe_pat_v1"})

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["Authorization"] == "Bearer probe_pat_v1"


def test_helper_serves_no_token_when_the_active_context_is_missing(tmp_path: Path) -> None:
    """An unknown `current_context` must not fall through to a sibling.

    Handing the MCP another context's credential would point it at an endpoint the
    user is not on -- a wrong answer is worse here than no answer, because no answer
    is a diagnosable failure and a wrong one silently reads someone else's lab.
    """
    result = _run_helper_against_config(
        tmp_path,
        {
            "version": 2,
            "current_context": "gone",
            "contexts": {"default": {"mcp_token": "probe_pat_other"}},
        },
    )

    assert result.returncode == 1
    assert "probe_pat_other" not in result.stdout


def test_helper_never_serves_the_write_token(tmp_path: Path) -> None:
    """The MCP surface is read-only. A context holding only a write token has no
    credential for this helper, and must not borrow one."""
    result = _run_helper_against_config(
        tmp_path,
        {
            "version": 2,
            "current_context": "default",
            "contexts": {"default": {"token": "probe_pat_write"}},
        },
    )

    assert result.returncode == 1
    assert "probe_pat_write" not in result.stdout


def test_helper_adds_plugin_metadata_to_cli_fallback_token(tmp_path: Path) -> None:
    metadata = tmp_path / "plugin" / ".claude-plugin" / "plugin.json"
    metadata.parent.mkdir(parents=True)
    metadata.write_text('{"name":"probe-research","version":"0.7.0"}\n')

    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_probe = fake_bin / "probe"
    fake_probe.write_text(
        "#!/bin/sh\n"
        '[ "$1 $2" = "mcp headers" ] || exit 1\n'
        """printf '%s\\n' '{"Authorization": "Bearer probe_pat_fallback"}'\n"""
    )
    fake_probe.chmod(0o755)

    assert _run_helper(
        tmp_path / "plugin",
        include_env_token=False,
        extra_env={
            "HOME": str(tmp_path / "home"),
            "XDG_CONFIG_HOME": str(tmp_path / "config"),
            "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}",
        },
    ) == {
        "Authorization": "Bearer probe_pat_fallback",
        "X-Probe-Client": "plugin",
        "X-Probe-Client-Version": "0.7.0",
    }


# ---------------------------------------------------------------------------
# Agent + session attribution
#
# The hosted MCP is stateless and multi-tenant: a bearer token is all it otherwise
# receives, so without these two headers it cannot tell which conversation it is
# serving, and a tool call can never be joined back to its captured transcript
# (graph id agent_session:{agent}:{session_id} -- the PAIR is the key).
#
# The charset bound is load-bearing for a second reason: this value is interpolated
# into the JSON on stdout, and broken stdout here is not degraded telemetry, it is an
# unauthenticated request and a user bounced into OAuth.
# ---------------------------------------------------------------------------

_GOOD_SESSION = "385cbaab-3a35-4e8f-91d7-cc57826261e4"


def _plugin_root(tmp_path: Path, version: str = "0.7.0") -> Path:
    root = tmp_path / "plugin"
    (root / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    (root / ".claude-plugin" / "plugin.json").write_text(
        json.dumps({"name": "probe-research", "version": version})
    )
    return root


def test_claude_code_reports_its_agent_and_session(tmp_path: Path) -> None:
    headers = _run_helper(
        _plugin_root(tmp_path),
        extra_env={"CLAUDECODE": "1", "CLAUDE_CODE_SESSION_ID": _GOOD_SESSION},
    )
    assert headers["X-Probe-Agent"] == "claude_code"
    assert headers["X-Probe-Agent-Session"] == _GOOD_SESSION


def test_an_older_claude_code_without_a_session_still_authenticates(tmp_path: Path) -> None:
    """Claude Code only exports the session id from 2.1.132. Below that we send neither
    header -- but auth must be untouched, or the upgrade nudge becomes a lockout."""
    headers = _run_helper(_plugin_root(tmp_path), extra_env={"CLAUDECODE": "1"})
    assert headers["Authorization"] == "Bearer probe_pat_test"
    assert "X-Probe-Agent" not in headers
    assert "X-Probe-Agent-Session" not in headers


def test_cursor_is_detectable_but_never_reported(tmp_path: Path) -> None:
    """Cursor transcripts are not captured, so a session id we could never resolve is
    worse than none: it invites someone to follow a dead link."""
    headers = _run_helper(
        _plugin_root(tmp_path),
        extra_env={"CURSOR_TRACE_ID": "abcdefgh12345678"},
    )
    assert "X-Probe-Agent" not in headers
    assert "X-Probe-Agent-Session" not in headers


def test_codex_is_reported_only_once_its_tap_is_paired(tmp_path: Path) -> None:
    unpaired = _run_helper(
        _plugin_root(tmp_path),
        extra_env={
            "CODEX_THREAD_ID": "abcdefgh12345678",
            "PRBE_CODEX_TAP_PLUGIN_DIR": str(tmp_path / "absent"),
        },
    )
    assert "X-Probe-Agent" not in unpaired

    tap = tmp_path / "tap"
    tap.mkdir()
    (tap / ".token").write_text("a-credential")
    paired = _run_helper(
        _plugin_root(tmp_path),
        extra_env={
            "CODEX_THREAD_ID": "abcdefgh12345678",
            "PRBE_CODEX_TAP_PLUGIN_DIR": str(tap),
        },
    )
    assert paired["X-Probe-Agent"] == "codex"
    assert paired["X-Probe-Agent-Session"] == "abcdefgh12345678"


@pytest.mark.parametrize(
    ("session", "why"),
    [
        ("short", "under the 8 character floor"),
        ("x" * 201, "over the 200 character ceiling"),
        ('aaaaaaaa", "X-Evil": "1', "a quote would close the JSON string early"),
        ("aaaaaaaa\\", "a backslash would escape the closing quote"),
        ("aaaaaaaa\nevil", "a newline would split the document"),
        ("aaaaaaaa evil", "a space is outside the permitted charset"),
        ("aaaaaaaa{}", "braces are outside the permitted charset"),
    ],
)
def test_an_unusable_session_id_is_dropped_and_stdout_stays_valid(
    tmp_path: Path, session: str, why: str
) -> None:
    # _run_helper json.loads() the output, so a broken document fails here loudly.
    headers = _run_helper(
        _plugin_root(tmp_path),
        extra_env={"CLAUDECODE": "1", "CLAUDE_CODE_SESSION_ID": session},
    )
    assert "X-Probe-Agent-Session" not in headers, why
    assert headers["Authorization"] == "Bearer probe_pat_test", "auth must survive: " + why


def test_agent_headers_ride_the_no_metadata_branch_too(tmp_path: Path) -> None:
    """emit() has two printf branches. The one without plugin metadata is the one a
    stale or unreadable plugin.json takes, and it must still attribute."""
    root = tmp_path / "plugin"
    (root / ".claude-plugin").mkdir(parents=True)
    (root / ".claude-plugin" / "plugin.json").write_text("{ not json")
    headers = _run_helper(
        root,
        extra_env={"CLAUDECODE": "1", "CLAUDE_CODE_SESSION_ID": _GOOD_SESSION},
    )
    assert "X-Probe-Client-Version" not in headers
    assert headers["X-Probe-Agent"] == "claude_code"
    assert headers["X-Probe-Agent-Session"] == _GOOD_SESSION


@pytest.mark.parametrize(
    "session",
    [
        "a" * 7,
        "a" * 8,
        "a" * 200,
        "a" * 201,
        "a.b_c:d-e12",
        "aaaaaaaa!",
        "aaaaaaaa é",
        "aaaaaaaa１２",
    ],
)
def test_the_shell_and_the_server_agree_on_every_session_id(tmp_path: Path, session: str) -> None:
    """One rule, two implementations, and nothing was pinning them together.

    The helper enforces the charset/bounds in shell; the server enforces the same rule
    through `agent_session.valid_session_id`. If either side tightens, the plugin keeps
    sending values the server silently drops and attribution goes dark with both test
    files green. `_telemetry_core`'s mirror and the AGENTS table both have parity tests;
    this one did not.

    LC_ALL=C is pinned because the shell guard is a glob whose A-Z/a-z ranges are
    resolved by the current locale's collation, while the server's regex is ASCII-strict
    regardless. Without it this test's verdict depends on the developer's locale.
    """
    from probe.sdk.agent_session import valid_session_id

    headers = _run_helper(
        _plugin_root(tmp_path),
        extra_env={
            "CLAUDECODE": "1",
            "CLAUDE_CODE_SESSION_ID": session,
            "LC_ALL": "C",
        },
    )
    sent = "X-Probe-Agent-Session" in headers
    assert sent is valid_session_id(session), (
        f"shell sends={sent} but the server accepts={valid_session_id(session)} "
        f"for {session!r}"
    )
