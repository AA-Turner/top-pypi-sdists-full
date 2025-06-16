from abc import ABCMeta
from typing import Any, Dict, Optional

import valohai_yaml
from valohai_yaml.objs import Step
from valohai_yaml.utils import listify

from .base import PapiObject
from .edges import EdgeDescriptor
from .utils import compact_dict


class Node(PapiObject, metaclass=ABCMeta):
    type: str
    name: str

    def __init__(self, *, name: str):
        self.name = name

    def output(self, key: str) -> EdgeDescriptor:
        return EdgeDescriptor(node=self, type="output", key=key)

    def input(self, key: str) -> EdgeDescriptor:
        return EdgeDescriptor(node=self, type="input", key=key)


class ExecutionNode(Node):
    type = "execution"
    parameters: Dict[str, Any]
    inputs: Dict[str, Any]

    def __init__(self, *, name: str, step: Step):
        super().__init__(name=name)
        self.step = step
        self.parameters = {}
        self.inputs = {}

    def parameter(self, name: str, value) -> "ExecutionNode":
        self._check_parameter_name(name)
        self.parameters[name] = value
        return self

    def to_api(self, api_context):
        step = self.step
        step_data = step.serialize()
        step_data.pop("name")
        step_data["parameters"] = {
            **step.get_parameter_defaults(include_flags=True),
            **self.parameters,
        }
        step_data["inputs"] = {
            i["name"]: self.inputs.get(i["name"], listify(i.get("default")))
            for i in step_data.get("inputs", [])
        }
        step_data.pop("mounts", None)
        return {
            "type": self.type,
            "name": self.name,
            "template": {
                "commit": api_context.commit_identifier,
                "step": step.name,
                **step_data,
            },
        }

    def to_yaml(self, yaml_context):
        return valohai_yaml.objs.ExecutionNode(
            name=self.name,
            step=self.step.name,
        )

    def input(self, key: str) -> EdgeDescriptor:
        if key not in self.step.inputs:
            raise ValueError(f"{key} not known in {self.step.name}")
        return super().input(key)

    def _check_parameter_name(self, name):
        if name not in self.step.parameters:
            raise ValueError(f"No such parameter {name}")


class TaskNode(ExecutionNode):
    type = "task"
    task_type: str = "grid_search"
    task_stop_expression: Optional[str] = None
    task_configuration: Optional[dict] = None

    def grid_search(self) -> "TaskNode":
        self.task_type = "grid_search"
        self.task_configuration = {}
        return self

    def random_search(self, executions: int) -> "TaskNode":
        self.task_type = "random_search"
        self.task_configuration = {
            "execution_count": executions,
        }
        return self

    def bayesian_tpe(self) -> "TaskNode":
        raise NotImplementedError("bayesian_tpe() is not implemented yet")

    def linear_parameter(
        self, name: str, *, min: float, max: float, step: float = 1
    ) -> "TaskNode":
        self._check_parameter_name(name)
        self.parameters[name] = {
            "style": "linear",
            "rules": {
                "start": float(min),
                "end": float(max),
                "step": float(step),
            },
        }
        return self

    def multiple_parameter(
        self,
        name: str,
        choices: list,
    ) -> "TaskNode":
        self._check_parameter_name(name)
        self.parameters[name] = {
            "style": "multiple",
            "rules": {
                "items": choices,
            },
        }
        return self

    def random_parameter(
        self,
        name: str,
        *,
        min: float,
        max: float,
        count: Optional[int] = 1,
        integerify: bool = False,
        seed: Optional[int] = None,
    ) -> "TaskNode":
        self._check_parameter_name(name)
        self.parameters[name] = {
            "style": "random",
            "rules": {
                "min": min,
                "max": max,
                "count": count,
                "integerify": bool(integerify),
                "seed": seed,
            },
        }
        return self

    def to_api(self, api_context):
        payload = super().to_api(api_context)
        payload["template"].update(
            compact_dict(
                dict(
                    type=self.task_type,
                    task_stop_expression=self.task_stop_expression,
                    configuration=self.task_configuration,
                )
            )
        )
        return payload

    def to_yaml(self, yaml_context):
        return valohai_yaml.objs.TaskNode(
            name=self.name,
            step=self.step.name,
        )
