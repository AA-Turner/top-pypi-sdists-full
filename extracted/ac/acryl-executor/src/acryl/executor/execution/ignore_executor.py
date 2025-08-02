from acryl.executor.context.execution_context import ExecutionContext
from acryl.executor.execution.executor import Executor
from acryl.executor.request.execution_request import ExecutionRequest
from acryl.executor.request.signal_request import SignalRequest
from acryl.executor.result.execution_result import ExecutionResult, Type


class IgnoreExecutor(Executor):
    """Ignores CLI Execution Requests"""

    def __init__(self, id: str) -> None:
        self.id = id

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        ctx = ExecutionContext(request)
        return ExecutionResult(ctx, Type.RUNNING)

    def signal(self, request: SignalRequest) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def get_id(self) -> str:
        return self.id
