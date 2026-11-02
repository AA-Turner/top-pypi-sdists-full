"""Synthetic-fixture parse: typed data model with open-record passthrough.

Emulates SPEC 4: a mocked POST /v1/run returns the synthetic envelope, the
generated (here hand-built) typed data model parses it, and the extra key on an
open item record round-trips via ``.model_extra``.
"""

from __future__ import annotations

from typing import Any

import httpx
from pydantic import BaseModel, ConfigDict

from getanyapi import RunResult, unwrap
from conftest import json_response, make_sync_client, run_envelope


class ReviewItem(BaseModel):
    # Open item record: additionalProperties not false -> extra="allow".
    model_config = ConfigDict(extra="allow")
    id: str
    rating: int


class AmazonReviewsData(BaseModel):
    # Closed data wrapper.
    reviews: list[ReviewItem]


def test_typed_data_model_parses_synthetic_fixture() -> None:
    synth = {"reviews": [{"id": "sample", "rating": 1, "_extra": "passthrough"}]}
    fixture = run_envelope(synth, cost_usd=0.001, items=1)

    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(200, fixture)

    client, _ = make_sync_client(respond)
    raw: RunResult[Any] = client.run("amazon.reviews", {"product": "B0"})
    # Re-validate the untyped envelope into the typed data model (what the
    # generated method returns via RunResult[AmazonReviewsData]).
    typed = RunResult[AmazonReviewsData].model_validate(
        raw.model_dump(by_alias=True)
    )
    data = unwrap(typed)
    assert isinstance(data, AmazonReviewsData)
    assert data.reviews[0].id == "sample"
    assert data.reviews[0].rating == 1
    # Open record kept the unknown field.
    assert data.reviews[0].model_extra == {"_extra": "passthrough"}
    assert typed.cost_usd > 0
    assert typed.items == 1
