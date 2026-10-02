from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="UpdateRubricBodyDto")



@_attrs_define
class UpdateRubricBodyDto:
    """ Request body for partially updating an existing rubric.

        Example:
            {'criterion': 'Correctly identifies all surface defects and reports none that are absent', 'weight': 3,
                'useGraderSupport': True}

        Attributes:
            criterion (str | Unset): New criterion text.
            weight (float | Unset): New non-zero weight for the rubric. Example: 2.
            use_grader_support (bool | Unset): Toggle whether the LLM grader evaluates this rubric.
            issue_template (None | str | Unset): New per-rubric issue template override. Send null (not an empty string) to
                clear the override and inherit the environment-wide template.
     """

    criterion: str | Unset = UNSET
    weight: float | Unset = UNSET
    use_grader_support: bool | Unset = UNSET
    issue_template: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        criterion = self.criterion

        weight = self.weight

        use_grader_support = self.use_grader_support

        issue_template: None | str | Unset
        if isinstance(self.issue_template, Unset):
            issue_template = UNSET
        else:
            issue_template = self.issue_template


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if criterion is not UNSET:
            field_dict["criterion"] = criterion
        if weight is not UNSET:
            field_dict["weight"] = weight
        if use_grader_support is not UNSET:
            field_dict["useGraderSupport"] = use_grader_support
        if issue_template is not UNSET:
            field_dict["issueTemplate"] = issue_template

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        criterion = d.pop("criterion", UNSET)

        weight = d.pop("weight", UNSET)

        use_grader_support = d.pop("useGraderSupport", UNSET)

        def _parse_issue_template(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        issue_template = _parse_issue_template(d.pop("issueTemplate", UNSET))


        update_rubric_body_dto = cls(
            criterion=criterion,
            weight=weight,
            use_grader_support=use_grader_support,
            issue_template=issue_template,
        )


        update_rubric_body_dto.additional_properties = d
        return update_rubric_body_dto

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
