"""Translate administrator-friendly flags into one compute settings merge patch."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from labqoat.json_document import JsonDocument, JsonValue


@dataclass(frozen=True, kw_only=True)
class SettingsPatch:
    """Build Merge Patch documents where ``none`` removes a limit and family flags edit the current list."""

    cpu: str | None = None
    memory_gib: str | None = None
    gpus: str | None = None
    family_limits: Sequence[str] = ()
    clear_family_limits: bool = False
    rate: str | None = None
    timings: Mapping[str, int | None] | None = None

    FAMILY = re.compile(r"[a-z0-9]+:[a-z0-9][a-z0-9.-]*")

    def build(self, current: Mapping[str, JsonValue]) -> JsonDocument:
        """Return only the requested changes, rejecting an empty update."""
        patch = JsonDocument()
        workload = self._workload(current)
        if workload:
            patch["workload_limits"] = workload
        if self.rate is not None:
            patch["elastic_instance_rate_usd_per_hour"] = self.usd(self.rate)
        patch.update({name: value for name, value in (self.timings or {}).items() if value is not None})
        if not patch:
            raise ValueError("No settings were selected to change.")
        return patch

    def _workload(self, current: Mapping[str, JsonValue]) -> dict[str, JsonValue]:
        """Collect CPU, memory and GPU ceilings under workload_limits."""
        workload: dict[str, JsonValue] = {}
        if self.cpu is not None:
            workload["cpu_millicores"] = self.scaled(self.cpu, 1000, "--cpu")
        if self.memory_gib is not None:
            workload["memory_mib"] = self.scaled(self.memory_gib, 1024, "--memory-gib")
        gpu: dict[str, JsonValue] = {}
        if self.gpus is not None:
            gpu["total_devices"] = self.scaled(self.gpus, 1, "--gpus")
        if self.family_limits or self.clear_family_limits:
            gpu["families"] = self.families(self.current_families(current))
        if gpu:
            workload["gpu_limits"] = gpu
        return workload

    def families(self, existing: list[JsonValue]) -> list[JsonValue]:
        """Replace the family list with current entries edited by each FAMILY=N or FAMILY=none flag."""
        limits: dict[str, JsonValue] = {} if self.clear_family_limits else self.indexed(existing)
        seen: set[str] = set()
        for entry in self.family_limits:
            family, separator, value = entry.partition("=")
            if not separator or self.FAMILY.fullmatch(family) is None:
                raise ValueError(f"--gpu-family-limit expects FAMILY=COUNT such as nvidia:h100=4, not {entry!r}")
            if family in seen:
                raise ValueError(f"--gpu-family-limit names {family} more than once")
            seen.add(family)
            count = self.scaled(value, 1, "--gpu-family-limit")
            limits.pop(family, None)
            if count is not None:
                limits[family] = count
        return [{"family": family, "max_devices": count} for family, count in limits.items()]

    @staticmethod
    def indexed(existing: list[JsonValue]) -> dict[str, JsonValue]:
        """Index current family ceilings by canonical family identifier."""
        limits: dict[str, JsonValue] = {}
        for item in existing:
            entry = JsonDocument.expect_dict(item)
            limits[JsonDocument.expect_scalar(entry["family"], str)] = entry["max_devices"]
        return limits

    @staticmethod
    def current_families(current: Mapping[str, JsonValue]) -> list[JsonValue]:
        """Read the persisted family ceilings, treating absent members as an empty list."""
        workload = JsonDocument.expect_dict(current.get("workload_limits") or {})
        gpu = JsonDocument.expect_dict(workload.get("gpu_limits") or {})
        return JsonDocument.expect_list(gpu.get("families") or [])

    @staticmethod
    def scaled(value: str, scale: int, flag: str) -> int | None:
        """Parse a nonnegative quantity in display units, returning null for ``none``."""
        if value.strip().lower() == "none":
            return None
        try:
            amount = Decimal(value) * scale
        except InvalidOperation as error:
            raise ValueError(f"{flag} expects a nonnegative number or 'none', not {value!r}") from error
        if not amount.is_finite() or amount < 0 or amount != amount.to_integral_value():
            raise ValueError(f"{flag} expects a nonnegative whole amount or 'none', not {value!r}")
        return int(amount)

    @staticmethod
    def usd(value: str) -> str | None:
        """Normalize an hourly USD ceiling to cents, returning null for ``none``."""
        cents = SettingsPatch.scaled(value, 100, "--rate")
        return None if cents is None else f"{cents // 100}.{cents % 100:02d}"
