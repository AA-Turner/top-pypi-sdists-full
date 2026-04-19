"""Unit tests for the memory service — CRUD, validation, scope/FQN contract."""

from __future__ import annotations

import sqlite3

import pytest

from anteroom.db import _SCHEMA, ThreadSafeConnection
from anteroom.services.memory_service import (
    MEMORY_CATEGORIES,
    MEMORY_SCOPES,
    MEMORY_STATUSES,
    create_memory,
    delete_memory,
    get_memory,
    list_memories,
    namespace_for_scope,
    update_memory_content,
    update_memory_metadata,
)

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


# ---------------------------------------------------------------------------
# namespace_for_scope
# ---------------------------------------------------------------------------


class TestNamespaceForScope:
    def test_user_scope(self) -> None:
        assert namespace_for_scope("user") == "user"

    def test_local_scope(self) -> None:
        assert namespace_for_scope("local") == "local"

    def test_project_scope_with_slug(self) -> None:
        assert namespace_for_scope("project", project_slug="myproject") == "myproject"

    def test_project_scope_without_slug_raises(self) -> None:
        with pytest.raises(ValueError, match="project_slug is required"):
            namespace_for_scope("project")

    def test_project_scope_empty_slug_raises(self) -> None:
        with pytest.raises(ValueError, match="project_slug is required"):
            namespace_for_scope("project", project_slug="")

    def test_project_slug_with_invalid_chars_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid project_slug"):
            namespace_for_scope("project", project_slug="My Project!")

    def test_project_slug_with_uppercase_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid project_slug"):
            namespace_for_scope("project", project_slug="MyProject")

    def test_invalid_scope_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid memory scope"):
            namespace_for_scope("team")

    def test_project_slug_with_dots_and_hyphens(self) -> None:
        assert namespace_for_scope("project", project_slug="my-project.v2") == "my-project.v2"

    @pytest.mark.parametrize("reserved", ["user", "local"])
    def test_project_slug_reserved_namespace_raises(self, reserved: str) -> None:
        # Reject project_slug values that collide with reserved scope
        # namespaces — otherwise a project memory would receive an FQN
        # indistinguishable from a real user/local memory.
        with pytest.raises(ValueError, match="reserved scope namespace"):
            namespace_for_scope("project", project_slug=reserved)


# ---------------------------------------------------------------------------
# create_memory
# ---------------------------------------------------------------------------


