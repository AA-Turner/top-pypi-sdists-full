from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.data_frame_update_upload_status import DataFrameUpdateUploadStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="DataFrameUpdate")


@attr.s(auto_attribs=True, repr=False)
class DataFrameUpdate:
    """  """

    _upload_status: Union[Unset, DataFrameUpdateUploadStatus] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("upload_status={}".format(repr(self._upload_status)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "DataFrameUpdate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        upload_status: Union[Unset, int] = UNSET
        if not isinstance(self._upload_status, Unset):
            upload_status = self._upload_status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if upload_status is not UNSET:
            field_dict["uploadStatus"] = upload_status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_upload_status() -> Union[Unset, DataFrameUpdateUploadStatus]:
            upload_status = UNSET
            _upload_status = d.pop("uploadStatus")
            if _upload_status is not None and _upload_status is not UNSET:
                try:
                    upload_status = DataFrameUpdateUploadStatus(_upload_status)
                except ValueError:
                    upload_status = DataFrameUpdateUploadStatus.of_unknown(_upload_status)

            return upload_status

        try:
            upload_status = get_upload_status()
        except KeyError:
            if strict:
                raise
            upload_status = cast(Union[Unset, DataFrameUpdateUploadStatus], UNSET)

        data_frame_update = cls(
            upload_status=upload_status,
        )

        data_frame_update.additional_properties = d
        return data_frame_update

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
    def upload_status(self) -> DataFrameUpdateUploadStatus:
        if isinstance(self._upload_status, Unset):
            raise NotPresentError(self, "upload_status")
        return self._upload_status

    @upload_status.setter
    def upload_status(self, value: DataFrameUpdateUploadStatus) -> None:
        self._upload_status = value

    @upload_status.deleter
    def upload_status(self) -> None:
        self._upload_status = UNSET
