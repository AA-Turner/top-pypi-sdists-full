from enum import Enum


class CustomersUsersListOrganizationRoleItemType0(str, Enum):
    CUSTOMER_MANAGER = "CUSTOMER.MANAGER"
    CUSTOMER_OWNER = "CUSTOMER.OWNER"
    CUSTOMER_SUPPORT = "CUSTOMER.SUPPORT"

    def __str__(self) -> str:
        return str(self.value)
