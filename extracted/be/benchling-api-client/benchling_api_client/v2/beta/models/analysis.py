from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="Analysis")


@attr.s(auto_attribs=True, repr=False)
class Analysis:
    """  """

    _data_frame_ids: Union[Unset, List[str]] = UNSET
    _file_ids: Union[Unset, List[str]] = UNSET
    _folder_id: Union[Unset, str] = UNSET
    _id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("data_frame_ids={}".format(repr(self._data_frame_ids)))
        fields.append("file_ids={}".format(repr(self._file_ids)))
        fields.append("folder_id={}".format(repr(self._folder_id)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "Analysis({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        data_frame_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._data_frame_ids, Unset):
            data_frame_ids = self._data_frame_ids

        file_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._file_ids, Unset):
            file_ids = self._file_ids

        folder_id = self._folder_id
        id = self._id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if data_frame_ids is not UNSET:
            field_dict["dataFrameIds"] = data_frame_ids
        if file_ids is not UNSET:
            field_dict["fileIds"] = file_ids
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_data_frame_ids() -> Union[Unset, List[str]]:
            data_frame_ids = cast(List[str], d.pop("dataFrameIds"))

            return data_frame_ids

        try:
            data_frame_ids = get_data_frame_ids()
        except KeyError:
            if strict:
                raise
            data_frame_ids = cast(Union[Unset, List[str]], UNSET)

        def get_file_ids() -> Union[Unset, List[str]]:
            file_ids = cast(List[str], d.pop("fileIds"))

            return file_ids

        try:
            file_ids = get_file_ids()
        except KeyError:
            if strict:
                raise
            file_ids = cast(Union[Unset, List[str]], UNSET)

        def get_folder_id() -> Union[Unset, str]:
            folder_id = d.pop("folderId")
            return folder_id

        try:
            folder_id = get_folder_id()
        except KeyError:
            if strict:
                raise
            folder_id = cast(Union[Unset, str], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        analysis = cls(
            data_frame_ids=data_frame_ids,
            file_ids=file_ids,
            folder_id=folder_id,
            id=id,
        )

        analysis.additional_properties = d
        return analysis

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
    def data_frame_ids(self) -> List[str]:
        if isinstance(self._data_frame_ids, Unset):
            raise NotPresentError(self, "data_frame_ids")
        return self._data_frame_ids

    @data_frame_ids.setter
    def data_frame_ids(self, value: List[str]) -> None:
        self._data_frame_ids = value

    @data_frame_ids.deleter
    def data_frame_ids(self) -> None:
        self._data_frame_ids = UNSET

    @property
    def file_ids(self) -> List[str]:
        if isinstance(self._file_ids, Unset):
            raise NotPresentError(self, "file_ids")
        return self._file_ids

    @file_ids.setter
    def file_ids(self, value: List[str]) -> None:
        self._file_ids = value

    @file_ids.deleter
    def file_ids(self) -> None:
        self._file_ids = UNSET

    @property
    def folder_id(self) -> str:
        """ ID of the folder that contains the analysis """
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
