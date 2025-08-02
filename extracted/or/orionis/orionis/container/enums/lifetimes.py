from enum import Enum, auto

class Lifetime(Enum):
    """
    Represents the lifecycle types used for dependency injection.

    This enumeration defines how and when instances of a dependency are created and shared.

    Attributes
    ----------
    TRANSIENT : Lifetime
        A new instance is created and provided every time the dependency is requested.
    SINGLETON : Lifetime
        A single shared instance is created and used throughout the entire application lifetime.
    SCOPED : Lifetime
        An instance is created and shared within a defined scope (such as per request or session).

    Returns
    -------
    Lifetime
        An enumeration member representing the selected lifecycle type.
    """

    # A new instance is provided every time the dependency is requested.
    TRANSIENT = auto()

    # A single shared instance is provided for the entire application lifetime.
    SINGLETON = auto()

    # An instance is provided per scope (e.g., per request or session).
    SCOPED = auto()
