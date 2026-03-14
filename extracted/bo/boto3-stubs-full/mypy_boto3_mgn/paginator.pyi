"""
Type annotations for mgn service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/)

Copyright 2026 Vlad Emelianov

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
        ListImportFileEnrichmentsPaginator,
        ListImportsPaginator,
        ListManagedAccountsPaginator,
        ListNetworkMigrationAnalysesPaginator,
        ListNetworkMigrationAnalysisResultsPaginator,
        ListNetworkMigrationCodeGenerationSegmentsPaginator,
        ListNetworkMigrationCodeGenerationsPaginator,
        ListNetworkMigrationDefinitionsPaginator,
        ListNetworkMigrationDeployedStacksPaginator,
        ListNetworkMigrationDeploymentsPaginator,
        ListNetworkMigrationExecutionsPaginator,
        ListNetworkMigrationMapperSegmentConstructsPaginator,
        ListNetworkMigrationMapperSegmentsPaginator,
        ListNetworkMigrationMappingUpdatesPaginator,
        ListNetworkMigrationMappingsPaginator,
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
    list_import_file_enrichments_paginator: ListImportFileEnrichmentsPaginator = client.get_paginator("list_import_file_enrichments")
    list_imports_paginator: ListImportsPaginator = client.get_paginator("list_imports")
    list_managed_accounts_paginator: ListManagedAccountsPaginator = client.get_paginator("list_managed_accounts")
    list_network_migration_analyses_paginator: ListNetworkMigrationAnalysesPaginator = client.get_paginator("list_network_migration_analyses")
    list_network_migration_analysis_results_paginator: ListNetworkMigrationAnalysisResultsPaginator = client.get_paginator("list_network_migration_analysis_results")
    list_network_migration_code_generation_segments_paginator: ListNetworkMigrationCodeGenerationSegmentsPaginator = client.get_paginator("list_network_migration_code_generation_segments")
    list_network_migration_code_generations_paginator: ListNetworkMigrationCodeGenerationsPaginator = client.get_paginator("list_network_migration_code_generations")
    list_network_migration_definitions_paginator: ListNetworkMigrationDefinitionsPaginator = client.get_paginator("list_network_migration_definitions")
    list_network_migration_deployed_stacks_paginator: ListNetworkMigrationDeployedStacksPaginator = client.get_paginator("list_network_migration_deployed_stacks")
    list_network_migration_deployments_paginator: ListNetworkMigrationDeploymentsPaginator = client.get_paginator("list_network_migration_deployments")
    list_network_migration_executions_paginator: ListNetworkMigrationExecutionsPaginator = client.get_paginator("list_network_migration_executions")
    list_network_migration_mapper_segment_constructs_paginator: ListNetworkMigrationMapperSegmentConstructsPaginator = client.get_paginator("list_network_migration_mapper_segment_constructs")
    list_network_migration_mapper_segments_paginator: ListNetworkMigrationMapperSegmentsPaginator = client.get_paginator("list_network_migration_mapper_segments")
    list_network_migration_mapping_updates_paginator: ListNetworkMigrationMappingUpdatesPaginator = client.get_paginator("list_network_migration_mapping_updates")
    list_network_migration_mappings_paginator: ListNetworkMigrationMappingsPaginator = client.get_paginator("list_network_migration_mappings")
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
    ListImportFileEnrichmentsRequestPaginateTypeDef,
    ListImportFileEnrichmentsResponseTypeDef,
    ListImportsRequestPaginateTypeDef,
    ListImportsResponseTypeDef,
    ListManagedAccountsRequestPaginateTypeDef,
    ListManagedAccountsResponseTypeDef,
    ListNetworkMigrationAnalysesRequestPaginateTypeDef,
    ListNetworkMigrationAnalysesResponseTypeDef,
    ListNetworkMigrationAnalysisResultsRequestPaginateTypeDef,
    ListNetworkMigrationAnalysisResultsResponseTypeDef,
    ListNetworkMigrationCodeGenerationSegmentsRequestPaginateTypeDef,
    ListNetworkMigrationCodeGenerationSegmentsResponseTypeDef,
    ListNetworkMigrationCodeGenerationsRequestPaginateTypeDef,
    ListNetworkMigrationCodeGenerationsResponseTypeDef,
    ListNetworkMigrationDefinitionsRequestPaginateTypeDef,
    ListNetworkMigrationDefinitionsResponseTypeDef,
    ListNetworkMigrationDeployedStacksRequestPaginateTypeDef,
    ListNetworkMigrationDeployedStacksResponseTypeDef,
    ListNetworkMigrationDeployerJobResponseTypeDef,
    ListNetworkMigrationDeploymentsRequestPaginateTypeDef,
    ListNetworkMigrationExecutionsRequestPaginateTypeDef,
    ListNetworkMigrationExecutionsResponseTypeDef,
    ListNetworkMigrationMapperSegmentConstructsRequestPaginateTypeDef,
    ListNetworkMigrationMapperSegmentConstructsResponseTypeDef,
    ListNetworkMigrationMapperSegmentsRequestPaginateTypeDef,
    ListNetworkMigrationMapperSegmentsResponseTypeDef,
    ListNetworkMigrationMappingsRequestPaginateTypeDef,
    ListNetworkMigrationMappingsResponseTypeDef,
    ListNetworkMigrationMappingUpdatesRequestPaginateTypeDef,
    ListNetworkMigrationMappingUpdatesResponseTypeDef,
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
    "ListImportFileEnrichmentsPaginator",
    "ListImportsPaginator",
    "ListManagedAccountsPaginator",
    "ListNetworkMigrationAnalysesPaginator",
    "ListNetworkMigrationAnalysisResultsPaginator",
    "ListNetworkMigrationCodeGenerationSegmentsPaginator",
    "ListNetworkMigrationCodeGenerationsPaginator",
    "ListNetworkMigrationDefinitionsPaginator",
    "ListNetworkMigrationDeployedStacksPaginator",
    "ListNetworkMigrationDeploymentsPaginator",
    "ListNetworkMigrationExecutionsPaginator",
    "ListNetworkMigrationMapperSegmentConstructsPaginator",
    "ListNetworkMigrationMapperSegmentsPaginator",
    "ListNetworkMigrationMappingUpdatesPaginator",
    "ListNetworkMigrationMappingsPaginator",
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
    _ListImportFileEnrichmentsPaginatorBase = Paginator[ListImportFileEnrichmentsResponseTypeDef]
else:
    _ListImportFileEnrichmentsPaginatorBase = Paginator  # type: ignore[assignment]

class ListImportFileEnrichmentsPaginator(_ListImportFileEnrichmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListImportFileEnrichments.html#Mgn.Paginator.ListImportFileEnrichments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listimportfileenrichmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImportFileEnrichmentsRequestPaginateTypeDef]
    ) -> PageIterator[ListImportFileEnrichmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListImportFileEnrichments.html#Mgn.Paginator.ListImportFileEnrichments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listimportfileenrichmentspaginator)
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
    _ListNetworkMigrationAnalysesPaginatorBase = Paginator[
        ListNetworkMigrationAnalysesResponseTypeDef
    ]
else:
    _ListNetworkMigrationAnalysesPaginatorBase = Paginator  # type: ignore[assignment]

class ListNetworkMigrationAnalysesPaginator(_ListNetworkMigrationAnalysesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationAnalyses.html#Mgn.Paginator.ListNetworkMigrationAnalyses)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationanalysespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationAnalysesRequestPaginateTypeDef]
    ) -> PageIterator[ListNetworkMigrationAnalysesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationAnalyses.html#Mgn.Paginator.ListNetworkMigrationAnalyses.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationanalysespaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationAnalysisResultsPaginatorBase = Paginator[
        ListNetworkMigrationAnalysisResultsResponseTypeDef
    ]
else:
    _ListNetworkMigrationAnalysisResultsPaginatorBase = Paginator  # type: ignore[assignment]

class ListNetworkMigrationAnalysisResultsPaginator(
    _ListNetworkMigrationAnalysisResultsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationAnalysisResults.html#Mgn.Paginator.ListNetworkMigrationAnalysisResults)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationanalysisresultspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationAnalysisResultsRequestPaginateTypeDef]
    ) -> PageIterator[ListNetworkMigrationAnalysisResultsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationAnalysisResults.html#Mgn.Paginator.ListNetworkMigrationAnalysisResults.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationanalysisresultspaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationCodeGenerationSegmentsPaginatorBase = Paginator[
        ListNetworkMigrationCodeGenerationSegmentsResponseTypeDef
    ]
else:
    _ListNetworkMigrationCodeGenerationSegmentsPaginatorBase = Paginator  # type: ignore[assignment]

class ListNetworkMigrationCodeGenerationSegmentsPaginator(
    _ListNetworkMigrationCodeGenerationSegmentsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationCodeGenerationSegments.html#Mgn.Paginator.ListNetworkMigrationCodeGenerationSegments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationcodegenerationsegmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationCodeGenerationSegmentsRequestPaginateTypeDef]
    ) -> PageIterator[ListNetworkMigrationCodeGenerationSegmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationCodeGenerationSegments.html#Mgn.Paginator.ListNetworkMigrationCodeGenerationSegments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationcodegenerationsegmentspaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationCodeGenerationsPaginatorBase = Paginator[
        ListNetworkMigrationCodeGenerationsResponseTypeDef
    ]
else:
    _ListNetworkMigrationCodeGenerationsPaginatorBase = Paginator  # type: ignore[assignment]

class ListNetworkMigrationCodeGenerationsPaginator(
    _ListNetworkMigrationCodeGenerationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationCodeGenerations.html#Mgn.Paginator.ListNetworkMigrationCodeGenerations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationcodegenerationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationCodeGenerationsRequestPaginateTypeDef]
    ) -> PageIterator[ListNetworkMigrationCodeGenerationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationCodeGenerations.html#Mgn.Paginator.ListNetworkMigrationCodeGenerations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationcodegenerationspaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationDefinitionsPaginatorBase = Paginator[
        ListNetworkMigrationDefinitionsResponseTypeDef
    ]
else:
    _ListNetworkMigrationDefinitionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListNetworkMigrationDefinitionsPaginator(_ListNetworkMigrationDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationDefinitions.html#Mgn.Paginator.ListNetworkMigrationDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationdefinitionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationDefinitionsRequestPaginateTypeDef]
    ) -> PageIterator[ListNetworkMigrationDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationDefinitions.html#Mgn.Paginator.ListNetworkMigrationDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationdefinitionspaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationDeployedStacksPaginatorBase = Paginator[
        ListNetworkMigrationDeployedStacksResponseTypeDef
    ]
else:
    _ListNetworkMigrationDeployedStacksPaginatorBase = Paginator  # type: ignore[assignment]

class ListNetworkMigrationDeployedStacksPaginator(_ListNetworkMigrationDeployedStacksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationDeployedStacks.html#Mgn.Paginator.ListNetworkMigrationDeployedStacks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationdeployedstackspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationDeployedStacksRequestPaginateTypeDef]
    ) -> PageIterator[ListNetworkMigrationDeployedStacksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationDeployedStacks.html#Mgn.Paginator.ListNetworkMigrationDeployedStacks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationdeployedstackspaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationDeploymentsPaginatorBase = Paginator[
        ListNetworkMigrationDeployerJobResponseTypeDef
    ]
else:
    _ListNetworkMigrationDeploymentsPaginatorBase = Paginator  # type: ignore[assignment]

class ListNetworkMigrationDeploymentsPaginator(_ListNetworkMigrationDeploymentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationDeployments.html#Mgn.Paginator.ListNetworkMigrationDeployments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationdeploymentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationDeploymentsRequestPaginateTypeDef]
    ) -> PageIterator[ListNetworkMigrationDeployerJobResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationDeployments.html#Mgn.Paginator.ListNetworkMigrationDeployments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationdeploymentspaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationExecutionsPaginatorBase = Paginator[
        ListNetworkMigrationExecutionsResponseTypeDef
    ]
else:
    _ListNetworkMigrationExecutionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListNetworkMigrationExecutionsPaginator(_ListNetworkMigrationExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationExecutions.html#Mgn.Paginator.ListNetworkMigrationExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationexecutionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationExecutionsRequestPaginateTypeDef]
    ) -> PageIterator[ListNetworkMigrationExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationExecutions.html#Mgn.Paginator.ListNetworkMigrationExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationexecutionspaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationMapperSegmentConstructsPaginatorBase = Paginator[
        ListNetworkMigrationMapperSegmentConstructsResponseTypeDef
    ]
else:
    _ListNetworkMigrationMapperSegmentConstructsPaginatorBase = Paginator  # type: ignore[assignment]

class ListNetworkMigrationMapperSegmentConstructsPaginator(
    _ListNetworkMigrationMapperSegmentConstructsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationMapperSegmentConstructs.html#Mgn.Paginator.ListNetworkMigrationMapperSegmentConstructs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationmappersegmentconstructspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationMapperSegmentConstructsRequestPaginateTypeDef]
    ) -> PageIterator[ListNetworkMigrationMapperSegmentConstructsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationMapperSegmentConstructs.html#Mgn.Paginator.ListNetworkMigrationMapperSegmentConstructs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationmappersegmentconstructspaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationMapperSegmentsPaginatorBase = Paginator[
        ListNetworkMigrationMapperSegmentsResponseTypeDef
    ]
else:
    _ListNetworkMigrationMapperSegmentsPaginatorBase = Paginator  # type: ignore[assignment]

class ListNetworkMigrationMapperSegmentsPaginator(_ListNetworkMigrationMapperSegmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationMapperSegments.html#Mgn.Paginator.ListNetworkMigrationMapperSegments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationmappersegmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationMapperSegmentsRequestPaginateTypeDef]
    ) -> PageIterator[ListNetworkMigrationMapperSegmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationMapperSegments.html#Mgn.Paginator.ListNetworkMigrationMapperSegments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationmappersegmentspaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationMappingUpdatesPaginatorBase = Paginator[
        ListNetworkMigrationMappingUpdatesResponseTypeDef
    ]
else:
    _ListNetworkMigrationMappingUpdatesPaginatorBase = Paginator  # type: ignore[assignment]

class ListNetworkMigrationMappingUpdatesPaginator(_ListNetworkMigrationMappingUpdatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationMappingUpdates.html#Mgn.Paginator.ListNetworkMigrationMappingUpdates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationmappingupdatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationMappingUpdatesRequestPaginateTypeDef]
    ) -> PageIterator[ListNetworkMigrationMappingUpdatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationMappingUpdates.html#Mgn.Paginator.ListNetworkMigrationMappingUpdates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationmappingupdatespaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationMappingsPaginatorBase = Paginator[
        ListNetworkMigrationMappingsResponseTypeDef
    ]
else:
    _ListNetworkMigrationMappingsPaginatorBase = Paginator  # type: ignore[assignment]

class ListNetworkMigrationMappingsPaginator(_ListNetworkMigrationMappingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationMappings.html#Mgn.Paginator.ListNetworkMigrationMappings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationmappingspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationMappingsRequestPaginateTypeDef]
    ) -> PageIterator[ListNetworkMigrationMappingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationMappings.html#Mgn.Paginator.ListNetworkMigrationMappings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#listnetworkmigrationmappingspaginator)
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
