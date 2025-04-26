from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.monomers_archive_reason import MonomersArchiveReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="MonomersArchive")


@attr.s(auto_attribs=True, repr=False)
class MonomersArchive:
    """The request body for archiving Monomers."""

    _monomer_ids: List[str]
    _reason: MonomersArchiveReason

    def __repr__(self):
        fields = []
        fields.append("monomer_ids={}".format(repr(self._monomer_ids)))
        fields.append("reason={}".format(repr(self._reason)))
        return "MonomersArchive({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        monomer_ids = self._monomer_ids

        reason = self._reason.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if monomer_ids is not UNSET:
            field_dict["monomerIds"] = monomer_ids
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_monomer_ids() -> List[str]:
            monomer_ids = cast(List[str], d.pop("monomerIds"))

            return monomer_ids

        try:
            monomer_ids = get_monomer_ids()
        except KeyError:
            if strict:
                raise
            monomer_ids = cast(List[str], UNSET)

        def get_reason() -> MonomersArchiveReason:
            _reason = d.pop("reason")
            try:
                reason = MonomersArchiveReason(_reason)
            except ValueError:
                reason = MonomersArchiveReason.of_unknown(_reason)

            return reason

        try:
            reason = get_reason()
        except KeyError:
            if strict:
                raise
            reason = cast(MonomersArchiveReason, UNSET)

        monomers_archive = cls(
            monomer_ids=monomer_ids,
            reason=reason,
        )

        return monomers_archive

    @property
    def monomer_ids(self) -> List[str]:
        if isinstance(self._monomer_ids, Unset):
            raise NotPresentError(self, "monomer_ids")
        return self._monomer_ids

    @monomer_ids.setter
    def monomer_ids(self, value: List[str]) -> None:
        self._monomer_ids = value

    @property
    def reason(self) -> MonomersArchiveReason:
        """The reason for archiving the provided Monomers. Accepted reasons may differ based on tenant configuration."""
        if isinstance(self._reason, Unset):
            raise NotPresentError(self, "reason")
        return self._reason

    @reason.setter
    def reason(self, value: MonomersArchiveReason) -> None:
        self._reason = value
