from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.membership import Membership
from ..types import UNSET, Unset

T = TypeVar("T", bound="MembershipsPaginatedList")


@attr.s(auto_attribs=True, repr=False)
class MembershipsPaginatedList:
    """  """

    _memberships: Union[Unset, List[Membership]] = UNSET
    _next_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("memberships={}".format(repr(self._memberships)))
        fields.append("next_token={}".format(repr(self._next_token)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "MembershipsPaginatedList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        memberships: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._memberships, Unset):
            memberships = []
            for memberships_item_data in self._memberships:
                memberships_item = memberships_item_data.to_dict()

                memberships.append(memberships_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if memberships is not UNSET:
            field_dict["memberships"] = memberships
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_memberships() -> Union[Unset, List[Membership]]:
            memberships = []
            _memberships = d.pop("memberships")
            for memberships_item_data in _memberships or []:
                memberships_item = Membership.from_dict(memberships_item_data, strict=False)

                memberships.append(memberships_item)

            return memberships

        try:
            memberships = get_memberships()
        except KeyError:
            if strict:
                raise
            memberships = cast(Union[Unset, List[Membership]], UNSET)

        def get_next_token() -> Union[Unset, str]:
            next_token = d.pop("nextToken")
            return next_token

        try:
            next_token = get_next_token()
        except KeyError:
            if strict:
                raise
            next_token = cast(Union[Unset, str], UNSET)

        memberships_paginated_list = cls(
            memberships=memberships,
            next_token=next_token,
        )

        memberships_paginated_list.additional_properties = d
        return memberships_paginated_list

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
    def memberships(self) -> List[Membership]:
        if isinstance(self._memberships, Unset):
            raise NotPresentError(self, "memberships")
        return self._memberships

    @memberships.setter
    def memberships(self, value: List[Membership]) -> None:
        self._memberships = value

    @memberships.deleter
    def memberships(self) -> None:
        self._memberships = UNSET

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
