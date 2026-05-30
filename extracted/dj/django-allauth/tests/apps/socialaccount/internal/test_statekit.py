import time

from allauth.socialaccount.internal import statekit


def test_get_oldest_state():
    states = {
        "new": [{"id": "new"}, 300],
        "mid": [{"id": "mid"}, 200],
        "old": [{"id": "old"}, 100],
    }
    state_id, state = statekit.get_oldest_state(states)
    assert state_id == "old"
    assert state["id"] == "old"


def test_get_oldest_state_empty():
    state_id, state = statekit.get_oldest_state({})
    assert state_id is None
    assert state is None


def test_gc_states():
    now = time.time()
    states = {}
    for i in range(statekit.MAX_STATES + 1):
        states[f"state-{i}"] = [{"i": i}, now + i]
    assert len(states) == statekit.MAX_STATES + 1
    statekit.gc_states(states)
    assert len(states) == statekit.MAX_STATES
    assert "state-0" not in states


def test_gc_states_expires():
    now = time.time()
    states = {
        "fresh": [{"id": "fresh"}, now],
        "expired": [{"id": "expired"}, now - statekit.STATE_TTL - 1],
    }
    statekit.gc_states(states)
    assert "fresh" in states
    assert "expired" not in states


def test_stashing(rf):
    request = rf.get("/")
    request.session = {}

    # Stash states with a small delay
    state_id = statekit.stash_state(request, {"foo": "bar"})
    time.sleep(0.001)  # delay for microseconds
    state2_id = statekit.stash_state(request, {"foo2": "bar2"})
    time.sleep(0.001)  # delay for microseconds
    state3_id = statekit.stash_state(request, {"foo3": "bar3"})

    # Unstash last state and check order
    state = statekit.unstash_last_state(request)
    assert state == {"foo3": "bar3"}

    state = statekit.unstash_state(request, state3_id)
    assert state is None
    state = statekit.unstash_state(request, state2_id)
    assert state == {"foo2": "bar2"}
    state = statekit.unstash_state(request, state2_id)
    assert state is None
    state = statekit.unstash_state(request, state_id)
    assert state == {"foo": "bar"}
    state = statekit.unstash_state(request, state_id)
    assert state is None


def test_unstash_expired_state(rf):
    request = rf.get("/")
    request.session = {}
    state_id = statekit.stash_state(request, {"foo": "bar"})
    # Backdate the timestamp to simulate expiry
    states = statekit.get_states(request)
    states[state_id] = (states[state_id][0], time.time() - statekit.STATE_TTL - 1)
    request.session[statekit.STATES_SESSION_KEY] = states
    state = statekit.unstash_state(request, state_id)
    assert state is None
