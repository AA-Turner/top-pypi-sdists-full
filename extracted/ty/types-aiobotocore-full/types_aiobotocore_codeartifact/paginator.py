"""
Type annotations for codeartifact service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_codeartifact.client import CodeArtifactClient
    from types_aiobotocore_codeartifact.paginator import (
        ListAllowedRepositoriesForGroupPaginator,
        ListAssociatedPackagesPaginator,
        ListDomainsPaginator,
        ListPackageGroupsPaginator,
        ListPackageVersionAssetsPaginator,
        ListPackageVersionsPaginator,
        ListPackagesPaginator,
        ListRepositoriesInDomainPaginator,
        ListRepositoriesPaginator,
        ListSubPackageGroupsPaginator,
    )

    session = get_session()
    with session.create_client("codeartifact") as client:
        client: CodeArtifactClient

        list_allowed_repositories_for_group_paginator: ListAllowedRepositoriesForGroupPaginator = client.get_paginator("list_allowed_repositories_for_group")
        list_associated_packages_paginator: ListAssociatedPackagesPaginator = client.get_paginator("list_associated_packages")
        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        list_package_groups_paginator: ListPackageGroupsPaginator = client.get_paginator("list_package_groups")
        list_package_version_assets_paginator: ListPackageVersionAssetsPaginator = client.get_paginator("list_package_version_assets")
        list_package_versions_paginator: ListPackageVersionsPaginator = client.get_paginator("list_package_versions")
        list_packages_paginator: ListPackagesPaginator = client.get_paginator("list_packages")
        list_repositories_in_domain_paginator: ListRepositoriesInDomainPaginator = client.get_paginator("list_repositories_in_domain")
        list_repositories_paginator: ListRepositoriesPaginator = client.get_paginator("list_repositories")
        list_sub_package_groups_paginator: ListSubPackageGroupsPaginator = client.get_paginator("list_sub_package_groups")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAllowedRepositoriesForGroupRequestPaginateTypeDef,
    ListAllowedRepositoriesForGroupResultTypeDef,
    ListAssociatedPackagesRequestPaginateTypeDef,
    ListAssociatedPackagesResultTypeDef,
    ListDomainsRequestPaginateTypeDef,
    ListDomainsResultTypeDef,
    ListPackageGroupsRequestPaginateTypeDef,
    ListPackageGroupsResultTypeDef,
    ListPackagesRequestPaginateTypeDef,
    ListPackagesResultTypeDef,
    ListPackageVersionAssetsRequestPaginateTypeDef,
    ListPackageVersionAssetsResultTypeDef,
    ListPackageVersionsRequestPaginateTypeDef,
    ListPackageVersionsResultTypeDef,
    ListRepositoriesInDomainRequestPaginateTypeDef,
    ListRepositoriesInDomainResultTypeDef,
    ListRepositoriesRequestPaginateTypeDef,
    ListRepositoriesResultTypeDef,
    ListSubPackageGroupsRequestPaginateTypeDef,
    ListSubPackageGroupsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAllowedRepositoriesForGroupPaginator",
    "ListAssociatedPackagesPaginator",
    "ListDomainsPaginator",
    "ListPackageGroupsPaginator",
    "ListPackageVersionAssetsPaginator",
    "ListPackageVersionsPaginator",
    "ListPackagesPaginator",
    "ListRepositoriesInDomainPaginator",
    "ListRepositoriesPaginator",
    "ListSubPackageGroupsPaginator",
)


if TYPE_CHECKING:
    _ListAllowedRepositoriesForGroupPaginatorBase = AioPaginator[
        ListAllowedRepositoriesForGroupResultTypeDef
    ]
else:
    _ListAllowedRepositoriesForGroupPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAllowedRepositoriesForGroupPaginator(_ListAllowedRepositoriesForGroupPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListAllowedRepositoriesForGroup.html#CodeArtifact.Paginator.ListAllowedRepositoriesForGroup)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listallowedrepositoriesforgrouppaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAllowedRepositoriesForGroupRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAllowedRepositoriesForGroupResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListAllowedRepositoriesForGroup.html#CodeArtifact.Paginator.ListAllowedRepositoriesForGroup.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listallowedrepositoriesforgrouppaginator)
        """


if TYPE_CHECKING:
    _ListAssociatedPackagesPaginatorBase = AioPaginator[ListAssociatedPackagesResultTypeDef]
