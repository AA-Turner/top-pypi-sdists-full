"""BACore protocols."""
from typing import Protocol, runtime_checkable


class Exists(Protocol):
    """Protocol for verification of existing."""

    def exists(self) -> bool:
        """Verify if exists."""
        ...


@runtime_checkable
class SupportsRetrieveDict(Protocol):
    """Protocol for retrieval of file content as dict."""

    def data_to_dict(self) -> dict:
        """Content as dictionary."""
        ...
