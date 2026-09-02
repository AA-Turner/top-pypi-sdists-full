from abc import ABC, abstractmethod


class AbstractFlow(ABC):
    """Abstract Base Class for Flow Components.
    All Flow Components should inherit from this class and implement the
    abstract methods defined here.

    :interface: true
    """

    @abstractmethod
    async def start(self, **kwargs):
        """Start Method called on every component.
        """

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    async def run(self):
        """Execute the code for component.
        """
