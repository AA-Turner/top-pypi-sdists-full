"""Register a kind the moment it is SEEN — the name on a real value, no registry row yet.

Arman, 2026-11-15: "If a kind comes through, even if it's randomly made up by this chat ... the
server needs to immediately register it. Nothing fancy: the name, the data as the sample, the
schema, because all of that is automated." A value carrying an unregistered ``__kind`` is the
whole input a registration needs, so no door that meets one may answer "not registered" and stop
(content-ir rule 35). Rule 32 already says the road is keep the name, scream, register; this is
the register half for a value met at RUN time (an agent's answer, a block on a screen, a button).

ONE function, ``register_kind_on_sight``. It writes through ``kind_create`` (never a second
writer), so naming, shape reuse, nested kinds, the canonical example and the seeded input
component are exactly an authored kind's. The row is marked ``metadata.registered_on_sight``
(who saw it, where, when): provenance only, it gates nothing.

Outcomes, never an exception:

* ``already``     the name is registered (anywhere). Nothing written.
* ``registered``  the name is registered now, from this value.
* ``same_shape``  these exact fields are already the kind ``kind``; the registry keeps one kind
                  per shape, so the seen name was not minted. The caller opens ``kind``.
* ``refused``     the registry said no (a junk name, a value that is not an object). ``message``
                  is the registry's own sentence.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel

from matrx_ai.db._registry import get_model as get_db_model

__all__ = ["KindOnSight", "ON_SIGHT_METADATA_KEY", "register_kind_on_sight", "kinds_named_in"]

#: ``kind_definition.metadata`` key naming how a kind met on sight was registered.
ON_SIGHT_METADATA_KEY = "registered_on_sight"

#: What a kind met on sight is, until its owner says otherwise: an output that is kept, the
#: same answer rule 34 gives a view's shape (``kind_layer._register_unregistered_kind``).
ON_SIGHT_DISPOSITION = "record"

OnSightStatus = Literal["already", "registered", "same_shape", "refused"]


class KindOnSight(BaseModel):
    """What happened to one seen kind name."""

    seen: str
    status: OnSightStatus
    #: The registered name to use: ``seen`` unless ``same_shape``; empty when ``refused``.
    kind: str = ""
    kind_definition_id: str | None = None
    message: str = ""


def _label(slug: str) -> str:
    return " ".join(word.capitalize() for word in slug.replace("-", "_").split("_") if word) or slug


def kinds_named_in(value: Any) -> list[str]:
    """Every ``__kind`` name inside ``value``, outermost first, each once."""
    from matrx_graph.content_ir.occurrences import find_occurrences

    names: list[str] = []
    for occurrence in find_occurrences(value):
        if occurrence.kind and occurrence.kind not in names:
            names.append(occurrence.kind)
    return names


async def _registered_row(slug: str) -> Any | None:
    """The live definition of ``slug`` in ANY organization (slugs are globally unique), or None."""
    KindDefinition = get_db_model("KindDefinition")
    for row in await KindDefinition.filter(kind=slug).all():
        if row.deleted_at is None:
            return row
    return None


async def register_kind_on_sight(
    slug: str,
    sample: Any,
    ctx: Any,
    *,
    origin: str,
) -> KindOnSight:
    """Make sure ``slug`` is registered, from the value it was seen on. See the module docstring.

    ``ctx`` carries ``user_id`` and ``organization_id`` (the request's own; never rebuilt here).
    ``origin`` names the door that saw it (``agent_turn``, ``screen``, ``button``).
    """
    from matrx_graph.table_kinds import is_table_kind

    from matrx_ai.tools.implementations.kind_shared import normalize_kind_slug

    seen = (slug or "").strip()
    if not seen:
        return KindOnSight(seen=seen, status="refused", message="The value names no kind.")
    if is_table_kind(seen):
        # A Table's kind is derived from the Table; it is never a registry row.
        return KindOnSight(seen=seen, status="already", kind=seen)
    # Exactly as written first (platform names carry dots: `seo.tool_envelope`).
    row = await _registered_row(seen)
    if row is not None:
        return KindOnSight(seen=seen, status="already", kind=seen, kind_definition_id=str(row.id))
    # A new kind is stored under ONE spelling (`Text-Notice` is `text_notice`): ask for that one,
    # or a differently-cased sighting would be "unregistered" forever.
    slug = normalize_kind_slug(seen) or seen

    row = await _registered_row(slug)
    if row is not None:
        return KindOnSight(seen=seen, status="already", kind=slug, kind_definition_id=str(row.id))

    if not isinstance(sample, dict) or not [key for key in sample if key != "__kind"]:
        return KindOnSight(
            seen=seen,
            status="refused",
            message=f"'{slug}' is not registered and there is no value to register it from.",
        )

    from matrx_ai.tools.implementations.kind_authoring import kind_create

    # Every nested name that is not registered yet is created in the same call; each one needs
    # to say what it is, and a part of a kept output is kept with it.
    # Keyed by the registry's spelling (the planner looks a child up by its normalized name).
    child_dispositions: dict[str, str] = {}
    for name in kinds_named_in(sample):
        child = normalize_kind_slug(name) or name
        if child == slug or is_table_kind(name) or child in child_dispositions:
            continue
        if await _registered_row(child) is None:
            child_dispositions[child] = ON_SIGHT_DISPOSITION

    args: dict[str, Any] = {
        "name": slug,
        "label": _label(slug),
        "sample_data": {**sample, "__kind": slug},
        "disposition": ON_SIGHT_DISPOSITION,
        "loading_component": "card",
    }
    if child_dispositions:
        args["child_dispositions"] = child_dispositions

    created = await kind_create(args, ctx)
    if not created.success:
        # Two doors saw the same value at once and the other one won: that is "already".
        row = await _registered_row(slug)
        if row is not None:
            return KindOnSight(seen=seen, status="already", kind=slug, kind_definition_id=str(row.id))
        error = created.error
        return KindOnSight(
            seen=seen,
            status="refused",
            message=str(getattr(error, "message", "") or "The kind could not be registered."),
        )

    output = created.output
    final = str(getattr(output, "kind", "") or slug)
    definition_id = str(getattr(output, "kind_definition_id", "") or "") or None
    _forget_cached_registry(final)

    if final != slug:
        return KindOnSight(
            seen=seen,
            status="same_shape",
            kind=final,
            kind_definition_id=definition_id,
            message=f"These fields are already the kind '{final}'.",
        )

    await _mark_on_sight(slug, ctx, origin)
    return KindOnSight(seen=seen, status="registered", kind=slug, kind_definition_id=definition_id)


async def _mark_on_sight(slug: str, ctx: Any, origin: str) -> None:
    """Write the provenance mark. The kind is registered either way; a refused mark is reported."""
    from matrx_ai.tools.implementations.kind_shared import update_as_the_person

    row = await _registered_row(slug)
    if row is None:
        return
    metadata = dict(row.metadata or {})
    metadata[ON_SIGHT_METADATA_KEY] = {
        "origin": origin,
        "at": datetime.now(UTC).isoformat(),
        "by": str(getattr(ctx, "user_id", "") or "") or None,
    }
    try:
        await update_as_the_person(get_db_model("KindDefinition"), str(row.id), None, metadata=metadata)
    except Exception as exc:  # noqa: BLE001 - the registration stands; the missing mark is reported
        from matrx_connect.streaming.error_capture import capture_error

        await capture_error(exc, kind="kind_on_sight_mark_refused", kind_slug=slug, origin=origin)


def _forget_cached_registry(slug: str) -> None:
    """Drop this process's cached registry answers so the next read sees the new kind."""
    from matrx_graph.kinds import invalidate_kind_catalog_cache

    from matrx_ai.processing.blocks.kind_catalog import invalidate as invalidate_blocks

    invalidate_kind_catalog_cache()
    invalidate_blocks(slug)
