"""Curiosity-driven GraphRAG corpus growth.

Closes the loop the operator described:
    session encounters unfamiliar subject
      → curiosity.gap_detector emits unknown_term event
      → THIS MODULE processes the queue
      → drafts a chunk to /data3/drydock_cookbook/_staging/
      → operator reviews via `manage.sh review`
      → promotes safe drafts into the main cookbook
      → next session's auto-prefetch surfaces the new content

Design principles:
  - **Never touches the main cookbook directly.** Drafts land in
    /data3/drydock_cookbook/_staging/ and require explicit operator promote
    (manage.sh promote <slug>). Keeps the curated cookbook quality bar.
  - **Three signal sources, ranked:**
      (1) AUTO-RETRIEVE log lines that returned 0 above-threshold hits —
          confirmed gaps (the model literally tried to retrieve and got
          nothing).
      (2) unknown_term events from curiosity.jsonl with frequency >= 2
          across recent events.
      (3) unknown_term events with code-grep matches in the project tree
          (these are mechanically extractable; lowest-risk content).
  - **Aggressive deduplication.** A term/query is processed ONCE per
    week unless its staging draft was rejected (in which case it returns
    to the queue with a backoff multiplier).
  - **Idempotent.** Safe to run on a cron tick; state lives in
    ~/.drydock/curiosity_ingested.json so re-runs don't churn.

CLI:
    python3 -m drydock.curiosity.ingest --once       # process one batch
    python3 -m drydock.curiosity.ingest --review     # list staging
    python3 -m drydock.curiosity.ingest --promote SLUG
    python3 -m drydock.curiosity.ingest --reject SLUG
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import hashlib
import json
import logging
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

logger = logging.getLogger(__name__)

# ── paths ──────────────────────────────────────────────────────────────

COOKBOOK_ROOT = Path("/data3/drydock_cookbook")
STAGING_DIR = COOKBOOK_ROOT / "_staging"
CURIOSITY_QUEUE = Path.home() / ".drydock" / "dispatch" / "curiosity.jsonl"
DRYDOCK_LOG = Path.home() / ".drydock" / "logs" / "drydock.log"
STATE_PATH = Path.home() / ".drydock" / "curiosity_ingested.json"
COOKBOOK_DB = Path.home() / ".drydock" / "graphrag.sqlite"

# Source trees the code-grep step searches for a term's definition.
GREP_ROOTS = [
    Path("/data3/drydock/drydock"),
    Path("/data3/drydock_test_projects"),
    Path("/data3/drydock_cookbook"),
]

# Tuning knobs.
MIN_TERM_LENGTH = 4
MIN_TERM_FREQUENCY = 2          # need 2+ unknown_term events for a term
MAX_STAGING_PER_RUN = 5         # cap chunks created per --once invocation
RECENT_EVENTS_WINDOW = 2000     # how many events to scan from the tail
DUPLICATE_BACKOFF_DAYS = 7      # don't re-stage the same term for this long
PRIMARY_DB_NOISE_HIT_THRESHOLD = 8.0  # matches agent_loop's auto-prefetch

# Terms that look like noise even after gap_detector filtering.
EXTRA_NOISE = {
    # Generic prose fragments that slip past _is_template_noise
    "TRACE", "FINDINGS", "ANSWER", "REGEXES", "AUTH_MATRIX",
    "DATA_ISSUES", "EVICTION_NOTES", "CLARIFICATION", "API_AUDIT",
    "PRD", "TODO", "FIXME", "NOTE", "BUG",
    # Generic Python tokens
    "self", "cls", "args", "kwargs", "this", "that",
    # Common file-extension-as-suffix junk
    "json", "yaml", "toml", "md", "py", "txt",
}

ENGLISH_STOPISH = {
    "scratch", "fail", "pass", "tests", "test", "green", "cause", "stop",
    "step", "run", "build", "init", "ready", "found", "needed", "wanted",
    "given", "first", "second", "third", "yes", "no", "maybe", "true",
    "false", "none", "null", "result", "value", "data", "input", "output",
    "error", "warning", "info", "debug",
}

# Compound-term noise patterns. gap_detector's _RE_DOTTED_IDENT eagerly
# matches "scratch.Step" as a single dotted-identifier, but it's really
# two adjacent English-prose words. Filter compounds where each piece
# is an English stopword.
_DOTTED_NOISE_RE = re.compile(r"^[A-Za-z]+\.[A-Z][a-z]+$")


def _is_compound_noise(term: str) -> bool:
    """True if `term` looks like `english_word.English_word` (gauntlet
    output crud like `scratch.Step`, `fail.Step`, `tests.Step`)."""
    if not _DOTTED_NOISE_RE.match(term):
        return False
    left, right = term.lower().split(".", 1)
    return left in ENGLISH_STOPISH and right in ENGLISH_STOPISH


# ── state ──────────────────────────────────────────────────────────────

def _load_state() -> dict:
    if not STATE_PATH.is_file():
        return {"ingested": {}, "rejected": {}}
    try:
        return json.loads(STATE_PATH.read_text())
    except Exception:
        return {"ingested": {}, "rejected": {}}


def _save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True))


def _slug(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9._-]+", "_", name).strip("_.")
    return s.lower()[:80] or "unnamed"


def _recently_handled(state: dict, key: str) -> bool:
    """True if the term was ingested or rejected within DUPLICATE_BACKOFF_DAYS."""
    for bucket in ("ingested", "rejected"):
        entry = state.get(bucket, {}).get(key)
        if not entry:
            continue
        ts = entry.get("ts")
        if not ts:
            continue
        try:
            when = dt.datetime.fromisoformat(ts.rstrip("Z")).replace(
                tzinfo=dt.timezone.utc
            )
        except Exception:
            continue
        if (dt.datetime.now(dt.timezone.utc) - when).days < DUPLICATE_BACKOFF_DAYS:
            return True
    return False


# ── signal harvesting ─────────────────────────────────────────────────


def _is_noisy_term(term: str) -> bool:
    if not term or len(term) < MIN_TERM_LENGTH:
        return True
    if term in EXTRA_NOISE:
        return True
    if term.lower() in ENGLISH_STOPISH:
        return True
    # All-digit tokens
    if term.isdigit():
        return True
    # Looks like a sentence fragment (has spaces but also stopwords at the start)
    if " " in term and term.split()[0].lower() in ENGLISH_STOPISH:
        return True
    if _is_compound_noise(term):
        return True
    # Apostrophe-split sentence fragments — gap_detector eagerly grabs
    # quoted strings and "Don't edit any test" becomes "t edit any test"
    # when an outer quote splits on the apostrophe. These are always
    # multi-word with a tiny first token.
    if " " in term:
        words = term.split()
        if len(words) >= 4:
            return True            # too many words to be a single concept
        if words and len(words[0]) <= 2 and words[0].lower() not in {"io", "os", "re", "ai", "ml"}:
            return True            # starts with a sentence fragment like "t edit"
    return False


def _read_curiosity_events(limit: int = RECENT_EVENTS_WINDOW) -> list[dict]:
    if not CURIOSITY_QUEUE.is_file():
        return []
    lines = CURIOSITY_QUEUE.read_text(errors="replace").splitlines()
    out = []
    for line in lines[-limit:]:
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            continue
    return out


def _harvest_unknown_terms(state: dict) -> list[tuple[str, int, str]]:
    """Returns [(term, frequency, sample_context), ...] sorted by frequency desc.

    Filters: noise terms, recently-handled terms, terms already present
    as cookbook chunk names.
    """
    events = _read_curiosity_events()
    counter: collections.Counter[str] = collections.Counter()
    sample_ctx: dict[str, str] = {}
    for ev in events:
        if ev.get("kind") != "unknown_term":
            continue
        term = (ev.get("term") or "").strip()
        if not term or _is_noisy_term(term):
            continue
        counter[term] += 1
        if term not in sample_ctx:
            sample_ctx[term] = (ev.get("context") or "")[:400]

    out = []
    for term, freq in counter.most_common():
        if freq < MIN_TERM_FREQUENCY:
            break  # most_common is sorted desc; once below threshold, done
        if _recently_handled(state, f"term:{term}"):
            continue
        if _term_already_covered(term):
            continue   # cookbook already mentions this term — not a gap
        out.append((term, freq, sample_ctx.get(term, "")))
    return out


def _term_already_covered(term: str) -> bool:
    """True if any cookbook chunk's content mentions this term."""
    try:
        import sqlite3
    except Exception:
        return False
    if not COOKBOOK_DB.is_file():
        return False
    try:
        con = sqlite3.connect(COOKBOOK_DB)
        cur = con.cursor()
        # Try exact term-match against text_terms (lowercased).
        rows = cur.execute(
            "SELECT COUNT(*) FROM text_terms WHERE term = ? LIMIT 1",
            (term.lower(),),
        ).fetchone()
        con.close()
        if rows and rows[0] > 0:
            return True
        # Fall back to substring search on content (for compound terms like
        # `__init__.__all__` that get split during tokenisation).
        con = sqlite3.connect(COOKBOOK_DB)
        cur = con.cursor()
        rows = cur.execute(
            "SELECT COUNT(*) FROM text_chunks WHERE content LIKE ? LIMIT 1",
            (f"%{term}%",),
        ).fetchone()
        con.close()
        return bool(rows and rows[0] > 0)
    except Exception:
        return False


