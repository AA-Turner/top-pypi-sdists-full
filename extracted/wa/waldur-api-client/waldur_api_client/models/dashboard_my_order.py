import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.dashboard_my_order_type_enum import DashboardMyOrderTypeEnum
from ..models.order_state import OrderState

T = TypeVar("T", bound="DashboardMyOrder")


@_attrs_define
class DashboardMyOrder:
    """
    Attributes:
        uuid (UUID):
        offering_uuid (UUID):
        offering_name (str):
        resource_uuid (UUID):
        resource_name (str):
        project_uuid (UUID):
        project_name (str):
        customer_uuid (UUID):
        customer_name (str):
        state (OrderState):
        type_ (DashboardMyOrderTypeEnum):
        created (datetime.datetime):
    """

    uuid: UUID
    offering_uuid: UUID
    offering_name: str
    resource_uuid: UUID
    resource_name: str
    project_uuid: UUID
    project_name: str
    customer_uuid: UUID
    customer_name: str
    state: OrderState
    type_: DashboardMyOrderTypeEnum
    created: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        offering_uuid = str(self.offering_uuid)

        offering_name = self.offering_name

        resource_uuid = str(self.resource_uuid)

        resource_name = self.resource_name

        project_uuid = str(self.project_uuid)

        project_name = self.project_name

        customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        state = self.state.value

        type_ = self.type_.value

        created = self.created.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "offering_uuid": offering_uuid,
                "offering_name": offering_name,
                "resource_uuid": resource_uuid,
                "resource_name": resource_name,
                "project_uuid": project_uuid,
                "project_name": project_name,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
                "state": state,
                "type": type_,
                "created": created,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        offering_uuid = UUID(d.pop("offering_uuid"))

        offering_name = d.pop("offering_name")

        resource_uuid = UUID(d.pop("resource_uuid"))

        resource_name = d.pop("resource_name")

        project_uuid = UUID(d.pop("project_uuid"))

        project_name = d.pop("project_name")

        customer_uuid = UUID(d.pop("customer_uuid"))

        customer_name = d.pop("customer_name")

        state = OrderState(d.pop("state"))

        type_ = DashboardMyOrderTypeEnum(d.pop("type"))

        created = isoparse(d.pop("created"))

        dashboard_my_order = cls(
            uuid=uuid,
            offering_uuid=offering_uuid,
            offering_name=offering_name,
            resource_uuid=resource_uuid,
            resource_name=resource_name,
            project_uuid=project_uuid,
            project_name=project_name,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            state=state,
            type_=type_,
            created=created,
        )

        dashboard_my_order.additional_properties = d
        return dashboard_my_order

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
