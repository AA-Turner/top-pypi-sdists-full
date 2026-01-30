from django.utils.translation import gettext as _

from wbcore.menus import ItemPermission, MenuItem

POSITION_MENUITEM = MenuItem(
    label=_("Company Positions"),
    endpoint="wbcore:directory:position-list",
    permission=ItemPermission(
        method=lambda request: request.user.is_internal,
        permissions=["directory.view_position"],
    ),
    add=MenuItem(
        label=_("Create Position"),
        endpoint="wbcore:directory:position-list",
        permission=ItemPermission(
            method=lambda request: request.user.is_internal,
            permissions=["directory.add_position"],
        ),
    ),
)

CUSTOMERSTATUS_MENUITEM = MenuItem(
    label=_("Customer Statuses"),
    endpoint="wbcore:directory:customerstatus-list",
    permission=ItemPermission(
        method=lambda request: request.user.is_internal,
        permissions=["directory.view_customerstatus"],
    ),
    add=MenuItem(
        label=_("Create Customer Status"),
        endpoint="wbcore:directory:customerstatus-list",
        permission=ItemPermission(
            method=lambda request: request.user.is_internal,
            permissions=["directory.add_customerstatus"],
        ),
    ),
)

COMPANYTYPE_MENUITEM = MenuItem(
    label=_("Company Types"),
    endpoint="wbcore:directory:companytype-list",
    permission=ItemPermission(
        method=lambda request: request.user.is_internal,
        permissions=["directory.view_companytype"],
    ),
    add=MenuItem(
        label=_("Create Company Type"),
        endpoint="wbcore:directory:companytype-list",
        permission=ItemPermission(
            method=lambda request: request.user.is_internal,
            permissions=["directory.add_companytype"],
        ),
    ),
)


SPECIALIZATION_MENUITEM = MenuItem(
    label=_("Specializations"),
    endpoint="wbcore:directory:specialization-list",
    permission=ItemPermission(
        method=lambda request: request.user.is_internal,
        permissions=["directory.view_specialization"],
    ),
    add=MenuItem(
        label=_("Create Specialization"),
        endpoint="wbcore:directory:specialization-list",
        permission=ItemPermission(
            method=lambda request: request.user.is_internal,
            permissions=["directory.add_specialization"],
        ),
    ),
)
