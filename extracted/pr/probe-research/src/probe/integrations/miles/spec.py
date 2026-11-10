"""A Miles run's spec: its `probe.init` arguments (identity, project and experiment, name, config, parent) and links."""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any

from probe.foundation.compat.compat import UTC
from probe.foundation.safe_warn import safe_warn as _diagnostics
from probe.integrations.miles.scrub import _capture_config
from probe.sdk.agent_session import ComposedName

_JOB_ENV_LINKS = {
    "SLURM_JOB_ID": "slurm_job_id",
    "RAY_JOB_ID": "ray_job_id",
    "NEBIUS_CLUSTER_ID": "nebius_cluster_id",
    "NEBIUS_NODE_GROUP_ID": "nebius_node_group_id",
    "NEBIUS_GPU_CLUSTER_ID": "nebius_gpu_cluster_id",
    "KUBERNETES_POD_NAME": "kubernetes_pod_name",
    "KUBERNETES_NAMESPACE": "kubernetes_namespace",
}


def is_frozen_args(args: Any) -> bool:
    """Upstream Miles args are strict pydantic models: no undeclared field, declared ones immutable
    (`utils/args/runtime_base.py:24-27`, `pydantic_utils.py:5`). The fork's are an argparse Namespace."""
    return args is not None and hasattr(type(args), "model_fields")


def set_arg(args: Any, name: str, value: Any) -> None:
    """Publish a value on the fork's mutable args (its Ray actors read it); never write frozen args."""
    if args is not None and not is_frozen_args(args):
        setattr(args, name, value)


def _parse_links(values: list[str] | None) -> dict[str, str]:
    links: dict[str, str] = {}
    for raw in values or []:
        key, separator, value = raw.partition("=")
        if not separator or not key.strip() or not value.strip():
            raise ValueError(f"invalid Probe link {raw!r}; expected KEY=VALUE")
        links[key.strip()] = value.strip()
    return links


def _resolve_run_name(args, external_id: str) -> str:
    configured = (
        getattr(args, "probe_run_name", None)
        or os.environ.get("PROBE_RUN_NAME")
        or getattr(args, "wandb_group", None)
    )
    if configured:
        return str(configured)
    timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    return ComposedName(f"miles-{timestamp}-{external_id.rsplit(':', 1)[-1][:8]}")


def build_run_spec(args, external_id: str) -> dict[str, Any]:
    """`probe.init` arguments for a Miles run, plus its native-run `links` (sent with `run.link`)."""
    links = {"miles_run_id": external_id}
    for attr in ("wandb_run_id", "mlflow_run_id"):
        if value := getattr(args, attr, None):
            links[attr] = str(value)
    for env_name, link_name in _JOB_ENV_LINKS.items():
        if value := os.environ.get(env_name):
            links[link_name] = value
    links.update(_parse_links(getattr(args, "probe_links", None)))
    spec = {
        "project": getattr(args, "probe_project", None) or os.environ.get("PROBE_PROJECT") or "miles",
        # Not "miles": an experiment is a project row, and the two share one slug space.
        "experiment": getattr(args, "probe_experiment", None) or os.environ.get("PROBE_EXPERIMENT") or "miles-runs",
        "question": getattr(
            args,
            "probe_question",
            "Capture Miles training, rollout, and evaluation telemetry.",
        ),
        "name": _resolve_run_name(args, external_id),
        "source": "miles",
        "external_id": external_id,
        "tags": list(
            dict.fromkeys(["miles", *(getattr(args, "probe_tags", None) or [])])
        ),
        "config": _capture_config(args) if args is not None else {},
        "metadata": {
            "integration": "miles",
            "miles_run_id": external_id,
            "capture": {"metrics": "outbox", "samples": "sample_store"},
        },
        "links": links,
    }
    # Lineage. A run produced by this backend previously had no way to say
    # what it came from: `_run_spec` had no parent field and nothing can set
    # one afterwards, so an eval of a training run's checkpoint recorded no
    # edge back to it. `links` is not a substitute -- those become
    # foreign_keys, which a human can follow and a query cannot.
    #
    # client.run() takes **run_kw, so this flows through untouched.
    parent = getattr(args, "probe_parent_run", None) or os.environ.get(
        "PROBE_PARENT_RUN"
    )
    if parent:
        # Server-side enum: fork | resume | retry | branch.
        relation = getattr(args, "probe_parent_relation", None) or os.environ.get(
            "PROBE_PARENT_RELATION"
        )
        if not relation:
            # This block used to set the parent and leave the relation unset,
            # reasoning that none of the four honestly describes "evaluated this
            # run's checkpoint" so nothing should be invented. The reasoning was
            # right and the outcome was not: the SDK defaulted the relation to
            # `fork` one layer down, so the edge was written anyway, with the one
            # word the comment had just rejected.
            #
            # Raised HERE, not in the SDK, so the message names the env var the
            # person actually set rather than surfacing from inside a create call.
            #
            # DEPRECATION: warn for one release, then raise. `PROBE_PARENT_RUN`
            # alone works today (as a mislabeled `fork`), and zero runs in the
            # fleet have used it -- but a launcher may be configured for it, and a
            # working env var must not become a crash without notice.
            # `safe_warn`, never `warnings.warn`: this runs inside `_run_spec`,
            # which the caller wraps in `except Exception -> _handle_error`, so
            # under `-W error` (which several ML harnesses set) a raw warning here
            # would raise and silently disable ALL Probe tracking for the run. That
            # is the failure safe_warn was written for. It also actually reaches
            # the operator -- a DeprecationWarning is ignored by default outside
            # __main__, so the "warn for one release" plan would have shipped no
            # warning at all.
            _diagnostics.warn(
                "probe: PROBE_PARENT_RUN is set without PROBE_PARENT_RELATION. The "
                "relation is currently being guessed as 'fork', which is wrong for "
                "an evaluation run; from the next release this will raise. Set "
                "PROBE_PARENT_RELATION to one of fork|resume|retry|branch. If this "
                "run CONSUMED the parent's output rather than re-attempting it, it "
                "is a lineage edge, not parentage: `probe edge add --relation "
                "consumes` (or evaluates_on / derived_from)."
            )
            relation = "fork"
        spec["parent_run_id"] = str(parent)
        spec["parent_relation"] = str(relation)

    return spec
