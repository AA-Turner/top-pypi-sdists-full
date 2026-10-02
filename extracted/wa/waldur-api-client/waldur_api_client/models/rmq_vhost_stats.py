from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.rmq_queue_stats import RmqQueueStats
    from ..models.rmq_stats_user import RmqStatsUser


T = TypeVar("T", bound="RmqVhostStats")


@_attrs_define
class RmqVhostStats:
    """
    Attributes:
        name (str): Virtual host name (corresponds to Waldur user UUID)
        user (Union['RmqStatsUser', None]): Waldur user associated with this vhost
        queues (list['RmqQueueStats']): List of subscription queues in this vhost
        total_messages (int): Total messages across all queues in this vhost
    """

    name: str
    user: Union["RmqStatsUser", None]
    queues: list["RmqQueueStats"]
    total_messages: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.rmq_stats_user import RmqStatsUser

        name = self.name

        user: Union[None, dict[str, Any]]
        if isinstance(self.user, RmqStatsUser):
            user = self.user.to_dict()
        else:
            user = self.user

        queues = []
        for queues_item_data in self.queues:
            queues_item = queues_item_data.to_dict()
            queues.append(queues_item)

        total_messages = self.total_messages

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "user": user,
                "queues": queues,
                "total_messages": total_messages,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rmq_queue_stats import RmqQueueStats
        from ..models.rmq_stats_user import RmqStatsUser

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_user(data: object) -> Union["RmqStatsUser", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                user_type_1 = RmqStatsUser.from_dict(data)

                return user_type_1
            except:  # noqa: E722
                pass
            return cast(Union["RmqStatsUser", None], data)

        user = _parse_user(d.pop("user"))

        queues = []
        _queues = d.pop("queues")
        for queues_item_data in _queues:
            queues_item = RmqQueueStats.from_dict(queues_item_data)

            queues.append(queues_item)

        total_messages = d.pop("total_messages")

        rmq_vhost_stats = cls(
            name=name,
            user=user,
            queues=queues,
            total_messages=total_messages,
        )

        rmq_vhost_stats.additional_properties = d
        return rmq_vhost_stats

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
