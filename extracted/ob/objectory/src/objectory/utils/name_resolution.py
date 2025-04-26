"""Implement the name resolution mechanism.

Please read the documentation to learn more about the name resolution
mechanism.
"""

from __future__ import annotations

__all__ = ["resolve_name", "find_matches"]


from objectory.utils.object_helpers import full_object_name, import_object


def resolve_name(name: str, object_names: set[str], allow_import: bool = True) -> str | None:
    r"""Find a match of the query name in the set of object names.

    The resolution is successful only if there is only one object
    name that can match with the query name.
    Please read the documentation to learn more about the name
    resolution mechanism.

    Args:
        name: Specifies the query name to use to find a match
            in the set of object names.
        object_names: Specifies the set of object names.
        allow_import: If ``True``, the parent package
            is installed if it was not imported previously.

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
        return list(matches)[0]

    if (obj := import_object(name)) is not None:
        object_name = full_object_name(obj)
        if allow_import or object_name in object_names:
            return object_name
    return None


def find_matches(query: str, object_names: set[str]) -> set[str]:
    r"""Find the set of potential names that ends with the given query.

    This function is used when the user only specify a valid object
    identifier. For example, the user only gives the class name
    instead of the full name (module name + class name).
    This function will try to find the list of registered objects
    that can match with the query name.

    Args:
        query: Specifies the query.
        object_names: Specifies the set of object names where
            to look for the query.

    Returns:
        The list of names that matches with the query.

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
