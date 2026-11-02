from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.check_subject_kind import CheckSubjectKind
from ..types import UNSET, Unset






T = TypeVar("T", bound="CheckSubject")



@_attrs_define
class CheckSubject:
    """ 
        Attributes:
            kind (CheckSubjectKind):
            forge (str):
            full_name (str): The repository, as `owner/repo`.
            number (int | Unset): The pull request number. Required for `pull_request`.
     """

    kind: CheckSubjectKind
    forge: str
    full_name: str
    number: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        forge = self.forge

        full_name = self.full_name

        number = self.number


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "kind": kind,
            "forge": forge,
            "fullName": full_name,
        })
        if number is not UNSET:
            field_dict["number"] = number

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = CheckSubjectKind(d.pop("kind"))




        forge = d.pop("forge")

        full_name = d.pop("fullName")

        number = d.pop("number", UNSET)

        check_subject = cls(
            kind=kind,
            forge=forge,
            full_name=full_name,
            number=number,
        )


        check_subject.additional_properties = d
        return check_subject

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
