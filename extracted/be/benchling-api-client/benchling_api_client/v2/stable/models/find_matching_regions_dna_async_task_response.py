from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.find_matching_regions_dna_async_task_response_dna_sequence_matches_item import (
    FindMatchingRegionsDnaAsyncTaskResponseDnaSequenceMatchesItem,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="FindMatchingRegionsDnaAsyncTaskResponse")


@attr.s(auto_attribs=True, repr=False)
class FindMatchingRegionsDnaAsyncTaskResponse:
    """  """

    _dna_sequence_matches: Union[
        Unset, List[FindMatchingRegionsDnaAsyncTaskResponseDnaSequenceMatchesItem]
    ] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("dna_sequence_matches={}".format(repr(self._dna_sequence_matches)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "FindMatchingRegionsDnaAsyncTaskResponse({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        dna_sequence_matches: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._dna_sequence_matches, Unset):
            dna_sequence_matches = []
            for dna_sequence_matches_item_data in self._dna_sequence_matches:
                dna_sequence_matches_item = dna_sequence_matches_item_data.to_dict()

                dna_sequence_matches.append(dna_sequence_matches_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if dna_sequence_matches is not UNSET:
            field_dict["dnaSequenceMatches"] = dna_sequence_matches

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_dna_sequence_matches() -> Union[
            Unset, List[FindMatchingRegionsDnaAsyncTaskResponseDnaSequenceMatchesItem]
        ]:
            dna_sequence_matches = []
            _dna_sequence_matches = d.pop("dnaSequenceMatches")
            for dna_sequence_matches_item_data in _dna_sequence_matches or []:
                dna_sequence_matches_item = (
                    FindMatchingRegionsDnaAsyncTaskResponseDnaSequenceMatchesItem.from_dict(
                        dna_sequence_matches_item_data, strict=False
                    )
                )

                dna_sequence_matches.append(dna_sequence_matches_item)

            return dna_sequence_matches

        try:
            dna_sequence_matches = get_dna_sequence_matches()
        except KeyError:
            if strict:
                raise
            dna_sequence_matches = cast(
                Union[Unset, List[FindMatchingRegionsDnaAsyncTaskResponseDnaSequenceMatchesItem]], UNSET
            )

        find_matching_regions_dna_async_task_response = cls(
            dna_sequence_matches=dna_sequence_matches,
        )

        find_matching_regions_dna_async_task_response.additional_properties = d
        return find_matching_regions_dna_async_task_response

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
    def dna_sequence_matches(self) -> List[FindMatchingRegionsDnaAsyncTaskResponseDnaSequenceMatchesItem]:
        if isinstance(self._dna_sequence_matches, Unset):
            raise NotPresentError(self, "dna_sequence_matches")
        return self._dna_sequence_matches

    @dna_sequence_matches.setter
    def dna_sequence_matches(
        self, value: List[FindMatchingRegionsDnaAsyncTaskResponseDnaSequenceMatchesItem]
    ) -> None:
        self._dna_sequence_matches = value

    @dna_sequence_matches.deleter
    def dna_sequence_matches(self) -> None:
        self._dna_sequence_matches = UNSET
