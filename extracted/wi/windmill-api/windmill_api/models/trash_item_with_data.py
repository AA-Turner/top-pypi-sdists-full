import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.trash_item_with_data_item_data import TrashItemWithDataItemData


T = TypeVar("T", bound="TrashItemWithData")


@_attrs_define
class TrashItemWithData:
    """
    Attributes:
        id (int):
        workspace_id (str):
        item_kind (str): script, flow, app, schedule, variable, resource, or a trigger kind such as http_trigger
        item_path (str):
        deleted_by (str):
        deleted_at (datetime.datetime):
        expires_at (datetime.datetime): when the item is permanently deleted unless restored first
        item_data (TrashItemWithDataItemData): the deleted rows as they were stored; the shape depends on the kind, and
            a secret variable's value stays encrypted
    """

    id: int
    workspace_id: str
    item_kind: str
    item_path: str
    deleted_by: str
    deleted_at: datetime.datetime
    expires_at: datetime.datetime
    item_data: "TrashItemWithDataItemData"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        workspace_id = self.workspace_id
        item_kind = self.item_kind
        item_path = self.item_path
        deleted_by = self.deleted_by
        deleted_at = self.deleted_at.isoformat()

        expires_at = self.expires_at.isoformat()

        item_data = self.item_data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "workspace_id": workspace_id,
                "item_kind": item_kind,
                "item_path": item_path,
                "deleted_by": deleted_by,
                "deleted_at": deleted_at,
                "expires_at": expires_at,
                "item_data": item_data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.trash_item_with_data_item_data import TrashItemWithDataItemData

        d = src_dict.copy()
        id = d.pop("id")

        workspace_id = d.pop("workspace_id")

        item_kind = d.pop("item_kind")

        item_path = d.pop("item_path")

        deleted_by = d.pop("deleted_by")

        deleted_at = isoparse(d.pop("deleted_at"))

        expires_at = isoparse(d.pop("expires_at"))

        item_data = TrashItemWithDataItemData.from_dict(d.pop("item_data"))

        trash_item_with_data = cls(
            id=id,
            workspace_id=workspace_id,
            item_kind=item_kind,
            item_path=item_path,
            deleted_by=deleted_by,
            deleted_at=deleted_at,
            expires_at=expires_at,
            item_data=item_data,
        )

        trash_item_with_data.additional_properties = d
        return trash_item_with_data

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