def _harvest_zero_hit_queries(state: dict, hours: int = 2) -> list[str]:
    """AUTO-RETRIEVE queries that returned 0 above-threshold hits.

    These are the strongest signal: the auto-prefetch hook literally
    asked the corpus a question and got nothing useful back.

    Tight time window (default 2h) — older zero-hits often refer to
    gaps that have since been filled by hand-written chunks, and a
    fresh DB query would now find them. Re-checking each candidate
    against the current DB (in `_is_still_a_gap`) catches the
    leftover stragglers.
    """
    if not DRYDOCK_LOG.is_file():
        return []
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=hours)
    last_query = None
    zeros: collections.Counter[str] = collections.Counter()
    for line in DRYDOCK_LOG.read_text(errors="replace").splitlines():
        if "[AUTO-RETRIEVE]" not in line:
            continue
        m = re.match(r"(\S+)", line)
        try:
            ts = dt.datetime.fromisoformat(m.group(1))
        except Exception:
            continue
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=dt.timezone.utc)
        if ts < cutoff:
            continue
        m2 = re.search(r"extracted query: (.+)$", line)
        if m2:
            last_query = m2.group(1).strip()
            continue
        if (": 0 total hits" in line or ", 0 above threshold" in line) and last_query:
            zeros[last_query[:200]] += 1

    out = []
    for q, n in zeros.most_common():
        if n < MIN_TERM_FREQUENCY:
            break
        if _recently_handled(state, f"query:{hashlib.sha1(q.encode()).hexdigest()[:12]}"):
            continue
        if not _is_still_a_gap(q):
            continue   # the gap was filled by a hand-written chunk — skip
        out.append(q)
    return out


