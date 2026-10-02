"""Run liveness, SDK side: the auto-heartbeat thread.

The server reaps only runs that have beat at least once, so the thread's one job
is to make an SDK-owned run reapable for exactly as long as this process owns
it: first beat immediately at create, stop on the terminal PATCH. The negative
space matters as much: detached creates (CLI `run start`, the miles exporter,
raw `Run(...)` attach handles) must never beat, because beating once and going
silent gets a legitimately-running run reaped as crashed.
"""

from __future__ import annotations

import gc
import time
import warnings

import pytest

from probe.sdk.run import Run
from probe.sdk.session_marker import WIZARD_HINT
from tests.conftest import make_client, open_run


def _wait_for(predicate, timeout: float = 5.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.01)
    return predicate()


def test_create_run_beats_immediately_and_finish_stops_it(client, app, monkeypatch):
    monkeypatch.setenv("PROBE_HEARTBEAT_SECONDS", "60")
    run = open_run(client, experiment="e", name="r")
    # First beat lands at start, not one interval later: a run that crashes
    # five seconds in must already be reapable.
    assert _wait_for(lambda: app.run_heartbeats.get(run.id, 0) >= 1)
    assert app.runs[run.id]["last_heartbeat_at"]
    thread = run._hb_thread
    assert thread is not None and thread.is_alive()
    run.finish()
    thread.join(timeout=5)
    assert not thread.is_alive()
    assert run._hb_thread is None


def test_beats_keep_coming_on_the_interval(client, app):
    run = open_run(client, experiment="e", name="r", heartbeat=False)
    run.start_heartbeat(0.01)
    assert _wait_for(lambda: app.run_heartbeats.get(run.id, 0) >= 3)
    run.stop_heartbeat()


def test_start_heartbeat_is_idempotent(client, app):
    run = open_run(client, experiment="e", name="r", heartbeat=False)
    run.start_heartbeat(0.01)
    first = run._hb_thread
    run.start_heartbeat(0.01)
    assert run._hb_thread is first
    run.stop_heartbeat()


def test_observer_beat_stamps_observer_and_never_claims_ownership(client, app):
    """0106: role='observer' (the miles exporter) asserts only "something is
    watching" -- it must land on observer_heartbeat_at and leave the OWNER
    column untouched, or a dead sidecar would read as a dead training."""
    run = open_run(client, experiment="e", name="r", heartbeat=False)
    run.start_heartbeat(0.01, role="observer")
    assert _wait_for(lambda: app.run_observer_heartbeats.get(run.id, 0) >= 2)
    run.stop_heartbeat()
    assert app.runs[run.id]["observer_heartbeat_at"]
    assert app.run_heartbeats.get(run.id, 0) == 0
    assert "last_heartbeat_at" not in app.runs[run.id]


def test_client_heartbeat_run_carries_the_observer_role_param(client, app):
    run = open_run(client, experiment="e", name="r", heartbeat=False)
    client.heartbeat_run(run.id, role="observer")
    assert app.run_observer_heartbeats.get(run.id, 0) == 1
    client.heartbeat_run(run.id)
    assert app.run_heartbeats.get(run.id, 0) == 1


def test_a_typoed_role_fails_loudly_at_the_call_site(client, app):
    """The beat loop swallows exceptions, so a bad role must never reach it --
    a typo'd observer beat that 422s silently forever would get a watched run
    reaped despite a live heartbeat thread."""
    import pytest

    run = open_run(client, experiment="e", name="r", heartbeat=False)
    with pytest.raises(ValueError):
        client.heartbeat_run(run.id, role="observers")
    with pytest.raises(ValueError):
        run.start_heartbeat(0.01, role="watcher")


