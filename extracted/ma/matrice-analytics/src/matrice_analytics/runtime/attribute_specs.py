"""Classifier-attribute spec resolution for :mod:`runtime.backends`.

Split out of ``backends.py`` (INC-2026-146 file-size cap) rather than left inline --
this is a fully self-contained piece: one function, one constant, no shared state with
the rest of the engine backend.
"""

from __future__ import annotations

from typing import Any, Dict, Final, Tuple

#: Stage kinds whose manifest model declares a plain ``attribute: str`` field naming a
#: classifier-chain attribute (``engine/manifest/models.py`` -- ``AttributeVoteConfig``,
#: ``AttributeCountConfig``, ``AttributeBandConfig``). Anything named here is a stage that
#: reads ``PipelineDetection.attributes`` and therefore needs it populated.
_ATTRIBUTE_STAGE_KINDS: Final[frozenset[str]] = frozenset(
    {"attribute_vote", "attribute_count", "attribute_band"}
)


def _attribute_specs_for(manifest: Any) -> Tuple[Any, ...]:
    """The ``AttributeSpec`` list this manifest's attribute stages need, or ``()``.

    One spec per unique attribute name declared by an ``attribute_vote``/``attribute_count``/
    ``attribute_band`` stage, in first-seen pipeline order. Every :class:`AttributeSpec` field
    besides ``name`` is left at its default -- ``index_to_label`` empty, ``numeric=False`` --
    which decodes a flat ``label`` + ``confidence``/``class_confidence`` (or a ``top_k`` list)
    already on the detection. That covers every producer wired to this engine today; a producer
    that instead emits bare class indices needs its ``index_to_label`` supplied from a ``custom``
    stage's own ``config`` (see below), entirely app-owned -- this file has no knowledge of what
    any such map contains.

    An app with none of these three stages (most apps) returns ``()`` -- the caller's cheap
    early-out, so a plain detect/track/unique_count pipeline pays nothing for this.
    """
    from ..engine.intake.attributes import AttributeSpec

    seen: Dict[str, None] = {}
    index_maps: Dict[str, Any] = {}
    for stage in getattr(manifest, "pipeline", None) or ():
        kind = getattr(stage, "kind", None)
        if kind in _ATTRIBUTE_STAGE_KINDS:
            name = getattr(stage, "attribute", None)
            if isinstance(name, str) and name:
                seen[name] = None
        elif kind == "custom":
            # Generic escape hatch (CustomConfig.config), not a vehicle_type special case:
            # any app whose chained classifier emits a bare class index can declare a
            # custom stage carrying {"attribute": "<name>", "index_to_label": {...}} in its
            # own config, entirely inside that app's own logic.py. This file has no
            # knowledge of what any such map contains, only the generic shape of the
            # escape hatch itself.
            config = getattr(stage, "config", None)
            if isinstance(config, dict):
                name = config.get("attribute")
                mapping = config.get("index_to_label")
                if isinstance(name, str) and name and name not in index_maps and mapping:
                    index_maps[name] = mapping
    return tuple(AttributeSpec(name, index_to_label=index_maps.get(name, {})) for name in seen)
