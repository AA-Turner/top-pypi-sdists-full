from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.membership_update_role import MembershipUpdateRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="MembershipUpdate")


@attr.s(auto_attribs=True, repr=False)
class MembershipUpdate:
    """  """

    _role: Union[Unset, MembershipUpdateRole] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("role={}".format(repr(self._role)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "MembershipUpdate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        role: Union[Unset, int] = UNSET
        if not isinstance(self._role, Unset):
            role = self._role.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if role is not UNSET:
            field_dict["role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_role() -> Union[Unset, MembershipUpdateRole]:
            role = UNSET
            _role = d.pop("role")
            if _role is not None and _role is not UNSET:
                try:
                    role = MembershipUpdateRole(_role)
                except ValueError:
                    role = MembershipUpdateRole.of_unknown(_role)

            return role

        try:
            role = get_role()
        except KeyError:
            if strict:
                raise
            role = cast(Union[Unset, MembershipUpdateRole], UNSET)

        membership_update = cls(
            role=role,
        )

        membership_update.additional_properties = d
        return membership_update

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
    def role(self) -> MembershipUpdateRole:
        if isinstance(self._role, Unset):
            raise NotPresentError(self, "role")
        return self._role

    @role.setter
    def role(self, value: MembershipUpdateRole) -> None:
        self._role = value

    @role.deleter
    def role(self) -> None:
        self._role = UNSET
