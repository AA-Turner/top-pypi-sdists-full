"""Live blocks v2 — the server decides every block's and region's state (P1-CHAT T1 v2.1).

A client whose ``client.reads`` names ``blocks-v2`` gets, on top of every v1 event, the events that let
it draw WITHOUT reading the text itself (contract: ``FEATURE.md`` § Live block events, v2):

* ``blocks.ack`` first: the server speaks v2 for this message.
* ``block.grow {part, index, end, text}``: the part's text, slice by slice, word by word. The text is
  the part's own (control tokens filtered, reasoning excluded); ``end`` is the watermark. A line is
  released as it arrives unless its first characters could open a structure (a fence, ``{``, ``[``,
  ``<``, ``|``, ``$$``, or a bare container marker); such a line waits for its newline, and a ``|``
  line (a possible table header) waits one more line for the delimiter row. Inside an open fence only
  a line that could close it waits. Line breaks at the watermark wait for the next words (they are
  invisible, and the save drops the ones that only separated text from a reasoning region).
* ``region.open / region.partial / region.close`` inside a markdown block, from :class:`RegionReader` —
  equal to the save's ``markdown_regions`` (property test ``test_live_blocks_v2.py``).
* inline reasoning as its own ``reasoning.open / reasoning.grow / reasoning.close`` (never in a part).
* :meth:`LiveBlocksStreamV2.close_off` — THE stop close-off: every open block and region closes
  ``complete: false`` at ``min(last watermark SENT, the save's cut)`` (regions keep their language); the cut is
  the emitter's ``stop_cut_chars`` (the last grow the client's ``seen_seq`` covers), at most :attr:`shown_chars`. The live door (the emitter's seal), the stopped-call
  save (``_stopped_call_response`` via ``StreamEmitter.get_seen_turn_text``) and the late door
  (``late_stop``, via :func:`watermark_cut_chars`) all cut at that one point.
"""

from __future__ import annotations

from typing import Any

from matrx_connect.context.data_types import (
    BlockCloseData,
    BlockGrowData,
    BlockOpenData,
    DataPayload,
    ReasoningCloseData,
    ReasoningGrowData,
    ReasoningOpenData,
    RegionCloseData,
    RegionOpenData,
    RegionPartialData,
)

from matrx_ai.processing.blocks.blocks_v1 import (
    DIGEST_LABEL,
    DIGEST_TAG,
    KindValidator,
    blocks_v1_dicts,
    could_become_digest_heading,
)
from matrx_ai.processing.blocks.live_blocks import LiveBlocksStream
from matrx_ai.processing.blocks.region_reader import RegionEvents, RegionReader, region_kind_and_display

_BREAKS = (0x0A, 0x0D)
#: First characters of a line (after container markers) that may open a structure: held to the newline.
_RISKY_FIRST = ("`", "~", "{", "[", "<", "|", "$$")


def _strip_containers(line: str) -> str:
    """The line after its leading blockquote and list markers (``> ``, ``- ``, ``1. ``) and indentation."""
    s = line
    while True:
        t = s.lstrip(" \t")
        if t.startswith(">"):
            s = t[1:]
            continue
        if t[:1] in ("-", "*", "+") and t[1:2] in (" ", "\t"):
            s = t[2:]
            continue
        i = 0
        while i < len(t) and i < 9 and t[i].isdigit():
            i += 1
        if 0 < i and t[i : i + 1] in (".", ")") and t[i + 1 : i + 2] in (" ", "\t"):
            s = t[i + 2 :]
            continue
        return t


def releasable_prefix(pending: str, *, in_fence_marker: str | None) -> str:
    """How much of an unfinished line may be drawn now (the word-by-word rule of the contract)."""
    if not pending:
        return ""
    if in_fence_marker is not None:
        body = pending.lstrip(" \t")
        if not body or body[0] == in_fence_marker:
            return ""  # could be the closing fence
        return pending
    body = _strip_containers(pending)
    if not body:
        return ""  # only indentation or container markers so far: the next character decides
    if body.startswith(_RISKY_FIRST) or "|" in pending:
        return ""
    cut = pending.find("{")  # a same-line ``__kind`` object is lifted out of the line: never drawn as prose
    return pending if cut < 0 else pending[:cut]


