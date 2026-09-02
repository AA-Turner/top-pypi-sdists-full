"""C0 — export the conformance corpus from production history.

The corpus is not written; it is EXPORTED. ``providers/snapshot.py`` already
stashes the final SDK-ready provider payload for every persisted run, so
``chat.request_snapshot`` holds a real (input, expected-output) pair per row:

    unified_payload  -> the engine's input  (UnifiedConfig, as serialized)
    request_payload  -> the exact provider wire payload it produced
    provider/model   -> the routing that connected them

Both twins (Python and TypeScript) run this corpus. A twin is conformant when
it reproduces every ``request_payload`` byte-identically from its
``unified_payload`` (agent-engine-extraction D11).

Redaction: every leaf string is scrubbed of secrets and PII-shaped values, and
auth-bearing keys are dropped outright, before anything is written. Nothing
leaves the DB unredacted.

Usage:
    uv run python packages/matrx-ai/scripts/export_conformance_corpus.py --report
    uv run python packages/matrx-ai/scripts/export_conformance_corpus.py --out corpus/wire

Requires DIRECT Postgres egress. A cloud agent container whose egress is
proxy-only cannot reach the pooler and will time out in ``asyncpg.connect`` —
run this from a machine with real DB access, or reproduce the coverage report
with the equivalent SQL through the Supabase MCP (the query is mirrored in
common-docs `projects/agent-engine-extraction/CORPUS.md`).
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import re
from collections import Counter
from pathlib import Path
from typing import Any

_DROP_KEYS = {
    "authorization", "api_key", "apikey", "x-api-key", "key", "token",
    "access_token", "refresh_token", "secret", "password", "cookie",
    "anthropic-api-key", "openai-api-key", "bearer",
}
_SCRUB = [
    (re.compile(r"sk-[A-Za-z0-9_\-]{16,}"), "<REDACTED_KEY>"),
    (re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]{2,}\b"), "<REDACTED_EMAIL>"),
    (re.compile(r"\b(?:\+?\d[\d\s().-]{8,}\d)\b"), "<REDACTED_PHONE>"),
    (re.compile(r"\bBearer\s+[A-Za-z0-9._\-]+", re.I), "Bearer <REDACTED>"),
    (re.compile(r"eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"), "<REDACTED_JWT>"),
]


def redact(node: Any) -> Any:
    if isinstance(node, dict):
        return {
            k: ("<REDACTED>" if k.lower() in _DROP_KEYS else redact(v))
            for k, v in node.items()
        }
    if isinstance(node, list):
        return [redact(v) for v in node]
    if isinstance(node, str):
        out = node
        for pat, rep in _SCRUB:
            out = pat.sub(rep, out)
        return out
    return node


def wire_shape(payload: dict) -> str:
    """Which of the four wire shapes this payload is (D9)."""
    if not isinstance(payload, dict):
        return "other"
    if "contents" in payload:
        return "google_gemini"
    if "input" in payload and "messages" not in payload:
        return "openai_responses"
    if "system" in payload and "messages" in payload:
        return "anthropic_messages"
    if "messages" in payload:
        return "openai_chat_completions"
    return "other"


def shape_key(unified: dict, request: dict, provider: str, model: str) -> str:
    """Dedupe key: the STRUCTURE of a case, not its content.

    Two rows collapse when they exercise the same translator path — same wire
    shape, same set of config keys, same set of payload keys, same feature
    flags. Content differences (the user's actual prompt) do not create a new
    case; structural ones do.
    """
    feats = (
        wire_shape(request),
        provider or "?",
        "tools" if request.get("tools") else "-",
        "stream" if request.get("stream") else "-",
        "structured" if ("response_format" in request or "text" in request) else "-",
        "thinking" if any(k in request for k in ("thinking", "reasoning", "reasoning_effort")) else "-",
        "|".join(sorted(k for k in request if not k.startswith("_"))),
        "|".join(sorted(k for k in (unified or {}) if not k.startswith("_"))),
    )
    return hashlib.sha256("::".join(feats).encode()).hexdigest()[:16]


SQL = """
select id::text, provider, model, unified_payload, request_payload
from chat.request_snapshot
where deleted_at is null
  and unified_payload is not null and request_payload is not null
  and unified_payload::text <> 'null' and request_payload::text <> 'null'
order by created_at desc
"""


async def fetch() -> list[dict]:
    import asyncpg

    dsn = (
        f"postgresql://{os.environ['SUPABASE_MATRIX_USER']}:"
        f"{os.environ['SUPABASE_MATRIX_PASSWORD']}@"
        f"{os.environ['SUPABASE_MATRIX_HOST']}:{os.environ['SUPABASE_MATRIX_PORT']}/"
        f"{os.environ['SUPABASE_MATRIX_DATABASE_NAME']}"
    )
    conn = await asyncpg.connect(dsn, statement_cache_size=0)
    try:
        rows = await conn.fetch(SQL)
    finally:
        await conn.close()
    out = []
    for r in rows:
        try:
            out.append({
                "id": r["id"],
                "provider": r["provider"] or "",
                "model": r["model"] or "",
                "unified": json.loads(r["unified_payload"]) if isinstance(r["unified_payload"], str) else r["unified_payload"],
                "request": json.loads(r["request_payload"]) if isinstance(r["request_payload"], str) else r["request_payload"],
            })
        except Exception:
            continue
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None, help="write deduped cases here")
    ap.add_argument("--report", action="store_true", help="coverage report only")
    args = ap.parse_args()

    rows = asyncio.run(fetch())

    cases: dict[str, dict] = {}
    dupes = Counter()
    for r in rows:
        if not isinstance(r["request"], dict):
            continue
        k = shape_key(r["unified"] or {}, r["request"], r["provider"], r["model"])
        dupes[k] += 1
        cases.setdefault(k, r)

    by_shape = Counter(wire_shape(c["request"]) for c in cases.values())
    by_provider = Counter(c["provider"] or "(unstamped)" for c in cases.values())
    tool_cases = sum(1 for c in cases.values() if c["request"].get("tools"))
    models = {c["model"] for c in cases.values() if c["model"]}

    print(f"\nCONFORMANCE CORPUS — {len(rows)} production rows -> {len(cases)} distinct cases\n")
    print("BY WIRE SHAPE (the four translators the TS twin must implement)")
    for s, n in by_shape.most_common():
        print(f"  {s:<28} {n:>4} cases")
    print(f"\nBY PROVIDER")
    for p, n in by_provider.most_common():
        print(f"  {p:<28} {n:>4} cases")
    print(f"\n  cases exercising tools      {tool_cases:>4}")
    print(f"  distinct models covered     {len(models):>4}")
    print(f"  largest dedupe bucket       {max(dupes.values()):>4} rows collapsed into 1 case")

    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        for k, c in cases.items():
            (args.out / f"{wire_shape(c['request'])}__{k}.json").write_text(
                json.dumps(
                    {
                        "case_id": k,
                        "provider": c["provider"],
                        "model": c["model"],
                        "input_unified_config": redact(c["unified"]),
                        "expected_provider_payload": redact(c["request"]),
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
        print(f"\n  wrote {len(cases)} redacted cases to {args.out}/")
    else:
        print("\n  (report only — pass --out DIR to write the redacted cases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
