"""Live block events — blocks v1 on the wire while a reply streams (P1-CHAT T1, T1b; PF-1 D5).

A client whose ``client.reads`` names ``blocks-v1`` gets, beside the unchanged ``chunk`` events,
typed ``part.open`` / ``block.open`` / ``block.partial`` / ``block.close`` data events, addressed by
``(message_id, part, index)``. They are PROVISIONAL drawing instructions: the ``message_blocks``
event the save funnel sends at the end of each assistant message (``saved_blocks.py``) carries the
saved text parts and the client replaces every text part of that message with them.

THE ONE SPLITTER. The events come from :class:`BlocksV1Splitter` — the splitter the save uses —
fed the text the save will store as closely as the stream can know it:

* declared control-token lines are filtered with the emitter's own registry (``ControlTokenFilter``);
* reasoning is never inside a text part: a provider writes its thought inline as
  ``<reasoning>…</reasoning>`` and the row saves it as a ``thinking`` part (``reasoning_parts.py``),
  so a ``reasoning`` region ENDS the current text part and the next text opens a new one (the line
  breaks that only separated text from a region are dropped, as the save drops them); a reasoning
  delta on the reasoning channel or a tool event ends the part too;
* ``part`` is the 0-based ordinal of the text part among the row's TEXT parts — ``message_blocks.parts[k]``
  replaces live part ``k``;
* ``regions`` are read only at save time (they arrive with ``message_blocks``); a live markdown block
  never carries them. ``block.close.complete`` is False when the text ended inside the block — for a
  markdown block, when it ended inside an open code fence.

T1b: an OPEN ``kind`` block streams its value so far (``block.partial``): valid closed JSON from
``matrx_graph.content_ir.partial.parse_partial_json``, deduplicated and kept monotonic by
``PartialKindTracker``. The splitter reads a line only when its newline arrives, so partials are
throttled per line. A kind candidate is held until its first key is read (at most 512 chars / 8 lines,
``_HOLD_MAX_*``): a face must not treat that hold as a stall.

Nothing here can fail a reply: the watcher forwards every call first and any failure turns the live
events off for the rest of the call, said once.
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any
from uuid import uuid4

from matrx_connect.context.data_types import (
    BlockCloseData,
    BlockOpenData,
    BlockPartialData,
    DataPayload,
    PartOpenData,
)
from matrx_graph.content_ir.partial import PartialKindTracker, parse_partial_json

from matrx_ai.processing.blocks.blocks_v1 import BlocksV1Splitter, KindValidator

logger = logging.getLogger(__name__)

_OFFSET_FIELDS = ("start", "end", "body_start", "body_end")


class LiveBlocksStream:
    """One provider call's live block events for one assistant message. Pure and synchronous.

    ``feed(visible_text)`` / ``boundary()`` / ``finish()`` each return the typed payloads to send, in order.
    """

    def __init__(self, message_id: str, *, validate: KindValidator | None = None, fence_after_tag: bool = False) -> None:
        self.message_id = message_id
        self._validate = validate
        self._fence_after_tag = fence_after_tag
        self._part = -1  # ordinal of the current text part; -1 = none yet
        self._part_live = False  # the current part has been announced (part.open sent)
        self._tracker = PartialKindTracker()
        self._partial_seen: dict[str, int] = {}
        self._new_segment()

    # ── segments: one splitter per run of text between channel boundaries ─────────────────

    def _new_segment(self) -> None:
        self._splitter = BlocksV1Splitter(validate=self._validate, fence_after_tag=self._fence_after_tag)
        self._raw = bytearray()  # every byte fed to this segment's splitter
        self._fed_pending = ""  # text fed but not yet a whole line (the splitter holds it too)
        self._map: dict[int, int | None] = {}  # splitter index -> local index in the part (None = dropped)
        self._local = 0  # next local index in the current part
        self._base = 0  # byte offset of the current part's text inside this segment
        self._after_region = False  # the current part follows a reasoning region (leading breaks drop)
        self._in_part = False  # a text part is open in this segment
        self._deferred: dict[int, dict[str, Any]] = {}  # markdown opens waiting for real text
        self._held: list[dict[str, Any]] = []  # a block close whose end waits for what follows (see _undecided_tail)
        self._segment_used = False

    def feed(self, text: str) -> list[DataPayload]:
        if not text:
            return []
        self._segment_used = True
        self._raw += text.encode("utf-8")
        out = self._translate(self._splitter.feed(text))
        if self._held and not self._may_open_region(self._splitter._pending):
            out.extend(self._flush_held())
        out.extend(self._partial())
        return out

    # ── a block's end waits until the next block is known ──────────────────────────────
    #
    # The save drops the line breaks that only separate text from a following reasoning region
    # (``inline_reasoning_parts``). A block that closes on its line break (a kind, an artifact) cannot know
    # yet whether a reasoning region comes next, so its close — and the breaks after it, with any
    # breaks-only markdown — waits for the next line that decides it: one that cannot open a reasoning tag
    # releases it at once, a reasoning opener trims the breaks, the end of the text settles it.

    def _undecided_tail(self, events: list[dict[str, Any]]) -> int | None:
        blocks = self._splitter.blocks
        for i in range(len(events) - 1, -1, -1):
            ev = events[i]
            if ev["event"] == "block.regions":
                return None
            block = blocks[ev["index"]]
            if block.type == "markdown" and self._breaks_only(block):
                continue
            if ev["event"] == "block.close" and block.type != "reasoning" and self._trailing_breaks(block.start, block.end):
                return i
            return None
        return None

    def _breaks_only(self, block: Any) -> bool:
        return not bytes(self._raw[block.start : block.end]).strip(b"\r\n")

    @staticmethod
    def _may_open_region(pending: str) -> bool:
        """Can the unfinished line still open a reasoning tag (``<`` after at most 3 spaces)?"""
        body = pending.lstrip(" ")
        return len(pending) - len(body) <= 3 and body[:1] in ("", "<")

    def _flush_held(self) -> list[DataPayload]:
        held, self._held = self._held, []
        return self._translate(held, hold=False) if held else []

    def boundary(self) -> list[DataPayload]:
        """A thinking or tool part interrupts the text: the current part ends; later text opens a new one."""
        if not self._segment_used:
            return []
        out = self._finish_segment()
        self._new_segment()
        self._part_live = False
        return out

    def finish(self) -> list[DataPayload]:
        return self._finish_segment() if self._segment_used else []

    def _finish_segment(self) -> list[DataPayload]:
        events = self._splitter.finish()
        return self._translate(events, final=True, cut_in_fence=self._splitter.in_open_fence)

    # ── translation: splitter events (segment offsets) -> part events (part offsets) ────

    def _translate(
        self, events: list[dict[str, Any]], *, final: bool = False, cut_in_fence: bool = False, hold: bool = True
    ) -> list[DataPayload]:
        out: list[DataPayload] = []
        if self._held:
            events = self._held + events
            self._held = []
        if hold and not final:
            cut = self._undecided_tail(events)
            if cut is not None:
                self._held = events[cut:]
                events = events[:cut]
        blocks = self._splitter.blocks
        last_md_close = None
        if final:
            for i in range(len(events) - 1, -1, -1):
                ev = events[i]
                if ev["event"] == "block.close" and ev["block"]["type"] == "markdown":
                    last_md_close = i
                    break
        for i, ev in enumerate(events):
            name = ev["event"]
            if name == "block.regions":
                continue  # regions are read at save time; message_blocks carries them
            idx = ev["index"]
            block = blocks[idx]
            if name == "block.open":
                if block.type == "reasoning":
                    self._map[idx] = None
                    self._end_part_for_region()
                    self._on_reasoning_open(out, idx, block)
                    continue
                if block.type == "markdown":
                    if self._adopt_markdown(idx, block):
                        continue
                    # Opened by its first line; announced once it holds text the save keeps.
                    self._deferred[idx] = ev
                    self._release_deferred(out)
                    continue
                self._ensure_part(out, block.start)
                self._open_local(out, idx, block.type, block.start)
                continue
            # block.close
            if block.type == "reasoning":
                self._after_region = True
                self._on_reasoning_close(out, idx, block)
                continue
            next_is_region = self._next_opens_region(events, i)
            if idx in self._deferred:
                # A markdown block that never showed real text: only line breaks.
                self._deferred.pop(idx)
                if self._after_region and not self._in_part or next_is_region:
                    self._map[idx] = None  # the save drops breaks beside a reasoning region
                    continue
                self._ensure_part(out, block.start)
                self._open_local(out, idx, "markdown", block.start)
            local = self._map.get(idx)
            if local is None:
                continue
            end = block.end
            if next_is_region:
                end -= self._trailing_breaks(block.start, end)
            payload = self._rebased(ev["block"], end)
            complete = bool(payload.get("complete", True))
            if block.type == "markdown":
                complete = not (cut_in_fence and i == last_md_close)
            if block.type == "kind":
                self._tracker.closed(self._block_key(idx))
            complete = self._before_close(out, idx, local, end, block, complete)
            out.append(
                BlockCloseData(
                    message_id=self.message_id,
                    part=self._part,
                    index=local,
                    end=max(0, end - self._base),
                    complete=complete,
                    block=payload,
                )
            )
        self._release_deferred(out)
        return out

    # ── v2 hooks (LiveBlocksStreamV2, live_blocks_v2.py); no-ops for a blocks-v1 client ─────

    def _on_reasoning_open(self, out: list[DataPayload], idx: int, block: Any) -> None:
        return None

    def _on_reasoning_close(self, out: list[DataPayload], idx: int, block: Any) -> None:
        return None

    def _adopt_markdown(self, idx: int, block: Any) -> bool:
        return False

    def _before_close(self, out: list[DataPayload], idx: int, local: int, end: int, block: Any, complete: bool) -> bool:
        return complete

    def _next_opens_region(self, events: list[dict[str, Any]], i: int) -> bool:
        """Does the next block that holds anything but line breaks open a reasoning region?"""
        for ev in events[i + 1 :]:
            if ev["event"] == "block.open":
                block = self._splitter.blocks[ev["index"]]
                if block.type == "markdown" and self._breaks_only(block):
                    continue
                return block.type == "reasoning"
        return False

    def _end_part_for_region(self) -> None:
        self._in_part = False
        self._deferred.clear()

    def _ensure_part(self, out: list[DataPayload], start: int) -> None:
        if self._in_part:
            return
        self._in_part = True
        self._part += 1
        self._local = 0
        self._base = start + (self._leading_breaks(start) if self._after_region else 0)
        self._after_region = False
        out.append(PartOpenData(message_id=self.message_id, part=self._part))

    def _open_local(self, out: list[DataPayload], idx: int, block_type: str, start: int) -> None:
        local = self._local
        self._local += 1
        self._map[idx] = local
        out.append(
            BlockOpenData(
                message_id=self.message_id,
                part=self._part,
                index=local,
                block_type=block_type,  # type: ignore[arg-type]
                start=max(0, start - self._base),
            )
        )

    def _release_deferred(self, out: list[DataPayload]) -> None:
        for idx in sorted(self._deferred):
            block = self._splitter.blocks[idx]
            head = bytes(self._raw[block.start : block.end])
            if not head.strip(b"\r\n"):
                continue
            self._deferred.pop(idx)
            self._ensure_part(out, block.start)
            self._open_local(out, idx, "markdown", block.start)

    def _leading_breaks(self, start: int) -> int:
        n = 0
        raw = self._raw
        while start + n < len(raw) and raw[start + n] in (0x0A, 0x0D):
            n += 1
        return n

    def _trailing_breaks(self, start: int, end: int) -> int:
        n = 0
        raw = self._raw
        while end - n > start and raw[end - n - 1] in (0x0A, 0x0D):
            n += 1
        return n

    def _rebased(self, block: dict[str, Any], end: int) -> dict[str, Any]:
        out = {k: v for k, v in block.items() if k != "regions"}
        for key in _OFFSET_FIELDS:
            value = out.get(key)
            if isinstance(value, int):
                out[key] = max(0, min(value, end) - self._base)
        return out

    # ── T1b: the open kind block's value so far ─────────────────────────────────────────

    def _block_key(self, idx: int) -> str:
        return f"{self._part}:{idx}:{id(self._splitter)}"

    def _partial(self) -> list[DataPayload]:
        opened = self._splitter.open_kind_source()
        if opened is None:
            return []
        idx, source, slug = opened
        local = self._map.get(idx)
        if local is None or not slug:
            return []
        key = self._block_key(idx)
        # The source only grows by whole lines: an unchanged source parses to the same value (that the
        # tracker would drop), so it is not parsed again on every token (CPU budget, P1-CHAT T1 v2.1).
        if self._partial_seen.get(key) == len(source):
            return []
        self._partial_seen[key] = len(source)
        if self._tracker.regressed(key, len(source)):
            return []
        value = parse_partial_json(source)
        if not isinstance(value, (dict, list)):
            return []
        if not self._tracker.advanced(key, {"v": value}):
            return []
        self._tracker.opened(key, slug)
        return [
            BlockPartialData(
                message_id=self.message_id,
                part=self._part,
                index=local,
                kind=slug,
                seq=self._tracker.next_seq(key),
                value=value,
            )
        ]


# ── the watcher: one provider call, installed by send_once ───────────────────────────────


def _visible_filter(inner: Any) -> Any:
    """A control-token filter configured like the emitter's own, so live text equals the wire text."""
    from matrx_connect.emitters.control_tokens import ControlTokenFilter

    own = getattr(inner, "_control_filter", None)
    return ControlTokenFilter(
        mandate_key=getattr(own, "_mandate_key", None),
        enabled=getattr(own, "_enabled", True),
    )


