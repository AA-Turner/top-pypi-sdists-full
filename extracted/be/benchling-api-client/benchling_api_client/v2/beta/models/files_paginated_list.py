from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.file import File
from ..types import UNSET, Unset

T = TypeVar("T", bound="FilesPaginatedList")


@attr.s(auto_attribs=True, repr=False)
class FilesPaginatedList:
    """  """

    _files: Union[Unset, List[File]] = UNSET
    _next_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("files={}".format(repr(self._files)))
        fields.append("next_token={}".format(repr(self._next_token)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "FilesPaginatedList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        files: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._files, Unset):
            files = []
            for files_item_data in self._files:
                files_item = files_item_data.to_dict()

                files.append(files_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if files is not UNSET:
            field_dict["files"] = files
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_files() -> Union[Unset, List[File]]:
            files = []
            _files = d.pop("files")
            for files_item_data in _files or []:
                files_item = File.from_dict(files_item_data, strict=False)

                files.append(files_item)

            return files

        try:
            files = get_files()
        except KeyError:
            if strict:
                raise
            files = cast(Union[Unset, List[File]], UNSET)

        def get_next_token() -> Union[Unset, str]:
            next_token = d.pop("nextToken")
            return next_token

        try:
            next_token = get_next_token()
        except KeyError:
            if strict:
                raise
            next_token = cast(Union[Unset, str], UNSET)

        files_paginated_list = cls(
            files=files,
            next_token=next_token,
        )

        files_paginated_list.additional_properties = d
        return files_paginated_list

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
    def files(self) -> List[File]:
        if isinstance(self._files, Unset):
            raise NotPresentError(self, "files")
        return self._files

    @files.setter
    def files(self, value: List[File]) -> None:
        self._files = value

    @files.deleter
    def files(self) -> None:
        self._files = UNSET

    @property
    def next_token(self) -> str:
        if isinstance(self._next_token, Unset):
            raise NotPresentError(self, "next_token")
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @next_token.deleter
    def next_token(self) -> None:
        self._next_token = UNSET
