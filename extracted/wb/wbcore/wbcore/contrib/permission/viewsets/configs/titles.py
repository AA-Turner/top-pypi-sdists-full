from typing import TYPE_CHECKING

from wbcore.metadata.configs.titles import TitleViewConfig

if TYPE_CHECKING:
    from wbcore.contrib.permission.viewsets import PivotUserObjectPermissionModelViewSet


class PivotUserObjectPermissionTitleViewConfig(TitleViewConfig):
    view: "PivotUserObjectPermissionModelViewSet"

    def get_list_title(self) -> str:
        return f"Permissions for {self.view.linked_object}"

    def get_create_title(self) -> str:
        return f"Add permissions for {self.view.linked_object}"
