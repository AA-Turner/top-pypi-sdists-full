"""Tests for the memory recall pipeline (services/memory_recall.py).

Covers retrieve_memories (selection, budget, scope isolation, degradation),
format_memory_context (untrusted-content wrapping), strip_memory_context,
and visible_namespaces (scope visibility).
"""

from __future__ import annotations

import sqlite3
from unittest.mock import AsyncMock, MagicMock

import pytest

from anteroom.config import MemoryRecallConfig
from anteroom.db import _SCHEMA, ThreadSafeConnection
from anteroom.services.memory_recall import (
    RecalledMemory,
    format_memory_context,
    retrieve_memories,
    strip_memory_context,
    visible_namespaces,
)
from anteroom.services.memory_service import create_memory


def _make_config(**overrides: object) -> MemoryRecallConfig:
    defaults: dict = {
        "enabled": True,
        "max_memories": 5,
        "max_tokens": 800,
        "similarity_threshold": 0.5,
        "show_status": True,
    }
    defaults.update(overrides)
    return MemoryRecallConfig(**defaults)  # type: ignore[arg-type]


def _fake_embedding() -> list[float]:
    return [0.1] * 384


def _make_row(
    *,
    artifact_id: str,
    fqn: str,
    namespace: str,
    name: str,
    content: str,
    distance: float,
    scope: str,
    category: str = "preference",
    status: str = "active",
) -> dict:
    return {
        "id": artifact_id,
        "fqn": fqn,
        "namespace": namespace,
        "name": name,
        "content": content,
        "metadata": {
            "memory_scope": scope,
            "memory_category": category,
            "memory_status": status,
        },
        "distance": distance,
    }


def _make_vec_manager(*, has_memories: bool = True) -> MagicMock:
    vm = MagicMock()
    vm.memories = MagicMock() if has_memories else None
    return vm


def _make_empty_vec_manager() -> MagicMock:
    vm = _make_vec_manager()
    vm.memories.count.return_value = 0
    return vm


@pytest.fixture()
def real_db() -> ThreadSafeConnection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(_SCHEMA)
    conn.commit()
    return ThreadSafeConnection(conn)


class TestVisibleNamespaces:
    def test_user_only_when_no_context(self) -> None:
        assert visible_namespaces() == ["user"]

    def test_project_ns_included_when_provided(self) -> None:
        ns = visible_namespaces(project_namespace="myproject")
        assert "user" in ns
        assert "myproject" in ns

    def test_local_included_for_local_space(self) -> None:
        ns = visible_namespaces(space_type="local")
        assert "local" in ns

    def test_empty_project_namespace_ignored(self) -> None:
        ns = visible_namespaces(project_namespace="")
        assert ns == ["user"]


