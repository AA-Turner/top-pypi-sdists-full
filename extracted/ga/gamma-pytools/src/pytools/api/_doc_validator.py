"""
Core implementation of :class:`pytools.api.DocValidator`.
"""

import importlib
import logging
import os
import re
from collections.abc import Collection, Iterable
from glob import glob
from re import Pattern
from types import FunctionType, ModuleType
from typing import Any, TypeVar

from ._alltracker import AllTracker
from ._api import as_tuple
from .doc import (
    APIDefinition,
    DocTest,
    FunctionDefinition,
    HasDocstring,
    HasMatchingParameterDoc,
    HasTypeHints,
    HasWellFormedDocstring,
    ModuleDefinition,
    NamedElementDefinition,
)

log = logging.getLogger(__name__)

#
# Exported names
#

__all__ = ["DocValidator"]

#
# Type variables
#

T_NamedElementDefinition = TypeVar(
    "T_NamedElementDefinition", bound=NamedElementDefinition[Any]
)

#
# Ensure all symbols introduced below are included in __all__
#

__tracker = AllTracker(globals())


#
# Classes
#


class DocValidator:
    """
    Validates docstrings and type hints in all Python sources in a given directory tree.

    By default, only validates public classes, methods, and functions, and
    class initializers (``__init__``).
    Protected classes, methods, and functions are only validated if their name
    is provided in parameter ``validate_protected``.
    """

    #: The root directory of all Python files to be validated.
    root_dir: str

    #: Names of protected functions and methods to be validated.
    validate_protected: tuple[str, ...]

    #: Names of modules for which parameter documentation and type hints should not be
    #: validated.
    exclude_from_parameter_validation: Pattern[str] | None

    #: A dictionary mapping definitions to lists of errors identified during validation.
    validation_errors: dict[str, list[str]]

    #: The documentation tests to run on each definition during validation.
    validation_tests: tuple[DocTest, ...]

    #: The default value for parameter ``validate_protected``.
    DEFAULT_VALIDATE_PROTECTED = ("__init__",)

    #: Default collection of documentation tests to run during validation.
    DEFAULT_VALIDATION_TESTS: tuple[DocTest, ...] = (
        HasDocstring(),
        HasMatchingParameterDoc(),
        HasWellFormedDocstring(),
        HasTypeHints(),
    )

    def __init__(
        self,
        *,
        root_dir: str,
        validate_protected: Iterable[str] | None = None,
        exclude_from_parameter_validation: str | Pattern[str] | None = None,
        additional_tests: Iterable[DocTest] | None = None,
    ) -> None:
        """
        :param root_dir: the root directory of all Python files to be validated
        :param validate_protected: names of protected functions and methods to be
            validated (default: ``%VALIDATE_PROTECTED%``)
        :param exclude_from_parameter_validation: do not validate parameter
            documentation and type hints for classes, methods or functions whose full
            name (including the module prefix) matches the given regular expression
        :param additional_tests: additional documentation tests to run on each API
            element
        """
        self.root_dir = root_dir
        self.validate_protected = as_tuple(
            validate_protected or self.DEFAULT_VALIDATE_PROTECTED,
            element_type=str,
        )
        self.exclude_from_parameter_validation = (
            exclude_from_parameter_validation
            if (
                exclude_from_parameter_validation is None
                or isinstance(exclude_from_parameter_validation, Pattern)
            )
            else re.compile(exclude_from_parameter_validation)
        )

        if not all(name.startswith("_") for name in self.validate_protected):
            raise ValueError("all names in arg validate_protected must start with'_'")

        self.validation_errors = {}
        self.validation_tests = (
            (*self.DEFAULT_VALIDATION_TESTS, *additional_tests)
            if additional_tests
            else self.DEFAULT_VALIDATION_TESTS
        )

    __init__.__doc__ = __init__.__doc__.replace(  # type: ignore
        "%VALIDATE_PROTECTED%", repr(DEFAULT_VALIDATE_PROTECTED)
    )

    def validate_doc(self) -> bool:
        """
        Validate documentation, including docstrings and type annotations.

        :return: ``True`` if the validation was successful; ``False`` if the validation
            failed
        """

        modules = self._load_modules()

        if not modules:
            raise ValueError("no Python modules found")

        self._run_tests(definitions=map(ModuleDefinition, modules))

        for module in modules:
            self._validate_members(
                members=[
                    value
                    for name, value in vars(module).items()
                    if not name.startswith("_")
                ],
                public_module=module.__name__,
            )

        self._log_validation_errors()

        return not self.validation_errors

    def _run_tests(self, definitions: Iterable[APIDefinition]) -> None:
        """
        Run all validation tests on the given definitions, and store errors

        :param definitions: the definitions to run validation tests on
        """
        for definition in definitions:
            errors: list[str] = []
            for test in self.validation_tests:
                test_results = test.test(definition)
                if test_results:
                    if isinstance(test_results, str):
                        errors.append(test_results)
                    else:
                        errors.extend(test_results)
            if errors:
                self.validation_errors[definition.full_name] = errors

    def _validate_members(self, members: Collection[Any], public_module: str) -> None:
        def _filter_excluded(
            kind: type, definition_type: type[T_NamedElementDefinition]
        ) -> Iterable[T_NamedElementDefinition]:
            definitions = (
                definition_type(element=obj, public_module=public_module)
                for obj in members
                if isinstance(obj, kind)
            )

            if self.exclude_from_parameter_validation:
                _pattern = (
                    self.exclude_from_parameter_validation
                )  # https://github.com/python/mypy/issues/4297
                return filter(
                    lambda definition: not _pattern.match(definition.full_name),
                    definitions,
                )
            else:
                return definitions

        classes: list[NamedElementDefinition[type[Any]]] = list(
            _filter_excluded(kind=type, definition_type=NamedElementDefinition)
        )
        functions: Iterable[FunctionDefinition] = _filter_excluded(
            kind=FunctionType, definition_type=FunctionDefinition
        )

        self._run_tests(functions)
        self._run_tests(classes)

        validate_protected = self.validate_protected

        def _filter_protected(name: str) -> bool:
            return name in validate_protected or not name.startswith("_")

        # inspect classes recursively
        for cls in classes:
            self._validate_members(
                members=[
                    attribute
                    for name, attribute in vars(cls.element).items()
                    if _filter_protected(name)
                ],
                public_module=public_module,
            )

    def _log_validation_errors(self) -> None:
        if self.validation_errors:
            log.error(
                "\n"
                + "\n".join(
                    f"{full_name}: {error}"
                    for full_name, errors in self.validation_errors.items()
                    for error in errors
                )
            )

    def _load_modules(self) -> list[ModuleType]:
        # list paths to all python files
        suffix = ".py"
        root_dir = self.root_dir
        prefix_len = len(root_dir) + len(os.sep)
        suffix_len = len(suffix)

        return [
            importlib.import_module(module_path)
            for module_path in (
                path[prefix_len:-suffix_len]
                .replace(os.sep, ".")
                .replace(".__init__", "")
                for path in glob(
                    os.path.join(root_dir, "**", f"*{suffix}"), recursive=True
                )
            )
            if not module_path[module_path.rfind(".") + 1 :].startswith("_")
        ]


__tracker.validate()
