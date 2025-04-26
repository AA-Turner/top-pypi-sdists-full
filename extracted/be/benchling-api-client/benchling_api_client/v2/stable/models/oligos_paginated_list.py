from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.dna_oligo import DnaOligo
from ..models.rna_oligo import RnaOligo
from ..types import UNSET, Unset

T = TypeVar("T", bound="OligosPaginatedList")


@attr.s(auto_attribs=True, repr=False)
class OligosPaginatedList:
    """  """

    _oligos: Union[Unset, List[Union[DnaOligo, RnaOligo, UnknownType]]] = UNSET
    _next_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("oligos={}".format(repr(self._oligos)))
        fields.append("next_token={}".format(repr(self._next_token)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "OligosPaginatedList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        oligos: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._oligos, Unset):
            oligos = []
            for oligos_item_data in self._oligos:
                oligos_item = oligos_item_data.to_dict()

                oligos.append(oligos_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if oligos is not UNSET:
            field_dict["oligos"] = oligos
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_oligos() -> Union[Unset, List[Union[DnaOligo, RnaOligo, UnknownType]]]:
            oligos = []
            _oligos = d.pop("oligos")
            for oligos_item_data in _oligos or []:
                oligos_item: Union[DnaOligo, RnaOligo, UnknownType]
                _oligos_item = oligos_item_data

                if True:
                    discriminator = _oligos_item["nucleotideType"]
                    if discriminator == "DNA":
                        oligos_item = DnaOligo.from_dict(_oligos_item)
                    elif discriminator == "RNA":
                        oligos_item = RnaOligo.from_dict(_oligos_item)
                    else:
                        oligos_item = UnknownType(value=_oligos_item)

                oligos.append(oligos_item)

            return oligos

        try:
            oligos = get_oligos()
        except KeyError:
            if strict:
                raise
            oligos = cast(Union[Unset, List[Union[DnaOligo, RnaOligo, UnknownType]]], UNSET)

        def get_next_token() -> Union[Unset, str]:
            next_token = d.pop("nextToken")
            return next_token

        try:
            next_token = get_next_token()
        except KeyError:
            if strict:
                raise
            next_token = cast(Union[Unset, str], UNSET)

        oligos_paginated_list = cls(
            oligos=oligos,
            next_token=next_token,
        )

        oligos_paginated_list.additional_properties = d
        return oligos_paginated_list

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
    def oligos(self) -> List[Union[DnaOligo, RnaOligo, UnknownType]]:
        if isinstance(self._oligos, Unset):
            raise NotPresentError(self, "oligos")
        return self._oligos

    @oligos.setter
    def oligos(self, value: List[Union[DnaOligo, RnaOligo, UnknownType]]) -> None:
        self._oligos = value

    @oligos.deleter
    def oligos(self) -> None:
        self._oligos = UNSET

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
