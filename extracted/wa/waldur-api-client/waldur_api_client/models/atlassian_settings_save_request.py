from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auth_method_enum import AuthMethodEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.atlassian_settings_save_request_support_type_mapping import (
        AtlassianSettingsSaveRequestSupportTypeMapping,
    )


T = TypeVar("T", bound="AtlassianSettingsSaveRequest")


@_attrs_define
class AtlassianSettingsSaveRequest:
    """
    Attributes:
        api_url (str):
        auth_method (AuthMethodEnum):
        project_id (str):
        confirm_save (bool): Must be True to confirm saving settings
        email (Union[Unset, str]):
        token (Union[Unset, str]):
        personal_access_token (Union[Unset, str]):
        username (Union[Unset, str]):
        password (Union[Unset, str]):
        verify_ssl (Union[Unset, bool]):  Default: True.
        issue_types (Union[Unset, list[str]]):
        support_type_mapping (Union[Unset, AtlassianSettingsSaveRequestSupportTypeMapping]): Mapping from frontend types
            to backend request types
        reporter_field (Union[Unset, str]):
        impact_field (Union[Unset, str]):
        organisation_field (Union[Unset, str]):
        project_field (Union[Unset, str]):
        affected_resource_field (Union[Unset, str]):
        caller_field (Union[Unset, str]):
        template_field (Union[Unset, str]):
        sla_field (Union[Unset, str]):
        resolution_sla_field (Union[Unset, str]):
        satisfaction_field (Union[Unset, str]):
        request_feedback_field (Union[Unset, str]):
        waldur_backend_id_field (Union[Unset, str]):
        default_offering_issue_type (Union[Unset, str]): Default issue type for marketplace request-based orders
        use_old_api (Union[Unset, bool]):  Default: False.
        custom_field_mapping_enabled (Union[Unset, bool]):  Default: True.
    """

    api_url: str
    auth_method: AuthMethodEnum
    project_id: str
    confirm_save: bool
    email: Union[Unset, str] = UNSET
    token: Union[Unset, str] = UNSET
    personal_access_token: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    password: Union[Unset, str] = UNSET
    verify_ssl: Union[Unset, bool] = True
    issue_types: Union[Unset, list[str]] = UNSET
    support_type_mapping: Union[Unset, "AtlassianSettingsSaveRequestSupportTypeMapping"] = UNSET
    reporter_field: Union[Unset, str] = UNSET
    impact_field: Union[Unset, str] = UNSET
    organisation_field: Union[Unset, str] = UNSET
    project_field: Union[Unset, str] = UNSET
    affected_resource_field: Union[Unset, str] = UNSET
    caller_field: Union[Unset, str] = UNSET
    template_field: Union[Unset, str] = UNSET
    sla_field: Union[Unset, str] = UNSET
    resolution_sla_field: Union[Unset, str] = UNSET
    satisfaction_field: Union[Unset, str] = UNSET
    request_feedback_field: Union[Unset, str] = UNSET
    waldur_backend_id_field: Union[Unset, str] = UNSET
    default_offering_issue_type: Union[Unset, str] = UNSET
    use_old_api: Union[Unset, bool] = False
    custom_field_mapping_enabled: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        api_url = self.api_url

        auth_method = self.auth_method.value

        project_id = self.project_id

        confirm_save = self.confirm_save

        email = self.email

        token = self.token

        personal_access_token = self.personal_access_token

        username = self.username

        password = self.password

        verify_ssl = self.verify_ssl

        issue_types: Union[Unset, list[str]] = UNSET
        if not isinstance(self.issue_types, Unset):
            issue_types = self.issue_types

        support_type_mapping: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.support_type_mapping, Unset):
            support_type_mapping = self.support_type_mapping.to_dict()

        reporter_field = self.reporter_field

        impact_field = self.impact_field

        organisation_field = self.organisation_field

        project_field = self.project_field

        affected_resource_field = self.affected_resource_field

        caller_field = self.caller_field

        template_field = self.template_field

        sla_field = self.sla_field

        resolution_sla_field = self.resolution_sla_field

        satisfaction_field = self.satisfaction_field

        request_feedback_field = self.request_feedback_field

        waldur_backend_id_field = self.waldur_backend_id_field

        default_offering_issue_type = self.default_offering_issue_type

        use_old_api = self.use_old_api

        custom_field_mapping_enabled = self.custom_field_mapping_enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "api_url": api_url,
                "auth_method": auth_method,
                "project_id": project_id,
                "confirm_save": confirm_save,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email
        if token is not UNSET:
            field_dict["token"] = token
        if personal_access_token is not UNSET:
            field_dict["personal_access_token"] = personal_access_token
        if username is not UNSET:
            field_dict["username"] = username
        if password is not UNSET:
            field_dict["password"] = password
        if verify_ssl is not UNSET:
            field_dict["verify_ssl"] = verify_ssl
        if issue_types is not UNSET:
            field_dict["issue_types"] = issue_types
        if support_type_mapping is not UNSET:
            field_dict["support_type_mapping"] = support_type_mapping
        if reporter_field is not UNSET:
            field_dict["reporter_field"] = reporter_field
        if impact_field is not UNSET:
            field_dict["impact_field"] = impact_field
        if organisation_field is not UNSET:
            field_dict["organisation_field"] = organisation_field
        if project_field is not UNSET:
            field_dict["project_field"] = project_field
        if affected_resource_field is not UNSET:
            field_dict["affected_resource_field"] = affected_resource_field
        if caller_field is not UNSET:
            field_dict["caller_field"] = caller_field
        if template_field is not UNSET:
            field_dict["template_field"] = template_field
        if sla_field is not UNSET:
            field_dict["sla_field"] = sla_field
        if resolution_sla_field is not UNSET:
            field_dict["resolution_sla_field"] = resolution_sla_field
        if satisfaction_field is not UNSET:
            field_dict["satisfaction_field"] = satisfaction_field
        if request_feedback_field is not UNSET:
            field_dict["request_feedback_field"] = request_feedback_field
        if waldur_backend_id_field is not UNSET:
            field_dict["waldur_backend_id_field"] = waldur_backend_id_field
        if default_offering_issue_type is not UNSET:
            field_dict["default_offering_issue_type"] = default_offering_issue_type
        if use_old_api is not UNSET:
            field_dict["use_old_api"] = use_old_api
        if custom_field_mapping_enabled is not UNSET:
            field_dict["custom_field_mapping_enabled"] = custom_field_mapping_enabled

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.atlassian_settings_save_request_support_type_mapping import (
            AtlassianSettingsSaveRequestSupportTypeMapping,
        )

        d = dict(src_dict)
        api_url = d.pop("api_url")

        auth_method = AuthMethodEnum(d.pop("auth_method"))

        project_id = d.pop("project_id")

        confirm_save = d.pop("confirm_save")

        email = d.pop("email", UNSET)

        token = d.pop("token", UNSET)

        personal_access_token = d.pop("personal_access_token", UNSET)

        username = d.pop("username", UNSET)

        password = d.pop("password", UNSET)

        verify_ssl = d.pop("verify_ssl", UNSET)

        issue_types = cast(list[str], d.pop("issue_types", UNSET))

        _support_type_mapping = d.pop("support_type_mapping", UNSET)
        support_type_mapping: Union[Unset, AtlassianSettingsSaveRequestSupportTypeMapping]
        if isinstance(_support_type_mapping, Unset):
            support_type_mapping = UNSET
        else:
            support_type_mapping = AtlassianSettingsSaveRequestSupportTypeMapping.from_dict(_support_type_mapping)

        reporter_field = d.pop("reporter_field", UNSET)

        impact_field = d.pop("impact_field", UNSET)

        organisation_field = d.pop("organisation_field", UNSET)

        project_field = d.pop("project_field", UNSET)

        affected_resource_field = d.pop("affected_resource_field", UNSET)

        caller_field = d.pop("caller_field", UNSET)

        template_field = d.pop("template_field", UNSET)

        sla_field = d.pop("sla_field", UNSET)

        resolution_sla_field = d.pop("resolution_sla_field", UNSET)

        satisfaction_field = d.pop("satisfaction_field", UNSET)

        request_feedback_field = d.pop("request_feedback_field", UNSET)

        waldur_backend_id_field = d.pop("waldur_backend_id_field", UNSET)

        default_offering_issue_type = d.pop("default_offering_issue_type", UNSET)

        use_old_api = d.pop("use_old_api", UNSET)

        custom_field_mapping_enabled = d.pop("custom_field_mapping_enabled", UNSET)

        atlassian_settings_save_request = cls(
            api_url=api_url,
            auth_method=auth_method,
            project_id=project_id,
            confirm_save=confirm_save,
            email=email,
            token=token,
            personal_access_token=personal_access_token,
            username=username,
            password=password,
            verify_ssl=verify_ssl,
            issue_types=issue_types,
            support_type_mapping=support_type_mapping,
            reporter_field=reporter_field,
            impact_field=impact_field,
            organisation_field=organisation_field,
            project_field=project_field,
            affected_resource_field=affected_resource_field,
            caller_field=caller_field,
            template_field=template_field,
            sla_field=sla_field,
            resolution_sla_field=resolution_sla_field,
            satisfaction_field=satisfaction_field,
            request_feedback_field=request_feedback_field,
            waldur_backend_id_field=waldur_backend_id_field,
            default_offering_issue_type=default_offering_issue_type,
            use_old_api=use_old_api,
            custom_field_mapping_enabled=custom_field_mapping_enabled,
        )

        atlassian_settings_save_request.additional_properties = d
        return atlassian_settings_save_request

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
