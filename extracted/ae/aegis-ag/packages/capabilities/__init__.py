"""Capability contracts and registry primitives for Aegis."""

from .inventory import CAPABILITY_SURFACES
from .runtime import (
    AuthProviderCapability,
    CapabilityDescriptor,
    CapabilityHealth,
    CapabilityRegistry,
    ContextCapability,
    DeliveryAdapterCapability,
    MemoryCapability,
    ModelProviderCapability,
    PlanningCapability,
    SkillCapability,
    StorageBackendCapability,
    TelemetrySinkCapability,
    ToolCapability,
)

__all__ = [
    "AuthProviderCapability",
    "CAPABILITY_SURFACES",
    "CapabilityDescriptor",
    "CapabilityHealth",
    "CapabilityRegistry",
    "ContextCapability",
    "DeliveryAdapterCapability",
    "MemoryCapability",
    "ModelProviderCapability",
    "PlanningCapability",
    "SkillCapability",
    "StorageBackendCapability",
    "TelemetrySinkCapability",
    "ToolCapability",
]
