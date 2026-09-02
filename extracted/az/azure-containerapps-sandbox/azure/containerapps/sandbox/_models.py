"""Typed models for the Azure Container Apps Sandbox SDK.

This module re-exports all model classes from their domain-specific
submodules. Import from here or from ``azure.containerapps.sandbox`` directly.
"""

from azure.containerapps.sandbox._model_types._sandbox import (
    DiskImageRef,
    Sandbox,
    SandboxResources,
    SandboxSourcesRef,
    SandboxStateDetails,
    SnapshotRef,
    StoppedReason,
)
from azure.containerapps.sandbox._model_types._egress import (
    EgressDecisionEntry,
    EgressDecisions,
    EgressHeader,
    EgressHeaderValueRef,
    EgressHostRule,
    EgressManagedIdentityRef,
    EgressPolicy,
    EgressRule,
    EgressRuleAction,
    EgressRuleMatch,
    EgressSecretRef,
)
from azure.containerapps.sandbox._model_types._lifecycle import (
    AutoDeletePolicy,
    AutoSuspendPolicy,
    LifecyclePolicy,
)
from azure.containerapps.sandbox._model_types._ports import (
    AddPortRequest,
    PortAuthConfig,
    PortAuthEntraId,
    PortIpAccessControl,
    PortIpAccessControlRule,
    SandboxPort,
)
from azure.containerapps.sandbox._model_types._exec import ExecResult
from azure.containerapps.sandbox._model_types._images import (
    DiskImage,
    DiskImageSpec,
    DiskImageStatus,
    PublicDiskImage,
    RegistryCredentials,
)
from azure.containerapps.sandbox._model_types._snapshots import (
    Snapshot,
    SnapshotGpu,
    SnapshotResources,
)
from azure.containerapps.sandbox._model_types._volumes import (
    AddVolumeMountRequest,
    AzureBlobByoManagedIdentityAuth,
    SandboxGroupIdentitySelector,
    SandboxVolume,
    Volume,
    VolumeUsage,
)
from azure.containerapps.sandbox._model_types._files import DirListing, FileInfo
from azure.containerapps.sandbox._model_types._stats import (
    CpuUsage,
    NetworkEgressDecisions,
    NetworkUsage,
    ResourceUsage,
    SandboxStats,
)
from azure.containerapps.sandbox._model_types._secrets import (
    SecretMetadata,
    SecretValuePeek,
)
from azure.containerapps.sandbox._model_types._groups import SandboxGroup

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
    "EgressHeader",
    "EgressHeaderValueRef",
    "EgressHostRule",
    "EgressManagedIdentityRef",
    "EgressPolicy",
    "EgressRule",
    "EgressRuleAction",
    "EgressRuleMatch",
    "EgressSecretRef",
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
    "SnapshotGpu",
    "SnapshotResources",
    # Volumes
    "AddVolumeMountRequest",
    "AzureBlobByoManagedIdentityAuth",
    "SandboxGroupIdentitySelector",
    "SandboxVolume",
    "Volume",
    "VolumeUsage",
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
    "SandboxGroup",
]
