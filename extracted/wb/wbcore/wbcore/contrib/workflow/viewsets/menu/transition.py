from django.utils.translation import gettext as _

from wbcore.menus import ItemPermission, MenuItem

TRANSITION_MENUITEM = MenuItem(
    label=_("Transition"),
    endpoint="wbcore:workflow:transition-list",
    permission=ItemPermission(
        method=lambda request: request.user.is_internal, permissions=["workflow.view_transition"]
    ),
    add=MenuItem(
        label=_("Create Transition"),
        endpoint="wbcore:workflow:transition-list",
        permission=ItemPermission(
            method=lambda request: request.user.is_internal, permissions=["workflow.add_transition"]
        ),
    ),
)
