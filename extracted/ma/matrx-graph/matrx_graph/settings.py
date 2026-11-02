"""Workflow access to SETTINGS — the values an organization turns, read at run time.

A workflow that hard-codes "read 5 pages" or "stop at 3 good pages" in a node's
input has frozen an opinion into a definition; the platform rule is that every
limit is a setting (``platform.feature_knob``) an admin — or an organization —
can change, and the run reads the CURRENT value
(``common-docs/policies/limits-are-knobs-agents-set-them.md``). The
``data.setting.read`` step is that read; this module is its host door.

The host installs ONE async reader, ``(feature, key, organization_id) -> value``,
at boot (aidream: ``package_integration._workflow_setting_value`` →
``scoped_knob_raw``, which resolves organization overrides). The organization is
the RUN's own (``ctx.organization_id``), carried from the run's start — never an
input, never rebuilt.

Nothing fails silently: with no reader installed, or a setting that does not
exist, the step FAILS naming the setting — there is no default frozen here.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

#: ``async (feature, key, organization_id, user_id) -> the setting's effective value``.
SettingReader = Callable[[str, str, str | None, str | None], Awaitable[Any]]

#: ``async (feature, organization_id, user_id) -> {setting name: (effective value, where it came
#: from)}`` — EVERY setting of one feature, resolved for the run's organization and person.
FeatureSettingsReader = Callable[[str, str | None, str | None], Awaitable[dict[str, tuple[Any, str]]]]

_READER: SettingReader | None = None
_FEATURE_READER: FeatureSettingsReader | None = None


def set_setting_reader(reader: SettingReader | None) -> None:
    """Install the host's per-organization setting reader (``None`` = none)."""
    global _READER
    _READER = reader


def get_setting_reader() -> SettingReader | None:
    return _READER


def set_feature_settings_reader(reader: FeatureSettingsReader | None) -> None:
    """Install the host's read-every-setting-of-a-feature reader (``None`` = none)."""
    global _FEATURE_READER
    _FEATURE_READER = reader


def get_feature_settings_reader() -> FeatureSettingsReader | None:
    return _FEATURE_READER
