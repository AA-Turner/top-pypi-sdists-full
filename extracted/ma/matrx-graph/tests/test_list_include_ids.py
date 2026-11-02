"""List surfaces union the host's discoverable-id set (G14).

``DefinitionStore.list_for_user`` / ``RunStore.list_recent`` accept
``include_ids`` — the host resolves share grants through its access
kernel (aidream: ``iam.discoverable_ids``) and passes the ids in; the
package stays access-system-agnostic. Pins:

- a granted (include_ids) workflow appears even though created_by differs,
  in every organization the person belongs to (access decides a list, never
  the selected organization — Arman, 2026-09-25);
- with no include_ids the owner fast path is a plain kwargs filter (no Q);
- an explicit organization is a FILTER on that access set (the on-page
  control), binding every arm like the other common filters (archive /
  soft-delete / children / status), ordering, and limit/offset;
- invalid ids are dropped, never 500 the list.

Fake-backed: the real filter semantics are proven live against
``iam.discoverable_ids`` (wf_027) — these tests pin the query the stores
BUILD, which is what a regression would silently change.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_orm import Q

import matrx_graph.db.definition_store as ds
import matrx_graph.db.run_store as rs

OWNER = "11111111-1111-4111-8111-111111111111"
GRANTED_ID = "33333333-3333-4333-8333-333333333333"
ORG = "44444444-4444-4444-8444-444444444444"


class _FakeQuery:
    def __init__(self, log: dict[str, Any]):
        self.log = log

    def filter(self, *args: Any, **kwargs: Any) -> _FakeQuery:
        self.log["filter_args"] = args
        self.log["filter_kwargs"] = kwargs
        return self

    def order_by(self, *fields: str) -> _FakeQuery:
        self.log["order_by"] = fields[0] if len(fields) == 1 else fields
        return self

    def limit(self, n: int) -> _FakeQuery:
        self.log["limit"] = n
        return self

    def offset(self, n: int) -> _FakeQuery:
        self.log["offset"] = n
        return self

    async def values(self) -> list[dict[str, Any]]:
        return []

    async def count(self) -> int:
        self.log["counted"] = True
        return 7


@pytest.fixture()
def captured(monkeypatch) -> dict[str, Any]:
    log: dict[str, Any] = {}
    monkeypatch.setattr(ds, "get_model", lambda name: _FakeQuery(log))
    monkeypatch.setattr(rs, "get_model", lambda name: _FakeQuery(log))
    return log


def _or_arms(q: Q) -> list[dict[str, Any]]:
    """Flatten nested OR combinations ((a|b)|c) into their leaf kwarg dicts."""
    assert q.connector == Q.OR
    out: list[dict[str, Any]] = []
    for child in q.children:
        if getattr(child, "connector", None) == Q.OR and not child.kwargs:
            out.extend(_or_arms(child))
        else:
            out.append(child.kwargs)
    return out


async def test_definitions_owner_fast_path_unchanged(captured) -> None:
    # Owner-only stays the plain single query.
    await ds.DefinitionStore().list_for_user(user_id=OWNER)
    assert captured["filter_args"] == ()  # no Q object — single plain query
    assert captured["filter_kwargs"] == {
        "created_by": OWNER,
        "is_archived": False,
        "deleted_at__isnull": True,
        "workflow_type__in": ("user", "builtin"),
    }
    assert captured["order_by"] == "-updated_at"


async def test_definition_count_uses_the_identical_owner_scope(captured) -> None:
    assert await ds.DefinitionStore().count_for_user(user_id=OWNER) == 7
    assert captured["filter_args"] == ()
    assert captured["filter_kwargs"] == {
        "created_by": OWNER,
        "is_archived": False,
        "deleted_at__isnull": True,
        "workflow_type__in": ("user", "builtin"),
    }
    assert captured["counted"] is True


async def test_definitions_org_is_a_filter_on_the_owner_set(captured) -> None:
    """An explicit organization NARROWS what the person can access; it is an
    on-page filter, never the header's selection and never a widening."""
    await ds.DefinitionStore().list_for_user(user_id=OWNER, organization_id=ORG)
    assert captured["filter_args"] == ()
    assert captured["filter_kwargs"] == {
        "created_by": OWNER,
        "organization_id": ORG,
        "is_archived": False,
        "deleted_at__isnull": True,
        "workflow_type__in": ("user", "builtin"),
    }


