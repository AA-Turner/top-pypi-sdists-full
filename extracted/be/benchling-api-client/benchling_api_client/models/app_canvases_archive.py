from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.app_canvases_archive_reason import AppCanvasesArchiveReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppCanvasesArchive")


@attr.s(auto_attribs=True, repr=False)
class AppCanvasesArchive:
    """  """

    _canvas_ids: List[str]
    _reason: AppCanvasesArchiveReason

    def __repr__(self):
        fields = []
        fields.append("canvas_ids={}".format(repr(self._canvas_ids)))
        fields.append("reason={}".format(repr(self._reason)))
        return "AppCanvasesArchive({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        canvas_ids = self._canvas_ids

        reason = self._reason.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if canvas_ids is not UNSET:
            field_dict["canvasIds"] = canvas_ids
        if reason is not UNSET:
            field_dict["reason"] = reason

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

        def get_reason() -> AppCanvasesArchiveReason:
            _reason = d.pop("reason")
            try:
                reason = AppCanvasesArchiveReason(_reason)
            except ValueError:
                reason = AppCanvasesArchiveReason.of_unknown(_reason)

            return reason

        try:
            reason = get_reason()
        except KeyError:
            if strict:
                raise
            reason = cast(AppCanvasesArchiveReason, UNSET)

        app_canvases_archive = cls(
            canvas_ids=canvas_ids,
            reason=reason,
        )

        return app_canvases_archive

    @property
    def canvas_ids(self) -> List[str]:
        """ Array of canvas IDs """
        if isinstance(self._canvas_ids, Unset):
            raise NotPresentError(self, "canvas_ids")
        return self._canvas_ids

    @canvas_ids.setter
    def canvas_ids(self, value: List[str]) -> None:
        self._canvas_ids = value

    @property
    def reason(self) -> AppCanvasesArchiveReason:
        """ Reason that canvases are being archived. Actual reason enum varies by tenant. """
        if isinstance(self._reason, Unset):
            raise NotPresentError(self, "reason")
        return self._reason

    @reason.setter
    def reason(self, value: AppCanvasesArchiveReason) -> None:
        self._reason = value
