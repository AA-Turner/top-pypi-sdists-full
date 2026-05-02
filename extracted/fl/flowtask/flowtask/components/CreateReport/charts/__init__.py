"""Chart utilities using PyEcharts."""
from typing import Any
from .pie import pieChart
from .bar import barChart

__all__ = ["pieChart", "barChart"]


def loadChart(charttype: str, title: str, data: Any, **kwargs):
    if charttype == "bar":
        return barChart(title, data, **kwargs)
    elif charttype == "pie":
        return pieChart(title, data, **kwargs)
    else:
        raise RuntimeError("CreateReport: Invalid Chart Type")
