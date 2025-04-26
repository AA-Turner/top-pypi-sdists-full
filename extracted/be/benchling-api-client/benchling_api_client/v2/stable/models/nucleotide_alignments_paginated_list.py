from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.nucleotide_alignment_summary import NucleotideAlignmentSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="NucleotideAlignmentsPaginatedList")


@attr.s(auto_attribs=True, repr=False)
class NucleotideAlignmentsPaginatedList:
    """  """

    _alignments: Union[Unset, List[NucleotideAlignmentSummary]] = UNSET
    _next_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("alignments={}".format(repr(self._alignments)))
        fields.append("next_token={}".format(repr(self._next_token)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "NucleotideAlignmentsPaginatedList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        alignments: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._alignments, Unset):
            alignments = []
            for alignments_item_data in self._alignments:
                alignments_item = alignments_item_data.to_dict()

                alignments.append(alignments_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if alignments is not UNSET:
            field_dict["alignments"] = alignments
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_alignments() -> Union[Unset, List[NucleotideAlignmentSummary]]:
            alignments = []
            _alignments = d.pop("alignments")
            for alignments_item_data in _alignments or []:
                alignments_item = NucleotideAlignmentSummary.from_dict(alignments_item_data, strict=False)

                alignments.append(alignments_item)

            return alignments

        try:
            alignments = get_alignments()
        except KeyError:
            if strict:
                raise
            alignments = cast(Union[Unset, List[NucleotideAlignmentSummary]], UNSET)

        def get_next_token() -> Union[Unset, str]:
            next_token = d.pop("nextToken")
            return next_token

        try:
            next_token = get_next_token()
        except KeyError:
            if strict:
                raise
            next_token = cast(Union[Unset, str], UNSET)

        nucleotide_alignments_paginated_list = cls(
            alignments=alignments,
            next_token=next_token,
        )

        nucleotide_alignments_paginated_list.additional_properties = d
        return nucleotide_alignments_paginated_list

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
    def alignments(self) -> List[NucleotideAlignmentSummary]:
        if isinstance(self._alignments, Unset):
            raise NotPresentError(self, "alignments")
        return self._alignments

    @alignments.setter
    def alignments(self, value: List[NucleotideAlignmentSummary]) -> None:
        self._alignments = value

    @alignments.deleter
    def alignments(self) -> None:
        self._alignments = UNSET

    @property
    def next_token(self) -> str:
        if isinstance(self._next_token, Unset):
            raise NotPresentError(self, "next_token")
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @next_token.deleter
    def next_token(self) -> None:
        self._next_token = UNSET
