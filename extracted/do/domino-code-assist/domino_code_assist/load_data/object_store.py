from typing import TYPE_CHECKING, List, Optional

import reacton
import reacton.ipyvuetify as v
import solara

from .. import util
from .state import ReactiveDataSource, load_data

if TYPE_CHECKING:
    # needed for python 3.6 support
    from domino_data.data_sources import ObjectStoreDatasource


@reacton.component
def Panel(ds: "ObjectStoreDatasource"):
    data_source: ReactiveDataSource = load_data.data_source
    data_source.use()

    def get_s3_keys(_cancel) -> Optional[List]:
        if ds and ds.datasource_type in util.supported_object_store_types():
            res = ds.list_objects()
            return res
        else:
            return None

    s3_keys_result: solara.Result[Optional[List]] = solara.hooks.use_thread(get_s3_keys, [ds])

    with v.Sheet() as main:
        if s3_keys_result.error:
            solara.Warning(str(s3_keys_result.error))
        elif s3_keys_result.value is not None:
            keys = [obj.key for obj in s3_keys_result.value]
            with v.List():

                def on_value(index):
                    data_source.set_database(keys[index] if index is not None else None)

                database = data_source.value.database
                with v.ListItemGroup(v_model=keys.index(database) if database else None, on_v_model=on_value).meta(ref=ds.datasource_type):
                    for key in keys:
                        with v.ListItem().key(key):
                            with v.ListItemIcon():
                                v.Icon(children=["mdi-file-document"])
                            with v.ListItemContent():
                                v.ListItemTitle(children=key)
        else:
            v.ProgressLinear(indeterminate=True).meta(ref="s3_keys_loading")

    return main
