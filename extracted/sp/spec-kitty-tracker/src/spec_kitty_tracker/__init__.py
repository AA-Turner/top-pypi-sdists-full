"""spec-kitty-tracker: universal task tracker interface and sync engine."""

# --- Hosted transport (factory, Nango types, discovery) ---
from spec_kitty_tracker.hosted import (
    create_hosted_connector,
    GitHubHostedParams,
    GitLabHostedParams,
    HostedConnectorRequest,
    HostedProviderSlug,
    JiraHostedParams,
    LinearHostedParams,
)
from spec_kitty_tracker.nango import (
    NANGO_MANAGED_TOKEN,
    NangoConnectionContext,
    NangoProxyAdapter,
    NangoProxyTransport,
)

# --- Discovery (new registry-based architecture) ---
from spec_kitty_tracker.discovery import (
    discover_workspaces,
    discover_resources,
    DiscoveredWorkspace,
    DiscoveredResource,
    DiscoveryResult,
)
from spec_kitty_tracker.types import JSONValue

# --- Core domain (models, protocols, sync, policy, errors) ---
from spec_kitty_tracker.capabilities import TrackerCapabilities
from spec_kitty_tracker.conflicts import ConflictRecord, ConflictStrategy
from spec_kitty_tracker.errors import (
    CapabilityNotSupportedError,
    classify_http_status,
    ConnectorConfigError,
    ConnectorRequestError,
    DiscoveryContractError,
    FailureClass,
    IssueNotFoundError,
    SpecKittyTrackerError,
    SyncConflictError,
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
from spec_kitty_tracker.mission_sync import (
    BidirectionalIssueSync,
    DecisionReference,
    MissionSeed,
    MissionUpdate,
    mission_seed_from_issue,
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
from spec_kitty_tracker.sync import SyncEngine, SyncResult, SyncStats

# --- Connectors: SaaS-backed (used via NangoProxyAdapter / create_hosted_connector) ---
from spec_kitty_tracker.connectors import (
    GitHubConnector,
    GitHubConnectorConfig,
    GitLabConnector,
    GitLabConnectorConfig,
    JiraConnector,
    JiraConnectorConfig,
    LinearConnector,
    LinearConnectorConfig,
)

# --- Connectors: out-of-scope for hosted transport in this release ---
from spec_kitty_tracker.connectors import (
    AzureDevOpsConnector,
    AzureDevOpsConnectorConfig,
)

# --- Connectors: local/native (used directly, no proxy transport) ---
from spec_kitty_tracker.connectors import (
    BeadsConnector,
    BeadsConnectorConfig,
    FPConnector,
    FPConnectorConfig,
)

# --- Connectors: test/reference ---
from spec_kitty_tracker.connectors import InMemoryConnector

__version__ = "0.4.3"

__all__ = [
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
    "classify_http_status",
    "ConflictRecord",
    "ConflictStrategy",
    "ConnectorConfigError",
    "ConnectorRegistry",
    "ConnectorRequestError",
    "CORE_ISSUE_FIELDS",
    "create_hosted_connector",
    "DecisionReference",
    "DiscoveredResource",
    "DiscoveredWorkspace",
    "DiscoveryContractError",
    "DiscoveryResult",
    "discover_resources",
    "discover_workspaces",
    "ExternalRef",
    "FailureClass",
    "FieldOwner",
    "FPConnector",
    "FPConnectorConfig",
    "GitHubConnector",
    "GitHubConnectorConfig",
    "GitHubHostedParams",
    "GitLabConnector",
    "GitLabConnectorConfig",
    "GitLabHostedParams",
    "HostedConnectorRequest",
    "HostedProviderSlug",
    "InMemoryConnector",
    "InMemoryIssueStore",
    "IssueNotFoundError",
    "JiraConnector",
    "JiraConnectorConfig",
    "JiraHostedParams",
    "JSONValue",
    "LinearConnector",
    "LinearConnectorConfig",
    "LinearHostedParams",
    "LinkType",
    "LocalIssueStore",
    "mission_seed_from_issue",
    "MissionSeed",
    "MissionUpdate",
    "NANGO_MANAGED_TOKEN",
    "NangoConnectionContext",
    "NangoProxyAdapter",
    "NangoProxyTransport",
    "OwnershipMode",
    "OwnershipPolicy",
    "Page",
    "SpecKittyTrackerError",
    "SyncCheckpoint",
    "SyncConflictError",
    "SyncEngine",
    "SyncResult",
    "SyncStats",
    "TaskTrackerConnector",
    "TrackerCapabilities",
    "TrackerEvent",
    "TrackerEventType",
    "utcnow",
]
