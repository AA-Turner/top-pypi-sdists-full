"""Strict async transport for TypeSafe's System One API.

This adapter intentionally owns only TypeSafe's native decision wire contract.
The catalog-aware dispatcher resolves the offering and supplies its provider
model id/base URL; it must not route this through a chat translator.
"""

from __future__ import annotations

import asyncio
import math
from collections.abc import Awaitable, Callable, Mapping
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from typing import Annotated, Any, Literal, Protocol

import httpx
from matrx_utils.http_client import shared_client
from pydantic import BaseModel, ConfigDict, Field, JsonValue, StrictStr, model_validator

from matrx_ai.config.usage_config import TokenUsage
from matrx_ai.providers.errors import (
    attach_billed_usage,
    classify_billing_refusal,
    mark_billing_checked,
)
from matrx_ai.providers.keys import ApiKeyNotFoundError, resolve_api_key
from matrx_ai.providers.snapshot import capture_request_payload

DEFAULT_BASE_URL = "https://api.typesafe.ai"
SYSTEM_ONE_PATH = "/v1/systemone"
_ROUNDING_UNIT = 0.01  # TypeSafe reports probabilities to two decimals
DEFAULT_TIMEOUT_SECONDS = 30.0
DEFAULT_MAX_RETRIES = 2
# Vendor limits (docs.typesafe.ai/api, 2026-09-20): a Choice takes at most 255
# options and a Score at most 10 levels.  Refuse locally with the remedy rather
# than paying a round trip for a 422 whose body we deliberately do not surface.
MAX_CHOICE_OPTIONS = 255
MAX_SCORE_LEVELS = 10
# Images and Box questions (docs.typesafe.ai/images.md, 2026-10-30). TypeSafe
# calls them "Dreamer-ready": every request that carries an asset or a Box
# question must opt in with this header or it is refused with a 400.
IMAGES_HEADER = "TypeSafe-Danger-Zone-Images"
# Image limits, both ends inclusive. TypeSafe REJECTS an image outside them and
# never resizes, so the decisions layer fits every image before it gets here
# (``matrx_ai.decisions.images``); these are the adapter's last word.
MIN_IMAGE_SIDE = 280
MAX_IMAGE_SIDE = 1568
MAX_IMAGE_BYTES = 16 * 1024 * 1024
MAX_REQUEST_BYTES = 32 * 1024 * 1024
MAX_REFERENCE_BYTES = 1024
MAX_TOTAL_REFERENCE_BYTES = 65536

type SystemOneState = StrictStr | dict[str, JsonValue] | list[JsonValue]
type SystemOneEntry = StrictStr | dict[str, JsonValue] | list[JsonValue] | None


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)


class NoulQuestion(_StrictModel):
    type: Literal["noul"] = "noul"
    instructions: SystemOneEntry
    criteria: dict[Literal["true", "false"], SystemOneEntry] | None = None


class ChoiceQuestion(_StrictModel):
    type: Literal["choice"] = "choice"
    instructions: SystemOneEntry
    criteria: dict[StrictStr, SystemOneEntry] = Field(min_length=2, max_length=MAX_CHOICE_OPTIONS)

    @model_validator(mode="after")
    def _unique_nonblank_choices(self) -> ChoiceQuestion:
        if any(not key.strip() for key in self.criteria):
            raise ValueError("Choice criteria keys must be non-empty")
        return self


class ScoreQuestion(_StrictModel):
    type: Literal["score"] = "score"
    instructions: SystemOneEntry
    criteria: list[SystemOneEntry] = Field(min_length=2, max_length=MAX_SCORE_LEVELS)


class BoxQuestion(_StrictModel):
    """Where is something in an image — answered with four edges (Jev 1.14+).

    Takes no criteria. It always answers with a box, even for a target that is
    not there, so the decisions layer pairs it with a presence ``noul``.
    """

    type: Literal["box"] = "box"
    instructions: SystemOneEntry


type Question = Annotated[
    NoulQuestion | ChoiceQuestion | ScoreQuestion | BoxQuestion,
    Field(discriminator="type"),
]


class ImageAsset(_StrictModel):
    """One image, sent base64 in the JSON body and placed by its reference string."""

    type: Literal["image"] = "image"
    format: Literal["png", "jpg", "jpeg"]
    #: Standard base64 alphabet with padding, no whitespace, no ``data:`` prefix.
    data_base64: StrictStr = Field(min_length=4, pattern=r"^[A-Za-z0-9+/]+={0,2}$")


