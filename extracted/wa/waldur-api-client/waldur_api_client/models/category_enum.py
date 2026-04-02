from enum import Enum


class CategoryEnum(str, Enum):
    APPROVE = "approve"
    BACKUP = "backup"
    CONFIGURE = "configure"
    CONTACT = "contact"
    ESCALATE = "escalate"
    EXTEND = "extend"
    MIGRATE = "migrate"
    MONITOR = "monitor"
    REJECT = "reject"
    REPAIR = "repair"
    TERMINATE = "terminate"
    VIEW = "view"

    def __str__(self) -> str:
        return str(self.value)
