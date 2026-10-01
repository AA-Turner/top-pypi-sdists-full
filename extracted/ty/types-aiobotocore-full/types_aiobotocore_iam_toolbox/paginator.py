"""
Type annotations for iam-toolbox service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam_toolbox/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iam_toolbox.client import IAMToolboxPreviewClient
    from types_aiobotocore_iam_toolbox.paginator import (
        GetRequestAuthorizationDetailsPaginator,
    )

    session = get_session()
    with session.create_client("iam-toolbox") as client:
        client: IAMToolboxPreviewClient

        get_request_authorization_details_paginator: GetRequestAuthorizationDetailsPaginator = client.get_paginator("get_request_authorization_details")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetRequestAuthorizationDetailsInputPaginateTypeDef,
    GetRequestAuthorizationDetailsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("GetRequestAuthorizationDetailsPaginator",)


if TYPE_CHECKING:
    _GetRequestAuthorizationDetailsPaginatorBase = AioPaginator[
        GetRequestAuthorizationDetailsOutputTypeDef
    ]
else:
    _GetRequestAuthorizationDetailsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetRequestAuthorizationDetailsPaginator(_GetRequestAuthorizationDetailsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam-toolbox/paginator/GetRequestAuthorizationDetails.html#IAMToolboxPreview.Paginator.GetRequestAuthorizationDetails)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam_toolbox/paginators/#getrequestauthorizationdetailspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetRequestAuthorizationDetailsInputPaginateTypeDef]
    ) -> AioPageIterator[GetRequestAuthorizationDetailsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam-toolbox/paginator/GetRequestAuthorizationDetails.html#IAMToolboxPreview.Paginator.GetRequestAuthorizationDetails.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam_toolbox/paginators/#getrequestauthorizationdetailspaginator)
        """
