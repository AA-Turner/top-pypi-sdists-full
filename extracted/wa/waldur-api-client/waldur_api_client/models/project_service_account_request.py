from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectServiceAccountRequest")


@_attrs_define
class ProjectServiceAccountRequest:
    """
    Attributes:
        project (Union[None, UUID]):
        description (Union[Unset, str]):
        email (Union[Unset, str]):
        preferred_identifier (Union[Unset, str]):
    """

    project: Union[None, UUID]
    description: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    preferred_identifier: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project: Union[None, str]
        if isinstance(self.project, UUID):
            project = str(self.project)
        else:
            project = self.project

        description = self.description

        email = self.email

        preferred_identifier = self.preferred_identifier

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project": project,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if email is not UNSET:
            field_dict["email"] = email
        if preferred_identifier is not UNSET:
            field_dict["preferred_identifier"] = preferred_identifier

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_project(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_type_0 = UUID(data)

                return project_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        project = _parse_project(d.pop("project"))

        description = d.pop("description", UNSET)

        email = d.pop("email", UNSET)

        preferred_identifier = d.pop("preferred_identifier", UNSET)

        project_service_account_request = cls(
            project=project,
            description=description,
            email=email,
            preferred_identifier=preferred_identifier,
        )

        project_service_account_request.additional_properties = d
        return project_service_account_request

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
