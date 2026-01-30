from django.utils.translation import gettext as _

from wbcore.menus import ItemPermission, MenuItem

CONDITION_MENUITEM = MenuItem(
    label=_("Condition"),
    endpoint="wbcore:workflow:condition-list",
    permission=ItemPermission(
        method=lambda request: request.user.is_internal, permissions=["workflow.view_condition"]
    ),
    add=MenuItem(
        label=_("Create Condition"),
        endpoint="wbcore:workflow:condition-list",
        permission=ItemPermission(
            method=lambda request: request.user.is_internal, permissions=["workflow.add_condition"]
        ),
    ),
)
