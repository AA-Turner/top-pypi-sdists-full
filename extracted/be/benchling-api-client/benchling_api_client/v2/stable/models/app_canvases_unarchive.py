from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppCanvasesUnarchive")


@attr.s(auto_attribs=True, repr=False)
class AppCanvasesUnarchive:
    """  """

    _canvas_ids: List[str]

    def __repr__(self):
        fields = []
        fields.append("canvas_ids={}".format(repr(self._canvas_ids)))
        return "AppCanvasesUnarchive({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        canvas_ids = self._canvas_ids

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if canvas_ids is not UNSET:
            field_dict["canvasIds"] = canvas_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_canvas_ids() -> List[str]:
            canvas_ids = cast(List[str], d.pop("canvasIds"))

            return canvas_ids

        try:
            canvas_ids = get_canvas_ids()
        except KeyError:
            if strict:
                raise
            canvas_ids = cast(List[str], UNSET)

        app_canvases_unarchive = cls(
            canvas_ids=canvas_ids,
        )

        return app_canvases_unarchive

    @property
    def canvas_ids(self) -> List[str]:
        """ Array of canvas IDs """
        if isinstance(self._canvas_ids, Unset):
            raise NotPresentError(self, "canvas_ids")
        return self._canvas_ids

    @canvas_ids.setter
    def canvas_ids(self, value: List[str]) -> None:
        self._canvas_ids = value