async def test_definitions_include_ids_unions_granted_row(captured) -> None:
    await ds.DefinitionStore().list_for_user(
        user_id=OWNER,
        organization_id=ORG,
        include_ids=[GRANTED_ID],
        limit=25,
        offset=5,
    )
    (q,) = captured["filter_args"]
    owner_arm, shared_arm = _or_arms(q)
    assert owner_arm == {"created_by": OWNER}
    assert shared_arm == {"id__in": [GRANTED_ID]}
    # The filter, common filters + paging bind both arms.
    assert captured["filter_kwargs"] == {
        "organization_id": ORG,
        "is_archived": False,
        "deleted_at__isnull": True,
        "workflow_type__in": ("user", "builtin"),
    }
    assert (captured["limit"], captured["offset"]) == (25, 5)


async def test_definitions_include_ids_span_every_organization(captured) -> None:
    """Arman, 2026-09-25: a person with six organizations sees her workflows
    from all six. No organization = no narrowing; the discoverable ids (which
    already span every organization she belongs to) are unioned in."""
    await ds.DefinitionStore().list_for_user(user_id=OWNER, include_ids=["not-a-uuid", GRANTED_ID])
    (q,) = captured["filter_args"]
    owner_arm, shared_arm = _or_arms(q)
    assert owner_arm == {"created_by": OWNER}
    assert shared_arm == {"id__in": [GRANTED_ID]}
    assert "organization_id" not in captured["filter_kwargs"]


async def test_definition_count_uses_the_identical_access_scope(captured) -> None:
    assert await ds.DefinitionStore().count_for_user(user_id=OWNER, include_ids=[GRANTED_ID]) == 7
    (q,) = captured["filter_args"]
    assert _or_arms(q) == [{"created_by": OWNER}, {"id__in": [GRANTED_ID]}]
    assert captured["filter_kwargs"] == {
        "is_archived": False,
        "deleted_at__isnull": True,
        "workflow_type__in": ("user", "builtin"),
    }
    assert captured["counted"] is True


async def test_definitions_all_invalid_include_ids_keeps_owner_path(captured) -> None:
    await ds.DefinitionStore().list_for_user(user_id=OWNER, include_ids=["nope"])
    assert captured["filter_args"] == ()
    assert captured["filter_kwargs"]["created_by"] == OWNER


async def test_runs_owner_fast_path_unchanged(captured) -> None:
    await rs.RunStore().list_recent(user_id=OWNER)
    assert captured["filter_args"] == ()
    assert captured["filter_kwargs"] == {
        "parent_run_id__isnull": True,
        "created_by": OWNER,
        "deleted_at__isnull": True,
    }
    assert captured["order_by"] == "-created_at"


async def test_runs_include_ids_unions_and_keeps_common_filters(captured) -> None:
    await rs.RunStore().list_recent(user_id=OWNER, status="completed", include_ids=[GRANTED_ID])
    (q,) = captured["filter_args"]
    owner_arm, shared_arm = _or_arms(q)
    assert owner_arm == {"created_by": OWNER}
    assert shared_arm == {"id__in": [GRANTED_ID]}
    # Children-hiding + status + soft-delete stay ANDed over both arms.
    assert captured["filter_kwargs"] == {
        "parent_run_id__isnull": True,
        "status": "completed",
        "deleted_at__isnull": True,
    }


async def test_runs_page_filter_binds_the_granted_arm_too(captured) -> None:
    """The on-page organization filter narrows the WHOLE access set — a granted
    run from another organization must not escape it."""
    await rs.RunStore().list_recent(
        user_id=OWNER, include_ids=[GRANTED_ID], filter_organization_id=ORG
    )
    (q,) = captured["filter_args"]
    assert captured["filter_kwargs"]["organization_id"] == ORG


