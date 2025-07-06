"""
Type annotations for kendra service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kendra.client import KendraClient

    session = get_session()
    async with session.create_client("kendra") as client:
        client: KendraClient
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
    AssociateEntitiesToExperienceRequestTypeDef,
    AssociateEntitiesToExperienceResponseTypeDef,
    AssociatePersonasToEntitiesRequestTypeDef,
    AssociatePersonasToEntitiesResponseTypeDef,
    BatchDeleteDocumentRequestTypeDef,
    BatchDeleteDocumentResponseTypeDef,
    BatchDeleteFeaturedResultsSetRequestTypeDef,
    BatchDeleteFeaturedResultsSetResponseTypeDef,
    BatchGetDocumentStatusRequestTypeDef,
    BatchGetDocumentStatusResponseTypeDef,
    BatchPutDocumentRequestTypeDef,
    BatchPutDocumentResponseTypeDef,
    ClearQuerySuggestionsRequestTypeDef,
    CreateAccessControlConfigurationRequestTypeDef,
    CreateAccessControlConfigurationResponseTypeDef,
    CreateDataSourceRequestTypeDef,
    CreateDataSourceResponseTypeDef,
    CreateExperienceRequestTypeDef,
    CreateExperienceResponseTypeDef,
    CreateFaqRequestTypeDef,
    CreateFaqResponseTypeDef,
    CreateFeaturedResultsSetRequestTypeDef,
    CreateFeaturedResultsSetResponseTypeDef,
    CreateIndexRequestTypeDef,
    CreateIndexResponseTypeDef,
    CreateQuerySuggestionsBlockListRequestTypeDef,
    CreateQuerySuggestionsBlockListResponseTypeDef,
    CreateThesaurusRequestTypeDef,
    CreateThesaurusResponseTypeDef,
    DeleteAccessControlConfigurationRequestTypeDef,
    DeleteDataSourceRequestTypeDef,
    DeleteExperienceRequestTypeDef,
    DeleteFaqRequestTypeDef,
    DeleteIndexRequestTypeDef,
    DeletePrincipalMappingRequestTypeDef,
    DeleteQuerySuggestionsBlockListRequestTypeDef,
    DeleteThesaurusRequestTypeDef,
    DescribeAccessControlConfigurationRequestTypeDef,
    DescribeAccessControlConfigurationResponseTypeDef,
    DescribeDataSourceRequestTypeDef,
    DescribeDataSourceResponseTypeDef,
    DescribeExperienceRequestTypeDef,
    DescribeExperienceResponseTypeDef,
    DescribeFaqRequestTypeDef,
    DescribeFaqResponseTypeDef,
    DescribeFeaturedResultsSetRequestTypeDef,
    DescribeFeaturedResultsSetResponseTypeDef,
    DescribeIndexRequestTypeDef,
    DescribeIndexResponseTypeDef,
    DescribePrincipalMappingRequestTypeDef,
    DescribePrincipalMappingResponseTypeDef,
    DescribeQuerySuggestionsBlockListRequestTypeDef,
    DescribeQuerySuggestionsBlockListResponseTypeDef,
    DescribeQuerySuggestionsConfigRequestTypeDef,
    DescribeQuerySuggestionsConfigResponseTypeDef,
    DescribeThesaurusRequestTypeDef,
    DescribeThesaurusResponseTypeDef,
    DisassociateEntitiesFromExperienceRequestTypeDef,
    DisassociateEntitiesFromExperienceResponseTypeDef,
    DisassociatePersonasFromEntitiesRequestTypeDef,
    DisassociatePersonasFromEntitiesResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetQuerySuggestionsRequestTypeDef,
    GetQuerySuggestionsResponseTypeDef,
    GetSnapshotsRequestTypeDef,
    GetSnapshotsResponseTypeDef,
    ListAccessControlConfigurationsRequestTypeDef,
    ListAccessControlConfigurationsResponseTypeDef,
    ListDataSourcesRequestTypeDef,
    ListDataSourcesResponseTypeDef,
    ListDataSourceSyncJobsRequestTypeDef,
    ListDataSourceSyncJobsResponseTypeDef,
    ListEntityPersonasRequestTypeDef,
    ListEntityPersonasResponseTypeDef,
    ListExperienceEntitiesRequestTypeDef,
    ListExperienceEntitiesResponseTypeDef,
    ListExperiencesRequestTypeDef,
    ListExperiencesResponseTypeDef,
    ListFaqsRequestTypeDef,
    ListFaqsResponseTypeDef,
    ListFeaturedResultsSetsRequestTypeDef,
    ListFeaturedResultsSetsResponseTypeDef,
    ListGroupsOlderThanOrderingIdRequestTypeDef,
    ListGroupsOlderThanOrderingIdResponseTypeDef,
    ListIndicesRequestTypeDef,
    ListIndicesResponseTypeDef,
    ListQuerySuggestionsBlockListsRequestTypeDef,
    ListQuerySuggestionsBlockListsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListThesauriRequestTypeDef,
    ListThesauriResponseTypeDef,
    PutPrincipalMappingRequestTypeDef,
    QueryRequestTypeDef,
    QueryResultTypeDef,
    RetrieveRequestTypeDef,
    RetrieveResultTypeDef,
    StartDataSourceSyncJobRequestTypeDef,
    StartDataSourceSyncJobResponseTypeDef,
    StopDataSourceSyncJobRequestTypeDef,
    SubmitFeedbackRequestTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateAccessControlConfigurationRequestTypeDef,
    UpdateDataSourceRequestTypeDef,
    UpdateExperienceRequestTypeDef,
    UpdateFeaturedResultsSetRequestTypeDef,
    UpdateFeaturedResultsSetResponseTypeDef,
    UpdateIndexRequestTypeDef,
    UpdateQuerySuggestionsBlockListRequestTypeDef,
    UpdateQuerySuggestionsConfigRequestTypeDef,
    UpdateThesaurusRequestTypeDef,
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

__all__ = ("KendraClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    FeaturedResultsConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ResourceAlreadyExistException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceUnavailableException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class KendraClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KendraClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#generate_presigned_url)
        """

    async def associate_entities_to_experience(
        self, **kwargs: Unpack[AssociateEntitiesToExperienceRequestTypeDef]
    ) -> AssociateEntitiesToExperienceResponseTypeDef:
        """
        Grants users or groups in your IAM Identity Center identity source access to
        your Amazon Kendra experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/associate_entities_to_experience.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#associate_entities_to_experience)
        """

    async def associate_personas_to_entities(
        self, **kwargs: Unpack[AssociatePersonasToEntitiesRequestTypeDef]
    ) -> AssociatePersonasToEntitiesResponseTypeDef:
        """
        Defines the specific permissions of users or groups in your IAM Identity Center
        identity source with access to your Amazon Kendra experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/associate_personas_to_entities.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#associate_personas_to_entities)
        """

    async def batch_delete_document(
        self, **kwargs: Unpack[BatchDeleteDocumentRequestTypeDef]
    ) -> BatchDeleteDocumentResponseTypeDef:
        """
        Removes one or more documents from an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/batch_delete_document.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#batch_delete_document)
        """

    async def batch_delete_featured_results_set(
        self, **kwargs: Unpack[BatchDeleteFeaturedResultsSetRequestTypeDef]
    ) -> BatchDeleteFeaturedResultsSetResponseTypeDef:
        """
        Removes one or more sets of featured results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/batch_delete_featured_results_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#batch_delete_featured_results_set)
        """

    async def batch_get_document_status(
        self, **kwargs: Unpack[BatchGetDocumentStatusRequestTypeDef]
    ) -> BatchGetDocumentStatusResponseTypeDef:
        """
        Returns the indexing status for one or more documents submitted with the <a
        href="https://docs.aws.amazon.com/kendra/latest/dg/API_BatchPutDocument.html">
        BatchPutDocument</a> API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/batch_get_document_status.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#batch_get_document_status)
        """

    async def batch_put_document(
        self, **kwargs: Unpack[BatchPutDocumentRequestTypeDef]
    ) -> BatchPutDocumentResponseTypeDef:
        """
        Adds one or more documents to an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/batch_put_document.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#batch_put_document)
        """

    async def clear_query_suggestions(
        self, **kwargs: Unpack[ClearQuerySuggestionsRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Clears existing query suggestions from an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/clear_query_suggestions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#clear_query_suggestions)
        """

    async def create_access_control_configuration(
        self, **kwargs: Unpack[CreateAccessControlConfigurationRequestTypeDef]
    ) -> CreateAccessControlConfigurationResponseTypeDef:
        """
        Creates an access configuration for your documents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/create_access_control_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#create_access_control_configuration)
        """

    async def create_data_source(
        self, **kwargs: Unpack[CreateDataSourceRequestTypeDef]
    ) -> CreateDataSourceResponseTypeDef:
        """
        Creates a data source connector that you want to use with an Amazon Kendra
        index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/create_data_source.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#create_data_source)
        """

    async def create_experience(
        self, **kwargs: Unpack[CreateExperienceRequestTypeDef]
    ) -> CreateExperienceResponseTypeDef:
        """
        Creates an Amazon Kendra experience such as a search application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/create_experience.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#create_experience)
        """

    async def create_faq(
        self, **kwargs: Unpack[CreateFaqRequestTypeDef]
    ) -> CreateFaqResponseTypeDef:
        """
        Creates a set of frequently ask questions (FAQs) using a specified FAQ file
        stored in an Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/create_faq.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#create_faq)
        """

    async def create_featured_results_set(
        self, **kwargs: Unpack[CreateFeaturedResultsSetRequestTypeDef]
    ) -> CreateFeaturedResultsSetResponseTypeDef:
        """
        Creates a set of featured results to display at the top of the search results
        page.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/create_featured_results_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#create_featured_results_set)
        """

    async def create_index(
        self, **kwargs: Unpack[CreateIndexRequestTypeDef]
    ) -> CreateIndexResponseTypeDef:
        """
        Creates an Amazon Kendra index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/create_index.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#create_index)
        """

    async def create_query_suggestions_block_list(
        self, **kwargs: Unpack[CreateQuerySuggestionsBlockListRequestTypeDef]
    ) -> CreateQuerySuggestionsBlockListResponseTypeDef:
        """
        Creates a block list to exlcude certain queries from suggestions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/create_query_suggestions_block_list.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#create_query_suggestions_block_list)
        """

    async def create_thesaurus(
        self, **kwargs: Unpack[CreateThesaurusRequestTypeDef]
    ) -> CreateThesaurusResponseTypeDef:
        """
        Creates a thesaurus for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/create_thesaurus.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#create_thesaurus)
        """

    async def delete_access_control_configuration(
        self, **kwargs: Unpack[DeleteAccessControlConfigurationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an access control configuration that you created for your documents in
        an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/delete_access_control_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_access_control_configuration)
        """

    async def delete_data_source(
        self, **kwargs: Unpack[DeleteDataSourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Amazon Kendra data source connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/delete_data_source.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_data_source)
        """

    async def delete_experience(
        self, **kwargs: Unpack[DeleteExperienceRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes your Amazon Kendra experience such as a search application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/delete_experience.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_experience)
        """

    async def delete_faq(
        self, **kwargs: Unpack[DeleteFaqRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a FAQ from an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/delete_faq.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_faq)
        """

    async def delete_index(
        self, **kwargs: Unpack[DeleteIndexRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Amazon Kendra index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/delete_index.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_index)
        """

    async def delete_principal_mapping(
        self, **kwargs: Unpack[DeletePrincipalMappingRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a group so that all users that belong to the group can no longer access
        documents only available to that group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/delete_principal_mapping.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_principal_mapping)
        """

    async def delete_query_suggestions_block_list(
        self, **kwargs: Unpack[DeleteQuerySuggestionsBlockListRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a block list used for query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/delete_query_suggestions_block_list.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_query_suggestions_block_list)
        """

    async def delete_thesaurus(
        self, **kwargs: Unpack[DeleteThesaurusRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Amazon Kendra thesaurus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/delete_thesaurus.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_thesaurus)
        """

    async def describe_access_control_configuration(
        self, **kwargs: Unpack[DescribeAccessControlConfigurationRequestTypeDef]
    ) -> DescribeAccessControlConfigurationResponseTypeDef:
        """
        Gets information about an access control configuration that you created for
        your documents in an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/describe_access_control_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_access_control_configuration)
        """

    async def describe_data_source(
        self, **kwargs: Unpack[DescribeDataSourceRequestTypeDef]
    ) -> DescribeDataSourceResponseTypeDef:
        """
        Gets information about an Amazon Kendra data source connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/describe_data_source.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_data_source)
        """

    async def describe_experience(
        self, **kwargs: Unpack[DescribeExperienceRequestTypeDef]
    ) -> DescribeExperienceResponseTypeDef:
        """
        Gets information about your Amazon Kendra experience such as a search
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/describe_experience.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_experience)
        """

    async def describe_faq(
        self, **kwargs: Unpack[DescribeFaqRequestTypeDef]
    ) -> DescribeFaqResponseTypeDef:
        """
        Gets information about a FAQ.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/describe_faq.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_faq)
        """

    async def describe_featured_results_set(
        self, **kwargs: Unpack[DescribeFeaturedResultsSetRequestTypeDef]
    ) -> DescribeFeaturedResultsSetResponseTypeDef:
        """
        Gets information about a set of featured results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/describe_featured_results_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_featured_results_set)
        """

    async def describe_index(
        self, **kwargs: Unpack[DescribeIndexRequestTypeDef]
    ) -> DescribeIndexResponseTypeDef:
        """
        Gets information about an Amazon Kendra index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/describe_index.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_index)
        """

    async def describe_principal_mapping(
        self, **kwargs: Unpack[DescribePrincipalMappingRequestTypeDef]
    ) -> DescribePrincipalMappingResponseTypeDef:
        """
        Describes the processing of <code>PUT</code> and <code>DELETE</code> actions
        for mapping users to their groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/describe_principal_mapping.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_principal_mapping)
        """

    async def describe_query_suggestions_block_list(
        self, **kwargs: Unpack[DescribeQuerySuggestionsBlockListRequestTypeDef]
    ) -> DescribeQuerySuggestionsBlockListResponseTypeDef:
        """
        Gets information about a block list used for query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/describe_query_suggestions_block_list.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_query_suggestions_block_list)
        """

    async def describe_query_suggestions_config(
        self, **kwargs: Unpack[DescribeQuerySuggestionsConfigRequestTypeDef]
    ) -> DescribeQuerySuggestionsConfigResponseTypeDef:
        """
        Gets information on the settings of query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/describe_query_suggestions_config.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_query_suggestions_config)
        """

    async def describe_thesaurus(
        self, **kwargs: Unpack[DescribeThesaurusRequestTypeDef]
    ) -> DescribeThesaurusResponseTypeDef:
        """
        Gets information about an Amazon Kendra thesaurus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/describe_thesaurus.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_thesaurus)
        """

    async def disassociate_entities_from_experience(
        self, **kwargs: Unpack[DisassociateEntitiesFromExperienceRequestTypeDef]
    ) -> DisassociateEntitiesFromExperienceResponseTypeDef:
        """
        Prevents users or groups in your IAM Identity Center identity source from
        accessing your Amazon Kendra experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/disassociate_entities_from_experience.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#disassociate_entities_from_experience)
        """

    async def disassociate_personas_from_entities(
        self, **kwargs: Unpack[DisassociatePersonasFromEntitiesRequestTypeDef]
    ) -> DisassociatePersonasFromEntitiesResponseTypeDef:
        """
        Removes the specific permissions of users or groups in your IAM Identity Center
        identity source with access to your Amazon Kendra experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/disassociate_personas_from_entities.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#disassociate_personas_from_entities)
        """

    async def get_query_suggestions(
        self, **kwargs: Unpack[GetQuerySuggestionsRequestTypeDef]
    ) -> GetQuerySuggestionsResponseTypeDef:
        """
        Fetches the queries that are suggested to your users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/get_query_suggestions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#get_query_suggestions)
        """

    async def get_snapshots(
        self, **kwargs: Unpack[GetSnapshotsRequestTypeDef]
    ) -> GetSnapshotsResponseTypeDef:
        """
        Retrieves search metrics data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/get_snapshots.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#get_snapshots)
        """

    async def list_access_control_configurations(
        self, **kwargs: Unpack[ListAccessControlConfigurationsRequestTypeDef]
    ) -> ListAccessControlConfigurationsResponseTypeDef:
        """
        Lists one or more access control configurations for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/list_access_control_configurations.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_access_control_configurations)
        """

    async def list_data_source_sync_jobs(
        self, **kwargs: Unpack[ListDataSourceSyncJobsRequestTypeDef]
    ) -> ListDataSourceSyncJobsResponseTypeDef:
        """
        Gets statistics about synchronizing a data source connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/list_data_source_sync_jobs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_data_source_sync_jobs)
        """

    async def list_data_sources(
        self, **kwargs: Unpack[ListDataSourcesRequestTypeDef]
    ) -> ListDataSourcesResponseTypeDef:
        """
        Lists the data source connectors that you have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/list_data_sources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_data_sources)
        """

    async def list_entity_personas(
        self, **kwargs: Unpack[ListEntityPersonasRequestTypeDef]
    ) -> ListEntityPersonasResponseTypeDef:
        """
        Lists specific permissions of users and groups with access to your Amazon
        Kendra experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/list_entity_personas.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_entity_personas)
        """

    async def list_experience_entities(
        self, **kwargs: Unpack[ListExperienceEntitiesRequestTypeDef]
    ) -> ListExperienceEntitiesResponseTypeDef:
        """
        Lists users or groups in your IAM Identity Center identity source that are
        granted access to your Amazon Kendra experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/list_experience_entities.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_experience_entities)
        """

    async def list_experiences(
        self, **kwargs: Unpack[ListExperiencesRequestTypeDef]
    ) -> ListExperiencesResponseTypeDef:
        """
        Lists one or more Amazon Kendra experiences.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/list_experiences.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_experiences)
        """

    async def list_faqs(self, **kwargs: Unpack[ListFaqsRequestTypeDef]) -> ListFaqsResponseTypeDef:
        """
        Gets a list of FAQs associated with an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/list_faqs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_faqs)
        """

    async def list_featured_results_sets(
        self, **kwargs: Unpack[ListFeaturedResultsSetsRequestTypeDef]
    ) -> ListFeaturedResultsSetsResponseTypeDef:
        """
        Lists all your sets of featured results for a given index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/list_featured_results_sets.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_featured_results_sets)
        """

    async def list_groups_older_than_ordering_id(
        self, **kwargs: Unpack[ListGroupsOlderThanOrderingIdRequestTypeDef]
    ) -> ListGroupsOlderThanOrderingIdResponseTypeDef:
        """
        Provides a list of groups that are mapped to users before a given ordering or
        timestamp identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/list_groups_older_than_ordering_id.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_groups_older_than_ordering_id)
        """

    async def list_indices(
        self, **kwargs: Unpack[ListIndicesRequestTypeDef]
    ) -> ListIndicesResponseTypeDef:
        """
        Lists the Amazon Kendra indexes that you created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/list_indices.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_indices)
        """

    async def list_query_suggestions_block_lists(
        self, **kwargs: Unpack[ListQuerySuggestionsBlockListsRequestTypeDef]
    ) -> ListQuerySuggestionsBlockListsResponseTypeDef:
        """
        Lists the block lists used for query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/list_query_suggestions_block_lists.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_query_suggestions_block_lists)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Gets a list of tags associated with a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_tags_for_resource)
        """

    async def list_thesauri(
        self, **kwargs: Unpack[ListThesauriRequestTypeDef]
    ) -> ListThesauriResponseTypeDef:
        """
        Lists the thesauri for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/list_thesauri.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_thesauri)
        """

    async def put_principal_mapping(
        self, **kwargs: Unpack[PutPrincipalMappingRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Maps users to their groups so that you only need to provide the user ID when
        you issue the query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/put_principal_mapping.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#put_principal_mapping)
        """

    async def query(self, **kwargs: Unpack[QueryRequestTypeDef]) -> QueryResultTypeDef:
        """
        Searches an index given an input query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/query.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#query)
        """

    async def retrieve(self, **kwargs: Unpack[RetrieveRequestTypeDef]) -> RetrieveResultTypeDef:
        """
        Retrieves relevant passages or text excerpts given an input query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/retrieve.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#retrieve)
        """

    async def start_data_source_sync_job(
        self, **kwargs: Unpack[StartDataSourceSyncJobRequestTypeDef]
    ) -> StartDataSourceSyncJobResponseTypeDef:
        """
        Starts a synchronization job for a data source connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/start_data_source_sync_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#start_data_source_sync_job)
        """

    async def stop_data_source_sync_job(
        self, **kwargs: Unpack[StopDataSourceSyncJobRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a synchronization job that is currently running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/stop_data_source_sync_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#stop_data_source_sync_job)
        """

    async def submit_feedback(
        self, **kwargs: Unpack[SubmitFeedbackRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables you to provide feedback to Amazon Kendra to improve the performance of
        your index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/submit_feedback.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#submit_feedback)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds the specified tag to the specified index, FAQ, data source, or other
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes a tag from an index, FAQ, data source, or other resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#untag_resource)
        """

    async def update_access_control_configuration(
        self, **kwargs: Unpack[UpdateAccessControlConfigurationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates an access control configuration for your documents in an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/update_access_control_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#update_access_control_configuration)
        """

    async def update_data_source(
        self, **kwargs: Unpack[UpdateDataSourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an Amazon Kendra data source connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/update_data_source.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#update_data_source)
        """

    async def update_experience(
        self, **kwargs: Unpack[UpdateExperienceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates your Amazon Kendra experience such as a search application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/update_experience.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#update_experience)
        """

    async def update_featured_results_set(
        self, **kwargs: Unpack[UpdateFeaturedResultsSetRequestTypeDef]
    ) -> UpdateFeaturedResultsSetResponseTypeDef:
        """
        Updates a set of featured results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/update_featured_results_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#update_featured_results_set)
        """

    async def update_index(
        self, **kwargs: Unpack[UpdateIndexRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an Amazon Kendra index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/update_index.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#update_index)
        """

    async def update_query_suggestions_block_list(
        self, **kwargs: Unpack[UpdateQuerySuggestionsBlockListRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a block list used for query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/update_query_suggestions_block_list.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#update_query_suggestions_block_list)
        """

    async def update_query_suggestions_config(
        self, **kwargs: Unpack[UpdateQuerySuggestionsConfigRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the settings of query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/update_query_suggestions_config.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#update_query_suggestions_config)
        """

    async def update_thesaurus(
        self, **kwargs: Unpack[UpdateThesaurusRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a thesaurus for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra/client/update_thesaurus.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#update_thesaurus)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/)
        """
