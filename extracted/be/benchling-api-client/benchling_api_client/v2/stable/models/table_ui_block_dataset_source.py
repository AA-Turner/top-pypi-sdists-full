from typing import Any, cast, Dict, List, Optional, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.table_ui_block_dataset_source_type import TableUiBlockDatasetSourceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="TableUiBlockDatasetSource")


@attr.s(auto_attribs=True, repr=False)
class TableUiBlockDatasetSource:
    """  """

    _type: TableUiBlockDatasetSourceType
    _dataset_id: Optional[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("type={}".format(repr(self._type)))
        fields.append("dataset_id={}".format(repr(self._dataset_id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "TableUiBlockDatasetSource({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        type = self._type.value

        dataset_id = self._dataset_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if type is not UNSET:
            field_dict["type"] = type
        if dataset_id is not UNSET:
            field_dict["datasetId"] = dataset_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_type() -> TableUiBlockDatasetSourceType:
            _type = d.pop("type")
            try:
                type = TableUiBlockDatasetSourceType(_type)
            except ValueError:
                type = TableUiBlockDatasetSourceType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(TableUiBlockDatasetSourceType, UNSET)

        def get_dataset_id() -> Optional[str]:
            dataset_id = d.pop("datasetId")
            return dataset_id

        try:
            dataset_id = get_dataset_id()
        except KeyError:
            if strict:
                raise
            dataset_id = cast(Optional[str], UNSET)

        table_ui_block_dataset_source = cls(
            type=type,
            dataset_id=dataset_id,
        )

        table_ui_block_dataset_source.additional_properties = d
        return table_ui_block_dataset_source

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
    def type(self) -> TableUiBlockDatasetSourceType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: TableUiBlockDatasetSourceType) -> None:
        self._type = value

    @property
    def dataset_id(self) -> Optional[str]:
        """`datasetId` of an uploaded dataset (see [Create Data Frame endpoint](https://benchling.com/api/v2-beta/reference#/Data%20Frames)). Note: Canvas tables currently support only text-type columns. Datasets are currently undergoing re-work. datasetId will refer to a DataFrame until Dataset APIs are stable. Prefer `TableUiBlockDataFrameSource` meanwhile."""
        if isinstance(self._dataset_id, Unset):
            raise NotPresentError(self, "dataset_id")
        return self._dataset_id

    @dataset_id.setter
    def dataset_id(self, value: Optional[str]) -> None:
        self._dataset_id = value
