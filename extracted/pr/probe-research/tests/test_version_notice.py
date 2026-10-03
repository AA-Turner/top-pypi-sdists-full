"""The CLI's every-command version check: the gate chain and the state it writes.

Two properties matter more than the individual branches:

  1. The invoking process NEVER makes a network call. An inline fetch would put a
     periodic multi-second stall inside training loops.
  2. The gate order stays cheapest-first, so a `probe log` on an install that
     never opted in touches one small file and stops.

Both are asserted directly rather than inferred from behaviour.
"""

from __future__ import annotations

import importlib
import json
import time

import pytest

from probe import version_policy
from probe.cli import autoupdate

# NOT `from probe.cli import main`: probe/cli/__init__.py binds `main` to its own
# entry-point FUNCTION, which shadows the submodule of the same name.
cli_main = importlib.import_module("probe.cli.main")


@pytest.fixture(autouse=True)
def isolate(tmp_path, monkeypatch):
    """Isolate state, cache and config.

    Sets BOTH PROBE_CONFIG_PATH and XDG_CONFIG_HOME: the surfaces that resolve
    probe config disagree about which wins, and they only agree in production, so
    a fixture setting one can write to the developer's real config.
    """
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe" / "config.json"))
    monkeypatch.setenv("PROBE_BASE_URL", "http://127.0.0.1:9")
    return tmp_path


@pytest.fixture
def spawns(monkeypatch):
    """Record spawns instead of performing them."""
    calls: list[list[str]] = []
    monkeypatch.setattr(cli_main, "_spawn_version_refresh", lambda: calls.append(["refresh"]))
    monkeypatch.setattr(cli_main, "_spawn_autoupdate", lambda: calls.append(["apply"]))
    return calls


@pytest.fixture
def no_network(monkeypatch):
    """Any network call from the invoking process is a hard failure."""

    def _forbidden(*_args, **_kwargs):
        raise AssertionError(
            "the invoking CLI process fetched inline — this is what puts a "
            "multi-second stall inside a training loop"
        )

    monkeypatch.setattr(version_policy, "fetch", _forbidden)
    return monkeypatch


def _enable(enabled: bool = True) -> None:
    autoupdate.save(enabled=enabled)


def _cache(latest: str, *, age: int = 0, ok: bool = True) -> None:
    version_policy.write_cache({"cli": {"latest": latest, "min": "0.0.1"}}, ok)
    path = version_policy.cache_path()
    data = json.loads(path.read_text())
    data["fetched_at"] = int(time.time()) - age
    path.write_text(json.dumps(data))


def _as_tty(monkeypatch, value: bool = True) -> None:
    monkeypatch.setattr(cli_main.sys.stdout, "isatty", lambda: value)


def _argv(monkeypatch, command: str) -> None:
    monkeypatch.setattr(cli_main.sys, "argv", ["probe", command])


# ---------------------------------------------------------------------------
# The fast path.
# ---------------------------------------------------------------------------


def test_disabled_does_nothing_at_all(spawns, no_network):
    _enable(False)
    _cache("99.9.9", age=99999)
    cli_main._version_notice()
    assert spawns == [], "an install that never opted in must not spawn anything"


def test_a_fresh_cache_makes_no_network_call_and_no_refresh(spawns, no_network, capsys):
    _enable()
    _cache("0.0.1", age=10)  # fresh AND not newer
    cli_main._version_notice()
    assert spawns == []
    assert capsys.readouterr().err == ""


def test_a_stale_cache_spawns_a_detached_refresh_and_never_fetches(spawns, no_network):
    _enable()
    _cache("0.0.1", age=version_policy.TTL + 60)
    cli_main._version_notice()
    assert ["refresh"] in spawns


@pytest.mark.parametrize("command", ["wizard", "install"])
def test_the_wizard_refreshes_the_manifest_through_its_own_call(
    spawns, no_network, monkeypatch, command
):
    """`POST /v1/device-state` carries the manifest and writes the cache, so a
    detached refresher would be a second request for the same document."""
    _enable()
    _cache("0.0.1", age=version_policy.TTL + 60)
    _argv(monkeypatch, command)
    cli_main._version_notice()
    assert ["refresh"] not in spawns


def test_a_cold_cache_is_silent_until_the_refresh_lands(spawns, no_network, capsys):
    """update-notifier behaves the same way: the first run has nothing to compare
    against, so the nudge appears on the next one."""
    _enable()
    cli_main._version_notice()
    assert ["refresh"] in spawns
    assert capsys.readouterr().err == "", "nothing to say without a manifest"


def test_a_failed_fetch_uses_backoff_not_ttl(spawns, no_network):
    """A machine that cannot reach the API must not retry every 15 minutes."""
    _enable()
    _cache("99.9.9", age=version_policy.TTL + 60, ok=False)
    cli_main._version_notice()
    assert ["refresh"] not in spawns, "within BACKOFF, a failed fetch must not retry"


