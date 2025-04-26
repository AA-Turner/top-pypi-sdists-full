from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.field_type import FieldType
from ..types import UNSET, Unset

T = TypeVar("T", bound="FieldCreate")


@attr.s(auto_attribs=True, repr=False)
class FieldCreate:
    """  """

    _field_type: Union[Unset, FieldType] = UNSET
    _is_multi: Union[Unset, bool] = UNSET
    _is_parent_link: Union[Unset, bool] = UNSET
    _is_required: Union[Unset, bool] = UNSET
    _name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("field_type={}".format(repr(self._field_type)))
        fields.append("is_multi={}".format(repr(self._is_multi)))
        fields.append("is_parent_link={}".format(repr(self._is_parent_link)))
        fields.append("is_required={}".format(repr(self._is_required)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "FieldCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        field_type: Union[Unset, int] = UNSET
        if not isinstance(self._field_type, Unset):
            field_type = self._field_type.value

        is_multi = self._is_multi
        is_parent_link = self._is_parent_link
        is_required = self._is_required
        name = self._name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if field_type is not UNSET:
            field_dict["fieldType"] = field_type
        if is_multi is not UNSET:
            field_dict["isMulti"] = is_multi
        if is_parent_link is not UNSET:
            field_dict["isParentLink"] = is_parent_link
        if is_required is not UNSET:
            field_dict["isRequired"] = is_required
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_field_type() -> Union[Unset, FieldType]:
            field_type = UNSET
            _field_type = d.pop("fieldType")
            if _field_type is not None and _field_type is not UNSET:
                try:
                    field_type = FieldType(_field_type)
                except ValueError:
                    field_type = FieldType.of_unknown(_field_type)

            return field_type

        try:
            field_type = get_field_type()
        except KeyError:
            if strict:
                raise
            field_type = cast(Union[Unset, FieldType], UNSET)

        def get_is_multi() -> Union[Unset, bool]:
            is_multi = d.pop("isMulti")
            return is_multi

        try:
            is_multi = get_is_multi()
        except KeyError:
            if strict:
                raise
            is_multi = cast(Union[Unset, bool], UNSET)

        def get_is_parent_link() -> Union[Unset, bool]:
            is_parent_link = d.pop("isParentLink")
            return is_parent_link

        try:
            is_parent_link = get_is_parent_link()
        except KeyError:
            if strict:
                raise
            is_parent_link = cast(Union[Unset, bool], UNSET)

        def get_is_required() -> Union[Unset, bool]:
            is_required = d.pop("isRequired")
            return is_required

        try:
            is_required = get_is_required()
        except KeyError:
            if strict:
                raise
            is_required = cast(Union[Unset, bool], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        field_create = cls(
            field_type=field_type,
            is_multi=is_multi,
            is_parent_link=is_parent_link,
            is_required=is_required,
            name=name,
        )

        field_create.additional_properties = d
        return field_create

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
    def field_type(self) -> FieldType:
        if isinstance(self._field_type, Unset):
            raise NotPresentError(self, "field_type")
        return self._field_type

    @field_type.setter
    def field_type(self, value: FieldType) -> None:
        self._field_type = value

    @field_type.deleter
    def field_type(self) -> None:
        self._field_type = UNSET

    @property
    def is_multi(self) -> bool:
        if isinstance(self._is_multi, Unset):
            raise NotPresentError(self, "is_multi")
        return self._is_multi

    @is_multi.setter
    def is_multi(self, value: bool) -> None:
        self._is_multi = value

    @is_multi.deleter
    def is_multi(self) -> None:
        self._is_multi = UNSET

    @property
    def is_parent_link(self) -> bool:
        if isinstance(self._is_parent_link, Unset):
            raise NotPresentError(self, "is_parent_link")
        return self._is_parent_link

    @is_parent_link.setter
    def is_parent_link(self, value: bool) -> None:
        self._is_parent_link = value

    @is_parent_link.deleter
    def is_parent_link(self) -> None:
        self._is_parent_link = UNSET

    @property
    def is_required(self) -> bool:
        if isinstance(self._is_required, Unset):
            raise NotPresentError(self, "is_required")
        return self._is_required

    @is_required.setter
    def is_required(self, value: bool) -> None:
        self._is_required = value

    @is_required.deleter
    def is_required(self) -> None:
        self._is_required = UNSET

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
