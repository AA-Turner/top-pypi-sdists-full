from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.forbidden_restricted_sample_error_error_type import ForbiddenRestrictedSampleErrorErrorType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ForbiddenRestrictedSampleErrorError")


@attr.s(auto_attribs=True, repr=False)
class ForbiddenRestrictedSampleErrorError:
    """  """

    _invalid_ids: Union[Unset, List[str]] = UNSET
    _type: Union[Unset, ForbiddenRestrictedSampleErrorErrorType] = UNSET
    _message: Union[Unset, str] = UNSET
    _user_message: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("invalid_ids={}".format(repr(self._invalid_ids)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("message={}".format(repr(self._message)))
        fields.append("user_message={}".format(repr(self._user_message)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "ForbiddenRestrictedSampleErrorError({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        invalid_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._invalid_ids, Unset):
            invalid_ids = self._invalid_ids

        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        message = self._message
        user_message = self._user_message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if invalid_ids is not UNSET:
            field_dict["invalidIds"] = invalid_ids
        if type is not UNSET:
            field_dict["type"] = type
        if message is not UNSET:
            field_dict["message"] = message
        if user_message is not UNSET:
            field_dict["userMessage"] = user_message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_invalid_ids() -> Union[Unset, List[str]]:
            invalid_ids = cast(List[str], d.pop("invalidIds"))

            return invalid_ids

        try:
            invalid_ids = get_invalid_ids()
        except KeyError:
            if strict:
                raise
            invalid_ids = cast(Union[Unset, List[str]], UNSET)

        def get_type() -> Union[Unset, ForbiddenRestrictedSampleErrorErrorType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = ForbiddenRestrictedSampleErrorErrorType(_type)
                except ValueError:
                    type = ForbiddenRestrictedSampleErrorErrorType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, ForbiddenRestrictedSampleErrorErrorType], UNSET)

        def get_message() -> Union[Unset, str]:
            message = d.pop("message")
            return message

        try:
            message = get_message()
        except KeyError:
            if strict:
                raise
            message = cast(Union[Unset, str], UNSET)

        def get_user_message() -> Union[Unset, str]:
            user_message = d.pop("userMessage")
            return user_message

        try:
            user_message = get_user_message()
        except KeyError:
            if strict:
                raise
            user_message = cast(Union[Unset, str], UNSET)

        forbidden_restricted_sample_error_error = cls(
            invalid_ids=invalid_ids,
            type=type,
            message=message,
            user_message=user_message,
        )

        forbidden_restricted_sample_error_error.additional_properties = d
        return forbidden_restricted_sample_error_error

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
    def invalid_ids(self) -> List[str]:
        if isinstance(self._invalid_ids, Unset):
            raise NotPresentError(self, "invalid_ids")
        return self._invalid_ids

    @invalid_ids.setter
    def invalid_ids(self, value: List[str]) -> None:
        self._invalid_ids = value

    @invalid_ids.deleter
    def invalid_ids(self) -> None:
        self._invalid_ids = UNSET

    @property
    def type(self) -> ForbiddenRestrictedSampleErrorErrorType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: ForbiddenRestrictedSampleErrorErrorType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET

    @property
    def message(self) -> str:
        if isinstance(self._message, Unset):
            raise NotPresentError(self, "message")
        return self._message

    @message.setter
    def message(self, value: str) -> None:
        self._message = value

    @message.deleter
    def message(self) -> None:
        self._message = UNSET

    @property
    def user_message(self) -> str:
        if isinstance(self._user_message, Unset):
            raise NotPresentError(self, "user_message")
        return self._user_message

    @user_message.setter
    def user_message(self, value: str) -> None:
        self._user_message = value

    @user_message.deleter
    def user_message(self) -> None:
        self._user_message = UNSET
