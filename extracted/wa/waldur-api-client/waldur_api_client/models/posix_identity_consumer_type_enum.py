from enum import Enum


class PosixIdentityConsumerTypeEnum(str, Enum):
    OFFERINGROLEGROUP = "offeringrolegroup"
    OFFERINGUSERGROUP = "offeringusergroup"
    ROBOTACCOUNT = "robotaccount"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
