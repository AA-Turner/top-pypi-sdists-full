"""Goldens for `Transport.request`: every attempt it sends, the pauses between them, what it tells
its observer, and the response or typed error it returns, over scripted server answers."""

from __future__ import annotations

import warnings

import httpx
import pytest

from probe.sdk.delivery.transport import deadlines as deadlines_module
from probe.sdk.delivery.transport import protocols
from probe.sdk.delivery.transport.transport import Transport
from probe.sdk.settings.settings import Settings
from tests.sdk.delivery.goldens.recorder import Normaliser, check, describe_error, record_transport_sleeps

#: Headers whose values say something stable about the request (never a secret or a clock).
_SHOWN = ("content-type", "x-probe-surface", "x-probe-leases", "x-probe-attribution", "x-test-flag",
          "content-encoding")


@pytest.fixture(autouse=True)
def _isolated(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))
    monkeypatch.delenv("PROBE_IDEMPOTENCY_KEY", raising=False)


class Recorder:
    """Observer stand-in plus the scripted server."""

    def __init__(self, answers: list, norm: Normaliser):
        self.answers = list(answers)
        self.norm = norm
        self.sent: list[dict] = []
        self.events: list[list] = []

    def handler(self, request: httpx.Request) -> httpx.Response:
        auth = request.headers.get("authorization", "")
        self.sent.append({
            "method": request.method,
            "path": request.url.path,
            "query": dict(sorted(request.url.params.items())),
            "header_names": sorted(request.headers.keys()),
            "headers": {k: request.headers[k] for k in _SHOWN if k in request.headers},
            "auth": auth.split("_")[0] if auth else None,
            "signed": "x-signature" in request.headers,
            "body": request.content.decode(errors="replace") if request.content else None,
        })
        answer = self.answers.pop(0) if self.answers else 200
        if isinstance(answer, BaseException):
            raise answer
        if isinstance(answer, int):
            return httpx.Response(answer, json={"detail": f"scripted {answer}"})
        status, payload, *rest = answer
        return httpx.Response(status, json=payload, headers=rest[0] if rest else {})

    # TransportObserver
    def begin_transport(self, method, path, **kw):
        self.events.append(["begin", method, path])

    def end_transport(self):
        self.events.append(["end"])

    def record_transport(self, method, path, **kw):
        self.events.append(["record", method, path, kw.get("status"), self.norm.text(kw.get("error") or "")])


def run(tmp_path, monkeypatch, answers, call, *, settings=None, scope=None):
    norm = Normaliser(tmp_path)
    rec = Recorder(answers, norm)
    monkeypatch.setattr(protocols, "_observer", rec)
    sleeps: list[float] = []
    record_transport_sleeps(monkeypatch, sleeps)
    settings = settings or Settings(base_url="http://test", token="ros_pat_deadbeef",
                                    ingest_token="ros_ing_cafef00d", hmac_secret="s3cr3t")
    client = httpx.Client(base_url="http://test", transport=httpx.MockTransport(rec.handler))
    transport = Transport(settings, client=client)
    outcome: dict
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            with scope() if scope else _nothing():
                resp = call(transport)
            outcome = {"status": resp.status_code, "body": resp.text}
        except Exception as exc:  # noqa: BLE001 -- the error IS the golden
            outcome = {"error": describe_error(exc, norm)}
    return {"sent": rec.sent, "observer": rec.events, "sleeps": [s > 0 for s in sleeps], "pauses": sleeps,
            "outcome": outcome, "warnings": [norm.text(str(w.message)) for w in caught]}


class _nothing:
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _post(path="/v1/runs/r/metrics", body=None, **kw):
    return lambda t: t.request("POST", path, json_body=body if body is not None else {"points": []}, **kw)


def _get(path="/v1/runs/r", **kw):
    return lambda t: t.request("GET", path, **kw)


SCENARIOS = {
    "get_ok": ([(200, {"id": "r"})], _get(params={"cursor": "c1"})),
    "post_created": ([(201, {"id": "x"})], _post()),
    "post_503_not_retried": ([503], _post()),
    "get_503_then_ok": ([503, 503, (200, {"ok": True})], _get()),
    "get_503_exhausted": ([503] * 6, _get()),
    "post_idempotent_flag_retries": ([502, (200, {})], _post(idempotent=True)),
    "put_retried_by_default": ([504, (200, {})], lambda t: t.request("PUT", "/v1/runs/r/config", json_body={"a": 1})),
    "post_connect_error_replayed": ([httpx.ConnectError("refused"), (201, {})], _post()),
    "post_connect_error_exhausted": ([httpx.ConnectError("refused")] * 6, _post()),
    "post_read_timeout_not_replayed": ([httpx.ReadTimeout("lost")], _post()),
    "get_read_timeout_retried": ([httpx.ReadTimeout("lost"), (200, {})], _get()),
    "retry_after_short": ([(429, {"detail": "slow"}, {"Retry-After": "1"}), (200, {})], _get()),
    "retry_after_too_long": ([(429, {"detail": "slow"}, {"Retry-After": "120"})], _get()),
    "auth_401": ([(401, {"detail": "invalid or revoked token"})], _post()),
    "scope_403": ([(403, {"detail": "insufficient scope: write required"})], _post()),
    "not_found_404": ([(404, {"detail": "no such run"})], _get()),
    "not_found_under_workspace_limit": ([(404, {"detail": "no such run"}, {"X-Probe-Workspace-Limit-Applied": "ws-1"})], _get()),
    "conflict_409_existing": ([(409, {"detail": {"existing_id": "abc"}})], _post()),
    "gone_410_trash": ([(410, {"detail": "in_trash", "message": "in the trash since today"})], _get()),
    "validation_422": ([(422, {"detail": [{"loc": ["body"], "msg": "bad"}]})], _post()),
    "client_too_old": ([(426, {"detail": "upgrade", "code": "client_too_old", "min_version": "9.9.9"})], _get()),
    "server_500": ([500], _post()),
    "delete_retry_finds_trash": ([502, (404, {"detail": "in_trash", "message": "in the trash"})],
                                 lambda t: t.request("DELETE", "/v1/runs/r", idempotent=True)),
    "ingest_signed": ([(202, {})], lambda t: t.request("POST", "/ingest/v1", json_body={"events": [1]})),
    "public_read_no_auth": ([(200, {"docs": []})], lambda t: t.request("GET", "/public/v1/docs")),
    "raw_content": ([(200, {})], lambda t: t.request("PUT", "/v1/catalog/manifest", content=b"\x1f\x8bzz",
                                                     content_headers={"Content-Encoding": "gzip"})),
    "extra_headers": ([(201, {})], _post(extra_headers={"X-Test-Flag": "1"})),
    "sql_kept_verbatim": ([(200, {"rows": []})], _post("/v1/sql", {"sql": "select 'sk-baseline'"})),
    "nul_in_path": ([], lambda t: t.request("GET", "/v1/runs/a\x00b")),
    "nul_in_body_escaped": ([(201, {})], _post(body={"name": "a\x00b"})),
    "both_bodies": ([], lambda t: t.request("POST", "/v1/x", json_body={}, content=b"x")),
    "typed_get_post_delete": ([(200, {"a": 1}), (201, {"b": 2}), (204, None)],
                              lambda t: httpx.Response(200, json=[t.get("/v1/a"), t.post("/v1/b", {"x": 1}),
                                                                    t.delete("/v1/c")])),
}


@pytest.mark.parametrize("name", sorted(SCENARIOS))
def test_transport_golden(name, tmp_path, monkeypatch):
    answers, call = SCENARIOS[name]
    check(f"transport/{name}", run(tmp_path, monkeypatch, answers, call))


def test_transport_golden_no_token(tmp_path, monkeypatch):
    settings = Settings(base_url="http://test", token=None)
    check("transport/no_token", run(tmp_path, monkeypatch, [], _post(), settings=settings))


def test_transport_golden_deadline_passed(tmp_path, monkeypatch):
    scope = lambda: deadlines_module.deadline_scope(0.0)  # noqa: E731 -- a deadline already gone
    check("transport/deadline_passed", run(tmp_path, monkeypatch, [(200, {})], _get(), scope=scope))


def test_transport_golden_closed_client(tmp_path, monkeypatch):
    def call(t):
        t.close()
        return t.request("GET", "/v1/runs/r")

    check("transport/closed_client", run(tmp_path, monkeypatch, [], call))


def test_transport_golden_idempotency_key(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_IDEMPOTENCY_KEY", "op-1")
    record = run(tmp_path, monkeypatch, [(201, {}), (200, {})],
                 lambda t: (t.request("POST", "/v1/runs/r/metrics", json_body={}), t.request("GET", "/v1/r"))[1])
    record["keys"] = [("idempotency-key" in s["header_names"]) for s in record["sent"]]
    check("transport/idempotency_key", record)
