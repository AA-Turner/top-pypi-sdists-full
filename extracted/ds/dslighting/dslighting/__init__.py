"""
DSLighting - Data Science Agent Framework

An end-to-end automated system for data science tasks.

Quick Start:
    >>> from dslighting import run_agent
    >>> result = run_agent(task_id="bike-sharing-demand")

Documentation: https://github.com/usail-hkust/dslighting
"""

__version__ = "2.6.34"

# ============================================================================
# Top-level API imports
# ============================================================================

from dslighting.api import Agent, AgentResult, DataLoader, TaskContext
from dslighting.api.convenience import run_agent, load_data, setup, analyze, process, model
from dslighting import datasets

# ============================================================================
# Lazy imports for optional modules and backward compatibility
# ============================================================================

def __getattr__(name: str):
    """Lazily resolve optional symbols to keep import time light."""
    import importlib

    # Dataset API
    if name in ("Dataset", "load_dataset", "DatasetInfo"):
        return getattr(importlib.import_module("dslighting.core.dataset"), name)

    # Agents
    if name == "BaseAgent":
        return getattr(importlib.import_module("dslighting.agents"), "BaseAgent")

    if name in ("AIDE", "AutoKaggle", "DataInterpreter", "DeepAnalyze",
                "DSAgent", "AutoMind", "AFlow"):
        return getattr(importlib.import_module("dslighting.agents.presets"), name)

    if name in ("SearchStrategy", "GreedyStrategy", "BeamSearchStrategy",
                "MCTSStrategy", "EvolutionaryStrategy"):
        return getattr(importlib.import_module("dslighting.agents.strategies"), name)

    # Operators
    if name in ("Operator", "GenerateCodeAndPlanOperator", "PlanOperator",
                "ReviewOperator", "SummarizeOperator", "ExecuteAndTestOperator"):
        return getattr(importlib.import_module("dslighting.operators"), name)

    if name in ("Pipeline", "Parallel", "Conditional"):
        return getattr(importlib.import_module("dslighting.operators.orchestration"), name)

    # Services
    if name in ("LLMService", "SandboxService", "WorkspaceService",
                "DataAnalyzer", "VDBService"):
        return getattr(importlib.import_module("dslighting.services"), name)

    # State
    if name in ("JournalState", "Node", "MetricValue", "Experience",
                "MemoryManager", "ContextManager"):
        return getattr(importlib.import_module("dslighting.state"), name)

    # Prompts
    if name in ("PromptBuilder", "create_prompt_template", "get_common_guidelines",
                "create_modeling_prompt", "create_eda_prompt", "create_debug_prompt"):
        return getattr(importlib.import_module("dslighting.prompts"), name)

    # Types
    if name in ("TaskDefinition", "TaskType", "TaskMode", "WorkflowCandidate",
                "ReviewResult", "Plan"):
        return getattr(importlib.import_module("dslighting.core.types"), name)

    if name in ("LLMConfig", "TaskConfig"):
        return getattr(importlib.import_module("dslighting.core.config"), name)

    # Training
    if name in ("LitDSAgent", "RewardEvaluator", "KaggleReward",
                "ClassificationReward", "RegressionReward",
                "DatasetConverter", "VerlConfigBuilder"):
        return getattr(importlib.import_module("dslighting.training"), name)

    # Workflows
    if name in ("BaseWorkflowFactory", "MLETaskLoader"):
        module = importlib.import_module("dslighting.workflows" if name == "BaseWorkflowFactory" else "dslighting.benchmark.loaders")
        return getattr(module, name)

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


# ============================================================================
# Convenience helper functions
# ============================================================================

def help():
    """Show DSLighting help and quick start guide."""
    from dslighting.utils.help import show_help
    show_help()


def list_workflows():
    """List available workflow presets and their usage."""
    from dslighting.utils.help import list_workflows as _list
    _list()


def show_example(workflow: str):
    """Show an example for a given workflow preset."""
    from dslighting.utils.help import show_example as _show
    _show(workflow)


def list_prompts(category: str = "all") -> dict:
    """List available prompt templates by category."""
    from dslighting.prompts import list_available_prompts
    return list_available_prompts(category)


def list_operators(category: str = "all") -> dict:
    """List available operators by category."""
    from dslighting.operators import list_available_operators
    return list_available_operators(category)


def explore():
    """Launch an interactive exploration of DSLighting features."""
    from dslighting.utils.help import explore as _explore
    _explore()


# ============================================================================
# Default logging setup
# ============================================================================

import logging
try:
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


# ============================================================================
# Public exports
# ============================================================================

__all__ = [
    "__version__",
    # Core
    "Agent", "AgentResult", "DataLoader", "TaskContext",
    "run_agent", "load_data", "setup", "analyze", "process", "model", "datasets",
    # Dataset
    "Dataset", "load_dataset", "DatasetInfo",
    # Agents
    "BaseAgent", "AIDE", "AutoKaggle", "DataInterpreter", "DeepAnalyze",
    "DSAgent", "AutoMind", "AFlow",
    "SearchStrategy", "GreedyStrategy", "BeamSearchStrategy",
    "MCTSStrategy", "EvolutionaryStrategy",
    # Operators
    "Operator", "GenerateCodeAndPlanOperator", "PlanOperator",
    "ReviewOperator", "SummarizeOperator", "ExecuteAndTestOperator",
    "Pipeline", "Parallel", "Conditional",
    # Services
    "LLMService", "SandboxService", "WorkspaceService",
    "DataAnalyzer", "VDBService",
    # State
    "JournalState", "Node", "MetricValue", "Experience",
    "MemoryManager", "ContextManager",
    # Prompts
    "PromptBuilder", "create_prompt_template", "get_common_guidelines",
    "create_modeling_prompt", "create_eda_prompt", "create_debug_prompt",
    # Types
    "TaskDefinition", "TaskType", "TaskMode", "WorkflowCandidate",
    "ReviewResult", "Plan", "LLMConfig", "TaskConfig",
    # Training
    "LitDSAgent", "RewardEvaluator", "KaggleReward",
    "ClassificationReward", "RegressionReward",
    "DatasetConverter", "VerlConfigBuilder",
    # Helpers
    "help", "list_workflows", "show_example", "list_prompts",
    "list_operators", "explore",
    "BaseWorkflowFactory", "MLETaskLoader",
]
