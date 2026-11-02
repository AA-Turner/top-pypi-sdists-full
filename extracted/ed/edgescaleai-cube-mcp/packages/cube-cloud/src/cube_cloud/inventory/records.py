"""The inventory record — and the boundary that keeps the rest of it out.

An `edgescale-inventory` cube record is a **large, sensitive object**. Alongside the
seven display fields the console wants, one record carries `ipmi_password`,
`motherboard_bmc_mac`, `motherboard_lan_mac_1`/`_2`, `router_serial_number`,
`router_wifi_name`, `router_network_config`, `diag_subnet`, `block_number`, and
free-text `notes` (operator observations about the hardware). None of that has any
business reaching a browser to render a site label. (`router_mac_address` is the one
MAC that does — admitted on its own; see the note above `HARDWARE_KEYS`.)

**The containment rule, and why it is here rather than at the console.** The console
read layer's discipline (`console/reads.py`, rule 1) is "serialize through an
explicit allowlist, never passthrough". This module goes one step further and drops
the raw record at the *client* boundary: `record_from_raw` copies ten named keys
(nine identity keys plus the router serial, a join key) into `InventoryRecord` and
discards the source dict, so the un-allowlisted payload never propagates past the
client at all. The console's own serializer
(`_inventory_summary`) is then a **second, independent** barrier over an object that
is already minimal — the same two-barrier shape `_app_summary` has behind
`CONSOLE_ENVIRONMENT_ENTITIES` not fetching `declaredState.config`.

**"Select less" exists on this API, and cannot be used — which is worth stating
precisely, because the parameter looks made for this.** `GET /inventory?view=summary`
returns a 20-field projection that includes all six original display fields, skips
the KMS decrypt pass, and is served from a covering GSI. It also omits `clustername` AND
`apollo_environment_name` — both of this join's keys — so a caller using it gets
records that can never be matched to a cube: every cube renders as unfiled while the
payload looks perfectly healthy. The projection is capped at 20 non-key attributes by
the GSI and is already full, so adding a key is a destroy/recreate on the inventory
side rather than an edit. `client.py` therefore reads full rows, and
`test_inventory.py::test_the_fleet_read_never_asks_for_view_summary` pins that choice
so nobody "optimizes" it back.

**What DOES make this structural is the token's scope, not a query parameter.** The
API decrypts eight `SENSITIVE_FIELDS` into the response for any caller holding
`view_sensitive`, and strips them for one that does not — so whether
`ipmi_password` and `platform_kubeconfig` ever cross the wire is decided entirely by
the credential. A legacy service token authenticates as `admin` and holds it; a
minted read-only token scoped to `view_cubes` alone does not. `client.py`'s
`_warn_if_over_scoped` reports the difference rather than assuming it, because this
allowlist means the values are unused either way and "unused" is a weaker property
than "never sent".

`clustername` and `apollo_environment_name` are carried but **never displayed**:
they exist only as join keys (see `client.build_index`). The Apollo environment name
is already the console's cube name, so rendering it again would be redundant.

`router_serial_number` is the one sensitive-looking key that IS carried, for the same
reason: it joins a cube to its router's GPS position, server-side. It is a device
identifier of the customer's network hardware, and the console shows no router facts,
so it is on neither summary nor the record's repr. The rule is "carried, never
serialized" — not "never carried" — and `test_inventory.py` pins both halves.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Raw inventory keys copied into `InventoryRecord`. Everything else in the record is
# dropped. Kept as a module constant so a test can assert that a record containing
# every sensitive field still yields only these — the tripwire against someone
# "simplifying" `record_from_raw` into a passthrough.
_IDENTITY_KEYS = frozenset({
    "customer",
    "cube_label_name",
    "cube_env",
    "cube_serial",
    "status",
    "location",
    # The Peplink router's MAC — the one the inventory web app labels plain "MAC
    # Address". The ONLY MAC carried; see the exclusion note above HARDWARE_KEYS.
    "router_mac_address",
    # Join keys only — not display fields.
    "clustername",
    "apollo_environment_name",
    # Joins a cube to its router's GPS position, server-side. Never serialized.
    "router_serial_number",
})

# The seven fields that reach the browser, as their client-facing names. Asserted
# against the serializer's output so adding a field to one without the other fails.
SUMMARY_FIELDS = frozenset({
    "customer", "label", "environment", "serial", "status", "location",
    "router_mac",
})


# Values that mean "nobody filled this in" and must never render as a spec.
#
# Observed on the live prod fleet (2026-08-26), and the counts are why this exists
# rather than being defensive: `cpu_cooler_manufacturer` / `_model` /
# `_serial_number` and `manufacturer_name` hold the literal string
# `(NEEDS TO BE SET IN 'CUBE VERSIONS')` on **66 of 91 cubes**, and `TBD` appears
# across `cpu`, `gpu_count`, `gpu_type`, `cpu_serial_number`, `router_ip` and more.
# Rendered verbatim, a hardware table would read as though the cube's CPU cooler were
# a product called "(NEEDS TO BE SET IN 'CUBE VERSIONS')".
#
# EXACT lowercase match after trimming, never a substring — a real part number could
# contain "na" or "-". The one exception is the parenthetical placeholder, matched by
# prefix because its tail varies; it is distinctive enough that a genuine spec value
# starting `(needs to be set` is not a realistic collision.
_PLACEHOLDERS = frozenset({
    "tbd", "t.b.d.", "n/a", "na", "none", "null", "unknown", "-", "--", "?", "???",
})
_PLACEHOLDER_PREFIX = "(needs to be set"


def _is_placeholder(value: str) -> bool:
    v = value.strip().lower()
    return v in _PLACEHOLDERS or v.startswith(_PLACEHOLDER_PREFIX)


def _spec(raw: dict, key: str) -> str:
    """A displayable spec string for `key`, or "" if unset or a placeholder."""
    value = raw.get(key)
    if value is None:
        return ""
    text = str(value).strip()
    return "" if _is_placeholder(text) else text


def _spec_list(raw: dict, key: str) -> tuple[str, ...]:
    """A displayable list for `key`, placeholders dropped.

    A tuple rather than a list because `InventoryRecord`/`Hardware` are frozen and
    shared across requests from a process-lifetime cache; a mutable member would let
    one request's handling alter what the next one reads.
    """
    value = raw.get(key)
    if not isinstance(value, (list, tuple)):
        return ()
    out = []
    for item in value:
        if item is None:
            continue
        text = str(item).strip()
        if text and not _is_placeholder(text):
            out.append(text)
    return tuple(out)


def _text(raw: dict, key: str) -> str:
    """A trimmed string for `key`, whatever the record actually holds.

    DynamoDB-backed records use `null` and absent interchangeably for an unset field
    (the scrub in the inventory skill's Operation 7 writes explicit nulls), and a
    numeric-looking value can arrive as a number. Normalizing to `str` here means
    neither the join nor the UI has to carry `None` handling.
    """
    value = raw.get(key)
    if value is None:
        return ""
    return str(value).strip()


# Hardware keys copied into `Hardware`. Same allowlist discipline as CARRIED_KEYS,
# and the same tripwire watches it.
#
# **What is deliberately EXCLUDED, and why**, since the record carries all of it and
# the temptation is to show everything:
#   * Component serials (`memory_serial_numbers`, `ssd_serial_numbers`,
#     `motherboard_serial_number`, `cpu_serial_number`, `gpu_serial_number`) — asset
#     tracking, useful for an RMA and not to the customer looking at the cube.
#   * Host MAC addresses (`motherboard_bmc_mac`, `motherboard_lan_mac_1`/`_2`,
#     `motherboard_lan_mac_info`) — network fingerprinting. The router's MAC
#     (`router_mac_address`) IS shown, as an identity field rather than hardware:
#     it is what an operator matches against the Peplink/IC2 side, and it was
#     admitted deliberately and alone. Admitting it did not open the others.
#   * Firmware revisions (`motherboard_bios_firmware_revision`,
#     `motherboard_bmc_firmware_revision`, `ssd_firmware_revisions`) — publishing
#     exact firmware versions on a customer-facing page is a known-vulnerability
#     lookup for anyone who reads it.
#   * `cpu_cooler_*` — 66 of 91 cubes hold the "(NEEDS TO BE SET…)" placeholder, so
#     the field carries no information today even where it is "populated".
#   * The legacy scalars superseded by better fields: `cpu` (all `TBD`) vs
#     `cpu_model`, `memory` vs `memory_total`, `ssd_capacity` (1 row) vs
#     `ssd_capacities`, `gpu_count`/`gpu_type` vs `gpu_models`,
#     `dram_serial_numbers` vs `memory_serial_numbers`. Picking the obvious-looking
#     name would have produced a table full of `TBD`.
#
# Fill rates on the live prod fleet (91 cubes, 2026-08-26) are noted per field so the
# sparseness is visible here rather than discovered in the UI.
HARDWARE_KEYS = frozenset({
    # System — the best-populated identity fields.
    "server_manufacturer",       # 85%
    "server_model",              # 85%  e.g. "Cube v2"
    "motherboard_manufacturer",  #  3%  e.g. "Supermicro"
    "motherboard_model",         #  3%  e.g. "X14SBM-TF"
    # CPU
    "cpu_manufacturer",          # 48%
    "cpu_model",                 # 48%  e.g. "Intel(R) Xeon(R) 6521P"
    "cpu_cores",                 # 47%
    "cpu_threads",               # 48%
    "cpu_max_clock",             # 48%  MHz, numeric
    # Memory
    "memory_total",              # 48%  e.g. "128 GB"
    "memory_type",               # 47%  e.g. "DDR5"
    "memory_speed",              # 47%  e.g. "6400 MHz"
    "memory_manufacturer",       # 47%
    "memory_ecc",                # 47%  e.g. "ECC"
    "memory_dimm_count",         # 47%
    "memory_dimm_size",          # 47%  e.g. "32 GB"
    "memory_dimm_locators",      # 47%  list, e.g. ["DIMMA1", "DIMMC1", ...]
    # Storage
    "ssd_manufacturer",          # 48%
    "ssd_model",                 # 47%  e.g. "KINGSTON SEDC3000ME3T8"
    "ssd_type",                  # 47%  e.g. "NVMe"
    "ssd_capacities",            # 35%  list, e.g. ["3.84 TB", "3.84 TB", "3.84 TB"]
    # GPU
    "gpu_manufacturers",         # 48%  list
    "gpu_models",                # 48%  list, e.g. ["NVIDIA RTX Pro 5000 Blackwell"]
    "gpu_memories",              #  0%  list — in the schema, unpopulated today
})

# The client-facing keys of `Hardware.summary()`. Asserted against the serializer's
# real output so adding a field to one without the other fails.
HARDWARE_SUMMARY_FIELDS = frozenset({
    "server_manufacturer", "server_model", "motherboard_manufacturer",
    "motherboard_model", "cpu_manufacturer", "cpu_model", "cpu_cores",
    "cpu_threads", "cpu_max_clock", "memory_total", "memory_type", "memory_speed",
    "memory_manufacturer", "memory_ecc", "memory_dimm_count", "memory_dimm_size",
    "memory_dimm_locators", "ssd_manufacturer", "ssd_model", "ssd_type",
    "ssd_capacities", "gpu_manufacturers", "gpu_models", "gpu_memories",
})


# Every raw key `record_from_raw` reads, identity plus hardware. The `.get`-watching
# tripwire asserts against this, so it is the one list that must stay exhaustive.
CARRIED_KEYS = _IDENTITY_KEYS | HARDWARE_KEYS


@dataclass(frozen=True)
class Hardware:
    """One cube's hardware specification — the displayable subset.

    Every field is a string or a tuple of strings, already placeholder-cleaned, so
    the UI never has to know that `TBD` and `(NEEDS TO BE SET…)` mean "empty". A
    numeric field like `cpu_cores` is carried as a string for the same reason: the
    record has one shape, and the browser renders it rather than formatting it.
    """

    server_manufacturer: str = ""
    server_model: str = ""
    motherboard_manufacturer: str = ""
    motherboard_model: str = ""
    cpu_manufacturer: str = ""
    cpu_model: str = ""
    cpu_cores: str = ""
    cpu_threads: str = ""
    cpu_max_clock: str = ""
    memory_total: str = ""
    memory_type: str = ""
    memory_speed: str = ""
    memory_manufacturer: str = ""
    memory_ecc: str = ""
    memory_dimm_count: str = ""
    memory_dimm_size: str = ""
    memory_dimm_locators: tuple[str, ...] = ()
    ssd_manufacturer: str = ""
    ssd_model: str = ""
    ssd_type: str = ""
    ssd_capacities: tuple[str, ...] = ()
    gpu_manufacturers: tuple[str, ...] = ()
    gpu_models: tuple[str, ...] = ()
    gpu_memories: tuple[str, ...] = ()

    def any_known(self) -> bool:
        """True if ANY field is populated.

        Lets the UI distinguish "this cube has no hardware on file" — about half the
        fleet — from "the request failed", which is the same could-not-look versus
        nothing-there distinction the rest of this feature preserves.
        """
        return any(bool(v) for v in self.__dict__.values())

    def summary(self) -> dict:
        """JSON-ready. Whitelist by construction — it names its outputs.

        Lists become lists (not tuples) because `json` does not serialize a tuple
        distinguishably and the client's type says array.
        """
        return {
            "server_manufacturer": self.server_manufacturer,
            "server_model": self.server_model,
            "motherboard_manufacturer": self.motherboard_manufacturer,
            "motherboard_model": self.motherboard_model,
            "cpu_manufacturer": self.cpu_manufacturer,
            "cpu_model": self.cpu_model,
            "cpu_cores": self.cpu_cores,
            "cpu_threads": self.cpu_threads,
            "cpu_max_clock": self.cpu_max_clock,
            "memory_total": self.memory_total,
            "memory_type": self.memory_type,
            "memory_speed": self.memory_speed,
            "memory_manufacturer": self.memory_manufacturer,
            "memory_ecc": self.memory_ecc,
            "memory_dimm_count": self.memory_dimm_count,
            "memory_dimm_size": self.memory_dimm_size,
            "memory_dimm_locators": list(self.memory_dimm_locators),
            "ssd_manufacturer": self.ssd_manufacturer,
            "ssd_model": self.ssd_model,
            "ssd_type": self.ssd_type,
            "ssd_capacities": list(self.ssd_capacities),
            "gpu_manufacturers": list(self.gpu_manufacturers),
            "gpu_models": list(self.gpu_models),
            "gpu_memories": list(self.gpu_memories),
        }


def hardware_from_raw(raw: dict) -> Hardware:
    """Build a `Hardware` from one raw record, dropping every other field."""
    return Hardware(
        server_manufacturer=_spec(raw, "server_manufacturer"),
        server_model=_spec(raw, "server_model"),
        motherboard_manufacturer=_spec(raw, "motherboard_manufacturer"),
        motherboard_model=_spec(raw, "motherboard_model"),
        cpu_manufacturer=_spec(raw, "cpu_manufacturer"),
        cpu_model=_spec(raw, "cpu_model"),
        cpu_cores=_spec(raw, "cpu_cores"),
        cpu_threads=_spec(raw, "cpu_threads"),
        cpu_max_clock=_spec(raw, "cpu_max_clock"),
        memory_total=_spec(raw, "memory_total"),
        memory_type=_spec(raw, "memory_type"),
        memory_speed=_spec(raw, "memory_speed"),
        memory_manufacturer=_spec(raw, "memory_manufacturer"),
        memory_ecc=_spec(raw, "memory_ecc"),
        memory_dimm_count=_spec(raw, "memory_dimm_count"),
        memory_dimm_size=_spec(raw, "memory_dimm_size"),
        memory_dimm_locators=_spec_list(raw, "memory_dimm_locators"),
        ssd_manufacturer=_spec(raw, "ssd_manufacturer"),
        ssd_model=_spec(raw, "ssd_model"),
        ssd_type=_spec(raw, "ssd_type"),
        ssd_capacities=_spec_list(raw, "ssd_capacities"),
        gpu_manufacturers=_spec_list(raw, "gpu_manufacturers"),
        gpu_models=_spec_list(raw, "gpu_models"),
        gpu_memories=_spec_list(raw, "gpu_memories"),
    )


@dataclass(frozen=True)
class InventoryRecord:
    """One cube's inventory facts — the carried subset, nothing more.

    Frozen because this object is cached in a process-lifetime fleet index shared by
    every request; a mutable record would let one request's handling alter what the
    next one reads.
    """

    customer: str
    label: str
    environment: str
    serial: str
    status: str
    location: str
    router_mac: str
    clustername: str
    apollo_environment_name: str
    # Its own frozen dataclass rather than a dict, so the allowlist discipline holds
    # one level down too: a dict here would invite passthrough of the ~120 other keys
    # a raw record carries.
    hardware: Hardware = Hardware()
    # A join key for the GPS read, never a display field (see the module
    # docstring). `repr=False` so a record that reaches a log line does not carry
    # it there; defaulted so records built without inventory (simulated mode) need
    # not invent one.
    router_serial_number: str = field(default="", repr=False)

    def summary(self) -> dict:
        """The seven display fields, JSON-ready.

        The second of the two barriers described in the module docstring. Note this
        is a *whitelist by construction* — it names its seven outputs — so a field
        added to `InventoryRecord` for a future join key cannot leak through it by
        default, which is the failure mode `**self.__dict__` would have.
        """
        return {
            "customer": self.customer,
            "label": self.label,
            "environment": self.environment,
            "serial": self.serial,
            "status": self.status,
            "location": self.location,
            "router_mac": self.router_mac,
        }


def record_from_raw(raw: dict) -> InventoryRecord:
    """Build a record from one raw inventory item, dropping every other field.

    The raw dict is not retained anywhere. See the module docstring for why this,
    rather than the console serializer, is the primary containment boundary.
    """
    return InventoryRecord(
        customer=_text(raw, "customer"),
        label=_text(raw, "cube_label_name"),
        environment=_text(raw, "cube_env"),
        serial=_text(raw, "cube_serial"),
        status=_text(raw, "status"),
        location=_text(raw, "location"),
        # `_spec`, not `_text`: router fields hold `TBD` on the real fleet, and a
        # placeholder must render as unknown rather than as a MAC.
        router_mac=_spec(raw, "router_mac_address"),
        clustername=_text(raw, "clustername"),
        apollo_environment_name=_text(raw, "apollo_environment_name"),
        hardware=hardware_from_raw(raw),
        router_serial_number=_text(raw, "router_serial_number"),
    )
