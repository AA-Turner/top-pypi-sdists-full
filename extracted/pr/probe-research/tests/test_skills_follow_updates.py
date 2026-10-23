"""A session left open across a plugin update reads the installed plugin's skills.

Claude Code reads Probe's skills from its own skills folder: copies of the
installed plugin's `agent-skills/` (`root_skills_sync.py`), which it re-reads
when a file there changes. Only a session START refreshed those copies, so a
session open for days kept reading the text of whatever plugin last started a
session (Willow, 10-14: 0.129.0's plan-research-review five hours after 0.149.0
was installed, missing its "log every run to Probe" rule). Two refreshers now:

  * `probe update` and the Probe service's updater, right after they move the
    plugin (`root_skills.refresh`, from `upgrading.perform_update`);
  * the PreToolUse route on the Skill tool (`root_skills_sync.py skill-call`),
    for an update made from outside Probe: it refreshes the copies from the
    installed plugin and refuses that one call, because Claude Code renders the
    call from the text it already loaded; the agent's next call reads the new
    one.

The route must never write an OLDER plugin's text over the copies every session
reads: it acts only from the copy the install ledger names.
"""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from probe import root_skills_core as core
from probe.cli import root_skills, updater, upgrading

AGENT = Path(__file__).resolve().parents[1]
FULL = AGENT / "plugins" / "probe-research"
HOOKS = FULL / "hooks"
MARKET = "research-os-agent"
OLD, NEW = "0.150.0", "0.151.0"
SLUGS = ("plan-research-review", "probe")

pytestmark = pytest.mark.skipif(os.name != "posix", reason="the hooks are POSIX shell")


@pytest.fixture
def claude(tmp_path, monkeypatch):
    """Claude Code's home, as the hook sees it under Claude Code."""
    home = tmp_path / "claude"
    for name in ("PLUGIN_ROOT", "KIMI_PLUGIN_ROOT", "PROBE_AGENT", "CLAUDE_CODE_PLUGIN_CACHE_DIR",
                 "PROBE_INSTALLED_PLUGINS_JSON"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(home))
    return home


@pytest.fixture(params=["probe-research", "probe-research-daemon"])
def sync(request, monkeypatch):
    """The hook module, loaded as the dispatcher's in-process route loads it,
    from each plugin's own copy, with what it adds to sys.path and sys.modules
    taken back afterwards."""
    hooks = AGENT / "plugins" / request.param / "hooks"
    monkeypatch.setattr(sys, "path", list(sys.path))
    names = ("_harness_registry", "_root_skills_core")
    saved = {name: sys.modules.pop(name) for name in names if name in sys.modules}
    spec = importlib.util.spec_from_file_location("_skill_call_sync", hooks / "root_skills_sync.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    yield module
    for name in names:
        sys.modules.pop(name, None)
    sys.modules.update(saved)


def _install(home: Path, version: str, text: str, slugs=SLUGS, plugin: str = "probe-research") -> Path:
    """A version folder of the plugin as Claude Code caches it, its skills saying `text`."""
    root = home / "plugins" / "cache" / MARKET / plugin / version
    for slug in slugs:
        folder = root / core.PLUGIN_SKILLS_DIR / slug
        folder.mkdir(parents=True)
        (folder / "SKILL.md").write_text(f"---\nname: {slug}\n---\n{text}: {slug}\n", encoding="utf-8")
    return root


def _ledger(home: Path, *paths: Path, plugin: str = "probe-research", scope: str = "user",
            at: "Path | None" = None) -> None:
    """Claude Code's install ledger, in `home/plugins` or the folder `at`."""
    ledger = (at if at is not None else home / "plugins") / "installed_plugins.json"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    entries = [{"scope": scope, "installPath": str(p), "version": p.name} for p in paths]
    ledger.write_text(json.dumps({"version": 2, "plugins": {f"{plugin}@{MARKET}": entries}}), encoding="utf-8")


def _call(skill, tool="Skill") -> dict:
    return {"session_id": "s1", "hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": {"skill": skill}}


def _text(home: Path, folder: str) -> str:
    return (home / "skills" / folder / "SKILL.md").read_text(encoding="utf-8")


def _left_by_an_open_session(claude: Path, monkeypatch) -> tuple[Path, Path]:
    """The incident's shape: the copies say OLD (the last session start ran it),
    the ledger names NEW, and the event runs in NEW (`dispatch.hand_over`)."""
    old = _install(claude, OLD, "OLD")
    new = _install(claude, NEW, "NEW")
    core.apply(claude / "skills", old, SLUGS)
    _ledger(claude, new)
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(new))
    return old, new


