from dataclasses import dataclass
from typing import List, Optional

import humanize
import reacton
import reacton.ipyvuetify as v
import solara as sol
from solara.components.sql_code import SqlCode
from solara.lab import Ref

from .state import ReactiveDataSource, load_data


@dataclass(frozen=True)
class SchemasResult:
    default_region: Optional[str]
    schemas: List[str]


regions = [
    "default",
    "us",
    "eu",
    "us-central1",
    "us-west4",
    "us-west2",
    "northamerica-northeast1",
    "us-east4",
    "us-west1",
    "us-west3",
    "southamerica-east1",
    "southamerica-west1",
    "us-east1",
    "northamerica-northeast2",
    "europe-west1",
    "europe-north1",
    "europe-west3",
    "europe-west2",
    "europe-southwest1",
    "europe-west8",
    "europe-west4",
    "europe-west9",
    "europe-central2",
    "europe-west6",
    "asia-south2",
    "asia-east2",
    "asia-southeast2",
    "australia-southeast2",
    "asia-south1",
    "asia-northeast2",
    "asia-northeast3",
    "asia-southeast1",
    "australia-southeast1",
    "asia-east1",
    "asia-northeast1",
]

columns = ["table_schema", "table_name", "column_name"]


@reacton.component
def BigQueryPanel(ds):
    data_source: ReactiveDataSource = load_data.data_source
    data_source.use()
    project_temp, set_project_temp = sol.use_state_or_update(ds.config.get("project") or data_source.value.project)

    def project():
        return ds.config.get("project") or data_source.value.project

    def get_schemas(_cancel):
        if not project():
            return None
        if data_source.value.region == "default":
            schemas_and_location_df = ds.query(f"SELECT location, schema_name FROM `{project()}`.INFORMATION_SCHEMA.SCHEMATA").to_pandas()
            default_region = schemas_and_location_df["location"].tolist()[0]
            schemas = schemas_and_location_df["schema_name"].unique().tolist()
            return SchemasResult(default_region, schemas)

        schema_df = ds.query(f"SELECT schema_name FROM `{project()}.region-{data_source.value.region}`.INFORMATION_SCHEMA.SCHEMATA").to_pandas()
        schemas = schema_df["schema_name"].unique().tolist()
        return SchemasResult(None, schemas)

    schemas_result: sol.Result = sol.hooks.use_thread(get_schemas, [data_source.value.region, project()])

    def select_single_schema():
        if schemas_result.value and len(schemas_result.value.schemas) == 1:
            value = schemas_result.value.schemas[0]
            if value != data_source.value.schema:
                data_source.set_schema(value)

    reacton.use_memo(select_single_schema, [schemas_result.value and schemas_result.value.schemas])

    def get_tables(_cancel):
        if not data_source.value.schema or not schemas_result.value:
            return

        q = f"SELECT table_id, row_count, type FROM `{project()}.{data_source.value.schema}`.__TABLES__"
        table_df = ds.query(q).to_pandas()

        return [
            {
                "text": f'{item["table_id"]} ({humanize.intword(item["row_count"] if item["type"] == 1 else "-")}) rows',
                "value": item["table_id"],
                "rows": item["row_count"],
            }
            for item in table_df.to_dict("records")
        ]

    tables_result: sol.Result = sol.hooks.use_thread(get_tables, [data_source.value.region, project(), data_source.value.schema, schemas_result.value])

    def get_column_spec(_cancel):
        if not data_source.value.schema or not schemas_result.value:
            return
        return (
            ds.query(
                f"SELECT table_name, column_name FROM `{project()}.{data_source.value.schema}`.INFORMATION_SCHEMA.COLUMNS order by table_name, ordinal_position;"  # noqa
            )
            .to_pandas()
            .groupby("table_name")["column_name"]
            .apply(list)
            .to_dict()
        )

    column_spec_result: sol.Result = sol.hooks.use_thread(get_column_spec, [data_source.value.schema, schemas_result.value])

    def check_sample():
        if data_source.value.use_query:
            data_source.set_sample(False)
            return

        if tables_result.value is None:
            return

        large_table = [item for item in tables_result.value if item["value"] == data_source.value.table and item["rows"] > 3000]
        data_source.set_sample(bool(large_table))

    reacton.use_memo(check_sample, [data_source.value.table, data_source.value.use_query])

    with v.Sheet() as main:
        with v.Row():
            with v.Col(style_="display: flex; align-items: center"):
                v.TextField(label="Project", v_model=project_temp, on_v_model=set_project_temp, disabled=bool(ds.config.get("project"))).meta(ref="project")
                if not ds.config.get("project") and project() != project_temp:
                    sol.Button(
                        "apply",
                        on_click=lambda: data_source.set_project(project_temp),
                        icon_name="mdi-check",
                        color="primary",
                        small=True,
                        class_="ml-2",
                        outlined=True,
                    ).meta(ref="apply")
            with v.Col():
                v.Select(label="region", items=regions, v_model=data_source.value.region, on_v_model=data_source.set_region).meta(ref="region")
            with v.Col():
                if schemas_result.value and schemas_result.value.schemas:
                    v.Select(label="Dataset", items=schemas_result.value.schemas, v_model=data_source.value.schema, on_v_model=data_source.set_schema).key(
                        "schema"
                    ).meta(ref="schema")
        if tables_result.value:
            with v.Row():
                with v.Col():
                    v.Switch(label="Use query").connect(Ref(data_source.fields.use_query)).meta(ref="use_query")
            with v.Row():
                with v.Col():
                    if data_source.value.use_query:
                        if column_spec_result.value:
                            SqlCode(tables=column_spec_result.value, query=data_source.value.query or "", on_query=Ref(data_source.fields.query).set).meta(
                                ref="query_editor"
                            )
                    else:
                        v.Select(label="Table", items=tables_result.value).connect(Ref(data_source.fields.table)).key("table").meta(ref="table")

        if sol.ResultState.RUNNING in [schemas_result.state, tables_result.state, column_spec_result.state]:
            v.ProgressLinear(indeterminate=True).key("progress")
        if sol.ResultState.ERROR in [schemas_result.state, tables_result.state, column_spec_result.state]:
            sol.Warning(repr(schemas_result.error or tables_result.error or column_spec_result.error))

    return main