def test_observer_probe_fails_closed_against_a_pre_0106_server(client, app):
    """A server that predates role= silently records observer beats in the
    OWNERSHIP column, permanently poisoning the crashed-vs-untracked verdict.
    The capability probe reads the run first: no observer_heartbeat_at key in
    the response means old server, and NO beat may ever be sent."""
    run = open_run(client, experiment="e", name="r", heartbeat=False)
    # Impersonate a pre-0106 server: its RunDetailOut has no observer field.
    del app.runs[run.id]["observer_heartbeat_at"]
    run.start_heartbeat(0.01, role="observer")
    time.sleep(0.1)
    run.stop_heartbeat()
    assert app.run_observer_heartbeats.get(run.id, 0) == 0
    assert app.run_heartbeats.get(run.id, 0) == 0
    assert "last_heartbeat_at" not in app.runs[run.id]


def test_the_real_run_read_declares_the_key_the_observer_probe_reads():
    """Plan 2.9. The fake above serializes `observer_heartbeat_at`; the real
    server's RunDetailOut did not, so in prod the probe always read "old
    server" and no observer beat ever went out. Read the committed snapshot of
    the REAL OpenAPI document (`schema/openapi.json`, dumped from app.main)
    and the model generated from it, not the fake. The server side is pinned
    in tests/unit/test_run_read_observer_heartbeat.py and, end to end, in
    tests/integration/test_run_liveness_sdk_e2e.py."""
    import json
    from pathlib import Path

    from probe._generated.models import RunPageDetailOut

    probed = "observer_heartbeat_at"
    schema = json.loads(
        (Path(__file__).resolve().parent.parent / "schema" / "openapi.json").read_text()
    )
    ref = schema["paths"]["/v1/runs/{run_ref}"]["get"]["responses"]["200"]["content"][
        "application/json"
    ]["schema"]["$ref"]
    assert probed in schema["components"]["schemas"][ref.rsplit("/", 1)[-1]]["properties"]
    assert probed in RunPageDetailOut.model_fields


def test_role_change_restarts_the_beat_loop_explicitly(client, app):
    """Observer-then-owner must actually assert ownership (and vice versa) --
    a silently-kept old role turns a real death into 'untracked' or a watcher
    exit into 'crashed'."""
    run = open_run(client, experiment="e", name="r", heartbeat=False)
    run.start_heartbeat(0.01, role="observer")
    assert _wait_for(lambda: app.run_observer_heartbeats.get(run.id, 0) >= 1)
    run.start_heartbeat(0.01, role="owner")
    assert _wait_for(lambda: app.run_heartbeats.get(run.id, 0) >= 1)
    run.stop_heartbeat()


def test_detached_create_never_beats(client, app, monkeypatch):
    monkeypatch.setenv("PROBE_HEARTBEAT_SECONDS", "60")
    run = open_run(client, experiment="e", name="r", heartbeat=False)
    time.sleep(0.05)
    assert run._hb_thread is None
    assert app.run_heartbeats == {}


def test_attach_handle_is_inert(client, app, monkeypatch):
    """The miles attach path constructs Run(client, get_run(...)) directly; a
    handle that merely OBSERVES a run must never assert its liveness."""
    monkeypatch.setenv("PROBE_HEARTBEAT_SECONDS", "60")
    created = open_run(client, experiment="e", name="r", heartbeat=False)
    attached = Run(client, client.get_run(created.id))
    assert attached._hb_thread is None
    assert app.run_heartbeats == {}


def test_env_kill_switch_disables_the_default(client, app, monkeypatch):
    monkeypatch.setenv("PROBE_HEARTBEAT_SECONDS", "0")
    run = open_run(client, experiment="e", name="r")
    assert run._hb_thread is None


def test_terminal_set_status_stops_nonterminal_does_not(client, app):
    run = open_run(client, experiment="e", name="r", heartbeat=False)
    run.start_heartbeat(0.01)
    thread = run._hb_thread
    run.set_status("running")
    assert thread.is_alive()
    run.set_status("canceled")
    thread.join(timeout=5)
    assert not thread.is_alive()


