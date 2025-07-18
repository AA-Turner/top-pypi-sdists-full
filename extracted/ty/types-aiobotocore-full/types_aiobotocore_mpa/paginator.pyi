"""
Type annotations for mpa service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mpa/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mpa.client import MultipartyApprovalClient
    from types_aiobotocore_mpa.paginator import (
        ListApprovalTeamsPaginator,
        ListIdentitySourcesPaginator,
        ListPoliciesPaginator,
        ListPolicyVersionsPaginator,
        ListResourcePoliciesPaginator,
        ListSessionsPaginator,
    )

    session = get_session()
    with session.create_client("mpa") as client:
        client: MultipartyApprovalClient

        list_approval_teams_paginator: ListApprovalTeamsPaginator = client.get_paginator("list_approval_teams")
        list_identity_sources_paginator: ListIdentitySourcesPaginator = client.get_paginator("list_identity_sources")
        list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
        list_policy_versions_paginator: ListPolicyVersionsPaginator = client.get_paginator("list_policy_versions")
        list_resource_policies_paginator: ListResourcePoliciesPaginator = client.get_paginator("list_resource_policies")
        list_sessions_paginator: ListSessionsPaginator = client.get_paginator("list_sessions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListApprovalTeamsRequestPaginateTypeDef,
    ListApprovalTeamsResponseTypeDef,
    ListIdentitySourcesRequestPaginateTypeDef,
    ListIdentitySourcesResponseTypeDef,
    ListPoliciesRequestPaginateTypeDef,
    ListPoliciesResponseTypeDef,
    ListPolicyVersionsRequestPaginateTypeDef,
    ListPolicyVersionsResponseTypeDef,
    ListResourcePoliciesRequestPaginateTypeDef,
    ListResourcePoliciesResponseTypeDef,
    ListSessionsRequestPaginateTypeDef,
    ListSessionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListApprovalTeamsPaginator",
    "ListIdentitySourcesPaginator",
    "ListPoliciesPaginator",
    "ListPolicyVersionsPaginator",
    "ListResourcePoliciesPaginator",
    "ListSessionsPaginator",
)

if TYPE_CHECKING:
    _ListApprovalTeamsPaginatorBase = AioPaginator[ListApprovalTeamsResponseTypeDef]
else:
    _ListApprovalTeamsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListApprovalTeamsPaginator(_ListApprovalTeamsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mpa/paginator/ListApprovalTeams.html#MultipartyApproval.Paginator.ListApprovalTeams)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mpa/paginators/#listapprovalteamspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApprovalTeamsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListApprovalTeamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mpa/paginator/ListApprovalTeams.html#MultipartyApproval.Paginator.ListApprovalTeams.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mpa/paginators/#listapprovalteamspaginator)
        """

if TYPE_CHECKING:
    _ListIdentitySourcesPaginatorBase = AioPaginator[ListIdentitySourcesResponseTypeDef]
else:
    _ListIdentitySourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListIdentitySourcesPaginator(_ListIdentitySourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mpa/paginator/ListIdentitySources.html#MultipartyApproval.Paginator.ListIdentitySources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mpa/paginators/#listidentitysourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIdentitySourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListIdentitySourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mpa/paginator/ListIdentitySources.html#MultipartyApproval.Paginator.ListIdentitySources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mpa/paginators/#listidentitysourcespaginator)
        """

if TYPE_CHECKING:
    _ListPoliciesPaginatorBase = AioPaginator[ListPoliciesResponseTypeDef]
else:
    _ListPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPoliciesPaginator(_ListPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mpa/paginator/ListPolicies.html#MultipartyApproval.Paginator.ListPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mpa/paginators/#listpoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mpa/paginator/ListPolicies.html#MultipartyApproval.Paginator.ListPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mpa/paginators/#listpoliciespaginator)
        """

if TYPE_CHECKING:
    _ListPolicyVersionsPaginatorBase = AioPaginator[ListPolicyVersionsResponseTypeDef]
else:
    _ListPolicyVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPolicyVersionsPaginator(_ListPolicyVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mpa/paginator/ListPolicyVersions.html#MultipartyApproval.Paginator.ListPolicyVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mpa/paginators/#listpolicyversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPolicyVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPolicyVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mpa/paginator/ListPolicyVersions.html#MultipartyApproval.Paginator.ListPolicyVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mpa/paginators/#listpolicyversionspaginator)
        """

if TYPE_CHECKING:
    _ListResourcePoliciesPaginatorBase = AioPaginator[ListResourcePoliciesResponseTypeDef]
else:
    _ListResourcePoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListResourcePoliciesPaginator(_ListResourcePoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mpa/paginator/ListResourcePolicies.html#MultipartyApproval.Paginator.ListResourcePolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mpa/paginators/#listresourcepoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourcePoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourcePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mpa/paginator/ListResourcePolicies.html#MultipartyApproval.Paginator.ListResourcePolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mpa/paginators/#listresourcepoliciespaginator)
        """

if TYPE_CHECKING:
    _ListSessionsPaginatorBase = AioPaginator[ListSessionsResponseTypeDef]
else:
    _ListSessionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSessionsPaginator(_ListSessionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mpa/paginator/ListSessions.html#MultipartyApproval.Paginator.ListSessions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mpa/paginators/#listsessionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSessionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mpa/paginator/ListSessions.html#MultipartyApproval.Paginator.ListSessions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mpa/paginators/#listsessionspaginator)
        """
