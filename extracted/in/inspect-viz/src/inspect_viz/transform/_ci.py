from inspect_viz._core.param import Param
from inspect_viz._util.stats import z_score

from ._sql import sql
from ._transform import Transform


def ci_bounds(
    score: str | Param,
    *,
    level: float | None = None,
    stderr: str | Param | None = None,
    lower: str | Param | None = None,
    upper: str | Param | None = None,
) -> tuple[Transform, Transform]:
    """Compute a confidence interval boundary.

    Returns a tuple of two `Transform` objects corresponding to the lower and upper bounds of the confidence interval.

    Specify the confidence interval either as:

    1. A `level` and `stderr` column (where a z-score for level will be offset from the `stderr`); or
    2. Explicit `lower` and `upper` columns which should already be on the desired scale (e.g., z*stderr, bootstrap deltas, HDIs from bayesian posterior distributions, etc.).

    Args:
       score: Column name for score.
       level: Confidence level (e.g. 0.95)
       stderr: Column name for stderr.
       lower: Column name for lower bound.
       upper: Column name for upper bound.
    """
    if lower is not None and upper is not None:
        return sql(f"{score} - ({lower})"), sql(f"{score} + ({upper})")
    elif level is not None and stderr is not None:
        if not 0 < level < 1:
            raise ValueError("level must be between 0 and 1 (exclusive)")

        def bound(sign: str) -> Transform:
            return sql(f"{score} {sign}" + f"({z_score(level)} * {stderr})")

        return bound("-"), bound("+")
    else:
        raise ValueError(
            "You must specify either a 'level' and 'stderr' column or 'lower' and 'upper' columns"
        )
