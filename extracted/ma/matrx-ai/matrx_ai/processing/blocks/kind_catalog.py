"""The SYNC snapshot of the kind registry that the block pipeline reads mid-stream.

WHY THIS EXISTS. ``detect_json_block_type`` runs inside the token loop: it is synchronous,
it is called on every buffer change, and it must answer *"is this ``__kind`` a registered
kind?"* before the fence has even closed. The registry lives in Postgres and
``matrx_graph.kinds`` resolves it asynchronously with a 5-minute TTL. Those two facts cannot
be reconciled by making the detector async — the whole splitter is sync and has a TS twin
that a parity gate diffs. So the async catalog is projected into a snapshot the detector can
read without awaiting, and the snapshot is refreshed at the one moment the pipeline is
already async: stream start.

THE RULING THIS IMPLEMENTS (chair, 2026-09-12, DD-131). A fenced JSON body whose ``__kind``
names a REGISTERED, LIVE kind **is a kind block**, exactly like the 19 platform block types:
it is validated against that kind's ``emitted_json_schema`` and gets the same ``metadata.__ir``
envelope. An unregistered or dead slug stays a plain code block. Before this, ``BLOCK_KIND_MAP``
was the only route to an envelope, so a user-authored kind — every kind anyone creates in the
product — could never be verified server-side, and Arman's *"every output gets saved
automatically"* was unreachable for the entire class.

THREE PROPERTIES THIS FILE IS RESPONSIBLE FOR:

1. **A cold snapshot never LIES — it declines.** Unknown means "plain code block", which is
   exactly what happened before this feature existed. The failure direction is the safe one:
   a missed envelope degrades to the frontend's own parse, while a wrong envelope poisons the
   frontend's fingerprint-keyed cache for the whole region (envelope.py law 1).
2. **An outage is not an empty registry.** ``list_registered_kinds()`` returns ``None`` when
   it could not ask and ``()`` when the registry is genuinely empty. Conflating them would
   declassify every kind block on the platform for the length of an outage, silently.
3. **A version bump invalidates.** The snapshot stores each slug's version; the refresh drops
   the schema of any slug whose version moved, so an edited kind is re-fetched rather than
   validated against the shape it used to have. ``invalidate(slug)`` is the immediate path for
   the authoring tools, which know the moment a kind changes and should not wait out a TTL.
"""

from __future__ import annotations

import logging
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any

from matrx_graph.kind_control_keys import applies_to, with_control_keys

logger = logging.getLogger(__name__)

# slug -> (emitted_json_schema | None, version)
_snapshot: dict[str, tuple[dict[str, Any] | None, int]] = {}
# The slug set, kept beside the schemas because the two questions have different
# consumers: the DETECTOR only needs membership (is this a kind at all), the ENVELOPE
# needs the schema. Splitting them keeps "registered but schemaless" expressible, which
# is a real registration state and must not read as "not a kind".
_known_versions: dict[str, int] = {}
# slug -> declared disposition, from the same listing. A ``record`` kind's schema is served
# with the four control keys declared (``matrx_graph.kind_control_keys``, stored mode), built
# once per (slug, version) and held in ``_stored_schemas``.
_dispositions: dict[str, str | None] = {}
_stored_schemas: dict[str, dict[str, Any]] = {}
_listing_seen = False

# ``table:<uuid>`` kinds held for ONE request (KINDS-GLUE wave 3 §6.2 item 2). A Table's kind is
# derived from its Fields as the person asking, so it is never put in the process-wide snapshot
# above (a schema read as one person would type another person's stream) and never popped by
# ``prime_registered_kinds`` (it is not a registry row). A ``ContextVar``, so it reaches the
# replay's ``asyncio.to_thread`` worker (which copies the context) and nothing else.
_table_kinds: ContextVar[Mapping[str, dict[str, Any]] | None] = ContextVar(
    "matrx_ai_table_kinds", default=None
)


@contextmanager
def holding_table_kinds(schemas: Mapping[str, dict[str, Any]]) -> Iterator[None]:
    """Type ``table:<uuid>`` blocks with these stored schemas inside this block only.

    ``schemas`` maps each slug to its stored-mode schema (``matrx_graph.table_kinds.stored_schema``,
    control keys already declared). Nested holds see the union; leaving restores the outer set.
    """
    outer = _table_kinds.get() or {}
    token = _table_kinds.set({**outer, **schemas})
    try:
        yield
    finally:
        _table_kinds.reset(token)


