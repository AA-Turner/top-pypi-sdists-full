from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.membership_role import MembershipRole
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="Membership")


@attr.s(auto_attribs=True, repr=False)
class Membership:
    """  """

    _role: Union[Unset, MembershipRole] = UNSET
    _user: Union[Unset, UserSummary] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("role={}".format(repr(self._role)))
        fields.append("user={}".format(repr(self._user)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "Membership({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        role: Union[Unset, int] = UNSET
        if not isinstance(self._role, Unset):
            role = self._role.value

        user: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._user, Unset):
            user = self._user.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if role is not UNSET:
            field_dict["role"] = role
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_role() -> Union[Unset, MembershipRole]:
            role = UNSET
            _role = d.pop("role")
            if _role is not None and _role is not UNSET:
                try:
                    role = MembershipRole(_role)
                except ValueError:
                    role = MembershipRole.of_unknown(_role)

            return role

        try:
            role = get_role()
        except KeyError:
            if strict:
                raise
            role = cast(Union[Unset, MembershipRole], UNSET)

        def get_user() -> Union[Unset, UserSummary]:
            user: Union[Unset, Union[Unset, UserSummary]] = UNSET
            _user = d.pop("user")

            if not isinstance(_user, Unset):
                user = UserSummary.from_dict(_user)

            return user

        try:
            user = get_user()
        except KeyError:
            if strict:
                raise
            user = cast(Union[Unset, UserSummary], UNSET)

        membership = cls(
            role=role,
            user=user,
        )

        membership.additional_properties = d
        return membership

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
    def role(self) -> MembershipRole:
        if isinstance(self._role, Unset):
            raise NotPresentError(self, "role")
        return self._role

    @role.setter
    def role(self, value: MembershipRole) -> None:
        self._role = value

    @role.deleter
    def role(self) -> None:
        self._role = UNSET

    @property
    def user(self) -> UserSummary:
        if isinstance(self._user, Unset):
            raise NotPresentError(self, "user")
        return self._user

    @user.setter
    def user(self, value: UserSummary) -> None:
        self._user = value

    @user.deleter
    def user(self) -> None:
        self._user = UNSET
