"""Static validation/lint for issue.md templates (``agdt-validate-templates``).

Performs static analysis of ``{{placeholder}}`` templates without rendering:

- **E001** — malformed placeholder syntax (unclosed, empty, invalid chars, stray close).
- **E002** — a registered template file is missing on disk.
- **E003** — no templates discovered (missing preset directory and/or ``preset.yml``,
  or a ``--type`` filter that matches no registered template).
- **W001** — unknown placeholder (not canonical, alias, or a declared property).
- **W002** — a required property has no corresponding placeholder.
- **W003** — the template file is empty.

The command is synchronous (no background task, no network I/O) and follows the
existing ``agdt-*`` CLI conventions. Exit code is ``0`` when no errors exist (and
no warnings when ``--strict``), ``1`` otherwise.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

from agentic_devtools.cli.config.project_config import load_project_config
from agentic_devtools.cli.issue_template._repo_paths import (
    _PRESET_DIR_RELATIVE,
    _find_repo_root,
)
from agentic_devtools.cli.issue_template.template_placeholders import (
    BASE_REQUIRED_PROPERTIES,
    CANONICAL_PLACEHOLDER_NAMES,
    PLACEHOLDER_ALIASES,
    PLACEHOLDER_RE,
)
from agentic_devtools.cli.issue_template.type_resolver import slugify_type

_OPEN = "{{"
_CLOSE = "}}"
_INNER_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
_ISSUE_TYPE_PATTERN = re.compile(r"^issue-template-(.+)\.md$")
_DEFAULT_TEMPLATE_NAME = "issue-template.md"


# ──────────────────────────────────────────────────────────────────────────────
# Data types
# ──────────────────────────────────────────────────────────────────────────────


@dataclasses.dataclass(frozen=True)
class TemplateDiagnostic:
    """A single validation finding.

    Attributes:
        level: ``"error"`` or ``"warning"``.
        code: Machine-readable code (``E001``/``E002``/``E003``/``W001``/``W002``/``W003``).
        line: 1-based line number, or ``None`` when no specific location applies.
        column: 1-based column, or ``None`` when no specific location applies.
        message: Human-readable description.
    """

    level: str
    code: str
    line: int | None
    column: int | None
    message: str


@dataclasses.dataclass(frozen=True)
class TemplateValidationResult:
    """Validation outcome for a single template file."""

    template_path: str
    diagnostics: list[TemplateDiagnostic]

    @property
    def status(self) -> str:
        """``"fail"`` if any error-level diagnostic exists, else ``"pass"``."""
        if any(diag.level == "error" for diag in self.diagnostics):
            return "fail"
        return "pass"


@dataclasses.dataclass(frozen=True)
class ValidationSummary:
    """Aggregate result across all validated templates."""

    results: list[TemplateValidationResult]
    command_diagnostics: list[TemplateDiagnostic]

    @property
    def templates_checked(self) -> int:
        """Number of template files that were validated."""
        return len(self.results)

    @property
    def error_count(self) -> int:
        """Total number of error-level diagnostics (per-template + command-level)."""
        return sum(1 for diag in self._all_diagnostics() if diag.level == "error")

    @property
    def warning_count(self) -> int:
        """Total number of warning-level diagnostics (per-template + command-level)."""
        return sum(1 for diag in self._all_diagnostics() if diag.level == "warning")

    def _all_diagnostics(self) -> list[TemplateDiagnostic]:
        diagnostics: list[TemplateDiagnostic] = list(self.command_diagnostics)
        for result in self.results:
            diagnostics.extend(result.diagnostics)
        return diagnostics


# ──────────────────────────────────────────────────────────────────────────────
# Syntax checking (FR-001, E001)
# ──────────────────────────────────────────────────────────────────────────────


def _check_line_syntax(line: str, line_no: int) -> list[TemplateDiagnostic]:
    """Detect malformed placeholders on a single line (E001)."""
    diagnostics: list[TemplateDiagnostic] = []
    index = 0
    length = len(line)
    while index < length:
        if line[index : index + 2] == _OPEN:
            close = line.find(_CLOSE, index + 2)
            if close == -1:
                diagnostics.append(
                    TemplateDiagnostic(
                        level="error",
                        code="E001",
                        line=line_no,
                        column=index + 1,
                        message="Unclosed placeholder: missing '}}'",
                    )
                )
                break
            inner = line[index + 2 : close]
            if not _INNER_RE.match(inner):
                diagnostics.append(
                    TemplateDiagnostic(
                        level="error",
                        code="E001",
                        line=line_no,
                        column=index + 1,
                        message=f"Malformed placeholder: '{{{{{inner}}}}}'",
                    )
                )
            index = close + 2
        elif line[index : index + 2] == _CLOSE:
            diagnostics.append(
                TemplateDiagnostic(
                    level="error",
                    code="E001",
                    line=line_no,
                    column=index + 1,
                    message="Stray closing delimiter: '}}' with no matching '{{'",
                )
            )
            index += 2
        else:
            index += 1
    return diagnostics


def check_syntax(content: str) -> list[TemplateDiagnostic]:
    """Return E001 diagnostics for malformed placeholders in *content*."""
    diagnostics: list[TemplateDiagnostic] = []
    for line_no, line in enumerate(content.split("\n"), start=1):
        diagnostics.extend(_check_line_syntax(line, line_no))
    return diagnostics


# ──────────────────────────────────────────────────────────────────────────────
# Placeholder extraction and unknown check (FR-002, W001)
# ──────────────────────────────────────────────────────────────────────────────


def extract_placeholders(content: str) -> list[tuple[str, int, int]]:
    """Return ``(name, line, column)`` tuples for every valid placeholder."""
    result: list[tuple[str, int, int]] = []
    for line_no, line in enumerate(content.split("\n"), start=1):
        for match in PLACEHOLDER_RE.finditer(line):
            result.append((match.group(1), line_no, match.start() + 1))
    return result


def check_unknown_placeholders(content: str, known_names: set[str]) -> list[TemplateDiagnostic]:
    """Return W001 diagnostics for placeholders not in *known_names*.

    A placeholder is known if its name (or its alias-resolved canonical name)
    appears in *known_names*.
    """
    diagnostics: list[TemplateDiagnostic] = []
    for name, line, column in extract_placeholders(content):
        resolved = PLACEHOLDER_ALIASES.get(name, name)
        if name in known_names or resolved in known_names:
            continue
        diagnostics.append(
            TemplateDiagnostic(
                level="warning",
                code="W001",
                line=line,
                column=column,
                message=f"Unknown placeholder: '{{{{{name}}}}}'",
            )
        )
    return diagnostics


# ──────────────────────────────────────────────────────────────────────────────
# Property coverage (FR-003, W002)
# ──────────────────────────────────────────────────────────────────────────────


def _property_covered(prop: str, placeholders: set[str]) -> bool:
    """Return whether *prop* is covered by any placeholder, accounting for aliases."""
    for placeholder in placeholders:
        if placeholder == prop:
            return True
        if PLACEHOLDER_ALIASES.get(placeholder, placeholder) == prop:
            return True
        if PLACEHOLDER_ALIASES.get(prop, prop) == placeholder:
            return True
    return False


def check_property_coverage(
    content: str,
    required_properties: set[str],
    template_name: str,
) -> list[TemplateDiagnostic]:
    """Return W002 diagnostics for required properties with no placeholder."""
    placeholders = {name for name, _, _ in extract_placeholders(content)}
    diagnostics: list[TemplateDiagnostic] = []
    for prop in sorted(required_properties):
        if _property_covered(prop, placeholders):
            continue
        diagnostics.append(
            TemplateDiagnostic(
                level="warning",
                code="W002",
                line=None,
                column=None,
                message=(f"Required property '{prop}' has no placeholder in template '{template_name}'"),
            )
        )
    return diagnostics


# ──────────────────────────────────────────────────────────────────────────────
# Preset directory resolution (FR-004)
# ──────────────────────────────────────────────────────────────────────────────


def resolve_preset_dir(preset_dir_arg: str | None) -> Path | None:
    """Resolve the preset directory from ``--preset-dir`` or auto-discovery.

    Priority: (1) explicit *preset_dir_arg*, (2) ``<repo_root>/.specify/presets/agdt-templates``.
    Returns ``None`` when neither an explicit argument nor a repo root is available.
    """
    if preset_dir_arg is not None:
        return Path(preset_dir_arg)
    repo_root = _find_repo_root()
    if repo_root is None:
        return None
    return repo_root / _PRESET_DIR_RELATIVE


# ──────────────────────────────────────────────────────────────────────────────
# Type-schema loading from cached project.json
# ──────────────────────────────────────────────────────────────────────────────


def _load_type_schemas(git_root: Path | None) -> dict[str, tuple[set[str], set[str]]] | None:
    """Return ``slug -> (all_property_names, required_property_names)`` or ``None``.

    Loads cached issue-type metadata from ``.agdt/config/project.json`` (written by
    ``agdt-setup``). Cached type names are slugified before use. When multiple
    project identifiers are present, entries for the same slug are unioned.
    Returns ``None`` when no ``issue_types_metadata`` is available.
    """
    config = load_project_config(git_root=git_root)
    metadata = config.get("issue_types_metadata")
    if not isinstance(metadata, dict):
        return None

    schemas: dict[str, tuple[set[str], set[str]]] = {}
    for entry in metadata.values():
        if not isinstance(entry, dict):
            continue
        issue_types = entry.get("issue_types")
        if not isinstance(issue_types, list):
            continue
        for issue_type in issue_types:
            if not isinstance(issue_type, dict):
                continue
            name = issue_type.get("name")
            if not isinstance(name, str) or not name.strip():
                continue
            slug = slugify_type(name)
            all_names, required = schemas.get(slug, (set(), set()))
            _collect_properties(issue_type.get("properties"), all_names, required)
            schemas[slug] = (all_names, required)
    return schemas


def _collect_properties(properties: Any, all_names: set[str], required: set[str]) -> None:
    """Populate *all_names*/*required* from a ``properties`` list in place."""
    if not isinstance(properties, list):
        return
    for prop in properties:
        if not isinstance(prop, dict):
            continue
        prop_name = prop.get("name")
        if not isinstance(prop_name, str) or not prop_name.strip():
            continue
        all_names.add(prop_name)
        if prop.get("required") is True and prop.get("included_in_template", True) is True:
            required.add(prop_name)


def _known_and_required(
    slug: str | None,
    schemas: dict[str, tuple[set[str], set[str]]] | None,
) -> tuple[set[str], set[str]]:
    """Resolve the known-name and required-property sets for a template *slug*."""
    known: set[str] = set(CANONICAL_PLACEHOLDER_NAMES)
    required: set[str] = set(BASE_REQUIRED_PROPERTIES)
    if slug is not None and schemas is not None and slug in schemas:
        all_names, type_required = schemas[slug]
        known |= all_names
        required |= type_required
    return known, required


# ──────────────────────────────────────────────────────────────────────────────
# Single-template validation
# ──────────────────────────────────────────────────────────────────────────────


def validate_single_template(
    template_path: Path,
    content: str,
    known_names: set[str],
    required_properties: set[str],
) -> TemplateValidationResult:
    """Validate one template's *content* into a :class:`TemplateValidationResult`.

    An empty (whitespace-only) template yields a single W003 warning and skips
    the other checks.
    """
    template_name = template_path.name
    if not content.strip():
        return TemplateValidationResult(
            template_path=str(template_path),
            diagnostics=[
                TemplateDiagnostic(
                    level="warning",
                    code="W003",
                    line=None,
                    column=None,
                    message="Template file is empty",
                )
            ],
        )

    diagnostics: list[TemplateDiagnostic] = []
    diagnostics.extend(check_syntax(content))
    diagnostics.extend(check_unknown_placeholders(content, known_names))
    diagnostics.extend(check_property_coverage(content, required_properties, template_name))
    return TemplateValidationResult(template_path=str(template_path), diagnostics=diagnostics)


def _template_type_slug(entry: str) -> str | None:
    """Return the type slug for a registered template name, or ``None`` for the default."""
    if entry == _DEFAULT_TEMPLATE_NAME:
        return None
    match = _ISSUE_TYPE_PATTERN.match(entry)
    if match:
        return match.group(1)
    return None


def _read_registered_issue_templates(preset_dir: Path) -> list[str]:
    """Return registered issue-template filenames declared in ``preset.yml``."""
    preset_file = preset_dir / "preset.yml"
    if not preset_file.exists():
        return []
    try:
        with preset_file.open(encoding="utf-8") as file_handle:
            preset_data = yaml.safe_load(file_handle)
    except (OSError, UnicodeError, yaml.YAMLError):
        return []
    if not isinstance(preset_data, dict):
        return []
    templates_value = preset_data.get("templates")
    if not isinstance(templates_value, list):
        return []

    registered: list[str] = []
    for entry in templates_value:
        if not isinstance(entry, str):
            continue
        if "/" in entry or "\\" in entry:
            continue
        if entry == _DEFAULT_TEMPLATE_NAME or _ISSUE_TYPE_PATTERN.match(entry):
            registered.append(entry)
    return registered


# ──────────────────────────────────────────────────────────────────────────────
# Orchestration
# ──────────────────────────────────────────────────────────────────────────────


def validate_all_templates(
    preset_dir: Path | None,
    type_filter: str | None = None,
    *,
    git_root: Path | None = None,
) -> ValidationSummary:
    """Discover and validate every registered issue template in *preset_dir*."""
    command_diagnostics: list[TemplateDiagnostic] = []
    results: list[TemplateValidationResult] = []

    registered = list(dict.fromkeys(_read_registered_issue_templates(preset_dir))) if preset_dir is not None else []
    if preset_dir is None or not registered:
        command_diagnostics.append(
            TemplateDiagnostic(
                level="error",
                code="E003",
                line=None,
                column=None,
                message="No templates discovered (missing preset directory and/or preset.yml)",
            )
        )
        return ValidationSummary(results=results, command_diagnostics=command_diagnostics)

    schemas = _load_type_schemas(git_root)
    templates_dir = preset_dir / "templates"
    filter_slug = slugify_type(type_filter) if type_filter is not None else None

    for entry in registered:
        slug = _template_type_slug(entry)
        if filter_slug is not None and slug != filter_slug:
            continue
        file_path = templates_dir / entry
        if not file_path.exists():
            results.append(
                TemplateValidationResult(
                    template_path=str(file_path),
                    diagnostics=[
                        TemplateDiagnostic(
                            level="error",
                            code="E002",
                            line=None,
                            column=None,
                            message=f"Registered template file not found: {file_path}",
                        )
                    ],
                )
            )
            continue
        try:
            content = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            results.append(
                TemplateValidationResult(
                    template_path=str(file_path),
                    diagnostics=[
                        TemplateDiagnostic(
                            level="error",
                            code="E002",
                            line=None,
                            column=None,
                            message=f"Template file is not a readable UTF-8 file: {file_path}",
                        )
                    ],
                )
            )
            continue
        known_names, required_properties = _known_and_required(slug, schemas)
        results.append(validate_single_template(file_path, content, known_names, required_properties))

    if filter_slug is not None and not results:
        command_diagnostics.append(
            TemplateDiagnostic(
                level="error",
                code="E003",
                line=None,
                column=None,
                message=f"No registered templates matched --type '{type_filter}'",
            )
        )

    return ValidationSummary(results=results, command_diagnostics=command_diagnostics)


def validate_file(
    file_path: Path,
    type_filter: str | None = None,
    *,
    git_root: Path | None = None,
) -> ValidationSummary:
    """Validate a single template *file_path* (``--file`` mode)."""
    if not file_path.exists():
        return ValidationSummary(
            results=[
                TemplateValidationResult(
                    template_path=str(file_path),
                    diagnostics=[
                        TemplateDiagnostic(
                            level="error",
                            code="E002",
                            line=None,
                            column=None,
                            message=f"Template file not found: {file_path}",
                        )
                    ],
                )
            ],
            command_diagnostics=[],
        )

    schemas = _load_type_schemas(git_root) if type_filter is not None else None
    filter_slug = slugify_type(type_filter) if type_filter is not None else None
    known_names, required_properties = _known_and_required(filter_slug, schemas)
    try:
        content = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ValidationSummary(
            results=[
                TemplateValidationResult(
                    template_path=str(file_path),
                    diagnostics=[
                        TemplateDiagnostic(
                            level="error",
                            code="E002",
                            line=None,
                            column=None,
                            message=f"Template file is not a readable UTF-8 file: {file_path}",
                        )
                    ],
                )
            ],
            command_diagnostics=[],
        )
    result = validate_single_template(file_path, content, known_names, required_properties)
    return ValidationSummary(results=[result], command_diagnostics=[])


# ──────────────────────────────────────────────────────────────────────────────
# Output formatting (FR-005, FR-006, FR-008)
# ──────────────────────────────────────────────────────────────────────────────


def _format_diagnostic_line(file_label: str, diag: TemplateDiagnostic) -> str:
    line_label = str(diag.line) if diag.line is not None else "-"
    column_label = str(diag.column) if diag.column is not None else "-"
    return f"{file_label}:{line_label}:{column_label}: {diag.level}: [{diag.code}] {diag.message}"


def format_human_output(summary: ValidationSummary) -> str:
    """Format *summary* as lint-style human-readable lines plus a summary line."""
    lines: list[str] = []
    for result in summary.results:
        for diag in result.diagnostics:
            lines.append(_format_diagnostic_line(result.template_path, diag))
    for diag in summary.command_diagnostics:
        lines.append(_format_diagnostic_line("-", diag))
    lines.append(
        f"Checked {summary.templates_checked} template(s): "
        f"{summary.error_count} error(s), {summary.warning_count} warning(s)"
    )
    return "\n".join(lines)


def format_json_output(summary: ValidationSummary) -> str:
    """Format *summary* as a single JSON object string."""
    payload: dict[str, Any] = {
        "summary": {
            "errors": summary.error_count,
            "warnings": summary.warning_count,
            "templates_checked": summary.templates_checked,
        },
        "results": [
            {
                "template": result.template_path,
                "status": result.status,
                "diagnostics": [_diagnostic_to_dict(diag) for diag in result.diagnostics],
            }
            for result in summary.results
        ],
        "diagnostics": [_diagnostic_to_dict(diag) for diag in summary.command_diagnostics],
    }
    return json.dumps(payload, indent=2)


def _diagnostic_to_dict(diag: TemplateDiagnostic) -> dict[str, Any]:
    return {
        "level": diag.level,
        "code": diag.code,
        "line": diag.line,
        "column": diag.column,
        "message": diag.message,
    }


def _determine_exit_code(summary: ValidationSummary, strict: bool) -> int:
    """Return ``1`` when there are errors (or warnings under *strict*), else ``0``."""
    if summary.error_count > 0:
        return 1
    if strict and summary.warning_count > 0:
        return 1
    return 0


# ──────────────────────────────────────────────────────────────────────────────
# CLI entry point (NFR-002)
# ──────────────────────────────────────────────────────────────────────────────


def validate_templates_cli() -> None:
    """Argparse entry point for ``agdt-validate-templates``."""
    parser = argparse.ArgumentParser(
        prog="agdt-validate-templates",
        description="Statically validate issue.md templates (syntax, placeholders, coverage).",
    )
    target_group = parser.add_mutually_exclusive_group()
    target_group.add_argument(
        "--file",
        type=str,
        default=None,
        help="Validate a single template file instead of the preset directory.",
    )
    target_group.add_argument(
        "--preset-dir",
        type=str,
        default=None,
        help="Preset directory to validate (default: auto-discovered from repo root).",
    )
    parser.add_argument(
        "--type",
        type=str,
        default=None,
        help="Restrict/resolve validation to a specific issue type slug.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 when any warnings exist (does not relabel warnings).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Emit a single JSON object on stdout instead of human-readable output.",
    )
    args = parser.parse_args()

    if args.file is not None:
        summary = validate_file(Path(args.file), args.type)
    else:
        preset_dir = resolve_preset_dir(args.preset_dir)
        summary = validate_all_templates(preset_dir, args.type)

    if args.json_output:
        print(format_json_output(summary))
    else:
        print(format_human_output(summary), file=sys.stderr)

    sys.exit(_determine_exit_code(summary, args.strict))
