"""Where sandboxes start for code that does not say."""

import os

from labqoat.sandbox.sandbox_client import SandboxClient
from labqoat.sandbox.sandbox_platform import SandboxPlatform
from labqoat.sandbox.sandbox_route import SandboxRoute


class SandboxReach:
    """Prefer the sandbox host a worker was launched beside or pointed at; anywhere else, the platform places them.

    A function that declares ``sandboxes=[...]`` has its own host's socket, and ``LABQOAT_SANDBOX_URL`` points a
    process at a host another run serves. Without either, sandboxes are the platform's.
    """

    @staticmethod
    def nearest() -> SandboxClient | SandboxPlatform:
        """Return the client of the host this process has, or the platform."""
        if os.environ.get(SandboxRoute.SOCKET_VARIABLE) or os.environ.get(SandboxRoute.URL_VARIABLE):
            return SandboxClient()
        return SandboxPlatform.default()
