from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.entity_archive_reason import EntityArchiveReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="DnaSequencesArchive")


@attr.s(auto_attribs=True, repr=False)
class DnaSequencesArchive:
    """The request body for archiving DNA sequences."""

    _dna_sequence_ids: List[str]
    _reason: EntityArchiveReason

    def __repr__(self):
        fields = []
        fields.append("dna_sequence_ids={}".format(repr(self._dna_sequence_ids)))
        fields.append("reason={}".format(repr(self._reason)))
        return "DnaSequencesArchive({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        dna_sequence_ids = self._dna_sequence_ids

        reason = self._reason.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if dna_sequence_ids is not UNSET:
            field_dict["dnaSequenceIds"] = dna_sequence_ids
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_dna_sequence_ids() -> List[str]:
            dna_sequence_ids = cast(List[str], d.pop("dnaSequenceIds"))

            return dna_sequence_ids

        try:
            dna_sequence_ids = get_dna_sequence_ids()
        except KeyError:
            if strict:
                raise
            dna_sequence_ids = cast(List[str], UNSET)

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

        dna_sequences_archive = cls(
            dna_sequence_ids=dna_sequence_ids,
            reason=reason,
        )

        return dna_sequences_archive

    @property
    def dna_sequence_ids(self) -> List[str]:
        if isinstance(self._dna_sequence_ids, Unset):
            raise NotPresentError(self, "dna_sequence_ids")
        return self._dna_sequence_ids

    @dna_sequence_ids.setter
    def dna_sequence_ids(self, value: List[str]) -> None:
        self._dna_sequence_ids = value

    @property
    def reason(self) -> EntityArchiveReason:
        """The reason for archiving the provided entities. Accepted reasons may differ based on tenant configuration."""
        if isinstance(self._reason, Unset):
            raise NotPresentError(self, "reason")
        return self._reason

    @reason.setter
    def reason(self, value: EntityArchiveReason) -> None:
        self._reason = value
