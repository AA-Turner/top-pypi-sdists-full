from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.find_matching_regions_async_task_response_aa_sequence_matches_item import (
    FindMatchingRegionsAsyncTaskResponseAaSequenceMatchesItem,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="FindMatchingRegionsAsyncTaskResponse")


@attr.s(auto_attribs=True, repr=False)
class FindMatchingRegionsAsyncTaskResponse:
    """  """

    _aa_sequence_matches: Union[
        Unset, List[FindMatchingRegionsAsyncTaskResponseAaSequenceMatchesItem]
    ] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("aa_sequence_matches={}".format(repr(self._aa_sequence_matches)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "FindMatchingRegionsAsyncTaskResponse({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        aa_sequence_matches: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._aa_sequence_matches, Unset):
            aa_sequence_matches = []
            for aa_sequence_matches_item_data in self._aa_sequence_matches:
                aa_sequence_matches_item = aa_sequence_matches_item_data.to_dict()

                aa_sequence_matches.append(aa_sequence_matches_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if aa_sequence_matches is not UNSET:
            field_dict["aaSequenceMatches"] = aa_sequence_matches

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_aa_sequence_matches() -> Union[
            Unset, List[FindMatchingRegionsAsyncTaskResponseAaSequenceMatchesItem]
        ]:
            aa_sequence_matches = []
            _aa_sequence_matches = d.pop("aaSequenceMatches")
            for aa_sequence_matches_item_data in _aa_sequence_matches or []:
                aa_sequence_matches_item = (
                    FindMatchingRegionsAsyncTaskResponseAaSequenceMatchesItem.from_dict(
                        aa_sequence_matches_item_data, strict=False
                    )
                )

                aa_sequence_matches.append(aa_sequence_matches_item)

            return aa_sequence_matches

        try:
            aa_sequence_matches = get_aa_sequence_matches()
        except KeyError:
            if strict:
                raise
            aa_sequence_matches = cast(
                Union[Unset, List[FindMatchingRegionsAsyncTaskResponseAaSequenceMatchesItem]], UNSET
            )

        find_matching_regions_async_task_response = cls(
            aa_sequence_matches=aa_sequence_matches,
        )

        find_matching_regions_async_task_response.additional_properties = d
        return find_matching_regions_async_task_response

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
    def aa_sequence_matches(self) -> List[FindMatchingRegionsAsyncTaskResponseAaSequenceMatchesItem]:
        if isinstance(self._aa_sequence_matches, Unset):
            raise NotPresentError(self, "aa_sequence_matches")
        return self._aa_sequence_matches

    @aa_sequence_matches.setter
    def aa_sequence_matches(
        self, value: List[FindMatchingRegionsAsyncTaskResponseAaSequenceMatchesItem]
    ) -> None:
        self._aa_sequence_matches = value

    @aa_sequence_matches.deleter
    def aa_sequence_matches(self) -> None:
        self._aa_sequence_matches = UNSET
