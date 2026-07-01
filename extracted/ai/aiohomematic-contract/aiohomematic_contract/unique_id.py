# SPDX-License-Identifier: MIT
# Copyright (c) 2021-2026
"""
Reference implementation of the ``unique_id`` routing-key format.

The ``unique_id`` is the routing key for every Home Assistant value-change
subscription. ``aiohomematic`` derives it from device/channel addresses, and
``py-openccu-loom-client`` rebuilds it independently. The two MUST produce
**bit-identical** output, otherwise events route to the wrong (or no) entity.

This module is the algorithm-of-record. It is intentionally dependency-free
(constants are inlined, no I/O) so any backend can copy or import it. The
canonical contract is the golden fixture in ``data/unique_id_golden.json``;
this implementation is validated against that fixture by the package tests.

Format rules:

- ``:`` (address separator) and ``-`` both fold to ``_``.
- An optional ``parameter`` is appended as ``_{parameter}``.
- An optional ``prefix`` is prepended as ``{prefix}_`` (events, buttons).
- Hub-like addresses (``hub``, ``install_mode``, ``program``, ``sysvar``),
  internal addresses (``INT000*``) and virtual-remote addresses are prefixed
  with the ``central_id``; all other addresses are not.
- The whole result is lowercased last.
"""

from typing import Final

__all__ = [
    "ADDRESS_SEPARATOR",
    "HUB_ADDRESS",
    "INSTALL_MODE_ADDRESS",
    "INTERNAL_ADDRESS_PREFIX",
    "PROGRAM_ADDRESS",
    "SYSVAR_ADDRESS",
    "VIRTUAL_REMOTE_ADDRESSES",
    "generate_channel_unique_id",
    "generate_unique_id",
]

ADDRESS_SEPARATOR: Final = ":"
HUB_ADDRESS: Final = "hub"
INSTALL_MODE_ADDRESS: Final = "install_mode"
PROGRAM_ADDRESS: Final = "program"
SYSVAR_ADDRESS: Final = "sysvar"
INTERNAL_ADDRESS_PREFIX: Final = "INT000"
VIRTUAL_REMOTE_ADDRESSES: Final[tuple[str, ...]] = ("BidCoS-RF", "BidCoS-Wir", "HmIP-RCV-1")

_CENTRAL_ID_ADDRESSES: Final = frozenset({HUB_ADDRESS, INSTALL_MODE_ADDRESS, PROGRAM_ADDRESS, SYSVAR_ADDRESS})


def generate_unique_id(
    *,
    central_id: str,
    address: str,
    parameter: str | None = None,
    prefix: str | None = None,
) -> str:
    """
    Build the unique identifier from an address and an optional parameter.

    The ``central_id`` is prepended for hub-level, internal and virtual-remote
    addresses (it must match ``CentralConfig.central_id`` in aiohomematic).
    ``prefix`` is used for events and buttons.
    """
    unique_id = address.replace(ADDRESS_SEPARATOR, "_").replace("-", "_")
    if parameter:
        unique_id = f"{unique_id}_{parameter}"
    if prefix:
        unique_id = f"{prefix}_{unique_id}"
    if (
        address in _CENTRAL_ID_ADDRESSES
        or address.startswith(INTERNAL_ADDRESS_PREFIX)
        or address.split(ADDRESS_SEPARATOR, maxsplit=1)[0] in VIRTUAL_REMOTE_ADDRESSES
    ):
        return f"{central_id}_{unique_id}".lower()
    return unique_id.lower()


def generate_channel_unique_id(*, central_id: str, address: str) -> str:
    """
    Build the channel/device-level unique identifier from an address.

    This is aiohomematic's *second* routing key (``Channel._unique_id``); it
    carries no parameter and, unlike :func:`generate_unique_id`, prepends the
    ``central_id`` only for virtual-remote addresses (not for hub/internal
    addresses).
    """
    unique_id = address.replace(ADDRESS_SEPARATOR, "_").replace("-", "_")
    if address.split(ADDRESS_SEPARATOR, maxsplit=1)[0] in VIRTUAL_REMOTE_ADDRESSES:
        return f"{central_id}_{unique_id}".lower()
    return unique_id.lower()
