from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.molecules_archive_reason import MoleculesArchiveReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="MoleculesArchive")


@attr.s(auto_attribs=True, repr=False)
class MoleculesArchive:
    """The request body for archiving Molecules."""

    _molecule_ids: List[str]
    _reason: MoleculesArchiveReason

    def __repr__(self):
        fields = []
        fields.append("molecule_ids={}".format(repr(self._molecule_ids)))
        fields.append("reason={}".format(repr(self._reason)))
        return "MoleculesArchive({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        molecule_ids = self._molecule_ids

        reason = self._reason.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if molecule_ids is not UNSET:
            field_dict["moleculeIds"] = molecule_ids
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_molecule_ids() -> List[str]:
            molecule_ids = cast(List[str], d.pop("moleculeIds"))

            return molecule_ids

        try:
            molecule_ids = get_molecule_ids()
        except KeyError:
            if strict:
                raise
            molecule_ids = cast(List[str], UNSET)

        def get_reason() -> MoleculesArchiveReason:
            _reason = d.pop("reason")
            try:
                reason = MoleculesArchiveReason(_reason)
            except ValueError:
                reason = MoleculesArchiveReason.of_unknown(_reason)

            return reason

        try:
            reason = get_reason()
        except KeyError:
            if strict:
                raise
            reason = cast(MoleculesArchiveReason, UNSET)

        molecules_archive = cls(
            molecule_ids=molecule_ids,
            reason=reason,
        )

        return molecules_archive

    @property
    def molecule_ids(self) -> List[str]:
        if isinstance(self._molecule_ids, Unset):
            raise NotPresentError(self, "molecule_ids")
        return self._molecule_ids

    @molecule_ids.setter
    def molecule_ids(self, value: List[str]) -> None:
        self._molecule_ids = value

    @property
    def reason(self) -> MoleculesArchiveReason:
        """The reason for archiving the provided Molecules. Accepted reasons may differ based on tenant configuration."""
        if isinstance(self._reason, Unset):
            raise NotPresentError(self, "reason")
        return self._reason

    @reason.setter
    def reason(self, value: MoleculesArchiveReason) -> None:
        self._reason = value
