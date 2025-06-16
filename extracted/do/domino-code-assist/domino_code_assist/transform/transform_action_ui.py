from dataclasses import replace
from typing import Callable, List, Type, Union, cast

import pandas as pd
import reacton
import reacton.ipyvuetify as v
import solara as sol
from solara import Tooltip

from domino_code_assist import action
from domino_code_assist.util import is_valid_variable_name

from .. import util


@reacton.component
def FilterPanel(columns, dtypes, on_action, fill):
    state, set_state = reacton.use_state(fill)

    def make_action():
        on_action(state)

    with sol.Div().meta(ref="FilterPanel") as panel:
        with sol.Div():
            FilterPanelView(columns, dtypes, state, set_state)

        with v.CardActions():
            v.Spacer()
            sol.Button(
                "apply",
                color="primary",
                icon_name="mdi-check",
                disabled=not state.is_valid(),
                on_click=make_action,
            )
    return panel


def escape_special_chars(s):
    return s.replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r") if s else s


def unescape_special_chars(s):
    return s.replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r") if s else s


@reacton.component
def FilterPanelView(columns, dtypes, action_: action.ActionFilter, on_filter_action):
    with sol.Div().meta(ref="FilterPanel") as main:
        with v.Row():
            with v.Col():
                v.Select(label="Column", v_model=action_.col, items=columns, on_v_model=lambda v: on_filter_action(replace(action_, col=v, dtype=dtypes[v])))
            with v.Col():
                v.Select(
                    label="Operator",
                    v_model=action_.op,
                    items=["<", ">", "<=", ">=", "!=", "=="],
                    on_v_model=lambda v: on_filter_action(replace(action_, op=v)),
                )
            with v.Col():

                def is_float_or_nan(value):
                    if value.lower() == "nan":
                        return True
                    try:
                        float(value)
                        return True
                    except ValueError:
                        return False

                v.TextField(
                    label="Value",
                    v_model=escape_special_chars(action_.value),
                    on_v_model=lambda v: on_filter_action(replace(action_, value=unescape_special_chars(v))),
                    error_messages=['Invalid value, consider using "as string"']
                    if action_.value and not action_.is_string and not is_float_or_nan(action_.value)
                    else None,
                )
            with v.Col():
                v.Switch(label="as string", v_model=action_.is_string, on_v_model=lambda v: on_filter_action(replace(action_, is_string=v)))
        with v.Row():
            with v.Col(sm=4):
                valid_variable_name = is_valid_variable_name(action_.df_var_out)
                v.TextField(
                    label="New dataframe name",
                    v_model=action_.df_var_out,
                    on_v_model=lambda v: on_filter_action(replace(action_, df_var_out=v)),
                    error_messages=[] if valid_variable_name else ["Invalid variable name"],
                )

    return main


@reacton.component
def SelectColumnsPanelView(columns, dtypes, action_: Union[action.ActionSelectColumns, action.ActionDropColumns], on_columns_action):
    with sol.Div().meta(ref="SelectColumnsPanel") as main:
        with v.Row():
            with v.Col():
                v.Select(
                    label="Columns",
                    v_model=action_.columns,
                    items=columns,
                    on_v_model=lambda v: on_columns_action(replace(action_, columns=v)),
                    multiple=True,
                    deletable_chips=True,
                )
        with v.Row():
            with v.Col():
                valid_variable_name = is_valid_variable_name(action_.df_var_out)
                v.TextField(
                    label="New dataframe name",
                    v_model=action_.df_var_out,
                    on_v_model=lambda v: on_columns_action(replace(action_, df_var_out=v)),
                    error_messages=[] if valid_variable_name else ["Invalid variable name"],
                )
    return main


