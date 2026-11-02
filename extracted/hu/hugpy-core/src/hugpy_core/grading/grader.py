# LIFTED from hugpy_curation.review.fleet_grading (read-only reference): the tiered
# text suite (TASKS_TIERED: 9 categories x easy/medium/hard), its checkers (_ints,
# _r, _last, _has, _exact, _json_eq) and the /no_think prompt suffix — VERBATIM.
# think stripping lifted from hugpy_platform.no_think.strip_think.
# NEW: the curriculum (next ungraded item per model) and the grades table writer.
"""Tiered grading curriculum, deterministic checkers and grade persistence owned by Core.

Test-fire asks each model its NEXT ungraded item — every easy item across the
categories first, then medium, then hard — until all remaining items are graded.
Checkers are deterministic (no judge model). A grade is a pointer into the
wrapper's call log (request_id) plus the verdict; scores are rollups.
"""
from __future__ import annotations
from hugpy_core.imports import functions as _F

from contextlib import contextmanager
import json
import os
import re
from typing import Optional

DB = _F.core_dsn()
SUITE = "hugpy-native-v2"
TOKENS = 256                 # per item: enough to answer after a short think
NO_THINK = " /no_think"


# ── checkers (verbatim) ──────────────────────────────────────────────────────
def _ints(s): return [int(x) for x in re.findall(r"-?\d+", s or "")]


def _r(rule, fn, answer=None):
    fn.rule = rule
    fn.answer = answer
    return fn


def _last(n): return _r(f"last number == {n}", lambda s: _ints(s)[-1:] == [n], str(n))
def _has(word): return _r(f"contains {word!r} (case-insensitive)", lambda s: word.lower() in (s or "").lower(), word)
def _exact(value): return _r(f"reply == {value!r} exactly", lambda s: (s or "").strip() == value, value)


def _json_eq(expected):
    def check(value):
        match = re.search(r"\{.*\}", value or "", re.S)
        try: return bool(match) and json.loads(match.group(0)) == expected
        except ValueError: return False
    return _r(f"JSON object == {json.dumps(expected)}", check, json.dumps(expected))


TASKS_TIERED = {
    "math": (("easy", "Compute 15 + 22. Reply with only the final number.", _last(37)),
             ("medium", "Compute 17 * 23. Reply with only the final number.", _last(391)),
             ("hard", "Solve for x: 3x + 12 = 27. Reply with only the number.", _last(5))),
    "wordprob": (("easy", "John has 5 apples. He buys 3 more. How many? Reply number only.", _last(8)),
                 ("medium", "A store had 48 apples. Sold 19 in the morning, 12 in the afternoon. Left? Reply number only.", _last(17)),
                 ("hard", "Train A leaves at 60mph. 2 hours later Train B leaves at 80mph. Hours until they meet? Reply number only.", _last(6))),
    "factual": (("easy", "What planet is known as the Red Planet? Reply with only the planet name.", _has("mars")),
                ("medium", "What is the chemical symbol for gold? Reply with only the symbol.", _has("au")),
                ("hard", "Who discovered penicillin? Reply with only the last name.", _has("fleming"))),
    "format_primes": (("easy", "List the first three prime numbers separated by commas and nothing else.", _r("first 3 integers == [2, 3, 5]", lambda s: _ints(s)[:3] == [2, 3, 5], "2, 3, 5")),
                      ("medium", "List the first five prime numbers separated by commas and nothing else.", _r("first 5 integers == [2, 3, 5, 7, 11]", lambda s: _ints(s)[:5] == [2, 3, 5, 7, 11], "2, 3, 5, 7, 11")),
                      ("hard", "List the first five prime numbers in reverse order separated by commas and nothing else.", _r("first 5 integers == [11, 7, 5, 3, 2]", lambda s: _ints(s)[:5] == [11, 7, 5, 3, 2], "11, 7, 5, 3, 2"))),
    "logic": (("easy", "If all bloops are razzies, and all razzies are lazzies, are all bloops lazzies? Answer yes or no.", _has("yes")),
              ("medium", "A is taller than B. C is shorter than B. Who is the shortest? Reply only with the letter.", _r("reply == 'c' (case-insensitive)", lambda s: (s or "").strip().lower() == "c", "C")),
              ("hard", "Can a 3-gallon jug and a 5-gallon jug measure exactly 4 gallons? Answer yes or no.", _has("yes"))),
    "exact_instruction": (("easy", "Reply with exactly the single word: BANANA", _exact("BANANA")),
                          ("medium", "Reply with exactly the single word: BANANA, but in lowercase.", _exact("banana")),
                          ("hard", "Reply with exactly the string: [BANANA_123] and absolutely nothing else.", _exact("[BANANA_123]"))),
    "coding": (("easy", "Write a Python one-liner using sum() to total a list named xs. Reply with only code.", _r("code contains sum(xs)", lambda s: "sum(xs)" in re.sub(r"\s+", "", s or ""), "total = sum(xs)")),
               ("medium", "Write a Python list comprehension returning only even numbers from list xs. Reply with only code.", _r("code contains %2==0", lambda s: "%2==0" in re.sub(r"\s+", "", s or ""), "[x for x in xs if x % 2 == 0]")),
               ("hard", "Write a recursive Python lambda named fib for Fibonacci. Reply with only code.", _r("code has lambda, -1 and -2", lambda s: "lambda" in s and "-1" in s and "-2" in s, "fib = lambda n: n if n < 2 else fib(n-1) + fib(n-2)"))),
    "json": (("easy", 'Output only a JSON object with key "a" set to 1.', _json_eq({"a": 1})),
             ("medium", 'Output only a JSON object with keys "a" set to 1 and "b" set to 2.', _json_eq({"a": 1, "b": 2})),
             ("hard", 'Output only a JSON object with key "a" containing a list of 1 and 2.', _json_eq({"a": [1, 2]}))),
    "letters": (("easy", "How many times does the letter e appear in the word tree? Reply number only.", _last(2)),
                ("medium", "How many times does the letter r appear in the word strawberry? Reply number only.", _last(3)),
                ("hard", "How many times does the letter s appear in the word mississippi? Reply number only.", _last(4))),
}

