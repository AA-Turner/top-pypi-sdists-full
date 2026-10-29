"""One frozen hooks.json entry per event, and the dispatcher behind it.

Codex trusts each hooks.json entry by a hash of the whole entry and silently
skips a changed one until the researcher re-approves it in `/hooks`; 21 of the
23 edits to the old per-script hooks.json did that to every Codex user. So
hooks.json now holds one entry per event, with no tool matcher, that never
change, each running `hooks/dispatch.sh <lane>`, and what runs is routes.json:
the old per-script wiring, byte for byte, with a lane on each group.

What these tests hold:
  * the entries are frozen (a pinned hash per entry) and identical in both
    tracking plugins; the route surface is pinned too, so adding a route (which
    runs on every Codex user's machine with no approval) is a reviewed act;
  * ROUTING PARITY: for every event and tool, the dispatcher runs exactly the
    routes (and each exactly once) that registering routes.json directly would,
    and dispatch.sh's shell fast path never skips a payload a route matches;
  * a lone plain python route runs in-process with the env, argv and stdin its
    bash line would give, bounded by its own timeout; every other shape is
    exec'd unchanged with the signals Python ignores restored;
  * several routes run in parallel, each bounded, killed with what they started,
    and their outputs merge without losing a denial, a context or a block;
  * nothing the dispatcher does can veto on its own, missing files included;
  * Codex sessions leave the heartbeat the capture plugin looks for.
"""

from __future__ import annotations

import ast
import collections
import hashlib
import importlib.util
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest

AGENT = Path(__file__).resolve().parents[1]
PLUGINS = ("probe-research", "probe-research-daemon")
FULL = AGENT / "plugins" / "probe-research" / "hooks"
HASHES = Path(__file__).parent / "fixtures" / "hook_entry_hashes.json"
SURFACE = Path(__file__).parent / "fixtures" / "hook_route_surface.json"
SID = "0199a1b2-c3d4-7e5f-8a9b-0c1d2e3f4a5b"
TOOL_EVENTS = ("PreToolUse", "PostToolUse")

pytestmark = pytest.mark.skipif(os.name != "posix", reason="the hooks are POSIX shell")


