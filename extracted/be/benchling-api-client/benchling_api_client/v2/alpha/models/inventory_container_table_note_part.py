from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.inventory_container_table_note_part_mode import InventoryContainerTableNotePartMode
from ..models.inventory_container_table_note_part_type import InventoryContainerTableNotePartType
from ..models.structured_table_column_info import StructuredTableColumnInfo
from ..types import UNSET, Unset

T = TypeVar("T", bound="InventoryContainerTableNotePart")


@attr.s(auto_attribs=True, repr=False)
class InventoryContainerTableNotePart:
    """  """

    _destination_container_schema_id: Union[Unset, str] = UNSET
    _mode: Union[Unset, InventoryContainerTableNotePartMode] = UNSET
    _type: Union[Unset, InventoryContainerTableNotePartType] = UNSET
    _api_id: Union[Unset, str] = UNSET
    _columns: Union[Unset, List[StructuredTableColumnInfo]] = UNSET
    _indentation: Union[Unset, int] = 0
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append(
            "destination_container_schema_id={}".format(repr(self._destination_container_schema_id))
        )
        fields.append("mode={}".format(repr(self._mode)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("api_id={}".format(repr(self._api_id)))
        fields.append("columns={}".format(repr(self._columns)))
        fields.append("indentation={}".format(repr(self._indentation)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "InventoryContainerTableNotePart({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        destination_container_schema_id = self._destination_container_schema_id
        mode: Union[Unset, int] = UNSET
        if not isinstance(self._mode, Unset):
            mode = self._mode.value

        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        api_id = self._api_id
        columns: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._columns, Unset):
            columns = []
            for columns_item_data in self._columns:
                columns_item = columns_item_data.to_dict()

                columns.append(columns_item)

        indentation = self._indentation

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if destination_container_schema_id is not UNSET:
            field_dict["destinationContainerSchemaId"] = destination_container_schema_id
        if mode is not UNSET:
            field_dict["mode"] = mode
        if type is not UNSET:
            field_dict["type"] = type
        if api_id is not UNSET:
            field_dict["apiId"] = api_id
        if columns is not UNSET:
            field_dict["columns"] = columns
        if indentation is not UNSET:
            field_dict["indentation"] = indentation

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_destination_container_schema_id() -> Union[Unset, str]:
            destination_container_schema_id = d.pop("destinationContainerSchemaId")
            return destination_container_schema_id

        try:
            destination_container_schema_id = get_destination_container_schema_id()
        except KeyError:
            if strict:
                raise
            destination_container_schema_id = cast(Union[Unset, str], UNSET)

        def get_mode() -> Union[Unset, InventoryContainerTableNotePartMode]:
            mode = UNSET
            _mode = d.pop("mode")
            if _mode is not None and _mode is not UNSET:
                try:
                    mode = InventoryContainerTableNotePartMode(_mode)
                except ValueError:
                    mode = InventoryContainerTableNotePartMode.of_unknown(_mode)

            return mode

        try:
            mode = get_mode()
        except KeyError:
            if strict:
                raise
            mode = cast(Union[Unset, InventoryContainerTableNotePartMode], UNSET)

        def get_type() -> Union[Unset, InventoryContainerTableNotePartType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = InventoryContainerTableNotePartType(_type)
                except ValueError:
                    type = InventoryContainerTableNotePartType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, InventoryContainerTableNotePartType], UNSET)

        def get_api_id() -> Union[Unset, str]:
            api_id = d.pop("apiId")
            return api_id

        try:
            api_id = get_api_id()
        except KeyError:
            if strict:
                raise
            api_id = cast(Union[Unset, str], UNSET)

        def get_columns() -> Union[Unset, List[StructuredTableColumnInfo]]:
            columns = []
            _columns = d.pop("columns")
            for columns_item_data in _columns or []:
                columns_item = StructuredTableColumnInfo.from_dict(columns_item_data, strict=False)

                columns.append(columns_item)

            return columns

        try:
            columns = get_columns()
        except KeyError:
            if strict:
                raise
            columns = cast(Union[Unset, List[StructuredTableColumnInfo]], UNSET)

        def get_indentation() -> Union[Unset, int]:
            indentation = d.pop("indentation")
            return indentation

        try:
            indentation = get_indentation()
        except KeyError:
            if strict:
                raise
            indentation = cast(Union[Unset, int], UNSET)

        inventory_container_table_note_part = cls(
            destination_container_schema_id=destination_container_schema_id,
            mode=mode,
            type=type,
            api_id=api_id,
            columns=columns,
            indentation=indentation,
        )

        inventory_container_table_note_part.additional_properties = d
        return inventory_container_table_note_part

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
    def destination_container_schema_id(self) -> str:
        if isinstance(self._destination_container_schema_id, Unset):
            raise NotPresentError(self, "destination_container_schema_id")
        return self._destination_container_schema_id

    @destination_container_schema_id.setter
    def destination_container_schema_id(self, value: str) -> None:
        self._destination_container_schema_id = value

    @destination_container_schema_id.deleter
    def destination_container_schema_id(self) -> None:
        self._destination_container_schema_id = UNSET

    @property
    def mode(self) -> InventoryContainerTableNotePartMode:
        if isinstance(self._mode, Unset):
            raise NotPresentError(self, "mode")
        return self._mode

    @mode.setter
    def mode(self, value: InventoryContainerTableNotePartMode) -> None:
        self._mode = value

    @mode.deleter
    def mode(self) -> None:
        self._mode = UNSET

    @property
    def type(self) -> InventoryContainerTableNotePartType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: InventoryContainerTableNotePartType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET

    @property
    def api_id(self) -> str:
        if isinstance(self._api_id, Unset):
            raise NotPresentError(self, "api_id")
        return self._api_id

    @api_id.setter
    def api_id(self, value: str) -> None:
        self._api_id = value

    @api_id.deleter
    def api_id(self) -> None:
        self._api_id = UNSET

    @property
    def columns(self) -> List[StructuredTableColumnInfo]:
        if isinstance(self._columns, Unset):
            raise NotPresentError(self, "columns")
        return self._columns

    @columns.setter
    def columns(self, value: List[StructuredTableColumnInfo]) -> None:
        self._columns = value

    @columns.deleter
    def columns(self) -> None:
        self._columns = UNSET

    @property
    def indentation(self) -> int:
        """ All notes have an indentation level - the default is 0 for no indent. For lists, indentation gives notes hierarchy - a bulleted list with children is modeled as one note part with indentation 1 followed by note parts with indentation 2, for example. """
        if isinstance(self._indentation, Unset):
            raise NotPresentError(self, "indentation")
        return self._indentation

    @indentation.setter
    def indentation(self, value: int) -> None:
        self._indentation = value

    @indentation.deleter
    def indentation(self) -> None:
        self._indentation = UNSET
