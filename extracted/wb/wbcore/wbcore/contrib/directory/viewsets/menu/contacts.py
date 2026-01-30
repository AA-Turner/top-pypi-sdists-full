from django.utils.translation import gettext as _

from wbcore.contrib.directory.models import BankingContact
from wbcore.menus import ItemPermission, MenuItem

PENDING_BANKINGCONTACT_MENUITEM = MenuItem(
    label=_("Pending Banking Contacts"),
    endpoint="wbcore:directory:bankingcontact-list",
    endpoint_get_parameters={"status": BankingContact.Status.PENDING.value},
    permission=ItemPermission(
        method=lambda request: request.user.is_internal,
        permissions=[
            "directory.view_bankingcontact",
            "directory.administrate_banking_contact",
        ],
    ),
)

TELEPHONECONTACTSEARCH_MENUITEM = MenuItem(
    label=_("Search by Telephone Contact"),
    endpoint="wbcore:directory:telephonecontact-list",
    permission=ItemPermission(
        method=lambda request: request.user.is_internal, permissions=["directory.view_telephonecontact"]
    ),
)
