from typing import Any, cast, Dict, List, Optional, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.search_input_ui_block_item_type import SearchInputUiBlockItemType
from ..types import UNSET, Unset

T = TypeVar("T", bound="BaseSearchInputUIBlock")


@attr.s(auto_attribs=True, repr=False)
class BaseSearchInputUIBlock:
    """  """

    _item_type: SearchInputUiBlockItemType
    _schema_id: Optional[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("item_type={}".format(repr(self._item_type)))
        fields.append("schema_id={}".format(repr(self._schema_id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "BaseSearchInputUIBlock({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        item_type = self._item_type.value

        schema_id = self._schema_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if item_type is not UNSET:
            field_dict["itemType"] = item_type
        if schema_id is not UNSET:
            field_dict["schemaId"] = schema_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_item_type() -> SearchInputUiBlockItemType:
            _item_type = d.pop("itemType")
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
            item_type = cast(SearchInputUiBlockItemType, UNSET)

        def get_schema_id() -> Optional[str]:
            schema_id = d.pop("schemaId")
            return schema_id

        try:
            schema_id = get_schema_id()
        except KeyError:
            if strict:
                raise
            schema_id = cast(Optional[str], UNSET)

        base_search_input_ui_block = cls(
            item_type=item_type,
            schema_id=schema_id,
        )

        base_search_input_ui_block.additional_properties = d
        return base_search_input_ui_block

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
    def item_type(self) -> SearchInputUiBlockItemType:
        if isinstance(self._item_type, Unset):
            raise NotPresentError(self, "item_type")
        return self._item_type

    @item_type.setter
    def item_type(self, value: SearchInputUiBlockItemType) -> None:
        self._item_type = value

    @property
    def schema_id(self) -> Optional[str]:
        if isinstance(self._schema_id, Unset):
            raise NotPresentError(self, "schema_id")
        return self._schema_id

    @schema_id.setter
    def schema_id(self, value: Optional[str]) -> None:
        self._schema_id = value
