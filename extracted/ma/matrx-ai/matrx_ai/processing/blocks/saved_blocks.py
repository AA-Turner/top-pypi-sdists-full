"""Saved reply blocks — the fields a text part carries once the server's one splitter has read it.

PF-1 (saved equals streamed): ``chat.message`` text parts carry ``blocks_version``, ``blocks_of``
and ``blocks`` (models in :mod:`matrx_ai.db.message_parts`). ``blocks_of`` is md5 of the text as
stored; the database drops blocks whose text changed (trigger ``chat.zz_blocks_are_derived``), so
any reader can trust blocks that are present. Lane: common-docs/systems/chat/projects/chat-ground-up/PF-1-saved-equals-streamed.md.
"""

from __future__ import annotations

import hashlib
import json
import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from matrx_ai.processing.blocks.blocks_v1 import (
    BLOCKS_VERSION,
    Block,
    KindValidator,
    blocks_v1_dicts,
    kind_validator,
)

logger = logging.getLogger(__name__)

BLOCK_FIELDS: tuple[str, ...] = ("blocks_version", "blocks_of", "blocks")


def text_fingerprint(text: str) -> str:
    """md5 hex of the text's UTF-8 bytes — equal to Postgres ``md5(text)`` on a UTF-8 database."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()  # noqa: S324 — a fingerprint, not security


def has_current_blocks(part: dict[str, Any]) -> bool:
    text = part.get("text")
    return (
        part.get("type") == "text"
        and isinstance(text, str)
        and part.get("blocks_version") == BLOCKS_VERSION
        and isinstance(part.get("blocks"), list)
        and part.get("blocks_of") == text_fingerprint(text)
    )


@dataclass(frozen=True, slots=True)
class ReplyContract:
    """What a structured run's answer is, known before the reply is saved (PF-1 D3b).

    ``kind`` is a REGISTERED kind slug (else None); ``schema_name`` is the output schema's name.
    The run sets it on its ``ExecutionState``; the save funnel reads it there.
    """

    kind: str | None = None
    schema_name: str | None = None


def reply_contract_for(envelope: dict[str, Any] | None, metadata: dict[str, Any] | None) -> ReplyContract | None:
    """The contract of a run whose structured contract is ``envelope`` (the ``json_schema`` envelope), or None.

    The kind is the host's resolved run contract (``metadata["structured_output_content_ir"]["kind"]``,
    registered by construction), else the schema's root ``__kind`` const when that names a bindable,
    registered kind. A schema naming no kind saves its answer as a ``data`` block.
    """
    if not isinstance(envelope, dict):
        return None
    from matrx_ai.kinds import is_bindable_kind, root_kind_const

    meta = (metadata or {}).get("structured_output_content_ir") if isinstance(metadata, dict) else None
    kind = meta.get("kind") if isinstance(meta, dict) else None
    if not (isinstance(kind, str) and is_bindable_kind(kind)):
        kind = root_kind_const(envelope)
        if not (isinstance(kind, str) and is_bindable_kind(kind) and _kind_is_registered(kind)):
            kind = None
    name = envelope.get("name")
    return ReplyContract(kind=kind, schema_name=name if isinstance(name, str) and name else None)


def _kind_is_registered(slug: str) -> bool:
    # A cold registry cannot say no: the slug stands and validation records ``unchecked``.
    from matrx_ai.processing.blocks import kind_catalog

    return not kind_catalog.snapshot_is_warm() or kind_catalog.is_registered_kind(slug)


def _contract_block(
    text: str, blocks: list[dict[str, Any]], contract: ReplyContract, validate: KindValidator | None
) -> dict[str, Any] | None:
    """The one block over a whole-JSON text answered under ``contract``, or None to keep the splitter's.

    The text is never touched. A kind contract restores ``__kind`` on the VALUE, first key, root only, never
    over a marker the model wrote: the marker is data the run's registered contract declares — the
    settlement-stamping door of the marker law (``matrx_graph.content_ir.envelope.stamp_kind_marker``,
    KINDS_EVERYWHERE §4.2a; content-ir FEATURE rules 2-3). The provider schema had it stripped at the
    prompt door (``strip_kind_markers``); the saved instance carries it. The validator records the
    verdict on the block (an invalid one keeps its errors). A schema with no kind gives a ``data`` block.
    """
    if any(b.get("type") == "kind" for b in blocks):
        return None  # the model wrote its own marker; the splitter already read it
    body = text.strip()
    if not body or body[0] not in "{[" or body[-1] not in "}]":
        return None
    try:
        value = json.loads(body)
    except ValueError:
        return None
    end = len(text.encode("utf-8"))
    if contract.kind and isinstance(value, dict) and "__kind" not in value:
        block = Block(
            type="kind",
            start=0,
            end=end,
            fields={
                "kind": contract.kind,
                "kind_version": None,
                "array": False,
                "value": {"__kind": contract.kind, **value},
                "status": "unchecked",
                "errors": [],
            },
        )
        if validate is not None:
            validate(block)
        return block.to_dict()
    if isinstance(value, (dict, list)):
        return {"type": "data", "start": 0, "end": end, "complete": True, "schema_name": contract.schema_name, "value": value}
    return None


def block_fields(
    text: str,
    *,
    validate: KindValidator | None = None,
    contract: ReplyContract | None = None,
    citations: Any = None,
    stopped: bool = False,
) -> dict[str, Any]:
    """The fields for one text: version, fingerprint and the blocks that tile it (v1, unchanged for installed
    readers) and, while the v2 save knob is on, ``blocks2`` — the full reading, a sibling key, never inside v1."""
    blocks = blocks_v1_dicts(text, validate=validate)
    if contract is not None:
        whole = _contract_block(text, blocks, contract, validate)
        if whole is not None:
            blocks = [whole]
    v2 = None
    if blocks_v2_save_enabled():
        # blocks2 reads its own splitter pass (a fence right after a tag close is a fence); v1 `blocks` stay as www reads them.
        v2_blocks = blocks_v1_dicts(text, validate=validate, fence_after_tag=True)
        if contract is not None:
            whole2 = _contract_block(text, v2_blocks, contract, validate)
            if whole2 is not None:
                v2_blocks = [whole2]
        v2 = blocks2_reading(text, v2_blocks, citations=citations, stopped=stopped)
    if not regions_save_enabled():
        for b in blocks:
            b.pop("regions", None)
    fields: dict[str, Any] = {
        "blocks_version": BLOCKS_VERSION,
        "blocks_of": text_fingerprint(text),
        "blocks": blocks,
    }
    if v2 is not None:
        fields[BLOCKS2_FIELD] = v2
    return fields


#: The saved key of the full v2 reading (P1-CHAT T1 v2.1), beside the v1 fields.
BLOCKS2_FIELD = "blocks2"
BLOCKS2_VERSION = 2


def blocks2_reading(
    text: str, blocks: list[dict[str, Any]], *, citations: Any = None, stopped: bool = False
) -> dict[str, Any]:
    """``blocks2`` for one text part: the v1 blocks (the one splitter's tiling) read in full by the live v2 reader.

    Markdown blocks get their regions from :class:`RegionReader` — the reader the live ``region.*`` events come
    from, property-tested equal to the save's ``markdown_regions`` — so ``region_kind`` / ``display`` / ``container``
    / ``complete`` are the very values the stream announced. Every block carries ``complete``; the grounded digest
    its ``label``. ``stopped`` (the last text part of a reply the person stopped) closes the LAST block and the
    region still open in it ``complete: false``, as the live close-off did. One reading: no second parser.
    """
    import copy

    from matrx_ai.processing.blocks.blocks_v1 import DIGEST_LABEL, DIGEST_TAG

    raw = text.encode("utf-8")
    out: list[dict[str, Any]] = []
    last = len(blocks) - 1
    for i, block in enumerate(blocks):
        b = copy.deepcopy(block)
        cut = stopped and i == last
        if b.get("type") == "markdown":
            regions = _regions2(raw, int(b["start"]), int(b["end"]), cut=cut)
            b["regions"] = regions
            b["complete"] = (not cut) and all(r["complete"] for r in regions)
        else:
            b["complete"] = False if cut else b.get("complete", True) is not False
            if b.get("type") == "reasoning" and b.get("tag") == DIGEST_TAG:
                b["label"] = DIGEST_LABEL  # the server names the digest; the client never guesses
        out.append(b)
    reading: dict[str, Any] = {"version": BLOCKS2_VERSION, "of": text_fingerprint(text), "blocks": out}
    if isinstance(citations, list) and citations:
        reading["citations"] = [c for c in citations if isinstance(c, dict)]
    if stopped:
        reading["stopped"] = True
    return reading


def _regions2(raw: bytes, start: int, end: int, *, cut: bool) -> list[dict[str, Any]]:
    from matrx_ai.processing.blocks.region_reader import RegionReader, region_kind_and_display

    span = raw[start:end]
    reader = RegionReader()
    # Regions move on complete lines: the block's last line is read as one (the save's parser decides the ends).
    reader.feed(span if span.endswith(b"\n") else span + b"\n")
    reader.finish(span, cut=cut)
    if reader.anomaly:
        # The live reader and the save's parser disagree: the save's parser wins (what v1 saves), said, never silent.
        _announce("blocks2_anomaly", f"saved blocks2: region reader disagreed with the save ({reader.anomaly}); saved regions kept")
        from matrx_ai.processing.blocks.markdown_regions import markdown_regions
        from matrx_ai.processing.blocks.region_reader import _closed_flags

        final = markdown_regions(span, 0, all_kinds=True)
        rows = [
            (r["type"], r["start"], r["end"], r.get("language"), None, closed and not cut)
            for r, closed in zip(final, _closed_flags(span, final), strict=True)
        ]
    else:
        rows = [
            (r.type, r.start, r.end if r.end is not None else len(span), r.language, r.container, r.complete is not False)
            for r in sorted(reader.regions, key=lambda r: r.start)
        ]
    out: list[dict[str, Any]] = []
    for kind, r_start, r_end, language, container, complete in rows:
        region_kind, display = region_kind_and_display(kind, language)
        region: dict[str, Any] = {
            "region_kind": region_kind,
            "display": display,
            "start": start + r_start,
            "end": start + min(r_end, len(span)),
            "complete": bool(complete),
        }
        if language is not None:
            region["language"] = language
        if container:
            region["container"] = list(container)
        out.append(region)
    return out


def blocks2_is_current(part: dict[str, Any]) -> bool:
    """``blocks2`` describes the part's current text (whatever its stop mark)."""
    reading = part.get(BLOCKS2_FIELD)
    text = part.get("text")
    return isinstance(reading, dict) and isinstance(text, str) and reading.get("of") == text_fingerprint(text)


def has_current_blocks2(part: dict[str, Any], *, stopped: bool = False) -> bool:
    """The part carries a ``blocks2`` reading of its current text (and of its stop: a stopped part is marked)."""
    reading = part.get(BLOCKS2_FIELD)
    text = part.get("text")
    return (
        isinstance(reading, dict)
        and isinstance(text, str)
        and reading.get("version") == BLOCKS2_VERSION
        and isinstance(reading.get("blocks"), list)
        and reading.get("of") == text_fingerprint(text)
        and bool(reading.get("stopped")) == stopped
    )


_enabled: Callable[[], bool] | None = None
_regions_enabled: Callable[[], bool] | None = None


def configure_block_regions_save(enabled: Callable[[], bool] | None) -> None:
    """Bind whether saved (and announced) markdown blocks carry ``regions`` (PF-1 D9), or None for off.

    Off until every reader's generated ``MessagePart`` guard declares ``MarkdownRegion``: a guard built
    before it rejects a markdown block with an undeclared ``regions`` key, which blanks the reply
    (the strip of additive keys covers top-level part keys only). Same rollout rule as ``canvas``.
    """
    global _regions_enabled
    _regions_enabled = enabled


def regions_save_enabled() -> bool:
    fn = _regions_enabled
    if fn is None:
        return False
    try:
        return bool(fn())
    except Exception as exc:  # noqa: BLE001 — a switch that cannot be read is off, announced once
        _announce("regions_switch", f"saved blocks: regions switch could not be read ({exc!r}); regions not saved")
        return False
_canvas_materializer: Callable[[list[str]], Awaitable[None]] | None = None


def configure_canvas_materializer(materialize: Callable[[list[str]], Awaitable[None]] | None) -> None:
    """Bind the host's canvas step for saved replies (PF-1 D7), or None for none.

    The host makes each saved reply's canvas rows from its blocks and records each row ON its block
    (``canvas``); it needs the message row to exist, so the Coordinator awaits it with the ids of the
    assistant rows it saved, after each successful synchronous commit (``finalize``). The host decides
    whether it runs (its own switch); the package only carries the ids.
    """
    global _canvas_materializer
    _canvas_materializer = materialize


def canvas_materializer() -> Callable[[list[str]], Awaitable[None]] | None:
    return _canvas_materializer


_announced: set[str] = set()


_v2_enabled: Callable[[], bool] | None = None


def configure_blocks_v2_save(enabled: Callable[[], bool] | None) -> None:
    """P1-CHAT T1 v2.1: the switch that saves each text part's full reading as ``blocks2`` (a sibling key of the
    unchanged v1 fields; ``message_blocks`` carries it and the part's ``citations``). aidream binds it to
    ``platform.debug.blocks_v2_save_enabled`` (everyone) or ``blocks_v2_save_test_seats`` (agent test seats only).
    Unconfigured = off."""
    global _v2_enabled
    _v2_enabled = enabled


def blocks_v2_save_enabled() -> bool:
    fn = _v2_enabled
    if fn is None:
        return False
    try:
        return bool(fn())
    except Exception:  # noqa: BLE001 — an unreadable switch is off
        return False


_force_degraded: Callable[[], bool] | None = None


def configure_force_blocks_degraded(enabled: Callable[[], bool] | None) -> None:
    """A DEBUG switch for proof: on, a blocks-v2 turn sends ``blocks.degraded {reason: "forced_by_debug_knob"}`` at
    its start and streams the reply as the plain tail. aidream binds it to ``platform.debug.force_blocks_degraded``
    honoured only on agent test seats' requests. Unconfigured = off."""
    global _force_degraded
    _force_degraded = enabled


def force_blocks_degraded() -> bool:
    fn = _force_degraded
    if fn is None:
        return False
    try:
        return bool(fn())
    except Exception:  # noqa: BLE001 — an unreadable debug switch is off
        return False


def configure_blocks_save(enabled: Callable[[], bool] | None) -> None:
    """Bind the save switch to the host's setting (a zero-arg callable), or None for off."""
    global _enabled
    _enabled = enabled


def blocks_save_enabled() -> bool:
    fn = _enabled
    if fn is None:
        return False
    try:
        return bool(fn())
    except Exception as exc:  # noqa: BLE001 — a switch that cannot be read saves, announced once
        # Blocks are derived data (the database drops stale ones, every reader tolerates them), so a
        # process that cannot read its switch — a script that never loaded the server's settings —
        # saves them rather than silently writing replies without (4 such rows on 2026-11-02).
        _announce("switch", f"saved blocks: switch could not be read ({exc!r}); saving blocks anyway")
        return True


def _announce(key: str, message: str) -> None:
    if key not in _announced:
        _announced.add(key)
        logger.warning(message)


def annotate_content(
    content: Any, *, validate: KindValidator | None = None, contract: ReplyContract | None = None, stopped: bool = False
) -> Any:
    """``content`` with every text part that lacks current blocks given them; anything else untouched.

    ``stopped`` (the row's ``metadata.stopped``: the person stopped this reply) marks the LAST text part's
    ``blocks2`` stopped, its open block and region ``complete: false``. v1 never changes for it.

    ``contract`` (a structured run's, PF-1 D3b) turns a whole-JSON text part into one ``kind`` or
    ``data`` block; without it the splitter alone decides.

    Returns the same object when nothing changed. A part the splitter cannot read keeps no blocks
    (the reader asks the heal door) and the failure is captured, never raised into the save.
    """
    if not isinstance(content, list):
        return content
    out: list[Any] | None = None
    v2 = blocks_v2_save_enabled()
    last_text = max(
        (i for i, p in enumerate(content) if isinstance(p, dict) and p.get("type") == "text" and isinstance(p.get("text"), str)),
        default=-1,
    )
    for i, part in enumerate(content):
        if not isinstance(part, dict) or part.get("type") != "text" or not isinstance(part.get("text"), str):
            continue
        part_stopped = stopped and i == last_text
        v1_current = has_current_blocks(part)
        if v1_current and (not v2 or has_current_blocks2(part, stopped=part_stopped)):
            continue
        try:
            if v1_current:
                # v1 stays exactly as saved (its canvas refs included); only the v2 reading is added.
                fields = {
                    BLOCKS2_FIELD: blocks2_reading(
                        part["text"], part["blocks"], citations=part.get("citations"), stopped=part_stopped
                    )
                }
            else:
                fields = block_fields(
                    part["text"],
                    validate=validate if validate is not None else kind_validator(),
                    contract=contract,
                    citations=part.get("citations"),
                    stopped=part_stopped,
                )
        except Exception as exc:  # noqa: BLE001 — a failed split never fails the save
            _capture_split_failure(exc, chars=len(part["text"]))
            continue
        if out is None:
            out = list(content)
        out[i] = {**part, **fields}
    return content if out is None else out


def _capture_split_failure(exc: BaseException, *, chars: int) -> None:
    logger.error("saved blocks: the splitter failed on a %d-char text part (%r); saved without blocks", chars, exc)
    try:
        from matrx_connect.streaming.error_capture import capture_error
        from matrx_utils import detached_task

        detached_task(capture_error(exc, kind="saved_blocks_split_failed", chars=chars), name="saved_blocks_capture")
    except Exception as capture_exc:  # noqa: BLE001 — capture is best effort; the log line above is the floor
        _announce("capture", f"saved blocks: failure capture unavailable ({capture_exc!r})")


async def warm_kind_registry() -> None:
    """Make sure kind blocks are validated when saved: load the registry listing (TTL-cached).

    Without it the funnel saves every kind ``unchecked`` ("kind registry not loaded"), because
    only the old engine's stream path ever primed it (found live, 2026-11-01). A failure is said
    and leaves the save to record ``unchecked`` honestly; it never fails the call.
    """
    from matrx_ai.processing.blocks.blocks_shadow import shadow_enabled

    if not (blocks_save_enabled() or shadow_enabled()):
        return
    try:
        from matrx_ai.processing.blocks.kind_catalog import prime_registered_kinds

        await prime_registered_kinds()
    except Exception as exc:  # noqa: BLE001 — a cold registry is recorded on the blocks, never raised
        logger.warning("saved blocks: kind registry could not be loaded (%r); kinds save as unchecked", exc)


_pending: set[Any] = set()

#: Where a run's context keeps the reply shapes its client reads (``ClientContext.reads``), set at the agent-run boundary.
CLIENT_READS_METADATA_KEY = "client_reads"
#: The shape the ``message_blocks`` event carries.
BLOCKS_V1_READ = "blocks-v1"
#: The live blocks v2 contract (P1-CHAT T1 v2.1): grow text, regions, reasoning, degraded, stop close-off.
BLOCKS_V2_READ = "blocks-v2"


def metadata_with_client_reads(metadata: dict[str, Any], client: Any) -> dict[str, Any]:
    """The run metadata carrying what its client reads (``client.reads``), unchanged when it names nothing."""
    reads = getattr(client, "reads", None)
    if not isinstance(reads, list) or not reads:
        return metadata
    return {**metadata, CLIENT_READS_METADATA_KEY: [str(r) for r in reads if isinstance(r, str)]}


def client_reads(ctx: Any, shape: str) -> bool:
    """Did this run's client say it reads ``shape``?"""
    metadata = getattr(ctx, "metadata", None)
    reads = metadata.get(CLIENT_READS_METADATA_KEY) if isinstance(metadata, dict) else None
    return isinstance(reads, list) and shape in reads



def message_blocks_payload(message_id: str, content: Any) -> Any | None:
    """The ``message_blocks`` data event for one saved message, or None when no text part has blocks."""
    from matrx_connect.context.data_types import MessageBlocksData

    parts = [
        {
            "index": i,
            "id": p.get("id") or "",
            "text": p["text"],
            **{k: p[k] for k in BLOCK_FIELDS},
            # Text a tool call follows (blocks/interim_text.py): the client draws it as a progress note.
            # Key for key with the row (T1 v2 item 6): present only when the row carries it.
            **({"interim": p["interim"] is True} if "interim" in p else {}),
            # T1 v2.1 staged: citations ride message_blocks only while the v2 save knob is on.
            **({"citations": p["citations"]} if blocks_v2_save_enabled() and isinstance(p.get("citations"), list) else {}),
            # T1 v2.1: the part's full reading, the same object the row saves — live and saved are one.
            **({BLOCKS2_FIELD: p[BLOCKS2_FIELD]} if blocks2_is_current(p) else {}),
        }
        for i, p in enumerate(content if isinstance(content, list) else [])
        if isinstance(p, dict) and has_current_blocks(p)
    ]
    return MessageBlocksData(message_id=message_id, parts=parts) if parts else None


def announce_message_blocks(message_id: str, content: Any, emitter: Any) -> None:
    """Send the saved message's blocks on the request's stream (scheduled; never blocks or fails the save).

    The client replaces the message's text parts with these, so what it shows is what was saved.
    """
    if emitter is None or not message_id:
        return
    try:
        payload = message_blocks_payload(message_id, content)
        if payload is None:
            return
        import asyncio

        loop = asyncio.get_running_loop()
    except RuntimeError:
        return  # no running loop: a synchronous writer has no stream to announce on
    except Exception as exc:  # noqa: BLE001 — announcing never fails the save
        _announce("payload", f"saved blocks: message_blocks event could not be built ({exc!r})")
        return

    async def _send() -> None:
        try:
            await emitter.send_data(payload)
        except Exception as exc:  # noqa: BLE001 — a closed stream is not a failed save
            # Every lost event is said (never once per process): the reply then shows its streamed
            # text until reload, so a silent loss would hide a real difference.
            logger.warning("saved blocks: message_blocks event for %s not sent (%r)", message_id, exc)

    task = loop.create_task(_send(), name="saved_blocks_announce")
    _pending.add(task)
    task.add_done_callback(_pending.discard)


async def settle_announcements() -> None:
    """Wait for every ``message_blocks`` announcement already scheduled (live blocks orders the wire with it)."""
    if not _pending:
        return
    import asyncio

    await asyncio.gather(*list(_pending), return_exceptions=True)


__all__ = [
    "settle_announcements",
    "BLOCK_FIELDS",
    "ReplyContract",
    "reply_contract_for",
    "announce_message_blocks",
    "BLOCKS_V1_READ",
    "BLOCKS_V2_READ",
    "CLIENT_READS_METADATA_KEY",
    "client_reads",
    "metadata_with_client_reads",
    "warm_kind_registry",
    "message_blocks_payload",
    "annotate_content",
    "block_fields",
    "blocks2_reading",
    "blocks2_is_current",
    "has_current_blocks2",
    "BLOCKS2_FIELD",
    "blocks_save_enabled",
    "configure_block_regions_save",
    "configure_blocks_v2_save",
    "configure_force_blocks_degraded",
    "force_blocks_degraded",
    "blocks_v2_save_enabled",
    "configure_blocks_save",
    "regions_save_enabled",
    "has_current_blocks",
    "text_fingerprint",
]