else:
    _ListAssociatedPackagesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAssociatedPackagesPaginator(_ListAssociatedPackagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListAssociatedPackages.html#CodeArtifact.Paginator.ListAssociatedPackages)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listassociatedpackagespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssociatedPackagesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAssociatedPackagesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListAssociatedPackages.html#CodeArtifact.Paginator.ListAssociatedPackages.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listassociatedpackagespaginator)
        """


if TYPE_CHECKING:
    _ListDomainsPaginatorBase = AioPaginator[ListDomainsResultTypeDef]
else:
    _ListDomainsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDomainsPaginator(_ListDomainsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListDomains.html#CodeArtifact.Paginator.ListDomains)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listdomainspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDomainsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDomainsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListDomains.html#CodeArtifact.Paginator.ListDomains.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listdomainspaginator)
        """


if TYPE_CHECKING:
    _ListPackageGroupsPaginatorBase = AioPaginator[ListPackageGroupsResultTypeDef]
else:
    _ListPackageGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPackageGroupsPaginator(_ListPackageGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListPackageGroups.html#CodeArtifact.Paginator.ListPackageGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listpackagegroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPackageGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPackageGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListPackageGroups.html#CodeArtifact.Paginator.ListPackageGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listpackagegroupspaginator)
        """


if TYPE_CHECKING:
    _ListPackageVersionAssetsPaginatorBase = AioPaginator[ListPackageVersionAssetsResultTypeDef]
else:
    _ListPackageVersionAssetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPackageVersionAssetsPaginator(_ListPackageVersionAssetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListPackageVersionAssets.html#CodeArtifact.Paginator.ListPackageVersionAssets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listpackageversionassetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPackageVersionAssetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPackageVersionAssetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListPackageVersionAssets.html#CodeArtifact.Paginator.ListPackageVersionAssets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listpackageversionassetspaginator)
        """


if TYPE_CHECKING:
    _ListPackageVersionsPaginatorBase = AioPaginator[ListPackageVersionsResultTypeDef]
else:
    _ListPackageVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPackageVersionsPaginator(_ListPackageVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListPackageVersions.html#CodeArtifact.Paginator.ListPackageVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listpackageversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPackageVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPackageVersionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListPackageVersions.html#CodeArtifact.Paginator.ListPackageVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listpackageversionspaginator)
        """


if TYPE_CHECKING:
    _ListPackagesPaginatorBase = AioPaginator[ListPackagesResultTypeDef]
else:
    _ListPackagesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPackagesPaginator(_ListPackagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListPackages.html#CodeArtifact.Paginator.ListPackages)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listpackagespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPackagesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPackagesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListPackages.html#CodeArtifact.Paginator.ListPackages.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listpackagespaginator)
        """


if TYPE_CHECKING:
    _ListRepositoriesInDomainPaginatorBase = AioPaginator[ListRepositoriesInDomainResultTypeDef]
else:
    _ListRepositoriesInDomainPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRepositoriesInDomainPaginator(_ListRepositoriesInDomainPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListRepositoriesInDomain.html#CodeArtifact.Paginator.ListRepositoriesInDomain)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listrepositoriesindomainpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRepositoriesInDomainRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRepositoriesInDomainResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListRepositoriesInDomain.html#CodeArtifact.Paginator.ListRepositoriesInDomain.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listrepositoriesindomainpaginator)
        """


if TYPE_CHECKING:
    _ListRepositoriesPaginatorBase = AioPaginator[ListRepositoriesResultTypeDef]
else:
    _ListRepositoriesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRepositoriesPaginator(_ListRepositoriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListRepositories.html#CodeArtifact.Paginator.ListRepositories)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listrepositoriespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRepositoriesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRepositoriesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListRepositories.html#CodeArtifact.Paginator.ListRepositories.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listrepositoriespaginator)
        """


if TYPE_CHECKING:
    _ListSubPackageGroupsPaginatorBase = AioPaginator[ListSubPackageGroupsResultTypeDef]
else:
    _ListSubPackageGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSubPackageGroupsPaginator(_ListSubPackageGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListSubPackageGroups.html#CodeArtifact.Paginator.ListSubPackageGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listsubpackagegroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSubPackageGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSubPackageGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/paginator/ListSubPackageGroups.html#CodeArtifact.Paginator.ListSubPackageGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeartifact/paginators/#listsubpackagegroupspaginator)
        """