class TestRetrieveMemories:
    @pytest.mark.asyncio
    async def test_returns_selected_memories(self) -> None:
        emb = AsyncMock()
        emb.embed = AsyncMock(return_value=_fake_embedding())
        db = MagicMock()
        vm = _make_vec_manager()

        rows = [
            _make_row(
                artifact_id="a1",
                fqn="@user/memory/pref-1",
                namespace="user",
                name="pref-1",
                content="I prefer dark mode",
                distance=0.1,
                scope="user",
            ),
        ]
        with _patch_search(rows):
            memories, reason = await retrieve_memories(
                query="do I prefer dark or light?",
                db=db,
                embedding_service=emb,
                config=_make_config(),
                vec_manager=vm,
            )
        assert reason is None
        assert len(memories) == 1
        assert memories[0].fqn == "@user/memory/pref-1"
        assert memories[0].scope == "user"

    @pytest.mark.asyncio
    async def test_disabled_returns_reason(self) -> None:
        memories, reason = await retrieve_memories(
            query="anything at all",
            db=MagicMock(),
            embedding_service=AsyncMock(),
            config=_make_config(enabled=False),
            vec_manager=_make_vec_manager(),
        )
        assert memories == []
        assert reason == "Memory recall disabled"

    @pytest.mark.asyncio
    async def test_short_query_rejected(self) -> None:
        memories, reason = await retrieve_memories(
            query="hi",
            db=MagicMock(),
            embedding_service=AsyncMock(),
            config=_make_config(),
            vec_manager=_make_vec_manager(),
        )
        assert memories == []
        assert reason == "Query too short for recall"

    @pytest.mark.asyncio
    async def test_no_vec_support_returns_reason(self) -> None:
        memories, reason = await retrieve_memories(
            query="this is a long enough query",
            db=MagicMock(),
            embedding_service=AsyncMock(),
            config=_make_config(),
            vec_manager=_make_vec_manager(has_memories=False),
        )
        assert memories == []
        assert reason == "no_vec_support"

    @pytest.mark.asyncio
    async def test_missing_embedding_service(self) -> None:
        memories, reason = await retrieve_memories(
            query="this is a long enough query",
            db=MagicMock(),
            embedding_service=None,
            config=_make_config(),
            vec_manager=_make_vec_manager(),
        )
        assert memories == []
        assert reason == "Embedding service unavailable"

    @pytest.mark.asyncio
    async def test_empty_memory_index_skips_embedding(self) -> None:
        emb = AsyncMock()
        emb.embed = AsyncMock(return_value=_fake_embedding())
        memories, reason = await retrieve_memories(
            query="this is a long enough query",
            db=MagicMock(),
            embedding_service=emb,
            config=_make_config(),
            vec_manager=_make_empty_vec_manager(),
        )
        assert memories == []
        assert reason == "no_embeddings_yet"
        emb.embed.assert_not_called()

    @pytest.mark.asyncio
    async def test_embedding_failure_graceful(self) -> None:
        emb = AsyncMock()
        emb.embed = AsyncMock(side_effect=RuntimeError("kaboom"))
        memories, reason = await retrieve_memories(
            query="this is a long enough query",
            db=MagicMock(),
            embedding_service=emb,
            config=_make_config(),
            vec_manager=_make_vec_manager(),
        )
        assert memories == []
        assert reason == "Embedding failed"

    @pytest.mark.asyncio
    async def test_empty_embedding_graceful(self) -> None:
        emb = AsyncMock()
        emb.embed = AsyncMock(return_value=None)
        memories, reason = await retrieve_memories(
            query="this is a long enough query",
            db=MagicMock(),
            embedding_service=emb,
            config=_make_config(),
            vec_manager=_make_vec_manager(),
        )
        assert memories == []
        assert reason == "Embedding service returned empty result"

    @pytest.mark.asyncio
    async def test_no_embeddings_returns_reason(self) -> None:
        emb = AsyncMock()
        emb.embed = AsyncMock(return_value=_fake_embedding())
        with _patch_search([]):
            memories, reason = await retrieve_memories(
                query="this is a long enough query",
                db=MagicMock(),
                embedding_service=emb,
                config=_make_config(),
                vec_manager=_make_vec_manager(),
            )
        assert memories == []
        assert reason == "no_embeddings_yet"

    @pytest.mark.asyncio
    async def test_no_vec_support_falls_back_to_lexical_match(self, real_db: ThreadSafeConnection) -> None:
        create_memory(
            real_db,
            "My company id is 12345",
            scope="user",
            category="project_fact",
            name="company-id",
        )
        emb = AsyncMock()
        emb.embed = AsyncMock(return_value=_fake_embedding())

        memories, reason = await retrieve_memories(
            query="What is my company ID?",
            db=real_db,
            embedding_service=emb,
            config=_make_config(),
            vec_manager=_make_vec_manager(has_memories=False),
        )

        assert reason is None
        assert [m.fqn for m in memories] == ["@user/memory/company-id"]

    @pytest.mark.asyncio
    async def test_no_embeddings_yet_falls_back_to_active_memory_scan(self, real_db: ThreadSafeConnection) -> None:
        create_memory(
            real_db,
            "My company id is 12345",
            scope="user",
            category="project_fact",
            name="company-id-fallback",
        )
        emb = AsyncMock()
        emb.embed = AsyncMock(return_value=_fake_embedding())

        with _patch_search([]):
            memories, reason = await retrieve_memories(
                query="What is my company ID?",
                db=real_db,
                embedding_service=emb,
                config=_make_config(),
                vec_manager=_make_vec_manager(),
            )

        assert reason is None
        assert [m.fqn for m in memories] == ["@user/memory/company-id-fallback"]

    @pytest.mark.asyncio
    async def test_distance_threshold_filters(self) -> None:
        emb = AsyncMock()
        emb.embed = AsyncMock(return_value=_fake_embedding())
        rows = [
            _make_row(
                artifact_id="a1",
                fqn="@user/memory/far",
                namespace="user",
                name="far",
                content="far off memory",
                distance=0.9,  # above threshold 0.5
                scope="user",
            ),
        ]
        with _patch_search(rows):
            memories, reason = await retrieve_memories(
                query="this is a long enough query",
                db=MagicMock(),
                embedding_service=emb,
                config=_make_config(similarity_threshold=0.5),
                vec_manager=_make_vec_manager(),
            )
        assert memories == []
        assert reason == "no_matches_within_threshold"

    @pytest.mark.asyncio
    async def test_status_filter_excludes_non_active(self) -> None:
        emb = AsyncMock()
        emb.embed = AsyncMock(return_value=_fake_embedding())
        rows = [
            _make_row(
                artifact_id="a1",
                fqn="@user/memory/archived",
                namespace="user",
                name="archived",
                content="archived memory content",
                distance=0.1,
                scope="user",
                status="archived",
            ),
            _make_row(
                artifact_id="a2",
                fqn="@user/memory/active",
                namespace="user",
                name="active",
                content="active memory",
                distance=0.2,
                scope="user",
                status="active",
            ),
        ]
        with _patch_search(rows):
            memories, _ = await retrieve_memories(
                query="this is a long enough query",
                db=MagicMock(),
                embedding_service=emb,
                config=_make_config(),
                vec_manager=_make_vec_manager(),
            )
        assert len(memories) == 1
        assert memories[0].fqn == "@user/memory/active"

    @pytest.mark.asyncio
    async def test_scope_isolation_blocks_foreign_project(self) -> None:
        """A memory from a foreign project namespace must not be returned."""
        emb = AsyncMock()
        emb.embed = AsyncMock(return_value=_fake_embedding())
        # A row that somehow made it through the SQL filter with a foreign namespace
        rows = [
            _make_row(
                artifact_id="a1",
                fqn="@otherproj/memory/x",
                namespace="otherproj",
                name="x",
                content="project secret",
                distance=0.1,
                scope="project",
            ),
        ]
        with _patch_search(rows):
            memories, reason = await retrieve_memories(
                query="this is a long enough query",
                db=MagicMock(),
                embedding_service=emb,
                config=_make_config(),
                vec_manager=_make_vec_manager(),
                project_namespace="myproject",
            )
        # Defensive filter in retrieve_memories should drop it.
        assert memories == []
        assert reason == "no_matches_within_threshold"

    @pytest.mark.asyncio
    async def test_token_budget_enforced(self) -> None:
        emb = AsyncMock()
        emb.embed = AsyncMock(return_value=_fake_embedding())
        # Two 2000-char memories; 800-token budget (800 * 4 chars) fits exactly one.
        big = "x" * 2000
        rows = [
            _make_row(
                artifact_id="a1",
                fqn="@user/memory/a",
                namespace="user",
                name="a",
                content=big,
                distance=0.1,
                scope="user",
            ),
            _make_row(
                artifact_id="a2",
                fqn="@user/memory/b",
                namespace="user",
                name="b",
                content=big,
                distance=0.2,
                scope="user",
            ),
        ]
        with _patch_search(rows):
            memories, _ = await retrieve_memories(
                query="this is a long enough query",
                db=MagicMock(),
                embedding_service=emb,
                config=_make_config(max_tokens=800),
                vec_manager=_make_vec_manager(),
            )
        # 2000 chars / 4 = 500 tokens. First memory fits (500 <= 800); second
        # would push to 1000 tokens, over budget. So only one selected.
        assert len(memories) == 1
        assert memories[0].fqn == "@user/memory/a"

    @pytest.mark.asyncio
    async def test_max_memories_caps_result(self) -> None:
        emb = AsyncMock()
        emb.embed = AsyncMock(return_value=_fake_embedding())
        rows = [
            _make_row(
                artifact_id=f"a{i}",
                fqn=f"@user/memory/m{i}",
                namespace="user",
                name=f"m{i}",
                content=f"content {i}",
                distance=0.1 + i * 0.01,
                scope="user",
            )
            for i in range(10)
        ]
        with _patch_search(rows):
            memories, _ = await retrieve_memories(
                query="this is a long enough query",
                db=MagicMock(),
                embedding_service=emb,
                config=_make_config(max_memories=3),
                vec_manager=_make_vec_manager(),
            )
        assert len(memories) == 3

    @pytest.mark.asyncio
    async def test_search_exception_graceful(self) -> None:
        emb = AsyncMock()
        emb.embed = AsyncMock(return_value=_fake_embedding())
        from unittest.mock import patch

        with patch("anteroom.services.memory_recall.storage.search_similar_memory_artifacts") as mock:
            mock.side_effect = RuntimeError("DB exploded")
            memories, reason = await retrieve_memories(
                query="this is a long enough query",
                db=MagicMock(),
                embedding_service=emb,
                config=_make_config(),
                vec_manager=_make_vec_manager(),
            )
        assert memories == []
        assert reason == "search_failed"


