from enum import Enum

from ocsf.events.iam import IAM

from ocsf.objects.actor import Actor
from ocsf.objects.policy import Policy
from ocsf.objects.user import User


class AccountChangeActivityId(Enum):
    Create: int = 1 # A user/role was created.
    Enable: int = 2 # A user/role was enabled.
    Password_Change: int = 3 # An attempt was made to change an account's password.
    Password_Reset: int = 4 # An attempt was made to reset an account's password.
    Disable: int = 5 # A user/role was disabled.
    Delete: int = 6 # A user/role was deleted.
    Attach_Policy: int = 7 # An IAM Policy was attached to a user/role.
    Detach_Policy: int = 8 # An IAM Policy was detached from a user/role.
    Lock: int = 9 # A user account was locked out.
    Mfa_Factor_Enable: int = 10 # An authentication factor was enabled for an account.
    Mfa_Factor_Disable: int = 11 # An authentication factor was disabled for an account.


class AccountChange(IAM):
    """
    Account Change events report when specific user account management tasks are
    performed, such as a user/role being created, changed, deleted, renamed,
    disabled, enabled, locked out or unlocked.
    """

    class_uid = 3001
    class_name = 'Account Change'

    user: User # The user that was a target of an activity.

    # Recommended:
    actor: Actor | None = None
    user_result: User | None = None

    # Optional:
    activity_id: AccountChangeActivityId | None = None
    policy: Policy | None = None # Details about the IAM policy associated to the Attach/Detach Policy
                                 # activities.
