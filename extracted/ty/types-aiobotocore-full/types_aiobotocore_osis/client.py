"""
Type annotations for osis service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_osis.client import OpenSearchIngestionClient

    session = get_session()
    async with session.create_client("osis") as client:
        client: OpenSearchIngestionClient
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
    CreatePipelineRequestTypeDef,
    CreatePipelineResponseTypeDef,
    DeletePipelineRequestTypeDef,
    GetPipelineBlueprintRequestTypeDef,
    GetPipelineBlueprintResponseTypeDef,
    GetPipelineChangeProgressRequestTypeDef,
    GetPipelineChangeProgressResponseTypeDef,
    GetPipelineRequestTypeDef,
    GetPipelineResponseTypeDef,
    ListPipelineBlueprintsResponseTypeDef,
    ListPipelinesRequestTypeDef,
    ListPipelinesResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartPipelineRequestTypeDef,
    StartPipelineResponseTypeDef,
    StopPipelineRequestTypeDef,
    StopPipelineResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdatePipelineRequestTypeDef,
    UpdatePipelineResponseTypeDef,
    ValidatePipelineRequestTypeDef,
    ValidatePipelineResponseTypeDef,
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


__all__ = ("OpenSearchIngestionClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DisabledOperationException: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InvalidPaginationTokenException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class OpenSearchIngestionClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis.html#OpenSearchIngestion.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        OpenSearchIngestionClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis.html#OpenSearchIngestion.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/client/#generate_presigned_url)
        """

    async def create_pipeline(
        self, **kwargs: Unpack[CreatePipelineRequestTypeDef]
    ) -> CreatePipelineResponseTypeDef:
        """
        Creates an OpenSearch Ingestion pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis/client/create_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/client/#create_pipeline)
        """

    async def delete_pipeline(
        self, **kwargs: Unpack[DeletePipelineRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an OpenSearch Ingestion pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis/client/delete_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/client/#delete_pipeline)
        """

    async def get_pipeline(
        self, **kwargs: Unpack[GetPipelineRequestTypeDef]
    ) -> GetPipelineResponseTypeDef:
        """
        Retrieves information about an OpenSearch Ingestion pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis/client/get_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/client/#get_pipeline)
        """

    async def get_pipeline_blueprint(
        self, **kwargs: Unpack[GetPipelineBlueprintRequestTypeDef]
    ) -> GetPipelineBlueprintResponseTypeDef:
        """
        Retrieves information about a specific blueprint for OpenSearch Ingestion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis/client/get_pipeline_blueprint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/client/#get_pipeline_blueprint)
        """

    async def get_pipeline_change_progress(
        self, **kwargs: Unpack[GetPipelineChangeProgressRequestTypeDef]
    ) -> GetPipelineChangeProgressResponseTypeDef:
        """
        Returns progress information for the current change happening on an OpenSearch
        Ingestion pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis/client/get_pipeline_change_progress.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/client/#get_pipeline_change_progress)
        """

    async def list_pipeline_blueprints(self) -> ListPipelineBlueprintsResponseTypeDef:
        """
        Retrieves a list of all available blueprints for Data Prepper.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis/client/list_pipeline_blueprints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/client/#list_pipeline_blueprints)
        """

    async def list_pipelines(
        self, **kwargs: Unpack[ListPipelinesRequestTypeDef]
    ) -> ListPipelinesResponseTypeDef:
        """
        Lists all OpenSearch Ingestion pipelines in the current Amazon Web Services
        account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis/client/list_pipelines.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/client/#list_pipelines)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all resource tags associated with an OpenSearch Ingestion pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/client/#list_tags_for_resource)
        """

    async def start_pipeline(
        self, **kwargs: Unpack[StartPipelineRequestTypeDef]
    ) -> StartPipelineResponseTypeDef:
        """
        Starts an OpenSearch Ingestion pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis/client/start_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/client/#start_pipeline)
        """

    async def stop_pipeline(
        self, **kwargs: Unpack[StopPipelineRequestTypeDef]
    ) -> StopPipelineResponseTypeDef:
        """
        Stops an OpenSearch Ingestion pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis/client/stop_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/client/#stop_pipeline)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Tags an OpenSearch Ingestion pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes one or more tags from an OpenSearch Ingestion pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/client/#untag_resource)
        """

    async def update_pipeline(
        self, **kwargs: Unpack[UpdatePipelineRequestTypeDef]
    ) -> UpdatePipelineResponseTypeDef:
        """
        Updates an OpenSearch Ingestion pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis/client/update_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/client/#update_pipeline)
        """

    async def validate_pipeline(
        self, **kwargs: Unpack[ValidatePipelineRequestTypeDef]
    ) -> ValidatePipelineResponseTypeDef:
        """
        Checks whether an OpenSearch Ingestion pipeline configuration is valid prior to
        creation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis/client/validate_pipeline.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/client/#validate_pipeline)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis.html#OpenSearchIngestion.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/osis.html#OpenSearchIngestion.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/client/)
        """
