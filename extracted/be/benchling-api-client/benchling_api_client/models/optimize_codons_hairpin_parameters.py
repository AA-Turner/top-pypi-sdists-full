from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="OptimizeCodonsHairpinParameters")


@attr.s(auto_attribs=True, repr=False)
class OptimizeCodonsHairpinParameters:
    """These parameters are applied in the AvoidHairpins specification in DNAChisel. If hairpinParameters is not specified, hairpins will not be avoided."""

    _stem: Union[Unset, int] = 20
    _window: Union[Unset, int] = 200

    def __repr__(self):
        fields = []
        fields.append("stem={}".format(repr(self._stem)))
        fields.append("window={}".format(repr(self._window)))
        return "OptimizeCodonsHairpinParameters({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        stem = self._stem
        window = self._window

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if stem is not UNSET:
            field_dict["stem"] = stem
        if window is not UNSET:
            field_dict["window"] = window

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_stem() -> Union[Unset, int]:
            stem = d.pop("stem")
            return stem

        try:
            stem = get_stem()
        except KeyError:
            if strict:
                raise
            stem = cast(Union[Unset, int], UNSET)

        def get_window() -> Union[Unset, int]:
            window = d.pop("window")
            return window

        try:
            window = get_window()
        except KeyError:
            if strict:
                raise
            window = cast(Union[Unset, int], UNSET)

        optimize_codons_hairpin_parameters = cls(
            stem=stem,
            window=window,
        )

        return optimize_codons_hairpin_parameters

    @property
    def stem(self) -> int:
        if isinstance(self._stem, Unset):
            raise NotPresentError(self, "stem")
        return self._stem

    @stem.setter
    def stem(self, value: int) -> None:
        self._stem = value

    @stem.deleter
    def stem(self) -> None:
        self._stem = UNSET

    @property
    def window(self) -> int:
        if isinstance(self._window, Unset):
            raise NotPresentError(self, "window")
        return self._window

    @window.setter
    def window(self, value: int) -> None:
        self._window = value

    @window.deleter
    def window(self) -> None:
        self._window = UNSET
