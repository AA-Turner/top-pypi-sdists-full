from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.role_type import RoleType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SubmitRequestResponse")


@_attrs_define
class SubmitRequestResponse:
    """
    Attributes:
        uuid (str): UUID of the created permission request
        scope_name (str): Name of the invitation scope
        scope_uuid (str): UUID of the invitation scope
        auto_approved (bool): Whether the request was automatically approved
        scope_type (Union[None, RoleType, Unset]): Type of the invitation scope (e.g., 'customer', 'project')
        project_uuid (Union[None, Unset, str]): UUID of the project the user was added to. Present when the invitation
            has auto_approve and auto_create_project enabled. Null otherwise.
        project_created (Union[None, Unset, bool]): True if a new project was created for the user; false if an existing
            project with the same name was reused. Null when no project workflow ran.
    """

    uuid: str
    scope_name: str
    scope_uuid: str
    auto_approved: bool
    scope_type: Union[None, RoleType, Unset] = UNSET
    project_uuid: Union[None, Unset, str] = UNSET
    project_created: Union[None, Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        scope_name = self.scope_name

        scope_uuid = self.scope_uuid

        auto_approved = self.auto_approved

        scope_type: Union[None, Unset, str]
        if isinstance(self.scope_type, Unset):
            scope_type = UNSET
        elif isinstance(self.scope_type, RoleType):
            scope_type = self.scope_type.value
        else:
            scope_type = self.scope_type

        project_uuid: Union[None, Unset, str]
        if isinstance(self.project_uuid, Unset):
            project_uuid = UNSET
        else:
            project_uuid = self.project_uuid

        project_created: Union[None, Unset, bool]
        if isinstance(self.project_created, Unset):
            project_created = UNSET
        else:
            project_created = self.project_created

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "scope_name": scope_name,
                "scope_uuid": scope_uuid,
                "auto_approved": auto_approved,
            }
        )
        if scope_type is not UNSET:
            field_dict["scope_type"] = scope_type
        if project_uuid is not UNSET:
            field_dict["project_uuid"] = project_uuid
        if project_created is not UNSET:
            field_dict["project_created"] = project_created

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = d.pop("uuid")

        scope_name = d.pop("scope_name")

        scope_uuid = d.pop("scope_uuid")

        auto_approved = d.pop("auto_approved")

        def _parse_scope_type(data: object) -> Union[None, RoleType, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scope_type_type_0 = RoleType(data)

                return scope_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, RoleType, Unset], data)

        scope_type = _parse_scope_type(d.pop("scope_type", UNSET))

        def _parse_project_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_uuid = _parse_project_uuid(d.pop("project_uuid", UNSET))

        def _parse_project_created(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        project_created = _parse_project_created(d.pop("project_created", UNSET))

        submit_request_response = cls(
            uuid=uuid,
            scope_name=scope_name,
            scope_uuid=scope_uuid,
            auto_approved=auto_approved,
            scope_type=scope_type,
            project_uuid=project_uuid,
            project_created=project_created,
        )

        submit_request_response.additional_properties = d
        return submit_request_response

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
