from enum import StrEnum

class UpdateQaConfigBodyDtoLauncherTypeType0(StrEnum):
    CLOUD_BATCH = "cloud_batch"
    GKE = "gke"
    MODAL = "modal"

    def __str__(self) -> str:
        return str(self.value)
