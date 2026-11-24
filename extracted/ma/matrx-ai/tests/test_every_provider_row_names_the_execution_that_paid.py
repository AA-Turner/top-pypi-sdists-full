"""Every chat.request row names the spine execution that paid for it (Q4b, run_cost_agrees.sql).

Before: only workflow / scheduled contexts stamped execution_kind/id; a mandate or helper run inside
a tracked tree wrote a provider row naming NO run. The writer now carries the spine execution.
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.db.request_tracking_log import (
    SPINE_EXECUTION_KIND,
    resolve_request_execution_attribution,
)
from matrx_utils.source_guard import stable_source

_OWN = "11111111-1111-4111-8111-111111111111"
_NEST = "22222222-2222-4222-8222-222222222222"
_ROOT = "33333333-3333-4333-8333-333333333333"


def _ctx(meta: dict, kind=None, eid=None):
    return SimpleNamespace(metadata=meta, execution_kind=kind, execution_id=eid)


def test_a_mandate_run_inside_a_tracked_tree_names_its_spine_execution() -> None:
    meta = {"runtime_root_execution_id": _ROOT, "runtime_execution_id": _NEST}
    assert resolve_request_execution_attribution(_ctx(meta)) == (SPINE_EXECUTION_KIND, _NEST)


def test_the_runs_own_execution_outranks_the_nesting_parent() -> None:
    meta = {
        "runtime_settle_metered_execution": _OWN,
        "runtime_execution_id": _NEST,
        "runtime_root_execution_id": _ROOT,
    }
    assert resolve_request_execution_attribution(_ctx(meta)) == (SPINE_EXECUTION_KIND, _OWN)


def test_an_explicit_workflow_attribution_is_never_overridden() -> None:
    meta = {"runtime_execution_id": _NEST}
    assert resolve_request_execution_attribution(_ctx(meta, "workflow_run", _OWN)) == ("workflow_run", _OWN)


def test_no_carried_execution_leaves_the_pair_empty_together() -> None:
    assert resolve_request_execution_attribution(_ctx({})) == (None, None)
    assert resolve_request_execution_attribution(None) == (None, None)


def test_a_non_uuid_stamp_is_skipped_not_written() -> None:
    meta = {"runtime_execution_id": "not-a-uuid", "runtime_root_execution_id": _ROOT}
    assert resolve_request_execution_attribution(_ctx(meta)) == (SPINE_EXECUTION_KIND, _ROOT)


def test_the_request_writer_uses_the_carried_attribution() -> None:

    from matrx_ai.db import persistence

    src = stable_source(persistence.persist_completed_request)
    assert "resolve_request_execution_attribution(_ctx)" in src
