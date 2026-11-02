#!/usr/bin/env python3
"""Lossless rework transform: fold every importer-dropped legacy field into the
modeled `description`, so migration to todo-db retains ALL content via the
supported importer (no core changes, no raw SQL).

Reads a legacy YAML tracker (todo_dir, done_dir), writes a transformed mirror
tree where each item's description carries a delimited, verbatim block of the
residual (dropped) fields. Also emits residuals.json (item_id -> block) for the
verifier.

Usage: rework_transform.py <todo_dir> <done_dir> <out_dir>
Produces <out_dir>/TODO, <out_dir>/DONE, <out_dir>/residuals.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")
# keys the importer consumes (kept structurally); everything else is residual
CONSUMED_TOP = {
    "id", "title", "worktree", "priority", "status", "description", "category",
    "approach", "work", "deps", "dependencies", "deferred", "verification",
    "scope_limit", "scope", "must_preserve", "anti_patterns", "prior_art",
    "completed_date", "tasks",
}
CONSUMED_META = {"created_date"}
BEGIN = "<!-- MIGRATED-METADATA:BEGIN (retained verbatim from legacy YAML tracker) -->"
END = "<!-- MIGRATED-METADATA:END -->"


def slugify(raw: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", raw.lower()).strip("-") or "item"


def residual_of(data: dict) -> dict:
    res = {k: v for k, v in data.items() if k not in CONSUMED_TOP}
    meta = data.get("metadata") or {}
    # 'metadata' whole-key is non-consumed except created_date; keep only dropped subkeys
    res.pop("metadata", None)
    dropped_meta = {k: v for k, v in meta.items() if k not in CONSUMED_META}
    if dropped_meta:
        res["metadata"] = dropped_meta
    return res


def render_block(residual: dict) -> str:
    body = yaml.safe_dump(residual, sort_keys=False, allow_unicode=True, default_flow_style=False)
    return f"{BEGIN}\n## Migrated legacy metadata\n\n```yaml\n{body}```\n{END}"


def main() -> int:
    todo_dir, done_dir, out_dir = map(Path, sys.argv[1:4])
    residuals = {}
    for root, sub in ((todo_dir, "TODO"), (done_dir, "DONE")):
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.yaml")):
            if "_indexes" in path.parts:
                continue
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                continue
            raw_id = str(data.get("id") or path.stem)
            item_id = raw_id if SLUG_RE.match(raw_id) else slugify(raw_id)
            res = residual_of(data)
            desc = str(data.get("description", "")).rstrip()
            if res:
                block = render_block(res)
                data["description"] = f"{desc}\n\n{block}\n"
                residuals[item_id] = block
            rel = path.relative_to(root)
            dest = out_dir / sub / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    (out_dir / "residuals.json").write_text(json.dumps(residuals, indent=2), encoding="utf-8")
    print(f"transformed {len(residuals)} items carrying residual metadata; "
          f"wrote tree to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
