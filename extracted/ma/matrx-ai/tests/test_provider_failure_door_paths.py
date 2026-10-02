"""Every paid non-chat provider path takes the SAME failure pipe as chat.

SUT, per path, at its real entry point: ``execute_stt`` (→ ``GroqSTT``),
``GoogleEmbeddingRuntime.embed``, ``execute_decision`` (→ the real TypeSafe
``call_system_one`` retry loop), ``FastinoExtraction.extract`` (→ the real
``_post`` retry loop over an ``httpx.MockTransport``), ``CohereReranker.rerank``.
Doubles: the provider wire (SDK client / HTTP transport, raising the provider's
real error type), ``capture_error`` (the system_error writer) and ``sleep``.

Breaks named:
* the path dispatches outside ``UnifiedAIClient._dispatch_with_billing_net`` →
  an exhausted provider account files NO ``provider_account_out_of_credit`` row
  (the census of 2026-10-01: STT, embeddings, decisions, Fastino, rerank);
* a path's own retry loop retries a billing refusal (a 429 carrying
  out-of-credit wording) → the refusal is paid for N times and the operator
  learns nothing;
* the adapter never runs billing capture → the seam's LAYER 2 files a false
  ``provider_billing_capture_missing`` on every transient 5xx;
* a transient failure is filed as out-of-credit, or stops being retried.
"""

from __future__ import annotations

from typing import Any

import cohere
import groq
import httpx
import pytest
from cohere.core.api_error import ApiError
from google.genai.errors import ClientError, ServerError

import matrx_ai.providers.fastino.fastino_api as fastino_api
from matrx_ai.providers.failure_report import classify_for_report
from matrx_ai.testing.profile_factory import make_profile

_OUT_OF_CREDIT = "provider_account_out_of_credit"  # literal: the error surfaces collapse by it
_CAPTURE_MISSING = "provider_billing_capture_missing"


