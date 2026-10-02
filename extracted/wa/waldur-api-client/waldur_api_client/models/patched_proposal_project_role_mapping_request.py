from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedProposalProjectRoleMappingRequest")


@_attrs_define
class PatchedProposalProjectRoleMappingRequest:
    """
    Attributes:
        call (Union[Unset, str]):
        proposal_role (Union[Unset, str]):
        project_role (Union[None, Unset, str]):
    """

    call: Union[Unset, str] = UNSET
    proposal_role: Union[Unset, str] = UNSET
    project_role: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        call = self.call

        proposal_role = self.proposal_role

        project_role: Union[None, Unset, str]
        if isinstance(self.project_role, Unset):
            project_role = UNSET
        else:
            project_role = self.project_role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if call is not UNSET:
            field_dict["call"] = call
        if proposal_role is not UNSET:
            field_dict["proposal_role"] = proposal_role
        if project_role is not UNSET:
            field_dict["project_role"] = project_role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        call = d.pop("call", UNSET)

        proposal_role = d.pop("proposal_role", UNSET)

        def _parse_project_role(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_role = _parse_project_role(d.pop("project_role", UNSET))

        patched_proposal_project_role_mapping_request = cls(
            call=call,
            proposal_role=proposal_role,
            project_role=project_role,
        )

        patched_proposal_project_role_mapping_request.additional_properties = d
        return patched_proposal_project_role_mapping_request

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
