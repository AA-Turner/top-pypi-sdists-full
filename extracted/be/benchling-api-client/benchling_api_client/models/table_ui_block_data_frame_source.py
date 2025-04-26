from typing import Any, cast, Dict, List, Optional, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.table_ui_block_data_frame_source_type import TableUiBlockDataFrameSourceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="TableUiBlockDataFrameSource")


@attr.s(auto_attribs=True, repr=False)
class TableUiBlockDataFrameSource:
    """  """

    _type: TableUiBlockDataFrameSourceType
    _data_frame_id: Optional[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("type={}".format(repr(self._type)))
        fields.append("data_frame_id={}".format(repr(self._data_frame_id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "TableUiBlockDataFrameSource({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        type = self._type.value

        data_frame_id = self._data_frame_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if type is not UNSET:
            field_dict["type"] = type
        if data_frame_id is not UNSET:
            field_dict["dataFrameId"] = data_frame_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_type() -> TableUiBlockDataFrameSourceType:
            _type = d.pop("type")
            try:
                type = TableUiBlockDataFrameSourceType(_type)
            except ValueError:
                type = TableUiBlockDataFrameSourceType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(TableUiBlockDataFrameSourceType, UNSET)

        def get_data_frame_id() -> Optional[str]:
            data_frame_id = d.pop("dataFrameId")
            return data_frame_id

        try:
            data_frame_id = get_data_frame_id()
        except KeyError:
            if strict:
                raise
            data_frame_id = cast(Optional[str], UNSET)

        table_ui_block_data_frame_source = cls(
            type=type,
            data_frame_id=data_frame_id,
        )

        table_ui_block_data_frame_source.additional_properties = d
        return table_ui_block_data_frame_source

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
    def type(self) -> TableUiBlockDataFrameSourceType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: TableUiBlockDataFrameSourceType) -> None:
        self._type = value

    @property
    def data_frame_id(self) -> Optional[str]:
        """`dataFrameId` of an uploaded data frame (see [Create Data Frame endpoint](https://benchling.com/api/v2-beta/reference#/Data%20Frames)). Note: Canvas tables currently support only text-type columns."""
        if isinstance(self._data_frame_id, Unset):
            raise NotPresentError(self, "data_frame_id")
        return self._data_frame_id

    @data_frame_id.setter
    def data_frame_id(self, value: Optional[str]) -> None:
        self._data_frame_id = value
