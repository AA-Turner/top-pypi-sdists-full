"""hook_switches: which hooks answer an agent's event, Probe's own plugins or the frozen hook shim, by the
agent process's birth against an append-only switch history (stdlib-only, vendored to the hooks and the tap)."""

from .hook_switches import (
    LEDGER_VERSION,
    MARGIN_S,
    VIA_ENV,
    Side,
    find_agent_birth,
    get_birth_epoch,
    get_config_root,
    get_ledger_path,
    get_service_root,
    get_side,
    get_switches,
    has_any_ledger,
    is_legacy_owned,
    is_shim_owned,
    load_ledger,
    should_yield,
)

__all__ = [
    "LEDGER_VERSION",
    "MARGIN_S",
    "VIA_ENV",
    "Side",
    "find_agent_birth",
    "get_birth_epoch",
    "get_config_root",
    "get_ledger_path",
    "get_service_root",
    "get_side",
    "get_switches",
    "has_any_ledger",
    "is_legacy_owned",
    "is_shim_owned",
    "load_ledger",
    "should_yield",
]
