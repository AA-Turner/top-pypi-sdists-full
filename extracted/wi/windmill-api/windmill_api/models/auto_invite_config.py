from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auto_invite_config_mode import AutoInviteConfigMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.auto_invite_config_instance_groups_roles import AutoInviteConfigInstanceGroupsRoles


T = TypeVar("T", bound="AutoInviteConfig")


@_attrs_define
class AutoInviteConfig:
    """Configuration for auto-inviting users to the workspace

    Attributes:
        enabled (Union[Unset, bool]):
        domain (Union[Unset, str]):
        operator (Union[Unset, bool]): If true, auto-invited users are added as operators. If false, they are added as
            developers.
        mode (Union[Unset, AutoInviteConfigMode]):  Default: AutoInviteConfigMode.INVITE.
        instance_groups (Union[Unset, List[str]]):
        instance_groups_roles (Union[Unset, AutoInviteConfigInstanceGroupsRoles]):
    """

    enabled: Union[Unset, bool] = False
    domain: Union[Unset, str] = UNSET
    operator: Union[Unset, bool] = False
    mode: Union[Unset, AutoInviteConfigMode] = AutoInviteConfigMode.INVITE
    instance_groups: Union[Unset, List[str]] = UNSET
    instance_groups_roles: Union[Unset, "AutoInviteConfigInstanceGroupsRoles"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        enabled = self.enabled
        domain = self.domain
        operator = self.operator
        mode: Union[Unset, str] = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        instance_groups: Union[Unset, List[str]] = UNSET
        if not isinstance(self.instance_groups, Unset):
            instance_groups = self.instance_groups

        instance_groups_roles: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.instance_groups_roles, Unset):
            instance_groups_roles = self.instance_groups_roles.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if domain is not UNSET:
            field_dict["domain"] = domain
        if operator is not UNSET:
            field_dict["operator"] = operator
        if mode is not UNSET:
            field_dict["mode"] = mode
        if instance_groups is not UNSET:
            field_dict["instance_groups"] = instance_groups
        if instance_groups_roles is not UNSET:
            field_dict["instance_groups_roles"] = instance_groups_roles

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.auto_invite_config_instance_groups_roles import AutoInviteConfigInstanceGroupsRoles

        d = src_dict.copy()
        enabled = d.pop("enabled", UNSET)

        domain = d.pop("domain", UNSET)

        operator = d.pop("operator", UNSET)

        _mode = d.pop("mode", UNSET)
        mode: Union[Unset, AutoInviteConfigMode]
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = AutoInviteConfigMode(_mode)

        instance_groups = cast(List[str], d.pop("instance_groups", UNSET))

        _instance_groups_roles = d.pop("instance_groups_roles", UNSET)
        instance_groups_roles: Union[Unset, AutoInviteConfigInstanceGroupsRoles]
        if isinstance(_instance_groups_roles, Unset):
            instance_groups_roles = UNSET
        else:
            instance_groups_roles = AutoInviteConfigInstanceGroupsRoles.from_dict(_instance_groups_roles)

        auto_invite_config = cls(
            enabled=enabled,
            domain=domain,
            operator=operator,
            mode=mode,
            instance_groups=instance_groups,
            instance_groups_roles=instance_groups_roles,
        )

        auto_invite_config.additional_properties = d
        return auto_invite_config

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
