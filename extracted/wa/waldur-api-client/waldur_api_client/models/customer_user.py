import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_project_permission import NestedProjectPermission


T = TypeVar("T", bound="CustomerUser")


@_attrs_define
class CustomerUser:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        username (Union[Unset, str]): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_
            characters
        full_name (Union[Unset, str]):
        email (Union[Unset, str]):
        role_name (Union[None, Unset, str]):
        projects (Union[Unset, list['NestedProjectPermission']]):
        expiration_time (Union[None, Unset, datetime.datetime]):
        image (Union[None, Unset, str]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    username: Union[Unset, str] = UNSET
    full_name: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    role_name: Union[None, Unset, str] = UNSET
    projects: Union[Unset, list["NestedProjectPermission"]] = UNSET
    expiration_time: Union[None, Unset, datetime.datetime] = UNSET
    image: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        username = self.username

        full_name = self.full_name

        email = self.email

        role_name: Union[None, Unset, str]
        if isinstance(self.role_name, Unset):
            role_name = UNSET
        else:
            role_name = self.role_name

        projects: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.projects, Unset):
            projects = []
            for projects_item_data in self.projects:
                projects_item = projects_item_data.to_dict()
                projects.append(projects_item)

        expiration_time: Union[None, Unset, str]
        if isinstance(self.expiration_time, Unset):
            expiration_time = UNSET
        elif isinstance(self.expiration_time, datetime.datetime):
            expiration_time = self.expiration_time.isoformat()
        else:
            expiration_time = self.expiration_time

        image: Union[None, Unset, str]
        if isinstance(self.image, Unset):
            image = UNSET
        else:
            image = self.image

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if username is not UNSET:
            field_dict["username"] = username
        if full_name is not UNSET:
            field_dict["full_name"] = full_name
        if email is not UNSET:
            field_dict["email"] = email
        if role_name is not UNSET:
            field_dict["role_name"] = role_name
        if projects is not UNSET:
            field_dict["projects"] = projects
        if expiration_time is not UNSET:
            field_dict["expiration_time"] = expiration_time
        if image is not UNSET:
            field_dict["image"] = image

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_project_permission import NestedProjectPermission

        d = dict(src_dict)
        url = d.pop("url", UNSET)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        username = d.pop("username", UNSET)

        full_name = d.pop("full_name", UNSET)

        email = d.pop("email", UNSET)

        def _parse_role_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        role_name = _parse_role_name(d.pop("role_name", UNSET))

        projects = []
        _projects = d.pop("projects", UNSET)
        for projects_item_data in _projects or []:
            projects_item = NestedProjectPermission.from_dict(projects_item_data)

            projects.append(projects_item)

        def _parse_expiration_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expiration_time_type_0 = isoparse(data)

                return expiration_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        expiration_time = _parse_expiration_time(d.pop("expiration_time", UNSET))

        def _parse_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        image = _parse_image(d.pop("image", UNSET))

        customer_user = cls(
            url=url,
            uuid=uuid,
            username=username,
            full_name=full_name,
            email=email,
            role_name=role_name,
            projects=projects,
            expiration_time=expiration_time,
            image=image,
        )

        customer_user.additional_properties = d
        return customer_user

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