def is_registered_kind(slug: str) -> bool:
    """Sync: does this slug name a live kind? False while the snapshot is cold.

    False on a cold snapshot is a deliberate under-claim, not a bug — see property 1. A
    ``table:`` kind held for this request (``holding_table_kinds``) counts as known.
    """
    held = _table_kinds.get()
    if held and slug in held:
        return True
    return slug in _known_versions


def registered_kind_schema(slug: str) -> dict[str, Any] | None:
    """Sync: the kind's schema as the envelope validates it, or None (unknown, cold, schemaless).

    For a ``record`` kind that is its ``emitted_json_schema`` with the control keys declared
    (``with_control_keys(..., mode="stored")``, KINDS-GLUE wave 2 §1.4): a value carrying
    ``_replaces`` / ``_new`` / ``_record_id`` / ``_records`` keeps them through the envelope's
    partition, and a patch or a batch is not refused for the root Fields it does not carry. No
    registry row is edited; every other disposition gets the registered schema as it is.
    """
    held = _table_kinds.get()
    if held and slug in held:
        return held[slug]
    entry = _snapshot.get(slug)
    if not entry:
        return None
    schema = entry[0]
    if schema is None or not applies_to(_dispositions.get(slug)):
        return schema
    stored = _stored_schemas.get(slug)
    if stored is None:
        stored = with_control_keys(schema, mode="stored")
        _stored_schemas[slug] = stored
    return stored


def snapshot_is_warm() -> bool:
    """Has the registry listing ever landed in this process?

    Callers use it to tell "no kind blocks in this stream" from "we could not have seen one",
    which is the difference between a quiet success and an invisible outage.
    """
    return _listing_seen


def invalidate(slug: str | None = None) -> None:
    """Drop one slug (or the whole snapshot) so the next prime re-reads it.

    Call it from the kind-authoring path the moment a kind is created or edited: the TTL is a
    backstop for changes made elsewhere, never the mechanism for changes made here.
    """
    global _listing_seen
    if slug is None:
        _snapshot.clear()
        _known_versions.clear()
        _dispositions.clear()
        _stored_schemas.clear()
        _listing_seen = False
        return
    _snapshot.pop(slug, None)
    _known_versions.pop(slug, None)
    _dispositions.pop(slug, None)
    _stored_schemas.pop(slug, None)


async def prime_registered_kinds() -> None:
    """Refresh the snapshot from the registry. Idempotent; safe to call per stream.

    Cheap by construction: the listing is ONE query, behind ``matrx_graph.kinds``'s own TTL,
    and it carries each kind's schema with it — resolving them per slug afterwards would be a
    round trip each for data that query already had in hand. A steady-state call is a cache
    hit and a dict copy; measured on the live registry it is ~0.1 ms warm against ~1.4 s cold.
    """
    global _listing_seen
    from matrx_graph.kinds import list_registered_kinds, listed_kind_disposition

    listed = await list_registered_kinds()
    if listed is None:
        # Could not ask. Keep whatever we already hold rather than declassifying every kind
        # block on the platform for the length of the outage (property 2). The catalog has
        # already logged the outage once; a second scream here would be noise.
        return

    live = {slug: version for slug, version, _schema in listed}
    for slug in [s for s, v in _known_versions.items() if live.get(s) != v]:
        # A slug that left the registry, or whose kind was edited. Either way the schema we
        # hold no longer describes it (property 3).
        _snapshot.pop(slug, None)
        _known_versions.pop(slug, None)

    for slug, version, schema in listed:
        disposition = listed_kind_disposition(slug)
        held = _snapshot.get(slug)
        if held is None or held[0] is not schema or _dispositions.get(slug) != disposition:
            _stored_schemas.pop(slug, None)
        _snapshot[slug] = (schema, version)
        _known_versions[slug] = version
        _dispositions[slug] = disposition

    if not _listing_seen:
        logger.info(
            "kind catalog snapshot: warm — %d registered kinds are now typed as kind blocks "
            "in the chat stream (DD-131).",
            len(_known_versions),
        )
    _listing_seen = True
