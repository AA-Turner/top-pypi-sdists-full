from __future__ import annotations

import datetime as _datetime
import hashlib
import logging
import os
import re
from copy import deepcopy
from dataclasses import asdict, dataclass
from functools import partial, wraps
from typing import Any, Callable, Dict, Iterable, List, Optional, Union

from flytekit import PodTemplate
from flytekit.configuration import SerializationSettings
from flytekit.core import launch_plan as _annotated_launchplan
from flytekit.core import workflow as _annotated_workflow
from flytekit.core.base_task import TaskResolverMixin
from flytekit.core.python_auto_container import get_registerable_container_image
from flytekit.core.python_function_task import PythonFunctionTask
from flytekit.core.resources import Resources
from flytekit.core.task import TaskPlugins
from flytekit.core.task import task as flytekit_task_decorator
from flytekit.extras.accelerators import BaseAccelerator
from flytekit.image_spec import ImageSpec
from flytekit.models.documentation import Documentation
from flytekit.models.security import Secret

from union.actor._hash import _make_key

logger = logging.getLogger(__name__)


_ACTOR_NAME_RE = re.compile(r"[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*")
_ACTOR_STATE_CACHE = {}


def actor_cache(f):
    """Cache function between actor executions."""

    @wraps(f)
    def inner_func(*args, **kwargs):
        args_with_extra = (os.getcwd(), f.__name__, f.__module__, *args)
        key = _make_key(args_with_extra, kwargs)
        try:
            return _ACTOR_STATE_CACHE[key]
        except KeyError:
            _ACTOR_STATE_CACHE[key] = f(*args, **kwargs)
            return _ACTOR_STATE_CACHE[key]

    return inner_func


@dataclass
class ActorEnvironment:
    """
    ActorEnvironment class.

    :param name: The name of the actor. This is used in conjunction with the
        project, domain, and version to uniquely identify the actor.
    :param container_image: The container image to use for the task. Set to
        default image if none provided.
    :param replica_count: The number of workers to provision that are able to
        accept tasks.
    :param ttl_seconds: How long to keep the Actor alive while no tasks are
        being run. If not provided the default configuration value of 90s
        will be used.
    :param environment: Environment variables as key, value pairs in a Python
        dictionary.
    :param requests: Compute resource requests per task.
    :param limits: Compute resource limits.
    :param accelerator: The accelerator device to use for the task.
    :param secret_requests: Keys (ideally descriptive) that can identify the
        secrets supplied at runtime.
    :param pod_template: The pod template to use as the base configuration
        for actor replica pods.
    :param interruptible: Whether the actor replica pods are labelled as
        interruptible.
    """

    # These fields here are part of the actor config.
    name: str
    container_image: Optional[Union[str, ImageSpec]] = None
    replica_count: int = 1
    ttl_seconds: Optional[int] = None
    environment: Optional[Dict[str, str]] = None
    requests: Optional[Resources] = None
    limits: Optional[Resources] = None
    accelerator: Optional[BaseAccelerator] = None
    secret_requests: Optional[List[Secret]] = None
    pod_template: Optional[PodTemplate] = None
    interruptible: bool = None

    def __post_init__(self):
        match_re = _ACTOR_NAME_RE.fullmatch(self.name)
        if not match_re:
            raise ValueError("Actor name must consist of lower case alphanumeric characters, '-' or '.'")

        if self.ttl_seconds is not None and (self.ttl_seconds < 30 or self.ttl_seconds > 900):
            raise ValueError("Actor TTL must be between 30s and 15m (900s)")

    def _task(
        self,
        _task_function=None,
        cache: bool = False,
        cache_serialize: bool = False,
        cache_version: str = "",
        retries: int = 0,
        timeout: Union[_datetime.timedelta, int] = 0,
        node_dependency_hints: Optional[
            Iterable[
                Union[
                    PythonFunctionTask,
                    _annotated_launchplan.LaunchPlan,
                    _annotated_workflow.WorkflowBase,
                ]
            ]
        ] = None,
        task_resolver: Optional[TaskResolverMixin] = None,
        docs: Optional[Documentation] = None,
        execution_mode: PythonFunctionTask.ExecutionBehavior = PythonFunctionTask.ExecutionBehavior.DEFAULT,
        **kwargs,
    ):
        wrapper = partial(
            flytekit_task_decorator,
            task_config=self,
            cache=cache,
            cache_serialize=cache_serialize,
            cache_version=cache_version,
            retries=retries,
            timeout=timeout,
            node_dependency_hints=node_dependency_hints,
            task_resolver=task_resolver,
            docs=docs,
            container_image=self.container_image,
            environment=self.environment,
            requests=self.requests,
            limits=self.limits,
            accelerator=self.accelerator,
            secret_requests=self.secret_requests,
            execution_mode=execution_mode,
            pod_template=self.pod_template,
            interruptible=self.interruptible,
            **kwargs,
        )

        if _task_function:
            return wrapper(_task_function=_task_function)
        return wrapper

    @property
    def task(self):
        return self._task

    # Keeping this private for now to test
    @property
    def _dynamic(self):
        return partial(self._task, execution_mode=PythonFunctionTask.ExecutionBehavior.DYNAMIC)

    @property
    def version(self) -> str:
        fields = []
        for k, v in asdict(self).items():
            if isinstance(v, BaseAccelerator):
                fields.append(str(v.to_flyte_idl()))
            elif k == "pod_template":
                # Remove args from the version specification
                try:
                    for container in v["pod_spec"].containers:
                        container.args = []
                except Exception:
                    pass
                fields.append(str(v))
            else:
                fields.append(str(v))
        all_fields = "".join(fields)
        hash_object = hashlib.md5(all_fields.encode("utf-8"))
        hex_digest = hash_object.hexdigest()
        logger.debug(f"Computing actor hash with string {all_fields} to {hex_digest[:15]}")
        return hex_digest[:15]


