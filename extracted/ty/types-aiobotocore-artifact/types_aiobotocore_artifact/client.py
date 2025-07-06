"""
Type annotations for artifact service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_artifact.client import ArtifactClient

    session = get_session()
    async with session.create_client("artifact") as client:
        client: ArtifactClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListCustomerAgreementsPaginator, ListReportsPaginator
from .type_defs import (
    GetAccountSettingsResponseTypeDef,
    GetReportMetadataRequestTypeDef,
    GetReportMetadataResponseTypeDef,
    GetReportRequestTypeDef,
    GetReportResponseTypeDef,
    GetTermForReportRequestTypeDef,
    GetTermForReportResponseTypeDef,
    ListCustomerAgreementsRequestTypeDef,
    ListCustomerAgreementsResponseTypeDef,
    ListReportsRequestTypeDef,
    ListReportsResponseTypeDef,
    PutAccountSettingsRequestTypeDef,
    PutAccountSettingsResponseTypeDef,
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


__all__ = ("ArtifactClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ArtifactClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact.html#Artifact.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ArtifactClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact.html#Artifact.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#generate_presigned_url)
        """

    async def get_account_settings(self) -> GetAccountSettingsResponseTypeDef:
        """
        Get the account settings for Artifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/get_account_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#get_account_settings)
        """

    async def get_report(
        self, **kwargs: Unpack[GetReportRequestTypeDef]
    ) -> GetReportResponseTypeDef:
        """
        Get the content for a single report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/get_report.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#get_report)
        """

    async def get_report_metadata(
        self, **kwargs: Unpack[GetReportMetadataRequestTypeDef]
    ) -> GetReportMetadataResponseTypeDef:
        """
        Get the metadata for a single report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/get_report_metadata.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#get_report_metadata)
        """

    async def get_term_for_report(
        self, **kwargs: Unpack[GetTermForReportRequestTypeDef]
    ) -> GetTermForReportResponseTypeDef:
        """
        Get the Term content associated with a single report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/get_term_for_report.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#get_term_for_report)
        """

    async def list_customer_agreements(
        self, **kwargs: Unpack[ListCustomerAgreementsRequestTypeDef]
    ) -> ListCustomerAgreementsResponseTypeDef:
        """
        List active customer-agreements applicable to calling identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/list_customer_agreements.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#list_customer_agreements)
        """

    async def list_reports(
        self, **kwargs: Unpack[ListReportsRequestTypeDef]
    ) -> ListReportsResponseTypeDef:
        """
        List available reports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/list_reports.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#list_reports)
        """

    async def put_account_settings(
        self, **kwargs: Unpack[PutAccountSettingsRequestTypeDef]
    ) -> PutAccountSettingsResponseTypeDef:
        """
        Put the account settings for Artifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/put_account_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#put_account_settings)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_customer_agreements"]
    ) -> ListCustomerAgreementsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_reports"]
    ) -> ListReportsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact.html#Artifact.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact.html#Artifact.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/client/)
        """
