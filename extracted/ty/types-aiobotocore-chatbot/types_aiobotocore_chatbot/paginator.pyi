"""
Type annotations for chatbot service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_chatbot.client import ChatbotClient
    from types_aiobotocore_chatbot.paginator import (
        DescribeChimeWebhookConfigurationsPaginator,
        DescribeSlackChannelConfigurationsPaginator,
        DescribeSlackUserIdentitiesPaginator,
        DescribeSlackWorkspacesPaginator,
        ListAssociationsPaginator,
        ListCustomActionsPaginator,
        ListMicrosoftTeamsChannelConfigurationsPaginator,
        ListMicrosoftTeamsConfiguredTeamsPaginator,
        ListMicrosoftTeamsUserIdentitiesPaginator,
    )

    session = get_session()
    with session.create_client("chatbot") as client:
        client: ChatbotClient

        describe_chime_webhook_configurations_paginator: DescribeChimeWebhookConfigurationsPaginator = client.get_paginator("describe_chime_webhook_configurations")
        describe_slack_channel_configurations_paginator: DescribeSlackChannelConfigurationsPaginator = client.get_paginator("describe_slack_channel_configurations")
        describe_slack_user_identities_paginator: DescribeSlackUserIdentitiesPaginator = client.get_paginator("describe_slack_user_identities")
        describe_slack_workspaces_paginator: DescribeSlackWorkspacesPaginator = client.get_paginator("describe_slack_workspaces")
        list_associations_paginator: ListAssociationsPaginator = client.get_paginator("list_associations")
        list_custom_actions_paginator: ListCustomActionsPaginator = client.get_paginator("list_custom_actions")
        list_microsoft_teams_channel_configurations_paginator: ListMicrosoftTeamsChannelConfigurationsPaginator = client.get_paginator("list_microsoft_teams_channel_configurations")
        list_microsoft_teams_configured_teams_paginator: ListMicrosoftTeamsConfiguredTeamsPaginator = client.get_paginator("list_microsoft_teams_configured_teams")
        list_microsoft_teams_user_identities_paginator: ListMicrosoftTeamsUserIdentitiesPaginator = client.get_paginator("list_microsoft_teams_user_identities")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeChimeWebhookConfigurationsRequestPaginateTypeDef,
    DescribeChimeWebhookConfigurationsResultTypeDef,
    DescribeSlackChannelConfigurationsRequestPaginateTypeDef,
    DescribeSlackChannelConfigurationsResultTypeDef,
    DescribeSlackUserIdentitiesRequestPaginateTypeDef,
    DescribeSlackUserIdentitiesResultTypeDef,
    DescribeSlackWorkspacesRequestPaginateTypeDef,
    DescribeSlackWorkspacesResultTypeDef,
    ListAssociationsRequestPaginateTypeDef,
    ListAssociationsResultTypeDef,
    ListCustomActionsRequestPaginateTypeDef,
    ListCustomActionsResultTypeDef,
    ListMicrosoftTeamsConfiguredTeamsRequestPaginateTypeDef,
    ListMicrosoftTeamsConfiguredTeamsResultTypeDef,
    ListMicrosoftTeamsUserIdentitiesRequestPaginateTypeDef,
    ListMicrosoftTeamsUserIdentitiesResultTypeDef,
    ListTeamsChannelConfigurationsRequestPaginateTypeDef,
    ListTeamsChannelConfigurationsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeChimeWebhookConfigurationsPaginator",
    "DescribeSlackChannelConfigurationsPaginator",
    "DescribeSlackUserIdentitiesPaginator",
    "DescribeSlackWorkspacesPaginator",
    "ListAssociationsPaginator",
    "ListCustomActionsPaginator",
    "ListMicrosoftTeamsChannelConfigurationsPaginator",
    "ListMicrosoftTeamsConfiguredTeamsPaginator",
    "ListMicrosoftTeamsUserIdentitiesPaginator",
)

if TYPE_CHECKING:
    _DescribeChimeWebhookConfigurationsPaginatorBase = AioPaginator[
        DescribeChimeWebhookConfigurationsResultTypeDef
    ]
else:
    _DescribeChimeWebhookConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeChimeWebhookConfigurationsPaginator(_DescribeChimeWebhookConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeChimeWebhookConfigurations.html#Chatbot.Paginator.DescribeChimeWebhookConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#describechimewebhookconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeChimeWebhookConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeChimeWebhookConfigurationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeChimeWebhookConfigurations.html#Chatbot.Paginator.DescribeChimeWebhookConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#describechimewebhookconfigurationspaginator)
        """

if TYPE_CHECKING:
    _DescribeSlackChannelConfigurationsPaginatorBase = AioPaginator[
        DescribeSlackChannelConfigurationsResultTypeDef
    ]
