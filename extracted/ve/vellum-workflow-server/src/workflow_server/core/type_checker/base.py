from abc import ABC, abstractmethod
import dataclasses
import pathlib
from typing import Literal, Optional, Tuple, Union

ConfigurationStatus = Union[
    Tuple[Literal[True], None],
    Tuple[Literal[False], str],
]


@dataclasses.dataclass
class TypeCheckResult:
    success: bool

    type_errors: Optional[str] = None
    failure_message: Optional[str] = None


class WorkflowTypeChecker(ABC):
    def __init__(self) -> None:
        self._is_configured = False

    @abstractmethod
    def is_configured(self) -> ConfigurationStatus:
        pass

    def run(self, dir: pathlib.Path) -> TypeCheckResult:
        if not self._is_configured:
            return TypeCheckResult(
                success=False,
                failure_message="Type checker is not configured",
            )

        res = self._run(dir)
        if res.type_errors:
            res.type_errors = self._clean_type_errors(res.type_errors, dir)

        return res

    @abstractmethod
    def _run(self, dir: pathlib.Path) -> TypeCheckResult:
        pass

    @abstractmethod
    def _clean_type_errors(self, type_errors: str, dir: pathlib.Path) -> str:
        """
        Clean temp directory from type checker output.

        Implementation may be specific to each type checker, depending
        on the working directory used by the type checker.
        """
        pass

    def build_cache(self) -> Optional[str]:
        """Optionally pre-build a cache for the type checker.

        Return a string bubbling up any (non-type) errors that occurred
        while running the type checker.
        """
        pass
