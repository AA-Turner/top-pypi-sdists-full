"""AG Charts components."""

from reflex.vars.base import Var

from ..ag_grid.constants import CHARTS_VERSION
from ..component import ComponentEnterprise

BASE_PKG = "ag-charts-react"


class AgCharts(ComponentEnterprise):
    """A simple line chart component using AG Charts."""

    library = f"{BASE_PKG}@{CHARTS_VERSION}"

    tag = "AgCharts"

    options: Var[dict]


ag_chart = AgCharts.create
