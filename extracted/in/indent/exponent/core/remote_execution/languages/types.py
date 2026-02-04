from dataclasses import dataclass


@dataclass
class StreamedOutputPiece:
    content: str


@dataclass
class ShellExecutionResult:
    output: str
    cancelled_for_timeout: bool
    exit_code: int | None
    halted: bool = False
