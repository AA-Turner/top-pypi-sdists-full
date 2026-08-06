"""The contract every ecosystem implements to carry the registry credential.

Three implementations follow it — :mod:`npm`, :mod:`uv`, :mod:`docker` — and
the wiring layer drives them all through this interface. That matters for
rotation: rotating invalidates the old token, so the new value must be re-posed
in **every** ecosystem that already holds one, which is only expressible if
they are interchangeable.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from .targets import RegistryTargets


@dataclass
class ConsumerState:
    """Whether an ecosystem currently holds the credential, and where.

    ``configured`` answers "is a credential posed here", not "is it valid" —
    validity is a property of the token itself, established once by
    :func:`pysae_ai_tools.common.registry_auth.pat.token_info` and shared by
    every consumer rather than re-probed per ecosystem.
    """

    name: str
    configured: bool = False
    locations: tuple[str, ...] = ()
    detail: str = ""

    def to_dict(self) -> dict[str, object]:
        out: dict[str, object] = {"configured": self.configured}
        if self.locations:
            out["locations"] = list(self.locations)
        if self.detail:
            out["detail"] = self.detail
        return out


@dataclass
class ApplyResult:
    """Outcome of posing the credential in one ecosystem."""

    changed: bool = False
    locations: tuple[str, ...] = field(default_factory=tuple)
    error: str = ""

    @property
    def ok(self) -> bool:
        return not self.error


class RegistryConsumer(ABC):
    """One ecosystem whose configuration the credential is written into."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Ecosystem name as reported in ``tools status --json`` (e.g. ``node``)."""

    @abstractmethod
    def state(self, targets: RegistryTargets) -> ConsumerState:
        """Report whether the credential is posed here, without revealing it."""

    @abstractmethod
    def apply(self, token: str, targets: RegistryTargets) -> ApplyResult:
        """Pose (or re-pose) ``token``. Idempotent: a no-change run reports
        ``changed=False`` and rewrites nothing."""

    @abstractmethod
    def remove(self, targets: RegistryTargets) -> tuple[str, ...]:
        """Strip what this consumer wrote, leaving the rest of each file alone.
        Returns the locations actually cleaned."""
