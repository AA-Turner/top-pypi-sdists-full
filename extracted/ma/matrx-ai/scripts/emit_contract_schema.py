"""Emit the engine contract as ONE JSON Schema document.

agent-engine-extraction. **This is the artifact the whole pydantic migration
exists to produce.** D2 makes a pure-TypeScript sister package the goal and D8
puts the contract's home in matrx-utils; the mechanism connecting them is
`model_json_schema()`. `UnifiedConfig` being a dataclass is precisely why the
most important type in the system has had no cross-language definition — this is
that gap closing.

    python scripts/emit_contract_schema.py            # write contract.schema.json
    python scripts/emit_contract_schema.py --stdout   # print it
    python scripts/emit_contract_schema.py --check    # fail if the committed file is stale

It lives HERE rather than in aidream's `scripts/generate_types.py` on purpose:
the schema is the PACKAGE's contract, and a package does not depend on its host
to describe itself. Wiring it into the host's `/schema/bundle/{name}` delivery
path is a separate, host-side step.

WHAT IT DOES NOT CLAIM. The schema is only as complete as the twins, and several
fields are deliberately `Any` because the type they hold is not migrated
(`UnifiedConfig.messages`, `system_instruction`, `ToolResultContent.content`,
`UnifiedResponse.raw_response`, `TokenUsage.provider_charge`). Those emit an
unconstrained schema — TypeScript `any` — and the emitter REPORTS them rather
than letting a consumer discover it. A schema that hides its own soft spots is
worse than one that names them.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

from matrx_ai.config import models as contract_models

OUT = pathlib.Path(__file__).resolve().parent.parent / "matrx_ai" / "config" / "contract.schema.json"


def _exported_models() -> dict:
    """Every twin, including those exported only through a registry.

    The first version walked `__all__` alone and emitted 20 of 27 — the fourteen
    structured inputs reach the package surface through
    STRUCTURED_INPUT_MODEL_MAP, not as individual names, so a schema built from
    `__all__` silently described half a family. Registries are walked too.
    """
    out = {}
    for name in contract_models.__all__:
        obj = getattr(contract_models, name)
        if isinstance(obj, type) and hasattr(obj, "model_json_schema"):
            out[name] = obj
        elif isinstance(obj, dict):
            for member in obj.values():
                if isinstance(member, type) and hasattr(member, "model_json_schema"):
                    out[member.__name__] = member
    return out


def _is_unconstrained(spec: dict) -> bool:
    """True when a property describes nothing a consumer could rely on.

    A bare `{}` is obvious. The subtle case is an `anyOf` with an unconstrained
    MEMBER — `Any | list[Any]` emits a union whose first branch accepts anything,
    so the union as a whole constrains nothing. Missing that was a real gap:
    `UnifiedConfig.messages` and `system_instruction` are the two most important
    staged fields in the contract and neither was being reported.
    """
    if not any(k in spec for k in ("type", "$ref", "anyOf", "allOf", "enum", "const")):
        return True
    branches = spec.get("anyOf") or spec.get("allOf") or []
    return any(_is_unconstrained(b) for b in branches if isinstance(b, dict))


def build() -> tuple[dict, list[str]]:
    """Return (schema document, list of unconstrained fields)."""
    models = _exported_models()
    defs: dict = {}
    loose: list[str] = []

    for name, model in sorted(models.items()):
        schema = model.model_json_schema(ref_template="#/$defs/{model}")
        # Hoist nested $defs so the document is one flat, self-contained set.
        defs.update(schema.pop("$defs", {}))
        defs[name] = schema
        for field, spec in schema.get("properties", {}).items():
            if _is_unconstrained(spec):
                loose.append(f"{name}.{field}")

    doc = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Matrx engine contract",
        "description": (
            "Every exported contract type of the agentic engine. Generated from the "
            "pydantic twins by packages/matrx-ai/scripts/emit_contract_schema.py — the "
            "cross-language definition the TypeScript sister package (D2) generates from. "
            "Do not hand-edit."
        ),
        "x-unconstrained-fields": sorted(loose),
        "x-unconstrained-note": (
            "These fields emit no type constraint (TypeScript `any`) because the type they "
            "hold is not migrated yet. Listed rather than hidden: a consumer must know which "
            "parts of the contract are not actually described."
        ),
        "$defs": dict(sorted(defs.items())),
    }
    return doc, sorted(loose)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stdout", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    doc, loose = build()
    text = json.dumps(doc, indent=2, sort_keys=False) + "\n"

    if args.stdout:
        print(text)
        return 0

    if args.check:
        if not OUT.exists():
            print(f"🚨 {OUT.name} has never been generated.")
            return 1
        if OUT.read_text() != text:
            print(f"🚨 {OUT.name} is STALE — regenerate with: python scripts/emit_contract_schema.py")
            return 1
        print(f"✅ {OUT.name} matches the live models.")
        return 0

    OUT.write_text(text)
    print(f"wrote {OUT.relative_to(OUT.parent.parent.parent)}")
    print(f"  {len(doc['$defs'])} type definitions")
    print(f"  {len(loose)} unconstrained field(s) — reported in x-unconstrained-fields:")
    for f in loose:
        print(f"      {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
