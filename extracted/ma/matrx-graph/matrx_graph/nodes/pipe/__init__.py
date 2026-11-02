"""THE THREE PIPES — one step, three interchangeable executors.

Public surface: the ``pipe.step`` executor, its contract/config types, the
pure pipe-selection function, and the host injection seam for the AI pipe.
"""

from matrx_graph.nodes.pipe.contract import (
    PIPES,
    RUN_PIPE_VARIABLE,
    AiPipe,
    CodePipe,
    HumanPipe,
    Pipe,
    PipeBindings,
    PipePolicy,
    PipeSelection,
    PipeStepConfig,
    StepContract,
    run_pipe_override,
    select_pipe,
)
from matrx_graph.nodes.pipe.step import (
    AiPipeRequest,
    AiPipeRunner,
    PipeStepExecutor,
    PipeStepInput,
    PipeStepOutput,
    ai_pipe_configured,
    set_ai_pipe_runner,
)

__all__ = [
    "PIPES",
    "RUN_PIPE_VARIABLE",
    "AiPipe",
    "AiPipeRequest",
    "AiPipeRunner",
    "CodePipe",
    "HumanPipe",
    "Pipe",
    "PipeBindings",
    "PipePolicy",
    "PipeSelection",
    "PipeStepConfig",
    "PipeStepExecutor",
    "PipeStepInput",
    "PipeStepOutput",
    "StepContract",
    "ai_pipe_configured",
    "run_pipe_override",
    "select_pipe",
    "set_ai_pipe_runner",
]
