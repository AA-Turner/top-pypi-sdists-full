from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="User")


@attr.s(auto_attribs=True, repr=False)
class User:
    """  """

    _api_key_last_changed_at: Union[Unset, None, str] = UNSET
    _email: Union[Unset, str] = UNSET
    _is_suspended: Union[Unset, bool] = UNSET
    _password_last_changed_at: Union[Unset, None, str] = UNSET
    _handle: Union[Unset, str] = UNSET
    _id: Union[Unset, str] = UNSET
    _name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("api_key_last_changed_at={}".format(repr(self._api_key_last_changed_at)))
        fields.append("email={}".format(repr(self._email)))
        fields.append("is_suspended={}".format(repr(self._is_suspended)))
        fields.append("password_last_changed_at={}".format(repr(self._password_last_changed_at)))
        fields.append("handle={}".format(repr(self._handle)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "User({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        api_key_last_changed_at = self._api_key_last_changed_at
        email = self._email
        is_suspended = self._is_suspended
        password_last_changed_at = self._password_last_changed_at
        handle = self._handle
        id = self._id
        name = self._name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if api_key_last_changed_at is not UNSET:
            field_dict["apiKeyLastChangedAt"] = api_key_last_changed_at
        if email is not UNSET:
            field_dict["email"] = email
        if is_suspended is not UNSET:
            field_dict["isSuspended"] = is_suspended
        if password_last_changed_at is not UNSET:
            field_dict["passwordLastChangedAt"] = password_last_changed_at
        if handle is not UNSET:
            field_dict["handle"] = handle
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_api_key_last_changed_at() -> Union[Unset, None, str]:
            api_key_last_changed_at = d.pop("apiKeyLastChangedAt")
            return api_key_last_changed_at

        try:
            api_key_last_changed_at = get_api_key_last_changed_at()
        except KeyError:
            if strict:
                raise
            api_key_last_changed_at = cast(Union[Unset, None, str], UNSET)

        def get_email() -> Union[Unset, str]:
            email = d.pop("email")
            return email

        try:
            email = get_email()
        except KeyError:
            if strict:
                raise
            email = cast(Union[Unset, str], UNSET)

        def get_is_suspended() -> Union[Unset, bool]:
            is_suspended = d.pop("isSuspended")
            return is_suspended

        try:
            is_suspended = get_is_suspended()
        except KeyError:
            if strict:
                raise
            is_suspended = cast(Union[Unset, bool], UNSET)

        def get_password_last_changed_at() -> Union[Unset, None, str]:
            password_last_changed_at = d.pop("passwordLastChangedAt")
            return password_last_changed_at

        try:
            password_last_changed_at = get_password_last_changed_at()
        except KeyError:
            if strict:
                raise
            password_last_changed_at = cast(Union[Unset, None, str], UNSET)

        def get_handle() -> Union[Unset, str]:
            handle = d.pop("handle")
            return handle

        try:
            handle = get_handle()
        except KeyError:
            if strict:
                raise
            handle = cast(Union[Unset, str], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        user = cls(
            api_key_last_changed_at=api_key_last_changed_at,
            email=email,
            is_suspended=is_suspended,
            password_last_changed_at=password_last_changed_at,
            handle=handle,
            id=id,
            name=name,
        )

        user.additional_properties = d
        return user

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
    def api_key_last_changed_at(self) -> Optional[str]:
        if isinstance(self._api_key_last_changed_at, Unset):
            raise NotPresentError(self, "api_key_last_changed_at")
        return self._api_key_last_changed_at

    @api_key_last_changed_at.setter
    def api_key_last_changed_at(self, value: Optional[str]) -> None:
        self._api_key_last_changed_at = value

    @api_key_last_changed_at.deleter
    def api_key_last_changed_at(self) -> None:
        self._api_key_last_changed_at = UNSET

    @property
    def email(self) -> str:
        if isinstance(self._email, Unset):
            raise NotPresentError(self, "email")
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        self._email = value

    @email.deleter
    def email(self) -> None:
        self._email = UNSET

    @property
    def is_suspended(self) -> bool:
        if isinstance(self._is_suspended, Unset):
            raise NotPresentError(self, "is_suspended")
        return self._is_suspended

    @is_suspended.setter
    def is_suspended(self, value: bool) -> None:
        self._is_suspended = value

    @is_suspended.deleter
    def is_suspended(self) -> None:
        self._is_suspended = UNSET

    @property
    def password_last_changed_at(self) -> Optional[str]:
        if isinstance(self._password_last_changed_at, Unset):
            raise NotPresentError(self, "password_last_changed_at")
        return self._password_last_changed_at

    @password_last_changed_at.setter
    def password_last_changed_at(self, value: Optional[str]) -> None:
        self._password_last_changed_at = value

    @password_last_changed_at.deleter
    def password_last_changed_at(self) -> None:
        self._password_last_changed_at = UNSET

    @property
    def handle(self) -> str:
        if isinstance(self._handle, Unset):
            raise NotPresentError(self, "handle")
        return self._handle

    @handle.setter
    def handle(self, value: str) -> None:
        self._handle = value

    @handle.deleter
    def handle(self) -> None:
        self._handle = UNSET

    @property
    def id(self) -> str:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET
