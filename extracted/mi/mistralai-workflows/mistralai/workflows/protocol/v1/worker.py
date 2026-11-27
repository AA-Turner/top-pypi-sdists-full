from enum import StrEnum

from pydantic import BaseModel, Field


class PayloadEncryptionLevel(StrEnum):
    """How much of a worker's payloads are encrypted, ordered from weakest to strongest."""

    NONE = "none"
    PARTIAL = "partial"
    FULL = "full"

    def satisfies(self, required: "PayloadEncryptionLevel") -> bool:
        return _ENCRYPTION_LEVEL_RANK[self] >= _ENCRYPTION_LEVEL_RANK[required]


_ENCRYPTION_LEVEL_RANK = {
    PayloadEncryptionLevel.NONE: 0,
    PayloadEncryptionLevel.PARTIAL: 1,
    PayloadEncryptionLevel.FULL: 2,
}


class WorkerFeatures(BaseModel):
    """Server-resolved feature flags applied to worker configuration at startup.

    `None` means the server has no opinion and the worker's own default stands — which is also what
    an absent field yields, so an SDK newer than the API keeps behaving as it does today. Keeping
    "no opinion" distinct from an explicit `False` is what lets a flag's SDK default change later
    without a server that predates the change silently overriding it.
    """

    upload_graph: bool | None = None
    events_api_version: str | None = None


class WorkerInfo(BaseModel):
    scheduler_url: str
    namespace: str
    tls: bool = False
    features: WorkerFeatures = Field(default_factory=WorkerFeatures)
    required_payload_encryption_mode: PayloadEncryptionLevel = Field(
        default=PayloadEncryptionLevel.NONE,
        description="Minimum payload encryption mode the server accepts from workers",
    )


class ExecutorIdentityResult(BaseModel):
    customer_id: str
    workspace_id: str
    user_id: str | None = None
    organization_id: str | None = None


class ExecutorIdentityTokenResult(BaseModel):
    token: str
