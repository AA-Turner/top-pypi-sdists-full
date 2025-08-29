"""
Type annotations for healthlake service client waiters.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_healthlake.client import HealthLakeClient
    from types_boto3_healthlake.waiter import (
        FHIRDatastoreActiveWaiter,
        FHIRDatastoreDeletedWaiter,
        FHIRExportJobCompletedWaiter,
        FHIRImportJobCompletedWaiter,
    )

    session = Session()
    client: HealthLakeClient = session.client("healthlake")

    fhir_datastore_active_waiter: FHIRDatastoreActiveWaiter = client.get_waiter("fhir_datastore_active")
    fhir_datastore_deleted_waiter: FHIRDatastoreDeletedWaiter = client.get_waiter("fhir_datastore_deleted")
    fhir_export_job_completed_waiter: FHIRExportJobCompletedWaiter = client.get_waiter("fhir_export_job_completed")
    fhir_import_job_completed_waiter: FHIRImportJobCompletedWaiter = client.get_waiter("fhir_import_job_completed")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

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


class FHIRDatastoreActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/waiter/FHIRDatastoreActive.html#HealthLake.Waiter.FHIRDatastoreActive)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/waiters/#fhirdatastoreactivewaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFHIRDatastoreRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/waiter/FHIRDatastoreActive.html#HealthLake.Waiter.FHIRDatastoreActive.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/waiters/#fhirdatastoreactivewaiter)
        """


class FHIRDatastoreDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/waiter/FHIRDatastoreDeleted.html#HealthLake.Waiter.FHIRDatastoreDeleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/waiters/#fhirdatastoredeletedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFHIRDatastoreRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/waiter/FHIRDatastoreDeleted.html#HealthLake.Waiter.FHIRDatastoreDeleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/waiters/#fhirdatastoredeletedwaiter)
        """


class FHIRExportJobCompletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/waiter/FHIRExportJobCompleted.html#HealthLake.Waiter.FHIRExportJobCompleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/waiters/#fhirexportjobcompletedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFHIRExportJobRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/waiter/FHIRExportJobCompleted.html#HealthLake.Waiter.FHIRExportJobCompleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/waiters/#fhirexportjobcompletedwaiter)
        """


class FHIRImportJobCompletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/waiter/FHIRImportJobCompleted.html#HealthLake.Waiter.FHIRImportJobCompleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/waiters/#fhirimportjobcompletedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFHIRImportJobRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/waiter/FHIRImportJobCompleted.html#HealthLake.Waiter.FHIRImportJobCompleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/waiters/#fhirimportjobcompletedwaiter)
        """