def _load():
    spec = importlib.util.spec_from_file_location("_test_dispatch", FULL / "dispatch.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dispatch = _load()


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _wiring(plugin: str) -> dict:
    return _json(AGENT / "plugins" / plugin / "hooks" / "routes.json")


def _entries(plugin: str):
    for event, groups in _json(AGENT / "plugins" / plugin / "hooks" / "hooks.json")["hooks"].items():
        for group in groups:
            for hook in group["hooks"]:
                yield event, group.get("matcher"), hook


def _lane(command: str) -> str:
    found = re.search(r'exec "\$ROOT/hooks/dispatch\.sh" ([a-z-]+)\'$', command)
    assert found, command[-80:]
    return found.group(1)


# --- the frozen entries ----------------------------------------------------------


def _entry_hash(event: str, matcher, hook: dict) -> str:
    return hashlib.sha256(json.dumps([event, matcher, hook], sort_keys=True).encode()).hexdigest()[:16]


def test_the_entries_are_frozen():
    """Changing, adding or reordering a hooks.json entry switches that hook off
    for EVERY Codex user until they approve it again in /hooks, and nothing in
    their session says so (only the capture plugin's nudge). Add a route to
    routes.json instead. If an entry truly must change, regenerate this pin in
    the same PR as a release note telling Codex users to approve it."""
    pinned = _json(HASHES)
    for plugin in PLUGINS:
        actual = [f"{event}:{_entry_hash(event, matcher, hook)}" for event, matcher, hook in _entries(plugin)]
        assert actual == pinned["entries"], (
            f"{plugin}/hooks/hooks.json changed: this re-approves every Codex user's Probe hooks"
        )


def test_the_entries_name_no_tool():
    """Which tools are guarded is routes.json's and dispatch.sh's to decide, in
    any release. A matcher on a frozen entry would freeze it forever."""
    for plugin in PLUGINS:
        for event, matcher, _hook in _entries(plugin):
            assert matcher is None, f"{plugin} {event}: a frozen entry may not filter tools"


def test_both_tracking_plugins_ship_the_same_entries_and_dispatcher():
    for name in ("hooks.json", "dispatch.sh", "dispatch.py"):
        a, b = (AGENT / "plugins" / p / "hooks" / name for p in PLUGINS)
        assert a.read_bytes() == b.read_bytes(), f"{name} drifted: make sync-daemon-plugin"
    assert os.access(FULL / "dispatch.sh", os.X_OK), "the entries `exec` it after an -x check"


def test_every_entry_names_one_lane_of_its_own_event():
    for plugin in PLUGINS:
        lanes = []
        for event, _matcher, hook in _entries(plugin):
            lane = _lane(hook["command"])
            assert dispatch.LANE_EVENT[lane] == event
            lanes.append(lane)
        hooked = set(dispatch.LANE_EVENT) - dispatch.ADAPTER_LANES
        assert sorted(lanes) == sorted(hooked), "every lane but the adapter's has exactly one entry"
    # An adapter lane's event is one Claude Code and Codex never fire: only
    # `harness_io.py --event` (the Kimi manifest) runs it.
    events = {event for event, _matcher, _hook in _entries(PLUGINS[0])}
    assert not {dispatch.LANE_EVENT[lane] for lane in dispatch.ADAPTER_LANES} & events


def test_entry_timeouts_leave_every_route_its_own():
    """The dispatcher stops MARGIN_S before the entry's timeout so the harness
    never kills it (and every route's output) first; each route must still get
    its whole timeout. SessionEnd is bounded by the harness instead."""
    for plugin in PLUGINS:
        wiring = _wiring(plugin)["hooks"]
        for event, _matcher, hook in _entries(plugin):
            lane = _lane(hook["command"])
            assert hook.get("timeout") == dispatch.ENTRY_TIMEOUT[lane], lane
            if lane == "session-end":
                continue
            longest = max(h.get("timeout", 0) for g in wiring[event] if g["lane"] == lane for h in g["hooks"])
            assert dispatch.budget(lane) >= longest, f"{lane}: a route would lose time"


#: Plan D36: every route, by lane and script, says whether it is record-keeping
#: (True: nothing waits on its outcome, so on a host miss it is queued for the
#: Probe service, which runs it once) or not (False: a decision, context or a
#: message the agent waits on, which a miss runs where the agent is). routes.json
#: spells only `"record_keeping": true`; a route without it waits, the safe side.
#: A NEW ROUTE MUST BE ADDED HERE, with what it gives the agent.
ROUTE_CLASSES = {
    ("prompt", "tracking_guard.py"): False,  # refuses a switch move; the tracking context
    ("prompt", "statusline_refresh.py"): True,  # silent always: a detached fetch warms the status line's marker
    ("prompt", "note_audit.py"): False,  # the team note's audit line as context (once per session: queued, it is lost)
    ("prompt", "approvals_hook.py"): False,  # the daemon's waiting question as context
    ("prompt", "reads_hook.py"): False,  # claims daemon messages into the prompt's context
    # Moves a session off a `tap watch` too old to hand it to the Probe service
    # (silent, a detached child; queued, a dead session's wrapper would be swapped).
    ("prompt", "tap_handover.py"): False,
    ("session-start", "session-start.sh"): False,  # the session's opening context
    ("session-start", "statusline_refresh.py"): True,
    ("session-start", "approvals_hook.py"): False,
    ("pre-compact", "session-start.sh"): False,  # the context a compaction keeps
    ("pre-tool", "tracking_guard.py"): False,  # allow / deny
    ("pre-tool", "approvals_hook.py"): False,  # refuses a question not asked word for word
    ("pre-tool", "papers_hook.py"): False,  # refuses a paper web search before `probe paper find`
    ("pre-tool", "root_skills_sync.py skill-call"): False,  # the agent waits: it can refuse a Skill call (not record-keeping)
    ("post-tool", "telemetry.py post-tool"): True,  # observability only, a detached sender
    ("post-tool", "tracking_guard.py"): False,  # warns after a write that got through
    ("post-tool", "statusline_refresh.py"): True,
    ("post-tool", "approvals_hook.py"): False,  # the researcher's answer to the daemon's question
    ("post-tool", "reads_hook.py"): False,  # claims daemon messages into the tool result's context
    ("session-end", "telemetry.py session-end"): True,
    ("session-end", "team-note-sync.sh"): True,  # a detached `probe notes sync`, silent
    ("stop", "statusline_notify.py"): False,  # a status change as a message, once (queued, it is lost)
    ("stop", "owed_hook.py"): False,  # sends an inline agent back: a decision the turn waits on
    ("stop", "team-note-sync.sh"): True,  # a detached `probe notes sync --push-only`, silent
    ("turn-started", "tracking_guard.py"): False,
}


@pytest.mark.parametrize("plugin", PLUGINS)
def test_every_route_says_whether_it_is_record_keeping(plugin):
    seen = set()
    for event, groups in _wiring(plugin)["hooks"].items():
        for group in groups:
            for hook in group["hooks"]:
                script = re.findall(r"hooks/([A-Za-z0-9_.-]+\.(?:py|sh))\"?((?: [a-z][a-z-]*)*)'", hook["command"])
                key = (group["lane"], "".join(script[-1]) if script else hook["command"])
                assert key in ROUTE_CLASSES, (
                    f"{plugin} {event}: {key} is a new route: add it to ROUTE_CLASSES, record-keeping (queued "
                    "for the service on a host miss) or not (run where the agent is)"
                )
                assert "record_keeping" not in hook or hook["record_keeping"] is True, f"{plugin} {key}: true, or absent"
                assert dispatch.record_keeping(hook) is ROUTE_CLASSES[key], f"{plugin} {key}"
                seen.add(key)
    assert seen == set(ROUTE_CLASSES), f"{plugin}: classified routes it does not have: {set(ROUTE_CLASSES) - seen}"
    # A decision is never queued: nothing on the lanes that allow or deny is record-keeping.
    assert not [k for k, kept in ROUTE_CLASSES.items() if kept and k[0] in ("pre-tool", "turn-started")]


def test_the_route_surface_is_pinned():
    """What runs, on which event and tool, with which exports. A new row runs on
    every Codex user's machine without a /hooks prompt: regenerate this pin only
    with a reviewer who has read the new route (see agent/docs/adding-a-harness.md)."""
    surface = {}
    for plugin in PLUGINS:
        rows = []
        for event, groups in _wiring(plugin)["hooks"].items():
            for group in groups:
                for hook in group["hooks"]:
                    script = re.findall(r"hooks/([A-Za-z0-9_.-]+\.(?:py|sh))\"?((?: [a-z][a-z-]*)*)'", hook["command"])
                    exports = sorted(set(re.findall(r"export (PROBE_[A-Z_]+=[a-z_]+)", hook["command"])))
                    rows.append([event, group["lane"], group.get("matcher"), "".join(script[-1]) if script else None, exports])
        surface[plugin] = rows
    assert surface == _json(SURFACE)["routes"]


def test_the_dispatcher_runs_on_the_hook_runtime():
    """System python3 >= 3.9, stdlib only, no site-packages (`-S`).
    test_py310_compat covers agent/src, not these files."""
    stdlib = set(sys.stdlib_module_names)
    # The host (plan A0) and the service's paths it asks with are the
    # dispatcher's own, held to the same rule; a miss with no service reads the
    # session's switch through the vendored session marker, a stdlib-only copy
    # every hook imports (tests/test_session_marker_parity.py).
    own = {"dispatch", "_service_paths", "_session_marker"}
    for name in ("dispatch.py", "zygote.py", "_service_paths.py"):
        source = (FULL / name).read_text(encoding="utf-8")
        tree = ast.parse(source, feature_version=(3, 9))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                if node.level and name == "_service_paths.py":
                    # `paths.pipe_name`'s `from . import winpipe` (Windows): the
                    # copy's hooks reach the service by its socket, POSIX only.
                    continue
                names = [node.module or ""]
            else:
                continue
            for module in names:
                assert module.split(".")[0] in stdlib | {"__future__"} | own, (name, module)
        assert "StrEnum" not in source and "tomllib" not in source, name


# --- routing parity --------------------------------------------------------------

_SAMPLE_TOOLS = (
    "Bash", "Write", "Edit", "MultiEdit", "NotebookEdit", "AskUserQuestion", "Skill", "SlashCommand",
    "Read", "Grep", "Glob", "WebFetch", "Task", "BashOutput", "apply_patch",
    "mcp__plugin_probe-research_probe-research__search", "mcp__probe_research__run_list", "mcp__other__x", "",
)


def _tools() -> list[str]:
    """The sample, plus every name any route's matcher spells out."""
    named = {
        word
        for plugin in PLUGINS
        for groups in _wiring(plugin)["hooks"].values()
        for group in groups
        for word in re.findall(r"[A-Za-z][A-Za-z0-9_]+", group.get("matcher") or "")
    }
    return sorted(set(_SAMPLE_TOOLS) | named)


def _registered(groups: list, tool: str) -> collections.Counter:
    return collections.Counter(
        h["command"] for g in groups if dispatch.matches(g.get("matcher"), tool) for h in g["hooks"]
    )


@pytest.mark.parametrize("plugin", PLUGINS)
@pytest.mark.parametrize("tool", _tools())
def test_routing_parity(plugin, tool):
    """CRITICAL. For every event and tool: the routes the frozen entries reach,
    counted with repeats, equal what registering routes.json directly would run.
    A lane typo or a route reached twice fails here."""
    hooks = AGENT / "plugins" / plugin / "hooks"
    wiring = _json(hooks / "routes.json")
    entries = _json(hooks / "hooks.json")["hooks"]
    for event, groups in wiring["hooks"].items():
        expected = _registered(groups, tool)
        lanes = [_lane(hook["command"]) for entry in entries.get(event, []) for hook in entry["hooks"]]
        if not lanes:
            # An event no entry has (Kimi's TurnStarted): its adapter lane runs it.
            lanes = [lane for lane in dispatch.ADAPTER_LANES if dispatch.LANE_EVENT[lane] == event]
            assert lanes, f"{plugin} {event}: no entry and no adapter lane would ever run these routes"
        got = collections.Counter()
        for lane in lanes:
            payload = {"tool_name": tool} if tool else {}
            got.update(h["command"] for h in dispatch.routes(lane, payload, wiring))
        assert got == expected, f"{plugin} {event} {tool!r}"


@pytest.mark.parametrize("plugin", PLUGINS)
def test_the_tool_lanes_only_catch_all_is_the_gated_reads_route(plugin):
    """The dispatcher skips a tool call no route's matcher names, and drops a
    catch-all route on post-tool when no daemon message waits: both hold only
    while the tool lanes' one catch-all is the reads route behind that gate."""
    for event in TOOL_EVENTS:
        for group in _wiring(plugin)["hooks"][event]:
            if not group.get("matcher"):
                commands = [h["command"] for h in group["hooks"]]
                assert event == "PostToolUse" and all(
                    c.startswith("/bin/bash -c 'SID=") and "reads_hook.py" in c for c in commands
                ), f"{plugin} {event}: a catch-all tool route the dispatcher would skip"


def _tool_payload(tool: str, **extra) -> bytes:
    return json.dumps({"session_id": SID, "tool_name": tool, "tool_input": {"x": 1}, **extra}).encode()


@pytest.mark.parametrize("plugin", PLUGINS)
def test_the_byte_filter_goes_on_for_exactly_the_tools_a_route_matches(plugin):
    """TOOL_FILTER against routes.json's matchers: never skip a tool a route
    takes (a guard bypass), never start for one none takes (the cost on every
    Read, Grep and Glob). A new tool route needs its name in TOOL_FILTER."""
    wiring = _wiring(plugin)
    for lane, event in (("pre-tool", "PreToolUse"), ("post-tool", "PostToolUse")):
        for tool in _tools():
            wanted = any(g.get("matcher") and dispatch.matches(g["matcher"], tool) for g in wiring["hooks"][event])
            assert dispatch.could_route(lane, _tool_payload(tool)) is wanted, (lane, tool)


def test_file_contents_cannot_fake_a_tool_name_but_a_nested_key_only_adds_one():
    faked = _tool_payload("Read", tool_response={"content": 'x "tool_name": "Bash" y probe-research'})
    assert dispatch.named_tools(faked) == {"Read"}
    assert dispatch.could_route("pre-tool", faked) is False
    nested = _tool_payload("mcp__other__x", tool_input={"tool_name": "Bash"})
    assert dispatch.named_tools(nested) == {"mcp__other__x", "Bash"}
    assert dispatch.could_route("pre-tool", nested) is True, "a superset: never skip a real name"


def test_an_escaped_key_is_parsed_not_guessed():
    assert dispatch.could_route("pre-tool", b'{"tool\\u005fname": "Bash"}') is True


def test_a_projects_own_modules_never_run_in_the_dispatcher(tmp_path):
    """`python3 -c` puts the working directory first on sys.path; the
    bootstrap replaces it before importing anything but the builtin sys."""
    project = tmp_path / "project"
    project.mkdir()
    marker = tmp_path / "hijacked"
    for name in ("os", "json", "dispatch", "io", "re"):
        (project / f"{name}.py").write_text(f"open({str(marker)!r}, 'a').write({name!r})\nraise SystemExit(2)\n", encoding="utf-8")
    root = _plugin(tmp_path, _routes("Stop", "stop", _shell("cat >/dev/null; echo ran")))
    result = subprocess.run(["/bin/bash", str(root / "hooks" / "dispatch.sh"), "stop"], input="{}", capture_output=True,
                            text=True, env=_env(tmp_path, root, False), cwd=project, timeout=30)
    assert (result.returncode, result.stdout) == (0, "ran\n")
    assert not marker.exists()


def test_an_unguarded_tool_call_with_a_huge_payload_stays_cheap(tmp_path):
    payload = _tool_payload("Read", tool_response={"content": "y" * 5_000_000})
    env = {"PATH": os.environ["PATH"], "HOME": str(tmp_path), "XDG_STATE_HOME": str(tmp_path / "xdg"), "CLAUDE_PLUGIN_ROOT": str(FULL.parent)}
    started = time.monotonic()
    result = subprocess.run(["/bin/bash", str(FULL / "dispatch.sh"), "post-tool"], input=payload, capture_output=True, env=env, timeout=30)
    assert result.returncode == 0 and result.stdout == b""
    assert time.monotonic() - started < 1.0


# --- the exact plain-route shape ---------------------------------------------------


def test_every_python_route_is_recognized_and_nothing_else_is():
    """The in-process path rebuilds a route byte for byte; a route it does not
    recognise falls back to exec, which is always safe. These are the ones it
    must recognise (a lone pre-tool route is on every guarded call's path)."""
    for plugin in PLUGINS:
        for event, groups in _wiring(plugin)["hooks"].items():
            for group in groups:
                for hook in group["hooks"]:
                    command = hook["command"]
                    gated = command.startswith("/bin/bash -c 'SID=") or "FLAG=" in command
                    shell = re.search(r'hooks/[a-z-]+\.sh"', command) is not None
                    parts = dispatch.plain_route(command)
                    assert (parts is None) == (gated or shell), f"{plugin} {event}: {command[-60:]}"


_STUB = """import json, os, sys
print(json.dumps({
    "argv": sys.argv[1:],
    "file": os.path.basename(sys.argv[0]),
    "stdin": sys.stdin.read(),
    "env": {k: os.environ.get(k) for k in ("PROBE_AGENT", "PROBE_PLUGIN_PROFILE", "PROBE_HOOK_EVENT")},
}))
"""


#: D20: every event these tests send runs twice over, here (the dispatcher
#: itself) and in the warm hook host (`zygote.py`, plan A0), and must come out
#: the same. `hosting` picks; `_dispatch` starts the host a plugin needs.
_MODE = {"hosted": False}
_HOSTS: dict = {}


@pytest.fixture(autouse=True, params=["here", "hosted"])
def hosting(request):
    _MODE["hosted"] = request.param == "hosted"
    yield request.param
    _MODE["hosted"] = False
    for proc, path in _HOSTS.values():
        proc.kill()
        proc.wait()
        # Its socket and its key (#3355) live in this machine's real
        # `/tmp/probe-<uid>`: none is left behind.
        for leftover in (path, path[: -len(".sock")] + ".key"):
            if os.path.lexists(leftover):
                os.unlink(leftover)
    _HOSTS.clear()


def _host_for(root: Path) -> None:
    key = str(root.resolve())
    if key in _HOSTS or not (root / "hooks" / "zygote.py").exists():
        return
    path = dispatch.host_socket(str(root))
    proc = subprocess.Popen([sys.executable, "-S", str(root / "hooks" / "zygote.py"), path, str(os.getpid())])
    _HOSTS[key] = (proc, path)
    deadline = time.monotonic() + 10
    while not os.path.exists(path):
        # A plugin a test broke on purpose has no host to start: its events
        # run here, as they would for anyone.
        if proc.poll() is not None:
            return
        assert time.monotonic() < deadline, "the hook host never listened"
        time.sleep(0.02)


def _plugin(tmp_path: Path, routes: dict, scripts: dict[str, str] | None = None) -> Path:
    root = tmp_path / "plugin"
    hooks = root / "hooks"
    hooks.mkdir(parents=True)
    for name in ("dispatch.py", "dispatch.sh", "zygote.py", "_service_paths.py"):
        shutil.copy2(FULL / name, hooks / name)
    (hooks / "routes.json").write_text(json.dumps(routes), encoding="utf-8")
    for name, body in (scripts or {}).items():
        (hooks / name).write_text(body, encoding="utf-8")
        (hooks / name).chmod(0o755)
    return root


def _env(tmp_path: Path, root: Path, codex: bool, **extra: str) -> dict:
    env = {"PATH": os.environ["PATH"], "HOME": str(tmp_path / "home"), "XDG_STATE_HOME": str(tmp_path / "xdg")}
    env["PLUGIN_ROOT" if codex else "CLAUDE_PLUGIN_ROOT"] = str(root)
    if not _MODE["hosted"]:
        env["PROBE_HOOK_HOST"] = "off"
    env.update(extra)
    return env


def _dispatch(root: Path, lane: str, payload, env: dict, timeout: float = 30) -> subprocess.CompletedProcess:
    if _MODE["hosted"]:
        _host_for(root)
    data = payload if isinstance(payload, (str, bytes)) else json.dumps(payload)
    return subprocess.run(
        ["/bin/bash", str(root / "hooks" / "dispatch.sh"), lane],
        input=data, capture_output=True, text=isinstance(data, str), env=env, timeout=timeout,
    )


def _plain_routes():
    seen = {}
    for plugin in PLUGINS:
        for event, groups in _wiring(plugin)["hooks"].items():
            for group in groups:
                for hook in group["hooks"]:
                    if dispatch.plain_route(hook["command"]):
                        seen.setdefault(hook["command"], (plugin, event, group["lane"], group.get("matcher")))
    return [(command, *where) for command, where in seen.items()]


@pytest.mark.parametrize("codex", [False, True], ids=["claude-code", "codex"])
@pytest.mark.parametrize(("command", "plugin", "event", "lane", "matcher"), _plain_routes(), ids=lambda v: str(v)[-40:])
def test_a_lone_route_in_process_sees_what_its_bash_line_gives(tmp_path, codex, command, plugin, event, lane, matcher):
    """ENV PARITY. The same stub behind the same route, run by its own bash
    line and by the dispatcher's in-process path: argv, stdin (CRs included)
    and every PROBE_* the line exports must match exactly, under both harnesses."""
    script = dispatch.plain_route(command)[1]
    group = {"lane": lane, "hooks": [{"type": "command", "command": command}]}
    if matcher:
        group["matcher"] = matcher
    root = _plugin(tmp_path, {"hooks": {event: [group]}}, {script: _STUB})
    # The first tool the route's matcher accepts (every existing route keeps the
    # tool it had; `^WebSearch$` is the papers hook's, `^Skill$` the skills refresh's).
    tool = next(t for t in ("Bash", "AskUserQuestion", "Write", "WebSearch", "Skill")
                if not matcher or dispatch.matches(matcher, t))
    payload = '{"session_id": "%s", "hook_event_name": "%s",\r\n "tool_name": "%s"}\n' % (SID, event, tool)
    env = _env(tmp_path, root, codex)
    direct = subprocess.run(["/bin/bash", "-c", command], input=payload, capture_output=True, text=True, env=env, timeout=30)
    via = _dispatch(root, lane, payload, env)
    assert direct.returncode == via.returncode == 0, (direct.stderr, via.stderr)
    assert json.loads(via.stdout) == json.loads(direct.stdout)


def test_a_lone_plain_route_runs_in_the_dispatchers_process(tmp_path):
    """A second interpreter start on every guarded tool call is what the
    in-process path exists to avoid: only the dispatcher runs with -S."""
    command = dispatch._plain_command([], "site_flag.py", False, [])
    root = _plugin(tmp_path, {"hooks": {"PreToolUse": [{"lane": "pre-tool", "matcher": "^Bash$", "hooks": [{"type": "command", "command": command}]}]}},
                   {"site_flag.py": "import sys\nsys.stdin.read()\nprint(sys.flags.no_site)\n"})
    result = _dispatch(root, "pre-tool", {"tool_name": "Bash"}, _env(tmp_path, root, False))
    assert result.stdout.strip() == "1", "exec'd, not in-process"


def test_the_in_process_route_keeps_its_exit_and_its_traceback(tmp_path):
    command = dispatch._plain_command([], "boom.py", False, [])
    routes = {"hooks": {"PreToolUse": [{"lane": "pre-tool", "matcher": "^Bash$", "hooks": [{"type": "command", "command": command}]}]}}
    root = _plugin(tmp_path, routes, {"boom.py": "import sys\nprint('half')\nsys.exit(2)\n"})
    vetoed = _dispatch(root, "pre-tool", {"tool_name": "Bash"}, _env(tmp_path, root, False))
    assert (vetoed.returncode, vetoed.stdout.strip()) == (2, "half"), "a route's veto is its own to cast"
    (root / "hooks" / "boom.py").write_text("raise RuntimeError('broken route')\n", encoding="utf-8")
    broken = _dispatch(root, "pre-tool", {"tool_name": "Bash"}, _env(tmp_path, root, False))
    assert broken.returncode == 1 and "broken route" in broken.stderr, "as `python3 <route>` would fail"


@pytest.mark.parametrize("shape", ["in-process", "exec"])
def test_a_lone_route_is_bounded_by_its_own_timeout(tmp_path, shape):
    """The harness used to kill a hook at its own timeout; the frozen entry's is
    longer, so the dispatcher must do it."""
    if shape == "in-process":
        hook = {"type": "command", "command": dispatch._plain_command([], "slow.py", False, []), "timeout": 1}
        scripts = {"slow.py": "import time\ntime.sleep(5)\nprint('late')\n"}
    else:
        hook = _shell("cat >/dev/null; sleep 5; echo late", timeout=1)
        scripts = None
    root = _plugin(tmp_path, {"hooks": {"PreToolUse": [{"lane": "pre-tool", "matcher": "^Bash$", "hooks": [hook]}]}}, scripts)
    started = time.monotonic()
    result = _dispatch(root, "pre-tool", {"tool_name": "Bash"}, _env(tmp_path, root, False))
    assert time.monotonic() - started < 2.5 and "late" not in result.stdout
    assert result.returncode != 2, "a timeout is never a veto"


def test_a_lone_shell_route_gets_and_gives_its_bytes_unchanged(tmp_path):
    command = "/bin/bash -c 'cat'"
    root = _plugin(tmp_path, {"hooks": {"Stop": [{"lane": "stop", "hooks": [{"type": "command", "command": command}]}]}})
    for body in ('{"small": 1}', '{"trailing": 1}\n\n', json.dumps({"big": "x" * 300_000})):
        result = _dispatch(root, "stop", body, _env(tmp_path, root, False))
        assert (result.returncode, result.stdout) == (0, body)
    tool = _plugin(tmp_path / "tool", {"hooks": {"PreToolUse": [{"lane": "pre-tool", "matcher": "^Bash$", "hooks": [{"type": "command", "command": command}]}]}})
    body = '{"tool_name": "Bash", "x": "y"}\n\n'
    assert _dispatch(tool, "pre-tool", body, _env(tmp_path, tool, False)).stdout == body, "the shell fast path keeps every byte"


def test_a_route_gets_back_the_signals_python_ignores(tmp_path):
    """A pipeline in a route stops quietly on SIGPIPE, as it did under bash."""
    command = "/bin/bash -c 'cat >/dev/null; yes | head -1 >/dev/null; echo done'"
    root = _plugin(tmp_path, {"hooks": {"Stop": [{"lane": "stop", "hooks": [{"type": "command", "command": command}]}]}})
    result = _dispatch(root, "stop", {}, _env(tmp_path, root, False))
    assert (result.stdout.strip(), result.stderr) == ("done", "")


# --- several routes ------------------------------------------------------------------


@pytest.mark.parametrize("shape", ["in-process", "exec"])
def test_a_route_s_probe_commands_know_the_event_s_deadline(tmp_path, shape):
    """A `probe` a route runs waits for an update in progress only until the
    hook must be done (plan D12): the dispatcher says when, in PROBE_HOOK_DEADLINE."""
    if shape == "in-process":
        hook = {"type": "command", "command": dispatch._plain_command([], "when.py", False, []), "timeout": 4}
        scripts = {"when.py": "import os, sys\nsys.stdin.read()\nprint(os.environ['PROBE_HOOK_DEADLINE'])\n"}
    else:
        hook = _shell('cat >/dev/null; echo "$PROBE_HOOK_DEADLINE"', timeout=4)
        scripts = None
    root = _plugin(tmp_path, {"hooks": {"PreToolUse": [{"lane": "pre-tool", "matcher": "^Bash$", "hooks": [hook]}]}}, scripts)
    started = time.time()
    result = _dispatch(root, "pre-tool", {"tool_name": "Bash"}, _env(tmp_path, root, False))
    deadline = float(result.stdout.strip())
    limit = 4 if shape == "in-process" else dispatch.budget("pre-tool")
    assert started < deadline <= time.time() + limit + 0.5


def _shell(body: str, timeout: int | None = 5) -> dict:
    hook = {"type": "command", "command": f"/bin/bash -c '{body}'"}
    if timeout is not None:
        hook["timeout"] = timeout
    return hook


def _routes(event: str, lane: str, *hooks: dict) -> dict:
    return {"hooks": {event: [{"lane": lane, "hooks": list(hooks)}]}}


def _context(text: str) -> str:
    return json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": text}}).replace('"', '\\"')


def test_several_routes_run_in_parallel_and_merge_in_order(tmp_path):
    routes = _routes(
        "UserPromptSubmit", "prompt",
        _shell(f'cat >/dev/null; sleep 1; echo "{_context("one")}"'),
        _shell(f'cat >/dev/null; sleep 1; echo "{_context("two")}"'),
        _shell('cat >/dev/null; echo "{\\"systemMessage\\": \\"hi\\"}"'),
    )
    root = _plugin(tmp_path, routes)
    started = time.monotonic()
    result = _dispatch(root, "prompt", {"session_id": SID}, _env(tmp_path, root, False))
    elapsed = time.monotonic() - started
    assert result.returncode == 0, result.stderr
    out = json.loads(result.stdout)
    assert out["hookSpecificOutput"]["additionalContext"] == "one\n\ntwo"
    assert out["systemMessage"] == "hi"
    assert elapsed < 1.9, f"{elapsed:.2f}s: the two 1s routes did not run in parallel"


def test_every_parallel_route_reads_the_whole_payload(tmp_path):
    payload = json.dumps({"session_id": SID, "pad": "x" * 200_000})
    root = _plugin(tmp_path, _routes("UserPromptSubmit", "prompt", *[_shell("wc -c") for _ in range(3)]))
    result = _dispatch(root, "prompt", payload, _env(tmp_path, root, False))
    context = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
    assert [c.strip() for c in context.split("\n\n")] == [str(len(payload.encode()))] * 3


def test_routes_slower_to_read_than_a_poll_still_get_the_whole_payload(tmp_path):
    """The real routes import for ~50ms before they read stdin."""
    payload = json.dumps({"session_id": SID, "pad": "x" * 300_000})
    root = _plugin(tmp_path, _routes("UserPromptSubmit", "prompt", *[_shell("sleep 0.3; wc -c") for _ in range(2)]))
    started = time.monotonic()
    result = _dispatch(root, "prompt", payload, _env(tmp_path, root, False))
    assert time.monotonic() - started < 2
    context = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
    assert [c.strip() for c in context.split("\n\n")] == [str(len(payload.encode()))] * 2


def test_a_slow_route_is_killed_with_what_it_started_and_the_rest_still_print(tmp_path):
    marker = tmp_path / "survived"
    routes = _routes(
        "UserPromptSubmit", "prompt",
        _shell(f"cat >/dev/null; (sleep 3; touch {marker}) & wait", timeout=1),
        _shell("cat >/dev/null; echo on-time"),
        _shell('cat >/dev/null; echo "{\\"systemMessage\\": \\"also\\"}"'),
    )
    root = _plugin(tmp_path, routes)
    started = time.monotonic()
    result = _dispatch(root, "prompt", {}, _env(tmp_path, root, False))
    assert time.monotonic() - started < 2.5
    out = json.loads(result.stdout)
    assert out["hookSpecificOutput"]["additionalContext"] == "on-time" and out["systemMessage"] == "also"
    time.sleep(3.5)
    assert not marker.exists(), "the overrun route's process group was left running"


def test_a_route_that_exits_counts_even_if_what_it_started_holds_its_output(tmp_path):
    routes = _routes(
        "UserPromptSubmit", "prompt",
        _shell("cat >/dev/null; echo A-done; (sleep 6) &", timeout=5),
        _shell("cat >/dev/null; echo B-done"),
    )
    root = _plugin(tmp_path, routes)
    started = time.monotonic()
    result = _dispatch(root, "prompt", {}, _env(tmp_path, root, False))
    assert time.monotonic() - started < 2, "waited on a pipe the route no longer owns"
    assert json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"] == "A-done\n\nB-done"


def test_a_failing_route_contributes_nothing_and_a_veto_still_vetoes(tmp_path):
    routes = _routes("UserPromptSubmit", "prompt", _shell("cat >/dev/null; echo garbage; exit 1"), _shell("cat >/dev/null; echo kept"))
    root = _plugin(tmp_path, routes)
    result = _dispatch(root, "prompt", {}, _env(tmp_path, root, False))
    assert (result.returncode, result.stdout.strip()) == (0, "kept")
    routes["hooks"]["UserPromptSubmit"][0]["hooks"].append(_shell("cat >/dev/null; echo no >&2; exit 2"))
    (root / "hooks" / "routes.json").write_text(json.dumps(routes), encoding="utf-8")
    vetoed = _dispatch(root, "prompt", {}, _env(tmp_path, root, False))
    assert vetoed.returncode == 2 and "no" in vetoed.stderr


def test_a_stopped_dispatcher_takes_its_routes_with_it(tmp_path):
    marker = tmp_path / "orphan"
    routes = _routes("UserPromptSubmit", "prompt", _shell(f"cat >/dev/null; sleep 3; touch {marker}"), _shell("cat >/dev/null; sleep 3"))
    root = _plugin(tmp_path, routes)
    proc = subprocess.Popen(["/bin/bash", str(root / "hooks" / "dispatch.sh"), "prompt"], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=_env(tmp_path, root, False))
    proc.stdin.write(b"{}")
    proc.stdin.close()
    time.sleep(0.8)
    proc.send_signal(signal.SIGTERM)
    proc.wait(timeout=5)
    time.sleep(3)
    assert not marker.exists(), "a route outlived the dispatcher bounding it"


@pytest.mark.parametrize(
    ("codex", "extra", "bound"),
    [(False, {"CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS": "800"}, 1.2), (False, {}, 1.8), (True, {}, 3.0)],
    ids=["claude-code-800ms", "claude-code-default", "codex"],
)
def test_session_end_ends_its_routes_inside_the_harness_budget(tmp_path, codex, extra, bound):
    """Claude Code cancels the whole SessionEnd phase at its budget (1.5s by
    default; the plugin's timeout does not count), Codex at 3s, and cancelling
    kills the hooks. The dispatcher returns before then and takes the routes."""
    marker = tmp_path / "finished"
    routes = _routes("SessionEnd", "session-end", _shell(f"cat >/dev/null; sleep 3.5; touch {marker}", timeout=3), _shell("cat >/dev/null; true", timeout=3))
    root = _plugin(tmp_path, routes)
    started = time.monotonic()
    result = _dispatch(root, "session-end", {}, _env(tmp_path, root, codex, **extra))
    assert result.returncode == 0
    assert time.monotonic() - started < bound
    time.sleep(4)
    assert not marker.exists(), "a SessionEnd route outlived the harness's budget"


def test_the_codex_session_end_budget_leaves_room_for_what_runs_after_it(monkeypatch):
    """Codex kills the hook at CODEX_SESSION_END_S, counted from before this
    process starts. After the budget runs out the dispatcher still waits
    KILL_WAIT_S for a killed route and JOIN_SLACK_S on the join; with startup
    (STARTUP_ALLOWANCE_S) that has to end before the kill. It did not at 2.8s."""
    monkeypatch.setenv("PLUGIN_ROOT", "/plugin")
    codex = dispatch.budget("session-end")
    assert dispatch.STARTUP_ALLOWANCE_S >= 0.2, "an allowance below the measured cold start proves nothing"
    assert codex + dispatch.KILL_WAIT_S + dispatch.JOIN_SLACK_S < dispatch.CODEX_SESSION_END_S - dispatch.STARTUP_ALLOWANCE_S
    # Claude Code's is unchanged: 1.5s default less SESSION_END_MARGIN_S.
    monkeypatch.delenv("PLUGIN_ROOT")
    monkeypatch.delenv("CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS", raising=False)
    assert dispatch.budget("session-end") == pytest.approx(1.3)


@pytest.mark.parametrize("raw", ["", "soon", "²", "0", "-5", "99999999999999999999999"])
def test_a_session_end_budget_never_crashes(monkeypatch, raw):
    monkeypatch.delenv("PLUGIN_ROOT", raising=False)
    monkeypatch.setenv("CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS", raw)
    assert dispatch.budget("session-end") > 0


# --- matching ------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("matcher", "tool", "expected"),
    [
        (None, "Read", True), ("", "Read", True), ("*", "Bash", True),
        ("Bash", "Bash", True), ("Bash", "BashOutput", False), ("Edit|Write", "Write", True), ("Edit", "MultiEdit", False),
        ("^Bash$|probe[-_]research", "mcp__plugin_probe-research_probe-research__x", True),
        ("^(Write|Edit)$", "MultiEdit", False), ("Notebook.*", "NotebookEdit", True), ("[unclosed", "Bash", False),
    ],
)
def test_matching_reads_a_matcher_as_the_harness_does(matcher, tool, expected):
    assert dispatch.matches(matcher, tool) is expected


