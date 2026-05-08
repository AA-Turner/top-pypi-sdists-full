"""Unit tests for flowtask.parsers.syntax.checker.SyntaxChecker."""
import sys
from pathlib import Path

import orjson
import pytest

from flowtask.parsers.syntax.checker import SyntaxChecker
from flowtask.parsers.syntax.registry import ComponentSchemaRegistry


FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def fake_registry(tmp_path: Path) -> ComponentSchemaRegistry:
    """Registry backed by a minimal docs/ tree with AddDataset only."""
    components = tmp_path / "components"
    components.mkdir()
    (tmp_path / "index.json").write_bytes(orjson.dumps({
        "components": {
            "AddDataset": {
                "schema": "components/AddDataset.schema.json",
                "doc": "components/AddDataset.doc.json",
            }
        }
    }))
    (components / "AddDataset.schema.json").write_bytes(orjson.dumps({
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "title": "AddDataset",
        "properties": {"dataset": {"type": "string"}},
        "required": ["dataset"],
        "additionalProperties": False,
    }))
    return ComponentSchemaRegistry(docs_dir=tmp_path)


def test_module_import_does_not_load_taskrunner():
    """Importing SyntaxChecker must NOT trigger import of flowtask.runner."""
    # Module already imported at top of file; verify TaskRunner is absent.
    assert "flowtask.runner" not in sys.modules


@pytest.mark.asyncio
async def test_clean_task(fake_registry):
    """A valid task file produces an ok report with no issues."""
    checker = SyntaxChecker(registry=fake_registry)
    report = await checker.check_file(FIXTURES / "clean.yaml")
    assert report.ok is True
    assert report.issues == []


@pytest.mark.asyncio
async def test_parse_error(fake_registry):
    """A broken YAML file produces a report with E_PARSE."""
    checker = SyntaxChecker(registry=fake_registry)
    report = await checker.check_file(FIXTURES / "broken.yaml")
    assert report.ok is False
    assert any(i.code == "E_PARSE" for i in report.issues)


@pytest.mark.asyncio
async def test_missing_name_root_error(fake_registry):
    """A task missing the required 'name' produces E_ROOT_SCHEMA."""
    checker = SyntaxChecker(registry=fake_registry)
    content = "steps:\n  - AddDataset:\n      dataset: x\n"
    report = await checker.check_content(content, fmt="yaml")
    assert any(i.code == "E_ROOT_SCHEMA" for i in report.issues)


@pytest.mark.asyncio
async def test_unknown_component_non_strict(fake_registry):
    """Unknown component in non-strict mode → warning W_UNDOCUMENTED, report.ok True."""
    checker = SyntaxChecker(registry=fake_registry, strict=False)
    content = "name: t\nsteps:\n  - DoesNotExist:\n      foo: bar\n"
    report = await checker.check_content(content, fmt="yaml")
    assert report.ok is True
    assert any(
        i.code == "W_UNDOCUMENTED" and i.severity == "warning"
        for i in report.issues
    )


@pytest.mark.asyncio
async def test_unknown_component_strict(fake_registry):
    """Unknown component in strict mode → error E_UNKNOWN_COMPONENT, report.ok False."""
    checker = SyntaxChecker(registry=fake_registry, strict=True)
    content = "name: t\nsteps:\n  - DoesNotExist:\n      foo: bar\n"
    report = await checker.check_content(content, fmt="yaml")
    assert report.ok is False
    assert any(i.code == "E_UNKNOWN_COMPONENT" for i in report.issues)


@pytest.mark.asyncio
async def test_missing_required_attribute(fake_registry):
    """Missing required attribute → E_MISSING_ATTR with attribute name, report.ok False."""
    checker = SyntaxChecker(registry=fake_registry)
    content = "name: t\nsteps:\n  - AddDataset: {}\n"
    report = await checker.check_content(content, fmt="yaml")
    assert any(
        i.code == "E_MISSING_ATTR" and i.attribute == "dataset"
        for i in report.issues
    )
    assert report.ok is False


@pytest.mark.asyncio
async def test_unknown_attribute_warns(fake_registry):
    """Extra attribute not in schema → W_UNKNOWN_ATTR warning, report.ok True."""
    checker = SyntaxChecker(registry=fake_registry)
    content = (
        "name: t\nsteps:\n  - AddDataset:\n"
        "      dataset: x\n      typo: y\n"
    )
    report = await checker.check_content(content, fmt="yaml")
    assert any(i.code == "W_UNKNOWN_ATTR" for i in report.issues)
    assert report.ok is True


@pytest.mark.asyncio
async def test_value_type_mismatch_is_not_an_error(fake_registry):
    """Per spec §1 Non-Goals — schema says str, we pass list → no error/warning."""
    checker = SyntaxChecker(registry=fake_registry)
    content = "name: t\nsteps:\n  - AddDataset:\n      dataset: [1, 2]\n"
    report = await checker.check_content(content, fmt="yaml")
    # Type mismatches must be silently ignored.
    assert report.ok is True
    assert all(i.code != "E_TYPE" for i in report.issues)
    # No type-related issues at all.
    assert not any(
        i.code in ("E_MISSING_ATTR", "E_ROOT_SCHEMA", "E_PARSE")
        for i in report.issues
    )


@pytest.mark.asyncio
async def test_check_file_uses_fixture_directly(fake_registry):
    """check_file can be called on the fixture paths."""
    checker = SyntaxChecker(registry=fake_registry)
    report = await checker.check_file(FIXTURES / "missing_required.yaml")
    assert report.ok is False
    assert any(i.code == "E_MISSING_ATTR" for i in report.issues)


@pytest.mark.asyncio
async def test_check_file_unknown_component_fixture(fake_registry):
    """check_file on the unknown_component fixture yields W_UNDOCUMENTED."""
    checker = SyntaxChecker(registry=fake_registry, strict=False)
    report = await checker.check_file(FIXTURES / "unknown_component.yaml")
    assert any(i.code == "W_UNDOCUMENTED" for i in report.issues)


@pytest.mark.asyncio
async def test_report_has_correct_fmt_and_file(fake_registry):
    """The report's fmt and file fields must be populated correctly."""
    checker = SyntaxChecker(registry=fake_registry)
    path = FIXTURES / "clean.yaml"
    report = await checker.check_file(path)
    assert report.fmt == "yaml"
    assert report.file == str(path)