class _PlainTail:
    """blocks-v2 after a live-event failure: the rest of the reply as plain text in ONE markdown block.

    Still the server's decision (``blocks.degraded`` said so first), never a client guess; no regions.
    ``message_blocks`` still replaces the whole message at the end."""

    def __init__(self, message_id: str, part: int) -> None:
        self.message_id = message_id
        self.part = part
        self.end = 0
        self.opened = False

    def feed(self, text: str) -> list[DataPayload]:
        from matrx_connect.context.data_types import BlockGrowData

        if not text:
            return []
        out: list[DataPayload] = []
        if not self.opened:
            self.opened = True
            out.append(PartOpenData(message_id=self.message_id, part=self.part))
            out.append(BlockOpenData(message_id=self.message_id, part=self.part, index=0, block_type="markdown", start=0))
        self.end += len(text.encode("utf-8"))
        out.append(BlockGrowData(message_id=self.message_id, part=self.part, index=0, end=self.end, text=text))
        return out

    def finish(self, *, complete: bool = True) -> list[DataPayload]:
        if not self.opened:
            return []
        self.opened = False
        block = {"type": "markdown", "start": 0, "end": self.end}
        return [
            BlockCloseData(
                message_id=self.message_id, part=self.part, index=0, end=self.end, complete=complete, block=block
            )
        ]


