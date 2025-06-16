from enum import Enum


class ContactTypeEnum(str, Enum):
    OWNER = "owner"
    DRIVER = "driver"
    BUYER = "buyer"
    CLIENT = "client"
