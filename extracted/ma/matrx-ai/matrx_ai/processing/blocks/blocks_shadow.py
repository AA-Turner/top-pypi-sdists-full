"""Blocks v1 SHADOW (CGU-14 P2) — every live model call reads blocks beside today's path.

Nothing changes for anyone: the stream, the saved row and every client are untouched. For the
duration of one provider call (``send_once``, the seam every model call crosses) a watcher feeds
each text delta to :class:`~matrx_ai.processing.blocks.blocks_v1.BlocksV1Splitter` and times it.
When the call returns, the provider's own text parts are split one-shot (with kind validation)
and compared with what the stream read. The per-turn summary lands in
``chat.user_request.metadata.blocks_shadow`` (beside ``ttft_ms``), so a week of live turns is a
query, not a log hunt.

Recorded per turn: calls, tokens, per-token feed cost (total, p99, max — microseconds), one-shot
and validation cost, block types and kind statuses, and two kinds of divergence:

* ``text_mismatch`` — the streamed text is not the response's text (a provider writes reasoning
  tags into the stream, a control token, …): P3b must stream from the same text P3a saves;
* ``block_divergence`` — same text, different blocks: a broken guarantee, also captured as a
  ``system_error`` (``blocks_v1_shadow_divergence``).

Switch: the host binds :func:`configure_blocks_shadow` to a knob; unconfigured, the shadow is OFF.
A shadow failure never touches the call — it is counted in the summary and announced once.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Awaitable, Callable, Iterator
from contextlib import contextmanager
from typing import Any

from matrx_ai.processing.blocks.blocks_v1 import BlocksV1Splitter, kind_validator, split_blocks_v1

logger = logging.getLogger(__name__)

_enabled: Callable[[], bool] | None = None
_announced: set[str] = set()

#: Where the per-turn summary lives on the execution state (and then in request metadata).
STATE_ATTR = "blocks_shadow"
METADATA_KEY = "blocks_shadow"


def configure_blocks_shadow(enabled: Callable[[], bool] | None) -> None:
    """Bind the shadow switch to the host's setting (a zero-arg callable), or None for off."""
    global _enabled
    _enabled = enabled


def shadow_enabled() -> bool:
    fn = _enabled
    if fn is None:
        return False
    try:
        return bool(fn())
    except Exception as exc:  # noqa: BLE001 — a switch that cannot be read is off, announced once
        _announce("switch", f"blocks shadow: switch could not be read ({exc!r}); shadow OFF")
        return False


def _announce(key: str, message: str) -> None:
    if key not in _announced:
        _announced.add(key)
        logger.warning(message)


class _ShadowWatcher:
    """Forwards everything to the real emitter; reads each text delta into blocks v1."""

    def __init__(self, inner: Any) -> None:
        object.__setattr__(self, "_inner", inner)
        object.__setattr__(self, "_splitter", BlocksV1Splitter())
        object.__setattr__(self, "_chunks", [])
        object.__setattr__(self, "_costs", [])
        object.__setattr__(self, "_failed", None)

    async def send_chunk(self, text: str) -> None:
        if self._failed is None and text:
            try:
                t0 = time.perf_counter()
                self._splitter.feed(text)
                self._costs.append(time.perf_counter() - t0)
                self._chunks.append(text)
            except Exception as exc:  # noqa: BLE001 — the shadow never touches the call
                object.__setattr__(self, "_failed", f"{type(exc).__name__}: {exc}"[:300])
        await self._inner.send_chunk(text)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._inner, name)

    def __setattr__(self, name: str, value: Any) -> None:
        setattr(self._inner, name, value)


