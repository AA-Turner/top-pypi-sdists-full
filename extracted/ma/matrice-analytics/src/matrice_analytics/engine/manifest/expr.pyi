"""Auto-generated stub for module: expr."""
from typing import Any

# Functions
def parse_expression(text: str) -> Any:
    """
    Parse ``text`` into a :class:`DerivedExpression`, or raise :class:`ExpressionError`.
    
        Pure syntax: the operands are *not* checked against a pipeline here (the grammar does not
        know what a pipeline is).  :meth:`AppManifest._check_derived` does that with
        :func:`~matrice_analytics.engine.manifest.models.resolve_source`, so an operand and a
        ``metrics[].source`` fail the same way with the same message.
    """
    ...

# Classes
class DerivedExpression:
    # A parsed ``derived[].expr``: its text, its operands, and how to evaluate it.
    #
    #     Immutable and cheap to keep: the manifest parses once at load and the runtime evaluates
    #     the same object every window, so no text is ever re-parsed on the hot path.

    def evaluate(self: Any, values: Any[str, float]) -> float | None:
        """
        The expression's value, or ``None`` when it is **undefined**.
        
                Args:
                    values: ``<stage>.<value>`` → number.  Must contain every name in
                        :attr:`operands`; a missing one is an :class:`EvaluationError` rather than a
                        zero, because a metric that reads zero forever is indistinguishable from a
                        quiet camera (``09`` §3).
        
                Returns:
                    A finite float, or ``None`` when a denominator was zero anywhere in the
                    expression.  ``None`` means "no reading" — the caller publishes no sample for it,
                    which over a whole window is the ``0.0`` every legacy rate publishes.
        
                Raises:
                    EvaluationError: An operand is missing or non-finite, or the arithmetic
                        overflowed.  Never for a zero denominator.
        """
        ...

    def operands(self: Any) -> tuple[str, ...]:
        """
        Every ``<stage>.<value>`` the expression reads, first-appearance order, no repeats.
        
                This is what the manifest resolves against the pipeline — an operand that does not
                resolve is a load error, exactly like a bad ``metrics[].source``.
        """
        ...

class EvaluationError:
    # A parsed expression cannot produce a finite number from these values.
    #
    #     A missing operand, a non-finite operand, or an arithmetic overflow.  Never a zero
    #     denominator — that is ``None`` (undefined), which is a reading, not a fault.

    ...
class ExpressionError:
    # The expression text is not in the grammar. Raised at **load** time only.

    ...
