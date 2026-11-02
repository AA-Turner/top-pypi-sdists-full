from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_assets_graph_response_200_triggers_item_type_0_asset_kind import (
    GetAssetsGraphResponse200TriggersItemType0AssetKind,
)
from ..models.get_assets_graph_response_200_triggers_item_type_0_runnable_kind import (
    GetAssetsGraphResponse200TriggersItemType0RunnableKind,
)
from ..models.get_assets_graph_response_200_triggers_item_type_0_trigger_kind import (
    GetAssetsGraphResponse200TriggersItemType0TriggerKind,
)

T = TypeVar("T", bound="GetAssetsGraphResponse200TriggersItemType0")


@_attrs_define
class GetAssetsGraphResponse200TriggersItemType0:
    """Asset trigger edge (`// on <asset>`)

    Attributes:
        trigger_kind (GetAssetsGraphResponse200TriggersItemType0TriggerKind):
        asset_kind (GetAssetsGraphResponse200TriggersItemType0AssetKind):
        asset_path (str):
        runnable_kind (GetAssetsGraphResponse200TriggersItemType0RunnableKind):
        runnable_path (str):
    """

    trigger_kind: GetAssetsGraphResponse200TriggersItemType0TriggerKind
    asset_kind: GetAssetsGraphResponse200TriggersItemType0AssetKind
    asset_path: str
    runnable_kind: GetAssetsGraphResponse200TriggersItemType0RunnableKind
    runnable_path: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trigger_kind = self.trigger_kind.value

        asset_kind = self.asset_kind.value

        asset_path = self.asset_path
        runnable_kind = self.runnable_kind.value

        runnable_path = self.runnable_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "trigger_kind": trigger_kind,
                "asset_kind": asset_kind,
                "asset_path": asset_path,
                "runnable_kind": runnable_kind,
                "runnable_path": runnable_path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        trigger_kind = GetAssetsGraphResponse200TriggersItemType0TriggerKind(d.pop("trigger_kind"))

        asset_kind = GetAssetsGraphResponse200TriggersItemType0AssetKind(d.pop("asset_kind"))

        asset_path = d.pop("asset_path")

        runnable_kind = GetAssetsGraphResponse200TriggersItemType0RunnableKind(d.pop("runnable_kind"))

        runnable_path = d.pop("runnable_path")

        get_assets_graph_response_200_triggers_item_type_0 = cls(
            trigger_kind=trigger_kind,
            asset_kind=asset_kind,
            asset_path=asset_path,
            runnable_kind=runnable_kind,
            runnable_path=runnable_path,
        )

        get_assets_graph_response_200_triggers_item_type_0.additional_properties = d
        return get_assets_graph_response_200_triggers_item_type_0

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
