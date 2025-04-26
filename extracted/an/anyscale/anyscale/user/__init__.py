from typing import List, Optional

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk import sdk_docs
from anyscale._private.sdk.base_sdk import Timer
from anyscale.cli_logger import BlockLogger
from anyscale.user._private.user_sdk import PrivateUserSDK
from anyscale.user.commands import (
    _ADMIN_BATCH_CREATE_ARG_DOCSTRINGS,
    _ADMIN_BATCH_CREATE_EXAMPLE,
    admin_batch_create,
)
from anyscale.user.models import AdminCreatedUser, AdminCreateUser


class UserSDK:
    def __init__(
        self,
        *,
        client: Optional[AnyscaleClientInterface] = None,
        logger: Optional[BlockLogger] = None,
        timer: Optional[Timer] = None,
    ):
        self._private_sdk = PrivateUserSDK(client=client, logger=logger, timer=timer)

    @sdk_docs(
        doc_py_example=_ADMIN_BATCH_CREATE_EXAMPLE,
        arg_docstrings=_ADMIN_BATCH_CREATE_ARG_DOCSTRINGS,
    )
    def admin_batch_create(  # noqa: F811
        self, admin_create_users: List[AdminCreateUser],
    ) -> List[AdminCreatedUser]:
        """Batch create, as an admin, users without email verification.
        """
        return self._private_sdk.admin_batch_create(admin_create_users)
