"""Epic-tree document validation against the JSON Schema and semantic rules."""

from __future__ import annotations

import re
from typing import Any

from jsonschema import Draft201909Validator

from .config import EpicTreeConfig
from .errors import (
    CATEGORY_CYCLE_DETECTED,
    CATEGORY_DEPTH_EXCEEDED,
    CATEGORY_DISALLOWED_ISSUE_TYPE,
    CATEGORY_DISALLOWED_LABEL,
    CATEGORY_DUPLICATE_REF,
    CATEGORY_INVALID_REF_FORMAT,
    CATEGORY_MISSING_BODY_SECTION,
    CATEGORY_UNRESOLVED_REFERENCE,
    EpicTreeValidationError,
    ValidationReport,
    VersionMismatchError,
)
from .schema import load_schema

_REF_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")


def _to_json_pointer(path_parts: list) -> str:
    """Convert a sequence of path components to an RFC 6901 JSON Pointer.

    Special characters ``~`` and ``/`` within individual components are
    escaped as ``~0`` and ``~1`` respectively.
    """
    if not path_parts:
        return ""
    escaped = []
    for part in path_parts:
        s = str(part)
        s = s.replace("~", "~0").replace("/", "~1")
        escaped.append(s)
    return "/" + "/".join(escaped)


def validate_epic_tree(
    document: Any,
    config: EpicTreeConfig | None = None,
    *,
    skip_cycle_check: bool = False,
) -> ValidationReport:
    """Validate an epic-tree document against the schema and semantic rules.

    Performs structural JSON Schema validation followed by semantic checks
    (ref uniqueness, ref format, depth, dependency resolution, config rules).

    Args:
        document: Parsed epic-tree JSON document.
        config: Optional configuration for validation rules.
        skip_cycle_check: When ``True``, the dependency validation pass omits
            blocking-cycle detection while still reporting unresolved
            references.  Callers deferring cycle detection to a combined graph
            use this to avoid duplicate cycle reporting.

    Returns:
        A :class:`ValidationReport` with all schema errors aggregated, or (in a
        schema-valid document) all semantic errors aggregated.
    """
    if config is None:
        config = EpicTreeConfig()

    report = ValidationReport()

    # Pass 1: JSON Schema structural validation
    schema = load_schema()
    validator = Draft201909Validator(schema)
    schema_errors: list[EpicTreeValidationError] = []

    for error in sorted(validator.iter_errors(document), key=lambda e: list(e.absolute_path)):
        path = _to_json_pointer(list(error.absolute_path))
        property_name: str | None = None

        if error.validator == "required":
            property_name = (getattr(error, "params", None) or {}).get("property")
            if property_name is None:
                _match = re.match(r"'([^']+)' is a required property", error.message)
                if _match:
                    property_name = _match.group(1)
            if property_name is None:
                for field in error.validator_value:
                    if field not in error.instance:
                        property_name = field
                        break
        elif error.validator == "additionalProperties":
            additional = set(error.instance.keys()) - set(error.schema.get("properties", {}).keys())
            if additional:
                property_name = sorted(additional)[0]

        schema_errors.append(
            EpicTreeValidationError(
                path=path,
                message=error.message,
                keyword=error.validator,
                property_name=property_name,
            )
        )

    # If schema validation failed, semantic checks may not be meaningful
    if schema_errors:
        for err in schema_errors:
            report.add_error(
                category=err.keyword,
                message=err.message,
                paths=[err.path],
                property_name=err.property_name,
            )
        report.sort_entries()
        return report

    # Pass 2: Semantic validation on structurally valid document
    epic = document.get("epic", {})
    if not isinstance(epic, dict):
        report.sort_entries()
        return report

    # Collect all nodes with paths
    all_nodes: list[tuple[dict, str, int]] = []  # (node, dot_path, depth)
    _collect_all_nodes(epic, "epic", 0, all_nodes)

    # Check ref format
    _check_ref_format(all_nodes, report)

    # Check ref uniqueness
    _check_ref_uniqueness(all_nodes, report)

    # Check depth constraints
    _check_depth(all_nodes, config, report)

    # Check config-driven rules (labels, issue types, body sections)
    _check_config_rules(all_nodes, config, report)

    # Check dependency references and cycles
    _check_dependencies(all_nodes, report, skip_cycle_check=skip_cycle_check)

    report.sort_entries()
    return report


