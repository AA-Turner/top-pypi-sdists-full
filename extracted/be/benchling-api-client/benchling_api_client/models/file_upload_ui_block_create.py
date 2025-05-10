from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.file_upload_ui_block_type import FileUploadUiBlockType
from ..types import UNSET, Unset

T = TypeVar("T", bound="FileUploadUiBlockCreate")


@attr.s(auto_attribs=True, repr=False)
class FileUploadUiBlockCreate:
    """  """

    _id: str
    _file_types: Union[Unset, List[str]] = UNSET
    _max_files: Union[Unset, int] = 10
    _type: Union[Unset, FileUploadUiBlockType] = UNSET
    _label: Union[Unset, None, str] = UNSET
    _required: Union[Unset, None, bool] = UNSET
    _value: Union[Unset, None, List[str]] = UNSET
    _enabled: Union[Unset, None, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("file_types={}".format(repr(self._file_types)))
        fields.append("max_files={}".format(repr(self._max_files)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("label={}".format(repr(self._label)))
        fields.append("required={}".format(repr(self._required)))
        fields.append("value={}".format(repr(self._value)))
        fields.append("enabled={}".format(repr(self._enabled)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "FileUploadUiBlockCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        file_types: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._file_types, Unset):
            file_types = self._file_types

        max_files = self._max_files
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        label = self._label
        required = self._required
        value: Union[Unset, None, List[Any]] = UNSET
        if not isinstance(self._value, Unset):
            if self._value is None:
                value = None
            else:
                value = self._value

        enabled = self._enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id
        if file_types is not UNSET:
            field_dict["fileTypes"] = file_types
        if max_files is not UNSET:
            field_dict["maxFiles"] = max_files
        if type is not UNSET:
            field_dict["type"] = type
        if label is not UNSET:
            field_dict["label"] = label
        if required is not UNSET:
            field_dict["required"] = required
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

        def get_file_types() -> Union[Unset, List[str]]:
            file_types = cast(List[str], d.pop("fileTypes"))

            return file_types

        try:
            file_types = get_file_types()
        except KeyError:
            if strict:
                raise
            file_types = cast(Union[Unset, List[str]], UNSET)

        def get_max_files() -> Union[Unset, int]:
            max_files = d.pop("maxFiles")
            return max_files

        try:
            max_files = get_max_files()
        except KeyError:
            if strict:
                raise
            max_files = cast(Union[Unset, int], UNSET)

        def get_type() -> Union[Unset, FileUploadUiBlockType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = FileUploadUiBlockType(_type)
                except ValueError:
                    type = FileUploadUiBlockType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, FileUploadUiBlockType], UNSET)

        def get_label() -> Union[Unset, None, str]:
            label = d.pop("label")
            return label

        try:
            label = get_label()
        except KeyError:
            if strict:
                raise
            label = cast(Union[Unset, None, str], UNSET)

        def get_required() -> Union[Unset, None, bool]:
            required = d.pop("required")
            return required

        try:
            required = get_required()
        except KeyError:
            if strict:
                raise
            required = cast(Union[Unset, None, bool], UNSET)

        def get_value() -> Union[Unset, None, List[str]]:
            value = cast(List[str], d.pop("value"))

            return value

        try:
            value = get_value()
        except KeyError:
            if strict:
                raise
            value = cast(Union[Unset, None, List[str]], UNSET)

        def get_enabled() -> Union[Unset, None, bool]:
            enabled = d.pop("enabled")
            return enabled

        try:
            enabled = get_enabled()
        except KeyError:
            if strict:
                raise
            enabled = cast(Union[Unset, None, bool], UNSET)

        file_upload_ui_block_create = cls(
            id=id,
            file_types=file_types,
            max_files=max_files,
            type=type,
            label=label,
            required=required,
            value=value,
            enabled=enabled,
        )

        file_upload_ui_block_create.additional_properties = d
        return file_upload_ui_block_create

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
    def file_types(self) -> List[str]:
        if isinstance(self._file_types, Unset):
            raise NotPresentError(self, "file_types")
        return self._file_types

    @file_types.setter
    def file_types(self, value: List[str]) -> None:
        self._file_types = value

    @file_types.deleter
    def file_types(self) -> None:
        self._file_types = UNSET

    @property
    def max_files(self) -> int:
        if isinstance(self._max_files, Unset):
            raise NotPresentError(self, "max_files")
        return self._max_files

    @max_files.setter
    def max_files(self, value: int) -> None:
        self._max_files = value

    @max_files.deleter
    def max_files(self) -> None:
        self._max_files = UNSET

    @property
    def type(self) -> FileUploadUiBlockType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: FileUploadUiBlockType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET

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
    def required(self) -> Optional[bool]:
        """When true, the user must provide a value before the app can proceed. Block must specify a label if required is set to true."""
        if isinstance(self._required, Unset):
            raise NotPresentError(self, "required")
        return self._required

    @required.setter
    def required(self, value: Optional[bool]) -> None:
        self._required = value

    @required.deleter
    def required(self) -> None:
        self._required = UNSET

    @property
    def value(self) -> Optional[List[str]]:
        if isinstance(self._value, Unset):
            raise NotPresentError(self, "value")
        return self._value

    @value.setter
    def value(self, value: Optional[List[str]]) -> None:
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
