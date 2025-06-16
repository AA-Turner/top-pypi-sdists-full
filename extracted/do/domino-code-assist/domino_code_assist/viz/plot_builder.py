import inspect
import types
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

import plotly.express as px
import plotly.graph_objs._figure
import plotly.io as pio
import reacton
import reacton.ipyvuetify as v
import solara
import solara as sol
from solara.lab import Ref

from domino_code_assist.assistant import mixpanel

from .state import Viz, viz

basic_col_args = (
    "x",
    "y",
    "locations",
    "color",
    "symbol",
    "r",
    "theta",
    "lat",
    "lon",
    "z",
    "a",
    "b",
    "c",
    "size",
)
extra_col_args = (
    "line_group",
    "symbol",
    "pattern_shape",
    "line_dash",
    "names",
    "values",
    "parents",
    "text",
    "hover_name",
    "hover_data",
    "facet_row",
    "facet_col",
    "base",
)

col_list_args = ("hover_data",)

basic_plots = (
    "area",
    "bar",
    "histogram",
    "line",
    "line_3d",
    "scatter",
    "scatter_3d",
    "scatter_geo",
    "choropleth",
)

translations = {
    "area": "Area",
    "bar": "Bar",
    "histogram": "Histogram",
    "line": "Line",
    "line_3d": "Line 3D",
    "scatter": "Scatter",
    "scatter_3d": "Scatter 3D",
    "scatter_geo": "Scatter Map",
    "choropleth": "Choropleth Map",
    "x": "X-axis",
    "y": "Y-axis",
    "z": "Z-axis",
}


def un_dash(value):
    return " ".join([el.capitalize() for el in value.split("_")])


def get_args(name):
    return list(inspect.signature(getattr(px, name)).parameters.keys())


def get_col_args(name):
    return [a for a in get_args(name) if a in basic_col_args + extra_col_args]


specs = {
    n: {
        "name": n,
        "col_args": get_col_args(n),
        "args": get_args(n),
    }
    for n in dir(px)
    if isinstance(getattr(px, n), types.FunctionType) and get_args(n) and get_args(n)[0] == "data_frame"
}


arg_types: Dict[str, Dict[str, Any]] = {
    "template": {
        "type": list(pio.templates._templates.keys()),
        "default": "plotly",
        "name": "Theme",
    },
    "orientation": {
        "type": ["h", "v"],
        "default": "v",
        "type_mapping": ["Horizontal", "Vertical"],
        "name": "Orientation",
    },
    "histnorm": {
        "type": ["percent", "probability", "density"],
        "name": "Normalization",
    },
    "histfunc": {
        "type": ["count", "sum", "avg", "min", "max"],
        "default": "count",
        "name": "Aggregate Function",
    },
    "log_x": {"type": bool, "default": False, "description": "If True, the x-axis is log-scaled in cartesian coordinates", "name": "Logarithmic X-axis"},
    "log_y": {
        "type": bool,
        "default": False,
        "description": "If True, the x-axis is log-scaled in cartesian coordinates",
        "name": "Logarithmic Y-axis",
    },
    "color_continuous_scale": {
        "type": [x for x in dir(px.colors.sequential) if not x.startswith("_")],
        "default": "Plasma",
        "name": "Color Scale",
    },
}

plot_types = basic_plots


def nop(*_):  # pragma: no cover
    return


plot_type_items = [dict(value=t, text=translations[t]) for t in plot_types]


def track_set_attribute(col_arg):
    mixpanel.api.track_with_defaults(
        "interaction",
        {
            "section": "visualizations",
            "type": "set attribute",
            "attribute": col_arg,
        },
    )