# --- MERGE ---------------------------------------------------------------------------

_PROMPT = "UserPromptSubmit"


def _decision(value, reason):
    return json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": value, "permissionDecisionReason": reason}})


@pytest.mark.parametrize(
    ("event", "outputs", "expected"),
    [
        (_PROMPT, [""], ""),
        (_PROMPT, ["", '{"continue": true}\n'], '{"continue": true}\n'),
        (_PROMPT, ["not json at all"], "not json at all"),
        (_PROMPT, ['{"a": 1}', "plain text"], {"a": 1, "hookSpecificOutput": {"hookEventName": _PROMPT, "additionalContext": "plain text"}}),
        ("Stop", ['{"systemMessage": "a"}', "plain text"], {"systemMessage": "a"}),
        (_PROMPT, ['{"continue": true}', '{"continue": false, "stopReason": "x"}'], {"continue": False, "stopReason": "x"}),
        (_PROMPT, ['{"systemMessage": "a"}', '{"systemMessage": "b"}'], {"systemMessage": "a\nb"}),
        ("Stop", ['{"decision": "block", "reason": "r1"}', '{"decision": "approve"}'], {"decision": "block", "reason": "r1"}),
    ],
    ids=["empty", "one-passes-through", "plain-passes-through", "plain-is-context", "stop-takes-no-specific-output",
         "continue-false-wins", "messages-join", "block-wins"],
)
def test_merge(event, outputs, expected):
    merged = dispatch.merge(event, outputs)
    if isinstance(expected, str):
        assert merged == expected
    else:
        assert json.loads(merged) == expected


def test_merge_never_loses_a_denial():
    merged = json.loads(dispatch.merge("PreToolUse", [_decision("allow", "fine"), _decision("deny", "guard"), _decision("ask", "q"), _decision("deny", "second")]))
    out = merged["hookSpecificOutput"]
    assert (out["permissionDecision"], out["permissionDecisionReason"]) == ("deny", "guard\n\nsecond")


def test_merge_keeps_the_winning_reason_whatever_wins():
    context = json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": "c"}})
    out = json.loads(dispatch.merge("PreToolUse", [_decision("ask", "confirm X"), context]))["hookSpecificOutput"]
    assert (out["permissionDecision"], out.get("permissionDecisionReason")) == ("ask", "confirm X")


def test_one_malformed_output_costs_no_other_its_denial():
    odd = json.dumps({"hookSpecificOutput": {"permissionDecision": ["deny"]}})
    out = json.loads(dispatch.merge("PreToolUse", ['{"systemMessage": "x"}', odd, _decision("deny", "guard")]))
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_a_merge_failure_prints_a_veto_first(tmp_path):
    deny = _decision("deny", "guard").replace('"', '\\"')
    routes = _routes("UserPromptSubmit", "prompt", _shell("cat >/dev/null; echo first"), _shell(f'cat >/dev/null; echo "{deny}"'))
    root = _plugin(tmp_path, routes)
    source = (root / "hooks" / "dispatch.py").read_text(encoding="utf-8")
    broken = source.replace(
        '    present = [o for o in outputs if o.strip()]\n    if len(present) <= 1:',
        '    raise RuntimeError("merge bug")\n    if len(present) <= 1:',
    )
    assert broken != source
    (root / "hooks" / "dispatch.py").write_text(broken, encoding="utf-8")
    result = _dispatch(root, "prompt", {}, _env(tmp_path, root, False))
    assert result.returncode == 0 and json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"] == "deny"


