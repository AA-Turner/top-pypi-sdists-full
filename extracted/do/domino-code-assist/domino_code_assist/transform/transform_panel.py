import math
from typing import Optional, Tuple, Union, cast

import reacton
import reacton.ipyvuetify as v
import solara
from solara.components.code_highlight_css import CodeHighlightCss

import domino_code_assist.action as action
import domino_code_assist.actions_store as actions_store
from domino_code_assist import action_ui
from domino_code_assist.code import Code
from domino_code_assist.components import DataFrame
from domino_code_assist.transform import transform_action_ui
from domino_code_assist.util import DominoHeader


@reacton.component
def TransformPanel(state, dispatch, on_reset, on_save, breakpoints, assistant_mode=False):
    show_code, set_show_code = reacton.use_state(False)
    show_table, set_show_table = reacton.use_state(True)
    filter_like, set_filter_like = reacton.use_state(cast(Optional[Tuple[str, int]], None))

    def _get_for_index(colection, index):
        if index is None:
            return colection[-1]
        else:
            return colection[index] if 0 <= index < len(colection) else []

    def get_column_names(index):
        return _get_for_index(state.columns_for_action, index)

    def get_dtypes(index):
        return _get_for_index(state.dtypes_for_action, index)

    def reset():
        dispatch((actions_store.e_reset, None))
        on_reset()

    def on_code_view_event(event):
        if not event:
            return
        index = event["index"]
        if isinstance(state.actions[0], action.ActionUseNbLocals):
            index += 1
        name = event["name"]
        if name == "delete":
            dispatch((actions_store.e_delete_index, index))
        if name == "edit":
            dispatch((actions_store.e_edit_index, index))
        if name == "insert":
            dispatch((actions_store.e_insert_index, index))

    add_state, set_add_state = reacton.use_state(
        cast(Union[action.ActionFilter, action.ActionSelectColumns, action.ActionDropColumns, action.ActionGroupBy, action.ActionMerge], action.ActionFilter())
    )
    dialog_state, set_dialog_state = reacton.use_state(cast(action.Action, action.ActionFilter()))

    def on_edit_index():
        if state.index_of_edit_action is not None:
            set_dialog_state(state.actions[state.index_of_edit_action])
        if state.index_of_insert_action is not None:
            set_dialog_state(action.ActionFilter())

    reacton.use_memo(on_edit_index, [state.index_of_edit_action, state.index_of_insert_action])

    with v.Sheet() as main:
        if state.index_of_edit_action is not None:
            index = state.index_of_edit_action
            with v.Dialog(v_model=True, on_v_model=lambda open: dispatch((actions_store.e_edit_index, None)) if not open else None, width="50vw"):
                with v.Card().meta(ref="EditAction"):
                    DominoHeader(title="Edit transformation")
                    with v.CardText():
                        action_ui.EditAction(
                            columns=get_column_names(index - 1),
                            dtypes=get_dtypes(index - 1),
                            on_action=set_dialog_state,
                            action_obj=dialog_state,
                        ).meta(ref="EditAction")
                    with v.CardActions():
                        v.Spacer()
                        solara.Button("edit transformation", color="primary", on_click=lambda: dispatch((actions_store.e_edit_action, dialog_state)))
        if state.index_of_insert_action is not None:
            with v.Dialog(v_model=True, on_v_model=lambda open: dispatch((actions_store.e_insert_index, None)) if not open else None, width="50vw"):
                with v.Card().meta(ref="insert_panel"):
                    DominoHeader(title="Insert transformation")
                    with v.CardText():
                        transform_action_ui.TransformActionSelectPanel(
                            columns=get_column_names(state.index_of_insert_action),
                            dtypes=get_dtypes(state.index_of_insert_action),
                            action_=dialog_state,
                            on_action=set_dialog_state,
                            on_action_type=lambda t: set_dialog_state(t()),
                        )
                    with v.CardActions():
                        v.Spacer()
                        solara.Button("insert transformation", color="primary", on_click=lambda: dispatch((actions_store.e_insert_action, dialog_state)))
        if filter_like is not None:
            with v.Dialog(v_model=True, on_v_model=lambda open: set_filter_like(None) if not open else None, width="50vw"):
                with v.Card():
                    DominoHeader(title="Filter like")
                    with v.CardText():
                        column, index = filter_like
                        value = state.df_wrapper.df.iloc[index][column]
                        if math.isnan(value):
                            value = "NaN"
                        value = str(value)
                        action_val = action.ActionFilter(col=column, dtype=get_dtypes(None)[column], value=value, op="==")
                        transform_action_ui.FilterPanel(
                            columns=get_column_names(None),
                            dtypes=get_dtypes(None),
                            on_action=lambda action: [set_filter_like(None), dispatch((actions_store.e_insert_action, action))],
                            fill=action_val,
                        ).key(f"filter_like {action_val.__hash__()}")
        with v.Row(no_gutters=not breakpoints):
            with v.Col(sm=12, lg=5 if breakpoints else 12):
                with solara.Div():
                    if show_table and state.df_wrapper.has_df:
                        DataFrame(
                            state.df_wrapper.df,
                            on_drop_column=lambda column: dispatch((actions_store.e_insert_action, action.ActionDropColumns(columns=[column]))),
                            on_filter_value=lambda col, row: set_filter_like((col, row)),
                        ).meta(ref="DataTable").key("DataTable")

                    with solara.Div():

                        def on_action(action_):
                            dispatch((actions_store.e_insert_action, (idx, action_)))
                            set_add_state(action.ActionFilter())

                        idx = len(state.actions) - 1

                        if not state.error:
                            with solara.Div(style_="max-width: 600px; margin-left: auto; margin-right: auto;").meta(ref="insert_panel"):
                                transform_action_ui.TransformActionSelectPanel(
                                    columns=get_column_names(idx),
                                    dtypes=get_dtypes(idx),
                                    action_=add_state,
                                    on_action=set_add_state,
                                    on_action_type=lambda t: set_add_state(t()),
                                )
                                with solara.Div(style_="display: flex"):
                                    v.Spacer()
                                    solara.Button(
                                        outlined=True,
                                        color="primary",
                                        on_click=lambda: on_action(add_state),
                                        disabled=not add_state.is_valid(),
                                        children=["add transformation"],
                                    )
                    with v.CardActions(class_="ma-0"):
                        if not assistant_mode:
                            solara.Button(
                                icon_name="mdi-delete",
                                on_click=lambda: reset(),
                                icon=True,
                            )
                            solara.Button(
                                icon=True,
                                icon_name="mdi-content-copy",
                                disabled=True,
                            )
                            solara.Button(
                                icon_name="mdi-content-save",
                                on_click=on_save,
                                icon=True,
                            )
                        solara.Button(
                            icon_name="mdi-undo",
                            on_click=lambda: dispatch((actions_store.e_undo, None)),
                            icon=True,
                            disabled=not state.undo_stack,
                        ).meta(ref="btn_undo")
                        solara.Button(
                            icon_name="mdi-redo",
                            on_click=lambda: dispatch((actions_store.e_redo, None)),
                            icon=True,
                            disabled=len(state.redo_stack) == 0,
                        ).meta(ref="btn_redo")
                        v.Switch(label="Show table", v_model=show_table, on_v_model=set_show_table, class_="mx-4")
                        v.Switch(label="Show code", v_model=show_code, on_v_model=set_show_code, class_="mx-4")

                    if state.error:
                        v.Alert(
                            type="error",
                            text=True,
                            prominent=True,
                            icon="mdi-alert",
                            children=[f"{state.error[1]}"],
                        )
                    if show_code or state.error:
                        CodeHighlightCss()
                        Code(code_chunks=state.code_chunks, on_event=on_code_view_event, error=state.error, assistant_mode=assistant_mode)
    return main
