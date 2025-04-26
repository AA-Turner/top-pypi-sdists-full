"""
Type annotations for mgn service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_mgn.client import MgnClient
    from mypy_boto3_mgn.paginator import (
        DescribeJobLogItemsPaginator,
        DescribeJobsPaginator,
        DescribeLaunchConfigurationTemplatesPaginator,
        DescribeReplicationConfigurationTemplatesPaginator,
        DescribeSourceServersPaginator,
        DescribeVcenterClientsPaginator,
        ListApplicationsPaginator,
        ListConnectorsPaginator,
        ListExportErrorsPaginator,
        ListExportsPaginator,
        ListImportErrorsPaginator,
        ListImportsPaginator,
        ListManagedAccountsPaginator,
        ListSourceServerActionsPaginator,
        ListTemplateActionsPaginator,
        ListWavesPaginator,
    )

    session = Session()
    client: MgnClient = session.client("mgn")

    describe_job_log_items_paginator: DescribeJobLogItemsPaginator = client.get_paginator("describe_job_log_items")
    describe_jobs_paginator: DescribeJobsPaginator = client.get_paginator("describe_jobs")
    describe_launch_configuration_templates_paginator: DescribeLaunchConfigurationTemplatesPaginator = client.get_paginator("describe_launch_configuration_templates")
    describe_replication_configuration_templates_paginator: DescribeReplicationConfigurationTemplatesPaginator = client.get_paginator("describe_replication_configuration_templates")
    describe_source_servers_paginator: DescribeSourceServersPaginator = client.get_paginator("describe_source_servers")
    describe_vcenter_clients_paginator: DescribeVcenterClientsPaginator = client.get_paginator("describe_vcenter_clients")
    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    list_connectors_paginator: ListConnectorsPaginator = client.get_paginator("list_connectors")
    list_export_errors_paginator: ListExportErrorsPaginator = client.get_paginator("list_export_errors")
    list_exports_paginator: ListExportsPaginator = client.get_paginator("list_exports")
    list_import_errors_paginator: ListImportErrorsPaginator = client.get_paginator("list_import_errors")
    list_imports_paginator: ListImportsPaginator = client.get_paginator("list_imports")
    list_managed_accounts_paginator: ListManagedAccountsPaginator = client.get_paginator("list_managed_accounts")
    list_source_server_actions_paginator: ListSourceServerActionsPaginator = client.get_paginator("list_source_server_actions")
    list_template_actions_paginator: ListTemplateActionsPaginator = client.get_paginator("list_template_actions")
    list_waves_paginator: ListWavesPaginator = client.get_paginator("list_waves")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeJobLogItemsRequestPaginateTypeDef,
    DescribeJobLogItemsResponseTypeDef,
    DescribeJobsRequestPaginateTypeDef,
    DescribeJobsResponseTypeDef,
    DescribeLaunchConfigurationTemplatesRequestPaginateTypeDef,
    DescribeLaunchConfigurationTemplatesResponseTypeDef,
    DescribeReplicationConfigurationTemplatesRequestPaginateTypeDef,
    DescribeReplicationConfigurationTemplatesResponseTypeDef,
    DescribeSourceServersRequestPaginateTypeDef,
    DescribeSourceServersResponseTypeDef,
    DescribeVcenterClientsRequestPaginateTypeDef,
    DescribeVcenterClientsResponseTypeDef,
    ListApplicationsRequestPaginateTypeDef,
    ListApplicationsResponseTypeDef,
    ListConnectorsRequestPaginateTypeDef,
    ListConnectorsResponseTypeDef,
    ListExportErrorsRequestPaginateTypeDef,
    ListExportErrorsResponseTypeDef,
    ListExportsRequestPaginateTypeDef,
    ListExportsResponseTypeDef,
    ListImportErrorsRequestPaginateTypeDef,
    ListImportErrorsResponseTypeDef,
    ListImportsRequestPaginateTypeDef,
    ListImportsResponseTypeDef,
    ListManagedAccountsRequestPaginateTypeDef,
    ListManagedAccountsResponseTypeDef,
    ListSourceServerActionsRequestPaginateTypeDef,
    ListSourceServerActionsResponseTypeDef,
    ListTemplateActionsRequestPaginateTypeDef,
    ListTemplateActionsResponseTypeDef,
    ListWavesRequestPaginateTypeDef,
    ListWavesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeJobLogItemsPaginator",
    "DescribeJobsPaginator",
    "DescribeLaunchConfigurationTemplatesPaginator",
    "DescribeReplicationConfigurationTemplatesPaginator",
    "DescribeSourceServersPaginator",
    "DescribeVcenterClientsPaginator",
    "ListApplicationsPaginator",
    "ListConnectorsPaginator",
    "ListExportErrorsPaginator",
    "ListExportsPaginator",
    "ListImportErrorsPaginator",
    "ListImportsPaginator",
    "ListManagedAccountsPaginator",
    "ListSourceServerActionsPaginator",
    "ListTemplateActionsPaginator",
    "ListWavesPaginator",
)


if TYPE_CHECKING:
    _DescribeJobLogItemsPaginatorBase = Paginator[DescribeJobLogItemsResponseTypeDef]
else:
    _DescribeJobLogItemsPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeJobLogItemsPaginator(_DescribeJobLogItemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeJobLogItems.html#Mgn.Paginator.DescribeJobLogItems)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describejoblogitemspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeJobLogItemsRequestPaginateTypeDef]
    ) -> PageIterator[DescribeJobLogItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeJobLogItems.html#Mgn.Paginator.DescribeJobLogItems.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describejoblogitemspaginator)
        """


if TYPE_CHECKING:
    _DescribeJobsPaginatorBase = Paginator[DescribeJobsResponseTypeDef]
else:
    _DescribeJobsPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeJobsPaginator(_DescribeJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeJobs.html#Mgn.Paginator.DescribeJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describejobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeJobsRequestPaginateTypeDef]
    ) -> PageIterator[DescribeJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeJobs.html#Mgn.Paginator.DescribeJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describejobspaginator)
        """


if TYPE_CHECKING:
    _DescribeLaunchConfigurationTemplatesPaginatorBase = Paginator[
        DescribeLaunchConfigurationTemplatesResponseTypeDef
    ]
else:
    _DescribeLaunchConfigurationTemplatesPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeLaunchConfigurationTemplatesPaginator(
    _DescribeLaunchConfigurationTemplatesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeLaunchConfigurationTemplates.html#Mgn.Paginator.DescribeLaunchConfigurationTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describelaunchconfigurationtemplatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeLaunchConfigurationTemplatesRequestPaginateTypeDef]
    ) -> PageIterator[DescribeLaunchConfigurationTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeLaunchConfigurationTemplates.html#Mgn.Paginator.DescribeLaunchConfigurationTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describelaunchconfigurationtemplatespaginator)
        """


if TYPE_CHECKING:
    _DescribeReplicationConfigurationTemplatesPaginatorBase = Paginator[
        DescribeReplicationConfigurationTemplatesResponseTypeDef
    ]
else:
    _DescribeReplicationConfigurationTemplatesPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeReplicationConfigurationTemplatesPaginator(
    _DescribeReplicationConfigurationTemplatesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeReplicationConfigurationTemplates.html#Mgn.Paginator.DescribeReplicationConfigurationTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describereplicationconfigurationtemplatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationConfigurationTemplatesRequestPaginateTypeDef]
    ) -> PageIterator[DescribeReplicationConfigurationTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeReplicationConfigurationTemplates.html#Mgn.Paginator.DescribeReplicationConfigurationTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describereplicationconfigurationtemplatespaginator)
        """


if TYPE_CHECKING:
    _DescribeSourceServersPaginatorBase = Paginator[DescribeSourceServersResponseTypeDef]
else:
    _DescribeSourceServersPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeSourceServersPaginator(_DescribeSourceServersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeSourceServers.html#Mgn.Paginator.DescribeSourceServers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describesourceserverspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSourceServersRequestPaginateTypeDef]
    ) -> PageIterator[DescribeSourceServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeSourceServers.html#Mgn.Paginator.DescribeSourceServers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describesourceserverspaginator)
        """


if TYPE_CHECKING:
    _DescribeVcenterClientsPaginatorBase = Paginator[DescribeVcenterClientsResponseTypeDef]
else:
    _DescribeVcenterClientsPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeVcenterClientsPaginator(_DescribeVcenterClientsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeVcenterClients.html#Mgn.Paginator.DescribeVcenterClients)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describevcenterclientspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeVcenterClientsRequestPaginateTypeDef]
    ) -> PageIterator[DescribeVcenterClientsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeVcenterClients.html#Mgn.Paginator.DescribeVcenterClients.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describevcenterclientspaginator)
        """


if TYPE_CHECKING:
    _ListApplicationsPaginatorBase = Paginator[ListApplicationsResponseTypeDef]
else:
    _ListApplicationsPaginatorBase = Paginator  # type: ignore[assignment]


class ListApplicationsPaginator(_ListApplicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListApplications.html#Mgn.Paginator.ListApplications)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listapplicationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationsRequestPaginateTypeDef]
    ) -> PageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListApplications.html#Mgn.Paginator.ListApplications.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listapplicationspaginator)
        """


if TYPE_CHECKING:
    _ListConnectorsPaginatorBase = Paginator[ListConnectorsResponseTypeDef]
else:
    _ListConnectorsPaginatorBase = Paginator  # type: ignore[assignment]


class ListConnectorsPaginator(_ListConnectorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListConnectors.html#Mgn.Paginator.ListConnectors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listconnectorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConnectorsRequestPaginateTypeDef]
    ) -> PageIterator[ListConnectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListConnectors.html#Mgn.Paginator.ListConnectors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listconnectorspaginator)
        """


if TYPE_CHECKING:
    _ListExportErrorsPaginatorBase = Paginator[ListExportErrorsResponseTypeDef]
else:
    _ListExportErrorsPaginatorBase = Paginator  # type: ignore[assignment]


class ListExportErrorsPaginator(_ListExportErrorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListExportErrors.html#Mgn.Paginator.ListExportErrors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listexporterrorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExportErrorsRequestPaginateTypeDef]
    ) -> PageIterator[ListExportErrorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListExportErrors.html#Mgn.Paginator.ListExportErrors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listexporterrorspaginator)
        """


if TYPE_CHECKING:
    _ListExportsPaginatorBase = Paginator[ListExportsResponseTypeDef]
else:
    _ListExportsPaginatorBase = Paginator  # type: ignore[assignment]


class ListExportsPaginator(_ListExportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListExports.html#Mgn.Paginator.ListExports)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listexportspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExportsRequestPaginateTypeDef]
    ) -> PageIterator[ListExportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListExports.html#Mgn.Paginator.ListExports.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listexportspaginator)
        """


if TYPE_CHECKING:
    _ListImportErrorsPaginatorBase = Paginator[ListImportErrorsResponseTypeDef]
else:
    _ListImportErrorsPaginatorBase = Paginator  # type: ignore[assignment]


class ListImportErrorsPaginator(_ListImportErrorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListImportErrors.html#Mgn.Paginator.ListImportErrors)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listimporterrorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImportErrorsRequestPaginateTypeDef]
    ) -> PageIterator[ListImportErrorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListImportErrors.html#Mgn.Paginator.ListImportErrors.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listimporterrorspaginator)
        """


if TYPE_CHECKING:
    _ListImportsPaginatorBase = Paginator[ListImportsResponseTypeDef]
else:
    _ListImportsPaginatorBase = Paginator  # type: ignore[assignment]


class ListImportsPaginator(_ListImportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListImports.html#Mgn.Paginator.ListImports)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listimportspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImportsRequestPaginateTypeDef]
    ) -> PageIterator[ListImportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListImports.html#Mgn.Paginator.ListImports.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listimportspaginator)
        """


if TYPE_CHECKING:
    _ListManagedAccountsPaginatorBase = Paginator[ListManagedAccountsResponseTypeDef]
else:
    _ListManagedAccountsPaginatorBase = Paginator  # type: ignore[assignment]


class ListManagedAccountsPaginator(_ListManagedAccountsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListManagedAccounts.html#Mgn.Paginator.ListManagedAccounts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listmanagedaccountspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListManagedAccountsRequestPaginateTypeDef]
    ) -> PageIterator[ListManagedAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListManagedAccounts.html#Mgn.Paginator.ListManagedAccounts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listmanagedaccountspaginator)
        """


if TYPE_CHECKING:
    _ListSourceServerActionsPaginatorBase = Paginator[ListSourceServerActionsResponseTypeDef]
else:
    _ListSourceServerActionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListSourceServerActionsPaginator(_ListSourceServerActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListSourceServerActions.html#Mgn.Paginator.ListSourceServerActions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listsourceserveractionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSourceServerActionsRequestPaginateTypeDef]
    ) -> PageIterator[ListSourceServerActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListSourceServerActions.html#Mgn.Paginator.ListSourceServerActions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listsourceserveractionspaginator)
        """


if TYPE_CHECKING:
    _ListTemplateActionsPaginatorBase = Paginator[ListTemplateActionsResponseTypeDef]
else:
    _ListTemplateActionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListTemplateActionsPaginator(_ListTemplateActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListTemplateActions.html#Mgn.Paginator.ListTemplateActions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listtemplateactionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTemplateActionsRequestPaginateTypeDef]
    ) -> PageIterator[ListTemplateActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListTemplateActions.html#Mgn.Paginator.ListTemplateActions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listtemplateactionspaginator)
        """


if TYPE_CHECKING:
    _ListWavesPaginatorBase = Paginator[ListWavesResponseTypeDef]
else:
    _ListWavesPaginatorBase = Paginator  # type: ignore[assignment]


class ListWavesPaginator(_ListWavesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListWaves.html#Mgn.Paginator.ListWaves)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listwavespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWavesRequestPaginateTypeDef]
    ) -> PageIterator[ListWavesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListWaves.html#Mgn.Paginator.ListWaves.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listwavespaginator)
        """
