"""`innoday sync --status`, and the pre-flight that every sync now begins with.

Two agent sessions ran a sync on the same project minutes apart. Nothing warned
either of them: the board stage refuses a concurrent run, but only *after* one
has been attempted, so the way you learn a sync is in flight is to start one and
be refused. There was no command that answered "is something running", and the
project-level route that existed had no caller and deliberately ignored runs
that had not finished.
"""

from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timedelta, timezone

import pytest

from src.cli.commands.sync import SyncCommands


class _Resp:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code
        self.text = "{}"

    def json(self):
        return self._payload


class _ReachedTheCascade(Exception):
    """Raised by the fake on the first call *after* the pre-flight.

    Asserting "it carried on" by simulating the whole three-stage cascade would
    be testing the fakes. This says exactly the thing under test -- that the
    pre-flight let it through -- and nothing else.
    """


class _Client:
    """Records every path asked for, so a test can assert nothing was started."""

    def __init__(self, payload, status_code=200):
        self._payload = payload
        self._status_code = status_code
        self.gets: list = []
        self.posts: list = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False

    async def get(self, path, params=None):
        self.gets.append(path)
        if path.endswith("/sync/status"):
            return _Resp(self._payload, self._status_code)
        raise _ReachedTheCascade(path)

    async def post(self, path, **kwargs):
        self.posts.append(path)
        raise _ReachedTheCascade(path)


class _Config:
    def get_current_organization(self):
        return "bp"

    def get_organization_id(self, alias):
        return "org-1"

    def get_current_project_id(self):
        return "proj-1"

    def get_sync_timeout(self):
        return 30.0


def _args(**over):
    base = dict(sync_command=None, sync_status_only=False, since=None, scope="all")
    base.update(over)
    return argparse.Namespace(**base)


def _running_payload(started_minutes_ago=3):
    started = datetime.now(timezone.utc) - timedelta(minutes=started_minutes_ago)
    return {
        "project_id": "proj-1",
        "is_fresh": False,
        "is_running": True,
        "running": [
            {
                "id": "run-9",
                "board_registration_id": "board-1",
                "status": "in_progress",
                "started_at": started.isoformat(),
            }
        ],
        "last_sync": None,
    }


_IDLE = {
    "project_id": "proj-1",
    "is_fresh": True,
    "is_running": False,
    "running": [],
    "last_sync": {
        "id": "run-8",
        "board_registration_id": "board-1",
        "status": "completed",
        "started_at": "2026-08-21T07:00:00",
        "completed_at": "2026-08-21T07:02:16",
        "tickets_found": 216,
        "tickets_created": 14,
        "tickets_updated": 202,
        "error_message": None,
    },
}


def _run(monkeypatch, args, payload, status_code=200):
    import src.cli.commands.sync as sync_mod

    client = _Client(payload, status_code)
    monkeypatch.setattr(
        sync_mod, "InnoDayAPIClient", lambda config, timeout=None: client
    )
    rc = asyncio.run(SyncCommands.execute(args, _Config()))
    return rc, client


class TestStatusIsTheOnlyThingThatHappens:
    def test_it_reports_and_starts_nothing(self, monkeypatch):
        """A status flag that also syncs is one nobody can safely run -- and the
        reason to ask is usually that you are unsure it is safe to start one."""
        rc, client = _run(monkeypatch, _args(sync_status_only=True), _running_payload())
        assert rc == 0
        assert client.posts == []
        assert client.gets == ["/organizations/org-1/projects/proj-1/sync/status"]

    def test_it_reports_even_when_nothing_is_running(self, monkeypatch):
        rc, client = _run(monkeypatch, _args(sync_status_only=True), _IDLE)
        assert rc == 0
        assert client.posts == []

    def test_an_unanswerable_status_is_an_error_not_a_shrug(self, monkeypatch):
        """Asked directly, "I could not tell you" is a failure. It is only the
        pre-flight below that may continue past it."""
        rc, _ = _run(monkeypatch, _args(sync_status_only=True), {}, status_code=503)
        assert rc == 1


class TestEverySyncAsksFirst:
    def test_a_run_in_flight_stops_the_cascade_before_it_starts(self, monkeypatch):
        """Two sessions used to find each other by colliding: the board stage
        refuses a concurrent run, but only once one has been attempted."""
        rc, client = _run(monkeypatch, _args(), _running_payload())
        assert rc == 1
        assert client.posts == []
        assert client.gets == ["/organizations/org-1/projects/proj-1/sync/status"]

    def test_an_idle_project_syncs_normally(self, monkeypatch):
        """The pre-flight must not become a reason nothing ever runs."""
        with pytest.raises(_ReachedTheCascade):
            _run(monkeypatch, _args(), _IDLE)

    def test_an_unreadable_status_warns_and_continues(self, monkeypatch):
        """**Not permission, and not a blocker.** A server that cannot answer
        says nothing about whether a sync is running -- so it must not read as
        "nothing is running", and must not stop real work either."""
        with pytest.raises(_ReachedTheCascade):
            _run(monkeypatch, _args(), {}, status_code=503)


class TestAge:
    @pytest.mark.parametrize(
        "delta,expected_unit",
        [
            (timedelta(seconds=20), "s ago"),
            (timedelta(minutes=8), "m ago"),
            (timedelta(hours=3), "h ago"),
        ],
    )
    def test_the_roughest_useful_unit(self, delta, expected_unit):
        when = (datetime.now(timezone.utc) - delta).isoformat()
        assert SyncCommands._age(when).endswith(expected_unit)

    def test_a_missing_timestamp_does_not_raise(self):
        assert SyncCommands._age(None) == "at an unknown time"


class TestThePreflightCannotKillTheSync:
    """A check that cannot answer must cost the caller nothing.

    The first version caught only `APIError`. A slow status route raises
    `httpx.ReadTimeout`, which is not one -- so it escaped to the handler that
    turns any timeout into "the sync did not answer" and returns 1. The
    pre-flight would have killed the run it exists to protect, and the earlier
    tests missed it because they simulated a 503 rather than a slow reply.
    """

    @staticmethod
    def _timing_out_client():
        import httpx as _httpx

        class Client:
            def __init__(self):
                self.gets: list = []

            async def __aenter__(self):
                return self

            async def __aexit__(self, *a):
                return False

            async def get(self, path, params=None):
                self.gets.append(path)
                if path.endswith("/sync/status"):
                    raise _httpx.ReadTimeout("too slow")
                raise _ReachedTheCascade(path)

            async def post(self, path, **kwargs):
                raise _ReachedTheCascade(path)

        return Client()

    def test_a_slow_status_does_not_stop_the_cascade(self, monkeypatch):
        import src.cli.commands.sync as sync_mod

        client = self._timing_out_client()
        monkeypatch.setattr(
            sync_mod, "InnoDayAPIClient", lambda config, timeout=None: client
        )
        with pytest.raises(_ReachedTheCascade):
            asyncio.run(SyncCommands.execute(_args(), _Config()))

    def test_a_slow_status_asked_for_directly_is_still_an_error(self, monkeypatch):
        """Only the pre-flight may shrug. Asked directly, it must not claim
        anything about a project it could not reach."""
        import src.cli.commands.sync as sync_mod

        client = self._timing_out_client()
        monkeypatch.setattr(
            sync_mod, "InnoDayAPIClient", lambda config, timeout=None: client
        )
        assert (
            asyncio.run(SyncCommands.execute(_args(sync_status_only=True), _Config()))
            == 1
        )
