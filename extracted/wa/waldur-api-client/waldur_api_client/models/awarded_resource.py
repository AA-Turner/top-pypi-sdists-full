import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.awarded_resource_attributes import AwardedResourceAttributes
    from ..models.awarded_resource_limits import AwardedResourceLimits
    from ..models.nested_requested_offering import NestedRequestedOffering


T = TypeVar("T", bound="AwardedResource")


@_attrs_define
class AwardedResource:
    """
    Attributes:
        uuid (UUID):
        url (str):
        requested_resource (Union[None, UUID]):
        requested_offering (NestedRequestedOffering):
        plan_name (Union[None, str]):
        resource (Union[None, UUID]):
        resource_name (Union[None, str]):
        created_by (Union[None, UUID]):
        created_by_name (Union[None, str]):
        created (datetime.datetime):
        modified (datetime.datetime):
        plan (Union[None, UUID, Unset]): Plan of the awarded offering. Read back as the plan the item is provisioned on:
            the call offering's plan unless another was set. Null (or leaving it out when adding or moving) follows the call
            offering's plan.
        attributes (Union[Unset, AwardedResourceAttributes]):
        limits (Union[Unset, AwardedResourceLimits]):
        description (Union[Unset, str]):
    """

    uuid: UUID
    url: str
    requested_resource: Union[None, UUID]
    requested_offering: "NestedRequestedOffering"
    plan_name: Union[None, str]
    resource: Union[None, UUID]
    resource_name: Union[None, str]
    created_by: Union[None, UUID]
    created_by_name: Union[None, str]
    created: datetime.datetime
    modified: datetime.datetime
    plan: Union[None, UUID, Unset] = UNSET
    attributes: Union[Unset, "AwardedResourceAttributes"] = UNSET
    limits: Union[Unset, "AwardedResourceLimits"] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        requested_resource: Union[None, str]
        if isinstance(self.requested_resource, UUID):
            requested_resource = str(self.requested_resource)
        else:
            requested_resource = self.requested_resource

        requested_offering = self.requested_offering.to_dict()

        plan_name: Union[None, str]
        plan_name = self.plan_name

        resource: Union[None, str]
        if isinstance(self.resource, UUID):
            resource = str(self.resource)
        else:
            resource = self.resource

        resource_name: Union[None, str]
        resource_name = self.resource_name

        created_by: Union[None, str]
        if isinstance(self.created_by, UUID):
            created_by = str(self.created_by)
        else:
            created_by = self.created_by

        created_by_name: Union[None, str]
        created_by_name = self.created_by_name

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        plan: Union[None, Unset, str]
        if isinstance(self.plan, Unset):
            plan = UNSET
        elif isinstance(self.plan, UUID):
            plan = str(self.plan)
        else:
            plan = self.plan

        attributes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes.to_dict()

        limits: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "requested_resource": requested_resource,
                "requested_offering": requested_offering,
                "plan_name": plan_name,
                "resource": resource,
                "resource_name": resource_name,
                "created_by": created_by,
                "created_by_name": created_by_name,
                "created": created,
                "modified": modified,
            }
        )
        if plan is not UNSET:
            field_dict["plan"] = plan
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if limits is not UNSET:
            field_dict["limits"] = limits
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.awarded_resource_attributes import AwardedResourceAttributes
        from ..models.awarded_resource_limits import AwardedResourceLimits
        from ..models.nested_requested_offering import NestedRequestedOffering

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        def _parse_requested_resource(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                requested_resource_type_0 = UUID(data)

                return requested_resource_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        requested_resource = _parse_requested_resource(d.pop("requested_resource"))

        requested_offering = NestedRequestedOffering.from_dict(d.pop("requested_offering"))

        def _parse_plan_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        plan_name = _parse_plan_name(d.pop("plan_name"))

        def _parse_resource(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resource_type_0 = UUID(data)

                return resource_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        resource = _parse_resource(d.pop("resource"))

        def _parse_resource_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        resource_name = _parse_resource_name(d.pop("resource_name"))

        def _parse_created_by(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_by_type_0 = UUID(data)

                return created_by_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        created_by = _parse_created_by(d.pop("created_by"))

        def _parse_created_by_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        created_by_name = _parse_created_by_name(d.pop("created_by_name"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        def _parse_plan(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                plan_type_0 = UUID(data)

                return plan_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        plan = _parse_plan(d.pop("plan", UNSET))

        _attributes = d.pop("attributes", UNSET)
        attributes: Union[Unset, AwardedResourceAttributes]
        if isinstance(_attributes, Unset):
            attributes = UNSET
        else:
            attributes = AwardedResourceAttributes.from_dict(_attributes)

        _limits = d.pop("limits", UNSET)
        limits: Union[Unset, AwardedResourceLimits]
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = AwardedResourceLimits.from_dict(_limits)

        description = d.pop("description", UNSET)

        awarded_resource = cls(
            uuid=uuid,
            url=url,
            requested_resource=requested_resource,
            requested_offering=requested_offering,
            plan_name=plan_name,
            resource=resource,
            resource_name=resource_name,
            created_by=created_by,
            created_by_name=created_by_name,
            created=created,
            modified=modified,
            plan=plan,
            attributes=attributes,
            limits=limits,
            description=description,
        )

        awarded_resource.additional_properties = d
        return awarded_resource

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
