"""Unit tests for the memory promotion & review pipeline (#920)."""

from __future__ import annotations

import sqlite3
from typing import Any

import pytest

from anteroom.config import MemoryPromotionConfig
from anteroom.db import _SCHEMA, ThreadSafeConnection
from anteroom.services.memory_promotion import (
    PromotionAgentDisabledError,
    PromotionRateLimitError,
    PromotionStateError,
    _append_lineage,
    approve_candidate,
    list_candidates,
    propose_candidate,
    reject_candidate,
)
from anteroom.services.memory_service import get_memory

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db() -> ThreadSafeConnection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(_SCHEMA)
    conn.commit()
    return ThreadSafeConnection(conn)


@pytest.fixture()
def cfg() -> MemoryPromotionConfig:
    return MemoryPromotionConfig()


@pytest.fixture()
def auto_approve_cfg() -> MemoryPromotionConfig:
    return MemoryPromotionConfig(local_auto_approve=True)


@pytest.fixture()
def agent_disabled_cfg() -> MemoryPromotionConfig:
    return MemoryPromotionConfig(agent_proposals_enabled=False)


@pytest.fixture()
def pending_review_cfg() -> MemoryPromotionConfig:
    return MemoryPromotionConfig(default_review_state="pending_review")


@pytest.fixture()
def tight_rate_limit_cfg() -> MemoryPromotionConfig:
    return MemoryPromotionConfig(max_candidates_per_conversation=2)


@pytest.fixture()
def tiny_lineage_cfg() -> MemoryPromotionConfig:
    return MemoryPromotionConfig(max_lineage_entries=3)


CONV_A = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
CONV_B = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"


# ---------------------------------------------------------------------------
# _append_lineage
# ---------------------------------------------------------------------------


class TestAppendLineage:
    def test_append_to_empty_lineage(self) -> None:
        out = _append_lineage({}, "proposed", actor="user", max_entries=10)
        assert len(out) == 1
        assert out[0]["event"] == "proposed"
        assert out[0]["actor"] == "user"
        assert "at" in out[0]

    def test_append_preserves_existing(self) -> None:
        meta = {"lineage": [{"event": "proposed", "actor": "u", "at": "2026-01-01T00:00:00Z"}]}
        out = _append_lineage(meta, "approved", actor="r", max_entries=10)
        assert len(out) == 2
        assert out[0]["event"] == "proposed"
        assert out[1]["event"] == "approved"

    def test_truncation_adds_marker(self) -> None:
        meta = {
            "lineage": [{"event": "proposed", "actor": "u", "at": f"2026-01-{i:02d}T00:00:00Z"} for i in range(1, 6)]
        }
        out = _append_lineage(meta, "approved", actor="r", max_entries=3)
        assert len(out) == 3
        assert out[0]["event"] == "truncated"
        assert out[-1]["event"] == "approved"

    def test_unknown_event_rejected(self) -> None:
        with pytest.raises(ValueError, match="Unknown lineage event"):
            _append_lineage({}, "deleted", actor="u", max_entries=10)

    def test_optional_fields_passed_through(self) -> None:
        out = _append_lineage(
            {},
            "rejected",
            actor="reviewer-ui",
            actor_id="reviewer-1",
            notes="stale",
            from_status="candidate",
            to_status="rejected",
            max_entries=10,
        )
        assert out[-1]["notes"] == "stale"
        assert out[-1]["from_status"] == "candidate"
        assert out[-1]["to_status"] == "rejected"


# ---------------------------------------------------------------------------
# propose_candidate
# ---------------------------------------------------------------------------


