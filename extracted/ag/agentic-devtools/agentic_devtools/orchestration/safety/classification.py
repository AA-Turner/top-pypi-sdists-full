"""Action classification for the execution safety policy (FR-002).

Defines the four-level classification enum, registry entry dataclass,
and the ``ClassificationRegistry`` that maps tool names to their safety
classification.
"""

from __future__ import annotations

import dataclasses
import enum
from typing import TYPE_CHECKING

from .exceptions import UnclassifiedToolError

if TYPE_CHECKING:
    pass


class ActionClassification(enum.Enum):
    """Four-level action classification for safety enforcement.

    Levels (least to most impactful):
    - read_only: Fetch data, no side effects (always allowed)
    - local_mutation: Edit local files, run tests (allowed in live/dry_run)
    - external_mutation: Post comments, create PRs, push (live only, audit-logged)
    - destructive: Force push, delete branches (require explicit opt-in)
    """

    read_only = "read_only"
    local_mutation = "local_mutation"
    external_mutation = "external_mutation"
    destructive = "destructive"


@dataclasses.dataclass(frozen=True)
class ClassificationEntry:
    """A single tool's safety classification metadata.

    Attributes:
        tool_name: Registered tool identifier.
        classification: The action classification level.
        nondeterministic_fields: Optional dot-paths to exclude from operation ID
            computation (per-tool overrides beyond the default set).
    """

    tool_name: str
    classification: ActionClassification
    nondeterministic_fields: tuple[str, ...] = ()


class ClassificationRegistry:
    """Maps tool names to their safety classification.

    Raises ``UnclassifiedToolError`` for unknown tools (fail-closed).
    """

    def __init__(self) -> None:
        self._entries: dict[str, ClassificationEntry] = {}

    def register(self, entry: ClassificationEntry) -> None:
        """Register a tool's classification entry."""
        self._entries[entry.tool_name] = entry

    def get(self, tool_name: str) -> ClassificationEntry:
        """Look up a tool's classification.

        Raises:
            UnclassifiedToolError: If the tool has no registered classification.
        """
        entry = self._entries.get(tool_name)
        if entry is None:
            raise UnclassifiedToolError(tool_name)
        return entry

    def has(self, tool_name: str) -> bool:
        """Check if a tool has a registered classification."""
        return tool_name in self._entries

    @property
    def tool_names(self) -> frozenset[str]:
        """Return all registered tool names."""
        return frozenset(self._entries.keys())


# ---------------------------------------------------------------------------
# Default registry with all builtin tools classified
# ---------------------------------------------------------------------------


def build_default_registry() -> ClassificationRegistry:
    """Build a registry with all builtin tools classified per FR-002.

    Classification rationale:
    - read_only: Tools that only fetch/query data (no side effects)
    - local_mutation: Tools that modify local filesystem/state only
    - external_mutation: Tools that call external APIs (Jira, Azure DevOps, GitHub)
    - destructive: Tools that perform irreversible operations (force push)
    """
    registry = ClassificationRegistry()

    # Git tools
    registry.register(ClassificationEntry("git_stage_all", ActionClassification.local_mutation))
    registry.register(ClassificationEntry("git_save_work", ActionClassification.external_mutation))
    registry.register(ClassificationEntry("git_push", ActionClassification.external_mutation))
    registry.register(ClassificationEntry("git_force_push", ActionClassification.destructive))
    registry.register(ClassificationEntry("git_get_current_branch", ActionClassification.read_only))
    registry.register(ClassificationEntry("git_current_branch", ActionClassification.read_only))
    registry.register(ClassificationEntry("git_get_status", ActionClassification.read_only))

    # Jira tools
    registry.register(
        ClassificationEntry(
            "jira_add_comment",
            ActionClassification.external_mutation,
            nondeterministic_fields=("timestamp",),
        )
    )
    registry.register(ClassificationEntry("jira_get_issue", ActionClassification.read_only))
    registry.register(ClassificationEntry("get_issue_context", ActionClassification.read_only))

    # Azure DevOps tools
    registry.register(
        ClassificationEntry(
            "azure_devops_create_pr",
            ActionClassification.external_mutation,
            nondeterministic_fields=("timestamp",),
        )
    )
    registry.register(
        ClassificationEntry(
            "azure_devops_reply_to_thread",
            ActionClassification.external_mutation,
        )
    )
    registry.register(
        ClassificationEntry(
            "azure_devops_resolve_thread",
            ActionClassification.external_mutation,
        )
    )
    registry.register(
        ClassificationEntry(
            "azure_devops_approve_pull_request",
            ActionClassification.external_mutation,
        )
    )

    # GitHub tools
    registry.register(ClassificationEntry("github_get_pr_state", ActionClassification.read_only))
    registry.register(ClassificationEntry("github_get_pr_checks_status", ActionClassification.read_only))
    registry.register(
        ClassificationEntry(
            "github_add_comment",
            ActionClassification.external_mutation,
            nondeterministic_fields=("timestamp",),
        )
    )

    # Filesystem tools
    registry.register(ClassificationEntry("filesystem_read_file", ActionClassification.read_only))
    registry.register(ClassificationEntry("filesystem_write_file", ActionClassification.local_mutation))
    registry.register(ClassificationEntry("filesystem_list_directory", ActionClassification.read_only))

    # Testing tools
    registry.register(ClassificationEntry("testing_run_tests", ActionClassification.local_mutation))
    registry.register(ClassificationEntry("testing_run_pattern", ActionClassification.local_mutation))

    # State tools
    registry.register(ClassificationEntry("state_get", ActionClassification.read_only))
    registry.register(ClassificationEntry("state_set", ActionClassification.local_mutation))

    # Provider-neutral tools
    registry.register(
        ClassificationEntry(
            "reply_to_pull_request_thread",
            ActionClassification.external_mutation,
        )
    )

    return registry
