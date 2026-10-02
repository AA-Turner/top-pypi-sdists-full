from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DuplicateCallRequestRequest")


@_attrs_define
class DuplicateCallRequestRequest:
    """
    Attributes:
        name (str):
        copy_documents (Union[Unset, bool]):  Default: True.
        copy_offerings (Union[Unset, bool]):  Default: True.
        copy_rounds (Union[Unset, bool]):  Default: True.
        copy_workflow_steps (Union[Unset, bool]):  Default: True.
        copy_resource_templates (Union[Unset, bool]):  Default: True.
        copy_role_mappings (Union[Unset, bool]):  Default: True.
        copy_applicant_visibility_config (Union[Unset, bool]):  Default: True.
        copy_coi_configuration (Union[Unset, bool]):  Default: True.
        copy_matching_configuration (Union[Unset, bool]):  Default: True.
        copy_assignment_configuration (Union[Unset, bool]):  Default: True.
    """

    name: str
    copy_documents: Union[Unset, bool] = True
    copy_offerings: Union[Unset, bool] = True
    copy_rounds: Union[Unset, bool] = True
    copy_workflow_steps: Union[Unset, bool] = True
    copy_resource_templates: Union[Unset, bool] = True
    copy_role_mappings: Union[Unset, bool] = True
    copy_applicant_visibility_config: Union[Unset, bool] = True
    copy_coi_configuration: Union[Unset, bool] = True
    copy_matching_configuration: Union[Unset, bool] = True
    copy_assignment_configuration: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        copy_documents = self.copy_documents

        copy_offerings = self.copy_offerings

        copy_rounds = self.copy_rounds

        copy_workflow_steps = self.copy_workflow_steps

        copy_resource_templates = self.copy_resource_templates

        copy_role_mappings = self.copy_role_mappings

        copy_applicant_visibility_config = self.copy_applicant_visibility_config

        copy_coi_configuration = self.copy_coi_configuration

        copy_matching_configuration = self.copy_matching_configuration

        copy_assignment_configuration = self.copy_assignment_configuration

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if copy_documents is not UNSET:
            field_dict["copy_documents"] = copy_documents
        if copy_offerings is not UNSET:
            field_dict["copy_offerings"] = copy_offerings
        if copy_rounds is not UNSET:
            field_dict["copy_rounds"] = copy_rounds
        if copy_workflow_steps is not UNSET:
            field_dict["copy_workflow_steps"] = copy_workflow_steps
        if copy_resource_templates is not UNSET:
            field_dict["copy_resource_templates"] = copy_resource_templates
        if copy_role_mappings is not UNSET:
            field_dict["copy_role_mappings"] = copy_role_mappings
        if copy_applicant_visibility_config is not UNSET:
            field_dict["copy_applicant_visibility_config"] = copy_applicant_visibility_config
        if copy_coi_configuration is not UNSET:
            field_dict["copy_coi_configuration"] = copy_coi_configuration
        if copy_matching_configuration is not UNSET:
            field_dict["copy_matching_configuration"] = copy_matching_configuration
        if copy_assignment_configuration is not UNSET:
            field_dict["copy_assignment_configuration"] = copy_assignment_configuration

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        copy_documents = d.pop("copy_documents", UNSET)

        copy_offerings = d.pop("copy_offerings", UNSET)

        copy_rounds = d.pop("copy_rounds", UNSET)

        copy_workflow_steps = d.pop("copy_workflow_steps", UNSET)

        copy_resource_templates = d.pop("copy_resource_templates", UNSET)

        copy_role_mappings = d.pop("copy_role_mappings", UNSET)

        copy_applicant_visibility_config = d.pop("copy_applicant_visibility_config", UNSET)

        copy_coi_configuration = d.pop("copy_coi_configuration", UNSET)

        copy_matching_configuration = d.pop("copy_matching_configuration", UNSET)

        copy_assignment_configuration = d.pop("copy_assignment_configuration", UNSET)

        duplicate_call_request_request = cls(
            name=name,
            copy_documents=copy_documents,
            copy_offerings=copy_offerings,
            copy_rounds=copy_rounds,
            copy_workflow_steps=copy_workflow_steps,
            copy_resource_templates=copy_resource_templates,
            copy_role_mappings=copy_role_mappings,
            copy_applicant_visibility_config=copy_applicant_visibility_config,
            copy_coi_configuration=copy_coi_configuration,
            copy_matching_configuration=copy_matching_configuration,
            copy_assignment_configuration=copy_assignment_configuration,
        )

        duplicate_call_request_request.additional_properties = d
        return duplicate_call_request_request

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
