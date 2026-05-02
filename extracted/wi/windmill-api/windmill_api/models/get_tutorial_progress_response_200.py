from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetTutorialProgressResponse200")


@_attrs_define
class GetTutorialProgressResponse200:
    """
    Attributes:
        progress (Union[Unset, int]):
        skipped_all (Union[Unset, bool]):
    """

    progress: Union[Unset, int] = UNSET
    skipped_all: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        progress = self.progress
        skipped_all = self.skipped_all

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if progress is not UNSET:
            field_dict["progress"] = progress
        if skipped_all is not UNSET:
            field_dict["skipped_all"] = skipped_all

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        progress = d.pop("progress", UNSET)

        skipped_all = d.pop("skipped_all", UNSET)

        get_tutorial_progress_response_200 = cls(
            progress=progress,
            skipped_all=skipped_all,
        )

        get_tutorial_progress_response_200.additional_properties = d
        return get_tutorial_progress_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
