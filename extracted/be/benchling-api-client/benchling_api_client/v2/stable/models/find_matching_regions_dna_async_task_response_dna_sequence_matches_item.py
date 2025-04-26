from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="FindMatchingRegionsDnaAsyncTaskResponseDnaSequenceMatchesItem")


@attr.s(auto_attribs=True, repr=False)
class FindMatchingRegionsDnaAsyncTaskResponseDnaSequenceMatchesItem:
    """  """

    _matching_dna_sequence_ids: Union[Unset, List[str]] = UNSET
    _target_dna_sequence_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("matching_dna_sequence_ids={}".format(repr(self._matching_dna_sequence_ids)))
        fields.append("target_dna_sequence_id={}".format(repr(self._target_dna_sequence_id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "FindMatchingRegionsDnaAsyncTaskResponseDnaSequenceMatchesItem({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        matching_dna_sequence_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._matching_dna_sequence_ids, Unset):
            matching_dna_sequence_ids = self._matching_dna_sequence_ids

        target_dna_sequence_id = self._target_dna_sequence_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if matching_dna_sequence_ids is not UNSET:
            field_dict["matchingDnaSequenceIds"] = matching_dna_sequence_ids
        if target_dna_sequence_id is not UNSET:
            field_dict["targetDnaSequenceId"] = target_dna_sequence_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_matching_dna_sequence_ids() -> Union[Unset, List[str]]:
            matching_dna_sequence_ids = cast(List[str], d.pop("matchingDnaSequenceIds"))

            return matching_dna_sequence_ids

        try:
            matching_dna_sequence_ids = get_matching_dna_sequence_ids()
        except KeyError:
            if strict:
                raise
            matching_dna_sequence_ids = cast(Union[Unset, List[str]], UNSET)

        def get_target_dna_sequence_id() -> Union[Unset, str]:
            target_dna_sequence_id = d.pop("targetDnaSequenceId")
            return target_dna_sequence_id

        try:
            target_dna_sequence_id = get_target_dna_sequence_id()
        except KeyError:
            if strict:
                raise
            target_dna_sequence_id = cast(Union[Unset, str], UNSET)

        find_matching_regions_dna_async_task_response_dna_sequence_matches_item = cls(
            matching_dna_sequence_ids=matching_dna_sequence_ids,
            target_dna_sequence_id=target_dna_sequence_id,
        )

        find_matching_regions_dna_async_task_response_dna_sequence_matches_item.additional_properties = d
        return find_matching_regions_dna_async_task_response_dna_sequence_matches_item

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
    def matching_dna_sequence_ids(self) -> List[str]:
        if isinstance(self._matching_dna_sequence_ids, Unset):
            raise NotPresentError(self, "matching_dna_sequence_ids")
        return self._matching_dna_sequence_ids

    @matching_dna_sequence_ids.setter
    def matching_dna_sequence_ids(self, value: List[str]) -> None:
        self._matching_dna_sequence_ids = value

    @matching_dna_sequence_ids.deleter
    def matching_dna_sequence_ids(self) -> None:
        self._matching_dna_sequence_ids = UNSET

    @property
    def target_dna_sequence_id(self) -> str:
        if isinstance(self._target_dna_sequence_id, Unset):
            raise NotPresentError(self, "target_dna_sequence_id")
        return self._target_dna_sequence_id

    @target_dna_sequence_id.setter
    def target_dna_sequence_id(self, value: str) -> None:
        self._target_dna_sequence_id = value

    @target_dna_sequence_id.deleter
    def target_dna_sequence_id(self) -> None:
        self._target_dna_sequence_id = UNSET