@pytest.fixture
def captured(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    async def capture_error(exc: BaseException, **kwargs: Any) -> None:
        rows.append({"exc": exc, **kwargs})

    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", capture_error)

    async def _no_wait(_seconds: float) -> None:
        return None

    # The dispatch seam's transient retry (STT, Gemini embeddings) waits between
    # sends; these tests judge the report, not the wait.
    monkeypatch.setattr("matrx_ai.providers.unified_client._transient_retry_sleep", _no_wait)
    return rows


def _kinds(rows: list[dict[str, Any]]) -> list[str]:
    return [row["kind"] for row in rows]


def _assert_one_billing_alarm(rows: list[dict[str, Any]], raised: BaseException, provider: str) -> None:
    assert _kinds(rows) == [_OUT_OF_CREDIT], f"expected exactly one out-of-credit row, got {_kinds(rows)}"
    assert rows[0]["exc"] is raised
    assert rows[0]["error_type"] == f"{provider}.billing_error"
    info = classify_for_report(raised, provider)
    assert info is not None and info.error_type == "billing_error" and info.is_retryable is False


# ---------------------------------------------------------------------------
# 1. STT — execute_stt → GroqSTT
# ---------------------------------------------------------------------------

_GROQ_REQ = httpx.Request("POST", "https://api.groq.com/openai/v1/audio/transcriptions")


def _groq_error(status: int, message: str, error_type: str) -> groq.APIStatusError:
    body = {"error": {"message": message, "type": error_type}}
    return groq.APIStatusError(
        f"Error code: {status} - {body}",
        response=httpx.Response(status, request=_GROQ_REQ, json=body),
        body=body,
    )


def _wire_groq(monkeypatch: pytest.MonkeyPatch, exc: BaseException) -> list[dict[str, Any]]:
    import matrx_ai.catalog.resolve as resolve_module
    import matrx_ai.providers.groq.stt as groq_stt

    calls: list[dict[str, Any]] = []

    class _Transcriptions:
        async def create(self, **kwargs: Any) -> Any:
            calls.append(kwargs)
            raise exc

    class _Client:
        class audio:  # noqa: N801 — mirrors the SDK attribute
            transcriptions = _Transcriptions()
            translations = _Transcriptions()

    profile = make_profile(
        model_name="whisper-large-v3-turbo",
        provider_model_id="whisper-large-v3-turbo",
        wire_format="groq_stt",
        vendor="groq",
        rules={"language": {}, "response_format": {}, "timestamp_granularities": {}},
    ).model_copy(update={"client_attr": "stt", "offering_metadata": {"stt": {"max_file_size_mb": 25}}})

    async def _resolve(*_args: Any, **_kwargs: Any) -> Any:
        return profile

    monkeypatch.setattr(resolve_module, "resolve_call_profile", _resolve)
    # Patch the wire where the adapter execute_stt will ACTUALLY dispatch to
    # reads it: another test may have re-imported the module, leaving the
    # process-wide client cache holding a class from the earlier module object.
    from matrx_ai.providers.unified_client import UnifiedAIClient

    adapter = getattr(UnifiedAIClient(), "groq_stt")
    monkeypatch.setitem(type(adapter).execute.__globals__, "_client", lambda: _Client())
    monkeypatch.setattr(groq_stt, "_client", lambda: _Client())
    return calls


def _stt_request() -> Any:
    from matrx_ai.processing.audio.stt import STTRequest

    # A short voice memo from a dental practice's after-hours line, as the
    # transcription funnel sends it (container named by its data-URI type).
    return STTRequest(
        audio_source=b"RIFF....WAVEfmt voice-memo",
        model="whisper-large-v3-turbo",
        language="en",
        response_format="verbose_json",
        timestamp_granularities=["segment"],
    )


@pytest.mark.asyncio
async def test_stt_on_an_exhausted_groq_account_files_one_out_of_credit_alarm(monkeypatch, captured) -> None:
    from matrx_ai.processing.audio.stt import execute_stt

    exc = _groq_error(
        402, "Your organization has insufficient balance. Please add funds to continue.", "insufficient_balance"
    )
    calls = _wire_groq(monkeypatch, exc)
    with pytest.raises(groq.APIStatusError) as raised:
        await execute_stt(_stt_request())
    assert raised.value is exc
    assert len(calls) == 1
    _assert_one_billing_alarm(captured, exc, "groq")


@pytest.mark.asyncio
async def test_stt_transient_groq_503_is_not_filed_and_raises_untouched(monkeypatch, captured) -> None:
    from matrx_ai.processing.audio.stt import execute_stt

    exc = _groq_error(503, "Service Unavailable", "service_unavailable")
    _wire_groq(monkeypatch, exc)
    with pytest.raises(groq.APIStatusError) as raised:
        await execute_stt(_stt_request())
    assert raised.value is exc
    # No out-of-credit row, and no false LAYER-2 "billing capture missing":
    # the Groq adapter inspected billing (a failed transcription bills nothing).
    assert _kinds(captured) == []
    info = classify_for_report(exc, "groq")
    assert info is not None and info.is_retryable is True


# ---------------------------------------------------------------------------
# 2. Google embeddings — GoogleEmbeddingRuntime.embed
# ---------------------------------------------------------------------------


def _wire_google(monkeypatch: pytest.MonkeyPatch, exc: BaseException) -> list[dict[str, Any]]:
    import matrx_ai.providers.google.specialized as specialized

    calls: list[dict[str, Any]] = []

    class _Models:
        async def embed_content(self, **kwargs: Any) -> Any:
            calls.append(kwargs)
            raise exc

    class _Client:
        class aio:  # noqa: N801 — mirrors the SDK attribute
            models = _Models()

    monkeypatch.setattr(specialized, "get_google_client", lambda: _Client())
    return calls


def _embedding_runtime() -> Any:
    from matrx_ai.providers.google import GoogleEmbeddingRuntime

    return GoogleEmbeddingRuntime(
        make_profile(
            model_name="gemini-embedding-2",
            provider_model_id="gemini-embedding-2",
            wire_format="google_embeddings",
            vendor="google",
        )
    )


_PROPERTY_MANAGER_CHUNKS = [
    "Unit 4B reports a slow drain in the kitchen sink; tenant available weekdays after 3pm.",
    "Annual HVAC inspection for 1180 Harbor View completed; filter replaced, no faults found.",
]


@pytest.mark.asyncio
async def test_google_embedding_on_depleted_prepay_files_one_out_of_credit_alarm(monkeypatch, captured) -> None:
    exc = ClientError(
        429,
        {"error": {"code": 429, "status": "RESOURCE_EXHAUSTED",
                   "message": "Your prepayment credits are depleted. Please go to AI Studio to manage your project and billing."}},
    )
    calls = _wire_google(monkeypatch, exc)
    with pytest.raises(ClientError) as raised:
        await _embedding_runtime().embed(_PROPERTY_MANAGER_CHUNKS, output_dimensionality=1536)
    assert raised.value is exc
    assert len(calls) == 1
    _assert_one_billing_alarm(captured, exc, "google")


@pytest.mark.asyncio
async def test_google_embedding_transient_503_is_not_filed(monkeypatch, captured) -> None:
    exc = ServerError(503, {"error": {"code": 503, "status": "UNAVAILABLE", "message": "The model is overloaded."}})
    _wire_google(monkeypatch, exc)
    with pytest.raises(ServerError) as raised:
        await _embedding_runtime().embed(_PROPERTY_MANAGER_CHUNKS, output_dimensionality=1536)
    assert raised.value is exc
    assert _kinds(captured) == []


# ---------------------------------------------------------------------------
# 3. Decisions — execute_decision → TypeSafe call_system_one
# ---------------------------------------------------------------------------


class _SequencedHttp:
    """The TypeSafe wire: hands back the scripted responses in order, counts POSTs."""

    def __init__(self, *responses: httpx.Response) -> None:
        self._responses = list(responses)
        self.posts = 0

    async def post(self, url: str, **_kwargs: Any) -> httpx.Response:
        self.posts += 1
        response = self._responses[min(self.posts, len(self._responses)) - 1]
        response.request = httpx.Request("POST", url)
        return response


def _decision_profile() -> Any:
    from types import SimpleNamespace

    return SimpleNamespace(
        wire_format="typesafe_systemone",
        capabilities=SimpleNamespace(interaction="decision"),
        byok_secret_key=None,
        provider_model_id="jev-1.13.0",
        base_url="https://api.typesafe.ai",
        model_name="jev-1.13.0",
        vendor="typesafe",
        offering_id="typesafe-jev-offering",
        resolution_route="pinned",
        endpoint_id="typesafe-endpoint",
        offering_metadata={},
    )


async def _run_decision(monkeypatch: pytest.MonkeyPatch, http: _SequencedHttp, sleeps: list[float]) -> BaseException:
    from matrx_ai.decisions import DecisionRequest, execute_decision, runner
    from matrx_ai.providers.typesafe import call_system_one

    async def _priced() -> dict[str, Any]:
        return {"typesafe-jev-offering": object()}

    async def _sleep(seconds: float) -> None:
        sleeps.append(seconds)

    monkeypatch.setattr(runner, "ensure_pricing_lookup", _priced)

    async def caller(request: Any, **kwargs: Any) -> Any:
        return await call_system_one(
            request, api_key="ts-test-key", base_url=kwargs["base_url"], http=http, sleep=_sleep
        )

    with pytest.raises(Exception) as raised:  # noqa: PT011 — the type is asserted by the caller
        await execute_decision(
            DecisionRequest(
                model="jev-1.13.0",
                state={"claim": "Water damage to the kitchen subfloor at 1180 Harbor View, Unit 4B"},
                questions={"covered": {"type": "noul", "instructions": "Is this covered by the landlord policy?"}},
            ),
            profile=_decision_profile(),
            caller=caller,
        )
    return raised.value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response",
    [
        pytest.param(httpx.Response(402, json={"detail": "Payment required: insufficient credits on this account."}), id="402"),
        pytest.param(httpx.Response(429, json={"detail": "Insufficient credits remaining on this account."}), id="429-billing"),
    ],
)
async def test_decision_on_an_exhausted_typesafe_account_alarms_once_and_never_retries(
    monkeypatch, captured, response
) -> None:
    http = _SequencedHttp(response)
    sleeps: list[float] = []
    raised = await _run_decision(monkeypatch, http, sleeps)
    assert http.posts == 1, f"a billing refusal was retried ({http.posts} POSTs)"
    assert sleeps == []
    assert getattr(raised, "is_retryable", None) is False
    _assert_one_billing_alarm(captured, raised, "typesafe")


