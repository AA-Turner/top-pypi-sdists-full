"""
Type annotations for dms service client waiters.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_dms.client import DatabaseMigrationServiceClient
    from mypy_boto3_dms.waiter import (
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

    session = Session()
    client: DatabaseMigrationServiceClient = session.client("dms")

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

from botocore.waiter import Waiter

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


class EndpointDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/EndpointDeleted.html#DatabaseMigrationService.Waiter.EndpointDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#endpointdeletedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEndpointsMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/EndpointDeleted.html#DatabaseMigrationService.Waiter.EndpointDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#endpointdeletedwaiter)
        """


class ExtensionPackAssociatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ExtensionPackAssociated.html#DatabaseMigrationService.Waiter.ExtensionPackAssociated)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#extensionpackassociatedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeExtensionPackAssociationsMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ExtensionPackAssociated.html#DatabaseMigrationService.Waiter.ExtensionPackAssociated.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#extensionpackassociatedwaiter)
        """


class MetadataModelAssessedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelAssessed.html#DatabaseMigrationService.Waiter.MetadataModelAssessed)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#metadatamodelassessedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMetadataModelAssessmentsMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelAssessed.html#DatabaseMigrationService.Waiter.MetadataModelAssessed.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#metadatamodelassessedwaiter)
        """


class MetadataModelConversionCancelledWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelConversionCancelled.html#DatabaseMigrationService.Waiter.MetadataModelConversionCancelled)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#metadatamodelconversioncancelledwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMetadataModelConversionsMessageWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelConversionCancelled.html#DatabaseMigrationService.Waiter.MetadataModelConversionCancelled.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#metadatamodelconversioncancelledwaiter)
        """


class MetadataModelConvertedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelConverted.html#DatabaseMigrationService.Waiter.MetadataModelConverted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#metadatamodelconvertedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMetadataModelConversionsMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelConverted.html#DatabaseMigrationService.Waiter.MetadataModelConverted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#metadatamodelconvertedwaiter)
        """


class MetadataModelCreatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelCreated.html#DatabaseMigrationService.Waiter.MetadataModelCreated)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#metadatamodelcreatedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMetadataModelCreationsMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelCreated.html#DatabaseMigrationService.Waiter.MetadataModelCreated.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#metadatamodelcreatedwaiter)
        """


class MetadataModelCreationCancelledWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelCreationCancelled.html#DatabaseMigrationService.Waiter.MetadataModelCreationCancelled)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#metadatamodelcreationcancelledwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMetadataModelCreationsMessageWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelCreationCancelled.html#DatabaseMigrationService.Waiter.MetadataModelCreationCancelled.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#metadatamodelcreationcancelledwaiter)
        """


class MetadataModelExportedAsScriptWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelExportedAsScript.html#DatabaseMigrationService.Waiter.MetadataModelExportedAsScript)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#metadatamodelexportedasscriptwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMetadataModelExportsAsScriptMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelExportedAsScript.html#DatabaseMigrationService.Waiter.MetadataModelExportedAsScript.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#metadatamodelexportedasscriptwaiter)
        """


class MetadataModelExportedToTargetWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelExportedToTarget.html#DatabaseMigrationService.Waiter.MetadataModelExportedToTarget)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#metadatamodelexportedtotargetwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMetadataModelExportsToTargetMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelExportedToTarget.html#DatabaseMigrationService.Waiter.MetadataModelExportedToTarget.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#metadatamodelexportedtotargetwaiter)
        """


class MetadataModelImportedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelImported.html#DatabaseMigrationService.Waiter.MetadataModelImported)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#metadatamodelimportedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMetadataModelImportsMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/MetadataModelImported.html#DatabaseMigrationService.Waiter.MetadataModelImported.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#metadatamodelimportedwaiter)
        """


class ReplicationInstanceAvailableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationInstanceAvailable.html#DatabaseMigrationService.Waiter.ReplicationInstanceAvailable)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#replicationinstanceavailablewaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationInstancesMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationInstanceAvailable.html#DatabaseMigrationService.Waiter.ReplicationInstanceAvailable.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#replicationinstanceavailablewaiter)
        """


class ReplicationInstanceDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationInstanceDeleted.html#DatabaseMigrationService.Waiter.ReplicationInstanceDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#replicationinstancedeletedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationInstancesMessageWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationInstanceDeleted.html#DatabaseMigrationService.Waiter.ReplicationInstanceDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#replicationinstancedeletedwaiter)
        """


class ReplicationTaskDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskDeleted.html#DatabaseMigrationService.Waiter.ReplicationTaskDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#replicationtaskdeletedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationTasksMessageWaitExtraExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskDeleted.html#DatabaseMigrationService.Waiter.ReplicationTaskDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#replicationtaskdeletedwaiter)
        """


class ReplicationTaskReadyWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskReady.html#DatabaseMigrationService.Waiter.ReplicationTaskReady)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#replicationtaskreadywaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationTasksMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskReady.html#DatabaseMigrationService.Waiter.ReplicationTaskReady.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#replicationtaskreadywaiter)
        """


class ReplicationTaskRunningWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskRunning.html#DatabaseMigrationService.Waiter.ReplicationTaskRunning)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#replicationtaskrunningwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationTasksMessageWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskRunning.html#DatabaseMigrationService.Waiter.ReplicationTaskRunning.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#replicationtaskrunningwaiter)
        """


class ReplicationTaskStoppedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskStopped.html#DatabaseMigrationService.Waiter.ReplicationTaskStopped)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#replicationtaskstoppedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationTasksMessageWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/ReplicationTaskStopped.html#DatabaseMigrationService.Waiter.ReplicationTaskStopped.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#replicationtaskstoppedwaiter)
        """


class TestConnectionSucceedsWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/TestConnectionSucceeds.html#DatabaseMigrationService.Waiter.TestConnectionSucceeds)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#testconnectionsucceedswaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeConnectionsMessageWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms/waiter/TestConnectionSucceeds.html#DatabaseMigrationService.Waiter.TestConnectionSucceeds.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dms/waiters/#testconnectionsucceedswaiter)
        """
