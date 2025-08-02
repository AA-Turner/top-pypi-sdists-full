from abc import ABC, abstractmethod
from typing import Any, Callable
from orionis.container.contracts.container import IContainer
from orionis.container.entities.binding import Binding
from orionis.services.introspection.dependencies.entities.method_dependencies import MethodDependency

class IResolver(ABC):
    """
    Interface for dependency resolution in the container system.

    This interface defines the contract for resolvers that handle
    dependency injection and instance creation based on bindings.
    """

    @abstractmethod
    def __init__(self, container: IContainer) -> None:
        """
        Initialize the resolver with a container reference.

        Parameters
        ----------
        container : IContainer
            The container instance that this resolver will use to resolve dependencies.
        """
        pass

    @abstractmethod
    def resolve(
        self,
        binding: Binding,
        *args,
        **kwargs
    ) -> Any:
        """
        Resolves an instance from a binding.

        This method resolves an instance based on the binding's lifetime and type.
        It delegates to specific resolution methods based on the lifetime (transient, singleton, or scoped).

        Parameters
        ----------
        binding : Binding
            The binding to resolve.
        *args : tuple
            Additional positional arguments to pass to the constructor.
        **kwargs : dict
            Additional keyword arguments to pass to the constructor.

        Returns
        -------
        Any
            The resolved instance.

        Raises
        ------
        OrionisContainerException
            If the binding is not an instance of Binding or if resolution fails.
        """
        pass

    @abstractmethod
    def resolveType(
        self,
        type_: Callable[..., Any],
        *args,
        **kwargs
    ) -> Any:
        """
        Forces resolution of a type whether it's registered in the container or not.

        Parameters
        ----------
        type_ : Callable[..., Any]
            The type or callable to resolve.
        *args : tuple
            Positional arguments to pass to the constructor/callable.
        **kwargs : dict
            Keyword arguments to pass to the constructor/callable.

        Returns
        -------
        Any
            The resolved instance.

        Raises
        ------
        OrionisContainerException
            If the type cannot be resolved.
        """
        pass

    @abstractmethod
    def resolveSignature(
        self,
        signature: MethodDependency
    ) -> dict:
        """
        Resolves dependencies defined in a method signature.

        Parameters
        ----------
        signature : MethodDependency
            The method dependency information to resolve.

        Returns
        -------
        dict
            A dictionary of resolved parameter values.

        Raises
        ------
        OrionisContainerException
            If any dependencies cannot be resolved.
        """
        pass