@pytest.mark.asyncio
async def test_decision_transient_rate_limit_keeps_its_retries(monkeypatch, captured) -> None:
    http = _SequencedHttp(httpx.Response(429, json={"detail": "Too many requests."}, headers={"retry-after": "2"}))
    sleeps: list[float] = []
    raised = await _run_decision(monkeypatch, http, sleeps)
    assert http.posts == 3  # DEFAULT_MAX_RETRIES = 2 → 1 + 2 retries
    assert sleeps == [2.0, 2.0]
    assert getattr(raised, "error_type", None) == "rate_limit"
    assert _OUT_OF_CREDIT not in _kinds(captured)


# ---------------------------------------------------------------------------
# 4. Fastino — FastinoExtraction.extract → _post retry loop
# ---------------------------------------------------------------------------


@pytest.fixture
def fastino_wire(monkeypatch: pytest.MonkeyPatch) -> list[float]:
    monkeypatch.setattr(fastino_api, "_permanent_refusal", None, raising=False)
    monkeypatch.setenv("PIONEER_API_KEY", "pioneer-test-key")
    sleeps: list[float] = []

    async def _sleep(seconds: float) -> None:
        sleeps.append(seconds)

    async def _slot() -> None:
        return None

    monkeypatch.setattr(fastino_api.asyncio, "sleep", _sleep)
    monkeypatch.setattr(fastino_api, "acquire_fastino_slot", _slot)
    return sleeps


