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

    @seq.policy(name="my_policy_user", hz=15, gpu="L4", weights="hf://org/checkpoint",
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

from seq import replay, safety
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
from seq.adapter import adapter, adapter_registration
from seq.adapter_cli import adapter_source, adapter_versions
from seq.base import Policy
from seq.benchmark import benchmark
from seq.benchmark_registry import BenchmarkRegistration, benchmark_registration
from seq.deploy import DeploymentHandle, deploy, deployment_request
from seq.errors import (
    AdapterDefinitionError,
    BenchmarkDefinitionError,
    GpuRenderError,
    PolicyDefinitionError,
    SeqAuthoringError,
)
from seq.eval import EvalEstimate, eval
from seq._replay_player.read import read_replay
from seq.image import Image
from seq.usage_hist import gpu_usage
from seq.listing import benchmark_evals, benchmark_io, benchmark_tasks, benchmarks, eval_episodes
from seq.policy import concurrent, policy
from seq.human import ask_human, planner


from seq.settings_cli import policy_set, policy_settings
from seq.robot_cli import robot_add, robot_list, robot_revoke, robot_set
from seq.login_cli import login_list, login_revoke
from seq.key_cli import key_add, key_list, key_revoke, key_set

from seq.billing_cli import billing_credits, billing_details, billing_invoices, billing_plan, billing_top_up

from seq.billing_cli import redeem_promo_code
from seq.person_cli import account_delete, account_person, account_set
from seq.deployments_cli import fork as policy_fork


from seq.logs_cli import policy_logs
from seq.run_logs import benchmark_logs, eval_logs

from seq.machines_cli import robot_status
from seq.params import OneOf, Range
from seq.registry import registration
from seq.secret import Secret
from sequence_base.construct import config
from sequence_base.episode import Episode
from seq.volume import Volume
from seq.volume_upload import storage, volume_files, volume_get, volume_rm
from seq.weights import Weights


from seq.manage_cli import (
    adapter_list,
    adapter_rm,
    audit,
    benchmark_cancel,
    benchmark_rm,
    benchmark_source,
    benchmark_status,
    benchmark_upgrade,
    benchmark_versions,
    eval_cancel,
    eval_list,
    eval_rm,
    eval_report,
    eval_status,
    policy_list,
    policy_rm,
    policy_rollback,
    policy_source,
    policy_start,
    policy_metrics,
    policy_status,
    policy_stop,
    policy_upgrade,
    policy_versions,
    volume_list,
    volume_show,
)



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
    "safety",

    "Camera",

    "Episode",

    "policy",
    "planner",
    "ask_human",
    "concurrent",
    "policy_set",
    "policy_settings",
    "account_delete",
    "account_person",
    "account_set",
    "billing_credits",
    "billing_details",
    "billing_invoices",
    "billing_plan",
    "billing_top_up",
    "redeem_promo_code",
    "robot_add",
    "robot_list",
    "robot_revoke",
    "robot_set",
    "login_list",
    "login_revoke",
    "key_list",
    "key_add",
    "key_set",
    "key_revoke",
    "policy_fork",
    "policy_logs",
    "benchmark_logs",
    "eval_logs",
    "robot_status",
    "benchmark",
    "adapter",

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
    "storage",
    "volume_files",
    "volume_get",
    "volume_rm",
    "Secret",
    "config",

    "Range",
    "OneOf",

    "Replay",
    "replay",
    "RolloutResult",

    "deploy",
    "DeploymentHandle",
    "eval",
    "EvalEstimate",

    "read_replay",

    "benchmarks",
    "benchmark_evals",
    "benchmark_io",

    "benchmark_tasks",
    "eval_episodes",
    "adapter_source",
    "adapter_versions",
    "gpu_usage",
    "DeploymentRequest",
    "DeploymentAccepted",
    "DeploymentState",
    "DeploymentStatusResponse",

    "registration",
    "deployment_request",
    "benchmark_registration",
    "adapter_registration",
    "BenchmarkRegistration",

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

    "SeqAuthoringError",
    "PolicyDefinitionError",
    "BenchmarkDefinitionError",
    "AdapterDefinitionError",

    "GpuRenderError",

    "policy_list", "policy_metrics", "policy_status", "policy_stop", "policy_start", "policy_rm", "policy_upgrade", "policy_versions",
    "policy_rollback", "policy_source",
    "benchmark_status", "benchmark_cancel", "benchmark_rm", "benchmark_upgrade", "benchmark_versions",
    "benchmark_source",
    "eval_status", "eval_report", "eval_cancel", "eval_list", "eval_rm",
    "adapter_list", "adapter_rm",
    "volume_list", "volume_show",
    "audit",
]
