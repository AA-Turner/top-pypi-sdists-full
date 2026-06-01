"""Parse Flipper ``.sub`` file contents into :class:`RadioFrequencyCommand`."""

from __future__ import annotations

from typing import Any

from .commands import RadioFrequencyCommand
from .commands.ook import OOKCommand


def parse_sub_content(content: str) -> RadioFrequencyCommand:
    """Parse a Flipper ``.sub`` file into a :class:`RadioFrequencyCommand`."""
    fields: dict[str, str] = {}
    raw_parts: list[str] = []
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        key, sep, value = line.partition(":")
        if not sep:
            continue
        key = key.strip()
        value = value.strip()
        if key == "RAW_Data":
            raw_parts.append(value)
        else:
            fields[key] = value

    protocol = fields.get("Protocol", "")
    if protocol != "RAW":
        raise ValueError(f"Unsupported Protocol {protocol!r}; only RAW is supported")

    preset = fields.get("Preset", "")
    if "Ook" not in preset:
        raise ValueError(
            f"Unsupported Preset {preset!r}; only OOK presets are supported"
        )

    if "Frequency" not in fields:
        raise ValueError("Missing Frequency field")
    if not raw_parts:
        raise ValueError("Missing RAW_Data field")

    timings = [int(v) for part in raw_parts for v in part.split()]
    if len(timings) % 2 != 0:
        raise ValueError("RAW_Data must contain an even number of values")

    kwargs: dict[str, Any] = {
        "frequency": int(fields["Frequency"]),
        "timings": timings,
        "repeat_count": int(fields.get("Repeat", "0")),
    }
    return OOKCommand(**kwargs)
