"""pi's copies of the switch, the state names, the pairing rule and the MCP
token lookup match the Python they were copied from.

The pi extension cannot import the Python package, so four of its modules
re-state Python behaviour in TypeScript and, until this file, nothing compared
them: `trackingSwitch.ts` (the switch's words, `tracking_guard.py`),
`trackingState.ts` (the stored states, the recorder and the footer's words,
`session_marker`), `pairing.ts` (which capture token pi uses, the tap's `pi`
row) and `mcpAuth.ts` (where the read token comes from, `probe-mcp-headers`).
The day one of them drifted it was found the way the footer's daemon label
was: by reading both (`tracking (daemon)` on pi after the CLI said
`on (daemon)` everywhere else).
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from probe.sdk import session_marker
from tests.ts_source import ts_list, ts_object, ts_set, ts_string

AGENT = Path(__file__).resolve().parents[1]
HOOKS = AGENT / "plugins" / "probe-research" / "hooks"
TAP_ROOT = AGENT / "plugins" / "probe-research-tap"
MCP_HEADERS = AGENT / "plugins" / "probe-research" / "bin" / "probe-mcp-headers"
PI_CORE = AGENT / "plugins" / "probe-research-pi" / "src" / "core"
PATHS = PI_CORE / "paths.ts"
SWITCH = PI_CORE / "trackingSwitch.ts"
STATE = PI_CORE / "trackingState.ts"
PAIRING = PI_CORE / "pairing.ts"
MCP_AUTH = PI_CORE / "mcpAuth.ts"
HOSTED = PI_CORE / "hosted.ts"
WORKSPACE_LIMIT = PI_CORE / "workspaceLimit.ts"
TAP_RUNTIME = PI_CORE / "tapRuntime.ts"


def _guard():
    sys.path.insert(0, str(HOOKS))
    try:
        spec = importlib.util.spec_from_file_location("_tracking_guard_pi_core_parity", HOOKS / "tracking_guard.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.remove(str(HOOKS))


def _code(path: Path) -> str:
    """The source with comments removed, so a docstring naming a thing is not the code using it."""
    text = re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.S)
    return re.sub(r"(?m)^\s*//.*$", "", text)


# ---------------------------------------------------------------------------
# trackingSwitch.ts <- hooks/tracking_guard.py
# ---------------------------------------------------------------------------


def test_the_switch_words_are_the_guards():
    guard = _guard()
    for name in ("OFF_WORDS", "ON_WORDS", "READ_ONLY_WORDS", "TOGGLE_WORDS", "STATUS_WORDS", "INLINE_WORDS",
                 "LEGACY_SLUGS"):
        assert ts_set(SWITCH, name) == getattr(guard, name), name


def test_every_switch_spelling_is_a_slug_the_guard_flips_on():
    guard = _guard()
    spellings = re.search(r"const SPELLINGS = \[(.*?)\] as const;", SWITCH.read_text(encoding="utf-8"), re.S)
    assert spellings
    slugs = {re.sub(r"^[/$]", "", s).removeprefix("skill:") for s in re.findall(r'"([^"]+)"', spellings.group(1))}
    assert slugs and slugs <= guard.TOGGLE_SKILL_SLUGS
    assert ts_string(SWITCH, "CANONICAL") == "/skill:probe"


def test_the_switch_writes_the_states_the_cli_stores():
    sent = set(re.findall(r'\["state", "([^"]+)"\]', SWITCH.read_text(encoding="utf-8")))
    # `inline` is the researcher's hand-over (`probe session state inline`), not a stored state.
    assert sent == set(session_marker.SWITCH_STATES) | {session_marker.INLINE_WORD}


# ---------------------------------------------------------------------------
# trackingState.ts <- probe.sdk.session_marker
# ---------------------------------------------------------------------------


def test_the_stored_states_and_the_recorders_are_session_markers():
    assert set(ts_object(STATE, "ProbeState").values()) == set(session_marker.STATES)
    assert ts_object(STATE, "Recorder") == {
        "Agent": session_marker.RECORDER_AGENT,
        "Daemon": session_marker.RECORDER_DAEMON,
    }
    assert set(ts_object(STATE, "Recorder").values()) == set(session_marker.RECORDERS)


def test_every_printed_word_maps_back_to_its_stored_state():
    """The CLI prints `on`/`read`; pi's `parseState` must read both vocabularies."""
    aliases = dict(re.findall(r'if \(raw === "([\w-]+)"\) return "([\w-]+)";', STATE.read_text(encoding="utf-8")))
    printed = {label: state for state, label in session_marker.STATE_LABELS.items() if label != state}
    assert aliases == printed
    for word, state in aliases.items():
        assert session_marker.state_for_label(word) == state


