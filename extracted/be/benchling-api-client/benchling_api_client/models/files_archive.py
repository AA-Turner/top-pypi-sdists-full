from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.files_archive_reason import FilesArchiveReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="FilesArchive")


@attr.s(auto_attribs=True, repr=False)
class FilesArchive:
    """The request body for archiving Files."""

    _file_ids: List[str]
    _reason: FilesArchiveReason

    def __repr__(self):
        fields = []
        fields.append("file_ids={}".format(repr(self._file_ids)))
        fields.append("reason={}".format(repr(self._reason)))
        return "FilesArchive({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        file_ids = self._file_ids

        reason = self._reason.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if file_ids is not UNSET:
            field_dict["fileIds"] = file_ids
        if reason is not UNSET:
            field_dict["reason"] = reason

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

        def get_reason() -> FilesArchiveReason:
            _reason = d.pop("reason")
            try:
                reason = FilesArchiveReason(_reason)
            except ValueError:
                reason = FilesArchiveReason.of_unknown(_reason)

            return reason

        try:
            reason = get_reason()
        except KeyError:
            if strict:
                raise
            reason = cast(FilesArchiveReason, UNSET)

        files_archive = cls(
            file_ids=file_ids,
            reason=reason,
        )

        return files_archive

    @property
    def file_ids(self) -> List[str]:
        if isinstance(self._file_ids, Unset):
            raise NotPresentError(self, "file_ids")
        return self._file_ids

    @file_ids.setter
    def file_ids(self, value: List[str]) -> None:
        self._file_ids = value

    @property
    def reason(self) -> FilesArchiveReason:
        """The reason for archiving the provided Files. Accepted reasons may differ based on tenant configuration."""
        if isinstance(self._reason, Unset):
            raise NotPresentError(self, "reason")
        return self._reason

    @reason.setter
    def reason(self, value: FilesArchiveReason) -> None:
        self._reason = value