class TestCreateMemory:
    def test_user_scope(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "prefer dark mode", scope="user", category="preference")
        assert art["type"] == "memory"
        assert art["namespace"] == "user"
        assert art["fqn"].startswith("@user/memory/")
        meta = art["metadata"]
        assert meta["memory_scope"] == "user"
        assert meta["memory_category"] == "preference"
        assert meta["memory_status"] == "active"
        assert meta["recall_count"] == 0

    def test_project_scope(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "uses postgresql", scope="project", category="project_fact", project_slug="myapp")
        assert art["namespace"] == "myapp"
        assert art["fqn"].startswith("@myapp/memory/")
        assert art["metadata"]["memory_scope"] == "project"

    def test_local_scope(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "temp note", scope="local", category="workflow_hint")
        assert art["namespace"] == "local"
        assert art["fqn"].startswith("@local/memory/")
        assert art["metadata"]["memory_scope"] == "local"

    def test_custom_name(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "some content", scope="user", category="decision", name="my-decision")
        assert art["name"] == "my-decision"
        assert art["fqn"] == "@user/memory/my-decision"

    def test_auto_slug_generation(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "some content", scope="user", category="preference")
        assert art["name"].startswith("pref-")
        assert len(art["name"].split("-")) == 3  # prefix-hash-date

    def test_with_provenance(self, db: ThreadSafeConnection) -> None:
        prov = {
            "conversation_id": "12345678-1234-1234-1234-123456789012",
            "message_id": "abcdefab-abcd-abcd-abcd-abcdefabcdef",
        }
        art = create_memory(db, "learned from chat", scope="user", category="preference", provenance=prov)
        meta = art["metadata"]
        assert meta["provenance"]["conversation_id"] == prov["conversation_id"]
        assert meta["provenance"]["message_id"] == prov["message_id"]
        assert meta["provenance"]["workflow_run_id"] is None

    def test_status_override(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "a candidate", scope="user", category="preference", status="candidate")
        assert art["metadata"]["memory_status"] == "candidate"

    def test_created_by_agent(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "agent note", scope="user", category="decision", created_by="agent")
        assert art["metadata"]["created_by"] == "agent"

    def test_invalid_scope_raises(self, db: ThreadSafeConnection) -> None:
        with pytest.raises(ValueError, match="Invalid memory scope"):
            create_memory(db, "x", scope="team", category="preference")

    def test_invalid_category_raises(self, db: ThreadSafeConnection) -> None:
        with pytest.raises(ValueError, match="Invalid memory category"):
            create_memory(db, "x", scope="user", category="random")

    def test_invalid_status_raises(self, db: ThreadSafeConnection) -> None:
        with pytest.raises(ValueError, match="Invalid memory status"):
            create_memory(db, "x", scope="user", category="preference", status="deleted")

    def test_invalid_created_by_raises(self, db: ThreadSafeConnection) -> None:
        with pytest.raises(ValueError, match="Invalid created_by"):
            create_memory(db, "x", scope="user", category="preference", created_by="system")

    def test_project_scope_requires_slug(self, db: ThreadSafeConnection) -> None:
        with pytest.raises(ValueError, match="project_slug is required"):
            create_memory(db, "x", scope="project", category="preference")

    @pytest.mark.parametrize("reserved", ["user", "local"])
    def test_project_slug_reserved_namespace_raises(self, db: ThreadSafeConnection, reserved: str) -> None:
        with pytest.raises(ValueError, match="reserved scope namespace"):
            create_memory(db, "x", scope="project", category="preference", project_slug=reserved)

    def test_provenance_oversized_id_raises(self, db: ThreadSafeConnection) -> None:
        with pytest.raises(ValueError, match="exceeds max length"):
            create_memory(
                db,
                "x",
                scope="user",
                category="preference",
                provenance={"conversation_id": "a" * 100},
            )

    def test_duplicate_fqn_raises(self, db: ThreadSafeConnection) -> None:
        create_memory(db, "first", scope="user", category="preference", name="unique-name")
        with pytest.raises(sqlite3.IntegrityError):
            create_memory(db, "second", scope="user", category="preference", name="unique-name")


# ---------------------------------------------------------------------------
# get_memory
# ---------------------------------------------------------------------------


class TestGetMemory:
    def test_existing(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "hello", scope="user", category="preference", name="test-get")
        fetched = get_memory(db, art["fqn"])
        assert fetched is not None
        assert fetched["content"] == "hello"
        assert fetched["metadata"]["memory_scope"] == "user"

    def test_nonexistent_returns_none(self, db: ThreadSafeConnection) -> None:
        assert get_memory(db, "@user/memory/nonexistent") is None


# ---------------------------------------------------------------------------
# list_memories
# ---------------------------------------------------------------------------


