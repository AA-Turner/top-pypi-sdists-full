"""
DSLighting 2.0 - Data Science Agent Framework

A complete 5-layer architecture for building and running data science agents.

Quick Start:
    >>> from dslighting import run_agent
    >>> result = run_agent(task_id="bike-sharing-demand")

Documentation: https://github.com/usail-hkust/dslighting
"""

__version__ = "2.6.34"
__author__ = "DSLighting Team"

# ============================================================================
# Top-level API imports
# ============================================================================

from dslighting.api import Agent, AgentResult, DataLoader, TaskContext
from dslighting.api.convenience import run_agent, load_data, setup
from dslighting import datasets


# ============================================================================
# Lazy imports for optional modules and backward compatibility
# ============================================================================

def __getattr__(name: str):
    """
    Lazily resolve optional symbols for backward compatibility.

    Keeps import time minimal and loads submodules only when needed.
    Works on Python 3.7+.
    """
    import importlib
    import sys

    # Reserved for lazy module cache.
    _lazy_modules = {}

    # Dataset API.
    if name in ("Dataset", "load_dataset_new", "DatasetInfo"):
        module = importlib.import_module("dslighting.core.dataset")
        if name == "load_dataset_new":
            return getattr(module, "load_dataset")
        return getattr(module, name)

    # Types.
    if name in (
        "TaskDefinition", "TaskType", "TaskMode",
        "WorkflowCandidate", "ReviewResult", "Plan",
    ):
        module = importlib.import_module("dslighting.core.types")
        return getattr(module, name)

    if name in ("LLMConfig", "TaskConfig"):
        module = importlib.import_module("dslighting.core.config")
        return getattr(module, name)

    # Training APIs.
    if name in (
        "LitDSAgent", "RewardEvaluator", "KaggleReward",
        "ClassificationReward", "RegressionReward",
        "DatasetConverter", "VerlConfigBuilder"
    ):
        module = importlib.import_module("dslighting.training")
        return getattr(module, name)

    # Agents.
    if name == "BaseAgent":
        module = importlib.import_module("dslighting.agents")
        return getattr(module, name)

    # Preset workflows.
    if name in ("AIDE", "AutoKaggle", "DataInterpreter", "DeepAnalyze",
                "DSAgent", "AutoMind", "AFlow"):
        module = importlib.import_module("dslighting.agents.presets")
        return getattr(module, name)

    # Search strategies.
    if name in ("SearchStrategy", "GreedyStrategy", "BeamSearchStrategy",
                "MCTSStrategy", "EvolutionaryStrategy"):
        module = importlib.import_module("dslighting.agents.strategies")
        return getattr(module, name)

    # Operators.
    if name in ("Operator", "GenerateCodeAndPlanOperator", "PlanOperator",
                "ReviewOperator", "SummarizeOperator", "ExecuteAndTestOperator"):
        module = importlib.import_module("dslighting.operators")
        return getattr(module, name)

    # Orchestration operators.
    if name in ("Pipeline", "Parallel", "Conditional"):
        module = importlib.import_module("dslighting.operators.orchestration")
        return getattr(module, name)

    # Services.
    if name in ("LLMService", "SandboxService", "WorkspaceService",
                "DataAnalyzer", "VDBService"):
        module = importlib.import_module("dslighting.services")
        return getattr(module, name)

    # State.
    if name in ("JournalState", "Node", "MetricValue", "Experience",
                "MemoryManager", "ContextManager"):
        module = importlib.import_module("dslighting.state")
        return getattr(module, name)

    # Prompts.
    if name in ("PromptBuilder", "create_prompt_template", "get_common_guidelines",
                "create_modeling_prompt", "create_eda_prompt", "create_debug_prompt"):
        module = importlib.import_module("dslighting.prompts")
        return getattr(module, name)

    # Workflow factory.
    if name == "BaseWorkflowFactory":
        module = importlib.import_module("dslighting.workflows")
        return getattr(module, name)

    if name == "MLETaskLoader":
        module = importlib.import_module("dslighting.benchmark.loaders")
        return getattr(module, name)

    # Legacy compatibility.
    if name == "LegacyAgent":
        module = importlib.import_module("dslighting.core.agent")
        return getattr(module, "Agent")

    if name == "LegacyDataLoader":
        module = importlib.import_module("dslighting.core.data_loader")
        return getattr(module, "DataLoader")

    # Unknown attribute.
    raise AttributeError(f"module 'dslighting' has no attribute '{name}'")


