"""
Main interface for medical-imaging service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medical_imaging/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_medical_imaging import (
        Client,
        HealthImagingClient,
        ListDICOMImportJobsPaginator,
        ListDatastoresPaginator,
        ListImageSetVersionsPaginator,
        SearchImageSetsPaginator,
    )

    session = get_session()
    async with session.create_client("medical-imaging") as client:
        client: HealthImagingClient
        ...


    list_dicom_import_jobs_paginator: ListDICOMImportJobsPaginator = client.get_paginator("list_dicom_import_jobs")
    list_datastores_paginator: ListDatastoresPaginator = client.get_paginator("list_datastores")
    list_image_set_versions_paginator: ListImageSetVersionsPaginator = client.get_paginator("list_image_set_versions")
    search_image_sets_paginator: SearchImageSetsPaginator = client.get_paginator("search_image_sets")
    ```
"""

from .client import HealthImagingClient
from .paginator import (
    ListDatastoresPaginator,
    ListDICOMImportJobsPaginator,
    ListImageSetVersionsPaginator,
    SearchImageSetsPaginator,
)

Client = HealthImagingClient


__all__ = (
    "Client",
    "HealthImagingClient",
    "ListDICOMImportJobsPaginator",
    "ListDatastoresPaginator",
    "ListImageSetVersionsPaginator",
    "SearchImageSetsPaginator",
)
