"""Functions for generating Pydantic models from metadata schemas."""

import json
import logging
import re
import subprocess
import tempfile
from pathlib import Path

import yaml

from .utils import get_repo_root, to_snake_case_module

logger = logging.getLogger(__name__)


def _fix_enum_defaults(file_path: Path) -> None:
    """Replace string-literal defaults with enum member references.

    `datamodel-codegen` emits `] = "value"` for enum fields with defaults.
    Type checkers like pyrefly reject `Literal["value"]` as incompatible with
    the generated Enum type. This function rewrites those defaults to use the
    enum member, e.g. `] = MyEnum.value`.
    """
    content = file_path.read_text()

    # Collect all Enum classes and their members: {ClassName: {value: member_name}}
    # Handles both single-line `class Foo(Enum):` and multi-line (ruff-wrapped) forms.
    enum_class_pattern = re.compile(r"^class\s+(\w+)\(\s*Enum\s*\)\s*:", re.MULTILINE | re.DOTALL)
    enum_member_pattern = re.compile(r"^\s+(\w+)\s*=\s*\"([^\"]+)\"", re.MULTILINE)

    enum_members: dict[str, dict[str, str]] = {}
    for match in enum_class_pattern.finditer(content):
        class_name = match.group(1)
        class_start = match.start()
        next_class = re.search(r"^class \w+\(", content[class_start + 1 :], re.MULTILINE)
        block_end = (class_start + 1 + next_class.start()) if next_class else len(content)
        block = content[class_start:block_end]
        members: dict[str, str] = {}
        for m in enum_member_pattern.finditer(block):
            members[m.group(2)] = m.group(1)
        if members:
            enum_members[class_name] = members

    if not enum_members:
        return

    # Build reverse lookup: string value → list of (EnumClass, member_name)
    value_to_enums: dict[str, list[tuple[str, str]]] = {}
    for cls, members in enum_members.items():
        for value, member_name in members.items():
            value_to_enums.setdefault(value, []).append((cls, member_name))

    # Find each `] = "value"` default and look backwards in the Annotated block
    # for an enum class name to determine the correct replacement.
    default_pattern = re.compile(r'\]\s*=\s*"([^"]+)"')
    replacements: list[tuple[int, int, str]] = []
    for m in default_pattern.finditer(content):
        value = m.group(1)
        candidates = value_to_enums.get(value)
        if not candidates:
            continue
        block_start = content.rfind("Annotated[", 0, m.start())
        if block_start == -1:
            continue
        annotation_block = re.sub(r"\s+", " ", content[block_start : m.start()])
        for enum_class, member_name in candidates:
            if enum_class in annotation_block:
                replacement = f"] = {enum_class}.{member_name}"
                replacements.append((m.start(), m.end(), replacement))
                break

    if not replacements:
        return

    # Apply replacements in reverse order to preserve positions
    new_content = content
    for start, end, replacement in reversed(replacements):
        new_content = new_content[:start] + replacement + new_content[end:]

    file_path.write_text(new_content)
    logger.info(f"Fixed {len(replacements)} enum default(s) in {file_path}")


def _extract_class_blocks(
    lines: list[str],
    starts: list[tuple[str, int]],
    rebuild_start: int,
) -> list[tuple[str, str, str]]:
    """Extract class blocks as `(name, header_text, full_text)` tuples.

    `header_text` is the class definition line(s) joined into one string
    (may span multiple lines due to ruff wrapping long generics).
    """
    blocks: list[tuple[str, str, str]] = []
    for idx, (name, start) in enumerate(starts):
        end = starts[idx + 1][1] if idx + 1 < len(starts) else rebuild_start
        full_text = "\n".join(lines[start:end])
        header_lines = [lines[start]]
        if "):" not in lines[start]:
            for k in range(start + 1, end):
                header_lines.append(lines[k])
                if "):" in lines[k]:
                    break
        header_text = " ".join(header_lines)
        blocks.append((name, header_text, full_text))
    return blocks


