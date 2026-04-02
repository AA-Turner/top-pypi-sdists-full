from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.rmq_subscription import RmqSubscription
    from ..models.rmq_waldur_user import RmqWaldurUser


T = TypeVar("T", bound="RmqVHostStatsItem")


@_attrs_define
class RmqVHostStatsItem:
    """
    Attributes:
        name (str):
        waldur_user (RmqWaldurUser):
        subscriptions (list['RmqSubscription']):
    """

    name: str
    waldur_user: "RmqWaldurUser"
    subscriptions: list["RmqSubscription"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        waldur_user = self.waldur_user.to_dict()

        subscriptions = []
        for subscriptions_item_data in self.subscriptions:
            subscriptions_item = subscriptions_item_data.to_dict()
            subscriptions.append(subscriptions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "waldur_user": waldur_user,
                "subscriptions": subscriptions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rmq_subscription import RmqSubscription
        from ..models.rmq_waldur_user import RmqWaldurUser

        d = dict(src_dict)
        name = d.pop("name")

        waldur_user = RmqWaldurUser.from_dict(d.pop("waldur_user"))

        subscriptions = []
        _subscriptions = d.pop("subscriptions")
        for subscriptions_item_data in _subscriptions:
            subscriptions_item = RmqSubscription.from_dict(subscriptions_item_data)

            subscriptions.append(subscriptions_item)

        rmq_v_host_stats_item = cls(
            name=name,
            waldur_user=waldur_user,
            subscriptions=subscriptions,
        )

        rmq_v_host_stats_item.additional_properties = d
        return rmq_v_host_stats_item

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
