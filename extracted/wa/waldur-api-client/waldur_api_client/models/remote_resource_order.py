from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.order_state import OrderState
from ..models.remote_resource_order_remote_state_enum import RemoteResourceOrderRemoteStateEnum
from ..models.sync_status_enum import SyncStatusEnum

T = TypeVar("T", bound="RemoteResourceOrder")


@_attrs_define
class RemoteResourceOrder:
    """
    Attributes:
        order_uuid (UUID): Order UUID
        remote_state (RemoteResourceOrderRemoteStateEnum):
        local_state (OrderState):
        sync_status (SyncStatusEnum):
    """

    order_uuid: UUID
    remote_state: RemoteResourceOrderRemoteStateEnum
    local_state: OrderState
    sync_status: SyncStatusEnum
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        order_uuid = str(self.order_uuid)

        remote_state = self.remote_state.value

        local_state = self.local_state.value

        sync_status = self.sync_status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "order_uuid": order_uuid,
                "remote_state": remote_state,
                "local_state": local_state,
                "sync_status": sync_status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        order_uuid = UUID(d.pop("order_uuid"))

        remote_state = RemoteResourceOrderRemoteStateEnum(d.pop("remote_state"))

        local_state = OrderState(d.pop("local_state"))

        sync_status = SyncStatusEnum(d.pop("sync_status"))

        remote_resource_order = cls(
            order_uuid=order_uuid,
            remote_state=remote_state,
            local_state=local_state,
            sync_status=sync_status,
        )

        remote_resource_order.additional_properties = d
        return remote_resource_order

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
