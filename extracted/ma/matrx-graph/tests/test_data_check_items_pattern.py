"""``data.check_items`` ``pattern`` checks, run through the real scheduler, and the safe-regex judge.

Three users: checkable proof claims (aidream ``brand_discovery/tests/test_checkable_proof_as_a_pattern_check.py``
holds the exact-pattern parity), phone / email shapes on an extracted contact list, and banned URLs in
AI answers. A pattern is judged when the workflow is saved (or, from another input, when the step runs):
invalid, too long, or a shape that can backtrack catastrophically is refused with a sentence.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.checks import MAX_PATTERNS, ItemCheckSpec, check_items
from matrx_graph.safe_regex import MAX_PATTERN_LENGTH, UnsafePatternError, compile_safe, judge

from tests._fixtures import make_app_context


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


def _defn(inputs: dict[str, Any], checks: list[dict[str, Any]]) -> Definition:
    return Definition.model_validate({
        "nodes": [{
            "id": "n", "type": "data.check_items", "position": {"x": 0, "y": 0},
            "data": {"config": {"checks": checks}, "inputs": inputs},
        }],
        "edges": [],
    })


async def _run(inputs: dict[str, Any], checks: list[dict[str, Any]], *, ok: bool = True) -> Any:
    registry = _registry()
    graph = compile_graph(_defn(inputs, checks), registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    result = await scheduler.run(run_id="t-check-items-pattern", inputs=inputs)
    if ok:
        assert result.status is RunStatus.COMPLETED, result.error
        return result.last_outputs["n"]
    assert result.status is not RunStatus.COMPLETED
    return result


PHONE = r"^\+?1?[\s.-]?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$"
EMAIL = r"^[^@\s]+@[^@\s.]+(?:\.[^@\s.]+)+$"


async def test_phone_and_email_shapes_keep_well_formed_contacts_and_say_why_the_rest_failed():
    contacts = [
        {"name": "Front desk", "phone": "(702) 555-0142", "email": "desk@acme.example"},
        {"name": "Typo", "phone": "555-01", "email": "sales@acme.example"},
        {"name": "No at", "phone": "+1 702.555.0199", "email": "sales.acme.example"},
        {"name": "No email", "phone": "702 555 0100"},
    ]
    out = await _run({"items": contacts}, [
        {"type": "pattern", "path": "phone", "patterns": [PHONE]},
        {"type": "pattern", "path": "email", "patterns": [EMAIL], "optional": True},
    ])
    assert [c["name"] for c in out["items"]] == ["Front desk", "No email"]
    reasons = {r["index"]: [(x["check"], x["code"]) for x in r["reasons"]] for r in out["rejected"]}
    assert reasons == {1: [("phone.pattern", "no_pattern_match")], 2: [("email.pattern", "no_pattern_match")]}
    assert "matches none of the patterns" in out["rejected"][0]["reasons"][0]["detail"]


async def test_banned_urls_from_another_input_drop_answers_that_cite_them_in_any_case():
    answers = [
        {"text": "See https://www.Competitor.example/pricing for more."},
        {"text": "Our own guide: https://acme.example/guide"},
        {"text": ["fine", "also see http://spam.example"]},
    ]
    banned = [{"rx": r"https?://(?:www\.)?competitor\.example\b"}, {"rx": r"\bspam\.example\b"}]
    out = await _run({"items": answers, "banned": banned}, [
        {"type": "pattern", "path": "text", "mode": "must_not", "patterns_from": "banned", "from_field": "rx"},
    ])
    assert out["items"] == [answers[1]]
    assert out["counts"]["text.pattern:matches_pattern"] == 2
    assert "competitor" in out["rejected"][0]["reasons"][0]["detail"]


async def test_an_all_of_group_needs_every_pattern_and_any_entry_is_enough():
    items = [{"c": "won an award"}, {"c": "won the game"}, {"c": "ISO 9001 certified"}, {"c": "an award logo"}]
    out = await _run({"items": items}, [
        {"type": "pattern", "path": "c", "patterns": [[r"\bwon\b", r"\baward"], r"\bcertified\b"]},
    ])
    assert [i["c"] for i in out["items"]] == ["won an award", "ISO 9001 certified"]


async def test_ignore_case_is_on_by_default_and_can_be_turned_off():
    items = [{"c": "CERTIFIED"}]
    assert (await _run({"items": items}, [{"type": "pattern", "path": "c", "patterns": ["certified"]}]))["kept"] == 1
    off = await _run({"items": items}, [
        {"type": "pattern", "path": "c", "patterns": ["certified"], "ignore_case": False},
    ])
    assert off["kept"] == 0


async def test_when_path_runs_a_check_only_on_the_items_it_names():
    items = [{"topic": "proof", "c": "says it is great"}, {"topic": "place", "c": "Sioux Falls"},
             {"topic": "proof", "c": "licensed and insured"}]
    out = await _run({"items": items}, [
        {"type": "pattern", "path": "c", "patterns": [r"\blicen[cs]ed\b"], "when_path": "topic", "when_in": ["proof"]},
    ])
    assert [i["c"] for i in out["items"]] == ["Sioux Falls", "licensed and insured"]


async def test_whitespace_runs_read_as_one_space():
    out = await _run({"items": [{"c": "member\n   of the Chamber"}]}, [
        {"type": "pattern", "path": "c", "patterns": ["member of"]},
    ])
    assert out["kept"] == 1


@pytest.mark.parametrize("bad, why", [
    ("(a+)+b", "rounds can end in more than one place"),
    (r"(\w+\s?)*$", "rounds can end in more than one place"),
    ("(a|ab)*c", "alternatives inside a repeat"),
    ("(a*)*", "can match nothing"),
    (r".*\d+", "side by side"),
    (r"(x)\1", "back-references"),
    ("([", "not a valid regular expression"),
    ("a" * (MAX_PATTERN_LENGTH + 1), "at most"),
])
def test_an_unsafe_or_invalid_pattern_is_refused_when_saved(bad: str, why: str):
    with pytest.raises(ValidationError, match=why.replace("(", r"\(")):
        ItemCheckSpec.model_validate({"type": "pattern", "patterns": [bad]})
    with pytest.raises(Exception, match="could take too long|not allowed|not a valid|at most"):
        compile_graph(_defn({"items": []}, [{"type": "pattern", "patterns": [bad]}]), registry=_registry())


def test_the_refused_shapes_really_hang_python_re_and_the_safe_ones_do_not():
    """The judge is not theatre: (a+)+b on 24 a's costs Python far more CPU than what it allows on 40,000.
    CPU time (``process_time``), not the wall clock, so a busy machine does not fail it."""
    import re

    start = time.process_time()
    re.search(r"(a+)+b", "a" * 24)
    slow = time.process_time() - start
    for ok in [r"^\s*(?:\S+\s+){0,6}?(shows|lists)\b", EMAIL, PHONE, r"https?://(?:www\.)?x\.example\b"]:
        rx = compile_safe(ok, ignore_case=True)
        start = time.process_time()
        rx.search("a " * 20_000 + "!" * 20_000)
        assert time.process_time() - start < max(1.0, slow), ok


def test_patterns_from_an_input_are_judged_when_the_step_runs():
    with pytest.raises(Exception, match="could take too long"):
        check_items([{"c": "x"}], [ItemCheckSpec(type="pattern", path="c", patterns_from="p")], {"p": ["(a+)+"]})


def test_settings_that_do_not_fit_are_refused():
    for bad in (
        {"type": "pattern", "path": "c"},  # no patterns
        {"type": "pattern", "patterns": []},
        {"type": "pattern", "patterns": ["x"], "fold": "flat"},
        {"type": "pattern", "patterns": ["x"] * (MAX_PATTERNS + 1)},
        {"type": "pattern", "patterns": ["x"], "when_path": "topic"},
        {"type": "required", "mode": "must_not"},
        {"type": "required", "patterns": ["x"]},
    ):
        with pytest.raises(ValidationError):
            ItemCheckSpec.model_validate(bad)
    with pytest.raises(UnsafePatternError):
        compile_safe("")


# --------------------------------------------------------------------------- #
# Adversarial review 2026-10-27: every shape that hung a worker is refused,    #
# and every shape the judge accepts finishes on hostile text (run in a         #
# subprocess with a timeout, so a regression fails instead of hanging CI).     #
# --------------------------------------------------------------------------- #

#: Exponential: refused at every level (text.regex_*, data.batch, pattern checks).
HUNG_EXPONENTIAL = [
    r"(a{1,20}){1,20}$", r"(?:a{1,3})+$", r"(\d{1,3}[-. ]?)+$", r"(?:\w{1,20}\s?)+$",
    r"(?:[a-z]{1,15}\.?){1,20}$", r"(?:aa?)+b", r"(\d\d?)*x", r"(a+)+b",
    r"(?:[б-я]+б)+$", r"(?:\w+é)+$", r"(?:\w+ж)+$",
    # only the "any other letter" stand-in sees this one: no listed character is in both sets
    r"(?:[^\x00-\u024f]+\w)+$",
    # a growing piece swallows the character that ends the round
    r"(?:\w+x)+$",
]
#: Polynomial, side by side: refused for pattern checks (strict). Other polynomial shapes are allowed and
#: bounded by max_text_chars (re-review 2026-10-27: refusing them refused 11 of 39 realistic safe patterns).
HUNG_POLYNOMIAL = [r"\w+\w*x", r".*\d+", r"[a-z]+\w+!"]

_LIVE = json.loads((Path(__file__).parent / "fixtures" / "live_saved_regex_patterns.json").read_text())

_RUNNER = """
import json, re, sys, time
job = json.loads(sys.stdin.read())
rx = re.compile(job["pattern"], job["flags"])
worst = 0.0
for t in job["texts"]:
    start = time.process_time()
    rx.search(t)
    worst = max(worst, time.process_time() - start)
