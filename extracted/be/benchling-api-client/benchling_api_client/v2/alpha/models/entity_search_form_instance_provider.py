from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.entity_search_form_instance_provider_type import EntitySearchFormInstanceProviderType
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntitySearchFormInstanceProvider")


@attr.s(auto_attribs=True, repr=False)
class EntitySearchFormInstanceProvider:
    """  """

    _target_field_key: Union[Unset, str] = UNSET
    _type: Union[Unset, EntitySearchFormInstanceProviderType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("target_field_key={}".format(repr(self._target_field_key)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "EntitySearchFormInstanceProvider({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        target_field_key = self._target_field_key
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if target_field_key is not UNSET:
            field_dict["targetFieldKey"] = target_field_key
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_target_field_key() -> Union[Unset, str]:
            target_field_key = d.pop("targetFieldKey")
            return target_field_key

        try:
            target_field_key = get_target_field_key()
        except KeyError:
            if strict:
                raise
            target_field_key = cast(Union[Unset, str], UNSET)

        def get_type() -> Union[Unset, EntitySearchFormInstanceProviderType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = EntitySearchFormInstanceProviderType(_type)
                except ValueError:
                    type = EntitySearchFormInstanceProviderType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, EntitySearchFormInstanceProviderType], UNSET)

        entity_search_form_instance_provider = cls(
            target_field_key=target_field_key,
            type=type,
        )

        entity_search_form_instance_provider.additional_properties = d
        return entity_search_form_instance_provider

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
    def target_field_key(self) -> str:
        """Where the entities that we search for should be populated within our form. Note here that we inherit any considerations and limitations on the values these entities can take on, like schemaId, from the definition of the field we're routing them to."""
        if isinstance(self._target_field_key, Unset):
            raise NotPresentError(self, "target_field_key")
        return self._target_field_key

    @target_field_key.setter
    def target_field_key(self, value: str) -> None:
        self._target_field_key = value

    @target_field_key.deleter
    def target_field_key(self) -> None:
        self._target_field_key = UNSET

    @property
    def type(self) -> EntitySearchFormInstanceProviderType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: EntitySearchFormInstanceProviderType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET
