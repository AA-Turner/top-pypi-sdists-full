from __future__ import annotations

import typing as t
from functools import wraps

import click

from dbt_state.errors import BaseRunCacheError

DECORATOR_RETURN_TYPE = t.TypeVar("DECORATOR_RETURN_TYPE")


def error_handler(
    func: t.Callable[..., DECORATOR_RETURN_TYPE],
) -> t.Callable[..., DECORATOR_RETURN_TYPE]:
    @wraps(func)
    def wrapper(*args: t.Any, **kwargs: t.Any) -> DECORATOR_RETURN_TYPE:
        try:
            return func(*args, **kwargs)
        except (ValueError, BaseRunCacheError) as e:
            click.echo(click.style(str(e), fg="red"))
            exit(1)

    return wrapper