class ActorTask(PythonFunctionTask[ActorEnvironment]):
    _ACTOR_TASK_TYPE = "actor"

    def __init__(self, task_config: ActorEnvironment, task_function: Callable, **kwargs):
        super(ActorTask, self).__init__(
            task_config=task_config,
            task_type=self._ACTOR_TASK_TYPE,
            task_function=task_function,
            **kwargs,
        )

    def get_custom(self, settings: SerializationSettings) -> Optional[Dict[str, Any]]:
        """
        Serialize the `ActorTask` config into a dict.

        :param settings: Current serialization settings
        :return: Dictionary representation of the dask task config.
        """
        # Get version with the actual container_image value
        container_image = get_registerable_container_image(self.container_image, settings.image_config)
        task_config = deepcopy(self.task_config)
        task_config.container_image = container_image

        return {
            "name": self.task_config.name,
            "version": task_config.version,
            "type": self._ACTOR_TASK_TYPE,
            "spec": {
                "container_image": container_image,
                "backlog_length": None,
                "parallelism": 1,
                "replica_count": self.task_config.replica_count,
                "ttl_seconds": self.task_config.ttl_seconds,
            },
        }

    @classmethod
    def from_task(
        cls,
        task: PythonFunctionTask,
        replica_count: int,
        ttl_seconds: int = 60,
        name: Optional[str] = None,
    ) -> "ActorTask":
        """
        Create an ActorTask from a PythonFunctionTask.
        """

        if not isinstance(task, PythonFunctionTask):
            raise ValueError("Only PythonFunctionTask can be converted to ActorTask")

        if name is None:
            name = task.task_function.__name__.replace("_", "-")

        actor = ActorEnvironment(
            container_image=task.container_image,
            name=name,
            replica_count=replica_count,
            ttl_seconds=ttl_seconds,
            environment=task.environment,
            requests=task.resources.requests,
            limits=task.resources.limits,
            secret_requests=task._security_ctx.secrets if task._security_ctx else None,
            accelerator=task.accelerator,
            pod_template=task.pod_template,
        )

        return cls(
            task_config=actor,
            task_function=task.task_function,
            retries=task._metadata.retries,
            timeout=task._metadata.timeout,
            cache=task._metadata.cache,
            cache_serialize=task._metadata.cache_serialize,
            cache_version=task._metadata.cache_version,
            docs=task.docs,
            execution_mode=task.execution_mode,
        )


TaskPlugins.register_pythontask_plugin(ActorEnvironment, ActorTask)
