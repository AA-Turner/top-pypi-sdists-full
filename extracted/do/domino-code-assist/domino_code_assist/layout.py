from functools import partial
from itertools import groupby
from typing import List

import plotly
import reacton
import reacton.ipyvuetify as v
import solara as sol
import solara.express
from pandas.core.frame import DataFrame
from solara.lab.components.cross_filter import (
    CrossFilterReport,
    CrossFilterSelect,
    CrossFilterSlider,
)

import domino_code_assist.deploy
from domino_code_assist import app, css, util
from domino_code_assist.thumbnail import Thumbnail


def to_widget(x):
    if isinstance(x, plotly.graph_objs._figure.Figure):
        return sol.FigurePlotly(x)
    else:
        # todo: add special cases as needed
        return x


def _make_grid_panel_builder(layout_item, markdown_cells):

    children = []
    if layout_item.get("i"):
        i = layout_item.get("i")
        if util.nb_locals.get(i) is not None:
            obj = util.nb_locals[i]
            if isinstance(obj, plotly.graph_objs._figure.Figure):
                children = [sol.FigurePlotly(obj)]
            elif isinstance(obj, DataFrame):
                children = [sol.CrossFilterDataFrame(obj, items_per_page=10, scrollable=True)]
            elif isinstance(obj, app.ReactiveDf):
                children = [app.DropDataframe(obj.var_name, obj.label)]
            else:
                children = [obj]
        elif markdown_cells and i in markdown_cells:
            children = [sol.Markdown(markdown_cells[i])]

    with v.Card(style_="height: 100%;") as panel:
        v.CardText(style_="height: 100%; max-height: 100%; overflow: auto;", children=children)

    return panel


@reacton.component
def CrossFilterScope(children: List[reacton.core.Element] = []):
    sol.provide_cross_filter()

    return sol.Div(children=children)


@reacton.component
def CardGridLayoutBuilder(obj_vars, layout, on_layout, markdown_cells, on_toggle):
    objects_on = [k["i"] for k in layout]

    group_names = ["Plots", "Markdown", "Widgets", "Dataframes", "Other"]

    def group_obj_vars():
        def sort_vars(var):
            obj = util.nb_locals.get(var)
            if obj is None:
                # markdown
                return 1
            if isinstance(obj, plotly.graph_objs._figure.Figure) or (
                isinstance(obj, reacton.core.Element) and obj.component is solara.express.CrossFilteredFigurePlotly
            ):
                return 0
            if isinstance(obj, reacton.core.Element) and obj.component in [CrossFilterSlider, CrossFilterSelect, CrossFilterReport]:
                return 2
            if isinstance(obj, DataFrame) or (isinstance(obj, reacton.core.Element) and obj.component is DataTableCrossFiltered):
                return 3
            return 4

        grouped = groupby(
            sorted(obj_vars + list((markdown_cells or {}).keys()), key=sort_vars),
            sort_vars,
        )
        nb_order = list(util.nb_locals.keys())
        return [
            (group_names[group], sorted(rows, key=lambda x: nb_order.index(x) if x in nb_order else list(markdown_cells.keys()).index(x)))
            for (group, rows) in grouped
        ]

    grouped_obj_vars = reacton.use_memo(group_obj_vars, [obj_vars, markdown_cells])

    def toggle_layout(on, id):
        on_toggle(on)

        def update(layout):
            layout_contains_id = any([k for k in layout if k["i"] == id])

            if on:
                top_y = max([k["y"] + k["h"] for k in layout]) if layout else 0
                return layout + [dict(i=id, w=6, h=5, x=0, y=top_y)] if not layout_contains_id else layout
            else:
                return [k for k in layout if k["i"] != id] if layout_contains_id else layout

        on_layout(lambda state: update(state))

    items = {layout_item["i"]: _make_grid_panel_builder(layout_item, markdown_cells) for layout_item in layout}

    def preselect():
        if not layout and "plot_quick_start" in obj_vars:
            on_layout(
                lambda state: [
                    *([{"i": "df_quick_start", "w": 6, "h": 10, "x": 6, "y": 0}] if "df_quick_start" in obj_vars else []),
                    {"i": "plot_quick_start", "w": 6, "h": 10, "x": 0, "y": 0},
                ]
            )
        elif not layout and grouped_obj_vars and grouped_obj_vars[0][0] == "Plots":
            on_layout(lambda state: [{"i": grouped_obj_vars[0][1][0], "w": 6, "h": 10, "x": 0, "y": 0}])

    reacton.use_memo(preselect, [])

    with v.Sheet(class_="domino-plotly-auto-height domino-card-grid", style_="height: 100%; max-height: 100%; overflow: hidden; margin-left: -26px;") as main:
        css.Css()
        with sol.Div(style_="display: flex; height: 100%; max-height: 100%;"):
            with sol.Div(style_="width: 256px; overflow: auto; padding-left: 26px; background-color: var(--jp-border-color2);"):
                with sol.Div(style_="width: 200px"):
                    for group, group_vars in grouped_obj_vars:
                        sol.Div(style_="margin-top: 16px; margin-bottom: -8px; font-weight: bold", children=[group + ": "])
                        for obj_var in group_vars:
                            label = obj_var
                            if markdown_cells and obj_var in markdown_cells:
                                label = markdown_cells[obj_var].replace("\n", " ")
                                length = len(label)
                                label = label[:28] + ("..." if length > 28 else "")
                            with sol.Div():
                                with v.Sheet(elevation=1, class_="px-1"):
                                    v.Switch(label=label, v_model=obj_var in objects_on, on_v_model=partial(toggle_layout, id=obj_var))
                                    with CrossFilterScope():
                                        with Thumbnail():
                                            _make_grid_panel_builder({"i": obj_var}, markdown_cells)

            with sol.Div(style_="flex-grow: 1; overflow: auto"):
                with CrossFilterScope():
                    sol.GridLayout(items=items, grid_layout=layout, resizable=True, draggable=True, on_grid_layout=on_layout)

    return main


# for backward compatibility
Preview = domino_code_assist.deploy.Deployer
CardGridLayout = domino_code_assist.CardGridLayout
DataTableCrossFiltered = solara.CrossFilterDataFrame
