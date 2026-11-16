"""Keep sample identity out of the global series catalog; original observation times survive delivery."""

from uuid import UUID

from probe.generated.samples import derive_sample_id
from probe.generated.samples.hardware import GpuReading


class SampleHardwareWriter:
    def __init__(self, run) -> None:
        self._run = run

    def log_readings(self, sample_key: str, readings) -> None:
        sample_id = str(derive_sample_id(UUID(str(self._run.id)), self._run.write_epoch, sample_key))
        for value in readings:
            reading = GpuReading.model_validate(value)
            metrics = {f"rollout/{key}": number for key, number in reading.metrics.items()}
            metrics["rollout/gpu/active_requests"] = reading.active_requests
            self._run.log(metrics, step=None, kind="hardware", wall_clock=reading.wall_clock.isoformat(),
                          dimensions={"host": reading.host, "gpu": reading.device,
                                      "attribution": reading.attribution.value},
                          labels={"sample_id": sample_id, "request_id": reading.request_id})