@contextmanager
def shadowing_blocks(state: Any) -> Iterator[Callable[[Any], Awaitable[None]]]:
    """Watch one provider call. Yields ``await finish(response)``, to call once the call returned.

    The re-split at the end runs in a worker thread, so a long reply never blocks the event loop.
    """
    if state is None or not shadow_enabled():
        yield _nothing
        return
    from matrx_connect.context.app_context import set_app_context, try_get_app_context

    ctx = try_get_app_context()
    inner = getattr(ctx, "emitter", None) if ctx is not None else None
    if inner is None:
        yield _nothing
        return
    watcher = _ShadowWatcher(inner)
    set_app_context(ctx.with_overrides(emitter=watcher))

    async def finish(response: Any) -> None:
        import asyncio

        try:
            divergence = await asyncio.to_thread(_finish, state, watcher, response)
        except Exception as exc:  # noqa: BLE001 — the shadow never touches the call
            _announce("thread", f"blocks shadow: finish failed ({exc!r})")
            return
        if divergence is not None:
            await _capture_divergence(*divergence)

    try:
        yield finish
    finally:
        current = try_get_app_context()
        if current is not None and current.emitter is watcher:
            set_app_context(current.with_overrides(emitter=inner))


async def _nothing(_response: Any) -> None:
    return None


def _response_texts(response: Any) -> list[str]:
    texts: list[str] = []
    for message in getattr(response, "messages", None) or ():
        if getattr(message, "role", None) != "assistant":
            continue
        for part in getattr(message, "content", None) or ():
            if getattr(part, "type", None) == "text" and isinstance(getattr(part, "text", None), str):
                texts.append(part.text)
    return texts


def _summary(state: Any) -> dict[str, Any]:
    summary = getattr(state, STATE_ATTR, None)
    if not isinstance(summary, dict):
        summary = {
            "blocks_version": 1,
            "calls": 0,
            "tokens": 0,
            "feed_us_total": 0.0,
            "feed_us_worst_call_p99": 0.0,
            "feed_us_max": 0.0,
            "oneshot_us": 0.0,
            "validate_us": 0.0,
            "text_mismatch": 0,
            "block_divergence": 0,
            "divergence_unchecked": 0,
            "shadow_errors": 0,
            "types": {},
            "kind_status": {},
        }
        try:
            setattr(state, STATE_ATTR, summary)
        except Exception:  # noqa: BLE001 — a state without the slot gets no summary
            return summary
    return summary


#: How much of each side is kept around the first difference (CGU-14 step 6c: name every mismatch).
MISMATCH_HEAD_CHARS = 48


def _mismatch_cause(stream_only: str, response_only: str, stream_text: str) -> str:
    """One named cause for a stream/response text difference, read from what differs."""
    if "<reasoning>" in stream_text or "<think" in stream_text:
        return "reasoning_in_stream"
    if not response_only and not stream_only:
        return "same_text"
    extra = stream_only or response_only
    if not extra.strip():
        return "whitespace_only"
    if "MATRX_JSON_" in extra:
        return "grounded_json_markers"
    if "<matrxcite" in extra or "[[" in extra:
        return "citation_markers"
    if extra.lstrip().startswith(("```", "~~~")):
        return "fence"
    if "__kind" in extra:
        return "kind_json"
    if "<" in extra and ">" in extra:
        return "tag"
    return "stream_extra" if stream_only and not response_only else "response_extra" if response_only and not stream_only else "rewritten"


def _mismatch_head(stream_text: str, response_text: str) -> dict[str, Any]:
    """Where the two texts part and a bounded look at each side there (never the whole reply)."""
    limit = min(len(stream_text), len(response_text))
    start = 0
    while start < limit and stream_text[start] == response_text[start]:
        start += 1
    end = 0
    while end < limit - start and stream_text[-1 - end] == response_text[-1 - end]:
        end += 1
    stream_only = stream_text[start : len(stream_text) - end]
    response_only = response_text[start : len(response_text) - end]
    return {
        "common_prefix_chars": start,
        "common_suffix_chars": end,
        "stream_only_chars": len(stream_only),
        "response_only_chars": len(response_only),
        "stream_only_head": stream_only[:MISMATCH_HEAD_CHARS],
        "response_only_head": response_only[:MISMATCH_HEAD_CHARS],
        "cause": _mismatch_cause(stream_only, response_only, stream_text),
    }


