
catalog_sources = "catalog/data-sources"

def __get_schema_base_url(base_url: str, schema_id: int):
    return f"{base_url}/{catalog_sources}/schema/{schema_id}"

def __get_table_base_url(base_url: str, table_id: int):
    return f"{base_url}/{catalog_sources}/table/{table_id}"

def __get_column_base_url(base_url: str, column_id: int):
    return f"{base_url}/{catalog_sources}/column/{column_id}"

def get_schema_scorecard_url(base_url: str, schema_id: int) -> str:
    return f"{__get_schema_base_url(base_url=base_url, schema_id=schema_id)}/scorecard"

def get_schema_metrics_url(base_url: str, schema_id: int):
    return f"{__get_schema_base_url(base_url=base_url, schema_id=schema_id)}/metrics"

def get_table_scorecard_url(base_url: str, table_id: int):
    return f"{__get_table_base_url(base_url=base_url, table_id=table_id)}/scorecard"

def get_table_metrics_url(base_url: str, table_id: int):
    return f"{__get_table_base_url(base_url=base_url, table_id=table_id)}/metrics"

def get_issues_by_table_url(base_url: str, table_id: int):
    return f"{__get_table_base_url(base_url=base_url, table_id=table_id)}/issues"

def get_column_scorecard_url(base_url: str, column_id: int):
    return f"{__get_column_base_url(base_url=base_url, column_id=column_id)}/scorecard"

def get_issues_by_column_url(base_url: str, column_id: int):
    return f"{__get_column_base_url(base_url=base_url, column_id=column_id)}/issues"

def get_issues_deep_url(base_url: str, issue_id: int):
    return f"{base_url}/issues/{issue_id}/metric"

def get_metric_deep_url(base_url: str, metric_id: int):
    return f"{base_url}/{catalog_sources}/metric/{metric_id}/chart"

def get_data_node_url(base_url: str, node_id: int):
    return f"{base_url}/lineage/{node_id}"