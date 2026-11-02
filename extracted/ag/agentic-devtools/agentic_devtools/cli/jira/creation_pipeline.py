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
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, cast

from agentic_devtools.adapters.exceptions import AdapterValidationError, HierarchyLinkError
from agentic_devtools.adapters.factory import get_issue_provider, resolve_provider_name, resolve_provider_target
from agentic_devtools.adapters.issue_provider import (
    DefinitiveCreationFailure,
    HierarchyValidationProvider,
    IssueNotFoundError,
    PreCreateLookup,
    PreCreateLookupProvider,
    ProviderIssueResult,
    ProviderLinkResult,
)
from agentic_devtools.adapters.operation_plan import OperationDescriptor, OperationPlan
from agentic_devtools.adapters.orchestration_key import generate_orchestration_key
from agentic_devtools.cli.workflows.create_epic.records import (
    atomic_write_mapping_document,
    initialize_mapping_document,
    load_mapping_document,
    resolve_mapping_path,
    validate_mapping_document,
)
from agentic_devtools.cli.workflows.create_epic.registry import acquire_tree_lock
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
    migrate_schema_v1_to_v2,
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
_PENDING_RECOVERY_ATTEMPTS = 5
_PENDING_RECOVERY_DELAY_SECONDS = 0.1
_PRECREATE_SETTLING_ATTEMPTS = 5
_PRECREATE_SETTLING_INITIAL_DELAY_SECONDS = 0.1
_STALE_PENDING_THRESHOLD_MINUTES = 30
_NORMALIZED_STALE_PENDING_TIMESTAMP = "1970-01-01T00:00:00Z"


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
        operation_type: The failing operation type (``"create_issue"``,
            ``"link_subissue"``, or ``"add_blocked_by"``).
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
    provider: HierarchyValidationProvider | None
    provider_name: str
    provider_target: str | None = None
    node_index: dict[str, _NodeMeta] = field(default_factory=dict)
    mapping_document: dict[str, object] | None = None
    mapping_preexisting: bool | None = None
    mapping_path: Path | None = None
    start_from: str | None = None


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


def _extract_mapping_identifier(entry: object) -> str | None:
    """Return a stored provider identifier from a mapping entry when present."""
    identifier = (
        entry
        if isinstance(entry, str)
        else next(
            (
                entry.get(key)
                for key in ("identifier", "providerId", "provider_id", "id")
                if isinstance(entry, dict) and entry.get(key) is not None
            ),
            None,
        )
        if isinstance(entry, dict)
        else None
    )
    if not isinstance(identifier, str) or not identifier.strip():
        return None
    return identifier


