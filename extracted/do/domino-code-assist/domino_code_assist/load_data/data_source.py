import reacton.ipyvuetify as v
import solara

from .. import domino_api, util
from . import object_store, snowflake_redshift
from .big_query import BigQueryPanel
from .state import load_data


@solara.component
def DataSourcePanel(
    columns,
    visible,
):
    load_data.use()
    data_source = load_data.data_source

    datasource_list_result: solara.Result = solara.use_thread(lambda _cancel: domino_api.get_domino_api().get_datasource_list() if visible else None, [visible])

    def get_ds(name):
        if not name:
            return None
        from typing import TYPE_CHECKING

        from domino_code_assist.util import in_dev_mode

        if TYPE_CHECKING:
            from domino.data_sources import DataSourceClient  # pragma: no cover
        else:
            if in_dev_mode():
                from domino_code_assist.domino_lab_mock import DataSourceClient
            else:
                from domino.data_sources import DataSourceClient  # pragma: no cover
        ds_ = DataSourceClient().get_datasource(name)
        data_source.set_type(ds_.datasource_type)
        return ds_

    ds_result: solara.Result = solara.use_thread(lambda: get_ds(data_source.value.name), [data_source.value.name])
    ds = ds_result.value

    def supported(ds_type):
        return ds_type in [*util.supported_object_store_types(), *snowflake_redshift.supported_types, "BigQueryConfig"]

    def text(e):
        return f'{e["name"]} - {e["dataSourceType"].replace("Config", "")}{" - [not yet supported]" if not supported(e["dataSourceType"]) else ""}'

    with solara.Div() as main:
        with v.Row():
            with v.Col():
                if datasource_list_result.error:
                    solara.Error(str(datasource_list_result.error))
                else:
                    items = datasource_list_result.value and [
                        {
                            "text": text(e),
                            "value": e["name"],
                            "disabled": not supported(e["dataSourceType"]),
                        }
                        for e in datasource_list_result.value
                    ]  # type: ignore
                    v.Select(
                        label="Data Source",
                        # TODO: bug in vuetify wrappers
                        items=items,
                        v_model=data_source.value.name,
                        on_v_model=data_source.set_name,
                    ).meta(ref="datasources")
        if data_source.value.name:
            if ds_result.error:
                error = ds_result.error
                error_msg = f"{type(error).__name__}: {str(error)}"
                if isinstance(error, KeyError):
                    error_msg = (
                        error_msg
                        + ". This may be due to an environment with an incompatible version of the Domino-API-client (v"
                        + f"{domino_api.get_domino_api().get_client_version()}) for this Domino version (v{domino_api.get_domino_api().get_domino_version()})."
                    )
                solara.Warning(error_msg)
            elif not ds or ds_result.state == solara.ResultState.RUNNING:
                v.ProgressLinear(indeterminate=True).meta(ref="tables_loading")
            elif ds.datasource_type in util.supported_object_store_types():
                object_store.Panel(ds)
            elif ds.datasource_type in snowflake_redshift.supported_types:
                snowflake_redshift.Panel(ds)
            elif ds.datasource_type == "BigQueryConfig":
                BigQueryPanel(ds=ds).key("bq" + data_source.value.name)  # type: ignore
            if data_source.value.sample:
                with solara.Div(class_="ml-4"):
                    solara.Warning("This table has too many rows. A sample of this table will be loaded.")

    return main
