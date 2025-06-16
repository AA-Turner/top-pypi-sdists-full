import os
from metaflow.cards import (
    Markdown,
    Table,
    VegaChart,
    ProgressBar,
    MetaflowCardComponent,
    Artifact,
)
import math
from metaflow.plugins.cards.card_modules.components import (
    with_default_component_id,
    TaskToDict,
    ArtifactsComponent,
    render_safely,
)
import datetime
from metaflow.metaflow_current import current
import json
from functools import wraps
from collections import defaultdict
from threading import Thread, Event
import time

DEFAULT_WIDTH = 500
DEFAULT_HEIGHT = 200
DEFAULT_PADDING = 10
BG_COLOR = "#f2eeea"  # sand-100
VIEW_FILL = "#faf7f4"  # sand-200
GREYS = [
    "#ebe8e5",
    "#b2afac",
    "#6a6867",
]
BLACK = "#31302f"
GREENS = ["#dae8e2", "#3e8265", "#4c9878", "#428a6b", "#37795d"]
YELLOWS = ["#faf1db", "#f7e2b1", "#fbd784", "#e4b957", "#d7a530"]
PURPLES = ["#f5eff9", "#e7d4f3", "#976bac", "#8e53a9", "#77458f"]
REDS = ["#fce5e2", "#f3b6af", "#e6786c", "#e35f50", "#ce493a"]
BLUES = ["#dfe9f4", "#bdd8f2", "#88b7e3", "#6799c8", "#4e7ca7"]
ALL_COLORS = [
    # GREENS[0], PURPLES[0], REDS[0], BLUES[0], YELLOWS[0],
    GREENS[1],
    PURPLES[1],
    REDS[1],
    BLUES[1],
    YELLOWS[1],
    GREENS[2],
    PURPLES[2],
    REDS[2],
    BLUES[2],
    YELLOWS[2],
    GREENS[3],
    PURPLES[3],
    REDS[3],
    BLUES[3],
    YELLOWS[3],
    GREENS[4],
    PURPLES[4],
    REDS[4],
    BLUES[4],
    YELLOWS[4],
]


def update_spec_data(spec, data):
    spec["data"]["values"].append(data)
    return spec


def update_data_object(data_object, data):
    data_object["values"].append(data)
    return data_object


def line_chart_spec(
    title=None,
    category_name="u",
    y_name="v",
    xtitle=None,
    ytitle=None,
    width=DEFAULT_WIDTH,
    height=DEFAULT_HEIGHT,
    with_params=True,
    x_axis_temporal=False,
):
    parameters = [
        {
            "name": "interpolate",
            "value": "linear",
            "bind": {
                "input": "select",
                "options": [
                    "basis",
                    "cardinal",
                    "catmull-rom",
                    "linear",
                    "monotone",
                    "natural",
                    "step",
                    "step-after",
                    "step-before",
                ],
            },
        },
        {
            "name": "tension",
            "value": 0,
            "bind": {"input": "range", "min": 0, "max": 1, "step": 0.05},
        },
        {
            "name": "strokeWidth",
            "value": 2,
            "bind": {"input": "range", "min": 0, "max": 10, "step": 0.5},
        },
        {
            "name": "strokeCap",
            "value": "butt",
            "bind": {"input": "select", "options": ["butt", "round", "square"]},
        },
        {
            "name": "strokeDash",
            "value": [1, 0],
            "bind": {
                "input": "select",
                "options": [[1, 0], [8, 8], [8, 4], [4, 4], [4, 2], [2, 1], [1, 1]],
            },
        },
    ]
    parameter_marks = {
        "interpolate": {"expr": "interpolate"},
        "tension": {"expr": "tension"},
        "strokeWidth": {"expr": "strokeWidth"},
        "strokeDash": {"expr": "strokeDash"},
        "strokeCap": {"expr": "strokeCap"},
    }
    spec = {
        "title": title if title else "Line Chart",
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "width": DEFAULT_WIDTH,
        "height": DEFAULT_HEIGHT,
        "background": BG_COLOR,
        "padding": DEFAULT_PADDING,
        "view": {"fill": VIEW_FILL},
        "params": parameters if with_params else [],
        "data": {"name": "values", "values": []},
        "mark": {
            "type": "line",
            "tooltip": True,
            **(parameter_marks if with_params else {}),
        },
        "selection": {"grid": {"type": "interval", "bind": "scales"}},
        "encoding": {
            "x": {
                "field": category_name,
                "title": xtitle if xtitle else category_name,
                **({"timeUnit": "seconds"} if x_axis_temporal else {}),
                **({"type": "quantitative"} if not x_axis_temporal else {}),
            },
            "y": {
                "field": y_name,
                "type": "quantitative",
                "title": ytitle if ytitle else y_name,
            },
        },
    }
    data = {"values": []}
    return spec, data


