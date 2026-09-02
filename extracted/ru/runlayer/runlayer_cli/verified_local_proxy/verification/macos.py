"""macOS code signing verification using codesign."""

from __future__ import annotations

import os
import subprocess

import structlog

from runlayer_cli import regex_safe
from runlayer_cli.verified_local_proxy.config import VerificationConfig
from runlayer_cli.verified_local_proxy.exceptions import VerificationError
from runlayer_cli.verified_local_proxy.verification.base import (
    ProcessInfo,
    SignatureVerifier,
)

logger = structlog.get_logger(__name__)

# Absolute paths to system binaries to prevent PATH hijacking attacks
LSOF_PATH = "/usr/sbin/lsof"
CODESIGN_PATH = "/usr/bin/codesign"
PS_PATH = "/bin/ps"


def _verify_system_binary(path: str) -> None:
    """Verify a system binary exists and is in a protected location."""
    if not os.path.isfile(path):
        raise VerificationError(f"Required system binary not found: {path}")
    # Verify the binary is in a system-protected directory
    # (SIP protects /usr/bin, /usr/sbin, /bin on macOS)
    protected_prefixes = ("/usr/bin/", "/usr/sbin/", "/bin/", "/sbin/")
    if not any(path.startswith(p) for p in protected_prefixes):
        raise VerificationError(f"System binary not in protected location: {path}")


class MacOSVerifier(SignatureVerifier):
    """macOS signature verification using codesign."""

    def find_process_on_port(self, port: int) -> ProcessInfo | None:
        """Find process listening on port using lsof."""
        try:
            _verify_system_binary(LSOF_PATH)
            result = subprocess.run(
                [LSOF_PATH, f"-iTCP:{port}", "-sTCP:LISTEN", "-n", "-P"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0 or not result.stdout.strip():
                return None

            # Parse lsof output
            # Format: COMMAND  PID  USER  FD  TYPE  ...
            lines = result.stdout.strip().split("\n")
            if len(lines) < 2:
                return None

            # Skip header, get first data line
            parts = lines[1].split()
            if len(parts) < 2:
                return None

            command = parts[0]
            pid = int(parts[1])

            # Get binary path from PID
            binary_path = self._get_binary_path(pid)

            return ProcessInfo(
                pid=pid,
                binary_path=binary_path,
                name=command,
            )

        except subprocess.TimeoutExpired:
            logger.warning("lsof command timed out")
            return None
        except (ValueError, IndexError) as e:
            logger.error(f"Error parsing lsof output: {e}")
            return None
        except Exception as e:
            logger.error(f"Error finding process on port {port}: {e}")
            return None

    def _get_binary_path(self, pid: int) -> str:
        """Get the binary path for a PID."""
        # Try using ps to get the full path
        _verify_system_binary(PS_PATH)
        result = subprocess.run(
            [PS_PATH, "-p", str(pid), "-o", "comm="],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0 and result.stdout.strip():
            path = result.stdout.strip()
            # ps -o comm= may truncate, try lsof for full path
            if "/" in path:
                return path

        # Use lsof to find the executable
        _verify_system_binary(LSOF_PATH)
        result = subprocess.run(
            [LSOF_PATH, "-p", str(pid), "-Fn"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        for line in result.stdout.split("\n"):
            # Lines starting with 'n' contain file names
            if line.startswith("n/") and ".app" in line:
                # Extract the .app path
                path = line[1:]  # Remove 'n' prefix
                return path

        raise VerificationError(f"Could not determine binary path for PID {pid}")

    def verify_signature(
        self,
        process_info: ProcessInfo,
        config: VerificationConfig,
    ) -> None:
        """Verify code signature using codesign."""
        binary_path = process_info.binary_path

        # Check expected paths if configured (match binary path or its parent .app bundle)
        if config.expected_binary_paths:
            app_path = self._extract_app_bundle_path(binary_path)
            path_match = any(
                self._is_path_under(binary_path, expected)
                or (app_path and self._is_path_under(app_path, expected))
                for expected in config.expected_binary_paths
            )
            if not path_match:
                raise VerificationError(
                    f"Binary path {binary_path} not in expected paths: "
                    f"{config.expected_binary_paths}"
                )

        # Verify the binary directly (not .app bundle - avoids sealed resource issues)
        verify_path = binary_path

        # Verify the signature is valid
        # By default, --ignore-resources is used because Electron apps (like Figma) can have
        # sealed resource issues after updates, but the binary's code signature is still valid.
        # Set macos_strict_resource_check=True to also verify sealed resources.
        _verify_system_binary(CODESIGN_PATH)
        codesign_args = [CODESIGN_PATH, "--verify", "--verbose=2"]
        if not config.macos_strict_resource_check:
            codesign_args.insert(2, "--ignore-resources")
        codesign_args.append(verify_path)
        result = subprocess.run(
            codesign_args,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            raise VerificationError(
                f"Code signature invalid for {verify_path}: {result.stderr}"
            )

        # Get signature details
        result = subprocess.run(
            [CODESIGN_PATH, "-dv", "--verbose=4", verify_path],
            capture_output=True,
            text=True,
            timeout=30,
        )

        # codesign outputs to stderr
        output = result.stderr

        # Parse all Authority entries in the certificate chain
        authorities = regex_safe.findall(r"Authority=(.+)", output)
        if not authorities:
            raise VerificationError(
                f"Could not find Authority in codesign output for {verify_path}"
            )

        # Verify the signing authority (first in chain) - exact match to prevent spoofing
        if config.macos_authority:
            if authorities[0] != config.macos_authority:
                raise VerificationError(
                    f"Authority mismatch: expected '{config.macos_authority}', "
                    f"got '{authorities[0]}'"
                )

        # Verify the root CA is trusted (prevents risky CA attacks)
        # The certificate chain should end with a trusted root CA like "Apple Root CA"
        # Use exact match on last authority (root) to prevent spoofing with names like "Fake Apple Root CA"
        if config.macos_root_ca:
            root_ca = authorities[-1] if authorities else ""
            if root_ca != config.macos_root_ca:
                raise VerificationError(
                    f"Root CA mismatch: expected '{config.macos_root_ca}', "
                    f"got '{root_ca}'. Chain: {authorities}. This may indicate a risky certificate."
                )

        logger.info(f"Signature verified for {verify_path}")

    def _extract_app_bundle_path(self, path: str) -> str | None:
        """Extract the .app bundle path from a binary path.

        Only matches .app when followed by / to prevent attacks like:
        /Applications/Legit.app.evil/Contents/MacOS/binary
        """
        # Require .app to be followed by / (a real directory, not .app.evil).
        # RE2 has no lookahead, so the old `(.+\.app)(?=/)` consumes the `/`
        # instead; group(1) — the only thing read — is unchanged (greedy `.+`
        # still picks the rightmost `.app` that has a following `/`).
        match = regex_safe.search(r"(.+\.app)/", path)
        if match:
            return match.group(1)
        return None

    def _is_path_under(self, path: str, expected: str) -> bool:
        """
        Check if path is exactly expected or is under expected directory.

        Prevents path prefix attacks like /Applications/Figma.app.evil
        passing a check for /Applications/Figma.app.
        """
        # Exact match
        if path == expected:
            return True
        # Path is under expected (must have / separator after expected)
        # Normalize expected to not end with /
        expected_normalized = expected.rstrip("/")
        return path.startswith(expected_normalized + "/")
