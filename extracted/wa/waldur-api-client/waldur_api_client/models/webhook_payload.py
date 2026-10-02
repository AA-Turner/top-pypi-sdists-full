from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WebhookPayload")


@_attrs_define
class WebhookPayload:
    """
    Attributes:
        event_type (str):
        issue_backend_id (Union[Unset, str]):
        comment (Union[Unset, str]):
        new_status (Union[Unset, str]):
    """

    event_type: str
    issue_backend_id: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    new_status: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        event_type = self.event_type

        issue_backend_id = self.issue_backend_id

        comment = self.comment

        new_status = self.new_status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "event_type": event_type,
            }
        )
        if issue_backend_id is not UNSET:
            field_dict["issue_backend_id"] = issue_backend_id
        if comment is not UNSET:
            field_dict["comment"] = comment
        if new_status is not UNSET:
            field_dict["new_status"] = new_status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        event_type = d.pop("event_type")

        issue_backend_id = d.pop("issue_backend_id", UNSET)

        comment = d.pop("comment", UNSET)

        new_status = d.pop("new_status", UNSET)

        webhook_payload = cls(
            event_type=event_type,
            issue_backend_id=issue_backend_id,
            comment=comment,
            new_status=new_status,
        )

        webhook_payload.additional_properties = d
        return webhook_payload

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