class LiveBlocksStreamV2(LiveBlocksStream):
    """:class:`LiveBlocksStream` plus the v2 events. Pure and synchronous, like v1."""

    def __init__(self, message_id: str, *, validate: KindValidator | None = None) -> None:
        self._all = bytearray()  # the call's whole fed text (= the emitter's turn text, UTF-8)
        self._seg_abs = 0
        self.part_bases: list[int] = []  # each part's first byte in ``_all``
        self.reasoning_starts: list[int] = []  # each reasoning body's first byte in ``_all``
        self._shown_abs = 0  # the furthest byte of ``_all`` any grow released
        self._closed = False
        self._reasoning_count = 0
        self._withdraw_next = False  # the next reasoning close withdraws its row (a progress update)
        self._partial_grown: dict[str, int] = {}
        super().__init__(message_id, validate=validate, fence_after_tag=True)

    # ── segments ───────────────────────────────────────────────────────────────────────

    def _new_segment(self) -> None:
        super()._new_segment()
        self._seg_abs = len(self._all)
        self._sent = 0  # bytes of the segment released into the current part
        self._gi = 0  # grow pointer into the splitter's blocks
        self._preopen: tuple[int, int] | None = None  # (segment start, local) of a markdown block opened early
        self._readers: dict[int, list[Any]] = {}  # splitter idx -> [reader, fed upto, local, span start]
        # Every markdown block's reader of this segment, closed ones kept: a Stop whose cut is behind the server's
        # own position (the cancel reached the run late) closes off what was open AT THE CUT, not what is open now.
        self._spans: dict[int, list[Any]] = {}
        self._closed_idx: set[int] = set()
        self._reasoning: list[Any] | None = None  # [idx, ordinal, released upto]
        # (splitter idx, segment byte) of the open kind block's source the last ``block.partial`` covered: a
        # client draws an OPEN kind from its last partial value, never from grow text (P8-RUNS).
        self._kind_shown: tuple[int, int, int] | None = None  # (splitter idx, local index, segment byte)

    def feed(self, text: str) -> list[DataPayload]:
        if self._closed or not text:
            return []
        self._all += text.encode("utf-8")
        out = super().feed(text)
        out.extend(self._advance())
        return self._note_kind_closes(out)

    def boundary(self) -> list[DataPayload]:
        return [] if self._closed else super().boundary()

    def finish(self) -> list[DataPayload]:
        if self._closed:
            return []
        out = super().finish()
        self._closed = True
        return out

    # ── where the stop cuts ────────────────────────────────────────────────────────────

    @property
    def shown_chars(self) -> int:
        """Characters of the call's text up to the last released byte: the stopped turn saves exactly these.

        Inside an OPEN kind block, at most the source its last ``block.partial`` covered (``_open_kind_cap``)."""
        shown = self._shown_abs
        cap = self._open_kind_cap()
        if cap is not None:
            shown = min(shown, self._seg_abs + cap)
        return len(bytes(self._all[:shown]).decode("utf-8", errors="ignore"))

    def _open_kind_cap(self) -> int | None:
        """The segment byte the screen shows of the OPEN kind block: where its last ``block.partial`` read to.

        A client draws an open kind from its last partial value (``read-part-blocks``), and partials are re-read
        only every eighth of growth, so the grow watermark can run hundreds of bytes past the drawn value. A Stop
        mid-kind saves the drawn value, not the grow text (P8-RUNS, live 2026-11-15: a slow ``flashcard_set``
        stream saved 523 characters with 480 on screen). None when no kind is open or none of it was drawn yet
        (the client then draws the source so far, which IS the grow text)."""
        found = self._kind_shown
        return None if found is None else found[2]

    def _note_kind_closes(self, out: list[DataPayload]) -> list[DataPayload]:
        """Forget the drawn-kind cap once that kind's ``block.close`` goes out: the client then draws its value."""
        found = self._kind_shown
        if found is not None and any(
            isinstance(ev, BlockCloseData) and ev.index == found[1] and ev.part == self._part for ev in out
        ):
            self._kind_shown = None
        return out

    def close_off(self, cut_chars: int | None = None) -> list[DataPayload]:
        """THE stop close-off: nothing grows after this; every open region and block closes ``complete: false``
        at ``min(last watermark sent, cut_chars)``, with the saved shape of the text kept so far.

        ``cut_chars`` is where the save cuts the turn's text (``StreamEmitter.stop_cut_chars``: the last grow the
        client's ``seen_seq`` covers): the close-off and the saved row then end at the same byte."""
        if self._closed:
            return []
        cut_abs: int | None = None
        if cut_chars is not None and cut_chars >= 0:
            whole = bytes(self._all).decode("utf-8", errors="ignore")
            cut_abs = len(whole[:cut_chars].encode("utf-8"))
        self._closed = True
        # A block whose close waited for the next line (its end) closes as it stands: it was complete.
        out: list[DataPayload] = self._flush_held()
        if self._reasoning is not None:
            out.append(ReasoningCloseData(message_id=self.message_id, reasoning=self._reasoning[1], complete=False))
            self._reasoning = None
        if not self._in_part:
            return out
        upto = self._sent if cut_abs is None else max(self._base, min(self._sent, cut_abs - self._seg_abs))
        cap = self._open_kind_cap()
        if cap is not None:
            upto = max(self._base, min(upto, cap))  # an open kind closes at the value the screen drew
        watermark = upto - self._base
        shown = bytes(self._raw[self._base : upto]).decode("utf-8", errors="ignore")
        saved = {b["start"]: b for b in blocks_v1_dicts(shown, fence_after_tag=True)} if shown else {}
        out.extend(self._withdraw_regions_past(watermark))
        opened: list[tuple[int, int, int]] = []  # (local, segment start, idx or -1)
        for idx, local in self._map.items():
            if local is None:
                continue
            if idx in self._closed_idx:
                # Closed already — but if the server closed it PAST the cut (it kept reading after the press), the
                # cut leaves it open: it closes again, ``complete: false``, at the cut.
                b = self._splitter.blocks[idx]
                if not (b.start < upto < b.end) or self._only_breaks(upto, b.end):
                    continue
            opened.append((local, self._splitter.blocks[idx].start, idx))
        if self._preopen is not None:
            opened.append((self._preopen[1], self._preopen[0], -1))
        for local, seg_start, idx in sorted(opened):
            start = max(0, seg_start - self._base)
            entry = self._spans.get(idx)
            if entry is not None:
                for ordinal, region in enumerate(entry[0].regions):
                    shift = entry[3] - self._base
                    begins = region.start + shift
                    # Open at the cut: still open now, or closed by the server after the cut. A region that closed
                    # at or before the cut, or opened and closed wholly past it, is left as announced.
                    if region.end is not None and (
                        not (begins < watermark < region.end + shift)
                        or self._only_breaks(upto, region.end + entry[3])
                    ):
                        continue
                    end = max(begins, watermark)
                    region.end = end - shift
                    region.complete = False
                    out.append(
                        RegionCloseData(
                            message_id=self.message_id,
                            part=self._part,
                            index=local,
                            region=ordinal,
                            end=max(0, end),
                            complete=False,
                            language=region.language,
                        )
                    )
            block = dict(saved.get(start) or {"type": self._block_type(idx), "start": start, "end": watermark})
            block.pop("regions", None)
            block["end"] = max(start, watermark)
            if block["type"] != "markdown":
                block["complete"] = False
            out.append(
                BlockCloseData(
                    message_id=self.message_id,
                    part=self._part,
                    index=local,
                    end=max(start, watermark),
                    complete=False,
                    block=block,
                )
            )
        return out

    def _withdraw_regions_past(self, watermark: int) -> list[DataPayload]:
        """Every region the server announced AND closed that begins at or past the cut is WITHDRAWN: a ``region.close``
        ``complete: false`` whose ``end`` is its own ``start`` (an empty region). The vocabulary has no region retract,
        so this is the contract: a client drops a region closed ``complete: false`` at ``end <= start``. The saved row
        keeps no such region (its text ends at the cut), so a replay or a reader whose cursor ran ahead ends with the
        saved row's regions only."""
        out: list[DataPayload] = []
        for idx, local in self._map.items():
            entry = self._spans.get(idx)
            if local is None or entry is None:
                continue
            shift = entry[3] - self._base
            for ordinal, region in enumerate(entry[0].regions):
                begins = region.start + shift
                if region.end is None or begins < watermark:
                    continue
                region.end = begins - shift
                region.complete = False
                out.append(
                    RegionCloseData(
                        message_id=self.message_id,
                        part=self._part,
                        index=local,
                        region=ordinal,
                        end=max(0, begins),
                        complete=False,
                        language=region.language,
                    )
                )
        return out

    def _only_breaks(self, start: int, end: int) -> bool:
        """Segment bytes ``[start, end)`` are line breaks only: a close that far past the cut showed
        everything it closed (the watermark trims trailing breaks), so the cut does not reopen it."""
        return not bytes(self._raw[start:end]).strip(b"\r\n")

    def _partial(self) -> list[DataPayload]:
        """v1's open-kind partials, re-read only after the source grew by an eighth (at least 64 bytes):
        each re-read parses the whole value so far, so per line it is quadratic on a long kind; this keeps
        the per-token CPU bounded (T1 v2.1 budget) while values still only grow. v1 clients keep per-line."""
        opened = self._splitter.open_kind_source()
        if opened is None:
            return []
        idx, source, _slug = opened
        key = self._block_key(idx)
        last = self._partial_grown.get(key, 0)
        if last and len(source) < last + max(64, last // 8):
            return []
        out = super()._partial()
        if out or key in self._partial_seen:
            self._partial_grown[key] = len(source)
        local = self._map.get(idx)
        if out and local is not None:
            self._kind_shown = (idx, local, self._splitter.blocks[idx].end)
        return out

    def _block_type(self, idx: int) -> str:
        return "markdown" if idx < 0 else self._splitter.blocks[idx].type

    # ── hooks from the v1 translation ──────────────────────────────────────────────────

    def _ensure_part(self, out: list[DataPayload], start: int) -> None:
        was = self._in_part
        super()._ensure_part(out, start)
        if not was:
            self._sent = self._base
            self.part_bases.append(self._seg_abs + self._base)

    def _open_local(self, out: list[DataPayload], idx: int, block_type: str, start: int) -> None:
        super()._open_local(out, idx, block_type, start)
        if block_type == "markdown":
            self._readers[idx] = [RegionReader(), max(start, self._base), self._map[idx], max(start, self._base)]
            self._spans[idx] = self._readers[idx]

    def _adopt_markdown(self, idx: int, block: Any) -> bool:
        pre = self._preopen
        if pre is None or pre[0] != block.start:
            return False
        self._preopen = None
        self._map[idx] = pre[1]
        start = max(block.start, self._base)
        self._readers[idx] = [RegionReader(), start, pre[1], start]
        self._spans[idx] = self._readers[idx]
        return True

    def _on_reasoning_open(self, out: list[DataPayload], idx: int, block: Any) -> None:
        op = self._splitter._open
        body_start = op.body_start if op is not None and op.block is block else block.fields.get("body_start", block.start)
        ordinal = self._reasoning_count
        self._reasoning_count += 1
        self.reasoning_starts.append(self._seg_abs + body_start)
        self._reasoning = [idx, ordinal, body_start]
        out.append(
            ReasoningOpenData(
                message_id=self.message_id,
                reasoning=ordinal,
                position=self._part + 1,
                tag=str(block.fields.get("tag") or "reasoning"),
                label=DIGEST_LABEL if block.fields.get("tag") == DIGEST_TAG else None,
            )
        )

    def _on_reasoning_close(self, out: list[DataPayload], idx: int, block: Any) -> None:
        r = self._reasoning
        if r is None or r[0] != idx:
            return
        self._reasoning_grow(out, int(block.fields.get("body_end", block.end)))
        withdrawn = True if self._withdraw_next else None
        self._withdraw_next = False
        out.append(ReasoningCloseData(message_id=self.message_id, reasoning=r[1], complete=bool(block.complete), withdrawn=withdrawn))
        self._reasoning = None

    def withdraw_reasoning(self) -> None:
        """The open reasoning turned out to be a progress update (sent again as reply text): its close carries
        ``withdrawn: true`` so the client removes the row. Applies to the NEXT reasoning close only."""
        if self._reasoning is not None:
            self._withdraw_next = True

    def _before_close(self, out: list[DataPayload], idx: int, local: int, end: int, block: Any, complete: bool) -> bool:
        self._grow_to(out, end, trim=False)
        self._closed_idx.add(idx)
        entry = self._readers.pop(idx, None)
        if entry is None or block.type != "markdown":
            return complete
        reader, fed, _local, span_start = entry
        steps = reader.feed(bytes(self._raw[fed:end])) if end > fed else RegionEvents()
        span = bytes(self._raw[span_start:end])
        fin = reader.finish(span)
        steps.steps.extend(fin.steps)
        self._emit_regions(out, local, reader, steps, span_start)
        if reader.anomaly:
            raise RegionDisagreement(reader.anomaly)
        return all(r.complete is not False for r in reader.regions)

    # ── the live step: regions, then text ──────────────────────────────────────────────

    def _advance(self) -> list[DataPayload]:
        out: list[DataPayload] = []
        sp = self._splitter
        op = sp._open
        if op is not None and op.block.type == "reasoning" and self._reasoning is not None:
            pending = sp._pending
            if op.mode == "digest":
                # The digest runs to its json fence: only a line that could BE that fence waits.
                prefix = "" if pending.lstrip(" \t")[:1] in ("", "`") else pending
            else:
                cut = pending.find("<")
                prefix = pending if cut < 0 else pending[:cut]
            self._reasoning_grow(out, sp._pos + len(prefix.encode("utf-8")))
            return out
        steps: RegionEvents | None = None
        entry: list[Any] | None = None
        if sp._md is not None:
            idx = len(sp.blocks) - 1
            entry = self._readers.get(idx)
            if entry is not None and sp._md.end > entry[1]:
                steps = entry[0].feed(bytes(self._raw[entry[1] : sp._md.end]))
                entry[1] = sp._md.end
        target, extend = self._safe(entry)
        self._grow_to(out, target, trim=True, extend=extend)
        if steps is not None and entry is not None and steps.steps:
            self._emit_regions(out, entry[2], entry[0], steps, entry[3])
            if entry[0].anomaly:
                raise RegionDisagreement(entry[0].anomaly)
        return out

    def _safe(self, entry: list[Any] | None) -> tuple[int, bool]:
        """The segment byte the text may be released to now, and whether it runs past the committed lines."""
        sp = self._splitter
        if sp._hold is not None:
            return sp._hold.start, False
        if sp._open is not None:
            return sp._pos, False
        committed = sp._pos
        reader: RegionReader | None = entry[0] if entry is not None else None
        open_regions = reader.open_regions if reader is not None else []
        open_fence = next((r for _, r in open_regions if r.type == "code"), None)
        in_table = any(r.type == "table" for _, r in open_regions)
        # The first line of the text may be the grounded digest's heading: a line that could still become it waits.
        if not sp.seen_text and sp._pending and sp._open is None and could_become_digest_heading(sp._pending):
            return committed, False
        # A ``|`` line outside any region may be a table header: it waits for the next line.
        if not open_regions and sp._fence is None and committed > 0:
            line_start = self._raw.rfind(b"\n", 0, committed - 1) + 1
            if b"|" in self._raw[line_start:committed]:
                return line_start, False
        pending = sp._pending
        if not pending or in_table:
            return committed, False
        marker = None
        if open_fence is not None or sp._fence is not None:
            marker = "~" if (open_fence is not None and self._fence_char(entry, open_fence) == "~") else "`"
        prefix = releasable_prefix(pending, in_fence_marker=marker)
        if not prefix:
            return committed, False
        return committed + len(prefix.encode("utf-8")), True

    def _fence_char(self, entry: list[Any] | None, region: Any) -> str:
        if entry is None:
            return "`"
        line = bytes(self._raw[entry[3] + region.start : entry[3] + region.start + 400]).split(b"\n", 1)[0]
        body = line.lstrip(b" \t>-*+0123456789.)")
        return "~" if body[:1] == b"~" else "`"

    def _grow_to(self, out: list[DataPayload], target: int, *, trim: bool, extend: bool = False) -> None:
        raw = self._raw
        if trim:
            while target > self._sent and raw[target - 1] in _BREAKS:
                target -= 1
        if extend:
            self._open_for_pending(out)
        if not self._in_part or target <= self._sent:
            return
        blocks = self._splitter.blocks
        while self._sent < target:
            s = self._sent
            while self._gi + 1 < len(blocks) and blocks[self._gi + 1].start <= s:
                self._gi += 1
            local: int | None = None
            seg_end = target
            if blocks and blocks[self._gi].start <= s < blocks[self._gi].end:
                b = blocks[self._gi]
                local = self._map.get(self._gi)
                is_open_tail = self._gi == len(blocks) - 1 and self._splitter._md is b
                if not is_open_tail:
                    seg_end = min(target, b.end)
            elif self._preopen is not None and s >= self._preopen[0]:
                local = self._preopen[1]
            elif blocks and self._gi == len(blocks) - 1 and self._splitter._md is blocks[self._gi]:
                local = self._map.get(self._gi)
            if local is None:
                self._sent = seg_end  # bytes the save does not keep in this part (breaks beside a region)
                continue
            text = bytes(raw[s:seg_end]).decode("utf-8", errors="ignore")
            self._sent = seg_end
            self._shown_abs = max(self._shown_abs, self._seg_abs + seg_end)
            out.append(
                BlockGrowData(
                    message_id=self.message_id,
                    part=self._part,
                    index=local,
                    end=seg_end - self._base,
                    text=text,
                )
            )

    def _open_for_pending(self, out: list[DataPayload]) -> None:
        """The unfinished line will be markdown: make sure its block is announced before its first word."""
        sp = self._splitter
        if sp._md is not None:
            idx = len(sp.blocks) - 1
            if idx in self._map:
                return
            if idx in self._deferred:
                self._deferred.pop(idx)
                self._ensure_part(out, sp._md.start)
                self._open_local(out, idx, "markdown", sp._md.start)
            return
        if self._preopen is not None:
            return
        start = sp._pos
        self._ensure_part(out, start)
        local = self._local
        self._local += 1
        self._preopen = (start, local)
        out.append(
            BlockOpenData(
                message_id=self.message_id,
                part=self._part,
                index=local,
                block_type="markdown",
                start=max(0, start - self._base),
            )
        )

    def _reasoning_grow(self, out: list[DataPayload], target: int) -> None:
        r = self._reasoning
        if r is None or target <= r[2]:
            return
        text = bytes(self._raw[r[2] : target]).decode("utf-8", errors="ignore")
        r[2] = target
        self._shown_abs = max(self._shown_abs, self._seg_abs + target)
        out.append(ReasoningGrowData(message_id=self.message_id, reasoning=r[1], text=text))

    def _emit_regions(
        self, out: list[DataPayload], local: int, reader: RegionReader, steps: RegionEvents, span_start: int
    ) -> None:
        shift = span_start - self._base
        for step, ordinal in steps.steps:
            region = reader.regions[ordinal]
            if step == "open":
                region_kind, display = region_kind_and_display(region.type, region.language)
                out.append(
                    RegionOpenData(
                        message_id=self.message_id,
                        part=self._part,
                        index=local,
                        region=ordinal,
                        region_kind=region_kind,  # type: ignore[arg-type]
                        display=display,
                        language=region.language,
                        start=region.start + shift,
                        container=region.container,  # type: ignore[arg-type]
                    )
                )
            elif step == "partial":
                out.append(
                    RegionPartialData(
                        message_id=self.message_id, part=self._part, index=local, region=ordinal, rows=region.rows
                    )
                )
            else:
                out.append(
                    RegionCloseData(
                        message_id=self.message_id,
                        part=self._part,
                        index=local,
                        region=ordinal,
                        end=(region.end or 0) + shift,
                        complete=region.complete is not False,
                        language=region.language,
                    )
                )


class RegionDisagreement(RuntimeError):
    """The live region reader and the save's ``markdown_regions`` disagree: the stream degrades, loudly."""


def watermark_cut_chars(text: str, *, part: int | None = None, end: int | None = None, reasoning: int | None = None, reasoning_len: int = 0) -> int:
    """Where the stopped turn's text is cut for a watermark the client was sent (the LATE stop door).

    ``text`` is the turn's whole text (its chunk frames); the watermark is the last ``block.grow``
    (``part``, ``end``) or ``reasoning.grow`` (``reasoning`` ordinal, bytes of body sent ``reasoning_len``).
    The same stream the live door uses reads it, so both doors cut at the same byte."""
    stream = LiveBlocksStreamV2("cut")
    stream.feed(text)
    stream.finish()
    raw = bytes(stream._all)
    if reasoning is not None and reasoning < len(stream.reasoning_starts):
        at = stream.reasoning_starts[reasoning] + reasoning_len
    elif part is not None and part < len(stream.part_bases):
        at = stream.part_bases[part] + (end or 0)
    else:
        at = 0
    return len(raw[: min(at, len(raw))].decode("utf-8", errors="ignore"))


__all__ = ["LiveBlocksStreamV2", "RegionDisagreement", "releasable_prefix", "watermark_cut_chars"]
