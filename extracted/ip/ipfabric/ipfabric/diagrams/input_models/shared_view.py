from copy import deepcopy
from typing import Optional, Union

from deepdiff import DeepDiff
from pydantic import BaseModel, field_validator, Field

from ipfabric.diagrams.output_models import Position
from .constants import (
    DEFAULT_NETWORK,
    DEFAULT_PATHLOOKUP,
    HIDDEN_DEV_TYPES,
)
from .graph_parameters import (
    Unicast,
    Multicast,
    Host2GW,
    Network,
)
from .graph_settings import NetworkSettings, PathLookupSettings, PathLookup, Overlay

REMOVE_PATH_PARAMS = ["pathLookupType", "networkMode", "pathLookupType", "groupBy", "type"]
PARAMS_IMPORTS = [
    "EntryPoint",
    "Layout",
    "Technologies",
    "Instance",
    "STPInstances",
    "OtherOptions",
    "Algorithm",
    "Overlay",
    "EdgeSettings",
    "GroupSettings",
    "Style",
    "PathLookup",
]


class SharedView(BaseModel):
    snapshot_id: str
    client_snapshot_id: str
    positions: dict
    settings: list[dict]
    params: dict
    hidden_devs: Optional[list] = Field(default_factory=list)
    hidden_nodes: Optional[list] = Field(default_factory=list)  # Not available in API
    collapsed_node_groups: Optional[list] = Field(default_factory=list)  # Not available in API
    path_lookup: Optional[dict] = Field(default_factory=dict)
    overlay: Optional[dict] = Field(default_factory=dict)

    @field_validator("settings")
    @classmethod
    def _settings(cls, v):
        for e in v:
            e.pop("id", None)
            for c in e.get("children", []):
                c.pop("id", None)
        return v

    @property
    def graph_type(self):
        if self.params["type"] == "topology":
            return self.params["type"]
        else:
            return self.params["pathLookupType"]

    def graph_model(self) -> Union[Unicast, Host2GW, Multicast, Network]:
        if self.graph_type == "topology":
            return Network(sites=self.params["paths"], technologies=self.params.get("technologies", None))
        params = deepcopy(self.params)
        [params.pop(_, None) for _ in REMOVE_PATH_PARAMS]
        params.update(params.pop("l4Options", {}))
        if self.graph_type == "unicast":
            return Unicast(**params)
        elif self.graph_type == "hostToDefaultGW":
            return Host2GW(**params)
        elif self.graph_type == "multicast":
            return Multicast(**params)

    def graph_settings(self):
        if self.graph_type == "topology":
            if DeepDiff(self.settings, DEFAULT_NETWORK) or self.hidden_devs != HIDDEN_DEV_TYPES:
                return NetworkSettings(edges=self.settings, hiddenDeviceTypes=self.hidden_devs)
            else:
                return None
        else:
            if DeepDiff(self.settings, DEFAULT_PATHLOOKUP) or self.path_lookup != vars(PathLookup()):
                return PathLookupSettings(edges=self.settings, pathLookup=self.path_lookup)
            else:
                return None

    @property
    def overlay_settings(self):
        if self.overlay.get("type", None) == "intent":
            return Overlay(intentRuleId=self.overlay["intentRule"]["id"])
        elif self.overlay.get("type", None) == "compare":
            return Overlay(snapshotToCompare=self.overlay["snapshotToCompare"])
        return None

    @property
    def positions_settings(self) -> dict[str, Position]:
        return {k: Position(**v) for k, v in self.positions.items()}

    def create_code(self, positions: bool = False):
        settings = self.graph_settings()
        params = self.graph_model()
        code = [f"parameters = {params.__repr_name__()}({params.__repr_str__(', ')})"]
        imports, e_imports = {params.__repr_name__()}, {_ for _ in PARAMS_IMPORTS if _ in str(params)}

        imports.update({"ICMP"} if getattr(params, "protocol", None) == "icmp" else {})
        e_imports.update({"Overlay"} if self.overlay_settings else {})

        tmp = "diagram = ipf.diagram.model(parameters=parameters"
        if settings:
            imports.add(settings.__repr_name__())
            code.append(f"settings = {settings.__repr_name__()}({settings.__repr_str__(', ')})")
            e_imports.update({_ for _ in PARAMS_IMPORTS if _ in str(settings)})
            tmp += ", graph_settings=settings"
        if e_imports:
            code.insert(0, f"from ipfabric.diagrams.input_models import {', '.join(e_imports)}")

        if positions:
            imports.add("Position")
            code.append(f"positions = {self.positions_settings}")
            tmp += ", positions=positions"
        code.insert(0, f"from ipfabric.diagrams import {', '.join(imports)}")

        if self.snapshot_id != self.client_snapshot_id:
            tmp += f", snapshot_id='{self.snapshot_id}'"
        if self.overlay_settings:
            tmp += f", overlay=Overlay({self.overlay_settings.__repr_str__(', ')})"
        tmp += ")"
        code.append(tmp)

        return code
