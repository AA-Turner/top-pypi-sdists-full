"""Operation plan data model for dry-run and execution tracking (FR-006).

Defines ``OperationDescriptor`` (a single planned/executed operation) and
``OperationPlan`` (an ordered collection of descriptors).  Both are frozen
dataclasses — strictly in-memory, not designed for disk persistence.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any

from agentic_devtools.adapters.issue_provider import ProviderIssueResult, ProviderLinkResult

# Closed set of operation-outcome statuses an ``OperationDescriptor`` may carry.
# ``partial-created`` marks an issue whose creation succeeded but whose
# subsequent hierarchy-link step failed (see
# :class:`~agentic_devtools.adapters.exceptions.HierarchyLinkError`).
OPERATION_STATUSES: frozenset[str] = frozenset(
    {
        "dry-run",
        "existing",
        "already-linked",
        "created",
        "linked",
        "partial-created",
        "updated",
        "no-op",
        "resolved",
    }
)


@dataclass(frozen=True)
class OperationDescriptor:
    """A single planned or executed operation.

    Attributes:
        operation_type: One of "create_issue", "link_subissue", or "add_blocked_by".
        orchestration_key: 64-char hex SHA-256 key for this operation.
        refs: Manifest refs used in key derivation, in canonical order.
        status: Operation outcome — one of :data:`OPERATION_STATUSES`:
            "dry-run", "existing", "already-linked", "created", "linked",
            "partial-created" (issue created but hierarchy link failed),
            "updated", "no-op", or "resolved".
        provider_params: Provider-facing operation inputs captured in the
            plan (for example title/issue_type/labels, plus ref-based
            relationship fields such as parent_ref/child_ref/blocked_by_ref
            used during planning before provider identifiers are resolved).
        result: The adapter result object, or None for planning-only dry-run.
    """

    operation_type: str
    orchestration_key: str
    refs: tuple[str, ...]
    status: str
    provider_params: dict[str, Any] = field(default_factory=dict)
    result: ProviderIssueResult | ProviderLinkResult | None = None

    def __post_init__(self) -> None:
        """Validate the closed-set status contract."""
        if self.status not in OPERATION_STATUSES:
            allowed = ", ".join(sorted(OPERATION_STATUSES))
            raise ValueError(f"Unsupported operation status {self.status!r}. Expected one of: {allowed}")

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dictionary representation."""
        result_dict: dict[str, Any] | None = None
        if self.result is not None:
            result_dict = self.result.to_dict()
        return {
            "operation_type": self.operation_type,
            "orchestration_key": self.orchestration_key,
            "refs": list(self.refs),
            "status": self.status,
            "provider_params": copy.deepcopy(self.provider_params),
            "result": result_dict,
        }

    @property
    def is_dry_run(self) -> bool:
        """Return True if this descriptor represents a dry-run operation."""
        return self.status == "dry-run"

    @property
    def is_existing(self) -> bool:
        """Return True if this descriptor represents an already-existing entity."""
        return self.status in ("existing", "already-linked")

    @property
    def is_partial_created(self) -> bool:
        """Return True if the issue was created but its hierarchy link failed."""
        return self.status == "partial-created"


@dataclass(frozen=True)
class OperationPlan:
    """An ordered collection of operation descriptors.

    Strictly in-memory — not designed for serialization to disk for
    cross-run resumption. The orchestrator re-derives the plan from the
    manifest on each invocation.

    Attributes:
        operations: Dependency-safe ordered tuple of descriptors.
        dry_run: Whether this plan was generated in dry-run mode.
        check_existing: Whether existence checks were performed.
    """

    operations: tuple[OperationDescriptor, ...]
    dry_run: bool
    check_existing: bool

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dictionary representation."""
        return {
            "operations": [op.to_dict() for op in self.operations],
            "dry_run": self.dry_run,
            "check_existing": self.check_existing,
            "summary": {
                "total": len(self.operations),
                "creates": len(self.create_operations),
                "links": len(self.link_operations),
                "dependencies": len(self.dependency_operations),
            },
        }

    @property
    def create_operations(self) -> tuple[OperationDescriptor, ...]:
        """Return only create_issue operations."""
        return tuple(op for op in self.operations if op.operation_type == "create_issue")

    @property
    def link_operations(self) -> tuple[OperationDescriptor, ...]:
        """Return only link_subissue operations."""
        return tuple(op for op in self.operations if op.operation_type == "link_subissue")

    @property
    def dependency_operations(self) -> tuple[OperationDescriptor, ...]:
        """Return only add_blocked_by operations."""
        return tuple(op for op in self.operations if op.operation_type == "add_blocked_by")
