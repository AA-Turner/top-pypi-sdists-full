import uuid
from dataclasses import asdict, dataclass, field
from typing import Dict, Optional

import solara.lab


class EqWrapper:
    def __init__(self, obj):
        self.obj = obj

    def get(self):
        return self.obj


@dataclass(frozen=True)
class Viz:
    name: str = "Untitled"
    plot_type: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    col_args: Dict = field(default_factory=lambda: {})
    df_var_name: Optional[str] = None
    plot_var_name: Optional[str] = None
    crossfilter_enabled: bool = True


class ReactiveViz(solara.lab.Reactive[Viz]):
    pass


viz = ReactiveViz(Viz())


def to_json(obj):
    if isinstance(obj, Viz):
        return {"type_plot_state": asdict(obj)}


def from_json(dct):
    if "type_plot_state" in dct:
        res = Viz(**dct["type_plot_state"])
        return res
