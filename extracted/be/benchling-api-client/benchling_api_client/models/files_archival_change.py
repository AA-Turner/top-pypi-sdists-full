from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="FilesArchivalChange")


@attr.s(auto_attribs=True, repr=False)
class FilesArchivalChange:
    """IDs of all items that were archived or unarchived, grouped by resource type."""

    _file_ids: Union[Unset, List[str]] = UNSET

    def __repr__(self):
        fields = []
        fields.append("file_ids={}".format(repr(self._file_ids)))
        return "FilesArchivalChange({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        file_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._file_ids, Unset):
            file_ids = self._file_ids

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if file_ids is not UNSET:
            field_dict["fileIds"] = file_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_file_ids() -> Union[Unset, List[str]]:
            file_ids = cast(List[str], d.pop("fileIds"))

            return file_ids

        try:
            file_ids = get_file_ids()
        except KeyError:
            if strict:
                raise
            file_ids = cast(Union[Unset, List[str]], UNSET)

        files_archival_change = cls(
            file_ids=file_ids,
        )

        return files_archival_change

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
