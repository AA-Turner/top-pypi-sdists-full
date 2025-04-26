import datetime
from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserActivity")


@attr.s(auto_attribs=True, repr=False)
class UserActivity:
    """  """

    _last_seen: Union[Unset, None, datetime.datetime] = UNSET
    _user_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("last_seen={}".format(repr(self._last_seen)))
        fields.append("user_id={}".format(repr(self._user_id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "UserActivity({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        last_seen: Union[Unset, None, str] = UNSET
        if not isinstance(self._last_seen, Unset):
            last_seen = self._last_seen.isoformat() if self._last_seen else None

        user_id = self._user_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if last_seen is not UNSET:
            field_dict["lastSeen"] = last_seen
        if user_id is not UNSET:
            field_dict["userId"] = user_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_last_seen() -> Union[Unset, None, datetime.datetime]:
            last_seen: Union[Unset, None, datetime.datetime] = UNSET
            _last_seen = d.pop("lastSeen")
            if _last_seen is not None and not isinstance(_last_seen, Unset):
                last_seen = isoparse(cast(str, _last_seen))

            return last_seen

        try:
            last_seen = get_last_seen()
        except KeyError:
            if strict:
                raise
            last_seen = cast(Union[Unset, None, datetime.datetime], UNSET)

        def get_user_id() -> Union[Unset, str]:
            user_id = d.pop("userId")
            return user_id

        try:
            user_id = get_user_id()
        except KeyError:
            if strict:
                raise
            user_id = cast(Union[Unset, str], UNSET)

        user_activity = cls(
            last_seen=last_seen,
            user_id=user_id,
        )

        user_activity.additional_properties = d
        return user_activity

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
    def last_seen(self) -> Optional[datetime.datetime]:
        if isinstance(self._last_seen, Unset):
            raise NotPresentError(self, "last_seen")
        return self._last_seen

    @last_seen.setter
    def last_seen(self, value: Optional[datetime.datetime]) -> None:
        self._last_seen = value

    @last_seen.deleter
    def last_seen(self) -> None:
        self._last_seen = UNSET

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
