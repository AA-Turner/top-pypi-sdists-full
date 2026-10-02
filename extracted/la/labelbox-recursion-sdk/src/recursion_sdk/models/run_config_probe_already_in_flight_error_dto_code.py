from enum import StrEnum

class RunConfigProbeAlreadyInFlightErrorDtoCode(StrEnum):
    RUN_CONFIG_PROBE_ALREADY_IN_FLIGHT = "run_config_probe_already_in_flight"

    def __str__(self) -> str:
        return str(self.value)
