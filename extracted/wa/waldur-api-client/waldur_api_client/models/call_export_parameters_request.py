from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CallExportParametersRequest")


@_attrs_define
class CallExportParametersRequest:
    """
    Attributes:
        include_documents (Union[Unset, bool]):  Default: True.
        include_rounds (Union[Unset, bool]):  Default: True.
        include_offerings (Union[Unset, bool]): Requested offerings together with their resource templates. Default:
            True.
        include_workflow_steps (Union[Unset, bool]): Workflow steps with their notification rules and criteria. Default:
            True.
        include_field_configs (Union[Unset, bool]): Proposal field and applicant visibility configuration. Default:
            True.
        include_review_configs (Union[Unset, bool]): COI, reviewer matching and assignment configuration. Default: True.
        include_role_mappings (Union[Unset, bool]):  Default: True.
        include_compliance_checklist (Union[Unset, bool]):  Default: True.
    """

    include_documents: Union[Unset, bool] = True
    include_rounds: Union[Unset, bool] = True
    include_offerings: Union[Unset, bool] = True
    include_workflow_steps: Union[Unset, bool] = True
    include_field_configs: Union[Unset, bool] = True
    include_review_configs: Union[Unset, bool] = True
    include_role_mappings: Union[Unset, bool] = True
    include_compliance_checklist: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        include_documents = self.include_documents

        include_rounds = self.include_rounds

        include_offerings = self.include_offerings

        include_workflow_steps = self.include_workflow_steps

        include_field_configs = self.include_field_configs

        include_review_configs = self.include_review_configs

        include_role_mappings = self.include_role_mappings

        include_compliance_checklist = self.include_compliance_checklist

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if include_documents is not UNSET:
            field_dict["include_documents"] = include_documents
        if include_rounds is not UNSET:
            field_dict["include_rounds"] = include_rounds
        if include_offerings is not UNSET:
            field_dict["include_offerings"] = include_offerings
        if include_workflow_steps is not UNSET:
            field_dict["include_workflow_steps"] = include_workflow_steps
        if include_field_configs is not UNSET:
            field_dict["include_field_configs"] = include_field_configs
        if include_review_configs is not UNSET:
            field_dict["include_review_configs"] = include_review_configs
        if include_role_mappings is not UNSET:
            field_dict["include_role_mappings"] = include_role_mappings
        if include_compliance_checklist is not UNSET:
            field_dict["include_compliance_checklist"] = include_compliance_checklist

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        include_documents = d.pop("include_documents", UNSET)

        include_rounds = d.pop("include_rounds", UNSET)

        include_offerings = d.pop("include_offerings", UNSET)

        include_workflow_steps = d.pop("include_workflow_steps", UNSET)

        include_field_configs = d.pop("include_field_configs", UNSET)

        include_review_configs = d.pop("include_review_configs", UNSET)

        include_role_mappings = d.pop("include_role_mappings", UNSET)

        include_compliance_checklist = d.pop("include_compliance_checklist", UNSET)

        call_export_parameters_request = cls(
            include_documents=include_documents,
            include_rounds=include_rounds,
            include_offerings=include_offerings,
            include_workflow_steps=include_workflow_steps,
            include_field_configs=include_field_configs,
            include_review_configs=include_review_configs,
            include_role_mappings=include_role_mappings,
            include_compliance_checklist=include_compliance_checklist,
        )

        call_export_parameters_request.additional_properties = d
        return call_export_parameters_request

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
