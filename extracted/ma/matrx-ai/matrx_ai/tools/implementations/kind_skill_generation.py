"""The generated skill for a shape: template, hash stamp, and regeneration rule.

Pure logic (no database). ``kind_create_skill`` / the kind-activation auto-create and the
weekly ``shape_skills_weekly_refresh`` job all render through here, so a generated skill is
the same text whichever door made it.

REGENERATION RULE (Arman 2026-10-04, chat-shape-picks plan B2). A skill is regenerated only
when ALL hold: it carries ``metadata.created_via == "kind_create_skill"``, it was not made
from a body override, and its current body still hashes to ``metadata.generated_sha256`` --
nobody edited it. ``extra_guidance`` is carried forward. Everything else is hand-written and
never touched. A legacy generated skill (no hash yet) is stamped only when its body equals
what today's template produces from the guidance recoverable from that body.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

CREATED_VIA = "kind_create_skill"
GUIDANCE_HEADING = "\n## Additional guidance\n\n"

#: The line a generated skill carries while its shape has no description of its own.
def generic_description(kind: str) -> str:
    return (
        f"How and when to emit a {kind} render block as canonical "
        f'{{"__kind": "{kind}"}} JSON: the exact shape, required fields, '
        "and JSON syntax rules."
    )


def shape_description(kd: Any) -> str | None:
    """The shape's own one-line description (``kind_definition.metadata.description``)."""
    meta = getattr(kd, "metadata", None)
    if isinstance(meta, dict):
        text = meta.get("description")
        if isinstance(text, str) and text.strip():
            return text.strip()
    return None


def skill_description(kd: Any) -> str:
    return shape_description(kd) or generic_description(kd.kind)


def render_skill_body(kd: Any, canonical_example: Any, extra_guidance: str | None) -> str:
    """House-format render_block skill body: what it is, the shape with a real example,
    field notes, and the JSON syntax rules."""
    example_obj: dict[str, Any] = {"__kind": kd.kind}
    if isinstance(canonical_example, dict):
        example_obj.update(canonical_example)
    example_json = json.dumps(example_obj, indent=2, ensure_ascii=False)

    schema = kd.emitted_json_schema if isinstance(kd.emitted_json_schema, dict) else {}
    props = schema.get("properties") or {}
    required = set(schema.get("required") or [])
    field_rows = "\n".join(
        f"| `{name}` | {spec.get('type', 'any') if isinstance(spec, dict) else 'any'} | "
        f"{'yes' if name in required else 'no'} |"
        for name, spec in props.items()
    )
    field_table = (
        f"| Field | Type | Required |\n|---|---|---|\n| `__kind` | string | yes |\n{field_rows}\n"
        if field_rows
        else ""
    )
    guidance = f"{GUIDANCE_HEADING}{extra_guidance}\n" if extra_guidance else ""
    return (
        f"# {kd.label} (structured __kind JSON)\n\n"
        f"You can emit a **{kd.label}** as a single JSON object marked with\n"
        f'`"__kind": "{kd.kind}"`. It renders through the platform kind registry as a\n'
        f"live, custom component.\n\n"
        f"## The shape\n\n```json\n{example_json}\n```\n\n"
        f"{field_table}\n"
        f"## Syntax rules\n\n"
        f'1. `"__kind"` is always the literal `"{kd.kind}"` and must be the first key.\n'
        f"2. Valid JSON only: double-quoted keys/strings, no trailing commas, no comments.\n"
        f"3. Emit the COMPLETE object every time — when editing, return the full updated\n"
        f"   object, never a fragment or a diff.\n"
        f"4. One object per instance. Two ideas = two `{kd.kind}` objects with a sentence\n"
        f"   between them.\n"
        f"5. Match the schema exactly — include every required field; do not invent keys.\n"
        f"{guidance}"
    )


def body_hash(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def generated_metadata(
    kd: Any,
    body: str,
    *,
    extra_guidance: str | None,
    body_override: bool,
    description: str,
    base: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """The metadata a generated skill carries. ``kind_definition_id`` is what the server
    resolves shape -> skill by (Lane A), so every generated skill must have it."""
    meta = dict(base or {})
    meta["kind_definition_id"] = str(kd.id)
    meta["created_via"] = CREATED_VIA
    meta["template_inputs"] = {
        "extra_guidance": extra_guidance,
        "body_override": bool(body_override),
    }
    meta["generated_description"] = description
    if body_override:
        meta.pop("generated_sha256", None)
    else:
        meta["generated_sha256"] = body_hash(body)
    return meta


def extract_extra_guidance(body: str) -> str | None:
    """Recover the guidance a legacy generated body carries (it is always the last section)."""
    idx = body.rfind(GUIDANCE_HEADING)
    if idx < 0:
        return None
    text = body[idx + len(GUIDANCE_HEADING):]
    if text.endswith("\n"):
        text = text[:-1]
    return text or None


@dataclass(frozen=True)
class RefreshDecision:
    action: str  # skip_hand_written | skip_edited | up_to_date | stamp | regenerate
    body: str | None = None
    description: str | None = None
    metadata: dict[str, Any] | None = None
    reason: str = ""


def decide_refresh(existing: Any, kd: Any, canonical_example: Any) -> RefreshDecision:
    """What the weekly refresh does with an existing skill for this shape."""
    meta = dict(getattr(existing, "metadata", None) or {})
    if meta.get("created_via") != CREATED_VIA:
        return RefreshDecision("skip_hand_written", reason="no created_via")
    inputs = meta.get("template_inputs") or {}
    if inputs.get("body_override"):
        return RefreshDecision("skip_hand_written", reason="made from a body override")

    current_body = getattr(existing, "body", None) or ""
    stored_hash = meta.get("generated_sha256")
    if stored_hash:
        if body_hash(current_body) != stored_hash:
            return RefreshDecision("skip_edited", reason="body edited since generation")
        guidance = inputs.get("extra_guidance")
    else:
        # Legacy skill: only generated if today's template reproduces it exactly.
        guidance = extract_extra_guidance(current_body)
        if render_skill_body(kd, canonical_example, guidance) != current_body:
            # Guidance may legitimately be absent but the heading text appear in an
            # edited body; either way the template cannot reproduce it.
            return RefreshDecision("skip_hand_written", reason="legacy body not reproducible")

    new_body = render_skill_body(kd, canonical_example, guidance)
    new_desc = skill_description(kd)
    current_desc = getattr(existing, "description", None) or ""
    prev_generated_desc = meta.get("generated_description") or generic_description(kd.kind)
    # A human-edited description survives; only a description we generated is replaced.
    desc_is_ours = current_desc in (prev_generated_desc, generic_description(kd.kind), "")
    target_desc = new_desc if desc_is_ours else current_desc

    new_meta = generated_metadata(
        kd,
        new_body,
        extra_guidance=guidance,
        body_override=False,
        description=target_desc if desc_is_ours else (meta.get("generated_description") or ""),
        base=meta,
    )
    changed = new_body != current_body or target_desc != current_desc
    if not changed and meta == new_meta:
        return RefreshDecision("up_to_date")
    action = "regenerate" if changed else "stamp"
    return RefreshDecision(action, body=new_body, description=target_desc, metadata=new_meta)
