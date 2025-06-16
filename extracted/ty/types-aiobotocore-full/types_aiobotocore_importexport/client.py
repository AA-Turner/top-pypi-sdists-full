"""
Type annotations for importexport service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_importexport.client import ImportExportClient

    session = get_session()
    async with session.create_client("importexport") as client:
        client: ImportExportClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListJobsPaginator
from .type_defs import (
    CancelJobInputTypeDef,
    CancelJobOutputTypeDef,
    CreateJobInputTypeDef,
    CreateJobOutputTypeDef,
    GetShippingLabelInputTypeDef,
    GetShippingLabelOutputTypeDef,
    GetStatusInputTypeDef,
    GetStatusOutputTypeDef,
    ListJobsInputTypeDef,
    ListJobsOutputTypeDef,
    UpdateJobInputTypeDef,
    UpdateJobOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("ImportExportClient",)


class Exceptions(BaseClientExceptions):
    BucketPermissionException: Type[BotocoreClientError]
    CanceledJobIdException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    CreateJobQuotaExceededException: Type[BotocoreClientError]
    ExpiredJobIdException: Type[BotocoreClientError]
    InvalidAccessKeyIdException: Type[BotocoreClientError]
    InvalidAddressException: Type[BotocoreClientError]
    InvalidCustomsException: Type[BotocoreClientError]
    InvalidFileSystemException: Type[BotocoreClientError]
    InvalidJobIdException: Type[BotocoreClientError]
    InvalidManifestFieldException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidVersionException: Type[BotocoreClientError]
    MalformedManifestException: Type[BotocoreClientError]
    MissingCustomsException: Type[BotocoreClientError]
    MissingManifestFieldException: Type[BotocoreClientError]
    MissingParameterException: Type[BotocoreClientError]
    MultipleRegionsException: Type[BotocoreClientError]
    NoSuchBucketException: Type[BotocoreClientError]
    UnableToCancelJobIdException: Type[BotocoreClientError]
    UnableToUpdateJobIdException: Type[BotocoreClientError]


class ImportExportClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport.html#ImportExport.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ImportExportClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport.html#ImportExport.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/client/#generate_presigned_url)
        """

    async def cancel_job(self, **kwargs: Unpack[CancelJobInputTypeDef]) -> CancelJobOutputTypeDef:
        """
        This operation cancels a specified job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/client/cancel_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/client/#cancel_job)
        """

    async def create_job(self, **kwargs: Unpack[CreateJobInputTypeDef]) -> CreateJobOutputTypeDef:
        """
        This operation initiates the process of scheduling an upload or download of
        your data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/client/create_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/client/#create_job)
        """

    async def get_shipping_label(
        self, **kwargs: Unpack[GetShippingLabelInputTypeDef]
    ) -> GetShippingLabelOutputTypeDef:
        """
        This operation generates a pre-paid UPS shipping label that you will use to
        ship your device to AWS for processing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/client/get_shipping_label.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/client/#get_shipping_label)
        """

    async def get_status(self, **kwargs: Unpack[GetStatusInputTypeDef]) -> GetStatusOutputTypeDef:
        """
        This operation returns information about a job, including where the job is in
        the processing pipeline, the status of the results, and the signature value
        associated with the job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/client/get_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/client/#get_status)
        """

    async def list_jobs(self, **kwargs: Unpack[ListJobsInputTypeDef]) -> ListJobsOutputTypeDef:
        """
        This operation returns the jobs associated with the requester.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/client/list_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/client/#list_jobs)
        """

    async def update_job(self, **kwargs: Unpack[UpdateJobInputTypeDef]) -> UpdateJobOutputTypeDef:
        """
        You use this operation to change the parameters specified in the original
        manifest file by supplying a new manifest file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/client/update_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/client/#update_job)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_jobs"]
    ) -> ListJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport.html#ImportExport.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport.html#ImportExport.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_importexport/client/)
        """
