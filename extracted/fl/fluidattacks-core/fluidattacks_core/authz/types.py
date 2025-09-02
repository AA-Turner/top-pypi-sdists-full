from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from typing import (
    Literal,
    TypedDict,
)

AuthzType = Literal[
    "admin",
    "user",
    "organization",
    "group",
    "root",
]

AuthzRelation = Literal[
    "admin",
    "parent",
    "customer_manage",
    "customer_write",
    "customer_read",
    "fluid_manage",
    "fluid_write",
    "fluid_read",
    "manage",
    "write",
    "read",
]


@dataclass(frozen=True, kw_only=True)
class AuthzConditionFluidEmail:
    email: str

    class _ReturnTypeContext(TypedDict):
        email: str

    class _ReturnType(TypedDict):
        name: Literal["fluid_email"]
        context: AuthzConditionFluidEmail._ReturnTypeContext

    def __call__(self) -> _ReturnType:
        return {
            "name": "fluid_email",
            "context": {"email": self.email},
        }


@dataclass(frozen=True, kw_only=True)
class AuthzTuple:
    user_type: AuthzType
    user: str
    relation: AuthzRelation
    object_type: AuthzType
    object: str
    condition: AuthzConditionFluidEmail | None = None

    class _ReturnType(TypedDict):
        user: str
        relation: AuthzRelation
        object: str
        condition: AuthzConditionFluidEmail._ReturnType | None

    def __call__(self) -> _ReturnType:
        return {
            "user": f"{self.user_type}:{self.user}",
            "relation": self.relation,
            "object": f"{self.object_type}:{self.object}",
            "condition": self.condition() if self.condition else None,
        }
