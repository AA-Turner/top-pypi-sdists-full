"""Secret models."""

from __future__ import annotations

from dataclasses import dataclass, field

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