def _is_still_a_gap(query: str) -> bool:
    """Re-query the current cookbook DB; True if it still scores below threshold."""
    try:
        import sqlite3, math
    except Exception:
        return True
    if not COOKBOOK_DB.is_file():
        return True
    try:
        con = sqlite3.connect(COOKBOOK_DB)
        cur = con.cursor()
        # crude BM25: just count distinct text_chunks that match any term
        # in the query above the threshold; cheap enough for periodic use.
        terms = [t.lower() for t in re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]{3,}\b", query)][:25]
        if not terms:
            return True
        placeholders = ",".join("?" * len(terms))
        # If ANY chunk's tf-sum across query terms is high, we have coverage.
        rows = cur.execute(
            f"""
            SELECT chunk_id, SUM(tf) as score
            FROM text_terms
            WHERE term IN ({placeholders})
            GROUP BY chunk_id
            ORDER BY score DESC
            LIMIT 1
            """,
            terms,
        ).fetchall()
        con.close()
        if not rows:
            return True
        top_score = rows[0][1] or 0
        # If our cheap proxy score >> threshold, the gap is closed.
        return top_score < PRIMARY_DB_NOISE_HIT_THRESHOLD
    except Exception:
        return True


# ── chunk producers ────────────────────────────────────────────────────


@dataclass
class Draft:
    slug: str
    kind: str            # "code-symbol", "missing-knowledge"
    term: str
    body: str
    source: str          # "grep" | "queue" | "log"
    auto_safe: bool      # True if we believe the content is mechanically safe