class TestListMemories:
    def test_list_all(self, db: ThreadSafeConnection) -> None:
        create_memory(db, "a", scope="user", category="preference", name="mem-a")
        create_memory(db, "b", scope="local", category="decision", name="mem-b")
        assert len(list_memories(db)) == 2

    def test_filter_by_scope(self, db: ThreadSafeConnection) -> None:
        create_memory(db, "a", scope="user", category="preference", name="mem-a")
        create_memory(db, "b", scope="local", category="preference", name="mem-b")
        results = list_memories(db, scope="user")
        assert len(results) == 1
        assert results[0]["metadata"]["memory_scope"] == "user"

    def test_filter_by_category(self, db: ThreadSafeConnection) -> None:
        create_memory(db, "a", scope="user", category="preference", name="mem-a")
        create_memory(db, "b", scope="user", category="decision", name="mem-b")
        results = list_memories(db, category="decision")
        assert len(results) == 1

    def test_filter_by_status(self, db: ThreadSafeConnection) -> None:
        create_memory(db, "a", scope="user", category="preference", name="mem-a", status="active")
        create_memory(db, "b", scope="user", category="preference", name="mem-b", status="candidate")
        results = list_memories(db, status="active")
        assert len(results) == 1

    def test_filter_by_namespace(self, db: ThreadSafeConnection) -> None:
        create_memory(db, "a", scope="user", category="preference", name="mem-a")
        create_memory(db, "b", scope="project", category="preference", name="mem-b", project_slug="proj")
        results = list_memories(db, namespace="proj")
        assert len(results) == 1

    def test_combined_filters(self, db: ThreadSafeConnection) -> None:
        create_memory(db, "a", scope="user", category="preference", name="mem-a")
        create_memory(db, "b", scope="user", category="decision", name="mem-b")
        create_memory(db, "c", scope="local", category="preference", name="mem-c")
        results = list_memories(db, scope="user", category="preference")
        assert len(results) == 1
        assert results[0]["name"] == "mem-a"

    def test_empty_result(self, db: ThreadSafeConnection) -> None:
        assert list_memories(db, scope="user") == []


# ---------------------------------------------------------------------------
# update_memory_content
# ---------------------------------------------------------------------------


class TestUpdateMemoryContent:
    def test_content_change_bumps_version(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "v1", scope="user", category="preference", name="upd")
        assert art["version"] == 1
        updated = update_memory_content(db, art["fqn"], "v2")
        assert updated is not None
        assert updated["content"] == "v2"
        assert updated["version"] == 2

    def test_metadata_preserved(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "v1", scope="user", category="preference", name="upd2")
        updated = update_memory_content(db, art["fqn"], "v2")
        assert updated is not None
        assert updated["metadata"]["memory_scope"] == "user"
        assert updated["metadata"]["memory_category"] == "preference"

    def test_nonexistent_returns_none(self, db: ThreadSafeConnection) -> None:
        assert update_memory_content(db, "@user/memory/nope", "x") is None


# ---------------------------------------------------------------------------
# update_memory_metadata
# ---------------------------------------------------------------------------


class TestUpdateMemoryMetadata:
    def test_update_status(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="meta1")
        updated = update_memory_metadata(db, art["fqn"], memory_status="archived")
        assert updated is not None
        assert updated["metadata"]["memory_status"] == "archived"

    def test_update_category(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="meta2")
        updated = update_memory_metadata(db, art["fqn"], memory_category="decision")
        assert updated is not None
        assert updated["metadata"]["memory_category"] == "decision"

    def test_reject_scope_change(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="meta3")
        with pytest.raises(ValueError, match="Cannot change memory_scope"):
            update_memory_metadata(db, art["fqn"], memory_scope="local")

    def test_invalid_status_raises(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="meta4")
        with pytest.raises(ValueError, match="Invalid memory_status"):
            update_memory_metadata(db, art["fqn"], memory_status="deleted")

    def test_invalid_category_raises(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="meta5")
        with pytest.raises(ValueError, match="Invalid memory_category"):
            update_memory_metadata(db, art["fqn"], memory_category="random")

    def test_preserves_unmodified_fields(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="meta6")
        updated = update_memory_metadata(db, art["fqn"], promoted_by="reviewer-1")
        assert updated is not None
        assert updated["metadata"]["promoted_by"] == "reviewer-1"
        assert updated["metadata"]["memory_scope"] == "user"
        assert updated["metadata"]["memory_category"] == "preference"
        assert updated["metadata"]["memory_status"] == "active"

    def test_nonexistent_returns_none(self, db: ThreadSafeConnection) -> None:
        assert update_memory_metadata(db, "@user/memory/nope", memory_status="archived") is None

    def test_read_then_merge_preserves_extra_keys(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="meta7")
        # Manually inject an extra key via direct metadata update to simulate
        # non-memory metadata stored alongside memory fields.
        from anteroom.services.artifact_storage import update_artifact

        merged = dict(art["metadata"])
        merged["custom_key"] = "preserved"
        update_artifact(db, art["id"], metadata=merged)
        # Now update via memory service — custom_key should survive.
        updated = update_memory_metadata(db, art["fqn"], memory_status="candidate")
        assert updated is not None
        assert updated["metadata"]["custom_key"] == "preserved"
        assert updated["metadata"]["memory_status"] == "candidate"


