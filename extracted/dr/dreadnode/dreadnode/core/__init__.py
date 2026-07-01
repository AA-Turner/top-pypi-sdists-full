import importlib
import typing as t

__all__ = [
    "AnyTool",
    "BaseTrainer",
    "Environment",
    "EnvironmentContext",
    "FunctionCall",
    "FunctionDefinition",
    "SFTConfig",
    "SFTTrainer",
    "TaskEnvironment",
    "Tool",
    "ToolCall",
    "ToolDefinition",
    "ToolMode",
    "Toolset",
    "TrainingCallback",
    "TrainingConfig",
    "TrainingState",
    "Transform",
    "TransformCallable",
    "TransformLike",
    "TransformWarning",
    "TransformsLike",
    "current_task_environment",
    "discover_tools_on_obj",
    "render_task_instruction",
    "tool",
    "tool_method",
]

__lazy_components__: dict[str, str] = {
    "Environment": "dreadnode.core.environment",
    "EnvironmentContext": "dreadnode.core.environment",
    "TaskEnvironment": "dreadnode.core.environment",
    "current_task_environment": "dreadnode.core.environment",
    "render_task_instruction": "dreadnode.core.templating",
    "FunctionCall": "dreadnode.agents.tools.base",
    "FunctionDefinition": "dreadnode.agents.tools.base",
    "Tool": "dreadnode.agents.tools.base",
    "ToolCall": "dreadnode.agents.tools.base",
    "ToolDefinition": "dreadnode.agents.tools.base",
    "ToolMode": "dreadnode.agents.tools.base",
    "Toolset": "dreadnode.agents.tools.base",
    "discover_tools_on_obj": "dreadnode.agents.tools.base",
    "tool": "dreadnode.agents.tools.base",
    "tool_method": "dreadnode.agents.tools.base",
    "Transform": "dreadnode.core.transforms",
    "TransformCallable": "dreadnode.core.transforms",
    "TransformLike": "dreadnode.core.transforms",
    "TransformsLike": "dreadnode.core.transforms",
    "TransformWarning": "dreadnode.core.transforms",
}

__lazy_training__: set[str] = {
    "BaseTrainer",
    "SFTConfig",
    "SFTTrainer",
    "TrainingCallback",
    "TrainingConfig",
    "TrainingState",
}


def __getattr__(name: str) -> t.Any:
    if name in __lazy_components__:
        module = importlib.import_module(__lazy_components__[name])
        value = getattr(module, name)
        globals()[name] = value
        return value

    if name in __lazy_training__:
        if name in ("SFTConfig", "SFTTrainer"):
            from dreadnode.training import SFTConfig, SFTTrainer

            return SFTConfig if name == "SFTConfig" else SFTTrainer
        from dreadnode.training.base import (
            BaseTrainer,
            TrainingCallback,
            TrainingConfig,
            TrainingState,
        )

        return {
            "BaseTrainer": BaseTrainer,
            "TrainingCallback": TrainingCallback,
            "TrainingConfig": TrainingConfig,
            "TrainingState": TrainingState,
        }[name]

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
