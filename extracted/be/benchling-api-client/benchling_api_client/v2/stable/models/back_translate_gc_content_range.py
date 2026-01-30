from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="BackTranslateGcContentRange")


@attr.s(auto_attribs=True, repr=False)
class BackTranslateGcContentRange:
    """Custom GC content range for the optimized sequence, specified as decimal values between 0 and 1. The maximum must be greater than the minimum. Cannot be specified together with gcContent."""

    _max: Union[Unset, float] = UNSET
    _min: Union[Unset, float] = UNSET

    def __repr__(self):
        fields = []
        fields.append("max={}".format(repr(self._max)))
        fields.append("min={}".format(repr(self._min)))
        return "BackTranslateGcContentRange({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        max = self._max
        min = self._min

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if max is not UNSET:
            field_dict["max"] = max
        if min is not UNSET:
            field_dict["min"] = min

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_max() -> Union[Unset, float]:
            max = d.pop("max")
            return max

        try:
            max = get_max()
        except KeyError:
            if strict:
                raise
            max = cast(Union[Unset, float], UNSET)

        def get_min() -> Union[Unset, float]:
            min = d.pop("min")
            return min

        try:
            min = get_min()
        except KeyError:
            if strict:
                raise
            min = cast(Union[Unset, float], UNSET)

        back_translate_gc_content_range = cls(
            max=max,
            min=min,
        )

        return back_translate_gc_content_range

    @property
    def max(self) -> float:
        """ Maximum GC content ratio (e.g., 0.6 for 60%) """
        if isinstance(self._max, Unset):
            raise NotPresentError(self, "max")
        return self._max

    @max.setter
    def max(self, value: float) -> None:
        self._max = value

    @max.deleter
    def max(self) -> None:
        self._max = UNSET

    @property
    def min(self) -> float:
        """ Minimum GC content ratio (e.g., 0.4 for 40%) """
        if isinstance(self._min, Unset):
            raise NotPresentError(self, "min")
        return self._min

    @min.setter
    def min(self, value: float) -> None:
        self._min = value

    @min.deleter
    def min(self) -> None:
        self._min = UNSET
