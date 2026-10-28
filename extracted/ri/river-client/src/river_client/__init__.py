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
__version__ = "0.17.0"

from river_client.capacity import CapacityStatus
from river_client.images import ImageHandle
from river_client.client import (
    Client,
    Model,
    Session,
    SessionContext,
)
from river_client.images import ImageStore
from river_client.losses import BuiltinLoss, CustomLoss, Loss
from river_client.metrics import RunMetricsLogger
from river_client.wandb_metrics import inject_metrics
from river_client.tokenizers import (
    MODEL_TOKENIZER_ALIASES,
    load_tokenizer,
    resolve_tokenizer_name,
)
from river_client.types import (
    AuthenticationError,
    AttestedTrainingDataArtifact,
    AutoCheckpointFailedError,
    CapacityError,
    ChatCompleteResult,
    Checkpoint,
    Deployment,
    DeploymentReplicas,
    ExpertRouting,
    ForwardResult,
    LoraConfig,
    ModelNotFoundError,
    OptimStepResult,
    PolicyVersion,
    PolicySpan,
    PendingOp,
    PendingSample,
    RiverConnectionError,
    RiverError,
    SessionHeartbeatError,
    ServerCapabilities,
    RiverTimeoutError,
    Sample,
    TopLogprobs,
    TrainingDataArtifact,
    TrainingDataAttestation,
)

from river_client.sampling import (
    PendingSamplingBatch,
    SamplingCompletion,
    SamplingResultCollector,
)

from river_client import rl

__all__ = [
    "Loss",
    "BuiltinLoss",
    "CustomLoss",
    "ServerCapabilities",
    "ImageHandle",
    "ImageStore",
    "rl",
    "AuthenticationError",
    "AttestedTrainingDataArtifact",
    "AutoCheckpointFailedError",
    "CapacityError",
    "CapacityStatus",
    "ChatCompleteResult",
    "Checkpoint",
    "Client",
    "Deployment",
    "DeploymentReplicas",
    "ExpertRouting",
    "ForwardResult",
    "LoraConfig",
    "Model",
    "MODEL_TOKENIZER_ALIASES",
    "ModelNotFoundError",
    "OptimStepResult",
    "PolicyVersion",
    "PolicySpan",
    "PendingOp",
    "PendingSample",
    "PendingSamplingBatch",
    "SamplingCompletion",
    "SamplingResultCollector",
    "RiverConnectionError",
    "RiverError",
    "SessionHeartbeatError",
    "RiverTimeoutError",
    "RunMetricsLogger",
    "Sample",
    "Session",
    "SessionContext",
    "TopLogprobs",
    "TrainingDataArtifact",
    "TrainingDataAttestation",
    "inject_metrics",
    "load_tokenizer",
    "resolve_tokenizer_name",
]
