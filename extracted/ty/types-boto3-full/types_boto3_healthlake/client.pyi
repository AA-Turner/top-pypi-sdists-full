"""
Type annotations for healthlake service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_healthlake.client import HealthLakeClient

    session = Session()
    client: HealthLakeClient = session.client("healthlake")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListDataTransformationJobsPaginator,
    ListDataTransformationProfilesPaginator,
    ListDataTransformationProfileVersionsPaginator,
)
from .type_defs import (
    CreateDataTransformationProfileRequestTypeDef,
    CreateDataTransformationProfileResponseTypeDef,
    CreateFHIRDatastoreRequestTypeDef,
    CreateFHIRDatastoreResponseTypeDef,
    DeleteDataTransformationProfileRequestTypeDef,
    DeleteDataTransformationProfileResponseTypeDef,
    DeleteFHIRDatastoreRequestTypeDef,
    DeleteFHIRDatastoreResponseTypeDef,
    DescribeDataTransformationJobRequestTypeDef,
    DescribeDataTransformationJobResponseTypeDef,
    DescribeFHIRDatastoreRequestTypeDef,
    DescribeFHIRDatastoreResponseTypeDef,
    DescribeFHIRExportJobRequestTypeDef,
    DescribeFHIRExportJobResponseTypeDef,
    DescribeFHIRImportJobRequestTypeDef,
    DescribeFHIRImportJobResponseTypeDef,
    GetDataTransformationProfileRequestTypeDef,
    GetDataTransformationProfileResponseTypeDef,
    ListDataTransformationJobsRequestTypeDef,
    ListDataTransformationJobsResponseTypeDef,
    ListDataTransformationProfilesRequestTypeDef,
    ListDataTransformationProfilesResponseTypeDef,
    ListDataTransformationProfileVersionsRequestTypeDef,
    ListDataTransformationProfileVersionsResponseTypeDef,
    ListFHIRDatastoresRequestTypeDef,
    ListFHIRDatastoresResponseTypeDef,
    ListFHIRExportJobsRequestTypeDef,
    ListFHIRExportJobsResponseTypeDef,
    ListFHIRImportJobsRequestTypeDef,
    ListFHIRImportJobsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PublishDataTransformationProfileRequestTypeDef,
    PublishDataTransformationProfileResponseTypeDef,
    RestoreFHIRDatastoreRequestTypeDef,
    RestoreFHIRDatastoreResponseTypeDef,
    StartDataTransformationJobRequestTypeDef,
    StartDataTransformationJobResponseTypeDef,
    StartFHIRExportJobRequestTypeDef,
    StartFHIRExportJobResponseTypeDef,
    StartFHIRImportJobRequestTypeDef,
    StartFHIRImportJobResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateDataTransformationProfileRequestTypeDef,
    UpdateDataTransformationProfileResponseTypeDef,
    UpdateFHIRDatastoreRequestTypeDef,
    UpdateFHIRDatastoreResponseTypeDef,
    UpdateProfileWithAgentRequestTypeDef,
    UpdateProfileWithAgentResponseTypeDef,
)
from .waiter import (
    DataTransformationJobCompletedWaiter,
    FHIRDatastoreActiveWaiter,
    FHIRDatastoreDeletedWaiter,
    FHIRExportJobCompletedWaiter,
    FHIRImportJobCompletedWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("HealthLakeClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    AgentMessageOutOfContextException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    ConversationNotFoundException: type[BotocoreClientError]
    FailedDependencyException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    NotImplementedOperationException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    UnauthorizedException: type[BotocoreClientError]
    UnsupportedMIMETypeException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class HealthLakeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        HealthLakeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#generate_presigned_url)
        """

    def create_data_transformation_profile(
        self, **kwargs: Unpack[CreateDataTransformationProfileRequestTypeDef]
    ) -> CreateDataTransformationProfileResponseTypeDef:
        """
        Creates a data transformation profile in DRAFT state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/create_data_transformation_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#create_data_transformation_profile)
        """

    def create_fhir_datastore(
        self, **kwargs: Unpack[CreateFHIRDatastoreRequestTypeDef]
    ) -> CreateFHIRDatastoreResponseTypeDef:
        """
        Create a FHIR-enabled data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/create_fhir_datastore.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#create_fhir_datastore)
        """

    def delete_data_transformation_profile(
        self, **kwargs: Unpack[DeleteDataTransformationProfileRequestTypeDef]
    ) -> DeleteDataTransformationProfileResponseTypeDef:
        """
        Deletes a data transformation profile and all its versions, including the DRAFT
        and all published versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/delete_data_transformation_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#delete_data_transformation_profile)
        """

    def delete_fhir_datastore(
        self, **kwargs: Unpack[DeleteFHIRDatastoreRequestTypeDef]
    ) -> DeleteFHIRDatastoreResponseTypeDef:
        """
        Delete a FHIR-enabled data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/delete_fhir_datastore.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#delete_fhir_datastore)
        """

    def describe_data_transformation_job(
        self, **kwargs: Unpack[DescribeDataTransformationJobRequestTypeDef]
    ) -> DescribeDataTransformationJobResponseTypeDef:
        """
        Describes a data transformation job, including its current status,
        configuration, and progress information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/describe_data_transformation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#describe_data_transformation_job)
        """

    def describe_fhir_datastore(
        self, **kwargs: Unpack[DescribeFHIRDatastoreRequestTypeDef]
    ) -> DescribeFHIRDatastoreResponseTypeDef:
        """
        Get properties for a FHIR-enabled data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/describe_fhir_datastore.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#describe_fhir_datastore)
        """

    def describe_fhir_export_job(
        self, **kwargs: Unpack[DescribeFHIRExportJobRequestTypeDef]
    ) -> DescribeFHIRExportJobResponseTypeDef:
        """
        Get FHIR export job properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/describe_fhir_export_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#describe_fhir_export_job)
        """

    def describe_fhir_import_job(
        self, **kwargs: Unpack[DescribeFHIRImportJobRequestTypeDef]
    ) -> DescribeFHIRImportJobResponseTypeDef:
        """
        Get the import job properties to learn more about the job or job progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/describe_fhir_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#describe_fhir_import_job)
        """

    def get_data_transformation_profile(
        self, **kwargs: Unpack[GetDataTransformationProfileRequestTypeDef]
    ) -> GetDataTransformationProfileResponseTypeDef:
        """
        Retrieves a data transformation profile's metadata and profile content at a
        specific version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/get_data_transformation_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#get_data_transformation_profile)
        """

    def list_data_transformation_jobs(
        self, **kwargs: Unpack[ListDataTransformationJobsRequestTypeDef]
    ) -> ListDataTransformationJobsResponseTypeDef:
        """
        Lists data transformation jobs for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/list_data_transformation_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#list_data_transformation_jobs)
        """

    def list_data_transformation_profile_versions(
        self, **kwargs: Unpack[ListDataTransformationProfileVersionsRequestTypeDef]
    ) -> ListDataTransformationProfileVersionsResponseTypeDef:
        """
        Lists all versions of a specific data transformation profile (DRAFT and
        published), in reverse chronological order (newest first).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/list_data_transformation_profile_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#list_data_transformation_profile_versions)
        """

    def list_data_transformation_profiles(
        self, **kwargs: Unpack[ListDataTransformationProfilesRequestTypeDef]
    ) -> ListDataTransformationProfilesResponseTypeDef:
        """
        Lists all data transformation profiles in your account, returning the latest
        version summary for each.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/list_data_transformation_profiles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#list_data_transformation_profiles)
        """

    def list_fhir_datastores(
        self, **kwargs: Unpack[ListFHIRDatastoresRequestTypeDef]
    ) -> ListFHIRDatastoresResponseTypeDef:
        """
        List all FHIR-enabled data stores in a user's account, regardless of data store
        status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/list_fhir_datastores.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#list_fhir_datastores)
        """

    def list_fhir_export_jobs(
        self, **kwargs: Unpack[ListFHIRExportJobsRequestTypeDef]
    ) -> ListFHIRExportJobsResponseTypeDef:
        """
        Lists all FHIR export jobs associated with an account and their statuses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/list_fhir_export_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#list_fhir_export_jobs)
        """

    def list_fhir_import_jobs(
        self, **kwargs: Unpack[ListFHIRImportJobsRequestTypeDef]
    ) -> ListFHIRImportJobsResponseTypeDef:
        """
        List all FHIR import jobs associated with an account and their statuses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/list_fhir_import_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#list_fhir_import_jobs)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of all existing tags associated with a data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#list_tags_for_resource)
        """

    def publish_data_transformation_profile(
        self, **kwargs: Unpack[PublishDataTransformationProfileRequestTypeDef]
    ) -> PublishDataTransformationProfileResponseTypeDef:
        """
        Promotes the current DRAFT version of a data transformation profile to a new
        immutable published version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/publish_data_transformation_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#publish_data_transformation_profile)
        """

    def restore_fhir_datastore(
        self, **kwargs: Unpack[RestoreFHIRDatastoreRequestTypeDef]
    ) -> RestoreFHIRDatastoreResponseTypeDef:
        """
        Restore a backup-enabled data store to a point in time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/restore_fhir_datastore.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#restore_fhir_datastore)
        """

    def start_data_transformation_job(
        self, **kwargs: Unpack[StartDataTransformationJobRequestTypeDef]
    ) -> StartDataTransformationJobResponseTypeDef:
        """
        Starts an asynchronous data transformation job that converts source files from
        Amazon Simple Storage Service (Amazon S3) and writes the output to Amazon S3 or
        HealthLake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/start_data_transformation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#start_data_transformation_job)
        """

    def start_fhir_export_job(
        self, **kwargs: Unpack[StartFHIRExportJobRequestTypeDef]
    ) -> StartFHIRExportJobResponseTypeDef:
        """
        Start a FHIR export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/start_fhir_export_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#start_fhir_export_job)
        """

    def start_fhir_import_job(
        self, **kwargs: Unpack[StartFHIRImportJobRequestTypeDef]
    ) -> StartFHIRImportJobResponseTypeDef:
        """
        Start importing bulk FHIR data into an ACTIVE data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/start_fhir_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#start_fhir_import_job)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Add a user-specifed key and value tag to a data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Remove a user-specifed key and value tag from a data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#untag_resource)
        """

    def update_data_transformation_profile(
        self, **kwargs: Unpack[UpdateDataTransformationProfileRequestTypeDef]
    ) -> UpdateDataTransformationProfileResponseTypeDef:
        """
        Updates the DRAFT version (version 0) of a data transformation profile with new
        profile content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/update_data_transformation_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#update_data_transformation_profile)
        """

    def update_fhir_datastore(
        self, **kwargs: Unpack[UpdateFHIRDatastoreRequestTypeDef]
    ) -> UpdateFHIRDatastoreResponseTypeDef:
        """
        Update the properties of a FHIR-enabled data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/update_fhir_datastore.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#update_fhir_datastore)
        """

    def update_profile_with_agent(
        self, **kwargs: Unpack[UpdateProfileWithAgentRequestTypeDef]
    ) -> UpdateProfileWithAgentResponseTypeDef:
        """
        Updates a data transformation profile using chat-based interaction with an
        agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/update_profile_with_agent.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#update_profile_with_agent)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_transformation_jobs"]
    ) -> ListDataTransformationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_transformation_profile_versions"]
    ) -> ListDataTransformationProfileVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_transformation_profiles"]
    ) -> ListDataTransformationProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["data_transformation_job_completed"]
    ) -> DataTransformationJobCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["fhir_datastore_active"]
    ) -> FHIRDatastoreActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["fhir_datastore_deleted"]
    ) -> FHIRDatastoreDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["fhir_export_job_completed"]
    ) -> FHIRExportJobCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["fhir_import_job_completed"]
    ) -> FHIRImportJobCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_healthlake/client/#get_waiter)
        """
