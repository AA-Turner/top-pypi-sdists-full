"""
Type annotations for dms service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_dms.client import DatabaseMigrationServiceClient
    from types_aiobotocore_dms.waiter import (
        EndpointDeletedWaiter,
        ExtensionPackAssociatedWaiter,
        MetadataModelAssessedWaiter,
        MetadataModelConversionCancelledWaiter,
        MetadataModelConvertedWaiter,
        MetadataModelCreatedWaiter,
        MetadataModelCreationCancelledWaiter,
        MetadataModelExportedAsScriptWaiter,
        MetadataModelExportedToTargetWaiter,
        MetadataModelImportedWaiter,
        ReplicationInstanceAvailableWaiter,
        ReplicationInstanceDeletedWaiter,
        ReplicationTaskDeletedWaiter,
        ReplicationTaskReadyWaiter,
        ReplicationTaskRunningWaiter,
        ReplicationTaskStoppedWaiter,
        TestConnectionSucceedsWaiter,
    )

    session = get_session()
    async with session.create_client("dms") as client:
        client: DatabaseMigrationServiceClient

        endpoint_deleted_waiter: EndpointDeletedWaiter = client.get_waiter("endpoint_deleted")
        extension_pack_associated_waiter: ExtensionPackAssociatedWaiter = client.get_waiter("extension_pack_associated")
        metadata_model_assessed_waiter: MetadataModelAssessedWaiter = client.get_waiter("metadata_model_assessed")
        metadata_model_conversion_cancelled_waiter: MetadataModelConversionCancelledWaiter = client.get_waiter("metadata_model_conversion_cancelled")
        metadata_model_converted_waiter: MetadataModelConvertedWaiter = client.get_waiter("metadata_model_converted")
        metadata_model_created_waiter: MetadataModelCreatedWaiter = client.get_waiter("metadata_model_created")
        metadata_model_creation_cancelled_waiter: MetadataModelCreationCancelledWaiter = client.get_waiter("metadata_model_creation_cancelled")
        metadata_model_exported_as_script_waiter: MetadataModelExportedAsScriptWaiter = client.get_waiter("metadata_model_exported_as_script")
        metadata_model_exported_to_target_waiter: MetadataModelExportedToTargetWaiter = client.get_waiter("metadata_model_exported_to_target")
        metadata_model_imported_waiter: MetadataModelImportedWaiter = client.get_waiter("metadata_model_imported")
        replication_instance_available_waiter: ReplicationInstanceAvailableWaiter = client.get_waiter("replication_instance_available")
        replication_instance_deleted_waiter: ReplicationInstanceDeletedWaiter = client.get_waiter("replication_instance_deleted")
        replication_task_deleted_waiter: ReplicationTaskDeletedWaiter = client.get_waiter("replication_task_deleted")
        replication_task_ready_waiter: ReplicationTaskReadyWaiter = client.get_waiter("replication_task_ready")
        replication_task_running_waiter: ReplicationTaskRunningWaiter = client.get_waiter("replication_task_running")
        replication_task_stopped_waiter: ReplicationTaskStoppedWaiter = client.get_waiter("replication_task_stopped")
        test_connection_succeeds_waiter: TestConnectionSucceedsWaiter = client.get_waiter("test_connection_succeeds")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeConnectionsMessageWaitTypeDef,
    DescribeEndpointsMessageWaitTypeDef,
    DescribeExtensionPackAssociationsMessageWaitTypeDef,
    DescribeMetadataModelAssessmentsMessageWaitTypeDef,
    DescribeMetadataModelConversionsMessageWaitExtraTypeDef,
    DescribeMetadataModelConversionsMessageWaitTypeDef,
    DescribeMetadataModelCreationsMessageWaitExtraTypeDef,
    DescribeMetadataModelCreationsMessageWaitTypeDef,
    DescribeMetadataModelExportsAsScriptMessageWaitTypeDef,
    DescribeMetadataModelExportsToTargetMessageWaitTypeDef,
    DescribeMetadataModelImportsMessageWaitTypeDef,
    DescribeReplicationInstancesMessageWaitExtraTypeDef,
    DescribeReplicationInstancesMessageWaitTypeDef,
    DescribeReplicationTasksMessageWaitExtraExtraExtraTypeDef,
    DescribeReplicationTasksMessageWaitExtraExtraTypeDef,
    DescribeReplicationTasksMessageWaitExtraTypeDef,
    DescribeReplicationTasksMessageWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "EndpointDeletedWaiter",
    "ExtensionPackAssociatedWaiter",
    "MetadataModelAssessedWaiter",
    "MetadataModelConversionCancelledWaiter",
    "MetadataModelConvertedWaiter",
    "MetadataModelCreatedWaiter",
    "MetadataModelCreationCancelledWaiter",
    "MetadataModelExportedAsScriptWaiter",
    "MetadataModelExportedToTargetWaiter",
    "MetadataModelImportedWaiter",
    "ReplicationInstanceAvailableWaiter",
    "ReplicationInstanceDeletedWaiter",
    "ReplicationTaskDeletedWaiter",
    "ReplicationTaskReadyWaiter",
    "ReplicationTaskRunningWaiter",
    "ReplicationTaskStoppedWaiter",
    "TestConnectionSucceedsWaiter",
)

class EndpointDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/EndpointDeleted.html#DatabaseMigrationService.Waiter.EndpointDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#endpointdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEndpointsMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/EndpointDeleted.html#DatabaseMigrationService.Waiter.EndpointDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#endpointdeletedwaiter)
        """

class ExtensionPackAssociatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ExtensionPackAssociated.html#DatabaseMigrationService.Waiter.ExtensionPackAssociated)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#extensionpackassociatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeExtensionPackAssociationsMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ExtensionPackAssociated.html#DatabaseMigrationService.Waiter.ExtensionPackAssociated.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#extensionpackassociatedwaiter)
        """

class MetadataModelAssessedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelAssessed.html#DatabaseMigrationService.Waiter.MetadataModelAssessed)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#metadatamodelassessedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMetadataModelAssessmentsMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelAssessed.html#DatabaseMigrationService.Waiter.MetadataModelAssessed.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#metadatamodelassessedwaiter)
        """

class MetadataModelConversionCancelledWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelConversionCancelled.html#DatabaseMigrationService.Waiter.MetadataModelConversionCancelled)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#metadatamodelconversioncancelledwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMetadataModelConversionsMessageWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelConversionCancelled.html#DatabaseMigrationService.Waiter.MetadataModelConversionCancelled.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#metadatamodelconversioncancelledwaiter)
        """

class MetadataModelConvertedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelConverted.html#DatabaseMigrationService.Waiter.MetadataModelConverted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#metadatamodelconvertedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMetadataModelConversionsMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelConverted.html#DatabaseMigrationService.Waiter.MetadataModelConverted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#metadatamodelconvertedwaiter)
        """

class MetadataModelCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelCreated.html#DatabaseMigrationService.Waiter.MetadataModelCreated)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#metadatamodelcreatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMetadataModelCreationsMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelCreated.html#DatabaseMigrationService.Waiter.MetadataModelCreated.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#metadatamodelcreatedwaiter)
        """

class MetadataModelCreationCancelledWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelCreationCancelled.html#DatabaseMigrationService.Waiter.MetadataModelCreationCancelled)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#metadatamodelcreationcancelledwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMetadataModelCreationsMessageWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelCreationCancelled.html#DatabaseMigrationService.Waiter.MetadataModelCreationCancelled.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#metadatamodelcreationcancelledwaiter)
        """

class MetadataModelExportedAsScriptWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelExportedAsScript.html#DatabaseMigrationService.Waiter.MetadataModelExportedAsScript)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#metadatamodelexportedasscriptwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMetadataModelExportsAsScriptMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelExportedAsScript.html#DatabaseMigrationService.Waiter.MetadataModelExportedAsScript.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#metadatamodelexportedasscriptwaiter)
        """

class MetadataModelExportedToTargetWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelExportedToTarget.html#DatabaseMigrationService.Waiter.MetadataModelExportedToTarget)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#metadatamodelexportedtotargetwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMetadataModelExportsToTargetMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelExportedToTarget.html#DatabaseMigrationService.Waiter.MetadataModelExportedToTarget.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#metadatamodelexportedtotargetwaiter)
        """

class MetadataModelImportedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelImported.html#DatabaseMigrationService.Waiter.MetadataModelImported)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#metadatamodelimportedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMetadataModelImportsMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelImported.html#DatabaseMigrationService.Waiter.MetadataModelImported.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#metadatamodelimportedwaiter)
        """

class ReplicationInstanceAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationInstanceAvailable.html#DatabaseMigrationService.Waiter.ReplicationInstanceAvailable)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationinstanceavailablewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationInstancesMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationInstanceAvailable.html#DatabaseMigrationService.Waiter.ReplicationInstanceAvailable.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationinstanceavailablewaiter)
        """

class ReplicationInstanceDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationInstanceDeleted.html#DatabaseMigrationService.Waiter.ReplicationInstanceDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationinstancedeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationInstancesMessageWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationInstanceDeleted.html#DatabaseMigrationService.Waiter.ReplicationInstanceDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationinstancedeletedwaiter)
        """

class ReplicationTaskDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskDeleted.html#DatabaseMigrationService.Waiter.ReplicationTaskDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationTasksMessageWaitExtraExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskDeleted.html#DatabaseMigrationService.Waiter.ReplicationTaskDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskdeletedwaiter)
        """

class ReplicationTaskReadyWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskReady.html#DatabaseMigrationService.Waiter.ReplicationTaskReady)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskreadywaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationTasksMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskReady.html#DatabaseMigrationService.Waiter.ReplicationTaskReady.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskreadywaiter)
        """

class ReplicationTaskRunningWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskRunning.html#DatabaseMigrationService.Waiter.ReplicationTaskRunning)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskrunningwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationTasksMessageWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskRunning.html#DatabaseMigrationService.Waiter.ReplicationTaskRunning.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskrunningwaiter)
        """

class ReplicationTaskStoppedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskStopped.html#DatabaseMigrationService.Waiter.ReplicationTaskStopped)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskstoppedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationTasksMessageWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskStopped.html#DatabaseMigrationService.Waiter.ReplicationTaskStopped.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskstoppedwaiter)
        """

class TestConnectionSucceedsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/TestConnectionSucceeds.html#DatabaseMigrationService.Waiter.TestConnectionSucceeds)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#testconnectionsucceedswaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeConnectionsMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/TestConnectionSucceeds.html#DatabaseMigrationService.Waiter.TestConnectionSucceeds.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#testconnectionsucceedswaiter)
        """
