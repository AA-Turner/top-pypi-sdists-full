"""
Semantic Kernel integration for Aigie.

This module provides automatic tracing for Microsoft Semantic Kernel,
the enterprise AI SDK for building AI-powered applications.

Usage:
    # Manual handler usage
    from aigie.integrations.semantic_kernel import SemanticKernelHandler

    handler = SemanticKernelHandler(trace_name="enterprise-ai")
    # ... use with semantic_kernel

    # Auto-instrumentation
    from aigie.integrations.semantic_kernel import patch_semantic_kernel
    patch_semantic_kernel()  # Patches Kernel.invoke(), planners, etc.
"""

from .auto_instrument import (
    is_semantic_kernel_patched,
    patch_semantic_kernel,
    unpatch_semantic_kernel,
)
from .config import SemanticKernelConfig
from .handler import SemanticKernelHandler

__all__ = [
    "SemanticKernelConfig",
    "SemanticKernelHandler",
    "is_semantic_kernel_patched",
    "patch_semantic_kernel",
    "unpatch_semantic_kernel",
]
