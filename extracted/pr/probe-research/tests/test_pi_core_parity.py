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
from tests.ts_source import ts_object, ts_set, ts_string

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
    for name in ("OFF_WORDS", "ON_WORDS", "READ_ONLY_WORDS", "TOGGLE_WORDS", "STATUS_WORDS", "LEGACY_SLUGS"):
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
    assert sent == set(session_marker.SWITCH_STATES)


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
