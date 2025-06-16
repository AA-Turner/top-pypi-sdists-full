"""
Type annotations for supplychain service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_supplychain.client import SupplyChainClient

    session = get_session()
    async with session.create_client("supplychain") as client:
        client: SupplyChainClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListDataIntegrationEventsPaginator,
    ListDataIntegrationFlowExecutionsPaginator,
    ListDataIntegrationFlowsPaginator,
    ListDataLakeDatasetsPaginator,
    ListDataLakeNamespacesPaginator,
    ListInstancesPaginator,
)
from .type_defs import (
    CreateBillOfMaterialsImportJobRequestTypeDef,
    CreateBillOfMaterialsImportJobResponseTypeDef,
    CreateDataIntegrationFlowRequestTypeDef,
    CreateDataIntegrationFlowResponseTypeDef,
    CreateDataLakeDatasetRequestTypeDef,
    CreateDataLakeDatasetResponseTypeDef,
    CreateDataLakeNamespaceRequestTypeDef,
    CreateDataLakeNamespaceResponseTypeDef,
    CreateInstanceRequestTypeDef,
    CreateInstanceResponseTypeDef,
    DeleteDataIntegrationFlowRequestTypeDef,
    DeleteDataIntegrationFlowResponseTypeDef,
    DeleteDataLakeDatasetRequestTypeDef,
    DeleteDataLakeDatasetResponseTypeDef,
    DeleteDataLakeNamespaceRequestTypeDef,
    DeleteDataLakeNamespaceResponseTypeDef,
    DeleteInstanceRequestTypeDef,
    DeleteInstanceResponseTypeDef,
    GetBillOfMaterialsImportJobRequestTypeDef,
    GetBillOfMaterialsImportJobResponseTypeDef,
    GetDataIntegrationEventRequestTypeDef,
    GetDataIntegrationEventResponseTypeDef,
    GetDataIntegrationFlowExecutionRequestTypeDef,
    GetDataIntegrationFlowExecutionResponseTypeDef,
    GetDataIntegrationFlowRequestTypeDef,
    GetDataIntegrationFlowResponseTypeDef,
    GetDataLakeDatasetRequestTypeDef,
    GetDataLakeDatasetResponseTypeDef,
    GetDataLakeNamespaceRequestTypeDef,
    GetDataLakeNamespaceResponseTypeDef,
    GetInstanceRequestTypeDef,
    GetInstanceResponseTypeDef,
    ListDataIntegrationEventsRequestTypeDef,
    ListDataIntegrationEventsResponseTypeDef,
    ListDataIntegrationFlowExecutionsRequestTypeDef,
    ListDataIntegrationFlowExecutionsResponseTypeDef,
    ListDataIntegrationFlowsRequestTypeDef,
    ListDataIntegrationFlowsResponseTypeDef,
    ListDataLakeDatasetsRequestTypeDef,
    ListDataLakeDatasetsResponseTypeDef,
    ListDataLakeNamespacesRequestTypeDef,
    ListDataLakeNamespacesResponseTypeDef,
    ListInstancesRequestTypeDef,
    ListInstancesResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    SendDataIntegrationEventRequestTypeDef,
    SendDataIntegrationEventResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateDataIntegrationFlowRequestTypeDef,
    UpdateDataIntegrationFlowResponseTypeDef,
    UpdateDataLakeDatasetRequestTypeDef,
    UpdateDataLakeDatasetResponseTypeDef,
    UpdateDataLakeNamespaceRequestTypeDef,
    UpdateDataLakeNamespaceResponseTypeDef,
    UpdateInstanceRequestTypeDef,
    UpdateInstanceResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("SupplyChainClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class SupplyChainClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain.html#SupplyChain.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SupplyChainClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain.html#SupplyChain.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#generate_presigned_url)
        """

    async def create_bill_of_materials_import_job(
        self, **kwargs: Unpack[CreateBillOfMaterialsImportJobRequestTypeDef]
    ) -> CreateBillOfMaterialsImportJobResponseTypeDef:
        """
        CreateBillOfMaterialsImportJob creates an import job for the Product Bill Of
        Materials (BOM) entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/create_bill_of_materials_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#create_bill_of_materials_import_job)
        """

    async def create_data_integration_flow(
        self, **kwargs: Unpack[CreateDataIntegrationFlowRequestTypeDef]
    ) -> CreateDataIntegrationFlowResponseTypeDef:
        """
        Enables you to programmatically create a data pipeline to ingest data from
        source systems such as Amazon S3 buckets, to a predefined Amazon Web Services
        Supply Chain dataset (product, inbound_order) or a temporary dataset along with
        the data transformation query provided with the API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/create_data_integration_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#create_data_integration_flow)
        """

    async def create_data_lake_dataset(
        self, **kwargs: Unpack[CreateDataLakeDatasetRequestTypeDef]
    ) -> CreateDataLakeDatasetResponseTypeDef:
        """
        Enables you to programmatically create an Amazon Web Services Supply Chain data
        lake dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/create_data_lake_dataset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#create_data_lake_dataset)
        """

    async def create_data_lake_namespace(
        self, **kwargs: Unpack[CreateDataLakeNamespaceRequestTypeDef]
    ) -> CreateDataLakeNamespaceResponseTypeDef:
        """
        Enables you to programmatically create an Amazon Web Services Supply Chain data
        lake namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/create_data_lake_namespace.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#create_data_lake_namespace)
        """

    async def create_instance(
        self, **kwargs: Unpack[CreateInstanceRequestTypeDef]
    ) -> CreateInstanceResponseTypeDef:
        """
        Enables you to programmatically create an Amazon Web Services Supply Chain
        instance by applying KMS keys and relevant information associated with the API
        without using the Amazon Web Services console.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/create_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#create_instance)
        """

    async def delete_data_integration_flow(
        self, **kwargs: Unpack[DeleteDataIntegrationFlowRequestTypeDef]
    ) -> DeleteDataIntegrationFlowResponseTypeDef:
        """
        Enable you to programmatically delete an existing data pipeline for the
        provided Amazon Web Services Supply Chain instance and DataIntegrationFlow
        name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/delete_data_integration_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#delete_data_integration_flow)
        """

    async def delete_data_lake_dataset(
        self, **kwargs: Unpack[DeleteDataLakeDatasetRequestTypeDef]
    ) -> DeleteDataLakeDatasetResponseTypeDef:
        """
        Enables you to programmatically delete an Amazon Web Services Supply Chain data
        lake dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/delete_data_lake_dataset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#delete_data_lake_dataset)
        """

    async def delete_data_lake_namespace(
        self, **kwargs: Unpack[DeleteDataLakeNamespaceRequestTypeDef]
    ) -> DeleteDataLakeNamespaceResponseTypeDef:
        """
        Enables you to programmatically delete an Amazon Web Services Supply Chain data
        lake namespace and its underling datasets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/delete_data_lake_namespace.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#delete_data_lake_namespace)
        """

    async def delete_instance(
        self, **kwargs: Unpack[DeleteInstanceRequestTypeDef]
    ) -> DeleteInstanceResponseTypeDef:
        """
        Enables you to programmatically delete an Amazon Web Services Supply Chain
        instance by deleting the KMS keys and relevant information associated with the
        API without using the Amazon Web Services console.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/delete_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#delete_instance)
        """

    async def get_bill_of_materials_import_job(
        self, **kwargs: Unpack[GetBillOfMaterialsImportJobRequestTypeDef]
    ) -> GetBillOfMaterialsImportJobResponseTypeDef:
        """
        Get status and details of a BillOfMaterialsImportJob.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_bill_of_materials_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#get_bill_of_materials_import_job)
        """

    async def get_data_integration_event(
        self, **kwargs: Unpack[GetDataIntegrationEventRequestTypeDef]
    ) -> GetDataIntegrationEventResponseTypeDef:
        """
        Enables you to programmatically view an Amazon Web Services Supply Chain Data
        Integration Event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_data_integration_event.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#get_data_integration_event)
        """

    async def get_data_integration_flow(
        self, **kwargs: Unpack[GetDataIntegrationFlowRequestTypeDef]
    ) -> GetDataIntegrationFlowResponseTypeDef:
        """
        Enables you to programmatically view a specific data pipeline for the provided
        Amazon Web Services Supply Chain instance and DataIntegrationFlow name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_data_integration_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#get_data_integration_flow)
        """

    async def get_data_integration_flow_execution(
        self, **kwargs: Unpack[GetDataIntegrationFlowExecutionRequestTypeDef]
    ) -> GetDataIntegrationFlowExecutionResponseTypeDef:
        """
        Get the flow execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_data_integration_flow_execution.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#get_data_integration_flow_execution)
        """

    async def get_data_lake_dataset(
        self, **kwargs: Unpack[GetDataLakeDatasetRequestTypeDef]
    ) -> GetDataLakeDatasetResponseTypeDef:
        """
        Enables you to programmatically view an Amazon Web Services Supply Chain data
        lake dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_data_lake_dataset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#get_data_lake_dataset)
        """

    async def get_data_lake_namespace(
        self, **kwargs: Unpack[GetDataLakeNamespaceRequestTypeDef]
    ) -> GetDataLakeNamespaceResponseTypeDef:
        """
        Enables you to programmatically view an Amazon Web Services Supply Chain data
        lake namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_data_lake_namespace.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#get_data_lake_namespace)
        """

    async def get_instance(
        self, **kwargs: Unpack[GetInstanceRequestTypeDef]
    ) -> GetInstanceResponseTypeDef:
        """
        Enables you to programmatically retrieve the information related to an Amazon
        Web Services Supply Chain instance ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#get_instance)
        """

    async def list_data_integration_events(
        self, **kwargs: Unpack[ListDataIntegrationEventsRequestTypeDef]
    ) -> ListDataIntegrationEventsResponseTypeDef:
        """
        Enables you to programmatically list all data integration events for the
        provided Amazon Web Services Supply Chain instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/list_data_integration_events.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#list_data_integration_events)
        """

    async def list_data_integration_flow_executions(
        self, **kwargs: Unpack[ListDataIntegrationFlowExecutionsRequestTypeDef]
    ) -> ListDataIntegrationFlowExecutionsResponseTypeDef:
        """
        List flow executions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/list_data_integration_flow_executions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#list_data_integration_flow_executions)
        """

    async def list_data_integration_flows(
        self, **kwargs: Unpack[ListDataIntegrationFlowsRequestTypeDef]
    ) -> ListDataIntegrationFlowsResponseTypeDef:
        """
        Enables you to programmatically list all data pipelines for the provided Amazon
        Web Services Supply Chain instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/list_data_integration_flows.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#list_data_integration_flows)
        """

    async def list_data_lake_datasets(
        self, **kwargs: Unpack[ListDataLakeDatasetsRequestTypeDef]
    ) -> ListDataLakeDatasetsResponseTypeDef:
        """
        Enables you to programmatically view the list of Amazon Web Services Supply
        Chain data lake datasets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/list_data_lake_datasets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#list_data_lake_datasets)
        """

    async def list_data_lake_namespaces(
        self, **kwargs: Unpack[ListDataLakeNamespacesRequestTypeDef]
    ) -> ListDataLakeNamespacesResponseTypeDef:
        """
        Enables you to programmatically view the list of Amazon Web Services Supply
        Chain data lake namespaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/list_data_lake_namespaces.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#list_data_lake_namespaces)
        """

    async def list_instances(
        self, **kwargs: Unpack[ListInstancesRequestTypeDef]
    ) -> ListInstancesResponseTypeDef:
        """
        List all Amazon Web Services Supply Chain instances for a specific account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/list_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#list_instances)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List all the tags for an Amazon Web ServicesSupply Chain resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#list_tags_for_resource)
        """

    async def send_data_integration_event(
        self, **kwargs: Unpack[SendDataIntegrationEventRequestTypeDef]
    ) -> SendDataIntegrationEventResponseTypeDef:
        """
        Send the data payload for the event with real-time data for analysis or
        monitoring.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/send_data_integration_event.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#send_data_integration_event)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        You can create tags during or after creating a resource such as instance, data
        flow, or dataset in AWS Supply chain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        You can delete tags for an Amazon Web Services Supply chain resource such as
        instance, data flow, or dataset in AWS Supply Chain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#untag_resource)
        """

    async def update_data_integration_flow(
        self, **kwargs: Unpack[UpdateDataIntegrationFlowRequestTypeDef]
    ) -> UpdateDataIntegrationFlowResponseTypeDef:
        """
        Enables you to programmatically update an existing data pipeline to ingest data
        from the source systems such as, Amazon S3 buckets, to a predefined Amazon Web
        Services Supply Chain dataset (product, inbound_order) or a temporary dataset
        along with the data transformation query provided with the API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/update_data_integration_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#update_data_integration_flow)
        """

    async def update_data_lake_dataset(
        self, **kwargs: Unpack[UpdateDataLakeDatasetRequestTypeDef]
    ) -> UpdateDataLakeDatasetResponseTypeDef:
        """
        Enables you to programmatically update an Amazon Web Services Supply Chain data
        lake dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/update_data_lake_dataset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#update_data_lake_dataset)
        """

    async def update_data_lake_namespace(
        self, **kwargs: Unpack[UpdateDataLakeNamespaceRequestTypeDef]
    ) -> UpdateDataLakeNamespaceResponseTypeDef:
        """
        Enables you to programmatically update an Amazon Web Services Supply Chain data
        lake namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/update_data_lake_namespace.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#update_data_lake_namespace)
        """

    async def update_instance(
        self, **kwargs: Unpack[UpdateInstanceRequestTypeDef]
    ) -> UpdateInstanceResponseTypeDef:
        """
        Enables you to programmatically update an Amazon Web Services Supply Chain
        instance description by providing all the relevant information such as account
        ID, instance ID and so on without using the AWS console.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/update_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#update_instance)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_integration_events"]
    ) -> ListDataIntegrationEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_integration_flow_executions"]
    ) -> ListDataIntegrationFlowExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_integration_flows"]
    ) -> ListDataIntegrationFlowsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_lake_datasets"]
    ) -> ListDataLakeDatasetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_lake_namespaces"]
    ) -> ListDataLakeNamespacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_instances"]
    ) -> ListInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain.html#SupplyChain.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain.html#SupplyChain.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/client/)
        """
