"""Fastino GLiNER2 hosted-API client — information extraction, NOT chat.

A thin async HTTP client over Pioneer's OpenAI-compatible gateway
(``POST {base}/v1/chat/completions``), which hosts Fastino's GLiNER2 models. It
does span/entity extraction: although the transport is chat-shaped, the request
carries a ``schema`` of entity labels and the assistant message ``content`` is a
JSON string of typed spans — so this is deliberately NOT a chat provider and does
not ride the UnifiedConfig/messages chat dispatch. We call the API directly with
httpx instead of shipping the gliner2 SDK (which pulls in torch).
"""

from __future__ import annotations

import asyncio
import json
import random
from typing import Any

import httpx
from matrx_utils import vcprint

from .client import (
    acquire_fastino_slot,
    build_fastino_client,
    fastino_auth_headers,
    gliner2_url,
)
from .errors import (
    FastinoAuthError,
    FastinoError,
    FastinoServerError,
    FastinoValidationError,
)
from .models import ExtractedSpan, SpanExtractionResult


def _coerce_int(value: Any, default: int = -1) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _coerce_score(value: Any) -> float | None:
    try:
        c = float(value)
    except (TypeError, ValueError):
        return None
    return 0.0 if c < 0.0 else 1.0 if c > 1.0 else c


def _coerce_span(label: str, item: Any) -> ExtractedSpan | None:
    if isinstance(item, str):
        text = item.strip()
        return ExtractedSpan(label=label, text=text, start=-1, end=-1, score=None) if text else None
    if isinstance(item, dict):
        text = item.get("text") or item.get("span") or item.get("value") or ""
        if not isinstance(text, str) or not text.strip():
            return None
        return ExtractedSpan(
            label=label,
            text=text,
            start=_coerce_int(item.get("start", item.get("span_start", -1))),
            end=_coerce_int(item.get("end", item.get("span_end", -1))),
            score=_coerce_score(item.get("confidence", item.get("score"))),
        )
    return None


def parse_spans(result: Any) -> list[ExtractedSpan]:
    """Flatten the API's entity payload into a flat span list.

    Tolerates every shape the endpoint can return across the
    format_results / include_spans / include_confidence toggles:
    ``{"entities": {label: [span,...]}}``, a bare ``{label: [span,...]}``,
    a list of span dicts, and bare-string spans (when offsets are absent).
    Defensive on purpose — the exact shape is pinned by the live spike.
    """
    spans: list[ExtractedSpan] = []
    if not isinstance(result, dict):
        return spans
    entities = result.get("entities", result)
    if isinstance(entities, dict):
        for label, items in entities.items():
            if not isinstance(items, list):
                items = [items]
            for item in items:
                span = _coerce_span(str(label), item)
                if span is not None:
                    spans.append(span)
    elif isinstance(entities, list):
        for item in entities:
            label = ""
            if isinstance(item, dict):
                label = str(item.get("label") or item.get("type") or item.get("entity") or "")
            span = _coerce_span(label, item)
            if span is not None:
                spans.append(span)
    return spans


def _error_detail(resp: httpx.Response) -> str:
    try:
        body = resp.json()
    except ValueError:
        return resp.text[:300]
    if isinstance(body, dict):
        return str(body.get("detail") or body.get("error") or body)[:300]
    return str(body)[:300]


def _handle_response(resp: httpx.Response) -> dict[str, Any]:
    status = resp.status_code
    if status == 401:
        raise FastinoAuthError("Invalid or expired Pioneer/Fastino API key", status_code=status)
    if status in (400, 422):
        raise FastinoValidationError(
            f"Fastino request validation failed (HTTP {status}): {_error_detail(resp)}",
            status_code=status,
        )
    if status >= 500:
        raise FastinoServerError(f"Fastino server error (HTTP {status})", status_code=status)
    if not resp.is_success:
        raise FastinoError(
            f"Fastino request failed (HTTP {status}): {_error_detail(resp)}", status_code=status
        )
    try:
        data = resp.json()
    except ValueError as exc:
        raise FastinoError("Invalid JSON response from Fastino API") from exc
    return data if isinstance(data, dict) else {}


def _decode_response_off_loop(
    status_code: int,
    headers: httpx.Headers,
    raw_chunks: list[bytes],
    request: httpx.Request,
) -> httpx.Response:
    # Constructing a response eagerly decodes compressed content. Keep that CPU
    # work on the worker thread; callers offload JSON parsing separately.
    return httpx.Response(
        status_code=status_code,
        headers=headers,
        content=b"".join(raw_chunks),
        request=request,
    )


