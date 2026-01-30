from django.utils.translation import gettext as _

from wbcore.menus import ItemPermission, MenuItem

YOUR_CONTACT_MENUITEM = MenuItem(
    label=_("Your Contact"),
    endpoint="wbcore:directory:clientmanagerrelationship-userclient-list",
    permission=ItemPermission(method=lambda request: request.user.is_active and not request.user.is_internal),
)

COMPANY_MENUITEM = MenuItem(
    label=_("Companies"),
    endpoint="wbcore:directory:company-list",
    permission=ItemPermission(permissions=["directory.view_company"]),
    add=MenuItem(
        label=_("Create Company"),
        endpoint="wbcore:directory:company-list",
        permission=ItemPermission(permissions=["directory.add_company"]),
    ),
)
PERSON_MENUITEM = MenuItem(
    label=_("Persons"),
    endpoint="wbcore:directory:person-list",
    permission=ItemPermission(permissions=["directory.view_person"]),
    add=MenuItem(
        label=_("Create Person"),
        endpoint="wbcore:directory:person-list",
        permission=ItemPermission(permissions=["directory.add_person"]),
    ),
)

SYSTEMEMPLOYEE_MENUITEM = MenuItem(
    label=_("Employees"),
    endpoint="wbcore:directory:systememployee-list",
    permission=ItemPermission(method=lambda request: request.user.is_internal, permissions=["directory.view_person"]),
)

BANK_MENUITEM = MenuItem(
    label=_("Banks"),
    endpoint="wbcore:directory:bank-list",
    permission=ItemPermission(method=lambda request: request.user.is_internal, permissions=["directory.view_bank"]),
    add=MenuItem(
        label=_("Create Bank"),
        endpoint="wbcore:directory:bank-list",
        permission=ItemPermission(method=lambda request: request.user.is_internal, permissions=["directory.add_bank"]),
    ),
)

USERISMANAGER_MENUITEM = MenuItem(
    label=_("Your Clients/Prospects/Contacts"),
    endpoint="wbcore:directory:clientmanagerrelationship-usermanager-list",
    permission=ItemPermission(method=lambda request: request.user.is_internal, permissions=["directory.view_person"]),
)
