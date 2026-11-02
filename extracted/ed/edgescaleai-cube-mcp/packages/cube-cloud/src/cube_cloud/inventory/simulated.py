"""A simulated inventory backend, for building the join before the API is reachable.

**Why synthesis rather than a fixture list.** The console's cube list comes from
Apollo, so the cluster names it asks about are whatever the live stack returns — on
dev, ~110 real environment names. A hand-written fixture of invented cubes would
join against *none* of them, leaving every card blank and the feature unexercisable,
which defeats the point of simulating. So this backend answers for **any** cluster
name it is handed, deriving a stable record from the name itself.

**Determinism is load-bearing, and `hash()` cannot provide it.** Python salts
`hash()` per process (`PYTHONHASHSEED`), so two ECS tasks — or two runs of the test
suite — would disagree about a cube's simulated customer, which reads as data
corruption rather than as simulation. Every value here is derived from a SHA-256 of
the cluster name instead: same cube, same record, everywhere, forever.

**The data is conspicuously fictional on purpose.** The customer names are
well-known placeholder corporations, and callers stamp `simulated: true` onto any
payload built from this backend so the UI can badge it (see
`client.InventoryUnavailable` / `console/reads.py::_inventory_summary`). Simulated
inventory that looked plausibly real on a client-facing console would be a worse
outcome than no inventory at all — a customer reading an invented site label or
lifecycle status as fact. Both signals exist so that cannot happen quietly.
"""

from __future__ import annotations

import hashlib

from cube_cloud.inventory.records import InventoryRecord

# Deliberately recognizable fictional corporations — see the module docstring. Do
# NOT replace these with real customer names to make a demo look better: the whole
# safety argument for shipping a simulation mode rests on its output being
# self-evidently fake next to the `simulated: true` badge.
_CUSTOMERS = (
    "Acme Robotics",
    "Globex Manufacturing",
    "Initech Logistics",
    "Northwind Foods",
    "Umbra Materials",
    "Vandelay Industries",
)

_SITES = (
    ("Toledo", "OH"),
    ("Reno", "NV"),
    ("Greenville", "SC"),
    ("Waterloo", "IA"),
    ("Odessa", "TX"),
    ("Bakersfield", "CA"),
    ("Muskegon", "MI"),
    ("Chattanooga", "TN"),
)

# The real lifecycle enum from the inventory API, in lifecycle order. Weighted toward
# the late states because a cube the console can see has, by definition, been
# deployed far enough to have an Apollo environment — a `built` cube would not
# normally appear in this UI at all.
_STATUSES = (
    "allocated", "allocated", "allocated",
    "staged", "staged",
    "active", "active",
    "online",
    "inactive",
)

# `cube_env` values, OBSERVED on the live prod fleet 2026-08-26 via
# `scripts/probe-inventory-api.py` (check 7): Dev=42, empty=21, Prod=18,
# Pre-prod=6, Int=4 across 91 cubes.
#
# Two things the guess got wrong and are worth keeping right: the values are
# **Capitalized**, not lowercase, and there is no `staging` — the pre-production
# tiers are `Pre-prod` and `Int`. Weighted to match the real distribution, including
# the empty string, because ~23% of the fleet has no `cube_env` and a simulation
# where every cube has one hides how the UI actually looks.
_ENVIRONMENTS = ("Dev", "Dev", "Dev", "Dev", "Prod", "Prod", "Pre-prod", "Int", "", "")


def _digest(cluster: str) -> bytes:
    return hashlib.sha256(cluster.encode("utf-8")).digest()


def _pick(seq: tuple, digest: bytes, offset: int):
    """Stable choice from `seq`, using one byte of the digest.

    Separate offsets give independent-looking fields from one hash, so two cubes
    sharing a customer do not also always share a site.
    """
    return seq[digest[offset % len(digest)] % len(seq)]


def simulated_record(cluster: str) -> InventoryRecord:
    """A stable, fictional inventory record for `cluster`.

    Shaped like a real one: the label follows the `<Customer>-<Site>-<n>` convention
    the live records use (`Lear-Hammond-1`), and the serial follows `ES######`.
    """
    digest = _digest(cluster)

    customer = _pick(_CUSTOMERS, digest, 0)
    city, state = _pick(_SITES, digest, 1)
    status = _pick(_STATUSES, digest, 2)
    environment = _pick(_ENVIRONMENTS, digest, 3)

    # A serial in the real `ES######` shape, stable per cube. Derived from two bytes
    # so the space is wide enough that nearby cubes do not collide visibly.
    serial_n = (digest[4] << 8 | digest[5]) % 1_000_000
    # The trailing index on a site label — real fleets run several cubes per site.
    site_index = (digest[6] % 4) + 1

    # `Acme Robotics` -> `Acme`, matching the label convention's single-token company
    # segment rather than embedding a space in the middle of the label.
    company_token = customer.split(" ")[0]

    # A router MAC with the locally-administered bit set (`02:` first octet), so it
    # cannot collide with any vendor's real address — Peplink's OUI included. The
    # same "self-evidently fake" rule as the customer names, applied to a MAC.
    router_mac = ":".join(f"{b:02X}" for b in (0x02, *digest[7:12]))

    return InventoryRecord(
        customer=customer,
        label=f"{company_token}-{city}-{site_index}",
        environment=environment,
        serial=f"ES{serial_n:06d}",
        status=status,
        location=f"{city}, {state}",
        router_mac=router_mac,
        clustername=cluster,
        apollo_environment_name=cluster,
    )
