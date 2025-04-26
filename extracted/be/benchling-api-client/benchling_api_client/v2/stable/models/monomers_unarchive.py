from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="MonomersUnarchive")


@attr.s(auto_attribs=True, repr=False)
class MonomersUnarchive:
    """The request body for unarchiving Monomers."""

    _monomer_ids: List[str]

    def __repr__(self):
        fields = []
        fields.append("monomer_ids={}".format(repr(self._monomer_ids)))
        return "MonomersUnarchive({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        monomer_ids = self._monomer_ids

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if monomer_ids is not UNSET:
            field_dict["monomerIds"] = monomer_ids

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

        monomers_unarchive = cls(
            monomer_ids=monomer_ids,
        )

        return monomers_unarchive

    @property
    def monomer_ids(self) -> List[str]:
        if isinstance(self._monomer_ids, Unset):
            raise NotPresentError(self, "monomer_ids")
        return self._monomer_ids

    @monomer_ids.setter
    def monomer_ids(self, value: List[str]) -> None:
        self._monomer_ids = value
