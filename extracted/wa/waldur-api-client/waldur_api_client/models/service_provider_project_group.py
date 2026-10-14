import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.service_provider_project_group_offering import ServiceProviderProjectGroupOffering


T = TypeVar("T", bound="ServiceProviderProjectGroup")


@_attrs_define
class ServiceProviderProjectGroup:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        gid (Union[None, int]):
        in_use (bool): The project has a non-terminated resource on an offering of the provider. An unused group keeps
            its GID.
        service_provider_uuid (UUID):
        service_provider_name (str):
        project_uuid (Union[None, UUID]):
        project_name (Union[None, str]):
        project_slug (Union[None, str]):
        customer_uuid (Union[None, UUID]):
        customer_name (Union[None, str]):
        customer_slug (Union[None, str]):
        offerings (list['ServiceProviderProjectGroupOffering']): The provider's offerings where the project has a non-
            terminated resource.
        members (list[str]): Sorted usernames of the live accounts at the provider of the users holding an active role
            in the project.
        created (datetime.datetime):
        modified (datetime.datetime):
    """

    url: str
    uuid: UUID
    name: str
    gid: Union[None, int]
    in_use: bool
    service_provider_uuid: UUID
    service_provider_name: str
    project_uuid: Union[None, UUID]
    project_name: Union[None, str]
    project_slug: Union[None, str]
    customer_uuid: Union[None, UUID]
    customer_name: Union[None, str]
    customer_slug: Union[None, str]
    offerings: list["ServiceProviderProjectGroupOffering"]
    members: list[str]
    created: datetime.datetime
    modified: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        gid: Union[None, int]
        gid = self.gid

        in_use = self.in_use

        service_provider_uuid = str(self.service_provider_uuid)

        service_provider_name = self.service_provider_name

        project_uuid: Union[None, str]
        if isinstance(self.project_uuid, UUID):
            project_uuid = str(self.project_uuid)
        else:
            project_uuid = self.project_uuid

        project_name: Union[None, str]
        project_name = self.project_name

        project_slug: Union[None, str]
        project_slug = self.project_slug

        customer_uuid: Union[None, str]
        if isinstance(self.customer_uuid, UUID):
            customer_uuid = str(self.customer_uuid)
        else:
            customer_uuid = self.customer_uuid

        customer_name: Union[None, str]
        customer_name = self.customer_name

        customer_slug: Union[None, str]
        customer_slug = self.customer_slug

        offerings = []
        for offerings_item_data in self.offerings:
            offerings_item = offerings_item_data.to_dict()
            offerings.append(offerings_item)

        members = self.members

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "gid": gid,
                "in_use": in_use,
                "service_provider_uuid": service_provider_uuid,
                "service_provider_name": service_provider_name,
                "project_uuid": project_uuid,
                "project_name": project_name,
                "project_slug": project_slug,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
                "customer_slug": customer_slug,
                "offerings": offerings,
                "members": members,
                "created": created,
                "modified": modified,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.service_provider_project_group_offering import ServiceProviderProjectGroupOffering

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        def _parse_gid(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        gid = _parse_gid(d.pop("gid"))

        in_use = d.pop("in_use")

        service_provider_uuid = UUID(d.pop("service_provider_uuid"))

        service_provider_name = d.pop("service_provider_name")

        def _parse_project_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_uuid_type_0 = UUID(data)

                return project_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        project_uuid = _parse_project_uuid(d.pop("project_uuid"))

        def _parse_project_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        project_name = _parse_project_name(d.pop("project_name"))

        def _parse_project_slug(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        project_slug = _parse_project_slug(d.pop("project_slug"))

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

        def _parse_customer_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        customer_name = _parse_customer_name(d.pop("customer_name"))

        def _parse_customer_slug(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        customer_slug = _parse_customer_slug(d.pop("customer_slug"))

        offerings = []
        _offerings = d.pop("offerings")
        for offerings_item_data in _offerings:
            offerings_item = ServiceProviderProjectGroupOffering.from_dict(offerings_item_data)

            offerings.append(offerings_item)

        members = cast(list[str], d.pop("members"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        service_provider_project_group = cls(
            url=url,
            uuid=uuid,
            name=name,
            gid=gid,
            in_use=in_use,
            service_provider_uuid=service_provider_uuid,
            service_provider_name=service_provider_name,
            project_uuid=project_uuid,
            project_name=project_name,
            project_slug=project_slug,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            customer_slug=customer_slug,
            offerings=offerings,
            members=members,
            created=created,
            modified=modified,
        )

        service_provider_project_group.additional_properties = d
        return service_provider_project_group

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