# ---------------------------------------------------------------------------
# The apply gate.
# ---------------------------------------------------------------------------


def test_not_a_tty_nudges_but_never_applies(spawns, no_network, monkeypatch, capsys):
    _enable()
    _cache("99.9.9")
    _as_tty(monkeypatch, False)
    _argv(monkeypatch, "ls")
    cli_main._version_notice()
    assert ["apply"] not in spawns
    assert "99.9.9" in capsys.readouterr().err, "a nudge is still useful in CI logs"
    assert autoupdate.load().last_skip.reason == autoupdate.SKIP_NOT_A_TTY


@pytest.mark.parametrize("command", sorted(cli_main._UPDATE_HOT_PATH_COMMANDS))
def test_no_hot_path_command_ever_applies_even_on_a_tty(command, spawns, no_network, monkeypatch):
    """The TTY test is holed by inheritance: a training script launched from a
    terminal hands its TTY to `probe log`, so isatty() is True in exactly the
    case where an upgrade is most destructive."""
    _enable()
    _cache("99.9.9")
    _as_tty(monkeypatch, True)
    _argv(monkeypatch, command)
    cli_main._version_notice()
    assert ["apply"] not in spawns
    assert autoupdate.load().last_skip.reason == autoupdate.SKIP_HOT_PATH_COMMAND


def test_a_live_run_blocks_the_upgrade_from_an_unrelated_command(spawns, no_network, monkeypatch):
    """THE scenario the denylist alone cannot cover: a training run in one shell,
    `probe ls` typed in another. `ls` is not hot-path and its stdout is a
    terminal, so only a cross-process lock closes this."""
    from probe.cli import run_lock

    _enable()
    _cache("99.9.9")
    _as_tty(monkeypatch, True)
    _argv(monkeypatch, "ls")

    lock = run_lock.acquire("training-run")
    try:
        cli_main._version_notice()
        assert ["apply"] not in spawns
        assert autoupdate.load().last_skip.reason == autoupdate.SKIP_RUN_IN_FLIGHT
    finally:
        lock.release()


def test_an_interactive_command_with_no_run_applies(spawns, no_network, monkeypatch):
    _enable()
    _cache("99.9.9")
    _as_tty(monkeypatch, True)
    _argv(monkeypatch, "ls")
    cli_main._version_notice()
    assert ["apply"] in spawns


def test_an_up_to_date_cli_never_applies(spawns, no_network, monkeypatch):
    _enable()
    _cache("0.0.1")
    _as_tty(monkeypatch, True)
    _argv(monkeypatch, "ls")
    cli_main._version_notice()
    assert spawns == []


def test_the_check_never_raises_into_the_command(monkeypatch, spawns):
    """This runs before every command. A broken version check that propagates
    would break `probe log` inside somebody's training loop."""

    def _boom():
        raise RuntimeError("state is on fire")

    monkeypatch.setattr(version_policy, "autoupdate_enabled", _boom)
    cli_main._version_notice()  # must not raise


# ---------------------------------------------------------------------------
# The skip record. What makes "correctly idle" distinguishable from "dead".
# ---------------------------------------------------------------------------


def test_consecutive_skips_for_one_reason_accumulate(isolate):
    autoupdate.record_skip(autoupdate.SKIP_RUN_IN_FLIGHT, available="9.9.9")
    autoupdate.record_skip(autoupdate.SKIP_RUN_IN_FLIGHT, available="9.9.9")
    autoupdate.record_skip(autoupdate.SKIP_RUN_IN_FLIGHT, available="9.9.9")
    skip = autoupdate.load().last_skip
    assert skip.count == 3
    assert "3x" in skip.describe()


def test_a_different_reason_restarts_the_count(isolate):
    autoupdate.record_skip(autoupdate.SKIP_RUN_IN_FLIGHT)
    autoupdate.record_skip(autoupdate.SKIP_RUN_IN_FLIGHT)
    autoupdate.record_skip(autoupdate.SKIP_NOT_A_TTY)
    skip = autoupdate.load().last_skip
    assert skip.count == 1
    assert skip.reason == autoupdate.SKIP_NOT_A_TTY


def test_a_skip_never_overwrites_the_last_real_attempt(isolate):
    """They answer different questions and doctor prints both. Without this, a
    fortnight of correct deferrals erases the record of the last real upgrade."""
    autoupdate.record_attempt(
        autoupdate.Attempt(at=1, ok=True, from_version="1.0.0", to_version="1.1.0")
    )
    autoupdate.record_skip(autoupdate.SKIP_RUN_IN_FLIGHT)
    settings = autoupdate.load()
    assert settings.last_attempt is not None
    assert settings.last_attempt.to_version == "1.1.0"
    assert settings.last_skip is not None