TIER_ORDER = ("easy", "medium", "hard")
# The curriculum: every easy item across the categories, then medium, then hard.
CURRICULUM = [(cat, tier, prompt, chk)
              for t in TIER_ORDER
              for cat, tiers in TASKS_TIERED.items()
              for tier, prompt, chk in tiers if tier == t]

_THINK = re.compile(r"<think>(.*?)(?:</think>|\Z)", re.S | re.I)


def strip_think(text: str) -> str:
    """The prose without its reasoning: <think>…</think> blocks, an unclosed
    <think> (all reasoning), and an ORPHAN </think> — templates that open the
    think block in the prompt make the reply start mid-reasoning, so everything
    up to the last </think> is reasoning."""
    t = _THINK.sub("", text or "")
    if "</think>" in t.lower():
        t = t[t.lower().rindex("</think>") + len("</think>"):]
    return t.strip()




# ── the store ────────────────────────────────────────────────────────────────
def _db():
    import psycopg
    return psycopg.connect(DB, autocommit=True, connect_timeout=5)


def providers() -> dict:
    """Optional installed suite providers; never install media dependencies in core."""
    try:
        from hugpy_curation.review.testfire import providers as media_providers
    except ModuleNotFoundError as exc:
        if exc.name != "hugpy_curation":
            raise
        return {}
    return media_providers()


def suite_names() -> list[str]:
    return [SUITE, *providers()]


def suites_for_tasks(tasks) -> list[str]:
    tasks = set(tasks)
    out = [SUITE] if tasks & {"text-generation", "text2text-generation"} else []
    out.extend(name for name, adapter in providers().items() if tasks.intersection(adapter["tasks"]))
    return out


def curriculum(suite: str = SUITE) -> list:
    if suite == SUITE:
        return CURRICULUM
    registered = providers().get(suite)
    if registered is None:
        raise ValueError(f"Grading suite {suite!r} is not installed")
    return [(category, tier, spec, check) for level in TIER_ORDER
            for category, rows in registered["suite"].tasks.items()
            for tier, spec, check in rows if tier == level]


def _prompt(spec):
    return spec if isinstance(spec, str) else str(spec.get("text") or spec.get("prompt") or "")


def pending_items(model_key: str, suite: str = SUITE) -> list[dict]:
    """All remaining curriculum items, in tier/category order. An item counts as attempted once any worker graded it
    (passed true/false); a failed CALL (passed NULL) is retried next run."""
    with _db() as c:
        done = {(r[0], r[1]) for r in c.execute(
            "SELECT category, tier FROM grades WHERE model_key = %s AND suite = %s AND passed IS NOT NULL",
            (model_key, suite)).fetchall()}
    return [{"suite": suite, "category": cat, "tier": tier, "prompt": _prompt(prompt) + (NO_THINK if suite == SUITE else ""), "spec": prompt,
             "rule": getattr(chk, "rule", None), "expected": getattr(chk, "answer", None)}
            for cat, tier, prompt, chk in curriculum(suite) if (cat, tier) not in done]


