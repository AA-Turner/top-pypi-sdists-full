"""File classification and specialized subtask-agent provisioning (FR-007, FR-008).

Classifies the file paths a Subtask Agent is responsible for, using a
strict precedence order:

1. The subtask's own task-specific entry in ``tasks.md`` (authoritative;
   the parent ``plan.md`` MUST NOT be used for this classification because
   it covers every sibling task and would produce an overly broad boundary).
2. A secondary source — the subtask's issue description or linked diff —
   when the planning artifact is absent or its file list is empty.
3. Exhausted sources: when neither source yields any files, the subtask is
   assigned to a general, discovery-only Subtask Agent with an initially
   empty file boundary.

Supported specialization categories are Python, Markdown, YAML, and
TypeScript (FR-007, FR-008); everything else is "unsupported or binary".
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .scopes import (
    AgentScopeLevel,
    FileBoundary,
    ScopeAgent,
    SpecializationCategory,
    make_subtask_scope,
    required_capabilities,
)

_EXTENSION_CATEGORY: dict[str, SpecializationCategory] = {
    ".py": SpecializationCategory.PYTHON,
    ".pyi": SpecializationCategory.PYTHON,
    ".md": SpecializationCategory.MARKDOWN,
    ".markdown": SpecializationCategory.MARKDOWN,
    ".yml": SpecializationCategory.YAML,
    ".yaml": SpecializationCategory.YAML,
    ".ts": SpecializationCategory.TYPESCRIPT,
    ".tsx": SpecializationCategory.TYPESCRIPT,
}


class ClassificationSource:
    """Trace-facing ``classification_source`` values (FR-012)."""

    PLANNING_ARTIFACT = "planning_artifact"
    SECONDARY_ISSUE_OR_DIFF = "secondary_issue_or_diff"
    DISCOVERY_CANDIDATE_LIST = "discovery_candidate_list"
    EXHAUSTED_SOURCES = "exhausted_sources"
    NOT_APPLICABLE = "not_applicable"


class ClassificationOutcome:
    """Trace-facing ``classification_outcome`` values (FR-012)."""

    CLASSIFIED = "classified"
    DISCOVERY_ONLY_UNCLASSIFIED = "discovery_only_unclassified"
    NOT_APPLICABLE = "not_applicable"


def classify_path(path: str) -> SpecializationCategory:
    """Classify a single repository-relative path into a specialization category."""
    lower = path.lower()
    for ext, category in _EXTENSION_CATEGORY.items():
        if lower.endswith(ext):
            return category
    return SpecializationCategory.UNSUPPORTED_OR_BINARY


@dataclass(frozen=True)
class ClassificationResult:
    """The outcome of classifying a subtask's affected files.

    Attributes:
        source: The ``ClassificationSource`` used to obtain ``paths``.
        outcome: ``CLASSIFIED`` when ``paths`` is non-empty,
            ``DISCOVERY_ONLY_UNCLASSIFIED`` when sources were exhausted.
        paths: The (possibly empty) list of classified repository-relative paths.
        by_category: Paths grouped by ``SpecializationCategory``.
    """

    source: str
    outcome: str
    paths: tuple[str, ...]
    by_category: dict[SpecializationCategory, tuple[str, ...]]

    @property
    def is_discovery_only(self) -> bool:
        return self.outcome == ClassificationOutcome.DISCOVERY_ONLY_UNCLASSIFIED


def _group_by_category(paths: tuple[str, ...]) -> dict[SpecializationCategory, tuple[str, ...]]:
    grouped: dict[SpecializationCategory, list[str]] = {}
    for path in paths:
        category = classify_path(path)
        grouped.setdefault(category, []).append(path)
    return {category: tuple(items) for category, items in grouped.items()}


# Matches a backtick-delimited token in a Markdown task entry.  The raw
# matches are post-filtered by ``_looks_like_file_path`` to exclude Python
# identifiers (e.g. ``orchestrate_hierarchy_cmd()``, ``__all__``) while
# preserving legitimate extensionless files such as ``Dockerfile``.
_BACKTICK_PATH_RE = re.compile(r"`([^`\s]+)`")

_KNOWN_EXTENSIONLESS_FILES = frozenset({"Dockerfile", "Makefile", "Jenkinsfile", "Procfile"})


def _is_repository_relative_path(token: str) -> bool:
    try:
        FileBoundary(paths=(token,))
    except ValueError:
        return False
    return True


def _looks_like_file_path(token: str) -> bool:
    """Return ``True`` iff *token* looks like a repository-relative file path.

    Tokens that contain parentheses are unconditionally rejected because they
    are Python/code identifiers (e.g. ``some_func()``).  A remaining token is
    accepted when it contains a ``/`` (path separator), a ``.`` (extension or
    dotfile prefix), or is a well-known extensionless filename.
    """
    if "(" in token or ")" in token:
        return False
    if "/" in token or "." in token or token in _KNOWN_EXTENSIONLESS_FILES:
        return _is_repository_relative_path(token)
    return False


def extract_task_entry(tasks_md_content: str, task_id: str) -> str | None:
    """Return the single task-entry line/block for ``task_id`` from ``tasks.md`` content.

    Only the line(s) beginning with the task's checkbox marker (e.g.
    ``- [ ] T001``) are returned — never the whole document — so that
    sibling tasks' file references are excluded from this subtask's
    classification (FR-007, SC-014).
    """
    pattern = re.compile(rf"^- \[[ Xx]\] {re.escape(task_id)}\b.*$", re.MULTILINE)
    match = pattern.search(tasks_md_content)
    if match is None:
        return None
    # Include indented continuation lines that belong to the same bullet.
    start = match.start()
    lines = tasks_md_content[start:].splitlines()
    entry_lines = [lines[0]]
    for line in lines[1:]:
        if line.startswith("  ") and not re.match(r"^\s*- \[", line):
            entry_lines.append(line)
        else:
            break
    return "\n".join(entry_lines)


def classify_from_planning_artifact(tasks_md_content: str, task_id: str) -> tuple[str, ...]:
    """Extract candidate file paths from a subtask's own ``tasks.md`` entry only."""
    entry = extract_task_entry(tasks_md_content, task_id)
    if not entry:
        return ()
    return tuple(dict.fromkeys(t for t in _BACKTICK_PATH_RE.findall(entry) if _looks_like_file_path(t)))