# --- the Skill route ------------------------------------------------------------


def test_a_copy_an_update_left_behind_is_refreshed_and_the_call_asked_for_again(sync, claude, monkeypatch):
    _left_by_an_open_session(claude, monkeypatch)
    slept = []

    out = sync.skill_call(_call("plan-research-review"), sleep=slept.append)

    decision = json.loads(out)["hookSpecificOutput"]
    assert decision["hookEventName"] == "PreToolUse" and decision["permissionDecision"] == "deny"
    reason = decision["permissionDecisionReason"]
    assert "`plan-research-review`" in reason and f"probe-research {NEW}" in reason and "again" in reason
    # Every copy, not just the one called: the next Probe skill is current too.
    assert all(_text(claude, slug).endswith(f"NEW: {slug}\n") for slug in SLUGS)
    # Claude Code's watcher loads the change about a second later; the refusal waits for it.
    assert slept == [sync.WATCHER_SETTLE_S]
    assert sync.skill_call(_call("plan-research-review"), sleep=slept.append) is None, "the retry runs"
    assert sync.skill_call(_call("probe"), sleep=slept.append) is None
    assert slept == [sync.WATCHER_SETTLE_S]


def test_a_current_copy_runs_untouched(sync, claude, monkeypatch):
    new = _install(claude, NEW, "NEW")
    core.apply(claude / "skills", new, SLUGS)
    _ledger(claude, new)
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(new))
    before = (claude / "skills" / "probe" / "SKILL.md").stat().st_mtime_ns

    assert sync.skill_call(_call("probe"), sleep=pytest.fail) is None
    assert (claude / "skills" / "probe" / "SKILL.md").stat().st_mtime_ns == before


@pytest.mark.parametrize("case", ["ledger-names-another", "not-in-the-ledger", "two-copies", "no-ledger"])
def test_a_copy_that_is_not_the_installed_one_never_writes(sync, claude, monkeypatch, case):
    """A session on an older copy that could not hand over (a project-scope
    install, a `--plugin-dir` checkout, a ledger it cannot read) must not put
    its text back over the copies every other session reads."""
    old = _install(claude, OLD, "OLD")
    new = _install(claude, NEW, "NEW")
    core.apply(claude / "skills", new, SLUGS)
    if case == "ledger-names-another":
        _ledger(claude, new)
    elif case == "two-copies":
        _ledger(claude, old, new)
    elif case == "not-in-the-ledger":
        checkout = claude.parent / "checkout" / "probe-research"
        shutil.copytree(old, checkout)
        old = checkout
        _ledger(claude, new)
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(old))

    assert sync.skill_call(_call("probe"), sleep=pytest.fail) is None
    assert _text(claude, "probe").endswith("NEW: probe\n")


def test_a_project_scope_install_of_this_copy_still_counts(sync, claude, monkeypatch):
    """Every entry naming this one folder is the installed copy whatever the
    scope: the question is only whether another copy is the installed one."""
    old = _install(claude, OLD, "OLD")
    new = _install(claude, NEW, "NEW")
    core.apply(claude / "skills", old, SLUGS)
    _ledger(claude, new, scope="project")
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(new))

    assert sync.skill_call(_call("probe"), sleep=lambda _s: None) is not None
    assert _text(claude, "probe").endswith("NEW: probe\n")


def test_a_ledger_claude_code_moved_is_the_one_read(sync, claude, tmp_path, monkeypatch):
    """CLAUDE_CODE_PLUGIN_CACHE_DIR moves Claude Code's whole plugins folder,
    its install ledger included; a stale one under the config dir is not it."""
    moved = tmp_path / "moved-plugins"
    old = _install(claude, OLD, "OLD")
    new = _install(claude, NEW, "NEW")
    core.apply(claude / "skills", old, SLUGS)
    _ledger(claude, old)
    _ledger(claude, new, at=moved)
    monkeypatch.setenv("CLAUDE_CODE_PLUGIN_CACHE_DIR", str(moved))
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(new))

    assert sync.skill_call(_call("probe"), sleep=lambda _s: None) is not None
    assert _text(claude, "probe").endswith("NEW: probe\n")


@pytest.mark.parametrize("payload", [
    _call("probe-research:probe"),
    _call("/probe-research:probe"),
    _call("../probe"),
    _call(".probe-sync.lock"),
    _call(""),
    _call(None),
    _call("probe", tool="Bash"),
    {"tool_name": "Skill", "tool_input": "probe"},
    {"tool_name": "Skill"},
    [],
])
def test_a_call_that_names_none_of_the_copies_runs_untouched(sync, claude, monkeypatch, payload):
    _left_by_an_open_session(claude, monkeypatch)

    assert sync.skill_call(payload, sleep=pytest.fail) is None
    assert _text(claude, "probe").endswith("OLD: probe\n")


def test_a_slash_before_the_name_is_the_same_skill(sync, claude, monkeypatch):
    _left_by_an_open_session(claude, monkeypatch)

    assert sync.skill_call(_call("/probe"), sleep=lambda _s: None) is not None
    assert _text(claude, "probe").endswith("NEW: probe\n")


def test_a_skill_of_the_researchers_own_is_never_touched(sync, claude, monkeypatch):
    _left_by_an_open_session(claude, monkeypatch)
    theirs = claude / "skills" / "review"
    theirs.mkdir()
    (theirs / "SKILL.md").write_text("# mine\n", encoding="utf-8")

    assert sync.skill_call(_call("review"), sleep=pytest.fail) is None
    assert (theirs / "SKILL.md").read_text(encoding="utf-8") == "# mine\n"
    assert _text(claude, "probe").endswith("OLD: probe\n"), "a foreign skill's call refreshes nothing"


def test_a_copy_installed_under_the_collision_name_is_refreshed_too(sync, claude, monkeypatch):
    """`probe` was already a skill of the researcher's, so ours is `probe-probe`."""
    old = _install(claude, OLD, "OLD")
    new = _install(claude, NEW, "NEW")
    theirs = claude / "skills" / "probe"
    theirs.mkdir(parents=True)
    (theirs / "SKILL.md").write_text("# mine\n", encoding="utf-8")
    core.apply(claude / "skills", old, SLUGS)
    _ledger(claude, new)
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(new))

    assert sync.skill_call(_call("probe-probe"), sleep=lambda _s: None) is not None
    assert _text(claude, "probe-probe").endswith("NEW: probe\n")
    assert (theirs / "SKILL.md").read_text(encoding="utf-8") == "# mine\n"


def test_a_skill_the_new_plugin_dropped_goes_and_the_agent_is_told(sync, claude, monkeypatch):
    old = _install(claude, OLD, "OLD", slugs=(*SLUGS, "track-work"))
    new = _install(claude, NEW, "NEW")
    core.apply(claude / "skills", old, (*SLUGS, "track-work"))
    _ledger(claude, new)
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(new))

    out = sync.skill_call(_call("track-work"), sleep=lambda _s: None)

    assert "no longer has the `track-work` skill" in json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
    assert not (claude / "skills" / "track-work").exists()
    assert _text(claude, "probe").endswith("NEW: probe\n")


def test_another_session_mid_sync_lets_the_call_run(sync, claude, monkeypatch):
    """Refused only when this call made its copy current: a refusal with nothing
    fixed would only send the agent round again."""
    _left_by_an_open_session(claude, monkeypatch)
    with core._one_writer(claude / "skills") as holder:
        assert holder
        assert sync.skill_call(_call("probe"), sleep=pytest.fail) is None
    assert _text(claude, "probe").endswith("OLD: probe\n")


def _with_hook(root: Path) -> Path:
    """A plugin folder that also ships this hook, as both Probe profiles do."""
    (root / "hooks").mkdir(parents=True, exist_ok=True)
    (root / "hooks" / "root_skills_sync.py").write_text("# the other profile's copy\n", encoding="utf-8")
    return root


def test_two_probe_profiles_installed_together_never_refuse_each_other(sync, claude, monkeypatch):
    """A Who-records switch can leave both plugins installed. Their `probe`
    skills differ, so each one's route would put back its own text and refuse,
    on every call, for good (reproduced): `probe` is the on / read / off switch.
    With another plugin keeping the same copies, the route leaves them to the
    session start and `probe update`, which know the profile."""
    full = _with_hook(_install(claude, NEW, "FULL"))
    lean = _with_hook(_install(claude, NEW, "LEAN", plugin="probe-research-daemon"))
    core.apply(claude / "skills", lean, SLUGS)
    ledger = claude / "plugins" / "installed_plugins.json"
    ledger.write_text(json.dumps({"version": 2, "plugins": {
        f"probe-research@{MARKET}": [{"scope": "user", "installPath": str(full)}],
        f"probe-research-daemon@{MARKET}": [{"scope": "user", "installPath": str(lean)}],
    }}), encoding="utf-8")

    for root in (full, lean, full, lean):
        monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(root))
        assert sync.skill_call(_call("probe"), sleep=pytest.fail) is None, root.parent.name
    assert _text(claude, "probe").endswith("LEAN: probe\n"), "nothing rewritten"


def test_a_session_is_refused_at_most_once_per_skill_and_install(sync, claude, monkeypatch):
    """Whatever puts older text back in between (another session's start on
    an old copy), the agent is never sent round twice for the same skill."""
    old, new = _left_by_an_open_session(claude, monkeypatch)
    assert sync.skill_call(_call("probe"), sleep=lambda _s: None) is not None

    core.apply(claude / "skills", old, SLUGS)
    assert sync.skill_call(_call("probe"), sleep=pytest.fail) is None
    assert _text(claude, "probe").endswith("NEW: probe\n"), "still refreshed, just not refused again"

    core.apply(claude / "skills", old, SLUGS)
    other = {**_call("probe"), "session_id": "s2"}
    assert sync.skill_call(other, sleep=lambda _s: None) is not None, "another session's first call"
    newer = _install(claude, "0.152.0", "NEWER")
    _ledger(claude, newer)
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(newer))
    assert sync.skill_call(_call("probe"), sleep=lambda _s: None) is not None, "and a later install's"


@pytest.mark.parametrize(("case", "writes"), [
    ("the-installed-copy", True),
    ("an-older-copy", False),
    ("codex-cache-under-claude-env", False),
    ("not-in-the-ledger", True),
    ("no-ledger", True),
])
def test_a_session_start_writes_only_from_a_copy_the_ledger_does_not_contradict(sync, claude, tmp_path,
                                                                               monkeypatch, case, writes):
    """A session start on an older version folder, or on Codex's cache in a
    Codex session that inherited Claude Code's environment (seen on this box:
    visualize-progress's marker named `~/.codex/plugins/cache/...`), used to put
    its text back over the installed plugin's for every open session."""
    old = _install(claude, OLD, "OLD")
    new = _install(claude, NEW, "NEW")
    core.apply(claude / "skills", new, SLUGS)
    root = old
    if case == "the-installed-copy":
        _ledger(claude, old)
    elif case == "an-older-copy":
        _ledger(claude, new)
    elif case == "codex-cache-under-claude-env":
        root = _install(tmp_path / "codex", OLD, "CODEX")
        _ledger(claude, new)
    elif case == "not-in-the-ledger":
        root = claude.parent / "checkout" / "probe-research"
        shutil.copytree(old, root)
        _ledger(claude, new)
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(root))

    assert sync.main([]) == 0
    assert _text(claude, "probe").endswith("NEW: probe\n") is not writes


def test_a_harness_that_reads_the_plugins_own_folder_is_left_alone(sync, claude, monkeypatch):
    """Codex lists a plugin's skills again on every turn, from its cache: it
    has no copies to refresh (and no Skill tool)."""
    _left_by_an_open_session(claude, monkeypatch)
    for name in ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("CODEX_THREAD_ID", "t1")

    assert sync.skill_call(_call("probe"), sleep=pytest.fail) is None
    assert _text(claude, "probe").endswith("OLD: probe\n")


def test_the_route_reads_its_call_from_stdin_and_prints_the_refusal(sync, claude, monkeypatch, capsys):
    import io

    _left_by_an_open_session(claude, monkeypatch)
    monkeypatch.setattr(sync.time, "sleep", lambda _s: None)
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(_call("probe"))))

    assert sync.main([sync.SKILL_CALL]) == 0
    assert json.loads(capsys.readouterr().out)["hookSpecificOutput"]["permissionDecision"] == "deny"
    monkeypatch.setattr(sys, "stdin", io.StringIO("not json"))
    assert sync.main([sync.SKILL_CALL]) == 0 and capsys.readouterr().out == ""


# --- end to end, through the frozen entry -------------------------------------------


def _real_copy(home: Path, version: str) -> Path:
    """This branch's whole plugin, as a version folder of Claude Code's cache."""
    root = home / "plugins" / "cache" / MARKET / "probe-research" / version
    shutil.copytree(FULL, root, ignore=shutil.ignore_patterns("__pycache__"))
    return root


def _hook_env(tmp_path: Path, home: Path, root: Path) -> dict:
    return {
        "PATH": os.environ["PATH"], "HOME": str(tmp_path / "home"), "XDG_STATE_HOME": str(tmp_path / "xdg"),
        "CLAUDECODE": "1", "CLAUDE_CONFIG_DIR": str(home), "CLAUDE_PLUGIN_ROOT": str(root),
        "PROBE_HOOK_HOST": "off", "PROBE_TELEMETRY": "off",
    }


def test_an_open_session_on_an_old_copy_gets_the_installed_skill_text(tmp_path):
    """The whole path a Skill call takes in a session started on OLD after NEW
    was installed: OLD's frozen entry, the hand-over to NEW, NEW's route."""
    home = tmp_path / "claude"
    old, new = _real_copy(home, OLD), _real_copy(home, NEW)
    # OLD is a release from before this route: no Skill route, and a byte filter
    # that lets no Skill call through. The hand-over comes first regardless.
    hooks = old / "hooks"
    source = (hooks / "dispatch.py").read_text(encoding="utf-8")
    assert '"WebSearch", "Skill")' in source
    (hooks / "dispatch.py").write_text(source.replace('"WebSearch", "Skill")', '"WebSearch")'), encoding="utf-8")
    wiring = json.loads((hooks / "routes.json").read_text(encoding="utf-8"))
    wiring["hooks"]["PreToolUse"] = [g for g in wiring["hooks"]["PreToolUse"] if g.get("matcher") != "^Skill$"]
    (hooks / "routes.json").write_text(json.dumps(wiring), encoding="utf-8")
    skill = new / core.PLUGIN_SKILLS_DIR / "plan-research-review" / "SKILL.md"
    skill.write_text(skill.read_text(encoding="utf-8") + "\nPROBE-SKILLTEST-NEW: only the new copy says this.\n",
                     encoding="utf-8")
    env = _hook_env(tmp_path, home, old)
    # The session start that ran OLD's sync, before NEW was installed.
    _ledger(home, old)
    subprocess.run([sys.executable, str(old / "hooks" / "root_skills_sync.py")], env=env, check=True, timeout=60)
    assert "PROBE-SKILLTEST-NEW" not in _text(home, "plan-research-review")
    _ledger(home, new)
    payload = json.dumps(_call("plan-research-review"))

    def call():
        return subprocess.run(["/bin/bash", str(old / "hooks" / "dispatch.sh"), "pre-tool"], input=payload,
                              capture_output=True, text=True, env=env, timeout=60)

    first = call()
    assert first.returncode == 0, first.stderr
    decision = json.loads(first.stdout)["hookSpecificOutput"]
    assert decision["permissionDecision"] == "deny" and NEW in decision["permissionDecisionReason"]
    assert "PROBE-SKILLTEST-NEW" in _text(home, "plan-research-review")
    marker = json.loads((home / "skills" / "plan-research-review" / core.MARKER).read_text(encoding="utf-8"))
    assert marker["edit"].startswith(str(new))
    second = call()
    assert (second.returncode, second.stdout) == (0, ""), "the agent's next call runs, on the new text"


# --- a writer that the ledger moved past while it waited ----------------------------------
#
# Every writer checks which copy is installed, then takes the copy lock. A
# writer whose check passed for v1, held up before the lock while the updater
# installed v2 and refreshed, then wrote v1's text back over v2's: v1's skills
# while v2 is installed (reported by review on #3301, reproduced). The check is
# made again INSIDE the lock, and a writer that lost the lock waits for it
# rather than leaving the work to a holder that may be writing older text.


def _while_it_waits_for_the_lock(monkeypatch, module, meanwhile) -> None:
    """Run `meanwhile` (another writer's whole pass) at the moment this
    writer, its check done, goes for the copy lock."""
    real = module._one_writer
    pending = [meanwhile]

    def interleaved(root):
        if pending:
            pending.pop()()
        return real(root)

    monkeypatch.setattr(module, "_one_writer", interleaved)


