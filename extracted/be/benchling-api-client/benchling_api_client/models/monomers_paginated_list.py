from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.monomer import Monomer
from ..types import UNSET, Unset

T = TypeVar("T", bound="MonomersPaginatedList")


@attr.s(auto_attribs=True, repr=False)
class MonomersPaginatedList:
    """  """

    _monomers: Union[Unset, List[Monomer]] = UNSET
    _next_token: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("monomers={}".format(repr(self._monomers)))
        fields.append("next_token={}".format(repr(self._next_token)))
        return "MonomersPaginatedList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        monomers: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._monomers, Unset):
            monomers = []
            for monomers_item_data in self._monomers:
                monomers_item = monomers_item_data.to_dict()

                monomers.append(monomers_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if monomers is not UNSET:
            field_dict["monomers"] = monomers
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_monomers() -> Union[Unset, List[Monomer]]:
            monomers = []
            _monomers = d.pop("monomers")
            for monomers_item_data in _monomers or []:
                monomers_item = Monomer.from_dict(monomers_item_data, strict=False)

                monomers.append(monomers_item)

            return monomers

        try:
            monomers = get_monomers()
        except KeyError:
            if strict:
                raise
            monomers = cast(Union[Unset, List[Monomer]], UNSET)

        def get_next_token() -> Union[Unset, str]:
            next_token = d.pop("nextToken")
            return next_token

        try:
            next_token = get_next_token()
        except KeyError:
            if strict:
                raise
            next_token = cast(Union[Unset, str], UNSET)

        monomers_paginated_list = cls(
            monomers=monomers,
            next_token=next_token,
        )

        return monomers_paginated_list

    @property
    def monomers(self) -> List[Monomer]:
        if isinstance(self._monomers, Unset):
            raise NotPresentError(self, "monomers")
        return self._monomers

    @monomers.setter
    def monomers(self, value: List[Monomer]) -> None:
        self._monomers = value

    @monomers.deleter
    def monomers(self) -> None:
        self._monomers = UNSET

    @property
    def next_token(self) -> str:
        if isinstance(self._next_token, Unset):
            raise NotPresentError(self, "next_token")
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @next_token.deleter
    def next_token(self) -> None:
        self._next_token = UNSET
