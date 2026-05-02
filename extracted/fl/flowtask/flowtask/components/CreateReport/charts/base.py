"""Base Class for all Chart types."""
from abc import (
    ABC,
    abstractmethod,
)
from typing import Any, Union, List, Dict
from pyecharts.globals import ThemeType
import pyecharts.options as opts
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot as driver
from asyncdb.utils.encoders import DefaultEncoder


class baseChart(ABC):
    theme: str = "LIGHT"

    def __init__(self, title: str, data: Union[List, Dict], **kwargs):
        self.formatter = None
        if "theme" in kwargs:
            self.theme = kwargs["theme"]
            del kwargs["theme"]
        try:
            self._fields = kwargs["fields"]
        except KeyError:
            self._fields = ["name", "value"]
        self._encoder = DefaultEncoder(sort_keys=False)
        self._theme = getattr(ThemeType, self.theme)
        # TODO: making more initializations
        self.init_opts = opts.InitOpts(theme=self._theme, width="620px", height="420px")
        self.chart = self.get_chart()
        self.args = self.get_basic_args(**kwargs)
        self.set_chart(data, title, **kwargs)

    @abstractmethod
    def get_chart(self):
        pass

    @abstractmethod
    def set_chart(self, data: Any, title: str, **kwargs):
        pass

    @abstractmethod
    def get_basic_args(self, **kwargs):
        pass

    @abstractmethod
    def get_global_opts(self, title: str, **kwargs):
        pass

    def get_series_opts(self, **kwargs):
        return {
            "label_opts": opts.LabelOpts(
                position="outside", formatter=self.formatter, is_show=True
            )
        }

    def chart(self):
        return self.chart

    def image(self):
        """Returns the Base64 version of Image."""
        img = None
        make_snapshot(driver, self.chart.render(), "graph.base64")
        with open("graph.base64", "r", encoding="utf-8") as f:
            img = f.read()
        return img
