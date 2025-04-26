from typing import Optional, Callable

from vessl.util.echo import print_warning


def deprecation_warning(target_command: str, new_command: Optional[str] = None):
    warning_text = f"The '{target_command}' command is deprecated and will be removed in a future release. "
    if new_command is not None:
        warning_text+=f"Please use the '{new_command}' command instead."
    print_warning(warning_text)


def deprecated(target_command: str, new_command: Optional[str] = None):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            deprecation_warning(target_command, new_command)
            return func(*args, **kwargs)
        return wrapper
    return decorator