def test_beat_failures_do_not_kill_the_loop(client, app):
    """Liveness reporting must never take down the work it reports on, and a
    transient failure must not end beating for good — a run that beat once and
    then went silent is exactly what the reaper crashes."""
    run = open_run(client, experiment="e", name="r", heartbeat=False)
    run.start_heartbeat(0.01)
    assert _wait_for(lambda: app.run_heartbeats.get(run.id, 0) >= 1)
    row = app.runs.pop(run.id)  # every beat now 404s
    baseline = app.run_heartbeats[run.id]
    time.sleep(0.05)  # a few failing cycles
    assert run._hb_thread.is_alive()
    app.runs[run.id] = row  # server "recovers"; beating resumes
    assert _wait_for(lambda: app.run_heartbeats[run.id] > baseline)
    run.stop_heartbeat()


def test_dropping_the_handle_stops_the_beat(client, app):
    """A run nobody holds a handle to can never be finished; the honest outcome
    is beats stopping so the reaper flips it — not a leaked thread per run for
    the life of a sweep process that hit an exception path."""
    run = open_run(client, experiment="e", name="r", heartbeat=False)
    run.start_heartbeat(0.01)
    thread = run._hb_thread
    rid = run.id  # captured up front so no closure below pins the handle
    assert _wait_for(lambda: app.run_heartbeats.get(rid, 0) >= 1)
    del run
    gc.collect()
    thread.join(timeout=5)
    assert not thread.is_alive()


def test_client_close_stops_the_beat(client, app):
    """Beats ride the client's transport: close() must take them down rather
    than leave threads spinning against a closed httpx client."""
    run = open_run(client, experiment="e", name="r", heartbeat=False)
    run.start_heartbeat(0.01)
    thread = run._hb_thread
    assert _wait_for(lambda: app.run_heartbeats.get(run.id, 0) >= 1)
    client.close()
    thread.join(timeout=5)
    assert not thread.is_alive()


def test_late_beat_racing_completion_is_a_noop(client, app):
    run = open_run(client, experiment="e", name="r", heartbeat=False)
    run.finish()
    client.heartbeat_run(run.id)  # 200, not an error — mirrors the backend
    assert app.run_heartbeats.get(run.id, 0) == 0
    assert "last_heartbeat_at" not in app.runs[run.id]


def test_cli_run_start_is_detached_and_never_beats(app, tmp_path, monkeypatch, capsys):
    """`probe run start` prints an id and exits; the run is closed later by
    `probe run end`. If the CLI forgot to opt out, the beat below would land."""
    from probe import cli
    from tests.conftest import make_client

    monkeypatch.setenv("PROBE_HEARTBEAT_SECONDS", "60")
    monkeypatch.setattr(cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "spool"))
    app.seed_experiment("e")
    rc = cli.main(["run", "start", "--experiment", "e", "--name", "r1"])
    assert rc == 0
    rid = capsys.readouterr().out.strip()
    time.sleep(0.05)
    assert app.run_heartbeats == {}
    assert "last_heartbeat_at" not in app.runs[rid]


# -- plan 2.7: a re-login must not silently kill a running job's heartbeat ------
#
# `probe login` revokes the token a running process was built with. The beat
# loop swallowed the 401 on every beat after that, and 15 minutes later the
# reaper marked the live run `crashed`. The detached worker never had this
# problem: it resolves credentials on every pass. The beat, the in-process
# exporter and `flush()` now ask the same resolver when the API refuses the
# credential -- for AMBIENT clients only (what `probe.init()` builds).

_OLD = "ros_pat_deadbeef"  # what `make_client` builds with
_FRESH = "ros_pat_fresh"


def _login(token: str) -> None:
    """What `probe login` leaves behind: the current context's stored token."""
    from probe.sdk import config as config_module

    config_module.save_context({"base_url": "http://test", "token": token})


def _as_ambient(client, source: str = "config"):
    """`make_client` passes explicit settings, so the client it builds is not
    ambient. Production's ambient client (`Client()`, `probe.init()`) builds its
    Transport over the SAME Settings object, exactly as `make_client` does, so
    flipping the flag gives the production shape over the fake transport.
    `test_only_a_client_built_from_the_environment_is_ambient` pins the flag.
    The identity lookup runs inline here; production runs it on a thread when a
    heartbeat or the exporter starts (pinned against a REAL `Client()` in
    `test_a_real_client_learns_its_account_when_its_heartbeat_starts`)."""
    client._ambient_credentials = True
    client._credential_source = source
    client._remember_identity()
    return client


def _credential_warnings(caught) -> list[str]:
    return [str(w.message) for w in caught if "credential" in str(w.message)]


@pytest.fixture
def reads(monkeypatch):
    """Every credential re-read (config file or environment, never network)."""
    from probe.sdk.client import Client

    calls: list = []
    real = Client._reread_credential

    def counted(self):
        calls.append(self._credential_source)
        return real(self)

    monkeypatch.setattr(Client, "_reread_credential", counted)
    return calls


def test_only_a_client_built_from_the_environment_is_ambient(monkeypatch, tmp_path):
    from probe.sdk.client import Client
    from probe.sdk.config import Settings

    monkeypatch.setenv("PROBE_BASE_URL", "http://test")
    monkeypatch.setenv("PROBE_TOKEN", _OLD)
    spool = {"spool_dir": tmp_path / "spool", "async_writes": False}
    built = [
        (Client(**spool), True),
        (Client(token="ros_pat_explicit", **spool), False),
        (Client(settings=Settings(base_url="http://test", token=_OLD), **spool), False),
    ]
    try:
        assert [c._ambient_credentials for c, _ in built] == [want for _, want in built]
        # An ambient token remembers where it came from: here, the environment.
        assert [c._credential_source for c, _ in built] == ["env", None, None]
    finally:
        for c, _ in built:
            c.close()


def test_a_relogin_is_picked_up_by_the_beat_with_one_warning(client, app):
    _login(_OLD)
    ambient = _as_ambient(client)
    run = open_run(ambient, experiment="e", name="r", heartbeat=False)
    _login(_FRESH)
    app.rejected_tokens.add(_OLD)  # the re-login revoked it
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        run.start_heartbeat(0.01)
        assert _wait_for(lambda: app.run_heartbeats.get(run.id, 0) >= 2)
        run.stop_heartbeat()
    assert ambient.settings.token == _FRESH
    (message,) = _credential_warnings(caught)
    assert "picked up" in message


def test_an_explicit_credential_is_never_reread(client, app, reads):
    _login(_FRESH)
    run = open_run(client, experiment="e", name="r", heartbeat=False)
    app.rejected_tokens.add(_OLD)
    run.start_heartbeat(0.01)
    time.sleep(0.2)
    run.stop_heartbeat()
    assert reads == []
    assert client.settings.token == _OLD
    assert app.run_heartbeats.get(run.id, 0) == 0


def test_a_scope_refusal_is_not_the_credential(client, app, monkeypatch, reads):
    """A 403 naming a missing scope refuses one request, not the key. Only a 401,
    or a 403 that says the key's team or membership is gone, is re-read."""
    from probe.sdk import errors
    from probe.sdk.run import _beat_once

    ambient = _as_ambient(client)
    run = open_run(ambient, experiment="e", name="r", heartbeat=False)

    def refuse(message):
        def beat(*a, **kw):
            raise errors.ScopeError(message, status=403)

        return beat

    monkeypatch.setattr(ambient, "heartbeat_run", refuse("token lacks the runs:write scope"))
    with pytest.raises(errors.ScopeError):
        _beat_once(ambient, run.id, role="owner", attached=False, write_epoch=None)
    assert reads == []

    monkeypatch.setattr(ambient, "heartbeat_run", refuse("not a member of this team"))
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        with pytest.raises(errors.ScopeError):
            _beat_once(ambient, run.id, role="owner", attached=False, write_epoch=None)
    assert len(reads) == 1  # the credential itself: re-read (nothing new here)


def test_a_revoked_token_is_reread_at_most_once_per_30s_and_warned_once(
    client, app, monkeypatch, reads
):
    _login(_OLD)
    ambient = _as_ambient(client)
    run = open_run(ambient, experiment="e", name="r", heartbeat=False)
    app.rejected_tokens.add(_OLD)  # revoked, and no new login to read
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        run.start_heartbeat(0.005)
        time.sleep(0.3)  # dozens of refused beats
        run.stop_heartbeat()
        assert len(reads) == 1
        # 31 s later: one more read, and still only the one warning.
        monkeypatch.setattr(ambient, "_credential_checked_at", ambient._credential_checked_at - 31)
        assert ambient.refresh_credentials() is False
    assert len(reads) == 2
    (message,) = _credential_warnings(caught)
    assert WIZARD_HINT in message


def test_a_token_from_the_environment_has_nothing_new_to_read(client, app, monkeypatch):
    """A k8s secret exported as PROBE_TOKEN cannot change under a running
    process; say so rather than claim a login would help."""
    monkeypatch.setenv("PROBE_BASE_URL", "http://test")  # the pod's shape: env only
    monkeypatch.setenv("PROBE_TOKEN", _OLD)
    ambient = _as_ambient(client, source="env")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert ambient.refresh_credentials() is False
    (message,) = _credential_warnings(caught)
    assert "PROBE_TOKEN" in message


def test_an_environment_token_never_switches_to_the_boxs_stored_login(
    client, app, monkeypatch, reads
):
    """#2021 review (HIGH). A job started with PROBE_TOKEN=A on a box where
    `probe login` holds B must not become B when A is refused: the stored
    login is somebody else's choice, possibly somebody else. An environment
    token is re-read from the environment alone."""
    _login(_FRESH)  # the box's own login, B
    monkeypatch.setenv("PROBE_TOKEN", _OLD)  # this job's token, A
    ambient = _as_ambient(client, source="env")
    app.rejected_tokens.add(_OLD)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert ambient.refresh_credentials(refused=_OLD) is False
    assert ambient.settings.token == _OLD
    assert reads == ["env"]
    (message,) = _credential_warnings(caught)
    assert "PROBE_TOKEN" in message


def test_a_login_as_another_account_is_never_adopted(client, app):
    """#2021 review (HIGH). A plain `probe login` as someone else overwrites
    the active context. Same team: this job's writes would land as them;
    another team: every run write 404s and dead-letters. The new token is
    checked with `/v1/me` against the account the process started as."""
    _login(_OLD)
    ambient = _as_ambient(client)
    app.me_identities[_FRESH] = {"user_id": "00000000-0000-0000-0000-00000000000b"}
    _login(_FRESH)
    app.rejected_tokens.add(_OLD)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert ambient.refresh_credentials(refused=_OLD) is False
    assert ambient.settings.token == _OLD
    (message,) = _credential_warnings(caught)
    assert "different account" in message


def test_a_login_to_another_team_is_never_adopted(client, app):
    _login(_OLD)
    ambient = _as_ambient(client)
    app.me_identities[_FRESH] = {"customer_id": "lab-99"}
    _login(_FRESH)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        assert ambient.refresh_credentials(refused=_OLD) is False
    assert ambient.settings.token == _OLD


def test_an_unknown_starting_account_adopts_nothing(client, app):
    """If the process never learned who it started as (the `/v1/me` read
    failed), no new login can be matched to it: keep the old token."""
    _login(_OLD)
    client._ambient_credentials = True
    client._credential_source = "config"
    client._credential_identity_ready.set()  # the read finished, and learned nothing
    _login(_FRESH)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert client.refresh_credentials(refused=_OLD) is False
    assert client.settings.token == _OLD
    (message,) = _credential_warnings(caught)
    assert "unknown" in message


def _scope_refused_metrics(app, monkeypatch):
    import httpx

    inner = app.handler

    def handler(request):
        if request.method == "POST" and request.url.path.endswith("/metrics"):
            return httpx.Response(403, json={"detail": "token lacks the runs:write scope"})
        return inner(request)

    monkeypatch.setattr(app, "handler", handler)