def _strings_in(value: Any) -> list[str]:
    """Every string VALUE in a state/instructions/criteria entry (keys excluded,
    exactly as TypeSafe matches references)."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [text for item in value.values() for text in _strings_in(item)]
    if isinstance(value, list):
        return [text for item in value for text in _strings_in(item)]
    return []


class SystemOneRequest(_StrictModel):
    state: SystemOneState
    model: StrictStr = Field(min_length=1)
    questions: dict[StrictStr, Question] = Field(min_length=1)
    #: Images keyed by an opaque reference written wherever the image belongs.
    assets: dict[StrictStr, ImageAsset] | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def _question_ids_are_nonblank(self) -> SystemOneRequest:
        if any(not question_id.strip() for question_id in self.questions):
            raise ValueError("System One question ids must be non-empty")
        return self

    @model_validator(mode="after")
    def _assets_are_placed(self) -> SystemOneRequest:
        """Refuse locally what TypeSafe would refuse with an opaque 400 or 413."""
        has_box = any(isinstance(question, BoxQuestion) for question in self.questions.values())
        if not self.assets:
            if has_box:
                raise ValueError("A Box question needs an image in the request; none was attached.")
            return self
        texts = _strings_in(self.state)
        for question in self.questions.values():
            texts.extend(_strings_in(question.instructions))
            texts.extend(_strings_in(getattr(question, "criteria", None)))
        total = 0
        for reference in self.assets:
            size = len(reference.encode("utf-8"))
            total += size
            if not reference.strip() or size > MAX_REFERENCE_BYTES:
                raise ValueError(
                    f"Image reference {reference[:40]!r} must be non-blank and at most "
                    f"{MAX_REFERENCE_BYTES} bytes."
                )
            if not any(reference in text for text in texts):
                raise ValueError(
                    f"Image {reference!r} is attached but never referenced in the state, "
                    "instructions or criteria; TypeSafe refuses an unplaced image."
                )
        if total > MAX_TOTAL_REFERENCE_BYTES:
            raise ValueError(
                f"Image references total {total} bytes; TypeSafe allows {MAX_TOTAL_REFERENCE_BYTES}."
            )
        return self

    @property
    def uses_images(self) -> bool:
        """True when the request must carry the images opt-in header."""
        return bool(self.assets) or any(
            isinstance(question, BoxQuestion) for question in self.questions.values()
        )


class NoulAnswer(_StrictModel):
    type: Literal["noul"] = "noul"
    noul: float = Field(ge=0.0, le=1.0)


class ChoiceAnswer(_StrictModel):
    type: Literal["choice"] = "choice"
    choice: StrictStr = Field(min_length=1)
    probabilities: dict[StrictStr, float] = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)


class ScoreAnswer(_StrictModel):
    type: Literal["score"] = "score"
    score: float
    probabilities: dict[StrictStr, float] = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)
    legend: dict[StrictStr, JsonValue] = Field(min_length=1)


class BoxCoordinates(_StrictModel):
    """Edges as fractions of the image: top/bottom of height, left/right of width."""

    top: float = Field(ge=0.0, le=1.0)
    bottom: float = Field(ge=0.0, le=1.0)
    left: float = Field(ge=0.0, le=1.0)
    right: float = Field(ge=0.0, le=1.0)


class BoxAnswer(_StrictModel):
    type: Literal["box"] = "box"
    box: BoxCoordinates
    #: Null when the model gives no confidence — never read as zero.
    confidence: float | None = Field(ge=0.0, le=1.0)


type Answer = Annotated[
    NoulAnswer | ChoiceAnswer | ScoreAnswer | BoxAnswer,
    Field(discriminator="type"),
]


class TypeSafeUsage(_StrictModel):
    input_tokens: int = Field(ge=0, strict=True)
    output_tokens: int = Field(ge=0, strict=True)


class SystemOneResult(_StrictModel):
    model: StrictStr = Field(min_length=1)
    answers: dict[StrictStr, Answer]
    usage: TypeSafeUsage
    request_id: StrictStr | None = None


class TypeSafeProviderError(RuntimeError):
    """Safe, classified TypeSafe failure for the generic decision dispatcher."""

    def __init__(
        self,
        *,
        error_type: str,
        message: str,
        status_code: int | None = None,
        retry_after: float | None = None,
        is_retryable: bool = False,
    ) -> None:
        super().__init__(message)
        self.error_type = error_type
        self.status_code = status_code
        self.retry_after = retry_after
        self.is_retryable = is_retryable


class _PostClient(Protocol):
    async def post(
        self,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ) -> httpx.Response: ...


def _retry_after(headers: Mapping[str, str], *, now: datetime | None = None) -> float | None:
    """Parse standard Retry-After delta seconds or an HTTP date without guessing."""
    raw = headers.get("retry-after")
    if raw is None:
        return None
    try:
        delay = float(raw)
    except (TypeError, ValueError):
        try:
            target = parsedate_to_datetime(raw)
        except (TypeError, ValueError, IndexError):
            return None
        if target.tzinfo is None:
            target = target.replace(tzinfo=UTC)
        delay = (target - (now or datetime.now(tz=UTC))).total_seconds()
    if not math.isfinite(delay):
        return None
    return max(0.0, delay)


def _billing_refusal(response: httpx.Response) -> TypeSafeProviderError | None:
    """The platform's TypeSafe account cannot pay — decided by the SHARED classifier.

    Checked before the status branches: an out-of-credit refusal arriving as a
    429 must never be retried as a rate limit. The provider's text rides only on
    ``error_info`` (operator-facing); the exception message stays safe.
    """
    probe = TypeSafeProviderError(
        error_type="provider_error",
        message=f"TypeSafe returned HTTP {response.status_code}.",
        status_code=response.status_code,
    )
    probe.body = response.text[:2000]  # type: ignore[attr-defined]
    info = classify_billing_refusal(probe, "typesafe")
    if info is None:
        return None
    error = TypeSafeProviderError(
        error_type="billing_error",
        message=info.user_message,
        status_code=response.status_code,
        is_retryable=False,
    )
    error.error_info = info  # type: ignore[attr-defined]
    return error


def _safe_http_error(response: httpx.Response) -> TypeSafeProviderError:
    status = response.status_code
    billing = _billing_refusal(response)
    if billing is not None:
        return billing
    retry_after = _retry_after(response.headers)
    if status in {401, 403}:
        return TypeSafeProviderError(
            error_type="auth_error",
            message="TypeSafe rejected the API credential.",
            status_code=status,
        )
    if status == 413:
        return TypeSafeProviderError(
            error_type="request_too_large",
            message=(
                "TypeSafe refused the request as too large: an image, all images together, "
                "or the expanded request is over its 32 MiB limit. Send fewer or smaller images."
            ),
            status_code=status,
        )
    if status == 422:
        return TypeSafeProviderError(
            error_type="invalid_request",
            message="TypeSafe rejected the System One request.",
            status_code=status,
        )
    if status in {429, 529}:
        return TypeSafeProviderError(
            error_type="rate_limit" if status == 429 else "provider_overloaded",
            message="TypeSafe is temporarily unavailable.",
            status_code=status,
            retry_after=retry_after,
            is_retryable=True,
        )
    if status >= 500:
        return TypeSafeProviderError(
            error_type="server_error",
            message="TypeSafe returned a server error.",
            status_code=status,
            retry_after=retry_after,
            is_retryable=True,
        )
    return TypeSafeProviderError(
        error_type="provider_error",
        message=f"TypeSafe returned HTTP {status}.",
        status_code=status,
    )


def _rejected_image_error(
    request: SystemOneRequest, response: httpx.Response
) -> TypeSafeProviderError | None:
    """A 400 on a request with images names the images, not a generic refusal.

    The adapter already checked placement and references, and the decisions
    layer fitted every image to the limits, so what is left is the vendor's own
    decode: a damaged file, an animated PNG, or images not yet enabled on the
    account. The provider body stays off the exception, as for every refusal.
    """
    if response.status_code != 400 or not request.uses_images:
        return None
    return TypeSafeProviderError(
        error_type="image_rejected",
        message=(
            "TypeSafe rejected an image in this decision request (an undecodable or animated "
            "file, or images not enabled for the account). Re-export the image as PNG or JPEG."
        ),
        status_code=400,
    )


def _unsupported_null_entry_error(
    request: SystemOneRequest, response: httpx.Response
) -> TypeSafeProviderError | None:
    """Name observed provider limits without changing the caller's data.

    The Advanced docs describe null as an EntryType, but native probes on
    2026-09-19 show that System One currently rejects a null instruction (400)
    and a null Score criterion (422). Keep the public typed contract intact:
    callers receive their truthful provider refusal and must choose an explicit
    non-null semantic value; this adapter must never stringify null silently.
    """
    if response.status_code not in {400, 422}:
        return None
    if any(question.instructions is None for question in request.questions.values()):
        return TypeSafeProviderError(
            error_type="unsupported_entry_type",
            message=(
                "TypeSafe currently rejects null instructions. Supply an explicit string, object, "
                "or array instruction; the adapter will not stringify null."
            ),
            status_code=response.status_code,
        )
    if any(
        isinstance(question, ScoreQuestion) and any(entry is None for entry in question.criteria)
        for question in request.questions.values()
    ):
        return TypeSafeProviderError(
            error_type="unsupported_entry_type",
            message=(
                "TypeSafe currently rejects null Score criteria. Supply an explicit string, object, "
                "or array criterion; the adapter will not stringify null."
            ),
            status_code=response.status_code,
        )
    return None


def _request_id_from_headers(headers: Mapping[str, str]) -> str | None:
    """Use TypeSafe's request-id header when a successful body omits it."""
    for name in ("x-typesafe-request-id", "x-request-id", "request-id"):
        value = headers.get(name)
        if value:
            return value
    return None


