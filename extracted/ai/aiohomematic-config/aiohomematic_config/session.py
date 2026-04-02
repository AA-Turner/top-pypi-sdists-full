"""
Configuration editing session with change tracking.

Tracks parameter modifications during an editing session, providing
undo/redo, dirty state detection, and validation before write.

Public API of this module is defined by __all__.
"""

from collections.abc import Mapping
from dataclasses import dataclass
import inspect
from typing import Any, Final

from aiohomematic.const import ParameterData
from aiohomematic.parameter_tools import (
    ParamsetChange,
    ValidationResult,
    diff_paramset,
    validate_cross_parameters,
    validate_paramset,
)


@dataclass(frozen=True)
class _UndoEntry:
    """A single undo/redo entry."""

    parameter: str
    old_value: Any
    new_value: Any


class ConfigSession:
    """
    Track changes during a configuration editing session.

    Provides change tracking, undo/redo, dirty state detection,
    validation, and export of changed values for put_paramset.
    """

    __slots__ = (
        "_current_values",
        "_descriptions",
        "_initial_values",
        "_redo_stack",
        "_undo_stack",
    )

    def __init__(
        self,
        *,
        descriptions: Mapping[str, ParameterData],
        initial_values: dict[str, Any],
    ) -> None:
        """Initialize the configuration session."""
        self._descriptions: Final = descriptions
        self._initial_values: Final[dict[str, Any]] = dict(initial_values)
        self._current_values: dict[str, Any] = dict(initial_values)
        self._undo_stack: list[_UndoEntry] = []
        self._redo_stack: list[_UndoEntry] = []

    @property
    def can_redo(self) -> bool:
        """Return True if redo is possible."""
        return len(self._redo_stack) > 0

    @property
    def can_undo(self) -> bool:
        """Return True if undo is possible."""
        return len(self._undo_stack) > 0

    @property
    def is_dirty(self) -> bool:
        """Return True if any parameter differs from the initial value."""
        return self._current_values != self._initial_values

    def discard(self) -> None:
        """Discard all changes and revert to initial values."""
        self._current_values = dict(self._initial_values)
        self._undo_stack.clear()
        self._redo_stack.clear()

    def get_changed_parameters(self) -> dict[str, ParamsetChange]:
        """Return a detailed diff between initial and current values."""
        result: dict[str, ParamsetChange] = diff_paramset(
            descriptions=self._descriptions,
            baseline=self._initial_values,
            current=self._current_values,
        )
        return result

    def get_changes(self) -> dict[str, Any]:
        """
        Return only the parameters that differ from initial values.

        Suitable for passing directly to put_paramset.
        """
        return {
            param: value for param, value in self._current_values.items() if self._initial_values.get(param) != value
        }

    def get_current_value(self, *, parameter: str) -> Any:
        """Return the current value of a parameter."""
        return self._current_values.get(parameter)

    def redo(self) -> bool:
        """
        Redo the last undone change.

        Returns True if a redo was performed, False if nothing to redo.
        """
        if not self._redo_stack:
            return False
        entry = self._redo_stack.pop()
        self._undo_stack.append(entry)
        self._current_values[entry.parameter] = entry.new_value
        return True

    def reset_to_defaults(self) -> None:
        """Reset all values to their DEFAULT from parameter descriptions."""
        for param, pd in self._descriptions.items():
            default = pd.get("DEFAULT")
            if default is not None and param in self._current_values:
                self.set(parameter=param, value=default)

    def set(self, *, parameter: str, value: Any) -> None:
        """
        Set a parameter value, recording the change for undo.

        Clears the redo stack since the user has diverged from the redo path.
        """
        if (old_value := self._current_values.get(parameter)) == value:
            return
        self._undo_stack.append(_UndoEntry(parameter=parameter, old_value=old_value, new_value=value))
        self._redo_stack.clear()
        self._current_values[parameter] = value

    def undo(self) -> bool:
        """
        Undo the last change.

        Returns True if an undo was performed, False if nothing to undo.
        """
        if not self._undo_stack:
            return False
        entry = self._undo_stack.pop()
        self._redo_stack.append(entry)
        self._current_values[entry.parameter] = entry.old_value
        return True

    def validate(self) -> dict[str, ValidationResult]:
        """
        Validate all current values against their descriptions.

        Returns only failures. An empty dict means all values are valid.
        Includes both single-parameter and cross-parameter validation.
        """
        result: dict[str, ValidationResult] = validate_paramset(
            descriptions=self._descriptions,
            values=self._current_values,
        )
        # Add cross-parameter validation errors
        for param_id, error_key in validate_cross_parameters(
            values=self._current_values,
        ).items():
            if param_id not in result:
                result[param_id] = ValidationResult(valid=False, reason=error_key)
        return result

    def validate_changes(self) -> dict[str, ValidationResult]:
        """
        Validate only the changed values.

        Returns only failures for parameters that differ from initial values.
        Includes cross-parameter validation against the full current state.
        """
        if not (changes := self.get_changes()):
            return {}
        result: dict[str, ValidationResult] = validate_paramset(
            descriptions=self._descriptions,
            values=changes,
        )
        # Cross-validate changes merged with current state
        for param_id, error_key in validate_cross_parameters(
            values=changes,
            current_values=self._current_values,
        ).items():
            if param_id not in result:
                result[param_id] = ValidationResult(valid=False, reason=error_key)
        return result


__all__ = tuple(
    sorted(
        name
        for name, obj in globals().items()
        if not name.startswith("_")
        and (name.isupper() or inspect.isfunction(obj) or inspect.isclass(obj))
        and getattr(obj, "__module__", __name__) == __name__
    )
)
