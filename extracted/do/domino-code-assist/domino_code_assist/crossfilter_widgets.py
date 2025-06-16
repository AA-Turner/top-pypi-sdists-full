import json
import textwrap
from dataclasses import asdict, dataclass, replace
from typing import List, Optional

import reacton.ipyvuetify as v
import solara
from solara.lab.utils.dataframe import df_py_types

from domino_code_assist import util
from domino_code_assist.assistant import drawer, mixpanel


@dataclass(frozen=True)
class WidgetState:
    df_var: Optional[str] = None
    widget: Optional[str] = None
    column: Optional[str] = None
    configurable: bool = True
    invert: bool = False
    mode: str = "=="
    multiple: bool = False
    out_var: Optional[str] = None


@solara.component
def CrossFilterWidgetsPanel(edit_data: Optional[WidgetState], set_code, dfs, open, edit, on_close, overwrite_warning=None):
    state, set_state = solara.use_state_or_update(edit_data if open and edit and edit_data else WidgetState(out_var=util.generate_var_name("widget")))

    def set_plot_var(val):
        set_state(lambda s: replace(s, out_var=val))

    available_widgets = list(_generate_map.keys())

    columns = solara.use_memo(lambda: util.nb_locals[state.df_var].columns.tolist() if state.df_var else [], [state.df_var])
    types = solara.use_memo(lambda: [i.name for i in util.nb_locals[state.df_var].dtypes.tolist()] if state.df_var else [], [state.df_var])
    column_items = [{"text": f"{c} ({t})", "value": c} for c, t in zip(columns, types)]

    def on_apply():
        assert state.widget is not None
        mixpanel.api.track_with_defaults(
            "inserted code",
            {
                "section": "Cross-filter widgets",
            },
        )
        set_code({"code": _generate_map[state.widget](state), "meta": json.dumps(to_json(state))})
        on_close()

    valid_conf = True
    invalid_reason = ""
    if state.widget == "Slider":
        if state.df_var and state.column:
            df = util.nb_locals[state.df_var]
            py_type = df_py_types(df)
            if py_type[state.column] not in (int, float):
                valid_conf = False
                invalid_reason = "Slider widget only supports numerical columns"

    with drawer.RightDrawer(
        open=open,
        on_open=lambda v: on_close() if not v else None,
        title="Crossfilter Widgets",
        edit=bool(edit),
        on_apply=on_apply,
        apply_disabled=not ((state.df_var and (state.widget == "Report" or state.column) and state.widget and state.out_var) and valid_conf),
        show_var_out=True,
        var_out=state.out_var or "",
        on_var_out=set_plot_var,
        width="768px",
        warning_widget=overwrite_warning,
    ) as main:
        with solara.Div():
            with solara.Div(class_="dca-transform-header", style_="margin-left: -24px; margin-right: -24px; margin-top: -4px; padding: 8px 80px;"):
                v.Select(label="Dataframe", items=dfs, v_model=state.df_var, on_v_model=lambda v: set_state(lambda s: replace(s, df_var=v)))
            if state.df_var:
                v.Select(label="Widget", items=available_widgets, v_model=state.widget, on_v_model=lambda v: set_state(replace(state, widget=v)))
                if state.widget:
                    if state.widget != "Report":
                        v.Select(label="Column", items=column_items, v_model=state.column, on_v_model=lambda v: set_state(replace(state, column=v)))
                        v.Switch(label="Invert filter", v_model=state.invert, on_v_model=lambda v: set_state(replace(state, invert=v)))
                        v.Switch(label="Configurable", v_model=state.configurable, on_v_model=lambda v: set_state(replace(state, configurable=v)))
                        if state.widget == "Slider":
                            solara.Div(children=["Mode"], style_="color: rgba(0, 0, 0, 0.6)")
                            with solara.ToggleButtonsSingle(value=state.mode, on_value=lambda v: set_state(replace(state, mode=v))):  # type: ignore
                                solara.Button(icon_name="mdi-code-equal", icon=True, value="==")
                                solara.Button(icon_name="mdi-code-not-equal", icon=True, value="!=")
                                solara.Button(icon_name="mdi-code-less-than", icon=True, value="<")
                                solara.Button(icon_name="mdi-code-less-than-or-equal", icon=True, value="<=")
                                solara.Button(icon_name="mdi-code-greater-than", icon=True, value=">")
                                solara.Button(icon_name="mdi-code-greater-than-or-equal", icon=True, value=">=")
                        if state.widget == "Select":
                            v.Switch(label="Multiple", v_model=state.multiple, on_v_model=lambda v: set_state(replace(state, multiple=v)))
                if not valid_conf:
                    solara.Error(invalid_reason, classes=["my-4"])
    return main


_default = WidgetState()


def _param_list_str(state: WidgetState, names: List[str]):
    def param_str(name: str):
        value = getattr(state, name)
        quoted = f'"{value}"' if isinstance(value, str) else value

        return f", {name}={quoted}" if value != getattr(_default, name) else ""

    return "".join([param_str(name) for name in names])


def _generate_select_widget(state: WidgetState):
    return textwrap.dedent(
        f"""\
        from solara import CrossFilterSelect

        {state.out_var} = CrossFilterSelect({state.df_var}{_param_list_str(state, ["column", "configurable", "invert", "multiple"])})
        {state.out_var}
        """
    )


def _generate_slider_widget(state: WidgetState):
    return textwrap.dedent(
        f"""\
        from solara import CrossFilterSlider

        {state.out_var} = CrossFilterSlider({state.df_var}{_param_list_str(state, ["column", "configurable", "invert", "mode"])})
        {state.out_var}
        """
    )


def _generate_report_widget(state: WidgetState):
    return textwrap.dedent(
        f"""\
        from solara import CrossFilterReport

        {state.out_var} = CrossFilterReport({state.df_var})
        {state.out_var}
        """
    )


_generate_map = {
    "Select": _generate_select_widget,
    "Slider": _generate_slider_widget,
    "Report": _generate_report_widget,
}


def to_json(obj):
    if isinstance(obj, WidgetState):
        return {"type_widget_state": asdict(obj)}


def from_json(dct):
    if "type_widget_state" in dct:
        dct = dct["type_widget_state"]
        return WidgetState(**dct)
