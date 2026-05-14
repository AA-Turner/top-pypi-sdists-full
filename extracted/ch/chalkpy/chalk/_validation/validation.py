from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class Validation(Generic[T]):
    """Specify explicit data validation for a feature.

    The `feature()` function can also specify these validations,
    but this class allows you to specify both strict and non-strict
    validations at the same time.
    """

    def __init__(
        self,
        min: T | None = None,
        max: T | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        strict: bool = False,
    ):
        """Set validation parameters for a feature.

        Parameters
        ----------
        min
            If specified, when this feature is computed, Chalk will check that `x >= min`.
        max
            If specified, when this feature is computed, Chalk will check that `x <= max`.
        min_length
            If specified, when this feature is computed, Chalk will check that `len(x) >= min_length`.
        max_length
            If specified, when this feature is computed, Chalk will check that `len(x) <= max_length`.
        strict
            If `True`, if this feature does not meet the validation criteria, Chalk will not persist
            the feature value and will treat it as failed.

        Examples
        --------
        >>> from chalk.features import features, feature
        >>> @features
        ... class User:
        ...     fico_score: int = feature(
        ...         validations=[
        ...             Validation(min=300, max=850, strict=True),
        ...             Validation(min=300, max=320, strict=False),
        ...             Validation(min=840, max=850, strict=False),
        ...         ]
        ...     )
        ...     # If only one set of validations were needed,
        ...     # you can use the `feature` function instead:
        ...     first_name: str = feature(
        ...         min_length=2, max_length=64, strict=True
        ...     )
        """
        super().__init__()
        self.min = min
        self.max = max
        self.min_length = min_length
        self.max_length = max_length
        self.strict = strict
