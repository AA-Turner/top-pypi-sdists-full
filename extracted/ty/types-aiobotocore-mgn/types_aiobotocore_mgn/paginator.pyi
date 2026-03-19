"""
Type annotations for mgn service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mgn.client import MgnClient
    from types_aiobotocore_mgn.paginator import (
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

    session = get_session()
    with session.create_client("mgn") as client:
        client: MgnClient

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

from aiobotocore.paginate import AioPageIterator, AioPaginator

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
    _DescribeJobLogItemsPaginatorBase = AioPaginator[DescribeJobLogItemsResponseTypeDef]
else:
    _DescribeJobLogItemsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeJobLogItemsPaginator(_DescribeJobLogItemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeJobLogItems.html#Mgn.Paginator.DescribeJobLogItems)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#describejoblogitemspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeJobLogItemsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeJobLogItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeJobLogItems.html#Mgn.Paginator.DescribeJobLogItems.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#describejoblogitemspaginator)
        """

if TYPE_CHECKING:
    _DescribeJobsPaginatorBase = AioPaginator[DescribeJobsResponseTypeDef]
else:
    _DescribeJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeJobsPaginator(_DescribeJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeJobs.html#Mgn.Paginator.DescribeJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#describejobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeJobs.html#Mgn.Paginator.DescribeJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#describejobspaginator)
        """

if TYPE_CHECKING:
    _DescribeLaunchConfigurationTemplatesPaginatorBase = AioPaginator[
        DescribeLaunchConfigurationTemplatesResponseTypeDef
    ]
else:
    _DescribeLaunchConfigurationTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeLaunchConfigurationTemplatesPaginator(
    _DescribeLaunchConfigurationTemplatesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeLaunchConfigurationTemplates.html#Mgn.Paginator.DescribeLaunchConfigurationTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#describelaunchconfigurationtemplatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeLaunchConfigurationTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeLaunchConfigurationTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeLaunchConfigurationTemplates.html#Mgn.Paginator.DescribeLaunchConfigurationTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#describelaunchconfigurationtemplatespaginator)
        """

if TYPE_CHECKING:
    _DescribeReplicationConfigurationTemplatesPaginatorBase = AioPaginator[
        DescribeReplicationConfigurationTemplatesResponseTypeDef
    ]
else:
    _DescribeReplicationConfigurationTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeReplicationConfigurationTemplatesPaginator(
    _DescribeReplicationConfigurationTemplatesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeReplicationConfigurationTemplates.html#Mgn.Paginator.DescribeReplicationConfigurationTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#describereplicationconfigurationtemplatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeReplicationConfigurationTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeReplicationConfigurationTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeReplicationConfigurationTemplates.html#Mgn.Paginator.DescribeReplicationConfigurationTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#describereplicationconfigurationtemplatespaginator)
        """

if TYPE_CHECKING:
    _DescribeSourceServersPaginatorBase = AioPaginator[DescribeSourceServersResponseTypeDef]
else:
    _DescribeSourceServersPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeSourceServersPaginator(_DescribeSourceServersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeSourceServers.html#Mgn.Paginator.DescribeSourceServers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#describesourceserverspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSourceServersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeSourceServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeSourceServers.html#Mgn.Paginator.DescribeSourceServers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#describesourceserverspaginator)
        """

if TYPE_CHECKING:
    _DescribeVcenterClientsPaginatorBase = AioPaginator[DescribeVcenterClientsResponseTypeDef]
else:
    _DescribeVcenterClientsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeVcenterClientsPaginator(_DescribeVcenterClientsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeVcenterClients.html#Mgn.Paginator.DescribeVcenterClients)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#describevcenterclientspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeVcenterClientsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeVcenterClientsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/DescribeVcenterClients.html#Mgn.Paginator.DescribeVcenterClients.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#describevcenterclientspaginator)
        """

if TYPE_CHECKING:
    _ListApplicationsPaginatorBase = AioPaginator[ListApplicationsResponseTypeDef]
else:
    _ListApplicationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListApplicationsPaginator(_ListApplicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListApplications.html#Mgn.Paginator.ListApplications)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listapplicationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListApplications.html#Mgn.Paginator.ListApplications.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listapplicationspaginator)
        """

if TYPE_CHECKING:
    _ListConnectorsPaginatorBase = AioPaginator[ListConnectorsResponseTypeDef]
else:
    _ListConnectorsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListConnectorsPaginator(_ListConnectorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListConnectors.html#Mgn.Paginator.ListConnectors)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listconnectorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConnectorsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListConnectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListConnectors.html#Mgn.Paginator.ListConnectors.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listconnectorspaginator)
        """

if TYPE_CHECKING:
    _ListExportErrorsPaginatorBase = AioPaginator[ListExportErrorsResponseTypeDef]
else:
    _ListExportErrorsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListExportErrorsPaginator(_ListExportErrorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListExportErrors.html#Mgn.Paginator.ListExportErrors)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listexporterrorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExportErrorsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListExportErrorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListExportErrors.html#Mgn.Paginator.ListExportErrors.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listexporterrorspaginator)
        """

if TYPE_CHECKING:
    _ListExportsPaginatorBase = AioPaginator[ListExportsResponseTypeDef]
else:
    _ListExportsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListExportsPaginator(_ListExportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListExports.html#Mgn.Paginator.ListExports)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listexportspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExportsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListExportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListExports.html#Mgn.Paginator.ListExports.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listexportspaginator)
        """

if TYPE_CHECKING:
    _ListImportErrorsPaginatorBase = AioPaginator[ListImportErrorsResponseTypeDef]
else:
    _ListImportErrorsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListImportErrorsPaginator(_ListImportErrorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListImportErrors.html#Mgn.Paginator.ListImportErrors)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listimporterrorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImportErrorsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListImportErrorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListImportErrors.html#Mgn.Paginator.ListImportErrors.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listimporterrorspaginator)
        """

if TYPE_CHECKING:
    _ListImportFileEnrichmentsPaginatorBase = AioPaginator[ListImportFileEnrichmentsResponseTypeDef]
else:
    _ListImportFileEnrichmentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListImportFileEnrichmentsPaginator(_ListImportFileEnrichmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListImportFileEnrichments.html#Mgn.Paginator.ListImportFileEnrichments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listimportfileenrichmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImportFileEnrichmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListImportFileEnrichmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListImportFileEnrichments.html#Mgn.Paginator.ListImportFileEnrichments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listimportfileenrichmentspaginator)
        """

if TYPE_CHECKING:
    _ListImportsPaginatorBase = AioPaginator[ListImportsResponseTypeDef]
else:
    _ListImportsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListImportsPaginator(_ListImportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListImports.html#Mgn.Paginator.ListImports)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listimportspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImportsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListImportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListImports.html#Mgn.Paginator.ListImports.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listimportspaginator)
        """

if TYPE_CHECKING:
    _ListManagedAccountsPaginatorBase = AioPaginator[ListManagedAccountsResponseTypeDef]
else:
    _ListManagedAccountsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListManagedAccountsPaginator(_ListManagedAccountsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListManagedAccounts.html#Mgn.Paginator.ListManagedAccounts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listmanagedaccountspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListManagedAccountsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListManagedAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListManagedAccounts.html#Mgn.Paginator.ListManagedAccounts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listmanagedaccountspaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationAnalysesPaginatorBase = AioPaginator[
        ListNetworkMigrationAnalysesResponseTypeDef
    ]
else:
    _ListNetworkMigrationAnalysesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNetworkMigrationAnalysesPaginator(_ListNetworkMigrationAnalysesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationAnalyses.html#Mgn.Paginator.ListNetworkMigrationAnalyses)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationanalysespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationAnalysesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNetworkMigrationAnalysesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationAnalyses.html#Mgn.Paginator.ListNetworkMigrationAnalyses.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationanalysespaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationAnalysisResultsPaginatorBase = AioPaginator[
        ListNetworkMigrationAnalysisResultsResponseTypeDef
    ]
else:
    _ListNetworkMigrationAnalysisResultsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNetworkMigrationAnalysisResultsPaginator(
    _ListNetworkMigrationAnalysisResultsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationAnalysisResults.html#Mgn.Paginator.ListNetworkMigrationAnalysisResults)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationanalysisresultspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationAnalysisResultsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNetworkMigrationAnalysisResultsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationAnalysisResults.html#Mgn.Paginator.ListNetworkMigrationAnalysisResults.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationanalysisresultspaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationCodeGenerationSegmentsPaginatorBase = AioPaginator[
        ListNetworkMigrationCodeGenerationSegmentsResponseTypeDef
    ]
else:
    _ListNetworkMigrationCodeGenerationSegmentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNetworkMigrationCodeGenerationSegmentsPaginator(
    _ListNetworkMigrationCodeGenerationSegmentsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationCodeGenerationSegments.html#Mgn.Paginator.ListNetworkMigrationCodeGenerationSegments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationcodegenerationsegmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationCodeGenerationSegmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNetworkMigrationCodeGenerationSegmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationCodeGenerationSegments.html#Mgn.Paginator.ListNetworkMigrationCodeGenerationSegments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationcodegenerationsegmentspaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationCodeGenerationsPaginatorBase = AioPaginator[
        ListNetworkMigrationCodeGenerationsResponseTypeDef
    ]
else:
    _ListNetworkMigrationCodeGenerationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNetworkMigrationCodeGenerationsPaginator(
    _ListNetworkMigrationCodeGenerationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationCodeGenerations.html#Mgn.Paginator.ListNetworkMigrationCodeGenerations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationcodegenerationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationCodeGenerationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNetworkMigrationCodeGenerationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationCodeGenerations.html#Mgn.Paginator.ListNetworkMigrationCodeGenerations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationcodegenerationspaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationDefinitionsPaginatorBase = AioPaginator[
        ListNetworkMigrationDefinitionsResponseTypeDef
    ]
else:
    _ListNetworkMigrationDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNetworkMigrationDefinitionsPaginator(_ListNetworkMigrationDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationDefinitions.html#Mgn.Paginator.ListNetworkMigrationDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationdefinitionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNetworkMigrationDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationDefinitions.html#Mgn.Paginator.ListNetworkMigrationDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationdefinitionspaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationDeployedStacksPaginatorBase = AioPaginator[
        ListNetworkMigrationDeployedStacksResponseTypeDef
    ]
else:
    _ListNetworkMigrationDeployedStacksPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNetworkMigrationDeployedStacksPaginator(_ListNetworkMigrationDeployedStacksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationDeployedStacks.html#Mgn.Paginator.ListNetworkMigrationDeployedStacks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationdeployedstackspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationDeployedStacksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNetworkMigrationDeployedStacksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationDeployedStacks.html#Mgn.Paginator.ListNetworkMigrationDeployedStacks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationdeployedstackspaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationDeploymentsPaginatorBase = AioPaginator[
        ListNetworkMigrationDeployerJobResponseTypeDef
    ]
else:
    _ListNetworkMigrationDeploymentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNetworkMigrationDeploymentsPaginator(_ListNetworkMigrationDeploymentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationDeployments.html#Mgn.Paginator.ListNetworkMigrationDeployments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationdeploymentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationDeploymentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNetworkMigrationDeployerJobResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationDeployments.html#Mgn.Paginator.ListNetworkMigrationDeployments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationdeploymentspaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationExecutionsPaginatorBase = AioPaginator[
        ListNetworkMigrationExecutionsResponseTypeDef
    ]
else:
    _ListNetworkMigrationExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNetworkMigrationExecutionsPaginator(_ListNetworkMigrationExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationExecutions.html#Mgn.Paginator.ListNetworkMigrationExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationexecutionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNetworkMigrationExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationExecutions.html#Mgn.Paginator.ListNetworkMigrationExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationexecutionspaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationMapperSegmentConstructsPaginatorBase = AioPaginator[
        ListNetworkMigrationMapperSegmentConstructsResponseTypeDef
    ]
else:
    _ListNetworkMigrationMapperSegmentConstructsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNetworkMigrationMapperSegmentConstructsPaginator(
    _ListNetworkMigrationMapperSegmentConstructsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationMapperSegmentConstructs.html#Mgn.Paginator.ListNetworkMigrationMapperSegmentConstructs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationmappersegmentconstructspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationMapperSegmentConstructsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNetworkMigrationMapperSegmentConstructsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationMapperSegmentConstructs.html#Mgn.Paginator.ListNetworkMigrationMapperSegmentConstructs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationmappersegmentconstructspaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationMapperSegmentsPaginatorBase = AioPaginator[
        ListNetworkMigrationMapperSegmentsResponseTypeDef
    ]
else:
    _ListNetworkMigrationMapperSegmentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNetworkMigrationMapperSegmentsPaginator(_ListNetworkMigrationMapperSegmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationMapperSegments.html#Mgn.Paginator.ListNetworkMigrationMapperSegments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationmappersegmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationMapperSegmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNetworkMigrationMapperSegmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationMapperSegments.html#Mgn.Paginator.ListNetworkMigrationMapperSegments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationmappersegmentspaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationMappingUpdatesPaginatorBase = AioPaginator[
        ListNetworkMigrationMappingUpdatesResponseTypeDef
    ]
else:
    _ListNetworkMigrationMappingUpdatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNetworkMigrationMappingUpdatesPaginator(_ListNetworkMigrationMappingUpdatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationMappingUpdates.html#Mgn.Paginator.ListNetworkMigrationMappingUpdates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationmappingupdatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationMappingUpdatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNetworkMigrationMappingUpdatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationMappingUpdates.html#Mgn.Paginator.ListNetworkMigrationMappingUpdates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationmappingupdatespaginator)
        """

if TYPE_CHECKING:
    _ListNetworkMigrationMappingsPaginatorBase = AioPaginator[
        ListNetworkMigrationMappingsResponseTypeDef
    ]
else:
    _ListNetworkMigrationMappingsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNetworkMigrationMappingsPaginator(_ListNetworkMigrationMappingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationMappings.html#Mgn.Paginator.ListNetworkMigrationMappings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationmappingspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkMigrationMappingsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNetworkMigrationMappingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListNetworkMigrationMappings.html#Mgn.Paginator.ListNetworkMigrationMappings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listnetworkmigrationmappingspaginator)
        """

if TYPE_CHECKING:
    _ListSourceServerActionsPaginatorBase = AioPaginator[ListSourceServerActionsResponseTypeDef]
else:
    _ListSourceServerActionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSourceServerActionsPaginator(_ListSourceServerActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListSourceServerActions.html#Mgn.Paginator.ListSourceServerActions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listsourceserveractionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSourceServerActionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSourceServerActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListSourceServerActions.html#Mgn.Paginator.ListSourceServerActions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listsourceserveractionspaginator)
        """

if TYPE_CHECKING:
    _ListTemplateActionsPaginatorBase = AioPaginator[ListTemplateActionsResponseTypeDef]
else:
    _ListTemplateActionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTemplateActionsPaginator(_ListTemplateActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListTemplateActions.html#Mgn.Paginator.ListTemplateActions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listtemplateactionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTemplateActionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTemplateActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListTemplateActions.html#Mgn.Paginator.ListTemplateActions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listtemplateactionspaginator)
        """

if TYPE_CHECKING:
    _ListWavesPaginatorBase = AioPaginator[ListWavesResponseTypeDef]
else:
    _ListWavesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListWavesPaginator(_ListWavesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListWaves.html#Mgn.Paginator.ListWaves)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listwavespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWavesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWavesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn/paginator/ListWaves.html#Mgn.Paginator.ListWaves.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/paginators/#listwavespaginator)
        """
