from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="AutoAnnotateRnaSequences")


@attr.s(auto_attribs=True, repr=False)
class AutoAnnotateRnaSequences:
    """  """

    _feature_library_ids: List[str]
    _rna_sequence_ids: List[str]

    def __repr__(self):
        fields = []
        fields.append("feature_library_ids={}".format(repr(self._feature_library_ids)))
        fields.append("rna_sequence_ids={}".format(repr(self._rna_sequence_ids)))
        return "AutoAnnotateRnaSequences({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        feature_library_ids = self._feature_library_ids

        rna_sequence_ids = self._rna_sequence_ids

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if feature_library_ids is not UNSET:
            field_dict["featureLibraryIds"] = feature_library_ids
        if rna_sequence_ids is not UNSET:
            field_dict["rnaSequenceIds"] = rna_sequence_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_feature_library_ids() -> List[str]:
            feature_library_ids = cast(List[str], d.pop("featureLibraryIds"))

            return feature_library_ids

        try:
            feature_library_ids = get_feature_library_ids()
        except KeyError:
            if strict:
                raise
            feature_library_ids = cast(List[str], UNSET)

        def get_rna_sequence_ids() -> List[str]:
            rna_sequence_ids = cast(List[str], d.pop("rnaSequenceIds"))

            return rna_sequence_ids

        try:
            rna_sequence_ids = get_rna_sequence_ids()
        except KeyError:
            if strict:
                raise
            rna_sequence_ids = cast(List[str], UNSET)

        auto_annotate_rna_sequences = cls(
            feature_library_ids=feature_library_ids,
            rna_sequence_ids=rna_sequence_ids,
        )

        return auto_annotate_rna_sequences

    @property
    def feature_library_ids(self) -> List[str]:
        """ Array of feature library IDs. """
        if isinstance(self._feature_library_ids, Unset):
            raise NotPresentError(self, "feature_library_ids")
        return self._feature_library_ids

    @feature_library_ids.setter
    def feature_library_ids(self, value: List[str]) -> None:
        self._feature_library_ids = value

    @property
    def rna_sequence_ids(self) -> List[str]:
        """ Array of RNA sequence IDs. """
        if isinstance(self._rna_sequence_ids, Unset):
            raise NotPresentError(self, "rna_sequence_ids")
        return self._rna_sequence_ids

    @rna_sequence_ids.setter
    def rna_sequence_ids(self, value: List[str]) -> None:
        self._rna_sequence_ids = value
