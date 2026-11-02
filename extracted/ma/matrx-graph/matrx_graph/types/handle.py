from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field

from matrx_graph.types.primitives import EdgeKind


class HandleDirection(str, Enum):
    INPUT = "input"
    OUTPUT = "output"


class HandleSpec(BaseModel):
    """Typed connection point on a node.

    A node declares its handles statically via NodeSpec.handles. The UI renders
    them as ReactFlow handle anchors; the compiler validates that every edge
    attaches to a declared handle and that the edge kind is compatible with
    the handle's accepted_kinds.
    """

    model_config = {"frozen": True}

    id: str = Field(min_length=1, max_length=60)
    direction: HandleDirection
    accepted_kinds: tuple[EdgeKind, ...] = (EdgeKind.DATA,)
    required: bool = True
    max_connections: int | None = None
    label: str | None = None
    description: str | None = None
    channel: str | None = Field(
        default=None,
        description=(
            "Optional channel name. If set, the scheduler wires this handle "
            "directly to that channel instead of passing the payload inline."
        ),
    )


#: A config field whose ``json_schema_extra`` carries this marker is a list of
#: names, each one an OUTPUT connection point of that node instance — the
#: output twin of ``workflow_input_handles``. The optional
#: :data:`CONFIG_OUTPUT_HANDLE_PREFIX` marker prefixes each id (``answers.`` on
#: ``ai.decision``: one handle per question, ``answers.is_defect``). Declared
#: in the config schema so the validator, the scheduler and every studio read
#: the SAME list from the SAME place.
CONFIG_OUTPUT_HANDLES = "workflow_output_handles"
CONFIG_OUTPUT_HANDLE_PREFIX = "workflow_output_handle_prefix"


def _marker_fields(config_schema: object) -> dict[str, str]:
    """Config field name → handle prefix, for every field carrying the marker."""
    fields = getattr(config_schema, "model_fields", None) or {}
    marked: dict[str, str] = {}
    for field_name, field in fields.items():
        extra = field.json_schema_extra
        if isinstance(extra, dict) and extra.get(CONFIG_OUTPUT_HANDLES) is True:
            prefix = extra.get(CONFIG_OUTPUT_HANDLE_PREFIX)
            marked[field_name] = prefix if isinstance(prefix, str) else ""
    return marked


def normalized_config_output_fields(spec: object, config: object) -> dict[str, list[str]] | None:
    """The marker fields of ``config`` AS THE NODE'S CONFIG MODEL COMPUTES THEM.

    A config-declared handle list is DERIVED data (``option_keys`` from the
    options, ``question_names`` from the questions…): a stored copy can be
    stale (a label edited after the keys were written) or absent (a Conductor,
    MCP or agent writing raw config). Reading the raw stored list therefore
    both accepts edges on handles the node will never fire and refuses edges on
    handles it will. So the list is read only after the spec's config model has
    validated the config — its validators recompute derived keys — and never
    from the raw dict.

    Returns ``{}`` when the spec has no marker field, and ``None`` when the
    config does not validate (the config gate reports why; no config-derived
    handle exists on a config the node cannot run with).
    """
    config_schema = getattr(spec, "config_schema", None)
    marked = _marker_fields(config_schema)
    if not marked:
        return {}
    validate = getattr(config_schema, "model_validate", None)
    if validate is None or not isinstance(config, dict):
        return None
    try:
        normalized = validate(config).model_dump(mode="json")
    except Exception:  # noqa: BLE001 — any invalid config: the config gate names it
        return None
    out: dict[str, list[str]] = {}
    for field_name in marked:
        names = normalized.get(field_name)
        out[field_name] = (
            [name for name in names if isinstance(name, str)] if isinstance(names, list) else []
        )
    return out


def config_output_handles(spec: object, node: object) -> set[str]:
    """Output handle ids a node INSTANCE declares through its (normalized) config."""
    data = getattr(node, "data", None)
    config = data.get("config") if isinstance(data, dict) else None
    fields = normalized_config_output_fields(spec, config if config is not None else {})
    if not fields:
        return set()
    marked = _marker_fields(getattr(spec, "config_schema", None))
    return {
        f"{marked[field_name]}{name}"
        for field_name, names in fields.items()
        for name in names
        if name and name.strip() == name
    }
