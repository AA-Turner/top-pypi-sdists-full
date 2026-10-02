"""Tests for the script-bindings BTEQ flow surfaces in CUR.

Covers:
- ``validate_bindings`` standalone helper (BindingDiff structure).
- ``FindOptions.bindings`` substitution against the new
  ``parameterizedReference`` kind.
"""

from __future__ import annotations

import pytest
from snowflake_code_unit_registry import (
    BindingDiff,
    CodeUnitRegistry,
    FindOptions,
    ScaiError,
    validate_bindings,
)
from snowflake_code_unit_registry.types import (
    CodeUnit,
    Kind,
    ObjectType,
    ScriptBinding,
    SourceFormat,
    SourceMetadata,
    SourcePlatform,
    TargetMetadata,
)


def _script_with_bindings(*pairs: tuple[str, str]) -> CodeUnit:
    return CodeUnit(
        id="script-1",
        kind=Kind.script,
        source=SourceMetadata.model_validate(
            {"platform": SourcePlatform.teradata, "format": SourceFormat.bteq}
        ),
        scriptBindings=[
            ScriptBinding.model_validate({"name": name, "kind": kind})
            for name, kind in pairs
        ],
    )


def test_validate_bindings_clean_when_provided_matches_declared():
    script = _script_with_bindings(("A", "string"), ("B", "database"))
    diff = validate_bindings(script, {"A": "x", "B": "PROD"})
    assert isinstance(diff, BindingDiff)
    assert diff.missing == []
    assert diff.extra == []
    assert diff.empty == []


def test_validate_bindings_reports_missing_extra_and_empty():
    script = _script_with_bindings(("A", "string"), ("B", "string"))
    diff = validate_bindings(script, {"A": "  ", "Z": "y"})
    assert diff.missing == ["B"]
    assert diff.extra == ["Z"]
    assert diff.empty == ["A"]


def test_validate_bindings_accepts_dict_payload():
    """Callers may pass either a Pydantic CodeUnit or a raw dict."""
    diff = validate_bindings(
        {
            "id": "s",
            "kind": "script",
            "source": {"platform": "teradata", "format": "bteq"},
            "scriptBindings": [{"name": "X", "kind": "string"}],
        },
        {"X": "v"},
    )
    assert diff.missing == []
    assert diff.extra == []
    assert diff.empty == []


def test_validate_bindings_errors_on_non_script_kind():
    unit = CodeUnit(
        id="u",
        kind=Kind.databaseObject,
        source=SourceMetadata.model_validate(
            {
                "objectType": ObjectType.table,
                "database": "DB",
                "schema": "dbo",
                "name": "T",
            }
        ),
    )
    with pytest.raises(ScaiError) as ei:
        validate_bindings(unit, {})
    assert "kind=script" in str(ei.value)


def test_find_options_bindings_substitutes_parameterized_reference(registry_dir: str):
    """A parameterizedReference CUR carries ${NAME}/<% NAME %> tokens; the
    bindings option substitutes both sides at query time."""
    registry = CodeUnitRegistry.init(registry_dir)
    pref = CodeUnit(
        id="pref-1",
        kind=Kind.parameterizedReference,
        source=SourceMetadata.model_validate(
            {
                "platform": SourcePlatform.teradata,
                "database": "${UTIL_DB_NAME}",
                "name": "error_codes",
            }
        ),
        target=TargetMetadata.model_validate(
            {"database": "<% UTIL_DB_NAME %>", "name": "error_codes"}
        ),
    )
    registry.create(pref)

    units = registry.find_all(
        FindOptions(
            bindings={
                "${UTIL_DB_NAME}": "PROD_UTIL",
                "<% UTIL_DB_NAME %>": "SC_TEST_UTIL",
            }
        )
    )
    [loaded] = [u for u in units if u.id == "pref-1"]
    assert loaded.source.database == "PROD_UTIL"
    assert loaded.target.database == "SC_TEST_UTIL"
