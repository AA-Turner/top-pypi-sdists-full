"""The psutil floor: CPU, memory, disk, network anywhere, plus a cgroup-v2 quota reader so containers
report percent-of-quota, not percent-of-host, even with the kubelet scrape off.
"""

from __future__ import annotations

import socket
from pathlib import Path

from probe.sdk.hardware.mappings import CounterTracker
from probe.sdk.hardware.types import HwSample


class SystemResource:
    def __init__(self, psutil_mod, cgroup_root: str) -> None:
        self._psutil = psutil_mod
        self._cgroup = Path(cgroup_root)
        self._counters = CounterTracker()
        # psutil's first non-blocking cpu_percent() is a meaningless 0.0: take it now so the first
        # sample (a sub-minute run's only one) measures the run.
        try:
            psutil_mod.cpu_percent(interval=None)
        except Exception:  # noqa: BLE001 -- a source never fails its creation
            pass

    @classmethod
    def create(cls, cgroup_root: str = "/sys/fs/cgroup"):
        try:
            import psutil  # lazy: absence disables the source, never errors
        except ImportError:
            return None
        return cls(psutil, cgroup_root)

    def probe(self) -> dict:
        return {
            "cpu_count": self._psutil.cpu_count(logical=True) or 1,
            "memory_total_bytes": self._psutil.virtual_memory().total,
            "hostname": socket.gethostname(),
        }

    def sample(self, ts: float) -> list[HwSample]:
        samples: list[HwSample] = []
        # Non-blocking: percent since the previous call (first call baselines at 0.0).
        cpu = self._psutil.cpu_percent(interval=None)
        samples.append(HwSample("hw/cpu/utilization", float(cpu), {}, "mean", ("min",)))
        samples.append(
            HwSample(
                "hw/mem/used_percent",
                float(self._psutil.virtual_memory().percent),
                {},
                "max",
            )
        )
        try:
            usage = self._psutil.disk_usage("/")
            samples.append(
                HwSample("hw/disk/used_percent", float(usage.percent), {"mount": "/"}, "max")
            )
        except OSError:
            pass

        net = self._psutil.net_io_counters()
        for sid, key, raw in (
            ("net.sent", "hw/net/sent_bytes_rate", net.bytes_sent),
            ("net.recv", "hw/net/recv_bytes_rate", net.bytes_recv),
        ):
            rate = self._counters.observe(sid, float(raw), ts)
            if rate is not None:
                samples.append(HwSample(key, rate, {}, "mean"))

        samples.extend(self._cgroup_quota_samples())
        return samples

    def _cgroup_quota_samples(self) -> list[HwSample]:
        samples: list[HwSample] = []
        mem_max = self._read(self._cgroup / "memory.max")
        mem_cur = self._read(self._cgroup / "memory.current")
        if mem_max and mem_max != "max" and mem_cur:
            limit = float(mem_max)
            if limit > 0:
                samples.append(
                    HwSample(
                        "hw/mem/quota_used_percent",
                        float(mem_cur) / limit * 100.0,
                        {},
                        "max",
                    )
                )
        cpu_max = self._read(self._cgroup / "cpu.max")
        if cpu_max:
            parts = cpu_max.split()
            if len(parts) == 2 and parts[0] != "max":
                quota, period = float(parts[0]), float(parts[1])
                if period > 0:
                    # A constant reduces exactly under mean ('last' is not in SERVER_AGGS).
                    samples.append(
                        HwSample("hw/cpu/quota_cores", quota / period, {}, "mean")
                    )
        return samples

    @staticmethod
    def _read(path: Path) -> str | None:
        try:
            return path.read_text().strip()
        except OSError:
            return None