def test_a_real_attempt_clears_a_stale_skip(isolate):
    """A week-old 'skipped, run in flight' printed beside a fresh success would
    read as though we were still blocked."""
    autoupdate.record_skip(autoupdate.SKIP_RUN_IN_FLIGHT)
    autoupdate.record_attempt(autoupdate.Attempt(at=2, ok=True, to_version="1.2.0"))
    assert autoupdate.load().last_skip is None


def test_enabling_autoupdate_preserves_an_existing_skip(isolate):
    """save() is a read-modify-write over the same file. It must not drop a
    sibling key it does not know about."""
    autoupdate.record_skip(autoupdate.SKIP_RUN_IN_FLIGHT)
    autoupdate.save(enabled=True)
    assert autoupdate.load().last_skip is not None


def test_record_skip_never_raises(isolate, monkeypatch):
    monkeypatch.setattr(
        version_policy, "atomic_write_json", lambda *a, **k: (_ for _ in ()).throw(OSError)
    )
    autoupdate.record_skip(autoupdate.SKIP_RUN_IN_FLIGHT)  # must not raise


# ---------------------------------------------------------------------------
# Cross-version compatibility. The plugin and the CLI update independently, so a
# new writer meeting an old reader is the normal case, not the edge case.
# ---------------------------------------------------------------------------


def test_an_unknown_key_written_by_a_newer_client_is_ignored(isolate):
    """Additive-only, unknown keys ignored. A reader that raised here would turn
    a valid state file into 'auto-update is off'."""
    autoupdate.save(enabled=True)
    raw = json.loads(autoupdate.state_path().read_text())
    raw["some_field_from_the_future"] = {"nested": [1, 2, 3]}
    autoupdate.state_path().write_text(json.dumps(raw))
    assert autoupdate.load().enabled is True


def test_a_skip_record_without_a_count_defaults_to_one(isolate):
    """Missing keys default to the reading that preserves old behaviour."""
    autoupdate.save(enabled=True)
    raw = json.loads(autoupdate.state_path().read_text())
    raw["last_skip"] = {"at": 123, "reason": "run in flight"}  # pre-count shape
    autoupdate.state_path().write_text(json.dumps(raw))
    assert autoupdate.load().last_skip.count == 1


def test_a_cache_with_extra_fields_still_reads(isolate):
    """The old plugin reading a cache written by a newer CLI. Raising here means
    refetching every session AND applying the failure backoff to a good cache."""
    version_policy.write_cache({"cli": {"latest": "1.0.0"}}, True)
    path = version_policy.cache_path()
    data = json.loads(path.read_text())
    data["future_field"] = "whatever"
    path.write_text(json.dumps(data))
    manifest, _, ok = version_policy.read_cache()
    assert manifest == {"cli": {"latest": "1.0.0"}}
    assert ok is True


def test_a_corrupt_cache_reads_as_empty_rather_than_raising(isolate):
    version_policy.cache_path().parent.mkdir(parents=True, exist_ok=True)
    version_policy.cache_path().write_text("{ this is not json")
    manifest, fetched_at, ok = version_policy.read_cache()
    assert (manifest, fetched_at, ok) == (None, 0.0, False)


def test_a_failed_write_does_not_leave_a_temp_file_behind(isolate, monkeypatch):
    target = isolate / "state" / "probe" / "autoupdate.json"
    target.parent.mkdir(parents=True, exist_ok=True)

    class _Unserializable:
        pass

    assert version_policy.atomic_write_json(target, {"bad": _Unserializable()}) is False
    leftovers = list(target.parent.glob("*.tmp"))
    assert leftovers == [], f"a temp file outlived its writer: {leftovers}"


def test_concurrent_writers_do_not_share_a_temp_filename(isolate):
    """The old fixed `autoupdate.json.tmp` was shared by every writer, so two
    racing through it could interleave a partial write — and a truncated state
    file reads as 'auto-update is off'."""
    target = isolate / "state" / "probe" / "autoupdate.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    seen: set[str] = set()
    real_replace = version_policy.os.replace

    def _capture(src, dst):
        seen.add(str(src))
        return real_replace(src, dst)

    version_policy.os.replace = _capture
    try:
        for index in range(5):
            version_policy.atomic_write_json(target, {"n": index})
    finally:
        version_policy.os.replace = real_replace
    assert len(seen) == 5, f"temp names collided: {seen}"


# ---------------------------------------------------------------------------
# Single-flight.
# ---------------------------------------------------------------------------


def test_only_one_of_many_concurrent_invocations_claims_the_refresh(isolate):
    """A sweep launching eight runs at once finds eight stale caches. Without
    this they all fetch the same 150-byte document."""
    claims = [version_policy.claim_refresh() for _ in range(8)]
    assert claims.count(True) == 1


