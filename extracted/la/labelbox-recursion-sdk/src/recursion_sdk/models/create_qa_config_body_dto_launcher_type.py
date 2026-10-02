from enum import StrEnum

class CreateQaConfigBodyDtoLauncherType(StrEnum):
    CLOUD_BATCH = "cloud_batch"
    GKE = "gke"
    MODAL = "modal"

    def __str__(self) -> str:
        return str(self.value)
