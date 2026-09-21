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
from pydantic import BaseModel, ConfigDict, Field, JsonValue, StrictStr, model_validator

from matrx_ai.config.usage_config import TokenUsage
from matrx_ai.providers.errors import attach_billed_usage, mark_billing_checked
from matrx_ai.providers.keys import ApiKeyNotFoundError, resolve_api_key

DEFAULT_BASE_URL = "https://api.typesafe.ai"
SYSTEM_ONE_PATH = "/v1/systemone"
DEFAULT_TIMEOUT_SECONDS = 30.0
DEFAULT_MAX_RETRIES = 2
# Vendor limits (docs.typesafe.ai/api, 2026-09-20): a Choice takes at most 255
# options and a Score at most 10 levels.  Refuse locally with the remedy rather
# than paying a round trip for a 422 whose body we deliberately do not surface.
MAX_CHOICE_OPTIONS = 255
MAX_SCORE_LEVELS = 10

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


type Question = Annotated[
    NoulQuestion | ChoiceQuestion | ScoreQuestion,
    Field(discriminator="type"),
]


class SystemOneRequest(_StrictModel):
    state: SystemOneState
    model: StrictStr = Field(min_length=1)
    questions: dict[StrictStr, Question] = Field(min_length=1)

    @model_validator(mode="after")
    def _question_ids_are_nonblank(self) -> SystemOneRequest:
        if any(not question_id.strip() for question_id in self.questions):
            raise ValueError("System One question ids must be non-empty")
        return self


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


type Answer = Annotated[
    NoulAnswer | ChoiceAnswer | ScoreAnswer,
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


def _safe_http_error(response: httpx.Response) -> TypeSafeProviderError:
    status = response.status_code
    retry_after = _retry_after(response.headers)
    if status in {401, 403}:
        return TypeSafeProviderError(
            error_type="auth_error",
            message="TypeSafe rejected the API credential.",
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
    if not math.isclose(sum(values), 1.0, rel_tol=0.0, abs_tol=1e-5):
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
    owns_client = http is None
    client = http or httpx.AsyncClient(timeout=timeout_seconds, follow_redirects=False)
    try:
        for attempt in range(max_retries + 1):
            try:
                response = await client.post(
                    url,
                    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                    json=payload,
                )
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
                error = _unsupported_null_entry_error(request, response) or _safe_http_error(response)
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
