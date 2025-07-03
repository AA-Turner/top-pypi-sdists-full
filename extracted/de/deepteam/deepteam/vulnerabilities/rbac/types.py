from enum import Enum
from typing import Literal


class RBACType(Enum):
    ROLE_BYPASS = "role bypass"
    PRIVILEGE_ESCALATION = "privilege escalation"
    UNAUTHORIZED_ROLE_ASSUMPTION = "unauthorized role assumption"


RBACTypes = Literal[
    RBACType.ROLE_BYPASS.value,
    RBACType.PRIVILEGE_ESCALATION.value,
    RBACType.UNAUTHORIZED_ROLE_ASSUMPTION.value,
]
