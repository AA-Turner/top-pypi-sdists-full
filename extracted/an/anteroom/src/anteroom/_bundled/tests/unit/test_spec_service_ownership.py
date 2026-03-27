"""Tests for spec service ownership guards (#1010)."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest

VALID_SPEC_YAML = """\
requirements: |
  Must support widgets.
design: |
  Use the widget parser pattern.
tasks:
  - id: t1
    summary: Implement widget parser
"""


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    from anteroom.db import init_db

    return init_db(tmp_path / "test.db")


def _create_spec(db: Any, fqn: str = "@testns/spec/my-spec") -> dict[str, Any]:
    from anteroom.services.spec_service import create_spec

    return create_spec(db, "testns", "my-spec", VALID_SPEC_YAML)


def _make_pack_owned(db: Any, artifact_id: str) -> str:
    pack_id = uuid.uuid4().hex
    now = datetime.now(timezone.utc).isoformat()
    db.execute(
        "INSERT INTO packs (id, name, namespace, version, description, source_path, installed_at, updated_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (pack_id, "test-pack", "testns", "1.0.0", "", "/tmp/pack", now, now),
    )
    db.execute(
        "INSERT INTO pack_artifacts (pack_id, artifact_id) VALUES (?, ?)",
        (pack_id, artifact_id),
    )
    db.commit()
    return pack_id


class TestUpdateSpecContentOwnership:
    def test_update_raises_for_pack_owned(self, db: Any) -> None:
        art = _create_spec(db)
        _make_pack_owned(db, art["id"])

        from anteroom.services.spec_service import update_spec_content

        with pytest.raises(ValueError, match="owned by a pack"):
            update_spec_content(db, "@testns/spec/my-spec", VALID_SPEC_YAML)

    def test_update_works_for_non_pack_owned(self, db: Any) -> None:
        _create_spec(db)

        from anteroom.services.spec_service import update_spec_content

        result = update_spec_content(db, "@testns/spec/my-spec", VALID_SPEC_YAML)
        assert result is not None


class TestApprovePhasePackOwned:
    def test_approve_works_for_pack_owned(self, db: Any) -> None:
        art = _create_spec(db)
        _make_pack_owned(db, art["id"])

        from anteroom.services.spec_service import approve_phase

        result = approve_phase(db, "@testns/spec/my-spec", "requirements")
        assert result is not None
        assert result["metadata"]["phases"]["requirements"]["status"] == "approved"


class TestUnapprovePhasePackOwned:
    def test_unapprove_works_for_pack_owned(self, db: Any) -> None:
        art = _create_spec(db)
        _make_pack_owned(db, art["id"])

        from anteroom.services.spec_service import approve_phase, unapprove_phase

        approve_phase(db, "@testns/spec/my-spec", "design")
        result = unapprove_phase(db, "@testns/spec/my-spec", "design")
        assert result is not None
        assert result["metadata"]["phases"]["design"]["status"] == "draft"
