"""Canonical resource identities used by authored workflows."""

from typing import Self
from uuid import UUID


class ResourceId(str):
    """A UUID identity independent of its storage location; it is its own canonical text, so JSON takes it as is."""

    __slots__ = ()

    def __new__(cls, value: UUID | str) -> Self:
        """Hold the canonical lowercase text of `value`."""
        return super().__new__(cls, str(value if isinstance(value, UUID) else UUID(value)))

    @classmethod
    def parse(cls, value: str) -> Self:
        """Parse a canonical lowercase UUID."""
        parsed = UUID(value)
        if str(parsed) != value:
            raise ValueError("Expected a canonical lowercase UUID")
        return cls(parsed)

    @property
    def value(self) -> UUID:
        """The identity as a UUID."""
        return UUID(self)
