# SPDX-License-Identifier: MIT
# Copyright (c) 2021-2026
"""
Canonical, loom-namespaced unique_id — the external HA registry key.

The cross-backend routing key (:func:`generate_unique_id`) is the
algorithm-of-record; the *canonical* key wraps it in two ways for the
openccu-loom drop-in:

- a constant ``loom_`` namespace prefix segregates loom entities from
  other integrations' entities in a shared registry (notably on the MQTT
  plane); and
- the central-id slot of the routing key carries the **CCU serial
  suffix** (last 10 chars, lower-cased) for the address classes whose
  addresses repeat across CCUs (hub roots, ``INT000*``, virtual remotes).
  Normal device addresses (e.g. ``VCU1234567``) are globally unique and
  carry no prefix.

This module is the Python side of the daemon's Go ``internal/routingkey``
(`SerialSuffix` / `CanonicalUniqueID`); both run the same
:func:`generate_unique_id` underneath, so the two produce bit-identical
output. See ``docs/external-clients/ha-unique-id-migration.md`` in the
daemon repo.
"""

from typing import Final

from aiohomematic_contract.unique_id import generate_unique_id

__all__ = [
    "LOOM_NAMESPACE",
    "SERIAL_SUFFIX_LEN",
    "canonical_unique_id",
    "serial_suffix",
]

# Constant prefix applied to every external unique_id.
LOOM_NAMESPACE: Final = "loom"

# How many trailing characters of the CCU serial form the per-CCU
# discriminator. Ten mirrors the legacy ``entry_id[-10:]`` width.
SERIAL_SUFFIX_LEN: Final = 10


def serial_suffix(serial: str) -> str:
    """Return the per-CCU discriminator from the CCU serial.

    This is the last :data:`SERIAL_SUFFIX_LEN` characters of the CCU serial,
    lower-cased. Serials shorter than that are returned whole; empty in, empty out.
    This feeds the central-id slot of :func:`canonical_unique_id` for
    hub / internal / virtual-remote addresses.
    """
    serial = serial.lower()
    if len(serial) <= SERIAL_SUFFIX_LEN:
        return serial
    return serial[-SERIAL_SUFFIX_LEN:]


def canonical_unique_id(
    *,
    serial_suffix: str,
    address: str,
    parameter: str | None = None,
    prefix: str | None = None,
) -> str:
    """Build the external, loom-namespaced unique_id ``loom_<routing-key>``.

    ``serial_suffix`` goes in the central-id slot (see :func:`serial_suffix`);
    devices come out unprefixed within the routing key
    (``loom_vcu1234567_1_state``), while hub / internal / virtual-remote
    addresses carry the serial suffix
    (``loom_<serial10>_sysvar_<hub-slug>``).

    For hub data points pass the pseudo-address (``"sysvar"`` /
    ``"program"`` / ``"install_mode"``) and the :func:`hub_slug`-ed name
    as ``parameter``.
    """
    return f"{LOOM_NAMESPACE}_" + generate_unique_id(
        central_id=serial_suffix,
        address=address,
        parameter=parameter,
        prefix=prefix,
    )
