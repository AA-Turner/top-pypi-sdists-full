"""Shared execution-record helpers."""

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar

from pydantic import Field
from pydantic.fields import FieldInfo

__all__ = [
    "OmitFromModelContext",
    "is_model_context_projection",
    "model_context_projection",
]

_model_context_projection: ContextVar[bool] = ContextVar("_model_context_projection", default=False)


def is_model_context_projection() -> bool:
    """True while serialization is in model-context projection mode."""
    return _model_context_projection.get()


def OmitFromModelContext(  # noqa: N802  (CapWords: reads as an Annotated Field helper)
    extra_exclude_if: Callable[[object], bool] | None = None,
) -> FieldInfo:
    """Field metadata for ``Annotated[...]`` that omits the field from model context."""

    def _predicate(value: object) -> bool:
        if extra_exclude_if is not None and extra_exclude_if(value):
            return True
        return is_model_context_projection()

    return Field(exclude_if=_predicate)


@contextmanager
def model_context_projection() -> Iterator[None]:
    """Serialize models for the LLM/harness context."""
    token = _model_context_projection.set(True)

    try:
        yield
    finally:
        _model_context_projection.reset(token)