class TestProposeCandidate:
    def test_proposal_lands_in_candidate_by_default(self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig) -> None:
        mem = propose_candidate(
            db,
            content="prefer dark mode",
            scope="user",
            category="preference",
            proposer="user",
            proposer_id="u-1",
            provenance={"conversation_id": CONV_A},
            config=cfg,
        )
        assert mem["metadata"]["memory_status"] == "candidate"
        lineage = mem["metadata"]["lineage"]
        assert len(lineage) == 1
        assert lineage[0]["event"] == "proposed"
        assert lineage[0]["actor"] == "user"
        assert lineage[0]["actor_id"] == "u-1"
        assert lineage[0]["to_status"] == "candidate"

    def test_pending_review_routing(self, db: ThreadSafeConnection, pending_review_cfg: MemoryPromotionConfig) -> None:
        mem = propose_candidate(
            db,
            content="use black for formatting",
            scope="user",
            category="decision",
            proposer="user",
            proposer_id="u-1",
            config=pending_review_cfg,
        )
        assert mem["metadata"]["memory_status"] == "pending_review"

    def test_local_auto_approve_jumps_to_active(
        self, db: ThreadSafeConnection, auto_approve_cfg: MemoryPromotionConfig
    ) -> None:
        mem = propose_candidate(
            db,
            content="daily standup at 9am",
            scope="user",
            category="project_fact",
            proposer="user",
            proposer_id="u-1",
            config=auto_approve_cfg,
        )
        assert mem["metadata"]["memory_status"] == "active"
        assert mem["metadata"]["reviewed_by"] == "system:auto_approve"
        assert mem["metadata"]["reviewed_at"]
        lineage = mem["metadata"]["lineage"]
        assert lineage[0]["event"] == "auto_approved"
        assert lineage[0]["actor"] == "system"

    def test_agent_proposer_allowed_by_default(self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig) -> None:
        mem = propose_candidate(
            db,
            content="project uses Python 3.11",
            scope="user",
            category="project_fact",
            proposer="agent",
            proposer_id="agent-id-1",
            config=cfg,
        )
        assert mem["metadata"]["memory_status"] == "candidate"
        assert mem["metadata"]["lineage"][0]["actor"] == "agent"

    def test_agent_proposer_blocked_when_disabled(
        self, db: ThreadSafeConnection, agent_disabled_cfg: MemoryPromotionConfig
    ) -> None:
        with pytest.raises(PromotionAgentDisabledError):
            propose_candidate(
                db,
                content="blocked",
                scope="user",
                category="preference",
                proposer="agent",
                proposer_id="agent-id-1",
                config=agent_disabled_cfg,
            )

    def test_user_proposer_unaffected_when_agent_disabled(
        self, db: ThreadSafeConnection, agent_disabled_cfg: MemoryPromotionConfig
    ) -> None:
        mem = propose_candidate(
            db,
            content="user fine",
            scope="user",
            category="preference",
            proposer="user",
            proposer_id="u-1",
            config=agent_disabled_cfg,
        )
        assert mem["metadata"]["memory_status"] == "candidate"

    def test_invalid_proposer_rejected(self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig) -> None:
        with pytest.raises(ValueError, match="proposer must be one of"):
            propose_candidate(
                db,
                content="x",
                scope="user",
                category="preference",
                proposer="system",  # not allowed
                proposer_id="s-1",
                config=cfg,
            )

    def test_invalid_scope_rejected(self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig) -> None:
        with pytest.raises(ValueError, match="Invalid memory scope"):
            propose_candidate(
                db,
                content="x",
                scope="bogus",
                category="preference",
                proposer="user",
                proposer_id="u-1",
                config=cfg,
            )

    def test_invalid_category_rejected(self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig) -> None:
        with pytest.raises(ValueError, match="Invalid memory category"):
            propose_candidate(
                db,
                content="x",
                scope="user",
                category="bogus",
                proposer="user",
                proposer_id="u-1",
                config=cfg,
            )


