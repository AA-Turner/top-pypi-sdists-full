from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.assembly_validation_status_type import AssemblyValidationStatusType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblyValidationStatus")


@attr.s(auto_attribs=True, repr=False)
class AssemblyValidationStatus:
    """  """

    _message: Union[Unset, str] = UNSET
    _type: Union[Unset, AssemblyValidationStatusType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("message={}".format(repr(self._message)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AssemblyValidationStatus({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        message = self._message
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if message is not UNSET:
            field_dict["message"] = message
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_message() -> Union[Unset, str]:
            message = d.pop("message")
            return message

        try:
            message = get_message()
        except KeyError:
            if strict:
                raise
            message = cast(Union[Unset, str], UNSET)

        def get_type() -> Union[Unset, AssemblyValidationStatusType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = AssemblyValidationStatusType(_type)
                except ValueError:
                    type = AssemblyValidationStatusType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, AssemblyValidationStatusType], UNSET)

        assembly_validation_status = cls(
            message=message,
            type=type,
        )

        assembly_validation_status.additional_properties = d
        return assembly_validation_status

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
    def type(self) -> AssemblyValidationStatusType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: AssemblyValidationStatusType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET
