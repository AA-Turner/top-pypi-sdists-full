"""#2035: a queued write goes out with the credential that queued it, or waits.

The outbox is one machine-wide queue, and whatever drains it -- the detached
worker, another job's ``flush()``, ``probe outbox drain`` -- used to pick the
credential by the op's login PROFILE alone. A job authenticated with
``PROBE_TOKEN=A`` on a box where someone else ran ``probe login`` (B) had its
metrics delivered as B: wrong attribution in one team, a 404 and a dead letter
(data lost) across two.

Every op now records where its credential came from and a fingerprint of it.
These tests use a real socket (``served_fake_app``) and the production
credential path (``drain`` with no ``client_factory``) wherever the question is
"which bearer went out", because a fake transport never sends one.
"""

from __future__ import annotations

import json
import warnings

import pytest

from probe.sdk import config
from probe.sdk.client import Client
from probe.sdk.journal import CREDENTIAL_NAMESPACE, Journal, credential_fingerprint, drain
from tests.served_fake_app import serve
from tests.test_outbox import seeded_run

ENV_A = "probe_pat_envtoken_A_0123456789abcdef"
STORED_B = "probe_pat_storedlogin_B_0123456789abcdef"
CODE_C = "probe_pat_codetoken_C_0123456789abcdef"


#: The account the fake's `/v1/me` answers with by default.
ACCOUNT = ("lab-42", "00000000-0000-0000-0000-000000000001")


def _login(url: str, token: str | None, name: str | None = None, *, account=None) -> None:
    """What `probe login` leaves on disk: this context's endpoint and token,
    and -- since the #2041 review -- which account that token is (``account``,
    bound to the token's fingerprint). ``account=None`` is a login saved
    without one (the setup wizard, or a release before the review)."""
    from probe.sdk.journal import credential_fingerprint

    updates = {"base_url": url, "token": token, "identity": None}
    if account is not None and token:
        updates["identity"] = {
            "fingerprint": credential_fingerprint(token, None),
            "customer_id": account[0],
            "user_id": account[1],
        }
    config.save_context(updates, name=name)


def _bearer_requests(app, token: str) -> int:
    return sum(
        1 for r in app.requests if r.headers.get("authorization", "") == f"Bearer {token}"
    )


def _bearers(app) -> list[str]:
    """The bearer of every metric POINT that reached the fake, in order: the
    drain coalesces a run's queued metric writes into one POST (#2053), so
    one entry per point, not per request."""
    out = []
    for r in app.requests:
        if not r.url.path.endswith("/metrics") or r.method != "POST":
            continue
        bearer = r.headers.get("authorization", "").removeprefix("Bearer ")
        try:
            points = json.loads(r.content or b"{}").get("points") or [None]
        except ValueError:
            points = [None]
        out.extend([bearer] * len(points))
    return out


def _queue_a_metric(client: Client, run_id: str, step: int = 1) -> None:
    client.write(
        "POST",
        f"/v1/runs/{run_id}/metrics",
        {"points": [{"key": "loss", "kind": "model", "value": 1.0, "step_index": step}]},
    )


@pytest.fixture
def env_job(app, tmp_path, monkeypatch):
    """A job started with PROBE_TOKEN=A on a machine logged in as B, one op
    queued. Yields (url, client, run_id); PROBE_TOKEN stays set."""
    run_id = seeded_run(app, tmp_path)
    with serve(app) as url:
        _login(url, STORED_B)
        monkeypatch.setenv("PROBE_TOKEN", ENV_A)
        client = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
        try:
            _queue_a_metric(client, run_id)
            assert len(client.journal.pending()) == 1
            yield url, client, run_id
        finally:
            client.close()


def test_a_worker_the_job_started_sends_the_jobs_token_not_the_stored_login(app, env_job):
    """The issue's repro. The worker a job kicks inherits its environment, so
    it holds A -- and the stored B used to outrank it."""
    _url, client, _run = env_job
    report = drain(Journal(client.journal.dir))  # the detached worker's call
    assert report.delivered == 1
    assert _bearers(app) == [ENV_A]


def test_a_worker_without_the_jobs_token_leaves_its_writes_queued(app, env_job, monkeypatch):
    """A worker someone ELSE started has no PROBE_TOKEN, only the stored login.
    B must never be sent; the op is not dead-lettered, not retried, and does
    not stop the queue -- it waits, and the job's own flush delivers it."""
    _url, client, _run = env_job
    monkeypatch.delenv("PROBE_TOKEN")
    report = drain(Journal(client.journal.dir))
    assert _bearers(app) == [], "the stored login was used for another credential's write"
    assert report.credential_held == 1 and not report.auth_blocked
    assert report.dead_lettered == 0 and client.journal.failed() == []
    ((_, op),) = client.journal.pending()
    assert op.get("attempts", 0) == 0, "waiting is not a failed delivery"
    status = Journal.read_status(str(client.journal.dir)) or {}
    assert "credential" in (status.get("last_error") or "")

    monkeypatch.setenv("PROBE_TOKEN", ENV_A)
    assert client.flush() == 1
    assert _bearers(app) == [ENV_A]


def test_another_jobs_flush_does_not_send_this_jobs_writes(app, env_job, monkeypatch):
    """Two jobs, one outbox. Job C's flush used to replay every op pinned to
    its context over ITS token -- job A's metrics written as C."""
    _url, client, _run = env_job
    monkeypatch.setenv("PROBE_TOKEN", CODE_C)
    other = Client(spool_dir=client.journal.dir, async_writes=True, auto_drain=False)
    try:
        other.flush()
    finally:
        other.close()
    assert _bearers(app) == []
    assert len(client.journal.pending()) == 1


def test_a_token_passed_in_code_is_never_swapped_for_the_stored_login(app, tmp_path):
    run_id = seeded_run(app, tmp_path)
    with serve(app) as url:
        _login(url, STORED_B)
        client = Client(
            token=CODE_C, spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False
        )
        try:
            _queue_a_metric(client, run_id)
            report = drain(Journal(client.journal.dir))
            assert _bearers(app) == [], "the stored login was used for a token passed in code"
            assert report.credential_held == 1
            assert client.journal.context["principal"]["source"] == "code"
            assert client.flush() == 1
        finally:
            client.close()
    assert _bearers(app) == [CODE_C]


def test_a_stored_login_write_survives_a_re_login(app, tmp_path):
    """Control: `probe login` promises to un-block queued writes, and a
    re-login mints a NEW token. An op queued under the old stored login still
    goes, with the new one -- that is the same person's login for the context."""
    run_id = seeded_run(app, tmp_path)
    with serve(app) as url:
        _login(url, STORED_B, account=ACCOUNT)
        client = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
        try:
            _queue_a_metric(client, run_id)
        finally:
            client.close()
        _login(url, "probe_pat_storedlogin_B_relogged_in", account=ACCOUNT)
        report = drain(Journal(tmp_path / "outbox"))
    assert report.delivered == 1
    assert _bearers(app) == ["probe_pat_storedlogin_B_relogged_in"]


def test_a_re_login_as_another_account_does_not_send_the_old_logins_writes(app, tmp_path):
    """#2041 review MED. The drainer sent a stored-login write with whoever
    was logged in to the context NOW: 5 of 5 queued points went out as another
    user (same team: wrong attribution; another team: 404, dead-lettered)."""
    run_id = seeded_run(app, tmp_path)
    other = "probe_pat_someone_else_0123456789abcdef"
    app.me_identities[other] = {"customer_id": "lab-99", "user_id": "u-someone-else"}
    with serve(app) as url:
        _login(url, STORED_B, account=ACCOUNT)
        client = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
        try:
            _queue_a_metric(client, run_id)
        finally:
            client.close()
        _login(url, other, account=("lab-99", "u-someone-else"))
        report = drain(Journal(tmp_path / "outbox"))
    assert _bearers(app) == [], "another account's login sent this write"
    assert report.delivered == 0 and report.credential_held == 1 and not report.auth_blocked
    ((_, op),) = Journal(tmp_path / "outbox").pending()
    assert op.get("attempts", 0) == 0
    status = Journal.read_status(str(tmp_path / "outbox")) or {}
    assert "another account" in (status.get("last_error") or "")


def test_a_login_with_no_recorded_account_is_never_trusted_with_the_old_writes(app, tmp_path):
    """The account behind a login saved without one is unknown, so a re-login
    cannot be matched to it: the write waits rather than guess."""
    run_id = seeded_run(app, tmp_path)
    with serve(app) as url:
        _login(url, STORED_B)  # no account recorded
        client = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
        try:
            _queue_a_metric(client, run_id)
        finally:
            client.close()
        _login(url, "probe_pat_storedlogin_B_relogged_in", account=ACCOUNT)
        report = drain(Journal(tmp_path / "outbox"))
    assert _bearers(app) == []
    assert report.credential_held == 1
    status = Journal.read_status(str(tmp_path / "outbox")) or {}
    assert "never recorded" in (status.get("last_error") or "")


def test_the_account_learned_when_work_starts_is_stamped_on_later_writes(app, tmp_path):
    """A login saved without an account still gets one: the lookup #2021 runs
    when a heartbeat or exporter starts records it in the stamp, so writes
    queued from then on can follow a re-login of the same account."""
    run_id = seeded_run(app, tmp_path)
    with serve(app) as url:
        _login(url, STORED_B)
        client = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
        try:
            client._remember_identity()
            _queue_a_metric(client, run_id)
        finally:
            client.close()
        _login(url, "probe_pat_storedlogin_B_relogged_in")
        report = drain(Journal(tmp_path / "outbox"))
    assert report.delivered == 1
    assert _bearers(app) == ["probe_pat_storedlogin_B_relogged_in"]


def test_a_recorded_account_for_another_token_is_ignored(tmp_path):
    """The account `probe login` records is bound to its token: a record left
    by an earlier login must never vouch for this one."""
    from probe.sdk.journal import credential_fingerprint

    config.save_context(
        {
            "base_url": "http://127.0.0.1:9",
            "token": STORED_B,
            "identity": {
                "fingerprint": credential_fingerprint("probe_pat_an_earlier_login", None),
                "customer_id": "lab-99",
                "user_id": "u-earlier",
            },
        }
    )
    client = Client(spool_dir=tmp_path / "outbox", async_writes=False)
    try:
        stamp = client.journal.context["principal"]
    finally:
        client.close()
    assert "customer_id" not in stamp and "user_id" not in stamp


def test_a_stored_login_write_is_never_sent_with_an_environment_token(app, tmp_path, monkeypatch):
    """Logged out since, and the drainer's environment carries someone's
    PROBE_TOKEN: park for `probe login` (as before), never fall back to it."""
    run_id = seeded_run(app, tmp_path)
    with serve(app) as url:
        _login(url, STORED_B)
        client = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
        try:
            _queue_a_metric(client, run_id)
        finally:
            client.close()
        _login(url, None)  # `probe logout`
        monkeypatch.setenv("PROBE_TOKEN", CODE_C)
        report = drain(Journal(tmp_path / "outbox"))
    assert _bearers(app) == []
    assert report.auth_blocked and len(Journal(tmp_path / "outbox").pending()) == 1


def test_an_op_queued_before_stamping_keeps_the_old_rule(app, tmp_path, monkeypatch):
    """Control, and the upgrade path: an op already on disk has no stamp, and
    the new drainer must deliver it exactly as the old one would have."""
    run_id = seeded_run(app, tmp_path)
    with serve(app) as url:
        _login(url, STORED_B)
        journal = Journal(tmp_path / "outbox", context={"name": None, "base_url": url})
        journal.append_http(
            "POST",
            f"/v1/runs/{run_id}/metrics",
            {"points": [{"key": "loss", "kind": "model", "value": 1.0, "step_index": 1}]},
        )
        monkeypatch.setenv("PROBE_TOKEN", ENV_A)
        report = drain(Journal(tmp_path / "outbox"))
    assert report.delivered == 1
    assert _bearers(app) == [STORED_B]


def test_a_held_op_does_not_hold_up_anyone_elses(app, tmp_path, monkeypatch):
    """Job A's op waits; the stored-login op queued after it still goes."""
    run_a = seeded_run(app, tmp_path)
    run_b = seeded_run(app, tmp_path)
    with serve(app) as url:
        _login(url, STORED_B)
        monkeypatch.setenv("PROBE_TOKEN", ENV_A)
        job = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
        _queue_a_metric(job, run_a)
        job.close()
        monkeypatch.delenv("PROBE_TOKEN")
        mine = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
        _queue_a_metric(mine, run_b)
        mine.close()
        report = drain(Journal(tmp_path / "outbox"))
    assert report.delivered == 1 and report.credential_held == 1
    assert _bearers(app) == [STORED_B]


def test_each_credential_has_its_own_queue(app, tmp_path, monkeypatch):
    """An env credential's writes queue apart from the stored login's
    (`credential-v1/<fingerprint>/`), so one never waits behind the other.
    The price, deliberately: order across two credentials writing ONE run is
    not kept (within a queue it is; see the set-aside tests)."""
    from probe.sdk.journal import CREDENTIAL_NAMESPACE, credential_fingerprint

    run_id = seeded_run(app, tmp_path)
    with serve(app) as url:
        _login(url, STORED_B)
        monkeypatch.setenv("PROBE_TOKEN", ENV_A)
        first = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
        _queue_a_metric(first, run_id, step=1)
        first.close()
        monkeypatch.delenv("PROBE_TOKEN")
        second = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
        _queue_a_metric(second, run_id, step=2)
        second.close()
        assert first.journal.dir == (
            tmp_path / "outbox" / CREDENTIAL_NAMESPACE / credential_fingerprint(ENV_A, None)
        )
        assert second.journal.dir == tmp_path / "outbox"
        report = drain(Journal(tmp_path / "outbox"))
    assert _bearers(app) == [STORED_B]  # A's waits for A; B's does not wait for it
    assert report.credential_held == 1 and report.delivered == 1


class _BackedOff(Exception):
    pass


def test_a_worker_backs_a_held_run_off_instead_of_exiting(app, env_job, monkeypatch):
    """#2041 round 3, MED-2. A worker left with only another credential's
    writes used to exit at once, so every kick forked a new one (~1/s, 0.9
    CPU-s each). Its run's lane now stalls, and the worker stays up waiting
    that run out: it neither spins nor exits (kicks then find its lease)."""
    from probe.sdk import outbox_worker

    _url, client, run_id = env_job
    monkeypatch.delenv("PROBE_TOKEN")
    waited: list = []

    def wait_out(journal, seen, lanes, seconds):
        waited.append((lanes.skip(), seconds))
        raise _BackedOff

    monkeypatch.setattr(outbox_worker, "_sleep_until_new_work", wait_out)
    with pytest.raises(_BackedOff):
        outbox_worker.run(str(client.journal.dir))
    assert waited and run_id in waited[0][0] and waited[0][1] > 0
    assert _bearers(app) == [] and len(client.journal.pending()) == 1


def test_a_kick_with_nothing_new_to_deliver_forks_no_worker(app, tmp_path, monkeypatch):
    """#2041 round 3, MED-2. When everything queued is what the last pass had
    to leave held, a kick forks nothing; a NEW write does."""
    from probe.sdk import outbox_worker

    run_id = seeded_run(app, tmp_path)
    with serve(app) as url:
        _login(url, STORED_B)
        monkeypatch.setenv("PROBE_TOKEN", ENV_A)
        job = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
        _queue_a_metric(job, run_id)
        job.close()
        monkeypatch.delenv("PROBE_TOKEN")
        queue = job.journal
        drain(Journal(queue.dir))  # a pass without A: held
        status = Journal.read_status(str(queue.dir), include_receipts=False) or {}
        assert status.get("held") == 1 and status.get("pending") == 1
        forks: list = []
        monkeypatch.setattr(outbox_worker.subprocess, "Popen", lambda *a, **k: forks.append(a) or (_ for _ in ()).throw(RuntimeError("forked")))
        assert outbox_worker.maybe_spawn(str(queue.dir)) is False
        assert forks == []
        monkeypatch.setenv("PROBE_TOKEN", ENV_A)
        again = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
        _queue_a_metric(again, run_id, step=2)  # something new: pending > held
        again.close()
        with pytest.raises(RuntimeError, match="forked"):
            outbox_worker.maybe_spawn(str(queue.dir))
        assert len(forks) == 1


