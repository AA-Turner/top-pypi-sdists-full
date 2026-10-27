"""Probe staff asked this machine to update now (research-os control/071).

The server answers a machine with an open request with `X-Probe-Update-Requested`;
the client that got it leaves a mark (`probe._shared.update_request`), and the
next `probe` command hands an update to the machine's own updater
(`probe.cli.main._remote_update_notice`). What each test pins would fail
silently: a request no client ever notices, an update started from inside a
training loop or against the person's own auto-update setting, one ask per
command instead of one per window, or a CLI that keeps asking after the server
stopped.
"""

from __future__ import annotations

import importlib
import json
import os
import time

import httpx
import pytest

from probe import version_policy
from probe._shared import update_request
from probe.cli import autoupdate, update_report
from probe.sdk.config import Settings
from probe.sdk.transport import Transport

cli_main = importlib.import_module("probe.cli.main")

STAMP = "1793000000"
#: The real network door, taken before conftest's autouse guard replaces it.
REAL_DELIVER = update_report._deliver


@pytest.fixture(autouse=True)
def fresh_process():
    update_request._reset_for_tests()
    yield
    update_request._reset_for_tests()


def _mark_path():
    return version_policy.state_dir() / update_request.FILENAME


def _mark(seen_ago: float = 0.0) -> None:
    path = _mark_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"requested_at": int(STAMP), "seen_at": time.time() - seen_ago}))


def _argv(monkeypatch, command: str) -> None:
    monkeypatch.setattr(cli_main.sys, "argv", ["probe", command])


# ---------------------------------------------------------------------------
# the mark
# ---------------------------------------------------------------------------


def test_no_header_leaves_nothing():
    update_request.note(httpx.Headers({"x-probe-client-status": "ok"}))
    assert not _mark_path().exists()
    assert update_request.fresh() is False


def test_the_header_leaves_a_fresh_mark_any_case():
    update_request.note(httpx.Headers({"x-probe-update-requested": STAMP}))

    data = json.loads(_mark_path().read_text())
    assert data["requested_at"] == int(STAMP)
    assert abs(data["seen_at"] - time.time()) < 5
    assert update_request.fresh() is True


def test_one_process_rewrites_the_mark_at_most_every_five_minutes(monkeypatch):
    update_request.note({update_request.HEADER: STAMP})
    first = _mark_path().read_text()
    update_request.note({update_request.HEADER: "1793000999"})
    assert _mark_path().read_text() == first

    later = time.monotonic() + update_request.WRITE_EVERY_S + 1
    monkeypatch.setattr(update_request.time, "monotonic", lambda: later)
    update_request.note({update_request.HEADER: "1793000999"})
    assert json.loads(_mark_path().read_text())["requested_at"] == 1793000999


@pytest.mark.parametrize("value", ["", "soon", "-1", "1e9", "١٢٣", "1" * 13, " 17"])
def test_a_value_that_is_not_a_unix_time_leaves_nothing(value):
    update_request.note({update_request.HEADER: value})
    assert not _mark_path().exists()


def test_a_mark_ages_out_and_a_future_or_broken_one_never_counts():
    _mark(seen_ago=update_request.FRESH_S - 60)
    assert update_request.fresh() is True
    _mark(seen_ago=update_request.FRESH_S + 1)
    assert update_request.fresh() is False
    _mark(seen_ago=-3600)
    assert update_request.fresh() is False
    _mark_path().write_text("{not json")
    assert update_request.fresh() is False


def test_note_never_raises():
    class Broken:
        def get(self, _key):
            raise RuntimeError("boom")

    update_request.note(Broken())


# ---------------------------------------------------------------------------
# who notes it
# ---------------------------------------------------------------------------


def _transport(headers: dict[str, str]) -> Transport:
    def handle(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={}, headers=headers)

    return Transport(
        Settings(base_url="http://test", token="test-token"),
        client=httpx.Client(base_url="http://test", transport=httpx.MockTransport(handle)),
        max_retries=0,
    )


def test_the_sdk_transport_notes_it_on_its_own_requests():
    _transport({"X-Probe-Update-Requested": STAMP}).request("GET", "/v1/me")
    assert update_request.fresh() is True


def test_the_sdk_transport_leaves_nothing_without_it():
    _transport({}).request("GET", "/v1/me")
    assert not _mark_path().exists()


def test_the_update_report_flush_notes_it(monkeypatch):
    """The refresher's report flush is often the one request a machine that only
    runs hooks makes with its device."""
    real_client = httpx.Client

    def client(**kwargs):
        def handle(_request):
            return httpx.Response(202, json={"recorded": True}, headers={update_request.HEADER: STAMP})

        kwargs.pop("verify", None)
        return real_client(transport=httpx.MockTransport(handle), **kwargs)

    monkeypatch.setattr(update_report.httpx, "Client", client)

    assert REAL_DELIVER("http://test", {}, {"schema_version": 1}, 1.0) == 202
    assert update_request.fresh() is True


# ---------------------------------------------------------------------------
# the next command acts
# ---------------------------------------------------------------------------


@pytest.fixture
def service(monkeypatch):
    """The Probe service owns updates: record each ask."""
    asks: list[str] = []
    monkeypatch.setattr(cli_main, "_service_owns_updates", lambda: True)
    monkeypatch.setattr(cli_main, "_ask_service_to_update", asks.append)
    return asks


@pytest.fixture
def no_service(monkeypatch):
    """No service (Windows, a pip install): record each spawn."""
    spawns: list[str] = []
    monkeypatch.setattr(cli_main, "_service_owns_updates", lambda: False)
    monkeypatch.setattr(cli_main, "_spawn_update", lambda flag, **_: spawns.append(flag))
    return spawns


def _enable(enabled: bool = True) -> None:
    autoupdate.save(enabled=enabled)


def test_a_fresh_mark_asks_the_service_once_per_window(service, monkeypatch):
    _enable()
    _mark()
    _argv(monkeypatch, "ls")

    for _ in range(5):
        cli_main._remote_update_notice()
    assert service == ["cli"]

    stamp = autoupdate.state_dir() / cli_main._REMOTE_ASK_STAMP
    then = time.time() - cli_main._REMOTE_ASK_EVERY_S - 1
    os.utime(stamp, (then, then))
    cli_main._remote_update_notice()
    assert service == ["cli", "cli"]


def test_it_asks_with_no_cached_manifest_and_its_own_window(service, monkeypatch):
    """The every-command check only asks when the cached manifest shows an
    update; a remote request asks regardless, and an every-command ask the
    service just answered never holds it back."""
    _enable()
    _mark()
    _argv(monkeypatch, "ls")
    assert cli_main._claim_window(cli_main._SERVICE_ASK_STAMP, cli_main._SERVICE_ASK_EVERY_S)

    cli_main._remote_update_notice()

    assert service == ["cli"]


def test_no_mark_or_a_stale_one_does_nothing(service, monkeypatch):
    _enable()
    _argv(monkeypatch, "ls")
    cli_main._remote_update_notice()
    _mark(seen_ago=update_request.FRESH_S + 1)
    cli_main._remote_update_notice()
    assert service == []


def test_automatic_updates_off_is_the_persons_choice(service, no_service, monkeypatch):
    _enable(False)
    _mark()
    _argv(monkeypatch, "ls")
    cli_main._remote_update_notice()
    assert service == [] and no_service == []


@pytest.mark.parametrize(
    "command",
    sorted(cli_main._UPDATE_HOT_PATH_COMMANDS | cli_main._REMOTE_UPDATE_SKIP_COMMANDS),
)
def test_never_from_a_run_command_the_service_the_daemon_or_the_wizard(service, monkeypatch, command):
    _enable()
    _mark()
    _argv(monkeypatch, command)
    cli_main._remote_update_notice()
    assert service == []
    assert not (autoupdate.state_dir() / cli_main._REMOTE_ASK_STAMP).exists()


def test_never_from_a_command_the_service_runs_itself(service, monkeypatch):
    from probe.service.paths import SERVICE_CHILD_ENV

    _enable()
    _mark()
    _argv(monkeypatch, "agent-rules")
    monkeypatch.setenv(SERVICE_CHILD_ENV, "1")
    cli_main._remote_update_notice()
    assert service == []


def test_a_command_finding_the_window_being_claimed_leaves_the_ask_to_it(service, monkeypatch):
    from probe._shared import oscompat

    _enable()
    _mark()
    _argv(monkeypatch, "ls")
    stamp = autoupdate.state_dir() / cli_main._REMOTE_ASK_STAMP
    stamp.parent.mkdir(parents=True, exist_ok=True)
    with open(stamp, "a+b") as other:
        oscompat.flock(other.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        cli_main._remote_update_notice()
        assert service == []
    cli_main._remote_update_notice()
    assert service == ["cli"]


def test_without_the_service_it_runs_the_session_start_update_off_a_terminal(no_service, monkeypatch):
    _enable()
    _mark()
    _argv(monkeypatch, "ls")
    monkeypatch.setattr(cli_main.sys.stdout, "isatty", lambda: False)

    cli_main._remote_update_notice()

    assert no_service == ["--apply-if-newer"]


def test_without_the_service_a_live_run_records_the_wait_and_starts_nothing(no_service, monkeypatch):
    from probe.cli import run_lock

    _enable()
    _mark()
    _argv(monkeypatch, "ls")
    lock = run_lock.acquire("training-run")
    try:
        cli_main._remote_update_notice()
    finally:
        lock.release()

    assert no_service == []
    assert autoupdate.load().last_skip.reason == autoupdate.SKIP_RUN_IN_FLIGHT


def test_it_never_raises_and_prints_nothing(monkeypatch, capsys):
    _enable()
    _mark()
    _argv(monkeypatch, "ls")

    def boom():
        raise RuntimeError("no service")

    monkeypatch.setattr(cli_main, "_service_owns_updates", boom)
    cli_main._remote_update_notice()
    assert capsys.readouterr() == ("", "")


def test_every_command_runs_it_but_a_read_only_one(monkeypatch):
    """Wired into the root callback with the other notices; `probe status` runs none."""
    from typer.testing import CliRunner

    order: list[str] = []
    monkeypatch.setattr(cli_main, "_outbox_notice", lambda **_: None)
    monkeypatch.setattr(cli_main, "_version_notice", lambda: order.append("version"))
    monkeypatch.setattr(cli_main, "_remote_update_notice", lambda: order.append("remote"))
    monkeypatch.setattr(cli_main, "_ensure_capture_notice", lambda _command: None)

    CliRunner().invoke(cli_main.app, ["ignore", "list"])
    CliRunner().invoke(cli_main.app, ["status", "--json"])  # read-only: no notices

    assert order == ["version", "remote"]


def test_without_the_service_never_from_a_command_a_daemon_runs(no_service, monkeypatch):
    from probe.sdk.agent_session import DAEMON_SESSION_ENV

    _enable()
    _mark()
    _argv(monkeypatch, "ls")
    monkeypatch.setenv(DAEMON_SESSION_ENV, "sess-1")
    cli_main._remote_update_notice()
    assert no_service == []


def test_without_the_service_a_live_daemon_worker_records_the_wait(no_service, monkeypatch):
    """The update lands in place there: never under a recording daemon."""
    from probe.service import updater

    _enable()
    _mark()
    _argv(monkeypatch, "ls")
    monkeypatch.setattr(updater, "daemon_worker_running", lambda: True)
    cli_main._remote_update_notice()
    assert no_service == []
    assert autoupdate.load().last_skip.reason == autoupdate.SKIP_DAEMON_RECORDING
