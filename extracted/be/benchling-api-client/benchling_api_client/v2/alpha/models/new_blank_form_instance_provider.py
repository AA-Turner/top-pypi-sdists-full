from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.new_blank_form_instance_provider_type import NewBlankFormInstanceProviderType
from ..types import UNSET, Unset

T = TypeVar("T", bound="NewBlankFormInstanceProvider")


@attr.s(auto_attribs=True, repr=False)
class NewBlankFormInstanceProvider:
    """  """

    _type: Union[Unset, NewBlankFormInstanceProviderType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("type={}".format(repr(self._type)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "NewBlankFormInstanceProvider({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_type() -> Union[Unset, NewBlankFormInstanceProviderType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = NewBlankFormInstanceProviderType(_type)
                except ValueError:
                    type = NewBlankFormInstanceProviderType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, NewBlankFormInstanceProviderType], UNSET)

        new_blank_form_instance_provider = cls(
            type=type,
        )

        new_blank_form_instance_provider.additional_properties = d
        return new_blank_form_instance_provider

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
    def type(self) -> NewBlankFormInstanceProviderType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: NewBlankFormInstanceProviderType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET
