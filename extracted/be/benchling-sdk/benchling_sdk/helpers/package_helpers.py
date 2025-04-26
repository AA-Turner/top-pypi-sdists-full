import collections
from contextlib import ContextDecorator
from enum import Enum
from typing import Iterable, Union


class MissingExtrasError(Exception):
    """
    Missing extras error.

    Some SDK functionality requires optional extras packages are installed. Certain code paths
    may still be usable without them, so we ship all SDK features but will raise this error at
    runtime if a particular dependency is missing for code that requires it.
    """

    pass


class ExtrasPackage(Enum):
    """Names of optional extras packages in the SDK."""

    CRYPTOGRAPHY = "cryptography"
    PYTHON_JOSE = "python-jose"


class _required_packages_context(ContextDecorator):
    """
    Context Manager to run code with required packages.

    That will re-raise MissingExtrasError if it finds a missing module or import
    expected to be optionally installed as an extras package.
    """

    _required_packages: Iterable[ExtrasPackage]

    def __init__(
        self,
        required_packages: Union[ExtrasPackage, Iterable[ExtrasPackage]],
    ):
        """
        Initialize RequiredPackagesContext.

        :param required_packages: A list of enumerated packages expected for successful execution.
        """
        packages = (
            required_packages
            if isinstance(required_packages, collections.abc.Iterable)
            else [required_packages]
        )
        self._required_packages = packages

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type in (ImportError, ModuleNotFoundError):
            package_names = ", ".join([package.value for package in self._required_packages])
            raise MissingExtrasError(
                f"One or more missing optional packages must be installed to use this functionality. "
                f"Please install [{package_names}] as extras.",
                exc_value,
            )
        elif exc_value:
            raise exc_value
