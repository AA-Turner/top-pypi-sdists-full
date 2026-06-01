from typing import Any, Type


def is_instance_or_sandboxed_subclass(arg: Any, param_type: Type) -> bool:
    """Check if arg is an instance of param_type, with a fallback for Temporal sandbox.

    When Temporal's sandbox re-imports modules, it creates duplicate class objects.
    This causes isinstance() to fail even though the classes are semantically identical.
    As a fallback, we compare qualified class names through the MRO.
    """
    if isinstance(arg, param_type):
        return True

    def qualified_name(cls: Type) -> str:
        return f"{cls.__module__}.{cls.__qualname__}"

    expected_name = qualified_name(param_type)
    return any(qualified_name(cls) == expected_name for cls in type(arg).__mro__)
