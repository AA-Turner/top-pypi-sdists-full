"""Model exports for the Azure Container Apps Sandbox SDK.

This module re-exports all model classes from their domain-specific
submodules. Import from here or from ``azure.containerapps.sandbox`` directly.
Migrated families are direct aliases of ``azure.containerapps.sandbox.models``.
Other families retain their existing implementations until migration.
"""

from azure.containerapps.sandbox.models import (
    Sandbox,
    SandboxResources,
    SandboxSource as SandboxSourcesRef,
    SandboxSourceDiskImage as DiskImageRef,
    SandboxSourceSnapshot as SnapshotRef,
    SandboxStateDetails,
    StoppedReason,
)
from azure.containerapps.sandbox.models import (
    AzureBlobByoManagedIdentityAuth,
    SandboxGroupIdentitySelector,
    SystemAssignedSandboxGroupIdentitySelector,
    UserAssignedSandboxGroupIdentitySelector,
    EgressDecisionEntry,
    EgressDecisions,
    EgressForwardProxy,
    EgressHeader,
    EgressHeaderValueRef,
    EgressHostRule,
    EgressHookRef,
    EgressHttpPolicy,
    EgressManagedIdentityRef,
    EgressPolicy,
    EgressRule,
    EgressRuleAction,
    EgressRuleMatch,
    EgressSecretRef,
    TdsCredential,
    TdsEgressAction,
    TdsEgressMatch,
    TdsEgressRule,
    TdsEgressSection,
    PostgresCredential,
    PostgresEgressAction,
    PostgresEgressMatch,
    PostgresEgressRule,
    PostgresEgressSection,
    EgressTransportPolicy,
    EgressTransportRule,
    EgressValidationWarning,
    NetworkEgressDecisions,
)
from azure.containerapps.sandbox.models import (
    AutoDeletePolicy,
    AutoSuspendPolicy,
    LifecyclePolicy,
)
from azure.containerapps.sandbox.models import (
    AddPortRequest,
    PortAuthConfig,
    PortAuthEntraId,
    PortIpAccessControl,
    PortIpAccessControlRule,
    SandboxPort,
)
from azure.containerapps.sandbox.models import (
    CpuUsage,
    DirListing,
    DiskImage,
    DiskImageSpec,
    DiskImageStatus,
    ExecResult,
    FileInfo,
    NetworkUsage,
    PublicDiskImage,
    RegistryCredentials,
    ResourceUsage,
    SandboxStats,
    SandboxVolume as AddVolumeMountRequest,
    Snapshot,
    SnapshotResources,
)
from azure.containerapps.sandbox.models import (
    BlobVolumeUsage,
    DataDiskVolumeUsage,
    SandboxVolume,
    Secret as SecretMetadata,
    Volume,
)
from azure.containerapps.sandbox._model_types._secrets import (
    SecretValuePeek,
)

__all__ = [
    # Sandbox core
    "DiskImageRef",
    "Sandbox",
    "SandboxResources",
    "SandboxSourcesRef",
    "SandboxStateDetails",
    "SnapshotRef",
    "StoppedReason",
    # Egress
    "EgressDecisionEntry",
    "EgressDecisions",
    "EgressForwardProxy",
    "EgressHeader",
    "EgressHeaderValueRef",
    "EgressHostRule",
    "EgressHookRef",
    "EgressHttpPolicy",
    "EgressManagedIdentityRef",
    "EgressPolicy",
    "EgressRule",
    "EgressRuleAction",
    "EgressRuleMatch",
    "EgressSecretRef",
    "TdsCredential",
    "TdsEgressAction",
    "TdsEgressMatch",
    "TdsEgressRule",
    "TdsEgressSection",
    "PostgresCredential",
    "PostgresEgressAction",
    "PostgresEgressMatch",
    "PostgresEgressRule",
    "PostgresEgressSection",
    "EgressTransportPolicy",
    "EgressTransportRule",
    "EgressValidationWarning",
    # Lifecycle
    "AutoDeletePolicy",
    "AutoSuspendPolicy",
    "LifecyclePolicy",
    # Ports
    "AddPortRequest",
    "PortAuthConfig",
    "PortAuthEntraId",
    "PortIpAccessControl",
    "PortIpAccessControlRule",
    "SandboxPort",
    # Exec
    "ExecResult",
    # Images
    "DiskImage",
    "DiskImageSpec",
    "DiskImageStatus",
    "PublicDiskImage",
    "RegistryCredentials",
    # Snapshots
    "Snapshot",
    "SnapshotResources",
    # Volumes
    "AddVolumeMountRequest",
    "AzureBlobByoManagedIdentityAuth",
    "SandboxGroupIdentitySelector",
    "SystemAssignedSandboxGroupIdentitySelector",
    "UserAssignedSandboxGroupIdentitySelector",
    "SandboxVolume",
    "Volume",
    "BlobVolumeUsage",
    "DataDiskVolumeUsage",
    # Files
    "DirListing",
    "FileInfo",
    # Stats
    "CpuUsage",
    "NetworkEgressDecisions",
    "NetworkUsage",
    "ResourceUsage",
    "SandboxStats",
    # Secrets
    "SecretMetadata",
    "SecretValuePeek",
    # Groups
]