def test_the_footer_says_what_the_status_line_says():
    assert ts_object(STATE, "RecordingLabel") == {
        "Tracking": session_marker._LABEL_TRACKING_BARE,
        "Daemon": session_marker._LABEL_DAEMON_BARE,
        "DaemonDegraded": session_marker._LABEL_DAEMON_DEGRADED_BARE,
        "Inline": session_marker._LABEL_INLINE_BARE,
    }
    source = STATE.read_text(encoding="utf-8")
    assert f'"○ {session_marker._LABEL_NOT_TRACKING}"' in source
    assert "`◐ ${label}" + session_marker._LABEL_NO_CAPTURE + "${capture.reason}`" in source


# ---------------------------------------------------------------------------
# pairing.ts <- the tap's `pi` row (tap/sources.py, tap/config.py)
# ---------------------------------------------------------------------------


def _ask_the_tap(home: Path, **env: str) -> dict:
    """The tap's own answer for pi, from a subprocess (see test_watcher_prefix_parity)."""
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import json;"
            "from tap import config as cfg, sources;"
            "row = sources.get('pi');"
            "print(json.dumps({'token_env': row.token_env, 'plugin_dir_env': row.plugin_dir_env,"
            "'source_id': row.source_id, 'token_file': cfg.token_file().name,"
            "'token': cfg.load_token()}))",
        ],
        capture_output=True,
        text=True,
        timeout=60,
        env={"PATH": os.environ.get("PATH", ""), "HOME": str(home), "PYTHONPATH": str(TAP_ROOT),
             "PROBE_TAP_SOURCE": "pi", **env},
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_pi_pairs_with_the_names_in_the_taps_pi_row(tmp_path):
    tap = _ask_the_tap(tmp_path)
    assert ts_string(PATHS, "SOURCE_ID") == tap["source_id"] == "pi"
    assert ts_string(PATHS, "TOKEN_ENV") == tap["token_env"]
    assert ts_string(PATHS, "PLUGIN_DIR_ENV") == tap["plugin_dir_env"]
    assert re.search(r'return join\(pluginDir\(env\), "' + re.escape(tap["token_file"]) + r'"\);', PATHS.read_text(encoding="utf-8"))


def test_pi_uses_the_same_token_the_tap_uploads_with(tmp_path):
    """`load_token` for pi: the paired file, then pi's env var, and NOTHING else --
    the CLI config's `ingest_token` is Claude Code's (D3). `checkPairing` reads
    the same two in the same order and never opens the config."""
    plugin_dir = tmp_path / "pi-state"
    plugin_dir.mkdir()
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"ingest_token": "claude-codes"}))
    env = {"PROBE_PI_TAP_PLUGIN_DIR": str(plugin_dir), "PROBE_CONFIG_PATH": str(config)}

    assert _ask_the_tap(tmp_path, **env)["token"] is None
    assert _ask_the_tap(tmp_path, **env, PROBE_PI_TAP_TOKEN="from-env")["token"] == "from-env"
    (plugin_dir / ".token").write_text("paired\n")
    assert _ask_the_tap(tmp_path, **env, PROBE_PI_TAP_TOKEN="from-env")["token"] == "paired"

    code = _code(PAIRING)
    body = code[code.index("export function checkPairing"):]
    assert body.index("readTrimmed(devicePath)") < body.index("env[TOKEN_ENV]")
    assert "probeConfigPath" not in code and "ingest_token" not in code


# ---------------------------------------------------------------------------
# mcpAuth.ts <- plugins/probe-research/bin/probe-mcp-headers
# ---------------------------------------------------------------------------


