r"""Implement the name resolution mechanism.

Please read the documentation to learn more about the name resolution
mechanism.
"""

from __future__ import annotations

__all__ = ["find_matches", "resolve_name"]


from objectory.utils import import_object
from objectory.utils.introspection import get_fully_qualified_name


def resolve_name(name: str, object_names: set[str], allow_import: bool = True) -> str | None:
    r"""Find a match of the query name in the set of object names.

    This function implements a name resolution mechanism that allows
    short names (e.g., "MyClass") to be resolved to fully qualified
    names (e.g., "mymodule.MyClass"). The resolution is successful
    only if there is exactly one object name that matches the query.
    If the name is a fully qualified name not in the set, it will
    attempt to import the module and return the resolved name.

    Args:
        name: The query name to use to find a match in the set of
            object names. Can be a short name or fully qualified name.
        object_names: The set of registered object names to search
            through.
        allow_import: If ``True`` (default), the function will attempt
            to import the module if the name appears to be a fully
            qualified name not in the set.

    Returns:
        The resolved name if the resolution was successful,
            otherwise ``None``

    Example usage:

    ```pycon

    >>> from objectory.utils import resolve_name
    >>> resolve_name("OrderedDict", {"collections.OrderedDict", "collections.Counter"})
    collections.OrderedDict
    >>> resolve_name("objectory.utils.resolve_name", {"math.isclose"})
    'objectory.utils.name_resolution.resolve_name'
    >>> resolve_name("OrderedDict", {"collections.Counter", "math.isclose"})
    None

    ```
    """
    if name in object_names:
        return name

    if len(matches := find_matches(name, object_names)) == 1:
        return next(iter(matches))

    try:
        obj = import_object(name)
    except ImportError:
        return None
    object_name = get_fully_qualified_name(obj)
    if allow_import or object_name in object_names:
        return object_name
    return None


def find_matches(query: str, object_names: set[str]) -> set[str]:
    r"""Find the set of potential names that end with the given query.

    This function searches for all registered object names that end
    with the given query string. It is used when a short identifier
    is provided (e.g., "MyClass") to find all fully qualified names
    that could match (e.g., "pkg1.MyClass", "pkg2.MyClass"). The
    query must be a valid Python identifier.

    Args:
        query: The query string to search for. Must be a valid Python
            identifier (e.g., "MyClass", not "pkg.MyClass").
        object_names: The set of registered object names to search
            through.

    Returns:
        The set of names that match with the query.

    Example usage:

    ```pycon

    >>> from objectory.utils.name_resolution import find_matches
    >>> find_matches("OrderedDict", {"collections.Counter", "math.isclose"})
    set()
    >>> find_matches(
    ...     "OrderedDict", {"collections.OrderedDict", "collections.Counter", "math.isclose"}
    ... )
    {'collections.OrderedDict'}
    >>> find_matches(
    ...     "OrderedDict", {"collections.OrderedDict", "typing.OrderedDict", "math.isclose"}
    ... )
    {...}

    ```
    """
    if not query.isidentifier():
        return set()

    matches = set()
    for name in object_names:
        obj_name = name.rsplit(sep=".", maxsplit=1)[-1]
        if obj_name == query:
            matches.add(name)
    return matches
