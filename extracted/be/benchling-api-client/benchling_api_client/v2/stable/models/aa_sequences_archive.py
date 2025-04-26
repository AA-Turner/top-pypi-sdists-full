from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.entity_archive_reason import EntityArchiveReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="AaSequencesArchive")


@attr.s(auto_attribs=True, repr=False)
class AaSequencesArchive:
    """The request body for archiving AA sequences."""

    _aa_sequence_ids: List[str]
    _reason: EntityArchiveReason

    def __repr__(self):
        fields = []
        fields.append("aa_sequence_ids={}".format(repr(self._aa_sequence_ids)))
        fields.append("reason={}".format(repr(self._reason)))
        return "AaSequencesArchive({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        aa_sequence_ids = self._aa_sequence_ids

        reason = self._reason.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if aa_sequence_ids is not UNSET:
            field_dict["aaSequenceIds"] = aa_sequence_ids
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_aa_sequence_ids() -> List[str]:
            aa_sequence_ids = cast(List[str], d.pop("aaSequenceIds"))

            return aa_sequence_ids

        try:
            aa_sequence_ids = get_aa_sequence_ids()
        except KeyError:
            if strict:
                raise
            aa_sequence_ids = cast(List[str], UNSET)

        def get_reason() -> EntityArchiveReason:
            _reason = d.pop("reason")
            try:
                reason = EntityArchiveReason(_reason)
            except ValueError:
                reason = EntityArchiveReason.of_unknown(_reason)

            return reason

        try:
            reason = get_reason()
        except KeyError:
            if strict:
                raise
            reason = cast(EntityArchiveReason, UNSET)

        aa_sequences_archive = cls(
            aa_sequence_ids=aa_sequence_ids,
            reason=reason,
        )

        return aa_sequences_archive

    @property
    def aa_sequence_ids(self) -> List[str]:
        if isinstance(self._aa_sequence_ids, Unset):
            raise NotPresentError(self, "aa_sequence_ids")
        return self._aa_sequence_ids

    @aa_sequence_ids.setter
    def aa_sequence_ids(self, value: List[str]) -> None:
        self._aa_sequence_ids = value

    @property
    def reason(self) -> EntityArchiveReason:
        """The reason for archiving the provided entities. Accepted reasons may differ based on tenant configuration."""
        if isinstance(self._reason, Unset):
            raise NotPresentError(self, "reason")
        return self._reason

    @reason.setter
    def reason(self, value: EntityArchiveReason) -> None:
        self._reason = value
