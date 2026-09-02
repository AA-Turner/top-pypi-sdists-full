"""Secret models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SecretMetadata:
    """Metadata about a secret."""
    id: str = ""
    keys: list[str] = field(default_factory=list)
    created_at: str | None = None
    updated_at: str | None = None

    @classmethod
    def _from_dict(cls, d: dict) -> SecretMetadata:
        return cls(
            id=d.get("id", ""),
            keys=d.get("keys", []),
            created_at=d.get("createdAt"),
            updated_at=d.get("updatedAt"),
        )


@dataclass(frozen=True, repr=False)
class SecretValuePeek:
    """Returned values from creating/updating a secret."""
    id: str = ""
    values: dict[str, str] = field(default_factory=dict)

    def __repr__(self) -> str:
        masked = {k: "***" for k in self.values} if self.values else {}
        return f"SecretValuePeek(id={self.id!r}, values={masked})"

    @classmethod
    def _from_dict(cls, d: dict | None) -> SecretValuePeek | None:
        if not d:
            return None
        return cls(id=d.get("id", ""), values=d.get("values", {}))
