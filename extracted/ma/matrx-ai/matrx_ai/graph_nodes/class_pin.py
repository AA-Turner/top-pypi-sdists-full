"""A workflow step's chosen CLASS of its model — the ``offering_id`` beside ``model``.

A model's class is its serving endpoint (``ai.endpoint``: "Matrx Fast",
"Matrx Lightning"…). Different classes are separate products a person picks;
the choice travels as ``offering_id`` (an ``ai.offering`` of that model) and
MUST run. A class belongs to exactly ONE model, so a step's ``offering_id``
rides only with the ``model`` the same step names:

* no step ``model`` → the pin names no model of its own and is DROPPED, loudly;
* a ``model`` the catalog says the offering does not belong to → DROPPED, loudly
  (a stale pin left behind when the model changed — the model then runs its
  preferred class instead of refusing the run);
* otherwise → it runs (``resolve_call_profile`` honours it, falling back only
  inside the same class).

Every node that declares a model field declares :func:`offering_id_field` next
to it, and the model field names it with ``class_field=CLASS_FIELD`` so the
studio's model picker writes both together.
"""

from __future__ import annotations

import logging
from typing import Any

from matrx_utils import vcprint
from pydantic import Field

logger = logging.getLogger(__name__)

#: The config key every model field's class travels under.
CLASS_FIELD = "offering_id"


def model_class_extras(class_field: str = CLASS_FIELD) -> dict[str, Any]:
    """The ``field_extras`` keyword that ties a model field to its class field."""
    return {"class_field": class_field}


def offering_id_field(*, order: int | None = None, model_field: str = "model") -> Any:
    """The ``offering_id`` Field declared beside a model field.

    Hidden as its own control: the model picker writes it (one row per class).
    """
    from matrx_graph.types.usl import field_extras

    return Field(
        default=None,
        description=(
            "The chosen class of the model (an ai.offering id). Set together with "
            "the model; empty runs the model's preferred class."
        ),
        json_schema_extra=field_extras(hidden=True, order=order, model_class_of=model_field),
    )


def _offering_owner(offering_id: str) -> tuple[str | None, Any]:
    """``(model_id the offering belongs to, manager)`` — ``(None, None)`` when the
    catalog is not loaded or does not know the offering (the resolver then
    diagnoses it at call time)."""
    try:
        from matrx_ai.catalog.manager import ai_catalog_manager
    except Exception:  # noqa: BLE001 — a client host without the catalog
        return None, None
    if not getattr(ai_catalog_manager, "_loaded", False):
        return None, None
    known = ai_catalog_manager.offering(str(offering_id))
    if known is None:
        return None, None
    return str(known.model_id), ai_catalog_manager


def _drop(where: str, pin: str, model: Any, why: str) -> None:
    message = (
        f"{where}: class pin offering_id='{pin}' DROPPED — {why}. "
        f"The step runs model '{model or '(the Holder model)'}' in its preferred class. "
        "Re-pick the model and its class together in the step."
    )
    vcprint(message, title="⚠️ WORKFLOW STEP: class pin dropped", color="yellow")
    logger.warning(message)


def node_class_pin(model: Any, offering_id: Any, *, where: str) -> str | None:
    """The class pin a step's own ``model`` runs with, or ``None`` (dropped loudly)."""
    pin = str(offering_id or "").strip() or None
    if pin is None:
        return None
    if not str(model or "").strip():
        _drop(where, pin, model, "the step names no model of its own for it to belong to")
        return None
    owner, manager = _offering_owner(pin)
    if owner is not None and manager is not None:
        resolved = str(manager.resolve_model_ref(str(model)))
        if resolved != owner:
            _drop(
                where,
                pin,
                model,
                f"it belongs to model_id '{owner}', not the step's model '{model}'",
            )
            return None
    return pin


def class_pin_kwargs(model: Any, offering_id: Any, *, where: str) -> dict[str, Any]:
    """``{"offering_id": …}`` for a funnel call's kwargs, or ``{}``."""
    pin = node_class_pin(model, offering_id, where=where)
    return {CLASS_FIELD: pin} if pin else {}
