"""
Type annotations for glacier service ServiceResource.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_glacier.service_resource import GlacierServiceResource
    import types_boto3_glacier.service_resource as glacier_resources

    session = Session()
    resource: GlacierServiceResource = session.resource("glacier")

    my_account: glacier_resources.Account = resource.Account(...)
    my_archive: glacier_resources.Archive = resource.Archive(...)
    my_job: glacier_resources.Job = resource.Job(...)
    my_multipart_upload: glacier_resources.MultipartUpload = resource.MultipartUpload(...)
    my_notification: glacier_resources.Notification = resource.Notification(...)
    my_vault: glacier_resources.Vault = resource.Vault(...)
```
"""

from __future__ import annotations

import sys

from boto3.resources.base import ResourceMeta, ServiceResource
from boto3.resources.collection import ResourceCollection

from .client import GlacierClient
from .literals import ActionCodeType, StatusCodeType
from .type_defs import (
    ArchiveCreationOutputTypeDef,
    CompleteMultipartUploadInputMultipartUploadCompleteTypeDef,
    CreateVaultInputAccountCreateVaultTypeDef,
    CreateVaultInputServiceResourceCreateVaultTypeDef,
    CreateVaultOutputTypeDef,
    GetJobOutputInputJobGetOutputTypeDef,
    GetJobOutputOutputTypeDef,
    InitiateMultipartUploadInputVaultInitiateMultipartUploadTypeDef,
    InventoryRetrievalJobDescriptionTypeDef,
    ListPartsInputMultipartUploadPartsTypeDef,
    ListPartsOutputTypeDef,
    OutputLocationOutputTypeDef,
    SelectParametersTypeDef,
    SetVaultNotificationsInputNotificationSetTypeDef,
    UploadArchiveInputVaultUploadArchiveTypeDef,
    UploadMultipartPartInputMultipartUploadUploadPartTypeDef,
    UploadMultipartPartOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import list as List
    from collections.abc import Iterator, Sequence
else:
    from typing import Iterator, List, Sequence
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "Account",
    "AccountVaultsCollection",
    "Archive",
    "GlacierServiceResource",
    "Job",
    "MultipartUpload",
    "Notification",
    "ServiceResourceVaultsCollection",
    "Vault",
    "VaultCompletedJobsCollection",
    "VaultFailedJobsCollection",
    "VaultJobsCollection",
    "VaultJobsInProgressCollection",
    "VaultMultipartUplaodsCollection",
    "VaultMultipartUploadsCollection",
    "VaultSucceededJobsCollection",
)

class ServiceResourceVaultsCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/service-resource/vaults.html#Glacier.ServiceResource.vaults)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#serviceresourcevaultscollection)
    """
    def all(self) -> ServiceResourceVaultsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/service-resource/vaults.html#Glacier.ServiceResource.all)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#serviceresourcevaultscollection)
        """

    def filter(  # type: ignore[override]
        self, *, marker: str = ..., limit: str = ...
    ) -> ServiceResourceVaultsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/service-resource/vaults.html#filter)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#serviceresourcevaultscollection)
        """

    def limit(self, count: int) -> ServiceResourceVaultsCollection:
        """
        Return at most this many Vaults.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/service-resource/vaults.html#limit)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#serviceresourcevaultscollection)
        """

    def page_size(self, count: int) -> ServiceResourceVaultsCollection:
        """
        Fetch at most this many Vaults per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/service-resource/vaults.html#page_size)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#serviceresourcevaultscollection)
        """

    def pages(self) -> Iterator[List[Vault]]:
        """
        A generator which yields pages of Vaults.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/service-resource/vaults.html#pages)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#serviceresourcevaultscollection)
        """

    def __iter__(self) -> Iterator[Vault]:
        """
        A generator which yields Vaults.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/service-resource/vaults.html#__iter__)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#serviceresourcevaultscollection)
        """

class AccountVaultsCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/account/vaults.html#Glacier.Account.vaults)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#accountvaults)
    """
    def all(self) -> AccountVaultsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/account/vaults.html#Glacier.Account.all)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#accountvaults)
        """

    def filter(  # type: ignore[override]
        self, *, marker: str = ..., limit: str = ...
    ) -> AccountVaultsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/account/vaults.html#filter)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#accountvaults)
        """

    def limit(self, count: int) -> AccountVaultsCollection:
        """
        Return at most this many Vaults.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/account/vaults.html#limit)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#accountvaults)
        """

    def page_size(self, count: int) -> AccountVaultsCollection:
        """
        Fetch at most this many Vaults per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/account/vaults.html#page_size)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#accountvaults)
        """

    def pages(self) -> Iterator[List[Vault]]:
        """
        A generator which yields pages of Vaults.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/account/vaults.html#pages)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#accountvaults)
        """

    def __iter__(self) -> Iterator[Vault]:
        """
        A generator which yields Vaults.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/account/vaults.html#__iter__)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#accountvaults)
        """

class VaultCompletedJobsCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/completed_jobs.html#Glacier.Vault.completed_jobs)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultcompleted_jobs)
    """
    def all(self) -> VaultCompletedJobsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/completed_jobs.html#Glacier.Vault.all)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultcompleted_jobs)
        """

    def filter(  # type: ignore[override]
        self, *, limit: str = ..., marker: str = ..., statuscode: str = ..., completed: str = ...
    ) -> VaultCompletedJobsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/completed_jobs.html#filter)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultcompleted_jobs)
        """

    def limit(self, count: int) -> VaultCompletedJobsCollection:
        """
        Return at most this many Jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/completed_jobs.html#limit)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultcompleted_jobs)
        """

    def page_size(self, count: int) -> VaultCompletedJobsCollection:
        """
        Fetch at most this many Jobs per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/completed_jobs.html#page_size)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultcompleted_jobs)
        """

    def pages(self) -> Iterator[List[Job]]:
        """
        A generator which yields pages of Jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/completed_jobs.html#pages)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultcompleted_jobs)
        """

    def __iter__(self) -> Iterator[Job]:
        """
        A generator which yields Jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/completed_jobs.html#__iter__)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultcompleted_jobs)
        """

class VaultFailedJobsCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/failed_jobs.html#Glacier.Vault.failed_jobs)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultfailed_jobs)
    """
    def all(self) -> VaultFailedJobsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/failed_jobs.html#Glacier.Vault.all)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultfailed_jobs)
        """

    def filter(  # type: ignore[override]
        self, *, limit: str = ..., marker: str = ..., statuscode: str = ..., completed: str = ...
    ) -> VaultFailedJobsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/failed_jobs.html#filter)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultfailed_jobs)
        """

    def limit(self, count: int) -> VaultFailedJobsCollection:
        """
        Return at most this many Jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/failed_jobs.html#limit)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultfailed_jobs)
        """

    def page_size(self, count: int) -> VaultFailedJobsCollection:
        """
        Fetch at most this many Jobs per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/failed_jobs.html#page_size)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultfailed_jobs)
        """

    def pages(self) -> Iterator[List[Job]]:
        """
        A generator which yields pages of Jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/failed_jobs.html#pages)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultfailed_jobs)
        """

    def __iter__(self) -> Iterator[Job]:
        """
        A generator which yields Jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/failed_jobs.html#__iter__)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultfailed_jobs)
        """

class VaultJobsCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/jobs.html#Glacier.Vault.jobs)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultjobs)
    """
    def all(self) -> VaultJobsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/jobs.html#Glacier.Vault.all)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultjobs)
        """

    def filter(  # type: ignore[override]
        self, *, limit: str = ..., marker: str = ..., statuscode: str = ..., completed: str = ...
    ) -> VaultJobsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/jobs.html#filter)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultjobs)
        """

    def limit(self, count: int) -> VaultJobsCollection:
        """
        Return at most this many Jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/jobs.html#limit)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultjobs)
        """

    def page_size(self, count: int) -> VaultJobsCollection:
        """
        Fetch at most this many Jobs per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/jobs.html#page_size)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultjobs)
        """

    def pages(self) -> Iterator[List[Job]]:
        """
        A generator which yields pages of Jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/jobs.html#pages)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultjobs)
        """

    def __iter__(self) -> Iterator[Job]:
        """
        A generator which yields Jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/jobs.html#__iter__)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultjobs)
        """

class VaultJobsInProgressCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/jobs_in_progress.html#Glacier.Vault.jobs_in_progress)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultjobs_in_progress)
    """
    def all(self) -> VaultJobsInProgressCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/jobs_in_progress.html#Glacier.Vault.all)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultjobs_in_progress)
        """

    def filter(  # type: ignore[override]
        self, *, limit: str = ..., marker: str = ..., statuscode: str = ..., completed: str = ...
    ) -> VaultJobsInProgressCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/jobs_in_progress.html#filter)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultjobs_in_progress)
        """

    def limit(self, count: int) -> VaultJobsInProgressCollection:
        """
        Return at most this many Jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/jobs_in_progress.html#limit)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultjobs_in_progress)
        """

    def page_size(self, count: int) -> VaultJobsInProgressCollection:
        """
        Fetch at most this many Jobs per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/jobs_in_progress.html#page_size)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultjobs_in_progress)
        """

    def pages(self) -> Iterator[List[Job]]:
        """
        A generator which yields pages of Jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/jobs_in_progress.html#pages)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultjobs_in_progress)
        """

    def __iter__(self) -> Iterator[Job]:
        """
        A generator which yields Jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/jobs_in_progress.html#__iter__)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultjobs_in_progress)
        """

class VaultMultipartUplaodsCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/multipart_uplaods.html#Glacier.Vault.multipart_uplaods)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultmultipart_uplaods)
    """
    def all(self) -> VaultMultipartUplaodsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/multipart_uplaods.html#Glacier.Vault.all)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultmultipart_uplaods)
        """

    def filter(  # type: ignore[override]
        self, *, marker: str = ..., limit: str = ...
    ) -> VaultMultipartUplaodsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/multipart_uplaods.html#filter)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultmultipart_uplaods)
        """

    def limit(self, count: int) -> VaultMultipartUplaodsCollection:
        """
        Return at most this many MultipartUploads.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/multipart_uplaods.html#limit)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultmultipart_uplaods)
        """

    def page_size(self, count: int) -> VaultMultipartUplaodsCollection:
        """
        Fetch at most this many MultipartUploads per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/multipart_uplaods.html#page_size)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultmultipart_uplaods)
        """

    def pages(self) -> Iterator[List[MultipartUpload]]:
        """
        A generator which yields pages of MultipartUploads.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/multipart_uplaods.html#pages)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultmultipart_uplaods)
        """

    def __iter__(self) -> Iterator[MultipartUpload]:
        """
        A generator which yields MultipartUploads.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/multipart_uplaods.html#__iter__)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultmultipart_uplaods)
        """

class VaultMultipartUploadsCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/multipart_uploads.html#Glacier.Vault.multipart_uploads)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultmultipart_uploads)
    """
    def all(self) -> VaultMultipartUploadsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/multipart_uploads.html#Glacier.Vault.all)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultmultipart_uploads)
        """

    def filter(  # type: ignore[override]
        self, *, marker: str = ..., limit: str = ...
    ) -> VaultMultipartUploadsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/multipart_uploads.html#filter)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultmultipart_uploads)
        """

    def limit(self, count: int) -> VaultMultipartUploadsCollection:
        """
        Return at most this many MultipartUploads.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/multipart_uploads.html#limit)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultmultipart_uploads)
        """

    def page_size(self, count: int) -> VaultMultipartUploadsCollection:
        """
        Fetch at most this many MultipartUploads per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/multipart_uploads.html#page_size)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultmultipart_uploads)
        """

    def pages(self) -> Iterator[List[MultipartUpload]]:
        """
        A generator which yields pages of MultipartUploads.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/multipart_uploads.html#pages)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultmultipart_uploads)
        """

    def __iter__(self) -> Iterator[MultipartUpload]:
        """
        A generator which yields MultipartUploads.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/multipart_uploads.html#__iter__)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultmultipart_uploads)
        """

class VaultSucceededJobsCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/succeeded_jobs.html#Glacier.Vault.succeeded_jobs)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultsucceeded_jobs)
    """
    def all(self) -> VaultSucceededJobsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/succeeded_jobs.html#Glacier.Vault.all)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultsucceeded_jobs)
        """

    def filter(  # type: ignore[override]
        self, *, limit: str = ..., marker: str = ..., statuscode: str = ..., completed: str = ...
    ) -> VaultSucceededJobsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/succeeded_jobs.html#filter)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultsucceeded_jobs)
        """

    def limit(self, count: int) -> VaultSucceededJobsCollection:
        """
        Return at most this many Jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/succeeded_jobs.html#limit)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultsucceeded_jobs)
        """

    def page_size(self, count: int) -> VaultSucceededJobsCollection:
        """
        Fetch at most this many Jobs per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/succeeded_jobs.html#page_size)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultsucceeded_jobs)
        """

    def pages(self) -> Iterator[List[Job]]:
        """
        A generator which yields pages of Jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/succeeded_jobs.html#pages)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultsucceeded_jobs)
        """

    def __iter__(self) -> Iterator[Job]:
        """
        A generator which yields Jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/succeeded_jobs.html#__iter__)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultsucceeded_jobs)
        """

class Account(ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/account/index.html#Glacier.Account)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#account)
    """

    id: str
    vaults: AccountVaultsCollection
    meta: GlacierResourceMeta  # type: ignore[override]

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/account/get_available_subresources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#accountget_available_subresources-method)
        """

    def create_vault(self, **kwargs: Unpack[CreateVaultInputAccountCreateVaultTypeDef]) -> _Vault:
        """
        This operation creates a new vault with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/account/create_vault.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#accountcreate_vault-method)
        """

    def Vault(self, name: str) -> _Vault:
        """
        Creates a Vault resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/account/Vault.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#accountvault-method)
        """

_Account = Account

class Archive(ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/archive/index.html#Glacier.Archive)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#archive)
    """

    account_id: str
    vault_name: str
    id: str
    meta: GlacierResourceMeta  # type: ignore[override]

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/archive/get_available_subresources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#archiveget_available_subresources-method)
        """

    def delete(self) -> None:
        """
        This operation deletes an archive from a vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/archive/delete.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#archivedelete-method)
        """

    def initiate_archive_retrieval(self) -> _Job:
        """
        This operation initiates a job of the specified type, which can be a select, an
        archival retrieval, or a vault retrieval.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/archive/initiate_archive_retrieval.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#archiveinitiate_archive_retrieval-method)
        """

    def Vault(self) -> _Vault:
        """
        Creates a Vault resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/archive/Vault.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#archivevault-method)
        """

_Archive = Archive

class Job(ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/job/index.html#Glacier.Job)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#job)
    """

    account_id: str
    vault_name: str
    id: str
    job_id: str
    job_description: str
    action: ActionCodeType
    archive_id: str
    vault_arn: str
    creation_date: str
    completed: bool
    status_code: StatusCodeType
    status_message: str
    archive_size_in_bytes: int
    inventory_size_in_bytes: int
    sns_topic: str
    completion_date: str
    sha256_tree_hash: str
    archive_sha256_tree_hash: str
    retrieval_byte_range: str
    tier: str
    inventory_retrieval_parameters: InventoryRetrievalJobDescriptionTypeDef
    job_output_path: str
    select_parameters: SelectParametersTypeDef
    output_location: OutputLocationOutputTypeDef
    meta: GlacierResourceMeta  # type: ignore[override]

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/job/get_available_subresources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#jobget_available_subresources-method)
        """

    def get_output(
        self, **kwargs: Unpack[GetJobOutputInputJobGetOutputTypeDef]
    ) -> GetJobOutputOutputTypeDef:
        """
        This operation downloads the output of the job you initiated using
        <a>InitiateJob</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/job/get_output.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#jobget_output-method)
        """

    def Vault(self) -> _Vault:
        """
        Creates a Vault resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/job/Vault.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#jobvault-method)
        """

    def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/job/load.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#jobload-method)
        """

    def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/job/reload.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#jobreload-method)
        """

_Job = Job

class MultipartUpload(ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/multipartupload/index.html#Glacier.MultipartUpload)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#multipartupload)
    """

    account_id: str
    vault_name: str
    id: str
    multipart_upload_id: str
    vault_arn: str
    archive_description: str
    part_size_in_bytes: int
    creation_date: str
    meta: GlacierResourceMeta  # type: ignore[override]

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this MultipartUpload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/multipartupload/get_available_subresources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#multipartuploadget_available_subresources-method)
        """

    def abort(self) -> None:
        """
        This operation aborts a multipart upload identified by the upload ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/multipartupload/abort.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#multipartuploadabort-method)
        """

    def complete(
        self, **kwargs: Unpack[CompleteMultipartUploadInputMultipartUploadCompleteTypeDef]
    ) -> ArchiveCreationOutputTypeDef:
        """
        You call this operation to inform Amazon S3 Glacier (Glacier) that all the
        archive parts have been uploaded and that Glacier can now assemble the archive
        from the uploaded parts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/multipartupload/complete.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#multipartuploadcomplete-method)
        """

    def parts(
        self, **kwargs: Unpack[ListPartsInputMultipartUploadPartsTypeDef]
    ) -> ListPartsOutputTypeDef:
        """
        This operation lists the parts of an archive that have been uploaded in a
        specific multipart upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/multipartupload/parts.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#multipartuploadparts-method)
        """

    def upload_part(
        self, **kwargs: Unpack[UploadMultipartPartInputMultipartUploadUploadPartTypeDef]
    ) -> UploadMultipartPartOutputTypeDef:
        """
        This operation uploads a part of an archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/multipartupload/upload_part.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#multipartuploadupload_part-method)
        """

    def Vault(self) -> _Vault:
        """
        Creates a Vault resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/multipartupload/Vault.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#multipartuploadvault-method)
        """

_MultipartUpload = MultipartUpload

class Notification(ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/notification/index.html#Glacier.Notification)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#notification)
    """

    account_id: str
    vault_name: str
    sns_topic: str
    events: List[str]
    meta: GlacierResourceMeta  # type: ignore[override]

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Notification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/notification/get_available_subresources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#notificationget_available_subresources-method)
        """

    def delete(self) -> None:
        """
        This operation deletes the notification configuration set for a vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/notification/delete.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#notificationdelete-method)
        """

    def set(self, **kwargs: Unpack[SetVaultNotificationsInputNotificationSetTypeDef]) -> None:
        """
        This operation configures notifications that will be sent when specific events
        happen to a vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/notification/set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#notificationset-method)
        """

    def Vault(self) -> _Vault:
        """
        Creates a Vault resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/notification/Vault.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#notificationvault-method)
        """

    def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/notification/load.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#notificationload-method)
        """

    def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/notification/reload.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#notificationreload-method)
        """

_Notification = Notification

class Vault(ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/index.html#Glacier.Vault)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vault)
    """

    account_id: str
    name: str
    completed_jobs: VaultCompletedJobsCollection
    failed_jobs: VaultFailedJobsCollection
    jobs: VaultJobsCollection
    jobs_in_progress: VaultJobsInProgressCollection
    multipart_uplaods: VaultMultipartUplaodsCollection
    multipart_uploads: VaultMultipartUploadsCollection
    succeeded_jobs: VaultSucceededJobsCollection
    vault_arn: str
    vault_name: str
    creation_date: str
    last_inventory_date: str
    number_of_archives: int
    size_in_bytes: int
    meta: GlacierResourceMeta  # type: ignore[override]

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/get_available_subresources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultget_available_subresources-method)
        """

    def create(self) -> CreateVaultOutputTypeDef:
        """
        This operation creates a new vault with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/create.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultcreate-method)
        """

    def delete(self) -> None:
        """
        This operation deletes a vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/delete.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultdelete-method)
        """

    def initiate_inventory_retrieval(self) -> _Job:
        """
        This operation initiates a job of the specified type, which can be a select, an
        archival retrieval, or a vault retrieval.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/initiate_inventory_retrieval.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultinitiate_inventory_retrieval-method)
        """

    def initiate_multipart_upload(
        self, **kwargs: Unpack[InitiateMultipartUploadInputVaultInitiateMultipartUploadTypeDef]
    ) -> _MultipartUpload:
        """
        This operation initiates a multipart upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/initiate_multipart_upload.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultinitiate_multipart_upload-method)
        """

    def upload_archive(
        self, **kwargs: Unpack[UploadArchiveInputVaultUploadArchiveTypeDef]
    ) -> _Archive:
        """
        This operation adds an archive to a vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/upload_archive.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultupload_archive-method)
        """

    def Account(self) -> _Account:
        """
        Creates a Account resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/Account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultaccount-method)
        """

    def Archive(self, id: str) -> _Archive:
        """
        Creates a Archive resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/Archive.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultarchive-method)
        """

    def Job(self, id: str) -> _Job:
        """
        Creates a Job resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/Job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultjob-method)
        """

    def MultipartUpload(self, id: str) -> _MultipartUpload:
        """
        Creates a MultipartUpload resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/MultipartUpload.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultmultipartupload-method)
        """

    def Notification(self) -> _Notification:
        """
        Creates a Notification resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/Notification.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultnotification-method)
        """

    def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/load.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultload-method)
        """

    def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/vault/reload.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#vaultreload-method)
        """

_Vault = Vault

class GlacierResourceMeta(ResourceMeta):
    client: GlacierClient  # type: ignore[override]

class GlacierServiceResource(ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/service-resource/index.html)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/)
    """

    meta: GlacierResourceMeta  # type: ignore[override]
    vaults: ServiceResourceVaultsCollection

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/service-resource/get_available_subresources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#glacierserviceresourceget_available_subresources-method)
        """

    def create_vault(
        self, **kwargs: Unpack[CreateVaultInputServiceResourceCreateVaultTypeDef]
    ) -> _Vault:
        """
        This operation creates a new vault with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/service-resource/create_vault.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#glacierserviceresourcecreate_vault-method)
        """

    def Account(self, id: str) -> _Account:
        """
        Creates a Account resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/service-resource/Account.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#glacierserviceresourceaccount-method)
        """

    def Archive(self, account_id: str, vault_name: str, id: str) -> _Archive:
        """
        Creates a Archive resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/service-resource/Archive.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#glacierserviceresourcearchive-method)
        """

    def Job(self, account_id: str, vault_name: str, id: str) -> _Job:
        """
        Creates a Job resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/service-resource/Job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#glacierserviceresourcejob-method)
        """

    def MultipartUpload(self, account_id: str, vault_name: str, id: str) -> _MultipartUpload:
        """
        Creates a MultipartUpload resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/service-resource/MultipartUpload.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#glacierserviceresourcemultipartupload-method)
        """

    def Notification(self, account_id: str, vault_name: str) -> _Notification:
        """
        Creates a Notification resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/service-resource/Notification.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#glacierserviceresourcenotification-method)
        """

    def Vault(self, account_id: str, name: str) -> _Vault:
        """
        Creates a Vault resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/service-resource/Vault.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/service_resource/#glacierserviceresourcevault-method)
        """
