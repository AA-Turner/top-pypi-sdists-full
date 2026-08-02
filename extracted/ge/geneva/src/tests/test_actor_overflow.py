# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import time

import pytest
import ray
from ray.util.state import list_actors
from ray.util.state.exception import RayStateApiException


@ray.remote
class DummyActor:
    def ping(self) -> str:
        return "pong"


@pytest.mark.limit
@pytest.mark.ray
def test_actor_listing_explodes() -> None:
    ray.init()
    try:
        # Spin up > 10,000 actors (Ray’s state API cap is 10k)
        num_actors = 11000
        actors = [DummyActor.remote() for _ in range(num_actors)]  # noqa: F841

        # Give Ray a moment to register all the actors
        time.sleep(2)

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
        # Spin up > 10,000 actors (Ray’s state API cap is 10k)
        num_actors = 11000
        actors = [DummyActor.remote() for _ in range(num_actors)]  # noqa: F841

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
        # Spin up > 10,000 actors (Ray’s state API cap is 10k)
        num_actors = 11000
        actors = [DummyActor.remote() for _ in range(num_actors)]  # noqa: F841

        # Call list_actors without filters, but truncating
        _ = list_actors(
            filters=[("state", "=", "ALIVE")], raise_on_missing_output=False
        )  # filtered
    finally:
        ray.shutdown()