class TestFormatMemoryContext:
    def test_empty_returns_empty_string(self) -> None:
        assert format_memory_context([]) == ""

    def test_wraps_every_memory_in_untrusted(self) -> None:
        mems = [
            RecalledMemory(
                fqn="@user/memory/m1",
                namespace="user",
                name="m1",
                content="secret content one",
                distance=0.1,
                scope="user",
                category="preference",
            ),
            RecalledMemory(
                fqn="@user/memory/m2",
                namespace="user",
                name="m2",
                content="another one",
                distance=0.2,
                scope="user",
                category="decision",
            ),
        ]
        output = format_memory_context(mems)
        # Both contents should be wrapped in untrusted envelopes.
        # wrap_untrusted uses <untrusted-content> or similar tags — just
        # verify both FQNs appear as origins and both contents are present.
        assert "memory:@user/memory/m1" in output
        assert "memory:@user/memory/m2" in output
        assert "secret content one" in output
        assert "another one" in output
        assert "Recalled Memories" in output

    def test_no_trusted_marker(self) -> None:
        mems = [
            RecalledMemory(
                fqn="@user/memory/m1",
                namespace="user",
                name="m1",
                content="c",
                distance=0.1,
                scope="user",
                category="preference",
            ),
        ]
        output = format_memory_context(mems)
        # Must NOT contain the trusted-section marker — memory is always untrusted.
        assert "<trusted>" not in output


