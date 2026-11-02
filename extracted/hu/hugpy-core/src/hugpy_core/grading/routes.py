"""grading route registration (abstract_flask ``register_categories`` convention).

The benchmark / review handlers live in ``review.py`` and the evictions feed in
``evictions.py`` as plain functions (kwargs in, JSON-able out, ``(payload,
status)`` where a non-200 matters). This module only states the URL tree.

Dict nesting is the path, a ``<param>`` key is a path parameter that reaches
the handler as the same-named kwarg, and a ``spec(...)`` leaf declares the
exact methods and that the answer is served BARE (``response="native"``: the
console reads ``{runs: [...]}``, not ``{result: {...}}``) — on the same tree
path, so this section's dict merges with every other section's into one app
surface (see ``hugpy_core.routes``).
"""
from __future__ import annotations

from abstract_flask import get_bp, register_categories, spec

from hugpy_core.grading import evictions, review

grading_bp, logger = get_bp("grading_bp", __name__)


def _get(view):
    return spec(view, "GET", response="native")


def _post(view):
    return spec(view, "POST", response="native")


ALL_CATEGORIES = {
    "llm": {
        "benchmark": {
            "runs": {
                "": _get(review.benchmark_runs),               # /llm/benchmark/runs
                "<run_id>": _get(review.benchmark_run_get),    # /llm/benchmark/runs/<run_id>
            },
            "status": _get(review.benchmark_status),           # /llm/benchmark/status
            "events": _get(review.benchmark_events),           # /llm/benchmark/events?tail=
            "run": _post(review.benchmark_run),                # /llm/benchmark/run {models,workers,tokens,...}
            "judge": _post(review.benchmark_judge),            # /llm/benchmark/judge
            "cancel": _post(review.benchmark_cancel),          # /llm/benchmark/cancel {scope,...}
        },
        "compute-actions": _get(review.compute_actions_log),   # /llm/compute-actions?limit=&model=&worker=
        "review": {
            "status": _get(review.review_status),              # /llm/review/status
            "criteria": {
                "": _get(review.review_criteria_list),         # /llm/review/criteria
                "<name>": [                                    # /llm/review/criteria/<name>
                    _get(review.review_criteria_get),
                    spec(review.review_criteria_put, "PUT", response="native"),
                ],
            },
            "screen": _post(review.review_screen),
            "run": _post(review.review_run),
            "runs": _get(review.review_runs),
            "results": _get(review.review_results),
            "dossiers": _get(review.review_dossiers),          # ?criteria=
            "dossier": _get(review.review_dossier),            # ?criteria=&hub_id=
            "radar": _get(review.review_radar),                # ?criteria=
            "ingest": _post(review.review_ingest),
        },
        "evictions": {
            "": _get(evictions.evictions_list),                # /llm/evictions?limit=
            "stream": _get(evictions.evictions_stream),        # /llm/evictions/stream (SSE)
        },
    },
}
register_categories(grading_bp, ALL_CATEGORIES)
