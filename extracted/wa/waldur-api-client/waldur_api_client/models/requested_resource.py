from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_requested_offering import NestedRequestedOffering


T = TypeVar("T", bound="RequestedResource")


@_attrs_define
class RequestedResource:
    """
    Attributes:
        uuid (UUID):
        url (str):
        requested_offering (NestedRequestedOffering):
        resource (Union[None, str]):
        resource_name (str):
        call_resource_template (str):
        call_resource_template_name (str):
        created_by (Union[None, str]):
        created_by_name (str):
        attributes (Union[Unset, Any]):
        limits (Union[Unset, Any]):
        description (Union[Unset, str]):
    """

    uuid: UUID
    url: str
    requested_offering: "NestedRequestedOffering"
    resource: Union[None, str]
    resource_name: str
    call_resource_template: str
    call_resource_template_name: str
    created_by: Union[None, str]
    created_by_name: str
    attributes: Union[Unset, Any] = UNSET
    limits: Union[Unset, Any] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        requested_offering = self.requested_offering.to_dict()

        resource: Union[None, str]
        resource = self.resource

        resource_name = self.resource_name

        call_resource_template = self.call_resource_template

        call_resource_template_name = self.call_resource_template_name

        created_by: Union[None, str]
        created_by = self.created_by

        created_by_name = self.created_by_name

        attributes = self.attributes

        limits = self.limits

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "requested_offering": requested_offering,
                "resource": resource,
                "resource_name": resource_name,
                "call_resource_template": call_resource_template,
                "call_resource_template_name": call_resource_template_name,
                "created_by": created_by,
                "created_by_name": created_by_name,
            }
        )
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if limits is not UNSET:
            field_dict["limits"] = limits
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_requested_offering import NestedRequestedOffering

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        requested_offering = NestedRequestedOffering.from_dict(d.pop("requested_offering"))

        def _parse_resource(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        resource = _parse_resource(d.pop("resource"))

        resource_name = d.pop("resource_name")

        call_resource_template = d.pop("call_resource_template")

        call_resource_template_name = d.pop("call_resource_template_name")

        def _parse_created_by(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        created_by = _parse_created_by(d.pop("created_by"))

        created_by_name = d.pop("created_by_name")

        attributes = d.pop("attributes", UNSET)

        limits = d.pop("limits", UNSET)

        description = d.pop("description", UNSET)

        requested_resource = cls(
            uuid=uuid,
            url=url,
            requested_offering=requested_offering,
            resource=resource,
            resource_name=resource_name,
            call_resource_template=call_resource_template,
            call_resource_template_name=call_resource_template_name,
            created_by=created_by,
            created_by_name=created_by_name,
            attributes=attributes,
            limits=limits,
            description=description,
        )

        requested_resource.additional_properties = d
        return requested_resource

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
