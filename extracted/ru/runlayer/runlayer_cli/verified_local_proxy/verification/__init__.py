"""Signature verification module."""

from __future__ import annotations

import sys

from runlayer_cli.verified_local_proxy.verification.base import (
    ProcessInfo,
    SignatureVerifier,
)

__all__ = ["get_verifier", "SignatureVerifier", "ProcessInfo"]


def get_verifier() -> SignatureVerifier:
    """
    Get the appropriate verifier for the current platform.

    Returns:
        Platform-specific SignatureVerifier instance

    Raises:
        RuntimeError: If the current platform is not supported
    """
    if sys.platform == "darwin":
        from runlayer_cli.verified_local_proxy.verification.macos import MacOSVerifier

        return MacOSVerifier()
    elif sys.platform == "win32":
        from runlayer_cli.verified_local_proxy.verification.windows import (
            WindowsVerifier,
        )

        return WindowsVerifier()
    else:
        raise RuntimeError(
            f"Unsupported platform: {sys.platform}. "
            "Only macOS and Windows are supported."
        )
