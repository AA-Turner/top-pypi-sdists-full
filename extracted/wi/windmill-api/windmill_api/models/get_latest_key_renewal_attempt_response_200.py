import datetime
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="GetLatestKeyRenewalAttemptResponse200")


@_attrs_define
class GetLatestKeyRenewalAttemptResponse200:
    """
    Attributes:
        result (str):
        attempted_at (datetime.datetime):
    """

    result: str
    attempted_at: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        result = self.result
        attempted_at = self.attempted_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "result": result,
                "attempted_at": attempted_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        result = d.pop("result")

        attempted_at = isoparse(d.pop("attempted_at"))

        get_latest_key_renewal_attempt_response_200 = cls(
            result=result,
            attempted_at=attempted_at,
        )

        get_latest_key_renewal_attempt_response_200.additional_properties = d
        return get_latest_key_renewal_attempt_response_200

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
