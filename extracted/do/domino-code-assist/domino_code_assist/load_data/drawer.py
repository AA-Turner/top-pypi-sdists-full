from dataclasses import replace
from pathlib import Path
from typing import cast

import reacton
from solara.lab import Ref

from domino_code_assist import action
from domino_code_assist.assistant import drawer, mixpanel
from domino_code_assist.settings import settings

from .. import util
from ..serialize import dumps
from . import state
from .panel import LoadDataPanel


@reacton.component
def LoadDataDrawer(edit_action, set_code, open, edit, on_close, overwrite_warning=None):
    state.load_data.use()

    def reset_data():
        # reset state
        state.load_data.set(state.LoadData())

    reacton.use_memo(reset_data, [open])
    load_data_value = state.load_data.use_value()
    tab = load_data_value.tab

    def set_action(new_action):
        data_type = None
        data_source_type = None
        if isinstance(new_action, action.ActionOpen):
            if (new_action.filename or "").startswith(settings.domino_datasets_dir):
                data_type = "dataset"
            else:
                data_type = "file"
        elif isinstance(new_action, action.ActionDownloadDataSource):
            data_type = "data source"
            data_source_type = new_action.type_ or ""
        elif isinstance(new_action, action.ActionDemo):
            data_type = "demo"
        mixpanel.api.track_with_defaults(
            "inserted code",
            {
                "section": "load_data",
                "data_type": data_type,
                **({"data_source_type": data_source_type} if data_source_type else {}),
            },
        )
        set_code({"code": new_action.render_code("df") + f"\n{new_action.df_var_out}", "meta": dumps(new_action)})
        on_close()

    def on_file_name(filename: str, df_var: str, reactive: bool):
        set_action(action.ActionOpen(filename=filename, df_var_out=df_var, reactive=reactive))

    def on_apply():
        if tab == 0:
            action_ds = Ref(state.load_data.fields.data_source).get()
            action_ds = replace(action_ds, df_var_out=Ref(state.load_data.fields.df_out).value)
            set_action(action_ds)
        elif tab == 1 and load_data_value.dataset_file:
            on_file_name(load_data_value.dataset_file, load_data_value.df_out, load_data_value.reactive)
        elif tab == 2 and load_data_value.project_file:
            on_file_name(load_data_value.project_file, load_data_value.df_out, load_data_value.reactive)
        elif tab == 3 and load_data_value.upload_file:
            dest_name = util.copy_upload(load_data_value.upload_file["file_obj"], load_data_value.upload_file["name"])
            on_file_name(dest_name, load_data_value.df_out, load_data_value.reactive)
        elif tab == 4:
            set_action(action.ActionDemo(df_name=load_data_value.demo_df_name, df_var_out=load_data_value.df_out, reactive=load_data_value.reactive))

    def set_edit():
        if open and edit:
            if isinstance(edit_action, action.ActionOpen):
                filename = cast(action.ActionOpen, edit_action).filename
                if filename is None:
                    state.load_data.update(tab=0, df_out=edit_action.df_var_out)
                elif "domino_code_assist_data" in filename:
                    state.load_data.update(tab=3, df_out=edit_action.df_var_out)
                elif filename.startswith(settings.domino_datasets_dir):
                    state.load_data.update(tab=1, dataset_dir=Path(filename or "mypy").parent, df_out=edit_action.df_var_out, reactive=edit_action.reactive)
                else:
                    state.load_data.update(tab=2, project_dir=Path(filename).parent, df_out=edit_action.df_var_out, reactive=edit_action.reactive)
            elif isinstance(edit_action, action.ActionDownloadDataSource):
                state.load_data.update(tab=0, data_source=edit_action, df_out=edit_action.df_var_out)
            elif isinstance(edit_action, action.ActionDemo):
                state.load_data.update(tab=4, demo_df_name=edit_action.df_name, df_out=edit_action.df_var_out)

    reacton.use_memo(set_edit, [open, edit, edit_action])

    with drawer.RightDrawer(
        open=open,
        on_open=lambda v: on_close() if not v else None,
        title="Load data",
        edit=bool(edit),
        apply_disabled=not state.load_data.get().valid(),
        on_apply=on_apply,
        show_var_out=True,
        var_out=state.load_data.get().df_out,
        on_var_out=Ref(state.load_data.fields.df_out).set,
        warning_widget=overwrite_warning,
    ) as main:
        if open:
            LoadDataPanel()

    return main
