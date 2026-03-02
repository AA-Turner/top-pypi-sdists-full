from ocsf.events.discovery import Discovery

from ocsf.objects.actor import Actor
from ocsf.objects.user import User


class UserInventoryInfo(Discovery):
    """
    User Inventory Info events report user inventory data that is either logged or
    proactively collected. For example, when collecting user information from Active
    Directory entries.
    """

    class_uid: int = 5003
    class_name: str = 'User Inventory Info'

    user: User # The user that is being discovered by an inventory process.


    # Optional:
    actor: Actor | None = None # The actor describes the process that was the source of the inventory
                               # activity. In the case of user inventory data, that could be a
                               # particular process or script that is run to scrape the user data. For
                               # example, it could be a powershell process that runs to pull data from
                               # the Azure AD graph API.