def test_an_abandoned_claim_ages_out(isolate, monkeypatch):
    """A killed refresher must not suppress refreshes forever."""
    assert version_policy.claim_refresh() is True
    assert version_policy.claim_refresh() is False
    future = time.time() + version_policy.REFRESH_CLAIM_SECONDS + 5
    monkeypatch.setattr(version_policy.time, "time", lambda: future)
    assert version_policy.claim_refresh() is True


def test_releasing_a_claim_lets_the_next_caller_through(isolate):
    assert version_policy.claim_refresh() is True
    version_policy.release_refresh()
    assert version_policy.claim_refresh() is True


# ---------------------------------------------------------------------------
# Regressions from the adversarial review of this change.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "argv, expected",
    [
        (["probe", "log"], "log"),
        (["probe", "--base-url", "http://x", "log"], "log"),
        (["probe", "--base-url=http://x", "log"], "log"),
        (["probe", "--spool-dir", "/tmp/s", "exec"], "exec"),
        (["probe", "--async", "log"], "log"),
        (["probe", "ls"], "ls"),
        (["probe"], None),
    ],
)
def test_option_values_are_not_mistaken_for_the_command(argv, expected, monkeypatch):
    """`probe --base-url URL log` used to resolve to the URL, so `log` missed the
    denylist entirely — the gate opened for the exact command it exists to stop."""
    monkeypatch.setattr(cli_main.sys, "argv", argv)
    assert cli_main._invoked_command() == expected


def test_the_hook_path_also_respects_the_run_lock(isolate, monkeypatch):
    """The plugin's SessionStart hook runs `probe wizard --action update --yes`,
    which reaches perform_update with NO parent pid. The run-lock check used to
    live inside the wait-for-parent branch, so that path — the OLDEST caller —
    upgraded straight through a live training run."""
    from probe.cli import run_lock
    from probe.cli.upgrading import perform_update

    monkeypatch.delenv(autoupdate.WAIT_FOR_PID_ENV, raising=False)
    lock = run_lock.acquire("training-run")
    assert lock is not None
    try:
        outcome = perform_update(base_url="http://127.0.0.1:9")
        assert outcome.restart_needed is False
        assert any("deferred" in line for line in outcome.lines)
        assert autoupdate.load().last_skip.reason == autoupdate.SKIP_RUN_IN_FLIGHT
    finally:
        lock.release()


def test_release_refresh_never_removes_another_processes_claim(isolate):
    """Two processes racing to reap one stale claim could both proceed, and
    either one's release would then delete the other's live claim."""
    assert version_policy.claim_refresh() is True
    version_policy.refresh_lock_path().write_text("999999")  # somebody else owns it
    version_policy.release_refresh()
    assert version_policy.refresh_lock_path().exists(), "released a claim we did not own"


def test_release_refresh_honours_an_explicit_owner(isolate):
    """The claim is taken by the CLI and released by the refresher it spawns —
    two pids, one claim."""
    assert version_policy.claim_refresh() is True
    owner = int(version_policy.refresh_lock_path().read_text())
    version_policy.release_refresh(owner)
    assert not version_policy.refresh_lock_path().exists()


def test_a_huge_runs_directory_is_refused_rather_than_scanned(isolate):
    """This runs before every command; walking an unbounded directory would make
    an ordinary command slow in proportion to a cleanup failure."""
    from probe.cli import run_lock

    directory = run_lock.runs_dir()
    directory.mkdir(parents=True, exist_ok=True)
    for index in range(run_lock.MAX_SCAN_ENTRIES + 1):
        (directory / f"junk-{index}{run_lock.LEASE_SUFFIX}").write_text("{}")
    assert run_lock.any_live() is True


def test_an_sdk_write_renews_a_detached_runs_lease(isolate):
    """A detached run has no process to hold an flock, so its lease has to be
    renewed by its own traffic or it expires under a job longer than 30 minutes."""
    from probe.cli import run_lock
    from probe.sdk.client import _touch_run_lease

    run_lock.touch_lease("detached-run", seconds=10)  # nearly expired
    lease = run_lock.runs_dir() / f"detached-run{run_lock.LEASE_SUFFIX}"
    before = json.loads(lease.read_text())["expires_at"]
    _touch_run_lease("/v1/runs/detached-run/metrics")
    assert json.loads(lease.read_text())["expires_at"] > before


def test_a_write_to_a_non_run_path_touches_nothing(isolate):
    from probe.sdk.client import _touch_run_lease

    _touch_run_lease("/v1/projects")  # must not raise, must not create anything
    assert not (isolate / "state" / "probe" / "runs").exists()


# ---------------------------------------------------------------------------
# The run-end apply: `_apply_deferred_update`.
#
# `_version_notice` FINDS the update and then refuses it, because every command
# a run-scoped researcher types is on the denylist. That refusal used to be
# terminal. These cover the revisit.
#
# The `no_network` fixture still applies to every parent test below: this path
# reads no cache and fetches nothing, so the "the invoking process never makes a
# network call" invariant holds here exactly as it does for _version_notice.
# ---------------------------------------------------------------------------


