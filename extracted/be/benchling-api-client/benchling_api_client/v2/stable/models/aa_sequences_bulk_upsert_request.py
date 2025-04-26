from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.aa_sequence_bulk_upsert_request import AaSequenceBulkUpsertRequest
from ..types import UNSET, Unset

T = TypeVar("T", bound="AaSequencesBulkUpsertRequest")


@attr.s(auto_attribs=True, repr=False)
class AaSequencesBulkUpsertRequest:
    """  """

    _aa_sequences: List[AaSequenceBulkUpsertRequest]

    def __repr__(self):
        fields = []
        fields.append("aa_sequences={}".format(repr(self._aa_sequences)))
        return "AaSequencesBulkUpsertRequest({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        aa_sequences = []
        for aa_sequences_item_data in self._aa_sequences:
            aa_sequences_item = aa_sequences_item_data.to_dict()

            aa_sequences.append(aa_sequences_item)

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if aa_sequences is not UNSET:
            field_dict["aaSequences"] = aa_sequences

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_aa_sequences() -> List[AaSequenceBulkUpsertRequest]:
            aa_sequences = []
            _aa_sequences = d.pop("aaSequences")
            for aa_sequences_item_data in _aa_sequences:
                aa_sequences_item = AaSequenceBulkUpsertRequest.from_dict(
                    aa_sequences_item_data, strict=False
                )

                aa_sequences.append(aa_sequences_item)

            return aa_sequences

        try:
            aa_sequences = get_aa_sequences()
        except KeyError:
            if strict:
                raise
            aa_sequences = cast(List[AaSequenceBulkUpsertRequest], UNSET)

        aa_sequences_bulk_upsert_request = cls(
            aa_sequences=aa_sequences,
        )

        return aa_sequences_bulk_upsert_request

    @property
    def aa_sequences(self) -> List[AaSequenceBulkUpsertRequest]:
        if isinstance(self._aa_sequences, Unset):
            raise NotPresentError(self, "aa_sequences")
        return self._aa_sequences

    @aa_sequences.setter
    def aa_sequences(self, value: List[AaSequenceBulkUpsertRequest]) -> None:
        self._aa_sequences = value