@contextmanager
def test_turn(model_key: str):
    """Serialize selection + call + verdict across test callers/processes.

    This is a session lock, not a data collector or a second grading table.
    Closing the connection (including on a crash) releases it automatically.
    """
    with _db() as c:
        c.execute("SELECT pg_advisory_lock(hashtextextended(%s, 47382))", (model_key,))
        try:
            yield
        finally:
            c.execute("SELECT pg_advisory_unlock(hashtextextended(%s, 47382))", (model_key,))


def next_item(model_key: str, suite: str = SUITE) -> Optional[dict]:
    """First ungraded item in cumulative curriculum order, or None."""
    return next(iter(pending_items(model_key, suite)), None)


def check(item: dict, raw_text: str, response=None) -> "tuple[bool, str, Optional[str]]":
    """(passed, answer-as-checked, why-not)."""
    chk = next(c for cat, tier, _p, c in curriculum(item["suite"])
               if cat == item["category"] and tier == item["tier"])
    answer = strip_think(raw_text)
    if item["suite"] != SUITE:
        adapter = providers()[item["suite"]]
        passed = adapter["suite"].score(response, chk)
        return passed, str((response or {}).get("output") or answer), None if passed else str(getattr(chk, "rule", "media check failed"))
    if not answer.strip():
        return False, answer, "empty reply; expected " + str(getattr(chk, "answer", None))
    passed = bool(chk(answer))
    why = None if passed else f"got {answer[:200]!r}; expected {getattr(chk, 'answer', None)}"
    return passed, answer, why


def record(model_key: str, item: dict, *, request_id: Optional[str],
           passed: Optional[bool], why: Optional[str] = None, source: str = "test-fire",
           at: Optional[float] = None, **_legacy) -> bool:
    """Persist only the criterion, verdict and pointer. The call owns its data.
    One grade per call: a pointer that already has a grade is left alone (False).
    ``at`` = the call's own time when the grade is derived later (the fill)."""
    if not request_id:
        raise ValueError("A grade requires its call-log request_id")
    with _db() as c:
        cur = c.execute("INSERT INTO grades (at, model_key, suite, category, tier, request_id, passed, why, source)"
                        " SELECT coalesce(to_timestamp(%s::double precision), now()), %s,%s,%s,%s,%s,%s,%s,%s"
                        " WHERE NOT EXISTS (SELECT 1 FROM grades WHERE request_id = %s)",
                        (at, model_key, item["suite"], item["category"], item["tier"], request_id,
                         passed, why, source, request_id))
        return bool(cur.rowcount)


# ── grades derive from the call log ──────────────────────────────────────────
FILL_SETTLE_S = 120.0        # the caller that asked grades first; the fill takes what is left
_BY_PROMPT = {prompt: {"suite": SUITE, "category": cat, "tier": tier}
              for cat, tier, prompt, _chk in CURRICULUM}




def reply_text(payload):
    """The reply as the call row holds it (chat choices, a task's text, artifacts)."""
    if not isinstance(payload, dict):
        return None
    try:
        return payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        text = payload.get("text")
        if text is None and payload.get("artifacts"):
            text = json.dumps(payload["artifacts"], default=str)
        return text



def item_of(metadata, prompt) -> Optional[dict]:
    """Which curriculum item a grading call asked: the item the caller stamped
    (metadata.grade), else the text suite's item with exactly this prompt. None
    = not a text-suite item (a media suite scores a provider response, not text)."""
    grade = metadata.get("grade") if isinstance(metadata, dict) else None
    if isinstance(grade, dict):
        known = grade.get("suite") == SUITE and any(
            (cat, tier) == (grade.get("category"), grade.get("tier")) for cat, tier, _p, _c in CURRICULUM)
        return {"suite": SUITE, "category": grade["category"], "tier": grade["tier"]} if known else None
    text = (prompt or "").strip()
    return _BY_PROMPT.get(text.removesuffix(NO_THINK.strip()).strip())


def fill_from_call_log(since_s: float = 86400.0, settle_s: float = FILL_SETTLE_S) -> int:
    """Grade every answered grading call that has no grade yet (operator
    2026-10-06: "intent: grading resolves grading without a separate instance";
    "grader DB should auto-fill from call logs"). The call log is the source: a
    call whose own intent is grading and that asked a curriculum item is checked
    from its recorded reply, whoever sent it — a test-fire or benchmark whose
    core died before recording, or any client. Returns the grades written."""
    from hugpy_core.calllog import calllog
    pointers = calllog.grading_executions(since_s, settle_s)
    if not pointers:
        return 0
    with _db() as c:
        have = {r[0] for r in c.execute("SELECT request_id FROM grades WHERE request_id = ANY(%s)",
                                        ([i for pair in pointers for i in pair if i],)).fetchall()}
    filled = 0
    for call in calllog.grading_calls([e for e, central in pointers if e not in have and central not in have]):
        metadata = call["metadata"] if isinstance(call["metadata"], dict) else {}
        item = item_of(metadata, call["prompt"])
        if item is None or not call["model"]:
            continue
        passed, _answer, _why = check(item, reply_text(call["response_body"]) or "")
        source = "benchmark" if metadata.get("benchmark") else "test-fire" if metadata.get("test_fire") else "call-log"
        filled += record(call["model"], item, request_id=call["request_id"], passed=passed,
                         why=None if passed else "Response did not satisfy the suite criterion",
                         source=source, at=call["responded_at"])
    return filled


