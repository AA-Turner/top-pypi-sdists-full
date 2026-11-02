"""Public data models and typed dicts for the getanyapi SDK (SPEC 3.3, 3.7).

Output models use pydantic v2. The run envelope is discriminated on ``found``:
``OutputFound[T]`` carries the data payload, ``OutputNotFound`` carries None.
Wire keys are camelCase; models use ``populate_by_name`` plus per-field aliases
so callers read snake_case attributes while the transport round-trips camelCase.
Data models allow extra keys (``extra="allow"``) so open provider records keep
unknown fields, exposed via ``.model_extra``.
"""

from __future__ import annotations

from typing import Any, Generic, Literal, TypeVar, cast

from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing_extensions import TypedDict

from ._errors import AnyAPIError, ResultNotFoundError
from .discovery_types import (
    CatalogEntry,
    CatalogSearchResult,
    CatalogSearchResults,
    DiscoveryExecution,
    DiscoveryLane,
    DiscoveryLatency,
    DiscoveryPricing,
    DiscoverySource,
    FlatPricingOffer,
    HighlightField,
    LaneHealth,
    LinearPricingOffer,
    PricingOffer,
)

__all__ = [
    "OutputFound",
    "OutputNotFound",
    "Output",
    "RunResult",
    "BareRunResult",
    "unwrap",
    "Balance",
    "AccountProfile",
    "FlatPricingOffer",
    "LinearPricingOffer",
    "PricingOffer",
    "DiscoveryPricing",
    "DiscoveryExecution",
    "DiscoverySource",
    "LaneHealth",
    "DiscoveryLane",
    "DiscoveryLatency",
    "CatalogEntry",
    "HighlightField",
    "CatalogSearchResult",
    "CatalogSearchResults",
    "RequestOptions",
    "AgentSignupResult",
]

T = TypeVar("T")


class OutputFound(BaseModel, Generic[T]):
    """The ``found: true`` branch: the upstream returned a matching entity."""

    found: Literal[True]
    data: T


# Why a call answered ``found: false``. The gateway owns this vocabulary and can
# add a word after a release is published, so ``NotFoundReason`` names the words
# known at release for autocomplete but accepts any string, which arrives exactly
# as the gateway sent it. ``not_found``: the source states the target does not
# exist, or returned nothing for it. ``suspended``: the platform has suspended the
# account. ``unavailable``: the platform did not show this to the source: it may not
# exist, or it may be visible only to signed-in users. ``too_long``: the video is
# too long to transcribe.
NotFoundReason = Literal["not_found", "suspended", "unavailable", "too_long"] | str


class OutputNotFound(BaseModel):
    """The ``found: false`` branch: no matching entity, ``data`` is None.

    ``reason`` says why; it is absent only on a response from a gateway older
    than the field.
    """

    found: Literal[False]
    data: None = None
    reason: NotFoundReason | None = None


# Output[T] is the discriminated union on `found`.
Output = OutputFound[T] | OutputNotFound


_OUTPUT_NOT_RETAINED = (
    "the run output was not retained: this response is an idempotent replay whose "
    "stored payload has expired or was too large to store, so only the run metadata "
    "came back. Re-run the request without the idempotency key (or with a fresh one) "
    "to fetch the data again."
)


def _reject_unretained_output(data: Any) -> Any:
    """Raise the actionable not-retained error before ``output`` is validated.

    The wire sends ``output`` on every success envelope, but an idempotent replay
    can outlive the payload it replays (24h TTL, or a payload over the storage size
    cap), so the body is legally ``{"output": null, ...}``. Neither declared
    ``output`` type admits None, so without this guard pydantic would reject the
    body with a generic ``ValidationError`` that never mentions idempotency, and a
    caller of a generated typed method would never reach :func:`unwrap`.

    Raising a non-``ValueError`` is deliberate: pydantic propagates it unchanged
    rather than folding it into a ``ValidationError``, so the caller sees the same
    :class:`AnyAPIError` (status 200, same message) the TypeScript SDK raises.
    A missing ``output`` key is treated identically, matching SPEC 2.3.
    """
    # Narrow a copy so ``data`` itself keeps its declared type and is returned unchanged
    # (pydantic then validates the original body, guard or no guard).
    incoming: object = data
    if (
        isinstance(incoming, dict)
        and cast("dict[str, object]", incoming).get("output") is None
    ):
        raise AnyAPIError(_OUTPUT_NOT_RETAINED, status=200)
    return data


