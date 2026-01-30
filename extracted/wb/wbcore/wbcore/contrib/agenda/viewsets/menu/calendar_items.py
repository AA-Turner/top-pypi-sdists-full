from django.utils.translation import gettext as _

from wbcore.menus import ItemPermission, MenuItem

CALENDAR_MENUITEM = MenuItem(
    label=_("Calendar"),
    endpoint="wbcore:agenda:calendaritem-list",
    permission=ItemPermission(
        method=lambda request: request.user.is_internal, permissions=["agenda.view_calendaritem"]
    ),
)