async def _extract_with(response: httpx.Response) -> tuple[int, BaseException]:
    posts = 0

    def _handle(request: httpx.Request) -> httpx.Response:
        nonlocal posts
        posts += 1
        return httpx.Response(response.status_code, content=response.content, headers=response.headers)

    async with httpx.AsyncClient(transport=httpx.MockTransport(_handle)) as client:
        with pytest.raises(fastino_api.FastinoError) as raised:
            await fastino_api.FastinoExtraction(client).extract(
                "Harbor Dental's new-patient form lists Dr. Lena Ortiz and an insurer, Delta Dental.",
                ["person", "organization"],
            )
    return posts, raised.value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response",
    [
        pytest.param(httpx.Response(402, json={"detail": "Insufficient credits. Top up your Pioneer account."}), id="402"),
        pytest.param(
            httpx.Response(429, json={"error": {"message": "Insufficient credits remaining.", "type": "insufficient_quota"}}),
            id="429-billing",
        ),
    ],
)
async def test_fastino_on_an_exhausted_account_alarms_once_and_never_retries(fastino_wire, captured, response) -> None:
    posts, raised = await _extract_with(response)
    assert posts == 1, f"a billing refusal was retried ({posts} POSTs)"
    assert fastino_wire == []
    _assert_one_billing_alarm(captured, raised, "fastino")


@pytest.mark.asyncio
async def test_fastino_transient_503_keeps_its_retries(fastino_wire, captured) -> None:
    posts, raised = await _extract_with(httpx.Response(503, json={"detail": "upstream overloaded"}))
    assert posts == fastino_api._MAX_ATTEMPTS
    assert len(fastino_wire) == fastino_api._MAX_ATTEMPTS - 1
    assert isinstance(raised, fastino_api.FastinoServerError)
    # Neither an out-of-credit row nor a false LAYER-2 "billing capture missing".
    assert _kinds(captured) == []


# ---------------------------------------------------------------------------
# 5. Cohere rerank — CohereReranker.rerank
# ---------------------------------------------------------------------------


def _wire_cohere(monkeypatch: pytest.MonkeyPatch, exc: BaseException) -> list[dict[str, Any]]:
    from matrx_ai.providers.cohere.rerank import CohereReranker

    calls: list[dict[str, Any]] = []

    class _Client:
        async def rerank(self, **kwargs: Any) -> Any:
            calls.append(kwargs)
            raise exc

    monkeypatch.setattr(CohereReranker, "client", _Client())
    return calls


@pytest.mark.asyncio
async def test_cohere_rerank_on_a_payment_refusal_files_one_out_of_credit_alarm(monkeypatch, captured) -> None:
    from matrx_ai.providers.cohere.rerank import CohereReranker

    # Cohere's documented 402 body (docs.cohere.com/reference/errors).
    exc = ApiError(
        status_code=402,
        body={
            "message": "Maximum billing reached for this API key as set in your dashboard, please go to "
            "https://dashboard.cohere.com/billing?tab=payment to increase your maximum amount to continue "
            "using this API key."
        },
    )
    calls = _wire_cohere(monkeypatch, exc)
    with pytest.raises(ApiError) as raised:
        await CohereReranker().rerank(
            "slow kitchen drain", _PROPERTY_MANAGER_CHUNKS, model="rerank-v4.0-pro", max_retries=0
        )
    assert raised.value is exc
    assert len(calls) == 1
    _assert_one_billing_alarm(captured, exc, "cohere")


