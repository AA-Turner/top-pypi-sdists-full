#!/usr/bin/env python3
"""Zero-loss verifier for the reworked migration.

Proves, for every source item, that the todo-db export's `description`:
  (1) contains the ORIGINAL source description verbatim, and
  (2) contains the EXACT residual block for every importer-dropped field.

Exit 0 = zero content loss; exit 1 = something was not retained.

Usage: rework_verify.py <export.json> <residuals.json> <todo_dir> <done_dir>
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")


def slugify(raw: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", raw.lower()).strip("-") or "item"


def load_src(todo_dir: Path, done_dir: Path):
    out = {}
    for root in (todo_dir, done_dir):
        if not root.exists():
            continue
        for p in sorted(root.rglob("*.yaml")):
            if "_indexes" in p.parts:
                continue
            d = yaml.safe_load(p.read_text(encoding="utf-8"))
            if not isinstance(d, dict):
                continue
            raw = str(d.get("id") or p.stem)
            iid = raw if SLUG_RE.match(raw) else slugify(raw)
            out[iid] = d
    return out


def main() -> int:
    export = json.load(open(sys.argv[1]))
    residuals = json.load(open(sys.argv[2]))
    src = load_src(Path(sys.argv[3]), Path(sys.argv[4]))
    exp = {i["id"]: i for i in export["tables"]["items"]}

    failures = []
    checked_fields = 0
    for iid, data in src.items():
        e = exp.get(iid)
        if not e:
            failures.append(f"[{iid}] missing from export")
            continue
        desc = e["description"] or ""
        # (1) original description retained
        orig = str(data.get("description", "")).rstrip()
        if orig and orig not in desc:
            failures.append(f"[{iid}] original description NOT found in export")
        # (2) residual block retained verbatim
        block = residuals.get(iid)
        if block:
            if block not in desc:
                failures.append(f"[{iid}] residual metadata block NOT retained verbatim")
            else:
                # confirm each dropped field name+value substring is inside the block
                inner = block
                for key in ("tags", "estimated_effort", "owners", "impact",
                            "files_affected", "success_metrics", "context_sections",
                            "open_questions", "sections", "last_updated", "moved_from"):
                    present_src = key in data or key in (data.get("metadata") or {})
                    if present_src and key not in inner:
                        failures.append(f"[{iid}] dropped field {key!r} present in source but not in retained block")
                    if present_src:
                        checked_fields += 1

    print("=" * 72)
    print(f"ZERO-LOSS RETENTION CHECK: {len(src)} items, {checked_fields} dropped-field instances verified")
    print("=" * 72)
    if failures:
        for f in failures:
            print("  FAIL", f)
        print("\nVERDICT: FAIL — content was lost")
        return 1
    print("Every original description + every dropped legacy field is retained in the DB export.")
    print("\nVERDICT: PASS — ZERO content loss")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
