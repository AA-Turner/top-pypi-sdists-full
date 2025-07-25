"""
Type annotations for qbusiness service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_qbusiness.client import QBusinessClient
    from types_aiobotocore_qbusiness.paginator import (
        GetChatControlsConfigurationPaginator,
        ListApplicationsPaginator,
        ListAttachmentsPaginator,
        ListChatResponseConfigurationsPaginator,
        ListConversationsPaginator,
        ListDataAccessorsPaginator,
        ListDataSourceSyncJobsPaginator,
        ListDataSourcesPaginator,
        ListDocumentsPaginator,
        ListGroupsPaginator,
        ListIndicesPaginator,
        ListMessagesPaginator,
        ListPluginActionsPaginator,
        ListPluginTypeActionsPaginator,
        ListPluginTypeMetadataPaginator,
        ListPluginsPaginator,
        ListRetrieversPaginator,
        ListSubscriptionsPaginator,
        ListWebExperiencesPaginator,
        SearchRelevantContentPaginator,
    )

    session = get_session()
    with session.create_client("qbusiness") as client:
        client: QBusinessClient

        get_chat_controls_configuration_paginator: GetChatControlsConfigurationPaginator = client.get_paginator("get_chat_controls_configuration")
        list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
        list_attachments_paginator: ListAttachmentsPaginator = client.get_paginator("list_attachments")
        list_chat_response_configurations_paginator: ListChatResponseConfigurationsPaginator = client.get_paginator("list_chat_response_configurations")
        list_conversations_paginator: ListConversationsPaginator = client.get_paginator("list_conversations")
        list_data_accessors_paginator: ListDataAccessorsPaginator = client.get_paginator("list_data_accessors")
        list_data_source_sync_jobs_paginator: ListDataSourceSyncJobsPaginator = client.get_paginator("list_data_source_sync_jobs")
        list_data_sources_paginator: ListDataSourcesPaginator = client.get_paginator("list_data_sources")
        list_documents_paginator: ListDocumentsPaginator = client.get_paginator("list_documents")
        list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
        list_indices_paginator: ListIndicesPaginator = client.get_paginator("list_indices")
        list_messages_paginator: ListMessagesPaginator = client.get_paginator("list_messages")
        list_plugin_actions_paginator: ListPluginActionsPaginator = client.get_paginator("list_plugin_actions")
        list_plugin_type_actions_paginator: ListPluginTypeActionsPaginator = client.get_paginator("list_plugin_type_actions")
        list_plugin_type_metadata_paginator: ListPluginTypeMetadataPaginator = client.get_paginator("list_plugin_type_metadata")
        list_plugins_paginator: ListPluginsPaginator = client.get_paginator("list_plugins")
        list_retrievers_paginator: ListRetrieversPaginator = client.get_paginator("list_retrievers")
        list_subscriptions_paginator: ListSubscriptionsPaginator = client.get_paginator("list_subscriptions")
        list_web_experiences_paginator: ListWebExperiencesPaginator = client.get_paginator("list_web_experiences")
        search_relevant_content_paginator: SearchRelevantContentPaginator = client.get_paginator("search_relevant_content")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetChatControlsConfigurationRequestPaginateTypeDef,
    GetChatControlsConfigurationResponseTypeDef,
    ListApplicationsRequestPaginateTypeDef,
    ListApplicationsResponseTypeDef,
    ListAttachmentsRequestPaginateTypeDef,
    ListAttachmentsResponseTypeDef,
    ListChatResponseConfigurationsRequestPaginateTypeDef,
    ListChatResponseConfigurationsResponseTypeDef,
    ListConversationsRequestPaginateTypeDef,
    ListConversationsResponseTypeDef,
    ListDataAccessorsRequestPaginateTypeDef,
    ListDataAccessorsResponseTypeDef,
    ListDataSourcesRequestPaginateTypeDef,
    ListDataSourcesResponseTypeDef,
    ListDataSourceSyncJobsRequestPaginateTypeDef,
    ListDataSourceSyncJobsResponseTypeDef,
    ListDocumentsRequestPaginateTypeDef,
    ListDocumentsResponseTypeDef,
    ListGroupsRequestPaginateTypeDef,
    ListGroupsResponseTypeDef,
    ListIndicesRequestPaginateTypeDef,
    ListIndicesResponseTypeDef,
    ListMessagesRequestPaginateTypeDef,
    ListMessagesResponseTypeDef,
    ListPluginActionsRequestPaginateTypeDef,
    ListPluginActionsResponseTypeDef,
    ListPluginsRequestPaginateTypeDef,
    ListPluginsResponseTypeDef,
    ListPluginTypeActionsRequestPaginateTypeDef,
    ListPluginTypeActionsResponseTypeDef,
    ListPluginTypeMetadataRequestPaginateTypeDef,
    ListPluginTypeMetadataResponseTypeDef,
    ListRetrieversRequestPaginateTypeDef,
    ListRetrieversResponseTypeDef,
    ListSubscriptionsRequestPaginateTypeDef,
    ListSubscriptionsResponseTypeDef,
    ListWebExperiencesRequestPaginateTypeDef,
    ListWebExperiencesResponseTypeDef,
    SearchRelevantContentRequestPaginateTypeDef,
    SearchRelevantContentResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetChatControlsConfigurationPaginator",
    "ListApplicationsPaginator",
    "ListAttachmentsPaginator",
    "ListChatResponseConfigurationsPaginator",
    "ListConversationsPaginator",
    "ListDataAccessorsPaginator",
    "ListDataSourceSyncJobsPaginator",
    "ListDataSourcesPaginator",
    "ListDocumentsPaginator",
    "ListGroupsPaginator",
    "ListIndicesPaginator",
    "ListMessagesPaginator",
    "ListPluginActionsPaginator",
    "ListPluginTypeActionsPaginator",
    "ListPluginTypeMetadataPaginator",
    "ListPluginsPaginator",
    "ListRetrieversPaginator",
    "ListSubscriptionsPaginator",
    "ListWebExperiencesPaginator",
    "SearchRelevantContentPaginator",
)

if TYPE_CHECKING:
    _GetChatControlsConfigurationPaginatorBase = AioPaginator[
        GetChatControlsConfigurationResponseTypeDef
    ]
else:
    _GetChatControlsConfigurationPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetChatControlsConfigurationPaginator(_GetChatControlsConfigurationPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/GetChatControlsConfiguration.html#QBusiness.Paginator.GetChatControlsConfiguration)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#getchatcontrolsconfigurationpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetChatControlsConfigurationRequestPaginateTypeDef]
    ) -> AioPageIterator[GetChatControlsConfigurationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/GetChatControlsConfiguration.html#QBusiness.Paginator.GetChatControlsConfiguration.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#getchatcontrolsconfigurationpaginator)
        """