@pytest.mark.asyncio
async def test_cohere_rerank_trial_rate_limit_is_not_filed(monkeypatch, captured) -> None:
    from matrx_ai.providers.cohere.rerank import CohereReranker

    exc = cohere.TooManyRequestsError(
        body={"message": "You are using a Trial key, which is limited to 10 API calls / minute."}
    )
    calls = _wire_cohere(monkeypatch, exc)
    with pytest.raises(cohere.TooManyRequestsError) as raised:
        await CohereReranker().rerank(
            "slow kitchen drain", _PROPERTY_MANAGER_CHUNKS, model="rerank-v4.0-pro", max_retries=0
        )
    assert raised.value is exc
    # The caller's own SDK retry policy is passed through untouched.
    assert calls[0]["request_options"] == {"max_retries": 0}
    assert _kinds(captured) == []


# ---------------------------------------------------------------------------
# The seam itself: nesting and non-chat results
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_a_nested_dispatch_on_the_same_pool_is_admitted_once(monkeypatch) -> None:
    """UnifiedAIClient's extraction route wraps ``extract_spans``, which wraps its own
    send: a nested admission on the same pool double-counts the slot and, at the
    concurrency ceiling, deadlocks every outer holder waiting for an inner slot."""
    from matrx_ai.providers import admission
    from matrx_ai.providers.unified_client import UnifiedAIClient

    entered: list[str] = []
    real = admission.admit_provider_call

    def _counting(profile: Any) -> Any:
        entered.append(admission.admission_key(profile))
        return real(profile)

    monkeypatch.setattr(admission, "admit_provider_call", _counting)
    profile = make_profile(model_name="gliner2-large", wire_format="fastino_extraction", vendor="fastino")

    async def inner() -> str:
        return "spans"

    async def outer() -> str:
        return await UnifiedAIClient._dispatch_with_billing_net(inner, profile=profile)

    assert await UnifiedAIClient._dispatch_with_billing_net(outer, profile=profile) == "spans"
    assert entered == [admission.admission_key(profile)]


@pytest.mark.asyncio
async def test_sibling_tasks_inside_a_dispatch_each_take_their_own_slot(monkeypatch) -> None:
    """The same-task passthrough must not leak: a ContextVar is copied into every
    child task, so keyed by pool alone, gathered siblings (and a task outliving the
    outer call) skipped admission entirely — no pacing, no failure report."""
    import asyncio

    from matrx_ai.providers import admission
    from matrx_ai.providers.unified_client import UnifiedAIClient

    entered: list[str] = []
    real = admission.admit_provider_call

    def _counting(profile: Any) -> Any:
        entered.append(admission.admission_key(profile))
        return real(profile)

    monkeypatch.setattr(admission, "admit_provider_call", _counting)
    profile = make_profile(model_name="gliner2-large", wire_format="fastino_extraction", vendor="fastino")

    async def leaf() -> str:
        return "spans"

    async def fan_out() -> list[str]:
        return list(
            await asyncio.gather(
                *(UnifiedAIClient._dispatch_with_billing_net(leaf, profile=profile) for _ in range(3))
            )
        )

    assert await UnifiedAIClient._dispatch_with_billing_net(fan_out, profile=profile) == ["spans"] * 3
    assert len(entered) == 4  # the outer call + one per sibling task


@pytest.mark.asyncio
async def test_a_non_chat_result_under_a_declared_contract_is_not_judged(monkeypatch) -> None:
    """An STT result or an embedding vector is not an answer: a contract bound by the
    surrounding turn must not judge it, and the findings must not claim it was on-contract."""
    from matrx_ai.providers.unified_client import UnifiedAIClient
    from matrx_ai.schema import answer_contract

    token = answer_contract._DECLARED.set({"schema": {"type": "object", "required": ["verdict"]}, "name": "verdict"})
    judged: list[Any] = []

    async def _verify(response: Any, **_kwargs: Any) -> list[str]:
        judged.append(response)
        return []

    monkeypatch.setattr(answer_contract, "verify_answer_and_record", _verify)
    outcomes: list[Any] = []

    async def _flush(**kwargs: Any) -> None:
        outcomes.append(kwargs["answer_off_contract"])

    monkeypatch.setattr("matrx_ai.providers.structured_output_findings.flush_translation_findings", _flush)
    vectors = [[0.12, -0.08, 0.33]]

    async def embed() -> list[list[float]]:
        return vectors

    try:
        result = await UnifiedAIClient._dispatch_with_billing_net(
            embed, profile=make_profile(model_name="gemini-embedding-2", wire_format="google_embeddings", vendor="google")
        )
    finally:
        answer_contract._DECLARED.reset(token)
    assert result is vectors
    assert judged == []
    assert outcomes == [None]

