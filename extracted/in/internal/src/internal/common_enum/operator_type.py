from enum import Enum


class OperatorTypeEnum(str, Enum):
    SYSTEM = "system"
    USER = "user"
    CUSTOMER = "customer"
    PROVIDER = "provider"
    CLIENT = "client"
