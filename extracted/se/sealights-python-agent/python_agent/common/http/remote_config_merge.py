"""
Typed merge for the v3 remote-configuration response.

Background
----------
The legacy v2 flow did a blind ``config_data.__dict__.update(parsed_dict)`` on
whatever came back from the backend. Any stray key became a ConfigData
attribute. The v3 flow is stricter for two reasons:

1. v3 responses are flat ``dict[str, str]`` — every value arrives as a string,
   so ints / bools must be explicitly coerced.
2. The BE uses customer-facing alias names (e.g. ``footprintsSendIntervalSecs``)
   that the agent wants to translate into its own internal attributes
   (``intervalSeconds``).

This module encapsulates both concerns and its failure modes are explicit:
unknown keys log a WARNING once and are dropped; type-coercion failures log a
WARNING and leave the default in place. The merge never raises.
"""

import logging
from typing import Any, Dict


log = logging.getLogger(__name__)


# BE-facing name -> internal ConfigData attribute.
# Keys not listed here are looked up directly on ConfigData — the alias map
# only handles cases where the external and internal names differ.
REMOTE_FIELD_ALIASES: Dict[str, str] = {
    "footprintsSendIntervalSecs": "intervalSeconds",
    "footprintsCollectIntervalSecs": "_add_coverage_interval_seconds",
    "footprintsBufferThresholdMB": "footprintsBufferThresholdMB",
}


# ConfigData attributes that remote config must never write, even though they
# exist on ConfigData and would otherwise be applied by name. Lookup below is
# deny-by-unknown-name, so every new attribute is remotely settable by default;
# these two must not be.
#
# testNameFormat: identity must not change without a visible change to the CI
# command, because flipping it retrains TIA (contract C1, AC51).
# skipFootprintsPipeline: a remote `false` would rebuild the footprints
# pipeline inside a Robot process, reinstating the BuildMapper scan and the
# tracer that contract C11 exists to remove (Rule 5).
NON_REMOTE_FIELDS: frozenset = frozenset({"testNameFormat", "skipFootprintsPipeline"})


# Internal ConfigData attribute -> expected Python type for v3 coercion.
# Add entries here whenever a new remote-tunable int/bool field is introduced.
TYPED_FIELDS: Dict[str, type] = {
    "interval": int,
    "intervalSeconds": int,
    "_add_coverage_interval_seconds": int,
    "footprintsBufferThresholdMB": int,
}


def _coerce(value: Any, target_type: type):
    """Best-effort string → target_type conversion. Raises ValueError on failure."""
    if target_type is int:
        # Accept both ints and ints-as-strings ("10"). Reject non-integer
        # strings (e.g. "xyz") so the caller can log and skip.
        if isinstance(value, bool):  # bool subclasses int in Python — reject
            raise ValueError("bool received where int expected")
        return int(value)
    if target_type is bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            lowered = value.strip().lower()
            if lowered in ("true", "1", "yes", "on"):
                return True
            if lowered in ("false", "0", "no", "off"):
                return False
            raise ValueError("cannot coerce %r to bool" % value)
        raise ValueError("cannot coerce %r to bool" % value)
    return target_type(value)


def build_typed_update(
    remote_config: Dict[str, Any],
    target_attrs: set,
) -> Dict[str, Any]:
    """
    Translate a flat v3 remote-config dict into a ``{attr: typed_value}`` map
    that can be applied via ``config_data.__dict__.update(...)``.

    ``target_attrs`` is the set of valid ConfigData attribute names (usually
    ``set(dir(config_data))``). Anything that is neither in the alias map nor
    in ``target_attrs`` is dropped with a WARNING — that catches field-name
    drift between the Agents microservice and this agent.

    The function never raises; individual malformed values are skipped and
    logged, leaving the agent to keep its existing defaults for those fields.
    """
    if not isinstance(remote_config, dict):
        log.warning(
            "Remote config is not a dict (%s) — ignoring entirely",
            type(remote_config).__name__,
        )
        return {}

    typed_update: Dict[str, Any] = {}
    for raw_key, raw_value in remote_config.items():
        # Empty / None values are treated as "field not provided" - skip quietly.
        if raw_value is None or (isinstance(raw_value, str) and raw_value == ""):
            continue

        # Resolve alias -> internal attribute
        attr = REMOTE_FIELD_ALIASES.get(raw_key, raw_key)

        if attr in NON_REMOTE_FIELDS:
            log.warning(
                "Remote-config key %s is not remotely configurable — ignored "
                "(value=%r)",
                raw_key,
                raw_value,
            )
            continue

        if attr not in target_attrs:
            log.warning(
                "Unknown remote-config key: %s (value=%r) — ignored", raw_key, raw_value
            )
            continue

        # Coerce type if we know the target type; otherwise pass through.
        target_type = TYPED_FIELDS.get(attr)
        if target_type is None:
            typed_update[attr] = raw_value
            continue

        try:
            typed_update[attr] = _coerce(raw_value, target_type)
        except (ValueError, TypeError) as e:
            log.warning(
                "Failed to coerce remote-config value for %s: %r — "
                "leaving default in place (error=%s)",
                raw_key,
                raw_value,
                e,
            )
            continue

    return typed_update