def test_the_stamp_names_the_credential_without_carrying_it(app, env_job):
    from probe.sdk.journal import credential_fingerprint

    url, client, _run = env_job
    ((path, op),) = client.journal.pending()
    raw = path.read_text()
    assert ENV_A not in raw and STORED_B not in raw
    stamp = op["context"]["principal"]
    assert stamp == {"source": "env", "fingerprint": credential_fingerprint(ENV_A, None)}
    assert len(stamp["fingerprint"]) == 16
    assert op["context"]["name"] == "default" and op["context"]["base_url"] == url
    assert json.loads(raw)["context"] == op["context"]


def test_a_stored_login_is_stamped_as_the_login(tmp_path):
    from probe.sdk.journal import credential_fingerprint

    config.save_context({"base_url": "http://127.0.0.1:9", "token": STORED_B})
    client = Client(spool_dir=tmp_path / "outbox", async_writes=False)
    try:
        assert client.journal.context["principal"] == {
            "source": "config",
            "fingerprint": credential_fingerprint(STORED_B, None),
        }
    finally:
        client.close()


def test_a_crashed_runs_recovery_keeps_the_runs_credential(tmp_path, monkeypatch):
    """The capture record a dead run's recovery reads carries the stamp, so the
    log it queues goes out as the run, not as the machine."""
    import os
    from types import SimpleNamespace

    from probe.sdk.outputs import OutputCapture

    monkeypatch.setenv("PROBE_TOKEN", ENV_A)
    client = Client(spool_dir=tmp_path / "outbox", base_url="http://127.0.0.1:9", async_writes=False)
    try:
        capture = SimpleNamespace(
            journal=client.journal, run_id="r", pid=os.getpid(), host="h", root=str(tmp_path),
            started_at=None, launcher=None, sweeps=False, _baseline_file=None,
            _log_path=None, log_name=None, _helper_pid=None, ignore=None, _entry=None, writer=None,
        )
        record = OutputCapture._record(capture, shared_with=[])
    finally:
        client.close()
    assert record["context"]["principal"] == client.journal.context["principal"]
    assert record["context"]["principal"]["source"] == "env"


def test_probe_outbox_drain_says_why_it_kept_them(app, env_job, monkeypatch, capsys):
    import importlib

    import typer

    main = importlib.import_module("probe.cli.main")
    _url, client, _run = env_job
    monkeypatch.delenv("PROBE_TOKEN")
    monkeypatch.setattr(main, "_journal", lambda: Journal(client.journal.dir))
    with pytest.raises(typer.Exit):
        main._drain_foreground()
    err = capsys.readouterr().err
    assert "1 kept: queued with a credential from env (fingerprint " in err
    assert "that this process does not hold" in err
    assert _bearers(app) == []


# -- #2041 security review ------------------------------------------------------


def _queue_as_stored_login(url, tmp_path, run_id, token=STORED_B) -> None:
    _login(url, token, account=ACCOUNT)
    client = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
    try:
        _queue_a_metric(client, run_id)
    finally:
        client.close()


def _queue_as_env_job(tmp_path, monkeypatch, run_id, n=3) -> None:
    monkeypatch.setenv("PROBE_TOKEN", ENV_A)
    job = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
    try:
        for step in range(1, n + 1):
            _queue_a_metric(job, run_id, step=step)
    finally:
        job.close()


def test_a_revoked_logins_writes_are_set_aside_and_the_rest_still_go(app, tmp_path, monkeypatch):
    """MED-2. A refused stamped write stopped the WHOLE pass and set the
    box-wide auth block: a PROBE_TOKEN job delivered 0 of its 3 writes because
    someone else's login had been revoked. Only the refused credential's
    writes stop now."""
    run_b = seeded_run(app, tmp_path)
    run_a = seeded_run(app, tmp_path)
    with serve(app) as url:
        _queue_as_stored_login(url, tmp_path, run_b)
        app.rejected_tokens.add(STORED_B)  # revoked since
        _queue_as_env_job(tmp_path, monkeypatch, run_a)
        report = drain(Journal(tmp_path / "outbox"))
    assert _bearers(app) == [STORED_B, ENV_A, ENV_A, ENV_A]
    assert report.delivered == 3 and report.credential_refused == 1
    assert report.auth_blocked and not report.queue_auth_stopped and not report.auth_stopped
    ((_, left),) = Journal(tmp_path / "outbox").pending()
    assert left["run_ref"] == run_b
    status = Journal.read_status(str(tmp_path / "outbox")) or {}
    assert not status.get("auth_blocked_since"), "one login's refusal blocked the whole box"
    assert list(status.get("refused_fingerprints") or {}) == [_stamp_of(left)]


def _stamp_of(op) -> str:
    return op["context"]["principal"]["fingerprint"]


def test_an_unstamped_refusal_still_stops_the_queue(app, tmp_path, monkeypatch):
    """Negative control: an op queued by an older release names no credential,
    so nothing tells it apart from the rest of ITS queue -- it stops that
    queue's pass, as before. A credential queue is not that queue."""
    run_id = seeded_run(app, tmp_path)
    with serve(app) as url:
        _login(url, STORED_B)
        legacy = Journal(tmp_path / "outbox", context={"name": None, "base_url": url})
        legacy.append_http(
            "POST",
            f"/v1/runs/{run_id}/metrics",
            {"points": [{"key": "loss", "kind": "model", "value": 1.0, "step_index": 1}]},
        )
        app.rejected_tokens.add(STORED_B)
        _queue_as_env_job(tmp_path, monkeypatch, run_id, n=1)
        report = drain(Journal(tmp_path / "outbox"))
    assert report.queue_auth_stopped and report.auth_stopped
    assert report.delivered == 1 and _bearers(app) == [STORED_B, ENV_A]  # A's own queue went
    status = Journal.read_status(str(tmp_path / "outbox"), include_receipts=False) or {}
    assert status.get("auth_blocked_since")


def test_a_logged_out_logins_write_does_not_block_a_probe_token_jobs_worker(
    app, tmp_path, monkeypatch
):
    """The review's repro: a stored-login write queued, then `probe logout`,
    then a PROBE_TOKEN job. Its worker exited "auth-blocked" having delivered
    none of the job's writes."""
    from probe.sdk import outbox_worker

    run_b = seeded_run(app, tmp_path)
    run_a = seeded_run(app, tmp_path)
    with serve(app) as url:
        _queue_as_stored_login(url, tmp_path, run_b)
        _login(url, None)  # `probe logout`
        _queue_as_env_job(tmp_path, monkeypatch, run_a)
        monkeypatch.setattr(outbox_worker.time, "sleep", lambda _s: None)

        def wait_out(*_a, **_k):
            raise _BackedOff  # the worker stays up, backing B's run off

        monkeypatch.setattr(outbox_worker, "_sleep_until_new_work", wait_out)
        with pytest.raises(_BackedOff):
            outbox_worker.run(str(tmp_path / "outbox"))
        # A's writes are in A's own queue: the worker `run` started for it
        # (this environment holds A) delivers them, beside the root's.
        import time

        deadline = time.monotonic() + 30
        while len(_bearers(app)) < 3 and time.monotonic() < deadline:
            time.sleep(0.1)
    assert _bearers(app) == [ENV_A, ENV_A, ENV_A]
    ((_, left),) = Journal(tmp_path / "outbox").pending()
    assert left["run_ref"] == run_b
    status = Journal.read_status(str(tmp_path / "outbox")) or {}
    assert not status.get("auth_blocked_since")


def test_a_refused_credential_is_asked_once_per_cooldown_not_once_per_pass(app, tmp_path, monkeypatch):
    """Set aside, a refused credential must not cost a 401 on every pass (the
    zombie-uploader the box-wide block exists to prevent); `probe login`
    (clear_auth_block) lets it try again at once."""
    run_id = seeded_run(app, tmp_path)
    with serve(app) as url:
        _queue_as_stored_login(url, tmp_path, run_id)
        app.rejected_tokens.add(STORED_B)
        journal = Journal(tmp_path / "outbox")
        drain(journal)
        assert _bearer_requests(app, STORED_B) == 1
        second = drain(journal)
        assert _bearer_requests(app, STORED_B) == 1, "re-asked inside the cooldown"
        assert second.credential_held == 1 and second.credential_refused == 0
        journal.clear_auth_block()
        drain(journal)
    assert _bearer_requests(app, STORED_B) == 2


