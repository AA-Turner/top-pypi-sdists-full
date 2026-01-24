"""
Type annotations for healthlake service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_healthlake.client import HealthLakeClient
    from types_aiobotocore_healthlake.waiter import (
        FHIRDatastoreActiveWaiter,
        FHIRDatastoreDeletedWaiter,
        FHIRExportJobCompletedWaiter,
        FHIRImportJobCompletedWaiter,
    )

    session = get_session()
    async with session.create_client("healthlake") as client:
        client: HealthLakeClient

        fhir_datastore_active_waiter: FHIRDatastoreActiveWaiter = client.get_waiter("fhir_datastore_active")
        fhir_datastore_deleted_waiter: FHIRDatastoreDeletedWaiter = client.get_waiter("fhir_datastore_deleted")
        fhir_export_job_completed_waiter: FHIRExportJobCompletedWaiter = client.get_waiter("fhir_export_job_completed")
        fhir_import_job_completed_waiter: FHIRImportJobCompletedWaiter = client.get_waiter("fhir_import_job_completed")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeFHIRDatastoreRequestWaitExtraTypeDef,
    DescribeFHIRDatastoreRequestWaitTypeDef,
    DescribeFHIRExportJobRequestWaitTypeDef,
    DescribeFHIRImportJobRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "FHIRDatastoreActiveWaiter",
    "FHIRDatastoreDeletedWaiter",
    "FHIRExportJobCompletedWaiter",
    "FHIRImportJobCompletedWaiter",
)

class FHIRDatastoreActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/waiter/FHIRDatastoreActive.html#HealthLake.Waiter.FHIRDatastoreActive)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/waiters/#fhirdatastoreactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFHIRDatastoreRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/waiter/FHIRDatastoreActive.html#HealthLake.Waiter.FHIRDatastoreActive.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/waiters/#fhirdatastoreactivewaiter)
        """

class FHIRDatastoreDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/waiter/FHIRDatastoreDeleted.html#HealthLake.Waiter.FHIRDatastoreDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/waiters/#fhirdatastoredeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFHIRDatastoreRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/waiter/FHIRDatastoreDeleted.html#HealthLake.Waiter.FHIRDatastoreDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/waiters/#fhirdatastoredeletedwaiter)
        """

class FHIRExportJobCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/waiter/FHIRExportJobCompleted.html#HealthLake.Waiter.FHIRExportJobCompleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/waiters/#fhirexportjobcompletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFHIRExportJobRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/waiter/FHIRExportJobCompleted.html#HealthLake.Waiter.FHIRExportJobCompleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/waiters/#fhirexportjobcompletedwaiter)
        """

class FHIRImportJobCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/waiter/FHIRImportJobCompleted.html#HealthLake.Waiter.FHIRImportJobCompleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/waiters/#fhirimportjobcompletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFHIRImportJobRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/waiter/FHIRImportJobCompleted.html#HealthLake.Waiter.FHIRImportJobCompleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/waiters/#fhirimportjobcompletedwaiter)
        """
