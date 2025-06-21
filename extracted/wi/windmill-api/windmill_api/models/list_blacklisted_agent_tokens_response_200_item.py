import datetime
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ListBlacklistedAgentTokensResponse200Item")


@_attrs_define
class ListBlacklistedAgentTokensResponse200Item:
    """
    Attributes:
        token (str): The blacklisted token (without prefix)
        expires_at (datetime.datetime): When the blacklist entry expires
        blacklisted_at (datetime.datetime): When the token was blacklisted
        blacklisted_by (str): Email of the user who blacklisted the token
    """

    token: str
    expires_at: datetime.datetime
    blacklisted_at: datetime.datetime
    blacklisted_by: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        token = self.token
        expires_at = self.expires_at.isoformat()

        blacklisted_at = self.blacklisted_at.isoformat()

        blacklisted_by = self.blacklisted_by

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "token": token,
                "expires_at": expires_at,
                "blacklisted_at": blacklisted_at,
                "blacklisted_by": blacklisted_by,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        token = d.pop("token")

        expires_at = isoparse(d.pop("expires_at"))

        blacklisted_at = isoparse(d.pop("blacklisted_at"))

        blacklisted_by = d.pop("blacklisted_by")

        list_blacklisted_agent_tokens_response_200_item = cls(
            token=token,
            expires_at=expires_at,
            blacklisted_at=blacklisted_at,
            blacklisted_by=blacklisted_by,
        )

        list_blacklisted_agent_tokens_response_200_item.additional_properties = d
        return list_blacklisted_agent_tokens_response_200_item

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
