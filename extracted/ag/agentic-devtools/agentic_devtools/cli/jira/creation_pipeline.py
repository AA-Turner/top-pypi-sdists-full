"""Provider-neutral topological creation pipeline (issue #2118).

This module owns the provider-neutral orchestration that loads and validates a
JSON epic-tree definition, resolves a dependency-safe topological order across
the combined hierarchy-and-blocking graph, and drives issue creation and
blocking-relationship establishment through the shared ``IssueProvider``
adapter contract.

The public entry point is :func:`run_creation_pipeline`, which returns an
:class:`~agentic_devtools.adapters.operation_plan.OperationPlan` capturing every
planned or executed operation.  The CLI boundary
(:func:`~agentic_devtools.cli.jira.tree_mode_commands.create_epic_tree`)
delegates to this function and discards the result to preserve its ``-> None``
contract.

Two structured error types are exposed:

- :class:`PipelineValidationError` — raised for any preflight failure (malformed
  input, path traversal, unsupported issue type, invalid hierarchy pair, missing
  provider capability, dependency cycle, or unsupported ``start_from``).  No
  provider mutation is ever requested when this is raised.
- :class:`PipelineExecutionError` — raised when an adapter mutation fails.  It
  carries the underlying cause, the failing operation type and canonical refs,
  the failing stage, any partial created result, and the partial
  :class:`OperationPlan` captured up to the point of failure.  Credentials are
  redacted from its message (NFR-004).  No rollback is attempted.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from agentic_devtools.adapters.exceptions import AdapterValidationError, HierarchyLinkError
from agentic_devtools.adapters.factory import get_issue_provider, resolve_provider_name
from agentic_devtools.adapters.issue_provider import HierarchyValidationProvider
from agentic_devtools.adapters.operation_plan import OperationDescriptor, OperationPlan
from agentic_devtools.adapters.orchestration_key import generate_orchestration_key
from agentic_devtools.epic_tree import (
    ConfigError,
    EpicTree,
    EpicTreeLoadError,
    IssueNode,
    VersionMismatchError,
    build_combined_graph,
    build_dependency_graph,
    creation_sequence,
    detect_cycles,
    load_epic_tree,
    topological_sort_graph,
)

if TYPE_CHECKING:  # pragma: no cover
    from agentic_devtools.adapters.issue_provider import ProviderIssueResult


# ---------------------------------------------------------------------------
# Credential redaction (NFR-004)
# ---------------------------------------------------------------------------

# Patterns for common secret material that must never leak into an error
# message surfaced to a user or log.  Matches are replaced with a fixed marker.
_SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"gho_[A-Za-z0-9]{20,}"),
    re.compile(r"ghs_[A-Za-z0-9]{20,}"),
    re.compile(r"ghu_[A-Za-z0-9]{20,}"),
    re.compile(r"ghr_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._\-]+"),
    re.compile(r"(?i)\bbasic\s+[A-Za-z0-9+/=]+"),
    re.compile(r"(?i)\bauthorization\b\s*[:=]\s*\S+"),
    re.compile(r"(?i)\b(?:api[_-]?key|token|secret|password|passwd|pwd)\b\s*[:=]\s*\S+"),
)

_REDACTION_MARKER = "[REDACTED]"


def _redact(text: str) -> str:
    """Return *text* with credential-like substrings replaced (NFR-004)."""
    redacted = text
    for pattern in _SECRET_PATTERNS:
        redacted = pattern.sub(_REDACTION_MARKER, redacted)
    return redacted


# ---------------------------------------------------------------------------
# Structured errors
# ---------------------------------------------------------------------------


class PipelineValidationError(Exception):
    """Raised when preflight validation fails before any provider mutation.

    Attributes:
        message: Human-readable description of the validation failure.  Equal to
            ``str(error)``.
        cause: The originating exception when this error wraps another, or
            ``None`` when raised directly.
    """

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.cause = cause


class PipelineExecutionError(Exception):
    """Raised when an adapter mutation fails during execution.

    The pipeline stops after the first failure and performs no rollback.  All
    captured state up to the failure is preserved on this error so callers can
    inspect what succeeded.

    Attributes:
        cause: The underlying adapter exception that triggered the failure.
        operation_type: The failing operation type (``"create_issue"`` or
            ``"add_blocked_by"``).
        refs: The canonical refs identifying the failing operation.
        stage: A short machine-readable label for the failing stage.
        created_result: The partial :class:`ProviderIssueResult` when the
            failure was a partial hierarchy-link failure, else ``None``.
        partial_plan: The :class:`OperationPlan` captured up to (and including
            any partial-created descriptor for) the failure.
        message: Human-readable, credential-redacted failure description.
    """

    def __init__(
        self,
        *,
        cause: Exception,
        operation_type: str,
        refs: tuple[str, ...],
        stage: str,
        created_result: ProviderIssueResult | None,
        partial_plan: OperationPlan,
    ) -> None:
        self.cause = cause
        self.operation_type = operation_type
        self.refs = tuple(refs)
        self.stage = stage
        self.created_result = created_result
        self.partial_plan = partial_plan
        message = (
            f"Creation pipeline failed during {operation_type} operation "
            f"(stage={stage}) for refs {self.refs}: {_redact(str(cause))}"
        )
        self.message = message
        super().__init__(message)


# ---------------------------------------------------------------------------
# Internal preflight context
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _NodeMeta:
    """Resolved metadata for a single tree node used during execution."""

    node: IssueNode
    parent_ref: str | None
    issue_type: str


@dataclass(frozen=True)
class _PreflightContext:
    """Validated inputs produced by :func:`_run_preflight`."""

    tree: EpicTree
    provider: HierarchyValidationProvider
    provider_name: str
    node_index: dict[str, _NodeMeta] = field(default_factory=dict)


_JIRA_TYPE_ALIASES = {
    "initiative": "epic",
    "story": "feature",
    "sub-task": "subtask",
}


def _effective_issue_type(node: IssueNode, provider_name: str) -> str:
    """Return the node's effective, provider-neutral issue type.

    ``load_epic_tree`` normalization guarantees ``issueType`` is populated
    (explicitly or loader-derived) for every node.
    """
    raw = (node.issueType or "").lower().strip()
    if provider_name == "jira":
        return _JIRA_TYPE_ALIASES.get(raw, raw)
    return raw


def _build_node_index(tree: EpicTree, provider_name: str = "github") -> dict[str, _NodeMeta]:
    """Build a ref → :class:`_NodeMeta` map for every node in *tree*."""
    index: dict[str, _NodeMeta] = {}
    epic = tree.epic
    index[epic.ref] = _NodeMeta(node=epic, parent_ref=None, issue_type=_effective_issue_type(epic, provider_name))
    for feature in epic.features:
        index[feature.ref] = _NodeMeta(
            node=feature, parent_ref=epic.ref, issue_type=_effective_issue_type(feature, provider_name)
        )
        for subtask in feature.subtasks:
            index[subtask.ref] = _NodeMeta(
                node=subtask, parent_ref=feature.ref, issue_type=_effective_issue_type(subtask, provider_name)
            )
    return index


def _is_contained(child: Path, root: Path) -> bool:
    """Return True when *child* is *root* itself or nested beneath it."""
    try:
        child.relative_to(root)
        return True
    except ValueError:
        return False


# ---------------------------------------------------------------------------
# Preflight
# ---------------------------------------------------------------------------


def _run_preflight(
    repo_path: Path,
    file_path: Path,
    *,
    provider: str | None = None,
    start_from: str | None = None,
) -> _PreflightContext:
    """Run the single, mutation-free preflight gate (NFR-002).

    Performs, in order: ``start_from`` support check, canonical real-path
    containment validation, provider-name resolution, single-loader
    load/validate with cycle-check deferred, provider construction, capability
    verification, and provider-contract issue-type and hierarchy-pair checks.

    Raises:
        PipelineValidationError: On any validation failure.  No provider
            mutation is requested before this method completes.
    """
    if start_from is not None:
        raise PipelineValidationError("start_from resumption is not supported yet; start_from must be None.")

    repo_path = Path(repo_path)
    file_path = Path(file_path)

    try:
        real_repo = repo_path.resolve(strict=True)
    except OSError as exc:
        raise PipelineValidationError(f"Repository root could not be resolved: {repo_path}", cause=exc) from exc
    if not real_repo.is_dir():
        raise PipelineValidationError(f"Repository root is not a directory: {repo_path}")

    try:
        real_file = file_path.resolve(strict=True)
    except OSError as exc:
        raise PipelineValidationError(f"Definition file could not be resolved: {file_path}", cause=exc) from exc

    if not _is_contained(real_file, real_repo):
        raise PipelineValidationError(
            f"Definition file {real_file} escapes the repository root {real_repo}; path traversal is not permitted."
        )

    try:
        provider_name = resolve_provider_name(real_repo, provider=provider)
    except ConfigError as exc:
        raise PipelineValidationError(f"Provider resolution failed: {exc}", cause=exc) from exc

    try:
        tree = load_epic_tree(
            real_file,
            config_path=real_repo,
            provider=provider_name,
            skip_cycle_check=True,
        )
    except (
        EpicTreeLoadError,
        ConfigError,
        VersionMismatchError,
        FileNotFoundError,
        json.JSONDecodeError,
        OSError,
        ValueError,
    ) as exc:
        raise PipelineValidationError(f"Failed to load epic-tree definition: {exc}", cause=exc) from exc

    try:
        issue_provider = get_issue_provider(real_repo, provider=provider_name)
    except ConfigError as exc:
        raise PipelineValidationError(f"Provider construction failed: {exc}", cause=exc) from exc
    if not isinstance(issue_provider, HierarchyValidationProvider):
        raise PipelineValidationError(
            f"Provider {provider_name!r} does not support hierarchy validation "
            "(HierarchyValidationProvider capability required)."
        )

    node_index = _build_node_index(tree, provider_name)

    try:
        for meta in node_index.values():
            issue_provider.validate_issue_type(meta.issue_type)
        for meta in node_index.values():
            if meta.parent_ref is None:
                continue
            parent_meta = node_index[meta.parent_ref]
            issue_provider.validate_hierarchy_pair(meta.issue_type, parent_meta.issue_type)
    except AdapterValidationError as exc:
        raise PipelineValidationError(str(exc), cause=exc) from exc

    return _PreflightContext(
        tree=tree,
        provider=issue_provider,
        provider_name=provider_name,
        node_index=node_index,
    )


# ---------------------------------------------------------------------------
# Ordering
# ---------------------------------------------------------------------------


def _build_execution_order(context: _PreflightContext) -> list[str]:
    """Return the deterministic dependency-safe creation order of node refs.

    Builds the combined hierarchy-and-blocking precedence graph, aggregates and
    reports *every* cycle, and computes a deterministic topological order using
    creation-sequence positions as the sole tie-breaker.

    Raises:
        PipelineValidationError: If the combined graph contains any cycle.  The
            message lists every detected cycle (FR-003).
    """
    graph = build_combined_graph(context.tree)
    cycles = detect_cycles(graph)
    if cycles:
        rendered = "; ".join(" \u2192 ".join(cycle) for cycle in cycles)
        raise PipelineValidationError(f"Definition contains dependency cycle(s) and cannot be ordered: {rendered}")
    return [node.ref for node in topological_sort_graph(graph, creation_sequence(context.tree))]


# ---------------------------------------------------------------------------
# Issue creation
# ---------------------------------------------------------------------------


def _create_issue_operations(
    context: _PreflightContext,
    ordered_refs: list[str],
    *,
    dry_run: bool = False,
) -> tuple[dict[str, str], list[OperationDescriptor]]:
    """Create (or plan) issues in dependency-safe order (FR-006, FR-008).

    Passes each already-created parent's provider identifier to child creation
    so hierarchy links are established during creation.  In dry-run mode no
    provider mutation occurs and planning descriptors are built from canonical
    refs.

    Returns:
        A ``(ref_to_id, descriptors)`` tuple.  ``ref_to_id`` maps each node ref
        to its provider identifier (empty in dry-run mode).

    Raises:
        PipelineExecutionError: On the first adapter failure.  Any partial
            hierarchy-link failure is captured as a ``partial-created``
            descriptor before raising.
    """
    ref_to_id: dict[str, str] = {}
    descriptors: list[OperationDescriptor] = []

    for ref in ordered_refs:
        meta = context.node_index[ref]
        node = meta.node
        labels = list(node.labels) if node.labels else None

        parent_id: str | None = None
        if meta.parent_ref is not None and not dry_run:
            parent_id = ref_to_id.get(meta.parent_ref)

        provider_params: dict[str, object] = {
            "title": node.title,
            "issue_type": meta.issue_type,
            "labels": labels,
            "parent_ref": meta.parent_ref,
        }
        key = generate_orchestration_key("create_issue", ref)

        try:
            result = context.provider.create_issue(  # type: ignore[attr-defined]
                node.title,
                node.body,
                meta.issue_type,
                parent_id=parent_id,
                labels=labels,
                dry_run=dry_run,
            )
        except HierarchyLinkError as exc:
            descriptors.append(
                OperationDescriptor(
                    operation_type="create_issue",
                    orchestration_key=key,
                    refs=(ref,),
                    status="partial-created",
                    provider_params=provider_params,
                    result=exc.created_result,
                )
            )
            partial_plan = OperationPlan(operations=tuple(descriptors), dry_run=dry_run, check_existing=False)
            raise PipelineExecutionError(
                cause=exc.cause,
                operation_type="create_issue",
                refs=(ref,),
                stage=exc.stage,
                created_result=exc.created_result,
                partial_plan=partial_plan,
            ) from None
        except Exception as exc:
            partial_plan = OperationPlan(operations=tuple(descriptors), dry_run=dry_run, check_existing=False)
            raise PipelineExecutionError(
                cause=exc,
                operation_type="create_issue",
                refs=(ref,),
                stage="create_issue",
                created_result=None,
                partial_plan=partial_plan,
            ) from None

        status = "dry-run" if dry_run else result.status
        descriptors.append(
            OperationDescriptor(
                operation_type="create_issue",
                orchestration_key=key,
                refs=(ref,),
                status=status,
                provider_params=provider_params,
                result=None if dry_run else result,
            )
        )
        if not dry_run:
            ref_to_id[ref] = result.identifier

    return ref_to_id, descriptors


# ---------------------------------------------------------------------------
# Blocking relationships
# ---------------------------------------------------------------------------


def _blocking_operations(
    context: _PreflightContext,
    ref_to_id: dict[str, str],
    *,
    dry_run: bool = False,
    prior_operations: tuple[OperationDescriptor, ...] = (),
) -> list[OperationDescriptor]:
    """Establish (or plan) declared blocking relationships (FR-009).

    Iterates the deduplicated blocking graph in deterministic
    ``(blocker_ref, blocked_ref)`` lexicographic order (NFR-001).  Complementary
    ``blocks``/``blockedBy`` declarations collapse to exactly one provider call
    and one descriptor.  Canonical descriptor refs are recorded as
    ``(blocked_ref, blocker_ref)``.

    Args:
        prior_operations: Descriptors already captured earlier in the run;
            included in any partial plan on failure.

    Raises:
        PipelineExecutionError: On the first adapter failure.
    """
    graph = build_dependency_graph(context.tree)
    edges = sorted(
        (blocker_ref, blocked_ref) for blocker_ref, blocked_refs in graph.items() for blocked_ref in blocked_refs
    )

    descriptors: list[OperationDescriptor] = []
    for blocker_ref, blocked_ref in edges:
        key = generate_orchestration_key("add_blocked_by", blocked_ref, blocker_ref)
        provider_params: dict[str, object] = {
            "blocked_ref": blocked_ref,
            "blocker_ref": blocker_ref,
        }

        if dry_run:
            descriptors.append(
                OperationDescriptor(
                    operation_type="add_blocked_by",
                    orchestration_key=key,
                    refs=(blocked_ref, blocker_ref),
                    status="dry-run",
                    provider_params=provider_params,
                    result=None,
                )
            )
            continue

        blocked_id = ref_to_id[blocked_ref]
        blocker_id = ref_to_id[blocker_ref]
        try:
            result = context.provider.add_blocked_by(blocked_id, blocker_id)  # type: ignore[attr-defined]
        except Exception as exc:
            all_ops = tuple(prior_operations) + tuple(descriptors)
            partial_plan = OperationPlan(operations=all_ops, dry_run=dry_run, check_existing=False)
            raise PipelineExecutionError(
                cause=exc,
                operation_type="add_blocked_by",
                refs=(blocked_ref, blocker_ref),
                stage="add_blocked_by",
                created_result=None,
                partial_plan=partial_plan,
            ) from None

        descriptors.append(
            OperationDescriptor(
                operation_type="add_blocked_by",
                orchestration_key=key,
                refs=(blocked_ref, blocker_ref),
                status=result.status,
                provider_params=provider_params,
                result=result,
            )
        )

    return descriptors


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def run_creation_pipeline(
    repo_path: Path,
    file_path: Path,
    *,
    provider: str | None = None,
    start_from: str | None = None,
    dry_run: bool = False,
) -> OperationPlan:
    """Load, validate, order, and execute an epic-tree creation plan.

    This is the provider-neutral extension boundary.  It runs a single
    mutation-free preflight gate, computes a deterministic dependency-safe
    order, then creates issues and establishes blocking relationships through
    the shared adapter contract, capturing every operation in the returned
    :class:`OperationPlan`.

    Args:
        repo_path: Absolute path to the repository root.  Used for loader
            containment validation and provider construction.
        file_path: Path to the JSON definition file to load and canonicalize.
        provider: Optional provider-name override; resolved via
            ``resolve_provider_name`` when ``None``.
        start_from: Reserved for a future resumption slice; must be ``None``.
        dry_run: When ``True``, run full preflight but suppress all provider
            mutations and return planning descriptors only.

    Returns:
        An :class:`OperationPlan` with ``check_existing=False`` capturing every
        planned or executed operation in deterministic order.

    Raises:
        PipelineValidationError: On any preflight failure (no mutation
            requested).
        PipelineExecutionError: On the first adapter failure during execution.
    """
    context = _run_preflight(repo_path, file_path, provider=provider, start_from=start_from)
    ordered_refs = _build_execution_order(context)
    ref_to_id, create_operations = _create_issue_operations(context, ordered_refs, dry_run=dry_run)
    blocking_operations = _blocking_operations(
        context,
        ref_to_id,
        dry_run=dry_run,
        prior_operations=tuple(create_operations),
    )
    operations = tuple(create_operations) + tuple(blocking_operations)
    return OperationPlan(operations=operations, dry_run=dry_run, check_existing=False)
