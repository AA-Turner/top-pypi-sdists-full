from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.app_canvases_archive_reason import AppCanvasesArchiveReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppCanvasBaseArchiveRecord")


@attr.s(auto_attribs=True, repr=False)
class AppCanvasBaseArchiveRecord:
    """  """

    _reason: Union[Unset, AppCanvasesArchiveReason] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("reason={}".format(repr(self._reason)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AppCanvasBaseArchiveRecord({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        reason: Union[Unset, int] = UNSET
        if not isinstance(self._reason, Unset):
            reason = self._reason.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_reason() -> Union[Unset, AppCanvasesArchiveReason]:
            reason = UNSET
            _reason = d.pop("reason")
            if _reason is not None and _reason is not UNSET:
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
            reason = cast(Union[Unset, AppCanvasesArchiveReason], UNSET)

        app_canvas_base_archive_record = cls(
            reason=reason,
        )

        app_canvas_base_archive_record.additional_properties = d
        return app_canvas_base_archive_record

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
    def reason(self) -> AppCanvasesArchiveReason:
        """ Reason that canvases are being archived. Actual reason enum varies by tenant. """
        if isinstance(self._reason, Unset):
            raise NotPresentError(self, "reason")
        return self._reason

    @reason.setter
    def reason(self, value: AppCanvasesArchiveReason) -> None:
        self._reason = value

    @reason.deleter
    def reason(self) -> None:
        self._reason = UNSET
