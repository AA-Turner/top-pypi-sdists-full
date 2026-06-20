"""
Main interface for glue service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glue/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_glue import (
        Client,
        DescribeEntityPaginator,
        GetClassifiersPaginator,
        GetConnectionsPaginator,
        GetCrawlerMetricsPaginator,
        GetCrawlersPaginator,
        GetDatabasesPaginator,
        GetDevEndpointsPaginator,
        GetJobRunsPaginator,
        GetJobsPaginator,
        GetPartitionIndexesPaginator,
        GetPartitionsPaginator,
        GetResourcePoliciesPaginator,
        GetSecurityConfigurationsPaginator,
        GetTableVersionsPaginator,
        GetTablesPaginator,
        GetTriggersPaginator,
        GetUserDefinedFunctionsPaginator,
        GetWorkflowRunsPaginator,
        GlueClient,
        ListAssetTypesPaginator,
        ListBlueprintsPaginator,
        ListConnectionTypesPaginator,
        ListEntitiesPaginator,
        ListFormTypesPaginator,
        ListGlossariesPaginator,
        ListGlossaryTermsPaginator,
        ListIterableFormsPaginator,
        ListJobsPaginator,
        ListMaterializedViewRefreshTaskRunsPaginator,
        ListRegistriesPaginator,
        ListSchemaVersionsPaginator,
        ListSchemasPaginator,
        ListTableOptimizerRunsPaginator,
        ListTriggersPaginator,
        ListUsageProfilesPaginator,
        ListWorkflowsPaginator,
        SearchAssetsPaginator,
    )

    session = Session()
    client: GlueClient = session.client("glue")

    describe_entity_paginator: DescribeEntityPaginator = client.get_paginator("describe_entity")
    get_classifiers_paginator: GetClassifiersPaginator = client.get_paginator("get_classifiers")
    get_connections_paginator: GetConnectionsPaginator = client.get_paginator("get_connections")
    get_crawler_metrics_paginator: GetCrawlerMetricsPaginator = client.get_paginator("get_crawler_metrics")
    get_crawlers_paginator: GetCrawlersPaginator = client.get_paginator("get_crawlers")
    get_databases_paginator: GetDatabasesPaginator = client.get_paginator("get_databases")
    get_dev_endpoints_paginator: GetDevEndpointsPaginator = client.get_paginator("get_dev_endpoints")
    get_job_runs_paginator: GetJobRunsPaginator = client.get_paginator("get_job_runs")
    get_jobs_paginator: GetJobsPaginator = client.get_paginator("get_jobs")
    get_partition_indexes_paginator: GetPartitionIndexesPaginator = client.get_paginator("get_partition_indexes")
    get_partitions_paginator: GetPartitionsPaginator = client.get_paginator("get_partitions")
    get_resource_policies_paginator: GetResourcePoliciesPaginator = client.get_paginator("get_resource_policies")
    get_security_configurations_paginator: GetSecurityConfigurationsPaginator = client.get_paginator("get_security_configurations")
    get_table_versions_paginator: GetTableVersionsPaginator = client.get_paginator("get_table_versions")
    get_tables_paginator: GetTablesPaginator = client.get_paginator("get_tables")
    get_triggers_paginator: GetTriggersPaginator = client.get_paginator("get_triggers")
    get_user_defined_functions_paginator: GetUserDefinedFunctionsPaginator = client.get_paginator("get_user_defined_functions")
    get_workflow_runs_paginator: GetWorkflowRunsPaginator = client.get_paginator("get_workflow_runs")
    list_asset_types_paginator: ListAssetTypesPaginator = client.get_paginator("list_asset_types")
    list_blueprints_paginator: ListBlueprintsPaginator = client.get_paginator("list_blueprints")
    list_connection_types_paginator: ListConnectionTypesPaginator = client.get_paginator("list_connection_types")
    list_entities_paginator: ListEntitiesPaginator = client.get_paginator("list_entities")
    list_form_types_paginator: ListFormTypesPaginator = client.get_paginator("list_form_types")
    list_glossaries_paginator: ListGlossariesPaginator = client.get_paginator("list_glossaries")
    list_glossary_terms_paginator: ListGlossaryTermsPaginator = client.get_paginator("list_glossary_terms")
    list_iterable_forms_paginator: ListIterableFormsPaginator = client.get_paginator("list_iterable_forms")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_materialized_view_refresh_task_runs_paginator: ListMaterializedViewRefreshTaskRunsPaginator = client.get_paginator("list_materialized_view_refresh_task_runs")
    list_registries_paginator: ListRegistriesPaginator = client.get_paginator("list_registries")
    list_schema_versions_paginator: ListSchemaVersionsPaginator = client.get_paginator("list_schema_versions")
    list_schemas_paginator: ListSchemasPaginator = client.get_paginator("list_schemas")
    list_table_optimizer_runs_paginator: ListTableOptimizerRunsPaginator = client.get_paginator("list_table_optimizer_runs")
    list_triggers_paginator: ListTriggersPaginator = client.get_paginator("list_triggers")
    list_usage_profiles_paginator: ListUsageProfilesPaginator = client.get_paginator("list_usage_profiles")
    list_workflows_paginator: ListWorkflowsPaginator = client.get_paginator("list_workflows")
    search_assets_paginator: SearchAssetsPaginator = client.get_paginator("search_assets")
    ```
"""

