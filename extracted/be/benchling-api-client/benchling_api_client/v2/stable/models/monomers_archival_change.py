from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="MonomersArchivalChange")


@attr.s(auto_attribs=True, repr=False)
class MonomersArchivalChange:
    """IDs of all items that were archived or unarchived, grouped by resource type."""

    _batch_ids: Union[Unset, List[str]] = UNSET
    _monomer_ids: Union[Unset, List[str]] = UNSET

    def __repr__(self):
        fields = []
        fields.append("batch_ids={}".format(repr(self._batch_ids)))
        fields.append("monomer_ids={}".format(repr(self._monomer_ids)))
        return "MonomersArchivalChange({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        batch_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._batch_ids, Unset):
            batch_ids = self._batch_ids

        monomer_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._monomer_ids, Unset):
            monomer_ids = self._monomer_ids

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if batch_ids is not UNSET:
            field_dict["batchIds"] = batch_ids
        if monomer_ids is not UNSET:
            field_dict["monomerIds"] = monomer_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_batch_ids() -> Union[Unset, List[str]]:
            batch_ids = cast(List[str], d.pop("batchIds"))

            return batch_ids

        try:
            batch_ids = get_batch_ids()
        except KeyError:
            if strict:
                raise
            batch_ids = cast(Union[Unset, List[str]], UNSET)

        def get_monomer_ids() -> Union[Unset, List[str]]:
            monomer_ids = cast(List[str], d.pop("monomerIds"))

            return monomer_ids

        try:
            monomer_ids = get_monomer_ids()
        except KeyError:
            if strict:
                raise
            monomer_ids = cast(Union[Unset, List[str]], UNSET)

        monomers_archival_change = cls(
            batch_ids=batch_ids,
            monomer_ids=monomer_ids,
        )

        return monomers_archival_change

    @property
    def batch_ids(self) -> List[str]:
        if isinstance(self._batch_ids, Unset):
            raise NotPresentError(self, "batch_ids")
        return self._batch_ids

    @batch_ids.setter
    def batch_ids(self, value: List[str]) -> None:
        self._batch_ids = value

    @batch_ids.deleter
    def batch_ids(self) -> None:
        self._batch_ids = UNSET

    @property
    def monomer_ids(self) -> List[str]:
        if isinstance(self._monomer_ids, Unset):
            raise NotPresentError(self, "monomer_ids")
        return self._monomer_ids

    @monomer_ids.setter
    def monomer_ids(self, value: List[str]) -> None:
        self._monomer_ids = value

    @monomer_ids.deleter
    def monomer_ids(self) -> None:
        self._monomer_ids = UNSET