@pytest.fixture
def deferred_spawns(monkeypatch):
    """Record the argv of a detached spawn instead of performing it."""
    calls: list[list[str]] = []
    monkeypatch.setattr(cli_main, "_spawn_detached", lambda argv, env: calls.append(argv))
    return calls


def test_deferred_apply_does_nothing_when_disabled(deferred_spawns, no_network):
    _enable(False)
    cli_main._apply_deferred_update()
    assert deferred_spawns == []


def test_deferred_apply_spawns_when_no_run_is_live(deferred_spawns, no_network):
    _enable()
    cli_main._apply_deferred_update()
    assert len(deferred_spawns) == 1
    assert "--apply-if-newer" in deferred_spawns[0]


def test_deferred_apply_never_reads_the_cache(deferred_spawns, no_network):
    """A cold cache must NOT stop the spawn.

    After a multi-hour run the cache is always stale, and reading it to decide
    would mean either blocking on a refresh or comparing against pre-run data.
    The child fetches and decides instead, so the parent spawns regardless.
    """
    _enable()
    assert not version_policy.cache_path().exists()
    cli_main._apply_deferred_update()
    assert len(deferred_spawns) == 1


def test_deferred_apply_ignores_the_tty(deferred_spawns, no_network, monkeypatch):
    """`probe exec python train.py > train.log` has a non-tty stdout, and that is
    the exact shape this fix exists to reach. Reusing _version_notice's TTY gate
    here would defeat it silently, so the absence of that gate is asserted."""
    _enable()
    _as_tty(monkeypatch, False)
    cli_main._apply_deferred_update()
    assert len(deferred_spawns) == 1


def test_a_live_run_blocks_the_deferred_apply(deferred_spawns, no_network):
    """The one real safety check on this path: another process's run."""
    from probe.cli import run_lock

    _enable()
    lock = run_lock.acquire("someone-elses-training-run")
    try:
        cli_main._apply_deferred_update()
        assert deferred_spawns == []
    finally:
        lock.release()


def test_the_deferred_apply_never_raises(monkeypatch, no_network):
    """It runs inside exec's `finally`. A raise there replaces the exception
    already propagating -- including a Ctrl-C -- and corrupts the exit code."""
    _enable()

    def _boom(*_a, **_k):
        raise RuntimeError("spawn exploded")

    monkeypatch.setattr(cli_main, "_spawn_detached", _boom)
    cli_main._apply_deferred_update()  # must not raise


# ---------------------------------------------------------------------------
# WIRING. A test of the helper in isolation passes against a build where nothing
# calls it, so each call site gets a mutant: delete the line, a test goes red.
# ---------------------------------------------------------------------------


class _Ctx:
    """Minimal stand-in for typer.Context: `exec` only reads `.args`."""

    def __init__(self, args: list[str]) -> None:
        self.args = args


def test_exec_applies_the_deferred_update_when_its_child_exits(monkeypatch):
    """MUTANT: delete `_apply_deferred_update()` from exec's finally -> red."""
    import contextlib

    applied: list[str] = []
    monkeypatch.setattr(cli_main, "_apply_deferred_update", lambda: applied.append("x"))
    monkeypatch.setattr(cli_main, "_client", lambda *a, **k: contextlib.nullcontext(object()))

    class _Result:
        returncode = 0

    class _Handle:
        def execute(self, *_a, **_k):
            return _Result()

    monkeypatch.setattr(cli_main, "_run_handle", lambda *_a, **_k: _Handle())

    import typer

    with pytest.raises(typer.Exit):
        cli_main.exec(_Ctx(["--", "true"]), run="r1", cwd=None)
    assert applied == ["x"], "exec must apply the deferred update once its child is gone"


def test_exec_still_applies_when_its_child_fails(monkeypatch):
    """The run is over whether the training script succeeded or not."""
    import contextlib

    applied: list[str] = []
    monkeypatch.setattr(cli_main, "_apply_deferred_update", lambda: applied.append("x"))
    monkeypatch.setattr(cli_main, "_client", lambda *a, **k: contextlib.nullcontext(object()))

    class _Result:
        returncode = 3

    class _Handle:
        def execute(self, *_a, **_k):
            return _Result()

    monkeypatch.setattr(cli_main, "_run_handle", lambda *_a, **_k: _Handle())

    import typer

    with pytest.raises(typer.Exit) as excinfo:
        cli_main.exec(_Ctx(["--", "false"]), run="r1", cwd=None)
    assert applied == ["x"]
    assert excinfo.value.exit_code == 3, "probe exec exists to hand back this code"