# ---------------------------------------------------------------------------
# delete_memory
# ---------------------------------------------------------------------------


class TestDeleteMemory:
    def test_existing_returns_true(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "doomed", scope="user", category="preference", name="del1")
        assert delete_memory(db, art["fqn"]) is True
        assert get_memory(db, art["fqn"]) is None

    def test_nonexistent_returns_false(self, db: ThreadSafeConnection) -> None:
        assert delete_memory(db, "@user/memory/nope") is False


# ---------------------------------------------------------------------------
# Constants validation
# ---------------------------------------------------------------------------


class TestTypeBoundary:
    """The memory service must refuse to touch non-memory artifacts even when
    they share the FQN namespace shape."""

    def _make_non_memory_artifact(self, db: ThreadSafeConnection) -> dict:
        from anteroom.services.artifact_storage import create_artifact
        from anteroom.services.artifacts import ArtifactType

        return create_artifact(
            db,
            fqn="@user/skill/not-a-memory",
            artifact_type=ArtifactType.SKILL,
            namespace="user",
            name="not-a-memory",
            content="a skill",
            metadata={},
        )

    def test_get_refuses_non_memory(self, db: ThreadSafeConnection) -> None:
        art = self._make_non_memory_artifact(db)
        assert get_memory(db, art["fqn"]) is None

    def test_update_content_refuses_non_memory(self, db: ThreadSafeConnection) -> None:
        art = self._make_non_memory_artifact(db)
        assert update_memory_content(db, art["fqn"], "mutated") is None
        # Original artifact content must remain untouched.
        from anteroom.services.artifact_storage import get_artifact_by_fqn

        assert get_artifact_by_fqn(db, art["fqn"])["content"] == "a skill"

    def test_update_metadata_refuses_non_memory(self, db: ThreadSafeConnection) -> None:
        art = self._make_non_memory_artifact(db)
        assert update_memory_metadata(db, art["fqn"], memory_status="archived") is None

    def test_delete_refuses_non_memory(self, db: ThreadSafeConnection) -> None:
        art = self._make_non_memory_artifact(db)
        assert delete_memory(db, art["fqn"]) is False
        # Artifact must still exist.
        from anteroom.services.artifact_storage import get_artifact_by_fqn

        assert get_artifact_by_fqn(db, art["fqn"]) is not None


