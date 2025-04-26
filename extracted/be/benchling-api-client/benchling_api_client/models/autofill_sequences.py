from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="AutofillSequences")


@attr.s(auto_attribs=True, repr=False)
class AutofillSequences:
    """  """

    _dna_sequence_ids: List[str]

    def __repr__(self):
        fields = []
        fields.append("dna_sequence_ids={}".format(repr(self._dna_sequence_ids)))
        return "AutofillSequences({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        dna_sequence_ids = self._dna_sequence_ids

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if dna_sequence_ids is not UNSET:
            field_dict["dnaSequenceIds"] = dna_sequence_ids

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

        autofill_sequences = cls(
            dna_sequence_ids=dna_sequence_ids,
        )

        return autofill_sequences

    @property
    def dna_sequence_ids(self) -> List[str]:
        """ Array of DNA sequence IDs. """
        if isinstance(self._dna_sequence_ids, Unset):
            raise NotPresentError(self, "dna_sequence_ids")
        return self._dna_sequence_ids

    @dna_sequence_ids.setter
    def dna_sequence_ids(self, value: List[str]) -> None:
        self._dna_sequence_ids = value
