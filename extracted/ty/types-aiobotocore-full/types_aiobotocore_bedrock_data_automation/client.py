"""
Type annotations for bedrock-data-automation service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_bedrock_data_automation.client import DataAutomationforBedrockClient

    session = get_session()
    async with session.create_client("bedrock-data-automation") as client:
        client: DataAutomationforBedrockClient
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListBlueprintsPaginator,
    ListDataAutomationLibrariesPaginator,
    ListDataAutomationLibraryEntitiesPaginator,
    ListDataAutomationLibraryIngestionJobsPaginator,
    ListDataAutomationProjectsPaginator,
)
from .type_defs import (
    CopyBlueprintStageRequestTypeDef,
    CreateBlueprintRequestTypeDef,
    CreateBlueprintResponseTypeDef,
    CreateBlueprintVersionRequestTypeDef,
    CreateBlueprintVersionResponseTypeDef,
    CreateDataAutomationLibraryRequestTypeDef,
    CreateDataAutomationLibraryResponseTypeDef,
    CreateDataAutomationProjectRequestTypeDef,
    CreateDataAutomationProjectResponseTypeDef,
    DeleteBlueprintRequestTypeDef,
    DeleteDataAutomationLibraryRequestTypeDef,
    DeleteDataAutomationLibraryResponseTypeDef,
    DeleteDataAutomationProjectRequestTypeDef,
    DeleteDataAutomationProjectResponseTypeDef,
    GetBlueprintOptimizationStatusRequestTypeDef,
    GetBlueprintOptimizationStatusResponseTypeDef,
    GetBlueprintRequestTypeDef,
    GetBlueprintResponseTypeDef,
    GetDataAutomationLibraryEntityRequestTypeDef,
    GetDataAutomationLibraryEntityResponseTypeDef,
    GetDataAutomationLibraryIngestionJobRequestTypeDef,
    GetDataAutomationLibraryIngestionJobResponseTypeDef,
    GetDataAutomationLibraryRequestTypeDef,
    GetDataAutomationLibraryResponseTypeDef,
    GetDataAutomationProjectRequestTypeDef,
    GetDataAutomationProjectResponseTypeDef,
    InvokeBlueprintOptimizationAsyncRequestTypeDef,
    InvokeBlueprintOptimizationAsyncResponseTypeDef,
    InvokeDataAutomationLibraryIngestionJobRequestTypeDef,
    InvokeDataAutomationLibraryIngestionJobResponseTypeDef,
    ListBlueprintsRequestTypeDef,
    ListBlueprintsResponseTypeDef,
    ListDataAutomationLibrariesRequestTypeDef,
    ListDataAutomationLibrariesResponseTypeDef,
    ListDataAutomationLibraryEntitiesRequestTypeDef,
    ListDataAutomationLibraryEntitiesResponseTypeDef,
    ListDataAutomationLibraryIngestionJobsRequestTypeDef,
    ListDataAutomationLibraryIngestionJobsResponseTypeDef,
    ListDataAutomationProjectsRequestTypeDef,
    ListDataAutomationProjectsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateBlueprintRequestTypeDef,
    UpdateBlueprintResponseTypeDef,
    UpdateDataAutomationLibraryRequestTypeDef,
    UpdateDataAutomationLibraryResponseTypeDef,
    UpdateDataAutomationProjectRequestTypeDef,
    UpdateDataAutomationProjectResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("DataAutomationforBedrockClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class DataAutomationforBedrockClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation.html#DataAutomationforBedrock.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DataAutomationforBedrockClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation.html#DataAutomationforBedrock.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#generate_presigned_url)
        """

    async def copy_blueprint_stage(
        self, **kwargs: Unpack[CopyBlueprintStageRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Copies a Blueprint from one stage to another.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/copy_blueprint_stage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#copy_blueprint_stage)
        """

    async def create_blueprint(
        self, **kwargs: Unpack[CreateBlueprintRequestTypeDef]
    ) -> CreateBlueprintResponseTypeDef:
        """
        Creates an Amazon Bedrock Data Automation Blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/create_blueprint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#create_blueprint)
        """

    async def create_blueprint_version(
        self, **kwargs: Unpack[CreateBlueprintVersionRequestTypeDef]
    ) -> CreateBlueprintVersionResponseTypeDef:
        """
        Creates a new version of an existing Amazon Bedrock Data Automation Blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/create_blueprint_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#create_blueprint_version)
        """

    async def create_data_automation_library(
        self, **kwargs: Unpack[CreateDataAutomationLibraryRequestTypeDef]
    ) -> CreateDataAutomationLibraryResponseTypeDef:
        """
        Creates an Amazon Bedrock Data Automation Library.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/create_data_automation_library.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#create_data_automation_library)
        """

    async def create_data_automation_project(
        self, **kwargs: Unpack[CreateDataAutomationProjectRequestTypeDef]
    ) -> CreateDataAutomationProjectResponseTypeDef:
        """
        Creates an Amazon Bedrock Data Automation Project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/create_data_automation_project.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#create_data_automation_project)
        """

    async def delete_blueprint(
        self, **kwargs: Unpack[DeleteBlueprintRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes an existing Amazon Bedrock Data Automation Blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/delete_blueprint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#delete_blueprint)
        """

    async def delete_data_automation_library(
        self, **kwargs: Unpack[DeleteDataAutomationLibraryRequestTypeDef]
    ) -> DeleteDataAutomationLibraryResponseTypeDef:
        """
        Deletes an existing Amazon Bedrock Data Automation Library.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/delete_data_automation_library.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#delete_data_automation_library)
        """

    async def delete_data_automation_project(
        self, **kwargs: Unpack[DeleteDataAutomationProjectRequestTypeDef]
    ) -> DeleteDataAutomationProjectResponseTypeDef:
        """
        Deletes an existing Amazon Bedrock Data Automation Project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/delete_data_automation_project.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#delete_data_automation_project)
        """

    async def get_blueprint(
        self, **kwargs: Unpack[GetBlueprintRequestTypeDef]
    ) -> GetBlueprintResponseTypeDef:
        """
        Gets an existing Amazon Bedrock Data Automation Blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/get_blueprint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#get_blueprint)
        """

    async def get_blueprint_optimization_status(
        self, **kwargs: Unpack[GetBlueprintOptimizationStatusRequestTypeDef]
    ) -> GetBlueprintOptimizationStatusResponseTypeDef:
        """
        API used to get blueprint optimization status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/get_blueprint_optimization_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#get_blueprint_optimization_status)
        """

    async def get_data_automation_library(
        self, **kwargs: Unpack[GetDataAutomationLibraryRequestTypeDef]
    ) -> GetDataAutomationLibraryResponseTypeDef:
        """
        Gets an existing Amazon Bedrock Data Automation Library.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/get_data_automation_library.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#get_data_automation_library)
        """

    async def get_data_automation_library_entity(
        self, **kwargs: Unpack[GetDataAutomationLibraryEntityRequestTypeDef]
    ) -> GetDataAutomationLibraryEntityResponseTypeDef:
        """
        Gets an existing entity based on entity type from the library.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/get_data_automation_library_entity.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#get_data_automation_library_entity)
        """

    async def get_data_automation_library_ingestion_job(
        self, **kwargs: Unpack[GetDataAutomationLibraryIngestionJobRequestTypeDef]
    ) -> GetDataAutomationLibraryIngestionJobResponseTypeDef:
        """
        API used to get status of data automation library ingestion job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/get_data_automation_library_ingestion_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#get_data_automation_library_ingestion_job)
        """

    async def get_data_automation_project(
        self, **kwargs: Unpack[GetDataAutomationProjectRequestTypeDef]
    ) -> GetDataAutomationProjectResponseTypeDef:
        """
        Gets an existing Amazon Bedrock Data Automation Project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/get_data_automation_project.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#get_data_automation_project)
        """

    async def invoke_blueprint_optimization_async(
        self, **kwargs: Unpack[InvokeBlueprintOptimizationAsyncRequestTypeDef]
    ) -> InvokeBlueprintOptimizationAsyncResponseTypeDef:
        """
        Invoke an async job to perform Blueprint Optimization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/invoke_blueprint_optimization_async.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#invoke_blueprint_optimization_async)
        """

    async def invoke_data_automation_library_ingestion_job(
        self, **kwargs: Unpack[InvokeDataAutomationLibraryIngestionJobRequestTypeDef]
    ) -> InvokeDataAutomationLibraryIngestionJobResponseTypeDef:
        """
        Async API: Invoke data automation library ingestion job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/invoke_data_automation_library_ingestion_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#invoke_data_automation_library_ingestion_job)
        """

    async def list_blueprints(
        self, **kwargs: Unpack[ListBlueprintsRequestTypeDef]
    ) -> ListBlueprintsResponseTypeDef:
        """
        Lists all existing Amazon Bedrock Data Automation Blueprints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/list_blueprints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#list_blueprints)
        """

    async def list_data_automation_libraries(
        self, **kwargs: Unpack[ListDataAutomationLibrariesRequestTypeDef]
    ) -> ListDataAutomationLibrariesResponseTypeDef:
        """
        Lists all existing Amazon Bedrock Data Automation Libraries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/list_data_automation_libraries.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#list_data_automation_libraries)
        """

    async def list_data_automation_library_entities(
        self, **kwargs: Unpack[ListDataAutomationLibraryEntitiesRequestTypeDef]
    ) -> ListDataAutomationLibraryEntitiesResponseTypeDef:
        """
        Lists all stored entities in the library.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/list_data_automation_library_entities.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#list_data_automation_library_entities)
        """

    async def list_data_automation_library_ingestion_jobs(
        self, **kwargs: Unpack[ListDataAutomationLibraryIngestionJobsRequestTypeDef]
    ) -> ListDataAutomationLibraryIngestionJobsResponseTypeDef:
        """
        Lists all data automation library ingestion jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/list_data_automation_library_ingestion_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#list_data_automation_library_ingestion_jobs)
        """

    async def list_data_automation_projects(
        self, **kwargs: Unpack[ListDataAutomationProjectsRequestTypeDef]
    ) -> ListDataAutomationProjectsResponseTypeDef:
        """
        Lists all existing Amazon Bedrock Data Automation Projects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/list_data_automation_projects.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#list_data_automation_projects)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List tags for an Amazon Bedrock Data Automation resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#list_tags_for_resource)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Tag an Amazon Bedrock Data Automation resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Untag an Amazon Bedrock Data Automation resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#untag_resource)
        """

    async def update_blueprint(
        self, **kwargs: Unpack[UpdateBlueprintRequestTypeDef]
    ) -> UpdateBlueprintResponseTypeDef:
        """
        Updates an existing Amazon Bedrock Data Automation Blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/update_blueprint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#update_blueprint)
        """

    async def update_data_automation_library(
        self, **kwargs: Unpack[UpdateDataAutomationLibraryRequestTypeDef]
    ) -> UpdateDataAutomationLibraryResponseTypeDef:
        """
        Updates an existing Amazon Bedrock Data Automation Library.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/update_data_automation_library.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#update_data_automation_library)
        """

    async def update_data_automation_project(
        self, **kwargs: Unpack[UpdateDataAutomationProjectRequestTypeDef]
    ) -> UpdateDataAutomationProjectResponseTypeDef:
        """
        Updates an existing Amazon Bedrock Data Automation Project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/update_data_automation_project.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#update_data_automation_project)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_blueprints"]
    ) -> ListBlueprintsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_automation_libraries"]
    ) -> ListDataAutomationLibrariesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_automation_library_entities"]
    ) -> ListDataAutomationLibraryEntitiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_automation_library_ingestion_jobs"]
    ) -> ListDataAutomationLibraryIngestionJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_automation_projects"]
    ) -> ListDataAutomationProjectsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation.html#DataAutomationforBedrock.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-data-automation.html#DataAutomationforBedrock.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation/client/)
        """
