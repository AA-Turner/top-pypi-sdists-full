from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.studies_archive_reason import StudiesArchiveReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="StudiesArchive")


@attr.s(auto_attribs=True, repr=False)
class StudiesArchive:
    """The request body for archiving Studies."""

    _reason: StudiesArchiveReason
    _study_ids: List[str]

    def __repr__(self):
        fields = []
        fields.append("reason={}".format(repr(self._reason)))
        fields.append("study_ids={}".format(repr(self._study_ids)))
        return "StudiesArchive({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        reason = self._reason.value

        study_ids = self._study_ids

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if reason is not UNSET:
            field_dict["reason"] = reason
        if study_ids is not UNSET:
            field_dict["studyIds"] = study_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_reason() -> StudiesArchiveReason:
            _reason = d.pop("reason")
            try:
                reason = StudiesArchiveReason(_reason)
            except ValueError:
                reason = StudiesArchiveReason.of_unknown(_reason)

            return reason

        try:
            reason = get_reason()
        except KeyError:
            if strict:
                raise
            reason = cast(StudiesArchiveReason, UNSET)

        def get_study_ids() -> List[str]:
            study_ids = cast(List[str], d.pop("studyIds"))

            return study_ids

        try:
            study_ids = get_study_ids()
        except KeyError:
            if strict:
                raise
            study_ids = cast(List[str], UNSET)

        studies_archive = cls(
            reason=reason,
            study_ids=study_ids,
        )

        return studies_archive

    @property
    def reason(self) -> StudiesArchiveReason:
        """The reason for archiving the provided Studies. Accepted reasons may differ based on tenant configuration."""
        if isinstance(self._reason, Unset):
            raise NotPresentError(self, "reason")
        return self._reason

    @reason.setter
    def reason(self, value: StudiesArchiveReason) -> None:
        self._reason = value

    @property
    def study_ids(self) -> List[str]:
        if isinstance(self._study_ids, Unset):
            raise NotPresentError(self, "study_ids")
        return self._study_ids

    @study_ids.setter
    def study_ids(self, value: List[str]) -> None:
        self._study_ids = value
