from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppCanvasesArchivalChange")


@attr.s(auto_attribs=True, repr=False)
class AppCanvasesArchivalChange:
    """IDs of all items that were archived or unarchived. This includes the IDs of canvases that were archived / unarchived."""

    _canvas_ids: Union[Unset, List[str]] = UNSET

    def __repr__(self):
        fields = []
        fields.append("canvas_ids={}".format(repr(self._canvas_ids)))
        return "AppCanvasesArchivalChange({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        canvas_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._canvas_ids, Unset):
            canvas_ids = self._canvas_ids

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if canvas_ids is not UNSET:
            field_dict["canvasIds"] = canvas_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_canvas_ids() -> Union[Unset, List[str]]:
            canvas_ids = cast(List[str], d.pop("canvasIds"))

            return canvas_ids

        try:
            canvas_ids = get_canvas_ids()
        except KeyError:
            if strict:
                raise
            canvas_ids = cast(Union[Unset, List[str]], UNSET)

        app_canvases_archival_change = cls(
            canvas_ids=canvas_ids,
        )

        return app_canvases_archival_change

    @property
    def canvas_ids(self) -> List[str]:
        if isinstance(self._canvas_ids, Unset):
            raise NotPresentError(self, "canvas_ids")
        return self._canvas_ids

    @canvas_ids.setter
    def canvas_ids(self, value: List[str]) -> None:
        self._canvas_ids = value

    @canvas_ids.deleter
    def canvas_ids(self) -> None:
        self._canvas_ids = UNSET