# --- fail-open --------------------------------------------------------------------------


@pytest.mark.parametrize("payload", ["", "not json", "[1, 2]", '{"tool_name": 7}'])
def test_odd_payloads_still_run_matcherless_routes(tmp_path, payload):
    root = _plugin(tmp_path, _routes("Stop", "stop", _shell("cat >/dev/null; echo ran")))
    result = _dispatch(root, "stop", payload, _env(tmp_path, root, False))
    assert (result.returncode, result.stdout, result.stderr) == (0, "ran\n", "")


@pytest.mark.parametrize("payload", ["", "not json", '{"tool_name": 7}', '{"tool_name": "Read"}'])
def test_odd_tool_payloads_run_no_guard(tmp_path, payload):
    root = _plugin(tmp_path, {"hooks": {"PreToolUse": [{"lane": "pre-tool", "matcher": "^Bash$", "hooks": [_shell("cat >/dev/null; echo ran")]}]}})
    result = _dispatch(root, "pre-tool", payload, _env(tmp_path, root, False))
    assert (result.returncode, result.stdout) == (0, "")


def test_an_unknown_lane_or_unreadable_routes_abstain(tmp_path):
    root = _plugin(tmp_path, _routes("Stop", "stop", _shell("cat >/dev/null; echo ran")))
    assert _dispatch(root, "nonsense", {}, _env(tmp_path, root, False)).stdout == ""
    (root / "hooks" / "routes.json").write_text("{broken", encoding="utf-8")
    result = _dispatch(root, "stop", {}, _env(tmp_path, root, False))
    assert (result.returncode, result.stdout) == (0, "")


@pytest.mark.parametrize("damage", ["missing", "unreadable", "half-written"])
@pytest.mark.parametrize("lane", ["pre-tool", "prompt", "stop"])
def test_a_half_installed_plugin_never_vetoes(tmp_path, lane, damage):
    """A version folder mid-delete (or a checkout mid-switch) can hold
    dispatch.sh with dispatch.py gone, unreadable or cut short; python3's own
    exit for a script it cannot open is 2, a veto."""
    if damage == "unreadable" and os.geteuid() == 0:
        pytest.skip("root reads anything")
    root = _plugin(tmp_path, _routes("Stop", "stop", _shell("cat >/dev/null; echo ran")))
    target = root / "hooks" / "dispatch.py"
    if damage == "missing":
        target.unlink()
    elif damage == "unreadable":
        target.chmod(0)
    else:
        target.write_text(target.read_text(encoding="utf-8")[:900], encoding="utf-8")
    try:
        result = _dispatch(root, lane, {"tool_name": "Bash"}, _env(tmp_path, root, False))
    finally:
        target.chmod(0o644) if target.exists() else None
    assert (result.returncode, result.stdout) == (0, "")


# --- the reads fast path ------------------------------------------------------------------


def _reads_states():
    """(name, env-sid, files under probe/reads) — the states the route's gate reads."""
    msg = "{}"
    return [
        ("nothing", SID, {}),
        ("mine", SID, {f"messages/{SID}/0001.json": msg}),
        ("another-session", SID, {"messages/other/0001.json": msg}),
        ("status-new", SID, {f"status/{SID}.json": msg}),
        ("status-shown", SID, {f"status/{SID}.json": msg, f"status/{SID}.shown": ""}),
        ("no-sid-nothing", "", {}),
        ("no-sid-any", "", {"messages/other/0001.json": msg}),
        # A service claim its caller never received (plan Q2): it waits too.
        ("orphaned-claim", SID, {f"claimed/{SID}/0001-r1.1700000000000_ab.json": msg}),
        ("no-sid-orphaned-claim", "", {"claimed/other/0001-r1.1700000000000_ab.json": msg}),
        ("received-claim", SID, {f"claimed/{SID}/0001-r1.json": msg}),
    ]


@pytest.mark.parametrize(("state", "sid", "files"), _reads_states(), ids=[s[0] for s in _reads_states()])
def test_the_reads_fast_path_passes_whenever_the_route_would(tmp_path, state, sid, files):
    """dispatch.sh copies the reads route's shell gate so no python starts on
    an unguarded tool call. A stricter copy would silently drop daemon messages."""
    route = next(
        h["command"]
        for g in _json(FULL / "routes.json")["hooks"]["PostToolUse"]
        if not g.get("matcher")
        for h in g["hooks"]
    )
    stub = "import sys\nsys.stdin.read()\nprint('reads ran')\n"
    root = _plugin(tmp_path, {"hooks": {"PostToolUse": [{"lane": "post-tool", "hooks": [{"type": "command", "command": route}]}]}},
                   {"reads_hook.py": stub})
    reads = tmp_path / "xdg" / "probe" / "reads"
    for rel, body in files.items():
        (reads / rel).parent.mkdir(parents=True, exist_ok=True)
        (reads / rel).write_text(body, encoding="utf-8")
    if f"status/{SID}.shown" in files:
        later = time.time() + 5
        os.utime(reads / f"status/{SID}.shown", (later, later))
    env = _env(tmp_path, root, False, CLAUDE_CODE_SESSION_ID=sid)
    payload = json.dumps({"tool_name": "Read"})
    direct = subprocess.run(["/bin/bash", "-c", route], input=payload, capture_output=True, text=True, env=env, timeout=30)
    via = _dispatch(root, "post-tool", payload, env)
    assert via.stdout == direct.stdout, state


def _serve(root: Path, argv: list, payload, env: dict) -> subprocess.CompletedProcess:
    """The dispatcher as `harness_io.py --event` calls it (`serve`, options after
    the lane, which dispatch.sh never passes), through the host when hosted."""
    if _MODE["hosted"]:
        _host_for(root)
    code = "import sys\nsys.path[0] = sys.argv[1]\nimport dispatch\nsys.exit(dispatch.serve(sys.argv[2:]))\n"
    return subprocess.run([sys.executable, "-S", "-c", code, str(root / "hooks"), *argv],
                          input=json.dumps(payload), capture_output=True, text=True, env=env, timeout=30)


def test_unshown_runs_no_catch_all_after_a_tool_call_even_with_a_message_waiting(tmp_path):
    """Kimi drops PostToolUse output: there `--unshown` keeps the reads
    catch-all from claiming a daemon message nobody would see. The routes the
    tool's matcher takes run either way, and nothing else changes."""
    reads = next(
        h["command"]
        for g in _json(FULL / "routes.json")["hooks"]["PostToolUse"]
        if not g.get("matcher")
        for h in g["hooks"]
    )
    say = "import json, sys\nsys.stdin.read()\nprint(json.dumps({'hookSpecificOutput': {'additionalContext': %r}}))\n"
    routes = {"hooks": {"PostToolUse": [
        {"lane": "post-tool", "matcher": "^Bash$",
         "hooks": [_shell('ROOT="${CLAUDE_PLUGIN_ROOT:-}"; exec python3 "$ROOT/hooks/tool.py"')]},
        {"lane": "post-tool", "hooks": [{"type": "command", "command": reads}]},
    ]}}
    root = _plugin(tmp_path, routes, {"tool.py": say % "tool ran", "reads_hook.py": say % "reads ran"})
    waiting = tmp_path / "xdg" / "probe" / "reads" / "messages" / SID / "0001.json"
    waiting.parent.mkdir(parents=True)
    waiting.write_text("{}", encoding="utf-8")
    env = _env(tmp_path, root, False, CLAUDE_CODE_SESSION_ID=SID)
    payload = {"session_id": SID, "hook_event_name": "PostToolUse", "tool_name": "Bash"}

    def context(done):
        assert done.returncode == 0, done.stderr
        return json.loads(done.stdout)["hookSpecificOutput"]["additionalContext"]

    assert context(_serve(root, ["post-tool"], payload, env)) == "tool ran\n\nreads ran"
    assert context(_serve(root, ["post-tool", dispatch.UNSHOWN], payload, env)) == "tool ran"
    assert context(_dispatch(root, "post-tool", payload, env)) == "tool ran\n\nreads ran", "dispatch.sh: unchanged"
    # A tool no route's matcher takes leaves before anything runs, unshown or not.
    read = {**payload, "tool_name": "Read"}
    assert _serve(root, ["post-tool", dispatch.UNSHOWN], read, env).stdout == ""