def _collect_all_nodes(
    node: dict,
    path: str,
    depth: int,
    result: list[tuple[dict, str, int]],
) -> None:
    """Recursively collect all nodes with their dot-notation paths and depths."""
    result.append((node, path, depth))

    if depth == 0:
        for i, feature in enumerate(node.get("features", [])):
            if isinstance(feature, dict):
                _collect_all_nodes(feature, f"{path}.features[{i}]", depth + 1, result)
    elif depth == 1:
        for i, subtask in enumerate(node.get("subtasks", [])):
            if isinstance(subtask, dict):
                _collect_all_nodes(
                    subtask,
                    f"{path}.subtasks[{i}]",
                    depth + 1,
                    result,
                )


def _check_ref_format(
    nodes: list[tuple[dict, str, int]],
    report: ValidationReport,
) -> None:
    """Check all refs match the required pattern."""
    for node, path, _depth in nodes:
        ref = node.get("ref")
        if isinstance(ref, str) and not _REF_PATTERN.match(ref):
            report.add_error(
                category=CATEGORY_INVALID_REF_FORMAT,
                message=f"Ref '{ref}' does not match pattern ^[a-zA-Z0-9_-]+$",
                paths=[path],
            )


def _check_ref_uniqueness(
    nodes: list[tuple[dict, str, int]],
    report: ValidationReport,
) -> None:
    """Check that all refs are unique across the tree."""
    ref_locations: dict[str, list[str]] = {}
    for node, path, _depth in nodes:
        ref = node.get("ref")
        if isinstance(ref, str):
            if ref not in ref_locations:
                ref_locations[ref] = []
            ref_locations[ref].append(path)

    for ref_value, paths in ref_locations.items():
        if len(paths) > 1:
            report.add_error(
                category=CATEGORY_DUPLICATE_REF,
                message=f"Duplicate ref '{ref_value}'",
                paths=paths,
            )


def _check_depth(
    nodes: list[tuple[dict, str, int]],
    config: EpicTreeConfig,
    report: ValidationReport,
) -> None:
    """Check that no node exceeds the configured max depth."""
    for node, path, depth in nodes:
        if depth >= config.max_depth:
            ref = node.get("ref", "<unknown>")
            report.add_error(
                category=CATEGORY_DEPTH_EXCEEDED,
                message=f"Node '{ref}' at depth {depth} exceeds max depth {config.max_depth - 1}",
                paths=[path],
            )


def _check_config_rules(
    nodes: list[tuple[dict, str, int]],
    config: EpicTreeConfig,
    report: ValidationReport,
) -> None:
    """Check config-driven validation rules (labels, issue types, body sections)."""
    for node, path, depth in nodes:
        ref = node.get("ref", "<unknown>")

        # Check allowed labels.
        # When labels are absent from the node, normalization will auto-derive
        # them from config.default_labels, so we validate those derived values
        # too rather than skipping the check silently.
        if depth in config.allowed_labels:
            allowed = config.allowed_labels[depth]
            raw_labels = node.get("labels")
            if raw_labels is None:
                node_labels: list[str] = list(config.default_labels.get(depth, []))
            elif isinstance(raw_labels, (list, tuple)):
                node_labels = list(raw_labels)
            else:
                node_labels = raw_labels
            if isinstance(node_labels, list):
                for label in node_labels:
                    if label not in allowed:
                        msg = f"Label '{label}' on node '{ref}' not in allowed labels for depth {depth}: {allowed}"
                        report.add_error(
                            category=CATEGORY_DISALLOWED_LABEL,
                            message=msg,
                            paths=[path],
                        )

        # Check allowed issue types.
        # When issueType is absent/None, normalization will auto-derive it from
        # config.default_issue_types, so we validate the effective value instead
        # of silently skipping the allowlist check.
        if depth in config.allowed_issue_types:
            allowed_types = config.allowed_issue_types[depth]
            issue_type = node.get("issueType")
            if issue_type is None:
                issue_type = config.default_issue_types.get(depth)
            if issue_type is not None and issue_type not in allowed_types:
                msg = (
                    f"Issue type '{issue_type}' on node '{ref}' not in allowed types for depth {depth}: {allowed_types}"
                )
                report.add_error(
                    category=CATEGORY_DISALLOWED_ISSUE_TYPE,
                    message=msg,
                    paths=[path],
                )

        # Check required body sections
        if depth in config.required_body_sections:
            required_sections = config.required_body_sections[depth]
            body = node.get("body", "")
            if isinstance(body, str):
                for section in required_sections:
                    # Check for markdown heading
                    if f"# {section}" not in body and f"## {section}" not in body:
                        report.add_error(
                            category=CATEGORY_MISSING_BODY_SECTION,
                            message=f"Node '{ref}' missing required body section '{section}' for depth {depth}",
                            paths=[path],
                        )


