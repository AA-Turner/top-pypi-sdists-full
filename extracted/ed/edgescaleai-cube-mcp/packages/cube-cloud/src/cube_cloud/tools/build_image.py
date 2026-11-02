"""Remote (daemonless) container image builds via a one-shot kaniko ECS task.

Three tools implement an async submit -> poll contract, because a real build
(with RUN steps) far exceeds the 120s agent<->cloud transport timeout:

  build_image_prepare(image_name, tag)      -> {job_id, upload_url, s3_key}
  build_image_start(job_id, dockerfile, ...) -> {job_id, task_arn, state}
  build_image_status(job_id)                 -> {state, image_uri?, logs_tail?}

Flow: the agent tars its build context and PUTs it to a presigned S3 URL, then
starts the build. `start` mints an ACR push token *server-side* (so it never
leaves the cloud), writes it into the kaniko task's docker config via a command
override, and RunTask's the kaniko task-def (see infra/terraform/build.tf). The
image is pinned to linux/amd64. Job state lives in a DynamoDB table so status
survives across the stateless MCP calls.

Everything AWS-facing is validated end-to-end by scripts/validate-kaniko-build.sh.
"""

from __future__ import annotations

import base64
import json
import logging
import shlex
import time
import uuid

import boto3
from botocore.exceptions import ClientError

from cube_common.apollo_client import ApolloClient
from cube_common.config import ACR_DOCKER_PREFIX, ACR_REGISTRY
from cube_cloud.config import settings

logger = logging.getLogger(__name__)

# awslogs-stream-prefix on the kaniko container (see build.tf); the Fargate
# log stream is "<prefix>/<container-name>/<task-id>".
_LOG_STREAM_PREFIX = "kaniko"

_PENDING = {"PROVISIONING", "PENDING", "ACTIVATING"}
_TERMINAL = {"DEACTIVATING", "STOPPING", "DEPROVISIONING", "STOPPED"}


def _err(msg: str) -> str:
    return json.dumps({"error": msg})


def _config_ready() -> str | None:
    missing = [
        n for n in ("build_ctx_bucket", "build_jobs_table", "kaniko_cluster",
                    "kaniko_task_def", "build_subnets", "build_security_group",
                    "kaniko_log_group")
        if not getattr(settings, n)
    ]
    if missing:
        return f"Remote build is not configured (missing: {', '.join(missing)})."
    return None


def _jobs_table():
    return boto3.resource("dynamodb", region_name=settings.aws_region).Table(settings.build_jobs_table)


def _get_job(job_id: str) -> dict | None:
    try:
        return _jobs_table().get_item(Key={"job_id": job_id}).get("Item")
    except ClientError as e:
        logger.error("build_jobs get_item failed: %s", e)
        return None


# ---------------------------------------------------------------------------
# prepare
# ---------------------------------------------------------------------------

async def build_image_prepare(image_name: str, tag: str) -> str:
    """Create a build job and return a presigned S3 URL for the context upload."""
    if cfg_err := _config_ready():
        return _err(cfg_err)
    if not image_name or "/" in image_name or ":" in image_name:
        return _err("image_name must be a bare name (no '/' or ':').")
    if not tag or "/" in tag:
        return _err("tag must be non-empty and contain no '/'.")

    job_id = uuid.uuid4().hex
    s3_key = f"contexts/{job_id}.tar.gz"
    image_uri = f"{ACR_DOCKER_PREFIX}/{image_name}:{tag}"

    try:
        upload_url = boto3.client("s3", region_name=settings.aws_region).generate_presigned_url(
            "put_object",
            Params={"Bucket": settings.build_ctx_bucket, "Key": s3_key},
            ExpiresIn=settings.build_upload_url_ttl_seconds,
        )
    except ClientError as e:
        return _err(f"could not presign upload URL: {e}")

    now = int(time.time())
    try:
        _jobs_table().put_item(Item={
            "job_id": job_id,
            "state": "PENDING",
            "image_name": image_name,
            "tag": tag,
            "image_uri": image_uri,
            "s3_key": s3_key,
            "created_at": now,
            "expiry": now + settings.build_job_ttl_seconds,
        })
    except ClientError as e:
        return _err(f"could not create build job: {e}")

    return json.dumps({"job_id": job_id, "upload_url": upload_url, "s3_key": s3_key})


# ---------------------------------------------------------------------------
# start
# ---------------------------------------------------------------------------

