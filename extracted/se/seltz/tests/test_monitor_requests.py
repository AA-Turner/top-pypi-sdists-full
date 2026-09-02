"""The cadence reaches the request as a scalar field.

`schedule` is a proto3 oneof with one string member, so the cadence is set
directly on the request rather than through a wrapper message. A wrong field
name here is silent: protobuf raises only on assignment, and the structural
tests never build a request.
"""

import pytest

from seltz.services.monitor_service import _create_request, _update_request
from seltz._types import OMIT


def test_create_carries_the_cadence() -> None:
    request = _create_request("key", "n", "1h", [], OMIT, OMIT)
    assert request.cadence == "1h"
    assert request.WhichOneof("schedule") == "cadence"


def test_update_sets_the_cadence_only_when_given() -> None:
    given = _update_request("key", "m", OMIT, OMIT, "6h", OMIT, OMIT)
    assert given.cadence == "6h"
    assert given.WhichOneof("schedule") == "cadence"

    omitted = _update_request("key", "m", OMIT, OMIT, OMIT, OMIT, OMIT)
    assert omitted.WhichOneof("schedule") is None


def test_update_rejects_an_explicitly_empty_search_request_list():
    """Refuse an empty list: the wire cannot carry it as anything but absent."""
    with pytest.raises(ValueError, match="must not be empty"):
        _update_request(
            "k",
            "m",
            name=OMIT,
            status=OMIT,
            cadence=OMIT,
            search_requests=[],
            webhook=OMIT,
        )
