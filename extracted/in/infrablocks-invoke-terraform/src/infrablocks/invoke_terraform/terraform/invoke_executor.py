from typing import IO, Iterable

from invoke.context import Context

from .terraform import Environment, Executor


class InvokeExecutor(Executor):
    def __init__(self, context: Context):
        self._context = context

    def execute(
        self,
        command: Iterable[str],
        environment: Environment | None = None,
        stdout: IO[str] | None = None,
        stderr: IO[str] | None = None,
    ) -> None:
        self._context.run(
            " ".join(command),
            env=(environment if environment is not None else {}),
            out_stream=stdout,
            err_stream=stderr,
        )
