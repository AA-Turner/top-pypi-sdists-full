from enum import Enum

from ._entity import Entity


class AccountTypeId(Enum):
    """
    The normalized account type identifier.
    """
    Other: int = 99 # The account type is not mapped.
    Unknown: int = 0 # The account type is unknown.
    Ldap_Account: int = 1
    Windows_Account: int = 2
    Aws_Iam_User: int = 3
    Aws_Iam_Role: int = 4
    Gcp_Account: int = 5
    Azure_Ad_Account: int = 6
    Mac_Os_Account: int = 7
    Apple_Account: int = 8
    Linux_Account: int = 9
    Aws_Account: int = 10

class Account(Entity):
    """
    The Account object contains details about the account that initiated or
    performed a specific activity within a system or application.
    """

    # Recommended:
    type_id: AccountTypeId | None = None # The normalized account type identifier.

    # Optional:
    name: str | None = None # The name of the account (e.g. GCP Account Name).
    type: str | None = None # The account type, normalized to the caption of 'account_type_id'. In the
                            # case of 'Other', it is defined by the event source.
    uid: str | None = None # The unique identifier of the account (e.g. AWS Account ID).
    labels: list[str] | None = None # The list of labels/tags associated to the account.
