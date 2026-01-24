"""
Type annotations for healthlake service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_healthlake.client import HealthLakeClient

    session = get_session()
    async with session.create_client("healthlake") as client:
        client: HealthLakeClient
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    CreateFHIRDatastoreRequestTypeDef,
    CreateFHIRDatastoreResponseTypeDef,
    DeleteFHIRDatastoreRequestTypeDef,
    DeleteFHIRDatastoreResponseTypeDef,
    DescribeFHIRDatastoreRequestTypeDef,
    DescribeFHIRDatastoreResponseTypeDef,
    DescribeFHIRExportJobRequestTypeDef,
    DescribeFHIRExportJobResponseTypeDef,
    DescribeFHIRImportJobRequestTypeDef,
    DescribeFHIRImportJobResponseTypeDef,
    ListFHIRDatastoresRequestTypeDef,
    ListFHIRDatastoresResponseTypeDef,
    ListFHIRExportJobsRequestTypeDef,
    ListFHIRExportJobsResponseTypeDef,
    ListFHIRImportJobsRequestTypeDef,
    ListFHIRImportJobsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartFHIRExportJobRequestTypeDef,
    StartFHIRExportJobResponseTypeDef,
    StartFHIRImportJobRequestTypeDef,
    StartFHIRImportJobResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
)
from .waiter import (
    FHIRDatastoreActiveWaiter,
    FHIRDatastoreDeletedWaiter,
    FHIRExportJobCompletedWaiter,
    FHIRImportJobCompletedWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("HealthLakeClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class HealthLakeClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        HealthLakeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#generate_presigned_url)
        """

    async def create_fhir_datastore(
        self, **kwargs: Unpack[CreateFHIRDatastoreRequestTypeDef]
    ) -> CreateFHIRDatastoreResponseTypeDef:
        """
        Create a FHIR-enabled data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/create_fhir_datastore.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#create_fhir_datastore)
        """

    async def delete_fhir_datastore(
        self, **kwargs: Unpack[DeleteFHIRDatastoreRequestTypeDef]
    ) -> DeleteFHIRDatastoreResponseTypeDef:
        """
        Delete a FHIR-enabled data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/delete_fhir_datastore.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#delete_fhir_datastore)
        """

    async def describe_fhir_datastore(
        self, **kwargs: Unpack[DescribeFHIRDatastoreRequestTypeDef]
    ) -> DescribeFHIRDatastoreResponseTypeDef:
        """
        Get properties for a FHIR-enabled data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/describe_fhir_datastore.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#describe_fhir_datastore)
        """

    async def describe_fhir_export_job(
        self, **kwargs: Unpack[DescribeFHIRExportJobRequestTypeDef]
    ) -> DescribeFHIRExportJobResponseTypeDef:
        """
        Get FHIR export job properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/describe_fhir_export_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#describe_fhir_export_job)
        """

    async def describe_fhir_import_job(
        self, **kwargs: Unpack[DescribeFHIRImportJobRequestTypeDef]
    ) -> DescribeFHIRImportJobResponseTypeDef:
        """
        Get the import job properties to learn more about the job or job progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/describe_fhir_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#describe_fhir_import_job)
        """

    async def list_fhir_datastores(
        self, **kwargs: Unpack[ListFHIRDatastoresRequestTypeDef]
    ) -> ListFHIRDatastoresResponseTypeDef:
        """
        List all FHIR-enabled data stores in a user's account, regardless of data store
        status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/list_fhir_datastores.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#list_fhir_datastores)
        """

    async def list_fhir_export_jobs(
        self, **kwargs: Unpack[ListFHIRExportJobsRequestTypeDef]
    ) -> ListFHIRExportJobsResponseTypeDef:
        """
        Lists all FHIR export jobs associated with an account and their statuses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/list_fhir_export_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#list_fhir_export_jobs)
        """

    async def list_fhir_import_jobs(
        self, **kwargs: Unpack[ListFHIRImportJobsRequestTypeDef]
    ) -> ListFHIRImportJobsResponseTypeDef:
        """
        List all FHIR import jobs associated with an account and their statuses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/list_fhir_import_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#list_fhir_import_jobs)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of all existing tags associated with a data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#list_tags_for_resource)
        """

    async def start_fhir_export_job(
        self, **kwargs: Unpack[StartFHIRExportJobRequestTypeDef]
    ) -> StartFHIRExportJobResponseTypeDef:
        """
        Start a FHIR export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/start_fhir_export_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#start_fhir_export_job)
        """

    async def start_fhir_import_job(
        self, **kwargs: Unpack[StartFHIRImportJobRequestTypeDef]
    ) -> StartFHIRImportJobResponseTypeDef:
        """
        Start importing bulk FHIR data into an ACTIVE data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/start_fhir_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#start_fhir_import_job)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Add a user-specifed key and value tag to a data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Remove a user-specifed key and value tag from a data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#untag_resource)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["fhir_datastore_active"]
    ) -> FHIRDatastoreActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["fhir_datastore_deleted"]
    ) -> FHIRDatastoreDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["fhir_export_job_completed"]
    ) -> FHIRExportJobCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["fhir_import_job_completed"]
    ) -> FHIRImportJobCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#get_waiter)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/)
        """
