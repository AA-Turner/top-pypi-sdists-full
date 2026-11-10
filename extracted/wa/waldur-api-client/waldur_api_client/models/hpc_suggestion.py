from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.hpc_suggestion_kind_enum import HpcSuggestionKindEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="HpcSuggestion")


@_attrs_define
class HpcSuggestion:
    """
    Attributes:
        kind (HpcSuggestionKindEnum):
        name (Union[None, str]):
        jobs (int):
        message (str):
        current_limit_minutes (Union[Unset, int]):
        suggested_limit_minutes (Union[Unset, int]):
    """

    kind: HpcSuggestionKindEnum
    name: Union[None, str]
    jobs: int
    message: str
    current_limit_minutes: Union[Unset, int] = UNSET
    suggested_limit_minutes: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        name: Union[None, str]
        name = self.name

        jobs = self.jobs

        message = self.message

        current_limit_minutes = self.current_limit_minutes

        suggested_limit_minutes = self.suggested_limit_minutes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "name": name,
                "jobs": jobs,
                "message": message,
            }
        )
        if current_limit_minutes is not UNSET:
            field_dict["current_limit_minutes"] = current_limit_minutes
        if suggested_limit_minutes is not UNSET:
            field_dict["suggested_limit_minutes"] = suggested_limit_minutes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = HpcSuggestionKindEnum(d.pop("kind"))

        def _parse_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        name = _parse_name(d.pop("name"))

        jobs = d.pop("jobs")

        message = d.pop("message")

        current_limit_minutes = d.pop("current_limit_minutes", UNSET)

        suggested_limit_minutes = d.pop("suggested_limit_minutes", UNSET)

        hpc_suggestion = cls(
            kind=kind,
            name=name,
            jobs=jobs,
            message=message,
            current_limit_minutes=current_limit_minutes,
            suggested_limit_minutes=suggested_limit_minutes,
        )

        hpc_suggestion.additional_properties = d
        return hpc_suggestion

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
