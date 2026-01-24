from importlib.util import find_spec


def is_dependency_available(name: str) -> bool:
    """
    Check if a dependency is available.

    Parameters
    ----------
    name : str
        The name of the dependency to check.

    Returns
    -------
    bool
        True if the dependency is available, False otherwise.
    """
    return find_spec(name) is not None
