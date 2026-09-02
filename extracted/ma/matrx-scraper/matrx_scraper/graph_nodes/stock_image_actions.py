"""``media.stock_image.search`` — find existing stock images via Unsplash.

Many study-pack and content-generation workflows need *real* photos
rather than synthesized ones — a textbook chapter on photosynthesis is
better illustrated by an actual leaf cross-section than by an AI hallucination.

This node is a thin matrx-graph wrapper over the reusable
``matrx_scraper.features.stock_image_search.search_stock_images`` primitive
(the single source of the Unsplash HTTP + parse logic, shared with the
``random_wheel`` LLM tool). The response shape is provider-agnostic (typed
``StockImage`` objects) so a future Pexels / Pixabay backend can plug in.

Auth:
- Unsplash: ``UNSPLASH_ACCESS_KEY`` env var, or ``ctx.app.api_keys["unsplash"]``.

The Unsplash API response embeds attribution data (photographer name +
profile link). We surface those fields directly because Unsplash's
licence requires attribution.
"""

from __future__ import annotations

import os
from typing import Any, Literal

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from matrx_graph.types.usl import field_extras
from pydantic import BaseModel, ConfigDict, Field

from matrx_scraper.features.stock_image_search import (
    parse_stock_image_item,
    search_stock_images,
)


def _resolve_unsplash_key(ctx: NodeExecutionContext | None, explicit: str | None) -> str | None:
    """Resolve an Unsplash key without requiring end-user input.

    Order of preference:
    1. Per-call override (``inputs.api_key``).
    2. ``ctx.app.api_keys["unsplash"]`` — host-injected per-request key.
    3. ``UNSPLASH_ACCESS_KEY`` env var — host process-level key.

    Returns None only if none of these are populated.
    """
    if explicit:
        return explicit
    if ctx is not None:
        try:
            api_keys = getattr(ctx.app, "api_keys", None) or {}
        except AttributeError:
            api_keys = {}
        host_key = api_keys.get("unsplash") or api_keys.get("UNSPLASH_ACCESS_KEY")
        if host_key:
            return host_key
    return os.environ.get("UNSPLASH_ACCESS_KEY")


class StockImage(BaseModel):
    """A stock-photo result with attribution + multiple size URLs.

    Fully closed shape: every constructor site spreads
    ``parse_stock_image_item(...)``, whose key set is exactly the declared
    fields — nothing dynamic ever lands here.
    """

    url_full: str = Field(description="Full-resolution image URL.")
    url_regular: str = Field(description="Regular-size variant — the default for embedding.")
    url_thumb: str = Field(description="Thumbnail URL.")
    width: int = 0
    height: int = 0
    description: str | None = None
    photographer_name: str | None = None
    photographer_url: str | None = None
    source: Literal["unsplash"] = "unsplash"
    source_id: str = Field(description="Provider-specific image id.")
    license: str = Field(default="Unsplash License")
    attribution_required: bool = True


class StockImageSearchInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    # NOT min_length=1: stock images are an OPTIONAL enrichment. A workflow
    # definition that bakes an empty/missing query (e.g. a saved study-pack
    # snapshot) must DEGRADE — skip the search and return empty — never crash
    # input validation and park the whole run on a non-essential node.
    query: str = Field(
        default="",
        description="Search terms. Blank → the node returns no images.",
        json_schema_extra=field_extras(widget="text"),
    )
    per_page: int = Field(
        default=5,
        ge=1,
        le=30,
        description="Results per call.",
    )
    page: int = Field(default=1, ge=1)
    orientation: Literal["any", "landscape", "portrait", "squarish"] = Field(
        default="any",
        description="Filter by aspect orientation.",
    )
    color: str | None = Field(
        default=None,
        description=(
            "Optional dominant-color filter. Unsplash accepts: "
            "black_and_white, black, white, yellow, orange, red, purple, "
            "magenta, green, teal, blue."
        ),
    )
    api_key: str | None = Field(
        default=None,
        description="Override UNSPLASH_ACCESS_KEY for this call.",
    )


class StockImageSearchOutput(BaseModel):
    """Success payload (Node Result System) — provider/config failures are
    node Failures with code ``search_failed``; a blank query degrades to an
    empty success (optional-enrichment contract, see StockImageSearchInput)."""

    model_config = ConfigDict(extra="forbid")

    images: list[StockImage] = Field(default_factory=list)
    total: int = 0
    total_pages: int = 0
    query: str


@register_node(
    name="media.stock_image.search",
    display_name="Find Stock Photos",
    description="Search Unsplash for real photos, with photographer credits included.",
    category=NodeCategory.IO,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=StockImageSearchInput,
    output_schema=StockImageSearchOutput,
    output_kind="stock_image_search_result",
    icon="image",
    tags=("stock", "image", "search", "unsplash"),
)
async def stock_image_search(
    ctx: NodeExecutionContext, inputs: StockImageSearchInput
) -> NodeResult[StockImageSearchOutput]:
    if not inputs.query.strip():
        # Optional-node degrade: nothing to search for. Return an EMPTY
        # SUCCESS rather than calling Unsplash with a blank query (which
        # 400s) or failing the node — a saved workflow with a blank query
        # must not park the whole run on a non-essential enrichment.
        return success(StockImageSearchOutput(query=""))

    api_key = _resolve_unsplash_key(ctx, inputs.api_key)
    if not api_key:
        return failure(
            "search_failed",
            "No Unsplash key available — host should provide via "
            "UNSPLASH_ACCESS_KEY env or AppContext.api_keys. End users "
            "do not need to supply their own. Get a host key at "
            "https://unsplash.com/developers.",
            details={"query": inputs.query, "reason": "missing_api_key"},
        )

    result = await search_stock_images(
        inputs.query,
        api_key=api_key,
        per_page=inputs.per_page,
        page=inputs.page,
        orientation=inputs.orientation,
        color=inputs.color,
    )
    if result.get("error"):
        return failure(
            "search_failed",
            str(result["error"]),
            details={"query": inputs.query},
        )

    images = [StockImage(**img) for img in result.get("images", [])]
    return success(
        StockImageSearchOutput(
            images=images,
            total=int(result.get("total", 0) or 0),
            total_pages=int(result.get("total_pages", 0) or 0),
            query=inputs.query,
        )
    )


def _parse_unsplash_item(item: dict[str, Any]) -> StockImage:
    """Back-compat thin wrapper over the shared parser (one parse implementation)."""
    return StockImage(**parse_stock_image_item(item))