def test_a_scope_refusal_in_flush_is_not_read_as_the_credential(app, tmp_path, monkeypatch, reads):
    """#2021 review (MED). A 403 naming a missing scope refuses one request,
    not the key: flush() must not re-read (or swap) credentials over it."""
    _login(_OLD)
    _scope_refused_metrics(app, monkeypatch)
    ambient = _as_ambient(make_client(app, tmp_spool=tmp_path / "spool"))
    run = open_run(ambient, experiment="e", name="r", heartbeat=False)
    ambient.async_writes = True
    try:
        run.log({"loss": 1.0}, step=0)
    finally:
        ambient.async_writes = False
    _login(_FRESH)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert ambient.flush() == 0
    assert reads == [] and ambient.settings.token == _OLD
    assert _credential_warnings(caught) == []


def test_a_scope_refusal_in_the_exporter_is_not_read_as_the_credential(
    app, tmp_path, monkeypatch, reads
):
    _login(_OLD)
    _scope_refused_metrics(app, monkeypatch)
    ambient = _as_ambient(
        make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True, drain_interval=0.05)
    )
    try:
        run = open_run(ambient, experiment="e", name="r", heartbeat=False)
        run.log({"loss": 1.0}, step=0)
        assert _wait_for(lambda: ambient._exporter is not None and not ambient._exporter.alive)
    finally:
        ambient.close()
    assert reads == []


def test_only_this_clients_own_refused_credential_counts(client):
    """#2021 review (LOW). The outbox is machine-wide: a pass can stop on an op
    pinned to ANOTHER context, whose refusal says nothing about this client's
    key. Neither can a scope 403."""
    from probe.sdk.journal import DrainReport

    mine = dict(client.journal.context or {})
    other = {"name": "other", "base_url": client.settings.base_url}

    def refused(status, message="invalid or revoked token", context=None):
        return DrainReport(
            auth_blocked=True, auth_status=status, auth_message=message, auth_context=context
        )

    assert client._own_credential_refusal(refused(401, context=mine))
    assert client._own_credential_refusal(refused(403, "not a member of this team", mine))
    assert not client._own_credential_refusal(refused(401, context=other))
    assert not client._own_credential_refusal(refused(403, "token lacks the runs:write scope", mine))
    assert not client._own_credential_refusal(DrainReport())


@pytest.mark.parametrize("order", ["revoke_then_write", "write_then_revoke"])
def test_the_exporter_survives_either_order_of_a_relogin(app, tmp_path, monkeypatch, order):
    """#2021 review (MED). `probe login` revokes the old token BEFORE it writes
    the new one: a pass in that gap finds nothing new, and the exporter used to
    exit there for good. It now waits (a config read at most every 30 s, no
    network) and resumes when the new login lands."""
    from probe.sdk.client import Client

    monkeypatch.setattr(Client, "_CREDENTIAL_REFRESH_SECONDS", 0.05)
    _login(_OLD)
    ambient = _as_ambient(
        make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True, drain_interval=0.05)
    )
    try:
        run = open_run(ambient, experiment="e", name="r", heartbeat=False)
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            if order == "revoke_then_write":
                app.rejected_tokens.add(_OLD)
                run.log({"loss": 1.0}, step=0)
                time.sleep(0.3)  # refused passes, nothing new to read yet
                assert not app.metric_points_posted.get(run.id)
                _login(_FRESH)
            else:
                _login(_FRESH)
                app.rejected_tokens.add(_OLD)
                run.log({"loss": 1.0}, step=0)
            assert _wait_for(lambda: app.metric_points_posted.get(run.id))
            run.log({"loss": 2.0}, step=1)
            assert _wait_for(lambda: len(app.metric_points_posted.get(run.id, [])) == 2)
        assert ambient._exporter.alive
        assert ambient.settings.token == _FRESH
    finally:
        ambient.close()


def test_the_exporter_keeps_draining_after_a_relogin(app, tmp_path):
    _login(_OLD)
    ambient = _as_ambient(
        make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True, drain_interval=0.05)
    )
    try:
        run = open_run(ambient, experiment="e", name="r", heartbeat=False)
        _login(_FRESH)
        app.rejected_tokens.add(_OLD)
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            run.log({"loss": 1.0}, step=0)
            assert _wait_for(lambda: app.metric_points_posted.get(run.id))
        assert ambient._exporter is not None and ambient._exporter.alive
    finally:
        ambient.close()


