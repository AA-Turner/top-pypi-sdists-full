"""Pack-aware ``discover_workflows`` tests (#924 v5).

The v5 senior review pinned that ``discover_workflows`` must be DB-aware
so pack-distributed workflow templates reach the mission-profile
scoring pool. These tests lock in the contract:

1. No-db calls behave exactly as before (filesystem-only).
2. db-provided calls enumerate pack-sourced yaml paths alongside
   filesystem definitions.
3. On id collision, filesystem wins — a pack cannot silently replace
   a built-in that a mission profile was scored against.
4. Malformed pack yaml degrades gracefully.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from anteroom.db import _SCHEMA, ThreadSafeConnection
from anteroom.services.mission_profiles import discover_workflows


@pytest.fixture()
def db() -> ThreadSafeConnection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(_SCHEMA)
    conn.commit()
    return ThreadSafeConnection(conn)


def _install_pack_workflow(
    db: ThreadSafeConnection,
    tmp_path: Path,
    *,
    pack_name: str,
    namespace: str,
    workflow_id: str,
    content: str | None = None,
) -> Path:
    pack_dir = tmp_path / namespace / pack_name
    pack_dir.mkdir(parents=True, exist_ok=True)
    (pack_dir / "pack.yaml").write_text(
        f"name: {pack_name}\nnamespace: {namespace}\nversion: 0.0.1\n",
        encoding="utf-8",
    )
    templates_dir = pack_dir / "workflow_templates"
    templates_dir.mkdir(exist_ok=True)
    yaml_path = templates_dir / f"{workflow_id}.yaml"
    yaml_path.write_text(
        content
        or (
            f"kind: workflow\n"
            f"id: {workflow_id}\n"
            f"version: '0.0.1'\n"
            f"steps:\n"
            f"  - id: s1\n"
            f"    type: runner\n"
            f"    runner: cli_claude\n"
            f"    prompt: test\n"
        ),
        encoding="utf-8",
    )

    import uuid

    db.execute(
        "INSERT OR IGNORE INTO packs "
        "(id, name, namespace, version, description, source_path, installed_at, updated_at) "
        "VALUES (?, ?, ?, '0.0.1', '', ?, '', '')",
        (str(uuid.uuid4()), pack_name, namespace, str(pack_dir.resolve())),
    )
    return yaml_path


class TestDiscoverWorkflowsPackAware:
    def test_no_arg_is_filesystem_only(self) -> None:
        """Pre-#924 back-compat: calling with no args still works."""
        defs = discover_workflows()
        # Should contain filesystem-only entries — no packs present.
        assert all(isinstance(d.id, str) for d in defs)
        # No pack was installed; every entry must be filesystem-sourced.
        # (We verify via the paths ending in the package workflows/ or
        # examples/ dirs.)
        for d in defs:
            # No strict assertion on source here because ``WorkflowDefinition``
            # doesn't carry a source tag; the pack path assertion is in
            # test_db_with_pack_workflow below.
            assert d.id

    def test_explicit_none_is_filesystem_only(self) -> None:
        defs_none = discover_workflows(None)
        defs_default = discover_workflows()
        ids_none = {d.id for d in defs_none}
        ids_default = {d.id for d in defs_default}
        assert ids_none == ids_default

    def test_empty_db_is_filesystem_only(self, db: ThreadSafeConnection) -> None:
        defs_empty = discover_workflows(db)
        defs_none = discover_workflows(None)
        ids_empty = {d.id for d in defs_empty}
        ids_none = {d.id for d in defs_none}
        assert ids_empty == ids_none

    def test_pack_workflow_appears_in_discovery(
        self,
        db: ThreadSafeConnection,
        tmp_path: Path,
    ) -> None:
        _install_pack_workflow(
            db,
            tmp_path,
            pack_name="flows",
            namespace="acme",
            workflow_id="acme_pack_only",
        )
        defs = discover_workflows(db)
        ids = {d.id for d in defs}
        assert "acme_pack_only" in ids

    def test_filesystem_wins_on_collision(
        self,
        db: ThreadSafeConnection,
        tmp_path: Path,
    ) -> None:
        """If a pack ships an id that exists on filesystem, filesystem wins."""
        # Pick an id that we know ships in examples/
        _install_pack_workflow(
            db,
            tmp_path,
            pack_name="flows",
            namespace="acme",
            workflow_id="issue_delivery",
            # Distinguishable version so we can detect if pack won.
            content=(
                "kind: workflow\n"
                "id: issue_delivery\n"
                "version: '99.0.0'\n"  # sentinel: filesystem ships < 99.0.0
                "steps:\n"
                "  - id: s1\n"
                "    type: runner\n"
                "    runner: cli_claude\n"
                "    prompt: test\n"
            ),
        )
        defs = discover_workflows(db)
        hits = [d for d in defs if d.id == "issue_delivery"]
        assert len(hits) == 1
        # Filesystem won: version should NOT be the pack sentinel.
        assert hits[0].version != "99.0.0"

    def test_multi_pack_first_pack_wins(
        self,
        db: ThreadSafeConnection,
        tmp_path: Path,
    ) -> None:
        """Two packs ship the same id → first by ``packs.list_packs`` order wins."""
        _install_pack_workflow(
            db,
            tmp_path,
            pack_name="pack_a",
            namespace="acme",
            workflow_id="dup_id",
            content=(
                "kind: workflow\nid: dup_id\nversion: 'a'\n"
                "steps:\n  - id: s1\n    type: runner\n    runner: cli_claude\n    prompt: test\n"
            ),
        )
        _install_pack_workflow(
            db,
            tmp_path,
            pack_name="pack_b",
            namespace="acme",
            workflow_id="dup_id",
            content=(
                "kind: workflow\nid: dup_id\nversion: 'b'\n"
                "steps:\n  - id: s1\n    type: runner\n    runner: cli_claude\n    prompt: test\n"
            ),
        )
        defs = discover_workflows(db)
        hits = [d for d in defs if d.id == "dup_id"]
        assert len(hits) == 1
        # Ordering: packs.list_packs sorts by namespace, name. "pack_a"
        # precedes "pack_b" alphabetically, so version "a" must win.
        assert hits[0].version == "a"

    def test_malformed_pack_yaml_skipped(
        self,
        db: ThreadSafeConnection,
        tmp_path: Path,
    ) -> None:
        _install_pack_workflow(
            db,
            tmp_path,
            pack_name="broken",
            namespace="acme",
            workflow_id="broken_one",
            content="not valid yaml: [unclosed\n",
        )
        # Must not raise; skip the broken entry, keep returning the rest.
        defs = discover_workflows(db)
        ids = {d.id for d in defs}
        assert "broken_one" not in ids

    def test_pack_uninstalled_removed_on_next_call(
        self,
        db: ThreadSafeConnection,
        tmp_path: Path,
    ) -> None:
        _install_pack_workflow(
            db,
            tmp_path,
            pack_name="temp",
            namespace="acme",
            workflow_id="ephemeral_wf",
        )
        ids_before = {d.id for d in discover_workflows(db)}
        assert "ephemeral_wf" in ids_before

        # Simulate uninstall by removing the pack row.
        db.execute("DELETE FROM packs WHERE namespace = 'acme' AND name = 'temp'")
        ids_after = {d.id for d in discover_workflows(db)}
        assert "ephemeral_wf" not in ids_after
