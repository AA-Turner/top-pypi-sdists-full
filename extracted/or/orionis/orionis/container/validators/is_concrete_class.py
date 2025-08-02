from typing import Callable, Any
from orionis.services.introspection.concretes.reflection import ReflectionConcrete
from orionis.container.exceptions import OrionisContainerTypeError

class __IsConcreteClass:
    """
    Validator that ensures a class is a concrete (non-abstract) class.
    """

    def __call__(self, concrete: Callable[..., Any], lifetime: str) -> None:
        """
        Ensures that the provided class is a concrete (non-abstract) class.

        Parameters
        ----------
        concrete : Callable[..., Any]
            The class intended to represent the concrete implementation.
        lifetime : str
            A string indicating the service lifetime, used in error messages.

        Raises
        ------
        OrionisContainerTypeError
            If the class is abstract or invalid.
        """
        try:
            ReflectionConcrete.ensureIsConcreteClass(concrete)
        except Exception as e:
            raise OrionisContainerTypeError(
                f"Unexpected error registering {lifetime} service: {e}"
            ) from e

# Exported singleton instance
IsConcreteClass = __IsConcreteClass()