class TestProposeRateLimit:
    def test_per_conversation_cap_enforced(
        self, db: ThreadSafeConnection, tight_rate_limit_cfg: MemoryPromotionConfig
    ) -> None:
        for i in range(2):
            propose_candidate(
                db,
                content=f"fact {i}",
                scope="user",
                category="preference",
                proposer="user",
                proposer_id="u-1",
                provenance={"conversation_id": CONV_A},
                config=tight_rate_limit_cfg,
                name=f"rl-a-{i}",
            )
        with pytest.raises(PromotionRateLimitError) as exc_info:
            propose_candidate(
                db,
                content="over the cap",
                scope="user",
                category="preference",
                proposer="user",
                proposer_id="u-1",
                provenance={"conversation_id": CONV_A},
                config=tight_rate_limit_cfg,
                name="rl-a-2",
            )
        assert exc_info.value.cap == 2
        assert exc_info.value.current == 2

    def test_cap_is_per_conversation_not_global(
        self, db: ThreadSafeConnection, tight_rate_limit_cfg: MemoryPromotionConfig
    ) -> None:
        for i in range(2):
            propose_candidate(
                db,
                content=f"fact {i}",
                scope="user",
                category="preference",
                proposer="user",
                proposer_id="u-1",
                provenance={"conversation_id": CONV_A},
                config=tight_rate_limit_cfg,
                name=f"rl-b-{i}",
            )
        # Different conversation_id — should still succeed.
        mem = propose_candidate(
            db,
            content="other conv",
            scope="user",
            category="preference",
            proposer="user",
            proposer_id="u-1",
            provenance={"conversation_id": CONV_B},
            config=tight_rate_limit_cfg,
            name="rl-b-other",
        )
        assert mem["metadata"]["memory_status"] == "candidate"

    def test_cap_skipped_when_conversation_id_absent(
        self, db: ThreadSafeConnection, tight_rate_limit_cfg: MemoryPromotionConfig
    ) -> None:
        for i in range(5):
            propose_candidate(
                db,
                content=f"no-conv {i}",
                scope="user",
                category="preference",
                proposer="user",
                proposer_id="u-1",
                provenance=None,
                config=tight_rate_limit_cfg,
                name=f"rl-c-{i}",
            )
        # No raise — conversation_id absent means rate limit is off.


# ---------------------------------------------------------------------------
# approve_candidate
# ---------------------------------------------------------------------------


def _propose(db: ThreadSafeConnection, cfg: MemoryPromotionConfig, **kwargs: Any) -> dict[str, Any]:
    defaults = dict(
        content="x",
        scope="user",
        category="preference",
        proposer="user",
        proposer_id="u-1",
        config=cfg,
    )
    defaults.update(kwargs)
    return propose_candidate(db, **defaults)


class TestApproveCandidate:
    def test_candidate_approved_to_active(self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig) -> None:
        mem = _propose(db, cfg, name="approve1")
        approved = approve_candidate(db, mem["fqn"], reviewer_id="rev-1", config=cfg)
        assert approved["metadata"]["memory_status"] == "active"
        assert approved["metadata"]["reviewed_by"] == "rev-1"
        assert approved["metadata"]["reviewed_at"]
        lineage = approved["metadata"]["lineage"]
        assert lineage[-1]["event"] == "approved"
        assert lineage[-1]["from_status"] == "candidate"
        assert lineage[-1]["to_status"] == "active"

    def test_pending_review_approved_to_active(
        self, db: ThreadSafeConnection, pending_review_cfg: MemoryPromotionConfig
    ) -> None:
        mem = _propose(db, pending_review_cfg, name="approve2")
        assert mem["metadata"]["memory_status"] == "pending_review"
        approved = approve_candidate(db, mem["fqn"], reviewer_id="rev-2", config=pending_review_cfg)
        assert approved["metadata"]["memory_status"] == "active"

    def test_approve_with_content_edit(self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig) -> None:
        mem = _propose(db, cfg, name="approve3", content="original")
        approved = approve_candidate(
            db,
            mem["fqn"],
            reviewer_id="rev-1",
            edits={"content": "edited"},
            config=cfg,
        )
        assert approved["content"] == "edited"
        events = [e["event"] for e in approved["metadata"]["lineage"]]
        assert "edit_applied" in events
        assert events[-1] == "approved"

    def test_approve_with_category_edit(self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig) -> None:
        mem = _propose(db, cfg, name="approve4")
        approved = approve_candidate(
            db,
            mem["fqn"],
            reviewer_id="rev-1",
            edits={"category": "decision"},
            config=cfg,
        )
        assert approved["metadata"]["memory_category"] == "decision"
        assert approved["metadata"]["memory_status"] == "active"

    def test_approve_already_active_rejected(
        self, db: ThreadSafeConnection, auto_approve_cfg: MemoryPromotionConfig, cfg: MemoryPromotionConfig
    ) -> None:
        mem = _propose(db, auto_approve_cfg, name="approve5")
        assert mem["metadata"]["memory_status"] == "active"
        with pytest.raises(PromotionStateError, match="Cannot approve memory"):
            approve_candidate(db, mem["fqn"], reviewer_id="rev-1", config=cfg)

    def test_approve_rejected_fails(self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig) -> None:
        mem = _propose(db, cfg, name="approve6")
        reject_candidate(db, mem["fqn"], reviewer_id="rev-1", reason="stale", config=cfg)
        with pytest.raises(PromotionStateError, match="Cannot approve memory"):
            approve_candidate(db, mem["fqn"], reviewer_id="rev-1", config=cfg)

    def test_approve_unknown_edit_key_rejected(self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig) -> None:
        mem = _propose(db, cfg, name="approve7")
        with pytest.raises(ValueError, match="Unknown edit field"):
            approve_candidate(db, mem["fqn"], reviewer_id="rev-1", edits={"status": "archived"}, config=cfg)

    def test_approve_unknown_fqn_raises(self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig) -> None:
        with pytest.raises(PromotionStateError, match="Memory not found"):
            approve_candidate(db, "@user/memory/does-not-exist", reviewer_id="rev-1", config=cfg)

    def test_approve_empty_content_edit_rejected(self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig) -> None:
        mem = _propose(db, cfg, name="approve8")
        with pytest.raises(ValueError, match="edits.content"):
            approve_candidate(db, mem["fqn"], reviewer_id="rev-1", edits={"content": ""}, config=cfg)


