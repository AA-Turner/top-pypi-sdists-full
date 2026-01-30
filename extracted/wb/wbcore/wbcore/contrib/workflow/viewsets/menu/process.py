from django.utils.translation import gettext as _

from wbcore.menus import ItemPermission, MenuItem

PROCESS_MENUITEM = MenuItem(
    label=_("Process"),
    endpoint="wbcore:workflow:process-list",
    permission=ItemPermission(method=lambda request: request.user.is_internal, permissions=["workflow.view_process"]),
)
PROCESSSTEP_MENUITEM = MenuItem(
    label=_("Process Step"),
    endpoint="wbcore:workflow:processstep-list",
    permission=ItemPermission(
        method=lambda request: request.user.is_internal, permissions=["workflow.view_processstep"]
    ),
)