class TestUpdateMemoryMetadataTypedContract:
    """The typed metadata contract must be enforced on update, not just create."""

    def test_unknown_field_rejected(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="typed1")
        with pytest.raises(ValueError, match="Unknown memory metadata field"):
            update_memory_metadata(db, art["fqn"], arbitrary_key="anything")

    def test_created_by_is_immutable(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="typed2")
        with pytest.raises(ValueError, match="Cannot change created_by"):
            update_memory_metadata(db, art["fqn"], created_by="agent")

    def test_promoted_by_oversized_rejected(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="typed3")
        with pytest.raises(ValueError, match="exceeds max length"):
            update_memory_metadata(db, art["fqn"], promoted_by="a" * 100)

    def test_recall_count_must_be_non_negative_int(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="typed4")
        with pytest.raises(ValueError, match="recall_count"):
            update_memory_metadata(db, art["fqn"], recall_count=-1)
        with pytest.raises(ValueError, match="recall_count"):
            update_memory_metadata(db, art["fqn"], recall_count="many")  # type: ignore[arg-type]

    def test_last_recalled_at_must_be_string_or_none(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="typed5")
        with pytest.raises(ValueError, match="last_recalled_at"):
            update_memory_metadata(db, art["fqn"], last_recalled_at=123)  # type: ignore[arg-type]

    def test_provenance_must_be_dict(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="typed6")
        with pytest.raises(ValueError, match="provenance"):
            update_memory_metadata(db, art["fqn"], provenance="not-a-dict")  # type: ignore[arg-type]

    def test_provenance_unknown_key_rejected(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="typed7")
        with pytest.raises(ValueError, match="Unknown provenance field"):
            update_memory_metadata(db, art["fqn"], provenance={"bogus": "x"})

    def test_provenance_oversized_id_rejected(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="typed8")
        with pytest.raises(ValueError, match="exceeds max length"):
            update_memory_metadata(db, art["fqn"], provenance={"conversation_id": "a" * 100})

    def test_valid_provenance_update(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="typed9")
        updated = update_memory_metadata(
            db,
            art["fqn"],
            provenance={"conversation_id": "12345678-1234-1234-1234-123456789012"},
        )
        assert updated is not None
        assert updated["metadata"]["provenance"]["conversation_id"] == "12345678-1234-1234-1234-123456789012"

    # Review-state allowlist extensions (#920)

    def test_reviewed_by_string_accepted(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="review1")
        updated = update_memory_metadata(db, art["fqn"], reviewed_by="reviewer-1")
        assert updated is not None
        assert updated["metadata"]["reviewed_by"] == "reviewer-1"

    def test_reviewed_by_non_string_rejected(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="review2")
        with pytest.raises(ValueError, match="reviewed_by"):
            update_memory_metadata(db, art["fqn"], reviewed_by=123)  # type: ignore[arg-type]

    def test_reviewed_by_oversized_rejected(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="review3")
        with pytest.raises(ValueError, match="exceeds max length"):
            update_memory_metadata(db, art["fqn"], reviewed_by="a" * 100)

    def test_reviewed_at_string_accepted(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="review4")
        updated = update_memory_metadata(db, art["fqn"], reviewed_at="2026-04-17T12:00:00Z")
        assert updated is not None
        assert updated["metadata"]["reviewed_at"] == "2026-04-17T12:00:00Z"

    def test_reviewed_at_non_string_rejected(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="review5")
        with pytest.raises(ValueError, match="reviewed_at"):
            update_memory_metadata(db, art["fqn"], reviewed_at=123)  # type: ignore[arg-type]

    def test_rejected_reason_short_accepted(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="review6")
        updated = update_memory_metadata(db, art["fqn"], rejected_reason="stale")
        assert updated is not None
        assert updated["metadata"]["rejected_reason"] == "stale"

    def test_rejected_reason_oversized_rejected(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="review7")
        with pytest.raises(ValueError, match="rejected_reason exceeds hard cap"):
            update_memory_metadata(db, art["fqn"], rejected_reason="x" * 5000)

    def test_lineage_list_of_valid_dicts_accepted(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="review8")
        updated = update_memory_metadata(
            db,
            art["fqn"],
            lineage=[
                {"event": "proposed", "actor": "user", "at": "2026-04-17T12:00:00Z"},
                {
                    "event": "approved",
                    "actor": "user",
                    "at": "2026-04-17T12:05:00Z",
                    "from_status": "candidate",
                    "to_status": "active",
                },
            ],
        )
        assert updated is not None
        assert len(updated["metadata"]["lineage"]) == 2

    def test_lineage_not_a_list_rejected(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="review9")
        with pytest.raises(ValueError, match="lineage must be a list"):
            update_memory_metadata(db, art["fqn"], lineage={"event": "approved"})  # type: ignore[arg-type]

    def test_lineage_unknown_event_rejected(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="review10")
        with pytest.raises(ValueError, match="lineage.0..event must be one of"):
            update_memory_metadata(
                db,
                art["fqn"],
                lineage=[{"event": "undeleted", "actor": "user", "at": "2026-04-17T12:00:00Z"}],
            )

    def test_lineage_missing_at_rejected(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="review11")
        with pytest.raises(ValueError, match="lineage.0..at"):
            update_memory_metadata(
                db,
                art["fqn"],
                lineage=[{"event": "approved", "actor": "user"}],
            )

    def test_lineage_non_dict_entry_rejected(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="review12")
        with pytest.raises(ValueError, match="lineage.0. must be a dict"):
            update_memory_metadata(db, art["fqn"], lineage=["not-a-dict"])  # type: ignore[list-item]

    # Retention pin flag (#625)

    def test_pinned_bool_accepted(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="pin1")
        updated = update_memory_metadata(db, art["fqn"], pinned=True)
        assert updated is not None
        assert updated["metadata"]["pinned"] is True

    def test_pinned_non_bool_rejected(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="pin2")
        with pytest.raises(ValueError, match="pinned must be a bool"):
            update_memory_metadata(db, art["fqn"], pinned="yes")  # type: ignore[arg-type]

    def test_pinned_int_1_rejected(self, db: ThreadSafeConnection) -> None:
        # Explicit regression: isinstance(True, int) is True in Python, so
        # the validator must not accept a plain int even though it would
        # "truthy-convert" to the same logical value.
        art = create_memory(db, "x", scope="user", category="preference", name="pin3")
        with pytest.raises(ValueError, match="pinned must be a bool"):
            update_memory_metadata(db, art["fqn"], pinned=1)  # type: ignore[arg-type]


