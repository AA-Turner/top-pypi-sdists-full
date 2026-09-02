"""Shared helpers for multi-action dispatcher tools.

Dispatcher tools register a discriminated-union ``RootModel`` (see
``arg_models``) and validate the incoming call against it in the body, so the
body is provably bound to the per-action contract the drift gate proves against
the DB. This module owns the executor's **arg-recovery** primitives — recover
when we can, scream clearly when we can't:

* ``coerce_stringified_containers`` — JSON *string* where a dict/list is required
* ``infer_missing_discriminator`` — omitted ``action``/``command`` inferred from
  variant-unique fields (``queries``→search, ``url``→read, …)
* ``remove_flattened_variant_extras`` — fields advertised by a flattened
  dispatcher schema but forbidden by the selected action
* ``recover_action_type_alias`` — client-tool ``action`` discriminator copied
  to canonical ``type`` only when the published enum proves the mapping
* ``format_args_error`` — flat agent-instructive line from a ValidationError

A rejected tool call still costs a full provider turn and returns nothing useful.
Recovery is the default; rejection is the last resort with an actionable menu.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Literal

from matrx_utils import suggestion_line

# Pydantic v2 error types that mean "a mapping/object was required here".
_DICT_ERROR_TYPES = frozenset(
    {"dict_type", "model_type", "model_attributes_type", "dataclass_type"}
)
# Pydantic v2 error types that mean "a sequence/array was required here".
_LIST_ERROR_TYPES = frozenset({"list_type", "tuple_type", "set_type"})
# Pydantic v2 error types that carry the permitted values in ctx["expected"].
_CHOICE_ERROR_TYPES = frozenset({"enum", "literal_error"})

_EXPECTED_VALUES_RE = re.compile(r"'([^']*)'")

_STRINGIFIED_JSON_ADVICE = (
    "You sent a JSON-encoded string; send the raw JSON object/array itself "
    "(no surrounding quotes, no escaping)."
)


def recover_action_type_alias(
    arguments: dict[str, Any],
    parameters: dict[str, Any],
) -> dict[str, Any] | None:
    """Recover ``action=<enum member>`` as canonical ``type=<same member>``.

    Some tools use the platform's common ``action`` discriminator; the
    client-interaction tool instead publishes ``type``. Models occasionally
    pattern-complete the former. This repair is deliberately schema-proven:

    * canonical ``type`` and batched ``questions`` must both be absent;
    * the published schema must define ``type.enum`` containing the value;
    * the schema must NOT define a real ``action`` property.

    Unknown values and ambiguous schemas return ``None`` and keep their normal
    validation/error path. Both the flat internal property map and a full JSON
    Schema ``properties`` wrapper are accepted.
    """
    if "type" in arguments or "questions" in arguments or "action" not in arguments:
        return None
    properties: Any = parameters.get("properties", parameters)
    if not isinstance(properties, dict) or "action" in properties:
        return None
    type_schema = properties.get("type")
    if not isinstance(type_schema, dict):
        return None
    allowed = type_schema.get("enum")
    action = arguments.get("action")
    if not isinstance(allowed, list) or action not in allowed:
        return None
    recovered = dict(arguments)
    recovered.pop("action", None)
    recovered["type"] = action
    return recovered


def _error_list(exc: Any) -> list[dict[str, Any]]:
    errs = getattr(exc, "errors", None)
    if callable(errs):
        try:
            return list(exc.errors())
        except Exception:  # noqa: BLE001 - defensive, caller falls back to str()
            return []
    return []


def format_args_error(exc: Any) -> str:
    errors = _error_list(exc)
    if errors:
        try:
            lines: list[str] = []
            advice: list[str] = []
            saw_stringified_container = False
            for e in errors:
                loc = ".".join(str(p) for p in e.get("loc", ())) or "(root)"
                lines.append(f"{loc}: {e.get('msg', 'invalid')}")
                etype = e.get("type", "")
                if (etype in _DICT_ERROR_TYPES or etype in _LIST_ERROR_TYPES) and isinstance(
                    e.get("input"), str
                ):
                    saw_stringified_container = True
                elif etype in _CHOICE_ERROR_TYPES:
                    expected = _EXPECTED_VALUES_RE.findall(
                        str((e.get("ctx") or {}).get("expected", ""))
                    )
                    supplied = e.get("input")
                    if expected and isinstance(supplied, str):
                        hint = suggestion_line(supplied, expected, noun="value")
                        if hint and hint not in advice:
                            advice.append(hint)
            # Pydantic's raw discriminator miss is useless to the model
            # ("Unable to extract tag using discriminator 'action'"). Prefer a
            # short redirect — the executor overlays the full action menu via
            # infer_missing_discriminator when it has the args model.
            if any(e.get("type") == "union_tag_not_found" for e in errors):
                disc = "action"
                for e in errors:
                    if e.get("type") == "union_tag_not_found":
                        ctx = e.get("ctx") or {}
                        if isinstance(ctx.get("discriminator"), str):
                            disc = ctx["discriminator"]
                        break
                return (
                    f"Missing required field {disc!r}. Set it explicitly "
                    f"(or supply the variant-unique fields so it can be inferred)."
                )[:900]
            joined = "; ".join(lines)[:600]
            if saw_stringified_container:
                advice.insert(0, _STRINGIFIED_JSON_ADVICE)
            if advice:
                joined = f"{joined} {' '.join(advice)}"
            if joined.strip():
                return joined[:900]
        except Exception:  # noqa: BLE001 - fall through to str()
            pass
    return str(exc)[:600] or "invalid arguments"


def coerce_stringified_containers(
    arguments: dict[str, Any],
    exc: Any,
) -> tuple[dict[str, Any], list[str]] | None:
    """Recover from the "JSON string where a dict/list is required" arg shape.

    Inspects a Pydantic ``ValidationError`` for container-type failures whose
    supplied value is a **top-level** string field of ``arguments`` that
    ``json.loads`` cleanly into exactly the required container type. Returns
    ``(coerced_arguments, coerced_field_names)`` when at least one field was
    fixed, else ``None``. The caller MUST re-validate the coerced arguments
    once (single pass, no recursion) — this function never guesses semantics,
    it only undoes a double-encoding.

    Union branches are handled naturally: a field typed ``dict | list`` fails
    both branches (``dict_type`` AND ``list_type``); the parsed value only has
    to match ONE required container to qualify.
    """
    errors = _error_list(exc)
    if not errors or not isinstance(arguments, dict):
        return None

    parsed_cache: dict[str, Any] = {}
    coerced: dict[str, Any] = {}

    for e in errors:
        etype = e.get("type", "")
        if etype in _DICT_ERROR_TYPES:
            want: type = dict
        elif etype in _LIST_ERROR_TYPES:
            want = list
        else:
            continue
        # Locs vary by shape: ('data',) plain, ('update', 'data') discriminated
        # union (tag prefix), ('insert', 'data', 'dict[str,any]') inner union
        # (branch name suffix). The coercible field is the last loc element
        # that IS a top-level key of the arguments dict.
        loc = e.get("loc", ())
        field = next((p for p in reversed(loc) if isinstance(p, str) and p in arguments), None)
        if field is None or field in coerced:
            continue
        supplied = arguments[field]
        # Top-level only: the failing value must BE the top-level field value
        # (discriminated-union locs like ('update', 'data') still resolve to
        # the top-level 'data' key; genuinely nested misses fail this check).
        if not isinstance(supplied, str) or e.get("input") != supplied:
            continue
        if field not in parsed_cache:
            try:
                parsed_cache[field] = json.loads(supplied)
            except (ValueError, TypeError):
                parsed_cache[field] = _UNPARSEABLE
        parsed = parsed_cache[field]
        if parsed is _UNPARSEABLE:
            continue
        if type(parsed) is want:  # exact container match — never a scalar/subclass
            coerced[field] = parsed

    if not coerced:
        return None
    merged = dict(arguments)
    merged.update(coerced)
    return merged, sorted(coerced)


_UNPARSEABLE = object()


# ── Missing discriminator (action / command) inference ───────────────────────


@dataclass(frozen=True)
class InferDiscriminatorResult:
    """Outcome of :func:`infer_missing_discriminator`.

    ``kind``:
      * ``not_applicable`` — not a discriminated union, or discriminator already set
      * ``inferred`` — uniquely recovered; ``args`` has the tag filled in
      * ``ambiguous`` — ≥2 variants fit; ``error`` names the conflict
      * ``uninferable`` — nothing unique enough; ``error`` is the action menu
    """

    kind: Literal["not_applicable", "inferred", "ambiguous", "uninferable"]
    args: dict[str, Any] | None = None
    discriminator: str | None = None
    tag: str | None = None
    error: str | None = None


def _has_discriminator(arguments: dict[str, Any], disc: str) -> bool:
    if disc not in arguments:
        return False
    value = arguments[disc]
    if value is None:
        return False
    if isinstance(value, str) and not value.strip():
        return False
    return True


def _variant_field_sets(
    members: dict[str, type],
    disc: str,
) -> dict[str, tuple[set[str], set[str]]]:
    """Per tag → (required_fields, allowed_fields), excluding the discriminator."""
    out: dict[str, tuple[set[str], set[str]]] = {}
    for tag, sub in members.items():
        required: set[str] = set()
        allowed: set[str] = set()
        for name, field in sub.model_fields.items():
            if name == disc:
                continue
            allowed.add(name)
            if field.is_required():
                required.add(name)
        out[tag] = (required, allowed)
    return out


def remove_flattened_variant_extras(
    arguments: dict[str, Any],
    args_model: type,
    exc: Any,
) -> tuple[dict[str, Any], list[str]] | None:
    """Remove only provably redundant fields from a selected union variant.

    Provider-facing dispatcher schemas are currently flattened into the union
    of every action's fields. A model can therefore send a field that the
    advertised schema allows globally but the selected Pydantic variant
    forbids (for example ``sql(action="query", query="…", table="…")``).

    Recovery is intentionally narrow:

    * the args model must be a discriminated union;
    * the discriminator must select a known variant;
    * every validation error must be ``extra_forbidden``;
    * every removed field must be declared by at least one *other* variant.

    A typo or an unknown field is never stripped. The caller must revalidate
    the returned candidate before dispatch and must log every recovery loudly.
    """
    if not isinstance(arguments, dict):
        return None
    errors = _error_list(exc)
    if not errors or any(e.get("type") != "extra_forbidden" for e in errors):
        return None

    from matrx_ai.tools.validation.schema import discriminated_union_members

    union = discriminated_union_members(args_model)
    if union is None:
        return None
    disc, members = union
    selected = arguments.get(disc)
    if not isinstance(selected, str) or selected not in members:
        return None

    selected_fields = set(members[selected].model_fields)
    other_fields: set[str] = set()
    for tag, member in members.items():
        if tag != selected:
            other_fields.update(member.model_fields)

    removable: set[str] = set()
    for error in errors:
        loc = error.get("loc", ())
        field = next(
            (
                part
                for part in reversed(loc)
                if isinstance(part, str) and part in arguments
            ),
            None,
        )
        if (
            field is None
            or field == disc
            or field in selected_fields
            or field not in other_fields
        ):
            return None
        removable.add(field)

    if not removable:
        return None
    recovered = {
        key: value for key, value in arguments.items() if key not in removable
    }
    return recovered, sorted(removable)


def _action_menu(
    disc: str,
    variant_info: dict[str, tuple[set[str], set[str]]],
) -> str:
    lines: list[str] = []
    for tag in sorted(variant_info):
        required, _allowed = variant_info[tag]
        if required:
            fields = ", ".join(sorted(required))
            lines.append(f'{disc}="{tag}" when you supply: {fields}')
        else:
            lines.append(f'{disc}="{tag}" (no other required fields)')
    return "Valid options:\n  - " + "\n  - ".join(lines)


def infer_missing_discriminator(
    arguments: dict[str, Any],
    args_model: type,
) -> InferDiscriminatorResult:
    """Recover a missing ``action``/``command`` from variant-unique fields.

    Structural match: required ⊆ present ⊆ allowed for exactly one variant.
    Unique-field vote: a field declared on exactly one variant votes for it
    (covers optional signals like ``operations``→``json_patch``).

    Never invents a tag when ≥2 variants fit or when nothing unique is present —
    returns an agent-facing menu instead. Caller MUST re-validate after inference.
    """
    if not isinstance(arguments, dict):
        return InferDiscriminatorResult(kind="not_applicable")

    # Lazy import: validation.schema pulls pydantic RootModel introspection;
    # keep _dispatch_util importable without that graph for unit tests that
    # only exercise coerce/format.
    from matrx_ai.tools.validation.schema import discriminated_union_members

    union = discriminated_union_members(args_model)
    if union is None:
        return InferDiscriminatorResult(kind="not_applicable")
    disc, members = union
    if _has_discriminator(arguments, disc):
        return InferDiscriminatorResult(kind="not_applicable")

    variant_info = _variant_field_sets(members, disc)
    present = {k for k in arguments if k != disc}

    structural = [
        tag
        for tag, (required, allowed) in variant_info.items()
        if required.issubset(present) and present.issubset(allowed)
    ]
    if len(structural) == 1:
        tag = structural[0]
        merged = dict(arguments)
        merged[disc] = tag
        return InferDiscriminatorResult(
            kind="inferred",
            args=merged,
            discriminator=disc,
            tag=tag,
        )

    # When several variants structurally fit, prefer ones that actually
    # *required* a present field over empty-required catch-alls
    # (memory recall / dataset list / sql schema). `{query:…}` → search,
    # not recall.
    if len(structural) > 1:
        nonempty = [t for t in structural if variant_info[t][0]]
        if len(nonempty) == 1:
            tag = nonempty[0]
            merged = dict(arguments)
            merged[disc] = tag
            return InferDiscriminatorResult(
                kind="inferred",
                args=merged,
                discriminator=disc,
                tag=tag,
            )

    # Unique-field voting — a field owned by exactly one variant.
    owners: dict[str, list[str]] = {}
    for tag, (_required, allowed) in variant_info.items():
        for field in allowed:
            owners.setdefault(field, []).append(tag)
    unique_owner = {f: tags[0] for f, tags in owners.items() if len(tags) == 1}

    votes: dict[str, list[str]] = {}
    for field in present:
        owner = unique_owner.get(field)
        if owner is not None:
            votes.setdefault(owner, []).append(field)

    if len(votes) == 1:
        tag = next(iter(votes))
        merged = dict(arguments)
        merged[disc] = tag
        return InferDiscriminatorResult(
            kind="inferred",
            args=merged,
            discriminator=disc,
            tag=tag,
        )

    if len(votes) > 1:
        conflict = "; ".join(
            f"{', '.join(repr(f) for f in fields)} → {disc}={tag!r}"
            for tag, fields in sorted(votes.items())
        )
        return InferDiscriminatorResult(
            kind="ambiguous",
            discriminator=disc,
            error=(
                f"Cannot infer {disc!r}: conflicting fields ({conflict}). "
                f"Set {disc} explicitly and drop fields that do not belong to "
                f"that variant. {_action_menu(disc, variant_info)}"
            ),
        )

    if len(structural) > 1:
        options = ", ".join(f'{disc}="{t}"' for t in sorted(structural))
        return InferDiscriminatorResult(
            kind="ambiguous",
            discriminator=disc,
            error=(
                f"Cannot infer {disc!r}: arguments match more than one variant "
                f"({options}). Set {disc} explicitly. "
                f"{_action_menu(disc, variant_info)}"
            ),
        )

    return InferDiscriminatorResult(
        kind="uninferable",
        discriminator=disc,
        error=(
            f"Missing required field {disc!r} and it could not be inferred from "
            f"the other arguments. Set {disc} explicitly. "
            f"{_action_menu(disc, variant_info)}"
        ),
    )
