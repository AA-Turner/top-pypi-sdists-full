from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.entity_archive_reason import EntityArchiveReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="OligosArchive")


@attr.s(auto_attribs=True, repr=False)
class OligosArchive:
    """The request body for archiving Oligos."""

    _oligo_ids: List[str]
    _reason: EntityArchiveReason

    def __repr__(self):
        fields = []
        fields.append("oligo_ids={}".format(repr(self._oligo_ids)))
        fields.append("reason={}".format(repr(self._reason)))
        return "OligosArchive({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        oligo_ids = self._oligo_ids

        reason = self._reason.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if oligo_ids is not UNSET:
            field_dict["oligoIds"] = oligo_ids
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_oligo_ids() -> List[str]:
            oligo_ids = cast(List[str], d.pop("oligoIds"))

            return oligo_ids

        try:
            oligo_ids = get_oligo_ids()
        except KeyError:
            if strict:
                raise
            oligo_ids = cast(List[str], UNSET)

        def get_reason() -> EntityArchiveReason:
            _reason = d.pop("reason")
            try:
                reason = EntityArchiveReason(_reason)
            except ValueError:
                reason = EntityArchiveReason.of_unknown(_reason)

            return reason

        try:
            reason = get_reason()
        except KeyError:
            if strict:
                raise
            reason = cast(EntityArchiveReason, UNSET)

        oligos_archive = cls(
            oligo_ids=oligo_ids,
            reason=reason,
        )

        return oligos_archive

    @property
    def oligo_ids(self) -> List[str]:
        if isinstance(self._oligo_ids, Unset):
            raise NotPresentError(self, "oligo_ids")
        return self._oligo_ids

    @oligo_ids.setter
    def oligo_ids(self, value: List[str]) -> None:
        self._oligo_ids = value

    @property
    def reason(self) -> EntityArchiveReason:
        """The reason for archiving the provided entities. Accepted reasons may differ based on tenant configuration."""
        if isinstance(self._reason, Unset):
            raise NotPresentError(self, "reason")
        return self._reason

    @reason.setter
    def reason(self, value: EntityArchiveReason) -> None:
        self._reason = value
