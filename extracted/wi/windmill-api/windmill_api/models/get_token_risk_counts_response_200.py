from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetTokenRiskCountsResponse200")


@_attrs_define
class GetTokenRiskCountsResponse200:
    """
    Attributes:
        superadmin (int):
        admin (int):
        all_workspaces (int):
        never_expires (int):
        unused (int):
    """

    superadmin: int
    admin: int
    all_workspaces: int
    never_expires: int
    unused: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        superadmin = self.superadmin
        admin = self.admin
        all_workspaces = self.all_workspaces
        never_expires = self.never_expires
        unused = self.unused

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "superadmin": superadmin,
                "admin": admin,
                "all_workspaces": all_workspaces,
                "never_expires": never_expires,
                "unused": unused,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        superadmin = d.pop("superadmin")

        admin = d.pop("admin")

        all_workspaces = d.pop("all_workspaces")

        never_expires = d.pop("never_expires")

        unused = d.pop("unused")

        get_token_risk_counts_response_200 = cls(
            superadmin=superadmin,
            admin=admin,
            all_workspaces=all_workspaces,
            never_expires=never_expires,
            unused=unused,
        )

        get_token_risk_counts_response_200.additional_properties = d
        return get_token_risk_counts_response_200

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
