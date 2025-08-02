from typing import Callable
from orionis.container.exceptions import OrionisContainerException

class __IsSubclass:
    """
    Validator that ensures a class is a subclass of a given abstract class.
    """

    def __call__(self, abstract: Callable[..., any], concrete: Callable[..., any]) -> None:
        """
        Validates that the concrete class is a subclass of the abstract class.

        Parameters
        ----------
        abstract : Callable[..., Any]
            The base or abstract class.
        concrete : Callable[..., Any]
            The class to verify.

        Raises
        ------
        OrionisContainerException
            If the concrete class is NOT a subclass of the abstract class.
        """
        if not issubclass(concrete, abstract):
            raise OrionisContainerException(
                "The concrete class must inherit from the provided abstract class. "
                "Please ensure that the concrete class is a subclass of the specified abstract class."
            )

# Exported singleton instance
IsSubclass = __IsSubclass()
