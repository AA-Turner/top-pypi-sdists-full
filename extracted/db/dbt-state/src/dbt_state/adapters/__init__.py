from __future__ import annotations

import typing as t

from dbt_state.adapters.base import BaseAdapterExtension
from dbt_state.adapters.bigquery import BigQueryAdapterExtension
from dbt_state.adapters.databricks import DatabricksAdapterExtension
from dbt_state.adapters.postgres import PostgresAdapterExtension
from dbt_state.adapters.redshift import RedshiftAdapterExtension
from dbt_state.adapters.snowflake import SnowflakeAdapterExtension
from dbt_state.errors import AdapterExtensionError

ADAPTER_EXTENSION_MAPPING = {
    "postgres": PostgresAdapterExtension,
    "bigquery": BigQueryAdapterExtension,
    "snowflake": SnowflakeAdapterExtension,
    "databricks": DatabricksAdapterExtension,
    "redshift": RedshiftAdapterExtension,
}


def create_adapter_extension(
    adapter: t.Any,
    threads: t.Optional[int] = None,
    cache_ttl_seconds: t.Optional[int] = None,
    **kwargs: t.Any,
) -> BaseAdapterExtension:
    if adapter.type() not in ADAPTER_EXTENSION_MAPPING:
        raise AdapterExtensionError(f"Extension not found for adapter type: {adapter.type()}")
    return ADAPTER_EXTENSION_MAPPING[adapter.type()](
        adapter=adapter, max_worker_threads=threads, cache_ttl_seconds=cache_ttl_seconds, **kwargs
    )
