from typing import Any, Union, List, Dict
import orjson
from pyecharts.charts import Bar
from borax.datasets.fetch import fetch
import pyecharts.options as opts
from .base import baseChart


class barChart(baseChart):
    rosetype: str = "radius"
    formatter: str = "{c}"
    axis_type: str = "category"

    def __init__(self, title: str, data: Union[List, Dict], **kwargs):
        fields = kwargs["fields"]
        self._x = fields["x_axis"]
        self._y = fields["y_axis"]
        super(barChart, self).__init__(title, data, **kwargs)

    def get_chart(self):
        return Bar(init_opts=self.init_opts)

    def set_chart(self, data: Any, title: str, **kwargs):
        # x, y = Base.cast(o_data)
        dst = self._encoder(data)
        dst = orjson.loads(dst)
        names = fetch(dst, self._x)
        self.chart.add_xaxis(names)
        for y in self._y:
            values = fetch(dst, y)
            self.chart.add_yaxis(y, values)
        self.chart.set_global_opts(
            **self.get_global_opts(title, **kwargs)
        ).set_series_opts(**self.get_series_opts(**kwargs))

    def get_basic_args(self, **kwargs):
        return {}

    def get_series_opts(self, **kwargs):
        return {
            "label_opts": opts.LabelOpts(
                position="outside", formatter=self.formatter, is_show=True
            )
        }

    def get_global_opts(self, title: str, **kwargs):
        return {
            "title_opts": opts.TitleOpts(title=title),
            "legend_opts": opts.LegendOpts(is_show=True, pos_right="15%"),
            "xaxis_opts": opts.AxisOpts(type_=self.axis_type),
        }
