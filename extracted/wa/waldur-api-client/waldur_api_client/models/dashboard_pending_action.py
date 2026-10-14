import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.variant_enum import VariantEnum

if TYPE_CHECKING:
    from ..models.corrective_action import CorrectiveAction
    from ..models.dashboard_pending_action_route_params import DashboardPendingActionRouteParams


T = TypeVar("T", bound="DashboardPendingAction")


@_attrs_define
class DashboardPendingAction:
    """
    Attributes:
        type_ (str):
        title (str):
        description (str):
        variant (VariantEnum):
        deadline (Union[None, datetime.datetime]):
        count (Union[None, int]):
        target_uuid (Union[None, UUID]):
        customer_uuid (Union[None, UUID]):
        uuid (Union[None, UUID]):
        urgency (Union[None, str]):
        route_name (Union[None, str]):
        route_params (DashboardPendingActionRouteParams):
        can_silence (bool):
        actions (list['CorrectiveAction']):
    """

    type_: str
    title: str
    description: str
    variant: VariantEnum
    deadline: Union[None, datetime.datetime]
    count: Union[None, int]
    target_uuid: Union[None, UUID]
    customer_uuid: Union[None, UUID]
    uuid: Union[None, UUID]
    urgency: Union[None, str]
    route_name: Union[None, str]
    route_params: "DashboardPendingActionRouteParams"
    can_silence: bool
    actions: list["CorrectiveAction"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        title = self.title

        description = self.description

        variant = self.variant.value

        deadline: Union[None, str]
        if isinstance(self.deadline, datetime.datetime):
            deadline = self.deadline.isoformat()
        else:
            deadline = self.deadline

        count: Union[None, int]
        count = self.count

        target_uuid: Union[None, str]
        if isinstance(self.target_uuid, UUID):
            target_uuid = str(self.target_uuid)
        else:
            target_uuid = self.target_uuid

        customer_uuid: Union[None, str]
        if isinstance(self.customer_uuid, UUID):
            customer_uuid = str(self.customer_uuid)
        else:
            customer_uuid = self.customer_uuid

        uuid: Union[None, str]
        if isinstance(self.uuid, UUID):
            uuid = str(self.uuid)
        else:
            uuid = self.uuid

        urgency: Union[None, str]
        urgency = self.urgency

        route_name: Union[None, str]
        route_name = self.route_name

        route_params = self.route_params.to_dict()

        can_silence = self.can_silence

        actions = []
        for actions_item_data in self.actions:
            actions_item = actions_item_data.to_dict()
            actions.append(actions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "title": title,
                "description": description,
                "variant": variant,
                "deadline": deadline,
                "count": count,
                "target_uuid": target_uuid,
                "customer_uuid": customer_uuid,
                "uuid": uuid,
                "urgency": urgency,
                "route_name": route_name,
                "route_params": route_params,
                "can_silence": can_silence,
                "actions": actions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.corrective_action import CorrectiveAction
        from ..models.dashboard_pending_action_route_params import DashboardPendingActionRouteParams

        d = dict(src_dict)
        type_ = d.pop("type")

        title = d.pop("title")

        description = d.pop("description")

        variant = VariantEnum(d.pop("variant"))

        def _parse_deadline(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deadline_type_0 = isoparse(data)

                return deadline_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        deadline = _parse_deadline(d.pop("deadline"))

        def _parse_count(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        count = _parse_count(d.pop("count"))

        def _parse_target_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                target_uuid_type_0 = UUID(data)

                return target_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        target_uuid = _parse_target_uuid(d.pop("target_uuid"))

        def _parse_customer_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                customer_uuid_type_0 = UUID(data)

                return customer_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        customer_uuid = _parse_customer_uuid(d.pop("customer_uuid"))

        def _parse_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                uuid_type_0 = UUID(data)

                return uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        uuid = _parse_uuid(d.pop("uuid"))

        def _parse_urgency(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        urgency = _parse_urgency(d.pop("urgency"))

        def _parse_route_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        route_name = _parse_route_name(d.pop("route_name"))

        route_params = DashboardPendingActionRouteParams.from_dict(d.pop("route_params"))

        can_silence = d.pop("can_silence")

        actions = []
        _actions = d.pop("actions")
        for actions_item_data in _actions:
            actions_item = CorrectiveAction.from_dict(actions_item_data)

            actions.append(actions_item)

        dashboard_pending_action = cls(
            type_=type_,
            title=title,
            description=description,
            variant=variant,
            deadline=deadline,
            count=count,
            target_uuid=target_uuid,
            customer_uuid=customer_uuid,
            uuid=uuid,
            urgency=urgency,
            route_name=route_name,
            route_params=route_params,
            can_silence=can_silence,
            actions=actions,
        )

        dashboard_pending_action.additional_properties = d
        return dashboard_pending_action

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
