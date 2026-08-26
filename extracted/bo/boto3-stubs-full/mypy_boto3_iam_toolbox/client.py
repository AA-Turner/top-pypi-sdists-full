"""
Type annotations for iam-toolbox service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam_toolbox/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_iam_toolbox.client import IAMToolboxPreviewClient

    session = Session()
    client: IAMToolboxPreviewClient = session.client("iam-toolbox")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import GetRequestAuthorizationDetailsPaginator
from .type_defs import (
    GetRequestAuthorizationDetailsInputTypeDef,
    GetRequestAuthorizationDetailsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("IAMToolboxPreviewClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class IAMToolboxPreviewClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam-toolbox.html#IAMToolboxPreview.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam_toolbox/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IAMToolboxPreviewClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam-toolbox.html#IAMToolboxPreview.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam_toolbox/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam-toolbox/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam_toolbox/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam-toolbox/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam_toolbox/client/#generate_presigned_url)
        """

    def get_request_authorization_details(
        self, **kwargs: Unpack[GetRequestAuthorizationDetailsInputTypeDef]
    ) -> GetRequestAuthorizationDetailsOutputTypeDef:
        """
        Retrieves the authorization details for a specific access denied request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam-toolbox/client/get_request_authorization_details.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam_toolbox/client/#get_request_authorization_details)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_request_authorization_details"]
    ) -> GetRequestAuthorizationDetailsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam-toolbox/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam_toolbox/client/#get_paginator)
        """
