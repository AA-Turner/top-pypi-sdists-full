from enum import Enum

class AccountStatus(str, Enum):
    Pending = "pending",
    Connected = "connected",
    Needs_reauth = "needs_reauth",