def test_a_session_start_held_up_past_an_update_does_not_restore_its_text(sync, claude, monkeypatch):
    old = _install(claude, OLD, "OLD")
    new = _install(claude, NEW, "NEW")
    core.apply(claude / "skills", old, SLUGS)
    _ledger(claude, old)
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(old))

    def the_update():
        _ledger(claude, new)
        sync.core.apply(claude / "skills", new, SLUGS)

    _while_it_waits_for_the_lock(monkeypatch, sync.core, the_update)
    assert sync.main([]) == 0

    assert all(_text(claude, slug).endswith(f"NEW: {slug}\n") for slug in SLUGS), "v1's start put its text back"


def test_a_session_start_held_up_past_its_plugins_removal_does_not_restore_its_skills(sync, claude, monkeypatch):
    """A full-profile session start passed its check, then waited for the lock
    while the wizard switched to the daemon profile: daemon skills in, the full
    plugin's ledger entry gone. An absent entry read as "never listed, allowed",
    so it put `track-work` back -- the agent recording inline while the daemon
    records the same session (review on #3301)."""
    full = _install(claude, OLD, "FULL", slugs=(*SLUGS, "track-work"))
    lean = _install(claude, NEW, "LEAN", plugin="probe-research-daemon")
    core.apply(claude / "skills", full, (*SLUGS, "track-work"))
    _ledger(claude, full)
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(full))

    def the_switch():
        _ledger(claude, lean, plugin="probe-research-daemon")
        sync.core.apply(claude / "skills", lean, SLUGS)

    _while_it_waits_for_the_lock(monkeypatch, sync.core, the_switch)
    assert sync.main([]) == 0

    assert not (claude / "skills" / "track-work").exists(), "track-work on the daemon profile = double recording"
    assert all(_text(claude, slug).endswith(f"LEAN: {slug}\n") for slug in SLUGS)


def test_a_skill_call_held_up_past_a_newer_update_does_not_restore_its_text(sync, claude, monkeypatch):
    _old, new = _left_by_an_open_session(claude, monkeypatch)
    newer = _install(claude, "0.152.0", "NEWER")

    def the_next_update():
        _ledger(claude, newer)
        sync.core.apply(claude / "skills", newer, SLUGS)

    _while_it_waits_for_the_lock(monkeypatch, sync.core, the_next_update)
    assert sync.skill_call(_call("probe"), sleep=pytest.fail) is None, "nothing of NEW's was written to refuse for"

    assert all(_text(claude, slug).endswith(f"NEWER: {slug}\n") for slug in SLUGS)


def test_the_updaters_refresh_held_up_past_a_newer_update_does_not_restore_its_text(claude, monkeypatch):
    old = _install(claude, OLD, "OLD")
    new = _install(claude, NEW, "NEW")
    newer = _install(claude, "0.152.0", "NEWER")
    core.apply(claude / "skills", old, SLUGS)
    _ledger(claude, new)

    def the_next_update():
        _ledger(claude, newer)
        core.apply(claude / "skills", newer, SLUGS)

    _while_it_waits_for_the_lock(monkeypatch, core, the_next_update)
    lines = root_skills.refresh("claude_code")

    assert all(_text(claude, slug).endswith(f"NEWER: {slug}\n") for slug in SLUGS), lines


def test_a_writer_that_finds_the_lock_held_waits_for_it_rather_than_skip(claude):
    """The holder may be writing an OLDER copy's text (a session start on v1
    while the updater refreshes v2): skipping left v1's text in place for good."""
    import threading

    old = _install(claude, OLD, "OLD")
    new = _install(claude, NEW, "NEW")
    core.apply(claude / "skills", old, SLUGS)
    held, release = threading.Event(), threading.Event()

    def holder():
        with core._one_writer(claude / "skills"):
            held.set()
            release.wait(5)

    thread = threading.Thread(target=holder)
    thread.start()
    held.wait(5)
    threading.Timer(0.3, release.set).start()
    try:
        report = core.apply(claude / "skills", new, SLUGS)
    finally:
        release.set()
        thread.join(5)

    assert sorted(report["refreshed"]) == sorted(SLUGS), report
    assert all(_text(claude, slug).endswith(f"NEW: {slug}\n") for slug in SLUGS)


