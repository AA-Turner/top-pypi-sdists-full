"""River Python client for ML training API.

Example usage:

    import river_client as river

    client = river.Client(api_key="...", endpoint="api.river.ai")

    # Stateless sampling from base model
    samples = client.sample(
        "What is 2+2?",
        base_model="Qwen/Qwen3.6-35B-A3B-FP8",
        max_tokens=50,
    )
    print(samples[0].text)

    # Training with session
    with client.session() as session:
        model = session.create_model(
            base_model="Qwen/Qwen3.6-35B-A3B-FP8",
            lora=river.LoraConfig(rank=16)
        )

        # Training loop
        result = model.forward_backward(data, loss_fn="cross_entropy")
        model.optim_step(lr=1e-4)

        # Sample from current weights
        sample_groups = model.sample("Continue:", max_tokens=100)
"""

# Defined before the submodule imports below: `river_client.client` reads it
# during package initialization to build the client identifier it sends to
# the server, so it must exist on the partially-initialized module. Also the
# version source for hatch (`[tool.hatch.version]` in pyproject.toml) and
# the release-tag guard in `.github/workflows/river-client-release.yml`.
__version__ = "0.9.1"

from river_client.client import (
    Client,
    Model,
    Session,
    SessionContext,
)
from river_client.metrics import RunMetricsLogger
from river_client.tokenizers import (
    MODEL_TOKENIZER_ALIASES,
    load_tokenizer,
    resolve_tokenizer_name,
)
from river_client.types import (
    AuthenticationError,
    AttestedTrainingDataArtifact,
    CapacityError,
    ChatCompleteResult,
    Checkpoint,
    ExpertRouting,
    ForwardResult,
    LoraConfig,
    ModelNotFoundError,
    OptimStepResult,
    PendingOp,
    PendingSample,
    PromotedStreamingReplica,
    RiverConnectionError,
    RiverError,
    SessionHeartbeatError,
    RiverTimeoutError,
    Sample,
    TrainingDataArtifact,
    TrainingDataAttestation,
)

__all__ = [
    "AuthenticationError",
    "AttestedTrainingDataArtifact",
    "CapacityError",
    "ChatCompleteResult",
    "Checkpoint",
    "Client",
    "ExpertRouting",
    "ForwardResult",
    "LoraConfig",
    "Model",
    "MODEL_TOKENIZER_ALIASES",
    "ModelNotFoundError",
    "OptimStepResult",
    "PendingOp",
    "PendingSample",
    "PromotedStreamingReplica",
    "RiverConnectionError",
    "RiverError",
    "SessionHeartbeatError",
    "RiverTimeoutError",
    "RunMetricsLogger",
    "Sample",
    "Session",
    "SessionContext",
    "TrainingDataArtifact",
    "TrainingDataAttestation",
    "load_tokenizer",
    "resolve_tokenizer_name",
]
