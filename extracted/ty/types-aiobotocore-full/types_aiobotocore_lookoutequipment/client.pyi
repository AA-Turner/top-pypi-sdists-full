"""
Type annotations for lookoutequipment service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_lookoutequipment.client import LookoutEquipmentClient

    session = get_session()
    async with session.create_client("lookoutequipment") as client:
        client: LookoutEquipmentClient
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
    CreateDatasetRequestTypeDef,
    CreateDatasetResponseTypeDef,
    CreateInferenceSchedulerRequestTypeDef,
    CreateInferenceSchedulerResponseTypeDef,
    CreateLabelGroupRequestTypeDef,
    CreateLabelGroupResponseTypeDef,
    CreateLabelRequestTypeDef,
    CreateLabelResponseTypeDef,
    CreateModelRequestTypeDef,
    CreateModelResponseTypeDef,
    CreateRetrainingSchedulerRequestTypeDef,
    CreateRetrainingSchedulerResponseTypeDef,
    DeleteDatasetRequestTypeDef,
    DeleteInferenceSchedulerRequestTypeDef,
    DeleteLabelGroupRequestTypeDef,
    DeleteLabelRequestTypeDef,
    DeleteModelRequestTypeDef,
    DeleteResourcePolicyRequestTypeDef,
    DeleteRetrainingSchedulerRequestTypeDef,
    DescribeDataIngestionJobRequestTypeDef,
    DescribeDataIngestionJobResponseTypeDef,
    DescribeDatasetRequestTypeDef,
    DescribeDatasetResponseTypeDef,
    DescribeInferenceSchedulerRequestTypeDef,
    DescribeInferenceSchedulerResponseTypeDef,
    DescribeLabelGroupRequestTypeDef,
    DescribeLabelGroupResponseTypeDef,
    DescribeLabelRequestTypeDef,
    DescribeLabelResponseTypeDef,
    DescribeModelRequestTypeDef,
    DescribeModelResponseTypeDef,
    DescribeModelVersionRequestTypeDef,
    DescribeModelVersionResponseTypeDef,
    DescribeResourcePolicyRequestTypeDef,
    DescribeResourcePolicyResponseTypeDef,
    DescribeRetrainingSchedulerRequestTypeDef,
    DescribeRetrainingSchedulerResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ImportDatasetRequestTypeDef,
    ImportDatasetResponseTypeDef,
    ImportModelVersionRequestTypeDef,
    ImportModelVersionResponseTypeDef,
    ListDataIngestionJobsRequestTypeDef,
    ListDataIngestionJobsResponseTypeDef,
    ListDatasetsRequestTypeDef,
    ListDatasetsResponseTypeDef,
    ListInferenceEventsRequestTypeDef,
    ListInferenceEventsResponseTypeDef,
    ListInferenceExecutionsRequestTypeDef,
    ListInferenceExecutionsResponseTypeDef,
    ListInferenceSchedulersRequestTypeDef,
    ListInferenceSchedulersResponseTypeDef,
    ListLabelGroupsRequestTypeDef,
    ListLabelGroupsResponseTypeDef,
    ListLabelsRequestTypeDef,
    ListLabelsResponseTypeDef,
    ListModelsRequestTypeDef,
    ListModelsResponseTypeDef,
    ListModelVersionsRequestTypeDef,
    ListModelVersionsResponseTypeDef,
    ListRetrainingSchedulersRequestTypeDef,
    ListRetrainingSchedulersResponseTypeDef,
    ListSensorStatisticsRequestTypeDef,
    ListSensorStatisticsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutResourcePolicyRequestTypeDef,
    PutResourcePolicyResponseTypeDef,
    StartDataIngestionJobRequestTypeDef,
    StartDataIngestionJobResponseTypeDef,
    StartInferenceSchedulerRequestTypeDef,
    StartInferenceSchedulerResponseTypeDef,
    StartRetrainingSchedulerRequestTypeDef,
    StartRetrainingSchedulerResponseTypeDef,
    StopInferenceSchedulerRequestTypeDef,
    StopInferenceSchedulerResponseTypeDef,
    StopRetrainingSchedulerRequestTypeDef,
    StopRetrainingSchedulerResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateActiveModelVersionRequestTypeDef,
    UpdateActiveModelVersionResponseTypeDef,
    UpdateInferenceSchedulerRequestTypeDef,
    UpdateLabelGroupRequestTypeDef,
    UpdateModelRequestTypeDef,
    UpdateRetrainingSchedulerRequestTypeDef,
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

__all__ = ("LookoutEquipmentClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class LookoutEquipmentClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LookoutEquipmentClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#generate_presigned_url)
        """

    async def create_dataset(
        self, **kwargs: Unpack[CreateDatasetRequestTypeDef]
    ) -> CreateDatasetResponseTypeDef:
        """
        Creates a container for a collection of data being ingested for analysis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/create_dataset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#create_dataset)
        """

    async def create_inference_scheduler(
        self, **kwargs: Unpack[CreateInferenceSchedulerRequestTypeDef]
    ) -> CreateInferenceSchedulerResponseTypeDef:
        """
        Creates a scheduled inference.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/create_inference_scheduler.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#create_inference_scheduler)
        """

    async def create_label(
        self, **kwargs: Unpack[CreateLabelRequestTypeDef]
    ) -> CreateLabelResponseTypeDef:
        """
        Creates a label for an event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/create_label.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#create_label)
        """

    async def create_label_group(
        self, **kwargs: Unpack[CreateLabelGroupRequestTypeDef]
    ) -> CreateLabelGroupResponseTypeDef:
        """
        Creates a group of labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/create_label_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#create_label_group)
        """

    async def create_model(
        self, **kwargs: Unpack[CreateModelRequestTypeDef]
    ) -> CreateModelResponseTypeDef:
        """
        Creates a machine learning model for data inference.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/create_model.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#create_model)
        """

    async def create_retraining_scheduler(
        self, **kwargs: Unpack[CreateRetrainingSchedulerRequestTypeDef]
    ) -> CreateRetrainingSchedulerResponseTypeDef:
        """
        Creates a retraining scheduler on the specified model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/create_retraining_scheduler.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#create_retraining_scheduler)
        """

    async def delete_dataset(
        self, **kwargs: Unpack[DeleteDatasetRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a dataset and associated artifacts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/delete_dataset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#delete_dataset)
        """

    async def delete_inference_scheduler(
        self, **kwargs: Unpack[DeleteInferenceSchedulerRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an inference scheduler that has been set up.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/delete_inference_scheduler.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#delete_inference_scheduler)
        """

    async def delete_label(
        self, **kwargs: Unpack[DeleteLabelRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a label.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/delete_label.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#delete_label)
        """

    async def delete_label_group(
        self, **kwargs: Unpack[DeleteLabelGroupRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a group of labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/delete_label_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#delete_label_group)
        """

    async def delete_model(
        self, **kwargs: Unpack[DeleteModelRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a machine learning model currently available for Amazon Lookout for
        Equipment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/delete_model.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#delete_model)
        """

    async def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the resource policy attached to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/delete_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#delete_resource_policy)
        """

    async def delete_retraining_scheduler(
        self, **kwargs: Unpack[DeleteRetrainingSchedulerRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a retraining scheduler from a model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/delete_retraining_scheduler.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#delete_retraining_scheduler)
        """

    async def describe_data_ingestion_job(
        self, **kwargs: Unpack[DescribeDataIngestionJobRequestTypeDef]
    ) -> DescribeDataIngestionJobResponseTypeDef:
        """
        Provides information on a specific data ingestion job such as creation time,
        dataset ARN, and status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/describe_data_ingestion_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#describe_data_ingestion_job)
        """

    async def describe_dataset(
        self, **kwargs: Unpack[DescribeDatasetRequestTypeDef]
    ) -> DescribeDatasetResponseTypeDef:
        """
        Provides a JSON description of the data in each time series dataset, including
        names, column names, and data types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/describe_dataset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#describe_dataset)
        """

    async def describe_inference_scheduler(
        self, **kwargs: Unpack[DescribeInferenceSchedulerRequestTypeDef]
    ) -> DescribeInferenceSchedulerResponseTypeDef:
        """
        Specifies information about the inference scheduler being used, including name,
        model, status, and associated metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/describe_inference_scheduler.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#describe_inference_scheduler)
        """

    async def describe_label(
        self, **kwargs: Unpack[DescribeLabelRequestTypeDef]
    ) -> DescribeLabelResponseTypeDef:
        """
        Returns the name of the label.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/describe_label.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#describe_label)
        """

    async def describe_label_group(
        self, **kwargs: Unpack[DescribeLabelGroupRequestTypeDef]
    ) -> DescribeLabelGroupResponseTypeDef:
        """
        Returns information about the label group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/describe_label_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#describe_label_group)
        """

    async def describe_model(
        self, **kwargs: Unpack[DescribeModelRequestTypeDef]
    ) -> DescribeModelResponseTypeDef:
        """
        Provides a JSON containing the overall information about a specific machine
        learning model, including model name and ARN, dataset, training and evaluation
        information, status, and so on.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/describe_model.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#describe_model)
        """

    async def describe_model_version(
        self, **kwargs: Unpack[DescribeModelVersionRequestTypeDef]
    ) -> DescribeModelVersionResponseTypeDef:
        """
        Retrieves information about a specific machine learning model version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/describe_model_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#describe_model_version)
        """

    async def describe_resource_policy(
        self, **kwargs: Unpack[DescribeResourcePolicyRequestTypeDef]
    ) -> DescribeResourcePolicyResponseTypeDef:
        """
        Provides the details of a resource policy attached to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/describe_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#describe_resource_policy)
        """

    async def describe_retraining_scheduler(
        self, **kwargs: Unpack[DescribeRetrainingSchedulerRequestTypeDef]
    ) -> DescribeRetrainingSchedulerResponseTypeDef:
        """
        Provides a description of the retraining scheduler, including information such
        as the model name and retraining parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/describe_retraining_scheduler.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#describe_retraining_scheduler)
        """

    async def import_dataset(
        self, **kwargs: Unpack[ImportDatasetRequestTypeDef]
    ) -> ImportDatasetResponseTypeDef:
        """
        Imports a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/import_dataset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#import_dataset)
        """

    async def import_model_version(
        self, **kwargs: Unpack[ImportModelVersionRequestTypeDef]
    ) -> ImportModelVersionResponseTypeDef:
        """
        Imports a model that has been trained successfully.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/import_model_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#import_model_version)
        """

    async def list_data_ingestion_jobs(
        self, **kwargs: Unpack[ListDataIngestionJobsRequestTypeDef]
    ) -> ListDataIngestionJobsResponseTypeDef:
        """
        Provides a list of all data ingestion jobs, including dataset name and ARN, S3
        location of the input data, status, and so on.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_data_ingestion_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#list_data_ingestion_jobs)
        """

    async def list_datasets(
        self, **kwargs: Unpack[ListDatasetsRequestTypeDef]
    ) -> ListDatasetsResponseTypeDef:
        """
        Lists all datasets currently available in your account, filtering on the
        dataset name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_datasets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#list_datasets)
        """

    async def list_inference_events(
        self, **kwargs: Unpack[ListInferenceEventsRequestTypeDef]
    ) -> ListInferenceEventsResponseTypeDef:
        """
        Lists all inference events that have been found for the specified inference
        scheduler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_inference_events.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#list_inference_events)
        """

    async def list_inference_executions(
        self, **kwargs: Unpack[ListInferenceExecutionsRequestTypeDef]
    ) -> ListInferenceExecutionsResponseTypeDef:
        """
        Lists all inference executions that have been performed by the specified
        inference scheduler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_inference_executions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#list_inference_executions)
        """

    async def list_inference_schedulers(
        self, **kwargs: Unpack[ListInferenceSchedulersRequestTypeDef]
    ) -> ListInferenceSchedulersResponseTypeDef:
        """
        Retrieves a list of all inference schedulers currently available for your
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_inference_schedulers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#list_inference_schedulers)
        """

    async def list_label_groups(
        self, **kwargs: Unpack[ListLabelGroupsRequestTypeDef]
    ) -> ListLabelGroupsResponseTypeDef:
        """
        Returns a list of the label groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_label_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#list_label_groups)
        """

    async def list_labels(
        self, **kwargs: Unpack[ListLabelsRequestTypeDef]
    ) -> ListLabelsResponseTypeDef:
        """
        Provides a list of labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_labels.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#list_labels)
        """

    async def list_model_versions(
        self, **kwargs: Unpack[ListModelVersionsRequestTypeDef]
    ) -> ListModelVersionsResponseTypeDef:
        """
        Generates a list of all model versions for a given model, including the model
        version, model version ARN, and status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_model_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#list_model_versions)
        """

    async def list_models(
        self, **kwargs: Unpack[ListModelsRequestTypeDef]
    ) -> ListModelsResponseTypeDef:
        """
        Generates a list of all models in the account, including model name and ARN,
        dataset, and status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_models.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#list_models)
        """

    async def list_retraining_schedulers(
        self, **kwargs: Unpack[ListRetrainingSchedulersRequestTypeDef]
    ) -> ListRetrainingSchedulersResponseTypeDef:
        """
        Lists all retraining schedulers in your account, filtering by model name prefix
        and status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_retraining_schedulers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#list_retraining_schedulers)
        """

    async def list_sensor_statistics(
        self, **kwargs: Unpack[ListSensorStatisticsRequestTypeDef]
    ) -> ListSensorStatisticsResponseTypeDef:
        """
        Lists statistics about the data collected for each of the sensors that have
        been successfully ingested in the particular dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_sensor_statistics.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#list_sensor_statistics)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all the tags for a specified resource, including key and value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#list_tags_for_resource)
        """

    async def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyRequestTypeDef]
    ) -> PutResourcePolicyResponseTypeDef:
        """
        Creates a resource control policy for a given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/put_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#put_resource_policy)
        """

    async def start_data_ingestion_job(
        self, **kwargs: Unpack[StartDataIngestionJobRequestTypeDef]
    ) -> StartDataIngestionJobResponseTypeDef:
        """
        Starts a data ingestion job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/start_data_ingestion_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#start_data_ingestion_job)
        """

    async def start_inference_scheduler(
        self, **kwargs: Unpack[StartInferenceSchedulerRequestTypeDef]
    ) -> StartInferenceSchedulerResponseTypeDef:
        """
        Starts an inference scheduler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/start_inference_scheduler.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#start_inference_scheduler)
        """

    async def start_retraining_scheduler(
        self, **kwargs: Unpack[StartRetrainingSchedulerRequestTypeDef]
    ) -> StartRetrainingSchedulerResponseTypeDef:
        """
        Starts a retraining scheduler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/start_retraining_scheduler.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#start_retraining_scheduler)
        """

    async def stop_inference_scheduler(
        self, **kwargs: Unpack[StopInferenceSchedulerRequestTypeDef]
    ) -> StopInferenceSchedulerResponseTypeDef:
        """
        Stops an inference scheduler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/stop_inference_scheduler.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#stop_inference_scheduler)
        """

    async def stop_retraining_scheduler(
        self, **kwargs: Unpack[StopRetrainingSchedulerRequestTypeDef]
    ) -> StopRetrainingSchedulerResponseTypeDef:
        """
        Stops a retraining scheduler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/stop_retraining_scheduler.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#stop_retraining_scheduler)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Associates a given tag to a resource in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes a specific tag from a given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#untag_resource)
        """

    async def update_active_model_version(
        self, **kwargs: Unpack[UpdateActiveModelVersionRequestTypeDef]
    ) -> UpdateActiveModelVersionResponseTypeDef:
        """
        Sets the active model version for a given machine learning model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/update_active_model_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#update_active_model_version)
        """

    async def update_inference_scheduler(
        self, **kwargs: Unpack[UpdateInferenceSchedulerRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an inference scheduler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/update_inference_scheduler.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#update_inference_scheduler)
        """

    async def update_label_group(
        self, **kwargs: Unpack[UpdateLabelGroupRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the label group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/update_label_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#update_label_group)
        """

    async def update_model(
        self, **kwargs: Unpack[UpdateModelRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a model in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/update_model.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#update_model)
        """

    async def update_retraining_scheduler(
        self, **kwargs: Unpack[UpdateRetrainingSchedulerRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a retraining scheduler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment/client/update_retraining_scheduler.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#update_retraining_scheduler)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/)
        """
