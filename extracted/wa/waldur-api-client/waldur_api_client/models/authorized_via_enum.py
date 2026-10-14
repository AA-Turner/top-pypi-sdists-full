from enum import Enum


class AuthorizedViaEnum(str, Enum):
    CUSTOMER_OWNER = "customer_owner"
    IDENTITY_MANAGER = "identity_manager"
    OFFERING_MANAGER = "offering_manager"
    SCOPE_ROLE = "scope_role"
    SELF = "self"
    STAFF = "staff"
    SUPPORT = "support"

    def __str__(self) -> str:
        return str(self.value)
