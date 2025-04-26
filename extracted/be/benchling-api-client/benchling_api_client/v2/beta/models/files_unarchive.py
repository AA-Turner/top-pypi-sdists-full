from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="FilesUnarchive")


@attr.s(auto_attribs=True, repr=False)
class FilesUnarchive:
    """The request body for unarchiving Files."""

    _file_ids: List[str]

    def __repr__(self):
        fields = []
        fields.append("file_ids={}".format(repr(self._file_ids)))
        return "FilesUnarchive({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        file_ids = self._file_ids

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if file_ids is not UNSET:
            field_dict["fileIds"] = file_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_file_ids() -> List[str]:
            file_ids = cast(List[str], d.pop("fileIds"))

            return file_ids

        try:
            file_ids = get_file_ids()
        except KeyError:
            if strict:
                raise
            file_ids = cast(List[str], UNSET)

        files_unarchive = cls(
            file_ids=file_ids,
        )

        return files_unarchive

    @property
    def file_ids(self) -> List[str]:
        if isinstance(self._file_ids, Unset):
            raise NotPresentError(self, "file_ids")
        return self._file_ids

    @file_ids.setter
    def file_ids(self, value: List[str]) -> None:
        self._file_ids = value
