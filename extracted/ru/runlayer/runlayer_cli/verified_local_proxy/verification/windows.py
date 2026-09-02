"""Windows Authenticode signature verification - NOT IMPLEMENTED."""

from __future__ import annotations

from runlayer_cli.verified_local_proxy.config import VerificationConfig
from runlayer_cli.verified_local_proxy.exceptions import VerificationError
from runlayer_cli.verified_local_proxy.verification.base import (
    ProcessInfo,
    SignatureVerifier,
)


class WindowsVerifier(SignatureVerifier):
    """Windows signature verification - not yet implemented."""

    def find_process_on_port(self, port: int) -> ProcessInfo | None:
        """Find process listening on port - not implemented."""
        raise VerificationError(
            "Windows signature verification is not yet implemented. "
            "Please use macOS for now."
        )

    def verify_signature(
        self,
        process_info: ProcessInfo,
        config: VerificationConfig,
    ) -> None:
        """Verify Authenticode signature - not implemented."""
        raise VerificationError(
            "Windows signature verification is not yet implemented. "
            "Please use macOS for now."
        )
