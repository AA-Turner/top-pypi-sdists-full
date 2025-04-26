import datetime
from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="WarehouseCredentialSummary")


@attr.s(auto_attribs=True, repr=False)
class WarehouseCredentialSummary:
    """  """

    _created_at: Union[Unset, datetime.datetime] = UNSET
    _id: Union[Unset, str] = UNSET
    _label: Union[Unset, str] = UNSET
    _modified_at: Union[Unset, datetime.datetime] = UNSET
    _user_id: Union[Unset, str] = UNSET
    _username: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("label={}".format(repr(self._label)))
        fields.append("modified_at={}".format(repr(self._modified_at)))
        fields.append("user_id={}".format(repr(self._user_id)))
        fields.append("username={}".format(repr(self._username)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "WarehouseCredentialSummary({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self._created_at, Unset):
            created_at = self._created_at.isoformat()

        id = self._id
        label = self._label
        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self._modified_at, Unset):
            modified_at = self._modified_at.isoformat()

        user_id = self._user_id
        username = self._username

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if id is not UNSET:
            field_dict["id"] = id
        if label is not UNSET:
            field_dict["label"] = label
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if user_id is not UNSET:
            field_dict["userId"] = user_id
        if username is not UNSET:
            field_dict["username"] = username

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_created_at() -> Union[Unset, datetime.datetime]:
            created_at: Union[Unset, datetime.datetime] = UNSET
            _created_at = d.pop("createdAt")
            if _created_at is not None and not isinstance(_created_at, Unset):
                created_at = isoparse(cast(str, _created_at))

            return created_at

        try:
            created_at = get_created_at()
        except KeyError:
            if strict:
                raise
            created_at = cast(Union[Unset, datetime.datetime], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_label() -> Union[Unset, str]:
            label = d.pop("label")
            return label

        try:
            label = get_label()
        except KeyError:
            if strict:
                raise
            label = cast(Union[Unset, str], UNSET)

        def get_modified_at() -> Union[Unset, datetime.datetime]:
            modified_at: Union[Unset, datetime.datetime] = UNSET
            _modified_at = d.pop("modifiedAt")
            if _modified_at is not None and not isinstance(_modified_at, Unset):
                modified_at = isoparse(cast(str, _modified_at))

            return modified_at

        try:
            modified_at = get_modified_at()
        except KeyError:
            if strict:
                raise
            modified_at = cast(Union[Unset, datetime.datetime], UNSET)

        def get_user_id() -> Union[Unset, str]:
            user_id = d.pop("userId")
            return user_id

        try:
            user_id = get_user_id()
        except KeyError:
            if strict:
                raise
            user_id = cast(Union[Unset, str], UNSET)

        def get_username() -> Union[Unset, str]:
            username = d.pop("username")
            return username

        try:
            username = get_username()
        except KeyError:
            if strict:
                raise
            username = cast(Union[Unset, str], UNSET)

        warehouse_credential_summary = cls(
            created_at=created_at,
            id=id,
            label=label,
            modified_at=modified_at,
            user_id=user_id,
            username=username,
        )

        warehouse_credential_summary.additional_properties = d
        return warehouse_credential_summary

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
    def created_at(self) -> datetime.datetime:
        if isinstance(self._created_at, Unset):
            raise NotPresentError(self, "created_at")
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime.datetime) -> None:
        self._created_at = value

    @created_at.deleter
    def created_at(self) -> None:
        self._created_at = UNSET

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
    def label(self) -> str:
        if isinstance(self._label, Unset):
            raise NotPresentError(self, "label")
        return self._label

    @label.setter
    def label(self, value: str) -> None:
        self._label = value

    @label.deleter
    def label(self) -> None:
        self._label = UNSET

    @property
    def modified_at(self) -> datetime.datetime:
        if isinstance(self._modified_at, Unset):
            raise NotPresentError(self, "modified_at")
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value: datetime.datetime) -> None:
        self._modified_at = value

    @modified_at.deleter
    def modified_at(self) -> None:
        self._modified_at = UNSET

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

    @property
    def username(self) -> str:
        """ The username to connect to the warehouse. """
        if isinstance(self._username, Unset):
            raise NotPresentError(self, "username")
        return self._username

    @username.setter
    def username(self, value: str) -> None:
        self._username = value

    @username.deleter
    def username(self) -> None:
        self._username = UNSET
