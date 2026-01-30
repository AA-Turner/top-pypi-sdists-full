from django.utils.translation import gettext as _

from wbcore.menus import ItemPermission, MenuItem

WORKFLOW_MENUITEM = MenuItem(
    label=_("Workflow"),
    endpoint="wbcore:workflow:workflow-list",
    permission=ItemPermission(method=lambda request: request.user.is_internal, permissions=["workflow.view_workflow"]),
    add=MenuItem(
        label=_("Create Workflow"),
        endpoint="wbcore:workflow:workflow-list",
        permission=ItemPermission(
            method=lambda request: request.user.is_internal, permissions=["workflow.add_workflow"]
        ),
    ),
)