# ---------------------------------------------------------------------------
# reject_candidate
# ---------------------------------------------------------------------------


class TestRejectCandidate:
    def test_candidate_rejected(self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig) -> None:
        mem = _propose(db, cfg, name="reject1")
        rejected = reject_candidate(db, mem["fqn"], reviewer_id="rev-1", reason="stale", config=cfg)
        assert rejected["metadata"]["memory_status"] == "rejected"
        assert rejected["metadata"]["rejected_reason"] == "stale"
        assert rejected["metadata"]["reviewed_by"] == "rev-1"
        lineage = rejected["metadata"]["lineage"]
        assert lineage[-1]["event"] == "rejected"
        assert lineage[-1]["notes"] == "stale"

    def test_reject_active_fails(
        self, db: ThreadSafeConnection, auto_approve_cfg: MemoryPromotionConfig, cfg: MemoryPromotionConfig
    ) -> None:
        mem = _propose(db, auto_approve_cfg, name="reject2")
        with pytest.raises(PromotionStateError, match="Cannot reject memory"):
            reject_candidate(db, mem["fqn"], reviewer_id="rev-1", reason="x", config=cfg)

    def test_reject_reason_empty_rejected(self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig) -> None:
        mem = _propose(db, cfg, name="reject3")
        with pytest.raises(ValueError, match="non-empty"):
            reject_candidate(db, mem["fqn"], reviewer_id="rev-1", reason="", config=cfg)

    def test_reject_reason_truncated_to_cap(self, db: ThreadSafeConnection) -> None:
        tight_cfg = MemoryPromotionConfig(max_reject_reason_chars=10)
        mem = _propose(db, tight_cfg, name="reject4")
        rejected = reject_candidate(db, mem["fqn"], reviewer_id="rev-1", reason="x" * 500, config=tight_cfg)
        assert len(rejected["metadata"]["rejected_reason"]) == 10

    def test_reject_unknown_fqn_raises(self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig) -> None:
        with pytest.raises(PromotionStateError, match="Memory not found"):
            reject_candidate(db, "@user/memory/does-not-exist", reviewer_id="rev-1", reason="stale", config=cfg)


# ---------------------------------------------------------------------------
# list_candidates
# ---------------------------------------------------------------------------


class TestListCandidates:
    def test_list_defaults_to_candidate_status(self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig) -> None:
        _propose(db, cfg, name="list1")
        _propose(db, cfg, name="list2")
        mem_active = _propose(db, cfg, name="list3")
        approve_candidate(db, mem_active["fqn"], reviewer_id="rev-1", config=cfg)
        results = list_candidates(db)
        assert len(results) == 2
        assert {r["name"] for r in results} == {"list1", "list2"}

    def test_filter_by_pending_review(
        self, db: ThreadSafeConnection, pending_review_cfg: MemoryPromotionConfig, cfg: MemoryPromotionConfig
    ) -> None:
        _propose(db, pending_review_cfg, name="pr1")
        _propose(db, cfg, name="cand1")
        results = list_candidates(db, status="pending_review")
        assert len(results) == 1
        assert results[0]["name"] == "pr1"

    def test_filter_by_namespace(self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig) -> None:
        _propose(db, cfg, scope="user", name="ns1")
        _propose(db, cfg, scope="local", name="ns2")
        results = list_candidates(db, namespace="local")
        assert len(results) == 1
        assert results[0]["namespace"] == "local"

    def test_limit_respected(self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig) -> None:
        for i in range(5):
            _propose(db, cfg, name=f"lim{i}")
        results = list_candidates(db, limit=3)
        assert len(results) == 3

    def test_invalid_status_rejected(self, db: ThreadSafeConnection) -> None:
        with pytest.raises(ValueError, match="Invalid status"):
            list_candidates(db, status="bogus")


