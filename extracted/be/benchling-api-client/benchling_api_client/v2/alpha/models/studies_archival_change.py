from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="StudiesArchivalChange")


@attr.s(auto_attribs=True, repr=False)
class StudiesArchivalChange:
    """IDs of all items that were archived or unarchived."""

    _study_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("study_ids={}".format(repr(self._study_ids)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "StudiesArchivalChange({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        study_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._study_ids, Unset):
            study_ids = self._study_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if study_ids is not UNSET:
            field_dict["studyIds"] = study_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_study_ids() -> Union[Unset, List[str]]:
            study_ids = cast(List[str], d.pop("studyIds"))

            return study_ids

        try:
            study_ids = get_study_ids()
        except KeyError:
            if strict:
                raise
            study_ids = cast(Union[Unset, List[str]], UNSET)

        studies_archival_change = cls(
            study_ids=study_ids,
        )

        studies_archival_change.additional_properties = d
        return studies_archival_change

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

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def study_ids(self) -> List[str]:
        if isinstance(self._study_ids, Unset):
            raise NotPresentError(self, "study_ids")
        return self._study_ids

    @study_ids.setter
    def study_ids(self, value: List[str]) -> None:
        self._study_ids = value

    @study_ids.deleter
    def study_ids(self) -> None:
        self._study_ids = UNSET
