"""
`seq` — write a robot policy or a benchmark, then deploy and evaluate it on the platform.

In one sentence: you decorate a class (`@seq.policy` or `@seq.benchmark`) with what it needs — GPU, image, weights —
→ `seq deploy [folder]` (or `seq.deploy(Cls)`) sends that declaration and the folder its code is in to the platform,
which builds and serves it → `seq eval run` (or `seq.eval(...)`) scores a deployed policy on a registered benchmark, on the platform.
Nothing is built or run on this machine.

WHY this is a separate package from the `sequence_ai` client: the client is deliberately httpx-only and installs on a
Python 3.9 robot, while authoring needs pydantic (through `sequence_base`) and Python 3.10+. Both ship in the one
`sequence-ai` distribution; on 3.9 only the client is installed.

Usage::

    import seq

    @seq.policy(name="my_policy_user", hz=15, weights="hf://org/checkpoint",
                init={"weights_dir": "{weights}"})
    class MyPolicy_user(seq.Policy):
        def __init__(self, weights_dir): ...              # loads the model: init= hands it the weights directory
        @seq.infer
        def infer_user(self, inputs, *, seed=None): ...   # takes and returns whatever the robot's own code sends

    reg_user = seq.registration(MyPolicy_user)            # -> sequence_base.PolicyRegistration

The registration is a `sequence_base.PolicyRegistration` — a harness importing ONLY `sequence_base` reads it
back without importing `seq`.
"""
from __future__ import annotations

from seq import safety
from seq._partial import (
    action,
    infer,
    observation,
    observe,
    on_episode,
    plan,
    reset,
    sample,
    shutdown,
    step,
)
from seq.base import Policy
from seq.errors import (
    AdapterDefinitionError,
    BenchmarkDefinitionError,
    GpuRenderError,
    PolicyDefinitionError,
    SeqAuthoringError,
)
from seq.image import Image
from seq.policy import concurrent, policy
from seq.human import ask_human
from seq.params import OneOf, Range
from seq.registry import registration
from seq.secret import Secret
from sequence_base.construct import config
from sequence_base.episode import Episode
from seq.volume import Volume
from seq.weights import Weights



from sequence_base.contract import (
    Camera,
    BenchmarkSpec,
    DeploymentAccepted,
    DeploymentRequest,
    DeploymentState,
    DeploymentStatusResponse,
    Estimate,
    EvalReport,
    EvalStatus,
    MetricAgg,
    PolicyRegistration,
    PolicySpec,
    ReplaySpec,
    RolloutResult,
    SeqFlags,
    TaskAgg,
)



Replay = ReplaySpec

__all__ = [
    "AdapterDefinitionError",
    "BenchmarkDefinitionError",
    "GpuRenderError",
    "PolicyDefinitionError",
    "SeqAuthoringError",
    "safety",
    "Camera",
    "Episode",
    "policy",
    "ask_human",
    "concurrent",
    "infer",
    "observe",
    "on_episode",
    "sample",
    "shutdown",
    "plan",
    "reset",
    "step",
    "observation",
    "action",
    "Policy",
    "Image",
    "Volume",
    "Weights",
    "Secret",
    "config",
    "Range",
    "OneOf",
    "Replay",
    "RolloutResult",
    "DeploymentRequest",
    "DeploymentAccepted",
    "DeploymentState",
    "DeploymentStatusResponse",
    "registration",
    "PolicyRegistration",
    "PolicySpec",
    "SeqFlags",
    "BenchmarkSpec",
    "ReplaySpec",
    "Estimate",
    "EvalReport",
    "EvalStatus",
    "MetricAgg",
    "TaskAgg",
]





_CLOUD_NAMES = frozenset({
    "BenchmarkRegistration",
    "DeploymentHandle",
    "EvalEstimate",
    "account_delete",
    "account_person",
    "account_set",
    "adapter",
    "adapter_list",
    "adapter_registration",
    "adapter_rm",
    "adapter_source",
    "adapter_versions",
    "audit",
    "benchmark",
    "benchmark_cancel",
    "benchmark_evals",
    "benchmark_io",
    "benchmark_logs",
    "benchmark_registration",
    "benchmark_rm",
    "benchmark_source",
    "benchmark_status",
    "benchmark_tasks",
    "benchmark_upgrade",
    "benchmark_versions",
    "benchmarks",
    "billing_credits",
    "billing_details",
    "billing_invoices",
    "billing_plan",
    "billing_top_up",
    "deploy",
    "deployment_request",
    "eval",
    "eval_cancel",
    "eval_episodes",
    "eval_list",
    "eval_logs",
    "eval_report",
    "eval_rm",
    "eval_status",
    "gpu_add",
    "gpu_allow",
    "gpu_history",
    "gpu_list",
    "gpu_places",
    "gpu_remove",
    "gpu_save",
    "gpu_saved",
    "gpu_saved_remove",
    "gpu_ssh",
    "gpu_usage",
    "key_add",
    "key_list",
    "key_revoke",
    "key_set",
    "login_list",
    "login_revoke",
    "policy_fork",
    "policy_list",
    "policy_logs",
    "policy_metrics",
    "policy_rm",
    "policy_rollback",
    "policy_set",
    "policy_settings",
    "policy_source",
    "policy_start",
    "policy_status",
    "policy_stop",
    "policy_upgrade",
    "policy_versions",
    "read_replay",
    "redeem_promo_code",
    "replay",
    "robot_add",
    "robot_create",
    "robot_key",
    "robot_list",
    "robot_revoke",
    "robot_rm",
    "robot_set",
    "robot_show",
    "storage",
    "volume_files",
    "volume_get",
    "volume_list",
    "volume_rm",
    "volume_show",
})


def __getattr__(name: str):
    """The names sequence-cloud adds to `seq` (its `seq.api` entry point's __all__: seq.deploy, seq.benchmark, ...), and
    the sentence each of the platform's says without it. A submodule's name is never looked up: `from seq import
    columns` asks this before it imports seq.columns, and loading sequence-cloud from inside one of its own modules'
    imports would import that module again, half made."""
    import importlib.util

    from sequence_ai._core.plugins import first, needs_cloud






    if name in _CLOUD_NAMES:
        api = first("seq.api")
        if api is not None and name in getattr(api, "__all__", ()):
            return getattr(api, name)
        raise AttributeError(needs_cloud(f"seq.{name}"))

    spec = None if name.startswith("__") else importlib.util.find_spec(f"{__name__}.{name}")
    if name.startswith("__") or (spec is not None and spec.origin is not None):
        raise AttributeError(f"module 'seq' has no attribute {name!r}")
    api = first("seq.api")
    if api is not None and name in getattr(api, "__all__", ()):
        return getattr(api, name)
    raise AttributeError(f"module 'seq' has no attribute {name!r}")


def __dir__() -> list[str]:
    from sequence_ai._core.plugins import first

    api = first("seq.api")
    return sorted(set(globals()) | set(getattr(api, "__all__", ()) if api is not None else ()))
