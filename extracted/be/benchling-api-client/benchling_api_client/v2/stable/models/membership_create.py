from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.membership_create_role import MembershipCreateRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="MembershipCreate")


@attr.s(auto_attribs=True, repr=False)
class MembershipCreate:
    """  """

    _role: Union[Unset, MembershipCreateRole] = UNSET
    _user_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("role={}".format(repr(self._role)))
        fields.append("user_id={}".format(repr(self._user_id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "MembershipCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        role: Union[Unset, int] = UNSET
        if not isinstance(self._role, Unset):
            role = self._role.value

        user_id = self._user_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if role is not UNSET:
            field_dict["role"] = role
        if user_id is not UNSET:
            field_dict["userId"] = user_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_role() -> Union[Unset, MembershipCreateRole]:
            role = UNSET
            _role = d.pop("role")
            if _role is not None and _role is not UNSET:
                try:
                    role = MembershipCreateRole(_role)
                except ValueError:
                    role = MembershipCreateRole.of_unknown(_role)

            return role

        try:
            role = get_role()
        except KeyError:
            if strict:
                raise
            role = cast(Union[Unset, MembershipCreateRole], UNSET)

        def get_user_id() -> Union[Unset, str]:
            user_id = d.pop("userId")
            return user_id

        try:
            user_id = get_user_id()
        except KeyError:
            if strict:
                raise
            user_id = cast(Union[Unset, str], UNSET)

        membership_create = cls(
            role=role,
            user_id=user_id,
        )

        membership_create.additional_properties = d
        return membership_create

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
    def role(self) -> MembershipCreateRole:
        if isinstance(self._role, Unset):
            raise NotPresentError(self, "role")
        return self._role

    @role.setter
    def role(self, value: MembershipCreateRole) -> None:
        self._role = value

    @role.deleter
    def role(self) -> None:
        self._role = UNSET

    @property
    def user_id(self) -> str:
        if isinstance(self._user_id, Unset):
            raise NotPresentError(self, "user_id")
        return self._user_id

    @user_id.setter
    def user_id(self, value: str) -> None:
        self._user_id = value

    @user_id.deleter
    def user_id(self) -> None:
        self._user_id = UNSET
