#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see http://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Module for typing related functionality."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable

    from invenio_records_resources.records.api import Record
    from invenio_records_resources.services.records.results import RecordItem


def require_kwargs(*kwargs_names: str) -> Any:
    """Wrap function to require specific kwargs in a function call.

    This decorator is used to fix typing errors in inherited classes where the base class defines kwargs and the
    inherited class needs to access a specific kwarg.

    Example:
    ```python
    # base class
    class ConditionalGenerator(
        InvenioConditionalGenerator, ABC
    ):
        @abstractmethod
        def _condition(
            self, **kwargs: Any
        ) -> bool: ...


    # inherited class
    class IfRecordHasField(
        ConditionalGenerator
    ):
        @override
        @require_kwargs("field")
        def _condition(
            self, *, field, **kwargs: Any
        ) -> bool: ...
    ```

    """

    def wrapper(f: Callable) -> Callable:
        def wrapped_f(*args: Any, **kwargs: Any) -> Any:
            for kwarg_name in kwargs_names:
                if kwarg_name not in kwargs:
                    raise ValueError(f"Keyword argument {kwarg_name} not found in function call.")
            return f(*args, **kwargs)

        return wrapped_f

    return wrapper


def record_from_result(result: RecordItem) -> Record:
    """Convert a RecordItem to a Record."""
    return result._record  # noqa: SLF001
