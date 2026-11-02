"""Immutable worker report identity for exact transport replay."""

from dataclasses import dataclass

from labqoat.json_document import JsonDocument


@dataclass(frozen=True)
class FitReport:
    """Capture monotonically increasing elapsed usage before issuing any request."""

    sequence: int
    elapsed_ms: int
    stopped: bool

    def __post_init__(self) -> None:
        """Bound counters to interoperable JSON integers and reject implicit scalar coercion."""
        for number in (self.sequence, self.elapsed_ms):
            if type(number) is not int or not 0 <= number <= 9_007_199_254_740_991:
                raise ValueError("Fit usage must use nonnegative portable integers")
        if type(self.stopped) is not bool:
            raise ValueError("Fit stopping must be explicit")

    def to_dict(self) -> JsonDocument:
        """Return the exact immutable report envelope."""
        return JsonDocument(sequence=self.sequence, elapsed_ms=self.elapsed_ms, stopped=self.stopped)
