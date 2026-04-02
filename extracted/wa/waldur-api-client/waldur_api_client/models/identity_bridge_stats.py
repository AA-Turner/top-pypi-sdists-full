from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.identity_manager import IdentityManager
    from ..models.isd_user_count import ISDUserCount


T = TypeVar("T", bound="IdentityBridgeStats")


@_attrs_define
class IdentityBridgeStats:
    """
    Attributes:
        enabled (bool):
        deactivation_policy (str):
        allowed_attributes (list[str]):
        total_federated_users (int):
        total_active_federated_users (int):
        users_per_isd (list['ISDUserCount']):
        stale_threshold_days (int):
        identity_managers (list['IdentityManager']):
    """

    enabled: bool
    deactivation_policy: str
    allowed_attributes: list[str]
    total_federated_users: int
    total_active_federated_users: int
    users_per_isd: list["ISDUserCount"]
    stale_threshold_days: int
    identity_managers: list["IdentityManager"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        deactivation_policy = self.deactivation_policy

        allowed_attributes = self.allowed_attributes

        total_federated_users = self.total_federated_users

        total_active_federated_users = self.total_active_federated_users

        users_per_isd = []
        for users_per_isd_item_data in self.users_per_isd:
            users_per_isd_item = users_per_isd_item_data.to_dict()
            users_per_isd.append(users_per_isd_item)

        stale_threshold_days = self.stale_threshold_days

        identity_managers = []
        for identity_managers_item_data in self.identity_managers:
            identity_managers_item = identity_managers_item_data.to_dict()
            identity_managers.append(identity_managers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
                "deactivation_policy": deactivation_policy,
                "allowed_attributes": allowed_attributes,
                "total_federated_users": total_federated_users,
                "total_active_federated_users": total_active_federated_users,
                "users_per_isd": users_per_isd,
                "stale_threshold_days": stale_threshold_days,
                "identity_managers": identity_managers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.identity_manager import IdentityManager
        from ..models.isd_user_count import ISDUserCount

        d = dict(src_dict)
        enabled = d.pop("enabled")

        deactivation_policy = d.pop("deactivation_policy")

        allowed_attributes = cast(list[str], d.pop("allowed_attributes"))

        total_federated_users = d.pop("total_federated_users")

        total_active_federated_users = d.pop("total_active_federated_users")

        users_per_isd = []
        _users_per_isd = d.pop("users_per_isd")
        for users_per_isd_item_data in _users_per_isd:
            users_per_isd_item = ISDUserCount.from_dict(users_per_isd_item_data)

            users_per_isd.append(users_per_isd_item)

        stale_threshold_days = d.pop("stale_threshold_days")

        identity_managers = []
        _identity_managers = d.pop("identity_managers")
        for identity_managers_item_data in _identity_managers:
            identity_managers_item = IdentityManager.from_dict(identity_managers_item_data)

            identity_managers.append(identity_managers_item)

        identity_bridge_stats = cls(
            enabled=enabled,
            deactivation_policy=deactivation_policy,
            allowed_attributes=allowed_attributes,
            total_federated_users=total_federated_users,
            total_active_federated_users=total_active_federated_users,
            users_per_isd=users_per_isd,
            stale_threshold_days=stale_threshold_days,
            identity_managers=identity_managers,
        )

        identity_bridge_stats.additional_properties = d
        return identity_bridge_stats

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
