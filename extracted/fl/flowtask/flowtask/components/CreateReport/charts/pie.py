from typing import Any, Union, List, Dict
import orjson
from pyecharts.charts import Pie
from borax.datasets.fetch import fetch
import pyecharts.options as opts
from .base import baseChart


class pieChart(baseChart):
    rosetype: str = "radius"
    formatter: str = "{b}: {c} / {d}%"

    def __init__(self, title: str, data: Union[List, Dict], **kwargs):
        if "rosetype" in kwargs:
            self.rosetype = kwargs["rosetype"]
            del kwargs["rosetype"]
        super(pieChart, self).__init__(title, data, **kwargs)

    def get_chart(self):
        return Pie(init_opts=self.init_opts)

    def set_chart(self, data: Any, title: str, **kwargs):
        # x, y = Base.cast(o_data)
        dst = self._encoder(data)
        dst = orjson.loads(dst)
        # print('DATA ', dst)
        if isinstance(dst, dict):
            names, values = zip(*dst.items())
        else:
            names, values = fetch(dst, *self._fields)
        self.args["data_pair"] = [list(z) for z in zip(names, values)]
        # add arguments:
        self.chart.add(series_name="", **self.args).set_global_opts(
            **self.get_global_opts(title, **kwargs)
        ).set_series_opts(**self.get_series_opts(**kwargs))

    def get_basic_args(self, **kwargs):
        return {
            "radius": "55%",
            "center": ["50%", "50%"],
            # "rosetype": self.rosetype
        }

    def get_series_opts(self, **kwargs):
        return {
            "label_opts": opts.LabelOpts(
                position="outside",
                # formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                formatter=self.formatter,
                is_show=True,
            )
        }

    def get_global_opts(self, title: str, **kwargs):
        return {
            "title_opts": opts.TitleOpts(
                title=title,
                pos_left="center",
                pos_top="0",
            ),
            "legend_opts": opts.LegendOpts(
                is_show=True, pos_left="center", pos_bottom="20"
            ),
        }
