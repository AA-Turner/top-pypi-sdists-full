"""
Type annotations for support-app service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support_app/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_support_app.client import SupportAppClient

    session = get_session()
    async with session.create_client("support-app") as client:
        client: SupportAppClient
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
    CreateSlackChannelConfigurationRequestTypeDef,
    DeleteSlackChannelConfigurationRequestTypeDef,
    DeleteSlackWorkspaceConfigurationRequestTypeDef,
    GetAccountAliasResultTypeDef,
    ListSlackChannelConfigurationsRequestTypeDef,
    ListSlackChannelConfigurationsResultTypeDef,
    ListSlackWorkspaceConfigurationsRequestTypeDef,
    ListSlackWorkspaceConfigurationsResultTypeDef,
    PutAccountAliasRequestTypeDef,
    RegisterSlackWorkspaceForOrganizationRequestTypeDef,
    RegisterSlackWorkspaceForOrganizationResultTypeDef,
    UpdateSlackChannelConfigurationRequestTypeDef,
    UpdateSlackChannelConfigurationResultTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack

__all__ = ("SupportAppClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class SupportAppClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app.html#SupportApp.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support_app/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SupportAppClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app.html#SupportApp.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support_app/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support_app/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support_app/client/#generate_presigned_url)
        """

    async def create_slack_channel_configuration(
        self, **kwargs: Unpack[CreateSlackChannelConfigurationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a Slack channel configuration for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/create_slack_channel_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support_app/client/#create_slack_channel_configuration)
        """

    async def delete_account_alias(self) -> Dict[str, Any]:
        """
        Deletes an alias for an Amazon Web Services account ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/delete_account_alias.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support_app/client/#delete_account_alias)
        """

    async def delete_slack_channel_configuration(
        self, **kwargs: Unpack[DeleteSlackChannelConfigurationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Slack channel configuration from your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/delete_slack_channel_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support_app/client/#delete_slack_channel_configuration)
        """

    async def delete_slack_workspace_configuration(
        self, **kwargs: Unpack[DeleteSlackWorkspaceConfigurationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Slack workspace configuration from your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/delete_slack_workspace_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support_app/client/#delete_slack_workspace_configuration)
        """

    async def get_account_alias(self) -> GetAccountAliasResultTypeDef:
        """
        Retrieves the alias from an Amazon Web Services account ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/get_account_alias.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support_app/client/#get_account_alias)
        """

    async def list_slack_channel_configurations(
        self, **kwargs: Unpack[ListSlackChannelConfigurationsRequestTypeDef]
    ) -> ListSlackChannelConfigurationsResultTypeDef:
        """
        Lists the Slack channel configurations for an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/list_slack_channel_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support_app/client/#list_slack_channel_configurations)
        """

    async def list_slack_workspace_configurations(
        self, **kwargs: Unpack[ListSlackWorkspaceConfigurationsRequestTypeDef]
    ) -> ListSlackWorkspaceConfigurationsResultTypeDef:
        """
        Lists the Slack workspace configurations for an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/list_slack_workspace_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support_app/client/#list_slack_workspace_configurations)
        """

    async def put_account_alias(
        self, **kwargs: Unpack[PutAccountAliasRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates or updates an individual alias for each Amazon Web Services account ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/put_account_alias.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support_app/client/#put_account_alias)
        """

    async def register_slack_workspace_for_organization(
        self, **kwargs: Unpack[RegisterSlackWorkspaceForOrganizationRequestTypeDef]
    ) -> RegisterSlackWorkspaceForOrganizationResultTypeDef:
        """
        Registers a Slack workspace for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/register_slack_workspace_for_organization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support_app/client/#register_slack_workspace_for_organization)
        """

    async def update_slack_channel_configuration(
        self, **kwargs: Unpack[UpdateSlackChannelConfigurationRequestTypeDef]
    ) -> UpdateSlackChannelConfigurationResultTypeDef:
        """
        Updates the configuration for a Slack channel, such as case update
        notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app/client/update_slack_channel_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support_app/client/#update_slack_channel_configuration)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app.html#SupportApp.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support_app/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support-app.html#SupportApp.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support_app/client/)
        """