def summary(model_key: Optional[str] = None, suite: Optional[str] = None) -> list:
    """Rollup per model: items graded / passed / of the suite, depth per category
    (passed tiers), last graded."""
    if suite is None:
        return [row for name in suite_names() for row in summary(model_key, name)]
    entries = curriculum(suite)
    categories = list(dict.fromkeys(row[0] for row in entries))
    q = ("SELECT model_key, count(*) FILTER (WHERE passed IS NOT NULL), count(*) FILTER (WHERE passed),"
         " extract(epoch FROM max(at)), json_object_agg(category || ':' || tier, passed)"
         " FROM (SELECT DISTINCT ON (model_key, category, tier) model_key, category, tier, passed, at"
         "       FROM grades WHERE suite = %s AND passed IS NOT NULL"
         "       ORDER BY model_key, category, tier, at DESC) g"
         + (" WHERE model_key = %s" if model_key else "") + " GROUP BY model_key")
    with _db() as c:
        rows = c.execute(q, (suite, model_key) if model_key else (suite,)).fetchall()
    out = []
    for mk, graded, passed, last, items in rows:
        depth = {cat: sum(1 for t in TIER_ORDER if (items or {}).get(f"{cat}:{t}")) for cat in categories}
        out.append({"model_key": mk, "suite": suite, "graded": int(graded), "passed": int(passed),
                    "of": len(entries), "score": round(passed / len(entries), 4),
                    "depth": depth, "last_graded": float(last) if last else None})
    return out


def latest(model_key: Optional[str] = None, suite: Optional[str] = None) -> list:
    """The latest verdict per model x item (the grade rows the console reads)."""
    if suite is None:
        return [row for name in suite_names() for row in latest(model_key, name)]
    q = ("SELECT DISTINCT ON (model_key, category, tier) model_key, category, tier, passed, why,"
         " request_id, extract(epoch FROM at) FROM grades WHERE suite = %s AND passed IS NOT NULL"
         + (" AND model_key = %s" if model_key else "")
         + " ORDER BY model_key, category, tier, at DESC")
    with _db() as c:
        rows = c.execute(q, (suite, model_key) if model_key else (suite,)).fetchall()
    from hugpy_core.calllog import calllog
    ids = [row[5] for row in rows if row[5]]
    # exec_* = the EXECUTION row of the pointed call's chain (sql/009), resolved
    # by calllog.py (the one reader): a grade pointing at a core-/bench- hop still
    # shows the worker and quant that ran it — never a stored copy (grades.worker/
    # quant are dropped, sql/011).
    calls = calllog.by_request_ids(ids, ["exec_worker", "exec_quantization", "response_body"])
    out = []
    for model, category, tier, passed, why, rid, at in rows:
        c = calls.get(rid) or {}
        worker, quant, answer = c.get("exec_worker"), c.get("exec_quantization"), reply_text(c.get("response_body"))
        out.append({"model_key": model, "suite": suite, "category": category, "tier": tier,
                    "passed": passed, "why": why, "request_id": rid, "at": float(at),
                    "worker": worker, "quant": quant, "answer": answer})
    return out


def item_def(category: str, tier: str, suite: str = SUITE) -> dict:
    for cat, t, prompt, chk in curriculum(suite):
        if cat == category and t == tier:
            return {"prompt": _prompt(prompt), "expected": getattr(chk, "rule", None),
                    "expected_answer": getattr(chk, "answer", None)}
    return {}


def matrix(items: list, suite: str = SUITE) -> dict:
    """grade_detail as the console's grading matrix reads it: per category a
    history of {tier, pass, prompt, expected, actual, why} (latest verdicts)."""
    entries = curriculum(suite)
    out = {"suite": suite, "max": len(entries), "tiers": len(TIER_ORDER), "tasks": list(dict.fromkeys(row[0] for row in entries))}
    for it in items:
        out.setdefault(it["category"], {"history": []})["history"].append({
            "tier": it["tier"], "pass": it["passed"], **item_def(it["category"], it["tier"], suite),
            "actual": it["answer"], "why": it["why"], "request_id": it["request_id"]})
    return out
