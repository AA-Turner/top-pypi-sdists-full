"""
Type annotations for supplychain service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_supplychain.client import SupplyChainClient

    session = Session()
    client: SupplyChainClient = session.client("supplychain")
    ```
"""

from __future__ import annotations

import sys
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListDataIntegrationFlowsPaginator,
    ListDataLakeDatasetsPaginator,
    ListInstancesPaginator,
)
from .type_defs import (
    CreateBillOfMaterialsImportJobRequestTypeDef,
    CreateBillOfMaterialsImportJobResponseTypeDef,
    CreateDataIntegrationFlowRequestTypeDef,
    CreateDataIntegrationFlowResponseTypeDef,
    CreateDataLakeDatasetRequestTypeDef,
    CreateDataLakeDatasetResponseTypeDef,
    CreateInstanceRequestTypeDef,
    CreateInstanceResponseTypeDef,
    DeleteDataIntegrationFlowRequestTypeDef,
    DeleteDataIntegrationFlowResponseTypeDef,
    DeleteDataLakeDatasetRequestTypeDef,
    DeleteDataLakeDatasetResponseTypeDef,
    DeleteInstanceRequestTypeDef,
    DeleteInstanceResponseTypeDef,
    GetBillOfMaterialsImportJobRequestTypeDef,
    GetBillOfMaterialsImportJobResponseTypeDef,
    GetDataIntegrationFlowRequestTypeDef,
    GetDataIntegrationFlowResponseTypeDef,
    GetDataLakeDatasetRequestTypeDef,
    GetDataLakeDatasetResponseTypeDef,
    GetInstanceRequestTypeDef,
    GetInstanceResponseTypeDef,
    ListDataIntegrationFlowsRequestTypeDef,
    ListDataIntegrationFlowsResponseTypeDef,
    ListDataLakeDatasetsRequestTypeDef,
    ListDataLakeDatasetsResponseTypeDef,
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
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

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

class SupplyChainClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain.html#SupplyChain.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SupplyChainClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain.html#SupplyChain.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#generate_presigned_url)
        """

    def create_bill_of_materials_import_job(
        self, **kwargs: Unpack[CreateBillOfMaterialsImportJobRequestTypeDef]
    ) -> CreateBillOfMaterialsImportJobResponseTypeDef:
        """
        CreateBillOfMaterialsImportJob creates an import job for the Product Bill Of
        Materials (BOM) entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/create_bill_of_materials_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#create_bill_of_materials_import_job)
        """

    def create_data_integration_flow(
        self, **kwargs: Unpack[CreateDataIntegrationFlowRequestTypeDef]
    ) -> CreateDataIntegrationFlowResponseTypeDef:
        """
        Enables you to programmatically create a data pipeline to ingest data from
        source systems such as Amazon S3 buckets, to a predefined Amazon Web Services
        Supply Chain dataset (product, inbound_order) or a temporary dataset along with
        the data transformation query provided with the API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/create_data_integration_flow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#create_data_integration_flow)
        """

    def create_data_lake_dataset(
        self, **kwargs: Unpack[CreateDataLakeDatasetRequestTypeDef]
    ) -> CreateDataLakeDatasetResponseTypeDef:
        """
        Enables you to programmatically create an Amazon Web Services Supply Chain data
        lake dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/create_data_lake_dataset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#create_data_lake_dataset)
        """

    def create_instance(
        self, **kwargs: Unpack[CreateInstanceRequestTypeDef]
    ) -> CreateInstanceResponseTypeDef:
        """
        Enables you to programmatically create an Amazon Web Services Supply Chain
        instance by applying KMS keys and relevant information associated with the API
        without using the Amazon Web Services console.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/create_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#create_instance)
        """

    def delete_data_integration_flow(
        self, **kwargs: Unpack[DeleteDataIntegrationFlowRequestTypeDef]
    ) -> DeleteDataIntegrationFlowResponseTypeDef:
        """
        Enable you to programmatically delete an existing data pipeline for the
        provided Amazon Web Services Supply Chain instance and DataIntegrationFlow
        name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/delete_data_integration_flow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#delete_data_integration_flow)
        """

    def delete_data_lake_dataset(
        self, **kwargs: Unpack[DeleteDataLakeDatasetRequestTypeDef]
    ) -> DeleteDataLakeDatasetResponseTypeDef:
        """
        Enables you to programmatically delete an Amazon Web Services Supply Chain data
        lake dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/delete_data_lake_dataset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#delete_data_lake_dataset)
        """

    def delete_instance(
        self, **kwargs: Unpack[DeleteInstanceRequestTypeDef]
    ) -> DeleteInstanceResponseTypeDef:
        """
        Enables you to programmatically delete an Amazon Web Services Supply Chain
        instance by deleting the KMS keys and relevant information associated with the
        API without using the Amazon Web Services console.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/delete_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#delete_instance)
        """

    def get_bill_of_materials_import_job(
        self, **kwargs: Unpack[GetBillOfMaterialsImportJobRequestTypeDef]
    ) -> GetBillOfMaterialsImportJobResponseTypeDef:
        """
        Get status and details of a BillOfMaterialsImportJob.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_bill_of_materials_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#get_bill_of_materials_import_job)
        """

    def get_data_integration_flow(
        self, **kwargs: Unpack[GetDataIntegrationFlowRequestTypeDef]
    ) -> GetDataIntegrationFlowResponseTypeDef:
        """
        Enables you to programmatically view a specific data pipeline for the provided
        Amazon Web Services Supply Chain instance and DataIntegrationFlow name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_data_integration_flow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#get_data_integration_flow)
        """

    def get_data_lake_dataset(
        self, **kwargs: Unpack[GetDataLakeDatasetRequestTypeDef]
    ) -> GetDataLakeDatasetResponseTypeDef:
        """
        Enables you to programmatically view an Amazon Web Services Supply Chain data
        lake dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_data_lake_dataset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#get_data_lake_dataset)
        """

    def get_instance(
        self, **kwargs: Unpack[GetInstanceRequestTypeDef]
    ) -> GetInstanceResponseTypeDef:
        """
        Enables you to programmatically retrieve the information related to an Amazon
        Web Services Supply Chain instance ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#get_instance)
        """

    def list_data_integration_flows(
        self, **kwargs: Unpack[ListDataIntegrationFlowsRequestTypeDef]
    ) -> ListDataIntegrationFlowsResponseTypeDef:
        """
        Enables you to programmatically list all data pipelines for the provided Amazon
        Web Services Supply Chain instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/list_data_integration_flows.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#list_data_integration_flows)
        """

    def list_data_lake_datasets(
        self, **kwargs: Unpack[ListDataLakeDatasetsRequestTypeDef]
    ) -> ListDataLakeDatasetsResponseTypeDef:
        """
        Enables you to programmatically view the list of Amazon Web Services Supply
        Chain data lake datasets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/list_data_lake_datasets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#list_data_lake_datasets)
        """

    def list_instances(
        self, **kwargs: Unpack[ListInstancesRequestTypeDef]
    ) -> ListInstancesResponseTypeDef:
        """
        List all Amazon Web Services Supply Chain instances for a specific account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/list_instances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#list_instances)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List all the tags for an Amazon Web ServicesSupply Chain resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#list_tags_for_resource)
        """

    def send_data_integration_event(
        self, **kwargs: Unpack[SendDataIntegrationEventRequestTypeDef]
    ) -> SendDataIntegrationEventResponseTypeDef:
        """
        Send the transactional data payload for the event with real-time data for
        analysis or monitoring.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/send_data_integration_event.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#send_data_integration_event)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        You can create tags during or after creating a resource such as instance, data
        flow, or dataset in AWS Supply chain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        You can delete tags for an Amazon Web Services Supply chain resource such as
        instance, data flow, or dataset in AWS Supply Chain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#untag_resource)
        """

    def update_data_integration_flow(
        self, **kwargs: Unpack[UpdateDataIntegrationFlowRequestTypeDef]
    ) -> UpdateDataIntegrationFlowResponseTypeDef:
        """
        Enables you to programmatically update an existing data pipeline to ingest data
        from the source systems such as, Amazon S3 buckets, to a predefined Amazon Web
        Services Supply Chain dataset (product, inbound_order) or a temporary dataset
        along with the data transformation query provided with the API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/update_data_integration_flow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#update_data_integration_flow)
        """

    def update_data_lake_dataset(
        self, **kwargs: Unpack[UpdateDataLakeDatasetRequestTypeDef]
    ) -> UpdateDataLakeDatasetResponseTypeDef:
        """
        Enables you to programmatically update an Amazon Web Services Supply Chain data
        lake dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/update_data_lake_dataset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#update_data_lake_dataset)
        """

    def update_instance(
        self, **kwargs: Unpack[UpdateInstanceRequestTypeDef]
    ) -> UpdateInstanceResponseTypeDef:
        """
        Enables you to programmatically update an Amazon Web Services Supply Chain
        instance description by providing all the relevant information such as account
        ID, instance ID and so on without using the AWS console.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/update_instance.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#update_instance)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_integration_flows"]
    ) -> ListDataIntegrationFlowsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_lake_datasets"]
    ) -> ListDataLakeDatasetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_instances"]
    ) -> ListInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/client/#get_paginator)
        """
