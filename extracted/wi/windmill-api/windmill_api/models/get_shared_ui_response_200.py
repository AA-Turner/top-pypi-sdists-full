import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.get_shared_ui_response_200_files import GetSharedUiResponse200Files


T = TypeVar("T", bound="GetSharedUiResponse200")


@_attrs_define
class GetSharedUiResponse200:
    """
    Attributes:
        files (GetSharedUiResponse200Files):
        version (int):
        edited_at (datetime.datetime):
        edited_by (str):
    """

    files: "GetSharedUiResponse200Files"
    version: int
    edited_at: datetime.datetime
    edited_by: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        files = self.files.to_dict()

        version = self.version
        edited_at = self.edited_at.isoformat()

        edited_by = self.edited_by

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "files": files,
                "version": version,
                "edited_at": edited_at,
                "edited_by": edited_by,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_shared_ui_response_200_files import GetSharedUiResponse200Files

        d = src_dict.copy()
        files = GetSharedUiResponse200Files.from_dict(d.pop("files"))

        version = d.pop("version")

        edited_at = isoparse(d.pop("edited_at"))

        edited_by = d.pop("edited_by")

        get_shared_ui_response_200 = cls(
            files=files,
            version=version,
            edited_at=edited_at,
            edited_by=edited_by,
        )

        get_shared_ui_response_200.additional_properties = d
        return get_shared_ui_response_200

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
