from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="StudiesUnarchive")


@attr.s(auto_attribs=True, repr=False)
class StudiesUnarchive:
    """The request body for unarchiving Studies."""

    _study_ids: List[str]

    def __repr__(self):
        fields = []
        fields.append("study_ids={}".format(repr(self._study_ids)))
        return "StudiesUnarchive({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        study_ids = self._study_ids

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if study_ids is not UNSET:
            field_dict["studyIds"] = study_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_study_ids() -> List[str]:
            study_ids = cast(List[str], d.pop("studyIds"))

            return study_ids

        try:
            study_ids = get_study_ids()
        except KeyError:
            if strict:
                raise
            study_ids = cast(List[str], UNSET)

        studies_unarchive = cls(
            study_ids=study_ids,
        )

        return studies_unarchive

    @property
    def study_ids(self) -> List[str]:
        if isinstance(self._study_ids, Unset):
            raise NotPresentError(self, "study_ids")
        return self._study_ids

    @study_ids.setter
    def study_ids(self, value: List[str]) -> None:
        self._study_ids = value
