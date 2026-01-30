from django.utils.translation import gettext as _

from wbcore.menus import ItemPermission, MenuItem

DATA_MENUITEM = MenuItem(
    label=_("Data"),
    endpoint="wbcore:workflow:data-list",
    permission=ItemPermission(method=lambda request: request.user.is_internal, permissions=["workflow.view_data"]),
    add=MenuItem(
        label=_("Create Data"),
        endpoint="wbcore:workflow:data-list",
        permission=ItemPermission(method=lambda request: request.user.is_internal, permissions=["workflow.add_data"]),
    ),
)
