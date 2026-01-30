from django.utils.translation import gettext as _

from wbcore.menus import ItemPermission, MenuItem

BUILDING_MENUITEM = MenuItem(
    label=_("Buildings"),
    endpoint="wbcore:agenda:building-list",
    permission=ItemPermission(
        method=lambda request: request.user.is_internal,
        permissions=["agenda.view_building"],
    ),
    add=MenuItem(
        label=_("Create Building"),
        endpoint="wbcore:agenda:building-list",
        permission=ItemPermission(
            method=lambda request: request.user.is_internal,
            permissions=["agenda.add_building"],
        ),
    ),
)

CONFERENCE_ROOM_MENUITEM = MenuItem(
    label=_("Conference Rooms"),
    endpoint="wbcore:agenda:conferenceroom-list",
    permission=ItemPermission(
        method=lambda request: request.user.is_internal,
        permissions=["agenda.view_conferenceroom"],
    ),
    add=MenuItem(
        label=_("Create Conference Room"),
        endpoint="wbcore:agenda:conferenceroom-list",
        permission=ItemPermission(
            method=lambda request: request.user.is_internal,
            permissions=["agenda.add_conferenceroom"],
        ),
    ),
)