if TYPE_CHECKING:
    _ListApplicationsPaginatorBase = AioPaginator[ListApplicationsResponseTypeDef]
else:
    _ListApplicationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListApplicationsPaginator(_ListApplicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListApplications.html#QBusiness.Paginator.ListApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listapplicationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListApplications.html#QBusiness.Paginator.ListApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listapplicationspaginator)
        """

if TYPE_CHECKING:
    _ListAttachmentsPaginatorBase = AioPaginator[ListAttachmentsResponseTypeDef]
else:
    _ListAttachmentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAttachmentsPaginator(_ListAttachmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListAttachments.html#QBusiness.Paginator.ListAttachments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listattachmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAttachmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAttachmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListAttachments.html#QBusiness.Paginator.ListAttachments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listattachmentspaginator)
        """

if TYPE_CHECKING:
    _ListChatResponseConfigurationsPaginatorBase = AioPaginator[
        ListChatResponseConfigurationsResponseTypeDef
    ]
else:
    _ListChatResponseConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListChatResponseConfigurationsPaginator(_ListChatResponseConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListChatResponseConfigurations.html#QBusiness.Paginator.ListChatResponseConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listchatresponseconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListChatResponseConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListChatResponseConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListChatResponseConfigurations.html#QBusiness.Paginator.ListChatResponseConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listchatresponseconfigurationspaginator)
        """

if TYPE_CHECKING:
    _ListConversationsPaginatorBase = AioPaginator[ListConversationsResponseTypeDef]
else:
    _ListConversationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListConversationsPaginator(_ListConversationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListConversations.html#QBusiness.Paginator.ListConversations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listconversationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConversationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListConversationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListConversations.html#QBusiness.Paginator.ListConversations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listconversationspaginator)
        """

if TYPE_CHECKING:
    _ListDataAccessorsPaginatorBase = AioPaginator[ListDataAccessorsResponseTypeDef]
else:
    _ListDataAccessorsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataAccessorsPaginator(_ListDataAccessorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDataAccessors.html#QBusiness.Paginator.ListDataAccessors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listdataaccessorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataAccessorsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataAccessorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDataAccessors.html#QBusiness.Paginator.ListDataAccessors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listdataaccessorspaginator)
        """

if TYPE_CHECKING:
    _ListDataSourceSyncJobsPaginatorBase = AioPaginator[ListDataSourceSyncJobsResponseTypeDef]
else:
    _ListDataSourceSyncJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataSourceSyncJobsPaginator(_ListDataSourceSyncJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDataSourceSyncJobs.html#QBusiness.Paginator.ListDataSourceSyncJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listdatasourcesyncjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataSourceSyncJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataSourceSyncJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDataSourceSyncJobs.html#QBusiness.Paginator.ListDataSourceSyncJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listdatasourcesyncjobspaginator)
        """

if TYPE_CHECKING:
    _ListDataSourcesPaginatorBase = AioPaginator[ListDataSourcesResponseTypeDef]
else:
    _ListDataSourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataSourcesPaginator(_ListDataSourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDataSources.html#QBusiness.Paginator.ListDataSources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listdatasourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataSourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDataSources.html#QBusiness.Paginator.ListDataSources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listdatasourcespaginator)
        """

if TYPE_CHECKING:
    _ListDocumentsPaginatorBase = AioPaginator[ListDocumentsResponseTypeDef]
else:
    _ListDocumentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDocumentsPaginator(_ListDocumentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDocuments.html#QBusiness.Paginator.ListDocuments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listdocumentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDocumentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDocumentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDocuments.html#QBusiness.Paginator.ListDocuments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listdocumentspaginator)
        """

if TYPE_CHECKING:
    _ListGroupsPaginatorBase = AioPaginator[ListGroupsResponseTypeDef]
else:
    _ListGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListGroupsPaginator(_ListGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListGroups.html#QBusiness.Paginator.ListGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listgroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListGroups.html#QBusiness.Paginator.ListGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listgroupspaginator)
        """

if TYPE_CHECKING:
    _ListIndicesPaginatorBase = AioPaginator[ListIndicesResponseTypeDef]
else:
    _ListIndicesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListIndicesPaginator(_ListIndicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListIndices.html#QBusiness.Paginator.ListIndices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listindicespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIndicesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListIndicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListIndices.html#QBusiness.Paginator.ListIndices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listindicespaginator)
        """

if TYPE_CHECKING:
    _ListMessagesPaginatorBase = AioPaginator[ListMessagesResponseTypeDef]
else:
    _ListMessagesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMessagesPaginator(_ListMessagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListMessages.html#QBusiness.Paginator.ListMessages)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listmessagespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMessagesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMessagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListMessages.html#QBusiness.Paginator.ListMessages.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listmessagespaginator)
        """

if TYPE_CHECKING:
    _ListPluginActionsPaginatorBase = AioPaginator[ListPluginActionsResponseTypeDef]
else:
    _ListPluginActionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPluginActionsPaginator(_ListPluginActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPluginActions.html#QBusiness.Paginator.ListPluginActions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listpluginactionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPluginActionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPluginActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPluginActions.html#QBusiness.Paginator.ListPluginActions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listpluginactionspaginator)
        """

if TYPE_CHECKING:
    _ListPluginTypeActionsPaginatorBase = AioPaginator[ListPluginTypeActionsResponseTypeDef]
else:
    _ListPluginTypeActionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPluginTypeActionsPaginator(_ListPluginTypeActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPluginTypeActions.html#QBusiness.Paginator.ListPluginTypeActions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listplugintypeactionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPluginTypeActionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPluginTypeActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPluginTypeActions.html#QBusiness.Paginator.ListPluginTypeActions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listplugintypeactionspaginator)
        """

if TYPE_CHECKING:
    _ListPluginTypeMetadataPaginatorBase = AioPaginator[ListPluginTypeMetadataResponseTypeDef]
else:
    _ListPluginTypeMetadataPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPluginTypeMetadataPaginator(_ListPluginTypeMetadataPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPluginTypeMetadata.html#QBusiness.Paginator.ListPluginTypeMetadata)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listplugintypemetadatapaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPluginTypeMetadataRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPluginTypeMetadataResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPluginTypeMetadata.html#QBusiness.Paginator.ListPluginTypeMetadata.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listplugintypemetadatapaginator)
        """

if TYPE_CHECKING:
    _ListPluginsPaginatorBase = AioPaginator[ListPluginsResponseTypeDef]
else:
    _ListPluginsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPluginsPaginator(_ListPluginsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPlugins.html#QBusiness.Paginator.ListPlugins)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listpluginspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPluginsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPluginsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPlugins.html#QBusiness.Paginator.ListPlugins.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listpluginspaginator)
        """

if TYPE_CHECKING:
    _ListRetrieversPaginatorBase = AioPaginator[ListRetrieversResponseTypeDef]
else:
    _ListRetrieversPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRetrieversPaginator(_ListRetrieversPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListRetrievers.html#QBusiness.Paginator.ListRetrievers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listretrieverspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRetrieversRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRetrieversResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListRetrievers.html#QBusiness.Paginator.ListRetrievers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listretrieverspaginator)
        """

if TYPE_CHECKING:
    _ListSubscriptionsPaginatorBase = AioPaginator[ListSubscriptionsResponseTypeDef]
else:
    _ListSubscriptionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSubscriptionsPaginator(_ListSubscriptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListSubscriptions.html#QBusiness.Paginator.ListSubscriptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listsubscriptionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSubscriptionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListSubscriptions.html#QBusiness.Paginator.ListSubscriptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listsubscriptionspaginator)
        """

if TYPE_CHECKING:
    _ListWebExperiencesPaginatorBase = AioPaginator[ListWebExperiencesResponseTypeDef]
else:
    _ListWebExperiencesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListWebExperiencesPaginator(_ListWebExperiencesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListWebExperiences.html#QBusiness.Paginator.ListWebExperiences)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listwebexperiencespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWebExperiencesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWebExperiencesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListWebExperiences.html#QBusiness.Paginator.ListWebExperiences.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listwebexperiencespaginator)
        """

if TYPE_CHECKING:
    _SearchRelevantContentPaginatorBase = AioPaginator[SearchRelevantContentResponseTypeDef]
else:
    _SearchRelevantContentPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchRelevantContentPaginator(_SearchRelevantContentPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/SearchRelevantContent.html#QBusiness.Paginator.SearchRelevantContent)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#searchrelevantcontentpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchRelevantContentRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchRelevantContentResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/SearchRelevantContent.html#QBusiness.Paginator.SearchRelevantContent.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#searchrelevantcontentpaginator)
        """
