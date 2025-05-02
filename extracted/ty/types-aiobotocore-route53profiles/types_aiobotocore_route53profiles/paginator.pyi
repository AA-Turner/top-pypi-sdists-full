"""
Type annotations for route53profiles service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_route53profiles.client import Route53ProfilesClient
    from types_aiobotocore_route53profiles.paginator import (
        ListProfileAssociationsPaginator,
        ListProfileResourceAssociationsPaginator,
        ListProfilesPaginator,
    )

    session = get_session()
    with session.create_client("route53profiles") as client:
        client: Route53ProfilesClient

        list_profile_associations_paginator: ListProfileAssociationsPaginator = client.get_paginator("list_profile_associations")
        list_profile_resource_associations_paginator: ListProfileResourceAssociationsPaginator = client.get_paginator("list_profile_resource_associations")
        list_profiles_paginator: ListProfilesPaginator = client.get_paginator("list_profiles")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListProfileAssociationsRequestPaginateTypeDef,
    ListProfileAssociationsResponseTypeDef,
    ListProfileResourceAssociationsRequestPaginateTypeDef,
    ListProfileResourceAssociationsResponseTypeDef,
    ListProfilesRequestPaginateTypeDef,
    ListProfilesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListProfileAssociationsPaginator",
    "ListProfileResourceAssociationsPaginator",
    "ListProfilesPaginator",
)

if TYPE_CHECKING:
    _ListProfileAssociationsPaginatorBase = AioPaginator[ListProfileAssociationsResponseTypeDef]
else:
    _ListProfileAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListProfileAssociationsPaginator(_ListProfileAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/paginator/ListProfileAssociations.html#Route53Profiles.Paginator.ListProfileAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/paginators/#listprofileassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProfileAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProfileAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/paginator/ListProfileAssociations.html#Route53Profiles.Paginator.ListProfileAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/paginators/#listprofileassociationspaginator)
        """

if TYPE_CHECKING:
    _ListProfileResourceAssociationsPaginatorBase = AioPaginator[
        ListProfileResourceAssociationsResponseTypeDef
    ]
else:
    _ListProfileResourceAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListProfileResourceAssociationsPaginator(_ListProfileResourceAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/paginator/ListProfileResourceAssociations.html#Route53Profiles.Paginator.ListProfileResourceAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/paginators/#listprofileresourceassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProfileResourceAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProfileResourceAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/paginator/ListProfileResourceAssociations.html#Route53Profiles.Paginator.ListProfileResourceAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/paginators/#listprofileresourceassociationspaginator)
        """

if TYPE_CHECKING:
    _ListProfilesPaginatorBase = AioPaginator[ListProfilesResponseTypeDef]
else:
    _ListProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListProfilesPaginator(_ListProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/paginator/ListProfiles.html#Route53Profiles.Paginator.ListProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/paginators/#listprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles/paginator/ListProfiles.html#Route53Profiles.Paginator.ListProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/paginators/#listprofilespaginator)
        """