class TestStripMemoryContext:
    def test_strips_memory_block(self) -> None:
        prompt = "## Intro\n\nhello\n\n## Recalled Memories\nSome memory\n"
        stripped = strip_memory_context(prompt)
        assert "Recalled Memories" not in stripped
        assert "hello" in stripped

    def test_idempotent_with_no_block(self) -> None:
        prompt = "## Intro\n\nhello"
        assert strip_memory_context(prompt) == prompt

    def test_preserves_following_sections(self) -> None:
        prompt = "## Intro\n\n## Recalled Memories\nX\n\n## Tail\nkeep me\n"
        stripped = strip_memory_context(prompt)
        assert "Recalled Memories" not in stripped
        assert "keep me" in stripped

    def test_handles_block_at_end_no_trailing_newline(self) -> None:
        """Block at absolute end-of-string with no trailing newline."""
        prompt = "## Intro\n\nhello\n\n## Recalled Memories\ntail memory"
        stripped = strip_memory_context(prompt)
        assert "Recalled Memories" not in stripped
        assert "tail memory" not in stripped
        assert "hello" in stripped

    def test_redos_safe_on_pathological_input(self) -> None:
        """Large inputs with no section boundary must terminate quickly.

        The prior regex ``## Recalled Memories.*?(?=\\n## |\\Z)`` under DOTALL
        invited polynomial backtracking on content that contained many ``\\n``
        candidates but no actual ``\\n## `` header.  The ``str.find``-based
        implementation is O(n) and cannot degrade.
        """
        import time

        hostile = "## Recalled Memories\n" + ("a" * 100_000) + ("\n" * 10_000)
        start = time.monotonic()
        stripped = strip_memory_context(hostile)
        elapsed = time.monotonic() - start
        # O(n) on a 110KB input should complete in well under 100ms on any machine.
        assert elapsed < 0.5, f"strip_memory_context took {elapsed:.2f}s — possible ReDoS regression"
        assert "Recalled Memories" not in stripped

    def test_strips_fully_when_memory_content_has_heading(self) -> None:
        """A memory whose content contains a ``## `` heading must still strip cleanly.

        Regression for a bug where the boundary scan stopped at the first
        ``\\n## `` after the section header — including headings embedded
        inside the recalled memory's wrapped content — leaving stale
        recalled context in the prompt for the next turn.
        """
        from anteroom.services.memory_recall import RecalledMemory, format_memory_context

        hostile = RecalledMemory(
            fqn="@user/memory/embed-heading",
            namespace="user",
            name="embed-heading",
            content="Before\n## Not Really A Section\nAfter",
            distance=0.1,
            scope="user",
            category="preference",
        )
        memory_block = format_memory_context([hostile])
        prompt = "## Intro\n\nhello" + memory_block

        stripped = strip_memory_context(prompt)

        assert "Recalled Memories" not in stripped
        assert "Not Really A Section" not in stripped
        assert "After" not in stripped
        assert "hello" in stripped

    def test_strips_when_memory_heading_precedes_real_next_section(self) -> None:
        """Envelope-embedded heading + real trailing section is handled correctly."""
        from anteroom.services.memory_recall import RecalledMemory, format_memory_context

        hostile = RecalledMemory(
            fqn="@user/memory/nested",
            namespace="user",
            name="nested",
            content="line1\n## Fake Heading\nline2",
            distance=0.1,
            scope="user",
            category="preference",
        )
        memory_block = format_memory_context([hostile])
        prompt = "## Intro\n\nhello" + memory_block + "\n\n## RAG Context\nreal tail\n"

        stripped = strip_memory_context(prompt)

        assert "Recalled Memories" not in stripped
        assert "Fake Heading" not in stripped
        assert "real tail" in stripped
        assert "hello" in stripped

    def test_handles_multiple_memories_with_embedded_headings(self) -> None:
        """Multiple recalled memories, each containing headings, all stripped."""
        from anteroom.services.memory_recall import RecalledMemory, format_memory_context

        memories = [
            RecalledMemory(
                fqn=f"@user/memory/m{i}",
                namespace="user",
                name=f"m{i}",
                content=f"content {i}\n## Inner {i}\nmore {i}",
                distance=0.1 * (i + 1),
                scope="user",
                category="preference",
            )
            for i in range(3)
        ]
        prompt = "## Intro\nbase" + format_memory_context(memories) + "\n\n## After\ntail\n"

        stripped = strip_memory_context(prompt)

        for i in range(3):
            assert f"Inner {i}" not in stripped
            assert f"content {i}" not in stripped
        assert "tail" in stripped
        assert "base" in stripped


# -- Helpers -----------------------------------------------------------


def _patch_search(rows: list[dict]):
    """Context manager that patches the storage search function to return *rows*."""
    from unittest.mock import patch

    return patch(
        "anteroom.services.memory_recall.storage.search_similar_memory_artifacts",
        return_value=rows,
    )
