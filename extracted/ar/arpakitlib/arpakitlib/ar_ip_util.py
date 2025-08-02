# arpakit

import ipaddress

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def is_ipv4_address(value: str) -> bool:
    try:
        ipaddress.IPv4Address(value)
    except ValueError:
        return False
    return True


def raise_if_not_ipv4_address(value: str):
    if not is_ipv4_address(value):
        raise ValueError(f"not is_ipv4_address({value})")


def is_ipv6_address(value: str) -> bool:
    try:
        ipaddress.IPv6Address(value)
    except ValueError:
        return False
    return True


def raise_if_not_ipv6_address(value: str):
    if not is_ipv6_address(value):
        raise ValueError(f"not is_ipv6_address({value})")


def is_ipv4_interface(value: str) -> bool:
    try:
        ipaddress.IPv4Interface(value)
    except ValueError:
        return False
    return True


def raise_if_not_ipv4_interface(value: str):
    if not is_ipv4_interface(value):
        raise ValueError(f"not is_ipv4_interface({value})")


def __example():
    pass


if __name__ == '__main__':
    __example()