def test_the_mcp_token_comes_from_where_probe_mcp_headers_reads_it():
    script = MCP_HEADERS.read_text(encoding="utf-8")
    code = _code(MCP_AUTH)
    first = re.search(r'\[ -n "\$\{(\w+):-\}" \] && emit', script)
    assert first and ts_string(PATHS, "MCP_TOKEN_ENV") == first.group(1)
    # Then the config's read token, v2 contexts first, an absent context being "default".
    assert 'data.get("mcp_token")' in script and "flat.mcp_token" in code
    assert 'data.get("current_context") or "default"' in script and ': "default"' in code
    resolve = code[code.index("export function resolveMcpBearerToken"):]
    assert resolve.index("env[MCP_TOKEN_ENV]") < resolve.index("readProbeConfigMcpToken(env)")
    # Never the write token in the same file.
    assert 'print(data.get("mcp_token") or "")' in script
    assert "ingest_token" not in code


# ---------------------------------------------------------------------------
# workspaceLimit.ts <- probe.sdk.workspace_limit, bin/probe-mcp-headers
# ---------------------------------------------------------------------------


def test_the_workspace_limit_names_are_the_sdks_and_the_helpers():
    from probe.sdk import workspace_limit as wl

    assert ts_string(WORKSPACE_LIMIT, "WORKSPACE_LIMIT_HEADER") == wl.LIMIT_HEADER
    assert ts_string(WORKSPACE_LIMIT, "WORKSPACE_LIMIT_TEAM_ITEMS_HEADER") == wl.TEAM_ITEMS_HEADER
    assert ts_string(WORKSPACE_LIMIT, "WORKSPACE_LIMIT_ENV") == wl.LIMIT_ENV
    assert ts_string(WORKSPACE_LIMIT, "WORKSPACE_LIMIT_TEAM_ITEMS_ENV") == wl.TEAM_ITEMS_ENV
    assert ts_string(WORKSPACE_LIMIT, "WORKSPACE_LIMIT_TEAM_WORD") == wl.TEAM_WORD
    assert ts_string(WORKSPACE_LIMIT, "UNREADABLE_LIMIT") == wl.UNREADABLE_FORWARD
    assert set(ts_object(WORKSPACE_LIMIT, "TeamItems").values()) == {item.value for item in wl.TeamItems}
    script = MCP_HEADERS.read_text(encoding="utf-8")
    for name in (wl.LIMIT_HEADER, wl.TEAM_ITEMS_HEADER, wl.LIMIT_ENV, wl.TEAM_ITEMS_ENV, wl.UNREADABLE_FORWARD):
        assert name in script, name
    # The config keys all three read: the pin's `workspace`, its `limit` and `team_items`.
    code = _code(WORKSPACE_LIMIT)
    assert "anchor.limit !== true" in code and "anchor.team_items" in code and ".workspace" in code
    assert 'anchor.get("limit") is True' in script and 'anchor.get("team_items")' in script
    # The environment first, `team` meaning none, then the active context.
    resolve = code[code.index("export function resolveWorkspaceLimit"):]
    assert resolve.index("WORKSPACE_LIMIT_ENV") < resolve.index("readActiveProbeContext(env)")


def _helper_limit(tmp_path: Path, config: dict, **env: str) -> dict:
    home = tmp_path / "home"
    config_home = tmp_path / "config"
    (config_home / "probe").mkdir(parents=True, exist_ok=True)
    (config_home / "probe" / "config.json").write_text(json.dumps(config))
    home.mkdir(exist_ok=True)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    if not (bin_dir / "python3").exists():
        (bin_dir / "python3").symlink_to(sys.executable)
    result = subprocess.run(
        [str(MCP_HEADERS)],
        env={"HOME": str(home), "XDG_CONFIG_HOME": str(config_home), "PATH": f"{bin_dir}:/usr/bin:/bin",
             "CLAUDE_PLUGIN_ROOT": str(tmp_path / "plugin"), **env},
        capture_output=True, text=True, timeout=20, check=True,
    )
    from probe.sdk.workspace_limit import limit_headers_of

    return limit_headers_of(json.loads(result.stdout))


