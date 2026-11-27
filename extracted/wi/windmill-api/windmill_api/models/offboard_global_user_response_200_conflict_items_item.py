from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OffboardGlobalUserResponse200ConflictItemsItem")


@_attrs_define
class OffboardGlobalUserResponse200ConflictItemsItem:
    """
    Attributes:
        workspace_id (str):
        kind (str): Item kind, as its table name (script, flow, app, resource, variable, schedule, eval_dataset,
            http_trigger, ...)
        source_path (str): The offboarded user's item, under u/{username}/
        target_path (str): The existing item at the reassignment target
    """

    workspace_id: str
    kind: str
    source_path: str
    target_path: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workspace_id = self.workspace_id
        kind = self.kind
        source_path = self.source_path
        target_path = self.target_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workspace_id": workspace_id,
                "kind": kind,
                "source_path": source_path,
                "target_path": target_path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workspace_id = d.pop("workspace_id")

        kind = d.pop("kind")

        source_path = d.pop("source_path")

        target_path = d.pop("target_path")

        offboard_global_user_response_200_conflict_items_item = cls(
            workspace_id=workspace_id,
            kind=kind,
            source_path=source_path,
            target_path=target_path,
        )

        offboard_global_user_response_200_conflict_items_item.additional_properties = d
        return offboard_global_user_response_200_conflict_items_item

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
