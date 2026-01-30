from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="ReducedPattern")


@attr.s(auto_attribs=True, repr=False)
class ReducedPattern:
    """DNA patterns to avoid during optimization. Supports two formats: 1) DNA base patterns: strings of ATGC bases (case-insensitive, e.g., "ATGC" or "gat") 2) Repeat patterns: format "nxkmer" specifying n repeats of k-sized sequences (e.g., "3x4mer" matches 3 consecutive 4-base repeats). Maximum total length for repeat patterns is 50 bases (n * k ≤ 50).
    If avoidReverseComplement is true, the pattern's reverse complement will also be avoided. Note: avoidReverseComplement cannot be true for repeat patterns (nxkmer format).
    """

    _avoid_reverse_complement: Union[Unset, bool] = False
    _pattern: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("avoid_reverse_complement={}".format(repr(self._avoid_reverse_complement)))
        fields.append("pattern={}".format(repr(self._pattern)))
        return "ReducedPattern({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        avoid_reverse_complement = self._avoid_reverse_complement
        pattern = self._pattern

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if avoid_reverse_complement is not UNSET:
            field_dict["avoidReverseComplement"] = avoid_reverse_complement
        if pattern is not UNSET:
            field_dict["pattern"] = pattern

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_avoid_reverse_complement() -> Union[Unset, bool]:
            avoid_reverse_complement = d.pop("avoidReverseComplement")
            return avoid_reverse_complement

        try:
            avoid_reverse_complement = get_avoid_reverse_complement()
        except KeyError:
            if strict:
                raise
            avoid_reverse_complement = cast(Union[Unset, bool], UNSET)

        def get_pattern() -> Union[Unset, str]:
            pattern = d.pop("pattern")
            return pattern

        try:
            pattern = get_pattern()
        except KeyError:
            if strict:
                raise
            pattern = cast(Union[Unset, str], UNSET)

        reduced_pattern = cls(
            avoid_reverse_complement=avoid_reverse_complement,
            pattern=pattern,
        )

        return reduced_pattern

    @property
    def avoid_reverse_complement(self) -> bool:
        if isinstance(self._avoid_reverse_complement, Unset):
            raise NotPresentError(self, "avoid_reverse_complement")
        return self._avoid_reverse_complement

    @avoid_reverse_complement.setter
    def avoid_reverse_complement(self, value: bool) -> None:
        self._avoid_reverse_complement = value

    @avoid_reverse_complement.deleter
    def avoid_reverse_complement(self) -> None:
        self._avoid_reverse_complement = UNSET

    @property
    def pattern(self) -> str:
        if isinstance(self._pattern, Unset):
            raise NotPresentError(self, "pattern")
        return self._pattern

    @pattern.setter
    def pattern(self, value: str) -> None:
        self._pattern = value

    @pattern.deleter
    def pattern(self) -> None:
        self._pattern = UNSET
