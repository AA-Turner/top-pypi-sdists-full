"""fit whole results and row windows under a token budget, and say the budget that would have fit."""

from __future__ import annotations
import json
from collections.abc import Callable
from typing import Any
from ....foundation.token_budget.token_budget import BYTES_PER_TOKEN as _BYTES_PER_TOKEN
from ....foundation.token_budget.token_budget import MAX_TOKENS as _MAX_TOKEN_BUDGET
from ....foundation.token_budget.token_budget import Budget, count_tokens, serialize
from ....shared.reads.search_contract import (
    EnvelopeState,
    MissingMarker)


# -- research_get: token budget, cursor, and the view table --------------------

# ~4 chars per token of JSON. Approximate on purpose: this only has to BOUND a
# payload, and a real tokenizer would drag a model dependency into a read path
# without making the bound any safer.
_CHARS_PER_TOKEN = 4


# `limit` at 200; the token budget trims below this anyway.


def _tokens(value: Any) -> int:
    return max(1, len(json.dumps(value, default=str)) // _CHARS_PER_TOKEN)


def _fit_whole_results(
    results: list[dict],
    build: Callable[[list[dict], dict | None], dict],
    budget: Budget,
    *,
    available: int | None = None,
) -> dict:
    """As many WHOLE result cards as the budget holds, and an honest note.

    A card is a fixed shape: title, preview, ids, url, provenance. It is never
    shrunk to make one more fit and never cut in half, so the only thing that
    bends is how many arrive. That is the trade this function exists to make --
    an agent can act on "there were 12, ask for 3,400 tokens next time", and
    cannot act on half a JSON object.

    Measured against the COMPLETE envelope, not the rows: completeness markers,
    the query echo and the budget note all cost tokens, and a fit computed on
    rows alone is a fit that overflows once the envelope is wrapped around it.
    Measured with the real tokenizer, too -- the chars/4 estimate used elsewhere
    in this file over-counts ids and repeated structure, and a response cut by a
    bad guess looks exactly like one cut by a real limit.
    """
    available = len(results) if available is None else available

    def note(_kept: int) -> dict:
        """What the trial envelope carries, so the measurement includes it."""
        return {"results_available": available}

    if not results:
        return build(results, None)

    # Binary search on the number of whole cards. `fits` is monotonic -- one
    # more card is never smaller -- so this lands on the largest prefix that
    # fits in ~6 exact measurements rather than walking the list. An estimate
    # (chars/4) is not enough on its own: it over-counts ids and repeated
    # structure, and a response cut by a bad guess is indistinguishable to the
    # caller from one cut by a real limit.
    low, high, kept = 1, len(results), 0
    while low <= high:
        mid = (low + high) // 2
        if budget.fits(build(results[:mid], note(mid))):
            kept, low = mid, mid + 1
        else:
            high = mid - 1

    if kept:
        if kept == available:
            return build(results, {"results_available": available})
        # Cut. Name the budget that would carry everything this search found,
        # so the caller has a number to act on rather than a wall to hit again.
        return build(
            results[:kept],
            {
                "results_available": available,
                "fits_all_at_token_budget": _budget_for(build, results),
            },
        )

    # Not even one card fits. Nothing is truncated to pretend otherwise.
    one = build(results[:1], {"results_available": available})
    needed = _budget_cost(one)
    refusal = build(
        [],
        {
            "results_available": available,
            "first_result_tokens": needed,
            **(
                {"min_token_budget": needed}
                if needed <= _MAX_TOKEN_BUDGET
                else {"read_instead": "entity"}
            ),
        },
    )
    # The compact envelope omits a complete `completeness`; a refusal never is one.
    missing = (refusal.get("completeness") or {}).get("missing", [])
    refusal["completeness"] = {
        "state": EnvelopeState.PARTIAL,
        "missing": sorted({*missing, MissingMarker.FIRST_RESULT_EXCEEDS_BUDGET}),
    }
    return refusal


def _budget_cost(payload: dict) -> int:
    """The smallest `token_budget` that admits this payload.

    A budget is TWO limits -- tokens, and `BYTES_PER_TOKEN` times as many bytes
    -- and either can bind. Text that tokenizes efficiently (ids, repeated
    structure, long runs of one character) hits the byte wall first, so a hint
    computed from tokens alone would name a budget that still refuses the
    payload. Answering with a number that does not work is worse than not
    answering.
    """
    text = serialize(payload)
    by_tokens = count_tokens(text)
    by_bytes = -(-len(text.encode("utf-8")) // _BYTES_PER_TOKEN)
    return max(by_tokens, by_bytes)


def _budget_for(
    build: Callable[[list[dict], dict | None], dict],
    results: list[dict],
) -> int:
    """The token budget at which every fetched result would have fitted.

    Rounded UP to the next hundred: a caller passing back the exact measurement
    would sit one token from the edge, and the next search's results are not the
    same size as this one's.
    """
    whole = _budget_cost(build(results, {"results_available": len(results)}))
    return min(_MAX_TOKEN_BUDGET, -(-whole // 100) * 100)


def _largest(high: int, ok: Callable[[int], bool]) -> int:
    """The largest n in 1..high for which `ok(n)`, by binary search; 0 if none.
    Only an n that passed is returned, so the caller keeps nothing unmeasured."""
    low, kept = 1, 0
    while low <= high:
        mid = (low + high) // 2
        if ok(mid):
            kept, low = mid, mid + 1
        else:
            high = mid - 1
    return kept


def _fit(rows: list, budget: int) -> list:
    """Select a source-page row window using a cheap size estimate.

    Always select the first row so no item becomes unreachable. The MCP
    continuation layer fragments oversized source pages and enforces the exact
    whole-response limit after every envelope and cursor is included. Direct
    service callers retain the legacy approximate selection behavior.
    """
    out: list = []
    spent = 0
    for row in rows:
        cost = _tokens(row)
        if out and spent + cost > budget:
            break
        out.append(row)
        spent += cost
    return out


def _fit_sections(sections: list[tuple[str, list]], budget: int) -> tuple[dict[str, list], bool]:
    """Spend one budget across several lists in priority order.

    research_context has no cursor, so unlike _fit there is no always-emit-one
    floor — nothing is paginating and a forced row would just blow the budget.
    Dropping rows silently is the failure to avoid, hence the `truncated` flag."""
    kept: dict[str, list] = {}
    truncated = False
    spent = 0
    for key, rows in sections:
        taken: list = []
        for row in rows:
            cost = _tokens(row)
            if spent + cost > budget:
                break
            taken.append(row)
            spent += cost
        truncated = truncated or len(taken) < len(rows)
        kept[key] = taken
    return kept, truncated
