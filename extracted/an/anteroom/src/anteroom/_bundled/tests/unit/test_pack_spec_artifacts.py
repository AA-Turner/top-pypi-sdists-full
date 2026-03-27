"""Tests for spec artifact support in packs (#1010)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

from anteroom.services.artifacts import ArtifactType
from anteroom.services.packs import (
    _TYPE_DIRS,
    install_pack,
    parse_manifest,
    remove_pack,
    update_pack,
)

VALID_SPEC_YAML = """\
requirements: |
  Must support widgets.
design: |
  Use the widget parser pattern.
tasks:
  - id: t1
    summary: Implement widget parser
  - id: t2
    summary: Add validation layer
    depends_on: [t1]
"""

INVALID_SPEC_YAML = """\
requirements: |
  Valid requirements.
design: |
  Valid design.
tasks: not-a-list
"""

UPDATED_SPEC_YAML = """\
requirements: |
  Must support widgets and gadgets.
design: |
  Use the widget parser pattern with gadget extension.
tasks:
  - id: t1
    summary: Implement widget parser
  - id: t2
    summary: Add validation layer
    depends_on: [t1]
  - id: t3
    summary: Add gadget support
    depends_on: [t1]
"""


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    from anteroom.db import init_db

    return init_db(tmp_path / "test.db")


def _make_spec_pack(tmp_path: Path, spec_yaml: str, name: str = "my-spec") -> Path:
    pack_dir = tmp_path / "pack"
    pack_dir.mkdir(parents=True, exist_ok=True)
    specs_dir = pack_dir / "specs"
    specs_dir.mkdir(exist_ok=True)
    (specs_dir / f"{name}.yaml").write_text(spec_yaml, encoding="utf-8")
    manifest = {
        "name": "spec-pack",
        "namespace": "testns",
        "version": "1.0.0",
        "artifacts": [{"type": "spec", "name": name}],
    }
    (pack_dir / "pack.yaml").write_text(yaml.dump(manifest), encoding="utf-8")
    return pack_dir


class TestTypeDirsIncludesSpec:
    def test_spec_in_type_dirs(self) -> None:
        assert ArtifactType.SPEC in _TYPE_DIRS
        assert _TYPE_DIRS[ArtifactType.SPEC] == "specs"


class TestInstallPackWithSpec:
    def test_install_with_valid_spec(self, db: Any, tmp_path: Path) -> None:
        pack_dir = _make_spec_pack(tmp_path, VALID_SPEC_YAML)
        manifest = parse_manifest(pack_dir / "pack.yaml")
        result = install_pack(db, manifest, pack_dir)

        assert result["action"] == "installed"
        assert result["artifact_count"] == 1
        assert result["skipped_artifacts"] == []

        # Verify the artifact exists in DB with correct metadata
        from anteroom.services.artifact_storage import get_artifact_by_fqn

        art = get_artifact_by_fqn(db, "@testns/spec/my-spec")
        assert art is not None
        assert art["type"] == "spec"
        assert art["content"] == VALID_SPEC_YAML
        meta = art["metadata"]
        assert "phases" in meta
        for phase in ("requirements", "design", "tasks"):
            assert meta["phases"][phase]["status"] == "draft"

    def test_install_with_invalid_spec_skips(self, db: Any, tmp_path: Path) -> None:
        pack_dir = _make_spec_pack(tmp_path, INVALID_SPEC_YAML)
        manifest = parse_manifest(pack_dir / "pack.yaml")
        result = install_pack(db, manifest, pack_dir)

        assert result["artifact_count"] == 0
        assert "spec/my-spec" in result["skipped_artifacts"]

    def test_install_with_mixed_artifacts(self, db: Any, tmp_path: Path) -> None:
        pack_dir = tmp_path / "pack"
        pack_dir.mkdir(parents=True)
        (pack_dir / "specs").mkdir()
        (pack_dir / "specs" / "feat.yaml").write_text(VALID_SPEC_YAML, encoding="utf-8")
        (pack_dir / "skills").mkdir()
        (pack_dir / "skills" / "greet.yaml").write_text("content: Hello!\n", encoding="utf-8")
        manifest_data = {
            "name": "mixed-pack",
            "namespace": "testns",
            "version": "1.0.0",
            "artifacts": [
                {"type": "spec", "name": "feat"},
                {"type": "skill", "name": "greet"},
            ],
        }
        (pack_dir / "pack.yaml").write_text(yaml.dump(manifest_data), encoding="utf-8")
        manifest = parse_manifest(pack_dir / "pack.yaml")
        result = install_pack(db, manifest, pack_dir)

        assert result["artifact_count"] == 2


class TestUpdatePackWithSpec:
    def test_update_unchanged_preserves_metadata(self, db: Any, tmp_path: Path) -> None:
        pack_dir = _make_spec_pack(tmp_path, VALID_SPEC_YAML)
        manifest = parse_manifest(pack_dir / "pack.yaml")
        install_pack(db, manifest, pack_dir)

        # Approve a phase
        from anteroom.services.spec_service import approve_phase

        approve_phase(db, "@testns/spec/my-spec", "requirements")

        # Update with same content
        result = update_pack(db, manifest, pack_dir)
        assert result["artifact_count"] == 1

        from anteroom.services.artifact_storage import get_artifact_by_fqn

        art = get_artifact_by_fqn(db, "@testns/spec/my-spec")
        assert art["metadata"]["phases"]["requirements"]["status"] == "approved"

    def test_update_changed_content_triggers_invalidation(self, db: Any, tmp_path: Path) -> None:
        pack_dir = _make_spec_pack(tmp_path, VALID_SPEC_YAML)
        manifest = parse_manifest(pack_dir / "pack.yaml")
        install_pack(db, manifest, pack_dir)

        # Approve design
        from anteroom.services.spec_service import approve_phase

        approve_phase(db, "@testns/spec/my-spec", "design")

        # Update with changed requirements
        (pack_dir / "specs" / "my-spec.yaml").write_text(UPDATED_SPEC_YAML, encoding="utf-8")
        result = update_pack(db, manifest, pack_dir)
        assert result["artifact_count"] == 1

        from anteroom.services.artifact_storage import get_artifact_by_fqn

        art = get_artifact_by_fqn(db, "@testns/spec/my-spec")
        # Design should be stale because requirements changed
        assert art["metadata"]["phases"]["design"]["status"] == "stale"


class TestRemovePackCleansUpSpec:
    def test_remove_deletes_spec_artifact(self, db: Any, tmp_path: Path) -> None:
        pack_dir = _make_spec_pack(tmp_path, VALID_SPEC_YAML)
        manifest = parse_manifest(pack_dir / "pack.yaml")
        install_pack(db, manifest, pack_dir)

        from anteroom.services.artifact_storage import get_artifact_by_fqn

        assert get_artifact_by_fqn(db, "@testns/spec/my-spec") is not None

        removed = remove_pack(db, "testns", "spec-pack")
        assert removed is True
        assert get_artifact_by_fqn(db, "@testns/spec/my-spec") is None
