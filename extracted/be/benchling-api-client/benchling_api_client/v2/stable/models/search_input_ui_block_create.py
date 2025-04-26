from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.search_input_ui_block_item_type import SearchInputUiBlockItemType
from ..models.search_input_ui_block_type import SearchInputUiBlockType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchInputUiBlockCreate")


@attr.s(auto_attribs=True, repr=False)
class SearchInputUiBlockCreate:
    """  """

    _id: str
    _type: Union[Unset, SearchInputUiBlockType] = UNSET
    _item_type: Union[Unset, SearchInputUiBlockItemType] = UNSET
    _schema_id: Union[Unset, None, str] = UNSET
    _label: Union[Unset, None, str] = UNSET
    _value: Union[Unset, None, str] = UNSET
    _enabled: Union[Unset, None, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("item_type={}".format(repr(self._item_type)))
        fields.append("schema_id={}".format(repr(self._schema_id)))
        fields.append("label={}".format(repr(self._label)))
        fields.append("value={}".format(repr(self._value)))
        fields.append("enabled={}".format(repr(self._enabled)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "SearchInputUiBlockCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        item_type: Union[Unset, int] = UNSET
        if not isinstance(self._item_type, Unset):
            item_type = self._item_type.value

        schema_id = self._schema_id
        label = self._label
        value = self._value
        enabled = self._enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id
        if type is not UNSET:
            field_dict["type"] = type
        if item_type is not UNSET:
            field_dict["itemType"] = item_type
        if schema_id is not UNSET:
            field_dict["schemaId"] = schema_id
        if label is not UNSET:
            field_dict["label"] = label
        if value is not UNSET:
            field_dict["value"] = value
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_id() -> str:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(str, UNSET)

        def get_type() -> Union[Unset, SearchInputUiBlockType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = SearchInputUiBlockType(_type)
                except ValueError:
                    type = SearchInputUiBlockType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, SearchInputUiBlockType], UNSET)

        def get_item_type() -> Union[Unset, SearchInputUiBlockItemType]:
            item_type = UNSET
            _item_type = d.pop("itemType")
            if _item_type is not None and _item_type is not UNSET:
                try:
                    item_type = SearchInputUiBlockItemType(_item_type)
                except ValueError:
                    item_type = SearchInputUiBlockItemType.of_unknown(_item_type)

            return item_type

        try:
            item_type = get_item_type()
        except KeyError:
            if strict:
                raise
            item_type = cast(Union[Unset, SearchInputUiBlockItemType], UNSET)

        def get_schema_id() -> Union[Unset, None, str]:
            schema_id = d.pop("schemaId")
            return schema_id

        try:
            schema_id = get_schema_id()
        except KeyError:
            if strict:
                raise
            schema_id = cast(Union[Unset, None, str], UNSET)

        def get_label() -> Union[Unset, None, str]:
            label = d.pop("label")
            return label

        try:
            label = get_label()
        except KeyError:
            if strict:
                raise
            label = cast(Union[Unset, None, str], UNSET)

        def get_value() -> Union[Unset, None, str]:
            value = d.pop("value")
            return value

        try:
            value = get_value()
        except KeyError:
            if strict:
                raise
            value = cast(Union[Unset, None, str], UNSET)

        def get_enabled() -> Union[Unset, None, bool]:
            enabled = d.pop("enabled")
            return enabled

        try:
            enabled = get_enabled()
        except KeyError:
            if strict:
                raise
            enabled = cast(Union[Unset, None, bool], UNSET)

        search_input_ui_block_create = cls(
            id=id,
            type=type,
            item_type=item_type,
            schema_id=schema_id,
            label=label,
            value=value,
            enabled=enabled,
        )

        search_input_ui_block_create.additional_properties = d
        return search_input_ui_block_create

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
    def id(self) -> str:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @property
    def type(self) -> SearchInputUiBlockType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: SearchInputUiBlockType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET

    @property
    def item_type(self) -> SearchInputUiBlockItemType:
        if isinstance(self._item_type, Unset):
            raise NotPresentError(self, "item_type")
        return self._item_type

    @item_type.setter
    def item_type(self, value: SearchInputUiBlockItemType) -> None:
        self._item_type = value

    @item_type.deleter
    def item_type(self) -> None:
        self._item_type = UNSET

    @property
    def schema_id(self) -> Optional[str]:
        if isinstance(self._schema_id, Unset):
            raise NotPresentError(self, "schema_id")
        return self._schema_id

    @schema_id.setter
    def schema_id(self, value: Optional[str]) -> None:
        self._schema_id = value

    @schema_id.deleter
    def schema_id(self) -> None:
        self._schema_id = UNSET

    @property
    def label(self) -> Optional[str]:
        if isinstance(self._label, Unset):
            raise NotPresentError(self, "label")
        return self._label

    @label.setter
    def label(self, value: Optional[str]) -> None:
        self._label = value

    @label.deleter
    def label(self) -> None:
        self._label = UNSET

    @property
    def value(self) -> Optional[str]:
        if isinstance(self._value, Unset):
            raise NotPresentError(self, "value")
        return self._value

    @value.setter
    def value(self, value: Optional[str]) -> None:
        self._value = value

    @value.deleter
    def value(self) -> None:
        self._value = UNSET

    @property
    def enabled(self) -> Optional[bool]:
        if isinstance(self._enabled, Unset):
            raise NotPresentError(self, "enabled")
        return self._enabled

    @enabled.setter
    def enabled(self, value: Optional[bool]) -> None:
        self._enabled = value

    @enabled.deleter
    def enabled(self) -> None:
        self._enabled = UNSET