# --- the updater's refresh -------------------------------------------------------------


def test_the_cli_reads_the_ledger_claude_code_moved(claude, tmp_path, monkeypatch):
    old = _install(claude, OLD, "OLD")
    new = _install(claude, NEW, "NEW")
    _ledger(claude, old)
    _ledger(claude, new, at=tmp_path / "moved")
    monkeypatch.setenv("CLAUDE_CODE_PLUGIN_CACHE_DIR", str(tmp_path / "moved"))

    assert root_skills.installed_plugin_root("probe-research") == new


def test_refresh_brings_the_copies_to_the_installed_plugin(claude, monkeypatch):
    old = _install(claude, OLD, "OLD")
    new = _install(claude, NEW, "NEW")
    core.apply(claude / "skills", old, SLUGS)
    _ledger(claude, new)

    lines = root_skills.refresh("claude_code")

    assert any("Refreshed 2 skill(s)" in line for line in lines), lines
    assert all(_text(claude, slug).endswith(f"NEW: {slug}\n") for slug in SLUGS)
    assert root_skills.refresh("claude_code") == [], "a second pass has nothing to say"


def test_refresh_never_fails_the_update(claude, monkeypatch):
    def boom(*_a, **_k):
        raise PermissionError("read-only")

    _install(claude, NEW, "NEW")
    _ledger(claude, claude / "plugins" / "cache" / MARKET / "probe-research" / NEW)
    monkeypatch.setattr(root_skills.core, "apply", boom)

    assert root_skills.refresh("claude_code") == ["! could not refresh Probe's skills: read-only"]


def _stub_update(monkeypatch, result: updater.PluginResult) -> None:
    monkeypatch.setattr(upgrading.updater, "fetch_latest", lambda base: {
        "cli": {"latest": "0.179.3"}, "plugin": {"latest": NEW}, "tap": {"latest": "0.7.2"}})
    monkeypatch.setattr(upgrading.updater, "detect_install", lambda: updater.Install(updater.Method.UV_TOOL))
    monkeypatch.setattr(upgrading.updater, "upgrade_cli", lambda install, current, target: updater.CliResult(
        True, True, False, current, "0.179.3", "CLI already at the latest (0.179.3)"))
    monkeypatch.setattr(upgrading.updater, "update_plugin", lambda target: result)
    monkeypatch.setattr(upgrading.updater, "update_codex_plugins", lambda: result)


def _plugin_result(attempted=True) -> updater.PluginResult:
    return updater.PluginResult(
        attempted=attempted, confirmed=attempted, changed=attempted, before=OLD, after=NEW if attempted else None,
        message=f"plugin updated to {NEW}" if attempted else "`claude` not found on PATH (skipping plugin update)",
        tap_before="0.7.2", tap_after="0.7.2",
    )


@pytest.fixture
def updating(tmp_path, claude, monkeypatch):
    """An update run whose plugin step moved the plugin from OLD to NEW."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    old = _install(claude, OLD, "OLD")
    new = _install(claude, NEW, "NEW")
    core.apply(claude / "skills", old, SLUGS)
    _ledger(claude, new)
    return claude


def test_an_update_refreshes_the_skills_every_open_session_reads(updating, monkeypatch):
    _stub_update(monkeypatch, _plugin_result())

    outcome = upgrading.perform_update(base_url="https://x", include_plugin=True)

    text = "\n".join(outcome.lines)
    assert f"plugin updated to {NEW}" in text and "Refreshed 2 skill(s)" in text, text
    assert all(_text(updating, slug).endswith(f"NEW: {slug}\n") for slug in SLUGS)


def test_an_update_with_no_claude_code_leaves_the_folder_alone(updating, monkeypatch):
    _stub_update(monkeypatch, _plugin_result(attempted=False))

    upgrading.perform_update(base_url="https://x", include_plugin=True)

    assert _text(updating, "probe").endswith("OLD: probe\n")


def test_a_codex_update_writes_no_claude_skills(updating, monkeypatch):
    monkeypatch.setenv("PROBE_AGENT", "codex")
    _stub_update(monkeypatch, _plugin_result())

    upgrading.perform_update(base_url="https://x", include_plugin=True)

    assert _text(updating, "probe").endswith("OLD: probe\n")
