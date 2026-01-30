from django.utils.translation import gettext as _

from wbcore.menus import ItemPermission, MenuItem

RELATIONSHIPTYPE_MENUITEM = MenuItem(
    label=_("Relationship Types"),
    endpoint="wbcore:directory:relationship-type-list",
    permission=ItemPermission(
        method=lambda request: request.user.is_internal,
        permissions=["directory.view_relationshiptype"],
    ),
    add=MenuItem(
        label=_("Create Relationship Type"),
        endpoint="wbcore:directory:relationship-type-list",
        permission=ItemPermission(
            method=lambda request: request.user.is_internal,
            permissions=["directory.add_relationshiptype"],
        ),
    ),
)

CLIENTMANAGER_MENUITEM = MenuItem(
    label=_("Client Manager Relationships"),
    endpoint="wbcore:directory:clientmanagerrelationship-list",
    permission=ItemPermission(permissions=["directory.view_clientmanagerrelationship"]),
    add=MenuItem(
        label=_("Create Client Manager Relationship"),
        endpoint="wbcore:directory:clientmanagerrelationship-list",
        permission=ItemPermission(permissions=["directory.add_clientmanagerrelationship"]),
    ),
)
