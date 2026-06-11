"""
Type annotations for signin service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signin/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_signin.client import SignInServiceClient

    session = Session()
    client: SignInServiceClient = session.client("signin")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListResourcePermissionStatementsPaginator
from .type_defs import (
    CreateOAuth2TokenRequestTypeDef,
    CreateOAuth2TokenResponseTypeDef,
    DeleteConsoleAuthorizationConfigurationInputTypeDef,
    DeleteConsoleAuthorizationConfigurationOutputTypeDef,
    DeleteResourcePermissionStatementInputTypeDef,
    GetConsoleAuthorizationConfigurationInputTypeDef,
    GetConsoleAuthorizationConfigurationOutputTypeDef,
    GetResourcePolicyOutputTypeDef,
    ListResourcePermissionStatementsInputTypeDef,
    ListResourcePermissionStatementsOutputTypeDef,
    PutConsoleAuthorizationConfigurationInputTypeDef,
    PutConsoleAuthorizationConfigurationOutputTypeDef,
    PutResourcePermissionStatementInputTypeDef,
    PutResourcePermissionStatementOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("SignInServiceClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    TooManyRequestsError: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class SignInServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signin.html#SignInService.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signin/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SignInServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signin.html#SignInService.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signin/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signin/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signin/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signin/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signin/client/#generate_presigned_url)
        """

    def create_o_auth2_token(
        self, **kwargs: Unpack[CreateOAuth2TokenRequestTypeDef]
    ) -> CreateOAuth2TokenResponseTypeDef:
        """
        CreateOAuth2Token API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signin/client/create_o_auth2_token.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signin/client/#create_o_auth2_token)
        """

    def delete_console_authorization_configuration(
        self, **kwargs: Unpack[DeleteConsoleAuthorizationConfigurationInputTypeDef]
    ) -> DeleteConsoleAuthorizationConfigurationOutputTypeDef:
        """
        Delete console authorization configuration with automatic scope detection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signin/client/delete_console_authorization_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signin/client/#delete_console_authorization_configuration)
        """

    def delete_resource_permission_statement(
        self, **kwargs: Unpack[DeleteResourcePermissionStatementInputTypeDef]
    ) -> dict[str, Any]:
        """
        Remove a permission statement from the account's SignIn resource-based policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signin/client/delete_resource_permission_statement.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signin/client/#delete_resource_permission_statement)
        """

    def get_console_authorization_configuration(
        self, **kwargs: Unpack[GetConsoleAuthorizationConfigurationInputTypeDef]
    ) -> GetConsoleAuthorizationConfigurationOutputTypeDef:
        """
        Get console authorization configuration with automatic scope detection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signin/client/get_console_authorization_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signin/client/#get_console_authorization_configuration)
        """

    def get_resource_policy(self) -> GetResourcePolicyOutputTypeDef:
        """
        Retrieve the account's consolidated SignIn resource-based policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signin/client/get_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signin/client/#get_resource_policy)
        """

    def list_resource_permission_statements(
        self, **kwargs: Unpack[ListResourcePermissionStatementsInputTypeDef]
    ) -> ListResourcePermissionStatementsOutputTypeDef:
        """
        Retrieve all permission statements in the account's SignIn resource-based
        policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signin/client/list_resource_permission_statements.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signin/client/#list_resource_permission_statements)
        """

    def put_console_authorization_configuration(
        self, **kwargs: Unpack[PutConsoleAuthorizationConfigurationInputTypeDef]
    ) -> PutConsoleAuthorizationConfigurationOutputTypeDef:
        """
        Enable console authorization configuration with automatic scope detection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signin/client/put_console_authorization_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signin/client/#put_console_authorization_configuration)
        """

    def put_resource_permission_statement(
        self, **kwargs: Unpack[PutResourcePermissionStatementInputTypeDef]
    ) -> PutResourcePermissionStatementOutputTypeDef:
        """
        Create a permission statement in the account's SignIn resource-based policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signin/client/put_resource_permission_statement.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signin/client/#put_resource_permission_statement)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_resource_permission_statements"]
    ) -> ListResourcePermissionStatementsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signin/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signin/client/#get_paginator)
        """
