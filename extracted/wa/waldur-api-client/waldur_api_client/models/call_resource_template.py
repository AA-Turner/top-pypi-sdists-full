import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_public_plan import BasePublicPlan


T = TypeVar("T", bound="CallResourceTemplate")


@_attrs_define
class CallResourceTemplate:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        url (Union[Unset, str]):
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        attributes (Union[Unset, Any]):
        limits (Union[Unset, Any]):
        is_required (Union[Unset, bool]): If True, every proposal must include this resource type
        requested_offering (Union[Unset, str]):
        requested_offering_name (Union[Unset, str]):
        requested_offering_uuid (Union[Unset, UUID]):
        requested_offering_plan (Union[Unset, BasePublicPlan]):
        created_by (Union[None, Unset, str]):
        created_by_name (Union[Unset, str]):
        created (Union[Unset, datetime.datetime]):
    """

    uuid: Union[Unset, UUID] = UNSET
    url: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    attributes: Union[Unset, Any] = UNSET
    limits: Union[Unset, Any] = UNSET
    is_required: Union[Unset, bool] = UNSET
    requested_offering: Union[Unset, str] = UNSET
    requested_offering_name: Union[Unset, str] = UNSET
    requested_offering_uuid: Union[Unset, UUID] = UNSET
    requested_offering_plan: Union[Unset, "BasePublicPlan"] = UNSET
    created_by: Union[None, Unset, str] = UNSET
    created_by_name: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        url = self.url

        name = self.name

        description = self.description

        attributes = self.attributes

        limits = self.limits

        is_required = self.is_required

        requested_offering = self.requested_offering

        requested_offering_name = self.requested_offering_name

        requested_offering_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.requested_offering_uuid, Unset):
            requested_offering_uuid = str(self.requested_offering_uuid)

        requested_offering_plan: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.requested_offering_plan, Unset):
            requested_offering_plan = self.requested_offering_plan.to_dict()

        created_by: Union[None, Unset, str]
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        created_by_name = self.created_by_name

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if url is not UNSET:
            field_dict["url"] = url
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if limits is not UNSET:
            field_dict["limits"] = limits
        if is_required is not UNSET:
            field_dict["is_required"] = is_required
        if requested_offering is not UNSET:
            field_dict["requested_offering"] = requested_offering
        if requested_offering_name is not UNSET:
            field_dict["requested_offering_name"] = requested_offering_name
        if requested_offering_uuid is not UNSET:
            field_dict["requested_offering_uuid"] = requested_offering_uuid
        if requested_offering_plan is not UNSET:
            field_dict["requested_offering_plan"] = requested_offering_plan
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if created_by_name is not UNSET:
            field_dict["created_by_name"] = created_by_name
        if created is not UNSET:
            field_dict["created"] = created

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_public_plan import BasePublicPlan

        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        url = d.pop("url", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        attributes = d.pop("attributes", UNSET)

        limits = d.pop("limits", UNSET)

        is_required = d.pop("is_required", UNSET)

        requested_offering = d.pop("requested_offering", UNSET)

        requested_offering_name = d.pop("requested_offering_name", UNSET)

        _requested_offering_uuid = d.pop("requested_offering_uuid", UNSET)
        requested_offering_uuid: Union[Unset, UUID]
        if isinstance(_requested_offering_uuid, Unset):
            requested_offering_uuid = UNSET
        else:
            requested_offering_uuid = UUID(_requested_offering_uuid)

        _requested_offering_plan = d.pop("requested_offering_plan", UNSET)
        requested_offering_plan: Union[Unset, BasePublicPlan]
        if isinstance(_requested_offering_plan, Unset):
            requested_offering_plan = UNSET
        else:
            requested_offering_plan = BasePublicPlan.from_dict(_requested_offering_plan)

        def _parse_created_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        created_by_name = d.pop("created_by_name", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        call_resource_template = cls(
            uuid=uuid,
            url=url,
            name=name,
            description=description,
            attributes=attributes,
            limits=limits,
            is_required=is_required,
            requested_offering=requested_offering,
            requested_offering_name=requested_offering_name,
            requested_offering_uuid=requested_offering_uuid,
            requested_offering_plan=requested_offering_plan,
            created_by=created_by,
            created_by_name=created_by_name,
            created=created,
        )

        call_resource_template.additional_properties = d
        return call_resource_template

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
