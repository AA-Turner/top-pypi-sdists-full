from typing import Any
from orionis.services.introspection.instances.reflection import ReflectionInstance
from orionis.container.exceptions import OrionisContainerTypeError

class __IsInstance:
    """
    Validator that ensures the provided object is a valid instance (not a class or abstract type).
    """

    def __call__(self, instance: Any) -> None:
        """
        Ensures that the provided object is a valid instance.

        Parameters
        ----------
        instance : Any
            The object to be validated.

        Raises
        ------
        OrionisContainerTypeError
            If the object is not a valid instance.
        """
        try:
            ReflectionInstance.ensureIsInstance(instance)
        except Exception as e:
            raise OrionisContainerTypeError(
                f"Error registering instance: {e}"
            ) from e

# Exported singleton instance
IsInstance = __IsInstance()
