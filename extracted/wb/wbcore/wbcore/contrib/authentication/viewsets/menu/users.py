from django.utils.translation import gettext as _

from wbcore.menus import ItemPermission, MenuItem

USER_MENUITEM = MenuItem(
    label=_("Users"),
    endpoint="wbcore:authentication:user-list",
    permission=ItemPermission(
        method=lambda request: request.user.is_internal, permissions=["authentication.view_user"]
    ),
    add=MenuItem(
        label=_("Create New User"),
        endpoint="wbcore:authentication:user-list",
        permission=ItemPermission(permissions=["authentication.add_user"]),
    ),
)
