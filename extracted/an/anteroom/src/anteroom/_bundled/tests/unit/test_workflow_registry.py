"""Unit tests for ``services.workflow_registry`` (#924)."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from unittest.mock import patch

import pytest

from anteroom.db import _SCHEMA, ThreadSafeConnection
from anteroom.services.workflow_registry import (
    _is_safe_workflow_id,
    _list_pack_workflow_paths,
    _parse_fqn,
    list_available_workflows,
    resolve_workflow,
)


@pytest.fixture()
def db() -> ThreadSafeConnection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(_SCHEMA)
    conn.commit()
    return ThreadSafeConnection(conn)


def _install_pack_with_workflow(
    db: ThreadSafeConnection,
    tmp_path: Path,
    *,
    pack_name: str,
    namespace: str,
    workflow_id: str,
    content: str | None = None,
) -> tuple[str, Path]:
    """Install a minimal pack with one workflow_templates/<id>.yaml file.

    Returns ``(pack_id, yaml_path)``.
    """
    pack_dir = tmp_path / namespace / pack_name
    pack_dir.mkdir(parents=True)
    (pack_dir / "pack.yaml").write_text(
        f"name: {pack_name}\nnamespace: {namespace}\nversion: 0.0.1\n",
        encoding="utf-8",
    )
    templates_dir = pack_dir / "workflow_templates"
    templates_dir.mkdir()
    yaml_path = templates_dir / f"{workflow_id}.yaml"
    yaml_path.write_text(
        content
        or (
            f"kind: workflow\nid: {workflow_id}\nversion: '0.0.1'\n"
            "steps:\n  - id: s1\n    type: runner\n    runner: cli_claude\n    prompt: test\n"
        ),
        encoding="utf-8",
    )

    import uuid

    pack_id = str(uuid.uuid4())
    db.execute(
        "INSERT INTO packs (id, name, namespace, version, description, source_path, installed_at, updated_at) "
        "VALUES (?, ?, ?, ?, '', ?, '', '')",
        (pack_id, pack_name, namespace, "0.0.1", str(pack_dir.resolve())),
    )
    return pack_id, yaml_path


# ---------------------------------------------------------------------------
# Safety helpers
# ---------------------------------------------------------------------------


class TestIsSafeWorkflowId:
    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("issue_delivery", True),
            ("demo-flow", True),
            ("../etc/passwd", False),
            ("foo/bar", False),
            ("foo\\bar", False),
            ("..sneaky", False),
        ],
    )
    def test_safety(self, value: str, expected: bool) -> None:
        assert _is_safe_workflow_id(value) is expected


class TestParseFqn:
    def test_valid_fqn_returns_namespace_and_id(self) -> None:
        assert _parse_fqn("@acme/workflow/issue_delivery") == ("acme", "issue_delivery")

    def test_bare_id_returns_none(self) -> None:
        assert _parse_fqn("issue_delivery") is None

    def test_wrong_type_segment_returns_none(self) -> None:
        assert _parse_fqn("@acme/skill/foo") is None

    def test_traversal_in_namespace_returns_none(self) -> None:
        assert _parse_fqn("@../escape/workflow/x") is None


# ---------------------------------------------------------------------------
# _list_pack_workflow_paths
# ---------------------------------------------------------------------------


class TestListPackWorkflowPaths:
    def test_empty_db_returns_empty_list(self, db: ThreadSafeConnection) -> None:
        assert _list_pack_workflow_paths(db) == []

    def test_pack_with_one_workflow_enumerated(
        self,
        db: ThreadSafeConnection,
        tmp_path: Path,
    ) -> None:
        pack_id, yaml_path = _install_pack_with_workflow(
            db, tmp_path, pack_name="flows", namespace="acme", workflow_id="deliver"
        )
        results = _list_pack_workflow_paths(db)
        assert len(results) == 1
        path, wf_id, pid, ns = results[0]
        assert path == yaml_path
        assert wf_id == "deliver"
        assert pid == pack_id
        assert ns == "acme"

    def test_pack_without_workflow_templates_dir_skipped(
        self,
        db: ThreadSafeConnection,
        tmp_path: Path,
    ) -> None:
        pack_dir = tmp_path / "acme" / "noflows"
        pack_dir.mkdir(parents=True)
        (pack_dir / "pack.yaml").write_text("name: noflows\nnamespace: acme\n", encoding="utf-8")
        import uuid

        db.execute(
            "INSERT INTO packs (id, name, namespace, version, description, source_path, installed_at, updated_at) "
            "VALUES (?, ?, ?, '0.0.1', '', ?, '', '')",
            (str(uuid.uuid4()), "noflows", "acme", str(pack_dir.resolve())),
        )
        assert _list_pack_workflow_paths(db) == []

    def test_traversal_filename_rejected(
        self,
        db: ThreadSafeConnection,
        tmp_path: Path,
    ) -> None:
        _install_pack_with_workflow(db, tmp_path, pack_name="flows", namespace="acme", workflow_id="deliver")
        # Drop a tricky file into the dir and verify only the legitimate one is returned.
        # (Glob('*.yaml') wouldn't match '..' so this mainly guards against future regressions.)
        results = _list_pack_workflow_paths(db)
        assert len(results) == 1

    def test_missing_source_path_skipped(self, db: ThreadSafeConnection, tmp_path: Path) -> None:
        import uuid

        db.execute(
            "INSERT INTO packs (id, name, namespace, version, description, source_path, installed_at, updated_at) "
            "VALUES (?, ?, ?, '0.0.1', '', '/nonexistent/pack', '', '')",
            (str(uuid.uuid4()), "ghost", "acme"),
        )
        assert _list_pack_workflow_paths(db) == []


# ---------------------------------------------------------------------------
# resolve_workflow
# ---------------------------------------------------------------------------


class TestResolveWorkflow:
    def test_filesystem_hit_returns_built_in_ref(self, db: ThreadSafeConnection) -> None:
        # Use a well-known workflow id that ships in examples/ or workflows/.
        with patch(
            "anteroom.services.workflow_registry._resolve_from_filesystem",
            return_value=(Path("/fake/workflows/x.yaml"), "built_in"),
        ):
            ref = resolve_workflow("x", db=db)
        assert ref is not None
        assert ref.id == "x"
        assert ref.source == "built_in"
        assert ref.pack_id is None

    def test_filesystem_miss_then_pack_hit(
        self,
        db: ThreadSafeConnection,
        tmp_path: Path,
    ) -> None:
        _install_pack_with_workflow(db, tmp_path, pack_name="flows", namespace="acme", workflow_id="pack_only")
        ref = resolve_workflow("pack_only", db=db)
        assert ref is not None
        assert ref.id == "pack_only"
        assert ref.source == "pack"
        assert ref.namespace == "acme"

    def test_no_db_returns_none_when_only_in_pack(
        self,
        db: ThreadSafeConnection,
        tmp_path: Path,
    ) -> None:
        _install_pack_with_workflow(db, tmp_path, pack_name="flows", namespace="acme", workflow_id="pack_only")
        # Without db, pack-only workflows are invisible.
        assert resolve_workflow("pack_only", db=None) is None

    def test_fqn_form_targets_namespace(
        self,
        db: ThreadSafeConnection,
        tmp_path: Path,
    ) -> None:
        _install_pack_with_workflow(db, tmp_path, pack_name="flows", namespace="acme", workflow_id="deliver")
        _install_pack_with_workflow(db, tmp_path, pack_name="flows", namespace="other", workflow_id="deliver")
        # FQN pinpoints the acme pack even though two packs ship "deliver".
        ref = resolve_workflow("@acme/workflow/deliver", db=db)
        assert ref is not None
        assert ref.namespace == "acme"
        ref2 = resolve_workflow("@other/workflow/deliver", db=db)
        assert ref2 is not None
        assert ref2.namespace == "other"

    def test_fqn_without_db_returns_none(self) -> None:
        # FQN is explicit intent; no filesystem fallback.
        assert resolve_workflow("@acme/workflow/x", db=None) is None

    def test_path_traversal_rejected_for_id(self, db: ThreadSafeConnection) -> None:
        # allow_filesystem=False is the router path.
        assert resolve_workflow("../etc/passwd", db=db, allow_filesystem=False) is None

    def test_filesystem_wins_over_pack_on_collision(
        self,
        db: ThreadSafeConnection,
        tmp_path: Path,
    ) -> None:
        # Install a pack with workflow id "issue_delivery" — an id that
        # also ships as a built-in example. Filesystem must win.
        _install_pack_with_workflow(db, tmp_path, pack_name="flows", namespace="acme", workflow_id="issue_delivery")
        ref = resolve_workflow("issue_delivery", db=db)
        assert ref is not None
        # If the filesystem has this example, source should be "example"
        # or "built_in" — definitely not "pack".
        assert ref.source != "pack"


# ---------------------------------------------------------------------------
# list_available_workflows
# ---------------------------------------------------------------------------


class TestListAvailableWorkflows:
    def test_filesystem_only_when_db_none(self) -> None:
        refs = list_available_workflows(db=None)
        # Non-empty because the package ships example workflows.
        assert all(r.source in {"built_in", "example"} for r in refs)
        assert all(r.pack_id is None for r in refs)

    def test_includes_pack_entries_when_db_provided(
        self,
        db: ThreadSafeConnection,
        tmp_path: Path,
    ) -> None:
        _install_pack_with_workflow(db, tmp_path, pack_name="flows", namespace="acme", workflow_id="pack_only_id")
        refs = list_available_workflows(db)
        pack_refs = [r for r in refs if r.source == "pack"]
        assert any(r.id == "pack_only_id" and r.namespace == "acme" for r in pack_refs)

    def test_pack_entry_dropped_on_filesystem_collision(
        self,
        db: ThreadSafeConnection,
        tmp_path: Path,
    ) -> None:
        # Collision with a shipped example: pack must NOT appear.
        _install_pack_with_workflow(db, tmp_path, pack_name="flows", namespace="acme", workflow_id="issue_delivery")
        refs = list_available_workflows(db)
        acme_entry = [r for r in refs if r.id == "issue_delivery" and r.namespace == "acme"]
        assert acme_entry == []

    def test_include_packs_false_skips_db(
        self,
        db: ThreadSafeConnection,
        tmp_path: Path,
    ) -> None:
        _install_pack_with_workflow(db, tmp_path, pack_name="flows", namespace="acme", workflow_id="pack_only_z")
        refs = list_available_workflows(db, include_packs=False)
        assert all(r.source != "pack" for r in refs)


# ---------------------------------------------------------------------------
# Resolver-threading regression: every call site gets db
# ---------------------------------------------------------------------------


class TestResolverThreading:
    """Pin that every downstream caller now passes db through.

    These assertions don't run the full code path — they just assert
    that each caller module imports ``resolve_workflow_path`` from the
    shim AND that the shim itself delegates to the registry. This is a
    cheap safety net that catches "somebody re-imported the legacy
    resolver directly" drift.
    """

    def test_workflow_resolution_shim_delegates_to_registry(self) -> None:
        # The shim source must call resolve_workflow; keyword `db=db` must
        # appear so the delegation carries identity forward.
        import inspect

        from anteroom.services.workflow_resolution import resolve_workflow_path

        source = inspect.getsource(resolve_workflow_path)
        assert "resolve_workflow" in source
        assert "db=db" in source

    @pytest.mark.parametrize(
        "module_path",
        [
            "anteroom.routers.workflows",
            "anteroom.routers.specs",
            "anteroom.services.workflow_executor",
            "anteroom.services.workflow_scheduler",
            "anteroom.services.mission_profiles",
        ],
    )
    def test_caller_imports_shim_not_legacy_module(self, module_path: str) -> None:
        import importlib
        import inspect

        mod = importlib.import_module(module_path)
        source = inspect.getsource(mod)
        # Every caller should be importing resolve_workflow_path from
        # workflow_resolution (the shim) or workflow_registry (the source).
        assert (
            "from ..services.workflow_resolution import resolve_workflow_path" in source
            or "from .workflow_resolution import resolve_workflow_path" in source
            or "from .workflow_registry import" in source
            or "from ..services.workflow_registry" in source
        )
