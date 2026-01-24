"""
Main interface for healthlake service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_healthlake import (
        Client,
        FHIRDatastoreActiveWaiter,
        FHIRDatastoreDeletedWaiter,
        FHIRExportJobCompletedWaiter,
        FHIRImportJobCompletedWaiter,
        HealthLakeClient,
    )

    session = get_session()
    async with session.create_client("healthlake") as client:
        client: HealthLakeClient
        ...


    fhir_datastore_active_waiter: FHIRDatastoreActiveWaiter = client.get_waiter("fhir_datastore_active")
    fhir_datastore_deleted_waiter: FHIRDatastoreDeletedWaiter = client.get_waiter("fhir_datastore_deleted")
    fhir_export_job_completed_waiter: FHIRExportJobCompletedWaiter = client.get_waiter("fhir_export_job_completed")
    fhir_import_job_completed_waiter: FHIRImportJobCompletedWaiter = client.get_waiter("fhir_import_job_completed")
    ```
"""

from .client import HealthLakeClient
from .waiter import (
    FHIRDatastoreActiveWaiter,
    FHIRDatastoreDeletedWaiter,
    FHIRExportJobCompletedWaiter,
    FHIRImportJobCompletedWaiter,
)

Client = HealthLakeClient

__all__ = (
    "Client",
    "FHIRDatastoreActiveWaiter",
    "FHIRDatastoreDeletedWaiter",
    "FHIRExportJobCompletedWaiter",
    "FHIRImportJobCompletedWaiter",
    "HealthLakeClient",
)
