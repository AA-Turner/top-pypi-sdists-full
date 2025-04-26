from enum import Enum
import logging
from typing import Iterable, Optional
import warnings


class StabilityWarning(Warning):
    """Warning for users that a preview feature is being used."""

    pass


class StabilityLevel(Enum):
    """Stability levels for discrete guidelines."""

    ALPHA = "alpha"
    BETA = "beta"


def default_logger(name: str = "benchling_sdk") -> logging.Logger:
    """Construct the default logger for the SDK."""
    logger = logging.getLogger(name)
    logger.addHandler(logging.NullHandler())
    return logger


sdk_logger = default_logger()


def log_deprecation(source_name: str, suggestion: Optional[str] = None) -> None:
    """Log a standardized warning for use of deprecated functionality."""
    message = f"{source_name} is deprecated."
    if suggestion:
        message = f"{message} Please use {suggestion}"
    warnings.warn(
        message=message,
        category=DeprecationWarning,
        # Indicate the line in the caller's code, not this method or the SDK method referencing it
        stacklevel=3,
    )


class NotImplementedWarning(Warning):
    """Warning for users that a feature was shipped but not yet implemented."""

    pass


def log_not_implemented(source_name: str) -> None:
    """Log a standardized warning for use of unimplemented functionality."""
    warnings.warn(
        message=f"{source_name} is not yet implemented and is currently non-functional.",
        category=NotImplementedWarning,
        stacklevel=3,
    )


def log_stability_warning(level: StabilityLevel, package: str = "") -> None:
    """Log a standardized warning for using preview functionality."""
    prefix = "This package"
    if package:
        prefix = f"{prefix} {package}"
    warnings.warn(
        message=f"{prefix} is in {level.value} and not recommended for production use. "
        f"See our stability guidelines for more information: https://docs.benchling.com/docs/stability",
        category=StabilityWarning,
        # Indicate the line in the caller's code, not this method or the SDK method referencing it
        stacklevel=3,
    )


# This doesn't really belong in logging helpers, but we're not moving it for compatibility
# just in case someone else is importing and using it


def check_for_csv_bug_fix(variable: str, value: Optional[Iterable[str]]):
    """Specific error for a fixed bug that might cause breaks. See BNCH-24087."""
    if value:
        value_list = list(value)
        if len(value_list) == 1 and "," in value_list[0]:
            raise ValueError(f"Items in {variable} must not contain ','")
