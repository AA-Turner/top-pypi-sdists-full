# Copyright (C) 2018-present Jesus Lara
#
"""Docker job executor for the flowtask executor framework."""
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
    import aiodocker
    _AIODOCKER_AVAILABLE = True
except ImportError:
    _AIODOCKER_AVAILABLE = False


def _require_aiodocker() -> None:
    """Raise ImportError if aiodocker is not installed.

    Raises:
        ImportError: If aiodocker is not available.
    """
    if not _AIODOCKER_AVAILABLE:
        raise ImportError(
            "aiodocker is required for DockerJobExecutor. "
            "Install it with: pip install flowtask[docker]"
        )


@register_executor("docker")
class DockerJobExecutor(AbstractJobExecutor):
    """Launches flowtask tasks inside Docker containers via aiodocker.

    For ``dispatch()`` the container is started with ``AutoRemove=True``
    (fire-and-forget).  For ``run()`` the container is kept until the
    result arrives on a Redis PUB/SUB channel, or until ``config.timeout``
    seconds elapse.

    The container image defaults to ``DOCKER_IMAGE`` from conf.py and can be
    overridden per-task via ``ExecutorConfig.image``.

    Args:
        config: ExecutorConfig with ``type=DOCKER``.
        **kwargs: Passed through to the base constructor.
    """

    def __init__(self, config: ExecutorConfig, **kwargs) -> None:
        super().__init__(config, **kwargs)
        self._client: Optional[Any] = None
        self._publisher = ExecutorLifecyclePublisher()

    @classmethod
    def name(cls) -> str:
        """Return registry name.

        Returns:
            ``"docker"``
        """
        return "docker"

    async def _get_client(self):
        """Return (or lazily create) the aiodocker.Docker client.

        Returns:
            An aiodocker.Docker instance connected to the local daemon.

        Raises:
            ExecutorConnectionError: If the Docker daemon is not reachable.
        """
        _require_aiodocker()
        if self._client is None:
            try:
                self._client = aiodocker.Docker()
            except Exception as exc:
                raise ExecutorConnectionError(
                    f"Cannot connect to Docker daemon: {exc}"
                ) from exc
        return self._client

    def _image(self) -> str:
        """Return the container image to use.

        Returns:
            Config image or global DOCKER_IMAGE fallback.
        """
        from flowtask.conf import DOCKER_IMAGE  # lazy import
        return self._config.image or DOCKER_IMAGE

    def _container_name(self, program: str, task: str, task_id: str) -> str:
        """Build a container name from program, task, and truncated UUID.

        Args:
            program: Program slug.
            task: Task identifier.
            task_id: Full UUID.

        Returns:
            A DNS-compatible container name string.
        """
        short_id = task_id.replace("-", "")[:8]
        return f"flowtask-{program}-{task}-{short_id}"

    def _build_env(self, program: str, task: str, task_id: str) -> list[str]:
        """Build environment variable list for the container.

        Args:
            program: Program slug.
            task: Task identifier.
            task_id: Unique execution UUID.

        Returns:
            List of ``KEY=value`` strings.
        """
        env = [
            f"FLOWTASK_PROGRAM={program}",
            f"FLOWTASK_TASK={task}",
            f"FLOWTASK_TASK_ID={task_id}",
        ]
        for k, v in self._config.env.items():
            env.append(f"{k}={v}")
        return env

    def _build_container_config(
        self, program: str, task: str, task_id: str, auto_remove: bool = True
    ) -> dict:
        """Build the aiodocker container configuration dict.

        Args:
            program: Program slug.
            task: Task identifier.
            task_id: Unique execution UUID.
            auto_remove: If True, container is removed after it exits.

        Returns:
            A dict suitable for aiodocker containers.create_or_replace().
        """
        return {
            "Image": self._image(),
            "Env": self._build_env(program, task, task_id),
            "Cmd": [
                "python", "-m", "flowtask",
                "-p", program, "-t", task, "--executor", "local",
            ],
            "HostConfig": {
                "AutoRemove": auto_remove,
            },
        }

    async def dispatch(
        self,
        program: str,
        task: str,
        task_id: str,
        **kwargs,
    ) -> ExecutionHandle:
        """Create and start a container with AutoRemove=True.

        Args:
            program: Program slug.
            task: Task identifier.
            task_id: Unique execution UUID.
            **kwargs: Reserved for future use.

        Returns:
            ExecutionHandle with the Docker container ID.

        Raises:
            ExecutorConnectionError: If Docker daemon is unreachable.
            ExecutorError: If image pull or container creation fails.
        """
        execution_id = task_id or str(uuid.uuid4())
        channel = f"FLOWTASK:EXEC:{execution_id}"
        container_name = self._container_name(program, task, execution_id)

        try:
            client = await self._get_client()
        except ExecutorConnectionError:
            raise

        config = self._build_container_config(
            program, task, execution_id, auto_remove=True
        )

        try:
            container = await client.containers.create_or_replace(
                container_name, config
            )
            await container.start()
        except Exception as exc:
            exc_str = str(exc)
            if "No such image" in exc_str or "pull" in exc_str.lower():
                raise ExecutorError(
                    f"Docker image pull failed for '{self._image()}': {exc}"
                ) from exc
            raise ExecutorError(f"Container creation failed: {exc}") from exc

        container_id = container.id
        await self._publisher.publish(
            "dispatched", program, task, execution_id,
            container_id=container_id,
        )
        self.logger.info(
            "Container %s started for task %s.%s", container_id, program, task
        )

        return ExecutionHandle(
            executor_type=ExecutorType.DOCKER,
            execution_id=container_id,
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
        """Create container, wait for result via Redis PUB/SUB, then clean up.

        Falls back to polling container status if Redis is unavailable.
        Kills the container on timeout.

        Args:
            program: Program slug.
            task: Task identifier.
            task_id: Unique execution UUID.
            **kwargs: Reserved for future use.

        Returns:
            TaskResult with status and optional error.

        Raises:
            ExecutorConnectionError: If Docker daemon is unreachable.
        """
        execution_id = task_id or str(uuid.uuid4())
        container_name = self._container_name(program, task, execution_id)
        timeout = self._config.timeout

        try:
            client = await self._get_client()
        except ExecutorConnectionError:
            raise

        config = self._build_container_config(
            program, task, execution_id, auto_remove=False
        )

        try:
            container = await client.containers.create_or_replace(
                container_name, config
            )
            await container.start()
        except Exception as exc:
            raise ExecutorError(
                f"Container creation failed for {program}.{task}: {exc}"
            ) from exc

        container_id = container.id
        await self._publisher.publish(
            "started", program, task, execution_id,
            container_id=container_id,
        )

        # Try Redis PUB/SUB first, fall back to container.wait()
        result = await self._wait_for_result(
            program, task, execution_id, container, timeout
        )

        # Cleanup: remove container
        try:
            await container.delete(force=True)
        except Exception as exc:
            self.logger.warning("Failed to remove container %s: %s", container_id, exc)

        return result

    async def _wait_for_result(
        self,
        program: str,
        task: str,
        execution_id: str,
        container: Any,
        timeout: int,
    ) -> TaskResult:
        """Wait for the task result using Redis PUB/SUB with container fallback.

        Args:
            program: Program slug.
            task: Task identifier.
            execution_id: Unique execution UUID.
            container: The aiodocker container object.
            timeout: Maximum seconds to wait.

        Returns:
            TaskResult from the container execution.
        """
        from redis import asyncio as aioredis  # import here for testability
        from flowtask.conf import PUBSUB_REDIS  # lazy import

        result_channel = f"FLOWTASK:RESULT:{execution_id}"
        loop = asyncio.get_running_loop()
        deadline = loop.time() + timeout

        try:
            redis = await aioredis.from_url(
                PUBSUB_REDIS, decode_responses=True
            )
            pubsub = redis.pubsub()
            await pubsub.subscribe(result_channel)

            while True:
                remaining = deadline - loop.time()
                if remaining <= 0:
                    self.logger.warning(
                        "Redis PUB/SUB timed out (%ss) for %s.%s — "
                        "falling back to container.wait()",
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
                    await pubsub.unsubscribe(result_channel)
                    await pubsub.close()
                    await redis.close()
                    await self._publisher.publish(
                        "completed", program, task, execution_id
                    )
                    return TaskResult(
                        status="success",
                        result=msg.get("data"),
                        execution_id=execution_id,
                    )

            # Timeout: fall back to container inspection
            await pubsub.close()
            await redis.close()

        except Exception as exc:
            self.logger.warning(
                "Redis PUB/SUB unavailable, falling back to container.wait(): %s", exc
            )

        # Fallback: use whatever time is still remaining (minimum 30s)
        fallback_timeout = max(int(deadline - loop.time()), 30)
        return await self._wait_container_exit(
            program, task, execution_id, container, fallback_timeout
        )

    async def _wait_container_exit(
        self,
        program: str,
        task: str,
        execution_id: str,
        container: Any,
        timeout: int,
    ) -> TaskResult:
        """Fallback: poll container status via container.wait().

        Args:
            program: Program slug.
            task: Task identifier.
            execution_id: Unique execution UUID.
            container: The aiodocker container object.
            timeout: Maximum seconds to wait before killing.

        Returns:
            TaskResult based on container exit code.
        """
        try:
            result = await asyncio.wait_for(container.wait(), timeout=timeout)
            exit_code = result.get("StatusCode", -1)
        except asyncio.TimeoutError:
            self.logger.warning(
                "Container timeout (%ss) for %s.%s — killing", timeout, program, task
            )
            try:
                await container.kill()
            except Exception:
                pass
            await self._publisher.publish(
                "failed", program, task, execution_id, error="timeout"
            )
            return TaskResult(
                status="failed",
                error=f"Container timed out after {timeout}s",
                execution_id=execution_id,
            )

        if exit_code == 0:
            await self._publisher.publish(
                "completed", program, task, execution_id
            )
            return TaskResult(
                status="success",
                execution_id=execution_id,
            )

        if exit_code == 137:
            error_msg = "Container was OOM killed (exit code 137)"
        else:
            try:
                logs = await container.log(stdout=True, stderr=True)
                error_msg = "".join(logs[-20:]) if logs else f"Exit code {exit_code}"
            except Exception:
                error_msg = f"Container exited with code {exit_code}"

        await self._publisher.publish(
            "failed", program, task, execution_id, error=error_msg
        )
        return TaskResult(
            status="failed",
            error=error_msg,
            execution_id=execution_id,
        )

    async def close(self) -> None:
        """Close the aiodocker client and lifecycle publisher.

        Args: none.
        """
        if self._client is not None:
            try:
                await self._client.close()
            except Exception as exc:
                self.logger.warning("Error closing Docker client: %s", exc)
            finally:
                self._client = None
        await self._publisher.close()
