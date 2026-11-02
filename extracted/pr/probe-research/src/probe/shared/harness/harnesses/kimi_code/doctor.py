"""Kimi Code's diagnosis: its binary, version (2.1.1+) and plugin rows."""

from __future__ import annotations


def _kimi_rows() -> list[str]:
    """Kimi Code's binary and version (Probe needs 2.1.1+), and whether its
    plugin list is one the wizard can manage (Kimi has no install command, so
    the wizard writes that file; a layout it does not know is left alone)."""
    from probe.shared.harness.harnesses.kimi_code import config as kimi_config

    rows = []
    if not kimi_config.binary_available():
        rows.append(_row("Kimi Code CLI", _MISSING))
        return rows
    version = kimi_config.kimi_version()
    state = f"{_OK} ({'.'.join(map(str, version))})" if version else _OK
    problem = kimi_config.version_floor_problem()
    rows.append(_row("Kimi Code CLI", f"{state} -- {problem}" if problem else state))
    doc, refused = kimi_config._read_installed()  # noqa: SLF001 -- the same check the installer runs
    if refused:
        rows.append(_row("Kimi plugin list", f"not managed: {refused}"))
    else:
        ours = sorted(
            p.get("id") for p in doc["plugins"] if isinstance(p, dict) and p.get("id") in kimi_config.PLUGIN_IDS
        )
        rows.append(_row("Kimi plugin list", ", ".join(ours) if ours else "no Probe plugins"))
    return rows
from probe.shared.harness.diagnosis import _MISSING, _OK, _row  # noqa: E402 -- pieces need each other; the front door loads this one first