def _validate_probability_map(probabilities: Mapping[str, float], *, label: str) -> None:
    if not probabilities:
        raise TypeSafeProviderError(error_type="invalid_response", message=f"TypeSafe returned {label} without probabilities.")
    values = tuple(probabilities.values())
    if any(not math.isfinite(value) or value < 0.0 or value > 1.0 for value in values):
        raise TypeSafeProviderError(error_type="invalid_response", message=f"TypeSafe returned invalid {label} probabilities.")
    # TypeSafe reports each probability to two decimals, so n options may sum to
    # 1 ± n·0.005 (13 options came back 0.99 on 5 of 12 identical calls, 2026-10-16).
    # Rounding is an answer; anything further off is a malformed distribution.
    if not math.isclose(sum(values), 1.0, rel_tol=0.0, abs_tol=_ROUNDING_UNIT / 2 * len(values) + 1e-9):
        raise TypeSafeProviderError(error_type="invalid_response", message=f"TypeSafe returned {label} probabilities that do not sum to one.")


def _validate_result(request: SystemOneRequest, result: SystemOneResult) -> None:
    expected_ids = set(request.questions)
    actual_ids = set(result.answers)
    if actual_ids != expected_ids:
        raise TypeSafeProviderError(
            error_type="invalid_response",
            message="TypeSafe returned answers that do not match the requested question ids.",
        )
    for question_id, question in request.questions.items():
        answer = result.answers[question_id]
        if answer.type != question.type:
            raise TypeSafeProviderError(
                error_type="invalid_response",
                message=f"TypeSafe returned the wrong answer type for question {question_id!r}.",
            )
        if isinstance(question, ChoiceQuestion) and isinstance(answer, ChoiceAnswer):
            expected_choices = set(question.criteria)
            if answer.choice not in expected_choices or set(answer.probabilities) != expected_choices:
                raise TypeSafeProviderError(
                    error_type="invalid_response",
                    message=f"TypeSafe returned choices outside the requested criteria for question {question_id!r}.",
                )
            _validate_probability_map(answer.probabilities, label="Choice")
        if isinstance(question, ScoreQuestion) and isinstance(answer, ScoreAnswer):
            if not math.isfinite(answer.score) or not 0.0 <= answer.score <= len(question.criteria) - 1:
                raise TypeSafeProviderError(
                    error_type="invalid_response",
                    message=f"TypeSafe returned an out-of-range Score for question {question_id!r}.",
                )
            if set(answer.legend) != set(answer.probabilities) or len(answer.probabilities) != len(question.criteria):
                raise TypeSafeProviderError(
                    error_type="invalid_response",
                    message="TypeSafe returned a Score distribution that does not match its legend.",
                )
            _validate_probability_map(answer.probabilities, label="Score")
        if isinstance(question, BoxQuestion) and isinstance(answer, BoxAnswer):
            edges = answer.box
            if not (edges.left < edges.right and edges.top < edges.bottom):
                raise TypeSafeProviderError(
                    error_type="invalid_response",
                    message=f"TypeSafe returned a Box with crossed edges for question {question_id!r}.",
                )