def test_exec_does_not_mask_a_keyboard_interrupt(monkeypatch):
    """A Ctrl-C'd training run must still surface as KeyboardInterrupt."""
    import contextlib

    applied: list[str] = []
    monkeypatch.setattr(cli_main, "_apply_deferred_update", lambda: applied.append("x"))
    monkeypatch.setattr(cli_main, "_client", lambda *a, **k: contextlib.nullcontext(object()))

    class _Handle:
        def execute(self, *_a, **_k):
            raise KeyboardInterrupt

    monkeypatch.setattr(cli_main, "_run_handle", lambda *_a, **_k: _Handle())

    with pytest.raises(KeyboardInterrupt):
        cli_main.exec(_Ctx(["--", "sleep"]), run="r1", cwd=None)
    assert applied == ["x"], "the run ended; the apply still belongs here"


def test_run_end_wires_the_deferred_apply_on_the_terminal_path_only():
    """MUTANT: delete `_apply_deferred_update()` from run_end -> red.

    Source-level rather than a driven call: run_end's synchronous path needs the
    journal, the drainer and a live client, and stubbing all of it would assert
    more about the stubs than the wiring. What this DOES catch is the failure
    that matters -- the call being removed or never added.

    It also pins the placement. The queued path returns with a detached outbox
    worker still delivering this run's close, so exactly ONE call belongs in this
    function, after the terminal `clear_lease`.
    """
    import inspect

    source = inspect.getsource(cli_main.run_end)
    assert source.count("_apply_deferred_update()") == 1, (
        "exactly one call, on the terminal path -- the queued path leaves an "
        "outbox worker running and must not trigger an upgrade"
    )
    queued_marker = source.index("end queued for")
    assert source.index("_apply_deferred_update()") > queued_marker, (
        "the call must come after the queued-path early return, not before it"
    )


# ---------------------------------------------------------------------------
# The child: `version_refresh --apply-if-newer`.
#
# These deliberately do NOT use `no_network`: this half fetches by design. That
# fixture patches version_policy.fetch anyway, while this path goes through
# updater.fetch_latest over httpx -- so it would not even see a fetch here.
# ---------------------------------------------------------------------------


@pytest.fixture
def applied(monkeypatch):
    """Record perform_update calls instead of upgrading anything."""
    from probe.cli import upgrading

    calls: list[dict] = []
    monkeypatch.setattr(upgrading, "perform_update", lambda **kwargs: calls.append(kwargs) or None)
    return calls


def _stub_manifest(monkeypatch, latest: str):
    from probe.cli import updater

    monkeypatch.setattr(updater, "fetch_latest", lambda _base: {"cli": {"latest": latest}})


def test_apply_if_newer_does_nothing_when_already_current(applied, monkeypatch, isolate):
    """THE reason this mode exists. perform_update has no is-it-newer check: it
    calls upgrade_cli unconditionally, which runs `uv tool upgrade` plus two
    `claude plugin` subprocesses and overwrites last_attempt. Spawned at every
    run end, that would run forever on a machine that is already current."""
    from probe.cli import version_refresh

    _stub_manifest(monkeypatch, "0.0.1")
    version_refresh._apply_if_newer()
    assert applied == []


def test_apply_if_newer_upgrades_when_the_manifest_is_ahead(applied, monkeypatch, isolate):
    from probe.cli import version_refresh

    _stub_manifest(monkeypatch, "99.9.9")
    version_refresh._apply_if_newer()
    assert len(applied) == 1


def test_apply_if_newer_hands_its_manifest_to_perform_update(applied, monkeypatch, isolate):
    """Without this the child fetches twice, and a release landing between the
    two means comparing against one version and upgrading toward another."""
    from probe.cli import version_refresh

    _stub_manifest(monkeypatch, "99.9.9")
    version_refresh._apply_if_newer()
    assert applied[0]["manifest"] == {"cli": {"latest": "99.9.9"}}


def test_apply_if_newer_upgrades_nothing_when_the_fetch_fails(applied, monkeypatch, isolate):
    """Inverts perform_update's own posture on purpose: it upgrades anyway on a
    failed fetch because a human asked for it. Here nobody asked, and the next
    run end will try again."""
    from probe.cli import updater, version_refresh

    def _boom(_base):
        raise OSError("network down")

    monkeypatch.setattr(updater, "fetch_latest", _boom)
    version_refresh._apply_if_newer()
    assert applied == []


def test_apply_if_newer_defers_to_a_concurrent_upgrade(applied, monkeypatch, isolate):
    """Several runs ending at once must produce one upgrade, not N."""
    from probe.cli import autoupdate, version_refresh

    _stub_manifest(monkeypatch, "99.9.9")
    assert autoupdate.acquire_lock(), "the first holder takes it"
    try:
        version_refresh._apply_if_newer()
        assert applied == []
    finally:
        autoupdate.release_lock()