def test_the_writer_recovers_its_own_refused_writes_through_a_re_login(app, tmp_path, monkeypatch):
    """The cooldown binds other drainers, not the writer: once it picks up a
    new login of the same account (plan 2.7), its own set-aside writes go at
    once -- under the new token, with the stamp moved to it."""
    from probe.sdk.journal import credential_fingerprint

    run_id = seeded_run(app, tmp_path)
    new = "probe_pat_storedlogin_B_relogged_in"
    with serve(app) as url:
        _login(url, STORED_B, account=ACCOUNT)
        client = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
        try:
            client._ambient_credentials = True
            client._credential_source = "config"
            client._remember_identity()
            _queue_a_metric(client, run_id, step=1)
            app.rejected_tokens.add(STORED_B)
            drain(Journal(tmp_path / "outbox"))  # the detached worker: refused, set aside
            _login(url, new, account=ACCOUNT)
            assert client.refresh_credentials(refused=STORED_B)
            _queue_a_metric(client, run_id, step=2)
            delivered = client.flush()
        finally:
            client.close()
        stamps = [op["context"]["principal"] for _, op in Journal(tmp_path / "outbox").pending()]
    assert delivered == 2 and stamps == []
    assert _bearers(app)[-2:] == [new, new]
    assert credential_fingerprint(new, None) in client._credential_fingerprints


def test_an_older_drainer_never_sees_env_or_in_code_writes(app, tmp_path, monkeypatch):
    """MED-1, and the re-review's mixed-version MED. A release before #2035
    ignores the stamp and would send an env or in-code write as the stored
    login; faking a context it cannot resolve made it stop its whole pass
    there instead and block the box. Those writes now queue in
    `credential-v1/<fingerprint>/`, a directory no older release reads: it
    lists `ops/` and `delivery-v1/ops/` only. A stored-login write stays in the
    shared queue, where an older release sends it as the stored login -- what
    queued it."""
    from probe.sdk.journal import CREDENTIAL_NAMESPACE, _settings_for

    run_id = seeded_run(app, tmp_path)
    root = tmp_path / "outbox"
    with serve(app) as url:
        _login(url, STORED_B)
        _queue_as_env_job(tmp_path, monkeypatch, run_id, n=1)
        monkeypatch.setenv("PROBE_TOKEN", CODE_C)
        in_code = Client(token=CODE_C, spool_dir=root, async_writes=True, auto_drain=False)
        _queue_a_metric(in_code, run_id, step=5)
        in_code.close()
        monkeypatch.delenv("PROBE_TOKEN")
        mine = Client(spool_dir=root, async_writes=True, auto_drain=False)
        _queue_a_metric(mine, run_id, step=9)
        mine.close()
        # What an older drainer lists: the root queue and its receipt namespace.
        legacy_view = [op for _, op in Journal._read_dir(root / "ops")]
        legacy_view += [op for _, op in Journal._read_dir(root / "delivery-v1" / "ops")]
        assert [op["context"]["principal"]["source"] for op in legacy_view] == ["config"]
        assert _settings_for(legacy_view[0]["context"]).token == STORED_B
        hidden = sorted((root / CREDENTIAL_NAMESPACE).iterdir())
        assert len(hidden) == 2 and all(len(list((q / "ops").iterdir())) == 1 for q in hidden)
        # ... and every current reader still sees all three.
        assert Journal.read_status(str(root))["pending"] == 3
        assert sum(len(q.pending()) for q in Journal(root).namespaces()) == 3


def test_a_correlated_write_replays_after_a_re_login(app, tmp_path):
    """LOW. The request digest included the stamp, so re-queuing the same
    correlation after a re-login raised "belongs to a different request"."""
    run_id = seeded_run(app, tmp_path)
    with serve(app) as url:
        _login(url, STORED_B, account=ACCOUNT)
        results = []
        for token in (STORED_B, "probe_pat_storedlogin_B_relogged_in"):
            _login(url, token, account=ACCOUNT)
            client = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
            try:
                results.append(
                    client.enqueue_artifact_reference(
                        correlation="corr-1", anchor="run", anchor_id=run_id, name="ref",
                        uri="s3://bucket/x", content_hash="sha256:" + "0" * 64, size_bytes=1,
                    )
                )
            finally:
                client.close()
    assert results[0]["op_id"] == results[1]["op_id"]


def test_an_env_jobs_writes_survive_the_logins_ingest_token_changing(app, tmp_path, monkeypatch):
    """LOW. The fingerprint covered token AND ingest token, and a PROBE_TOKEN
    job's settings carry the stored login's ingest token: a re-login that
    changed only that stranded the job's writes. The bearer token names it."""
    run_id = seeded_run(app, tmp_path)
    with serve(app) as url:
        config.save_context({"base_url": url, "token": STORED_B, "ingest_token": "ros_ing_" + "11" * 16})
        _queue_as_env_job(tmp_path, monkeypatch, run_id, n=2)
        config.save_context({"ingest_token": "ros_ing_" + "22" * 16})
        report = drain(Journal(tmp_path / "outbox"))
    assert report.delivered == 2 and _bearers(app) == [ENV_A, ENV_A]


def test_a_crashed_runs_recovery_never_uses_another_credential(tmp_path, monkeypatch):
    """LOW. Recovery listed the run's artifacts and uploaded its outputs with
    whatever credential the recovering process resolved. With a stamp, only
    the run's own credential -- or none, and everything is queued."""
    from probe.sdk.journal import credential_fingerprint
    from probe.sdk.outputs import _recovery_client

    config.save_context({"base_url": "http://127.0.0.1:9", "token": STORED_B})
    record = {
        "journal_dir": str(tmp_path / "outbox"),
        "context": {
            "name": None,
            "base_url": "http://127.0.0.1:9",
            "principal": {"source": "env", "fingerprint": credential_fingerprint(ENV_A, None)},
        },
    }
    client, journal = _recovery_client(record)
    assert client is None and journal is not None  # the stored login is not the run's
    monkeypatch.setenv("PROBE_TOKEN", ENV_A)
    client, _journal = _recovery_client(record)
    try:
        assert client is not None and client.settings.token == ENV_A
    finally:
        client.close()


def test_another_logins_refusal_is_not_this_clients(tmp_path):
    """LOW (#2021). `_own_credential_refusal` matched on the context name only,
    so a PROBE_TOKEN job took the stored login's 401 for its own."""
    from types import SimpleNamespace

    from probe.sdk.journal import credential_fingerprint

    client = Client(token=CODE_C, base_url="http://127.0.0.1:9", spool_dir=tmp_path / "o", async_writes=False)
    try:
        def report(fingerprint):
            context = {"name": None, "base_url": "http://127.0.0.1:9",
                       "principal": {"source": "config", "fingerprint": fingerprint}}
            refusal = {"status": 401, "message": "invalid or revoked token", "context": context}
            return SimpleNamespace(
                auth_blocked=True, auth_status=401, auth_message=refusal["message"],
                auth_context=context, auth_refusals=[refusal],
            )

        assert not client._own_credential_refusal(report(credential_fingerprint(STORED_B, None)))
        assert client._own_credential_refusal(report(credential_fingerprint(CODE_C, None)))
    finally:
        client.close()


# -- #2041 security re-review ---------------------------------------------------

INGEST_A = "ros_ing_envjob_A_0123456789abcdef"
INGEST_B = "ros_ing_storedlogin_B_0123456789ab"


def _ingest_bearers(app) -> list[str]:
    return [
        r.headers.get("authorization", "").removeprefix("Bearer ")
        for r in app.requests
        if r.url.path.startswith("/ingest")
    ]


def test_an_ingest_write_goes_out_with_the_ingest_token_that_queued_it(app, tmp_path, monkeypatch):
    """HIGH. `/ingest` requests are sent with the INGEST token, but the stamp
    named the personal one: a job with PROBE_INGEST_TOKEN=I_A on a box logged
    in as B (ingest I_B) had its queued ingest write sent with I_B by B's
    worker and flush(). The write now names the key its route uses."""
    app.seed_experiment("e1")
    with serve(app) as url:
        config.save_context({"base_url": url, "token": STORED_B, "ingest_token": INGEST_B})
        monkeypatch.setenv("PROBE_INGEST_TOKEN", INGEST_A)
        job = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
        job.ingest(experiment_slug="e1", project_slug="p", run={"source": "x", "external_id": "rA", "name": "fromA"})
        job.close()
        monkeypatch.delenv("PROBE_INGEST_TOKEN")
        drain(Journal(tmp_path / "outbox"))  # a worker with only B's login
        other = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
        other.flush()  # B's own flush
        other.close()
        assert _ingest_bearers(app) == [], "the stored login's ingest token sent A's write"
        monkeypatch.setenv("PROBE_INGEST_TOKEN", INGEST_A)
        report = drain(Journal(tmp_path / "outbox"))  # the job's own worker
    assert report.delivered == 1 and _ingest_bearers(app) == [INGEST_A]


