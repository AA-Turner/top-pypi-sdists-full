from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.boxes_archive_reason import BoxesArchiveReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="BoxesArchive")


@attr.s(auto_attribs=True, repr=False)
class BoxesArchive:
    """  """

    _box_ids: List[str]
    _reason: BoxesArchiveReason
    _should_remove_barcodes: Union[Unset, bool] = UNSET

    def __repr__(self):
        fields = []
        fields.append("box_ids={}".format(repr(self._box_ids)))
        fields.append("reason={}".format(repr(self._reason)))
        fields.append("should_remove_barcodes={}".format(repr(self._should_remove_barcodes)))
        return "BoxesArchive({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        box_ids = self._box_ids

        reason = self._reason.value

        should_remove_barcodes = self._should_remove_barcodes

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if box_ids is not UNSET:
            field_dict["boxIds"] = box_ids
        if reason is not UNSET:
            field_dict["reason"] = reason
        if should_remove_barcodes is not UNSET:
            field_dict["shouldRemoveBarcodes"] = should_remove_barcodes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_box_ids() -> List[str]:
            box_ids = cast(List[str], d.pop("boxIds"))

            return box_ids

        try:
            box_ids = get_box_ids()
        except KeyError:
            if strict:
                raise
            box_ids = cast(List[str], UNSET)

        def get_reason() -> BoxesArchiveReason:
            _reason = d.pop("reason")
            try:
                reason = BoxesArchiveReason(_reason)
            except ValueError:
                reason = BoxesArchiveReason.of_unknown(_reason)

            return reason

        try:
            reason = get_reason()
        except KeyError:
            if strict:
                raise
            reason = cast(BoxesArchiveReason, UNSET)

        def get_should_remove_barcodes() -> Union[Unset, bool]:
            should_remove_barcodes = d.pop("shouldRemoveBarcodes")
            return should_remove_barcodes

        try:
            should_remove_barcodes = get_should_remove_barcodes()
        except KeyError:
            if strict:
                raise
            should_remove_barcodes = cast(Union[Unset, bool], UNSET)

        boxes_archive = cls(
            box_ids=box_ids,
            reason=reason,
            should_remove_barcodes=should_remove_barcodes,
        )

        return boxes_archive

    @property
    def box_ids(self) -> List[str]:
        """ Array of box IDs """
        if isinstance(self._box_ids, Unset):
            raise NotPresentError(self, "box_ids")
        return self._box_ids

    @box_ids.setter
    def box_ids(self, value: List[str]) -> None:
        self._box_ids = value

    @property
    def reason(self) -> BoxesArchiveReason:
        """Reason that boxes are being archived."""
        if isinstance(self._reason, Unset):
            raise NotPresentError(self, "reason")
        return self._reason

    @reason.setter
    def reason(self, value: BoxesArchiveReason) -> None:
        self._reason = value

    @property
    def should_remove_barcodes(self) -> bool:
        """Remove barcodes. Removing barcodes from archived inventory that contain items will also remove barcodes from the contained items."""
        if isinstance(self._should_remove_barcodes, Unset):
            raise NotPresentError(self, "should_remove_barcodes")
        return self._should_remove_barcodes

    @should_remove_barcodes.setter
    def should_remove_barcodes(self, value: bool) -> None:
        self._should_remove_barcodes = value

    @should_remove_barcodes.deleter
    def should_remove_barcodes(self) -> None:
        self._should_remove_barcodes = UNSET