def _fix_forward_references(file_path: Path) -> None:
    """Reorder classes so runtime dependencies are defined first.

    `datamodel-codegen` may emit classes in an order where a class uses
    another (in a base-class generic or as an enum-member default) before
    that class is defined. This performs a simple topological sort to fix
    the ordering while preserving `model_rebuild()` calls at the end.
    """
    content = file_path.read_text()
    lines = content.split("\n")

    # Locate class blocks by their starting lines
    class_def = re.compile(r"^class (\w+)\(")
    starts: list[tuple[str, int]] = []
    for i, line in enumerate(lines):
        m = class_def.match(line)
        if m:
            starts.append((m.group(1), i))

    if not starts:
        return

    # Find where model_rebuild() calls begin (they stay at the end)
    rebuild_start = len(lines)
    for i in range(len(lines) - 1, -1, -1):
        if re.match(r"\w+\.model_rebuild\(\)", lines[i]):
            rebuild_start = i
        elif lines[i].strip():
            break

    blocks = _extract_class_blocks(lines, starts, rebuild_start)

    # Only detect RUNTIME dependencies (not type annotations, which are
    # lazy strings under `from __future__ import annotations`):
    #  1. Base-class references: class name in the header (e.g. RootModel[Y])
    #  2. Enum-member defaults: "ClassName." in the body (e.g. = MyEnum.value)
    class_names = {b[0] for b in blocks}
    deps: dict[str, set[str]] = {}
    for name, header_text, full_text in blocks:
        runtime_deps: set[str] = set()
        for other in class_names:
            if other == name:
                continue
            if other in header_text or f"{other}." in full_text:
                runtime_deps.add(other)
        deps[name] = runtime_deps

    # Check whether reordering is actually needed
    order = [b[0] for b in blocks]
    needs_fix = any(order.index(dep) > i for i, name in enumerate(order) for dep in deps[name])
    if not needs_fix:
        return

    # Topological sort (DFS)
    sorted_names: list[str] = []
    visited: set[str] = set()

    def visit(name: str) -> None:
        if name in visited:
            return
        visited.add(name)
        for dep in deps.get(name, set()):
            visit(dep)
        sorted_names.append(name)

    for name in order:
        visit(name)

    # Reconstruct file
    header = "\n".join(lines[: starts[0][1]])
    block_map = {name: full_text for name, _, full_text in blocks}
    new_content = header.rstrip("\n") + "\n\n\n"
    new_content += "\n\n".join(block_map[name] for name in sorted_names)

    if rebuild_start < len(lines):
        rebuilds = "\n".join(lines[rebuild_start:])
        if rebuilds.strip():
            new_content = new_content.rstrip("\n") + "\n\n\n" + rebuilds

    new_content = new_content.rstrip("\n") + "\n"
    file_path.write_text(new_content)
    logger.info(f"Reordered classes in {file_path}")