def test_one_write_without_a_recorded_account_does_not_strand_the_tokens_others(app, tmp_path):
    """MED (regression). The pass cached "cannot deliver" per token, so the
    first write of a login whose account was not yet recorded stranded every
    write of that token after a same-account re-login (10 of 10). One token is
    one account: any of its writes that recorded it vouches for all."""
    run_id = seeded_run(app, tmp_path)
    with serve(app) as url:
        _login(url, STORED_B)  # saved without an account (an older CLI)
        client = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
        try:
            _queue_a_metric(client, run_id, step=1)  # queued before the account was known
            client._remember_identity()  # the heartbeat's lookup
            for step in range(2, 11):
                _queue_a_metric(client, run_id, step=step)
        finally:
            client.close()
        _login(url, "probe_pat_storedlogin_B_relogged_in", account=ACCOUNT)
        report = drain(Journal(tmp_path / "outbox"))
    assert report.delivered == 10 and report.credential_held == 0
    assert set(_bearers(app)) == {"probe_pat_storedlogin_B_relogged_in"}


def test_the_account_check_is_asked_once_not_once_per_pass(app, tmp_path):
    """LOW. `/v1/me` ran once per pass for another account's queued writes: an
    exporter at 0.2 s asked 43 times in 8 s. The answer is cached per token."""
    run_id = seeded_run(app, tmp_path)
    other = "probe_pat_someone_else_0123456789abcdef"
    app.me_identities[other] = {"customer_id": "lab-99", "user_id": "u-someone-else"}
    with serve(app) as url:
        _queue_as_stored_login(url, tmp_path, run_id)
        _login(url, other, account=("lab-99", "u-someone-else"))
        before = app.me_requests
        for _ in range(5):
            drain(Journal(tmp_path / "outbox"))
    assert app.me_requests - before == 1
    assert _bearers(app) == []


def test_a_token_passed_in_code_is_delivered_while_the_job_runs(app, tmp_path):
    """LOW. The detached worker can never hold a token passed in code, so such
    a client's async writes waited for flush()/finish() (0 of 5 live, stranded
    after a crash). It delivers through its in-process exporter instead."""
    import time

    run_id = seeded_run(app, tmp_path)
    with serve(app) as url:
        client = Client(token=CODE_C, base_url=url, spool_dir=tmp_path / "outbox", async_writes=True)
        try:
            assert client._drain_interval is not None
            for step in range(1, 6):
                _queue_a_metric(client, run_id, step=step)
            deadline = time.monotonic() + 10
            while len(_bearers(app)) < 5 and time.monotonic() < deadline:
                time.sleep(0.1)
            assert _bearers(app) == [CODE_C] * 5, "not delivered while the client was alive"
        finally:
            client.close()


def test_a_login_during_a_pass_is_not_undone_by_it(app, tmp_path):
    """LOW. A pass wrote back the refusal list it read when it started, so a
    `probe login` (clear_auth_block) that landed mid-pass was undone and the
    refused credential stayed set aside for another cooldown."""
    run_id = seeded_run(app, tmp_path)
    journal = Journal(tmp_path / "outbox")
    with serve(app) as url:
        _queue_as_stored_login(url, tmp_path, run_id)
        app.rejected_tokens.add(STORED_B)
        drain(journal)  # refused: set aside, remembered
        assert (Journal.read_status(str(journal.dir)) or {}).get("refused_fingerprints")

        def login_mid_pass(context):
            journal.clear_auth_block()  # `probe login`, while the pass runs
            return None

        drain(journal, client_factory=login_mid_pass)
    assert not (Journal.read_status(str(journal.dir)) or {}).get("refused_fingerprints")


# -- #2041 security review, round 3 ---------------------------------------------


def _patch_close(client: Client, run_id: str, status: str = "completed") -> None:
    """What `probe run end --async` and a deferred finish queue: the run's
    terminal status write."""
    client.write("PATCH", f"/v1/runs/{run_id}", {"status": status})


def _closes(app) -> list[str]:
    return [
        r.headers.get("authorization", "").removeprefix("Bearer ")
        for r in app.requests
        if r.method == "PATCH" and b'"status"' in (r.content or b"")
    ]


def test_a_probe_token_equal_to_the_stored_login_queues_in_the_shared_queue(app, tmp_path, monkeypatch):
    """Round 3, MED-1. The same token as PROBE_TOKEN and as the stored login
    went to a credential queue, so a close queued by the stored login landed
    before that job's data. By value, it is the stored login: shared queue."""
    run_id = seeded_run(app, tmp_path)
    with serve(app) as url:
        _login(url, STORED_B)
        monkeypatch.setenv("PROBE_TOKEN", STORED_B)
        job = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
        _queue_a_metric(job, run_id)
        job.close()
        assert job.journal.dir == tmp_path / "outbox"
        monkeypatch.delenv("PROBE_TOKEN")
        closer = Client(spool_dir=tmp_path / "outbox", async_writes=True, auto_drain=False)
        _patch_close(closer, run_id)
        closer.close()
        drain(Journal(tmp_path / "outbox"))
    order = [r.method for r in app.requests if r.url.path.startswith(f"/v1/runs/{run_id}")]
    assert order[-2:] == ["POST", "PATCH"], "the close overtook the run's data"


def test_a_run_close_waits_for_its_writes_in_another_queue(app, tmp_path, monkeypatch):
    """Round 3, MED-1. `probe run end --async` from a stored-login shell queued
    the close in the shared queue while a PROBE_TOKEN job's data for the same
    run sat in its credential queue: the close arrived first, 5 of 5. The
    drain now holds a run's close while its earlier writes are queued
    elsewhere; once they are gone it goes."""
    run_id = seeded_run(app, tmp_path)
    root = tmp_path / "outbox"
    with serve(app) as url:
        _login(url, STORED_B)
        _queue_as_env_job(tmp_path, monkeypatch, run_id, n=2)
        monkeypatch.delenv("PROBE_TOKEN")
        closer = Client(spool_dir=root, async_writes=True, auto_drain=False)
        _patch_close(closer, run_id)
        closer.close()
        first = drain(Journal(root))  # a stored-login worker: cannot send A's data
        assert _closes(app) == [], "the close went ahead of the run's data"
        assert first.close_held == 1
        assert any("waits for 2 of its write(s)" in r for r in first.held_reasons)
        monkeypatch.setenv("PROBE_TOKEN", ENV_A)
        drain(Journal(root))  # the job's own worker delivers its data...
        monkeypatch.delenv("PROBE_TOKEN")
        drain(Journal(root))  # ...and then the close goes
    assert _bearers(app) == [ENV_A, ENV_A]
    assert _closes(app) == [STORED_B]


def test_a_held_close_goes_after_the_cap(app, tmp_path, monkeypatch):
    """Control: writes nothing here may send never deliver; past
    CLOSE_HOLD_MAX_SECONDS the close goes rather than leave the run open."""
    from probe.sdk import journal as journal_module

    run_id = seeded_run(app, tmp_path)
    root = tmp_path / "outbox"
    with serve(app) as url:
        _login(url, STORED_B)
        _queue_as_env_job(tmp_path, monkeypatch, run_id, n=1)
        monkeypatch.delenv("PROBE_TOKEN")
        closer = Client(spool_dir=root, async_writes=True, auto_drain=False)
        _patch_close(closer, run_id)
        closer.close()
        monkeypatch.setattr(journal_module, "CLOSE_HOLD_MAX_SECONDS", -1.0)
        report = drain(Journal(root))
    assert report.close_held == 0 and _closes(app) == [STORED_B]