else:
    _DescribeSlackChannelConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeSlackChannelConfigurationsPaginator(_DescribeSlackChannelConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeSlackChannelConfigurations.html#Chatbot.Paginator.DescribeSlackChannelConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#describeslackchannelconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSlackChannelConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeSlackChannelConfigurationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeSlackChannelConfigurations.html#Chatbot.Paginator.DescribeSlackChannelConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#describeslackchannelconfigurationspaginator)
        """

if TYPE_CHECKING:
    _DescribeSlackUserIdentitiesPaginatorBase = AioPaginator[
        DescribeSlackUserIdentitiesResultTypeDef
    ]
else:
    _DescribeSlackUserIdentitiesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeSlackUserIdentitiesPaginator(_DescribeSlackUserIdentitiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeSlackUserIdentities.html#Chatbot.Paginator.DescribeSlackUserIdentities)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#describeslackuseridentitiespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSlackUserIdentitiesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeSlackUserIdentitiesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeSlackUserIdentities.html#Chatbot.Paginator.DescribeSlackUserIdentities.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#describeslackuseridentitiespaginator)
        """

if TYPE_CHECKING:
    _DescribeSlackWorkspacesPaginatorBase = AioPaginator[DescribeSlackWorkspacesResultTypeDef]
else:
    _DescribeSlackWorkspacesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeSlackWorkspacesPaginator(_DescribeSlackWorkspacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeSlackWorkspaces.html#Chatbot.Paginator.DescribeSlackWorkspaces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#describeslackworkspacespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSlackWorkspacesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeSlackWorkspacesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/DescribeSlackWorkspaces.html#Chatbot.Paginator.DescribeSlackWorkspaces.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#describeslackworkspacespaginator)
        """

if TYPE_CHECKING:
    _ListAssociationsPaginatorBase = AioPaginator[ListAssociationsResultTypeDef]
else:
    _ListAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAssociationsPaginator(_ListAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListAssociations.html#Chatbot.Paginator.ListAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#listassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListAssociations.html#Chatbot.Paginator.ListAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#listassociationspaginator)
        """

if TYPE_CHECKING:
    _ListCustomActionsPaginatorBase = AioPaginator[ListCustomActionsResultTypeDef]
else:
    _ListCustomActionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCustomActionsPaginator(_ListCustomActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListCustomActions.html#Chatbot.Paginator.ListCustomActions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#listcustomactionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCustomActionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCustomActionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListCustomActions.html#Chatbot.Paginator.ListCustomActions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#listcustomactionspaginator)
        """

if TYPE_CHECKING:
    _ListMicrosoftTeamsChannelConfigurationsPaginatorBase = AioPaginator[
        ListTeamsChannelConfigurationsResultTypeDef
    ]
else:
    _ListMicrosoftTeamsChannelConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMicrosoftTeamsChannelConfigurationsPaginator(
    _ListMicrosoftTeamsChannelConfigurationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListMicrosoftTeamsChannelConfigurations.html#Chatbot.Paginator.ListMicrosoftTeamsChannelConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#listmicrosoftteamschannelconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTeamsChannelConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTeamsChannelConfigurationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListMicrosoftTeamsChannelConfigurations.html#Chatbot.Paginator.ListMicrosoftTeamsChannelConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#listmicrosoftteamschannelconfigurationspaginator)
        """

if TYPE_CHECKING:
    _ListMicrosoftTeamsConfiguredTeamsPaginatorBase = AioPaginator[
        ListMicrosoftTeamsConfiguredTeamsResultTypeDef
    ]
else:
    _ListMicrosoftTeamsConfiguredTeamsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMicrosoftTeamsConfiguredTeamsPaginator(_ListMicrosoftTeamsConfiguredTeamsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListMicrosoftTeamsConfiguredTeams.html#Chatbot.Paginator.ListMicrosoftTeamsConfiguredTeams)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#listmicrosoftteamsconfiguredteamspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMicrosoftTeamsConfiguredTeamsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMicrosoftTeamsConfiguredTeamsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListMicrosoftTeamsConfiguredTeams.html#Chatbot.Paginator.ListMicrosoftTeamsConfiguredTeams.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#listmicrosoftteamsconfiguredteamspaginator)
        """

if TYPE_CHECKING:
    _ListMicrosoftTeamsUserIdentitiesPaginatorBase = AioPaginator[
        ListMicrosoftTeamsUserIdentitiesResultTypeDef
    ]
else:
    _ListMicrosoftTeamsUserIdentitiesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMicrosoftTeamsUserIdentitiesPaginator(_ListMicrosoftTeamsUserIdentitiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListMicrosoftTeamsUserIdentities.html#Chatbot.Paginator.ListMicrosoftTeamsUserIdentities)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#listmicrosoftteamsuseridentitiespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMicrosoftTeamsUserIdentitiesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMicrosoftTeamsUserIdentitiesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chatbot/paginator/ListMicrosoftTeamsUserIdentities.html#Chatbot.Paginator.ListMicrosoftTeamsUserIdentities.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chatbot/paginators/#listmicrosoftteamsuseridentitiespaginator)
        """
