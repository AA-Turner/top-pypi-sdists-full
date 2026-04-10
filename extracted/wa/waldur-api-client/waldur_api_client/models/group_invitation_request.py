from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GroupInvitationRequest")


@_attrs_define
class GroupInvitationRequest:
    """
    Attributes:
        role (UUID): UUID of the role to grant to the invited user
        scope (str): URL of the scope (Customer or Project) for this invitation
        is_public (Union[Unset, bool]): Allow non-authenticated users to see and accept this invitation. Only staff can
            create public invitations.
        auto_create_project (Union[Unset, bool]): Create project and grant project permissions instead of customer
            permissions
        auto_approve (Union[Unset, bool]): Automatically approve permission requests from users matching email patterns
            or affiliations
        project_name_template (Union[None, Unset, str]): Template for project name. Supports {username}, {email},
            {full_name} variables
        project_role (Union[None, UUID, Unset]): UUID of the project role to grant if auto_create_project is enabled
        user_affiliations (Union[Unset, Any]):
        user_email_patterns (Union[Unset, Any]):
        user_identity_sources (Union[Unset, Any]): List of allowed identity sources (identity providers).
        custom_text (Union[Unset, str]): Custom description text displayed to users viewing this invitation.
        allow_multiple_requests (Union[Unset, bool]): Allow users to submit multiple permission requests for this
            invitation.
        allow_custom_project_details (Union[Unset, bool]): Allow users to provide custom project name and description
            when accepting the invitation. If disabled, the project name is auto-generated from the template.
    """

    role: UUID
    scope: str
    is_public: Union[Unset, bool] = UNSET
    auto_create_project: Union[Unset, bool] = UNSET
    auto_approve: Union[Unset, bool] = UNSET
    project_name_template: Union[None, Unset, str] = UNSET
    project_role: Union[None, UUID, Unset] = UNSET
    user_affiliations: Union[Unset, Any] = UNSET
    user_email_patterns: Union[Unset, Any] = UNSET
    user_identity_sources: Union[Unset, Any] = UNSET
    custom_text: Union[Unset, str] = UNSET
    allow_multiple_requests: Union[Unset, bool] = UNSET
    allow_custom_project_details: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        role = str(self.role)

        scope = self.scope

        is_public = self.is_public

        auto_create_project = self.auto_create_project

        auto_approve = self.auto_approve

        project_name_template: Union[None, Unset, str]
        if isinstance(self.project_name_template, Unset):
            project_name_template = UNSET
        else:
            project_name_template = self.project_name_template

        project_role: Union[None, Unset, str]
        if isinstance(self.project_role, Unset):
            project_role = UNSET
        elif isinstance(self.project_role, UUID):
            project_role = str(self.project_role)
        else:
            project_role = self.project_role

        user_affiliations = self.user_affiliations

        user_email_patterns = self.user_email_patterns

        user_identity_sources = self.user_identity_sources

        custom_text = self.custom_text

        allow_multiple_requests = self.allow_multiple_requests

        allow_custom_project_details = self.allow_custom_project_details

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "scope": scope,
            }
        )
        if is_public is not UNSET:
            field_dict["is_public"] = is_public
        if auto_create_project is not UNSET:
            field_dict["auto_create_project"] = auto_create_project
        if auto_approve is not UNSET:
            field_dict["auto_approve"] = auto_approve
        if project_name_template is not UNSET:
            field_dict["project_name_template"] = project_name_template
        if project_role is not UNSET:
            field_dict["project_role"] = project_role
        if user_affiliations is not UNSET:
            field_dict["user_affiliations"] = user_affiliations
        if user_email_patterns is not UNSET:
            field_dict["user_email_patterns"] = user_email_patterns
        if user_identity_sources is not UNSET:
            field_dict["user_identity_sources"] = user_identity_sources
        if custom_text is not UNSET:
            field_dict["custom_text"] = custom_text
        if allow_multiple_requests is not UNSET:
            field_dict["allow_multiple_requests"] = allow_multiple_requests
        if allow_custom_project_details is not UNSET:
            field_dict["allow_custom_project_details"] = allow_custom_project_details

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        role = UUID(d.pop("role"))

        scope = d.pop("scope")

        is_public = d.pop("is_public", UNSET)

        auto_create_project = d.pop("auto_create_project", UNSET)

        auto_approve = d.pop("auto_approve", UNSET)

        def _parse_project_name_template(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_name_template = _parse_project_name_template(d.pop("project_name_template", UNSET))

        def _parse_project_role(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_role_type_0 = UUID(data)

                return project_role_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        project_role = _parse_project_role(d.pop("project_role", UNSET))

        user_affiliations = d.pop("user_affiliations", UNSET)

        user_email_patterns = d.pop("user_email_patterns", UNSET)

        user_identity_sources = d.pop("user_identity_sources", UNSET)

        custom_text = d.pop("custom_text", UNSET)

        allow_multiple_requests = d.pop("allow_multiple_requests", UNSET)

        allow_custom_project_details = d.pop("allow_custom_project_details", UNSET)

        group_invitation_request = cls(
            role=role,
            scope=scope,
            is_public=is_public,
            auto_create_project=auto_create_project,
            auto_approve=auto_approve,
            project_name_template=project_name_template,
            project_role=project_role,
            user_affiliations=user_affiliations,
            user_email_patterns=user_email_patterns,
            user_identity_sources=user_identity_sources,
            custom_text=custom_text,
            allow_multiple_requests=allow_multiple_requests,
            allow_custom_project_details=allow_custom_project_details,
        )

        group_invitation_request.additional_properties = d
        return group_invitation_request

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
