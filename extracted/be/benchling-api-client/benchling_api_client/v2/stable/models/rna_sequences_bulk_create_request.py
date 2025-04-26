from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.rna_sequence_bulk_create import RnaSequenceBulkCreate
from ..types import UNSET, Unset

T = TypeVar("T", bound="RnaSequencesBulkCreateRequest")


@attr.s(auto_attribs=True, repr=False)
class RnaSequencesBulkCreateRequest:
    """  """

    _rna_sequences: Union[Unset, List[RnaSequenceBulkCreate]] = UNSET

    def __repr__(self):
        fields = []
        fields.append("rna_sequences={}".format(repr(self._rna_sequences)))
        return "RnaSequencesBulkCreateRequest({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        rna_sequences: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._rna_sequences, Unset):
            rna_sequences = []
            for rna_sequences_item_data in self._rna_sequences:
                rna_sequences_item = rna_sequences_item_data.to_dict()

                rna_sequences.append(rna_sequences_item)

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if rna_sequences is not UNSET:
            field_dict["rnaSequences"] = rna_sequences

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_rna_sequences() -> Union[Unset, List[RnaSequenceBulkCreate]]:
            rna_sequences = []
            _rna_sequences = d.pop("rnaSequences")
            for rna_sequences_item_data in _rna_sequences or []:
                rna_sequences_item = RnaSequenceBulkCreate.from_dict(rna_sequences_item_data, strict=False)

                rna_sequences.append(rna_sequences_item)

            return rna_sequences

        try:
            rna_sequences = get_rna_sequences()
        except KeyError:
            if strict:
                raise
            rna_sequences = cast(Union[Unset, List[RnaSequenceBulkCreate]], UNSET)

        rna_sequences_bulk_create_request = cls(
            rna_sequences=rna_sequences,
        )

        return rna_sequences_bulk_create_request

    @property
    def rna_sequences(self) -> List[RnaSequenceBulkCreate]:
        if isinstance(self._rna_sequences, Unset):
            raise NotPresentError(self, "rna_sequences")
        return self._rna_sequences

    @rna_sequences.setter
    def rna_sequences(self, value: List[RnaSequenceBulkCreate]) -> None:
        self._rna_sequences = value

    @rna_sequences.deleter
    def rna_sequences(self) -> None:
        self._rna_sequences = UNSET