def test_finish_from_another_credential_defers_the_close_behind_the_runs_data(app, tmp_path, monkeypatch):
    """Round 3, MED-1. `Run.finish()` in a stored-login process counted only
    its own queue, found nothing and wrote the close at once, ahead of the
    run's data queued by a PROBE_TOKEN job. It now counts the run's writes in
    every queue: the close is deferred, and the drain keeps it behind them."""
    from tests.conftest import open_run

    root = tmp_path / "outbox"
    with serve(app) as url:
        _login(url, STORED_B)
        monkeypatch.setenv("PROBE_BASE_URL", url)
        closer = Client(spool_dir=root, async_writes=True, auto_drain=False)
        run = open_run(closer, experiment="e", name="r", heartbeat=False)
        _queue_as_env_job(tmp_path, monkeypatch, run.id, n=2)
        monkeypatch.delenv("PROBE_TOKEN")
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            run.finish("completed", flush_timeout=1.0)
        closer.close()
        assert _closes(app) == [], "finish wrote the close ahead of the run's data"
        monkeypatch.setenv("PROBE_TOKEN", ENV_A)
        drain(Journal(root))
        monkeypatch.delenv("PROBE_TOKEN")
        drain(Journal(root))
    assert _bearers(app) == [ENV_A, ENV_A]
    assert len(_closes(app)) == 1


def test_a_wizard_logins_writes_follow_a_same_account_re_login(app, tmp_path):
    """Round 3, MED-3. A login saved without an account (the setup wizard) left
    its CLI writes stuck forever after a same-account re-login (0 of 3). The
    first write that goes out with that login teaches the machine its account
    (`record_account`), and the rest then follow the re-login."""
    run_id = seeded_run(app, tmp_path)
    root = tmp_path / "outbox"
    with serve(app) as url:
        _login(url, STORED_B)  # no account recorded
        writer = Client(spool_dir=root, async_writes=True, auto_drain=False)
        _queue_a_metric(writer, run_id, step=1)
        drain(Journal(root))  # delivered with B: B's account is learned
        for step in (2, 3, 4):
            _queue_a_metric(writer, run_id, step=step)
        writer.close()
        _login(url, "probe_pat_storedlogin_B_relogged_in")  # no account recorded either
        report = drain(Journal(root))
    assert report.delivered == 3 and report.credential_held == 0
    assert _bearers(app) == [STORED_B] + ["probe_pat_storedlogin_B_relogged_in"] * 3


def test_the_wizard_records_its_new_logins_account(app, tmp_path, monkeypatch):
    """Round 3, MED-3: the wizard's own record (conftest stubs it elsewhere)."""
    import importlib

    from probe.sdk.journal import credential_fingerprint, recorded_account

    setup = importlib.import_module("probe.cli.setup")
    real = importlib.reload(setup)._record_login_account
    with serve(app) as url:
        config.save_context({"base_url": url, "token": STORED_B})
        real(url, STORED_B, None)
    assert recorded_account(credential_fingerprint(STORED_B, None)) == ACCOUNT
    assert config.load_context()["identity"]["customer_id"] == ACCOUNT[0]


def test_probe_outbox_discard_held_drops_only_permanently_held_writes(app, tmp_path, monkeypatch, capsys):
    """Round 3 MED-3 and round 4 MED-A. `--held` drops what no credential here
    will send (B's write, now another account is logged in); it keeps a live
    PROBE_TOKEN job's writes (that job sends them -- round 3 destroyed 4 of
    4) and anything this shell can send; `--credential` names A to drop A's."""
    import importlib

    main = importlib.import_module("probe.cli.main")
    run_id = seeded_run(app, tmp_path)
    root = tmp_path / "outbox"
    other = "probe_pat_someone_else_0123456789abcdef"
    app.me_identities[other] = {"customer_id": "lab-99", "user_id": "u-someone-else"}
    with serve(app) as url:
        _queue_as_stored_login(url, tmp_path, run_id)  # B's, account recorded
        _queue_as_env_job(tmp_path, monkeypatch, run_id, n=4)  # A's, a live job's
        monkeypatch.delenv("PROBE_TOKEN")
        _login(url, other, account=("lab-99", "u-someone-else"))  # someone else now
        mine = Client(spool_dir=root, async_writes=True, auto_drain=False)
        _queue_a_metric(mine, run_id, step=9)  # deliverable here
        mine.close()
        monkeypatch.setattr(main, "_journal", lambda: Journal(root))
        main.outbox_discard(op_id=None, held=True, credential=None)
        assert "discarded 1 held write(s)" in capsys.readouterr().out
        left = [op for q in Journal(root).namespaces() for _, op in q.pending()]
        assert sorted(op["body"]["points"][0]["step_index"] for op in left) == [1, 2, 3, 4, 9]
        from probe.sdk.journal import credential_fingerprint

        main.outbox_discard(op_id=None, held=True, credential=credential_fingerprint(ENV_A, None))
    assert "discarded 4 held write(s)" in capsys.readouterr().out
    left = [op for q in Journal(root).namespaces() for _, op in q.pending()]
    assert [op["body"]["points"][0]["step_index"] for op in left] == [9]


def test_discard_held_keeps_a_login_whose_account_cannot_be_confirmed(app, tmp_path, monkeypatch, capsys):
    """Round 4 MED-A. With `/v1/me` answering 503, a stored-login write a
    same-account re-login would deliver is not "held": it stays."""
    import importlib

    main = importlib.import_module("probe.cli.main")
    from probe.sdk import journal as journal_module

    run_id = seeded_run(app, tmp_path)
    root = tmp_path / "outbox"
    with serve(app) as url:
        _queue_as_stored_login(url, tmp_path, run_id)
        _login(url, "probe_pat_storedlogin_B_relogged_in", account=ACCOUNT)
        app.me_status = 503
        monkeypatch.setattr(journal_module, "_IDENTITY_CACHE", {})
        monkeypatch.setattr(main, "_journal", lambda: Journal(root))
        main.outbox_discard(op_id=None, held=True, credential=None)
    assert "discarded 0 held write(s)" in capsys.readouterr().out
    assert len(Journal(root).pending()) == 1


def test_the_discard_hint_names_only_permanently_held_writes(app, env_job, monkeypatch, capsys):
    """Round 4 MED-A. `probe outbox drain` offered `discard --held` for a live
    PROBE_TOKEN job's writes; it offers it only for writes no credential here
    will send, and names the other job's credential instead."""
    import importlib

    import typer

    from probe.sdk.journal import credential_fingerprint

    main = importlib.import_module("probe.cli.main")
    _url, client, _run = env_job
    monkeypatch.delenv("PROBE_TOKEN")
    monkeypatch.setattr(main, "_journal", lambda: Journal(client.journal.dir))
    with pytest.raises(typer.Exit):
        main._drain_foreground()
    err = capsys.readouterr().err
    assert "discard --held" not in err
    assert credential_fingerprint(ENV_A, None) in err


def test_a_foreign_drains_held_count_does_not_silence_the_owners_kick(app, tmp_path, monkeypatch):
    """Round 4 LOW-B. B's drain wrote held=1 into A's queue; A's own kick was
    then suppressed for up to 5 minutes. A process holding the queue's
    credential is not suppressed."""
    from probe.sdk import outbox_worker

    run_id = seeded_run(app, tmp_path)
    with serve(app) as url:
        _login(url, STORED_B)
        _queue_as_env_job(tmp_path, monkeypatch, run_id, n=1)
        monkeypatch.delenv("PROBE_TOKEN")
        queue = next(q for q in Journal(tmp_path / "outbox").namespaces() if q.dir.parent.name == "credential-v1")
        drain(Journal(tmp_path / "outbox"))  # B's foreground drain reaches A's queue
        assert (Journal.read_status(str(queue.dir), include_receipts=False) or {}).get("held") == 1
        forks: list = []

        def popen(*a, **k):
            forks.append(a)
            raise RuntimeError("forked")

        monkeypatch.setattr(outbox_worker.subprocess, "Popen", popen)
        assert outbox_worker.maybe_spawn(str(queue.dir)) is False  # B: suppressed
        monkeypatch.setenv("PROBE_TOKEN", ENV_A)
        with pytest.raises(RuntimeError, match="forked"):
            outbox_worker.maybe_spawn(str(queue.dir))  # A: not
    assert len(forks) == 1


def test_kept_counts_every_held_write_not_every_run(app, env_job, monkeypatch):
    """Round 4 LOW-C: "N kept" said 1 for 5 held writes of one run."""
    _url, client, run_id = env_job
    for step in range(2, 6):
        _queue_a_metric(client, run_id, step=step)
    monkeypatch.delenv("PROBE_TOKEN")
    report = drain(Journal(client.journal.dir))
    assert report.credential_held == 5


