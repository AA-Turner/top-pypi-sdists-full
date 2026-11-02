"""Publish one split through the InstanceRepo SDK's benchmark-release workflow."""

from __future__ import annotations

import math
import sys
from typing import Optional

import typer

from .dataset_commands import _emit_detail, _fail, _fmt

#: SDK 等待循环返回后不再变化的状态;其余视为等待超时。
_TERMINAL = ("succeeded", "failed", "canceled", "awaiting_approval")


def dataset_split_publish(
    split: str = typer.Argument(..., help="One complete split to publish"),
    dataset: str = typer.Option(..., "--dataset", help="Dataset name (L1 or L1/L2)"),
    version: Optional[str] = typer.Option(None, "--version", help="Omit for a version-less split"),
    overwrite: bool = typer.Option(
        False, "--overwrite", help="Allow replacing destination objects"
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Confirm publishing this split to online"),
    no_wait: bool = typer.Option(False, "--no-wait", help="Submit without polling"),
    wait_timeout: Optional[float] = typer.Option(
        None, "--wait-timeout", help="Wait limit in seconds"
    ),
    output_format: Optional[str] = typer.Option(None, "--format", help="plain/table/json/yaml"),
):
    """Publish a complete split to online; source and target paths are SDK/server derived."""
    from .irepo_sdk import SdkMissing, _reason, load_repo

    fmt = _fmt(output_format)
    dataset, split, resolved_version = dataset.strip(), split.strip(), (version or "").strip()
    if no_wait and wait_timeout is not None:
        raise _fail(
            "--no-wait and --wait-timeout are mutually exclusive",
            "Choose only one waiting mode",
            exit_code=2,
        )
    timeout = 1800.0 if wait_timeout is None else wait_timeout
    if not math.isfinite(timeout) or timeout <= 0:
        raise _fail(
            "--wait-timeout must be a positive finite number",
            "Set the wait limit in seconds",
            exit_code=2,
        )
    if not dataset or not split or any(p in ("", ".", "..") for p in dataset.split("/")):
        raise _fail(
            "dataset and split must not be empty or contain empty path segments",
            "Provide a dataset and a complete split",
            2,
        )

    if not yes:
        if not sys.stdin.isatty():
            raise _fail(
                "Non-interactive publish requires confirmation",
                "Add --yes to confirm publishing this split to online",
                2,
            )
        target = (
            f"{dataset}/{resolved_version}/{split}" if resolved_version else f"{dataset}/{split}"
        )
        if not typer.confirm(f"Publish {target} to online?"):
            raise _fail("Publish canceled; no workflow submitted", "Rerun after confirming", 1)

    try:
        repo = load_repo()
    except SdkMissing as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(2) from exc

    # 源目录由 SDK 按 repo 配置(dataset/version/split 布局)推导,与 instance push 的
    # 落盘一致;目标路径由服务端从 online Dataset base 派生。
    src_bucket = (getattr(repo.profile, "oss_bucket", "") or "").strip()
    if not src_bucket:
        raise _fail(
            "Publish failed: the current AP cluster does not provide data-plane storage config (oss_bucket)",
            "Make sure AP_CLUSTER points to a dataset-enabled cluster, or contact the Dataset admin",
        )

    try:
        workflow = repo.versions.publish(
            dataset,
            resolved_version,
            split=split,
            metadata_model="split_first",
            overwrite=overwrite,
            # dataset_distributions 协议下服务端自行派生目标;SDK 的守卫仍要求
            # target_overrides 提供 oss_bucket,传源桶仅为过守卫,不影响请求体。
            target_overrides={"oss_bucket": src_bucket},
            approval_mode="internal",
            wait_approval=False,
            raise_on_failure=False,
            # timeout_sec=0 时 SDK 的等待循环一次都不进,等效"只提交不轮询"。
            timeout_sec=0.0 if no_wait else timeout,
        )
    except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
        raise _fail(
            f"Publish failed: {_reason(exc)}",
            "Rerunning the same command is safe (the SDK generates an idempotency key from content); "
            "check an already-submitted publish with ap dataset split publish-status <workflow-id>",
        ) from exc

    workflow = workflow if isinstance(workflow, dict) else {}
    workflow_id = str(workflow.get("id") or "")
    if not workflow_id:
        raise _fail(
            "Publish response is missing the workflow id", "Rerunning the same command is safe"
        )
    hint = f"ap dataset split publish-status {workflow_id}"
    _emit_detail(workflow, fmt)

    status = str(workflow.get("status") or "")
    if status in ("failed", "canceled"):
        raise _fail(
            f"Publish workflow {workflow_id} {status}: {workflow.get('error_msg') or ''}",
            "Inspect steps and outputs in the output, fix the failure, then submit the publish again",
        )
    if no_wait:
        return
    if status not in _TERMINAL:
        # 等待窗口内未到终态:SDK 返回最后一帧,服务端工作流不受影响。
        raise _fail("Publish wait timed out; the server-side workflow keeps running", hint)


def dataset_split_publish_status(
    workflow_id: str = typer.Argument(..., help="Release workflow id"),
    output_format: Optional[str] = typer.Option(None, "--format", help="plain/table/json/yaml"),
):
    """Show release progress, approval details and errors without submitting a new release."""
    from .dataset_commands import _model_dict
    from .instance_commands import _load_repo_or_exit
    from .irepo_sdk import _reason

    fmt = _fmt(output_format)
    try:
        workflow = _model_dict(_load_repo_or_exit().workflows.get(workflow_id))
    except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
        raise _fail(
            f"Failed to query publish progress: {_reason(exc)}",
            "Check the workflow id and current cluster",
        ) from exc
    _emit_detail(workflow, fmt)
    status = str((workflow or {}).get("status") or "")
    if status in ("failed", "canceled"):
        raise _fail(
            f"Publish workflow {workflow_id} {status}: {(workflow or {}).get('error_msg') or ''}",
            "Inspect steps and outputs in the output, fix the failure, then submit the publish again",
        )