class RunResult(BaseModel, Generic[T]):
    """The normalized run envelope returned by ``POST /v1/run/{slug}``.

    Extra top-level keys round-trip via ``.model_extra`` (the envelope root is
    open). ``provider`` is always the literal ``"AnyAPI"``; upstream backends
    are never named.

    ``replayed`` is True when the gateway served a stored response for a repeated
    ``Idempotency-Key`` instead of running the SKU again (a replay is not billed
    twice). A replay whose stored payload is no longer retained (a 24h TTL expiry,
    or a payload over the storage size cap) carries the metadata with a null
    ``output``, which :func:`unwrap` rejects. ``result_id`` is an opaque handle to
    the full unshaped result, cached about 15 minutes for a free re-read via
    ``GET /v1/results/{id}``. ``jq_error`` explains why a requested jq reshape did
    not apply; the run was still billed and ``output`` carries the full result.

    ``items`` is REQUIRED: the gateway sends it on every success envelope (its Go
    struct tag carries no ``omitempty``), including a metadata-only replay and the
    free re-read of a cached result.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    output: OutputFound[T] | OutputNotFound = Field(discriminator="found")
    provider: Literal["AnyAPI"]
    cost_usd: float = Field(alias="costUsd")
    items: int
    replayed: bool
    result_id: str | None = Field(default=None, alias="resultId")
    jq_error: str | None = Field(default=None, alias="jqError")
    hint: str | None = None

    @model_validator(mode="before")
    @classmethod
    def _guard_unretained_output(cls, data: Any) -> Any:
        return _reject_unretained_output(data)


class RequestSnapshot(BaseModel, Generic[T]):
    """Stored state for a durable AnyAPI Request."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)
    request_id: str = Field(alias="requestId")
    sku: str
    status: Literal["queued", "running", "succeeded", "failed", "expired"]
    created_at: str = Field(alias="createdAt")
    retry_after_seconds: int | None = Field(default=None, alias="retryAfterSeconds")
    result: RunResult[T] | None = None
    error: dict[str, str] | None = None
    result_expired: bool = Field(default=False, alias="resultExpired")


class BareRunResult(BaseModel, Generic[T]):
    """The conditional envelope for an operation without a found/data wrapper.

    If a future generated operation uses this SPEC 1.2 shape, ``output`` is its
    data payload directly. There is no not-found branch to discriminate, so
    ``unwrap`` returns ``output`` directly unless the payload was not retained.

    ``items``, ``replayed``, ``result_id``, and ``jq_error`` carry the same meaning
    and the same wire presence as on :class:`RunResult`.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    output: T
    provider: Literal["AnyAPI"]
    cost_usd: float = Field(alias="costUsd")
    items: int
    replayed: bool
    result_id: str | None = Field(default=None, alias="resultId")
    jq_error: str | None = Field(default=None, alias="jqError")
    hint: str | None = None

    @model_validator(mode="before")
    @classmethod
    def _guard_unretained_output(cls, data: Any) -> Any:
        return _reject_unretained_output(data)


def unwrap(result: RunResult[T] | BareRunResult[T]) -> T:
    """Return the data payload when found, else raise :class:`ResultNotFoundError`.

    For a found-data ``RunResult`` this narrows ``Output[T]`` to ``T`` and raises
    when ``found`` is false. For a ``BareRunResult`` the output IS the data, so it
    is returned directly.

    Either shape raises :class:`AnyAPIError` when ``output`` is None: an idempotent
    replay can outlive its stored payload, and the caller must never receive None
    typed as ``T``. See SPEC 2.3 / 3.3. Parsing a wire body normally raises that
    same error earlier (``_reject_unretained_output`` runs before field validation),
    so this guard covers models built by ``model_construct`` or by hand.

    Catching ``NotFoundError`` catches both an HTTP 404 and an empty found-data
    result; catch ``ResultNotFoundError`` to handle only empty results.
    """
    # Read through ``object`` so this stays a runtime guard rather than a claim that
    # the declared output type admits None (it does not, in either language).
    payload: object = result.output
    if payload is None:
        raise AnyAPIError(_OUTPUT_NOT_RETAINED, status=200)
    if isinstance(result, BareRunResult):
        return result.output
    output = result.output
    if isinstance(output, OutputFound):
        return output.data
    raise ResultNotFoundError("no matching result was found", status=404)


class Balance(BaseModel):
    """Wallet balance in USD (the server returns ``{usd}`` already in USD)."""

    usd: float


class AccountProfile(BaseModel):
    """Account profile from ``GET /v1/me`` (internal fields dropped)."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    email: str | None = None
    status: str
    created_at: str = Field(alias="createdAt")
    onboarding_complete: bool = Field(alias="onboardingComplete")


class RequestOptions(TypedDict, total=False):
    """Per-call response shaping and transport overrides (SPEC 3.7).

    ``fields``, ``max_items``, and ``summary`` shape the response and do NOT
    change cost. ``timeout`` overrides the client per-request timeout (seconds).
    ``max_retries`` overrides the client retry cap for this call.
    ``max_in_progress_wait`` overrides the client's whole-call budget (seconds)
    for waiting out a 409 ``idempotency_in_progress``; 0 surfaces that 409
    immediately. ``idempotency_key`` overrides the generated key for this billed
    POST.
    """

    fields: list[str]
    max_items: int
    summary: bool
    timeout: float
    max_retries: int
    max_in_progress_wait: float
    idempotency_key: str


class AgentSignupResult(BaseModel):
    """Result of :func:`getanyapi.agent_signup` (SPEC 3.7)."""

    model_config = ConfigDict(populate_by_name=True)

    secret: str
    cap_usd: float = Field(alias="capUsd")


# Convenience aliases used by the transport for untyped generic runs.
AnyRunResult = RunResult[Any]
AnyBareRunResult = BareRunResult[Any]
