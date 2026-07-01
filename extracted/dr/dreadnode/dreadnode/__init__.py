import importlib
import typing as t

from loguru import logger

from dreadnode.version import VERSION

if t.TYPE_CHECKING:
    from dreadnode.agents import Agent
    from dreadnode.app.main import DEFAULT_INSTANCE, Dreadnode
    from dreadnode.core import log as logging
    from dreadnode.core import meta
    from dreadnode.core.log import configure_logging, configure_server_logging
    from dreadnode.core.meta import (
        AgentInput,
        AgentOutput,
        AgentParam,
        Config,
        CurrentRun,
        CurrentTask,
        CurrentTrial,
        DatasetField,
        EnvVar,
        EvalInput,
        EvalOutput,
        EvalParam,
        ParentTask,
        StudyInput,
        StudyOutput,
        StudyParam,
        TaskInput,
        TaskOutput,
        TrialCandidate,
        TrialOutput,
        TrialScore,
    )
    from dreadnode.core.metric import Metric, MetricSeries
    from dreadnode.core.object import Object
    from dreadnode.core.scorer import Scorer
    from dreadnode.core.task import Task
    from dreadnode.core.transforms import Transform
    from dreadnode.core.types import Audio, Code, Image, Markdown, Object3D, Table, Text, Video
    from dreadnode.datasets.dataset import Dataset
    from dreadnode.evaluations import Evaluation
    from dreadnode.optimization import (
        DreadnodeAgentAdapter,
        Optimization,
        OptimizationConfig,
        OptimizationResult,
    )
    from dreadnode.tracing import convert
    from dreadnode.tracing.exporters import TraceBackend
    from dreadnode.tracing.span import Span, TaskSpan
    from dreadnode.tracing.spans import (
        study_span,
        trial_span,
    )


def get_default_instance() -> "Dreadnode":
    """Get the default Dreadnode instance (lazy import to avoid circular dependency)."""
    from dreadnode.app.main import DEFAULT_INSTANCE

    return DEFAULT_INSTANCE


def _get_default_instance() -> "Dreadnode":
    """Internal lazy getter for DEFAULT_INSTANCE."""
    from dreadnode.app.main import DEFAULT_INSTANCE

    return DEFAULT_INSTANCE


logger.disable("dreadnode")

__version__ = VERSION

__all__ = [
    "DEFAULT_INSTANCE",
    "Agent",
    "AgentInput",
    "AgentOutput",
    "AgentParam",
    "Audio",
    "Code",
    "Config",
    "CurrentRun",
    "CurrentTask",
    "CurrentTrial",
    "Dataset",
    "DatasetField",
    "Dreadnode",
    "DreadnodeAgentAdapter",
    "EnvVar",
    "EvalInput",
    "EvalOutput",
    "EvalParam",
    "Evaluation",
    "Image",
    "Markdown",
    "Metric",
    "MetricSeries",
    "Object",
    "Object3D",
    "Optimization",
    "OptimizationConfig",
    "OptimizationResult",
    "ParentTask",
    "Scorer",
    "Span",
    "StudyInput",
    "StudyOutput",
    "StudyParam",
    "Table",
    "Task",
    "TaskInput",
    "TaskOutput",
    "TaskSpan",
    "Text",
    "TraceBackend",
    "Transform",
    "TrialCandidate",
    "TrialOutput",
    "TrialScore",
    "Video",
    "__version__",
    "airt",
    "configure",
    "configure_logging",
    "configure_server_logging",
    "convert",
    "evaluation",
    "get_current_run",
    "get_current_task",
    "get_default_instance",
    "link_objects",
    "load_dataset",
    "load_model",
    "load_package",
    "log_artifact",
    "log_input",
    "log_inputs",
    "log_metric",
    "log_metrics",
    "log_output",
    "log_outputs",
    "log_param",
    "log_params",
    "log_sample",
    "log_samples",
    "logging",
    "meta",
    "optimize_anything",
    "push_capability",
    "push_dataset",
    "push_environment",
    "push_hf_dataset",
    "push_model",
    "push_update",
    "run",
    "scorer",
    "scorers",
    "shutdown",
    "span",
    "study",
    "study_span",
    "tag",
    "task",
    "task_and_run",
    "task_env",
    "task_span",
    "tool",
    "tool_method",
    "train",
    "training",
    "transforms",
    "trial_span",
]

__lazy_submodules__: list[str] = ["scorers", "agents", "airt", "eval", "transforms", "training"]

# Lazy module imports - these return the entire module
__lazy_modules__: dict[str, str] = {
    "convert": "dreadnode.tracing.convert",
    "logging": "dreadnode.core.log",
    "meta": "dreadnode.core.meta",
}