def generate_metadata_models() -> None:
    """Generate Pydantic models from metadata schemas.

    Reads all YAML schemas from src/metadata/v0/ and generates
    corresponding Pydantic models in airbyte_connector_models/metadata/v0/.
    """
    logger.info("Generating metadata models")

    repo_root = get_repo_root()
    schema_dir = repo_root / "src" / "metadata" / "v0"
    output_dir = repo_root / "airbyte_connector_models" / "metadata" / "v0"
    output_dir.mkdir(parents=True, exist_ok=True)

    header_path = repo_root / ".header.txt"

    schema_files = sorted(schema_dir.glob("*.yaml"))

    if not schema_files:
        logger.warning(f"No schema files found in {schema_dir}")
        return

    logger.info(f"Found {len(schema_files)} metadata schema files")

    for schema_file in schema_files:
        model_name = schema_file.stem  # e.g., "ConnectorMetadataDefinitionV0"
        module_name = to_snake_case_module(schema_file.stem)
        output_file = output_dir / f"{module_name}.py"

        logger.info(f"Generating model for {schema_file.name} -> {module_name}.py")

        try:
            with schema_file.open() as f:
                schema_data = yaml.safe_load(f)

            with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as temp_file:
                json.dump(schema_data, temp_file)
                temp_schema_path = temp_file.name

            try:
                subprocess.run(
                    [
                        "datamodel-codegen",
                        "--input",
                        temp_schema_path,
                        "--output",
                        str(output_file),
                        "--input-file-type",
                        "jsonschema",
                        "--output-model-type",
                        "pydantic_v2.BaseModel",
                        "--class-name",
                        model_name,
                        "--use-standard-collections",
                        "--use-union-operator",
                        "--field-constraints",
                        "--use-annotated",
                        "--keyword-only",
                        "--disable-timestamp",
                        "--use-exact-imports",
                        "--use-double-quotes",
                        "--keep-model-order",
                        "--use-schema-description",
                        "--parent-scoped-naming",
                        "--use-title-as-name",
                        "--target-python-version",
                        "3.10",
                        "--custom-file-header-path",
                        str(header_path),
                        "--snake-case-field",
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )

                logger.info(f"Generated {output_file}")

            finally:
                Path(temp_schema_path).unlink(missing_ok=True)

        except Exception:
            logger.exception(f"Failed to generate model for {schema_file.name}")

    init_file = output_dir / "__init__.py"
    init_content = (
        "# Copyright (c) 2025 Airbyte, Inc., all rights reserved.\n\n"
        '"""Metadata models for Airbyte connectors."""\n'
    )
    init_file.write_text(init_content)

    logger.info(f"Generated {len(schema_files)} metadata models in {output_dir}")


def generate_consolidated_metadata_model() -> None:
    """Generate a single consolidated Pydantic model from bundled JSON schema.

    Reads the bundled ConnectorMetadataDefinitionV0.json and generates a single
    Python file containing all metadata model classes.
    """
    logger.info("Generating consolidated metadata model from bundled JSON")

    repo_root = get_repo_root()
    bundled_json = (
        repo_root
        / "airbyte_connector_models"
        / "metadata"
        / "v0"
        / "ConnectorMetadataDefinitionV0.json"
    )
    output_file = (
        repo_root
        / "airbyte_connector_models"
        / "metadata"
        / "v0"
        / "connector_metadata_definition_v0.py"
    )

    _generate_consolidated_model(bundled_json, output_file, "ConnectorMetadataDefinitionV0")


def generate_consolidated_registry_model() -> None:
    """Generate a single consolidated Pydantic model for registry from bundled JSON schema.

    Reads the bundled ConnectorRegistryV0.json and generates a single
    Python file containing all registry model classes.
    """
    logger.info("Generating consolidated registry model from bundled JSON")

    repo_root = get_repo_root()
    bundled_json = (
        repo_root / "airbyte_connector_models" / "metadata" / "v0" / "ConnectorRegistryV0.json"
    )
    output_file = (
        repo_root / "airbyte_connector_models" / "metadata" / "v0" / "connector_registry_v0.py"
    )

    _generate_consolidated_model(bundled_json, output_file, "ConnectorRegistryV0")


def _generate_consolidated_model(bundled_json: Path, output_file: Path, schema_name: str) -> None:
    """Internal helper to generate a consolidated model from bundled JSON.

    Args:
        bundled_json: Path to the bundled JSON schema
        output_file: Path to the output Python file
        schema_name: Name of the schema for logging
    """
    if not bundled_json.exists():
        logger.error(f"Bundled JSON not found: {bundled_json}")
        logger.error("Run 'npm run bundle-schemas' first to create the bundled JSON")
        return

    repo_root = get_repo_root()
    header_path = repo_root / ".header.txt"

    try:
        subprocess.run(
            [
                "datamodel-codegen",
                "--input",
                str(bundled_json),
                "--output",
                str(output_file),
                "--input-file-type",
                "jsonschema",
                "--output-model-type",
                "pydantic_v2.BaseModel",
                "--use-standard-collections",
                "--use-union-operator",
                "--field-constraints",
                "--use-annotated",
                "--keyword-only",
                "--disable-timestamp",
                "--use-exact-imports",
                "--use-double-quotes",
                "--keep-model-order",
                "--use-schema-description",
                "--parent-scoped-naming",
                "--use-title-as-name",
                "--target-python-version",
                "3.10",
                "--custom-file-header-path",
                str(header_path),
                "--snake-case-field",
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        logger.info(f"Generated consolidated model: {output_file}")

        # Fix enum defaults (string literals → enum members) before reordering,
        # so that the dependency graph includes enum member references.
        _fix_enum_defaults(output_file)

        # Reorder classes so dependencies (including enums used as defaults)
        # are defined before their dependents.
        _fix_forward_references(output_file)

    except subprocess.CalledProcessError as e:
        logger.exception(f"Failed to generate consolidated model for {schema_name}")
        logger.info(f"stdout: {e.stdout}")
        logger.info(f"stderr: {e.stderr}")
