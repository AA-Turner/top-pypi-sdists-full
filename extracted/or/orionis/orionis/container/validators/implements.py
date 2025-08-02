from typing import Callable, Any
from orionis.services.introspection.objects.types import Type
from orionis.container.exceptions import OrionisContainerException

class __ImplementsAbstractMethods:
    """
    Validator that ensures a concrete class or instance implements all abstract methods of an abstract class.
    """

    def __call__(
        self,
        *,
        abstract: Callable[..., Any] = None,
        concrete: Callable[..., Any] = None,
        instance: Any = None
    ) -> None:
        """
        Validates that a concrete class or instance implements all abstract methods defined in an abstract class.

        Parameters
        ----------
        abstract : Callable[..., Any]
            The abstract base class.
        concrete : Callable[..., Any], optional
            The class expected to implement the abstract methods.
        instance : Any, optional
            The instance expected to implement the abstract methods.

        Raises
        ------
        OrionisContainerException
            If any abstract method is not implemented.
        """

        # Validate that the abstract class is provided
        if abstract is None:
            raise OrionisContainerException("Abstract class must be provided for implementation check.")

        # Check if the abstract class has abstract methods
        abstract_methods = getattr(abstract, '__abstractmethods__', set())
        if not abstract_methods:
            raise OrionisContainerException(
                f"The abstract class '{abstract.__name__}' does not define any abstract methods. "
                "An abstract class must have at least one abstract method."
            )

        # Determine the target class or instance to check
        target = concrete if concrete is not None else instance
        if target is None:
            raise OrionisContainerException("Either concrete class or instance must be provided for implementation check.")

        # Validate that the target is a class or instance
        target_class = target if Type(target).isClass() else target.__class__
        target_name = target_class.__name__
        abstract_name = abstract.__name__

        # Check if the target class implements all abstract methods
        not_implemented = []
        for method in abstract_methods:
            expected_method = str(method).replace(f"_{abstract_name}", f"_{target_name}")
            if not expected_method in target_class.__dict__:
                not_implemented.append(method)

        # If any abstract methods are not implemented, raise an exception
        if not_implemented:
            formatted = "\n  • " + "\n  • ".join(not_implemented)
            raise OrionisContainerException(
                f"'{target_name}' does not implement the following abstract methods defined in '{abstract_name}':{formatted}\n"
                "Please ensure that all abstract methods are implemented."
            )

# Exported singleton instance
ImplementsAbstractMethods = __ImplementsAbstractMethods()