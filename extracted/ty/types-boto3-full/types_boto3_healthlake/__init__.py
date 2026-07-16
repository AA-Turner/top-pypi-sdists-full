"""
Main interface for healthlake service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_healthlake import (
        Client,
        DataTransformationJobCompletedWaiter,
        FHIRDatastoreActiveWaiter,
        FHIRDatastoreDeletedWaiter,
        FHIRExportJobCompletedWaiter,
        FHIRImportJobCompletedWaiter,
        HealthLakeClient,
        ListDataTransformationJobsPaginator,
        ListDataTransformationProfileVersionsPaginator,
        ListDataTransformationProfilesPaginator,
    )

    session = Session()
    client: HealthLakeClient = session.client("healthlake")

    data_transformation_job_completed_waiter: DataTransformationJobCompletedWaiter = client.get_waiter("data_transformation_job_completed")
    fhir_datastore_active_waiter: FHIRDatastoreActiveWaiter = client.get_waiter("fhir_datastore_active")
    fhir_datastore_deleted_waiter: FHIRDatastoreDeletedWaiter = client.get_waiter("fhir_datastore_deleted")
    fhir_export_job_completed_waiter: FHIRExportJobCompletedWaiter = client.get_waiter("fhir_export_job_completed")
    fhir_import_job_completed_waiter: FHIRImportJobCompletedWaiter = client.get_waiter("fhir_import_job_completed")

    list_data_transformation_jobs_paginator: ListDataTransformationJobsPaginator = client.get_paginator("list_data_transformation_jobs")
    list_data_transformation_profile_versions_paginator: ListDataTransformationProfileVersionsPaginator = client.get_paginator("list_data_transformation_profile_versions")
    list_data_transformation_profiles_paginator: ListDataTransformationProfilesPaginator = client.get_paginator("list_data_transformation_profiles")
    ```
"""

from .client import HealthLakeClient
from .paginator import (
    ListDataTransformationJobsPaginator,
    ListDataTransformationProfilesPaginator,
    ListDataTransformationProfileVersionsPaginator,
)
from .waiter import (
    DataTransformationJobCompletedWaiter,
    FHIRDatastoreActiveWaiter,
    FHIRDatastoreDeletedWaiter,
    FHIRExportJobCompletedWaiter,
    FHIRImportJobCompletedWaiter,
)

Client = HealthLakeClient


__all__ = (
    "Client",
    "DataTransformationJobCompletedWaiter",
    "FHIRDatastoreActiveWaiter",
    "FHIRDatastoreDeletedWaiter",
    "FHIRExportJobCompletedWaiter",
    "FHIRImportJobCompletedWaiter",
    "HealthLakeClient",
    "ListDataTransformationJobsPaginator",
    "ListDataTransformationProfileVersionsPaginator",
    "ListDataTransformationProfilesPaginator",
)