def test_the_helper_sends_the_limit_the_sdk_resolves(tmp_path, monkeypatch):
    """Same config, same environment: the headers helper (Claude Code's MCP) and
    the SDK's transport send the same limit."""
    from probe.sdk import workspace_limit as wl

    ws = "11111111-1111-1111-1111-111111111111"
    cases = [
        ({"workspace": {"id": ws}}, {}),
        ({"workspace": {"id": ws, "limit": True}}, {}),
        ({"workspace": {"id": f"id:{ws}", "limit": True, "team_items": "hide"}}, {}),
        ({"workspace": {"id": ws, "limit": True, "team_items": "hide"}}, {"PROBE_WORKSPACE_LIMIT_TEAM_ITEMS": "show"}),
        ({"workspace": {"id": ws, "limit": True}}, {"PROBE_WORKSPACE_LIMIT": "team"}),
        ({}, {"PROBE_WORKSPACE_LIMIT": "22222222-2222-2222-2222-222222222222"}),
    ]
    for index, (context, env) in enumerate(cases):
        config = {"version": 2, "current_context": "default",
                  "contexts": {"default": {"mcp_token": "probe_pat_read", **context}}}
        limit = wl.resolve_limit(config["contexts"]["default"], env)
        expected = {} if limit is None else wl.request_headers(limit, limit.id)
        assert _helper_limit(tmp_path / str(index), config, **env) == expected, (context, env)


# ---------------------------------------------------------------------------
# hosted.ts, paths.ts, tapRuntime.ts <- probe/service/paths.py, hooks/tap-python.sh
# ---------------------------------------------------------------------------


def test_pi_finds_the_service_where_the_service_keeps_its_files():
    """A session the Probe service records is read, on a Mac, through the
    service's lock file (`statusline_refresh._is_the_service`); pi re-states
    where that file is. The machine key is pinned by a fixture both languages
    read (tests/hosted.test.ts the other half)."""
    from probe.service import paths

    assert ts_string(PATHS, "SERVICE_DIRNAME") == paths.SERVICE_DIRNAME
    assert ts_string(PATHS, "SERVICE_LOCK_NAME") == paths.LOCK_NAME
    assert ts_string(PATHS, "SERVICE_RUNTIME_NAME") == paths.RUNTIME_NAME
    assert tuple(ts_list(HOSTED, "MACHINE_ID_FILES")) == paths.MACHINE_ID_FILES
    # sha256(b"probe-service\0" + id): the prefix, one NUL byte, the id.
    assert 'b"probe-service\\0" + machine_id()' in (AGENT / "src" / "probe" / "service" / "paths.py").read_text(encoding="utf-8")
    assert ts_string(HOSTED, "MACHINE_KEY_PREFIX") == "probe-service"
    assert re.search(r"export const MACHINE_KEY_SEPARATOR = 0x00;", HOSTED.read_text(encoding="utf-8"))
    assert re.search(rf"export const MACHINE_KEY_LEN = {paths.MACHINE_KEY_LEN};", HOSTED.read_text(encoding="utf-8"))
    # Windows's machine id: the same registry value the service reads (`_windows_guid`).
    source = (AGENT / "src" / "probe" / "service" / "paths.py").read_text(encoding="utf-8")
    key = re.search(r'winreg\.HKEY_LOCAL_MACHINE, r"([^"]+)"', source)
    value = re.search(r'QueryValueEx\(key, "([^"]+)"\)', source)
    assert key and value and "KEY_WOW64_64KEY" in source
    assert ts_string(HOSTED, "WINDOWS_GUID_KEY") == "HKLM\\" + key.group(1)
    assert ts_string(HOSTED, "WINDOWS_GUID_VALUE") == value.group(1)
    # What the service runs as (`client.py`: `python -I -m probe.service`), which /proc shows.
    assert ts_string(HOSTED, "SERVICE_COMMAND_MARK") == "probe.service"
    assert '"-m", "probe.service"' in (AGENT / "src" / "probe" / "service" / "client.py").read_text(encoding="utf-8")