__lazy_components__: dict[str, str] = {
    # Types
    "Audio": "dreadnode.core.types",
    "Image": "dreadnode.core.types",
    "Table": "dreadnode.core.types",
    "Video": "dreadnode.core.types",
    "Code": "dreadnode.core.types",
    "Markdown": "dreadnode.core.types",
    "Object3D": "dreadnode.core.types",
    "Text": "dreadnode.core.types",
    # Core classes
    "Agent": "dreadnode.agents",
    "Dataset": "dreadnode.datasets.dataset",
    "Dreadnode": "dreadnode.app.main",
    "DEFAULT_INSTANCE": "dreadnode.app.main",
    "Evaluation": "dreadnode.evaluations",
    "Metric": "dreadnode.core.metric",
    "MetricSeries": "dreadnode.core.metric",
    "Object": "dreadnode.core.object",
    "DreadnodeAgentAdapter": "dreadnode.optimization",
    "Optimization": "dreadnode.optimization",
    "OptimizationConfig": "dreadnode.optimization",
    "OptimizationResult": "dreadnode.optimization",
    "Scorer": "dreadnode.core.scorer",
    "Span": "dreadnode.tracing.span",
    "Task": "dreadnode.core.task",
    "TaskSpan": "dreadnode.tracing.span",
    "TraceBackend": "dreadnode.tracing.exporters",
    "Transform": "dreadnode.core.transforms",
    # Meta/annotations
    "AgentInput": "dreadnode.core.meta",
    "AgentOutput": "dreadnode.core.meta",
    "AgentParam": "dreadnode.core.meta",
    "Config": "dreadnode.core.meta",
    "CurrentRun": "dreadnode.core.meta",
    "CurrentTask": "dreadnode.core.meta",
    "CurrentTrial": "dreadnode.core.meta",
    "DatasetField": "dreadnode.core.meta",
    "EnvVar": "dreadnode.core.meta",
    "EvalInput": "dreadnode.core.meta",
    "EvalOutput": "dreadnode.core.meta",
    "EvalParam": "dreadnode.core.meta",
    "ParentTask": "dreadnode.core.meta",
    "StudyInput": "dreadnode.core.meta",
    "StudyOutput": "dreadnode.core.meta",
    "StudyParam": "dreadnode.core.meta",
    "TaskInput": "dreadnode.core.meta",
    "TaskOutput": "dreadnode.core.meta",
    "TrialCandidate": "dreadnode.core.meta",
    "TrialOutput": "dreadnode.core.meta",
    "TrialScore": "dreadnode.core.meta",
    # Span factories
    "study_span": "dreadnode.tracing.spans",
    "trial_span": "dreadnode.tracing.spans",
    # Tools
    "tool": "dreadnode.core.tools",
    "tool_method": "dreadnode.core.tools",
    # Functions from modules
    "configure_logging": "dreadnode.core.log",
    "configure_server_logging": "dreadnode.core.log",
}

# Dreadnode instance method/property aliases - these use lazy getters
__instance_methods__: list[str] = [
    "configure",
    "shutdown",
    "serve",
    "storage",
    "change_workspace",
    "list_workspaces",
    "list_registry",
    "span",
    "task",
    "task_span",
    "run",
    "task_and_run",
    "task_env",
    "scorer",
    "evaluation",
    "optimize_anything",
    "study",
    "push_update",
    "tag",
    "log_metric",
    "log_metrics",
    "log_param",
    "log_params",
    "log_input",
    "log_inputs",
    "log_output",
    "log_outputs",
    "log_sample",
    "log_samples",
    "link_objects",
    "log_artifact",
    "get_current_run",
    "get_current_task",
    "train",
    "load_package",
    "load_dataset",
    "load_model",
    "load_capability",
    "push_capability",
    "push_dataset",
    "push_environment",
    "push_hf_dataset",
    "push_model",
]

# Aliases with different names
__instance_aliases__: dict[str, str] = {
    "push_repo": "push_package",
    "pull_repo": "pull_package",
    "build_repo": "build_package",
    "push_package": "push_package",
    "pull_package": "pull_package",
    "build_package": "build_package",
}


def __getattr__(name: str) -> t.Any:
    # Lazy submodules
    if name in __lazy_submodules__:
        module = importlib.import_module(f".{name}", __name__)
        globals()[name] = module
        return module

    # Lazy module imports (return entire module)
    if name in __lazy_modules__:
        module_path = __lazy_modules__[name]
        module = importlib.import_module(module_path)
        globals()[name] = module
        return module

    # Lazy components (return specific attribute from module)
    if name in __lazy_components__:
        module_name = __lazy_components__[name]
        module = importlib.import_module(module_name)
        component = getattr(module, name)
        globals()[name] = component
        return component

    # Instance methods (delegate to DEFAULT_INSTANCE)
    if name in __instance_methods__:
        return getattr(_get_default_instance(), name)

    # Instance method aliases
    if name in __instance_aliases__:
        method_name = __instance_aliases__[name]
        return getattr(_get_default_instance(), method_name)

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