def test_a_locked_out_child_does_not_even_fetch(monkeypatch, isolate):
    """THE rate limit on this path. Every run end spawns one of these, so a sweep
    of short runs would put one manifest request per run on the API -- all of
    them pointless, since only one child can hold the lock. Taking the lock
    BEFORE the fetch is what collapses N requests into one; if the fetch ever
    moves back above `acquire_lock`, this goes red."""
    from probe.cli import autoupdate, updater, version_refresh

    fetches: list[str] = []

    def _counting_fetch(base):
        fetches.append(base)
        return {"cli": {"latest": "99.9.9"}}

    monkeypatch.setattr(updater, "fetch_latest", _counting_fetch)
    assert autoupdate.acquire_lock(), "somebody else is already upgrading"
    try:
        version_refresh._apply_if_newer()
        assert fetches == [], "a child that cannot upgrade must not hit the API"
    finally:
        autoupdate.release_lock()


def test_a_failed_fetch_still_releases_the_lock(monkeypatch, isolate):
    """The fetch now happens INSIDE the lock, so its early return has to unwind
    it. Leaking the lock here would wedge auto-update for STALE_LOCK_SECONDS."""
    from probe.cli import autoupdate, updater, version_refresh

    def _boom(_base):
        raise OSError("network down")

    monkeypatch.setattr(updater, "fetch_latest", _boom)
    version_refresh._apply_if_newer()
    assert autoupdate.acquire_lock(), "the lock must be free after a failed fetch"
    autoupdate.release_lock()


# ---------------------------------------------------------------------------
# pi's session start (2026-10-02). pi has no SessionStart hook, and every
# `probe` call its extension makes is off a terminal, so the TTY gate refused
# them all and pi never auto-updated.
# ---------------------------------------------------------------------------


def test_pis_session_start_applies_an_update_off_a_terminal(spawns, no_network, monkeypatch):
    _enable()
    _cache("99.9.9", age=10)
    _as_tty(monkeypatch, False)
    monkeypatch.setenv("PROBE_AGENT", "pi")
    monkeypatch.setattr(cli_main.sys, "argv", ["probe", "session", "initialize", "--session", "s1"])
    from probe.cli import run_lock

    monkeypatch.setattr(run_lock, "any_live", lambda: False)
    monkeypatch.setattr(cli_main, "_spawn_harness_update", lambda: spawns.append(["harness"]))

    cli_main._version_notice()

    assert spawns[-1] == ["harness"], "it waits for pi, not just for this command"
    assert ["apply"] not in spawns


def test_the_harness_update_waits_for_pi_before_taking_the_lock(monkeypatch):
    """pi runs `probe session initialize` itself, so our parent IS pi: the child
    waits for it, and takes the update lock only after."""
    from probe.cli import version_refresh

    spawned = {}
    monkeypatch.setattr(cli_main, "_spawn_detached", lambda argv, env: spawned.update(argv=argv, env=env))
    cli_main._spawn_harness_update()
    assert spawned["argv"][-1] == "--apply-if-newer"
    assert spawned["env"][autoupdate.WAIT_FOR_HARNESS_PID_ENV] == str(cli_main.os.getppid())

    order = []
    monkeypatch.setenv(autoupdate.WAIT_FOR_HARNESS_PID_ENV, "4242")
    monkeypatch.setenv(autoupdate.WAIT_FOR_PID_ENV, "4243")
    monkeypatch.setattr(autoupdate, "wait_for_pid_exit", lambda pid, timeout=None: order.append(("wait", pid)) or True)
    monkeypatch.setattr(autoupdate, "acquire_lock", lambda: order.append(("lock",)) or False)
    restarted = {}

    def execve(path, argv, env):
        order.append(("restart",))
        restarted.update(argv=argv, env=env)
        raise _Restarted

    monkeypatch.setattr(version_refresh.os, "execve", execve)
    with pytest.raises(_Restarted):
        version_refresh._apply_if_newer()
    assert order == [("wait", 4242), ("restart",)], "no lock before the restart"
    assert restarted["argv"][-2:] == ["--apply-if-newer", "--no-daemon"]
    assert autoupdate.WAIT_FOR_HARNESS_PID_ENV not in restarted["env"]
    assert autoupdate.WAIT_FOR_PID_ENV not in restarted["env"], "hours later that pid may be anyone's"

    # The restarted process: no pid to wait for, so straight to the lock.
    monkeypatch.delenv(autoupdate.WAIT_FOR_HARNESS_PID_ENV)
    version_refresh._apply_if_newer()
    assert order[-1] == ("lock",)


class _Restarted(Exception):
    """Stands in for `os.execve` replacing the process."""


def test_a_pi_that_outlives_the_wait_updates_nothing(monkeypatch):
    from probe.cli import version_refresh

    monkeypatch.setenv(autoupdate.WAIT_FOR_HARNESS_PID_ENV, "4242")
    monkeypatch.setattr(autoupdate, "wait_for_pid_exit", lambda pid, timeout=None: False)
    monkeypatch.setattr(version_refresh.os, "execve", lambda *a: pytest.fail("no restart on a timeout"))
    monkeypatch.setattr(autoupdate, "acquire_lock", lambda: pytest.fail("no update on a timeout"))

    version_refresh._apply_if_newer()


