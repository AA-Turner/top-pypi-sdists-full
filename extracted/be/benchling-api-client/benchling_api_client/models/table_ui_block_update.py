from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.table_ui_block_data_frame_source import TableUiBlockDataFrameSource
from ..models.table_ui_block_dataset_source import TableUiBlockDatasetSource
from ..models.table_ui_block_type import TableUiBlockType
from ..types import UNSET, Unset

T = TypeVar("T", bound="TableUiBlockUpdate")


@attr.s(auto_attribs=True, repr=False)
class TableUiBlockUpdate:
    """  """

    _id: str
    _max_rows: Union[Unset, int] = UNSET
    _name: Union[Unset, str] = UNSET
    _source: Union[Unset, TableUiBlockDatasetSource, TableUiBlockDataFrameSource, UnknownType] = UNSET
    _type: Union[Unset, TableUiBlockType] = UNSET
    _enabled: Union[Unset, None, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("max_rows={}".format(repr(self._max_rows)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("source={}".format(repr(self._source)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("enabled={}".format(repr(self._enabled)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "TableUiBlockUpdate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        max_rows = self._max_rows
        name = self._name
        source: Union[Unset, Dict[str, Any]]
        if isinstance(self._source, Unset):
            source = UNSET
        elif isinstance(self._source, UnknownType):
            source = self._source.value
        elif isinstance(self._source, TableUiBlockDatasetSource):
            source = self._source.to_dict()

        else:
            source = self._source.to_dict()

        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        enabled = self._enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id
        if max_rows is not UNSET:
            field_dict["maxRows"] = max_rows
        if name is not UNSET:
            field_dict["name"] = name
        if source is not UNSET:
            field_dict["source"] = source
        if type is not UNSET:
            field_dict["type"] = type
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

        def get_max_rows() -> Union[Unset, int]:
            max_rows = d.pop("maxRows")
            return max_rows

        try:
            max_rows = get_max_rows()
        except KeyError:
            if strict:
                raise
            max_rows = cast(Union[Unset, int], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        def get_source() -> Union[Unset, TableUiBlockDatasetSource, TableUiBlockDataFrameSource, UnknownType]:
            source: Union[Unset, TableUiBlockDatasetSource, TableUiBlockDataFrameSource, UnknownType]
            _source = d.pop("source")

            if not isinstance(_source, Unset):
                discriminator = _source["type"]
                if discriminator == "DATASET":
                    source = TableUiBlockDatasetSource.from_dict(_source)
                elif discriminator == "DATA_FRAME":
                    source = TableUiBlockDataFrameSource.from_dict(_source)
                else:
                    source = UnknownType(value=_source)

            return source

        try:
            source = get_source()
        except KeyError:
            if strict:
                raise
            source = cast(
                Union[Unset, TableUiBlockDatasetSource, TableUiBlockDataFrameSource, UnknownType], UNSET
            )

        def get_type() -> Union[Unset, TableUiBlockType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = TableUiBlockType(_type)
                except ValueError:
                    type = TableUiBlockType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, TableUiBlockType], UNSET)

        def get_enabled() -> Union[Unset, None, bool]:
            enabled = d.pop("enabled")
            return enabled

        try:
            enabled = get_enabled()
        except KeyError:
            if strict:
                raise
            enabled = cast(Union[Unset, None, bool], UNSET)

        table_ui_block_update = cls(
            id=id,
            max_rows=max_rows,
            name=name,
            source=source,
            type=type,
            enabled=enabled,
        )

        table_ui_block_update.additional_properties = d
        return table_ui_block_update

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
    def max_rows(self) -> int:
        if isinstance(self._max_rows, Unset):
            raise NotPresentError(self, "max_rows")
        return self._max_rows

    @max_rows.setter
    def max_rows(self, value: int) -> None:
        self._max_rows = value

    @max_rows.deleter
    def max_rows(self) -> None:
        self._max_rows = UNSET

    @property
    def name(self) -> str:
        """ Display name for the table block, to be shown in the UI """
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET

    @property
    def source(self) -> Union[TableUiBlockDatasetSource, TableUiBlockDataFrameSource, UnknownType]:
        if isinstance(self._source, Unset):
            raise NotPresentError(self, "source")
        return self._source

    @source.setter
    def source(
        self, value: Union[TableUiBlockDatasetSource, TableUiBlockDataFrameSource, UnknownType]
    ) -> None:
        self._source = value

    @source.deleter
    def source(self) -> None:
        self._source = UNSET

    @property
    def type(self) -> TableUiBlockType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: TableUiBlockType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET

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