from .client import GlueClient
from .paginator import (
    DescribeEntityPaginator,
    GetClassifiersPaginator,
    GetConnectionsPaginator,
    GetCrawlerMetricsPaginator,
    GetCrawlersPaginator,
    GetDatabasesPaginator,
    GetDevEndpointsPaginator,
    GetJobRunsPaginator,
    GetJobsPaginator,
    GetPartitionIndexesPaginator,
    GetPartitionsPaginator,
    GetResourcePoliciesPaginator,
    GetSecurityConfigurationsPaginator,
    GetTablesPaginator,
    GetTableVersionsPaginator,
    GetTriggersPaginator,
    GetUserDefinedFunctionsPaginator,
    GetWorkflowRunsPaginator,
    ListAssetTypesPaginator,
    ListBlueprintsPaginator,
    ListConnectionTypesPaginator,
    ListEntitiesPaginator,
    ListFormTypesPaginator,
    ListGlossariesPaginator,
    ListGlossaryTermsPaginator,
    ListIterableFormsPaginator,
    ListJobsPaginator,
    ListMaterializedViewRefreshTaskRunsPaginator,
    ListRegistriesPaginator,
    ListSchemasPaginator,
    ListSchemaVersionsPaginator,
    ListTableOptimizerRunsPaginator,
    ListTriggersPaginator,
    ListUsageProfilesPaginator,
    ListWorkflowsPaginator,
    SearchAssetsPaginator,
)

Client = GlueClient

__all__ = (
    "Client",
    "DescribeEntityPaginator",
    "GetClassifiersPaginator",
    "GetConnectionsPaginator",
    "GetCrawlerMetricsPaginator",
    "GetCrawlersPaginator",
    "GetDatabasesPaginator",
    "GetDevEndpointsPaginator",
    "GetJobRunsPaginator",
    "GetJobsPaginator",
    "GetPartitionIndexesPaginator",
    "GetPartitionsPaginator",
    "GetResourcePoliciesPaginator",
    "GetSecurityConfigurationsPaginator",
    "GetTableVersionsPaginator",
    "GetTablesPaginator",
    "GetTriggersPaginator",
    "GetUserDefinedFunctionsPaginator",
    "GetWorkflowRunsPaginator",
    "GlueClient",
    "ListAssetTypesPaginator",
    "ListBlueprintsPaginator",
    "ListConnectionTypesPaginator",
    "ListEntitiesPaginator",
    "ListFormTypesPaginator",
    "ListGlossariesPaginator",
    "ListGlossaryTermsPaginator",
    "ListIterableFormsPaginator",
    "ListJobsPaginator",
    "ListMaterializedViewRefreshTaskRunsPaginator",
    "ListRegistriesPaginator",
    "ListSchemaVersionsPaginator",
    "ListSchemasPaginator",
    "ListTableOptimizerRunsPaginator",
    "ListTriggersPaginator",
    "ListUsageProfilesPaginator",
    "ListWorkflowsPaginator",
    "SearchAssetsPaginator",
)
