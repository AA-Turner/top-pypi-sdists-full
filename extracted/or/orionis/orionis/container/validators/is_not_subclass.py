from typing import Callable
from orionis.container.exceptions import OrionisContainerException

class __IsNotSubclass:
    """
    Validator that ensures a class is NOT a subclass of another class.
    """

    def __call__(self, abstract: Callable[..., any], concrete: Callable[..., any]) -> None:
        """
        Validates that the concrete class is NOT a subclass of the abstract class.

        Parameters
        ----------
        abstract : Callable[..., Any]
            The supposed base class or interface.
        concrete : Callable[..., Any]
            The implementation class to check.

        Raises
        ------
        OrionisContainerException
            If the concrete class IS a subclass of the abstract class.
        """
        if issubclass(concrete, abstract):
            raise OrionisContainerException(
                "The concrete class must NOT inherit from the provided abstract class. "
                "Please ensure that the concrete class is not a subclass of the specified abstract class."
            )

# Exported singleton instance
IsNotSubclass = __IsNotSubclass()
