"""
Type annotations for rolesanywhere service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_rolesanywhere.client import IAMRolesAnywhereClient
    from types_aiobotocore_rolesanywhere.paginator import (
        ListCrlsPaginator,
        ListProfilesPaginator,
        ListSubjectsPaginator,
        ListTrustAnchorsPaginator,
    )

    session = get_session()
    with session.create_client("rolesanywhere") as client:
        client: IAMRolesAnywhereClient

        list_crls_paginator: ListCrlsPaginator = client.get_paginator("list_crls")
        list_profiles_paginator: ListProfilesPaginator = client.get_paginator("list_profiles")
        list_subjects_paginator: ListSubjectsPaginator = client.get_paginator("list_subjects")
        list_trust_anchors_paginator: ListTrustAnchorsPaginator = client.get_paginator("list_trust_anchors")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListCrlsResponseTypeDef,
    ListProfilesResponseTypeDef,
    ListRequestPaginateExtraExtraExtraTypeDef,
    ListRequestPaginateExtraExtraTypeDef,
    ListRequestPaginateExtraTypeDef,
    ListRequestPaginateTypeDef,
    ListSubjectsResponseTypeDef,
    ListTrustAnchorsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListCrlsPaginator",
    "ListProfilesPaginator",
    "ListSubjectsPaginator",
    "ListTrustAnchorsPaginator",
)


if TYPE_CHECKING:
    _ListCrlsPaginatorBase = AioPaginator[ListCrlsResponseTypeDef]
else:
    _ListCrlsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCrlsPaginator(_ListCrlsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/paginator/ListCrls.html#IAMRolesAnywhere.Paginator.ListCrls)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/paginators/#listcrlspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCrlsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/paginator/ListCrls.html#IAMRolesAnywhere.Paginator.ListCrls.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/paginators/#listcrlspaginator)
        """


if TYPE_CHECKING:
    _ListProfilesPaginatorBase = AioPaginator[ListProfilesResponseTypeDef]
else:
    _ListProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListProfilesPaginator(_ListProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/paginator/ListProfiles.html#IAMRolesAnywhere.Paginator.ListProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/paginators/#listprofilespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRequestPaginateExtraTypeDef]
    ) -> AioPageIterator[ListProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/paginator/ListProfiles.html#IAMRolesAnywhere.Paginator.ListProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/paginators/#listprofilespaginator)
        """


if TYPE_CHECKING:
    _ListSubjectsPaginatorBase = AioPaginator[ListSubjectsResponseTypeDef]
else:
    _ListSubjectsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSubjectsPaginator(_ListSubjectsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/paginator/ListSubjects.html#IAMRolesAnywhere.Paginator.ListSubjects)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/paginators/#listsubjectspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRequestPaginateExtraExtraTypeDef]
    ) -> AioPageIterator[ListSubjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/paginator/ListSubjects.html#IAMRolesAnywhere.Paginator.ListSubjects.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/paginators/#listsubjectspaginator)
        """


if TYPE_CHECKING:
    _ListTrustAnchorsPaginatorBase = AioPaginator[ListTrustAnchorsResponseTypeDef]
else:
    _ListTrustAnchorsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTrustAnchorsPaginator(_ListTrustAnchorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/paginator/ListTrustAnchors.html#IAMRolesAnywhere.Paginator.ListTrustAnchors)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/paginators/#listtrustanchorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRequestPaginateExtraExtraExtraTypeDef]
    ) -> AioPageIterator[ListTrustAnchorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/paginator/ListTrustAnchors.html#IAMRolesAnywhere.Paginator.ListTrustAnchors.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/paginators/#listtrustanchorspaginator)
        """
