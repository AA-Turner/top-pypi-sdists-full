"""
Type annotations for account-access-runtime service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account_access_runtime/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_account_access_runtime.client import AccountAccessRuntimeClient

    session = Session()
    client: AccountAccessRuntimeClient = session.client("account-access-runtime")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListRolesPaginator
from .type_defs import (
    GetRoleCredentialsRequestTypeDef,
    GetRoleCredentialsResponseTypeDef,
    ListRolesRequestTypeDef,
    ListRolesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("AccountAccessRuntimeClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    UnauthorizedException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class AccountAccessRuntimeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access-runtime.html#AccountAccessRuntime.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account_access_runtime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AccountAccessRuntimeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access-runtime.html#AccountAccessRuntime.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account_access_runtime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access-runtime/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account_access_runtime/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access-runtime/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account_access_runtime/client/#generate_presigned_url)
        """

    def get_role_credentials(
        self, **kwargs: Unpack[GetRoleCredentialsRequestTypeDef]
    ) -> GetRoleCredentialsResponseTypeDef:
        """
        Returns temporary Amazon Web Services credentials for a role that you are
        entitled to assume within a tenant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access-runtime/client/get_role_credentials.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account_access_runtime/client/#get_role_credentials)
        """

    def list_roles(self, **kwargs: Unpack[ListRolesRequestTypeDef]) -> ListRolesResponseTypeDef:
        """
        Returns the roles that you are entitled to access within a tenant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access-runtime/client/list_roles.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account_access_runtime/client/#list_roles)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_roles"]
    ) -> ListRolesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access-runtime/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account_access_runtime/client/#get_paginator)
        """