def _finish(state: Any, watcher: _ShadowWatcher, response: Any) -> tuple[int, int, int] | None:
    """Fill the summary; return ``(chars, streamed, one_shot)`` when the guarantee broke."""
    summary = _summary(state)
    try:
        summary["calls"] += 1
        if watcher._failed is not None:
            summary["shadow_errors"] += 1
            summary["last_error"] = watcher._failed
            return None
        t0 = time.perf_counter()
        watcher._splitter.finish()
        costs = watcher._costs
        costs.append(time.perf_counter() - t0)
        streamed = [b.to_dict() for b in watcher._splitter.blocks]
        costs_sorted = sorted(costs)
        summary["tokens"] += len(watcher._chunks)
        summary["feed_us_total"] = round(summary["feed_us_total"] + sum(costs) * 1e6, 1)
        p99 = costs_sorted[min(len(costs_sorted) - 1, int(len(costs_sorted) * 0.99))] * 1e6
        summary["feed_us_worst_call_p99"] = round(max(summary["feed_us_worst_call_p99"], p99), 1)
        summary["feed_us_max"] = round(max(summary["feed_us_max"], costs_sorted[-1] * 1e6), 1)

        stream_text = "".join(watcher._chunks)
        texts = _response_texts(response)
        t1 = time.perf_counter()
        one_shot = [[b.to_dict() for b in split_blocks_v1(t)] for t in texts]
        summary["oneshot_us"] = round(summary["oneshot_us"] + (time.perf_counter() - t1) * 1e6, 1)
        t2 = time.perf_counter()
        validated = [split_blocks_v1(t, validate=kind_validator()) for t in texts]
        summary["validate_us"] = round(summary["validate_us"] + (time.perf_counter() - t2) * 1e6, 1)

        for blocks in validated:
            for b in blocks:
                summary["types"][b.type] = summary["types"].get(b.type, 0) + 1
                if b.type == "kind":
                    status = str(b.fields.get("status"))
                    summary["kind_status"][status] = summary["kind_status"].get(status, 0) + 1

        if not stream_text and not any(texts):
            return None
        if stream_text != "".join(texts):
            summary["text_mismatch"] += 1
            response_text = "".join(texts)
            summary["last_text_mismatch"] = {
                "stream_chars": len(stream_text),
                "response_chars": len(response_text),
                "response_text_parts": len(texts),
                "stream_has_reasoning_tag": "<reasoning>" in stream_text or "<think" in stream_text,
                **_mismatch_head(stream_text, response_text),
            }
            causes = summary.setdefault("text_mismatch_causes", {})
            cause = summary["last_text_mismatch"]["cause"]
            causes[cause] = causes.get(cause, 0) + 1
            return None
        if len(texts) != 1:
            # Several text parts with one stream between them: the per-part spans cannot be
            # compared with one stream's blocks yet (P3b streams per part). Counted, never silent.
            summary["divergence_unchecked"] += 1
            return None
        if streamed != one_shot[0]:
            summary["block_divergence"] += 1
            return (len(stream_text), len(streamed), len(one_shot[0]))
        return None
    except Exception as exc:  # noqa: BLE001 — the shadow never touches the call
        summary["shadow_errors"] += 1
        summary["last_error"] = f"{type(exc).__name__}: {exc}"[:300]
        _announce("finish", f"blocks shadow: summary failed ({exc!r}); counted in blocks_shadow.shadow_errors")
    return None


async def _capture_divergence(chars: int, streamed: int, one_shot: int) -> None:
    """Same text, different blocks: the one guarantee v1 makes. Loud, never blocking."""
    logger.error(
        "blocks shadow: streamed blocks differ from one-shot on the same text "
        "(chars=%d streamed=%d one_shot=%d) — blocks v1 guarantee broken",
        chars, streamed, one_shot,
    )
    from matrx_connect.streaming.error_capture import capture_error

    await capture_error(
        RuntimeError("blocks v1 streamed != one-shot"),
        kind="blocks_v1_shadow_divergence",
        chars=chars, streamed_blocks=streamed, one_shot_blocks=one_shot,
    )


def take_summary(state: Any) -> dict[str, Any] | None:
    """The turn's summary for request metadata, or None when the shadow did not run."""
    summary = getattr(state, STATE_ATTR, None) if state is not None else None
    return dict(summary) if isinstance(summary, dict) and summary.get("calls") else None


__all__ = [
    "METADATA_KEY",
    "configure_blocks_shadow",
    "shadow_enabled",
    "shadowing_blocks",
    "take_summary",
]