async def test_runs_parent_filter_lists_only_that_runs_children(captured) -> None:
    """GET /runs?parent_run_id= once ignored the filter and returned the caller's
    latest runs; an agent then resumed another session's gate. The filter binds
    every arm and replaces the children-hiding default."""
    await rs.RunStore().list_recent(user_id=OWNER, include_ids=[GRANTED_ID], parent_run_id=ORG)
    assert captured["filter_kwargs"]["parent_run_id"] == ORG
    assert "parent_run_id__isnull" not in captured["filter_kwargs"]


async def test_runs_invalid_parent_matches_nothing(captured) -> None:
    assert await rs.RunStore().list_recent(user_id=OWNER, parent_run_id="not-a-uuid") == []
    assert "filter_kwargs" not in captured


async def test_definition_lists_hide_generated_rows_by_default(captured) -> None:
    # workflow_type='generated' = a platform feature made it for a parent record
    # (Understudy, Masterwork, seeded copy); the list lanes never show it.
    await ds.DefinitionStore().list_for_user(user_id=OWNER)
    assert captured["filter_kwargs"]["workflow_type__in"] == ("user", "builtin")
    assert "generated" not in captured["filter_kwargs"]["workflow_type__in"]
    await ds.DefinitionStore().count_for_user(user_id=OWNER)
    assert captured["filter_kwargs"]["workflow_type__in"] == ("user", "builtin")


async def test_include_generated_drops_the_type_predicate(captured) -> None:
    await ds.DefinitionStore().list_for_user(user_id=OWNER, include_generated=True)
    assert "workflow_type__in" not in captured["filter_kwargs"]
    await ds.DefinitionStore().count_for_user(user_id=OWNER, include_generated=True)
    assert "workflow_type__in" not in captured["filter_kwargs"]


async def test_runs_flagged_filter_and_sort_run_in_the_query(captured) -> None:
    """The Flagged filter/sort are part of the QUERY (so an old flagged run is found past the
    page window), not a client-side pass over the newest page."""
    await rs.RunStore().list_recent(user_id=OWNER, flagged=True, sort_flagged_first=True)
    assert captured["filter_kwargs"]["review_flag_count__gt"] == 0
    assert captured["filter_kwargs"]["created_by"] == OWNER
    assert captured["order_by"] == ("-review_flag_count", "-created_at")

    await rs.RunStore().list_recent(user_id=OWNER, flagged=False)
    assert captured["filter_kwargs"]["review_flag_count"] == 0
    assert "review_flag_count__gt" not in captured["filter_kwargs"]
    assert captured["order_by"] == "-created_at"

    await rs.RunStore().list_recent(user_id=OWNER)
    assert not any(k.startswith("review_flag_count") for k in captured["filter_kwargs"])


async def test_runs_flagged_binds_the_discoverable_arm_too(captured) -> None:
    await rs.RunStore().list_recent(user_id=OWNER, include_ids=[GRANTED_ID], flagged=True)
    assert captured["filter_kwargs"]["review_flag_count__gt"] == 0  # common: binds every arm


async def test_workflow_runs_flagged_filter_and_sort(captured) -> None:
    await rs.RunStore().list_for_definition(GRANTED_ID, flagged=True, sort_flagged_first=True)
    assert captured["filter_kwargs"]["review_flag_count__gt"] == 0
    assert captured["order_by"] == ("-review_flag_count", "-created_at")


def test_run_row_carries_the_review_flag_count() -> None:
    """The runs lists read the count off the row — dropping it from the row dict shows every run as
    unflagged-unknown."""
    base = {
        k: None
        for k in (
            "parent_run_id", "definition_version_id", "definition_hash", "input", "error",
            "interrupt_payload", "last_checkpoint_id", "created_by", "organization_id",
            "project_id", "task_id", "conversation_id", "agent_id", "agent_version_id",
            "metadata", "created_at", "started_at", "completed_at",
        )
    }
    base.update(id="55555555-5555-4555-8555-555555555555", thread_id="t", definition_id="d",
                status="completed", steps_executed=3)
    assert rs._row_to_run_dict({**base, "review_flag_count": 2})["review_flag_count"] == 2
    assert rs._row_to_run_dict(base)["review_flag_count"] == 0