def _grep_for_term(term: str) -> list[tuple[Path, int, str]]:
    """Return [(file_path, line_no, line_text), ...] hits for `term`.

    Limits to GREP_ROOTS so we don't crawl arbitrary directories. Caps the
    total hit count to keep the output bounded.
    """
    hits: list[tuple[Path, int, str]] = []
    for root in GREP_ROOTS:
        if not root.is_dir():
            continue
        try:
            r = subprocess.run(
                ["grep", "-rnE", "--include=*.py", "--include=*.md",
                 f"\\b{re.escape(term)}\\b", str(root)],
                capture_output=True, text=True, timeout=10,
            )
        except Exception:
            continue
        for line in r.stdout.splitlines()[:30]:
            try:
                path_s, lineno_s, *rest = line.split(":", 2)
                hits.append((Path(path_s), int(lineno_s), ":".join(rest)))
            except Exception:
                continue
        if len(hits) >= 30:
            break
    return hits


def _extract_def_chunk(file_path: Path, line_no: int) -> str | None:
    """If `term` appears as a def/class definition, return ~10 lines around it."""
    try:
        lines = file_path.read_text(errors="replace").splitlines()
    except Exception:
        return None
    if line_no <= 0 or line_no > len(lines):
        return None
    # Look back up to 30 lines for a `def <term>` or `class <term>` header.
    start = max(0, line_no - 30)
    for i in range(line_no - 1, start - 1, -1):
        if re.match(r"\s*(def|class|async def)\s+\w", lines[i]):
            # extract up to 25 lines starting here
            end = min(len(lines), i + 25)
            return "\n".join(lines[i:end])
    return None


def _make_code_symbol_draft(term: str, freq: int, context: str) -> Draft | None:
    """If `term` appears as a function/class def somewhere reachable, draft a chunk."""
    hits = _grep_for_term(term)
    def_hits = []
    for fp, lno, line in hits:
        if re.search(rf"\b(def|class|async def)\s+{re.escape(term)}\b", line):
            def_hits.append((fp, lno))
    if not def_hits:
        return None

    # Take the first def site (deterministic enough; operator can refine).
    fp, lno = def_hits[0]
    snippet = _extract_def_chunk(fp, lno)
    if not snippet:
        return None

    slug = f"sym_{_slug(term)}"
    body = (
        f"# `{term}` — code-symbol reference\n"
        f"\n"
        f"Auto-extracted by curiosity ingest after observing {freq} unknown-term "
        f"events for this identifier. Source: {fp}:{lno}.\n"
        f"\n"
        f"## Definition site\n\n"
        f"```python\n{snippet}\n```\n"
        f"\n"
        f"## Other references in tree\n"
    )
    refs = [
        (f, l)
        for (f, l, ln) in hits
        if not re.search(rf"\b(def|class|async def)\s+{re.escape(term)}\b", ln)
    ][:8]
    if refs:
        for f, l in refs:
            body += f"- `{f}:{l}`\n"
    else:
        body += "- _(no other references found)_\n"
    body += (
        f"\n## Context where the gap was detected\n\n"
        f"> {context[:300]}{'…' if len(context) > 300 else ''}\n"
    )
    return Draft(
        slug=slug, kind="code-symbol", term=term, body=body,
        source="grep", auto_safe=True,
    )


