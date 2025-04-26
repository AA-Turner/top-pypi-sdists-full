from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.data_frame_create_column_metadata import DataFrameCreateColumnMetadata
from ..models.data_frame_create_manifest_manifest_item import DataFrameCreateManifestManifestItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="DataFrameCreate")


@attr.s(auto_attribs=True, repr=False)
class DataFrameCreate:
    """  """

    _name: str
    _columns: Union[Unset, None, List[DataFrameCreateColumnMetadata]] = UNSET
    _manifest: Union[Unset, List[DataFrameCreateManifestManifestItem]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("name={}".format(repr(self._name)))
        fields.append("columns={}".format(repr(self._columns)))
        fields.append("manifest={}".format(repr(self._manifest)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "DataFrameCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        name = self._name
        columns: Union[Unset, None, List[Any]] = UNSET
        if not isinstance(self._columns, Unset):
            if self._columns is None:
                columns = None
            else:
                columns = []
                for columns_item_data in self._columns:
                    columns_item = columns_item_data.to_dict()

                    columns.append(columns_item)

        manifest: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._manifest, Unset):
            manifest = []
            for manifest_item_data in self._manifest:
                manifest_item = manifest_item_data.to_dict()

                manifest.append(manifest_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if name is not UNSET:
            field_dict["name"] = name
        if columns is not UNSET:
            field_dict["columns"] = columns
        if manifest is not UNSET:
            field_dict["manifest"] = manifest

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_name() -> str:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(str, UNSET)

        def get_columns() -> Union[Unset, None, List[DataFrameCreateColumnMetadata]]:
            columns = []
            _columns = d.pop("columns")
            for columns_item_data in _columns or []:
                columns_item = DataFrameCreateColumnMetadata.from_dict(columns_item_data, strict=False)

                columns.append(columns_item)

            return columns

        try:
            columns = get_columns()
        except KeyError:
            if strict:
                raise
            columns = cast(Union[Unset, None, List[DataFrameCreateColumnMetadata]], UNSET)

        def get_manifest() -> Union[Unset, List[DataFrameCreateManifestManifestItem]]:
            manifest = []
            _manifest = d.pop("manifest")
            for manifest_item_data in _manifest or []:
                manifest_item = DataFrameCreateManifestManifestItem.from_dict(
                    manifest_item_data, strict=False
                )

                manifest.append(manifest_item)

            return manifest

        try:
            manifest = get_manifest()
        except KeyError:
            if strict:
                raise
            manifest = cast(Union[Unset, List[DataFrameCreateManifestManifestItem]], UNSET)

        data_frame_create = cls(
            name=name,
            columns=columns,
            manifest=manifest,
        )

        data_frame_create.additional_properties = d
        return data_frame_create

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
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def columns(self) -> Optional[List[DataFrameCreateColumnMetadata]]:
        """Metadata for each column in the data frame. If provided, data will be validated for conformity to type and nullability constraints. If provided, columns array is expected to contain the same number of elements as the number of data columns in the data. Validation will be performed when `PATCH` is called. If not provided, column metadata will be inferred from the data. For more info on type inference, [click here](https://docs.benchling.com/docs/datasets-ingestion-reference)."""
        if isinstance(self._columns, Unset):
            raise NotPresentError(self, "columns")
        return self._columns

    @columns.setter
    def columns(self, value: Optional[List[DataFrameCreateColumnMetadata]]) -> None:
        self._columns = value

    @columns.deleter
    def columns(self) -> None:
        self._columns = UNSET

    @property
    def manifest(self) -> List[DataFrameCreateManifestManifestItem]:
        if isinstance(self._manifest, Unset):
            raise NotPresentError(self, "manifest")
        return self._manifest

    @manifest.setter
    def manifest(self, value: List[DataFrameCreateManifestManifestItem]) -> None:
        self._manifest = value

    @manifest.deleter
    def manifest(self) -> None:
        self._manifest = UNSET
