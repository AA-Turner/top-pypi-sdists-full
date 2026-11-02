from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetSlackAgentsStatusResponse200")


@_attrs_define
class GetSlackAgentsStatusResponse200:
    """
    Attributes:
        signing_secret_set (bool): agents answer in Slack only when the server has the Slack app's signing secret
            (SLACK_SIGNING_SECRET)
    """

    signing_secret_set: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        signing_secret_set = self.signing_secret_set

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "signing_secret_set": signing_secret_set,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        signing_secret_set = d.pop("signing_secret_set")

        get_slack_agents_status_response_200 = cls(
            signing_secret_set=signing_secret_set,
        )

        get_slack_agents_status_response_200.additional_properties = d
        return get_slack_agents_status_response_200

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