def _make_missing_knowledge_draft(term: str, freq: int, context: str) -> Draft:
    """Stub for a term we couldn't ground in code. Operator drafts the content."""
    slug = f"todo_{_slug(term)}"
    body = (
        f"# `{term}` — knowledge gap (TODO)\n"
        f"\n"
        f"Auto-staged by curiosity ingest after {freq} unknown-term events for "
        f"this token. Grep across `{', '.join(str(r) for r in GREP_ROOTS)}` "
        f"did NOT find a definition.\n"
        f"\n"
        f"## Sample context where the gap appeared\n\n"
        f"> {context[:400]}{'…' if len(context) > 400 else ''}\n"
        f"\n"
        f"## TODO\n\n"
        f"- [ ] If this is a real subject (not noise), write the reference content here.\n"
        f"- [ ] If this is noise (false positive from gap_detector), reject this draft:\n"
        f"      `python3 -m drydock.curiosity.ingest --reject {slug}`\n"
    )
    return Draft(
        slug=slug, kind="missing-knowledge", term=term, body=body,
        source="queue", auto_safe=False,
    )


def _make_zero_hit_draft(query: str) -> Draft:
    qhash = hashlib.sha1(query.encode()).hexdigest()[:12]
    slug = f"gap_{qhash}"
    body = (
        f"# Retrieval gap: {qhash}\n"
        f"\n"
        f"The auto-prefetch hook scored 0 above-threshold (≥{PRIMARY_DB_NOISE_HIT_THRESHOLD}) "
        f"chunks for this query.\n"
        f"\n"
        f"## Query\n\n"
        f"> {query[:600]}{'…' if len(query) > 600 else ''}\n"
        f"\n"
        f"## TODO\n\n"
        f"- [ ] Identify what subject this query is asking about.\n"
        f"- [ ] If the cookbook should cover it, write a chunk and re-ingest.\n"
        f"- [ ] If the query is one-off noise, reject:\n"
        f"      `python3 -m drydock.curiosity.ingest --reject {slug}`\n"
    )
    return Draft(
        slug=slug, kind="missing-knowledge", term=query[:80], body=body,
        source="log", auto_safe=False,
    )


# ── promote / reject ──────────────────────────────────────────────────


def _staging_path(slug: str) -> Path:
    return STAGING_DIR / f"{slug}.md"


def _write_staging(draft: Draft) -> Path:
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    path = _staging_path(draft.slug)
    if path.is_file():
        return path  # idempotent — don't clobber
    path.write_text(draft.body)
    return path


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def promote(slug: str, target_subdir: str = "python") -> Path | None:
    """Move a staged draft to /data3/drydock_cookbook/<target_subdir>/<slug>.md."""
    src = _staging_path(slug)
    if not src.is_file():
        print(f"no staged draft named {slug!r}")
        return None
    dst = COOKBOOK_ROOT / target_subdir / src.name
    dst.parent.mkdir(parents=True, exist_ok=True)
    src.replace(dst)
    state = _load_state()
    state.setdefault("ingested", {})[f"slug:{slug}"] = {"ts": _now(), "path": str(dst)}
    _save_state(state)
    print(f"promoted: {src} → {dst}")
    return dst


def reject(slug: str) -> bool:
    src = _staging_path(slug)
    if not src.is_file():
        print(f"no staged draft named {slug!r}")
        return False
    src.unlink()
    state = _load_state()
    # remember it so we don't re-stage immediately
    state.setdefault("rejected", {})[f"slug:{slug}"] = {"ts": _now()}
    _save_state(state)
    print(f"rejected: {src}")
    return True


