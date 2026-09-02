"""spec-kitty-tracker: universal task tracker interface and sync engine.

Imports below are alphabetized by module (ruff/isort, rule I001); the
public surface is grouped semantically instead in the __all__ list and
in docs/PUBLIC_API.md (TRK-M1-08), not via source-order comments here.
"""

from spec_kitty_tracker.capabilities import TrackerCapabilities
from spec_kitty_tracker.conflicts import ConflictRecord, ConflictStrategy
from spec_kitty_tracker.connectors import (
    AzureDevOpsConnector,
    AzureDevOpsConnectorConfig,
    BeadsConnector,
    BeadsConnectorConfig,
    FPConnector,
    FPConnectorConfig,
    GitHubConnector,
    GitHubConnectorConfig,
    GitLabConnector,
    GitLabConnectorConfig,
    InMemoryConnector,
    JiraConnector,
    JiraConnectorConfig,
    LinearConnector,
    LinearConnectorConfig,
)
from spec_kitty_tracker.context import LocalExecutionContext

# --- Discovery (new registry-based architecture) ---
from spec_kitty_tracker.discovery import (
    DiscoveredResource,
    DiscoveredWorkspace,
    DiscoveryResult,
    discover_resources,
    discover_workspaces,
)
from spec_kitty_tracker.errors import (
    CapabilityNotSupportedError,
    ConnectorConfigError,
    ConnectorRequestError,
    DecisionReferenceContractError,
    DiscoveryContractError,
    FailureClass,
    HostedAuthRequiredError,
    IssueNotFoundError,
    IssuePayloadContractError,
    ScopeViolationError,
    SpecKittyTrackerError,
    SyncConflictError,
    TrackerContractError,
    classify_http_status,
)
from spec_kitty_tracker.hosted import (
    GitHubHostedParams,
    GitLabHostedParams,
    HostedConnectorRequest,
    HostedProviderSlug,
    JiraHostedParams,
    LinearHostedParams,
    create_hosted_connector,
)
from spec_kitty_tracker.mission_sync import (
    BidirectionalIssueSync,
    DecisionReference,
    MissionSeed,
    MissionUpdate,
    decision_link_mismatches,
    mission_seed_from_issue,
)
from spec_kitty_tracker.mode import (
    ALL_KNOWN_PROVIDERS,
    HOSTED_PROVIDERS,
    LOCAL_PROVIDERS,
    TrackerMode,
    is_hosted_provider,
    is_local_provider,
    provider_mode,
)
from spec_kitty_tracker.models import (
    CanonicalIssue,
    CanonicalIssueType,
    CanonicalLink,
    CanonicalStatus,
    ExternalRef,
    LinkType,
    Page,
    SyncCheckpoint,
    TrackerEvent,
    TrackerEventType,
    utcnow,
)
from spec_kitty_tracker.nango import (
    NANGO_MANAGED_TOKEN,
    NangoConnectionContext,
    NangoProxyAdapter,
    NangoProxyTransport,
)
from spec_kitty_tracker.policy import (
    CORE_ISSUE_FIELDS,
    FieldOwner,
    OwnershipMode,
    OwnershipPolicy,
)
from spec_kitty_tracker.protocols import LocalIssueStore, TaskTrackerConnector
from spec_kitty_tracker.registry import ConnectorRegistry
from spec_kitty_tracker.store import InMemoryIssueStore
from spec_kitty_tracker.sync import SyncEngine, SyncFailure, SyncResult, SyncStats
from spec_kitty_tracker.types import JSONValue

__version__ = "0.5.2"

__all__ = [
    "ALL_KNOWN_PROVIDERS",
    "CORE_ISSUE_FIELDS",
    "HOSTED_PROVIDERS",
    "LOCAL_PROVIDERS",
    "NANGO_MANAGED_TOKEN",
    "AzureDevOpsConnector",
    "AzureDevOpsConnectorConfig",
    "BeadsConnector",
    "BeadsConnectorConfig",
    "BidirectionalIssueSync",
    "CanonicalIssue",
    "CanonicalIssueType",
    "CanonicalLink",
    "CanonicalStatus",
    "CapabilityNotSupportedError",
    "ConflictRecord",
    "ConflictStrategy",
    "ConnectorConfigError",
    "ConnectorRegistry",
    "ConnectorRequestError",
    "DecisionReference",
    "DecisionReferenceContractError",
    "DiscoveredResource",
    "DiscoveredWorkspace",
    "DiscoveryContractError",
    "DiscoveryResult",
    "ExternalRef",
    "FPConnector",
    "FPConnectorConfig",
    "FailureClass",
    "FieldOwner",
    "GitHubConnector",
    "GitHubConnectorConfig",
    "GitHubHostedParams",
    "GitLabConnector",
    "GitLabConnectorConfig",
    "GitLabHostedParams",
    "HostedAuthRequiredError",
    "HostedConnectorRequest",
    "HostedProviderSlug",
    "InMemoryConnector",
    "InMemoryIssueStore",
    "IssueNotFoundError",
    "IssuePayloadContractError",
    "JSONValue",
    "JiraConnector",
    "JiraConnectorConfig",
    "JiraHostedParams",
    "LinearConnector",
    "LinearConnectorConfig",
    "LinearHostedParams",
    "LinkType",
    "LocalExecutionContext",
    "LocalIssueStore",
    "MissionSeed",
    "MissionUpdate",
    "NangoConnectionContext",
    "NangoProxyAdapter",
    "NangoProxyTransport",
    "OwnershipMode",
    "OwnershipPolicy",
    "Page",
    "ScopeViolationError",
    "SpecKittyTrackerError",
    "SyncCheckpoint",
    "SyncConflictError",
    "SyncEngine",
    "SyncFailure",
    "SyncResult",
    "SyncStats",
    "TaskTrackerConnector",
    "TrackerCapabilities",
    "TrackerContractError",
    "TrackerEvent",
    "TrackerEventType",
    "TrackerMode",
    "classify_http_status",
    "create_hosted_connector",
    "decision_link_mismatches",
    "discover_resources",
    "discover_workspaces",
    "is_hosted_provider",
    "is_local_provider",
    "mission_seed_from_issue",
    "provider_mode",
    "utcnow",
]
