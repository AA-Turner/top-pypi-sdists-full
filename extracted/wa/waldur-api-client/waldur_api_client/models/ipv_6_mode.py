from enum import Enum


class Ipv6Mode(str, Enum):
    DHCPV6_STATEFUL = "dhcpv6-stateful"
    DHCPV6_STATELESS = "dhcpv6-stateless"
    SLAAC = "slaac"

    def __str__(self) -> str:
        return str(self.value)
