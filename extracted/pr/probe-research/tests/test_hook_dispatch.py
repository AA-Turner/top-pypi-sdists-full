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
        assert sorted(lanes) == sorted(dispatch.LANE_EVENT), "every lane has exactly one entry"


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
    source = (FULL / "dispatch.py").read_text(encoding="utf-8")
    tree = ast.parse(source, feature_version=(3, 9))
    stdlib = set(sys.stdlib_module_names)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = [node.module or ""]
        else:
            continue
        for name in names:
            assert name.split(".")[0] in stdlib | {"__future__"}, name
    assert "StrEnum" not in source and "tomllib" not in source


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
        got = collections.Counter()
        for entry in entries.get(event, []):
            for hook in entry["hooks"]:
                payload = {"tool_name": tool} if tool else {}
                got.update(h["command"] for h in dispatch.routes(_lane(hook["command"]), payload, wiring))
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


def _plugin(tmp_path: Path, routes: dict, scripts: dict[str, str] | None = None) -> Path:
    root = tmp_path / "plugin"
    hooks = root / "hooks"
    hooks.mkdir(parents=True)
    for name in ("dispatch.py", "dispatch.sh"):
        shutil.copy2(FULL / name, hooks / name)
    (hooks / "routes.json").write_text(json.dumps(routes), encoding="utf-8")
    for name, body in (scripts or {}).items():
        (hooks / name).write_text(body, encoding="utf-8")
        (hooks / name).chmod(0o755)
    return root


def _env(tmp_path: Path, root: Path, codex: bool, **extra: str) -> dict:
    env = {"PATH": os.environ["PATH"], "HOME": str(tmp_path / "home"), "XDG_STATE_HOME": str(tmp_path / "xdg")}
    env["PLUGIN_ROOT" if codex else "CLAUDE_PLUGIN_ROOT"] = str(root)
    env.update(extra)
    return env


def _dispatch(root: Path, lane: str, payload, env: dict, timeout: float = 30) -> subprocess.CompletedProcess:
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
    # tool it had; `^WebSearch$` is the papers hook's).
    tool = next(t for t in ("Bash", "AskUserQuestion", "Write", "WebSearch") if not matcher or dispatch.matches(matcher, t))
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
