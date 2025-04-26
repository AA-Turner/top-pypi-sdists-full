"""
Type annotations for sts service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sts.client import STSClient

    session = get_session()
    async with session.create_client("sts") as client:
        client: STSClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    AssumeRoleRequestTypeDef,
    AssumeRoleResponseTypeDef,
    AssumeRoleWithSAMLRequestTypeDef,
    AssumeRoleWithSAMLResponseTypeDef,
    AssumeRoleWithWebIdentityRequestTypeDef,
    AssumeRoleWithWebIdentityResponseTypeDef,
    AssumeRootRequestTypeDef,
    AssumeRootResponseTypeDef,
    DecodeAuthorizationMessageRequestTypeDef,
    DecodeAuthorizationMessageResponseTypeDef,
    GetAccessKeyInfoRequestTypeDef,
    GetAccessKeyInfoResponseTypeDef,
    GetCallerIdentityResponseTypeDef,
    GetFederationTokenRequestTypeDef,
    GetFederationTokenResponseTypeDef,
    GetSessionTokenRequestTypeDef,
    GetSessionTokenResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack

__all__ = ("STSClient",)

class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    ExpiredTokenException: Type[BotocoreClientError]
    IDPCommunicationErrorException: Type[BotocoreClientError]
    IDPRejectedClaimException: Type[BotocoreClientError]
    InvalidAuthorizationMessageException: Type[BotocoreClientError]
    InvalidIdentityTokenException: Type[BotocoreClientError]
    MalformedPolicyDocumentException: Type[BotocoreClientError]
    PackedPolicyTooLargeException: Type[BotocoreClientError]
    RegionDisabledException: Type[BotocoreClientError]

class STSClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        STSClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#generate_presigned_url)
        """

    async def assume_role(
        self, **kwargs: Unpack[AssumeRoleRequestTypeDef]
    ) -> AssumeRoleResponseTypeDef:
        """
        Returns a set of temporary security credentials that you can use to access
        Amazon Web Services resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/assume_role.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#assume_role)
        """

    async def assume_role_with_saml(
        self, **kwargs: Unpack[AssumeRoleWithSAMLRequestTypeDef]
    ) -> AssumeRoleWithSAMLResponseTypeDef:
        """
        Returns a set of temporary security credentials for users who have been
        authenticated via a SAML authentication response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/assume_role_with_saml.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#assume_role_with_saml)
        """

    async def assume_role_with_web_identity(
        self, **kwargs: Unpack[AssumeRoleWithWebIdentityRequestTypeDef]
    ) -> AssumeRoleWithWebIdentityResponseTypeDef:
        """
        Returns a set of temporary security credentials for users who have been
        authenticated in a mobile or web application with a web identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/assume_role_with_web_identity.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#assume_role_with_web_identity)
        """

    async def assume_root(
        self, **kwargs: Unpack[AssumeRootRequestTypeDef]
    ) -> AssumeRootResponseTypeDef:
        """
        Returns a set of short term credentials you can use to perform privileged tasks
        on a member account in your organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/assume_root.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#assume_root)
        """

    async def decode_authorization_message(
        self, **kwargs: Unpack[DecodeAuthorizationMessageRequestTypeDef]
    ) -> DecodeAuthorizationMessageResponseTypeDef:
        """
        Decodes additional information about the authorization status of a request from
        an encoded message returned in response to an Amazon Web Services request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/decode_authorization_message.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#decode_authorization_message)
        """

    async def get_access_key_info(
        self, **kwargs: Unpack[GetAccessKeyInfoRequestTypeDef]
    ) -> GetAccessKeyInfoResponseTypeDef:
        """
        Returns the account identifier for the specified access key ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/get_access_key_info.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#get_access_key_info)
        """

    async def get_caller_identity(self) -> GetCallerIdentityResponseTypeDef:
        """
        Returns details about the IAM user or role whose credentials are used to call
        the operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/get_caller_identity.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#get_caller_identity)
        """

    async def get_federation_token(
        self, **kwargs: Unpack[GetFederationTokenRequestTypeDef]
    ) -> GetFederationTokenResponseTypeDef:
        """
        Returns a set of temporary security credentials (consisting of an access key
        ID, a secret access key, and a security token) for a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/get_federation_token.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#get_federation_token)
        """

    async def get_session_token(
        self, **kwargs: Unpack[GetSessionTokenRequestTypeDef]
    ) -> GetSessionTokenResponseTypeDef:
        """
        Returns a set of temporary credentials for an Amazon Web Services account or
        IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/get_session_token.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#get_session_token)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/)
        """
