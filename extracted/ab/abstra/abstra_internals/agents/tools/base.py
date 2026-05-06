from abc import ABC, abstractmethod


class AgentTools(ABC):
    """
    Abstract base class for agent toolkits. A toolkit groups a set of related Python methods that can be exposed to `run_agent` as a single `tools=[...]` entry.

    Subclass `AgentTools` and implement `__tools__()` to return the list of method names the agent may call. Each listed method must have type hints and a docstring — those become the tool's JSON schema and description.
    """

    def __init__(self):
        """
        Initialize the toolkit base. Subclasses define their own `__init__` with concrete configuration (allowed methods, URLs, globs, etc.).
        """
        super().__init__()

    @abstractmethod
    def __tools__(self) -> list[str]:
        raise NotImplementedError("You must implement the __tools__ method")