def classify_from_secondary_source(issue_description: str = "", diff_paths: tuple[str, ...] = ()) -> tuple[str, ...]:
    """Extract candidate file paths from an issue description and/or a linked diff (fallback)."""
    from_description = tuple(
        dict.fromkeys(t for t in _BACKTICK_PATH_RE.findall(issue_description) if _looks_like_file_path(t))
    )
    combined = tuple(dict.fromkeys((*from_description, *diff_paths)))
    return combined


def classify_subtask_files(
    *,
    tasks_md_content: str | None,
    task_id: str,
    issue_description: str = "",
    diff_paths: tuple[str, ...] = (),
) -> ClassificationResult:
    """Classify a subtask's affected files using the FR-007 precedence order.

    Args:
        tasks_md_content: The subtask's own ``tasks.md`` file content, or
            ``None``/empty when unavailable. This MUST be the subtask
            spec's own file — never the parent feature's ``plan.md``.
        task_id: The task identifier to extract (e.g. ``"T001"``).
        issue_description: Fallback source when the planning artifact yields
            no paths.
        diff_paths: Fallback source (linked-diff paths) when the planning
            artifact yields no paths.
    """
    planning_paths: tuple[str, ...] = ()
    if tasks_md_content:
        planning_paths = classify_from_planning_artifact(tasks_md_content, task_id)

    if planning_paths:
        return ClassificationResult(
            source=ClassificationSource.PLANNING_ARTIFACT,
            outcome=ClassificationOutcome.CLASSIFIED,
            paths=planning_paths,
            by_category=_group_by_category(planning_paths),
        )

    secondary_paths = classify_from_secondary_source(issue_description, diff_paths)
    if secondary_paths:
        return ClassificationResult(
            source=ClassificationSource.SECONDARY_ISSUE_OR_DIFF,
            outcome=ClassificationOutcome.CLASSIFIED,
            paths=secondary_paths,
            by_category=_group_by_category(secondary_paths),
        )

    return ClassificationResult(
        source=ClassificationSource.EXHAUSTED_SOURCES,
        outcome=ClassificationOutcome.DISCOVERY_ONLY_UNCLASSIFIED,
        paths=(),
        by_category={},
    )


