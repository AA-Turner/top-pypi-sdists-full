from abc import abstractmethod
from typing import TYPE_CHECKING

from connector.generated import StandardCapabilityName

if TYPE_CHECKING:
    from connector.oai.integration import Integration


class BaseIntegrationModule:
    """
    Base class for all integration modules.
    Integration modules allow you to register "global" capabilities that are not specific to a particular integration.
    """

    capabilities: list[StandardCapabilityName | str]

    def __init__(self):
        self.capabilities = []

    def add_capability(self, capability: str):
        """Add a capability to the module."""
        self.capabilities.append(capability)

    def get_capability(self, capability: str) -> StandardCapabilityName | str | None:
        """Get a capability from the module."""
        for cap in self.capabilities:
            if cap == capability:
                return cap
        return None

    @abstractmethod
    def register(self, integration: "Integration"):
        """Register all capabilities of the module / the module."""
        pass
