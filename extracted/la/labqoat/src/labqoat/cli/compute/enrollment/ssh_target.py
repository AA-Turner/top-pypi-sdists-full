"""Administrator-selected SSH destination with host-key verification always enforced."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SshTarget:
    """Build ssh argument vectors that verify the host key and never prompt."""

    destination: str
    options: tuple[str, ...] = ()

    DESTINATION = re.compile(r"[A-Za-z0-9._-]+@[A-Za-z0-9._:\[\]-]+")
    OPTION = re.compile(r"[A-Za-z]+=\S+")
    RESERVED = frozenset({"stricthostkeychecking", "batchmode"})

    def __post_init__(self) -> None:
        """Reject option injection and any attempt to weaken host-key verification."""
        if self.DESTINATION.fullmatch(self.destination) is None:
            raise ValueError(f"SSH destination must look like user@host, not {self.destination!r}")
        for option in self.options:
            self.validate_option(option)

    def validate_option(self, option: str) -> None:
        """Allow ordinary KEY=VALUE options except those that disable verification or prompting."""
        if self.OPTION.fullmatch(option) is None:
            raise ValueError(f"--ssh-option expects KEY=VALUE such as Port=2222, not {option!r}")
        key, _, value = option.partition("=")
        if key.lower() in self.RESERVED:
            raise ValueError(f"--ssh-option cannot override {key}; enrollment always verifies host keys")
        if key.lower().endswith("knownhostsfile") and value == "/dev/null":
            raise ValueError("--ssh-option cannot discard known host keys")

    def command(self, remote: str) -> list[str]:
        """Return the ssh invocation for one remote shell command."""
        selected = [part for option in self.options for part in ("-o", option)]
        verified = ["-o", "StrictHostKeyChecking=yes", "-o", "BatchMode=yes"]
        return ["ssh", *verified, *selected, "--", self.destination, remote]

    @staticmethod
    def privileged(command: str) -> str:
        """Run a remote command as root directly or through noninteractive sudo."""
        return f'if [ "$(id -u)" -eq 0 ]; then {command}; else sudo -n {command}; fi'
