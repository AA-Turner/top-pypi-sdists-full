from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomNotationPrefilterTerminals")


@attr.s(auto_attribs=True, repr=False)
class CustomNotationPrefilterTerminals:
    """ Configuration for an optional feature where unrecognized tokens at the 5'/3' terminal ends of an input sequence can be stripped and output to schema fields. """

    _five_prime_left_delimiter: Union[Unset, None, str] = UNSET
    _five_prime_right_delimiter: Union[Unset, str] = UNSET
    _max_depth: Union[Unset, None, int] = UNSET
    _three_prime_left_delimiter: Union[Unset, str] = UNSET
    _three_prime_right_delimiter: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("five_prime_left_delimiter={}".format(repr(self._five_prime_left_delimiter)))
        fields.append("five_prime_right_delimiter={}".format(repr(self._five_prime_right_delimiter)))
        fields.append("max_depth={}".format(repr(self._max_depth)))
        fields.append("three_prime_left_delimiter={}".format(repr(self._three_prime_left_delimiter)))
        fields.append("three_prime_right_delimiter={}".format(repr(self._three_prime_right_delimiter)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "CustomNotationPrefilterTerminals({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        five_prime_left_delimiter = self._five_prime_left_delimiter
        five_prime_right_delimiter = self._five_prime_right_delimiter
        max_depth = self._max_depth
        three_prime_left_delimiter = self._three_prime_left_delimiter
        three_prime_right_delimiter = self._three_prime_right_delimiter

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if five_prime_left_delimiter is not UNSET:
            field_dict["fivePrimeLeftDelimiter"] = five_prime_left_delimiter
        if five_prime_right_delimiter is not UNSET:
            field_dict["fivePrimeRightDelimiter"] = five_prime_right_delimiter
        if max_depth is not UNSET:
            field_dict["maxDepth"] = max_depth
        if three_prime_left_delimiter is not UNSET:
            field_dict["threePrimeLeftDelimiter"] = three_prime_left_delimiter
        if three_prime_right_delimiter is not UNSET:
            field_dict["threePrimeRightDelimiter"] = three_prime_right_delimiter

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_five_prime_left_delimiter() -> Union[Unset, None, str]:
            five_prime_left_delimiter = d.pop("fivePrimeLeftDelimiter")
            return five_prime_left_delimiter

        try:
            five_prime_left_delimiter = get_five_prime_left_delimiter()
        except KeyError:
            if strict:
                raise
            five_prime_left_delimiter = cast(Union[Unset, None, str], UNSET)

        def get_five_prime_right_delimiter() -> Union[Unset, str]:
            five_prime_right_delimiter = d.pop("fivePrimeRightDelimiter")
            return five_prime_right_delimiter

        try:
            five_prime_right_delimiter = get_five_prime_right_delimiter()
        except KeyError:
            if strict:
                raise
            five_prime_right_delimiter = cast(Union[Unset, str], UNSET)

        def get_max_depth() -> Union[Unset, None, int]:
            max_depth = d.pop("maxDepth")
            return max_depth

        try:
            max_depth = get_max_depth()
        except KeyError:
            if strict:
                raise
            max_depth = cast(Union[Unset, None, int], UNSET)

        def get_three_prime_left_delimiter() -> Union[Unset, str]:
            three_prime_left_delimiter = d.pop("threePrimeLeftDelimiter")
            return three_prime_left_delimiter

        try:
            three_prime_left_delimiter = get_three_prime_left_delimiter()
        except KeyError:
            if strict:
                raise
            three_prime_left_delimiter = cast(Union[Unset, str], UNSET)

        def get_three_prime_right_delimiter() -> Union[Unset, None, str]:
            three_prime_right_delimiter = d.pop("threePrimeRightDelimiter")
            return three_prime_right_delimiter

        try:
            three_prime_right_delimiter = get_three_prime_right_delimiter()
        except KeyError:
            if strict:
                raise
            three_prime_right_delimiter = cast(Union[Unset, None, str], UNSET)

        custom_notation_prefilter_terminals = cls(
            five_prime_left_delimiter=five_prime_left_delimiter,
            five_prime_right_delimiter=five_prime_right_delimiter,
            max_depth=max_depth,
            three_prime_left_delimiter=three_prime_left_delimiter,
            three_prime_right_delimiter=three_prime_right_delimiter,
        )

        custom_notation_prefilter_terminals.additional_properties = d
        return custom_notation_prefilter_terminals

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
    def five_prime_left_delimiter(self) -> Optional[str]:
        if isinstance(self._five_prime_left_delimiter, Unset):
            raise NotPresentError(self, "five_prime_left_delimiter")
        return self._five_prime_left_delimiter

    @five_prime_left_delimiter.setter
    def five_prime_left_delimiter(self, value: Optional[str]) -> None:
        self._five_prime_left_delimiter = value

    @five_prime_left_delimiter.deleter
    def five_prime_left_delimiter(self) -> None:
        self._five_prime_left_delimiter = UNSET

    @property
    def five_prime_right_delimiter(self) -> str:
        if isinstance(self._five_prime_right_delimiter, Unset):
            raise NotPresentError(self, "five_prime_right_delimiter")
        return self._five_prime_right_delimiter

    @five_prime_right_delimiter.setter
    def five_prime_right_delimiter(self, value: str) -> None:
        self._five_prime_right_delimiter = value

    @five_prime_right_delimiter.deleter
    def five_prime_right_delimiter(self) -> None:
        self._five_prime_right_delimiter = UNSET

    @property
    def max_depth(self) -> Optional[int]:
        if isinstance(self._max_depth, Unset):
            raise NotPresentError(self, "max_depth")
        return self._max_depth

    @max_depth.setter
    def max_depth(self, value: Optional[int]) -> None:
        self._max_depth = value

    @max_depth.deleter
    def max_depth(self) -> None:
        self._max_depth = UNSET

    @property
    def three_prime_left_delimiter(self) -> str:
        if isinstance(self._three_prime_left_delimiter, Unset):
            raise NotPresentError(self, "three_prime_left_delimiter")
        return self._three_prime_left_delimiter

    @three_prime_left_delimiter.setter
    def three_prime_left_delimiter(self, value: str) -> None:
        self._three_prime_left_delimiter = value

    @three_prime_left_delimiter.deleter
    def three_prime_left_delimiter(self) -> None:
        self._three_prime_left_delimiter = UNSET

    @property
    def three_prime_right_delimiter(self) -> Optional[str]:
        if isinstance(self._three_prime_right_delimiter, Unset):
            raise NotPresentError(self, "three_prime_right_delimiter")
        return self._three_prime_right_delimiter

    @three_prime_right_delimiter.setter
    def three_prime_right_delimiter(self, value: Optional[str]) -> None:
        self._three_prime_right_delimiter = value

    @three_prime_right_delimiter.deleter
    def three_prime_right_delimiter(self) -> None:
        self._three_prime_right_delimiter = UNSET
