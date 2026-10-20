"""`status.get` (plan X7): a `probe.core.run status` child, cached, refreshed on change.

At most one child per context within the TTL; `refresh: true` always runs one,
with the slow checks; a session starting or ending and an action ending make
the next answer a fresh one; each request context has its own entry and its
child gets that context. Real service, real children (`FakeCore` plays
`probe.core.run status`; the real one is `test_core_run.py`'s and the T3
`test_status_get_runs_probe_status_and_caches_it`).
"""

from __future__ import annotations

import json
import sys

import pytest

from probe.service.protocol import Method, Mode
from tests.service_fakes import FakeCore
from tests.service_harness import kill_agent, service_home, spawn_agent, wait_for  # noqa: F401 -- a fixture

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="the service is POSIX-only (plan S8)")

SNAPSHOT = {"schema_version": 1, "signed_in": True, "agents": []}


@pytest.fixture
def core(service_home):
    fake = FakeCore(service_home.home)
    fake.plan("status", stdout=SNAPSHOT)
    fake.plan("logout", steps=[])
    return fake


def test_one_child_per_ttl_and_refresh_runs_the_slow_checks(service_home, core):
    service_home.start()
    with service_home.connect() as conn:
        assert conn.call(Method.STATUS_GET, {}) == SNAPSHOT
        assert conn.call(Method.STATUS_GET, {}) == SNAPSHOT
        assert len(core.calls("status")) == 1
        assert conn.call(Method.STATUS_GET, {"refresh": True}) == SNAPSHOT
        assert conn.call(Method.STATUS_GET, {}) == SNAPSHOT  # the refreshed answer, cached
    calls = core.calls("status")
    assert [json.loads(c["stdin"]) for c in calls] == [{}, {"refresh": True}]
    assert all(c["flags"] == ["-I"] for c in calls)


def test_a_session_change_and_an_action_end_make_the_next_answer_fresh(service_home, core):
    service_home.start()
    agent, owner = spawn_agent()
    try:
        with service_home.connect() as conn:
            conn.call(Method.STATUS_GET, {})
            conn.call(
                Method.SESSION_REGISTER,
                {"sid": "s-1", "harness": "test", "mode": Mode.INLINE, "owner": owner, "generation": 1},
            )
            conn.call(Method.STATUS_GET, {})
            assert len(core.calls("status")) == 2
            # A heartbeat (the same registration again) changes nothing.
            conn.call(
                Method.SESSION_REGISTER,
                {"sid": "s-1", "harness": "test", "mode": Mode.INLINE, "owner": owner, "generation": 1},
            )
            conn.call(Method.STATUS_GET, {})
            assert len(core.calls("status")) == 2
            action_id = conn.call(
                Method.ACTION_RUN, {"action": "logout", "params": {}, "client_request_id": "c"}
            )["action_id"]
            assert wait_for(
                lambda: conn.call(Method.ACTION_STATUS, {"action_id": action_id})["state"] == "done", 5.0
            )
            conn.call(Method.STATUS_GET, {})
            assert len(core.calls("status")) == 3
            kill_agent(agent)
            assert wait_for(lambda: not conn.call(Method.SESSION_LIST)["sessions"], 5.0)
            conn.call(Method.STATUS_GET, {})
            assert len(core.calls("status")) == 4
    finally:
        kill_agent(agent)


def test_each_context_has_its_own_answer_and_its_child_gets_the_context(service_home, core):
    service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.STATUS_GET, {})
        custom = {"context": {"PROBE_CONFIG_PATH": "/app/probe.json", "XDG_CONFIG_HOME": "/app/xdg"}}
        conn.call(Method.STATUS_GET, custom)
        conn.call(Method.STATUS_GET, custom)
        conn.call(Method.STATUS_GET, {})
    plain, scoped = core.calls("status")
    assert plain["env"]["PROBE_CONFIG_PATH"] is None
    assert scoped["env"]["PROBE_CONFIG_PATH"] == "/app/probe.json"
    assert scoped["env"]["XDG_CONFIG_HOME"] == "/app/xdg"


def test_a_child_with_no_answer_is_refused(service_home, core):
    from probe.service import client
    from probe.service.protocol import ErrorCode

    core.plan("status", stdout="not an object", exit=1)
    service_home.start()
    with service_home.connect() as conn:
        with pytest.raises(client.ServiceError) as raised:
            conn.call(Method.STATUS_GET, {})
    assert raised.value.code == ErrorCode.REFUSED
    assert raised.value.data == {"reason": "status_unavailable"}


def test_max_age_zero_runs_a_fresh_local_child(service_home, core):
    service_home.start()
    with service_home.connect() as conn:
        conn.call(Method.STATUS_GET, {})
        conn.call(Method.STATUS_GET, {"max_age": 0})
        conn.call(Method.STATUS_GET, {"max_age": 0})
        conn.call(Method.STATUS_GET, {"max_age": 25})  # the last answer is young enough
        with pytest.raises(Exception):
            conn.call(Method.STATUS_GET, {"max_age": -1})
    calls = core.calls("status")
    assert [json.loads(c["stdin"]) for c in calls] == [{}, {}, {}]  # never the slow checks
