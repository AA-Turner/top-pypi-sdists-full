from dataclasses import replace
from typing import Optional, cast

import reacton
import reacton.ipyvuetify as v
import solara as sol

import domino_code_assist.actions_store as actions_store
import domino_code_assist.util
from domino_code_assist import action, data, util
from domino_code_assist.assistant import drawer, mixpanel
from domino_code_assist.df_select import DfSelect
from domino_code_assist.hooks import use_reducer_addon
from domino_code_assist.serialize import dumps

from .transform_panel import TransformPanel


@reacton.component
def TransformDrawer(action_state: Optional[actions_store.ActionsState], set_code, dfs, open, edit, on_close, on_load_own_data, overwrite_warning=None):
    state, set_state = sol.use_state_or_update(action_state if open and edit and action_state else actions_store.ActionsState(preview=True))
    dispatch = use_reducer_addon(actions_store.actions_reducer, set_state)
    df_var_name, set_df_var_name = reacton.use_state(
        cast(Optional[str], (state.actions and state.actions[0] and cast(action.ActionUseNbLocals, state.actions[0]).var_name) or None)
    )

    actions_store.use_execute_df(state, set_state, domino_code_assist.util.nb_locals)

    quick_start_created, set_quick_start_created = reacton.use_state(False)

    def set_transformations():
        if df_var_name == "df_quick_start" and quick_start_created:
            set_quick_start_created(False)
            new_action = action.ActionDemo(df_var_out="df_quick_start", df_name="palmerpenguins")
            set_code({"code": new_action.render_code("df") + f"\n{new_action.df_var_out}", "meta": dumps(new_action), "modifier": "insert-above"})
            set_quick_start_created(False)

        code_str = action.render_code(action.render_code_chunks(state.actions))
        set_code({"code": code_str, "meta": dumps(state)})
        mixpanel.api.track_with_defaults("inserted code", {"section": "transformations"})
        close()

    def close():
        on_close()
        if quick_start_created:
            set_quick_start_created(False)
            util.nb_locals.pop("df_quick_start", None)
        set_df_var_name(None)
        set_state(actions_store.ActionsState(preview=True))

    def on_df_var_change():
        if df_var_name:
            if df_var_name == "Load more data":
                close()
                on_load_own_data()
                return
            if df_var_name == "df_quick_start" and df_var_name not in dfs:
                # pre populate notebook scope
                set_quick_start_created(True)
                util.nb_locals["df_quick_start"] = data.palmerpenguins()

            set_state(
                lambda state: replace(
                    state,
                    actions=[action.ActionUseNbLocals(var_name=df_var_name, df_var_out=df_var_name or "mypy")]
                    + (state.actions[1:] if state.actions else []),  # type: ignore
                )
            )
            mixpanel.api.track_with_defaults(
                "interaction",
                {
                    "section": "transformations",
                    "type": "selected dataframe",
                },
            )

    reacton.use_memo(on_df_var_change, [df_var_name])

    extended_dfs = dfs
    if len(dfs) == 0:
        extended_dfs = ["df_quick_start"] + extended_dfs
    if not edit:
        extended_dfs = extended_dfs + [{"divider": True}, "Load more data"]

    def pre_select_df():
        if open and (df_var_name is None or df_var_name not in dfs):
            set_df_var_name(dfs[0] if dfs else "df_quick_start")

    reacton.use_memo(pre_select_df, [open, dfs])

    with drawer.RightDrawer(
        open=open,
        on_open=lambda v: close() if not v else None,
        title="Transformations",
        edit=bool(edit),
        on_apply=set_transformations,
        warning_widget=overwrite_warning,
    ) as main:
        should_select_var = not df_var_name and not (state.actions and edit)
        with sol.Div(class_="dca-transform-header", style_="margin-left: -24px; margin-right: -24px; margin-top: -4px; padding: 8px 80px;"):
            DfSelect(value=df_var_name, label="DataFrame", on_value=set_df_var_name, items=extended_dfs or [])
        with sol.Div(style_="margin-left: -24px; margin-right: -24px"):
            v.Divider()
        if not should_select_var:
            TransformPanel(state, dispatch, on_reset=lambda: None, on_save=lambda: None, breakpoints=False, assistant_mode=True).meta(ref="TransformPanel")
    return main