@reacton.component
def GroupByPanelView(columns, dtypes, action_: action.ActionGroupBy, on_group_by_action):
    with sol.Div().meta(ref="GroupByPanel") as main:
        with v.Row():
            with v.Col(sm=4):
                v.Select(
                    label="Columns to group by",
                    v_model=action_.columns,
                    items=columns,
                    on_v_model=lambda v: on_group_by_action(replace(action_, columns=v)),
                    multiple=True,
                    deletable_chips=True,
                )
            with v.Col(sm=8, class_="pa-0"):
                new_aggs = []
                i = 0
                agg_names = ["size", "sum", "mean", "min", "max"]
                # filter out empty entries
                aggs = action_.aggregations and [k for k in action_.aggregations if not all(el is None for el in k)]
                for col, agg in aggs or []:
                    with v.Row():
                        with v.Col():
                            colnew = sol.ui_dropdown("Column to aggregate", col, columns, key=f"col_{i}")
                        with v.Col():
                            aggnew = sol.ui_dropdown("Aggregator", agg, agg_names, key=f"agg_{i}")
                            new_aggs.append((colnew, aggnew))
                            i += -1

                with v.Row():
                    with v.Col():
                        col = sol.ui_dropdown("Column to aggregate", None, columns, key=f"col_{i}")
                    with v.Col():
                        agg_name = sol.ui_dropdown("Aggregator", None, agg_names, key=f"agg_{i}")
                        if col and agg_name:
                            new_aggs.append((col, agg_name))

                on_group_by_action(replace(action_, aggregations=new_aggs))
        with v.Row():
            with v.Col(sm=4):
                valid_variable_name = is_valid_variable_name(action_.df_var_out)
                v.TextField(
                    label="New dataframe name",
                    v_model=action_.df_var_out,
                    on_v_model=lambda v: on_group_by_action(replace(action_, df_var_out=v)),
                    error_messages=[] if valid_variable_name else ["Invalid variable name"],
                )

    return main


@reacton.component
def MergePanelView(columns, dtypes, action_: action.ActionMerge, on_merge_action):
    dfs = util.get_vars(lambda v: isinstance(v, pd.DataFrame))

    common_cols, set_common_cols = sol.use_state(cast(List[str], []))

    def get_common_cols():
        if not action_.var_name_other:
            return
        cols = util.nb_locals[action_.var_name_other].columns.tolist()
        common = list(set(columns).intersection(set(cols)))

        mapping = {k: v for k, v in action_.mapping.items() if k is not None and v is not None}
        missing_mappings = [k for k in mapping.keys() if k not in columns] + [v for v in mapping.values() if v not in cols]
        if not mapping or missing_mappings:
            on_merge_action(replace(action_, auto=bool(common), mapping={None: None}))
        set_common_cols(common)

    sol.use_effect(get_common_cols, [columns, action_.var_name_other])

    def handle_empty(changed):
        incomplete = [k for k, v in changed.items() if k is None or v is None]
        if not incomplete:
            return {**changed, None: None}
        return changed

    def to_item(df_name):
        cols = util.nb_locals[df_name].columns.tolist()
        matching_cols = ", ".join(set(columns).intersection(set(cols)))
        return {"text": f"{df_name} [{matching_cols}]", "value": df_name}

    items = [to_item(df) for df in dfs]

    def update_key(new, old):
        changed = {new if k == old else k: v for k, v in action_.mapping.items()}
        on_merge_action(replace(action_, mapping=handle_empty(changed)))

    def update_value(new, key):
        changed = action_.mapping.copy()
        changed[key] = new
        on_merge_action(replace(action_, mapping=handle_empty(changed)))

    def remove(key):
        changed = action_.mapping.copy()
        del changed[key]
        on_merge_action(replace(action_, mapping=handle_empty(changed)))

    how_options = [None, "left", "right", "outer"]

    with v.Sheet():
        v.Select(
            label="Dataframe to join/merge",
            items=items,
            v_model=action_.var_name_other,
            on_v_model=lambda v: on_merge_action(replace(action_, var_name_other=v)),
        )

        if action_.var_name_other:
            v.Switch(v_model=action_.on_index, on_v_model=lambda v: on_merge_action(replace(action_, on_index=v)), label="Join on index")
            if not action_.on_index:
                with v.BtnToggle(
                    v_model=how_options.index(action_.how), on_v_model=lambda v: on_merge_action(replace(action_, how=how_options[v])), mandatory=True
                ):
                    with Tooltip("Inner (default)"):
                        sol.Button(icon_name="mdi-set-center")
                    with Tooltip("Left outer"):
                        sol.Button(icon_name="mdi-set-left-center")
                    with Tooltip("Right outer"):
                        sol.Button(icon_name="mdi-set-center-right")
                    with Tooltip("Full outer"):
                        sol.Button(icon_name="mdi-set-all")

                v.Switch(
                    v_model=action_.auto,
                    on_v_model=lambda v: on_merge_action(replace(action_, auto=v)),
                    label="Join on all common columns",
                    disabled=not common_cols,
                )
                if action_.auto:
                    v.Html(tag="span", children=["Join on column(s): "])
                    v.Html(tag="span", children=[", ".join(common_cols)])
                else:
                    left_cols = [c for c in columns if c not in action_.mapping]
                    right_cols = [c for c in util.nb_locals[action_.var_name_other].columns.tolist() if c not in action_.mapping.values()]
                    for map_a, map_b in action_.mapping.items():
                        with v.Row(style_="align-items: center"):
                            with v.Col():
                                sol.Div(children=[" join "])
                            with v.Col():
                                v.Select(
                                    label="column",
                                    items=([map_a] if map_a else []) + left_cols,
                                    v_model=map_a,
                                    on_v_model=lambda new, old=map_a: update_key(new, old),
                                )
                            with v.Col():
                                sol.Div(children=[" on "])
                            with v.Col():
                                v.Select(
                                    label="column",
                                    items=([map_b] if map_b else []) + right_cols,
                                    v_model=map_b,
                                    on_v_model=lambda new, key=map_a: update_value(new, key),
                                )
                            with v.Col():
                                if not (map_a is None and map_b is None):
                                    sol.Button(icon_name="mdi-trash-can", icon=True, on_click=lambda key=map_a: remove(key))
        valid_variable_name = is_valid_variable_name(action_.df_var_out)
        v.TextField(
            label="New dataframe name",
            v_model=action_.df_var_out,
            on_v_model=lambda v: on_merge_action(replace(action_, df_var_out=v)),
            error_messages=[] if valid_variable_name else ["Invalid variable name"],
        )


@reacton.component
def TransformActionSelectPanel(
    columns,
    dtypes,
    action_: action.Action,
    on_action,
    on_action_type: Callable[
        [Type[Union[action.ActionFilter, action.ActionSelectColumns, action.ActionDropColumns, action.ActionGroupBy, action.ActionMerge]]], None
    ],
):
    action_mapping = {
        action.ActionFilter: "Filter rows",
        action.ActionDropColumns: "Drop columns",
        action.ActionSelectColumns: "Select columns",
        action.ActionGroupBy: "Groupby and aggregate",
        action.ActionMerge: "Join/merge",
    }
    action_mapping_reverse = {val: k for k, val in action_mapping.items()}

    op = action_mapping[type(action_)]

    def get_panel():
        if isinstance(action_, action.ActionFilter):
            return FilterPanelView(columns, dtypes, action_, on_action).key("filter_rows")
        if isinstance(action_, action.ActionDropColumns):
            return SelectColumnsPanelView(columns, dtypes, action_, on_action).key("drop columns")
        if isinstance(action_, action.ActionSelectColumns):
            return SelectColumnsPanelView(columns, dtypes, action_, on_action).key("select columns")
        if isinstance(action_, action.ActionGroupBy):
            return GroupByPanelView(columns, dtypes, action_, on_action).key("group by")
        if isinstance(action_, action.ActionMerge):
            return MergePanelView(columns, dtypes, action_, on_action).key("merge")

    with v.Sheet() as main:
        v.Select(
            label="Transformation",
            v_model=op,
            items=list(action_mapping.values()),
            on_v_model=lambda v: on_action_type(action_mapping_reverse[v]),  # type: ignore
        )
        if op is not None:
            get_panel()

    return main
