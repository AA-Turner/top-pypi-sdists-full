"""Build fillable Evidence Manifest stubs for procedural KSIs.

`manifests draft <KSI>` walks one manifest interactively. `manifests scaffold`
lays down a fillable stub for *every* procedural KSI that doesn't have one yet,
so a customer can see — and fill in — the whole set in their editor. Each stub
is schema-valid (so it loads + doesn't break the pipeline) but deliberately
non-substantive (TODO placeholders), so `manifests status` / `efterlev next`
keep flagging it until it's actually filled in.
"""

from __future__ import annotations

import importlib.resources
from datetime import date
from typing import Any

import yaml


def template_questions(ksi: str) -> tuple[str | None, list[str]]:
    """Return `(name, questions)` from the bundled starter-pack template for `ksi`,
    or `(None, [])` when there's no template. Questions guide what to fill in."""
    try:
        pkg = importlib.resources.files("efterlev.manifest_templates")
        entry = pkg / f"{ksi}.template.yml"
        if not entry.is_file():
            return None, []
        data: dict[str, Any] = yaml.safe_load(entry.read_text(encoding="utf-8")) or {}
    except Exception:
        return None, []
    name = data.get("name")
    help_block = data.get("_template_help") or {}
    questions = help_block.get("questions") or []
    return (name if isinstance(name, str) else None), [str(q) for q in questions]


def stub_yaml(ksi: str, *, today: date | None = None) -> str:
    """A fillable, schema-valid (but non-substantive) manifest stub for `ksi`."""
    today = today or date.today()
    name, questions = template_questions(ksi)
    title = name or ksi
    lines = [
        f"# {ksi} — {title}",
        "# Procedural KSI: no scanner can see this — you attest to it here.",
        f"# Fill TODOs, then: efterlev manifests validate .efterlev/manifests/{ksi}.yml",
    ]
    if questions:
        lines.append("# Answer these:")
        lines.extend(f"#   - {q}" for q in questions)
    lines.extend(
        [
            f"ksi: {ksi}",
            f'name: "{title}"',
            "evidence:",
            '  - statement: "TODO: describe how this control is satisfied"',
            '    attested_by: "TODO: name + email of the accountable owner"',
            f"    attested_at: {today.isoformat()}",
            "    next_review: null",
            "    supporting_docs: []",
        ]
    )
    return "\n".join(lines) + "\n"
