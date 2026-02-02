"""
Preset Agents - Ready-to-Use Agents

Preset agents fully re-exported from DSAT.
"""
try:
    # ========== Manual Workflows ==========
    from dsat.workflows.manual.autokaggle_workflow import AutoKaggleWorkflow
    from dsat.workflows.manual.data_interpreter_workflow import DataInterpreterWorkflow
    from dsat.workflows.manual.deepanalyze_workflow import DeepAnalyzeWorkflow
    from dsat.workflows.manual.dsagent_workflow import DSAgentWorkflow

    # ========== Search Workflows ==========
    from dsat.workflows.search.aide_workflow import AIDEWorkflow
    from dsat.workflows.search.automind_workflow import AutoMindWorkflow
    from dsat.workflows.search.aflow_workflow import AFlowWorkflow

    # Aliases for backward compatibility and simpler naming.
    AIDE = AIDEWorkflow
    AutoKaggle = AutoKaggleWorkflow
    DataInterpreter = DataInterpreterWorkflow
    DeepAnalyze = DeepAnalyzeWorkflow
    DSAgent = DSAgentWorkflow
    AutoMind = AutoMindWorkflow
    AFlow = AFlowWorkflow

except ImportError as e:
    # If DSAT is unavailable, provide placeholders.
    AIDE = None
    AutoKaggle = None
    DataInterpreter = None
    DeepAnalyze = None
    DSAgent = None
    AutoMind = None
    AFlow = None
    AIDEWorkflow = None
    AutoKaggleWorkflow = None
    DataInterpreterWorkflow = None
    DeepAnalyzeWorkflow = None
    DSAgentWorkflow = None
    AutoMindWorkflow = None
    AFlowWorkflow = None

__all__ = [
    # Manual workflows
    "AIDE",
    "AutoKaggle",
    "DataInterpreter",
    "DeepAnalyze",
    "DSAgent",
    # Search workflows
    "AutoMind",
    "AFlow",
    # Full class names
    "AIDEWorkflow",
    "AutoKaggleWorkflow",
    "DataInterpreterWorkflow",
    "DeepAnalyzeWorkflow",
    "DSAgentWorkflow",
    "AutoMindWorkflow",
    "AFlowWorkflow",
]