def test_coalescing_never_merges_two_credentials(app, tmp_path, monkeypatch):
    """#2053 integration: a coalesced batch shares its head's context, so two
    credentials' writes of one run never ride one POST."""
    from probe.sdk.journal import _merge_key

    run = "00000000-0000-4000-8000-000000000001"
    point = {"key": "loss", "kind": "model", "value": 1.0, "step_index": 1}
    a = {"kind": "http", "method": "POST", "path": f"/v1/runs/{run}/metrics", "run_ref": run,
         "context": {"name": None, "base_url": "u", "principal": {"source": "env", "fingerprint": "a" * 16}},
         "body": {"points": [point]}}
    b = {**a, "context": {"name": None, "base_url": "u", "principal": {"source": "config", "fingerprint": "b" * 16}}}
    assert _merge_key(a) is not None and _merge_key(b) is not None
    assert _merge_key(a) != _merge_key(b)
    assert _merge_key(a) == _merge_key({**a})


def test_a_direct_send_waits_for_the_runs_writes_in_another_queue(app, tmp_path, monkeypatch):
    """#2054 integration: below the free-space floor a write is sent directly
    only when its run has nothing queued -- in ANY queue: a direct send would
    overtake the run's writes queued under another credential."""
    from probe.sdk import journal as journal_module

    run_id = seeded_run(app, tmp_path)
    root = tmp_path / "outbox"
    with serve(app) as url:
        _login(url, STORED_B)
        _queue_as_env_job(tmp_path, monkeypatch, run_id, n=1)
        monkeypatch.delenv("PROBE_TOKEN")
        mine = Client(spool_dir=root, async_writes=True, auto_drain=False)
        monkeypatch.setattr(journal_module.Journal, "below_floor", lambda self: "low disk")
        try:
            sent = mine._send_instead_of_queueing(
                "POST", f"/v1/runs/{run_id}/metrics",
                {"points": [{"key": "loss", "kind": "model", "value": 1.0, "step_index": 7}]},
            )
        finally:
            mine.close()
    assert sent is False and _bearers(app) == []


def test_idle_credential_queues_are_pruned(tmp_path, monkeypatch):
    """Round 3, LOW-1. One folder per token ever used piled up (420 made
    `finish()` 15x slower). An empty, idle, unlocked one is removed; one with
    a queued write, or whose worker holds its lease, is not."""
    import fcntl
    import os

    from probe.sdk import journal as journal_module

    root = tmp_path / "outbox"
    empty = Journal.for_credential(root, "a" * 16)
    busy = Journal.for_credential(root, "b" * 16)
    leased = Journal.for_credential(root, "c" * 16)
    for queue in (empty, busy, leased):
        queue._ensure()
    busy.append_http("POST", "/v1/runs/r/metrics", {"points": []})
    for queue in (empty, busy, leased):
        for path in (queue.dir, *queue.dir.iterdir()):
            os.utime(path, (1, 1))
    handle = (leased.dir / ".worker.lock").open("a+")
    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    os.utime(leased.dir / ".worker.lock", (1, 1))
    monkeypatch.setattr(journal_module, "_last_prune", float("-inf"))
    try:
        assert journal_module.prune_credential_queues(root) == 1
    finally:
        handle.close()
    assert not empty.dir.exists() and busy.dir.exists() and leased.dir.exists()
    empty.append_http("POST", "/v1/runs/r/metrics", {"points": []})  # a writer comes back
    assert len(empty.pending()) == 1


# -- #2041 security review, round 5 ---------------------------------------------


def test_a_held_close_is_looked_at_again_when_its_hold_ends(app, tmp_path, monkeypatch):
    """Round 5 MED. A close held to its cap went 216 s late (its run's backoff
    had grown to 300 s) and landed after the reaper. The close hold stalls the
    run with `wake_by` = what is left of the hold, and the run's backoff never
    waits past it; the cap is under the reaper's window."""
    from probe.sdk import journal as journal_module
    from probe.sdk.journal import LaneBackoff

    assert journal_module.CLOSE_HOLD_MAX_SECONDS <= 780  # 900 s stale - 120 s sweep
    run_id = seeded_run(app, tmp_path)
    root = tmp_path / "outbox"
    with serve(app) as url:
        _login(url, STORED_B)
        _queue_as_env_job(tmp_path, monkeypatch, run_id, n=1)
        monkeypatch.delenv("PROBE_TOKEN")
        closer = Client(spool_dir=root, async_writes=True, auto_drain=False)
        _patch_close(closer, run_id)
        closer.close()
        report = drain(Journal(root))
    stall = report.stalled_runs[run_id]
    assert stall.held and 0 < stall.wake_by <= journal_module.CLOSE_HOLD_MAX_SECONDS
    lanes = LaneBackoff(ceiling=300.0)
    for _ in range(12):  # a backoff grown to its ceiling...
        lanes.record(report, now=0.0)
    stall.wake_by = 5.0  # ...still wakes when the hold ends
    lanes.record(report, now=0.0)
    assert lanes.next_wake(now=0.0) <= 5.0


def test_a_close_never_waits_for_an_older_attempts_writes(app, tmp_path, monkeypatch):
    """Round 5 MED. Writes stamped with an older write epoch than the close's
    are refused by the server anyway; the close does not wait for them."""
    run_id = seeded_run(app, tmp_path)
    root = tmp_path / "outbox"
    with serve(app) as url:
        _login(url, STORED_B)
        monkeypatch.setenv("PROBE_TOKEN", ENV_A)
        job = Client(spool_dir=root, async_writes=True, auto_drain=False)
        job.write("POST", f"/v1/runs/{run_id}/metrics",
                  {"points": [{"key": "loss", "kind": "model", "value": 1.0, "step_index": 1}], "write_epoch": 1})
        job.close()
        monkeypatch.delenv("PROBE_TOKEN")
        closer = Client(spool_dir=root, async_writes=True, auto_drain=False)
        closer.write("PATCH", f"/v1/runs/{run_id}", {"status": "completed", "write_epoch": 2})
        closer.close()
        report = drain(Journal(root))
    assert report.close_held == 0 and len(_closes(app)) == 1


def test_a_held_run_is_not_read_as_an_unreachable_server(app, env_job, monkeypatch):
    """Round 5 item 4. hold() stalled a run like a network failure (status
    None); #2069's takeover barrier read that as "unreachable" and stopped."""
    _url, client, run_id = env_job
    monkeypatch.delenv("PROBE_TOKEN")
    report = drain(Journal(client.journal.dir))
    stall = report.stalled_runs[run_id]
    assert stall.held is True and stall.status is None
    assert not report.unreachable


def test_a_takeover_names_the_old_attempts_writes_it_cannot_send(app, tmp_path, monkeypatch, capsys):
    """Round 5 MED. A relaunch with a ROTATED PROBE_TOKEN took over silently:
    the old attempt's writes sat in the old token's queue, could not land
    before the reopen, and were later dead-lettered as stale. The barrier now
    says so."""
    import warnings as _warnings

    from tests.test_run_takeover import EXTERNAL_ID, _quiet

    rotated = "probe_pat_envtoken_A_rotated_456789abcdef"
    root = tmp_path / "outbox"
    with serve(app) as url:
        monkeypatch.setenv("PROBE_BASE_URL", url)
        _login(url, STORED_B)
        monkeypatch.setenv("PROBE_TOKEN", ENV_A)
        first = Client(spool_dir=root, async_writes=True, auto_drain=False)
        first.create_project("takeover-lab", "Takeover Lab", kind="general")
        old = first.run(project="takeover-lab", name=EXTERNAL_ID, external_id=EXTERNAL_ID, heartbeat=False)
        for step in range(3):
            old.log({"loss": 1.0}, step=step)
        first.close()
        _quiet(app, old.id, 1000.0)
        monkeypatch.setenv("PROBE_TOKEN", rotated)
        app.me_identities[rotated] = {}
        second = Client(spool_dir=root, async_writes=True, auto_drain=False)
        try:
            with _warnings.catch_warnings(record=True) as caught:
                _warnings.simplefilter("always")
                second.run(project="takeover-lab", name=EXTERNAL_ID, external_id=EXTERNAL_ID, heartbeat=False)
        finally:
            second.close()
    said = [str(w.message) for w in caught if "previous attempt" in str(w.message)]
    assert said and "queued under another credential" in said[0], [str(w.message) for w in caught]
    assert "3 op(s)" in said[0]