# ---------------------------------------------------------------------------
# Lineage truncation at service-level
# ---------------------------------------------------------------------------


class TestLineageTruncation:
    def test_truncation_fires_after_cap(
        self, db: ThreadSafeConnection, tiny_lineage_cfg: MemoryPromotionConfig
    ) -> None:
        mem = _propose(db, tiny_lineage_cfg, name="trunc1")
        # propose + approve + (re-propose not possible because approve is terminal,
        # so we simulate extra edits by calling approve with an edit) — but approve
        # on active raises, so exercise truncation by calling _append_lineage-heavy
        # operations through the edit path:
        # Instead: keep proposing different memories and call approve on each; at
        # 3-entry cap, approving a memory that received 2 lineage events (proposed,
        # edit_applied) plus the approval event should produce a truncated marker.
        approved = approve_candidate(
            db,
            mem["fqn"],
            reviewer_id="rev-1",
            edits={"content": "v2"},
            config=tiny_lineage_cfg,
        )
        # propose (1) + edit_applied (2) + approved (3) = exactly 3 events
        lineage = approved["metadata"]["lineage"]
        assert len(lineage) == 3
        events = [e["event"] for e in lineage]
        assert events == ["proposed", "edit_applied", "approved"]

    def test_truncation_marker_inserted_when_exceeded(
        self, db: ThreadSafeConnection, tiny_lineage_cfg: MemoryPromotionConfig
    ) -> None:
        mem = _propose(db, tiny_lineage_cfg, name="trunc2")
        # Force four events into a 3-entry lineage via manual metadata seeding
        # through the allowed update path — this verifies the truncation marker
        # path end-to-end.
        from anteroom.services.memory_service import update_memory_metadata

        update_memory_metadata(
            db,
            mem["fqn"],
            lineage=[
                {"event": "proposed", "actor": "u", "at": "2026-01-01T00:00:00Z"},
                {"event": "edit_applied", "actor": "u", "at": "2026-01-02T00:00:00Z"},
                {"event": "edit_applied", "actor": "u", "at": "2026-01-03T00:00:00Z"},
            ],
        )
        rejected = reject_candidate(db, mem["fqn"], reviewer_id="rev-1", reason="stale", config=tiny_lineage_cfg)
        lineage = rejected["metadata"]["lineage"]
        assert len(lineage) == 3
        assert lineage[0]["event"] == "truncated"
        assert lineage[-1]["event"] == "rejected"


# ---------------------------------------------------------------------------
# Integration sanity: recall should skip non-active statuses
# ---------------------------------------------------------------------------


class TestRecallCompatibility:
    def test_get_memory_still_returns_candidates(self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig) -> None:
        """get_memory is status-agnostic by design; recall enforcement lives in #921.

        This test just pins the service behaviour so a downstream change
        cannot accidentally filter status here.
        """
        mem = _propose(db, cfg, name="recall1")
        fetched = get_memory(db, mem["fqn"])
        assert fetched is not None
        assert fetched["metadata"]["memory_status"] == "candidate"


# ---------------------------------------------------------------------------
# Mid-operation db-failure branches (PromotionStateError paths)
# ---------------------------------------------------------------------------