# ============================================================================
# Convenience helper functions
# ============================================================================

def help():
    """Show DSLighting 2.0 help and quick start guide."""
    from dslighting.utils.help import show_help
    show_help()


def list_workflows():
    """List all available workflows."""
    from dslighting.utils.help import list_workflows as _list_workflows
    _list_workflows()


def show_example(workflow_name: str):
    """Show workflow example code."""
    from dslighting.utils.help import show_example as _show_example
    _show_example(workflow_name)


def list_prompts(category: str = "all") -> dict[str, list[str]]:
    """
    List all available prompts by category.

    Args:
        category: Filter by category ('all', 'aide', 'autokaggle', etc.)

    Returns:
        Dictionary mapping category names to lists of prompt functions

    Example:
        >>> import dslighting
        >>> prompts = dslighting.list_prompts()
    """
    from dslighting.prompts import list_available_prompts
    return list_available_prompts(category)


def list_operators(category: str = "all") -> dict[str, list[str]]:
    """
    List all available operators by category.

    Args:
        category: Filter by category ('all', 'llm', 'code', 'data', etc.)

    Returns:
        Dictionary mapping category names to lists of operator names

    Example:
        >>> import dslighting
        >>> ops = dslighting.list_operators()
    """
    from dslighting.operators import list_available_operators
    return list_available_operators(category)


def explore():
    """
    Interactive exploration of DSLighting components.

    Shows all available prompts, operators, and workflows.

    Example:
        >>> import dslighting
        >>> dslighting.explore()
    """
    from dslighting.utils.help import explore as _explore
    _explore()


# ============================================================================
# Public exports
# ============================================================================

__all__ = [
    # Metadata
    "__version__",
    "__author__",

    # Top-level API
    "Agent",
    "AgentResult",
    "DataLoader",
    "TaskContext",
    "run_agent",
    "load_data",
    "setup",
    "datasets",

    # Dataset API
    "Dataset",
    "load_dataset_new",  # Backward-compatible alias.
    "DatasetInfo",

    # Types and config
    "TaskDefinition",
    "TaskType",
    "TaskMode",
    "WorkflowCandidate",
    "ReviewResult",
    "Plan",
    "LLMConfig",
    "TaskConfig",

    # Training APIs
    "LitDSAgent",
    "RewardEvaluator",
    "KaggleReward",
    "ClassificationReward",
    "RegressionReward",
    "DatasetConverter",
    "VerlConfigBuilder",

    # ========== Agents ==========
    "BaseAgent",
    "AIDE",
    "AutoKaggle",
    "DataInterpreter",
    "DeepAnalyze",
    "DSAgent",
    "AutoMind",
    "AFlow",
    "SearchStrategy",
    "GreedyStrategy",
    "BeamSearchStrategy",
    "MCTSStrategy",
    "EvolutionaryStrategy",

    # ========== Operators ==========
    "Operator",
    "GenerateCodeAndPlanOperator",
    "PlanOperator",
    "ReviewOperator",
    "SummarizeOperator",
    "ExecuteAndTestOperator",
    "Pipeline",
    "Parallel",
    "Conditional",

    # ========== Services ==========
    "LLMService",
    "SandboxService",
    "WorkspaceService",
    "DataAnalyzer",
    "VDBService",

    # ========== State ==========
    "JournalState",
    "Node",
    "MetricValue",
    "Experience",
    "MemoryManager",
    "ContextManager",

    # ========== Prompts ==========
    "PromptBuilder",
    "create_prompt_template",
    "get_common_guidelines",
    "create_modeling_prompt",
    "create_eda_prompt",
    "create_debug_prompt",

    # Helpers
    "help",
    "list_workflows",
    "show_example",
    "list_prompts",
    "list_operators",
    "explore",

    # Workflows and loaders
    "BaseWorkflowFactory",
    "MLETaskLoader",
]


# ============================================================================
# Default logging setup
# ============================================================================

try:
    import logging
    from rich.logging import RichHandler

    logging.basicConfig(
        level="INFO",
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
        handlers=[RichHandler(show_path=False)],
    )
except ImportError:
    logging.basicConfig(
        level="INFO",
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
