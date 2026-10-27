"""Probe staff repaired this machine's session capture (research-os control/073).

The server answers a device with an open repair with `X-Probe-Capture-Repair`;
the client that got it leaves a mark (`probe._shared.capture_repair`), and the
next `probe` command fetches the replacement credentials and writes them where
the wizard's sign-in would (`probe.cli.main._capture_repair_notice`). What each
test pins would fail silently: a repair no client notices, a credential written
somewhere the tap never reads, a lock left in place over a credential that now
works, a fetch from inside a training loop, or a mark that keeps the CLI
fetching after the server closed the request.
"""

from __future__ import annotations

import datetime as dt
import importlib
import json
import os
import time

import httpx
import pytest

from probe import version_policy
from probe._shared import capture_repair
from probe.cli import setup, update_report
from probe.cli import telemetry as tm
from probe.cli.capture import AWAITING_CONFIRMATION
from probe.cli.capabilities import tap_plugin_dir
from probe.sdk.config import Settings, load_context, save_context
from probe.sdk.transport import Transport

cli_main = importlib.import_module("probe.cli.main")
#: Captured before conftest swaps the module's one network call for an offline stub.
REAL_DELIVER = update_report._deliver

STAMP = "1793060000"
BASE = "http://test"
DELIBERATE = "disabled by the Probe Research wizard\n"
FETCH = cli_main.CAPTURE_REPAIR_PATH
APPLIED = cli_main.CAPTURE_REPAIR_APPLIED_PATH


@pytest.fixture(autouse=True)
def fresh_process(tmp_path, monkeypatch):
    capture_repair._reset_for_tests()
    monkeypatch.setenv("PROBE_RESEARCH_TAP_PLUGIN_DIR", str(tmp_path / "claude-tap"))
    monkeypatch.setenv("PRBE_CODEX_TAP_PLUGIN_DIR", str(tmp_path / "codex-tap"))
    monkeypatch.delenv("PROBE_INGEST_TOKEN", raising=False)
    monkeypatch.delenv("PROBE_TOKEN", raising=False)
    monkeypatch.delenv("PROBE_BASE_URL", raising=False)
    monkeypatch.delenv("PROBE_DAEMON_SESSION", raising=False)
    yield
    capture_repair._reset_for_tests()


def _mark_path():
    return version_policy.state_dir() / capture_repair.FILENAME


def _mark(seen_ago: float = 0.0) -> None:
    path = _mark_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"requested_at": int(STAMP), "seen_at": time.time() - seen_ago}))


def _argv(monkeypatch, command: str) -> None:
    monkeypatch.setattr(cli_main.sys, "argv", ["probe", command])


def _lock(source: str, text: str, *, set_at: float | None = None) -> None:
    directory = tap_plugin_dir(source)
    directory.mkdir(parents=True, exist_ok=True)
    (directory / ".disabled").write_text(text)
    if set_at is not None:
        os.utime(directory / ".disabled", (set_at, set_at))


def _iso(at: float) -> str:
    return dt.datetime.fromtimestamp(at, dt.UTC).isoformat().replace("+00:00", "Z")


def _answer(*sources: str, requested_at: float | None = None) -> dict:
    return {
        "requested_at": _iso(requested_at if requested_at is not None else time.time() - 3600),
        "credentials": [
            {"capture_source": source, "token": f"ros_ing_{source}_new", "device_id": f"{i}" * 32}
            for i, source in enumerate(sources)
        ],
    }


# ---------------------------------------------------------------------------
# the mark
# ---------------------------------------------------------------------------


def _transport(headers: dict[str, str]) -> Transport:
    def handle(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={}, headers=headers)

    return Transport(
        Settings(base_url=BASE, token="test-token"),
        client=httpx.Client(base_url=BASE, transport=httpx.MockTransport(handle)),
        max_retries=0,
    )


def test_the_sdk_transport_notes_it_on_its_own_requests():
    _transport({capture_repair.HEADER: STAMP}).request("GET", "/v1/me")
    assert capture_repair.fresh() is True


def test_no_header_leaves_nothing():
    _transport({}).request("GET", "/v1/me")
    assert not _mark_path().exists()


@pytest.mark.parametrize("value", ["", "soon", "1" * 13, "１２３"])
def test_a_value_that_is_not_a_unix_time_leaves_nothing(value):
    capture_repair.note({capture_repair.HEADER: value})
    assert not _mark_path().exists()


def test_one_process_rewrites_the_mark_at_most_every_five_minutes():
    capture_repair.note({capture_repair.HEADER: STAMP})
    first = _mark_path().read_text()
    time.sleep(0.01)
    capture_repair.note({capture_repair.HEADER: STAMP})
    assert _mark_path().read_text() == first


def test_a_mark_ages_out_and_clear_removes_it():
    _mark(seen_ago=capture_repair.FRESH_S + 1)
    assert capture_repair.fresh() is False
    _mark()
    assert capture_repair.fresh() is True
    capture_repair.clear()
    assert not _mark_path().exists() and capture_repair.fresh() is False


def test_note_and_clear_never_raise():
    class Broken:
        def get(self, _key):
            raise RuntimeError("headers")

    capture_repair.note(Broken())  # type: ignore[arg-type]
    capture_repair.clear()


# ---------------------------------------------------------------------------
# the next command fetches and applies
# ---------------------------------------------------------------------------


@pytest.fixture
def server(monkeypatch):
    """The CLI's real Client and Transport over a fake fetch and confirmation;
    `answers[path]` is that path's (status, body)."""
    calls: list[httpx.Request] = []
    answers: dict[str, tuple[int, dict]] = {FETCH: (200, {}), APPLIED: (200, {"state": "cleared"})}

    def handle(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        status, body = answers.get(request.url.path, (404, {"detail": "no route"}))
        return httpx.Response(status, json=body)

    # The CLI's own client, transport and headers; only the socket is fake.
    from probe.sdk import transport as transport_mod

    real_client = httpx.Client

    def client(*args, **kwargs):
        kwargs.pop("verify", None)
        kwargs.pop("transport", None)
        return real_client(*args, transport=httpx.MockTransport(handle), **kwargs)

    monkeypatch.setattr(transport_mod.httpx, "Client", client)
    monkeypatch.setattr(cli_main._conn, "base_url", BASE, raising=False)
    save_context({"token": "probe_pat_device", "base_url": BASE})
    return calls, answers


def _paths(calls) -> list[str]:
    return [call.url.path for call in calls]


def _confirmation(calls) -> dict:
    (ack,) = [call for call in calls if call.url.path == APPLIED]
    return json.loads(ack.content)


@pytest.fixture
def events(monkeypatch):
    records: list[dict] = []
    monkeypatch.setattr(
        tm,
        "emit_capture_repair_applied",
        lambda **kw: records.append(kw) or True,
    )
    return records


def test_a_repair_writes_each_credential_where_its_tap_reads_it_lifts_its_lock_and_confirms(
    server, events, monkeypatch, capsys
):
    calls, answers = server
    asked = time.time() - 60
    _lock("claude_code", DELIBERATE, set_at=asked - 3600)  # the buggy turn-off, before staff asked
    _lock("codex", AWAITING_CONFIRMATION)
    answers[FETCH] = (200, _answer("claude_code", "codex", requested_at=asked))
    _mark()
    _argv(monkeypatch, "ls")

    cli_main._capture_repair_notice()

    assert _paths(calls) == [FETCH, APPLIED]
    fetch = calls[0]
    assert fetch.method == "POST" and json.loads(fetch.content) == {}
    assert fetch.headers.get("X-Probe-Device"), "delivery is bound to the device the request names"
    assert _confirmation(calls) == {
        "requested_at": _iso(asked), "applied": ["claude_code", "codex"], "kept_off": [], "unsupported": [],
    }
    assert load_context()["ingest_token"] == "ros_ing_claude_code_new"
    codex_dir = tap_plugin_dir("codex")
    assert (codex_dir / ".token").read_text() == "ros_ing_codex_new"
    assert json.loads((codex_dir / ".config").read_text())["api_base_url"] == BASE
    assert not (tap_plugin_dir("claude_code") / ".disabled").exists()
    assert not (codex_dir / ".disabled").exists()
    assert not _mark_path().exists()
    out, err = capsys.readouterr()
    assert out == ""
    assert "Probe staff restored session capture for Claude Code on this machine" in err, (
        "a turn-off was lifted: the person is told, once"
    )
    assert "Codex" not in err, "a sign-in's pending lock is lifted silently"
    assert events == [{
        "sources": ["claude_code", "codex"], "outcome": "applied", "locks_lifted": 2, "base_url": BASE,
        "kept_off": [], "confirmed": True, "unsupported": [],
    }]


def test_a_turn_off_made_after_staff_asked_is_kept(server, events, monkeypatch, capsys):
    calls, answers = server
    asked = time.time() - 3600
    _lock("codex", DELIBERATE, set_at=asked + 600)  # the person turned it off after the request
    _lock("claude_code", AWAITING_CONFIRMATION)
    answers[FETCH] = (200, _answer("claude_code", "codex", requested_at=asked))
    _mark()
    _argv(monkeypatch, "ls")

    cli_main._capture_repair_notice()

    assert _confirmation(calls) == {
        "requested_at": _iso(asked), "applied": ["claude_code"], "kept_off": ["codex"], "unsupported": [],
    }
    codex_dir = tap_plugin_dir("codex")
    assert (codex_dir / ".disabled").read_text() == DELIBERATE, "the newer turn-off stands"
    assert not (codex_dir / ".token").exists(), "nothing is written for an agent kept off"
    assert not (tap_plugin_dir("claude_code") / ".disabled").exists()
    assert not _mark_path().exists()
    assert capsys.readouterr().err == "", "nothing resumed that the person had turned off"
    assert events[0]["outcome"] == "applied" and events[0]["kept_off"] == ["codex"]


def test_every_agent_kept_off_still_confirms(server, events, monkeypatch):
    calls, answers = server
    asked = time.time() - 3600
    _lock("codex", DELIBERATE, set_at=asked + 60)
    answers[FETCH] = (200, _answer("codex", requested_at=asked))
    _mark()
    _argv(monkeypatch, "ls")

    cli_main._capture_repair_notice()

    assert _confirmation(calls) == {"requested_at": _iso(asked), "applied": [], "kept_off": ["codex"], "unsupported": []}
    assert events[0]["outcome"] == "kept_off"


def test_without_the_request_time_every_turn_off_is_kept(server, events, monkeypatch):
    calls, answers = server
    _lock("codex", DELIBERATE, set_at=time.time() - 86400)
    body = _answer("codex")
    body.pop("requested_at")
    answers[FETCH] = (200, body)
    _mark()
    _argv(monkeypatch, "ls")

    cli_main._capture_repair_notice()

    assert _confirmation(calls)["kept_off"] == ["codex"]
    assert (tap_plugin_dir("codex") / ".disabled").exists()


def test_a_partial_write_confirms_only_what_applied_and_keeps_the_mark(server, events, monkeypatch):
    calls, answers = server
    _lock("claude_code", AWAITING_CONFIRMATION)
    _lock("codex", AWAITING_CONFIRMATION)
    answers[FETCH] = (200, _answer("claude_code", "codex"))
    answers[APPLIED] = (200, {"state": "open", "remaining": ["codex"]})
    real = setup.write_capture_credential

    def flaky(source, token, base):
        if source == "codex":
            raise OSError("read-only")
        real(source, token, base)

    monkeypatch.setattr(setup, "write_capture_credential", flaky)
    _mark()
    _argv(monkeypatch, "ls")

    cli_main._capture_repair_notice()

    assert _paths(calls) == [FETCH, APPLIED], "the agent that applied is settled, so it is never re-minted"
    assert _confirmation(calls)["applied"] == ["claude_code"], "the failed agent is left out: it stays open"
    assert capture_repair.fresh() is True, "still open on the server: the next window fetches only codex"
    assert load_context()["ingest_token"] == "ros_ing_claude_code_new"
    assert (tap_plugin_dir("codex") / ".disabled").exists()
    assert events == [{
        "sources": ["claude_code"], "outcome": "write_failed", "locks_lifted": 1, "base_url": BASE,
        "kept_off": [], "confirmed": True, "unsupported": [],
    }]


def test_a_confirmation_the_server_finds_closed_clears_the_mark(server, events, monkeypatch):
    calls, answers = server
    answers[FETCH] = (200, _answer("codex"))
    answers[APPLIED] = (404, {"detail": {"code": "none_open"}})
    _mark()
    _argv(monkeypatch, "ls")

    cli_main._capture_repair_notice()

    assert _paths(calls) == [FETCH, APPLIED]
    assert not _mark_path().exists()
    assert events[0]["confirmed"] is True


def test_an_unconfirmed_repair_keeps_the_mark(server, events, monkeypatch):
    calls, answers = server
    answers[FETCH] = (200, _answer("codex"))
    answers[APPLIED] = (500, {"detail": "boom"})
    _mark()
    _argv(monkeypatch, "ls")

    cli_main._capture_repair_notice()

    assert (tap_plugin_dir("codex") / ".token").read_text() == "ros_ing_codex_new", "applied all the same"
    assert capture_repair.fresh() is True, "the next window fetches and confirms again"
    assert events[0]["confirmed"] is False


def test_a_stale_claude_code_tap_token_is_replaced(server, events, monkeypatch):
    calls, answers = server
    claude_dir = tap_plugin_dir("claude_code")
    claude_dir.mkdir(parents=True, exist_ok=True)
    (claude_dir / ".token").write_text("ros_ing_old_pairing")
    answers[FETCH] = (200, _answer("claude_code"))
    _mark()
    _argv(monkeypatch, "ls")

    cli_main._capture_repair_notice()

    assert load_context()["ingest_token"] == "ros_ing_claude_code_new"
    assert (claude_dir / ".token").read_text() == "ros_ing_claude_code_new", "the tap reads .token first"


def test_an_ingest_token_in_the_environment_is_reported(server, events, monkeypatch):
    _calls, answers = server
    monkeypatch.setenv("PROBE_INGEST_TOKEN", "ros_ing_from_env")
    answers[FETCH] = (200, _answer("claude_code"))
    _mark()
    _argv(monkeypatch, "ls")

    cli_main._capture_repair_notice()

    assert events[0]["outcome"] == "env_shadowed"


def test_no_open_repair_clears_the_mark(server, events, monkeypatch):
    calls, answers = server
    answers[FETCH] = (404, {"detail": "no open capture repair for this device"})
    _lock("codex", AWAITING_CONFIRMATION)
    _mark()
    _argv(monkeypatch, "ls")

    cli_main._capture_repair_notice()

    assert _paths(calls) == [FETCH]
    assert not _mark_path().exists()
    assert (tap_plugin_dir("codex") / ".disabled").exists(), "nothing was repaired"
    assert events == []


def test_a_server_error_keeps_the_mark_for_the_next_window(server, events, monkeypatch):
    _calls, answers = server
    answers[FETCH] = (500, {"detail": "boom"})
    _mark()
    _argv(monkeypatch, "ls")

    cli_main._capture_repair_notice()

    assert capture_repair.fresh() is True
    assert events == []


def test_one_fetch_per_window(server, events, monkeypatch):
    calls, answers = server
    answers[FETCH] = (500, {})
    _mark()
    _argv(monkeypatch, "ls")

    cli_main._capture_repair_notice()
    cli_main._capture_repair_notice()

    assert len(calls) == 1


def test_an_agent_this_cli_cannot_capture_is_settled_as_unsupported(server, events, monkeypatch):
    calls, answers = server
    answers[FETCH] = (200, {"requested_at": _iso(time.time()),
                            "credentials": [{"capture_source": "not-an-agent", "token": "ros_ing_x"}]})
    _mark()
    _argv(monkeypatch, "ls")

    cli_main._capture_repair_notice()

    assert _paths(calls) == [FETCH, APPLIED], "settled, never retried for 48 hours"
    assert _confirmation(calls)["unsupported"] == ["not-an-agent"]
    assert "ingest_token" not in load_context()
    assert not _mark_path().exists()
    assert events and events[0]["outcome"] == "unsupported" and events[0]["unsupported"] == ["not-an-agent"]


def test_a_command_the_daemon_runs_neither_fetches_nor_spends_the_window(server, monkeypatch):
    calls, answers = server
    answers[FETCH] = (500, {})
    monkeypatch.setenv("PROBE_DAEMON_SESSION", "sess-1")
    _mark()
    _argv(monkeypatch, "ls")

    cli_main._capture_repair_notice()
    assert calls == [] and capture_repair.fresh() is True

    monkeypatch.delenv("PROBE_DAEMON_SESSION")
    cli_main._capture_repair_notice()
    assert len(calls) == 1, "the person's own next command still gets its window"


def test_the_same_token_under_another_url_still_repairs(server, monkeypatch):
    """An in-cluster alias or an explicit port for the same API: the token decides."""
    calls, answers = server
    _lock("codex", AWAITING_CONFIRMATION)
    answers[FETCH] = (200, _answer("codex"))
    monkeypatch.setattr(cli_main._conn, "base_url", None, raising=False)
    monkeypatch.setenv("PROBE_BASE_URL", "http://elsewhere")
    _mark()
    _argv(monkeypatch, "ls")
    cli_main._capture_repair_notice()
    assert calls and calls[0].url.host == "elsewhere", "the override really was in force"
    assert _paths(calls) == [FETCH, APPLIED]
    pinned = json.loads((tap_plugin_dir("codex") / ".config").read_text())["api_base_url"]
    assert pinned == BASE, "the tap uploads to the config context's API, not the shell's override"


@pytest.mark.parametrize(
    ("env", "flag"),
    [({"PROBE_TOKEN": "probe_pat_other_account"}, BASE)],
    ids=["env-token"],
)
def test_an_override_of_the_files_identity_neither_fetches_nor_spends_the_window(server, monkeypatch, env, flag):
    calls, answers = server
    answers[FETCH] = (500, {})
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setattr(cli_main._conn, "base_url", flag, raising=False)
    _mark()
    _argv(monkeypatch, "ls")

    cli_main._capture_repair_notice()
    assert calls == [] and capture_repair.fresh() is True

    for name in env:
        monkeypatch.delenv(name)
    monkeypatch.setattr(cli_main._conn, "base_url", None, raising=False)
    cli_main._capture_repair_notice()
    assert len(calls) == 1, "with the file's own identity the window is still there"


def test_no_mark_or_a_stale_one_fetches_nothing(server, monkeypatch):
    calls, _answers = server
    _argv(monkeypatch, "ls")
    cli_main._capture_repair_notice()
    _mark(seen_ago=capture_repair.FRESH_S + 5)
    cli_main._capture_repair_notice()
    assert calls == []


@pytest.mark.parametrize("command", ["log", "run", "artifact", "daemon", "mcp", "update", "wizard"])
def test_never_from_a_run_command_the_daemon_or_the_wizard(server, monkeypatch, command):
    calls, _answers = server
    _mark()
    _argv(monkeypatch, command)
    cli_main._capture_repair_notice()
    assert calls == []


def test_never_from_a_command_the_service_runs_itself(server, monkeypatch):
    from probe.service.paths import SERVICE_CHILD_ENV

    calls, _answers = server
    monkeypatch.setenv(SERVICE_CHILD_ENV, "1")
    _mark()
    _argv(monkeypatch, "ls")
    cli_main._capture_repair_notice()
    assert calls == []


def test_signed_out_fetches_nothing(server, monkeypatch):
    calls, _answers = server
    save_context({"token": None})
    _mark()
    _argv(monkeypatch, "ls")
    cli_main._capture_repair_notice()
    assert calls == []


def test_it_never_raises_and_prints_nothing(monkeypatch, capsys):
    _mark()
    _argv(monkeypatch, "ls")
    save_context({"token": "probe_pat_device"})

    def boom(**_kw):
        raise RuntimeError("no client")

    monkeypatch.setattr(cli_main, "_new_client", boom)
    cli_main._capture_repair_notice()
    assert capsys.readouterr() == ("", "")


def test_every_command_runs_it_after_the_remote_update_but_a_read_only_one(monkeypatch):
    from typer.testing import CliRunner

    order: list[str] = []
    monkeypatch.setattr(cli_main, "_outbox_notice", lambda **_: None)
    monkeypatch.setattr(cli_main, "_version_notice", lambda: None)
    monkeypatch.setattr(cli_main, "_remote_update_notice", lambda: order.append("remote"))
    monkeypatch.setattr(cli_main, "_capture_repair_notice", lambda: order.append("repair"))
    monkeypatch.setattr(cli_main, "_ensure_capture_notice", lambda _command: None)

    CliRunner().invoke(cli_main.app, ["ignore", "list"])
    CliRunner().invoke(cli_main.app, ["status", "--json"])  # read-only: no notices

    assert order == ["remote", "repair"]


def test_the_update_report_flush_notes_it(monkeypatch):
    """The refresher's report flush is often the one request a machine that only
    runs hooks makes with its device."""
    real_client = httpx.Client

    def client(**kwargs):
        def handle(_request):
            return httpx.Response(202, json={"recorded": True}, headers={capture_repair.HEADER: STAMP})

        kwargs.pop("verify", None)
        return real_client(transport=httpx.MockTransport(handle), **kwargs)

    monkeypatch.setattr(update_report.httpx, "Client", client)

    assert REAL_DELIVER("http://test", {}, {"schema_version": 1}, 1.0) == 202
    assert capture_repair.fresh() is True


# ---------------------------------------------------------------------------
# one writer for the sign-in and the repair
# ---------------------------------------------------------------------------


def test_the_token_is_created_owner_only_before_its_secret_is_written(monkeypatch):
    opened: list[tuple[str, int, int]] = []
    real_open = os.open

    def spy(path, flags, mode=0o777, *args, **kwargs):
        opened.append((os.fspath(path), flags, mode))
        return real_open(path, flags, mode, *args, **kwargs)

    monkeypatch.setattr(setup.os, "open", spy)
    stale = tap_plugin_dir("codex") / ".token.tmp"
    stale.parent.mkdir(parents=True, exist_ok=True)
    stale.write_text("half a secret")
    stale.chmod(0o644)

    setup.write_paired_capture_token("codex", "ros_ing_secret", BASE)

    (path, flags, mode) = [entry for entry in opened if entry[0].endswith(".token.tmp")][0]
    assert mode == 0o600 and flags & os.O_EXCL, "created owner-only, never an old file reused"
    assert (tap_plugin_dir("codex") / ".token").stat().st_mode & 0o777 == 0o600
    assert not stale.exists()


def test_the_writer_puts_claude_codes_credential_in_the_cli_config_and_others_in_their_tap():
    setup.write_capture_credential("claude_code", "ros_ing_one", BASE)
    setup.write_capture_credential("codex", "ros_ing_two", BASE + "/")
    assert load_context()["ingest_token"] == "ros_ing_one"
    codex_dir = tap_plugin_dir("codex")
    assert (codex_dir / ".token").read_text() == "ros_ing_two"
    assert (codex_dir / ".token").stat().st_mode & 0o777 == 0o600
    assert json.loads((codex_dir / ".config").read_text()) == {"api_base_url": BASE}
    assert not (tap_plugin_dir("claude_code") / ".token").exists()


def test_the_event_carries_slugs_and_counts_only(monkeypatch):
    records: list[dict] = []
    monkeypatch.setenv("PROBE_TELEMETRY", "on")
    monkeypatch.setattr(tm, "_sender", None)
    monkeypatch.setattr(tm, "_flush_registered", True)
    monkeypatch.setattr(tm._Sender, "start", lambda self: None)
    monkeypatch.setattr(tm._Sender, "put", lambda self, rec: records.append(rec))

    assert tm.emit_capture_repair_applied(
        sources=["codex", "claude_code"], outcome="applied", locks_lifted=2,
        base_url="https://api.research.prbe.ai", kept_off=["pi"], confirmed=True,
    )
    (record,) = [r for r in records if r["event"] == tm.EVENT_CAPTURE_REPAIR_APPLIED]
    props = record["properties"]
    assert props["sources"] == ["claude_code", "codex"] and props["kept_off"] == ["pi"]
    assert props["outcome"] == "applied" and props["locks_lifted"] == 2 and props["confirmed"] is True
    assert not any(str(value).startswith("ros_ing_") for value in props.values()), "never a credential"
