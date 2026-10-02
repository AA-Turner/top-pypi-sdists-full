import enum
from dataclasses import dataclass


class HushStatus(enum.Enum):
    FULL = "full"
    PARTIAL = "partial"
    NONE = "none"


@dataclass
class SettingResult:
    name: str
    connection: str
    suppressed: bool
    original_value: str | None
    error: str | None


@dataclass
class HushResult:
    status: HushStatus
    details: list[SettingResult]

    def __bool__(self) -> bool:
        return self.status == HushStatus.FULL
