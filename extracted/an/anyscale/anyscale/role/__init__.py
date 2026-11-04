from typing import List, Optional

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk import sdk_docs
from anyscale._private.sdk.base_sdk import Timer
from anyscale.cli_logger import BlockLogger
from anyscale.role._private.role_sdk import PrivateRoleSDK
from anyscale.role.commands import (
    _GET_ARG_DOCSTRINGS,
    _GET_EXAMPLE,
    _LIST_ARG_DOCSTRINGS,
    _LIST_EXAMPLE,
    get as get,
    list as list,  # noqa: A004
)
from anyscale.role.models import Role


class RoleSDK:
    def __init__(
        self,
        *,
        client: Optional[AnyscaleClientInterface] = None,
        logger: Optional[BlockLogger] = None,
        timer: Optional[Timer] = None,
    ):
        self._private_sdk = PrivateRoleSDK(client=client, logger=logger, timer=timer)

    @sdk_docs(
        doc_py_example=_LIST_EXAMPLE,
        arg_docstrings=_LIST_ARG_DOCSTRINGS,
    )
    def list(  # noqa: F811
        self,
        *,
        name: Optional[str] = None,
        include_archived: bool = False,
        max_items: Optional[int] = None,
    ) -> List[Role]:
        """Roles the caller's organization can assign."""
        return self._private_sdk.list(
            name=name,
            include_archived=include_archived,
            max_items=max_items,
        )

    @sdk_docs(
        doc_py_example=_GET_EXAMPLE,
        arg_docstrings=_GET_ARG_DOCSTRINGS,
    )
    def get(self, *, role_id: str) -> Role:  # noqa: F811
        """One role, with the permissions it grants and denies."""
        return self._private_sdk.get(role_id=role_id)


__all__ = [
    "Role",
    "RoleSDK",
    "get",
    "list",
]