async def _post_without_loop_decode(
    client: httpx.AsyncClient,
    url: str,
    payload: dict[str, Any],
    headers: dict[str, str],
) -> httpx.Response:
    request = client.build_request("POST", url, json=payload, headers=headers)
    response = await client.send(request, stream=True)
    # Mock/custom transports may return an already-buffered response. Its
    # content is already decoded, but JSON parsing is still offloaded below.
    if response.is_stream_consumed:
        return response
    try:
        raw_chunks = [chunk async for chunk in response.aiter_raw()]
    finally:
        await response.aclose()

    return await asyncio.to_thread(
        _decode_response_off_loop,
        response.status_code,
        response.headers,
        raw_chunks,
        request,
    )


def _entities_from_completion(completion: dict[str, Any]) -> dict[str, Any]:
    """Pull the entity payload out of an OpenAI-style chat completion.

    The gateway returns ``choices[0].message.content`` as a JSON *string* of the
    shape ``{"entities": {label: [span, ...]}}``. Parse it back into a dict for
    ``parse_spans``. Tolerant of the content already being a dict (defensive)."""
    choices = completion.get("choices")
    if not isinstance(choices, list) or not choices:
        return {}
    message = choices[0].get("message") if isinstance(choices[0], dict) else None
    content = message.get("content") if isinstance(message, dict) else None
    if isinstance(content, dict):
        return content
    if not isinstance(content, str) or not content.strip():
        return {}
    try:
        parsed = json.loads(content)
    except ValueError as exc:
        raise FastinoError("Fastino returned non-JSON span content") from exc
    return parsed if isinstance(parsed, dict) else {}


def _parse_completion_off_loop(
    completion: dict[str, Any],
) -> tuple[dict[str, Any], list[ExtractedSpan]]:
    entities = _entities_from_completion(completion)
    return entities, parse_spans(entities)


# Default Pioneer-hosted GLiNER2 model id (largest currently live; xl/small are
# not hosted). The offering's provider_model_id overrides this per request.
DEFAULT_GLINER2_MODEL = "fastino/gliner2-large-v1"

# Resilience policy for the hosted gateway. A large fan-out (e.g. NER over a
# few-thousand-chunk document) hammers Pioneer's GLiNER2 endpoint hard enough
# that it sheds load: HTTP 429 (rate limit) and 5xx (overloaded / cold-start)
# come back for a large fraction of the burst. Those are TRANSIENT — the same
# request succeeds moments later once capacity frees up — so we retry them with
# exponential backoff + jitter (jitter de-syncs concurrent callers so they don't
# all retry in lockstep and re-trigger the same overload).
#
# NON-retryable (real protocol violations, retrying only wastes calls): 401
# (auth), 400/422 (validation). Those bubble up immediately from _handle_response.
_RETRYABLE_STATUS: frozenset[int] = frozenset({429, 500, 502, 503, 504})
_MAX_ATTEMPTS = 4  # 1 initial + 3 retries
_BACKOFF_BASE_S = 1.0
_BACKOFF_MAX_S = 30.0
_BACKOFF_JITTER_S = 0.75


def _parse_retry_after(value: str | None) -> float | None:
    """Honor a numeric ``Retry-After`` header (seconds). HTTP-date form is rare
    from this gateway and intentionally ignored — we fall back to our own
    backoff schedule. Capped so a hostile/huge value can't stall the run."""
    if not value:
        return None
    try:
        secs = float(value.strip())
    except (TypeError, ValueError):
        return None
    if secs < 0:
        return None
    return min(secs, _BACKOFF_MAX_S)


def _backoff_delay(attempt: int, retry_after: float | None) -> float:
    """Server-provided Retry-After wins; otherwise exponential base*2**attempt
    capped at _BACKOFF_MAX_S, plus uniform jitter."""
    if retry_after is not None:
        return retry_after
    capped = min(_BACKOFF_MAX_S, _BACKOFF_BASE_S * (2**attempt))
    return capped + random.uniform(0.0, _BACKOFF_JITTER_S)


