from enum import StrEnum

class CreateCheckFixCycleDtoFixStepType0Kind(StrEnum):
    RUN_CONFIG = "run_config"

    def __str__(self) -> str:
        return str(self.value)
