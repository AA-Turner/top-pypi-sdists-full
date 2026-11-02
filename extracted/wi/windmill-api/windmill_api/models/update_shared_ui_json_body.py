from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.update_shared_ui_json_body_files import UpdateSharedUiJsonBodyFiles


T = TypeVar("T", bound="UpdateSharedUiJsonBody")


@_attrs_define
class UpdateSharedUiJsonBody:
    """
    Attributes:
        files (UpdateSharedUiJsonBodyFiles):
    """

    files: "UpdateSharedUiJsonBodyFiles"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        files = self.files.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "files": files,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_shared_ui_json_body_files import UpdateSharedUiJsonBodyFiles

        d = src_dict.copy()
        files = UpdateSharedUiJsonBodyFiles.from_dict(d.pop("files"))

        update_shared_ui_json_body = cls(
            files=files,
        )

        update_shared_ui_json_body.additional_properties = d
        return update_shared_ui_json_body

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
