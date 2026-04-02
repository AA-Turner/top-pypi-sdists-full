from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedProjectServiceAccountRequest")


@_attrs_define
class PatchedProjectServiceAccountRequest:
    """
    Attributes:
        username (Union[Unset, str]):
        description (Union[Unset, str]):
        error_traceback (Union[Unset, str]):
        email (Union[Unset, str]):
        preferred_identifier (Union[Unset, str]):
        project (Union[Unset, UUID]):
    """

    username: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    error_traceback: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    preferred_identifier: Union[Unset, str] = UNSET
    project: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        description = self.description

        error_traceback = self.error_traceback

        email = self.email

        preferred_identifier = self.preferred_identifier

        project: Union[Unset, str] = UNSET
        if not isinstance(self.project, Unset):
            project = str(self.project)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if username is not UNSET:
            field_dict["username"] = username
        if description is not UNSET:
            field_dict["description"] = description
        if error_traceback is not UNSET:
            field_dict["error_traceback"] = error_traceback
        if email is not UNSET:
            field_dict["email"] = email
        if preferred_identifier is not UNSET:
            field_dict["preferred_identifier"] = preferred_identifier
        if project is not UNSET:
            field_dict["project"] = project

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        username = d.pop("username", UNSET)

        description = d.pop("description", UNSET)

        error_traceback = d.pop("error_traceback", UNSET)

        email = d.pop("email", UNSET)

        preferred_identifier = d.pop("preferred_identifier", UNSET)

        _project = d.pop("project", UNSET)
        project: Union[Unset, UUID]
        if isinstance(_project, Unset):
            project = UNSET
        else:
            project = UUID(_project)

        patched_project_service_account_request = cls(
            username=username,
            description=description,
            error_traceback=error_traceback,
            email=email,
            preferred_identifier=preferred_identifier,
            project=project,
        )

        patched_project_service_account_request.additional_properties = d
        return patched_project_service_account_request

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