def _check_dependencies(
    nodes: list[tuple[dict, str, int]],
    report: ValidationReport,
    *,
    skip_cycle_check: bool = False,
) -> None:
    """Check dependency references exist and detect cycles.

    When *skip_cycle_check* is ``True`` the unresolved-reference checks still
    run but the cycle-detection pass is omitted, allowing callers to defer
    cycle detection to a combined hierarchy/blocking graph.
    """
    ref_set: set[str] = set()
    ref_to_path: dict[str, str] = {}
    for node, path, _depth in nodes:
        ref = node.get("ref")
        if isinstance(ref, str):
            ref_set.add(ref)
            ref_to_path[ref] = path

    # Check unresolved references
    graph: dict[str, set[str]] = {ref: set() for ref in ref_set}
    for node, path, _depth in nodes:
        ref = node.get("ref", "")
        for blocked_ref in node.get("blocks", []):
            if isinstance(blocked_ref, str):
                if blocked_ref not in ref_set:
                    report.add_error(
                        category=CATEGORY_UNRESOLVED_REFERENCE,
                        message=f"Ref '{blocked_ref}' in blocks of '{ref}' does not exist",
                        paths=[path],
                    )
                else:
                    graph[ref].add(blocked_ref)
        for blocker_ref in node.get("blockedBy", []):
            if isinstance(blocker_ref, str):
                if blocker_ref not in ref_set:
                    report.add_error(
                        category=CATEGORY_UNRESOLVED_REFERENCE,
                        message=f"Ref '{blocker_ref}' in blockedBy of '{ref}' does not exist",
                        paths=[path],
                    )
                else:
                    graph[blocker_ref].add(ref)

    # Always check for cycles (collect-all, no short-circuit) unless the caller
    # defers cycle detection to a combined graph.
    if skip_cycle_check:
        return
    sccs = _detect_cycles_in_graph(graph)
    for scc in sccs:
        cycle_paths = [ref_to_path[ref] for ref in scc if ref in ref_to_path]
        report.add_error(
            category=CATEGORY_CYCLE_DETECTED,
            message=f"Dependency cycle detected involving: {', '.join(scc)}",
            paths=cycle_paths,
        )


def _detect_cycles_in_graph(graph: dict[str, set[str]]) -> list[list[str]]:
    """Detect cycles using Tarjan's SCC algorithm.

    Returns a list of strongly connected components that constitute cycles.
    Each inner list is sorted for deterministic output. Only SCCs of size > 1
    or singleton nodes with a self-loop are included.
    """
    index_map: dict[str, int] = {}
    lowlink: dict[str, int] = {}
    on_stack: set[str] = set()
    stack: list[str] = []
    counter: list[int] = [0]
    sccs: list[list[str]] = []

    def strongconnect(v: str) -> None:
        index_map[v] = counter[0]
        lowlink[v] = counter[0]
        counter[0] += 1
        stack.append(v)
        on_stack.add(v)

        for w in sorted(graph.get(v, set())):
            if w not in index_map:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], index_map[w])

        if lowlink[v] == index_map[v]:
            scc: list[str] = []
            while True:
                w = stack.pop()
                on_stack.discard(w)
                scc.append(w)
                if w == v:
                    break
            # A non-trivial SCC (size > 1) is always a cycle.
            # A singleton SCC is a cycle only if the node has a self-loop.
            node_neighbors = graph.get(scc[0], set())
            if len(scc) > 1 or (len(scc) == 1 and scc[0] in node_neighbors):
                sccs.append(sorted(scc))

    for v in sorted(graph.keys()):
        if v not in index_map:
            strongconnect(v)

    return sorted(sccs)


def check_schema_version(
    document: dict,
    supported_major: int = 1,
) -> None:
    """Verify that the document's ``schemaVersion`` is compatible.

    Args:
        document: Parsed epic-tree JSON document.
        supported_major: The major version number the consumer supports.

    Raises:
        VersionMismatchError: If the document's major version does not match.
        KeyError: If ``schemaVersion`` is not present in the document.
        TypeError: If ``schemaVersion`` is not a string.
        ValueError: If ``schemaVersion`` is not parseable as major.minor.
    """
    version_str = document["schemaVersion"]
    if not isinstance(version_str, str):
        raise TypeError("schemaVersion must be a string")

    version_pattern = load_schema()["properties"]["schemaVersion"]["pattern"]
    if re.fullmatch(version_pattern, version_str) is None:
        raise ValueError("schemaVersion must match the pattern major.minor (e.g. '1.0')")

    major_str = version_str.split(".", 1)[0]
    major = int(major_str)
    if major != supported_major:
        raise VersionMismatchError(version_str, supported_major)