class _LiveBlocksWatcher:
    """Forwards everything to the real emitter; turns the call's text into live block events."""

    def __init__(self, inner: Any, stream: LiveBlocksStream, *, v2: bool = False) -> None:
        object.__setattr__(self, "_inner", inner)
        object.__setattr__(self, "_stream", stream)
        object.__setattr__(self, "_filter", _visible_filter(inner))
        object.__setattr__(self, "_dead", False)
        object.__setattr__(self, "_v2", v2)
        object.__setattr__(self, "_plain", None)
        object.__setattr__(self, "_over", False)

    def _sealed(self) -> bool:
        return getattr(self._inner, "sealed", False) is True

    @property
    def streams_thinking_live(self) -> bool:
        """A blocks-v2 reader draws every thought live as ``reasoning.open/grow/close``: a provider that would hold a
        thought back (Anthropic, until a block's signature says whether it is a progress update) streams it at once.
        A v1 reader (www) keeps the hold, so what it draws is unchanged."""
        return self._v2 and not self._dead and self._plain is None

    def withdraw_reasoning(self) -> None:
        """The open thought was a progress update (also sent as reply text): its close carries ``withdrawn: true``."""
        mark = getattr(self._stream, "withdraw_reasoning", None)
        if self._v2 and callable(mark):
            mark()

    async def _send(self, payloads: list[DataPayload]) -> None:
        for payload in payloads:
            await self._inner.send_data(payload)

    async def _run(self, step: Any) -> bool:
        if self._dead:
            return False
        try:
            await self._send(step())
            return True
        except Exception as exc:  # noqa: BLE001 — live events never touch the reply
            object.__setattr__(self, "_dead", True)
            logger.error("live blocks: events stopped for message %s (%r); message_blocks still replaces the reply", self._stream.message_id, exc)
            if self._v2:
                await self._degrade(f"{type(exc).__name__}: {exc}"[:300])
            return False

    async def _degrade(self, reason: str) -> None:
        """No silent loss for a v2 client: say so, then stream the rest as plain grow text."""
        from matrx_connect.context.data_types import BlocksDegradedData

        part = max(getattr(self._stream, "_part", -1), -1) + 1
        object.__setattr__(self, "_plain", _PlainTail(self._stream.message_id, part))
        try:
            await self._inner.send_data(BlocksDegradedData(message_id=self._stream.message_id, reason=reason))
        except Exception as exc:  # noqa: BLE001 — the wire itself is gone; the save still replaces
            logger.error("live blocks: blocks.degraded for %s not sent (%r)", self._stream.message_id, exc)

    async def _plain_step(self, step: Any) -> None:
        try:
            await self._send(step())
        except Exception as exc:  # noqa: BLE001 — the plain tail failing too leaves message_blocks
            object.__setattr__(self, "_plain", None)
            logger.error("live blocks: plain tail stopped for %s (%r)", self._stream.message_id, exc)

    async def send_chunk(self, text: str) -> None:
        await self._inner.send_chunk(text)
        if not text or self._over:
            return
        if self._v2 and self._sealed():
            return  # STOP IS FINAL: nothing grows after the seal; the close-off closes at the last watermark
        visible = self._filter.feed(text).text
        if self._plain is not None:
            await self._plain_step(lambda: self._plain.feed(visible))
            return
        if not await self._run(lambda: self._stream.feed(visible)) and self._plain is not None:
            # The chunk whose events failed opens the plain tail: no word is lost from the screen.
            await self._plain_step(lambda: self._plain.feed(visible))

    async def send_reasoning_chunk(self, text: str) -> None:
        if self._plain is None and not (self._v2 and self._sealed()):
            await self._run(self._stream.boundary)
        await self._inner.send_reasoning_chunk(text)

    async def send_tool_event(self, event_data: Any) -> None:
        if self._plain is None and not (self._v2 and self._sealed()):
            await self._run(self._stream.boundary)
        await self._inner.send_tool_event(event_data)

    async def finish(self) -> None:
        if self._over:
            return
        if self._v2 and self._sealed():
            return  # the seal's close-off (``close_off``, run by the emitter before END) owns the ending
        object.__setattr__(self, "_over", True)
        if self._plain is not None:
            tail = self._filter.flush().text
            plain = self._plain
            await self._plain_step(lambda: [*plain.feed(tail), *plain.finish()])
            return

        def step() -> list[DataPayload]:
            tail = self._filter.flush().text
            return [*self._stream.feed(tail), *self._stream.finish()]

        await self._run(step)
        if self._v2 and not self._dead:
            # The blocks closed ``complete: true``: the client holds the whole reply, so a Stop's cut cannot
            # be drawn any more — the save equals what was sent (P8-RUNS).
            final = getattr(self._inner, "note_shown_final", None)
            if callable(final):
                final()

    async def close_off(self) -> None:
        """THE stop close-off (blocks-v2): registered with ``StreamEmitter.on_sealed``; runs after the seal, before END."""
        if self._over:
            return
        object.__setattr__(self, "_over", True)
        if self._plain is not None:
            plain = self._plain
            await self._plain_step(lambda: plain.finish(complete=False))
            return
        cut_fn = getattr(self._inner, "stop_cut_chars", None)
        cut = cut_fn() if callable(cut_fn) else None
        stream = self._stream
        await self._run(lambda: stream.close_off(cut if isinstance(cut, int) else None))

    def shown_chars(self) -> int | None:
        """Where a stopped turn's text is cut: the last watermark sent (None before any v2 event)."""
        if self._plain is not None or self._dead:
            return None
        return getattr(self._stream, "shown_chars", None)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._inner, name)

    def __setattr__(self, name: str, value: Any) -> None:
        setattr(self._inner, name, value)


