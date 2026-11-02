"""Call INTENT: why a call was made (operator 2026-10-06) — grading, smoke-test,
generation, ... — separate from the call's identity (request_id) and from the
model task it runs (chat, embeddings, text-to-image, ...).

It is not tracked anywhere of its own: it rides the call's request as
``metadata.intent`` and so lands in the call's own call_log row
(request_body.metadata). Every view filters on that. Rows written before intent
existed read through ``SQL`` below: a test-fire row whose own run metadata says
grade true/false is grading/smoke-test; anything else is "unlabeled" (never guessed)."""
from __future__ import annotations

from typing import Optional

GENERATION = "generation"     # an ordinary caller asking for output (the default)
GRADING = "grading"           # a graded curriculum item (test-fire with grading)
SMOKE_TEST = "smoke-test"     # does it load and answer (test-fire without grading)

# intent of a call_log / call_log_derived row, as a SQL expression
SQL = ("coalesce(request_body->'metadata'->>'intent',"
       " CASE request_body->'metadata'->'test_fire'->>'grade'"
       "   WHEN 'true' THEN 'grading' WHEN 'false' THEN 'smoke-test' ELSE 'unlabeled' END)")


def stamp(metadata: Optional[dict], intent: Optional[str] = None,
          default: str = GENERATION) -> dict:
    """The caller's metadata with ``intent`` set: the caller's own label wins,
    then ``intent``, then ``default``."""
    md = dict(metadata) if isinstance(metadata, dict) else {}
    if not (isinstance(md.get("intent"), str) and md["intent"].strip()):
        md["intent"] = (intent or default).strip()
    return md
