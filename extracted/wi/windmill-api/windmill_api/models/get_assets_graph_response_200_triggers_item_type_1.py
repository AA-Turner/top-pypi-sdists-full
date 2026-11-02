from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_assets_graph_response_200_triggers_item_type_1_runnable_kind import (
    GetAssetsGraphResponse200TriggersItemType1RunnableKind,
)
from ..models.get_assets_graph_response_200_triggers_item_type_1_trigger_kind import (
    GetAssetsGraphResponse200TriggersItemType1TriggerKind,
)

T = TypeVar("T", bound="GetAssetsGraphResponse200TriggersItemType1")


@_attrs_define
class GetAssetsGraphResponse200TriggersItemType1:
    """Native trigger edge (schedule, email, kafka, ...). `path` is the trigger row's path.

    Attributes:
        trigger_kind (GetAssetsGraphResponse200TriggersItemType1TriggerKind):
        path (str):
        runnable_kind (GetAssetsGraphResponse200TriggersItemType1RunnableKind):
        runnable_path (str):
    """

    trigger_kind: GetAssetsGraphResponse200TriggersItemType1TriggerKind
    path: str
    runnable_kind: GetAssetsGraphResponse200TriggersItemType1RunnableKind
    runnable_path: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trigger_kind = self.trigger_kind.value

        path = self.path
        runnable_kind = self.runnable_kind.value

        runnable_path = self.runnable_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "trigger_kind": trigger_kind,
                "path": path,
                "runnable_kind": runnable_kind,
                "runnable_path": runnable_path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        trigger_kind = GetAssetsGraphResponse200TriggersItemType1TriggerKind(d.pop("trigger_kind"))

        path = d.pop("path")

        runnable_kind = GetAssetsGraphResponse200TriggersItemType1RunnableKind(d.pop("runnable_kind"))

        runnable_path = d.pop("runnable_path")

        get_assets_graph_response_200_triggers_item_type_1 = cls(
            trigger_kind=trigger_kind,
            path=path,
            runnable_kind=runnable_kind,
            runnable_path=runnable_path,
        )

        get_assets_graph_response_200_triggers_item_type_1.additional_properties = d
        return get_assets_graph_response_200_triggers_item_type_1

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