async def build_image_start(
    client: ApolloClient,
    job_id: str,
    dockerfile: str = "Dockerfile",
    target: str | None = None,
    build_args: dict[str, str] | None = None,
    platform: str = "linux/amd64",
) -> str:
    """Launch the kaniko build task for a prepared job."""
    if cfg_err := _config_ready():
        return _err(cfg_err)

    job = _get_job(job_id)
    if not job:
        return _err(f"unknown job_id: {job_id}")
    image_uri = job["image_uri"]
    s3_key = job["s3_key"]

    # Mint the ACR push token server-side and inject it as the kaniko docker
    # config; it never leaves the cloud.
    token = await client.get_token()
    auth = base64.b64encode(f"apollo:{token}".encode()).decode()
    docker_config = json.dumps({"auths": {ACR_REGISTRY: {"auth": auth}}})

    executor = [
        "/kaniko/executor",
        f"--context=s3://{settings.build_ctx_bucket}/{s3_key}",
        f"--dockerfile={dockerfile}",
        f"--destination={image_uri}",
        f"--custom-platform={platform}",
    ]
    if target:
        executor.append(f"--target={target}")
    for k, v in (build_args or {}).items():
        if "=" in k:
            return _err(f"invalid build-arg name '{k}': must not contain '='")
        executor.append(f"--build-arg={k}={v}")

    # Runs under the task-def entryPoint ["/busybox/sh","-c"]. $DOCKER_CONFIG_JSON
    # is expanded inside the container from the env override below.
    executor_str = " ".join(shlex.quote(a) for a in executor)
    command = f'printf %s "$DOCKER_CONFIG_JSON" > /kaniko/.docker/config.json && {executor_str}'

    try:
        resp = boto3.client("ecs", region_name=settings.aws_region).run_task(
            cluster=settings.kaniko_cluster,
            launchType="FARGATE",
            taskDefinition=settings.kaniko_task_def,
            count=1,
            networkConfiguration={"awsvpcConfiguration": {
                "subnets": [s for s in settings.build_subnets.split(",") if s],
                "securityGroups": [settings.build_security_group],
                # Default VPC has no NAT/endpoints — the task needs a public IP
                # to reach ECR/S3/ACR, or it hangs until timeout.
                "assignPublicIp": "ENABLED",
            }},
            overrides={"containerOverrides": [{
                "name": settings.kaniko_container,
                "command": [command],
                "environment": [
                    {"name": "DOCKER_CONFIG_JSON", "value": docker_config},
                    {"name": "AWS_REGION", "value": settings.aws_region},
                ],
            }]},
        )
    except ClientError as e:
        return _err(f"RunTask failed: {e}")

    failures = resp.get("failures") or []
    if failures or not resp.get("tasks"):
        return _err(f"RunTask returned no task: {failures or 'unknown reason'}")

    task_arn = resp["tasks"][0]["taskArn"]
    try:
        _jobs_table().update_item(
            Key={"job_id": job_id},
            UpdateExpression="SET #s = :s, task_arn = :t",
            ExpressionAttributeNames={"#s": "state"},
            ExpressionAttributeValues={":s": "RUNNING", ":t": task_arn},
        )
    except ClientError as e:
        logger.error("build_jobs update after RunTask failed: %s", e)

    return json.dumps({"job_id": job_id, "task_arn": task_arn, "state": "RUNNING"})


# ---------------------------------------------------------------------------
# status
# ---------------------------------------------------------------------------

def _log_tail(task_arn: str, limit: int = 80) -> str:
    task_id = task_arn.rsplit("/", 1)[-1]
    stream = f"{_LOG_STREAM_PREFIX}/{settings.kaniko_container}/{task_id}"
    try:
        ev = boto3.client("logs", region_name=settings.aws_region).get_log_events(
            logGroupName=settings.kaniko_log_group,
            logStreamName=stream,
            startFromHead=False,
            limit=limit,
        )
        return "\n".join(e["message"] for e in ev.get("events", []))
    except ClientError as e:
        logger.warning("could not fetch kaniko logs (%s): %s", stream, e)
        return ""


def _save_terminal(job_id: str, state: str, exit_code, reason: str, logs: str) -> None:
    try:
        _jobs_table().update_item(
            Key={"job_id": job_id},
            UpdateExpression="SET #s = :s, exit_code = :e, stopped_reason = :r, logs_tail = :l",
            ExpressionAttributeNames={"#s": "state"},
            ExpressionAttributeValues={
                ":s": state, ":e": exit_code if exit_code is not None else -1,
                ":r": reason or "", ":l": logs,
            },
        )
    except ClientError as e:
        logger.error("build_jobs terminal update failed: %s", e)


async def build_image_status(job_id: str) -> str:
    """Poll a build job: PENDING | RUNNING | SUCCEEDED | FAILED."""
    if cfg_err := _config_ready():
        return _err(cfg_err)

    job = _get_job(job_id)
    if not job:
        return _err(f"unknown job_id: {job_id}")

    # Cached terminal result (also survives the task aging out of ECS).
    if job.get("state") in ("SUCCEEDED", "FAILED"):
        out = {"state": job["state"], "logs_tail": job.get("logs_tail", "")}
        if job["state"] == "SUCCEEDED":
            out["image_uri"] = job["image_uri"]
        else:
            out["stopped_reason"] = job.get("stopped_reason", "")
        return json.dumps(out)

    task_arn = job.get("task_arn")
    if not task_arn:
        return json.dumps({"state": job.get("state", "PENDING")})

    try:
        resp = boto3.client("ecs", region_name=settings.aws_region).describe_tasks(
            cluster=settings.kaniko_cluster, tasks=[task_arn]
        )
    except ClientError as e:
        return _err(f"DescribeTasks failed: {e}")

    tasks = resp.get("tasks") or []
    if not tasks:
        # Task aged out before we recorded a terminal state; report last known.
        return json.dumps({"state": job.get("state", "RUNNING")})

    task = tasks[0]
    last = task.get("lastStatus", "")
    containers = task.get("containers") or [{}]
    exit_code = containers[0].get("exitCode")
    reason = task.get("stoppedReason", "")

    if last in _PENDING:
        return json.dumps({"state": "PENDING"})
    if last == "RUNNING":
        return json.dumps({"state": "RUNNING"})
    if last in _TERMINAL:
        logs = _log_tail(task_arn)
        if exit_code == 0:
            _save_terminal(job_id, "SUCCEEDED", 0, reason, logs)
            return json.dumps({"state": "SUCCEEDED", "image_uri": job["image_uri"], "logs_tail": logs})
        _save_terminal(job_id, "FAILED", exit_code, reason, logs)
        return json.dumps({
            "state": "FAILED", "exit_code": exit_code if exit_code is not None else -1,
            "stopped_reason": reason, "logs_tail": logs,
        })

    return json.dumps({"state": "RUNNING"})
