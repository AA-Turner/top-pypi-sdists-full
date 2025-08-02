from typing import Callable, Any
from orionis.services.introspection.abstract.reflection import ReflectionAbstract
from orionis.container.exceptions import OrionisContainerTypeError

class __IsAbstractClass:
    """
    Validator that ensures a class is an abstract class.
    """

    def __call__(self, abstract: Callable[..., Any], lifetime: str) -> None:
        """
        Ensures that the provided class is an abstract class.

        Parameters
        ----------
        abstract : Callable[..., Any]
            The class intended to represent the abstract type.
        lifetime : str
            A string indicating the service lifetime, used in error messages.

        Raises
        ------
        OrionisContainerTypeError
            If the class is not abstract.
        """
        try:
            ReflectionAbstract.ensureIsAbstractClass(abstract)
        except Exception as e:
            raise OrionisContainerTypeError(
                f"Unexpected error registering {lifetime} service: {e}"
            ) from e

# Exported singleton instance
IsAbstractClass = __IsAbstractClass()