def test_flush_retries_once_under_the_current_credential(client, app):
    _login(_OLD)
    ambient = _as_ambient(client)
    run = open_run(ambient, experiment="e", name="r", heartbeat=False)
    ambient.async_writes = True  # queue the write; this client has no drainer
    try:
        run.log({"loss": 1.0}, step=0)
    finally:
        ambient.async_writes = False
    _login(_FRESH)
    app.rejected_tokens.add(_OLD)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        assert ambient.flush() == 1
    assert app.metric_points_posted.get(run.id)


# -- #2021 security re-review ---------------------------------------------------


def _me_requests(app, token: str | None = None) -> list[str]:
    out = []
    for request in app.requests:
        if request.url.path == "/v1/me":
            bearer = request.headers.get("authorization", "").removeprefix("Bearer ")
            if token is None or bearer == token:
                out.append(bearer)
    return out


def test_a_real_client_learns_its_account_when_its_heartbeat_starts(app, tmp_path, monkeypatch):
    """HIGH. The lookup used to start in __init__ BEFORE the transport existed:
    an AttributeError, swallowed, so no real client ever learned its account
    and every re-login was refused. A real `Client()`, over a real socket."""
    from probe.sdk.client import Client
    from tests.served_fake_app import serve

    app.seed_experiment("e1")
    with serve(app) as url:
        monkeypatch.setenv("PROBE_BASE_URL", url)
        monkeypatch.setenv("PROBE_TOKEN", _OLD)
        monkeypatch.setenv("PROBE_HEARTBEAT_SECONDS", "60")
        client = Client(spool_dir=tmp_path / "spool", async_writes=False)
        try:
            assert _me_requests(app) == [], "a client that has not started work asks nothing"
            run = client.run(experiment="e1", name="r")
            assert client._credential_identity_ready.wait(5.0)
            assert client._credential_identity == ("lab-42", "00000000-0000-0000-0000-000000000001")
            run.finish()
        finally:
            client.close()


def test_a_failed_identity_lookup_prints_nothing(app, tmp_path, monkeypatch, capfd):
    """#2021 security review LOW. A `/v1/me` that fails when the heartbeat
    starts left the lookup thread's traceback on stderr, which output capture
    uploads with the run. It must leave the account unknown, quietly."""
    import threading

    from probe.sdk.client import Client
    from tests.served_fake_app import serve

    app.seed_experiment("e1")
    app.me_status = 500
    hooked: list = []
    monkeypatch.setattr(threading, "excepthook", lambda args: hooked.append(args))
    with serve(app) as url:
        monkeypatch.setenv("PROBE_BASE_URL", url)
        monkeypatch.setenv("PROBE_TOKEN", _OLD)
        monkeypatch.setenv("PROBE_HEARTBEAT_SECONDS", "60")
        client = Client(spool_dir=tmp_path / "spool", async_writes=False)
        try:
            run = client.run(experiment="e1", name="r")
            assert client._credential_identity_ready.wait(5.0)
            assert client._credential_identity is None
            run.finish()
        finally:
            client.close()
    assert hooked == []
    assert "Traceback" not in capfd.readouterr().err


def test_a_one_request_client_sends_no_identity_lookup(app, tmp_path, monkeypatch):
    """MED. A CLI command builds a client for one request; it must not pay a
    second one for a refresh it will never make."""
    from probe.sdk.client import Client
    from tests.served_fake_app import serve

    with serve(app) as url:
        monkeypatch.setenv("PROBE_BASE_URL", url)
        monkeypatch.setenv("PROBE_TOKEN", _OLD)
        for _ in range(3):
            client = Client(spool_dir=tmp_path / "spool", async_writes=False)
            client.list_projects(limit=1)
            client.close()
    assert _me_requests(app) == []


