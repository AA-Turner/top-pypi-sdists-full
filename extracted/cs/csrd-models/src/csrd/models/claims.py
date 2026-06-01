from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta


@dataclass
class UserClaims:
    """Generic user claims for API authentication."""

    sub: str = ""
    user_name: str = ""
    authorities: list[str] = field(default_factory=list)
    iat: datetime = field(default_factory=lambda: datetime.now(UTC))
    exp: datetime | None = None

    def __post_init__(self) -> None:
        if self.user_name == "" and self.sub != "":
            self.user_name = self.sub
        if self.exp is None:
            self.exp = self.iat + timedelta(hours=1)


__all__ = ("UserClaims",)