def _usage_from_raw_response(payload: Any, *, model: str) -> TokenUsage | None:
    """Recover billed tokens before refusing a malformed post-inference body."""
    if not isinstance(payload, dict):
        return None
    raw = payload.get("usage")
    if not isinstance(raw, dict):
        return None
    counters = {key: value for key in ("input_tokens", "output_tokens")
                if type(value := raw.get(key)) is int and value >= 0}
    if not counters:
        return None
    return TokenUsage(
        input_tokens=counters.get("input_tokens", 0),
        output_tokens=counters.get("output_tokens", 0),
        matrx_model_name=model,
        provider_model_name=str(payload.get("model") or model),
        api="typesafe",
        response_id=str(payload.get("request_id") or ""),
        raw_usage=counters,
    )


async def call_system_one(
    request: SystemOneRequest,
    *,
    api_key: str | None = None,
    base_url: str = DEFAULT_BASE_URL,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    max_retries: int = DEFAULT_MAX_RETRIES,
    http: _PostClient | None = None,
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
) -> SystemOneResult:
    """Execute a strictly typed System One request.

    ``api_key`` is an optional already-resolved catalog credential.  When it is
    omitted, canonical ``resolve_api_key`` resolution is used.  The injected
    client exists only for deterministic transport tests; production callers
    normally let this function own and close its httpx client.
    """
    if not base_url.startswith("https://"):
        raise ValueError("TypeSafe base_url must use https")
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")
    if max_retries < 0:
        raise ValueError("max_retries must be non-negative")
    key = api_key or resolve_api_key("TYPESAFE_API_KEY")
    if not key:
        raise ApiKeyNotFoundError("No API key found for TYPESAFE_API_KEY.")
    url = base_url.rstrip("/") + SYSTEM_ONE_PATH
    payload = request.model_dump(mode="json")
    if payload.get("assets") is None:
        payload.pop("assets", None)
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    if request.uses_images:
        headers[IMAGES_HEADER] = "true"
    # The exact JSON body that goes on the wire, stashed for chat.request_snapshot
    # (the same seam every chat provider uses). Without it the snapshot row was
    # written with request_payload = {} for every TypeSafe decision call.
    capture_request_payload(payload, provider="typesafe")
    owns_client = http is None
    client = http or shared_client(timeout=timeout_seconds, follow_redirects=False)
    try:
        for attempt in range(max_retries + 1):
            try:
                response = await client.post(url, headers=headers, json=payload)
            except httpx.TimeoutException as exc:
                error = TypeSafeProviderError(
                    error_type="timeout", message="TypeSafe request timed out.", is_retryable=True
                )
                mark_billing_checked(error)
                if attempt >= max_retries:
                    raise error from exc
                await sleep(min(2**attempt, 30.0))
                continue
            except httpx.HTTPError as exc:
                error = TypeSafeProviderError(
                    error_type="connection_error", message="TypeSafe connection failed.", is_retryable=True
                )
                mark_billing_checked(error)
                if attempt >= max_retries:
                    raise error from exc
                await sleep(min(2**attempt, 30.0))
                continue
            if response.status_code < 200 or response.status_code >= 300:
                error = (
                    _unsupported_null_entry_error(request, response)
                    or _rejected_image_error(request, response)
                    or _safe_http_error(response)
                )
                mark_billing_checked(error)
                if error.is_retryable and attempt < max_retries:
                    await sleep(error.retry_after if error.retry_after is not None else min(2**attempt, 30.0))
                    continue
                raise error
            raw_response: Any = None
            try:
                raw_response = response.json()
                parsed = SystemOneResult.model_validate(raw_response)
            except (ValueError, TypeError) as exc:
                error = TypeSafeProviderError(
                    error_type="invalid_response", message="TypeSafe returned an invalid System One response."
                )
                attach_billed_usage(error, _usage_from_raw_response(raw_response, model=request.model))
                raise error from exc
            if parsed.request_id is None:
                request_id = _request_id_from_headers(response.headers)
                if request_id is not None:
                    parsed = parsed.model_copy(update={"request_id": request_id})
            try:
                _validate_result(request, parsed)
            except TypeSafeProviderError as error:
                attach_billed_usage(error, _usage_from_raw_response(raw_response, model=request.model))
                raise
            return parsed
    finally:
        if owns_client:
            await client.aclose()  # type: ignore[union-attr]
    raise AssertionError("System One retry loop exited unexpectedly")
