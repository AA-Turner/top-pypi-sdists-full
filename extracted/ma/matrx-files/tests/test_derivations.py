from __future__ import annotations

import re

import pytest

from matrx_files.cloud_sync import get_migration_sql
from matrx_files.derivations import (
    FILE_DERIVATION_KINDS,
    FileDerivationKind,
    UnknownFileDerivationKindError,
    normalize_derivation_payload,
    resolve_file_lineage,
)


def test_runtime_vocabulary_matches_both_migration_layouts() -> None:
    # The LATEST vocabulary migration must stay in lockstep with the enum.
    sql = get_migration_sql("021_pdf_conversion_derivation_kind.sql")
    arrays = re.findall(r"ARRAY\[(.*?)\]\s*\)", sql, flags=re.DOTALL)

    assert len(arrays) == 2
    for array in arrays:
        migration_kinds = set(re.findall(r"'([a-z_]+)'::text", array))
        assert migration_kinds == FILE_DERIVATION_KINDS


def test_legacy_metadata_lineage_is_promoted() -> None:
    lineage = resolve_file_lineage(
        parent_file_id=None,
        derivation_kind=None,
        metadata={
            "parent_file_id": "parent-1",
            "derivation_kind": "pdf_page_selection",
        },
    )

    assert lineage.parent_file_id == "parent-1"
    assert lineage.derivation_kind is FileDerivationKind.PDF_PAGE_SELECTION


def test_conflicting_lineage_is_rejected() -> None:
    with pytest.raises(ValueError, match="Conflicting derivation_kind"):
        resolve_file_lineage(
            parent_file_id="parent-1",
            derivation_kind="cropped",
            metadata={
                "parent_file_id": "parent-1",
                "derivation_kind": "rotated",
            },
        )


def test_parent_requires_registered_derivation_kind() -> None:
    with pytest.raises(ValueError, match="parent_file_id requires derivation_kind"):
        resolve_file_lineage(
            parent_file_id="parent-1",
            derivation_kind=None,
            metadata=None,
        )


def test_unknown_kind_is_rejected_by_db_payload_guard() -> None:
    with pytest.raises(UnknownFileDerivationKindError, match="future_kind"):
        normalize_derivation_payload({"derivation_kind": "future_kind"})