class TestApproveEditFailurePaths:
    """The approve-with-edits flow has several mid-chain update_memory_*
    calls that return ``None`` when the row disappears between reads. These
    tests assert each branch surfaces a ``PromotionStateError`` rather than
    leaving the memory half-updated."""

    def test_edit_content_returning_none_raises_state_error(
        self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mem = _propose(db, cfg, name="edit-gone-content")
        # ``update_memory_content`` is imported lazily inside approve_candidate
        # via ``from .memory_service import ...`` — so patch it at its
        # definition site, not on the promotion module.
        monkeypatch.setattr(
            "anteroom.services.memory_service.update_memory_content",
            lambda *a, **kw: None,
        )
        with pytest.raises(PromotionStateError, match="during edit"):
            approve_candidate(
                db,
                mem["fqn"],
                reviewer_id="rev-1",
                config=cfg,
                edits={"content": "new body"},
            )

    def test_edit_category_returning_none_raises_state_error(
        self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mem = _propose(db, cfg, name="edit-gone-cat")
        # Only fail the metadata update path (category edit uses
        # update_memory_metadata). Content edit path is not exercised here.
        from anteroom.services import memory_service as _ms

        real_update = _ms.update_memory_metadata

        def _flaky(db_arg: Any, fqn_arg: str, **fields: Any) -> Any:
            if "memory_category" in fields and "memory_status" not in fields:
                return None
            return real_update(db_arg, fqn_arg, **fields)

        monkeypatch.setattr("anteroom.services.memory_promotion.update_memory_metadata", _flaky)
        with pytest.raises(PromotionStateError, match="during category edit"):
            approve_candidate(
                db,
                mem["fqn"],
                reviewer_id="rev-1",
                config=cfg,
                edits={"category": "decision"},
            )

    def test_final_commit_returning_none_raises_state_error(
        self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mem = _propose(db, cfg, name="final-gone")
        # Fail only the final approval commit (the one that sets
        # memory_status="active"). Other metadata updates pass through.
        from anteroom.services import memory_service as _ms

        real_update = _ms.update_memory_metadata

        def _flaky(db_arg: Any, fqn_arg: str, **fields: Any) -> Any:
            if fields.get("memory_status") == "active":
                return None
            return real_update(db_arg, fqn_arg, **fields)

        monkeypatch.setattr("anteroom.services.memory_promotion.update_memory_metadata", _flaky)
        with pytest.raises(PromotionStateError, match="during approval commit"):
            approve_candidate(db, mem["fqn"], reviewer_id="rev-1", config=cfg)

    def test_approve_edits_with_unknown_key_raises_value_error(
        self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig
    ) -> None:
        mem = _propose(db, cfg, name="unknown-edit")
        with pytest.raises(ValueError, match="Unknown edit field"):
            approve_candidate(
                db,
                mem["fqn"],
                reviewer_id="rev-1",
                config=cfg,
                edits={"bogus": "x"},
            )

    def test_approve_edits_with_invalid_category_raises_value_error(
        self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig
    ) -> None:
        mem = _propose(db, cfg, name="bad-cat-edit")
        with pytest.raises(ValueError, match="Invalid edit.category"):
            approve_candidate(
                db,
                mem["fqn"],
                reviewer_id="rev-1",
                config=cfg,
                edits={"category": "not-a-real-category"},
            )


class TestRejectFailurePath:
    def test_metadata_update_returning_none_raises_state_error(
        self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mem = _propose(db, cfg, name="reject-gone")
        monkeypatch.setattr(
            "anteroom.services.memory_promotion.update_memory_metadata",
            lambda *a, **kw: None,
        )
        with pytest.raises(PromotionStateError, match="during rejection commit"):
            reject_candidate(db, mem["fqn"], reviewer_id="rev-1", reason="stale", config=cfg)


class TestListCandidatesCombinedFilters:
    def test_namespace_and_status_filter_together(self, db: ThreadSafeConnection, cfg: MemoryPromotionConfig) -> None:
        _propose(db, cfg, name="c-user-1", scope="user")
        _propose(db, cfg, name="c-user-2", scope="user")
        proj = _propose(db, cfg, name="c-proj", scope="project", project_slug="myapp")
        # Approve the project one so it's no longer a candidate.
        approve_candidate(db, proj["fqn"], reviewer_id="rev-1", config=cfg)

        user_candidates = list_candidates(db, namespace="user", status="candidate")
        assert all(m["namespace"] == "user" for m in user_candidates)
        assert all(m["metadata"]["memory_status"] == "candidate" for m in user_candidates)
        assert len(user_candidates) == 2

        proj_candidates = list_candidates(db, namespace="myapp", status="candidate")
        # The project candidate was approved, so it's no longer in the
        # `candidate` queue.
        assert proj_candidates == []