def test_a_restart_that_fails_updates_nothing(monkeypatch):
    """The interpreter went with the old install: carrying on would run the
    very stale process the restart exists to replace."""
    from probe.cli import version_refresh

    def gone(*_args):
        raise FileNotFoundError("python")

    monkeypatch.setenv(autoupdate.WAIT_FOR_HARNESS_PID_ENV, "4242")
    monkeypatch.setattr(autoupdate, "wait_for_pid_exit", lambda pid, timeout=None: True)
    monkeypatch.setattr(version_refresh.os, "execve", gone)
    monkeypatch.setattr(autoupdate, "acquire_lock", lambda: pytest.fail("no update without the restart"))

    version_refresh._apply_if_newer()


def test_an_orphaned_session_start_waits_for_no_one(monkeypatch):
    """Parent already gone (reparented to init): waiting on init would hold
    the update for the whole timeout."""
    monkeypatch.setattr(cli_main.os, "getppid", lambda: 1)
    monkeypatch.setattr(cli_main, "_spawn_detached", lambda *a: pytest.fail("nothing to wait for"))
    cli_main._spawn_harness_update()


def _pi_session_start(monkeypatch, spawns):
    _enable()
    _as_tty(monkeypatch, False)
    monkeypatch.setenv("PROBE_AGENT", "pi")
    monkeypatch.setattr(cli_main.sys, "argv", ["probe", "session", "initialize", "--session", "s1"])
    monkeypatch.setattr(cli_main, "_spawn_harness_update", lambda: spawns.append(["harness"]))


@pytest.mark.parametrize("cache", ["current", "cold"])
def test_pis_session_start_retries_an_owed_pi_update_with_the_cli_current(spawns, no_network, monkeypatch, cache):
    """The update that skipped pi's package because pi was running owes it:
    with the CLI current nothing else would ever retry it before the next
    release."""
    _pi_session_start(monkeypatch, spawns)
    if cache == "current":
        _cache("0.0.1", age=10)

    cli_main._version_notice()
    assert ["harness"] not in spawns, "nothing owed, nothing spawned"

    autoupdate.mark_pi_update_pending(True)
    cli_main._version_notice()
    assert spawns[-1] == ["harness"]


def test_only_pis_session_start_retries_an_owed_pi_update(spawns, no_network, monkeypatch):
    _pi_session_start(monkeypatch, spawns)
    _cache("0.0.1", age=10)
    autoupdate.mark_pi_update_pending(True)
    monkeypatch.setattr(cli_main.sys, "argv", ["probe", "session", "status"])

    cli_main._version_notice()

    assert ["harness"] not in spawns


def test_apply_if_newer_runs_only_the_owed_pi_step_when_the_cli_is_current(applied, monkeypatch, isolate):
    from probe.cli import upgrading, version_refresh

    owed = []
    monkeypatch.setattr(upgrading, "update_owed_pi_package", lambda: owed.append(1))
    _stub_manifest(monkeypatch, "0.0.1")

    version_refresh._apply_if_newer()
    assert owed == [], "nothing owed"

    autoupdate.mark_pi_update_pending(True)
    version_refresh._apply_if_newer()
    assert owed == [1] and applied == [], "the pi step alone, never the CLI and plugins"


@pytest.mark.parametrize(
    ("agent", "argv"),
    [
        ("pi", ["probe", "session", "status"]),  # only the session start
        ("claude_code", ["probe", "session", "initialize"]),  # Claude Code has its hook
        (None, ["probe", "session", "initialize"]),
    ],
)
def test_other_calls_off_a_terminal_still_skip(spawns, no_network, monkeypatch, agent, argv):
    _enable()
    _cache("99.9.9", age=10)
    _as_tty(monkeypatch, False)
    if agent:
        monkeypatch.setenv("PROBE_AGENT", agent)
    else:
        monkeypatch.delenv("PROBE_AGENT", raising=False)
    monkeypatch.setattr(cli_main.sys, "argv", argv)

    cli_main._version_notice()

    assert ["apply"] not in spawns


def test_windows_never_applies_from_pis_session_start(spawns, no_network, monkeypatch):
    """No fork: the update would run inline and outlast the extension's 5 s budget."""
    _enable()
    _cache("99.9.9", age=10)
    _as_tty(monkeypatch, False)
    monkeypatch.setenv("PROBE_AGENT", "pi")
    monkeypatch.setattr(cli_main.sys, "argv", ["probe", "session", "initialize"])
    monkeypatch.delattr(cli_main.os, "fork", raising=False)

    cli_main._version_notice()

    assert ["apply"] not in spawns