def review() -> None:
    if not STAGING_DIR.is_dir():
        print("no staging dir")
        return
    drafts = sorted(STAGING_DIR.glob("*.md"))
    if not drafts:
        print("staging is empty")
        return
    for d in drafts:
        text = d.read_text()
        first_heading = next(
            (line for line in text.splitlines() if line.startswith("# ")),
            d.stem,
        )
        print(f"  {d.stem:40s} {first_heading[:60]}")


# ── orchestration ─────────────────────────────────────────────────────


def run_once(include_prose: bool = False) -> dict:
    """Process one batch of signals; return a report dict.

    Default (autonomous-safe): only stages code-symbol drafts where
    a grep against project source produced a real definition site.
    Prose TODO stubs (where no def was found) are noisier and require
    `include_prose=True`.
    """
    state = _load_state()
    created: list[Draft] = []
    skipped_existing = 0
    skipped_no_def = 0

    # Signal 1: zero-hit retrieve queries (strongest signal, but currently
    # we can only stub these — operator must write the chunk). Only when
    # include_prose=True.
    if include_prose:
        for q in _harvest_zero_hit_queries(state):
            if len(created) >= MAX_STAGING_PER_RUN:
                break
            draft = _make_zero_hit_draft(q)
            if _staging_path(draft.slug).is_file():
                skipped_existing += 1
                continue
            _write_staging(draft)
            key = f"query:{hashlib.sha1(q.encode()).hexdigest()[:12]}"
            state.setdefault("ingested", {})[key] = {"ts": _now(), "slug": draft.slug}
            created.append(draft)

    # Signal 2: high-frequency unknown_terms with code-grep matches.
    # Auto-safe: only stage when we found a real def site in the tree.
    for term, freq, ctx in _harvest_unknown_terms(state):
        if len(created) >= MAX_STAGING_PER_RUN:
            break
        draft = _make_code_symbol_draft(term, freq, ctx)
        if draft is None:
            skipped_no_def += 1
            if not include_prose:
                # Mark this term as handled so we don't re-evaluate it
                # next tick — but with a shorter backoff in case a def
                # gets added to the tree later.
                state.setdefault("rejected", {})[f"term:{term}"] = {
                    "ts": _now(), "reason": "no-def-site",
                }
                continue
            draft = _make_missing_knowledge_draft(term, freq, ctx)
        if _staging_path(draft.slug).is_file():
            skipped_existing += 1
            continue
        _write_staging(draft)
        state.setdefault("ingested", {})[f"term:{term}"] = {
            "ts": _now(), "slug": draft.slug, "kind": draft.kind,
        }
        created.append(draft)

    _save_state(state)

    report = {
        "drafts_created": len(created),
        "skipped_existing": skipped_existing,
        "skipped_no_def_site": skipped_no_def,
        "details": [
            {"slug": d.slug, "kind": d.kind, "term": d.term, "source": d.source}
            for d in created
        ],
    }
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="drydock.curiosity.ingest")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--once", action="store_true",
                   help="process one batch of curiosity signals into _staging/")
    g.add_argument("--review", action="store_true",
                   help="list staged drafts")
    g.add_argument("--promote", metavar="SLUG",
                   help="promote a staged draft into the main cookbook")
    g.add_argument("--reject", metavar="SLUG",
                   help="reject a staged draft (deletes it; backs off re-staging)")
    ap.add_argument("--target-subdir", default="python",
                    help="for --promote: cookbook subdir (default: python)")
    ap.add_argument("--include-prose", action="store_true",
                    help="for --once: also stage prose TODO stubs (noisier; operator-review-heavy)")

    args = ap.parse_args(argv)

    if args.once:
        report = run_once(include_prose=args.include_prose)
        print(json.dumps(report, indent=2))
        return 0
    if args.review:
        review()
        return 0
    if args.promote:
        return 0 if promote(args.promote, args.target_subdir) else 1
    if args.reject:
        return 0 if reject(args.reject) else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
