from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.plates_archive_reason import PlatesArchiveReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="PlatesArchive")


@attr.s(auto_attribs=True, repr=False)
class PlatesArchive:
    """  """

    _plate_ids: List[str]
    _reason: PlatesArchiveReason
    _should_remove_barcodes: bool

    def __repr__(self):
        fields = []
        fields.append("plate_ids={}".format(repr(self._plate_ids)))
        fields.append("reason={}".format(repr(self._reason)))
        fields.append("should_remove_barcodes={}".format(repr(self._should_remove_barcodes)))
        return "PlatesArchive({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        plate_ids = self._plate_ids

        reason = self._reason.value

        should_remove_barcodes = self._should_remove_barcodes

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if plate_ids is not UNSET:
            field_dict["plateIds"] = plate_ids
        if reason is not UNSET:
            field_dict["reason"] = reason
        if should_remove_barcodes is not UNSET:
            field_dict["shouldRemoveBarcodes"] = should_remove_barcodes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_plate_ids() -> List[str]:
            plate_ids = cast(List[str], d.pop("plateIds"))

            return plate_ids

        try:
            plate_ids = get_plate_ids()
        except KeyError:
            if strict:
                raise
            plate_ids = cast(List[str], UNSET)

        def get_reason() -> PlatesArchiveReason:
            _reason = d.pop("reason")
            try:
                reason = PlatesArchiveReason(_reason)
            except ValueError:
                reason = PlatesArchiveReason.of_unknown(_reason)

            return reason

        try:
            reason = get_reason()
        except KeyError:
            if strict:
                raise
            reason = cast(PlatesArchiveReason, UNSET)

        def get_should_remove_barcodes() -> bool:
            should_remove_barcodes = d.pop("shouldRemoveBarcodes")
            return should_remove_barcodes

        try:
            should_remove_barcodes = get_should_remove_barcodes()
        except KeyError:
            if strict:
                raise
            should_remove_barcodes = cast(bool, UNSET)

        plates_archive = cls(
            plate_ids=plate_ids,
            reason=reason,
            should_remove_barcodes=should_remove_barcodes,
        )

        return plates_archive

    @property
    def plate_ids(self) -> List[str]:
        """ Array of plate IDs """
        if isinstance(self._plate_ids, Unset):
            raise NotPresentError(self, "plate_ids")
        return self._plate_ids

    @plate_ids.setter
    def plate_ids(self, value: List[str]) -> None:
        self._plate_ids = value

    @property
    def reason(self) -> PlatesArchiveReason:
        """Reason that plates are being archived."""
        if isinstance(self._reason, Unset):
            raise NotPresentError(self, "reason")
        return self._reason

    @reason.setter
    def reason(self, value: PlatesArchiveReason) -> None:
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
