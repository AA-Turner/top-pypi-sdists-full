# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import time

import pytest
import ray
import ray.actor
from ray._private import state
from ray.util.state import list_actors
from ray.util.state.exception import RayStateApiException

# More than Ray's state API cap (RAY_MAX_LIMIT_FROM_DATA_SOURCE, 10,000).
NUM_ACTORS = 11000
REGISTRATION_TIMEOUT_S = 120
REGISTRATION_POLL_S = 0.5


@ray.remote
class DummyActor:
    def ping(self) -> str:
        return "pong"


def _create_registered_actors(num_actors: int) -> list[ray.actor.ActorHandle]:
    """Create actors and wait until the GCS has registered all of them.

    ``.remote()`` returns before the actor is registered, and the state API only
    sees actors the GCS has registered.
    """
    actors = [DummyActor.remote() for _ in range(num_actors)]
    deadline = time.monotonic() + REGISTRATION_TIMEOUT_S
    # The private actor table is read uncapped; the public state API is not.
    while (registered := len(state.actors())) < num_actors:
        if time.monotonic() > deadline:
            pytest.fail(
                f"{registered} of {num_actors} actors registered after "
                f"{REGISTRATION_TIMEOUT_S}s"
            )
        time.sleep(REGISTRATION_POLL_S)
    return actors


@pytest.mark.limit
@pytest.mark.ray
def test_actor_listing_explodes() -> None:
    ray.init()
    try:
        actors = _create_registered_actors(NUM_ACTORS)  # noqa: F841

        # Call list_actors without filters, which will trigger truncation
        # and raise RayStateApiException because there are >10,000 actors
        with pytest.raises(RayStateApiException):
            _ = list_actors()  # defaults to raise_on_missing_output=True
    finally:
        ray.shutdown()


@pytest.mark.ray
@pytest.mark.limit
def test_actor_listing_truncates() -> None:
    ray.init()
    try:
        actors = _create_registered_actors(NUM_ACTORS)  # noqa: F841

        # Call list_actors without filters, but truncating
        lst_actors = list_actors(limit=42, raise_on_missing_output=False)  # truncates
        assert len(lst_actors) == 42  # if no limit specified its 100
    finally:
        ray.shutdown()


@pytest.mark.ray
@pytest.mark.limit
def test_actor_listing_filter() -> None:
    ray.init()
    try:
        actors = _create_registered_actors(NUM_ACTORS)  # noqa: F841

        # Call list_actors without filters, but truncating
        _ = list_actors(
            filters=[("state", "=", "ALIVE")], raise_on_missing_output=False
        )  # filtered
    finally:
        ray.shutdown()