def test_serve_hands_back_the_status_run_exits_with(tmp_path):
    """`serve` is `run` without the hand-over and the exit: a veto is returned
    (2), not raised, so an adapter can still translate what the routes said."""
    routes = {"hooks": {"PreToolUse": [{"lane": "pre-tool", "matcher": "^Bash$", "hooks": [
        _shell("cat >/dev/null; echo blocked >&2; exit 2"), _shell("cat >/dev/null; echo {}"),
    ]}]}}
    root = _plugin(tmp_path, routes)
    env = _env(tmp_path, root, False)
    payload = {"session_id": SID, "hook_event_name": "PreToolUse", "tool_name": "Bash"}
    served = _serve(root, ["pre-tool"], payload, env)
    run = _dispatch(root, "pre-tool", payload, env)
    assert (served.returncode, served.stdout, served.stderr) == (run.returncode, run.stdout, run.stderr)
    assert served.returncode == 2 and served.stderr.strip() == "blocked"


# --- the heartbeat ---------------------------------------------------------------------------


def test_codex_sessions_leave_the_heartbeat_the_capture_plugin_reads(tmp_path):
    root = _plugin(tmp_path, {"hooks": {}})
    alive = tmp_path / "xdg" / "probe" / "hooks" / "alive"
    _dispatch(root, "stop", {"session_id": SID}, _env(tmp_path, root, True))
    assert not alive.exists(), "only the session-start and prompt lanes write it"
    _dispatch(root, "prompt", {"session_id": "../" + SID}, _env(tmp_path, root, True))
    assert [p.name for p in alive.iterdir()] == [SID], "the same id rule as probe-hooks-trust.sh"
    old = alive / "gone"
    old.touch()
    os.utime(old, (time.time() - dispatch.HEARTBEAT_KEEP_S - 60,) * 2)
    _dispatch(root, "session-start", {"session_id": SID}, _env(tmp_path, root, True))
    assert not old.exists(), "pruned at session start"


def test_claude_code_sessions_leave_none(tmp_path):
    root = _plugin(tmp_path, {"hooks": {}})
    _dispatch(root, "session-start", {"session_id": SID}, _env(tmp_path, root, False))
    assert not (tmp_path / "xdg" / "probe" / "hooks").exists()


def test_the_heartbeat_path_matches_the_capture_plugins_check(tmp_path):
    """The other half of the contract: the tap's prompt hook reads the file this
    writes. Run its real check against a real heartbeat, not a string match."""
    tap = AGENT / "plugins" / "probe-research-tap" / "hooks" / "probe-hooks-trust.sh"
    assert tap.exists(), "the capture plugin's check (#2293) ships with the dispatcher"
    root = _plugin(tmp_path, {"hooks": {}})
    _dispatch(root, "prompt", {"session_id": "../" + SID}, _env(tmp_path, root, True))
    expect = tmp_path / "xdg" / "probe" / "hooks" / "expect"
    expect.mkdir(parents=True)
    (expect / SID).write_text("1\n", encoding="utf-8")
    env = {"PATH": os.environ["PATH"], "HOME": str(tmp_path / "home"), "XDG_STATE_HOME": str(tmp_path / "xdg")}
    heard = subprocess.run(["/bin/bash", "-c", f'. "{tap}"; probe_hooks_nudge "../{SID}" ""'],
                           capture_output=True, text=True, env=env, timeout=10)
    assert heard.stdout == "", "the tap did not see the dispatcher's heartbeat"
    (tmp_path / "xdg" / "probe" / "hooks" / "alive" / SID).unlink()
    heard = subprocess.run(["/bin/bash", "-c", f'. "{tap}"; probe_hooks_nudge "../{SID}" ""'],
                           capture_output=True, text=True, env=env, timeout=10)
    assert "systemMessage" in heard.stdout, "and without one, it speaks"


# --- the hand-over to the installed copy ------------------------------------------------------
#
# Claude Code fixes a session's plugin folder at its start; a session left open
# across releases ran a 0.129.0 guard that refused `probe paper find`, the
# command the current managed block named (2026-10-13). Each event goes to the
# copy the install ledger names instead.

OLD, NEW = "0.129.0", "0.145.0"
MARKET = "research-os-agent"


def _folder(tmp_path: Path, plugin: str = "probe-research") -> Path:
    return tmp_path / "home" / ".claude" / "plugins" / "cache" / MARKET / plugin


def _copy(root: Path, version: str) -> Path:
    """A version folder holding this branch's dispatcher, with a Stop route that
    prints its version and the plugin root it was given."""
    (root / "hooks").mkdir(parents=True)
    for name in ("dispatch.py", "dispatch.sh"):
        shutil.copy2(FULL / name, root / "hooks" / name)
    routes = _routes("Stop", "stop", _shell(f'cat >/dev/null; echo "{version} $CLAUDE_PLUGIN_ROOT"'))
    (root / "hooks" / "routes.json").write_text(json.dumps(routes), encoding="utf-8")
    return root


def _cache(tmp_path: Path, *versions: str, plugin: str = "probe-research") -> list[Path]:
    """Version folders of one plugin as Claude Code caches them."""
    return [_copy(_folder(tmp_path, plugin) / v, v) for v in versions]


def _ledger(tmp_path: Path, *paths, raw: str | None = None, scope: str = "user",
            key: str = f"probe-research@{MARKET}") -> Path:
    ledger = tmp_path / "home" / ".claude" / "plugins" / "installed_plugins.json"
    entries = [{"scope": scope, "installPath": str(p), "version": Path(p).name} for p in paths]
    ledger.write_text(raw if raw is not None else json.dumps({"version": 2, "plugins": {key: entries}}), encoding="utf-8")
    return ledger


@pytest.mark.parametrize("session, installed", [(OLD, NEW), (NEW, OLD)], ids=["upgraded", "rolled-back"])
def test_an_open_session_runs_the_installed_copy(tmp_path, session, installed):
    roots = dict(zip((OLD, NEW), _cache(tmp_path, OLD, NEW)))
    _ledger(tmp_path, roots[installed])
    result = _dispatch(roots[session], "stop", {}, _env(tmp_path, roots[session], False))
    assert (result.returncode, result.stdout) == (0, f"{installed} {roots[installed]}\n"), result.stderr


