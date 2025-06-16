"""
Type annotations for quicksight service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_quicksight.client import QuickSightClient
    from types_aiobotocore_quicksight.paginator import (
        DescribeFolderPermissionsPaginator,
        DescribeFolderResolvedPermissionsPaginator,
        ListAnalysesPaginator,
        ListAssetBundleExportJobsPaginator,
        ListAssetBundleImportJobsPaginator,
        ListBrandsPaginator,
        ListCustomPermissionsPaginator,
        ListDashboardVersionsPaginator,
        ListDashboardsPaginator,
        ListDataSetsPaginator,
        ListDataSourcesPaginator,
        ListFolderMembersPaginator,
        ListFoldersForResourcePaginator,
        ListFoldersPaginator,
        ListGroupMembershipsPaginator,
        ListGroupsPaginator,
        ListIAMPolicyAssignmentsForUserPaginator,
        ListIAMPolicyAssignmentsPaginator,
        ListIngestionsPaginator,
        ListNamespacesPaginator,
        ListRoleMembershipsPaginator,
        ListTemplateAliasesPaginator,
        ListTemplateVersionsPaginator,
        ListTemplatesPaginator,
        ListThemeVersionsPaginator,
        ListThemesPaginator,
        ListUserGroupsPaginator,
        ListUsersPaginator,
        SearchAnalysesPaginator,
        SearchDashboardsPaginator,
        SearchDataSetsPaginator,
        SearchDataSourcesPaginator,
        SearchFoldersPaginator,
        SearchGroupsPaginator,
        SearchTopicsPaginator,
    )

    session = get_session()
    with session.create_client("quicksight") as client:
        client: QuickSightClient

        describe_folder_permissions_paginator: DescribeFolderPermissionsPaginator = client.get_paginator("describe_folder_permissions")
        describe_folder_resolved_permissions_paginator: DescribeFolderResolvedPermissionsPaginator = client.get_paginator("describe_folder_resolved_permissions")
        list_analyses_paginator: ListAnalysesPaginator = client.get_paginator("list_analyses")
        list_asset_bundle_export_jobs_paginator: ListAssetBundleExportJobsPaginator = client.get_paginator("list_asset_bundle_export_jobs")
        list_asset_bundle_import_jobs_paginator: ListAssetBundleImportJobsPaginator = client.get_paginator("list_asset_bundle_import_jobs")
        list_brands_paginator: ListBrandsPaginator = client.get_paginator("list_brands")
        list_custom_permissions_paginator: ListCustomPermissionsPaginator = client.get_paginator("list_custom_permissions")
        list_dashboard_versions_paginator: ListDashboardVersionsPaginator = client.get_paginator("list_dashboard_versions")
        list_dashboards_paginator: ListDashboardsPaginator = client.get_paginator("list_dashboards")
        list_data_sets_paginator: ListDataSetsPaginator = client.get_paginator("list_data_sets")
        list_data_sources_paginator: ListDataSourcesPaginator = client.get_paginator("list_data_sources")
        list_folder_members_paginator: ListFolderMembersPaginator = client.get_paginator("list_folder_members")
        list_folders_for_resource_paginator: ListFoldersForResourcePaginator = client.get_paginator("list_folders_for_resource")
        list_folders_paginator: ListFoldersPaginator = client.get_paginator("list_folders")
        list_group_memberships_paginator: ListGroupMembershipsPaginator = client.get_paginator("list_group_memberships")
        list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
        list_iam_policy_assignments_for_user_paginator: ListIAMPolicyAssignmentsForUserPaginator = client.get_paginator("list_iam_policy_assignments_for_user")
        list_iam_policy_assignments_paginator: ListIAMPolicyAssignmentsPaginator = client.get_paginator("list_iam_policy_assignments")
        list_ingestions_paginator: ListIngestionsPaginator = client.get_paginator("list_ingestions")
        list_namespaces_paginator: ListNamespacesPaginator = client.get_paginator("list_namespaces")
        list_role_memberships_paginator: ListRoleMembershipsPaginator = client.get_paginator("list_role_memberships")
        list_template_aliases_paginator: ListTemplateAliasesPaginator = client.get_paginator("list_template_aliases")
        list_template_versions_paginator: ListTemplateVersionsPaginator = client.get_paginator("list_template_versions")
        list_templates_paginator: ListTemplatesPaginator = client.get_paginator("list_templates")
        list_theme_versions_paginator: ListThemeVersionsPaginator = client.get_paginator("list_theme_versions")
        list_themes_paginator: ListThemesPaginator = client.get_paginator("list_themes")
        list_user_groups_paginator: ListUserGroupsPaginator = client.get_paginator("list_user_groups")
        list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
        search_analyses_paginator: SearchAnalysesPaginator = client.get_paginator("search_analyses")
        search_dashboards_paginator: SearchDashboardsPaginator = client.get_paginator("search_dashboards")
        search_data_sets_paginator: SearchDataSetsPaginator = client.get_paginator("search_data_sets")
        search_data_sources_paginator: SearchDataSourcesPaginator = client.get_paginator("search_data_sources")
        search_folders_paginator: SearchFoldersPaginator = client.get_paginator("search_folders")
        search_groups_paginator: SearchGroupsPaginator = client.get_paginator("search_groups")
        search_topics_paginator: SearchTopicsPaginator = client.get_paginator("search_topics")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeFolderPermissionsRequestPaginateTypeDef,
    DescribeFolderPermissionsResponseTypeDef,
    DescribeFolderResolvedPermissionsRequestPaginateTypeDef,
    DescribeFolderResolvedPermissionsResponseTypeDef,
    ListAnalysesRequestPaginateTypeDef,
    ListAnalysesResponseTypeDef,
    ListAssetBundleExportJobsRequestPaginateTypeDef,
    ListAssetBundleExportJobsResponseTypeDef,
    ListAssetBundleImportJobsRequestPaginateTypeDef,
    ListAssetBundleImportJobsResponseTypeDef,
    ListBrandsRequestPaginateTypeDef,
    ListBrandsResponseTypeDef,
    ListCustomPermissionsRequestPaginateTypeDef,
    ListCustomPermissionsResponseTypeDef,
    ListDashboardsRequestPaginateTypeDef,
    ListDashboardsResponseTypeDef,
    ListDashboardVersionsRequestPaginateTypeDef,
    ListDashboardVersionsResponseTypeDef,
    ListDataSetsRequestPaginateTypeDef,
    ListDataSetsResponseTypeDef,
    ListDataSourcesRequestPaginateTypeDef,
    ListDataSourcesResponseTypeDef,
    ListFolderMembersRequestPaginateTypeDef,
    ListFolderMembersResponseTypeDef,
    ListFoldersForResourceRequestPaginateTypeDef,
    ListFoldersForResourceResponseTypeDef,
    ListFoldersRequestPaginateTypeDef,
    ListFoldersResponseTypeDef,
    ListGroupMembershipsRequestPaginateTypeDef,
    ListGroupMembershipsResponseTypeDef,
    ListGroupsRequestPaginateTypeDef,
    ListGroupsResponseTypeDef,
    ListIAMPolicyAssignmentsForUserRequestPaginateTypeDef,
    ListIAMPolicyAssignmentsForUserResponseTypeDef,
    ListIAMPolicyAssignmentsRequestPaginateTypeDef,
    ListIAMPolicyAssignmentsResponseTypeDef,
    ListIngestionsRequestPaginateTypeDef,
    ListIngestionsResponseTypeDef,
    ListNamespacesRequestPaginateTypeDef,
    ListNamespacesResponseTypeDef,
    ListRoleMembershipsRequestPaginateTypeDef,
    ListRoleMembershipsResponseTypeDef,
    ListTemplateAliasesRequestPaginateTypeDef,
    ListTemplateAliasesResponseTypeDef,
    ListTemplatesRequestPaginateTypeDef,
    ListTemplatesResponseTypeDef,
    ListTemplateVersionsRequestPaginateTypeDef,
    ListTemplateVersionsResponseTypeDef,
    ListThemesRequestPaginateTypeDef,
    ListThemesResponseTypeDef,
    ListThemeVersionsRequestPaginateTypeDef,
    ListThemeVersionsResponseTypeDef,
    ListUserGroupsRequestPaginateTypeDef,
    ListUserGroupsResponseTypeDef,
    ListUsersRequestPaginateTypeDef,
    ListUsersResponseTypeDef,
    SearchAnalysesRequestPaginateTypeDef,
    SearchAnalysesResponseTypeDef,
    SearchDashboardsRequestPaginateTypeDef,
    SearchDashboardsResponseTypeDef,
    SearchDataSetsRequestPaginateTypeDef,
    SearchDataSetsResponseTypeDef,
    SearchDataSourcesRequestPaginateTypeDef,
    SearchDataSourcesResponseTypeDef,
    SearchFoldersRequestPaginateTypeDef,
    SearchFoldersResponseTypeDef,
    SearchGroupsRequestPaginateTypeDef,
    SearchGroupsResponseTypeDef,
    SearchTopicsRequestPaginateTypeDef,
    SearchTopicsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeFolderPermissionsPaginator",
    "DescribeFolderResolvedPermissionsPaginator",
    "ListAnalysesPaginator",
    "ListAssetBundleExportJobsPaginator",
    "ListAssetBundleImportJobsPaginator",
    "ListBrandsPaginator",
    "ListCustomPermissionsPaginator",
    "ListDashboardVersionsPaginator",
    "ListDashboardsPaginator",
    "ListDataSetsPaginator",
    "ListDataSourcesPaginator",
    "ListFolderMembersPaginator",
    "ListFoldersForResourcePaginator",
    "ListFoldersPaginator",
    "ListGroupMembershipsPaginator",
    "ListGroupsPaginator",
    "ListIAMPolicyAssignmentsForUserPaginator",
    "ListIAMPolicyAssignmentsPaginator",
    "ListIngestionsPaginator",
    "ListNamespacesPaginator",
    "ListRoleMembershipsPaginator",
    "ListTemplateAliasesPaginator",
    "ListTemplateVersionsPaginator",
    "ListTemplatesPaginator",
    "ListThemeVersionsPaginator",
    "ListThemesPaginator",
    "ListUserGroupsPaginator",
    "ListUsersPaginator",
    "SearchAnalysesPaginator",
    "SearchDashboardsPaginator",
    "SearchDataSetsPaginator",
    "SearchDataSourcesPaginator",
    "SearchFoldersPaginator",
    "SearchGroupsPaginator",
    "SearchTopicsPaginator",
)

if TYPE_CHECKING:
    _DescribeFolderPermissionsPaginatorBase = AioPaginator[DescribeFolderPermissionsResponseTypeDef]
else:
    _DescribeFolderPermissionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeFolderPermissionsPaginator(_DescribeFolderPermissionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/DescribeFolderPermissions.html#QuickSight.Paginator.DescribeFolderPermissions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#describefolderpermissionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFolderPermissionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeFolderPermissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/DescribeFolderPermissions.html#QuickSight.Paginator.DescribeFolderPermissions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#describefolderpermissionspaginator)
        """

if TYPE_CHECKING:
    _DescribeFolderResolvedPermissionsPaginatorBase = AioPaginator[
        DescribeFolderResolvedPermissionsResponseTypeDef
    ]
else:
    _DescribeFolderResolvedPermissionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeFolderResolvedPermissionsPaginator(_DescribeFolderResolvedPermissionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/DescribeFolderResolvedPermissions.html#QuickSight.Paginator.DescribeFolderResolvedPermissions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#describefolderresolvedpermissionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFolderResolvedPermissionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeFolderResolvedPermissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/DescribeFolderResolvedPermissions.html#QuickSight.Paginator.DescribeFolderResolvedPermissions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#describefolderresolvedpermissionspaginator)
        """

if TYPE_CHECKING:
    _ListAnalysesPaginatorBase = AioPaginator[ListAnalysesResponseTypeDef]
else:
    _ListAnalysesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAnalysesPaginator(_ListAnalysesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListAnalyses.html#QuickSight.Paginator.ListAnalyses)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listanalysespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAnalysesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAnalysesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListAnalyses.html#QuickSight.Paginator.ListAnalyses.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listanalysespaginator)
        """

if TYPE_CHECKING:
    _ListAssetBundleExportJobsPaginatorBase = AioPaginator[ListAssetBundleExportJobsResponseTypeDef]
else:
    _ListAssetBundleExportJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAssetBundleExportJobsPaginator(_ListAssetBundleExportJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListAssetBundleExportJobs.html#QuickSight.Paginator.ListAssetBundleExportJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listassetbundleexportjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssetBundleExportJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAssetBundleExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListAssetBundleExportJobs.html#QuickSight.Paginator.ListAssetBundleExportJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listassetbundleexportjobspaginator)
        """

if TYPE_CHECKING:
    _ListAssetBundleImportJobsPaginatorBase = AioPaginator[ListAssetBundleImportJobsResponseTypeDef]
else:
    _ListAssetBundleImportJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAssetBundleImportJobsPaginator(_ListAssetBundleImportJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListAssetBundleImportJobs.html#QuickSight.Paginator.ListAssetBundleImportJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listassetbundleimportjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssetBundleImportJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAssetBundleImportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListAssetBundleImportJobs.html#QuickSight.Paginator.ListAssetBundleImportJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listassetbundleimportjobspaginator)
        """

if TYPE_CHECKING:
    _ListBrandsPaginatorBase = AioPaginator[ListBrandsResponseTypeDef]
else:
    _ListBrandsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBrandsPaginator(_ListBrandsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListBrands.html#QuickSight.Paginator.ListBrands)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listbrandspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBrandsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBrandsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListBrands.html#QuickSight.Paginator.ListBrands.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listbrandspaginator)
        """

if TYPE_CHECKING:
    _ListCustomPermissionsPaginatorBase = AioPaginator[ListCustomPermissionsResponseTypeDef]
else:
    _ListCustomPermissionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCustomPermissionsPaginator(_ListCustomPermissionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListCustomPermissions.html#QuickSight.Paginator.ListCustomPermissions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listcustompermissionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCustomPermissionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCustomPermissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListCustomPermissions.html#QuickSight.Paginator.ListCustomPermissions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listcustompermissionspaginator)
        """

if TYPE_CHECKING:
    _ListDashboardVersionsPaginatorBase = AioPaginator[ListDashboardVersionsResponseTypeDef]
else:
    _ListDashboardVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDashboardVersionsPaginator(_ListDashboardVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListDashboardVersions.html#QuickSight.Paginator.ListDashboardVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listdashboardversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDashboardVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDashboardVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListDashboardVersions.html#QuickSight.Paginator.ListDashboardVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listdashboardversionspaginator)
        """

if TYPE_CHECKING:
    _ListDashboardsPaginatorBase = AioPaginator[ListDashboardsResponseTypeDef]
else:
    _ListDashboardsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDashboardsPaginator(_ListDashboardsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListDashboards.html#QuickSight.Paginator.ListDashboards)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listdashboardspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDashboardsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDashboardsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListDashboards.html#QuickSight.Paginator.ListDashboards.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listdashboardspaginator)
        """

if TYPE_CHECKING:
    _ListDataSetsPaginatorBase = AioPaginator[ListDataSetsResponseTypeDef]
else:
    _ListDataSetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataSetsPaginator(_ListDataSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListDataSets.html#QuickSight.Paginator.ListDataSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listdatasetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataSetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListDataSets.html#QuickSight.Paginator.ListDataSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listdatasetspaginator)
        """

if TYPE_CHECKING:
    _ListDataSourcesPaginatorBase = AioPaginator[ListDataSourcesResponseTypeDef]
else:
    _ListDataSourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataSourcesPaginator(_ListDataSourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListDataSources.html#QuickSight.Paginator.ListDataSources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listdatasourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataSourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListDataSources.html#QuickSight.Paginator.ListDataSources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listdatasourcespaginator)
        """

if TYPE_CHECKING:
    _ListFolderMembersPaginatorBase = AioPaginator[ListFolderMembersResponseTypeDef]
else:
    _ListFolderMembersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFolderMembersPaginator(_ListFolderMembersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListFolderMembers.html#QuickSight.Paginator.ListFolderMembers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listfoldermemberspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFolderMembersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFolderMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListFolderMembers.html#QuickSight.Paginator.ListFolderMembers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listfoldermemberspaginator)
        """

if TYPE_CHECKING:
    _ListFoldersForResourcePaginatorBase = AioPaginator[ListFoldersForResourceResponseTypeDef]
else:
    _ListFoldersForResourcePaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFoldersForResourcePaginator(_ListFoldersForResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListFoldersForResource.html#QuickSight.Paginator.ListFoldersForResource)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listfoldersforresourcepaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFoldersForResourceRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFoldersForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListFoldersForResource.html#QuickSight.Paginator.ListFoldersForResource.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listfoldersforresourcepaginator)
        """

if TYPE_CHECKING:
    _ListFoldersPaginatorBase = AioPaginator[ListFoldersResponseTypeDef]
else:
    _ListFoldersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFoldersPaginator(_ListFoldersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListFolders.html#QuickSight.Paginator.ListFolders)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listfolderspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFoldersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFoldersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListFolders.html#QuickSight.Paginator.ListFolders.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listfolderspaginator)
        """

if TYPE_CHECKING:
    _ListGroupMembershipsPaginatorBase = AioPaginator[ListGroupMembershipsResponseTypeDef]
else:
    _ListGroupMembershipsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListGroupMembershipsPaginator(_ListGroupMembershipsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListGroupMemberships.html#QuickSight.Paginator.ListGroupMemberships)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listgroupmembershipspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGroupMembershipsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGroupMembershipsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListGroupMemberships.html#QuickSight.Paginator.ListGroupMemberships.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listgroupmembershipspaginator)
        """

if TYPE_CHECKING:
    _ListGroupsPaginatorBase = AioPaginator[ListGroupsResponseTypeDef]
else:
    _ListGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListGroupsPaginator(_ListGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListGroups.html#QuickSight.Paginator.ListGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listgroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListGroups.html#QuickSight.Paginator.ListGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listgroupspaginator)
        """

if TYPE_CHECKING:
    _ListIAMPolicyAssignmentsForUserPaginatorBase = AioPaginator[
        ListIAMPolicyAssignmentsForUserResponseTypeDef
    ]
else:
    _ListIAMPolicyAssignmentsForUserPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListIAMPolicyAssignmentsForUserPaginator(_ListIAMPolicyAssignmentsForUserPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListIAMPolicyAssignmentsForUser.html#QuickSight.Paginator.ListIAMPolicyAssignmentsForUser)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listiampolicyassignmentsforuserpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIAMPolicyAssignmentsForUserRequestPaginateTypeDef]
    ) -> AioPageIterator[ListIAMPolicyAssignmentsForUserResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListIAMPolicyAssignmentsForUser.html#QuickSight.Paginator.ListIAMPolicyAssignmentsForUser.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listiampolicyassignmentsforuserpaginator)
        """

if TYPE_CHECKING:
    _ListIAMPolicyAssignmentsPaginatorBase = AioPaginator[ListIAMPolicyAssignmentsResponseTypeDef]
else:
    _ListIAMPolicyAssignmentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListIAMPolicyAssignmentsPaginator(_ListIAMPolicyAssignmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListIAMPolicyAssignments.html#QuickSight.Paginator.ListIAMPolicyAssignments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listiampolicyassignmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIAMPolicyAssignmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListIAMPolicyAssignmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListIAMPolicyAssignments.html#QuickSight.Paginator.ListIAMPolicyAssignments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listiampolicyassignmentspaginator)
        """

if TYPE_CHECKING:
    _ListIngestionsPaginatorBase = AioPaginator[ListIngestionsResponseTypeDef]
else:
    _ListIngestionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListIngestionsPaginator(_ListIngestionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListIngestions.html#QuickSight.Paginator.ListIngestions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listingestionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIngestionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListIngestionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListIngestions.html#QuickSight.Paginator.ListIngestions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listingestionspaginator)
        """

if TYPE_CHECKING:
    _ListNamespacesPaginatorBase = AioPaginator[ListNamespacesResponseTypeDef]
else:
    _ListNamespacesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNamespacesPaginator(_ListNamespacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListNamespaces.html#QuickSight.Paginator.ListNamespaces)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listnamespacespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNamespacesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNamespacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListNamespaces.html#QuickSight.Paginator.ListNamespaces.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listnamespacespaginator)
        """

if TYPE_CHECKING:
    _ListRoleMembershipsPaginatorBase = AioPaginator[ListRoleMembershipsResponseTypeDef]
else:
    _ListRoleMembershipsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRoleMembershipsPaginator(_ListRoleMembershipsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListRoleMemberships.html#QuickSight.Paginator.ListRoleMemberships)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listrolemembershipspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRoleMembershipsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRoleMembershipsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListRoleMemberships.html#QuickSight.Paginator.ListRoleMemberships.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listrolemembershipspaginator)
        """

if TYPE_CHECKING:
    _ListTemplateAliasesPaginatorBase = AioPaginator[ListTemplateAliasesResponseTypeDef]
else:
    _ListTemplateAliasesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTemplateAliasesPaginator(_ListTemplateAliasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListTemplateAliases.html#QuickSight.Paginator.ListTemplateAliases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listtemplatealiasespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTemplateAliasesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTemplateAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListTemplateAliases.html#QuickSight.Paginator.ListTemplateAliases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listtemplatealiasespaginator)
        """

if TYPE_CHECKING:
    _ListTemplateVersionsPaginatorBase = AioPaginator[ListTemplateVersionsResponseTypeDef]
else:
    _ListTemplateVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTemplateVersionsPaginator(_ListTemplateVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListTemplateVersions.html#QuickSight.Paginator.ListTemplateVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listtemplateversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTemplateVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTemplateVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListTemplateVersions.html#QuickSight.Paginator.ListTemplateVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listtemplateversionspaginator)
        """

if TYPE_CHECKING:
    _ListTemplatesPaginatorBase = AioPaginator[ListTemplatesResponseTypeDef]
else:
    _ListTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTemplatesPaginator(_ListTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListTemplates.html#QuickSight.Paginator.ListTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listtemplatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListTemplates.html#QuickSight.Paginator.ListTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listtemplatespaginator)
        """

if TYPE_CHECKING:
    _ListThemeVersionsPaginatorBase = AioPaginator[ListThemeVersionsResponseTypeDef]
else:
    _ListThemeVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListThemeVersionsPaginator(_ListThemeVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListThemeVersions.html#QuickSight.Paginator.ListThemeVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listthemeversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThemeVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListThemeVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListThemeVersions.html#QuickSight.Paginator.ListThemeVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listthemeversionspaginator)
        """

if TYPE_CHECKING:
    _ListThemesPaginatorBase = AioPaginator[ListThemesResponseTypeDef]
else:
    _ListThemesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListThemesPaginator(_ListThemesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListThemes.html#QuickSight.Paginator.ListThemes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listthemespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThemesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListThemesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListThemes.html#QuickSight.Paginator.ListThemes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listthemespaginator)
        """

if TYPE_CHECKING:
    _ListUserGroupsPaginatorBase = AioPaginator[ListUserGroupsResponseTypeDef]
else:
    _ListUserGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListUserGroupsPaginator(_ListUserGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListUserGroups.html#QuickSight.Paginator.ListUserGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listusergroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUserGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUserGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListUserGroups.html#QuickSight.Paginator.ListUserGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listusergroupspaginator)
        """

if TYPE_CHECKING:
    _ListUsersPaginatorBase = AioPaginator[ListUsersResponseTypeDef]
else:
    _ListUsersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListUsersPaginator(_ListUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListUsers.html#QuickSight.Paginator.ListUsers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listuserspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUsersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/ListUsers.html#QuickSight.Paginator.ListUsers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#listuserspaginator)
        """

if TYPE_CHECKING:
    _SearchAnalysesPaginatorBase = AioPaginator[SearchAnalysesResponseTypeDef]
else:
    _SearchAnalysesPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchAnalysesPaginator(_SearchAnalysesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchAnalyses.html#QuickSight.Paginator.SearchAnalyses)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchanalysespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchAnalysesRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchAnalysesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchAnalyses.html#QuickSight.Paginator.SearchAnalyses.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchanalysespaginator)
        """

if TYPE_CHECKING:
    _SearchDashboardsPaginatorBase = AioPaginator[SearchDashboardsResponseTypeDef]
else:
    _SearchDashboardsPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchDashboardsPaginator(_SearchDashboardsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchDashboards.html#QuickSight.Paginator.SearchDashboards)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchdashboardspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchDashboardsRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchDashboardsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchDashboards.html#QuickSight.Paginator.SearchDashboards.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchdashboardspaginator)
        """

if TYPE_CHECKING:
    _SearchDataSetsPaginatorBase = AioPaginator[SearchDataSetsResponseTypeDef]
else:
    _SearchDataSetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchDataSetsPaginator(_SearchDataSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchDataSets.html#QuickSight.Paginator.SearchDataSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchdatasetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchDataSetsRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchDataSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchDataSets.html#QuickSight.Paginator.SearchDataSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchdatasetspaginator)
        """

if TYPE_CHECKING:
    _SearchDataSourcesPaginatorBase = AioPaginator[SearchDataSourcesResponseTypeDef]
else:
    _SearchDataSourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchDataSourcesPaginator(_SearchDataSourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchDataSources.html#QuickSight.Paginator.SearchDataSources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchdatasourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchDataSourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchDataSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchDataSources.html#QuickSight.Paginator.SearchDataSources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchdatasourcespaginator)
        """

if TYPE_CHECKING:
    _SearchFoldersPaginatorBase = AioPaginator[SearchFoldersResponseTypeDef]
else:
    _SearchFoldersPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchFoldersPaginator(_SearchFoldersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchFolders.html#QuickSight.Paginator.SearchFolders)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchfolderspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchFoldersRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchFoldersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchFolders.html#QuickSight.Paginator.SearchFolders.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchfolderspaginator)
        """

if TYPE_CHECKING:
    _SearchGroupsPaginatorBase = AioPaginator[SearchGroupsResponseTypeDef]
else:
    _SearchGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchGroupsPaginator(_SearchGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchGroups.html#QuickSight.Paginator.SearchGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchgroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchGroups.html#QuickSight.Paginator.SearchGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchgroupspaginator)
        """

if TYPE_CHECKING:
    _SearchTopicsPaginatorBase = AioPaginator[SearchTopicsResponseTypeDef]
else:
    _SearchTopicsPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchTopicsPaginator(_SearchTopicsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchTopics.html#QuickSight.Paginator.SearchTopics)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchtopicspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchTopicsRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchTopicsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/paginator/SearchTopics.html#QuickSight.Paginator.SearchTopics.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_quicksight/paginators/#searchtopicspaginator)
        """
