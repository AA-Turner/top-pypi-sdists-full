from typing import Literal, TypeGuard

Operation = Literal[
    "!=",
    "<",
    "<=",
    "==",
    ">",
    ">=",
    "and",
    "in",
    "is_near_cos",
    "is_near_ip",
    "is_near_l2",
    "not in",
    "not",
    "or",
]


def is_valid_operation(operation: str) -> TypeGuard[Operation]:
    return operation in (
        "!=",
        "<",
        "<=",
        "==",
        ">",
        ">=",
        "and",
        "in",
        "is_near_cos",
        "is_near_ip",
        "is_near_l2",
        "not in",
        "not",
        "or",
    )