def test_the_hand_over_comes_before_the_old_copys_own_rules(tmp_path):
    """The incident's shape: the open session's copy does not route the call at
    all (its byte filter and routes predate the rule); the installed one does."""
    old, new = _cache(tmp_path, OLD, NEW)
    source = (old / "hooks" / "dispatch.py").read_text(encoding="utf-8")
    assert 'frozenset(("Bash", ' in source
    (old / "hooks" / "dispatch.py").write_text(source.replace('frozenset(("Bash", ', "frozenset(("), encoding="utf-8")
    deny = tmp_path / "deny.json"
    deny.write_text(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny"}}))
    guard = {"hooks": {"PreToolUse": [{"lane": "pre-tool", "matcher": "Bash", "hooks": [
        _shell(f'cat >/dev/null; cat "{deny}"')]}]}}
    (new / "hooks" / "routes.json").write_text(json.dumps(guard), encoding="utf-8")
    payload = _tool_payload("Bash")
    env = _env(tmp_path, old, False)
    assert _dispatch(old, "pre-tool", payload, env).stdout == b"", "unrouted in the open session's copy"
    _ledger(tmp_path, new)
    assert json.loads(_dispatch(old, "pre-tool", payload, env).stdout)["hookSpecificOutput"]["permissionDecision"] == "deny"


def _stays(tmp_path: Path, case: str):
    """(root, env) for an event that must run in the session's own copy."""
    old, new = _cache(tmp_path, OLD, NEW)
    env = _env(tmp_path, old, False)
    hooks = new / "hooks"
    if case == "no-ledger":
        pass
    elif case == "lists-this-copy":
        _ledger(tmp_path, old)
    elif case == "two-copies":
        _ledger(tmp_path, old, new)
    elif case == "unparseable":
        _ledger(tmp_path, raw='{"plugins": {"x": [{"installPath": "%s"' % new)
    elif case == "a-fifo":
        os.mkfifo(tmp_path / "home" / ".claude" / "plugins" / "installed_plugins.json")
    elif case == "project-scope":
        _ledger(tmp_path, new, scope="project")
    elif case == "another-plugins-key":
        _ledger(tmp_path, new, key=f"probe-research-daemon@{MARKET}")
    elif case == "another-plugins-folder":
        (other,) = _cache(tmp_path, NEW, plugin="probe-research-daemon")
        _ledger(tmp_path, other, key=f"probe-research-daemon@{MARKET}")
    elif case == "symlinked-out-of-the-cache":
        outside = _copy(tmp_path / "elsewhere" / "0.146.0", "0.146.0")
        (_folder(tmp_path) / "0.146.0").symlink_to(outside)
        _ledger(tmp_path, _folder(tmp_path) / "0.146.0")
    elif case == "codex":
        _ledger(tmp_path, new)
        env = _env(tmp_path, old, True)
    elif case == "no-dispatcher-there":
        _ledger(tmp_path, new)
        (hooks / "dispatch.sh").unlink()
    elif case == "dispatch-py-gone":
        _ledger(tmp_path, new)
        (hooks / "dispatch.py").unlink()
    elif case == "dispatch-py-cut-short":
        _ledger(tmp_path, new)
        (hooks / "dispatch.py").write_text((hooks / "dispatch.py").read_text(encoding="utf-8")[:900], encoding="utf-8")
    elif case == "dispatch-py-without-run":
        _ledger(tmp_path, new)
        (hooks / "dispatch.py").write_text("X = 1\n", encoding="utf-8")
    elif case == "routes-broken":
        _ledger(tmp_path, new)
        (hooks / "routes.json").write_text("{broken", encoding="utf-8")
    elif case == "a-routed-script-missing":
        _ledger(tmp_path, new)
        routes = json.loads((hooks / "routes.json").read_text(encoding="utf-8"))
        routes["hooks"]["Stop"][0]["hooks"].append({"type": "command", "command": '/bin/bash -c \'exec "$ROOT/hooks/gone.py"\''})
        (hooks / "routes.json").write_text(json.dumps(routes), encoding="utf-8")
    elif case == "plugin-dir-checkout":
        _ledger(tmp_path, new)
        old = _plugin(tmp_path / "checkout", _routes("Stop", "stop", _shell(f'cat >/dev/null; echo "{OLD} $CLAUDE_PLUGIN_ROOT"')))
        env = _env(tmp_path, old, False)
    return old, env


@pytest.mark.parametrize("case", [
    "no-ledger", "lists-this-copy", "two-copies", "unparseable", "a-fifo", "project-scope",
    "another-plugins-key", "another-plugins-folder", "symlinked-out-of-the-cache", "codex",
    "no-dispatcher-there", "dispatch-py-gone", "dispatch-py-cut-short", "dispatch-py-without-run",
    "routes-broken", "a-routed-script-missing", "plugin-dir-checkout",
])
def test_otherwise_the_event_runs_in_the_sessions_own_copy(tmp_path, case):
    """Nothing to hand to, a copy that is not this plugin's own version folder,
    or one that is not whole (mid-install, mid-delete): the session's own copy,
    which is whole, runs the event."""
    root, env = _stays(tmp_path, case)
    result = _dispatch(root, "stop", {}, env, timeout=10)
    assert (result.returncode, result.stdout) == (0, f"{OLD} {env.get('CLAUDE_PLUGIN_ROOT', '')}\n"), result.stderr


def test_one_copy_listed_under_two_entries_is_still_one_copy(tmp_path):
    old, new = _cache(tmp_path, OLD, NEW)
    _ledger(tmp_path, new, new)
    assert _dispatch(old, "stop", {}, _env(tmp_path, old, False)).stdout == f"{NEW} {new}\n"


def test_an_event_moves_once_and_its_routes_never_see_the_marker(tmp_path):
    old, new = _cache(tmp_path, OLD, NEW)
    _ledger(tmp_path, new)
    seen = tmp_path / "marker-at-hand-over"
    source = (new / "hooks" / "dispatch.py").read_text(encoding="utf-8")
    pop = "    if os.environ.pop(HANDED_OVER, None) is not None:\n"
    assert source.count(pop) == 1
    (new / "hooks" / "dispatch.py").write_text(source.replace(
        pop, f"    open({str(seen)!r}, 'w').write(os.environ.get(HANDED_OVER, ''))\n" + pop), encoding="utf-8")
    (new / "hooks" / "routes.json").write_text(json.dumps(_routes(
        "Stop", "stop", _shell('cat >/dev/null; echo "ran:${PROBE_HOOKS_HANDED_OVER:-}"'))), encoding="utf-8")
    result = _dispatch(old, "stop", {}, _env(tmp_path, old, False))
    assert result.stdout == "ran:\n", result.stderr
    assert seen.read_text(encoding="utf-8") == str(old), "the installed copy was told, so it hands over no further"


def test_a_symlinked_home_still_finds_the_installed_copy(tmp_path):
    old, new = _cache(tmp_path, OLD, NEW)
    _ledger(tmp_path, new)
    (tmp_path / "link").symlink_to(tmp_path / "home")
    via = tmp_path / "link" / old.relative_to(tmp_path / "home")
    result = _dispatch(via, "stop", {}, _env(tmp_path, via, False))
    assert result.stdout == f"{NEW} {new}\n", result.stderr


def test_the_ledger_under_claude_config_dir_wins(tmp_path):
    """Claude Code reads `$CLAUDE_CONFIG_DIR` and never `~/.claude` when it is
    set; a stale ledger in HOME naming this copy must not keep the event here."""
    old, new = _cache(tmp_path, OLD, NEW)
    config = tmp_path / "config"
    (config / "plugins").mkdir(parents=True)
    _ledger(tmp_path, new).rename(config / "plugins" / "installed_plugins.json")
    _ledger(tmp_path, old)
    result = _dispatch(old, "stop", {}, _env(tmp_path, old, False, CLAUDE_CONFIG_DIR=str(config)))
    assert result.stdout == f"{NEW} {new}\n", result.stderr


def test_a_ledger_claude_code_moved_is_the_one_followed(tmp_path):
    """CLAUDE_CODE_PLUGIN_CACHE_DIR moves Claude Code's whole plugins folder,
    the ledger with it: one left under the config dir is not the one it reads."""
    old, new = _cache(tmp_path, OLD, NEW)
    moved = tmp_path / "moved"
    moved.mkdir()
    _ledger(tmp_path, new).rename(moved / "installed_plugins.json")
    _ledger(tmp_path, old)
    result = _dispatch(old, "stop", {}, _env(tmp_path, old, False, CLAUDE_CODE_PLUGIN_CACHE_DIR=str(moved)))
    assert result.stdout == f"{NEW} {new}\n", result.stderr


@pytest.mark.parametrize(("case", "expected"), [
    ("lists-this-copy", True),
    ("this-copy-twice", True),
    ("this-copy-at-project-scope", True),
    ("lists-another", False),
    ("two-copies", False),
    ("not-listed", False),
    ("no-ledger", False),
    ("unparseable", False),
    ("another-plugins-key", False),
])
def test_is_installed_copy(tmp_path, case, expected):
    """Before writing what every session reads: only from the copy the ledger
    names, and from no copy when the ledger names several or none."""
    old, new = _cache(tmp_path, OLD, NEW)
    if case == "lists-this-copy":
        _ledger(tmp_path, new)
    elif case == "this-copy-twice":
        _ledger(tmp_path, new, new)
    elif case == "this-copy-at-project-scope":
        _ledger(tmp_path, new, scope="project")
    elif case == "lists-another":
        _ledger(tmp_path, old)
    elif case == "two-copies":
        _ledger(tmp_path, old, new)
    elif case == "not-listed":
        _ledger(tmp_path, tmp_path / "elsewhere" / NEW)
    elif case == "unparseable":
        _ledger(tmp_path, raw='{"plugins": {"probe-research@%s": [{"installPath": "%s"' % (MARKET, new))
    elif case == "another-plugins-key":
        _ledger(tmp_path, new, key=f"probe-research-daemon@{MARKET}")
    env = {"CLAUDE_CONFIG_DIR": str(tmp_path / "home" / ".claude")}
    assert dispatch.is_installed_copy(str(new), env) is expected


def test_the_usual_event_reads_the_ledger_without_importing_json(tmp_path):
    """Every event reads the ledger; when it lists this copy (the usual answer)
    that costs no `json` import (~10 ms of the ~12 ms an unguarded call costs)."""
    old, _new = _cache(tmp_path, OLD, NEW)
    _ledger(tmp_path, old)
    probe = (
        "import sys; sys.path[0] = sys.argv[1]; import dispatch, os\n"
        "print(dispatch.installed_root(sys.argv[2], os.environ), 'json' in sys.modules)"
    )
    result = subprocess.run([sys.executable, "-S", "-c", probe, str(FULL), str(old)],
                            capture_output=True, text=True, timeout=30, env=_env(tmp_path, old, False))
    assert result.stdout.split() == ["None", "False"], result.stderr


# Codex fixes `PLUGIN_ROOT` at session start too, and keeps no ledger: the
# newest complete version folder in its plugin cache is the installed copy.


def _codex_folder(tmp_path: Path, plugin: str = "probe-research", codex_home: Path | None = None) -> Path:
    return (codex_home or tmp_path / "home" / ".codex") / "plugins" / "cache" / MARKET / plugin


def _codex_copy(root: Path, version: str) -> Path:
    """A version folder as Codex caches it, with a Stop route that prints its
    version and both plugin-root variables."""
    _copy(root, version)
    (root / ".codex-plugin").mkdir()
    (root / ".codex-plugin" / "plugin.json").write_text(json.dumps({"version": version}), encoding="utf-8")
    routes = _routes("Stop", "stop", _shell(
        f'cat >/dev/null; echo "{version} $PLUGIN_ROOT ${{CLAUDE_PLUGIN_ROOT:-none}}"'))
    (root / "hooks" / "routes.json").write_text(json.dumps(routes), encoding="utf-8")
    return root


def _codex_cache(tmp_path: Path, *versions: str, **kw) -> list[Path]:
    return [_codex_copy(_codex_folder(tmp_path, **kw) / v, v) for v in versions]


def _ran(result: subprocess.CompletedProcess) -> str:
    assert result.returncode == 0, result.stderr
    return result.stdout


def test_an_open_codex_session_runs_the_newest_copy_in_codexs_cache(tmp_path):
    old, new = _codex_cache(tmp_path, OLD, NEW)
    assert _ran(_dispatch(old, "stop", {}, _env(tmp_path, old, True))) == f"{NEW} {new} none\n", (
        "PLUGIN_ROOT, never CLAUDE_PLUGIN_ROOT: a Codex route reads it first"
    )


def test_codex_picks_the_newest_by_version_number_not_by_name_or_mtime(tmp_path):
    old, newest, newer_mtime = _codex_cache(tmp_path, "0.9.9", "0.10.0", "0.9.10")
    later = time.time() + 60
    os.utime(newer_mtime, (later, later))
    assert _ran(_dispatch(old, "stop", {}, _env(tmp_path, old, True))).startswith(f"0.10.0 {newest} ")


def test_an_unfinished_newest_copy_does_not_hide_a_whole_newer_one(tmp_path):
    """Running 0.9.9, a complete 0.10.0, an interrupted 0.11.0: the event goes to 0.10.0."""
    old, whole, broken = _codex_cache(tmp_path, "0.9.9", "0.10.0", "0.11.0")
    (broken / "hooks" / "routes.json").write_text("{half", encoding="utf-8")
    assert _ran(_dispatch(old, "stop", {}, _env(tmp_path, old, True))).startswith(f"0.10.0 {whole} ")


def test_codex_reads_its_cache_under_codex_home(tmp_path):
    elsewhere = tmp_path / "codex-home"
    old, new = _codex_cache(tmp_path, OLD, NEW, codex_home=elsewhere)
    env = _env(tmp_path, old, True)
    assert _ran(_dispatch(old, "stop", {}, env)).startswith(f"{OLD} "), "not under ~/.codex: stays"
    env["CODEX_HOME"] = str(elsewhere)
    assert _ran(_dispatch(old, "stop", {}, env)) == f"{NEW} {new} none\n"


def _codex_stays(tmp_path: Path, case: str):
    """(root, env) for a Codex event that must run in the session's own copy."""
    old, new = _codex_cache(tmp_path, OLD, NEW)
    env = _env(tmp_path, old, True)
    hooks = new / "hooks"
    if case == "already-the-newest":
        shutil.rmtree(new)
    elif case == "rolled-back-beside-it":
        # The session is on the newest; an older copy beside it is not newer.
        old, new = new, old
        env = _env(tmp_path, old, True)
    elif case == "no-codex-manifest":
        shutil.rmtree(new / ".codex-plugin")
    elif case == "not-a-version-name":
        new.rename(new.with_name("latest"))
    elif case == "a-pre-release-name":
        new.rename(new.with_name(NEW + "-rc1"))
    elif case == "this-copy-not-a-version":
        renamed = old.with_name("local")
        old.rename(renamed)
        old, env = renamed, _env(tmp_path, renamed, True)
    elif case == "symlinked-out-of-the-cache":
        outside = _codex_copy(tmp_path / "elsewhere" / "0.146.0", "0.146.0")
        (_codex_folder(tmp_path) / "0.146.0").symlink_to(outside)
        shutil.rmtree(new)
    elif case == "outside-codexs-cache":
        # Claude Code's cache (or a checkout), with whole versions beside it.
        old = _codex_copy(_folder(tmp_path) / OLD, OLD)
        _codex_copy(_folder(tmp_path) / NEW, NEW)
        env = _env(tmp_path, old, True)
    elif case == "no-dispatcher-there":
        (hooks / "dispatch.sh").unlink()
    elif case == "routes-broken":
        (hooks / "routes.json").write_text("{broken", encoding="utf-8")
    elif case == "dispatch-py-without-run":
        (hooks / "dispatch.py").write_text("X = 1\n", encoding="utf-8")
    return old, env


@pytest.mark.parametrize("case", [
    "already-the-newest", "rolled-back-beside-it", "no-codex-manifest", "not-a-version-name",
    "a-pre-release-name", "this-copy-not-a-version", "symlinked-out-of-the-cache", "outside-codexs-cache",
    "no-dispatcher-there", "routes-broken", "dispatch-py-without-run",
])
def test_otherwise_a_codex_event_runs_in_the_sessions_own_copy(tmp_path, case):
    root, env = _codex_stays(tmp_path, case)
    version = root.name if case != "this-copy-not-a-version" else OLD
    assert _ran(_dispatch(root, "stop", {}, env, timeout=10)) == f"{version} {root} none\n"


def test_a_codex_event_moves_once_and_still_leaves_the_heartbeat(tmp_path):
    old, new = _codex_cache(tmp_path, OLD, NEW)
    (new / "hooks" / "routes.json").write_text(json.dumps(_routes(
        "UserPromptSubmit", "prompt", _shell('cat >/dev/null; echo "ran:${PROBE_HOOKS_HANDED_OVER:-}:$PLUGIN_ROOT"'))),
        encoding="utf-8")
    assert _ran(_dispatch(old, "prompt", {"session_id": SID}, _env(tmp_path, old, True))) == f"ran::{new}\n"
    assert (tmp_path / "xdg" / "probe" / "hooks" / "alive" / SID).is_file()


def test_the_usual_codex_event_imports_no_json(tmp_path):
    """Under Codex the usual answer (this is the newest) is one folder listing."""
    (old,) = _codex_cache(tmp_path, OLD)
    probe = (
        "import sys; sys.path[0] = sys.argv[1]; import dispatch, os\n"
        "print(dispatch.installed_root(sys.argv[2], os.environ), 'json' in sys.modules)"
    )
    result = subprocess.run([sys.executable, "-S", "-c", probe, str(FULL), str(old)],
                            capture_output=True, text=True, timeout=30, env=_env(tmp_path, old, True))
    assert result.stdout.split() == ["None", "False"], result.stderr


# The Stop wake comes from claude-reads.json, not hooks.json, so dispatch.py
# never sees it: reads_hook.py hands it over itself.

_READS_STUB = "import os, sys\nprint(os.environ['CLAUDE_PLUGIN_ROOT'], sys.stdin.read())\n"


def _reads_copies(tmp_path: Path) -> tuple[Path, Path]:
    old, new = _cache(tmp_path, OLD, NEW)
    for name in os.listdir(FULL):
        if (FULL / name).is_file() and not (old / "hooks" / name).exists():
            shutil.copy2(FULL / name, old / "hooks" / name)
    (new / "hooks" / "reads_hook.py").write_text(_READS_STUB, encoding="utf-8")
    return old, new


@pytest.mark.parametrize("event", ["Stop", "UserPromptSubmit"])
def test_the_stop_wake_runs_the_installed_reads_hook(tmp_path, event):
    old, new = _reads_copies(tmp_path)
    _ledger(tmp_path, new)
    payload = json.dumps({"session_id": SID, "hook_event_name": event})
    result = subprocess.run([sys.executable, str(old / "hooks" / "reads_hook.py")], input=payload,
                            capture_output=True, text=True, timeout=30, env=_env(tmp_path, old, False))
    expected = f"{new} {payload}\n" if event == "Stop" else ""
    assert (result.returncode, result.stdout) == (0, expected), result.stderr


def test_a_handed_over_reads_hook_gets_the_root_variable_its_harness_reads(tmp_path):
    """reads_hook.py's own hand-over names the copy where a Codex route reads it."""
    old, new = _codex_cache(tmp_path, OLD, NEW)
    for name in os.listdir(FULL):
        if (FULL / name).is_file() and not (old / "hooks" / name).exists():
            shutil.copy2(FULL / name, old / "hooks" / name)
    (new / "hooks" / "reads_hook.py").write_text(
        "import os, sys\nprint(os.environ['PLUGIN_ROOT'], os.environ.get('CLAUDE_PLUGIN_ROOT'), sys.stdin.read())\n",
        encoding="utf-8")
    payload = json.dumps({"session_id": SID, "hook_event_name": "Stop"})
    result = subprocess.run([sys.executable, str(old / "hooks" / "reads_hook.py")], input=payload,
                            capture_output=True, text=True, timeout=30, env=_env(tmp_path, old, True))
    assert (result.returncode, result.stdout) == (0, f"{new} None {payload}\n"), result.stderr


@pytest.mark.parametrize("damage", ["none-installed", "will-not-compile"])
def test_otherwise_the_stop_wake_waits_in_the_sessions_own_copy(tmp_path, damage):
    old, new = _reads_copies(tmp_path)
    if damage == "none-installed":
        _ledger(tmp_path, old)
    else:
        _ledger(tmp_path, new)
        (new / "hooks" / "reads_hook.py").write_text("def broken(:\n", encoding="utf-8")
    payload = json.dumps({"session_id": SID, "hook_event_name": "Stop"})
    result = subprocess.run([sys.executable, str(old / "hooks" / "reads_hook.py")], input=payload,
                            capture_output=True, text=True, timeout=30, env=_env(tmp_path, old, False))
    assert (result.returncode, result.stdout) == (0, ""), "an unattended session's own waiter returns at once"


def test_a_copy_that_will_not_import_leaves_this_copys_modules_in_place(tmp_path):
    """The fallback restores sys.path[0]: a lone python route runs in-process
    and imports its sibling modules from there, so they must be this copy's."""
    old, new = _cache(tmp_path, OLD, NEW)
    _ledger(tmp_path, new)
    for root, version in ((old, OLD), (new, NEW)):
        (root / "hooks" / "_which.py").write_text(f"VERSION = {version!r}\n", encoding="utf-8")
        (root / "hooks" / "route.py").write_text("import sys, _which\nsys.stdin.read()\nprint(_which.VERSION)\n", encoding="utf-8")
        route = {"type": "command", "command": dispatch._plain_command([], "route.py", False, [])}
        (root / "hooks" / "routes.json").write_text(json.dumps(_routes("Stop", "stop", route)), encoding="utf-8")
    assert _dispatch(old, "stop", {}, _env(tmp_path, old, False)).stdout == f"{NEW}\n", "the installed copy, whole"
    (new / "hooks" / "dispatch.py").write_text("def broken(:\n", encoding="utf-8")
    result = _dispatch(old, "stop", {}, _env(tmp_path, old, False))
    assert (result.returncode, result.stdout) == (0, f"{OLD}\n"), result.stderr


def test_a_route_past_its_deadline_is_ended_on_windows_too(monkeypatch):
    """Windows has no `os.killpg` (and ignores start_new_session): an overrun
    route was left running there. There each route's process tree is ended by
    pid (taskkill /T, no console window), every route's at once and for
    KILL_TREE_S at most however slow taskkill is, then the route itself; a
    route is ended once however many threads ask."""
    dispatch = _load()
    started: list = []
    killed: list = []

    class Child:
        def __init__(self, pid):
            self.pid = pid

        def poll(self):
            return None

        def kill(self):
            killed.append(self.pid)

    class SlowTaskkill:
        def __init__(self, argv, **kwargs):
            started.append((time.monotonic(), argv, kwargs))

        def wait(self, timeout=None):
            time.sleep(timeout if timeout is not None else 5)
            raise subprocess.TimeoutExpired("taskkill", timeout)

    monkeypatch.setattr(dispatch, "_WINDOWS", True)
    monkeypatch.setattr(dispatch, "_KILLED", {})
    monkeypatch.setattr(dispatch, "KILL_TREE_S", 0.3)
    monkeypatch.delattr(os, "killpg", raising=False)
    monkeypatch.setattr(subprocess, "Popen", SlowTaskkill)
    began = time.monotonic()
    dispatch._kill_routes([Child(4242), None, Child(4343)])
    took = time.monotonic() - began
    assert [argv for _, argv, _ in started] == [["taskkill", "/F", "/T", "/PID", "4242"],
                                                ["taskkill", "/F", "/T", "/PID", "4343"]]
    assert all(kw.get("creationflags") == 0x08000000 for _, _, kw in started)  # CREATE_NO_WINDOW
    assert took < 0.6, f"two slow taskkills took {took:.2f}s: they must share one bounded window"
    assert killed == [4242, 4343]
    dispatch._kill_routes([Child(4242)])  # the final sweep, after the waiter
    assert len(started) == 2 and killed == [4242, 4343], "a route was ended twice"
