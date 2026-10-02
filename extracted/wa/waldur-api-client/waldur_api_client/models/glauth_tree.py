from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.glauth_tree_group import GlauthTreeGroup
    from ..models.glauth_tree_offering import GlauthTreeOffering
    from ..models.glauth_tree_robot_account import GlauthTreeRobotAccount
    from ..models.glauth_tree_user import GlauthTreeUser


T = TypeVar("T", bound="GlauthTree")


@_attrs_define
class GlauthTree:
    """
    Attributes:
        offering (GlauthTreeOffering):
        groups (list['GlauthTreeGroup']):
        users (list['GlauthTreeUser']):
        robot_accounts (list['GlauthTreeRobotAccount']):
    """

    offering: "GlauthTreeOffering"
    groups: list["GlauthTreeGroup"]
    users: list["GlauthTreeUser"]
    robot_accounts: list["GlauthTreeRobotAccount"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering = self.offering.to_dict()

        groups = []
        for groups_item_data in self.groups:
            groups_item = groups_item_data.to_dict()
            groups.append(groups_item)

        users = []
        for users_item_data in self.users:
            users_item = users_item_data.to_dict()
            users.append(users_item)

        robot_accounts = []
        for robot_accounts_item_data in self.robot_accounts:
            robot_accounts_item = robot_accounts_item_data.to_dict()
            robot_accounts.append(robot_accounts_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering": offering,
                "groups": groups,
                "users": users,
                "robot_accounts": robot_accounts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.glauth_tree_group import GlauthTreeGroup
        from ..models.glauth_tree_offering import GlauthTreeOffering
        from ..models.glauth_tree_robot_account import GlauthTreeRobotAccount
        from ..models.glauth_tree_user import GlauthTreeUser

        d = dict(src_dict)
        offering = GlauthTreeOffering.from_dict(d.pop("offering"))

        groups = []
        _groups = d.pop("groups")
        for groups_item_data in _groups:
            groups_item = GlauthTreeGroup.from_dict(groups_item_data)

            groups.append(groups_item)

        users = []
        _users = d.pop("users")
        for users_item_data in _users:
            users_item = GlauthTreeUser.from_dict(users_item_data)

            users.append(users_item)

        robot_accounts = []
        _robot_accounts = d.pop("robot_accounts")
        for robot_accounts_item_data in _robot_accounts:
            robot_accounts_item = GlauthTreeRobotAccount.from_dict(robot_accounts_item_data)

            robot_accounts.append(robot_accounts_item)

        glauth_tree = cls(
            offering=offering,
            groups=groups,
            users=users,
            robot_accounts=robot_accounts,
        )

        glauth_tree.additional_properties = d
        return glauth_tree

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
