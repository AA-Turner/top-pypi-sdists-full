from django.utils.translation import gettext as _

from wbcore.menus import ItemPermission, MenuItem

STARTSTEP_MENUITEM = MenuItem(
    label=_("Start Step"),
    endpoint="wbcore:workflow:startstep-list",
    permission=ItemPermission(
        method=lambda request: request.user.is_internal, permissions=["workflow.view_startstep"]
    ),
    add=MenuItem(
        label=_("Create Start Step"),
        endpoint="wbcore:workflow:startstep-list",
        permission=ItemPermission(
            method=lambda request: request.user.is_internal, permissions=["workflow.add_startstep"]
        ),
    ),
)

USERSTEP_MENUITEM = MenuItem(
    label=_("User Step"),
    endpoint="wbcore:workflow:userstep-list",
    permission=ItemPermission(method=lambda request: request.user.is_internal, permissions=["workflow.view_userstep"]),
    add=MenuItem(
        label=_("Create User Step"),
        endpoint="wbcore:workflow:userstep-list",
        permission=ItemPermission(
            method=lambda request: request.user.is_internal, permissions=["workflow.add_userstep"]
        ),
    ),
)

DECISIONSTEP_MENUITEM = MenuItem(
    label=_("Decision Step"),
    endpoint="wbcore:workflow:decisionstep-list",
    permission=ItemPermission(
        method=lambda request: request.user.is_internal, permissions=["workflow.view_decisionstep"]
    ),
    add=MenuItem(
        label=_("Create Decision Step"),
        endpoint="wbcore:workflow:decisionstep-list",
        permission=ItemPermission(
            method=lambda request: request.user.is_internal, permissions=["workflow.add_decisionstep"]
        ),
    ),
)

SPLITSTEP_MENUITEM = MenuItem(
    label=_("Split Step"),
    endpoint="wbcore:workflow:splitstep-list",
    permission=ItemPermission(
        method=lambda request: request.user.is_internal, permissions=["workflow.view_splitstep"]
    ),
    add=MenuItem(
        label=_("Create Split Step"),
        endpoint="wbcore:workflow:splitstep-list",
        permission=ItemPermission(
            method=lambda request: request.user.is_internal, permissions=["workflow.add_splitstep"]
        ),
    ),
)

JOINSTEP_MENUITEM = MenuItem(
    label=_("Join Step"),
    endpoint="wbcore:workflow:joinstep-list",
    permission=ItemPermission(method=lambda request: request.user.is_internal, permissions=["workflow.view_joinstep"]),
    add=MenuItem(
        label=_("Create Join Step"),
        endpoint="wbcore:workflow:joinstep-list",
        permission=ItemPermission(
            method=lambda request: request.user.is_internal, permissions=["workflow.add_joinstep"]
        ),
    ),
)

SCRIPTSTEP_MENUITEM = MenuItem(
    label=_("Script Step"),
    endpoint="wbcore:workflow:scriptstep-list",
    permission=ItemPermission(
        method=lambda request: request.user.is_internal, permissions=["workflow.view_scriptstep"]
    ),
    add=MenuItem(
        label=_("Create Script Step"),
        endpoint="wbcore:workflow:scriptstep-list",
        permission=ItemPermission(
            method=lambda request: request.user.is_internal, permissions=["workflow.add_scriptstep"]
        ),
    ),
)

EMAILSTEP_MENUITEM = MenuItem(
    label=_("Email Step"),
    endpoint="wbcore:workflow:emailstep-list",
    permission=ItemPermission(
        method=lambda request: request.user.is_internal, permissions=["workflow.view_emailstep"]
    ),
    add=MenuItem(
        label=_("Create Email Step"),
        endpoint="wbcore:workflow:emailstep-list",
        permission=ItemPermission(
            method=lambda request: request.user.is_internal, permissions=["workflow.add_emailstep"]
        ),
    ),
)

FINISHSTEP_MENUITEM = MenuItem(
    label=_("Finish Step"),
    endpoint="wbcore:workflow:finishstep-list",
    permission=ItemPermission(
        method=lambda request: request.user.is_internal, permissions=["workflow.view_finishstep"]
    ),
    add=MenuItem(
        label=_("Create Finish Step"),
        endpoint="wbcore:workflow:finishstep-list",
        permission=ItemPermission(
            method=lambda request: request.user.is_internal, permissions=["workflow.add_finishstep"]
        ),
    ),
)
