from typing import List, Optional

from anyscale._private.sdk import sdk_command
from anyscale.role._private.role_sdk import PrivateRoleSDK
from anyscale.role.models import Role


_ROLE_SDK_SINGLETON_KEY = "role_sdk"

_LIST_EXAMPLE = """
import anyscale

# Every role the organization can assign, its own and the built-in ones
for role in anyscale.role.list():
    print(role.id, role.name, "System" if role.built_in else "Custom")
"""

_GET_EXAMPLE = """
import anyscale

role = anyscale.role.get(role_id="rol_abc123")
print(role.name, role.allowed_permissions, role.denied_permissions)
"""

_GET_ARG_DOCSTRINGS = {
    "role_id": "The id of the role to read.",
}

_LIST_ARG_DOCSTRINGS = {
    "name": "Only roles whose name contains this text.",
    "include_archived": "Include archived roles, which cannot be newly assigned.",
    "max_items": "Maximum number of roles to return. None reads every page.",
}


@sdk_command(
    _ROLE_SDK_SINGLETON_KEY,
    PrivateRoleSDK,
    doc_py_example=_LIST_EXAMPLE,
    arg_docstrings=_LIST_ARG_DOCSTRINGS,
)
def list(  # noqa: A001
    *,
    name: Optional[str] = None,
    include_archived: bool = False,
    max_items: Optional[int] = None,
    _private_sdk: PrivateRoleSDK,
) -> List[Role]:
    """Roles the caller's organization can assign."""
    return _private_sdk.list(
        name=name,
        include_archived=include_archived,
        max_items=max_items,
    )


@sdk_command(
    _ROLE_SDK_SINGLETON_KEY,
    PrivateRoleSDK,
    doc_py_example=_GET_EXAMPLE,
    arg_docstrings=_GET_ARG_DOCSTRINGS,
)
def get(*, role_id: str, _private_sdk: PrivateRoleSDK) -> Role:
    """One role, with the permissions it grants and denies."""
    return _private_sdk.get(role_id=role_id)
