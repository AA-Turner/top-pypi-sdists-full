from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.custom_fields import CustomFields
from ..models.file_update_upload_status import FileUpdateUploadStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="FileUpdate")


@attr.s(auto_attribs=True, repr=False)
class FileUpdate:
    """  """

    _custom_fields: Union[Unset, CustomFields] = UNSET
    _error_message: Union[Unset, str] = UNSET
    _folder_id: Union[Unset, str] = UNSET
    _upload_status: Union[Unset, FileUpdateUploadStatus] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("custom_fields={}".format(repr(self._custom_fields)))
        fields.append("error_message={}".format(repr(self._error_message)))
        fields.append("folder_id={}".format(repr(self._folder_id)))
        fields.append("upload_status={}".format(repr(self._upload_status)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "FileUpdate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        custom_fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._custom_fields, Unset):
            custom_fields = self._custom_fields.to_dict()

        error_message = self._error_message
        folder_id = self._folder_id
        upload_status: Union[Unset, int] = UNSET
        if not isinstance(self._upload_status, Unset):
            upload_status = self._upload_status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if custom_fields is not UNSET:
            field_dict["customFields"] = custom_fields
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if upload_status is not UNSET:
            field_dict["uploadStatus"] = upload_status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_custom_fields() -> Union[Unset, CustomFields]:
            custom_fields: Union[Unset, Union[Unset, CustomFields]] = UNSET
            _custom_fields = d.pop("customFields")

            if not isinstance(_custom_fields, Unset):
                custom_fields = CustomFields.from_dict(_custom_fields)

            return custom_fields

        try:
            custom_fields = get_custom_fields()
        except KeyError:
            if strict:
                raise
            custom_fields = cast(Union[Unset, CustomFields], UNSET)

        def get_error_message() -> Union[Unset, str]:
            error_message = d.pop("errorMessage")
            return error_message

        try:
            error_message = get_error_message()
        except KeyError:
            if strict:
                raise
            error_message = cast(Union[Unset, str], UNSET)

        def get_folder_id() -> Union[Unset, str]:
            folder_id = d.pop("folderId")
            return folder_id

        try:
            folder_id = get_folder_id()
        except KeyError:
            if strict:
                raise
            folder_id = cast(Union[Unset, str], UNSET)

        def get_upload_status() -> Union[Unset, FileUpdateUploadStatus]:
            upload_status = UNSET
            _upload_status = d.pop("uploadStatus")
            if _upload_status is not None and _upload_status is not UNSET:
                try:
                    upload_status = FileUpdateUploadStatus(_upload_status)
                except ValueError:
                    upload_status = FileUpdateUploadStatus.of_unknown(_upload_status)

            return upload_status

        try:
            upload_status = get_upload_status()
        except KeyError:
            if strict:
                raise
            upload_status = cast(Union[Unset, FileUpdateUploadStatus], UNSET)

        file_update = cls(
            custom_fields=custom_fields,
            error_message=error_message,
            folder_id=folder_id,
            upload_status=upload_status,
        )

        file_update.additional_properties = d
        return file_update

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
    def custom_fields(self) -> CustomFields:
        if isinstance(self._custom_fields, Unset):
            raise NotPresentError(self, "custom_fields")
        return self._custom_fields

    @custom_fields.setter
    def custom_fields(self, value: CustomFields) -> None:
        self._custom_fields = value

    @custom_fields.deleter
    def custom_fields(self) -> None:
        self._custom_fields = UNSET

    @property
    def error_message(self) -> str:
        """ Error message for the file upload """
        if isinstance(self._error_message, Unset):
            raise NotPresentError(self, "error_message")
        return self._error_message

    @error_message.setter
    def error_message(self, value: str) -> None:
        self._error_message = value

    @error_message.deleter
    def error_message(self) -> None:
        self._error_message = UNSET

    @property
    def folder_id(self) -> str:
        """ ID of the folder that the file is moved into """
        if isinstance(self._folder_id, Unset):
            raise NotPresentError(self, "folder_id")
        return self._folder_id

    @folder_id.setter
    def folder_id(self, value: str) -> None:
        self._folder_id = value

    @folder_id.deleter
    def folder_id(self) -> None:
        self._folder_id = UNSET

    @property
    def upload_status(self) -> FileUpdateUploadStatus:
        if isinstance(self._upload_status, Unset):
            raise NotPresentError(self, "upload_status")
        return self._upload_status

    @upload_status.setter
    def upload_status(self, value: FileUpdateUploadStatus) -> None:
        self._upload_status = value

    @upload_status.deleter
    def upload_status(self) -> None:
        self._upload_status = UNSET
