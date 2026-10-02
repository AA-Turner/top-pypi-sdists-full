import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.urgency_enum import UrgencyEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.corrective_action import CorrectiveAction
    from ..models.user_action_route_params import UserActionRouteParams


T = TypeVar("T", bound="UserAction")


@_attrs_define
class UserAction:
    """
    Attributes:
        uuid (UUID):
        action_type (str): Type of action, e.g. 'pending_order', 'expiring_resource'
        title (str):
        description (str):
        urgency (UrgencyEnum):
        is_temporarily_silenced (bool):
        is_effectively_silenced (bool):
        created (datetime.datetime):
        modified (datetime.datetime):
        related_object_name (str):
        related_object_type (str):
        corrective_actions (list['CorrectiveAction']):
        days_until_due (Union[None, int]):
        route_params (UserActionRouteParams):
        due_date (Union[None, Unset, datetime.datetime]):
        is_silenced (Union[Unset, bool]):
        silenced_until (Union[None, Unset, datetime.datetime]):
        route_name (Union[Unset, str]): UI-Router state name for navigation
        project_name (Union[Unset, str]):
        project_uuid (Union[None, UUID, Unset]):
        organization_name (Union[Unset, str]):
        organization_uuid (Union[None, UUID, Unset]):
        offering_name (Union[Unset, str]):
        offering_uuid (Union[None, UUID, Unset]):
        offering_type (Union[Unset, str]):
        resource_name (Union[Unset, str]):
        resource_uuid (Union[None, UUID, Unset]):
        order_type (Union[Unset, str]):
    """

    uuid: UUID
    action_type: str
    title: str
    description: str
    urgency: UrgencyEnum
    is_temporarily_silenced: bool
    is_effectively_silenced: bool
    created: datetime.datetime
    modified: datetime.datetime
    related_object_name: str
    related_object_type: str
    corrective_actions: list["CorrectiveAction"]
    days_until_due: Union[None, int]
    route_params: "UserActionRouteParams"
    due_date: Union[None, Unset, datetime.datetime] = UNSET
    is_silenced: Union[Unset, bool] = UNSET
    silenced_until: Union[None, Unset, datetime.datetime] = UNSET
    route_name: Union[Unset, str] = UNSET
    project_name: Union[Unset, str] = UNSET
    project_uuid: Union[None, UUID, Unset] = UNSET
    organization_name: Union[Unset, str] = UNSET
    organization_uuid: Union[None, UUID, Unset] = UNSET
    offering_name: Union[Unset, str] = UNSET
    offering_uuid: Union[None, UUID, Unset] = UNSET
    offering_type: Union[Unset, str] = UNSET
    resource_name: Union[Unset, str] = UNSET
    resource_uuid: Union[None, UUID, Unset] = UNSET
    order_type: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        action_type = self.action_type

        title = self.title

        description = self.description

        urgency = self.urgency.value

        is_temporarily_silenced = self.is_temporarily_silenced

        is_effectively_silenced = self.is_effectively_silenced

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        related_object_name = self.related_object_name

        related_object_type = self.related_object_type

        corrective_actions = []
        for corrective_actions_item_data in self.corrective_actions:
            corrective_actions_item = corrective_actions_item_data.to_dict()
            corrective_actions.append(corrective_actions_item)

        days_until_due: Union[None, int]
        days_until_due = self.days_until_due

        route_params = self.route_params.to_dict()

        due_date: Union[None, Unset, str]
        if isinstance(self.due_date, Unset):
            due_date = UNSET
        elif isinstance(self.due_date, datetime.datetime):
            due_date = self.due_date.isoformat()
        else:
            due_date = self.due_date

        is_silenced = self.is_silenced

        silenced_until: Union[None, Unset, str]
        if isinstance(self.silenced_until, Unset):
            silenced_until = UNSET
        elif isinstance(self.silenced_until, datetime.datetime):
            silenced_until = self.silenced_until.isoformat()
        else:
            silenced_until = self.silenced_until

        route_name = self.route_name

        project_name = self.project_name

        project_uuid: Union[None, Unset, str]
        if isinstance(self.project_uuid, Unset):
            project_uuid = UNSET
        elif isinstance(self.project_uuid, UUID):
            project_uuid = str(self.project_uuid)
        else:
            project_uuid = self.project_uuid

        organization_name = self.organization_name

        organization_uuid: Union[None, Unset, str]
        if isinstance(self.organization_uuid, Unset):
            organization_uuid = UNSET
        elif isinstance(self.organization_uuid, UUID):
            organization_uuid = str(self.organization_uuid)
        else:
            organization_uuid = self.organization_uuid

        offering_name = self.offering_name

        offering_uuid: Union[None, Unset, str]
        if isinstance(self.offering_uuid, Unset):
            offering_uuid = UNSET
        elif isinstance(self.offering_uuid, UUID):
            offering_uuid = str(self.offering_uuid)
        else:
            offering_uuid = self.offering_uuid

        offering_type = self.offering_type

        resource_name = self.resource_name

        resource_uuid: Union[None, Unset, str]
        if isinstance(self.resource_uuid, Unset):
            resource_uuid = UNSET
        elif isinstance(self.resource_uuid, UUID):
            resource_uuid = str(self.resource_uuid)
        else:
            resource_uuid = self.resource_uuid

        order_type = self.order_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "action_type": action_type,
                "title": title,
                "description": description,
                "urgency": urgency,
                "is_temporarily_silenced": is_temporarily_silenced,
                "is_effectively_silenced": is_effectively_silenced,
                "created": created,
                "modified": modified,
                "related_object_name": related_object_name,
                "related_object_type": related_object_type,
                "corrective_actions": corrective_actions,
                "days_until_due": days_until_due,
                "route_params": route_params,
            }
        )
        if due_date is not UNSET:
            field_dict["due_date"] = due_date
        if is_silenced is not UNSET:
            field_dict["is_silenced"] = is_silenced
        if silenced_until is not UNSET:
            field_dict["silenced_until"] = silenced_until
        if route_name is not UNSET:
            field_dict["route_name"] = route_name
        if project_name is not UNSET:
            field_dict["project_name"] = project_name
        if project_uuid is not UNSET:
            field_dict["project_uuid"] = project_uuid
        if organization_name is not UNSET:
            field_dict["organization_name"] = organization_name
        if organization_uuid is not UNSET:
            field_dict["organization_uuid"] = organization_uuid
        if offering_name is not UNSET:
            field_dict["offering_name"] = offering_name
        if offering_uuid is not UNSET:
            field_dict["offering_uuid"] = offering_uuid
        if offering_type is not UNSET:
            field_dict["offering_type"] = offering_type
        if resource_name is not UNSET:
            field_dict["resource_name"] = resource_name
        if resource_uuid is not UNSET:
            field_dict["resource_uuid"] = resource_uuid
        if order_type is not UNSET:
            field_dict["order_type"] = order_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.corrective_action import CorrectiveAction
        from ..models.user_action_route_params import UserActionRouteParams

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        action_type = d.pop("action_type")

        title = d.pop("title")

        description = d.pop("description")

        urgency = UrgencyEnum(d.pop("urgency"))

        is_temporarily_silenced = d.pop("is_temporarily_silenced")

        is_effectively_silenced = d.pop("is_effectively_silenced")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        related_object_name = d.pop("related_object_name")

        related_object_type = d.pop("related_object_type")

        corrective_actions = []
        _corrective_actions = d.pop("corrective_actions")
        for corrective_actions_item_data in _corrective_actions:
            corrective_actions_item = CorrectiveAction.from_dict(corrective_actions_item_data)

            corrective_actions.append(corrective_actions_item)

        def _parse_days_until_due(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        days_until_due = _parse_days_until_due(d.pop("days_until_due"))

        route_params = UserActionRouteParams.from_dict(d.pop("route_params"))

        def _parse_due_date(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                due_date_type_0 = isoparse(data)

                return due_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        due_date = _parse_due_date(d.pop("due_date", UNSET))

        is_silenced = d.pop("is_silenced", UNSET)

        def _parse_silenced_until(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                silenced_until_type_0 = isoparse(data)

                return silenced_until_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        silenced_until = _parse_silenced_until(d.pop("silenced_until", UNSET))

        route_name = d.pop("route_name", UNSET)

        project_name = d.pop("project_name", UNSET)

        def _parse_project_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_uuid_type_0 = UUID(data)

                return project_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        project_uuid = _parse_project_uuid(d.pop("project_uuid", UNSET))

        organization_name = d.pop("organization_name", UNSET)

        def _parse_organization_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                organization_uuid_type_0 = UUID(data)

                return organization_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        organization_uuid = _parse_organization_uuid(d.pop("organization_uuid", UNSET))

        offering_name = d.pop("offering_name", UNSET)

        def _parse_offering_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                offering_uuid_type_0 = UUID(data)

                return offering_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        offering_uuid = _parse_offering_uuid(d.pop("offering_uuid", UNSET))

        offering_type = d.pop("offering_type", UNSET)

        resource_name = d.pop("resource_name", UNSET)

        def _parse_resource_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resource_uuid_type_0 = UUID(data)

                return resource_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        resource_uuid = _parse_resource_uuid(d.pop("resource_uuid", UNSET))

        order_type = d.pop("order_type", UNSET)

        user_action = cls(
            uuid=uuid,
            action_type=action_type,
            title=title,
            description=description,
            urgency=urgency,
            is_temporarily_silenced=is_temporarily_silenced,
            is_effectively_silenced=is_effectively_silenced,
            created=created,
            modified=modified,
            related_object_name=related_object_name,
            related_object_type=related_object_type,
            corrective_actions=corrective_actions,
            days_until_due=days_until_due,
            route_params=route_params,
            due_date=due_date,
            is_silenced=is_silenced,
            silenced_until=silenced_until,
            route_name=route_name,
            project_name=project_name,
            project_uuid=project_uuid,
            organization_name=organization_name,
            organization_uuid=organization_uuid,
            offering_name=offering_name,
            offering_uuid=offering_uuid,
            offering_type=offering_type,
            resource_name=resource_name,
            resource_uuid=resource_uuid,
            order_type=order_type,
        )

        user_action.additional_properties = d
        return user_action

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