# ── Oversized-input windowing (GLiNER2 max_model_len guard) ──────────────────
# GLiNER2 (gliner2-large) rejects any request whose tokenised input exceeds the
# model's configured ``max_model_len`` with a NON-retryable HTTP 400
# ("GLiNER2 request exceeds the configured max_model_len; reduce text or schema
# size, …, or set 'truncate_overflow_text' to true"). Before this guard a single
# oversized chunk (a dense PDF page, a long reference list) raised that 400, the
# chunk's NER call failed, and the chunk was dropped upstream — silently gutting
# a fraction of the document's entities. That is the exact class of failure the
# NER pipeline comments are built to prevent; it just lived one layer down, in
# the provider that physically cannot accept the input size.
#
# The fix: never send the model more than it can take. We window oversized text
# into pieces under a conservative CHARACTER budget (no tokenizer here — shipping
# one would drag in torch — so we approximate at the ~4 chars/token ratio used
# elsewhere in the codebase), extract each window, and merge the spans back with
# offset-adjusted positions, deduping the overlap region. NO content is ever
# silently truncated: every character is seen by at least one window.
#
# This is CONFIG, not a per-environment toggle (a server-specific limit that
# silently differs is the failure mode we forbid): a CAPS constant changed via
# code push. The budget sits well under the observed failure point (~3958 chars
# / ~990 est. tokens FAILED; ≤986 chars SUCCEEDED) with headroom for the schema
# + special tokens. A deliberate batch job may override via the env var below.
FASTINO_MAX_INPUT_CHARS: int = 1500
# Overlap between adjacent windows so an entity straddling a window boundary is
# still wholly contained in at least one window (then deduped on merge).
FASTINO_WINDOW_OVERLAP_CHARS: int = 150


def _fastino_max_input_chars() -> int:
    # FASTINO_MAX_INPUT_CHARS is a code-reviewed constant, not an env var.
    # (Was MATRX_AI_FASTINO_MAX_INPUT_CHARS.)
    return FASTINO_MAX_INPUT_CHARS


def _split_into_windows(text: str, *, budget: int, overlap: int) -> list[tuple[int, str]]:
    """Split ``text`` into ``(char_offset, window_text)`` pieces each ≤ ``budget``
    characters. Cuts prefer the last whitespace/newline before the budget so a
    word (and therefore a multi-token entity) is never split mid-token. Adjacent
    windows overlap by ``overlap`` chars so a boundary-straddling entity is wholly
    inside at least one window. Returns ``[(0, text)]`` unchanged when the text
    already fits — the common case, with zero added cost."""
    n = len(text)
    if n <= budget:
        return [(0, text)]
    windows: list[tuple[int, str]] = []
    start = 0
    while start < n:
        end = min(start + budget, n)
        if end < n:
            # Back up to the last whitespace within the latter half of the
            # window so we cut on a word boundary. Keeping the search floor at
            # start + budget//2 guarantees forward progress (since overlap <
            # budget//2) even for text with no whitespace in the first half.
            floor = start + budget // 2
            cut = max(text.rfind(" ", floor, end), text.rfind("\n", floor, end))
            if cut > start:
                end = cut
        windows.append((start, text[start:end]))
        if end >= n:
            break
        start = max(end - overlap, start + 1)
    return windows


