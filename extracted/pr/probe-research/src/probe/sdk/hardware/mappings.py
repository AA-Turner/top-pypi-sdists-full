"""The single Prometheus-name → hardware-rail translation table.

Shared by the exporter scraper (phase 1a) and the PromQL source (phase 1b) so tiers cannot drift.
Entries carry the `hw/` key, label->coord mapping, counter-vs-gauge, declared agg and stall
companions. The default pack covers DCGM-exporter, node_exporter and cAdvisor; users extend it
declaratively (fleets rewrite labels via relabel_configs, so overrides are the supported path).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Mapped:
    key: str
    coords: dict
    kind: str  # "gauge" | "counter"
    agg: str
    companions: tuple = ()


# Entry spec: key, coord_labels {label -> coord}, kind, agg, companions,
# int_coords (coord names coerced to int — device indices are integer coords).
_DEFAULT: dict[str, dict] = {
    # --- DCGM-exporter (NVIDIA fleet) ---
    "DCGM_FI_DEV_GPU_UTIL": {
        "key": "hw/gpu/utilization",
        "coord_labels": {"gpu": "gpu"},
        "int_coords": ("gpu",),
        "kind": "gauge",
        "agg": "mean",
        "companions": ("min",),
    },
    "DCGM_FI_DEV_FB_USED": {
        "key": "hw/gpu/memory_used_bytes",
        "coord_labels": {"gpu": "gpu"},
        "int_coords": ("gpu",),
        "kind": "gauge",
        "agg": "max",
    },
    "DCGM_FI_DEV_GPU_TEMP": {
        "key": "hw/gpu/temp",
        "coord_labels": {"gpu": "gpu"},
        "int_coords": ("gpu",),
        "kind": "gauge",
        "agg": "max",
    },
    "DCGM_FI_DEV_POWER_USAGE": {
        "key": "hw/gpu/powerWatts",
        "coord_labels": {"gpu": "gpu"},
        "int_coords": ("gpu",),
        "kind": "gauge",
        "agg": "mean",
    },
    # --- node_exporter (host) ---
    "node_memory_MemAvailable_bytes": {
        "key": "hw/mem/available_bytes",
        "kind": "gauge",
        # min: pressure is the LOWEST headroom in the window ('last' is not in SERVER_AGGS).
        "agg": "min",
    },
    "node_network_transmit_bytes_total": {
        "key": "hw/net/sent_bytes_rate",
        "coord_labels": {"device": "nic"},
        "kind": "counter",
        "agg": "mean",
    },
    "node_network_receive_bytes_total": {
        "key": "hw/net/recv_bytes_rate",
        "coord_labels": {"device": "nic"},
        "kind": "counter",
        "agg": "mean",
    },
    "node_filesystem_avail_bytes": {
        "key": "hw/disk/available_bytes",
        "coord_labels": {"mountpoint": "mount"},
        "kind": "gauge",
        "agg": "min",  # lowest headroom; 'last' is not server-legal
    },
    # --- cAdvisor / kubelet (container-quota truth psutil cannot see) ---
    "container_cpu_usage_seconds_total": {
        "key": "hw/proc/cpu_seconds_rate",
        "kind": "counter",
        "agg": "mean",
    },
    "container_memory_working_set_bytes": {
        "key": "hw/proc/memory_working_set_bytes",
        "kind": "gauge",
        "agg": "max",
    },
    "container_cpu_cfs_throttled_periods_total": {
        "key": "hw/proc/cpu_throttled_periods_rate",
        "kind": "counter",
        "agg": "mean",
    },
}


class MappingPack:
    def __init__(self, table: dict[str, dict]) -> None:
        self._table = table

    @classmethod
    def default(cls) -> MappingPack:
        return cls(dict(_DEFAULT))

    def extend(self, entries: dict[str, dict]) -> MappingPack:
        return MappingPack({**self._table, **entries})

    def resolve(self, name: str, labels: dict[str, str]) -> Mapped | None:
        entry = self._table.get(name)
        if entry is None:
            return None
        coords: dict = {}
        int_coords = entry.get("int_coords", ())
        for label, coord in entry.get("coord_labels", {}).items():
            if label in labels:
                value = labels[label]
                coords[coord] = int(value) if coord in int_coords else value
        return Mapped(
            key=entry["key"],
            coords=coords,
            kind=entry["kind"],
            agg=entry["agg"],
            companions=tuple(entry.get("companions", ())),
        )


class CounterTracker:
    """Per-series cumulative-counter → per-second-rate state.

    The first observation baselines (None). A negative delta means the exporter restarted: None and
    re-baseline, never the naive-delta spike.
    """

    def __init__(self) -> None:
        self._last: dict[str, tuple[float, float]] = {}  # sid -> (raw, ts)

    def observe(self, sid: str, raw: float, ts: float) -> float | None:
        prev = self._last.get(sid)
        self._last[sid] = (raw, ts)
        if prev is None:
            return None
        prev_raw, prev_ts = prev
        delta, dt = raw - prev_raw, ts - prev_ts
        if delta < 0 or dt <= 0:
            return None
        return delta / dt