class TestPinWrappers:
    def test_pin_memory_sets_pinned_true(self, db: ThreadSafeConnection) -> None:
        from anteroom.services.memory_service import pin_memory

        art = create_memory(db, "x", scope="user", category="preference", name="pw1")
        updated = pin_memory(db, art["fqn"])
        assert updated is not None
        assert updated["metadata"]["pinned"] is True

    def test_unpin_memory_sets_pinned_false(self, db: ThreadSafeConnection) -> None:
        from anteroom.services.memory_service import pin_memory, unpin_memory

        art = create_memory(db, "x", scope="user", category="preference", name="pw2")
        pin_memory(db, art["fqn"])
        updated = unpin_memory(db, art["fqn"])
        assert updated is not None
        assert updated["metadata"]["pinned"] is False

    def test_pin_memory_unknown_fqn_returns_none(self, db: ThreadSafeConnection) -> None:
        from anteroom.services.memory_service import pin_memory

        assert pin_memory(db, "@user/memory/nope") is None

    def test_unpin_memory_unknown_fqn_returns_none(self, db: ThreadSafeConnection) -> None:
        from anteroom.services.memory_service import unpin_memory

        assert unpin_memory(db, "@user/memory/nope") is None

    def test_pin_preserves_other_metadata(self, db: ThreadSafeConnection) -> None:
        from anteroom.services.memory_service import pin_memory

        art = create_memory(db, "x", scope="user", category="preference", name="pw3")
        # First mutate something else through the canonical path.
        update_memory_metadata(db, art["fqn"], recall_count=5)
        updated = pin_memory(db, art["fqn"])
        assert updated is not None
        assert updated["metadata"]["pinned"] is True
        assert updated["metadata"]["recall_count"] == 5


class TestConstants:
    def test_all_categories_are_fqn_safe(self) -> None:
        import re

        pattern = re.compile(r"^[a-z0-9_]+$")
        for cat in MEMORY_CATEGORIES:
            assert pattern.match(cat), f"Category {cat!r} is not FQN-safe"

    def test_scopes_match_expected(self) -> None:
        assert MEMORY_SCOPES == {"user", "project", "local"}

    def test_statuses_match_expected(self) -> None:
        assert MEMORY_STATUSES == {"active", "candidate", "pending_review", "rejected", "archived"}
