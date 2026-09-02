from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SetPublicAppRateLimitJsonBody")


@_attrs_define
class SetPublicAppRateLimitJsonBody:
    """
    Attributes:
        public_app_execution_limit_per_minute (Union[Unset, int]): Rate limit for public app executions per minute per
            server. NULL or 0 to disable. Example: 100.
    """

    public_app_execution_limit_per_minute: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        public_app_execution_limit_per_minute = self.public_app_execution_limit_per_minute

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if public_app_execution_limit_per_minute is not UNSET:
            field_dict["public_app_execution_limit_per_minute"] = public_app_execution_limit_per_minute

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        public_app_execution_limit_per_minute = d.pop("public_app_execution_limit_per_minute", UNSET)

        set_public_app_rate_limit_json_body = cls(
            public_app_execution_limit_per_minute=public_app_execution_limit_per_minute,
        )

        set_public_app_rate_limit_json_body.additional_properties = d
        return set_public_app_rate_limit_json_body

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
