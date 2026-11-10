from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.patched_rancher_application_request_answers import PatchedRancherApplicationRequestAnswers


T = TypeVar("T", bound="PatchedRancherApplicationRequest")


@_attrs_define
class PatchedRancherApplicationRequest:
    """
    Attributes:
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        version (Union[Unset, str]):
        answers (Union[Unset, PatchedRancherApplicationRequestAnswers]):
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    answers: Union[Unset, "PatchedRancherApplicationRequestAnswers"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        version = self.version

        answers: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.answers, Unset):
            answers = self.answers.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if version is not UNSET:
            field_dict["version"] = version
        if answers is not UNSET:
            field_dict["answers"] = answers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.patched_rancher_application_request_answers import PatchedRancherApplicationRequestAnswers

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        version = d.pop("version", UNSET)

        _answers = d.pop("answers", UNSET)
        answers: Union[Unset, PatchedRancherApplicationRequestAnswers]
        if isinstance(_answers, Unset):
            answers = UNSET
        else:
            answers = PatchedRancherApplicationRequestAnswers.from_dict(_answers)

        patched_rancher_application_request = cls(
            name=name,
            description=description,
            version=version,
            answers=answers,
        )

        patched_rancher_application_request.additional_properties = d
        return patched_rancher_application_request

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
