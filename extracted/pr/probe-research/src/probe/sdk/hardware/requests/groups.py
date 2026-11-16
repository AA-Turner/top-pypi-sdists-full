"""GpuRequestGroups: one `GpuRequests` sampler per device group a serving process runs requests on (a DP group's
GPUs, verl's routed TP group), so a request only ever holds readings of the GPUs that served it."""

from __future__ import annotations

from collections.abc import Callable

from .requests import GpuRequests


class GpuRequestGroups:
    """Samplers by device group (a `CUDA_VISIBLE_DEVICES`-style list, the group's key), made on first use."""

    def __init__(self, create: Callable[[str | None], GpuRequests] | None = None) -> None:
        self._create = create or (lambda devices: GpuRequests(visible_devices=devices))
        self._groups: dict[str | None, GpuRequests] = {}

    def get(self, devices: str | None) -> GpuRequests:
        """The sampler for ``devices`` (None: every device this process sees)."""
        found = self._groups.get(devices)
        if found is None:
            found = self._groups[devices] = self._create(devices)
        return found

    async def close(self) -> None:
        for requests in list(self._groups.values()):
            await requests.close()
        self._groups.clear()
