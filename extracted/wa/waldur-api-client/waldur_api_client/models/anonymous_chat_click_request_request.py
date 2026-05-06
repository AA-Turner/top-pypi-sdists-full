from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AnonymousChatClickRequestRequest")


@_attrs_define
class AnonymousChatClickRequestRequest:
    """
    Attributes:
        interaction_uuid (UUID): UUID of the interaction this click belongs to.
        feedback_token (str): HMAC-bound bearer issued in the streaming `m` frame (same as /feedback/).
        offering_uuid (UUID): UUID of the clicked offering. Must appear in the parent interaction's recommended set,
            else 400.
    """

    interaction_uuid: UUID
    feedback_token: str
    offering_uuid: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        interaction_uuid = str(self.interaction_uuid)

        feedback_token = self.feedback_token

        offering_uuid = str(self.offering_uuid)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "interaction_uuid": interaction_uuid,
                "feedback_token": feedback_token,
                "offering_uuid": offering_uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        interaction_uuid = UUID(d.pop("interaction_uuid"))

        feedback_token = d.pop("feedback_token")

        offering_uuid = UUID(d.pop("offering_uuid"))

        anonymous_chat_click_request_request = cls(
            interaction_uuid=interaction_uuid,
            feedback_token=feedback_token,
            offering_uuid=offering_uuid,
        )

        anonymous_chat_click_request_request.additional_properties = d
        return anonymous_chat_click_request_request

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
