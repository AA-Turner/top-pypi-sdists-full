"""Base interface for signature verification."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from runlayer_cli.verified_local_proxy.config import VerificationConfig


@dataclass
class ProcessInfo:
    """Information about a process discovered on a port."""

    pid: int
    binary_path: str
    name: str | None = None


class SignatureVerifier(ABC):
    """Abstract base class for platform-specific signature verification."""

    @abstractmethod
    def find_process_on_port(self, port: int) -> ProcessInfo | None:
        """
        Find the process listening on the specified port.

        Args:
            port: Port number to check

        Returns:
            ProcessInfo if a process is found, None otherwise
        """
        pass

    @abstractmethod
    def verify_signature(
        self,
        process_info: ProcessInfo,
        config: VerificationConfig,
    ) -> None:
        """
        Verify the process signature matches expected config.

        Args:
            process_info: Information about the process to verify
            config: Expected verification configuration

        Raises:
            VerificationError: If signature verification fails
        """
        pass
