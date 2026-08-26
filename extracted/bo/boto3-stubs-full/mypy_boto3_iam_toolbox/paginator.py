"""
Type annotations for iam-toolbox service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam_toolbox/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_iam_toolbox.client import IAMToolboxPreviewClient
    from mypy_boto3_iam_toolbox.paginator import (
        GetRequestAuthorizationDetailsPaginator,
    )

    session = Session()
    client: IAMToolboxPreviewClient = session.client("iam-toolbox")

    get_request_authorization_details_paginator: GetRequestAuthorizationDetailsPaginator = client.get_paginator("get_request_authorization_details")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

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
    _GetRequestAuthorizationDetailsPaginatorBase = Paginator[
        GetRequestAuthorizationDetailsOutputTypeDef
    ]
else:
    _GetRequestAuthorizationDetailsPaginatorBase = Paginator  # type: ignore[assignment]


class GetRequestAuthorizationDetailsPaginator(_GetRequestAuthorizationDetailsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam-toolbox/paginator/GetRequestAuthorizationDetails.html#IAMToolboxPreview.Paginator.GetRequestAuthorizationDetails)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam_toolbox/paginators/#getrequestauthorizationdetailspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetRequestAuthorizationDetailsInputPaginateTypeDef]
    ) -> PageIterator[GetRequestAuthorizationDetailsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam-toolbox/paginator/GetRequestAuthorizationDetails.html#IAMToolboxPreview.Paginator.GetRequestAuthorizationDetails.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iam_toolbox/paginators/#getrequestauthorizationdetailspaginator)
        """
