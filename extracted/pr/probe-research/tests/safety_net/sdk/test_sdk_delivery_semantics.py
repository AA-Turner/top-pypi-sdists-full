"""Pins what a write does in each delivery mode, flag by flag (eng review O3).

For every mode (direct, journaled, offline) and every strict/sync/blocking combination,
against a server that answers, fails, refuses or is unreachable: what is sent, what is
journaled (and whether it holds the run's close), what raises, and what the client counts.
Disabled mode, per strict value (its `run.log` takes no sync or blocking). Recorded on main before the Sink interface (agent step 8); a move keeps it
byte-identical. Ops are read from disk, so no module path appears in the baseline.
"""

from __future__ import annotations

import errno
import itertools
import json
import warnings
from pathlib import Path
from typing import Any

import httpx
import pytest

import probe
from probe.sdk.client.client import Client
from probe.sdk.settings.settings import Settings
from probe.sdk.delivery.journal.journal import Journal
from probe.sdk.delivery.offline.client import OfflineClient
from probe.sdk.delivery.transport.transport import Transport

from tests.safety_net.sdk.sdk_session import close_open_runs

RUN = "11111111-1111-4111-8111-111111111111"
PATH = f"/v1/runs/{RUN}/metrics"
BODY = {"points": [{"key": "loss", "value": 1.0, "step": 1}]}
MODES = ("direct", "journaled", "offline")
#: What the fake server does with every request.
OUTCOMES = {
    "ok": lambda request: httpx.Response(200, json={"ok": True}),
    "transient": lambda request: httpx.Response(503, json={"detail": "down"}),
    "permanent": lambda request: httpx.Response(422, json={"detail": "refused"}),
    "conflict": lambda request: httpx.Response(409, json={"detail": "exists", "existing_id": RUN}),
    "unreachable": None,
}
STRICT = (None, True, False)
FLAGS = list(itertools.product(STRICT, (False, True), (True, False)))


@pytest.fixture(autouse=True)
def _quiet(monkeypatch):
    monkeypatch.delenv("PROBE_RUN_ID", raising=False)
    monkeypatch.delenv("PROBE_MODE", raising=False)
    monkeypatch.delenv("PROBE_ASYNC", raising=False)
    monkeypatch.delenv("PROBE_EXPORT_INTERVAL_SEC", raising=False)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        yield


class _Server:
    def __init__(self, outcome: str) -> None:
        self.outcome = outcome
        self.sent: list[str] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.sent.append(f"{request.method} {request.url.path}")
        answer = OUTCOMES[self.outcome]
        if answer is None:
            raise httpx.ConnectError("unreachable", request=request)
        return answer(request)


def _settings() -> Settings:
    return Settings(
        base_url="http://test",
        token="ros_pat_deadbeef",
        ingest_token="ros_ing_cafef00d",
        hmac_secret="s3cr3t",
        workspace="ws-mine",
    )


def _client(mode: str, server: _Server, folder: Path, *, fail_open: bool = True) -> Client:
    settings = _settings()
    journal = Journal(str(folder), context={"name": None, "base_url": settings.base_url})
    if mode == "offline":
        client = OfflineClient(settings, journal)
        client.fail_open = fail_open
        return client
    transport = Transport(
        settings,
        client=httpx.Client(base_url="http://test", transport=httpx.MockTransport(server)),
        max_retries=0,
    )
    return Client(
        settings=settings,
        transport=transport,
        journal=journal,
        fail_open=fail_open,
        async_writes=mode == "journaled",
        auto_drain=False,
    )


def _ops(folder: Path) -> list[dict]:
    """Every op on disk, by where it sits and what it would send."""
    found = []
    for path in sorted(folder.rglob("*.json")):
        parts = path.relative_to(folder).parts
        if parts[0] in ("producers",) or path.name == "status.json":
            continue
        try:
            op = json.loads(path.read_text())
        except ValueError:
            continue
        if not isinstance(op, dict) or "kind" not in op:
            continue
        found.append({
            "where": "/".join(parts[:-1]),
            "kind": op.get("kind"),
            "method": op.get("method"),
            "path": op.get("path"),
            "blocking": op.get("blocking"),
            "rejected": op.get("validation_error") is not None or op.get("kind") == "rejected_http",
        })
    return sorted(found, key=lambda op: json.dumps(op, sort_keys=True))


def _outcome(client: Client, server: _Server, folder: Path, call) -> dict[str, Any]:
    undelivered: list[dict] = []
    client.on_undelivered = undelivered.append
    raised = returned = None
    try:
        returned = call(client)
    except Exception as exc:  # noqa: BLE001 -- what raises is the point
        raised = type(exc).__name__
    ops = _ops(folder)
    return {
        "sent": server.sent,
        "raised": raised,
        "returned": returned if returned in (None, True, False) or isinstance(returned, dict) else type(returned).__name__,
        "journaled": ops,
        # An op without `blocking: false` holds the close (the journal omits the default).
        "holds_close": sum(1 for op in ops if op["blocking"] is not False and op["where"] == "ops"),
        "dropped": client.dropped_writes,
        "direct_sends": client.direct_sends,
        "undelivered": [{"queued": e["queued"], "path": e["path"]} for e in undelivered],
    }


def _cell(tmp_path: Path, name: str, mode: str, outcome: str, call, *, fail_open: bool = True, prepare=None) -> dict:
    folder = tmp_path / name
    server = _Server(outcome)
    client = _client(mode, server, folder, fail_open=fail_open)
    try:
        if prepare is not None:
            prepare(client)
        return _outcome(client, server, folder, call)
    finally:
        client.close()


def _write(**flags):
    return lambda client: client.write("POST", PATH, dict(BODY), **flags)


def _below_floor(client: Client) -> None:
    client.journal.below_floor = lambda: "test floor"


def _broken_append(error: BaseException):
    def prepare(client: Client) -> None:
        def append_http(*_a, **_kw):
            raise error

        client.journal.append_http = append_http
    return prepare


def test_each_mode_and_flag_does_what_it_did(tmp_path, baseline):
    table: dict[str, Any] = {}
    n = 0
    for mode, fail_open, outcome in itertools.product(MODES, (True, False), OUTCOMES):
        for strict, sync, blocking in FLAGS:
            n += 1
            key = f"{mode} fail_open={fail_open} server={outcome} strict={strict} sync={sync} blocking={blocking}"
            table[key] = _cell(tmp_path, f"c{n}", mode, outcome,
                               _write(strict=strict, sync=sync, blocking=blocking), fail_open=fail_open)
        extras = {
            "durable=False": _write(durable=False),
            "raise_permanent=True": _write(raise_permanent=True),
            "raise_permanent=True sync=True": _write(raise_permanent=True, sync=True),
            "admitted=True": _write(admitted=True),
            "nul body": lambda client: client.write("POST", PATH, {"points": BODY["points"], "note": "a\x00b"}),
            "nul body strict=True": lambda client: client.write(
                "POST", PATH, {"points": BODY["points"], "note": "a\x00b"}, strict=True),
            "best effort": lambda client: client._enqueue_best_effort("POST", PATH, dict(BODY)),
        }
        for label, call in extras.items():
            n += 1
            table[f"{mode} fail_open={fail_open} server={outcome} {label}"] = _cell(
                tmp_path, f"c{n}", mode, outcome, call, fail_open=fail_open)
    for mode, outcome in itertools.product(MODES, ("ok", "transient")):
        n += 1
        table[f"{mode} server={outcome} below the free-space floor"] = _cell(
            tmp_path, f"c{n}", mode, outcome, _write(), prepare=_below_floor)
        n += 1
        table[f"{mode} server={outcome} journal out of space"] = _cell(
            tmp_path, f"c{n}", mode, outcome, _write(), prepare=_broken_append(OSError(errno.ENOSPC, "full")))
        n += 1
        table[f"{mode} server={outcome} journal broken"] = _cell(
            tmp_path, f"c{n}", mode, outcome, _write(), prepare=_broken_append(OSError(errno.EROFS, "read-only")))
        n += 1
        table[f"{mode} server={outcome} best effort, journal broken"] = _cell(
            tmp_path, f"c{n}", mode, outcome, lambda client: client._enqueue_best_effort("POST", PATH, dict(BODY)),
            prepare=_broken_append(OSError(errno.EROFS, "read-only")))
    for mode in MODES:
        n += 1
        source = tmp_path / f"blob{n}.bin"
        source.write_bytes(b"x" * 64)
        table[f"{mode} upload"] = _cell(
            tmp_path, f"c{n}", mode, "ok",
            lambda client, src=str(source): bool(client._enqueue_upload(
                anchor="run", anchor_id=RUN, name="blob.bin", src_path=src, run_ref=RUN, blocking=False)))
    baseline("delivery_semantics", table)


def test_disabled_mode_records_nothing(tmp_path, monkeypatch, baseline):
    """``PROBE_MODE=disabled``: no client, no request, no queue, nothing raised."""
    sent: list[str] = []
    real_send = httpx.Client.send

    def send(self, request, *a, **kw):
        sent.append(f"{request.method} {request.url.path}")
        return real_send(self, request, *a, **kw)

    monkeypatch.setattr(httpx.Client, "send", send)
    monkeypatch.setenv("PROBE_MODE", "disabled")
    state = tmp_path / "state"
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    close_open_runs()
    table: dict[str, Any] = {}
    run = probe.init(project="p", name="r")
    for strict in STRICT:  # `run.log` takes strict only: sync and blocking are Client.write's
        raised = None
        try:
            run.log({"loss": 1.0}, step=1, strict=strict)
        except Exception as exc:  # noqa: BLE001
            raised = type(exc).__name__
        table[f"log strict={strict}"] = {"raised": raised}
    raised = None
    try:
        run.finish()
    except Exception as exc:  # noqa: BLE001
        raised = type(exc).__name__
    table["finish"] = {"raised": raised}
    table["run type"] = type(run).__name__
    table["sent"] = sent
    table["files written"] = sorted(str(p.relative_to(state)) for p in state.rglob("*") if p.is_file()) \
        if state.exists() else []
    close_open_runs()
    baseline("delivery_semantics_disabled", table)


# -- failure policy, beyond the five answers above (plan sdk-typed-write-ops T10/T11) --------------
#: Recorded before DirectSink became Sender + one policy resolver: every answer the classifier
#: (`ops/classify.py`) sorts differently, a 2xx that is not JSON, a client whose transport was
#: injected (forced sync, as hosted MCP), and a CLI client whose `raise_permanent` is set after
#: construction (`cli/connection.py`).
POLICY_OUTCOMES = {
    "unauthorized": lambda request: httpx.Response(401, json={"detail": "bad token"}),
    "forbidden": lambda request: httpx.Response(403, json={"detail": "missing scope"}),
    "timeout": lambda request: httpx.Response(408, json={"detail": "slow"}),
    "throttled": lambda request: httpx.Response(429, json={"detail": "slow down"}, headers={"Retry-After": "0"}),
    "not_implemented": lambda request: httpx.Response(501, json={"detail": "no"}),
    "html": lambda request: httpx.Response(200, text="<html>gateway</html>", headers={"content-type": "text/html"}),
    "empty": lambda request: httpx.Response(204),
}
POLICY_MODES = ("direct", "journaled", "offline", "injected")


class _PolicyServer(_Server):
    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.sent.append(f"{request.method} {request.url.path}")
        if self.outcome == "bug":
            raise RuntimeError("a bug of ours in the transport")
        answer = POLICY_OUTCOMES.get(self.outcome) or OUTCOMES[self.outcome]
        if answer is None:
            raise httpx.ConnectError("unreachable", request=request)
        return answer(request)


def _policy_client(mode: str, server: _Server, folder: Path, *, fail_open: bool) -> Client:
    if mode != "injected":
        return _client(mode, server, folder, fail_open=fail_open)
    settings = _settings()
    journal = Journal(str(folder), context={"name": None, "base_url": settings.base_url})
    transport = Transport(
        settings, client=httpx.Client(base_url="http://test", transport=httpx.MockTransport(server)), max_retries=0)
    # async_writes left to the client: an injected transport makes it sync (hosted MCP).
    return Client(settings=settings, transport=transport, journal=journal, fail_open=fail_open, auto_drain=False)


def _policy_cell(tmp_path: Path, name: str, mode: str, outcome: str, call, *, fail_open: bool, prepare=None) -> dict:
    folder = tmp_path / name
    server = _PolicyServer(outcome)
    client = _policy_client(mode, server, folder, fail_open=fail_open)
    try:
        if prepare is not None:
            prepare(client)
        cell = _outcome(client, server, folder, call)
        cell["async_writes"] = client.async_writes
        return cell
    finally:
        client.close()


def _cli_raise_permanent(client: Client) -> None:
    client.raise_permanent = True  # the CLI sets it after construction


def test_each_failure_policy_does_what_it_did(tmp_path, baseline):
    table: dict[str, Any] = {}
    n = 0
    flags = list(itertools.product(STRICT, (False, True), (None, True)))
    outcomes = [*POLICY_OUTCOMES, "bug"]
    for mode, fail_open in itertools.product(POLICY_MODES, (True, False)):
        for outcome in (outcomes if mode != "injected" else [*outcomes, *OUTCOMES]):
            for strict, sync, raise_permanent in flags:
                n += 1
                table[f"{mode} fail_open={fail_open} server={outcome} strict={strict} sync={sync} "
                      f"raise_permanent={raise_permanent}"] = _policy_cell(
                    tmp_path, f"p{n}", mode, outcome,
                    _write(strict=strict, sync=sync, raise_permanent=raise_permanent), fail_open=fail_open)
            for label, call, prepare in (
                ("durable=False", _write(durable=False), None),
                ("client raise_permanent", _write(), _cli_raise_permanent),
                ("client raise_permanent sync=True", _write(sync=True), _cli_raise_permanent),
                ("client raise_permanent strict=False", _write(strict=False), _cli_raise_permanent),
            ):
                n += 1
                table[f"{mode} fail_open={fail_open} server={outcome} {label}"] = _policy_cell(
                    tmp_path, f"p{n}", mode, outcome, call, fail_open=fail_open, prepare=prepare)
        for outcome in ("ok", "transient", "permanent"):
            n += 1
            table[f"{mode} fail_open={fail_open} server={outcome} client raise_permanent"] = _policy_cell(
                tmp_path, f"p{n}", mode, outcome, _write(), fail_open=fail_open, prepare=_cli_raise_permanent)
        for strict, sync in itertools.product(STRICT, (False, True)):
            n += 1
            # An experiment write is addressed by whether it will be queued (`_journals`).
            table[f"{mode} fail_open={fail_open} journals strict={strict} sync={sync}"] = _policy_cell(
                tmp_path, f"p{n}", mode, "ok",
                lambda client, s=strict, y=sync: client._journals(strict=s, sync=y), fail_open=fail_open)
    n += 1

    def queue_only_write(client: Client):
        from probe.sdk.delivery.sinks.direct import queue_only  # where the snapshot gate imports it

        with queue_only():
            return client.write("POST", PATH, dict(BODY))

    table["journaled server=ok below the floor inside queue_only"] = _policy_cell(
        tmp_path, f"p{n}", "journaled", "ok", queue_only_write, fail_open=True, prepare=_below_floor)
    baseline("delivery_semantics_policy", table)
