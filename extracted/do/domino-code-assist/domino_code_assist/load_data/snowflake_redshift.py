import textwrap

import humanize
import pandas as pd
import reacton
import reacton.ipyvuetify as v
import solara
from solara.lab import Ref

from ..domino_api import get_domino_api
from .state import ReactiveDataSource, load_data

supported_types = ["RedshiftConfig", "SnowflakeConfig"]


query_snowflake_meta = """select
                    TABLE_CATALOG as "database_name",
                    TABLE_SCHEMA as "schema_name",
                    TABLE_NAME as "name",
                    IFNULL(ROW_COUNT, -1) as "rows"
                    from INFORMATION_SCHEMA.TABLES
                    where TABLE_SCHEMA != 'INFORMATION_SCHEMA'"""


@reacton.component
def Panel(ds):
    data_source: ReactiveDataSource = load_data.data_source
    data_source.use()

    def get_tables(_cancel):
        if not ds:
            return None
        if ds.datasource_type == "SnowflakeConfig":
            if ds.config.get("database"):
                return ds.query(query_snowflake_meta).to_pandas()
            else:
                df_tables = ds.query("show tables").to_pandas()
                views = ds.query("show views").to_pandas()
                views = views.loc[views["schema_name"] != "INFORMATION_SCHEMA"]
                views = views.loc[views["database_name"] != "SNOWFLAKE"]
                views["rows"] = -1
                views["bytes"] = -1
                return pd.concat([df_tables, views])
        if ds.datasource_type == "RedshiftConfig":
            res = ds.query(
                textwrap.dedent(
                    """\
                select tab.table_schema as schema_name,
                       tab.table_name as name,
                       class.reltuples as rows
                from svv_tables tab
                         join pg_class class
                              on tab.table_name = class.relname
                where tab.table_type = 'BASE TABLE'
                  and tab.table_schema not in('pg_catalog','information_schema')
                  and class.reltuples > 1
                """
                )
            )
            return res.to_pandas()
        raise RuntimeError(f"Unknown datasource: {ds.datasource_type}")

    tables_result: solara.Result = solara.hooks.use_thread(get_tables, [ds])

    tables = tables_result.value

    database_items = []
    schema_items = []
    table_items = []
    names = None
    rows = None

    if tables is not None and ds is not None:
        database_items = tables["database_name"].unique().tolist() if "database_name" in tables else [ds.config.get("database")]
        database = data_source.value.database
        schema = data_source.value.schema
        if database:
            if ds.datasource_type == "SnowflakeConfig":
                schema_items = tables.loc[tables["database_name"] == database]["schema_name"].unique().tolist()
            else:
                schema_items = tables["schema_name"].unique().tolist()
            if schema:
                if ds.datasource_type == "SnowflakeConfig":
                    table_rows = tables[(tables["database_name"] == database) & (tables["schema_name"] == schema)]
                else:
                    table_rows = tables.loc[tables["schema_name"] == schema]
                names = table_rows["name"].tolist()
                rows = table_rows["rows"].tolist()

                def row_str(r):
                    return f"({humanize.intword(r)} rows)" if r >= 0 else " (view)"

                table_items = [{"value": n, "text": f"{n} {row_str(r)}"} for n, r in zip(names, rows)]

    def get_schema_spec(_cancel):
        database = data_source.value.database
        schema = data_source.value.schema
        if not (ds and database and schema):
            return None
        elif ds.datasource_type == "RedshiftConfig":
            return (
                ds.query(
                    textwrap.dedent(
                        f"""\
                    select table_name, column_name
                    from information_schema.columns
                    where table_schema = '{schema}'
                    and table_catalog = '{database}'
                    order by table_name, ordinal_position
                    """
                    )
                )
                .to_pandas()
                .groupby("table_name")["column_name"]
                .apply(list)
                .to_dict()
            )
        elif ds.datasource_type == "SnowflakeConfig":
            return ds.query(f"SHOW COLUMNS IN SCHEMA {database}.{schema}").to_pandas().groupby("table_name")["column_name"].apply(list).to_dict()

    spec_result: solara.Result = solara.hooks.use_thread(get_schema_spec, [ds and ds.datasource_type, data_source.value.database, data_source.value.schema])

    def pre_select_database():
        if len(database_items) == 1 and database_items[0] != data_source.value.database:
            data_source.set_database(database_items[0])

    solara.use_memo(pre_select_database, [database_items])

    def pre_selelect_schema():
        if len(schema_items) == 1 and schema_items[0] != data_source.value.schema:
            data_source.set_schema(schema_items[0])

    solara.use_memo(pre_selelect_schema, [schema_items])

    def check_sample():
        if data_source.value.use_query:
            data_source.set_sample(False)
            return

        if tables is None:
            return

        name_index = not data_source.value.use_query and names and data_source.value.table and names.index(data_source.value.table)
        nr_rows = name_index is not None and rows and rows[name_index]

        data_source.set_sample(nr_rows and nr_rows > 3000)

    solara.use_memo(check_sample, [data_source.value.table, data_source.value.use_query])

    with v.Sheet() as main:
        if tables_result.error:
            error = tables_result.error
            error_msg = f"{type(error).__name__}: {str(error)}"
            if isinstance(error, KeyError):
                error_msg = (
                    error_msg
                    + ". This may be due to an environment with an incompatible version of the Domino-API-client (v"
                    + f"{get_domino_api().get_client_version()}) for this Domino version (v{get_domino_api().get_domino_version()})."
                )
            solara.Warning(error_msg)
        elif not ds or tables_result.state == solara.ResultState.RUNNING:
            v.ProgressLinear(indeterminate=True).meta(ref="tables_loading")
        else:
            with v.Row():
                with v.Col():
                    v.Select(label="Database", items=database_items, v_model=data_source.value.database, on_v_model=data_source.set_database).meta(
                        ref="database"
                    )
                with v.Col():
                    v.Select(label="Schema", items=schema_items, v_model=data_source.value.schema, on_v_model=data_source.set_schema).meta(ref="schema")
            with v.Row():
                with v.Col():
                    v.Switch(label="Use query").connect(Ref(data_source.fields.use_query)).meta(ref="use_query")
            with v.Row():
                if data_source.value.use_query:
                    with v.Col():
                        solara.SqlCode(query=data_source.value.query or "", tables=spec_result.value or {}, on_query=Ref(data_source.fields.query).set).meta(
                            ref="query_editor"
                        )
                else:
                    with v.Col():
                        v.Select(label="Table", items=table_items).connect(Ref(data_source.fields.table))

    return main
