"""
Common utilities and models for Vortex clients.

This module provides shared functionality used by all Vortex client types.
"""

from .exceptions import ValidationError, VortexClientError

__all__ = ["ValidationError", "VortexClientError"]
