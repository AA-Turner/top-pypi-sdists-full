"""
Parameter grouping for configuration forms.

Groups a flat list of parameters into logical sections using
prefix-based heuristics and curated category mappings.

Public API of this module is defined by __all__.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
import inspect
import re
from typing import Final

from aiohomematic.const import ParameterData
from aiohomematic.easymode_data import get_channel_metadata

from aiohomematic_config.const import DEFAULT_LOCALE


@dataclass(frozen=True)
class ParameterGroup:
    """A logical group of parameters."""

    id: str
    title: str
    parameters: tuple[str, ...]


# Curated group definitions: (group_id, title_en, regex patterns)
_GROUP_DEFINITIONS: Final[tuple[tuple[str, str, tuple[str, ...]], ...]] = (
    (
        "temperature",
        "Temperature Settings",
        (r"TEMPERATURE_.*", r".*_TEMP_.*", r"FROST_.*", r"COMFORT_.*", r"ECO_.*"),
    ),
    (
        "timing",
        "Timing & Duration",
        (r".*_TIME_.*", r".*_DURATION_.*", r".*_DELAY_.*", r".*_INTERVAL_.*", r".*_TIMEOUT_.*"),
    ),
    (
        "display",
        "Display Settings",
        (r"SHOW_.*", r"DISPLAY_.*", r"BACKLIGHT_.*", r"LED_.*"),
    ),
    (
        "transmission",
        "Transmission & Communication",
        (r"TRANSMIT_.*", r"TX_.*", r"SIGNAL_.*", r"DUTYCYCLE_.*", r"COND_TX_.*"),
    ),
    (
        "powerup",
        "Power-Up Behavior",
        (r"POWERUP_.*",),
    ),
    (
        "boost",
        "Boost Settings",
        (r"BOOST_.*",),
    ),
    (
        "button",
        "Button Behavior",
        (r"BUTTON_.*", r"LOCAL_.*"),
    ),
    (
        "threshold",
        "Thresholds & Conditions",
        (r".*_THRESHOLD_.*", r".*_DECISION_.*", r".*_FILTER.*"),
    ),
    (
        "status",
        "Status & Reporting",
        (r"STATUSINFO_.*", r"STATUS_.*"),
    ),
)

# Section title translations keyed by locale then group_id.
_SECTION_TITLES: Final[dict[str, dict[str, str]]] = {
    "de": {
        "temperature": "Temperatur-Einstellungen",
        "timing": "Zeit & Dauer",
        "display": "Anzeige-Einstellungen",
        "transmission": "Übertragung & Kommunikation",
        "powerup": "Einschaltverhalten",
        "boost": "Boost-Einstellungen",
        "button": "Tastenverhalten",
        "threshold": "Schwellwerte & Bedingungen",
        "status": "Status & Meldungen",
        "other": "Sonstige Einstellungen",
    },
}


@dataclass
class _GroupCollector:
    """Mutable collector for building parameter groups."""

    id: str
    title: str
    patterns: tuple[re.Pattern[str], ...]
    parameters: list[str] = field(default_factory=list)


class ParameterGrouper:
    """
    Group parameters into logical sections.

    Applies pattern-based heuristics to organize flat parameter lists.
    """

    __slots__ = ("_collectors", "_locale")

    def __init__(self, *, locale: str = DEFAULT_LOCALE) -> None:
        """Initialize the parameter grouper."""
        self._locale = locale
        self._collectors: tuple[_GroupCollector, ...] = tuple(
            _GroupCollector(
                id=gid,
                title=self._translate(group_id=gid, fallback=title),
                patterns=tuple(re.compile(p) for p in patterns),
            )
            for gid, title, patterns in _GROUP_DEFINITIONS
        )

    def group(
        self,
        *,
        descriptions: Mapping[str, ParameterData],
        channel_type: str = "",
        sender_type: str = "",
    ) -> tuple[ParameterGroup, ...]:
        """
        Group parameters into logical sections.

        When easymode metadata is available for the channel type, use the
        semantically defined groups from the CCU WebUI instead of
        prefix-based heuristics.

        Args:
            descriptions: Parameter descriptions to group.
            channel_type: Optional receiver channel type for metadata lookup.
            sender_type: Optional sender channel type for metadata lookup.

        Returns:
            Tuple of ParameterGroup instances.

        """
        # Try metadata-based grouping first
        if (
            channel_type
            and sender_type
            and (
                result := self._groups_from_metadata(
                    descriptions=descriptions,
                    channel_type=channel_type,
                    sender_type=sender_type,
                )
            )
        ):
            return result

        # Fallback: pattern-based grouping
        return self._groups_from_patterns(descriptions=descriptions)

    def _groups_from_metadata(
        self,
        *,
        descriptions: Mapping[str, ParameterData],
        channel_type: str,
        sender_type: str,
    ) -> tuple[ParameterGroup, ...] | None:
        """Build groups from easymode metadata if available."""
        from aiohomematic_config.profile_store import _RECEIVER_TYPE_ALIASES  # noqa: PLC0415

        effective_type = _RECEIVER_TYPE_ALIASES.get(channel_type, channel_type)
        if not (metadata := get_channel_metadata(channel_type=effective_type)):
            return None
        st_meta = metadata.sender_types.get(sender_type)
        if not st_meta or not st_meta.parameter_order:
            return None

        available = set(descriptions.keys())

        # Use semantic parameter groups from metadata when populated
        if st_meta.parameter_groups:
            groups: list[ParameterGroup] = []
            assigned: set[str] = set()
            for group_def in st_meta.parameter_groups:
                if not (params := tuple(p for p in group_def.parameters if p in available)):
                    continue
                assigned.update(params)
                label = group_def.label.get(self._locale) or group_def.label.get("en", group_def.id)
                groups.append(
                    ParameterGroup(
                        id=group_def.id,
                        title=label,
                        parameters=params,
                    )
                )
            # Add ungrouped parameters in a fallback section
            if ungrouped := sorted(available - assigned):
                groups.append(
                    ParameterGroup(
                        id="other",
                        title=self._translate(group_id="other", fallback="Other Settings"),
                        parameters=tuple(ungrouped),
                    )
                )
            if groups:
                return tuple(groups)

        # Fallback: use parameter_order for sorting within a single group
        ordered_params = [p for p in st_meta.parameter_order if p in available]
        # Add remaining params not in the order list
        remaining = sorted(available - set(ordered_params))
        if not (all_params := ordered_params + remaining):
            return None

        return (
            ParameterGroup(
                id="all",
                title=self._translate(group_id="other", fallback="Settings"),
                parameters=tuple(all_params),
            ),
        )

    def _groups_from_patterns(
        self,
        *,
        descriptions: Mapping[str, ParameterData],
    ) -> tuple[ParameterGroup, ...]:
        """Group parameters using prefix-based pattern matching (fallback)."""
        # Reset collectors
        for collector in self._collectors:
            collector.parameters.clear()

        ungrouped: list[str] = []

        for param_id in sorted(descriptions.keys()):
            matched = False
            for collector in self._collectors:
                if any(pattern.fullmatch(param_id) for pattern in collector.patterns):
                    collector.parameters.append(param_id)
                    matched = True
                    break
            if not matched:
                ungrouped.append(param_id)

        groups: list[ParameterGroup] = [
            ParameterGroup(
                id=collector.id,
                title=collector.title,
                parameters=tuple(collector.parameters),
            )
            for collector in self._collectors
            if collector.parameters
        ]

        if ungrouped:
            groups.append(
                ParameterGroup(
                    id="other",
                    title=self._translate(group_id="other", fallback="Other Settings"),
                    parameters=tuple(ungrouped),
                )
            )

        return tuple(groups)

    def _translate(self, *, group_id: str, fallback: str) -> str:
        """Return translated section title or fallback."""
        return _SECTION_TITLES.get(self._locale, {}).get(group_id, fallback)


__all__ = tuple(
    sorted(
        name
        for name, obj in globals().items()
        if not name.startswith("_")
        and (name.isupper() or inspect.isfunction(obj) or inspect.isclass(obj))
        and getattr(obj, "__module__", __name__) == __name__
    )
)