def test_the_machine_key_fixture_is_the_services(monkeypatch):
    from probe.service import paths

    fixture = json.loads((AGENT / "tests" / "fixtures" / "service-machine-key.json").read_text(encoding="utf-8"))
    assert fixture["cases"]
    for case in fixture["cases"]:
        monkeypatch.setattr(paths, "_machine_key", None)
        monkeypatch.setattr(paths, "machine_id", lambda case=case: case["machine_id"])
        assert paths.machine_key() == case["machine_key"], case


def test_pi_picks_the_taps_interpreter_as_tap_python_sh_does():
    """#3338 taught the hooks to run the tap on a Python 3.11+ (Apple's 3.9 broke
    every session); pi's own search (`tapRuntime.ts`) asks the same places in the
    same order and leaves the same note for `probe doctor`."""
    from probe.cli import doctor
    from probe.service import paths

    script = (TAP_ROOT / "hooks" / "tap-python.sh").read_text(encoding="utf-8")
    versioned = re.search(r"for name in ((?:python3\.\d+ ?)+); do", script)
    assert versioned and ts_list(TAP_RUNTIME, "VERSIONED_PYTHONS") == versioned.group(1).split()
    assert "sys.version_info >= (3, 11)" in script
    start = (TAP_ROOT / "tap" / "start.py").read_text(encoding="utf-8")
    minimum = re.search(r"^MIN_PYTHON = \((\d+), (\d+)\)$", start, re.M)
    assert minimum
    assert re.search(
        rf"export const MIN_TAP_PYTHON = \[{minimum.group(1)}, {minimum.group(2)}\] as const;",
        TAP_RUNTIME.read_text(encoding="utf-8"),
    )
    assert tuple(ts_list(PATHS, "UV_TOOL_PYTHON")) == paths.UV_TOOL_PYTHON
    assert ts_list(PATHS, "UV_TOOL_PYTHON_WINDOWS") == ["uv", "tools", "probe-research", "Scripts", "python.exe"]
    assert "uv/tools/probe-research/Scripts/python.exe" in script
    assert ts_string(PATHS, "TAP_PYTHON_MISSING") == doctor.TAP_PYTHON_MISSING
    assert 'TAP_PYTHON_MISSING="' + doctor.TAP_PYTHON_MISSING + '"' in script


def test_pi_asks_tap_finish_with_the_flags_its_parser_takes(tmp_path):
    """pi's quit runs `tap finish` for a session the Probe service records
    (`daemon.ts::finishHostedSession`, session-end.sh's call). A flag the tap's
    parser stopped taking would exit 1 like "not recorded", silently; ask the
    parser itself, in a subprocess with the tap on PYTHONPATH."""
    code = _code(PI_CORE / "daemon.ts")
    assert '["-m", "tap", "finish", "--session-id", sessionId, "--wait", String(waitS)]' in code
    probe = (
        "import sys\n"
        "from tap import record_client as rc\n"
        "seen = []\n"
        "rc.finish = lambda args: seen.append((args.session_id, args.wait)) or 0\n"
        "code = rc.main('finish', ['--session-id', 'sid-1', '--wait', '3'])\n"
        "print(code, seen)\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", probe],
        capture_output=True, text=True, cwd=tmp_path,
        env={"PATH": os.environ.get("PATH", ""), "HOME": str(tmp_path), "PYTHONPATH": str(TAP_ROOT)},
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "0 [('sid-1', 3.0)]"


def test_pi_names_what_it_found_in_tap_python_sh_words():
    """When no Python 3.11+ is found pi says what `python3` is, in the words
    `tap_python_seen` uses (they reach `probe doctor` the same way)."""
    script = (TAP_ROOT / "hooks" / "tap-python.sh").read_text(encoding="utf-8")
    body = script[script.index("tap_python_seen() {"):]
    for name in ("PYTHON_SEEN_NONE", "PYTHON_SEEN_BROKEN"):
        assert f"printf '{ts_string(TAP_RUNTIME, name)}\\n'" in body, name
    assert ts_string(TAP_RUNTIME, "PYTHON_SEEN_PREFIX") == "python3 "
    assert "printf 'python3 %s\\n'" in body
