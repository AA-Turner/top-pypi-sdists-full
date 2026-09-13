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
from typing import Any

logger = logging.getLogger(__name__)

# slug -> (emitted_json_schema | None, version)
_snapshot: dict[str, tuple[dict[str, Any] | None, int]] = {}
# The slug set, kept beside the schemas because the two questions have different
# consumers: the DETECTOR only needs membership (is this a kind at all), the ENVELOPE
# needs the schema. Splitting them keeps "registered but schemaless" expressible, which
# is a real registration state and must not read as "not a kind".
_known_versions: dict[str, int] = {}
_listing_seen = False


def is_registered_kind(slug: str) -> bool:
    """Sync: does this slug name a live kind? False while the snapshot is cold.

    False on a cold snapshot is a deliberate under-claim, not a bug — see property 1.
    """
    return slug in _known_versions


def registered_kind_schema(slug: str) -> dict[str, Any] | None:
    """Sync: the kind's ``emitted_json_schema``, or None (unknown, cold, or schemaless)."""
    entry = _snapshot.get(slug)
    return entry[0] if entry else None


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
        _listing_seen = False
        return
    _snapshot.pop(slug, None)
    _known_versions.pop(slug, None)


async def prime_registered_kinds() -> None:
    """Refresh the snapshot from the registry. Idempotent; safe to call per stream.

    Cheap by construction: the listing is ONE query, behind ``matrx_graph.kinds``'s own TTL,
    and it carries each kind's schema with it — resolving them per slug afterwards would be a
    round trip each for data that query already had in hand. A steady-state call is a cache
    hit and a dict copy; measured on the live registry it is ~0.1 ms warm against ~1.4 s cold.
    """
    global _listing_seen
    from matrx_graph.kinds import list_registered_kinds

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
        _snapshot[slug] = (schema, version)
        _known_versions[slug] = version

    if not _listing_seen:
        logger.info(
            "kind catalog snapshot: warm — %d registered kinds are now typed as kind blocks "
            "in the chat stream (DD-131).",
            len(_known_versions),
        )
    _listing_seen = True
