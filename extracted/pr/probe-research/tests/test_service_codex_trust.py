"""The Probe service keeps Probe's hooks approved in Codex (#3617).

Codex rebuilds its copies of Probe's plugins from the marketplace (main), and
every rewrite switches all of their hooks off until approved; the approval came
only with an update, which a live run defers up to a day. The service's healer
(`probe.service.codextrust`) fingerprints the copies each tick and, on a
change, asks a `probe.core.run codex_trust` child to approve them
(`codex_hooks.heal` -> `approve`), retrying with backoff until Codex trusts
them. The critical path at the bottom runs the real child against a fake
Codex app-server (`test_codex_hooks.FAKE_APP_SERVER`); a real Codex is the
manual check after release.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

import pytest

from probe.cli import capabilities, codex_hooks
from probe.core import requests as core_requests
from probe.core import run as core_run
from probe.service import codextrust
from probe.service.codextrust import BACKOFF_S, MAX_ASKS_PER_HOUR, CodexTrust, Healing, Trust
from tests.test_codex_hooks import FAKE_APP_SERVER, _hook

MARKET = codextrust.MARKETPLACE

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="the fake codex is a shell script")


# -- one vocabulary --------------------------------------------------------


def test_the_service_names_the_copies_approve_may_approve():
    """The healer is stdlib-only and cannot import the CLI: its plugin list and
    marketplace are copies, held equal here."""
    assert codextrust.PLUGINS == codex_hooks.PROBE_PLUGINS
    assert codextrust.MARKETPLACE == capabilities.MARKETPLACE


def test_the_child_is_a_read_the_service_can_ask():
    assert codextrust.READ == core_requests.ActionName.CODEX_TRUST.value
    assert core_requests.ActionName.CODEX_TRUST in core_run.READS
    assert core_requests.parse(codextrust.READ, {}) is not None
    with pytest.raises(core_requests.RequestError):
        core_requests.parse(codextrust.READ, {"anything": True})
    from probe.service import protocol

    assert codextrust.READ not in protocol.ACTIONS, "never an `action.run` action: it takes no mutating slot"


@pytest.mark.parametrize(
    ("binary", "outcome", "expected"),
    [
        (None, None, {"outcome": Trust.NO_CODEX, "approved": [], "error": None}),
        ("codex", None, {"outcome": Trust.UNASKED, "approved": [], "error": None}),
        ("codex", codex_hooks.Approval(done=True), {"outcome": Trust.SETTLED, "approved": [], "error": None}),
        ("codex", codex_hooks.Approval(approved=("a", "b"), done=True),
         {"outcome": Trust.SETTLED, "approved": ["a", "b"], "error": None}),
        # A Probe-named hook from another marketplace waits for the person: nothing
        # more for Probe to approve, so the service settles (status still says so).
        ("codex", codex_hooks.Approval(done=False), {"outcome": Trust.SETTLED, "approved": [], "error": None}),
        ("codex", codex_hooks.Approval(error="Codex refused it: managed"),
         {"outcome": Trust.WAITING, "approved": [], "error": "Codex refused it: managed"}),
    ],
)
def test_heal_answers_in_the_services_words(monkeypatch, binary, outcome, expected):
    monkeypatch.setattr(codex_hooks, "codex_binary", lambda: binary)
    monkeypatch.setattr(codex_hooks, "approve", lambda *_a, **_k: outcome)
    assert codex_hooks.heal() == expected
    assert expected["outcome"] in codextrust.OUTCOMES


def test_heal_never_raises(monkeypatch):
    def boom(*_a, **_k):
        raise RuntimeError("broken")

    monkeypatch.setattr(codex_hooks, "codex_binary", lambda: "codex")
    monkeypatch.setattr(codex_hooks, "approve", boom)
    assert codex_hooks.heal()["outcome"] == Trust.WAITING


# -- the fingerprint -------------------------------------------------------


def _copy(home: Path, plugin: str = "probe-research-daemon", version: str = "0.189.1", *,
          market: str = MARKET, files: dict | None = None) -> Path:
    root = home / "plugins" / "cache" / market / plugin / version
    for rel, text in (files or {"hooks/hooks.json": '{"hooks": {}}', "skills/a/SKILL.md": "a"}).items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
    return root


def _bump(path: Path, text: str | None = None) -> None:
    """A rewrite: new content (or the same) and a newer mtime."""
    if text is not None:
        path.write_text(text, encoding="utf-8")
    st = path.stat()
    os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns + 1_000_000_000))


def test_no_copy_is_no_fingerprint(tmp_path):
    assert codextrust.fingerprint(tmp_path) is None
    _copy(tmp_path, market="someone-else")
    assert codextrust.fingerprint(tmp_path) is None, "another marketplace's copy is never Probe's to approve"
    (tmp_path / "plugins" / "cache" / MARKET / "probe-research-tap" / ".staging").mkdir(parents=True)
    assert codextrust.fingerprint(tmp_path) is None, "Codex's own staging folder is no copy"


def test_any_rewrite_of_a_copy_changes_the_fingerprint(tmp_path):
    """Codex untrusts a plugin's hooks on any content change, with or without a
    version bump (#3617: three version rewrites and a same-version one)."""
    root = _copy(tmp_path)
    first = codextrust.fingerprint(tmp_path)
    assert first and codextrust.fingerprint(tmp_path) == first, "a look changes nothing"
    _bump(root / "skills" / "a" / "SKILL.md")  # same version, a skill rewritten
    second = codextrust.fingerprint(tmp_path)
    assert second != first
    _copy(tmp_path, version="0.190.0")  # a new version beside it
    third = codextrust.fingerprint(tmp_path)
    assert third not in (first, second)
    (root / "skills" / "a" / "SKILL.md").unlink()
    assert codextrust.fingerprint(tmp_path) != third


def test_the_fingerprint_reads_codexs_own_home(tmp_path, monkeypatch):
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex"))
    _copy(tmp_path / "codex", plugin="probe-research-tap")
    assert codextrust.codex_home() == tmp_path / "codex"
    assert codextrust.fingerprint() == codextrust.fingerprint(tmp_path / "codex") is not None
    monkeypatch.delenv("CODEX_HOME")
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    assert codextrust.codex_home() == tmp_path / "home" / ".codex"
    assert codextrust.codex_home({"CODEX_HOME": str(tmp_path / "farm")}) == tmp_path / "farm", "the login shell's"


def test_bytecode_probes_own_hooks_write_into_a_copy_is_no_change(tmp_path):
    """dispatch.sh and `python -m tap` cache their bytecode in the copy: every
    session would otherwise read as a rewrite and cost a child."""
    root = _copy(tmp_path)
    first = codextrust.fingerprint(tmp_path)
    (root / "hooks" / "__pycache__").mkdir()
    (root / "hooks" / "__pycache__" / "dispatch.cpython-312.pyc").write_bytes(b"\0" * 64)
    (root / "skills" / "a" / "stray.pyc").write_bytes(b"\0")
    assert codextrust.fingerprint(tmp_path) == first
    (root / ".codex-plugin").mkdir()
    (root / ".codex-plugin" / "plugin.json").write_text("{}", encoding="utf-8")
    assert codextrust.fingerprint(tmp_path) != first, "the plugin's manifest (a dot folder) is its content"


# -- the healer's decisions --------------------------------------------------


class Box:
    """A fake login shell, fingerprint and child: `fp` is what the copies read
    as now; each ask returns the next of `answers` (default settled) and may
    move `fp`. What the healer handed each is kept (`homes`, `envs`)."""

    def __init__(self, fp: str | None = "A") -> None:
        self.fp = fp
        self.answers: list = []
        self.asked = 0
        self.move_to: str | None = None
        self.now = 1_000_000.0
        self.login_env = {"PATH": "/login/bin"}
        self.logins = 0
        self.homes: list = []
        self.envs: list = []

    async def login(self) -> dict:
        self.logins += 1
        return dict(self.login_env)

    def fingerprint(self, home: Path) -> str | None:
        self.homes.append(home)
        return self.fp

    async def ask(self, env: dict) -> dict | None:
        self.asked += 1
        self.envs.append(env)
        if self.move_to is not None:
            self.fp, self.move_to = self.move_to, None
        return self.answers.pop(0) if self.answers else {"outcome": Trust.SETTLED, "approved": ["k"], "error": None}

    def healer(self, tmp_path: Path, **kw) -> CodexTrust:
        logged: list[str] = []
        healer = CodexTrust(log=logged.append, login=self.login, fingerprint=self.fingerprint, ask=self.ask,
                            clock=lambda: self.now, record=tmp_path / "codex-trust.json", **kw)
        healer.logged = logged
        return healer


def _look(healer: CodexTrust) -> None:
    asyncio.run(healer.look())


def test_an_unchanged_copy_never_asks_codex(tmp_path):
    box = Box()
    healer = box.healer(tmp_path)
    _look(healer)
    assert box.asked == 1 and healer.state == Healing.SETTLED
    for _ in range(5):
        box.now += 60
        _look(healer)
    assert box.asked == 1, "the app-server is asked only on a change"


def test_a_change_asks_once_and_a_new_service_remembers_it(tmp_path):
    box = Box()
    healer = box.healer(tmp_path)
    _look(healer)
    assert box.asked == 1 and healer.approved == 1 and healer.public()["state"] == Healing.SETTLED
    assert any("approved 1 of Probe's hooks" in line for line in healer.logged)
    assert json.loads((tmp_path / "codex-trust.json").read_text())["fingerprint"] == "A"
    again = box.healer(tmp_path)  # the next service, same copies
    _look(again)
    assert box.asked == 1, "a change this machine settled is not asked about again"
    box.fp = "B"  # Codex rewrote its copies
    _look(again)
    assert box.asked == 2 and again.settled == "B"


@pytest.mark.parametrize("answer", [
    {"outcome": Trust.WAITING, "approved": [], "error": "Codex refused it: managed"},
    {"outcome": Trust.UNASKED, "approved": [], "error": None},
    None,  # the child died, timed out or wrote no answer
])
def test_an_ask_that_does_not_settle_is_retried_with_backoff_until_it_does(tmp_path, answer):
    box = Box()
    box.answers = [answer, answer, answer]
    healer = box.healer(tmp_path)
    _look(healer)
    assert box.asked == 1 and healer.state == Healing.WAITING
    assert healer.retry_at == box.now + BACKOFF_S[0]
    assert not (tmp_path / "codex-trust.json").exists(), "nothing unsettled is remembered"
    box.now += BACKOFF_S[0] - 1
    _look(healer)
    assert box.asked == 1, "not before the backoff"
    for step in (1, 2):
        box.now = healer.retry_at
        _look(healer)
        assert box.asked == step + 1
        assert healer.retry_at == box.now + BACKOFF_S[step], "each failure waits longer"
    box.now = healer.retry_at
    _look(healer)  # Codex takes it this time
    assert box.asked == 4 and healer.state == Healing.SETTLED and healer.retry_at is None
    assert healer.failures == 0


def test_the_backoff_stops_growing_and_never_gives_up(tmp_path):
    box = Box()
    box.answers = [None] * 20
    healer = box.healer(tmp_path)
    for _ in range(12):
        box.now = max(box.now, healer.retry_at or box.now) + 3600  # past the hour's limit too
        _look(healer)
    assert box.asked == 12 and healer.retry_at - box.now == BACKOFF_S[-1]


def test_a_new_change_asks_at_once_even_while_backing_off(tmp_path):
    box = Box()
    box.answers = [None, None]
    healer = box.healer(tmp_path)
    _look(healer)
    box.answers = [None]
    box.now += 1
    box.fp = "B"
    _look(healer)
    assert box.asked == 2 and healer.failures == 1, "a new change starts over"


@pytest.mark.parametrize("answer", [
    {"outcome": Trust.SETTLED, "approved": ["k"], "error": None},
    {"outcome": Trust.WAITING, "approved": [], "error": "Codex refused it: managed"},
    {"outcome": Trust.UNASKED, "approved": [], "error": None},
    None,
    {"outcome": Trust.NO_CODEX, "approved": [], "error": None},
])
def test_copies_that_move_while_codex_is_asked_are_asked_about_at_the_next_tick(tmp_path, answer):
    """Whatever Codex said, the copies it was asked about are gone: the new ones
    are a new change, asked about at the next tick, and nothing is settled."""
    box = Box()
    box.answers = [answer]
    box.move_to = "B"
    healer = box.healer(tmp_path)
    _look(healer)
    assert box.asked == 1 and healer.settled is None and healer.retry_at is None and healer.failures == 0
    assert not (tmp_path / "codex-trust.json").exists()
    box.now += 60
    _look(healer)
    assert box.asked == 2 and healer.settled == "B" and healer.state == Healing.SETTLED


@pytest.mark.parametrize("text", ['{"v": 2, "fingerprint": "A"}', "not json", '{"v": 1, "fingerprint": ""}',
                                  '{"v": 1}', "[]"])
def test_a_record_it_cannot_read_settles_nothing(tmp_path, text):
    (tmp_path / "codex-trust.json").write_text(text)
    box = Box()
    healer = box.healer(tmp_path)
    assert healer.settled is None
    _look(healer)
    assert box.asked == 1 and json.loads((tmp_path / "codex-trust.json").read_text())["fingerprint"] == "A"


def test_with_automatic_updates_off_nothing_is_approved_without_the_person(tmp_path):
    """No update approves anything for them either: `probe doctor --fix` or
    `/hooks` does (status and doctor name both)."""
    box = Box()
    on = [False]
    healer = box.healer(tmp_path, enabled=lambda: on[0])
    _look(healer)
    assert box.asked == 0 and box.logins == 0 and healer.state == Healing.OFF
    on[0] = True
    _look(healer)
    assert box.asked == 1 and healer.state == Healing.SETTLED


def test_codex_is_found_where_the_login_shell_finds_it(tmp_path, monkeypatch):
    """The service's own environment is clean: an nvm `codex` and a profile's
    CODEX_HOME come from the login shell, to the fingerprint and to the child,
    read again only after LOGIN_TTL_S."""
    monotonic = [1000.0]
    monkeypatch.setattr(codextrust.time, "monotonic", lambda: monotonic[0])
    box = Box()
    box.login_env = {"PATH": "/home/u/.nvm/bin", "CODEX_HOME": str(tmp_path / "farm")}
    healer = box.healer(tmp_path)
    _look(healer)
    assert box.homes == [tmp_path / "farm", tmp_path / "farm"]
    assert box.envs == [{"PATH": "/home/u/.nvm/bin", "CODEX_HOME": str(tmp_path / "farm")}]
    box.now += 60
    _look(healer)
    assert box.logins == 1, "kept for LOGIN_TTL_S"
    monotonic[0] += codextrust.LOGIN_TTL_S
    _look(healer)
    assert box.logins == 2


def test_the_login_shell_keeps_only_where_codex_is(monkeypatch):
    """Never a variable that could carry a password (a proxy) in the healer."""
    async def child_env(*, vars):
        assert vars
        return {"PATH": "/p", "CODEX_HOME": "/c", "HTTPS_PROXY": "http://u:secret@proxy", "CLAUDE_CONFIG_DIR": "/x"}

    monkeypatch.setattr(codextrust.loginenv, "child_env", child_env)
    assert asyncio.run(codextrust.login_env()) == {"PATH": "/p", "CODEX_HOME": "/c"}


def test_a_codex_installed_since_is_found_at_the_next_login_read(tmp_path, monkeypatch):
    monotonic = [1000.0]
    monkeypatch.setattr(codextrust.time, "monotonic", lambda: monotonic[0])
    box = Box()
    box.answers = [{"outcome": Trust.NO_CODEX, "approved": [], "error": None}]
    healer = box.healer(tmp_path)
    _look(healer)
    box.now += 60
    _look(healer)
    assert box.asked == 1 and healer.state == Healing.NO_CODEX
    monotonic[0] += codextrust.LOGIN_TTL_S  # `npm i -g @openai/codex` meanwhile
    _look(healer)
    assert box.asked == 2 and healer.state == Healing.SETTLED


def test_an_ask_holds_the_service_and_says_when_it_starts_and_ends(tmp_path):
    seen: list = []
    box = Box()
    healer = box.healer(tmp_path, changed=lambda: seen.append(healer.asking()))
    _look(healer)
    assert seen == [True, False] and not healer.asking()


def test_no_codex_on_the_path_asks_nothing_more_until_the_copies_change(tmp_path):
    box = Box()
    box.answers = [{"outcome": Trust.NO_CODEX, "approved": [], "error": None}]
    healer = box.healer(tmp_path)
    _look(healer)
    box.now += 3600
    _look(healer)
    assert box.asked == 1 and healer.state == Healing.NO_CODEX
    assert not (tmp_path / "codex-trust.json").exists(), "a service with another login PATH asks again"
    box.fp = "B"
    _look(healer)
    assert box.asked == 2


def test_no_copy_of_probe_in_codex_asks_nothing(tmp_path):
    box = Box(fp=None)
    healer = box.healer(tmp_path)
    _look(healer)
    assert box.asked == 0 and healer.state == Healing.NONE


def test_an_update_an_action_or_a_setup_holds_it_off_until_the_next_tick(tmp_path):
    """They write Codex's config too (an update approves Probe's hooks itself)."""
    box = Box()
    busy = [True]
    healer = box.healer(tmp_path, held=lambda: busy[0])
    _look(healer)
    assert box.asked == 0 and healer.state == Healing.WAITING
    busy[0] = False
    _look(healer)
    assert box.asked == 1 and healer.state == Healing.SETTLED


def test_at_most_so_many_children_an_hour_whatever_changes(tmp_path):
    """A Codex that rewrote its copies at every ask must not be asked every tick."""
    box = Box()
    healer = box.healer(tmp_path)
    for n in range(MAX_ASKS_PER_HOUR + 3):
        box.fp = f"F{n}"
        box.now += 60
        _look(healer)
    assert box.asked == MAX_ASKS_PER_HOUR
    box.now += 3600
    _look(healer)
    assert box.asked == MAX_ASKS_PER_HOUR + 1


def test_the_timer_looks_and_stops(tmp_path):
    box = Box()

    async def main():
        healer = box.healer(tmp_path, tick_s=0.01, first_s=0)
        healer.start()
        for _ in range(200):
            if box.asked:
                break
            await asyncio.sleep(0.01)
        healer.close()
        return healer

    healer = asyncio.run(main())
    assert box.asked == 1 and healer.state == Healing.SETTLED


def test_a_look_that_fails_is_logged_and_the_timer_goes_on(tmp_path):
    box = Box()
    looks = [0]

    def broken(home):
        looks[0] += 1
        raise OSError("disk gone")

    async def main():
        healer = CodexTrust(log=logged.append, login=box.login, fingerprint=broken, ask=box.ask,
                            record=tmp_path / "r.json", tick_s=0.01, first_s=0)
        healer.start()
        for _ in range(200):
            if looks[0] >= 2:
                break
            await asyncio.sleep(0.01)
        healer.close()

    logged: list[str] = []
    asyncio.run(main())
    assert looks[0] >= 2 and any("disk gone" in line for line in logged)


# -- the service ---------------------------------------------------------------


def test_the_service_runs_one_holds_it_off_and_shows_it(tmp_path, monkeypatch):
    from types import SimpleNamespace

    from probe.service import updater as service_updater
    from probe.service.registry import Registry
    from probe.service.server import Service

    service = Service(registry=Registry(tmp_path / "sessions.json"), discovery_s=0)
    status = service._status(None, {})
    assert set(status["codex_trust"]) == {"state", "asks", "approved", "retry_at", "last"}
    assert status["codex_trust"]["state"] == Healing.STARTING
    monkeypatch.setattr(service_updater, "setup_running", lambda extra_dirs=(): False)
    assert not service.codex_trust.held()
    service.actions.running = object()
    assert service.codex_trust.held(), "never beside an action"
    service.actions.running = None
    service.management._changes["c1"] = object()  # a desktop change's child still running
    assert service.codex_trust.held(), "nor a desktop change"
    service.management._changes.clear()
    service.updater.task = SimpleNamespace(done=lambda: False)
    assert service.codex_trust.held(), "nor an update cycle"
    service.updater.task = None
    monkeypatch.setattr(service_updater, "setup_running", lambda extra_dirs=(): True)
    assert service.codex_trust.held(), "nor a `probe wizard` from a terminal"
    # An ask in flight keeps the service up; the healer says when it ends.
    assert not service.holds()
    service.codex_trust.state = Healing.ASKING
    assert service.holds()


def test_a_setup_is_seen_by_its_wizard_lock(tmp_path, monkeypatch):
    """`probe wizard`/`update`/`uninstall` hold `wizard.lock` exclusively while
    they run, in the default state folder or a session's own."""
    import fcntl

    from probe.service import paths as service_paths
    from probe.service import updater as service_updater

    monkeypatch.setattr(service_paths, "state_dir", lambda: tmp_path / "state")
    other = tmp_path / "xdg-state"
    for folder in (tmp_path / "state", other):
        folder.mkdir()
        assert not service_updater.setup_running([str(other)])
        with open(folder / service_updater.WIZARD_LOCK_NAME, "w") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            assert service_updater.setup_running([str(other)])
        assert not service_updater.setup_running([str(other)])


# -- the critical path: a plugin change, healed --------------------------------


@pytest.fixture
def codex_box(tmp_path, monkeypatch):
    """A Codex home holding Probe's daemon plugin and a `codex` whose app-server
    is the fake one, both known to the login shell only (`login`): what the
    service's own child finds."""
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("CODEX_HOME", raising=False)
    codex_home = tmp_path / "codex-home"
    copy = _copy(codex_home)
    server = tmp_path / "server.py"
    server.write_text(FAKE_APP_SERVER, encoding="utf-8")
    state, writes = tmp_path / "hooks.json", tmp_path / "writes.jsonl"
    writes.touch()
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake = bin_dir / "codex"
    fake.write_text(f"#!/bin/sh\nexec '{sys.executable}' '{server}' '{state}' '{writes}' 0\n", encoding="utf-8")
    fake.chmod(0o755)
    login = {"PATH": f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}", "CODEX_HOME": str(codex_home)}
    events = ("sessionStart", "userPromptSubmit", "stop")

    def plugin_changed() -> None:
        """Codex rewrote its copy from main: every hook of it reads modified."""
        _bump(copy / "hooks" / "hooks.json", '{"hooks": {"changed": true}}')
        state.write_text(json.dumps([_hook(codex_home, "probe-research-daemon", event, trust="modified",
                                           path=copy / "hooks" / "hooks.json") for event in events]))

    def trust() -> dict:
        return {hook["key"]: hook["trustStatus"] for hook in json.loads(state.read_text())}

    return type("CodexBox", (), {
        "home": codex_home, "login": login, "plugin_changed": staticmethod(plugin_changed),
        "trust": staticmethod(trust),
        "writes": staticmethod(lambda: [json.loads(line) for line in writes.read_text().splitlines()]),
    })


def test_a_plugin_change_is_healed_by_the_service_before_the_next_codex_session(codex_box, tmp_path):
    """Plugin change on main -> Codex hooks untrusted -> the service heals -> the
    next Codex session runs Probe's hooks (here: Codex says every one is trusted,
    which is what it reads when a session starts)."""
    codex_box.plugin_changed()
    assert set(codex_box.trust().values()) == {"modified"}
    logged: list[str] = []

    async def login() -> dict:
        return dict(codex_box.login)

    healer = CodexTrust(log=logged.append, login=login, record=tmp_path / "codex-trust.json")

    asyncio.run(healer.look())  # the real fingerprint and the real `probe.core.run codex_trust` child
    assert healer.state == Healing.SETTLED, (healer.last, logged)
    assert healer.last["outcome"] == Trust.SETTLED and healer.last["approved"] == 3
    assert set(codex_box.trust().values()) == {"trusted"}
    (write,) = codex_box.writes()
    assert sorted(edit["value"] for edit in write["edits"]) == sorted(
        f"sha256:probe-research-daemon-{event}" for event in ("sessionStart", "userPromptSubmit", "stop"))
    # Codex's own answer, as `probe status` and the next session read it.
    with pytest.MonkeyPatch.context() as env:
        env.setenv("PATH", codex_box.login["PATH"])
        env.setenv("CODEX_HOME", codex_box.login["CODEX_HOME"])
        assert codex_hooks.summarize(codex_hooks.list_hooks(timeout=10)).untrusted == ()

    asyncio.run(healer.look())  # nothing changed: the app-server is not started
    assert len(codex_box.writes()) == 1 and healer.asks == 1

    codex_box.plugin_changed()  # the next merge
    asyncio.run(healer.look())
    assert healer.asks == 2 and healer.state == Healing.SETTLED
    assert set(codex_box.trust().values()) == {"trusted"} and len(codex_box.writes()) == 2