def generate_code(viz: Viz):
    args = {k: v for k, v in viz.col_args.items() if k in specs[viz.plot_type]["args"]}  # type: ignore

    def transform_arg(k, value):
        if k == "color_continuous_scale":
            return f"px.colors.sequential.{value}"
        if type(value) is str:
            return f'"{value}"'
        return value

    arg_str = ", ".join(
        [f"{k}={transform_arg(k, v)}" for k, v in args.items() if v is not None and not (isinstance(v, list) and len(v) == 0)],
    )

    def remove_margins(var_name):
        return f"{var_name}.update_layout(margin=dict(l=0, r=0, t=40 if {var_name}.layout.title.text else 20, b=0))"

    if viz.crossfilter_enabled:
        base_var_name = "_base_" + (viz.plot_var_name or "")
        select_config = ""
        if viz.plot_type == "scatter":
            select_config = f'{base_var_name}.update_layout(dragmode="lasso")\n'
        elif viz.plot_type in ["bar", "histogram"]:
            direction = "v" if "orientation" in viz.col_args and viz.col_args["orientation.value"] == "h" else "h"
            select_config = f'{base_var_name}.update_layout(dragmode="select", selectdirection="{direction}")\n'
        return "".join(
            [
                "from solara.express import CrossFilteredFigurePlotly\n",
                "import plotly.express as px\n\n",
                f"{base_var_name} = px.{viz.plot_type}({viz.df_var_name}, {arg_str})\n",
                select_config,
                remove_margins(base_var_name) + "\n",
                f"{viz.plot_var_name} = " if viz.plot_var_name else "",
                f"CrossFilteredFigurePlotly({base_var_name})\n",
                f"\n{viz.plot_var_name}" if viz.plot_var_name else "",
            ]
        )
    return "".join(
        [
            "import plotly.express as px\n\n",
            f"{viz.plot_var_name} = " if viz.plot_var_name else "",
            f"px.{viz.plot_type}({viz.df_var_name}, {arg_str})\n",
            remove_margins(viz.plot_var_name),
            f"\n{viz.plot_var_name}" if viz.plot_var_name else "",
        ]
    )


@reacton.component
def DimensionSelects(columns, for_cols: Union[List[str], Tuple[str, ...]]):
    viz.use()
    assert viz.value.plot_type is not None
    with v.Row() as main:
        for col_arg in specs[viz.value.plot_type]["col_args"]:

            def set_attribute(value, col_arg=col_arg):
                track_set_attribute(col_arg)
                Ref(viz.fields.col_args[col_arg]).value = value

            if col_arg not in for_cols:
                continue
            with v.Col(sm=2):
                with solara.Div().key(str(col_arg)):
                    v.Select(
                        label=translations.get(col_arg) or un_dash(col_arg),
                        items=columns,
                        clearable=True,
                        multiple=col_arg in col_list_args,
                        v_model=viz.value.col_args.get(col_arg),
                        on_v_model=set_attribute,
                    ).meta(ref=f"dimension_{col_arg}")
    return main


@reacton.component
def OptionsPanel():
    viz.use()
    assert viz.value.plot_type is not None
    with v.Row() as main:
        for arg in specs[viz.value.plot_type]["args"]:

            def set_attribute(value, col_arg=arg):
                track_set_attribute(col_arg)
                Ref(viz.fields.col_args[col_arg]).value = value

            if arg not in arg_types:
                continue
            with v.Col(sm=2):
                with solara.Div():
                    arg_spec = arg_types[arg]
                    if arg_spec.get("type") == bool:
                        v.Switch(
                            label=arg_spec["name"],
                            v_model=viz.value.col_args.get(arg),
                            on_v_model=set_attribute,
                        ).meta(ref=f"dimension_{arg}")
                    elif type(arg_spec["type"]) in (list, tuple):
                        v.Select(
                            label=arg_spec["name"],
                            items=[dict(value=v, text=t) for v, t in zip(arg_spec["type"], arg_spec["type_mapping"])]
                            if arg_spec.get("type_mapping")
                            else arg_spec["type"],
                            v_model=viz.value.col_args.get(arg),
                            on_v_model=set_attribute,
                        ).meta(ref=f"dimension_{arg}")
    return main


@dataclass(frozen=True)
class FigState:
    fig: Optional[plotly.graph_objs._figure.Figure] = None
    error: Optional[str] = None
    code: Optional[str] = None


