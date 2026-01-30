from django.utils.translation import gettext as _

from wbcore.menus import ItemPermission, MenuItem

USER_ACTIVITY_MENUITEM = MenuItem(
    label=_("User Activity"),
    endpoint="wbcore:authentication:useractivity-list",
    permission=ItemPermission(
        method=lambda request: request.user.is_internal,
        permissions=[
            "authentication.view_user",
            "authentication.add_user",
            "authentication.delete_user",
            "authentication.change_user",
        ],
    ),
)
USER_ACTIVITY_TABLE_MENUITEM = MenuItem(
    label=_("User Activity Table"),
    endpoint="wbcore:authentication:useractivitytable-list",
    permission=ItemPermission(
        method=lambda request: request.user.is_internal,
        permissions=[
            "authentication.view_user",
            "authentication.add_user",
            "authentication.delete_user",
            "authentication.change_user",
        ],
    ),
)
USER_ACTIVITY_CHART_MENUITEM = MenuItem(
    label=_("User Activity Chart"),
    endpoint="wbcore:authentication:useractivitychart-list",
    permission=ItemPermission(
        method=lambda request: request.user.is_internal,
        permissions=[
            "authentication.view_user",
            "authentication.add_user",
            "authentication.delete_user",
            "authentication.change_user",
        ],
    ),
)
