from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.workspace_offboard_preview_preview import WorkspaceOffboardPreviewPreview


T = TypeVar("T", bound="WorkspaceOffboardPreview")


@_attrs_define
class WorkspaceOffboardPreview:
    """
    Attributes:
        workspace_id (str):
        username (str):
        preview (WorkspaceOffboardPreviewPreview):
    """

    workspace_id: str
    username: str
    preview: "WorkspaceOffboardPreviewPreview"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workspace_id = self.workspace_id
        username = self.username
        preview = self.preview.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workspace_id": workspace_id,
                "username": username,
                "preview": preview,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.workspace_offboard_preview_preview import WorkspaceOffboardPreviewPreview

        d = src_dict.copy()
        workspace_id = d.pop("workspace_id")

        username = d.pop("username")

        preview = WorkspaceOffboardPreviewPreview.from_dict(d.pop("preview"))

        workspace_offboard_preview = cls(
            workspace_id=workspace_id,
            username=username,
            preview=preview,
        )

        workspace_offboard_preview.additional_properties = d
        return workspace_offboard_preview

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
