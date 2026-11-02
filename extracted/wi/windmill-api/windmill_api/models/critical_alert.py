import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CriticalAlert")


@_attrs_define
class CriticalAlert:
    """
    Attributes:
        id (Union[Unset, int]): Unique identifier for the alert
        alert_type (Union[Unset, str]): Type of alert (e.g., critical_error)
        message (Union[Unset, str]): The message content of the alert
        created_at (Union[Unset, datetime.datetime]): Time when the alert was created
        acknowledged (Union[Unset, None, bool]): Acknowledgment status of the alert, can be true, false, or null if not
            set
        workspace_id (Union[Unset, None, str]): Workspace id if the alert is in the scope of a workspace
    """

    id: Union[Unset, int] = UNSET
    alert_type: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    acknowledged: Union[Unset, None, bool] = UNSET
    workspace_id: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        alert_type = self.alert_type
        message = self.message
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        acknowledged = self.acknowledged
        workspace_id = self.workspace_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if alert_type is not UNSET:
            field_dict["alert_type"] = alert_type
        if message is not UNSET:
            field_dict["message"] = message
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if acknowledged is not UNSET:
            field_dict["acknowledged"] = acknowledged
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        alert_type = d.pop("alert_type", UNSET)

        message = d.pop("message", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        acknowledged = d.pop("acknowledged", UNSET)

        workspace_id = d.pop("workspace_id", UNSET)

        critical_alert = cls(
            id=id,
            alert_type=alert_type,
            message=message,
            created_at=created_at,
            acknowledged=acknowledged,
            workspace_id=workspace_id,
        )

        critical_alert.additional_properties = d
        return critical_alert

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