def test_a_rotated_relaunch_closes_its_run_without_waiting_for_the_old_attempt(app, tmp_path, monkeypatch):
    """Round 5 MED, the finish() half. A relaunch under a rotated PROBE_TOKEN
    counted the old attempt's writes in the old token's queue as its own and
    deferred its close behind them; the server refuses those writes (older
    write epoch), so the run stayed "running" until the crash sweep."""
    from tests.test_run_takeover import EXTERNAL_ID, _quiet

    rotated = "probe_pat_envtoken_A_rotated_456789abcdef"
    root = tmp_path / "outbox"
    with serve(app) as url:
        monkeypatch.setenv("PROBE_BASE_URL", url)
        _login(url, STORED_B)
        monkeypatch.setenv("PROBE_TOKEN", ENV_A)
        first = Client(spool_dir=root, async_writes=True, auto_drain=False)
        first.create_project("takeover-lab", "Takeover Lab", kind="general")
        old = first.run(project="takeover-lab", name=EXTERNAL_ID, external_id=EXTERNAL_ID, heartbeat=False)
        for step in range(3):
            old.log({"loss": 1.0}, step=step)
        first.close()
        _quiet(app, old.id, 1000.0)
        monkeypatch.setenv("PROBE_TOKEN", rotated)
        app.me_identities[rotated] = {}
        second = Client(spool_dir=root, async_writes=True, auto_drain=False)
        try:
            with pytest.warns(UserWarning, match="previous attempt"):
                new = second.run(project="takeover-lab", name=EXTERNAL_ID, external_id=EXTERNAL_ID, heartbeat=False)
            new.log({"loss": 0.1}, step=10)
            new.finish(flush_timeout=5)
        finally:
            second.close()
        assert new.write_epoch == 2
        assert app.runs[old.id]["status"] == "completed"
        # The old attempt's writes are still there for their own credential,
        # which the server then refuses as superseded; nothing is lost here.
        assert Journal(root).run_ops_elsewhere(old.id).pending()
        assert not Journal(root).run_ops_elsewhere(old.id, min_epoch=2).pending()


def test_probe_run_end_does_not_wait_for_an_older_attempts_writes(app, tmp_path, monkeypatch, capsys):
    """Round 5 MED, the `probe run end` half. Its barrier counted the old
    attempt's writes, queued under a token this shell does not hold, and
    refused to close ("NOT closed: 1 still queued") behind writes the server
    refuses as superseded anyway."""
    import importlib

    from probe.cli import run_lock

    main = importlib.import_module("probe.cli.main")
    monkeypatch.setattr("probe.cli.outbox_worker.maybe_spawn", lambda directory=None: False)
    run_id = seeded_run(app, tmp_path)
    app.runs[run_id]["write_epoch"] = 2  # a newer attempt reopened it
    root = tmp_path / "outbox"
    with serve(app) as url:
        monkeypatch.setenv("PROBE_BASE_URL", url)
        _login(url, STORED_B)
        monkeypatch.setenv("PROBE_TOKEN", ENV_A)
        old = Client(spool_dir=root, async_writes=True, auto_drain=False)
        point = {"key": "loss", "kind": "model", "value": 1.0, "step_index": 1}
        old.write("POST", f"/v1/runs/{run_id}/metrics", {"points": [point], "write_epoch": 1})
        old.close()
        monkeypatch.delenv("PROBE_TOKEN")
        run_lock.touch_lease(run_id, write_epoch=2)  # what this attempt's `run start` pinned
        rc = main.main(["--spool-dir", str(root), "run", "end", run_id, "--flush-timeout", "1"])
    assert rc == 0, capsys.readouterr()
    assert app.runs[run_id]["status"] == "completed"


def test_a_lease_release_waits_behind_another_credentials_writes(app, tmp_path, monkeypatch):
    """Round 6 MED (#2060 leases x #2035). On a `leases` run the close is the
    owner's lease release, and the close hold matched only a status PATCH: the
    release went out, the server closed the run, and a PROBE_TOKEN job's 3
    writes of it were still queued in their own queue."""
    app.supports_leases = True
    root = tmp_path / "outbox"
    with serve(app) as url:
        monkeypatch.setenv("PROBE_BASE_URL", url)
        _login(url, STORED_B)
        owner = Client(spool_dir=root, async_writes=True, auto_drain=False)
        owner.create_project("lease-lab", "Lease Lab", kind="general")
        run = owner.run(project="lease-lab", name="leased")
        assert run._leased()
        monkeypatch.setenv("PROBE_TOKEN", ENV_A)
        job = Client(spool_dir=root, async_writes=True, auto_drain=False)
        for step in range(3):
            point = {"key": "a", "kind": "model", "value": float(step), "step_index": step}
            job.write("POST", f"/v1/runs/{run.id}/metrics", {"points": [point]})
        job.close()
        monkeypatch.delenv("PROBE_TOKEN")
        try:
            report = run.finish(flush_timeout=0.2)
            assert report["finish_queued"] is True
            drain(Journal(root))  # the stored login's worker: A's writes are not its to send
            assert [r for r in app.lease_releases if r["run_id"] == run.id] == []
            assert app.runs[run.id]["status"] == "running"
            monkeypatch.setenv("PROBE_TOKEN", ENV_A)
            drain(Journal(root / CREDENTIAL_NAMESPACE / credential_fingerprint(ENV_A, None)))
            monkeypatch.delenv("PROBE_TOKEN")
            drain(Journal(root))
        finally:
            owner.close()
    assert sorted(p["step_index"] for p in app.metric_points_posted[run.id]) == [0, 1, 2]
    assert [r for r in app.lease_releases if r["run_id"] == run.id]
    assert app.runs[run.id]["status"] == "completed"


def test_the_cross_queue_count_forgets_writes_that_left(tmp_path):
    """A long-lived counter over several queues forgets delivered files, as the
    one-queue counter does (review of #2054); its cache is keyed per queue."""
    from probe.sdk.journal import CREDENTIAL_NAMESPACE

    root = tmp_path / "outbox"
    shared = Journal(root)
    other = Journal(root / CREDENTIAL_NAMESPACE / ("ab" * 8))
    run_id = "run-1"
    for queue in (shared, other):
        queue.append_http("POST", f"/v1/runs/{run_id}/metrics", {"points": []}, run_ref=run_id)
    counter = shared.run_ops_elsewhere(run_id)
    assert len(counter.pending()) == 1
    for path in other.ops_dir.iterdir():
        path.unlink()
    assert counter.pending() == []
    assert counter._mine == {}


def test_probe_login_wakes_a_worker_sleeping_on_held_runs(tmp_path):
    """Round 5 LOW. After `probe login`, held writes went up to 300 s later
    (the worker mid-sleep). `clear_auth_block` stamps `.wake`, which ends the
    worker's sleep."""
    import threading
    import time

    from probe.sdk import outbox_worker
    from probe.sdk.journal import LaneBackoff

    journal = Journal(tmp_path / "outbox")
    journal._ensure()
    done = threading.Event()

    def sleeper():
        outbox_worker._sleep_until_new_work(journal, set(), LaneBackoff(ceiling=300.0), 60.0)
        done.set()

    thread = threading.Thread(target=sleeper, daemon=True)
    started = time.monotonic()
    thread.start()
    time.sleep(0.2)
    journal.clear_auth_block()
    assert done.wait(10.0), "the worker slept through `probe login`"
    assert time.monotonic() - started < 10.0


def test_the_discard_hint_counts_every_permanently_held_write(app, tmp_path, monkeypatch, capsys):
    """Round 5 LOW. The hint said "1 of them" when `discard --held` drops 3:
    only each run's first held write was counted."""
    import importlib

    import typer

    main = importlib.import_module("probe.cli.main")
    run_id = seeded_run(app, tmp_path)
    root = tmp_path / "outbox"
    other = "probe_pat_someone_else_0123456789abcdef"
    app.me_identities[other] = {"customer_id": "lab-99", "user_id": "u-someone-else"}
    with serve(app) as url:
        _login(url, STORED_B, account=ACCOUNT)
        writer = Client(spool_dir=root, async_writes=True, auto_drain=False)
        for _ in range(3):  # unstepped points: not coalesced, one op each
            writer.write("POST", f"/v1/runs/{run_id}/metrics",
                         {"points": [{"key": "loss", "kind": "model", "value": 1.0}]})
        writer.close()
        _login(url, other, account=("lab-99", "u-someone-else"))
        monkeypatch.setattr(main, "_journal", lambda: Journal(root))
        with pytest.raises(typer.Exit):
            main._drain_foreground()
    assert "(3 of them no credential here will send" in capsys.readouterr().err