@reacton.component
def PlotBuilder(df, columns, min_height="724px"):
    viz.use()
    state, set_state = reacton.use_state(FigState())
    exp_panel, set_exp_panel = reacton.use_state(0)
    auto_preview, set_auto_preview = reacton.use_state(True)
    update_preview, set_update_preview = reacton.use_state(0)
    should_update, set_should_update = reacton.use_state(False)

    def make_fig():
        if not should_update:
            return
        if not Ref(viz.fields.col_args).value or not viz.value.plot_type or not df:
            set_state(FigState())
            set_should_update(False)
            return
        try:
            args = {k: v for k, v in viz.value.col_args.items() if k in specs[viz.value.plot_type]["args"]}
            fig = getattr(px, viz.value.plot_type)(df.get(), **args)
            code = generate_code(viz.value)
            set_state(FigState(fig=fig, code=code))
        except Exception as e:
            set_state(FigState(error=str(e)))
        set_should_update(False)

    reacton.use_memo(lambda: set_should_update(True), [viz.value, df])
    reacton.use_effect(make_fig, [auto_preview and should_update, update_preview])

    with v.Sheet(style_=min_height and f"min-height: {min_height}") as main:

        def on_plot_type(plot_type):
            mixpanel.api.track_with_defaults(
                "interaction",
                {
                    "section": "visualizations",
                    "type": "selected plot type",
                    "plot_type": plot_type,
                },
            )
            Ref(viz.fields.plot_type).value = plot_type

        def on_crossfilter(value):
            mixpanel.api.track_with_defaults(
                "interaction",
                {
                    "section": "visualizations",
                    "type": "set crossfilter",
                },
            )
            Ref(viz.fields.crossfilter_enabled).value = value

        v.Select(
            label="Plot Type",
            items=plot_type_items,
            v_model=viz.value.plot_type,
            on_v_model=on_plot_type,
        ).meta(ref="plot_type")
        with v.Row():
            with v.Col(sm=2):
                v.Switch(label="Enable crossfilter", v_model=viz.value.crossfilter_enabled, on_v_model=on_crossfilter).meta(ref="crossfilter")
            with v.Col(sm=8, align_self="center"):
                controllers = ["scatter", "bar", "histogram"]
                v.Html(
                    tag="div",
                    children=(
                        "Cross-filtering allows you to interactively explore the relationship between multiple variables in a dataset by "
                        "filtering the data in one plot based on the selection made in another plot or widget."
                    ),
                )
                if viz.value.plot_type and viz.value.plot_type not in controllers and viz.value.crossfilter_enabled:
                    v.Html(
                        tag="span",
                        children="Note: this plot type can only view cross-filtered data, not select it.",
                        style_="padding: 4px; background-color: #ECE63D",
                    ).key("crossfilter info").meta(ref="crossfilter_info")

        if viz.value.plot_type:
            with v.Sheet():
                with v.ExpansionPanels(v_model=exp_panel, on_v_model=set_exp_panel):
                    with v.ExpansionPanel():
                        v.ExpansionPanelHeader(children=["Dimensions"])
                        with v.ExpansionPanelContent():
                            DimensionSelects(columns, basic_col_args)
                    with v.ExpansionPanel():
                        v.ExpansionPanelHeader(children=["Extra Dimensions"])
                        with v.ExpansionPanelContent():
                            DimensionSelects(columns, extra_col_args)
                    with v.ExpansionPanel():
                        v.ExpansionPanelHeader(children=["Options"])
                        with v.ExpansionPanelContent():
                            OptionsPanel()
            with solara.Div(style_="display: flex"):
                v.Switch(label="Auto preview", v_model=auto_preview, on_v_model=set_auto_preview).meta(ref="auto_preview")
                if not auto_preview:
                    sol.Button(
                        "Update preview",
                        icon_name="mdi-refresh-circle",
                        on_click=lambda: set_update_preview(update_preview + 1),
                        disabled=not should_update,
                        color="primary",
                        class_=" ma-3",
                    ).meta(ref="update_preview")
            if state.error:
                solara.Div(children=["plot error", state.error]).meta(ref="error")
            elif state.fig:
                solara.FigurePlotly(state.fig, dependencies=state).meta(ref="figure")
                from solara.components.code_highlight_css import CodeHighlightCss

                CodeHighlightCss()
                from domino_code_assist.code import Code

                Code(
                    code_chunks=[state.code],
                    on_event=lambda a: None,
                    error=None,
                ).meta(ref="code")

    return main