class LineChart(MetaflowCardComponent):
    REALTIME_UPDATABLE = True

    def __init__(
        self,
        title,
        xtitle,
        ytitle,
        category_name,
        y_name,
        with_params=False,
        x_axis_temporal=False,
    ):
        super().__init__()

        self.spec, _ = line_chart_spec(
            title=title,
            xtitle=xtitle,
            ytitle=ytitle,
            category_name=category_name,
            y_name=y_name,
            with_params=with_params,
            x_axis_temporal=x_axis_temporal,
        )

    def update(self, data):  # Can take a diff
        self.spec = update_spec_data(self.spec, data)

    @with_default_component_id
    def render(self):
        vega_chart = VegaChart(self.spec, show_controls=True)
        vega_chart.component_id = self.component_id
        return vega_chart.render()


class ArtifactTable(Artifact):
    def __init__(self, data_dict):
        self._data = data_dict
        self._task_to_dict = TaskToDict(only_repr=True)

    @with_default_component_id
    @render_safely
    def render(self):
        _art_list = []
        for k, v in self._data.items():
            _art = self._task_to_dict.infer_object(v)
            _art["name"] = k
            _art_list.append(_art)

        af_component = ArtifactsComponent(data=_art_list)
        af_component.component_id = self.component_id
        return af_component.render()


# fmt: off
class BarPlot(MetaflowCardComponent):
    REALTIME_UPDATABLE = True

    def __init__(self, title, category_name, value_name, orientation="vertical"):

        if orientation not in ["vertical", "horizontal"]:
            raise ValueError("orientation must be either 'vertical' or 'horizontal'")

        super().__init__()
        self.spec = {
            "title": title,
            "$schema": "https://vega.github.io/schema/vega/v5.json",
            "description": "A basic bar chart example to show a count of values grouped by a category.",
            "background": BG_COLOR,
            "view": {"fill": VIEW_FILL},
            "width": DEFAULT_WIDTH,
            "height": DEFAULT_HEIGHT,
            "padding": DEFAULT_PADDING,
            "data": [{"name": "table", "values": []}],
            "signals": [
                {
                    "name": "tooltip",
                    "value": {},
                    "on": [
                        {"events": "rect:pointerover", "update": "datum"},
                        {"events": "rect:pointerout", "update": "{}"},
                    ],
                }
            ],
            "scales": [
                {
                    "name": "xscale" if orientation == "vertical" else "yscale",
                    "type": "band",
                    "domain": {"data": "table", "field": category_name},
                    "range": "width" if orientation == "vertical" else "height",
                    "padding": 0.25,
                    "round": True,
                },
                {
                    "name": "yscale" if orientation == "vertical" else "xscale",
                    "domain": {"data": "table", "field": value_name},
                    "nice": True,
                    "range": "height" if orientation == "vertical" else "width",
                },
                {
                    "name": "color",
                    "type": "ordinal",
                    "domain": {"data": "table", "field": category_name},
                    "range": ALL_COLORS,
                },
            ],
            "axes": [
                {"orient": "bottom", "scale": "xscale", "zindex": 1},
                {"orient": "left", "scale": "yscale", "zindex": 1},
            ],
            "marks": [
                {
                    "type": "rect",
                    "from": {"data": "table"},
                    "encode": {
                        "enter": {
                            "x": {
                                "scale": "xscale",
                                "field": (
                                    category_name
                                    if orientation == "vertical"
                                    else value_name
                                ),
                            },
                            "y": {
                                "scale": "yscale",
                                "field": (
                                    value_name
                                    if orientation == "vertical"
                                    else category_name
                                ),
                            },
                            f"{'y2' if orientation == 'vertical' else 'x2'}": {
                                "scale": (
                                    "yscale" if orientation == "vertical" else "xscale"
                                ),
                                "value": 0,
                            },
                            "width": {"scale": "xscale", "band": 1},
                            "height": {"scale": "yscale", "band": 1},
                        },
                        "update": {
                            "fill": {"value": GREENS[0]},
                        },
                        "hover": {"fill": {"value": GREENS[2]}},
                    },
                },
                {
                    "type": "text",
                    "encode": {
                        "enter": {
                            "align": {"value": "center"},
                            "baseline": {"value": "bottom"},
                            "fill": {"value": BG_COLOR},
                        },
                        "update": {
                            "x": {
                                "scale": "xscale",
                                "signal": f"tooltip.{category_name if orientation == 'vertical' else value_name}",
                                f"{'band' if orientation == 'vertical' else 'offset'}": (
                                    0.5 if orientation == "vertical" else -10
                                ),
                            },
                            "y": {
                                "scale": "yscale",
                                "signal": f"tooltip.{value_name if orientation == 'vertical' else category_name}",
                                f"{'band' if orientation == 'horizontal' else 'offset'}": (
                                    0.5 if orientation == "horizontal" else 20
                                ),
                            },
                            "text": {"signal": f"tooltip.{value_name}"},
                            "fillOpacity": [
                                {"test": "datum === tooltip", "value": 0},
                                {"value": 1},
                            ],
                        },
                    },
                },
            ],
        }

    def update(self, data):  # Can take a diff
        self.spec = update_spec_data(self.spec, data)

    @with_default_component_id
    def render(self):
        vega_chart = VegaChart(self.spec, show_controls=True)
        vega_chart.component_id = self.component_id
        return vega_chart.render()