def live_message_id(state: Any, config: Any) -> str | None:
    """The row id this provider call's assistant message is saved on.

    The run's first answer is reserved before the loop (``state.reserved_message_ids``); a later
    iteration's row is created only at its save, so its id is minted HERE and kept on
    ``state.streamed_message_ids`` — the save funnel's fresh-row path takes it from there (by position),
    so the live events and the saved row share one id.
    """
    reserved = getattr(state, "reserved_message_ids", None)
    if not isinstance(reserved, dict):
        return None
    try:
        position = len(config.messages.to_list())
    except Exception:  # noqa: BLE001 — no message list, no live address
        return None
    found = reserved.get(position) or reserved.get(str(position))
    if found:
        return str(found)
    minted = getattr(state, "streamed_message_ids", None)
    if not isinstance(minted, dict):
        return None
    return minted.setdefault(position, str(uuid4()))


class _NoLive:
    async def finish(self) -> None:
        return None


@asynccontextmanager
async def streaming_live_blocks(state: Any, config: Any) -> AsyncIterator[Any]:
    """Watch one provider call for a ``blocks-v1`` / ``blocks-v2`` client. Yields an object with ``await finish()``.

    Off (yields a no-op) unless the run's client reads ``blocks-v1`` or ``blocks-v2``. The announcements of the
    previous message's ``message_blocks`` are settled first, so a message's replacement always
    precedes the next message's live events on the wire. A ``blocks-v2`` client gets ``blocks.ack`` first,
    and the emitter's seal runs this call's stop close-off (``on_sealed``) and cuts the saved stopped text at
    the last watermark sent (``set_shown_text_cut``).
    """
    from matrx_connect.context.app_context import set_app_context, try_get_app_context

    from matrx_ai.processing.blocks.saved_blocks import (
        BLOCKS_V1_READ,
        BLOCKS_V2_READ,
        client_reads,
        settle_announcements,
    )

    ctx = try_get_app_context()
    inner = getattr(ctx, "emitter", None) if ctx is not None else None
    v2 = inner is not None and client_reads(ctx, BLOCKS_V2_READ)
    if state is None or inner is None or not (v2 or client_reads(ctx, BLOCKS_V1_READ)):
        yield _NoLive()
        return
    message_id = live_message_id(state, config)
    if not message_id:
        if v2:
            await _say_degraded(inner, "", "no_message_address")
        yield _NoLive()
        return
    await settle_announcements()
    from matrx_ai.processing.blocks.blocks_v1 import kind_validator

    if v2:
        from matrx_connect.context.data_types import BlocksAckData

        from matrx_ai.processing.blocks.live_blocks_v2 import LiveBlocksStreamV2

        stream: LiveBlocksStream = LiveBlocksStreamV2(message_id, validate=kind_validator())
    else:
        stream = LiveBlocksStream(message_id, validate=kind_validator())
    watcher = _LiveBlocksWatcher(inner, stream, v2=v2)
    if v2:
        try:
            await inner.send_data(BlocksAckData(message_id=message_id))
        except Exception as exc:  # noqa: BLE001 — a lost ack leaves the client on its v1 path, said
            logger.error("live blocks: blocks.ack for %s not sent (%r)", message_id, exc)
        from matrx_ai.processing.blocks.saved_blocks import force_blocks_degraded

        if force_blocks_degraded():
            # The debug knob (test seats only): prove the degraded path on a real turn — said, then the plain tail.
            await watcher._degrade("forced_by_debug_knob")
        on_sealed = getattr(inner, "on_sealed", None)
        if callable(on_sealed):
            on_sealed(watcher.close_off)
        set_cut = getattr(inner, "set_shown_text_cut", None)
        if callable(set_cut):
            set_cut(watcher.shown_chars)
    set_app_context(ctx.with_overrides(emitter=watcher))
    try:
        yield watcher
    finally:
        current = try_get_app_context()
        if current is not None and current.emitter is watcher:
            set_app_context(current.with_overrides(emitter=inner))


async def _say_degraded(inner: Any, message_id: str, reason: str) -> None:
    from matrx_connect.context.data_types import BlocksDegradedData

    try:
        await inner.send_data(BlocksDegradedData(message_id=message_id, reason=reason))
    except Exception as exc:  # noqa: BLE001
        logger.error("live blocks: blocks.degraded (%s) not sent (%r)", reason, exc)


__all__ = ["LiveBlocksStream", "live_message_id", "streaming_live_blocks"]