def _extract_mapping_orchestration_key(entry: object) -> str | None:
    """Return a stored orchestration key from a mapping entry when present."""
    if not isinstance(entry, dict):
        return None
    for key in ("orchestrationKey", "orchestration_key"):
        orchestration_key = entry.get(key)
        if isinstance(orchestration_key, str) and orchestration_key.strip():
            return orchestration_key
    return None


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp for incremental mapping records."""
    return datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _validate_start_from_prerequisites(
    context: _PreflightContext,
    ordered_refs: list[str],
    start_index: int,
    mapped_ids: dict[str, str],
) -> None:
    """Reject unsafe resume requests whose skipped prerequisites lack mapped identifiers."""
    if start_index == 0 or context.start_from is None:
        return

    skipped_refs = set(ordered_refs[:start_index])
    missing_prerequisites = skipped_refs.difference(mapped_ids)

    if missing_prerequisites:
        rendered = ", ".join(sorted(missing_prerequisites))
        raise PipelineValidationError(
            "start_from requires verified mapped identifiers for skipped prerequisite refs: "
            f"{rendered}. Re-run from an earlier ref or restore the tree mapping first."
        )


# ---------------------------------------------------------------------------
# Preflight
# ---------------------------------------------------------------------------


def _run_preflight(
    repo_path: Path,
    file_path: Path,
    *,
    provider: str | None = None,
    start_from: str | None = None,
    load_mapping: bool = True,
    construct_provider: bool = True,
) -> _PreflightContext:
    """Run the single, mutation-free preflight gate (NFR-002).

    Performs, in order: ``start_from`` support check, canonical real-path
    containment validation, provider-name and target resolution, single-loader
    load/validate with cycle-check deferred, mapping identity validation, then
    optional provider construction, capability verification, and provider-contract
    issue-type and hierarchy-pair checks.

    Raises:
        PipelineValidationError: On any validation failure.  No provider
            mutation is requested before this method completes.
    """
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

    node_index = _build_node_index(tree, provider_name)

    try:
        provider_target = resolve_provider_target(real_repo, provider_name)
    except ConfigError as exc:
        raise PipelineValidationError(f"Provider target resolution failed: {exc}", cause=exc) from exc
    if tree.treeId is not None:
        try:
            initialize_mapping_document(tree, provider_name, provider_target)
        except ValueError as exc:
            raise PipelineValidationError(f"Provider target validation failed: {exc}", cause=exc) from exc

    if start_from is not None and start_from not in node_index:
        raise PipelineValidationError(f"start_from reference {start_from!r} does not exist in the epic tree.")
    mapping_document: dict[str, object] | None = None
    mapping_preexisting = False
    mapping_path: Path | None = None
    if tree.treeId is not None:
        mapping_path = resolve_mapping_path(tree, create=False)
        if load_mapping and mapping_path.is_file():
            try:
                mapping_document = load_mapping_document(mapping_path)
                mapping_document = validate_mapping_document(
                    mapping_document,
                    tree=tree,
                    provider_name=provider_name,
                    provider_target=provider_target,
                    allow_invalid_pending_timestamps=True,
                )
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                raise PipelineValidationError(f"Failed to load epic-create mapping document: {exc}", cause=exc) from exc
    mapping_preexisting = mapping_document is not None

    if not construct_provider:
        return _PreflightContext(
            tree=tree,
            provider=None,
            provider_name=provider_name,
            provider_target=provider_target,
            node_index=node_index,
            mapping_document=mapping_document,
            mapping_preexisting=mapping_preexisting,
            mapping_path=mapping_path,
            start_from=start_from,
        )

    try:
        issue_provider = get_issue_provider(real_repo, provider=provider_name)
    except ConfigError as exc:
        raise PipelineValidationError(f"Provider construction failed: {exc}", cause=exc) from exc
    if not isinstance(issue_provider, HierarchyValidationProvider):
        raise PipelineValidationError(
            f"Provider {provider_name!r} does not support hierarchy validation "
            "(HierarchyValidationProvider capability required)."
        )

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
        provider_target=provider_target,
        node_index=node_index,
        mapping_document=mapping_document,
        mapping_preexisting=mapping_preexisting,
        mapping_path=mapping_path,
        start_from=start_from,
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
    force_resume: bool = False,
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
    if context.provider is None:
        raise PipelineValidationError("Provider construction was not completed before issue creation.")
    ref_to_id: dict[str, str] = {}
    descriptors: list[OperationDescriptor] = []
    mapping_document = context.mapping_document
    tree_id = context.tree.treeId
    entries: dict[str, object] = {}
    if mapping_document is not None:
        entries = cast(dict[str, object], mapping_document["entries"])

    mapped_ids: dict[str, str] = {}
    mapped_results: dict[str, ProviderIssueResult] = {}
    pending_orchestration_keys: dict[str, str] = {}
    pending_promotions: dict[str, dict[str, object]] = {}
    pending_force_resumes: set[str] = set()
    precreate_lookup_results: dict[str, ProviderIssueResult | None] = {}
    mapped_identifier_owners: dict[str, str] = {}
    for ref, entry in entries.items():
        if isinstance(entry, dict):
            operation_type = entry.get("operation_type")
            status = entry.get("status")
            allowed_statuses = (
                {"pending", "confirmed"}
                if operation_type in {"link_subissue", "add_blocked_by"}
                else {"pending", "created", "trusted-match", "failed"}
            )
            if status is not None and status not in allowed_statuses:
                raise PipelineValidationError(f"Mapping entry for {ref!r} has unrecognized status {status!r}.")
            if (
                operation_type not in {"link_subissue", "add_blocked_by"}
                and status in {"created", "trusted-match"}
                and _extract_mapping_identifier(entry) is None
            ):
                raise PipelineValidationError(
                    f"Mapping entry for {ref!r} with status {status!r} requires a provider identifier."
                )
        if isinstance(entry, dict) and entry.get("operation_type") in {"link_subissue", "add_blocked_by"}:
            continue
        if isinstance(entry, dict) and entry.get("status") == "pending":
            pending_orchestration_keys[ref] = _extract_mapping_orchestration_key(entry) or (
                generate_orchestration_key("create_issue", tree_id, ref) if tree_id else ""
            )
        identifier = _extract_mapping_identifier(entry)
        if identifier is None and isinstance(entry, dict) and entry.get("status") == "pending":
            orchestration_key = pending_orchestration_keys.get(ref)
            find_existing_issue = getattr(context.provider, "find_existing_issue", None)
            if not orchestration_key or not callable(find_existing_issue):
                raise PipelineValidationError(
                    f"Pending mapping entry for {ref!r} has no safely recoverable identifier. "
                    "Restore the mapping or remove the pending entry before rerunning."
                )
            recovered: ProviderIssueResult | None = None
            try:
                for attempt in range(_PENDING_RECOVERY_ATTEMPTS):
                    recovered = find_existing_issue(orchestration_key)
                    if recovered is not None:
                        break
                    if attempt < _PENDING_RECOVERY_ATTEMPTS - 1:
                        time.sleep(_PENDING_RECOVERY_DELAY_SECONDS)
            except Exception as exc:
                raise PipelineValidationError(
                    f"Could not reconcile pending mapping entry for {ref!r}. No issue was created.",
                    cause=exc,
                ) from exc
            if recovered is None or not isinstance(recovered.identifier, str) or not recovered.identifier.strip():
                pending_since = entry.get("pending_since")
                try:
                    threshold_minutes = int(
                        os.environ.get("AGDT_STALE_LOCK_THRESHOLD_MINUTES", str(_STALE_PENDING_THRESHOLD_MINUTES))
                    )
                except ValueError as exc:
                    raise PipelineValidationError(
                        "AGDT_STALE_LOCK_THRESHOLD_MINUTES must be a positive integer."
                    ) from exc
                if threshold_minutes <= 0:
                    raise PipelineValidationError("AGDT_STALE_LOCK_THRESHOLD_MINUTES must be a positive integer.")
                malformed_timestamp = not isinstance(pending_since, str) or not pending_since.endswith("Z")
                if malformed_timestamp:
                    stale = True
                else:
                    try:
                        parsed_pending_since = datetime.fromisoformat(cast(str, pending_since)[:-1] + "+00:00")
                        if parsed_pending_since.tzinfo is None or parsed_pending_since.utcoffset() is None:
                            raise ValueError("pending timestamp must be timezone-aware")
                        now = datetime.now(UTC)
                        stale = parsed_pending_since > now or now - parsed_pending_since > timedelta(
                            minutes=threshold_minutes
                        )
                    except ValueError:
                        malformed_timestamp = True
                        stale = True
                if stale:
                    warning = (
                        f"Stale pending mapping entry for {ref!r} could represent a create that succeeded "
                        "but is not yet visible; forcing a retry risks creating a duplicate. Supply "
                        "--force-resume only if you accept this duplicate risk."
                    )
                    if not force_resume:
                        raise PipelineValidationError(warning)
                    print(warning, file=sys.stderr)
                    if malformed_timestamp and not dry_run:
                        entry["pending_since"] = _NORMALIZED_STALE_PENDING_TIMESTAMP
                    pending_force_resumes.add(ref)
                    precreate_lookup_results[ref] = None
                    continue
                raise PipelineValidationError(
                    f"Could not reconcile pending mapping entry for {ref!r} after "
                    f"{_PENDING_RECOVERY_ATTEMPTS} attempts. No issue was created."
                )
            identifier = recovered.identifier
            mapped_results[ref] = recovered
            pending_promotions[ref] = {
                "provider_id": context.provider.normalize_identifier(identifier),  # type: ignore[attr-defined]
                "status": "trusted-match",
                "match_basis": "pending-confirmation-unresolved",
            }
        if identifier is None:
            continue
        if isinstance(entry, dict):
            status = entry.get("status")
            if status == "pending":
                call_outcome = entry.get("call_outcome")
                if call_outcome not in {"created", "existing"}:
                    if ref not in pending_promotions:
                        continue
                else:
                    normalized_identifier = context.provider.normalize_identifier(identifier)  # type: ignore[attr-defined]
                    pending_promotions[ref] = {
                        "provider_id": normalized_identifier,
                        "status": "created" if call_outcome == "created" else "trusted-match",
                    }
                    if call_outcome == "existing":
                        pending_promotions[ref]["match_basis"] = "create-existing-response"
        try:
            resolved = context.provider.resolve_identifier(identifier, dry_run=False)  # type: ignore[attr-defined]
            if not isinstance(resolved, ProviderIssueResult) or not isinstance(resolved.identifier, str):
                raise TypeError("Provider returned an invalid issue resolution response.")
            if not resolved.identifier.strip():
                raise ValueError("Provider returned an empty issue identifier.")
            normalized_identifier = context.provider.normalize_identifier(resolved.identifier)  # type: ignore[attr-defined]
            if not isinstance(normalized_identifier, str) or not normalized_identifier.strip():
                raise ValueError("Provider returned an invalid normalized issue identifier.")
        except IssueNotFoundError as exc:
            raise PipelineValidationError(
                f"Mapped provider issue {identifier!r} for ref {ref!r} no longer exists; "
                "correct or remove the mapping entry before rerunning.",
                cause=exc,
            ) from exc
        except Exception as exc:
            raise PipelineValidationError(
                f"Could not resolve mapped provider issue {identifier!r} for ref {ref!r}.",
                cause=exc,
            ) from exc
        previous_ref = mapped_identifier_owners.get(normalized_identifier)
        if previous_ref is not None and previous_ref != ref:
            raise PipelineValidationError(
                f"Mapping entries {previous_ref!r} and {ref!r} resolve to the same "
                f"provider identifier {normalized_identifier!r}."
            )
        mapped_identifier_owners[normalized_identifier] = ref
        mapped_results[ref] = resolved
        mapped_ids[ref] = resolved.identifier
    ref_to_id.update(mapped_ids)

    start_index = ordered_refs.index(context.start_from) if context.start_from is not None else 0
    _validate_start_from_prerequisites(context, ordered_refs, start_index, mapped_ids)

    if pending_promotions and mapping_document is not None:
        for ref, update in pending_promotions.items():
            entries[ref] = update
        if not dry_run and context.mapping_path is not None:
            atomic_write_mapping_document(context.mapping_path, mapping_document)

    if (
        not dry_run
        and mapping_document is None
        and context.mapping_path is not None
        and context.provider_target is not None
    ):
        mapping_document = initialize_mapping_document(context.tree, context.provider_name, context.provider_target)
        atomic_write_mapping_document(context.mapping_path, mapping_document)
        object.__setattr__(context, "mapping_document", mapping_document)
        object.__setattr__(context, "mapping_preexisting", False)
        entries = cast(dict[str, object], mapping_document["entries"])

    for ref in ordered_refs[:start_index]:
        key_refs = (tree_id, ref) if tree_id else (ref,)
        key = generate_orchestration_key("create_issue", *key_refs)
        descriptors.append(
            OperationDescriptor(
                operation_type="resume_skip",
                orchestration_key=pending_orchestration_keys.get(ref, key),
                refs=(ref,),
                status="no-op",
                provider_params={},
                result=mapped_results.get(ref),
            )
        )

    if not dry_run and start_index:
        prefix_refs = set(ordered_refs[:start_index])
        prefix_links = _link_operations(
            context,
            ref_to_id,
            prior_operations=tuple(descriptors),
            only_refs=prefix_refs,
        )
        descriptors.extend(prefix_links)
        prefix_dependencies = _blocking_operations(
            context,
            ref_to_id,
            prior_operations=tuple(descriptors),
            only_refs=prefix_refs,
        )
        descriptors.extend(prefix_dependencies)

    for ref in ordered_refs[start_index:]:
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
        key_refs = (tree_id, ref) if tree_id else (ref,)
        key = generate_orchestration_key("create_issue", *key_refs)
        idempotency_key = pending_orchestration_keys.get(ref, key)
        provider_idempotency_key = idempotency_key if tree_id is not None else None

        if ref in mapped_results:
            existing = mapped_results[ref]
            descriptors.append(
                OperationDescriptor(
                    operation_type="create_issue",
                    orchestration_key=idempotency_key,
                    refs=(ref,),
                    status="existing",
                    provider_params=provider_params,
                    result=existing,
                )
            )
            continue

        legacy_orchestration_key = generate_orchestration_key("create_issue", ref) if tree_id else None
        prior_entry = entries.get(ref)
        legacy_adoption_permitted = (
            isinstance(prior_entry, dict)
            and prior_entry.get("status") == "trusted-match"
            and prior_entry.get("match_basis") == "import-legacy-mapping"
        )
        should_lookup = (
            not dry_run
            and mapping_document is not None
            and (
                ref not in entries
                or (isinstance(prior_entry, dict) and prior_entry.get("status") == "failed")
                or ref in pending_force_resumes
            )
        )
        if should_lookup and ref not in precreate_lookup_results:
            find_existing_issue = getattr(context.provider, "find_existing_issue", None)
            if not callable(find_existing_issue):
                raise PipelineValidationError(
                    f"Provider cannot safely check whether an issue already exists for ref {ref!r}; "
                    "no issue was created."
                )
            precreate_match: ProviderIssueResult | None = None
            try:
                delay = _PRECREATE_SETTLING_INITIAL_DELAY_SECONDS
                for attempt in range(_PRECREATE_SETTLING_ATTEMPTS):
                    precreate_match = find_existing_issue(idempotency_key)
                    if precreate_match is not None:
                        break
                    if attempt < _PRECREATE_SETTLING_ATTEMPTS - 1:
                        time.sleep(delay)
                        delay *= 2
            except Exception as exc:
                raise PipelineValidationError(
                    f"Could not check whether an issue already exists for ref {ref!r}; no issue was created.",
                    cause=exc,
                ) from exc
            precreate_lookup_results[ref] = precreate_match

        precreate_match = precreate_lookup_results.get(ref)
        if precreate_match is not None:
            normalized_identifier = context.provider.normalize_identifier(precreate_match.identifier)  # type: ignore[attr-defined]
            previous_ref = mapped_identifier_owners.get(normalized_identifier)
            if previous_ref is not None and previous_ref != ref:
                raise PipelineValidationError(
                    f"Mapping entries {previous_ref!r} and {ref!r} resolve to the same "
                    f"provider identifier {normalized_identifier!r}."
                )
            mapped_identifier_owners[normalized_identifier] = ref

        precreate_lookup = (
            PreCreateLookup(
                orchestration_key=idempotency_key,
                issue=precreate_match,
                legacy_orchestration_key=legacy_orchestration_key,
                legacy_adoption_permitted=legacy_adoption_permitted,
                node_ref=ref,
            )
            if ref in precreate_lookup_results
            else None
        )

        if not dry_run and mapping_document is not None:
            pending_since = _utc_timestamp()
            entries[ref] = {
                "status": "pending",
                "pending_since": pending_since,
            }
            if meta.parent_ref is not None:
                entries[f"link_subissue:{meta.parent_ref}:{ref}"] = {
                    "status": "pending",
                    "operation_type": "link_subissue",
                    "source_ref": meta.parent_ref,
                    "target_ref": ref,
                    "source_provider_id": ref_to_id[meta.parent_ref],
                    "target_provider_id": None,
                    "pending_since": pending_since,
                }
            if context.mapping_path is not None:
                atomic_write_mapping_document(context.mapping_path, mapping_document)

        try:
            create_issue_with_lookup = getattr(context.provider, "create_issue_with_precreate_lookup", None)
            if (
                precreate_lookup is not None
                and isinstance(context.provider, PreCreateLookupProvider)
                and callable(create_issue_with_lookup)
            ):
                result = create_issue_with_lookup(
                    node.title,
                    node.body,
                    meta.issue_type,
                    parent_id=parent_id,
                    labels=labels,
                    idempotency_key=provider_idempotency_key,
                    precreate_lookup=precreate_lookup,
                    dry_run=dry_run,
                )
            else:
                result = context.provider.create_issue(  # type: ignore[attr-defined]
                    node.title,
                    node.body,
                    meta.issue_type,
                    parent_id=parent_id,
                    labels=labels,
                    idempotency_key=provider_idempotency_key,
                    dry_run=dry_run,
                )
        except HierarchyLinkError as exc:
            if not dry_run and exc.created_result.identifier.strip():
                created_identifier = context.provider.normalize_identifier(  # type: ignore[attr-defined]
                    exc.created_result.identifier
                )
                previous_ref = mapped_identifier_owners.get(created_identifier)
                if previous_ref is not None and previous_ref != ref:
                    collision = RuntimeError(
                        f"Mapping entries {previous_ref!r} and {ref!r} resolve to the same "
                        f"provider identifier {created_identifier!r}."
                    )
                    collision_descriptor = OperationDescriptor(
                        operation_type="create_issue",
                        orchestration_key=idempotency_key,
                        refs=(ref,),
                        status="partial-created",
                        provider_params=provider_params,
                        result=exc.created_result,
                    )
                    partial_plan = OperationPlan(
                        operations=tuple(descriptors) + (collision_descriptor,),
                        dry_run=False,
                        check_existing=(
                            context.mapping_preexisting
                            if context.mapping_preexisting is not None
                            else mapping_document is not None
                        ),
                    )
                    raise PipelineExecutionError(
                        cause=collision,
                        operation_type="create_issue",
                        refs=(ref,),
                        stage="create_issue_result_validation",
                        created_result=exc.created_result,
                        partial_plan=partial_plan,
                    ) from None
                mapped_identifier_owners[created_identifier] = ref
                if mapping_document is not None:
                    if exc.created_result.status == "existing":
                        entries[ref] = {
                            "provider_id": created_identifier,
                            "status": "trusted-match",
                            "match_basis": "create-existing-response",
                        }
                    else:
                        entries[ref] = {"provider_id": created_identifier, "status": "created"}
                    if meta.parent_ref is not None:
                        relationship = cast(dict[str, object], entries[f"link_subissue:{meta.parent_ref}:{ref}"])
                        relationship["source_provider_id"] = ref_to_id[meta.parent_ref]
                        relationship["target_provider_id"] = created_identifier
                    assert context.mapping_path is not None
                    atomic_write_mapping_document(context.mapping_path, mapping_document)
            descriptors.append(
                OperationDescriptor(
                    operation_type="create_issue",
                    orchestration_key=idempotency_key,
                    refs=(ref,),
                    status="partial-created",
                    provider_params=provider_params,
                    result=exc.created_result,
                )
            )
            partial_plan = OperationPlan(
                operations=tuple(descriptors),
                dry_run=dry_run,
                check_existing=(
                    context.mapping_preexisting
                    if context.mapping_preexisting is not None
                    else mapping_document is not None
                ),
            )
            raise PipelineExecutionError(
                cause=exc.cause,
                operation_type="create_issue",
                refs=(ref,),
                stage=exc.stage,
                created_result=exc.created_result,
                partial_plan=partial_plan,
            ) from None
        except DefinitiveCreationFailure as exc:
            if not dry_run and mapping_document is not None:
                entries[ref] = {"status": "failed", "error": _redact(str(exc))}
                if context.mapping_path is not None:
                    atomic_write_mapping_document(context.mapping_path, mapping_document)
            partial_plan = OperationPlan(
                operations=tuple(descriptors),
                dry_run=dry_run,
                check_existing=(
                    context.mapping_preexisting
                    if context.mapping_preexisting is not None
                    else mapping_document is not None
                ),
            )
            raise PipelineExecutionError(
                cause=exc,
                operation_type="create_issue",
                refs=(ref,),
                stage="create_issue",
                created_result=None,
                partial_plan=partial_plan,
            ) from None
        except Exception as exc:
            partial_plan = OperationPlan(
                operations=tuple(descriptors),
                dry_run=dry_run,
                check_existing=(
                    context.mapping_preexisting
                    if context.mapping_preexisting is not None
                    else mapping_document is not None
                ),
            )
            raise PipelineExecutionError(
                cause=exc,
                operation_type="create_issue",
                refs=(ref,),
                stage="create_issue",
                created_result=None,
                partial_plan=partial_plan,
            ) from None

        if not dry_run:
            normalized_identifier = context.provider.normalize_identifier(result.identifier)  # type: ignore[attr-defined]
            previous_ref = mapped_identifier_owners.get(normalized_identifier)
            if previous_ref is not None and previous_ref != ref:
                collision = RuntimeError(
                    f"Mapping entries {previous_ref!r} and {ref!r} resolve to the same "
                    f"provider identifier {normalized_identifier!r}."
                )
                collision_descriptor = OperationDescriptor(
                    operation_type="create_issue",
                    orchestration_key=idempotency_key,
                    refs=(ref,),
                    status=result.status,
                    provider_params=provider_params,
                    result=result,
                )
                partial_plan = OperationPlan(
                    operations=tuple(descriptors) + (collision_descriptor,),
                    dry_run=False,
                    check_existing=(
                        context.mapping_preexisting
                        if context.mapping_preexisting is not None
                        else mapping_document is not None
                    ),
                )
                raise PipelineExecutionError(
                    cause=collision,
                    operation_type="create_issue",
                    refs=(ref,),
                    stage="create_issue_result_validation",
                    created_result=result,
                    partial_plan=partial_plan,
                )
            mapped_identifier_owners[normalized_identifier] = ref

        status = "dry-run" if dry_run else result.status
        descriptors.append(
            OperationDescriptor(
                operation_type="create_issue",
                orchestration_key=idempotency_key,
                refs=(ref,),
                status=status,
                provider_params=provider_params,
                result=None if dry_run else result,
            )
        )
        if not dry_run:
            ref_to_id[ref] = result.identifier
            if mapping_document is not None:
                if result.status == "existing":
                    entries[ref] = {
                        "provider_id": normalized_identifier,
                        "status": "trusted-match",
                        "match_basis": "pre-create-guard"
                        if precreate_match is not None
                        else "create-existing-response",
                    }
                else:
                    entries[ref] = {"provider_id": normalized_identifier, "status": "created"}
                if meta.parent_ref is not None:
                    relationship = cast(dict[str, object], entries[f"link_subissue:{meta.parent_ref}:{ref}"])
                    relationship["target_provider_id"] = normalized_identifier
                    if context.mapping_path is not None:
                        atomic_write_mapping_document(context.mapping_path, mapping_document)

            hierarchy_link_result = result.hierarchy_link_result if meta.parent_ref is not None else None
            if meta.parent_ref is not None and (
                not isinstance(hierarchy_link_result, ProviderLinkResult)
                or hierarchy_link_result.status not in {"linked", "already-linked"}
                or hierarchy_link_result.source_id != ref_to_id.get(meta.parent_ref)
                or hierarchy_link_result.target_id != result.identifier
            ):
                if mapping_document is not None and context.mapping_path is not None:
                    atomic_write_mapping_document(context.mapping_path, mapping_document)
                partial_plan = OperationPlan(
                    operations=tuple(descriptors),
                    dry_run=False,
                    check_existing=(
                        context.mapping_preexisting
                        if context.mapping_preexisting is not None
                        else mapping_document is not None
                    ),
                )
                raise PipelineExecutionError(
                    cause=RuntimeError(f"Provider returned no valid hierarchy link result for created issue {ref!r}."),
                    operation_type="create_issue",
                    refs=(ref,),
                    stage="hierarchy_link_result_validation",
                    created_result=result,
                    partial_plan=partial_plan,
                )

            if mapping_document is not None and meta.parent_ref is not None:
                relationship = cast(dict[str, object], entries[f"link_subissue:{meta.parent_ref}:{ref}"])
                assert hierarchy_link_result is not None
                relationship.update(
                    {
                        "source_provider_id": hierarchy_link_result.source_id,
                        "target_provider_id": hierarchy_link_result.target_id,
                        "status": "confirmed",
                        "confirmed_at": _utc_timestamp(),
                        "result": hierarchy_link_result.status,
                    }
                )
                relationship.pop("pending_since", None)
            if mapping_document is not None and context.mapping_path is not None:
                atomic_write_mapping_document(context.mapping_path, mapping_document)

    return ref_to_id, descriptors


def _link_operations(
    context: _PreflightContext,
    ref_to_id: dict[str, str],
    *,
    dry_run: bool = False,
    prior_operations: tuple[OperationDescriptor, ...] = (),
    only_refs: set[str] | None = None,
) -> list[OperationDescriptor]:
    """Reconcile parent-child links after issue identifiers are resolved."""
    if context.provider is None:
        raise PipelineValidationError("Provider construction was not completed before hierarchy reconciliation.")
    descriptors: list[OperationDescriptor] = []
    embedded_link_refs = {
        operation.refs[0]
        for operation in prior_operations
        if operation.operation_type == "create_issue"
        and operation.refs
        and getattr(operation.result, "hierarchy_link_result", None) is not None
    }
    completed_link_refs = {
        operation.refs
        for operation in prior_operations
        if operation.operation_type == "link_subissue" and len(operation.refs) == 2
    }
    for ref, meta in context.node_index.items():
        if meta.parent_ref is None:
            continue
        if only_refs is not None and (ref not in only_refs or meta.parent_ref not in only_refs):
            continue
        if ref in embedded_link_refs:
            continue
        parent_ref = meta.parent_ref
        if (parent_ref, ref) in completed_link_refs:
            continue
        key = generate_orchestration_key("link_subissue", parent_ref, ref)
        params = {"parent_ref": parent_ref, "child_ref": ref}
        if dry_run:
            descriptors.append(
                OperationDescriptor(
                    operation_type="link_subissue",
                    orchestration_key=key,
                    refs=(parent_ref, ref),
                    status="dry-run",
                    provider_params=params,
                )
            )
            continue
        if ref not in ref_to_id or parent_ref not in ref_to_id:
            continue
        parent_id = ref_to_id[parent_ref]
        child_id = ref_to_id[ref]
        if context.mapping_document is not None:
            mapping_key = f"link_subissue:{parent_ref}:{ref}"
            mapping_entries = cast(dict[str, object], context.mapping_document["entries"])
            mapping_entries[mapping_key] = {
                "status": "pending",
                "operation_type": "link_subissue",
                "source_ref": parent_ref,
                "target_ref": ref,
                "source_provider_id": parent_id,
                "target_provider_id": child_id,
                "pending_since": _utc_timestamp(),
            }
            assert context.mapping_path is not None
            atomic_write_mapping_document(context.mapping_path, context.mapping_document)
        try:
            result = context.provider.link_subissue(parent_id, child_id)  # type: ignore[attr-defined]
        except PipelineExecutionError:
            raise
        except Exception as exc:
            all_ops = tuple(prior_operations) + tuple(descriptors)
            partial_plan = OperationPlan(
                operations=all_ops,
                dry_run=dry_run,
                check_existing=(
                    context.mapping_preexisting
                    if context.mapping_preexisting is not None
                    else context.mapping_document is not None
                ),
            )
            raise PipelineExecutionError(
                cause=exc,
                operation_type="link_subissue",
                refs=(parent_ref, ref),
                stage="link_subissue",
                created_result=None,
                partial_plan=partial_plan,
            ) from None
        descriptors.append(
            OperationDescriptor(
                operation_type="link_subissue",
                orchestration_key=key,
                refs=(parent_ref, ref),
                status=result.status,
                provider_params=params,
                result=result,
            )
        )
        if context.mapping_document is not None:
            mapping_entries = cast(dict[str, object], context.mapping_document["entries"])
            relationship = cast(dict[str, object], mapping_entries[mapping_key])
            relationship.update(
                {
                    "source_provider_id": result.source_id,
                    "target_provider_id": result.target_id,
                    "status": "confirmed",
                    "confirmed_at": _utc_timestamp(),
                    "result": result.status,
                }
            )
            relationship.pop("pending_since", None)
            assert context.mapping_path is not None
            atomic_write_mapping_document(context.mapping_path, context.mapping_document)
    return descriptors


# ---------------------------------------------------------------------------
# Blocking relationships
# ---------------------------------------------------------------------------


def _blocking_operations(
    context: _PreflightContext,
    ref_to_id: dict[str, str],
    *,
    dry_run: bool = False,
    prior_operations: tuple[OperationDescriptor, ...] = (),
    only_refs: set[str] | None = None,
) -> list[OperationDescriptor]:
    """Establish (or plan) declared blocking relationships (FR-009).

    Iterates the deduplicated blocking graph in deterministic
    ``(blocker_ref, blocked_ref)`` lexicographic order (NFR-001).  Complementary
    ``blocks``/``blockedBy`` declarations collapse to exactly one provider call
    and one descriptor.  Canonical descriptor refs are recorded as
    ``(blocked_ref, blocker_ref)``.

    Edges whose ``blocked_ref`` or ``blocker_ref`` has no resolved provider
    identifier (e.g. a ``start_from`` resume that skips a fully unresolved
    prefix edge) are silently skipped, mirroring how :func:`_link_operations`
    skips hierarchy edges outside the resolved id set.

    Args:
        prior_operations: Descriptors already captured earlier in the run;
            included in any partial plan on failure.

    Raises:
        PipelineExecutionError: On the first adapter failure.
    """
    if context.provider is None:
        raise PipelineValidationError("Provider construction was not completed before dependency reconciliation.")
    graph = build_dependency_graph(context.tree)
    edges = sorted(
        (blocker_ref, blocked_ref) for blocker_ref, blocked_refs in graph.items() for blocked_ref in blocked_refs
    )

    descriptors: list[OperationDescriptor] = []
    completed_dependency_refs = {
        operation.refs
        for operation in prior_operations
        if operation.operation_type == "add_blocked_by" and len(operation.refs) == 2
    }
    for blocker_ref, blocked_ref in edges:
        if only_refs is not None and (blocker_ref not in only_refs or blocked_ref not in only_refs):
            continue
        if (blocked_ref, blocker_ref) in completed_dependency_refs:
            continue
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

        if blocked_ref not in ref_to_id or blocker_ref not in ref_to_id:
            continue

        blocked_id = ref_to_id[blocked_ref]
        blocker_id = ref_to_id[blocker_ref]
        try:
            mapping_key = f"add_blocked_by:{blocked_ref}:{blocker_ref}"
            if context.mapping_document is not None:
                mapping_entries = cast(dict[str, object], context.mapping_document["entries"])
                mapping_entries[mapping_key] = {
                    "status": "pending",
                    "operation_type": "add_blocked_by",
                    "source_ref": blocked_ref,
                    "target_ref": blocker_ref,
                    "source_provider_id": blocked_id,
                    "target_provider_id": blocker_id,
                    "pending_since": _utc_timestamp(),
                }
                assert context.mapping_path is not None
                atomic_write_mapping_document(context.mapping_path, context.mapping_document)
            result = context.provider.add_blocked_by(blocked_id, blocker_id)  # type: ignore[attr-defined]
        except Exception as exc:
            all_ops = tuple(prior_operations) + tuple(descriptors)
            partial_plan = OperationPlan(
                operations=all_ops,
                dry_run=dry_run,
                check_existing=(
                    context.mapping_preexisting
                    if context.mapping_preexisting is not None
                    else context.mapping_document is not None
                ),
            )
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
        if context.mapping_document is not None:
            mapping_entries = cast(dict[str, object], context.mapping_document["entries"])
            relationship = cast(dict[str, object], mapping_entries[mapping_key])
            relationship.update(
                {
                    "status": "confirmed",
                    "confirmed_at": _utc_timestamp(),
                    "result": result.status,
                    "source_provider_id": result.target_id,
                    "target_provider_id": result.source_id,
                }
            )
            relationship.pop("pending_since", None)
            assert context.mapping_path is not None
            atomic_write_mapping_document(context.mapping_path, context.mapping_document)

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
    force_resume: bool = False,
) -> OperationPlan:
    """Load, validate, order, and execute an epic-tree creation plan.

    This is the provider-neutral extension boundary. Live schema-v1 definitions
    are migrated to schema v2 before the tree lock is acquired. Live runs then
    validate the mapping and construct the provider while holding that lock.
    Dry runs validate the mapping before provider construction without
    acquiring the lock. The pipeline then computes a deterministic
    dependency-safe order and captures every operation in the returned
    :class:`OperationPlan`.

    Args:
        repo_path: Absolute path to the repository root.  Used for loader
            containment validation and provider construction.
        file_path: Path to the JSON definition file to load and canonicalize.
        provider: Optional provider-name override; resolved via
            ``resolve_provider_name`` when ``None``.
        start_from: Optional node ref from which execution begins.
        dry_run: When ``True``, run full preflight but suppress all provider
            mutations and return planning descriptors only.
        force_resume: Allow one fresh create attempt for a stale pending
            mapping entry after bounded provider reconciliation.

    Returns:
        An :class:`OperationPlan` capturing every planned or executed
        operation in deterministic order.  ``check_existing`` is ``True``
        when the run resumed from an existing schema-v2 mapping document
        (an existence check was performed against it) and ``False``
        otherwise.

    Raises:
        PipelineValidationError: On any preflight failure (no mutation
            requested).
        PipelineExecutionError: On the first adapter failure during execution.
    """
    if dry_run:
        context = _run_preflight(repo_path, file_path, provider=provider, start_from=start_from)
        return _execute_creation_plan(context, dry_run=dry_run, force_resume=force_resume)

    context = _run_preflight(
        repo_path,
        file_path,
        provider=provider,
        start_from=start_from,
        load_mapping=False,
        construct_provider=False,
    )
    if context.tree.treeId is None:
        try:
            migrated_tree = migrate_schema_v1_to_v2(Path(file_path).resolve(strict=True))
        except Exception as exc:
            raise PipelineValidationError(
                f"Failed to migrate schema-v1 epic-tree definition: {exc}", cause=exc
            ) from exc
        if migrated_tree.treeId is None:
            raise PipelineValidationError("Schema-v1 migration did not produce a treeId.")
        locked_tree_id = migrated_tree.treeId
    else:
        locked_tree_id = context.tree.treeId
    lock_cm = acquire_tree_lock(locked_tree_id)
    try:
        lock_cm.__enter__()
    except RuntimeError as exc:
        raise PipelineValidationError(str(exc), cause=exc) from exc
    try:
        context = _run_preflight(repo_path, file_path, provider=provider, start_from=start_from)
        if context.tree.treeId != locked_tree_id:
            raise PipelineValidationError("Epic-tree treeId changed while acquiring its lock; retry the command.")
        return _execute_creation_plan(context, dry_run=dry_run, force_resume=force_resume)
    finally:
        lock_cm.__exit__(None, None, None)


def _execute_creation_plan(context: _PreflightContext, *, dry_run: bool, force_resume: bool = False) -> OperationPlan:
    """Compute execution order and run (or plan) every pipeline operation.

    Callers holding a tree lock must invoke this only while the lock is held,
    so the mapping-document read/modify/write sequence performed by the
    nested operation builders stays serialized against concurrent reruns.
    """
    if context.provider is None:
        raise PipelineValidationError("Provider construction was not completed before pipeline execution.")
    ordered_refs = _build_execution_order(context)
    ref_to_id, create_operations = _create_issue_operations(
        context, ordered_refs, dry_run=dry_run, force_resume=force_resume
    )
    link_operations = _link_operations(
        context,
        ref_to_id,
        dry_run=dry_run,
        prior_operations=tuple(create_operations),
    )
    blocking_operations = _blocking_operations(
        context,
        ref_to_id,
        dry_run=dry_run,
        prior_operations=tuple(create_operations) + tuple(link_operations),
    )
    operations = tuple(create_operations) + tuple(link_operations) + tuple(blocking_operations)
    return OperationPlan(
        operations=operations,
        dry_run=dry_run,
        check_existing=(
            context.mapping_preexisting
            if context.mapping_preexisting is not None
            else context.mapping_document is not None
        ),
    )
