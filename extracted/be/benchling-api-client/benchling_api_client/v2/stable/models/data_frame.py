from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.data_frame_column_metadata import DataFrameColumnMetadata
from ..models.data_frame_manifest_manifest_item import DataFrameManifestManifestItem
from ..models.file_status_upload_status import FileStatusUploadStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="DataFrame")


@attr.s(auto_attribs=True, repr=False)
class DataFrame:
    """  """

    _columns: Union[Unset, List[DataFrameColumnMetadata]] = UNSET
    _id: Union[Unset, str] = UNSET
    _name: Union[Unset, str] = UNSET
    _manifest: Union[Unset, List[DataFrameManifestManifestItem]] = UNSET
    _error_message: Union[Unset, None, str] = UNSET
    _upload_status: Union[Unset, FileStatusUploadStatus] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("columns={}".format(repr(self._columns)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("manifest={}".format(repr(self._manifest)))
        fields.append("error_message={}".format(repr(self._error_message)))
        fields.append("upload_status={}".format(repr(self._upload_status)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "DataFrame({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        columns: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._columns, Unset):
            columns = []
            for columns_item_data in self._columns:
                columns_item = columns_item_data.to_dict()

                columns.append(columns_item)

        id = self._id
        name = self._name
        manifest: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._manifest, Unset):
            manifest = []
            for manifest_item_data in self._manifest:
                manifest_item = manifest_item_data.to_dict()

                manifest.append(manifest_item)

        error_message = self._error_message
        upload_status: Union[Unset, int] = UNSET
        if not isinstance(self._upload_status, Unset):
            upload_status = self._upload_status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if columns is not UNSET:
            field_dict["columns"] = columns
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if manifest is not UNSET:
            field_dict["manifest"] = manifest
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message
        if upload_status is not UNSET:
            field_dict["uploadStatus"] = upload_status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_columns() -> Union[Unset, List[DataFrameColumnMetadata]]:
            columns = []
            _columns = d.pop("columns")
            for columns_item_data in _columns or []:
                columns_item = DataFrameColumnMetadata.from_dict(columns_item_data, strict=False)

                columns.append(columns_item)

            return columns

        try:
            columns = get_columns()
        except KeyError:
            if strict:
                raise
            columns = cast(Union[Unset, List[DataFrameColumnMetadata]], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        def get_manifest() -> Union[Unset, List[DataFrameManifestManifestItem]]:
            manifest = []
            _manifest = d.pop("manifest")
            for manifest_item_data in _manifest or []:
                manifest_item = DataFrameManifestManifestItem.from_dict(manifest_item_data, strict=False)

                manifest.append(manifest_item)

            return manifest

        try:
            manifest = get_manifest()
        except KeyError:
            if strict:
                raise
            manifest = cast(Union[Unset, List[DataFrameManifestManifestItem]], UNSET)

        def get_error_message() -> Union[Unset, None, str]:
            error_message = d.pop("errorMessage")
            return error_message

        try:
            error_message = get_error_message()
        except KeyError:
            if strict:
                raise
            error_message = cast(Union[Unset, None, str], UNSET)

        def get_upload_status() -> Union[Unset, FileStatusUploadStatus]:
            upload_status = UNSET
            _upload_status = d.pop("uploadStatus")
            if _upload_status is not None and _upload_status is not UNSET:
                try:
                    upload_status = FileStatusUploadStatus(_upload_status)
                except ValueError:
                    upload_status = FileStatusUploadStatus.of_unknown(_upload_status)

            return upload_status

        try:
            upload_status = get_upload_status()
        except KeyError:
            if strict:
                raise
            upload_status = cast(Union[Unset, FileStatusUploadStatus], UNSET)

        data_frame = cls(
            columns=columns,
            id=id,
            name=name,
            manifest=manifest,
            error_message=error_message,
            upload_status=upload_status,
        )

        data_frame.additional_properties = d
        return data_frame

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
    def columns(self) -> List[DataFrameColumnMetadata]:
        if isinstance(self._columns, Unset):
            raise NotPresentError(self, "columns")
        return self._columns

    @columns.setter
    def columns(self, value: List[DataFrameColumnMetadata]) -> None:
        self._columns = value

    @columns.deleter
    def columns(self) -> None:
        self._columns = UNSET

    @property
    def id(self) -> str:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def name(self) -> str:
        """ The user-facing name for this DataFrame. """
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
    def manifest(self) -> List[DataFrameManifestManifestItem]:
        if isinstance(self._manifest, Unset):
            raise NotPresentError(self, "manifest")
        return self._manifest

    @manifest.setter
    def manifest(self, value: List[DataFrameManifestManifestItem]) -> None:
        self._manifest = value

    @manifest.deleter
    def manifest(self) -> None:
        self._manifest = UNSET

    @property
    def error_message(self) -> Optional[str]:
        if isinstance(self._error_message, Unset):
            raise NotPresentError(self, "error_message")
        return self._error_message

    @error_message.setter
    def error_message(self, value: Optional[str]) -> None:
        self._error_message = value

    @error_message.deleter
    def error_message(self) -> None:
        self._error_message = UNSET

    @property
    def upload_status(self) -> FileStatusUploadStatus:
        if isinstance(self._upload_status, Unset):
            raise NotPresentError(self, "upload_status")
        return self._upload_status

    @upload_status.setter
    def upload_status(self, value: FileStatusUploadStatus) -> None:
        self._upload_status = value

    @upload_status.deleter
    def upload_status(self) -> None:
        self._upload_status = UNSET
