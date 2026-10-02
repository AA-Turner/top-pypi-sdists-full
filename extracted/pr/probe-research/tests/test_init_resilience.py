"""`probe.init()` survives an API that is briefly down or loses a response (plan 2.5).

Measured before this: a refused API raised into the training script after
1.9 s, a blackholed one after 122 s, and a create whose response was lost was
either a hard error or -- retried -- a SECOND run. The tests below drive the
real SDK through a fake backend that commits the create and then drops the
answer, refuses connections, or answers 503 with `Retry-After`, on a fake clock
so a 90 s budget costs no wall time.
"""

from __future__ import annotations

import contextlib

import json
import re

import httpx
import pytest

import probe
from probe.sdk import errors, fluent, transport
from tests.conftest import make_client

_RUN_CREATE = re.compile(r"^/v1/(?:projects|experiments)/[^/]+/runs$|^/v1/runs$")


class FakeClock:
    """`time` for the transport: sleeping advances `monotonic()` instantly."""

    def __init__(self) -> None:
        self.now = 1_000.0
        self.sleeps: list[float] = []

    def monotonic(self) -> float:
        return self.now

    def time(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += max(0.0, seconds)


@pytest.fixture
def clock(monkeypatch) -> FakeClock:
    fake = FakeClock()
    monkeypatch.setattr(transport, "time", fake)
    return fake


@pytest.fixture(autouse=True)
def _clean_binding(monkeypatch):
    # A PROBE_RUN_ID leaked by another test in this worker (the miles
    # integration exports one) would turn every init here into an attach.
    monkeypatch.delenv("PROBE_RUN_ID", raising=False)
    fluent._current.set(None)
    fluent._process_default = None
    yield
    fluent._current.set(None)
    fluent._process_default = None


class Faults:
    """Wraps the fake backend's handler. Each rule is `(method, path regex,
    action)`; an action runs once per matching request until it returns None,
    after which the real backend answers."""

    def __init__(self, app) -> None:
        self.app = app
        self.real = app.handler
        self.rules: list[tuple[str, re.Pattern, list]] = []
        self.seen: list[httpx.Request] = []

    def add(self, method: str, pattern: re.Pattern | str, *actions) -> None:
        compiled = re.compile(pattern) if isinstance(pattern, str) else pattern
        self.rules.append((method, compiled, list(actions)))

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.seen.append(request)
        for method, pattern, actions in self.rules:
            if request.method == method and pattern.search(request.url.path) and actions:
                return actions.pop(0)(request)
        return self.real(request)

    def creates(self) -> list[httpx.Request]:
        return [r for r in self.seen if r.method == "POST" and _RUN_CREATE.match(r.url.path)]


def refuse(request: httpx.Request) -> httpx.Response:
    raise httpx.ConnectError("[Errno 111] Connection refused", request=request)


def status(code: int, *, retry_after: str | None = None):
    def answer(request: httpx.Request) -> httpx.Response:
        headers = {"Retry-After": retry_after} if retry_after is not None else {}
        return httpx.Response(code, json={"detail": f"injected {code}"}, headers=headers)

    return answer


def commit_then_lose(faults: Faults):
    """The server PROCESSES the create, then the answer never arrives."""

    def lose(request: httpx.Request) -> httpx.Response:
        faults.real(request)
        raise httpx.ReadTimeout("the response was lost", request=request)

    return lose


@pytest.fixture
def faulty(app, tmp_path, monkeypatch) -> Faults:
    """`probe.init()` builds its client against the fake backend, through `Faults`."""
    faults = Faults(app)
    app.handler = faults  # make_client binds `app.handler` at construction
    monkeypatch.setattr(
        fluent, "Client", lambda *_a, **_kw: make_client(app, tmp_spool=tmp_path / "spool")
    )
    app.seed_experiment("e1")
    return faults


def _bodies(requests: list[httpx.Request]) -> list[dict]:
    return [json.loads(r.content) for r in requests]


# -- a lost create response ----------------------------------------------------
def test_a_lost_create_response_is_replayed_into_the_same_run(app, faulty, clock):
    faulty.add("POST", _RUN_CREATE, commit_then_lose(faulty))
    run = probe.init(experiment="e1", name="r1")
    probe.finish()

    assert len(app.runs) == 1, "the retry must not make a second run"
    assert run.id in app.runs
    first, again = _bodies(faulty.creates())
    assert first == again, "the replay is the SAME request, key and body"
    assert len(first["creation_key"]) == 32


def test_on_a_server_without_creation_keys_a_lost_create_is_not_resent(app, faulty, clock):
    """Negative control: re-sending there would make a duplicate run, so the
    failure stands -- and exactly one run exists, not two."""
    app.supports_creation_key = False
    faulty.add("POST", _RUN_CREATE, commit_then_lose(faulty))
    with pytest.raises(errors.TransportError):
        probe.init(experiment="e1", name="r1")
    assert len(faulty.creates()) == 1
    assert len(app.runs) == 1


def test_a_gateway_503_on_the_create_is_retried_once_known_safe(app, faulty, clock):
    faulty.add("POST", _RUN_CREATE, status(503), status(502))
    run = probe.init(experiment="e1", name="r1")
    probe.finish()
    assert len(app.runs) == 1 and run.id in app.runs
    assert len({b["creation_key"] for b in _bodies(faulty.creates())}) == 1


def test_a_lost_create_with_an_external_id_replays_instead_of_conflicting(app, faulty, clock):
    """Today this is a 409 against its own create, and `on_conflict="auto"`
    would then treat the caller's own live run as an incumbent."""
    faulty.add("POST", _RUN_CREATE, commit_then_lose(faulty))
    run = probe.init(experiment="e1", name="r1", external_id="job-7", source="sdk")
    probe.finish()
    assert len(app.runs) == 1
    assert app.runs[run.id]["external_id"] == "job-7", "not superseded as job-7-r2"


def test_each_create_mints_its_own_key(app, faulty, clock):
    probe.init(experiment="e1", name="a")
    probe.finish()
    probe.init(experiment="e1", name="b")
    probe.finish()
    keys = [b["creation_key"] for b in _bodies(faulty.creates())]
    assert len(keys) == 2 and keys[0] != keys[1]


# -- the retry budget ----------------------------------------------------------
def test_init_rides_out_a_short_outage(app, faulty, clock):
    faulty.add("GET", r"^/v1/", refuse, refuse, refuse, refuse, refuse, refuse)
    run = probe.init(experiment="e1", name="r1")
    probe.finish()
    assert run.id in app.runs
    assert len(clock.sleeps) == 6, "six refusals, six waits, beyond the old 3 retries"
    # The patience ladder: 0.5, 1, 2, 4, 8, 10 s, each jittered to [half, full].
    for wait, step in zip(clock.sleeps, (0.5, 1, 2, 4, 8, 10)):
        assert step / 2 <= wait <= step, (wait, step)


def test_init_gives_up_when_its_budget_is_spent(app, faulty, clock, monkeypatch):
    monkeypatch.setenv("PROBE_INIT_TIMEOUT_SEC", "5")
    faulty.add("GET", r"^/v1/", *([refuse] * 1000))
    started = clock.now
    with pytest.raises(errors.TransportError):
        probe.init(experiment="e1", name="r1")
    spent = clock.now - started
    assert 3.0 <= spent <= 5.0, spent
    assert len(faulty.seen) > 4, "more than the old 1 + 3 attempts"
    assert not faulty.creates()


def test_a_zero_budget_keeps_the_old_quick_retries(app, faulty, clock, monkeypatch):
    monkeypatch.setenv("PROBE_INIT_TIMEOUT_SEC", "0")
    faulty.add("GET", r"^/v1/", *([refuse] * 1000))
    with pytest.raises(errors.TransportError):
        probe.init(experiment="e1", name="r1")
    assert len(faulty.seen) == 4, "one try and max_retries=3 retries"
    assert sum(clock.sleeps) < 2.0


@pytest.mark.parametrize("code, error", [(404, errors.NotFoundError), (401, errors.AuthError)])
def test_a_refusal_is_one_request_and_no_wait(app, faulty, clock, code, error):
    faulty.add("POST", _RUN_CREATE, status(code))
    with pytest.raises(error):
        probe.init(experiment="e1", name="r1")
    assert len(faulty.creates()) == 1
    assert clock.sleeps == []


def test_retry_after_is_honoured(app, faulty, clock):
    faulty.add("GET", r"^/v1/", status(503, retry_after="7"))
    probe.init(experiment="e1", name="r1")
    probe.finish()
    assert clock.sleeps and clock.sleeps[0] >= 7.0


def test_a_retry_after_longer_than_the_budget_is_not_waited_out(app, faulty, clock, monkeypatch):
    monkeypatch.setenv("PROBE_INIT_TIMEOUT_SEC", "5")
    faulty.add("GET", r"^/v1/", status(503, retry_after="60"))
    with pytest.raises(errors.ServerError):
        probe.init(experiment="e1", name="r1")
    assert clock.sleeps == []


def test_a_create_resent_after_a_503_waits_its_retry_after(app, faulty, clock):
    faulty.add("POST", _RUN_CREATE, status(503, retry_after="4"))
    probe.init(experiment="e1", name="r1")
    probe.finish()
    assert len(faulty.creates()) == 2
    assert any(wait >= 4.0 for wait in clock.sleeps), clock.sleeps


def test_an_unreadable_budget_warns_and_keeps_the_default(monkeypatch):
    from probe.sdk import config

    monkeypatch.setenv("PROBE_INIT_TIMEOUT_SEC", "ninety")
    with pytest.warns(UserWarning, match="PROBE_INIT_TIMEOUT_SEC"):
        assert config.init_timeout_seconds() == config.DEFAULT_INIT_TIMEOUT_SEC


# -- the transport scope itself ------------------------------------------------
def _refusing_transport(counter: list) -> transport.Transport:
    def handler(request: httpx.Request) -> httpx.Response:
        counter.append(request)
        raise httpx.ConnectError("refused", request=request)

    from probe.sdk.config import Settings

    settings = Settings(base_url="http://test", token="ros_pat_x")
    http = httpx.Client(base_url="http://test", transport=httpx.MockTransport(handler))
    return transport.Transport(settings, client=http)


def test_without_patience_restores_quick_retries_inside_a_scope(clock):
    patient, carved = [], []
    with transport.patience(30):
        with pytest.raises(errors.TransportError):
            _refusing_transport(patient).request("GET", "/v1/me")
        with transport.without_patience():
            assert transport._request_deadline.get() is None
            with pytest.raises(errors.TransportError):
                _refusing_transport(carved).request("GET", "/v1/me")
        assert transport._request_deadline.get() is not None
    assert len(patient) > 4
    assert len(carved) == 4


def test_a_patient_write_that_may_have_landed_is_not_resent(clock):
    """Patience changes HOW LONG, never WHAT: a non-idempotent POST that timed
    out after it was sent goes back to the caller on the first failure."""
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        raise httpx.ReadTimeout("lost", request=request)

    from probe.sdk.config import Settings

    http = httpx.Client(base_url="http://test", transport=httpx.MockTransport(handler))
    t = transport.Transport(Settings(base_url="http://test", token="ros_pat_x"), client=http)
    with transport.patience(30), pytest.raises(errors.TransportError) as caught:
        t.request("POST", "/v1/projects/p/runs", json_body={"name": "x"})
    assert len(calls) == 1
    assert transport.outcome_unknown(caught.value)


def test_outcome_unknown_reads_only_ambiguous_failures():
    request = httpx.Request("POST", "http://test/v1/runs")
    refused = errors.TransportError("refused")
    refused.__cause__ = httpx.ConnectError("refused", request=request)
    lost = errors.TransportError("lost")
    lost.__cause__ = httpx.ReadTimeout("lost", request=request)
    assert not transport.outcome_unknown(refused)
    assert transport.outcome_unknown(lost)
    assert transport.outcome_unknown(errors.ServerError("gw", status=504))
    assert not transport.outcome_unknown(errors.ServerError("app", status=500))
    assert not transport.outcome_unknown(errors.ValidationError("no", status=422))
    assert transport.outcome_unknown(errors.DeadlineExceeded("cut", sent=True))
    assert not transport.outcome_unknown(errors.DeadlineExceeded("never sent"))


# -- review of #2027 -----------------------------------------------------------
def _crashed_incumbent(app, external_id: str) -> str:
    """A dead run holding `external_id`, so `on_conflict="auto"` resumes it."""
    client = make_client(app)
    eid = next(e["id"] for e in app.experiments.values() if e["slug"] == "e1")
    run = client.create_run(eid, "incumbent", external_id=external_id, source="sdk", heartbeat=False)
    client.close()
    app.runs[run.id]["status"] = "crashed"
    return run.id


def _slow_resume(monkeypatch, *, opt_out: bool, wait: float = 120.0):
    """A reopen step that waits longer than init's whole budget first -- the
    shape of a requeue takeover waiting out a dead incumbent (plan 2.3)."""
    from probe.sdk.client import Client

    real = Client._resume_run

    def slow(self, old, run_kw, **kw):
        if opt_out:
            with transport.without_patience():
                transport.time.sleep(wait)
                return real(self, old, run_kw, **kw)
        transport.time.sleep(wait)
        return real(self, old, run_kw, **kw)

    monkeypatch.setattr(Client, "_resume_run", slow)


def test_a_step_can_opt_out_of_the_init_budget(app, faulty, clock, monkeypatch):
    """`without_patience()` is the door a long, bounded step inside init uses
    (lane F's takeover wait): its requests are not cut by init's deadline."""
    monkeypatch.setenv("PROBE_INIT_TIMEOUT_SEC", "30")
    incumbent = _crashed_incumbent(app, "job-9")
    _slow_resume(monkeypatch, opt_out=True)
    run = probe.init(experiment="e1", external_id="job-9", source="sdk")
    probe.finish()
    assert run.id == incumbent, "resumed after a 120 s wait inside a 30 s budget"


def test_without_the_opt_out_the_init_budget_cuts_the_step_off(app, faulty, clock, monkeypatch):
    """Negative control for the test above."""
    monkeypatch.setenv("PROBE_INIT_TIMEOUT_SEC", "30")
    _crashed_incumbent(app, "job-9")
    _slow_resume(monkeypatch, opt_out=False)
    with pytest.raises(errors.DeadlineExceeded):
        probe.init(experiment="e1", external_id="job-9", source="sdk")


def test_the_heartbeat_thread_starts_outside_the_init_budget(app, faulty, clock, monkeypatch):
    """A thread that inherits its creator's context (free-threaded 3.14) must
    not carry init's deadline for the life of the run."""
    from probe.sdk.run import Run

    seen = []
    monkeypatch.setattr(
        Run,
        "start_heartbeat",
        lambda self, **kw: seen.append((transport._request_deadline.get(), transport._patient())),
    )
    probe.init(experiment="e1", name="r1")
    probe.finish()
    assert seen == [(None, False)]


def test_a_huge_retry_after_raises_at_once_instead_of_sleeping(app, faulty, clock, monkeypatch):
    """`Retry-After: 3600` on a create, outside any budget (PROBE_INIT_TIMEOUT_SEC=0,
    `probe run start`, a direct Client.run()): raise now, never sleep an hour."""
    monkeypatch.setenv("PROBE_INIT_TIMEOUT_SEC", "0")
    faulty.add("POST", _RUN_CREATE, status(503, retry_after="3600"))
    with pytest.raises(errors.ServerError):
        probe.init(experiment="e1", name="r1")
    assert clock.sleeps == []
    assert len(faulty.creates()) == 1


def test_a_retry_after_that_does_not_fit_the_budget_raises_at_once(app, faulty, clock, monkeypatch):
    monkeypatch.setenv("PROBE_INIT_TIMEOUT_SEC", "5")
    faulty.add("POST", _RUN_CREATE, status(503, retry_after="8"))
    started = clock.now
    with pytest.raises(errors.ServerError):
        probe.init(experiment="e1", name="r1")
    assert clock.now - started < 1.0, "not the whole budget slept away first"
    assert len(faulty.creates()) == 1


@pytest.mark.parametrize("method", ["GET", "POST"], ids=["read", "create"])
def test_a_long_retry_after_inside_the_budget_is_waited_out_by_reads_and_creates_alike(
    app, faulty, clock, method
):
    """One rule for one header: `Retry-After: 30` inside init's 90 s budget is
    waited out whether it answered a read (the transport's `_patient_pause`)
    or a create (the re-send's `wait_out_retry_after`). The create used to
    raise at once, because its rule still applied the 10 s cap for code
    running outside any budget."""
    faulty.add(method, _RUN_CREATE if method == "POST" else r"^/v1/", status(503, retry_after="30"))
    run = probe.init(experiment="e1", name="r1")
    probe.finish()
    assert list(app.runs) == [run.id]
    assert any(wait >= 30.0 for wait in clock.sleeps), clock.sleeps
    if method == "POST":
        assert len(faulty.creates()) == 2, "the create was re-sent once, after the wait"


def test_a_429_on_the_create_is_resent_even_without_creation_keys(app, faulty, clock):
    """Rate limiting refuses BEFORE processing: nothing landed, so a re-send is
    safe on any server -- after the Retry-After it asked for."""
    app.supports_creation_key = False
    faulty.add("POST", _RUN_CREATE, status(429, retry_after="3"))
    run = probe.init(experiment="e1", name="r1")
    probe.finish()
    assert len(faulty.creates()) == 2
    assert list(app.runs) == [run.id]
    assert any(wait >= 3.0 for wait in clock.sleeps), clock.sleeps


def test_the_first_retry_says_so_once_on_stderr(app, faulty, clock, capsys):
    faulty.add("GET", r"^/v1/", refuse, refuse, refuse)
    probe.init(experiment="e1", name="r1")
    probe.finish()
    err = capsys.readouterr().err
    assert err.count("keeps retrying for up to 90s (PROBE_INIT_TIMEOUT_SEC)") == 1


def test_jitter_never_moves_the_callers_random_stream(app, faulty, clock):
    import random

    random.seed(1234)
    expected = [random.random() for _ in range(3)]
    random.seed(1234)
    faulty.add("GET", r"^/v1/", refuse, refuse, refuse)
    probe.init(experiment="e1", name="r1")
    probe.finish()
    assert clock.sleeps, "the patient path (and its jitter) ran"
    assert [random.random() for _ in range(3)] == expected


# -- lane F, 2.3: a requeue takeover inside probe.init() -------------------------


def _quiet_incumbent(app, external_id: str) -> str:
    """A `running` incumbent whose owner beat on a cadence and went quiet 30 s
    ago: a takeover must wait ~150 s for it (threshold 180 s)."""
    client = make_client(app)
    eid = next(e["id"] for e in app.experiments.values() if e["slug"] == "e1")
    run = client.create_run(eid, "incumbent", external_id=external_id, source="sdk", heartbeat=False)
    client.close()
    app.run_heartbeats[run.id] = 2  # a beat after the insert: a cadence
    app.run_beat_silence[run.id] = 30.0
    app.run_silence[run.id] = 30.0
    return run.id


@pytest.mark.parametrize("wrapped", [True, False], ids=["wrapped", "control"])
def test_a_takeover_wait_is_not_cut_off_by_the_init_budget(
    app, faulty, clock, monkeypatch, wrapped
):
    """Review of #2019: the takeover wait (~150 s here) is far longer than
    init's 30 s budget and is bounded by PROBE_TAKEOVER_WAIT_SEC instead. The
    control drops the opt-out and the budget cuts the requeue off."""
    from probe.sdk import client as client_mod

    monkeypatch.setenv("PROBE_INIT_TIMEOUT_SEC", "30")
    monkeypatch.setenv("PROBE_TAKEOVER_WAIT_SEC", "300")
    incumbent = _quiet_incumbent(app, "job-requeue")

    def time_passes(seconds: float) -> None:
        clock.sleep(seconds)  # the transport's clock: init's deadline moves
        for rid in list(app.run_beat_silence):
            app.run_beat_silence[rid] += seconds
            app.run_silence[rid] += seconds

    monkeypatch.setattr(client_mod, "_takeover_sleep", time_passes)
    if not wrapped:
        monkeypatch.setattr(transport, "without_patience", contextlib.nullcontext)

    if wrapped:
        run = probe.init(experiment="e1", external_id="job-requeue", source="sdk")
        probe.finish()
        assert run.id == incumbent and run.write_epoch == 2, "took the run over"
        assert clock.sleeps and sum(clock.sleeps) >= 140
    else:
        with pytest.raises(errors.DeadlineExceeded):
            probe.init(experiment="e1", external_id="job-requeue", source="sdk")
