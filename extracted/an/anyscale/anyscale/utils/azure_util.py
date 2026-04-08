from functools import wraps
from typing import Any, Callable

import click

from anyscale.shared_anyscale_utils.conf import ANYSCALE_ENDPOINTS, ANYSCALE_HOST


AZURE_HOSTS = set(ANYSCALE_ENDPOINTS["azure"].values())


def disabled_on_azure(command_name: str) -> Callable[..., Any]:
    """Decorator that disables a CLI command when running against an Azure host."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if ANYSCALE_HOST in AZURE_HOSTS:
                raise click.ClickException(
                    f"`{command_name}` is not supported on Azure, see https://docs.anyscale.com/azure#limitations"
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator
