"""List of possible functions for known operations."""
import re

DESCRIBE_FUNCTIONS = ["get", "head", "search", "describe"]

LIST_FUNCTIONS = ["list", "describe", "search", "get"]

DELETE_FUNCTIONS = [
    "delete",
    "disassociate",
    "reject",
    "deallocate",
    "unassign",
    "deregister",
    "deprovision",
    "revoke",
    "release",
    "terminate",
    "cancel",
    "disable",
]

CREATE_FUNCTIONS = [
    "create",
    "associate",
    "accept",
    "allocate",
    "assign",
    "register",
    "provision",
    "authorize",
    "run",
    "enable",
    "put",
    "publish",
    "request",
    "put",
    "add",
    "apply",
]

UPDATE_FUNCTIONS = ["modify", "update", "put", "apply"]


def get_possible_func_type(hub, resource_name: str, operation: str):
    if re.match(
        _get_regex_pattern(DESCRIBE_FUNCTIONS), operation
    ) and operation.endswith(resource_name):
        return "get"

    if (
        re.match(_get_regex_pattern(LIST_FUNCTIONS), operation)
        and (
            operation.endswith(f"{resource_name}s")
            or operation.endswith(f"{resource_name}es")
        )
    ) or re.match("(describe).*", operation):
        return "list"

    if re.match(_get_regex_pattern(CREATE_FUNCTIONS), operation):
        return "create"

    if re.match(_get_regex_pattern(UPDATE_FUNCTIONS), operation):
        return "update"

    if re.match(_get_regex_pattern(DELETE_FUNCTIONS), operation):
        return "delete"

    return "tools"


def _get_regex_pattern(possible_function):
    regex_str = "|".join(possible_function)
    regex_str = f"({regex_str}).*"
    return regex_str
