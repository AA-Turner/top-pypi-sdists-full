from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExportAuditLogAsyncTaskResponse")


@attr.s(auto_attribs=True, repr=False)
class ExportAuditLogAsyncTaskResponse:
    """  """

    _download_url: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("download_url={}".format(repr(self._download_url)))
        return "ExportAuditLogAsyncTaskResponse({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        download_url = self._download_url

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if download_url is not UNSET:
            field_dict["downloadURL"] = download_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_download_url() -> Union[Unset, str]:
            download_url = d.pop("downloadURL")
            return download_url

        try:
            download_url = get_download_url()
        except KeyError:
            if strict:
                raise
            download_url = cast(Union[Unset, str], UNSET)

        export_audit_log_async_task_response = cls(
            download_url=download_url,
        )

        return export_audit_log_async_task_response

    @property
    def download_url(self) -> str:
        if isinstance(self._download_url, Unset):
            raise NotPresentError(self, "download_url")
        return self._download_url

    @download_url.setter
    def download_url(self, value: str) -> None:
        self._download_url = value

    @download_url.deleter
    def download_url(self) -> None:
        self._download_url = UNSET
