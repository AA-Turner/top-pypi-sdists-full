"""Tests for the script-I/O BTEQ flow surfaces in CUR.

Covers:
- ``validate_script_io`` standalone helper (ScriptIoDiff structure).
- Round-trip of the ``scriptMetadata.IO`` field through the registry.
"""

from __future__ import annotations

import pytest
from snowflake_code_unit_registry import (
    CodeUnitRegistry,
    FindOptions,
    ScaiError,
    ScriptIoDiff,
    validate_script_io,
)
from snowflake_code_unit_registry.types import (
    CodeUnit,
    Files,
    Kind,
    ObjectType,
    ScriptBinding,
    ScriptIoDirection,
    ScriptIoFormat,
    ScriptIoReachability,
    ScriptMetadata,
    SourceFormat,
    SourceMetadata,
    SourcePlatform,
)


def _bteq_script(io: list[dict]) -> CodeUnit:
    return CodeUnit(
        id="script-io-1",
        kind=Kind.script,
        source=SourceMetadata.model_validate(
            {"platform": SourcePlatform.teradata, "format": SourceFormat.bteq}
        ),
        files=Files.model_validate({"source": {"path": "source/etl/daily/load_sales.btq"}}),
        scriptBindings=[ScriptBinding.model_validate({"name": "err_file", "kind": "file"})],
        scriptMetadata=ScriptMetadata.model_validate({"IO": io}),
    )


def _write_binding(name: str) -> dict:
    return {"direction": "write", "path": {"kind": "binding", "name": name}}


def test_validate_script_io_clean_when_provided_matches_declared():
    script = _bteq_script(
        [
            {
                "direction": "write",
                "format": "text",
                "formatNative": "report",
                "ordinal": 0,
                "reachability": "always",
                "path": {"kind": "binding", "name": "err_file"},
            }
        ]
    )
    diff = validate_script_io(script, [_write_binding("err_file")])
    assert isinstance(diff, ScriptIoDiff)
    assert diff.missing == []
    assert diff.extra == []
    assert diff.direction_mismatch == []


def test_validate_script_io_reports_missing_extra_and_direction_mismatch():
    script = _bteq_script(
        [
            {"direction": "write", "path": {"kind": "binding", "name": "err_file"}},
            {"direction": "read", "path": {"kind": "binding", "name": "in_file"}},
        ]
    )
    # err_file supplied with the wrong direction; in_file missing; out_file unexpected.
    diff = validate_script_io(
        script,
        [
            {"direction": "read", "path": {"kind": "binding", "name": "err_file"}},
            {"direction": "write", "path": {"kind": "binding", "name": "out_file"}},
        ],
    )
    assert diff.missing == ["binding:in_file"]
    assert diff.extra == ["binding:out_file"]
    assert diff.direction_mismatch == ["binding:err_file"]


def test_validate_script_io_accepts_dict_payload():
    """Callers may pass either a Pydantic CodeUnit or a raw dict."""
    diff = validate_script_io(
        {
            "id": "s",
            "kind": "script",
            "source": {"platform": "teradata", "format": "bteq"},
            "scriptMetadata": {
                "IO": [
                    {"direction": "read", "path": {"kind": "literal", "source": "/in/x.dat"}}
                ]
            },
        },
        [{"direction": "read", "path": {"kind": "literal", "source": "/in/x.dat"}}],
    )
    assert diff.missing == []
    assert diff.extra == []
    assert diff.direction_mismatch == []


def test_validate_script_io_errors_on_non_script_kind():
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
        validate_script_io(unit, [])
    assert "kind=script" in str(ei.value)


def test_script_metadata_round_trips(registry_dir: str):
    registry = CodeUnitRegistry.init(registry_dir)
    script = _bteq_script(
        [
            {
                "direction": "write",
                "format": "text",
                "formatNative": "report",
                "ordinal": 0,
                "reachability": "always",
                "path": {"kind": "binding", "name": "err_file"},
            }
        ]
    )
    registry.create(script)

    [loaded] = [u for u in registry.find_all(FindOptions()) if u.id == "script-io-1"]
    io = loaded.scriptMetadata.IO
    assert len(io) == 1
    entry = io[0]
    assert entry.direction == ScriptIoDirection.write
    assert entry.format == ScriptIoFormat.text
    assert entry.formatNative == "report"
    assert entry.ordinal == 0
    assert entry.reachability == ScriptIoReachability.always
    assert entry.path.name == "err_file"
