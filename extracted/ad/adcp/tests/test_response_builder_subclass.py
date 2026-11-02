"""Subclass passthrough tests for response builders.

Sellers routinely extend SDK-generated response types with internal
fields (``implementation_config``, ``seller_notes``, database primary
keys) marked ``exclude=True`` so they stay off the wire. The response
builders call ``_serialize`` which runs ``model_dump(exclude_none=True)``
— the Pydantic default. These tests lock the contract: a subclass with
``exclude=True`` internal fields round-trips through
``products_response()`` and friends with no leak.

Salesagent has hit this: their ``Product`` subclass carries an
``implementation_config`` dict describing how they map the spec
Product onto their ad server. If ``model_dump`` stopped honouring
``exclude`` or the builder started bypassing it, downstream would
silently leak internals — hard to catch in end-to-end tests, easy to
catch here.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from adcp.server.responses import (
    list_creatives_response,
    media_buys_response,
    products_response,
    signals_response,
)
from adcp.types import Creative, MediaBuy, MediaBuyStatus, Product, Signal


class _SubclassedProduct(Product):
    """Product with an internal-only field that MUST NOT appear in
    serialised responses."""

    implementation_config: dict[str, Any] = Field(default_factory=dict, exclude=True)
    seller_notes: str | None = Field(default=None, exclude=True)


def test_products_response_excludes_subclass_internal_fields() -> None:
    """``products_response`` round-trips subclassed Products without
    leaking fields marked ``exclude=True``."""
    subclassed = _SubclassedProduct.model_construct(
        product_id="p1",
        name="Display Home",
        publisher_properties=[],
        pricing_options=[],
        inventory_type="publisher_owned",
        implementation_config={
            "ad_server": "gam",
            "line_item_template_id": "internal-42",
        },
        seller_notes="budget-locked to Q3",
    )

    response = products_response([subclassed])

    assert len(response["products"]) == 1
    product_dict = response["products"][0]

    assert product_dict["product_id"] == "p1"
    assert product_dict["name"] == "Display Home"
    assert "implementation_config" not in product_dict, (
        f"implementation_config leaked into wire payload: {product_dict}. "
        f"exclude=True on a subclass field is load-bearing — sellers "
        f"rely on it to keep internals off the wire."
    )
    assert "seller_notes" not in product_dict


def test_products_response_accepts_mixed_subclass_and_base() -> None:
    """Mix of base Product + _SubclassedProduct — neither shape leaks
    extras, both serialise the wire fields."""
    base = Product.model_construct(
        product_id="base-1",
        name="Base product",
        publisher_properties=[],
        pricing_options=[],
        inventory_type="publisher_owned",
    )
    subbed = _SubclassedProduct.model_construct(
        product_id="sub-1",
        name="Subclass product",
        publisher_properties=[],
        pricing_options=[],
        inventory_type="publisher_owned",
        implementation_config={"leak": "must-not-appear"},
    )

    response = products_response([base, subbed])

    product_ids = {p["product_id"] for p in response["products"]}
    assert product_ids == {"base-1", "sub-1"}
    for product in response["products"]:
        assert "implementation_config" not in product
        assert "leak" not in product


def test_signals_response_honours_subclass_exclude() -> None:
    """Same guarantee for signals — Signal is a separate generated
    class, so this pins the behaviour broadly, not just on Product."""

    class _SubclassedSignal(Signal):
        internal_metric: float | None = Field(default=None, exclude=True)

    signal = _SubclassedSignal.model_construct(
        signal_agent_segment_id="seg-1",
        name="High-intent auto",
        description="Users researching auto",
        signal_type="audience",
        data_provider="internal",
        coverage_percentage=85.0,
        pricing=[],
        deployments=[],
        internal_metric=0.97,
    )

    response = signals_response([signal])

    signal_dict = response["signals"][0]
    assert signal_dict["signal_agent_segment_id"] == "seg-1"
    assert "internal_metric" not in signal_dict


def test_media_buys_response_honours_subclass_exclude() -> None:
    """media_buys_response runs the same _serialize path — ensure the
    subclass passthrough test covers that builder too so a future
    refactor splitting _serialize can't silently regress one builder."""

    class _SubclassedMediaBuy(MediaBuy):
        internal_pg_id: int | None = Field(default=None, exclude=True)

    mb = _SubclassedMediaBuy.model_construct(
        media_buy_id="mb-1",
        status=MediaBuyStatus.active,
        packages=[],
        internal_pg_id=12345,
    )

    response = media_buys_response([mb])
    mb_dict = response["media_buys"][0]
    assert mb_dict["media_buy_id"] == "mb-1"
    assert "internal_pg_id" not in mb_dict


def test_list_creatives_response_honours_subclass_exclude() -> None:
    """list_creatives_response runs the same _serialize path — confirm
    subclass passthrough for the creatives listing variant too."""

    class _SubclassedCreative(Creative):
        internal_approval_id: str | None = Field(default=None, exclude=True)

    creative = _SubclassedCreative.model_construct(
        creative_id="c-1",
        name="Video ad",
        format_id="video_30s",
        status="approved",
        internal_approval_id="approv-42",
    )

    response = list_creatives_response([creative])
    creative_dict = response["creatives"][0]
    assert creative_dict["creative_id"] == "c-1"
    assert "internal_approval_id" not in creative_dict