class FastinoExtraction:
    """Hosted GLiNER2 information extraction via Pioneer's OpenAI-compatible
    gateway (``POST {base}/v1/chat/completions``)."""

    def __init__(self, client: httpx.AsyncClient | None = None, *, debug: bool = False) -> None:
        # An optional shared client lets a fan-out (e.g. NER over many chunks)
        # pool connections; when None, each call opens its own via ``async with``.
        self._client = client
        self.debug = debug
        self.endpoint_name = "[FASTINO EXTRACTION]"

    async def extract(
        self,
        text: str,
        labels: list[str],
        *,
        threshold: float = 0.3,
        model_class: str | None = None,
        include_confidence: bool = True,
        include_spans: bool = True,
    ) -> SpanExtractionResult:
        model_id = model_class or DEFAULT_GLINER2_MODEL

        # Window oversized input so GLiNER2's max_model_len ceiling can never
        # turn into a dropped chunk (see the windowing rationale above). The
        # common path — text already under budget — yields a single window and
        # behaves exactly as the prior single-call code did.
        windows = _split_into_windows(
            text,
            budget=_fastino_max_input_chars(),
            overlap=FASTINO_WINDOW_OVERLAP_CHARS,
        )

        if len(windows) == 1:
            completion = await self._post(
                self._build_payload(
                    model_id, text, labels, threshold, include_confidence, include_spans
                )
            )
            entities, spans = await asyncio.to_thread(_parse_completion_off_loop, completion)
            raw: dict[str, Any] | None = entities if isinstance(entities, dict) else None
        else:
            spans, raw = await self._extract_windowed(
                model_id, windows, labels, threshold, include_confidence, include_spans
            )

        if self.debug:
            vcprint(
                data={
                    "model": model_id,
                    "labels": labels,
                    "threshold": threshold,
                    "n_spans": len(spans),
                },
                title=f"{self.endpoint_name} extracted",
                color="cyan",
                verbose=True,
            )
        return SpanExtractionResult(
            model=model_id,
            spans=spans,
            raw=raw,
        )

    @staticmethod
    def _build_payload(
        model_id: str,
        text: str,
        labels: list[str],
        threshold: float,
        include_confidence: bool,
        include_spans: bool,
    ) -> dict[str, Any]:
        return {
            "model": model_id,
            "messages": [{"role": "user", "content": text}],
            "schema": {"entities": list(labels)},
            "threshold": threshold,
            "include_confidence": include_confidence,
            "include_spans": include_spans,
            # Belt-and-suspenders: windowing already keeps each request under the
            # char budget, but a single window with NO whitespace (a degenerate
            # ~budget-long run, e.g. base64 / a giant table row) can still tokenise
            # past max_model_len. Tell the gateway to truncate THAT window's
            # overflow rather than 400 the request — at worst we lose the tail of
            # one already-small window, never the whole chunk. The common, in-budget
            # request is unaffected (nothing overflows, nothing is truncated).
            "truncate_overflow_text": True,
        }

    async def _extract_windowed(
        self,
        model_id: str,
        windows: list[tuple[int, str]],
        labels: list[str],
        threshold: float,
        include_confidence: bool,
        include_spans: bool,
    ) -> tuple[list[ExtractedSpan], dict[str, Any] | None]:
        """Extract over each window and merge the spans into one offset-correct,
        deduped list (relative to the ORIGINAL text). Overlap regions yield the
        same span from two windows; we keep the higher-confidence copy."""
        merged: dict[tuple[str, int, int, str], ExtractedSpan] = {}
        for base, window_text in windows:
            completion = await self._post(
                self._build_payload(
                    model_id, window_text, labels, threshold, include_confidence, include_spans
                )
            )
            _, window_spans = await asyncio.to_thread(_parse_completion_off_loop, completion)
            for span in window_spans:
                # Offsets come back relative to the window we sent — shift them
                # into the original text. Position-less spans (start == -1) keep
                # -1 and dedup purely on (label, text).
                if span.start >= 0:
                    end = span.end + base if span.end >= 0 else span.end
                    span = span.model_copy(update={"start": span.start + base, "end": end})
                    key = (span.label, span.start, span.end, span.text.lower())
                else:
                    key = (span.label, -1, -1, span.text.lower())
                prev = merged.get(key)
                if prev is None or (span.score or 0.0) > (prev.score or 0.0):
                    merged[key] = span
        return list(merged.values()), None

    async def _post(self, payload: dict[str, Any]) -> dict[str, Any]:
        url = gliner2_url()
        headers = fastino_auth_headers()

        # Retry both transient TRANSPORT failures (timeout, connection reset)
        # AND transient HTTP statuses (429 rate-limit, 5xx overload/cold-start)
        # with exponential backoff + jitter. This is what keeps a large NER
        # fan-out from silently losing 3/4 of a document: under a thousands-of-
        # chunk burst the hosted gateway sheds load with 429/503, which the old
        # one-shot transport-only retry didn't cover, so those chunks raised and
        # were dropped upstream. Auth (401) and validation (400/422) are real
        # protocol violations — _handle_response raises them and we never retry.
        last_exc: Exception | None = None
        for attempt in range(_MAX_ATTEMPTS):
            is_last = attempt == _MAX_ATTEMPTS - 1
            retry_after: float | None = None
            # Client-side rate gate: acquire a token from the shared token
            # bucket BEFORE every attempt (incl. retries) so the aggregate
            # outbound rate never exceeds the provider's documented ceiling.
            await acquire_fastino_slot()
            try:
                if self._client is not None:
                    resp = await _post_without_loop_decode(self._client, url, payload, headers)
                else:
                    client = await asyncio.to_thread(build_fastino_client)
                    async with client:
                        resp = await _post_without_loop_decode(client, url, payload, headers)
            except httpx.TimeoutException as exc:
                last_exc = FastinoError(f"Fastino request timed out: {exc}")
            except httpx.RequestError as exc:
                last_exc = FastinoError(f"Fastino connection error: {exc}")
            else:
                # On the last attempt, OR for a non-retryable status, hand the
                # response to _handle_response: it returns parsed data on success
                # and raises the precise typed error otherwise.
                if is_last or resp.status_code not in _RETRYABLE_STATUS:
                    return await asyncio.to_thread(_handle_response, resp)
                retry_after = _parse_retry_after(resp.headers.get("retry-after"))
                last_exc = FastinoServerError(
                    f"Fastino transient HTTP {resp.status_code} "
                    f"(attempt {attempt + 1}/{_MAX_ATTEMPTS})",
                    status_code=resp.status_code,
                )

            if not is_last:
                await asyncio.sleep(_backoff_delay(attempt, retry_after))

        assert last_exc is not None  # noqa: S101  - loop must have caught something
        raise last_exc
