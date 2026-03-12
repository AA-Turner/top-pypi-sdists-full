"""
Type annotations for simpledbv2 service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_simpledbv2/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_simpledbv2.client import SimpleDBv2Client

    session = Session()
    client: SimpleDBv2Client = session.client("simpledbv2")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListExportsPaginator
from .type_defs import (
    GetExportRequestTypeDef,
    GetExportResponseTypeDef,
    ListExportsRequestTypeDef,
    ListExportsResponseTypeDef,
    StartDomainExportRequestTypeDef,
    StartDomainExportResponseTypeDef,
)
from .waiter import ExportSucceededWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("SimpleDBv2Client",)

class Exceptions(BaseClientExceptions):
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InvalidNextTokenException: type[BotocoreClientError]
    InvalidParameterCombinationException: type[BotocoreClientError]
    InvalidParameterValueException: type[BotocoreClientError]
    NoSuchDomainException: type[BotocoreClientError]
    NoSuchExportException: type[BotocoreClientError]
    NumberExportsLimitExceeded: type[BotocoreClientError]

class SimpleDBv2Client(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simpledbv2.html#SimpleDBv2.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_simpledbv2/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SimpleDBv2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simpledbv2.html#SimpleDBv2.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_simpledbv2/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simpledbv2/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_simpledbv2/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simpledbv2/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_simpledbv2/client/#generate_presigned_url)
        """

    def get_export(self, **kwargs: Unpack[GetExportRequestTypeDef]) -> GetExportResponseTypeDef:
        """
        Returns information for an existing domain export.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simpledbv2/client/get_export.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_simpledbv2/client/#get_export)
        """

    def list_exports(
        self, **kwargs: Unpack[ListExportsRequestTypeDef]
    ) -> ListExportsResponseTypeDef:
        """
        Lists all exports that were created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simpledbv2/client/list_exports.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_simpledbv2/client/#list_exports)
        """

    def start_domain_export(
        self, **kwargs: Unpack[StartDomainExportRequestTypeDef]
    ) -> StartDomainExportResponseTypeDef:
        """
        Initiates the export of a SimpleDB domain to an S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simpledbv2/client/start_domain_export.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_simpledbv2/client/#start_domain_export)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_exports"]
    ) -> ListExportsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simpledbv2/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_simpledbv2/client/#get_paginator)
        """

    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["export_succeeded"]
    ) -> ExportSucceededWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simpledbv2/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_simpledbv2/client/#get_waiter)
        """
