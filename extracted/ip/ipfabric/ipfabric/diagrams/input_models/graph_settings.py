import os
from typing import Optional, Union, Literal, Any, Annotated
from uuid import UUID

from pydantic import field_validator, BaseModel, Field, model_serializer, StringConstraints
from pydantic.functional_validators import AfterValidator
from pydantic_extra_types.color import ColorType, Color

from ipfabric.tools.shared import valid_snapshot
from .constants import (
    VALID_DEV_TYPES,
    DEFAULT_NETWORK,
    DEFAULT_PATHLOOKUP,
    VALID_NET_PROTOCOLS,
    VALID_PROTOCOL_LABELS,
    VALID_PATH_PROTOCOLS,
    HIDDEN_DEV_TYPES,
)

PYDANTIC_EXTRAS = os.getenv("IPFABRIC_PYDANTIC_EXTRAS", "allow")


class Style(BaseModel, extra=PYDANTIC_EXTRAS):
    color: Union[ColorType]
    pattern: Annotated[str, AfterValidator(lambda s: s.lower()), StringConstraints(pattern=r'solid|dashed|dotted')] = "solid"
    thicknessThresholds: list[int] = [2, 4, 8]

    @field_validator("color")
    @classmethod
    def _parse_color(cls, v) -> str:
        return Color(v).as_hex()


class LabelsOptions(BaseModel, extra=PYDANTIC_EXTRAS):
    wrapCenterLabel: bool = False
    wrapLinecapLabel: bool = False


class Setting(BaseModel, extra=PYDANTIC_EXTRAS):
    name: str
    style: Style
    type: Literal["protocol", "pathLookupEdge", "group"]
    visible: bool = True
    grouped: bool = True
    id: Optional[UUID] = Field(None, exclude=True)
    labelsOptions: LabelsOptions = Field(default_factory=LabelsOptions)


class EdgeSettings(Setting, BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["protocol", "pathLookupEdge"]
    labels: list[str] = ["protocol"]


class GroupSettings(Setting, BaseModel, extra=PYDANTIC_EXTRAS):
    label: str
    children: list[EdgeSettings]
    type: Literal["group"] = "group"


class PathLookup(BaseModel, extra=PYDANTIC_EXTRAS):
    ignoredTopics: list[Literal['ACL', 'FORWARDING', 'NAT44', 'PBR', 'ZONEFW']] = Field(
        default_factory=list,
        description="List of topics to ignore.  Valid topics are in ['ACL', 'FORWARDING', 'NAT44', 'PBR', 'ZONEFW'].",
    )
    colorDetectedLoops: Optional[bool] = True


class NetworkSettings(BaseModel):
    edges: Optional[list[GroupSettings]] = None
    hiddenDeviceTypes: list[str] = Field(HIDDEN_DEV_TYPES, description="List of device types to hide.")

    def model_post_init(self, __context: Any) -> None:
        if not self.edges:
            self.edges = [GroupSettings(**edge) for edge in DEFAULT_NETWORK]

    @field_validator("hiddenDeviceTypes")
    @classmethod
    def _valid_dev_types(cls, v):
        if v and not all(d in VALID_DEV_TYPES for d in v):
            raise ValueError(f"Device Types '{v}' must be None or in {VALID_DEV_TYPES}.")
        return v

    @staticmethod
    def _update_edge(children: list[EdgeSettings], name: str, attribute: str, bool_value=False):
        for edge in children:
            if edge.name.lower() == name:
                setattr(edge, attribute, bool_value)
                return True
        return False

    def _update_group(self, name: str, attribute: str, group: bool = False, bool_value=False):
        for edge in self.edges:
            if group and isinstance(edge, GroupSettings) and edge.name.lower() == name:
                setattr(edge, attribute, bool_value)
                return True
            elif not group:
                if isinstance(edge, GroupSettings) and self._update_edge(edge.children, name, attribute, bool_value):
                    return self._update_group(edge.name.lower(), "grouped", True)
                elif isinstance(edge, EdgeSettings) and self._update_edge([edge], name, attribute, bool_value):
                    return True
        return False

    def hide_protocol(self, protocol_name: str, unhide: bool = False):
        if protocol_name.lower() in VALID_NET_PROTOCOLS:
            return self._update_group(
                VALID_NET_PROTOCOLS[protocol_name.lower()], attribute="visible", group=False, bool_value=unhide
            )
        else:
            raise KeyError(
                f"Protocol {protocol_name} does not exist.  Valid protocols are {VALID_NET_PROTOCOLS.values()}"
            )

    def hide_all_protocols(self):
        for protocol_name in VALID_NET_PROTOCOLS.values():
            self._update_group(protocol_name, attribute="visible", group=False)

    def ungroup_protocol(self, protocol_name: str):
        if protocol_name.lower() in VALID_NET_PROTOCOLS:
            return self._update_group(VALID_NET_PROTOCOLS[protocol_name.lower()], attribute="grouped", group=False)
        else:
            raise KeyError(
                f"Protocol {protocol_name} does not exist.  Valid protocols are {VALID_NET_PROTOCOLS.values()}"
            )

    def hide_group(self, group_name: str):
        group_names = [g.name.lower() for g in self.edges if isinstance(g, GroupSettings)]
        if group_name.lower() in group_names:
            return self._update_group(group_name.lower(), attribute="visible", group=True)
        else:
            raise KeyError(f"Group {group_name} does not exist.  Valid groups are {group_names}")

    def ungroup_group(self, group_name: str):
        group_names = [g.name.lower() for g in self.edges if isinstance(g, GroupSettings)]
        if group_name.lower() in group_names:
            return self._update_group(group_name.lower(), attribute="grouped", group=True)
        else:
            raise KeyError(f"Group {group_name} does not exist.  Valid groups are {group_names}")

    @staticmethod
    def _proto_label(edge: EdgeSettings, protocol_name: str, label_name: str):
        if edge.name.lower() == protocol_name:
            proto = next(x for x in VALID_PROTOCOL_LABELS[protocol_name].labels if x == label_name)
            if proto.center:
                edge.labels[0] = proto.name
            else:
                edge.labels[1] = proto.name
            return True
        return False

    def change_label(self, protocol_name: str, label_name: str):
        protocol_name, label_name = protocol_name.lower(), label_name.lower()
        if protocol_name not in VALID_NET_PROTOCOLS:
            raise KeyError(
                f"Protocol {protocol_name} does not exist.  Valid protocols are {VALID_NET_PROTOCOLS.values()}"
            )
        else:
            protocol_name = VALID_NET_PROTOCOLS[protocol_name]
        if label_name not in VALID_PROTOCOL_LABELS[protocol_name].labels:
            raise KeyError(
                f"Label {label_name} does not exist for protocol {protocol_name}.  "
                f"Valid labels for {protocol_name} are {VALID_PROTOCOL_LABELS[protocol_name].labels}"
            )
        for edge in self.edges:
            if isinstance(edge, GroupSettings):
                for child in edge.children:
                    if self._proto_label(child, protocol_name, label_name):
                        return True
            if self._proto_label(edge, protocol_name, label_name):
                return True
        return False


class PathLookupSettings(BaseModel):
    edges: Optional[list[EdgeSettings]] = None
    pathLookup: Optional[PathLookup] = Field(default_factory=PathLookup)

    def model_post_init(self, __context: Any) -> None:
        if not self.edges:
            self.edges = [EdgeSettings(**edge) for edge in DEFAULT_PATHLOOKUP]

    @property
    def protocol_priority(self):
        return {edge.name.lower(): idx for idx, edge in enumerate(self.edges)}

    def increase_priority(self, protocol_name: str):
        if protocol_name.lower() not in VALID_PATH_PROTOCOLS:
            raise KeyError(f"Protocol {protocol_name} does not exist.  Valid protocols are {VALID_PATH_PROTOCOLS}")
        current = self.protocol_priority[protocol_name]
        if current != 0:
            self.edges[current], self.edges[current - 1] = self.edges[current - 1], self.edges[current]
        return True

    def decrease_priority(self, protocol_name: str):
        if protocol_name.lower() not in VALID_PATH_PROTOCOLS:
            raise KeyError(f"Protocol {protocol_name} does not exist.  Valid protocols are {VALID_PATH_PROTOCOLS}")
        current = self.protocol_priority[protocol_name]
        if current != len(self.edges) - 1:
            self.edges[current], self.edges[current + 1] = self.edges[current + 1], self.edges[current]
        return True


class Overlay(BaseModel):
    """Set snapshotToCompare or intentRuleId, not both."""

    snapshotToCompare: Optional[Union[UUID, str]] = Field(None, description="Snapshot ID to compare.")
    intentRuleId: Optional[Union[int, str]] = Field(
        None,
        description="Intent Rule ID to overlay. Also valid: ['nonRedundantEdges', 'singlePointsOfFailure']",
    )

    @field_validator("snapshotToCompare")
    @classmethod
    def _valid_snapshot(cls, v):
        return valid_snapshot(v)

    @field_validator("intentRuleId")
    @classmethod
    def valid_intent_rule(cls, v):
        if v and v in ["nonRedundantEdges", "singlePointsOfFailure"]:
            return v
        try:
            return str(int(v))
        except ValueError:
            raise ValueError(f'"{v}" is not an Intent Rule ID or in ["nonRedundantEdges", "singlePointsOfFailure"]')

    @property
    def type(self):
        return "compare" if self.snapshotToCompare else "intent"

    @model_serializer
    def _serialize_overlay(self) -> dict:
        _ = {"intentRuleId": self.intentRuleId} if self.intentRuleId else {"snapshotToCompare": self.snapshotToCompare}
        return dict(type=self.type, **_)
