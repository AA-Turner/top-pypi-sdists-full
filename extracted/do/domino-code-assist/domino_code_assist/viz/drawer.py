from typing import Optional, cast

import pandas as pd
import reacton
import solara
from solara.lab import Ref

import domino_code_assist
from domino_code_assist import action, data, util
from domino_code_assist.assistant import drawer, mixpanel
from domino_code_assist.util import generate_var_name

from ..df_select import DfSelect
from ..serialize import dumps
from . import plot_builder
from .state import EqWrapper, Viz, viz


@solara.component
def VisualizationDrawer(edit_data: Optional[Viz], set_code, dfs, open, edit, on_close, on_load_own_data, overwrite_warning=None):
    viz.use()
    df_ref = solara.use_ref(cast(pd.DataFrame, None))
    quick_start_created, set_quick_start_created = reacton.use_state(False)

    def set_df_var_name(value):
        if value == "Load more data":
            close()
            on_load_own_data()
            return
        if value == "df_quick_start" and value not in dfs:
            # pre populate notebook scope
            set_quick_start_created(True)
            util.nb_locals["df_quick_start"] = data.palmerpenguins()

        mixpanel.api.track_with_defaults(
            "interaction",
            {
                "section": "visualizations",
                "type": "selected dataframe",
            },
        )
        Ref(viz.fields.df_var_name).value = value

    def set_visualization():
        if viz.value.df_var_name == "df_quick_start" and quick_start_created:
            set_quick_start_created(False)
            new_action = action.ActionDemo(df_var_out="df_quick_start", df_name="palmerpenguins")
            set_code({"code": new_action.render_code("df") + f"\n{new_action.df_var_out}", "meta": dumps(new_action), "modifier": "insert-above"})
            set_quick_start_created(False)

        code_str = plot_builder.generate_code(viz.value)
        set_code({"code": code_str, "meta": dumps(viz.value)})
        mixpanel.api.track_with_defaults("inserted code", {"section": "visualizations"})
        close()

    def close():
        on_close()
        if quick_start_created:
            set_quick_start_created(False)
            util.nb_locals.pop("df_quick_start", None)

    def init_plot_state():
        if open and edit_data and edit:
            viz.set(edit_data)
        else:
            viz.set(Viz(plot_var_name=generate_var_name("var")))

    solara.use_memo(init_plot_state, [open])

    def handle_var_name():
        df_ref.current = (
            EqWrapper(domino_code_assist.util.nb_locals[viz.value.df_var_name]) if viz.value.df_var_name and viz.value.df_var_name != "Load more data" else None
        )

    solara.use_memo(handle_var_name, [viz.value.df_var_name])
    plot_var_name = viz.value.plot_var_name

    extended_dfs = dfs
    if len(dfs) == 0:
        extended_dfs = ["df_quick_start"] + extended_dfs
    if not edit:
        extended_dfs = extended_dfs + [{"divider": True}, "Load more data"]

    def pre_select_df():
        if open and viz.value.df_var_name is None:
            set_df_var_name(dfs[0] if dfs else "df_quick_start")

    reacton.use_memo(pre_select_df, [open])

    def pre_select_plot_vars():
        if open and viz.value.df_var_name == "df_quick_start" and viz.value.plot_type is None:
            Ref(viz.fields.plot_type).set("scatter")
            Ref(viz.fields.col_args).set(
                {
                    "x": "bill_depth_mm",
                    "y": "bill_length_mm",
                    "color": "species",
                }
            )

    reacton.use_memo(pre_select_plot_vars, [viz.value.df_var_name, open])

    with drawer.RightDrawer(
        open=open,
        on_open=lambda v: close() if not v else None,
        title="Visualization",
        edit=bool(edit),
        on_apply=set_visualization,
        apply_disabled=not viz.value.df_var_name,
        show_var_out=True,
        var_out=plot_var_name or "",
        on_var_out=Ref(viz.fields.plot_var_name).set,
        width="1024px",
        warning_widget=overwrite_warning,
    ) as main:
        DfSelect(value=viz.value.df_var_name, label="DataFrame", on_value=set_df_var_name, items=extended_dfs or [])
        if viz.value.df_var_name:
            plot_builder.PlotBuilder(
                df_ref.current,
                df_ref.current and df_ref.current.get().columns.tolist(),
                min_height=None,
            )
    return main
