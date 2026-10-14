from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.proposal_field_state_enum import ProposalFieldStateEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="CallProposalFieldConfig")


@_attrs_define
class CallProposalFieldConfig:
    """
    Attributes:
        field_project_summary (Union[Unset, ProposalFieldStateEnum]):
        field_description (Union[Unset, ProposalFieldStateEnum]):
        field_science_sub_domain (Union[Unset, ProposalFieldStateEnum]):
        field_supporting_documentation (Union[Unset, ProposalFieldStateEnum]):
    """

    field_project_summary: Union[Unset, ProposalFieldStateEnum] = UNSET
    field_description: Union[Unset, ProposalFieldStateEnum] = UNSET
    field_science_sub_domain: Union[Unset, ProposalFieldStateEnum] = UNSET
    field_supporting_documentation: Union[Unset, ProposalFieldStateEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_project_summary: Union[Unset, str] = UNSET
        if not isinstance(self.field_project_summary, Unset):
            field_project_summary = self.field_project_summary.value

        field_description: Union[Unset, str] = UNSET
        if not isinstance(self.field_description, Unset):
            field_description = self.field_description.value

        field_science_sub_domain: Union[Unset, str] = UNSET
        if not isinstance(self.field_science_sub_domain, Unset):
            field_science_sub_domain = self.field_science_sub_domain.value

        field_supporting_documentation: Union[Unset, str] = UNSET
        if not isinstance(self.field_supporting_documentation, Unset):
            field_supporting_documentation = self.field_supporting_documentation.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_project_summary is not UNSET:
            field_dict["field_project_summary"] = field_project_summary
        if field_description is not UNSET:
            field_dict["field_description"] = field_description
        if field_science_sub_domain is not UNSET:
            field_dict["field_science_sub_domain"] = field_science_sub_domain
        if field_supporting_documentation is not UNSET:
            field_dict["field_supporting_documentation"] = field_supporting_documentation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _field_project_summary = d.pop("field_project_summary", UNSET)
        field_project_summary: Union[Unset, ProposalFieldStateEnum]
        if isinstance(_field_project_summary, Unset):
            field_project_summary = UNSET
        else:
            field_project_summary = ProposalFieldStateEnum(_field_project_summary)

        _field_description = d.pop("field_description", UNSET)
        field_description: Union[Unset, ProposalFieldStateEnum]
        if isinstance(_field_description, Unset):
            field_description = UNSET
        else:
            field_description = ProposalFieldStateEnum(_field_description)

        _field_science_sub_domain = d.pop("field_science_sub_domain", UNSET)
        field_science_sub_domain: Union[Unset, ProposalFieldStateEnum]
        if isinstance(_field_science_sub_domain, Unset):
            field_science_sub_domain = UNSET
        else:
            field_science_sub_domain = ProposalFieldStateEnum(_field_science_sub_domain)

        _field_supporting_documentation = d.pop("field_supporting_documentation", UNSET)
        field_supporting_documentation: Union[Unset, ProposalFieldStateEnum]
        if isinstance(_field_supporting_documentation, Unset):
            field_supporting_documentation = UNSET
        else:
            field_supporting_documentation = ProposalFieldStateEnum(_field_supporting_documentation)

        call_proposal_field_config = cls(
            field_project_summary=field_project_summary,
            field_description=field_description,
            field_science_sub_domain=field_science_sub_domain,
            field_supporting_documentation=field_supporting_documentation,
        )

        call_proposal_field_config.additional_properties = d
        return call_proposal_field_config

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