print("done", worst)
"""


def _hostile_texts(pattern: str, n: int) -> list[str]:
    named = sorted({c for c in pattern if c.isprintable() and not c.isspace()} | set("a1 .-éб_"))
    out = []
    for c in named:
        out += [c * n, c * n + "\u0001"]
    out += [("a " * n)[:n] + "!", ("a." * n)[:n] + "!", ("1-" * n)[:n] + "!", ("ab" * n)[:n] + "!"]
    return out


def _worst_cpu(pattern: str, flags: int, n: int, timeout: float = 30.0) -> float | None:
    """The slowest single search over the hostile texts, in CPU seconds; None when it did not finish."""
    job = json.dumps({"pattern": pattern, "flags": flags, "texts": _hostile_texts(pattern, n)})
    try:
        done = subprocess.run([sys.executable, "-c", _RUNNER], input=job, capture_output=True, text=True,
                              timeout=timeout)
    except subprocess.TimeoutExpired:
        return None
    word, _, worst = done.stdout.strip().partition(" ")
    return float(worst) if word == "done" else None


def _finishes(pattern: str, flags: int, n: int, timeout: float = 30.0) -> bool:
    return _worst_cpu(pattern, flags, n, timeout) is not None


@pytest.mark.parametrize("bad", HUNG_EXPONENTIAL)
def test_every_exponential_shape_is_refused_at_every_level(bad: str):
    for level in ("strict", "exponential"):
        with pytest.raises(UnsafePatternError, match="could take too long"):
            compile_safe(bad, level=level)


@pytest.mark.parametrize("bad", HUNG_POLYNOMIAL)
def test_side_by_side_growing_pieces_are_refused_for_pattern_checks(bad: str):
    with pytest.raises(UnsafePatternError, match="side by side"):
        compile_safe(bad)
    compile_safe(bad, level="exponential")  # the regex steps allow them (their input cap bounds them)


#: Re-review 2026-10-27: realistic safe patterns the strict level must accept, each under 1 CPU second
#: on hostile 10,000-character text.
MUST_ACCEPT = [
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}",
    r"https?://(?:www\.)?[\w-]+(?:\.[\w-]+)+(?:/\S*)?",
    r"(?:https?://)?(?:[\w-]+\.)+[a-z]{2,}(?:/\S*)?",
    r"\b(?:www\.)?[a-z0-9-]+\.(?:com|net|org)\b",
    r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    r"^.*award.*$",
    r"licen[cs]e\s*(?:no\.?|number|#)\s*\w+",
    r"\b\w+(?:\s+\w+){0,3}\s+award\b",
    r"(?:[^,]*,)*",
    r"(?:a\s*)+",
]


@pytest.mark.parametrize("ok", MUST_ACCEPT)
def test_realistic_safe_patterns_are_accepted_and_fast_at_the_cap(ok: str):
    import re

    compile_safe(ok, ignore_case=True)
    worst = _worst_cpu(ok, re.IGNORECASE, 10_000)
    assert worst is not None and worst < 1.0, (ok, worst)


def test_the_hung_shapes_really_hang_so_the_runner_can_tell():
    """The subprocess runner is not theatre: a refused shape does not finish in time."""
    assert not _finishes(r"(?:a{1,3})+$", 0, 10_000, timeout=3)
    assert not _finishes(r".*a.*b", 0, 10_000, timeout=3)


ACCEPTED_STRICT = [PHONE, EMAIL, r"https?://(?:www\.)?example\.com\b", r"\d{1,3}(?:,\d{3})*",
                   r"^\s*(?:\S+\s+){0,6}?(shows|lists)\b", r"(\w|\d)+", r"(?:é|\w)+$",
                   r"[A-Z][a-z]+\s+[A-Z][a-z]+", r"\bwon\b.*"]


@pytest.mark.parametrize("ok", ACCEPTED_STRICT)
def test_what_a_pattern_check_accepts_finishes_on_hostile_text_at_the_cap(ok: str):
    import re

    compile_safe(ok, ignore_case=True)
    worst = _worst_cpu(ok, re.IGNORECASE, 10_000)
    assert worst is not None and worst < 2.0, (ok, worst)


def test_saved_workflow_patterns_still_pass_the_regex_steps_and_strict_refuses_every_slow_one():
    """Census of every text.regex_* / data.batch pattern in live workflow.definition rows (2026-10-27):
    none is refused at the exponential level (saved workflows keep running), and every one that does
    not finish on hostile text is one the strict level refuses (one does: a lazy class between two
    ``\\s*`` — polynomial, bounded only by the regex steps' input cap)."""
    assert len(_LIVE) >= 30
    slow = []
    for p in _LIVE:
        judge(p, 0, level="exponential")
        if not _finishes(p, 0, 10_000, timeout=8):
            slow.append(p)
            with pytest.raises(UnsafePatternError):
                judge(p, 0, level="strict")
    assert len(slow) <= 1, slow


async def test_a_text_longer_than_max_text_chars_fails_the_item_with_a_reason():
    out = await _run({"items": [{"c": "a" * 200}, {"c": "abc"}]}, [
        {"type": "pattern", "path": "c", "patterns": ["a"], "max_text_chars": 100},
    ])
    assert out["kept"] == 1
    assert out["rejected"][0]["reasons"][0]["code"] == "text_too_long"
    assert "max_text_chars" in out["rejected"][0]["reasons"][0]["detail"]


async def test_the_regex_steps_refuse_an_exponential_pattern_with_a_sentence():
    res = await _run_node("text.regex_extract", {"text": "aaaa"}, {"pattern": "(?:a{1,3})+$"})
    assert res.status is not RunStatus.COMPLETED
    assert "could take too long" in str(res.error)


def test_data_batch_refuses_an_exponential_cut_pattern_when_saved():
    from matrx_graph.nodes.data.collections import BatchConfig

    with pytest.raises(ValidationError, match="could take too long"):
        BatchConfig.model_validate({"size": 10, "prefer_cut_pattern": "(\\d\\d?)*x"})


async def _run_node(node_type: str, inputs: dict[str, Any], config: dict[str, Any]) -> Any:
    registry = _registry()
    defn = Definition.model_validate({
        "nodes": [{"id": "n", "type": node_type, "position": {"x": 0, "y": 0},
                   "data": {"config": config, "inputs": inputs}}],
        "edges": [],
    })
    graph = compile_graph(defn, registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    return await scheduler.run(run_id="t-regex-node", inputs=inputs)


# --------------------------------------------------------------------------- #
# checks_from: a shared step's caller passes its own checks (2026-10-27)       #
# --------------------------------------------------------------------------- #


def _save_time_message(check: dict[str, Any]) -> str:
    with pytest.raises(ValidationError) as caught:
        ItemCheckSpec.model_validate(check)
    return str(caught.value.errors()[0]["msg"]).removeprefix("Value error, ")


async def test_checks_from_an_input_run_beside_the_written_checks():
    items = [{"phone": "(702) 555-0142", "name": "a"}, {"phone": "555-01", "name": "b"}, {"phone": "", "name": "c"}]
    out = await _run_cfg(
        {"items": items, "caller": {"checks": [{"type": "pattern", "path": "phone", "patterns": [PHONE]}]}},
        {"checks": [{"type": "required", "path": "name"}], "checks_from": "caller.checks"},
    )
    assert out["items"] == [items[0]]  # b fails the pattern, c's empty phone is missing


async def _run_cfg(inputs: dict[str, Any], config: dict[str, Any], *, ok: bool = True) -> Any:
    res = await _run_node("data.check_items", inputs, config)
    if ok:
        assert res.status is RunStatus.COMPLETED, res.error
        return res.last_outputs["n"]
    assert res.status is not RunStatus.COMPLETED
    return str(res.error)


async def test_checks_from_alone_is_enough_and_its_checks_are_counted():
    out = await _run_cfg(
        {"items": [{"c": "x"}, {"c": ""}], "checks": [{"type": "required", "path": "c", "key": "has_c"}]},
        {"checks_from": "checks"},
    )
    assert out["kept"] == 1 and out["counts"]["has_c:missing"] == 1


@pytest.mark.parametrize("bad", [
    {"type": "pattern", "path": "c"},
    {"type": "no_such_type", "path": "c"},
    {"type": "max_length", "path": "c"},
    {"type": "required", "path": "c", "patterns": ["x"]},
    {"type": "pattern", "path": "c", "patterns": ["(a+)+b"]},
])
async def test_an_invalid_check_from_an_input_is_refused_with_the_save_time_sentence(bad: dict[str, Any]):
    error = await _run_cfg({"items": [{"c": "x"}], "checks": [bad]}, {"checks_from": "checks"}, ok=False)
    assert _save_time_message(bad) in error
    assert "checks_from 'checks' #0" in error


async def test_an_unsafe_pattern_from_an_input_never_runs():
    error = await _run_cfg(
        {"items": [{"c": "a" * 50}], "checks": [{"type": "pattern", "path": "c", "patterns": ["(?:a{1,3})+$"]}]},
        {"checks_from": "checks"}, ok=False,
    )
    assert "could take too long" in error


async def test_checks_from_that_is_not_a_list_is_refused():
    assert "non-empty list of checks" in await _run_cfg(
        {"items": [], "checks": {"type": "required"}}, {"checks_from": "checks"}, ok=False
    )


@pytest.mark.parametrize("extra", [[], None, "absent"])
async def test_no_extra_checks_from_the_caller_means_nothing_extra_is_checked(extra: Any):
    # mandate.ask_and_check v13 (2026-10-27): every caller that sent no extra_checks failed with
    # "checks_from 'extra' must be a non-empty list of checks; it is list (empty)".
    items = [{"name": "a"}, {"name": ""}]
    inputs: dict[str, Any] = {"items": items}
    if extra != "absent":
        inputs["extra"] = extra
    out = await _run_cfg(inputs, {"checks": [{"type": "required", "path": "name"}], "checks_from": "extra"})
    assert out["items"] == [items[0]] and out["dropped"] == 1


def test_a_step_with_neither_checks_nor_checks_from_is_refused_when_saved():
    from matrx_graph.nodes.data.check_items import CheckItemsConfig

    with pytest.raises(ValidationError, match="`checks` or `checks_from`"):
        CheckItemsConfig.model_validate({})


async def test_the_regex_steps_read_at_most_the_knob_and_say_so(monkeypatch: pytest.MonkeyPatch):
    from matrx_graph import knobs

    async def small() -> int:
        return 1_000

    monkeypatch.setattr(knobs, "regex_max_input_chars", small)
    res = await _run_node("text.regex_extract", {"text": "a" * 1_001}, {"pattern": "a"})
    assert res.status is not RunStatus.COMPLETED
    assert "workflow.regex.max_input_chars" in str(res.error)
    ok = await _run_node("text.regex_replace", {"text": "a" * 1_000}, {"pattern": "a", "replacement": "b"})
    assert ok.status is RunStatus.COMPLETED, ok.error
    assert knobs.STARTING_REGEX_MAX_INPUT_CHARS == 50_000


@pytest.mark.parametrize("bad", [r".*a.*b", r"[\s\S]*a[\s\S]*b", r"[^x]*a.+b", r"\bfoo.*bar.*$"])
def test_two_unanchored_match_anything_runs_are_refused_for_pattern_checks(bad: str):
    """.*a.*b is cubic on hostile text even at max_text_chars (over 2 minutes on 10,000 characters)."""
    with pytest.raises(UnsafePatternError, match="match anything"):
        compile_safe(bad)
    compile_safe(bad, level="exponential")  # the regex steps keep them (saved workflows use .*)


@pytest.mark.parametrize("ok", [r"^.*award.*$", r"\A.*a.*b", r".*foo", r"\bwon\b.*", r"\S*a\S*b"])
def test_one_match_anything_run_or_an_anchored_pattern_is_accepted(ok: str):
    compile_safe(ok)
