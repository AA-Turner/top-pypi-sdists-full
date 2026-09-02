"""Refresh ``kind_schemas_sample.json`` from the LIVE kind catalog.

The block-envelope tests validate parser output against the REAL
``content_ir.kind_definition.emitted_json_schema`` rows (never hand-written
mocks). This script re-snapshots every kind in ``BLOCK_KIND_MAP`` so the
fixture can never silently drift into covering only a subset of the map.

Read-only. Run from the aidream repo root:

    .venv/bin/python packages/matrx-ai/tests/fixtures/refresh_kind_schemas.py

Fails loudly if any mapped kind is missing, inactive, or schema-less in the
live catalog — that is a platform defect, not something to snapshot around.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
FIXTURE = Path(__file__).parent / "kind_schemas_sample.json"

sys.path.insert(0, str(REPO_ROOT / "packages" / "matrx-ai"))


def _load_env() -> None:
    env_path = REPO_ROOT / ".env"
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


async def main() -> None:
    import asyncpg

    from matrx_ai.processing.blocks.envelope import BLOCK_KIND_MAP

    _load_env()
    conn = await asyncpg.connect(
        host=os.environ["SUPABASE_MATRIX_HOST"],
        port=int(os.environ["SUPABASE_MATRIX_PORT"]),
        user=os.environ["SUPABASE_MATRIX_USER"],
        password=os.environ["SUPABASE_MATRIX_PASSWORD"],
        database=os.environ["SUPABASE_MATRIX_DATABASE_NAME"],
        statement_cache_size=0,  # pgbouncer-safe
    )
    try:
        slugs = sorted(set(BLOCK_KIND_MAP.values()))
        rows = await conn.fetch(
            """
            select kind, is_active, emitted_json_schema
            from content_ir.kind_definition
            where kind = any($1::text[]) and deleted_at is null
            """,
            slugs,
        )
    finally:
        await conn.close()

    by_kind = {r["kind"]: r for r in rows}
    problems: list[str] = []
    schemas: dict[str, dict] = {}
    for slug in slugs:
        row = by_kind.get(slug)
        if row is None:
            problems.append(f"kind '{slug}' is NOT in content_ir.kind_definition")
            continue
        if not row["is_active"]:
            problems.append(f"kind '{slug}' is INACTIVE")
        schema = row["emitted_json_schema"]
        if schema is None:
            problems.append(f"kind '{slug}' has NO emitted_json_schema")
            continue
        schemas[slug] = json.loads(schema) if isinstance(schema, str) else schema

    if problems:
        for p in problems:
            print(f"DEFECT: {p}", file=sys.stderr)
        raise SystemExit(1)

    FIXTURE.write_text(
        json.dumps(
            {
                "_comment": (
                    "REAL emitted_json_schema rows pulled live from "
                    "content_ir.kind_definition (project brsgrqvjdzwihsvnfqkf, db.matrxserver.com) "
                    f"on {date.today().isoformat()} by refresh_kind_schemas.py — "
                    "one entry per BLOCK_KIND_MAP kind. Never hand-edit; rerun "
                    "the script."
                ),
                "schemas": schemas,
            },
            indent=2,
            ensure_ascii=False,
            sort_keys=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(schemas)} kind schemas -> {FIXTURE}")


if __name__ == "__main__":
    asyncio.run(main())