def classify_candidate_list(candidate_paths: tuple[str, ...]) -> ClassificationResult:
    """Classify a candidate file list discovered by a discovery-only Subtask Agent.

    Used after an ``EXHAUSTED_SOURCES`` classification, once the
    discovery-only agent has inspected the repository and produced a
    non-empty candidate list (FR-007). An empty ``candidate_paths`` here
    means no candidate list could be established, and the caller MUST
    record a no-edit reduced-scope outcome rather than permitting
    unbounded edits.
    """
    if not candidate_paths:
        return ClassificationResult(
            source=ClassificationSource.EXHAUSTED_SOURCES,
            outcome=ClassificationOutcome.DISCOVERY_ONLY_UNCLASSIFIED,
            paths=(),
            by_category={},
        )
    deduped = tuple(dict.fromkeys(candidate_paths))
    return ClassificationResult(
        source=ClassificationSource.DISCOVERY_CANDIDATE_LIST,
        outcome=ClassificationOutcome.CLASSIFIED,
        paths=deduped,
        by_category=_group_by_category(deduped),
    )


def supported_categories(
    by_category: dict[SpecializationCategory, tuple[str, ...]],
) -> dict[SpecializationCategory, tuple[str, ...]]:
    """Return only the supported (non-general) categories from a grouped classification."""
    return {
        category: paths
        for category, paths in by_category.items()
        if category != SpecializationCategory.UNSUPPORTED_OR_BINARY
    }


def unsupported_paths(by_category: dict[SpecializationCategory, tuple[str, ...]]) -> tuple[str, ...]:
    """Return the unsupported/binary paths from a grouped classification."""
    return by_category.get(SpecializationCategory.UNSUPPORTED_OR_BINARY, ())


def provision_subtask_agents(issue_key: str, classification: ClassificationResult) -> tuple[ScopeAgent, ...]:
    """Create one bounded Subtask Agent for each classified file category.

    Supported categories receive their matching logical capabilities.
    Unsupported and binary paths use a general agent with no type-specific
    capabilities. Exhausted sources produce one discovery-only agent with no
    writable boundary until a candidate list is established.
    """
    if classification.is_discovery_only:
        return (
            make_subtask_scope(
                agent_id=f"subtask-{issue_key}-discovery",
                issue_key=issue_key,
                file_boundary=FileBoundary(),
                specialization=None,
                capabilities=required_capabilities(AgentScopeLevel.SUBTASK),
                discovery_only=True,
            ),
        )

    categories = tuple(sorted(classification.by_category, key=lambda category: category.value))
    agent_ids = tuple(f"subtask-{issue_key}-{category.value}" for category in categories)
    return tuple(
        make_subtask_scope(
            agent_id=agent_id,
            issue_key=issue_key,
            file_boundary=FileBoundary(classification.by_category[category]),
            specialization=category,
            capabilities=required_capabilities(AgentScopeLevel.SUBTASK, category),
            sibling_ids=tuple(sibling for sibling in agent_ids if sibling != agent_id),
        )
        for category, agent_id in zip(categories, agent_ids, strict=True)
    )