def test_a_waiting_exporter_releases_the_shared_outbox_lock(app, tmp_path, monkeypatch):
    """MED. While it waits for a new login the exporter delivers nothing, so it
    must not hold the machine-wide `.worker.lock`: that stopped every other
    process's queued writes until this one exited."""
    from probe._shared import oscompat

    from probe.sdk.client import Client
    from probe.sdk.outbox_worker import _lease_path

    monkeypatch.setattr(Client, "_CREDENTIAL_REFRESH_SECONDS", 0.05)
    _login(_OLD)
    ambient = _as_ambient(
        make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True, drain_interval=0.05)
    )
    try:
        run = open_run(ambient, experiment="e", name="r", heartbeat=False)
        app.rejected_tokens.add(_OLD)
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            run.log({"loss": 1.0}, step=0)
            time.sleep(0.4)  # refused, and nothing new to read yet
            assert ambient._exporter.alive
            handle = open(_lease_path(ambient.journal), "a+")
            try:
                oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)  # must not block
                oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
            finally:
                handle.close()
            _login(_FRESH)
            assert _wait_for(lambda: app.metric_points_posted.get(run.id))
    finally:
        ambient.close()


def test_an_environment_token_exporter_does_not_wait(app, tmp_path, monkeypatch):
    """A PROBE_TOKEN has nothing new to read, so waiting would only hold the
    thread forever: it stops, as it did before this change."""
    monkeypatch.setenv("PROBE_TOKEN", _OLD)
    ambient = _as_ambient(
        make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True, drain_interval=0.05),
        source="env",
    )
    try:
        run = open_run(ambient, experiment="e", name="r", heartbeat=False)
        app.rejected_tokens.add(_OLD)
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            run.log({"loss": 1.0}, step=0)
            assert _wait_for(lambda: not ambient._exporter.alive)
    finally:
        ambient.close()


def test_a_malformed_stored_token_never_reaches_a_warning(client, app):
    """LOW (security). A token with a non-ASCII character fails inside httpx
    with the whole `Bearer <token>` header in the message, and warnings are
    uploaded with the run's stderr: only the exception's type is printed."""
    _login(_OLD)
    ambient = _as_ambient(client)
    _login("ros_pat_SECRETVALUE0123456789é")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert ambient.refresh_credentials(refused=_OLD) is False
    messages = _credential_warnings(caught)
    assert messages and not any("SECRETVALUE" in m for m in messages), messages


def test_the_mismatch_warning_does_not_name_the_other_team(client, app):
    _login(_OLD)
    ambient = _as_ambient(client)
    app.me_identities[_FRESH] = {"customer_id": "other-tenant"}
    _login(_FRESH)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert ambient.refresh_credentials(refused=_OLD) is False
    (message,) = _credential_warnings(caught)
    assert "different account" in message and "other-tenant" not in message


def test_another_accounts_login_is_asked_about_once(client, app):
    """LOW. While someone else's login sits in the config, a /v1/me used to go
    out every 30 s for the life of the process."""
    _login(_OLD)
    ambient = _as_ambient(client)
    app.me_identities[_FRESH] = {"user_id": "someone-else"}
    _login(_FRESH)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        for _ in range(10):
            ambient._credential_checked_at = float("-inf")  # 30 s passed
            assert ambient.refresh_credentials(refused=_OLD) is False
    assert len(_me_requests(app, _FRESH)) == 1


def test_the_account_check_is_one_short_attempt(client, app, monkeypatch):
    """LOW. flush() and finish() can wait on this check; the transport's usual
    30 s timeout with retries made that ~2 minutes. One attempt, 5 s."""
    _login(_OLD)
    ambient = _as_ambient(client)
    _login(_FRESH)
    app.me_status = 503
    seen = []
    real = type(ambient.transport).request

    def spy(self, method, path, **kw):
        if path == "/v1/me":
            seen.append((self.max_retries, kw.get("timeout")))
        return real(self, method, path, **kw)

    monkeypatch.setattr(type(ambient.transport), "request", spy)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        assert ambient.refresh_credentials(refused=_OLD) is False
    assert seen == [(0, 5.0)]
    assert ambient.settings.token == _OLD
