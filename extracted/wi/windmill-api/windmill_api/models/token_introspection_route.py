from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TokenIntrospectionRoute")


@_attrs_define
class TokenIntrospectionRoute:
    """
    Attributes:
        method (str):
        path (str):
        allowed (bool):
        reason (Union[Unset, str]): why the route layer refuses the token, when it does
    """

    method: str
    path: str
    allowed: bool
    reason: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        method = self.method
        path = self.path
        allowed = self.allowed
        reason = self.reason

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "method": method,
                "path": path,
                "allowed": allowed,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        method = d.pop("method")

        path = d.pop("path")

        allowed = d.pop("allowed")

        reason = d.pop("reason", UNSET)

        token_introspection_route = cls(
            method=method,
            path=path,
            allowed=allowed,
            reason=reason,
        )

        token_introspection_route.additional_properties = d
        return token_introspection_route

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