class ViolinPlot(MetaflowCardComponent):
    REALTIME_UPDATABLE = True

    def __init__(self, title, category_col_name, value_col_name):
        super().__init__()

        self.spec = {
            "title": title,
            "$schema": "https://vega.github.io/schema/vega/v5.json",
            "description": "A violin chart to show a distributional properties of each category.",
            "background": BG_COLOR,
            "view": {"fill": VIEW_FILL},
            "width": DEFAULT_WIDTH,
            "height": DEFAULT_HEIGHT,
            "padding": DEFAULT_PADDING,
            "config": {
                "axisBand": {"bandPosition": 1, "tickExtra": True, "tickOffset": 0}
            },
            "signals": [
                {"name": "plotWidth", "value": 75},
                {"name": "height", "update": "(plotWidth + 10) * 3"},
                {
                    "name": "bandwidth",
                    "value": 0.1,
                    "bind": {"input": "range", "min": 0, "max": 0.2, "step": 0.01},
                },
            ],
            "data": [
                {"name": "src", "values": []},
                {
                    "name": "density",
                    "source": "src",
                    "transform": [
                        {
                            "type": "kde",
                            "groupby": [category_col_name],
                            "field": value_col_name,
                            "bandwidth": {"signal": "bandwidth"},
                            "extent": {"signal": "domain('xscale')"},
                        }
                    ],
                },
                {
                    "name": "stats",
                    "source": "src",
                    "transform": [
                        {
                            "type": "aggregate",
                            "groupby": [category_col_name],
                            "fields": [value_col_name, value_col_name, value_col_name],
                            "ops": ["q1", "q3", "median"],
                            "as": ["q1", "q3", "median"],
                        }
                    ],
                },
            ],
            "scales": [
                {
                    "name": "layout",
                    "type": "band",
                    "range": "height",
                    "domain": {"data": "src", "field": category_col_name},
                },
                {
                    "name": "xscale",
                    "type": "linear",
                    "range": "width",
                    "round": True,
                    "domain": {"data": "src", "field": value_col_name},
                    "zero": False,
                    "nice": True,
                },
                {
                    "name": "hscale",
                    "type": "linear",
                    "range": [0, {"signal": "plotWidth"}],
                    "domain": {"data": "density", "field": "density"},
                },
                {
                    "name": "color",
                    "type": "ordinal",
                    "domain": {"data": "src", "field": category_col_name},
                    "range": ALL_COLORS,
                },
            ],
            "axes": [
                {"orient": "bottom", "scale": "xscale", "zindex": 1},
                {"orient": "left", "scale": "layout", "zindex": 1},
            ],
            "marks": [
                {
                    "type": "group",
                    "from": {
                        "facet": {
                            "data": "density",
                            "name": "violin",
                            "groupby": category_col_name,
                        }
                    },
                    "encode": {
                        "enter": {
                            "yc": {
                                "scale": "layout",
                                "field": category_col_name,
                                "band": 0.5,
                            },
                            "height": {"signal": "plotWidth"},
                            "width": {"signal": "width"},
                        }
                    },
                    "data": [
                        {
                            "name": "summary",
                            "source": "stats",
                            "transform": [
                                {
                                    "type": "filter",
                                    "expr": f"datum.{category_col_name} === parent.{category_col_name}",
                                }
                            ],
                        }
                    ],
                    "marks": [
                        {
                            "type": "area",
                            "from": {"data": "violin"},
                            "encode": {
                                "enter": {
                                    "fill": {
                                        "scale": "color",
                                        "field": {"parent": category_col_name},
                                    }
                                },
                                "update": {
                                    "x": {"scale": "xscale", "field": "value"},
                                    "yc": {"signal": "plotWidth / 2"},
                                    "height": {"scale": "hscale", "field": "density"},
                                },
                            },
                        },
                        {
                            "type": "rect",
                            "from": {"data": "summary"},
                            "encode": {
                                "enter": {
                                    "fill": {"value": BLACK},
                                    "height": {"value": 2},
                                },
                                "update": {
                                    "x": {"scale": "xscale", "field": "q1"},
                                    "x2": {"scale": "xscale", "field": "q3"},
                                    "yc": {"signal": "plotWidth / 2"},
                                },
                            },
                        },
                        {
                            "type": "rect",
                            "from": {"data": "summary"},
                            "encode": {
                                "enter": {
                                    "fill": {"value": BLACK},
                                    "width": {"value": 2},
                                    "height": {"value": 8},
                                },
                                "update": {
                                    "x": {"scale": "xscale", "field": "median"},
                                    "yc": {"signal": "plotWidth / 2"},
                                },
                            },
                        },
                    ],
                }
            ],
        }

    def update(self, data):  # Can take a diff
        self.spec = update_spec_data(self.spec, data)

    @with_default_component_id
    def render(self):
        vega_chart = VegaChart(self.spec, show_controls=True)
        vega_chart.component_id = self.component_id
        return vega_chart.render()
# fmt: on
