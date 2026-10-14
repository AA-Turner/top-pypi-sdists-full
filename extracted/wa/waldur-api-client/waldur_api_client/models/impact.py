from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.impact_affected_resources import ImpactAffectedResources
    from ..models.impact_affected_users import ImpactAffectedUsers


T = TypeVar("T", bound="Impact")


@_attrs_define
class Impact:
    """
    Attributes:
        risk (str):
        affected_scope (Union[Unset, str]):
        affected_resources (Union[Unset, ImpactAffectedResources]):
        affected_users (Union[Unset, ImpactAffectedUsers]):
    """

    risk: str
    affected_scope: Union[Unset, str] = UNSET
    affected_resources: Union[Unset, "ImpactAffectedResources"] = UNSET
    affected_users: Union[Unset, "ImpactAffectedUsers"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        risk = self.risk

        affected_scope = self.affected_scope

        affected_resources: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.affected_resources, Unset):
            affected_resources = self.affected_resources.to_dict()

        affected_users: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.affected_users, Unset):
            affected_users = self.affected_users.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "risk": risk,
            }
        )
        if affected_scope is not UNSET:
            field_dict["affected_scope"] = affected_scope
        if affected_resources is not UNSET:
            field_dict["affected_resources"] = affected_resources
        if affected_users is not UNSET:
            field_dict["affected_users"] = affected_users

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.impact_affected_resources import ImpactAffectedResources
        from ..models.impact_affected_users import ImpactAffectedUsers

        d = dict(src_dict)
        risk = d.pop("risk")

        affected_scope = d.pop("affected_scope", UNSET)

        _affected_resources = d.pop("affected_resources", UNSET)
        affected_resources: Union[Unset, ImpactAffectedResources]
        if isinstance(_affected_resources, Unset):
            affected_resources = UNSET
        else:
            affected_resources = ImpactAffectedResources.from_dict(_affected_resources)

        _affected_users = d.pop("affected_users", UNSET)
        affected_users: Union[Unset, ImpactAffectedUsers]
        if isinstance(_affected_users, Unset):
            affected_users = UNSET
        else:
            affected_users = ImpactAffectedUsers.from_dict(_affected_users)

        impact = cls(
            risk=risk,
            affected_scope=affected_scope,
            affected_resources=affected_resources,
            affected_users=affected_users,
        )

        impact.additional_properties = d
        return impact

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
