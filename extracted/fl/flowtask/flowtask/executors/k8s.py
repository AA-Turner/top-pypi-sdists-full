# Copyright (C) 2018-present Jesus Lara
#
"""Kubernetes job executor for the flowtask executor framework."""
from __future__ import annotations
import asyncio
import uuid
from typing import Any, Optional
from flowtask.executors.base import AbstractJobExecutor
from flowtask.executors.models import (
    ExecutorConfig,
    ExecutorType,
    ExecutionHandle,
    TaskResult,
)
from flowtask.executors.events import ExecutorLifecyclePublisher
from flowtask.executors.exceptions import ExecutorConnectionError, ExecutorError
from flowtask.executors.registry import register_executor

try:
    import kr8s
    from kr8s.asyncio import Api
    from kr8s.objects import Job
    _KR8S_AVAILABLE = True
except ImportError:
    _KR8S_AVAILABLE = False


def _require_kr8s() -> None:
    """Raise ImportError if kr8s is not installed.

    Raises:
        ImportError: If kr8s is not available.
    """
    if not _KR8S_AVAILABLE:
        raise ImportError(
            "kr8s is required for K8sJobExecutor. "
            "Install it with: pip install flowtask[k8s]"
        )


@register_executor("k8s")
class K8sJobExecutor(AbstractJobExecutor):
    """Launches flowtask tasks as ephemeral Kubernetes Jobs via kr8s.

    Uses the active kubeconfig context for cluster selection.  The Job
    manifest uses ``restartPolicy: Never`` and ``backoffLimit: 0`` to ensure
    each task runs exactly once.

    Image defaults to ``DOCKER_IMAGE`` from conf.py; namespace defaults to
    ``K8S_NAMESPACE``.  Both are overridable via ``ExecutorConfig``.

    Args:
        config: ExecutorConfig with ``type=K8S``.
        **kwargs: Passed through to the base constructor.
    """

    def __init__(self, config: ExecutorConfig, **kwargs) -> None:
        super().__init__(config, **kwargs)
        self._api: Optional[Any] = None
        self._publisher = ExecutorLifecyclePublisher()

    @classmethod
    def name(cls) -> str:
        """Return registry name.

        Returns:
            ``"k8s"``
        """
        return "k8s"

    async def _get_api(self):
        """Return (or lazily create) the kr8s API client.

        Returns:
            An kr8s asyncio Api instance.

        Raises:
            ExecutorConnectionError: If the K8s cluster is unreachable.
        """
        _require_kr8s()
        if self._api is None:
            try:
                self._api = await Api()
            except Exception as exc:
                raise ExecutorConnectionError(
                    f"Cannot connect to Kubernetes cluster: {exc}"
                ) from exc
        return self._api

    def _image(self) -> str:
        """Return container image.

        Returns:
            Config image or global DOCKER_IMAGE fallback.
        """
        from flowtask.conf import DOCKER_IMAGE  # lazy import
        return self._config.image or DOCKER_IMAGE

    def _namespace(self) -> str:
        """Return Kubernetes namespace.

        Returns:
            Config namespace or global K8S_NAMESPACE fallback.
        """
        from flowtask.conf import K8S_NAMESPACE  # lazy import
        return self._config.namespace or K8S_NAMESPACE

    def _job_name(self, program: str, task: str, task_id: str) -> str:
        """Build a DNS-compatible Job name.

        Kubernetes Job names must be lowercase, alphanumeric + hyphens, max 63 chars.

        Args:
            program: Program slug.
            task: Task identifier.
            task_id: Full UUID.

        Returns:
            A truncated, lowercase Job name string.
        """
        short_id = task_id.replace("-", "")[:8]
        raw = f"flowtask-{program}-{task}-{short_id}"
        # Ensure lowercase and DNS-safe characters
        name = raw.lower().replace("_", "-")[:63]
        return name

    def _build_env(self, program: str, task: str, task_id: str) -> list[dict]:
        """Build the env list for the container spec.

        Args:
            program: Program slug.
            task: Task identifier.
            task_id: Unique execution UUID.

        Returns:
            List of ``{"name": ..., "value": ...}`` dicts.
        """
        env = [
            {"name": "FLOWTASK_PROGRAM", "value": program},
            {"name": "FLOWTASK_TASK", "value": task},
            {"name": "FLOWTASK_TASK_ID", "value": task_id},
        ]
        for k, v in self._config.env.items():
            env.append({"name": k, "value": str(v)})
        return env

    def _build_job_manifest(
        self, program: str, task: str, task_id: str, job_name: str
    ) -> dict:
        """Build the Kubernetes Job manifest.

        Args:
            program: Program slug.
            task: Task identifier.
            task_id: Unique execution UUID.
            job_name: DNS-compatible Job name.

        Returns:
            A full Job manifest dict.
        """
        return {
            "apiVersion": "batch/v1",
            "kind": "Job",
            "metadata": {
                "name": job_name,
                "namespace": self._namespace(),
                "labels": {
                    "app": "flowtask",
                    "flowtask-program": program,
                    "flowtask-task": task,
                },
            },
            "spec": {
                "backoffLimit": 0,
                "ttlSecondsAfterFinished": 300,
                "template": {
                    "spec": {
                        "restartPolicy": "Never",
                        "containers": [
                            {
                                "name": "flowtask",
                                "image": self._image(),
                                "command": [
                                    "python", "-m", "flowtask",
                                    "-p", program, "-t", task, "--executor", "local",
                                ],
                                "env": self._build_env(program, task, task_id),
                            }
                        ],
                    }
                },
            },
        }

    async def dispatch(
        self,
        program: str,
        task: str,
        task_id: str,
        **kwargs,
    ) -> ExecutionHandle:
        """Create and submit a Kubernetes Job, return immediately.

        Args:
            program: Program slug.
            task: Task identifier.
            task_id: Unique execution UUID.
            **kwargs: Reserved for future use.

        Returns:
            ExecutionHandle with the Job name as execution_id.

        Raises:
            ExecutorConnectionError: If the K8s cluster is unreachable.
            ExecutorError: If the Job cannot be created.
        """
        execution_id = str(task_id) if task_id else str(uuid.uuid4())
        channel = f"FLOWTASK:EXEC:{execution_id}"
        job_name = self._job_name(program, task, execution_id)

        try:
            api = await self._get_api()
        except ExecutorConnectionError:
            raise

        manifest = self._build_job_manifest(program, task, execution_id, job_name)

        try:
            job = Job(manifest, api=api)
            await job.create()
        except Exception as exc:
            raise ExecutorError(
                f"Failed to create K8s Job '{job_name}': {exc}"
            ) from exc

        await self._publisher.publish(
            "dispatched", program, task, execution_id, job_name=job_name
        )
        self.logger.info(
            "K8s Job '%s' created for task %s.%s", job_name, program, task
        )

        return ExecutionHandle(
            executor_type=ExecutorType.K8S,
            execution_id=job_name,
            task_program=program,
            task_name=task,
            channel=channel,
        )

    async def run(
        self,
        program: str,
        task: str,
        task_id: str,
        **kwargs,
    ) -> TaskResult:
        """Create a K8s Job and wait for the result.

        Subscribes to ``FLOWTASK:RESULT:{task_id}`` via Redis PUB/SUB.
        Falls back to polling Job status if Redis is unavailable.
        Deletes the Job on timeout.

        Args:
            program: Program slug.
            task: Task identifier.
            task_id: Unique execution UUID.
            **kwargs: Reserved for future use.

        Returns:
            TaskResult with status and optional error.

        Raises:
            ExecutorConnectionError: If the K8s cluster is unreachable.
        """
        execution_id = str(task_id) if task_id else str(uuid.uuid4())
        job_name = self._job_name(program, task, execution_id)
        timeout = self._config.timeout

        try:
            api = await self._get_api()
        except ExecutorConnectionError:
            raise

        manifest = self._build_job_manifest(program, task, execution_id, job_name)

        try:
            job = Job(manifest, api=api)
            await job.create()
        except Exception as exc:
            raise ExecutorError(
                f"Failed to create K8s Job '{job_name}': {exc}"
            ) from exc

        await self._publisher.publish(
            "started", program, task, execution_id, job_name=job_name
        )

        result = await self._wait_for_result(
            program, task, execution_id, job, job_name, timeout
        )
        return result

    async def _wait_for_result(
        self,
        program: str,
        task: str,
        execution_id: str,
        job: Any,
        job_name: str,
        timeout: int,
    ) -> TaskResult:
        """Wait via Redis PUB/SUB, falling back to Job status polling.

        Args:
            program: Program slug.
            task: Task identifier.
            execution_id: Unique execution UUID.
            job: The kr8s Job object.
            job_name: The Job name.
            timeout: Maximum seconds to wait.

        Returns:
            TaskResult from the K8s Job execution.
        """
        from redis import asyncio as aioredis  # import here for testability
        from flowtask.conf import PUBSUB_REDIS  # lazy import

        result_channel = f"FLOWTASK:RESULT:{execution_id}"

        try:
            redis = await aioredis.from_url(
                PUBSUB_REDIS, decode_responses=True
            )
            pubsub = redis.pubsub()
            await pubsub.subscribe(result_channel)

            loop = asyncio.get_running_loop()
            deadline = loop.time() + timeout
            while True:
                remaining = deadline - loop.time()
                if remaining <= 0:
                    self.logger.warning(
                        "Redis PUB/SUB timed out (%ss) for %s.%s — "
                        "falling back to job status polling",
                        timeout, program, task,
                    )
                    break
                try:
                    msg = await asyncio.wait_for(
                        pubsub.get_message(ignore_subscribe_messages=True),
                        timeout=min(remaining, 1.0),
                    )
                except asyncio.TimeoutError:
                    msg = None

                if msg is not None and msg.get("type") == "message":
                    await pubsub.close()
                    await redis.close()
                    await self._publisher.publish(
                        "completed", program, task, execution_id
                    )
                    return TaskResult(
                        status="success",
                        result=msg.get("data"),
                        execution_id=job_name,
                    )

            await pubsub.close()
            await redis.close()

        except Exception as exc:
            self.logger.warning(
                "Redis PUB/SUB unavailable for K8s job, falling back to polling: %s", exc
            )

        # Fallback: poll Job status
        return await self._poll_job_status(
            program, task, execution_id, job, job_name, timeout
        )

    async def _poll_job_status(
        self,
        program: str,
        task: str,
        execution_id: str,
        job: Any,
        job_name: str,
        timeout: int,
    ) -> TaskResult:
        """Poll K8s Job status until succeeded, failed, or timeout.

        Args:
            program: Program slug.
            task: Task identifier.
            execution_id: Unique execution UUID.
            job: The kr8s Job object.
            job_name: The Job name.
            timeout: Maximum seconds to wait.

        Returns:
            TaskResult based on Job completion status.
        """
        loop = asyncio.get_running_loop()
        deadline = loop.time() + timeout
        poll_interval = 5.0

        while loop.time() < deadline:
            try:
                await job.refresh()
                status = job.status

                succeeded = getattr(status, "succeeded", 0) or 0
                failed_count = getattr(status, "failed", 0) or 0

                if succeeded > 0:
                    await self._publisher.publish(
                        "completed", program, task, execution_id
                    )
                    return TaskResult(
                        status="success",
                        execution_id=job_name,
                    )

                if failed_count > 0:
                    error_msg = await self._get_pod_error(job)
                    await self._publisher.publish(
                        "failed", program, task, execution_id, error=error_msg
                    )
                    return TaskResult(
                        status="failed",
                        error=error_msg,
                        execution_id=job_name,
                    )

            except Exception as exc:
                self.logger.warning("Error polling Job '%s': %s", job_name, exc)

            await asyncio.sleep(poll_interval)

        # Timeout: delete job
        self.logger.warning(
            "K8s Job '%s' timed out after %ss — deleting", job_name, timeout
        )
        try:
            await job.delete()
        except Exception as exc:
            self.logger.warning("Failed to delete timed-out Job '%s': %s", job_name, exc)

        await self._publisher.publish(
            "failed", program, task, execution_id, error="timeout"
        )
        return TaskResult(
            status="failed",
            error=f"K8s Job '{job_name}' timed out after {timeout}s",
            execution_id=job_name,
        )

    async def _get_pod_error(self, job: Any) -> str:
        """Get error details from the Job's failed Pod.

        Args:
            job: The kr8s Job object.

        Returns:
            An error string (OOMKilled, logs, or generic message).
        """
        try:
            pods = await job.pods()
            for pod in pods:
                # Check OOMKilled
                try:
                    pod_status = pod.status
                    for cs in (getattr(pod_status, "containerStatuses", None) or []):
                        state = getattr(cs, "state", None)
                        terminated = getattr(state, "terminated", None) if state else None
                        reason = getattr(terminated, "reason", None) if terminated else None
                        if reason == "OOMKilled":
                            return "Pod was OOMKilled"
                except Exception:
                    pass

                # Try to get last pod logs
                try:
                    logs = await pod.logs(tail_lines=20)
                    return logs or "Pod failed (no logs)"
                except Exception:
                    pass

        except Exception as exc:
            self.logger.debug("Could not retrieve pod error details: %s", exc)

        return "Job failed (no details available)"

    async def close(self) -> None:
        """Close the kr8s API session and lifecycle publisher.

        Args: none.
        """
        if self._api is not None:
            try:
                await self._api.close()
            except Exception as exc:
                self.logger.warning("Error closing K8s API: %s", exc)
            finally:
                self._api = None
        await self._publisher.close()
