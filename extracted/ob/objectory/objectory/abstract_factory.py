r"""Implement the ``AbstractFactory`` metaclass used to create abstract
factories.

This module provides an abstract factory implementation that allows
automatic registration and instantiation of classes and functions.
"""

from __future__ import annotations

__all__ = ["AbstractFactory", "is_abstract_factory", "register", "register_child_classes"]

import inspect
import logging
from abc import ABCMeta
from typing import TYPE_CHECKING, Any

from objectory.errors import (
    AbstractFactoryTypeError,
    IncorrectObjectFactoryError,
    UnregisteredObjectFactoryError,
)
from objectory.utils import (
    all_child_classes,
    get_fully_qualified_name,
    import_object,
    instantiate_object,
    is_lambda_function,
    resolve_name,
)

if TYPE_CHECKING:
    from collections.abc import Callable

logger: logging.Logger = logging.getLogger(__name__)


class AbstractFactory(ABCMeta):
    r"""Implement the abstract factory metaclass to create factories
    automatically.

    Please read the documentation about this abstract factory to
    learn how it works and how to use it.

    To avoid potential conflicts with the other classes, all the
    non-public attributes or functions starts with
    ``_abstractfactory_****`` where ``****`` is the name of the
    attribute or the function.

    Args:
        name: The class name. This becomes the ``__name__`` attribute
            of the class.
        bases: A tuple of the base classes from which the class
            inherits. This becomes the ``__bases__`` attribute of the
            class.
        dct: A namespace dictionary containing definitions for the
            class body. This becomes the ``__dict__`` attribute of the
            class.

    Example usage:

    ```pycon

    >>> from objectory import AbstractFactory
    >>> class BaseClass(metaclass=AbstractFactory):
    ...     pass
    ...
    >>> class MyClass(BaseClass):
    ...     pass
    ...
    >>> obj = BaseClass.factory("MyClass")
    >>> obj
    <....MyClass object at 0x...>

    ```
    """

    def __init__(cls, name: str, bases: tuple[type, ...], dct: dict[str, Any]) -> None:
        if not hasattr(cls, "_abstractfactory_inheritors"):
            cls._abstractfactory_inheritors = {}
        cls.register_object(cls)
        super().__init__(name, bases, dct)

    @property
    def inheritors(cls) -> dict[str, Any]:
        r"""Get the inheritors.

        Returns:
            The inheritors.

        Example usage:

        ```pycon

        >>> from objectory import AbstractFactory
        >>> class BaseClass(metaclass=AbstractFactory):
        ...     pass
        ...
        >>> class MyClass(BaseClass):
        ...     pass
        ...
        >>> BaseClass.inheritors
        {'....BaseClass': <class '....BaseClass'>, '....MyClass': <class '....MyClass'>}

        ```
        """
        return cls._abstractfactory_inheritors

    def factory(cls, _target_: str, *args: Any, _init_: str = "__init__", **kwargs: Any) -> Any:
        r"""Instantiate dynamically an object given its configuration.

        This method creates an instance of a registered class or calls
        a registered function. The target can be specified using either
        the short name (e.g., "MyClass") or the fully qualified name
        (e.g., "mymodule.MyClass"). If the target is not yet registered,
        it will attempt to import and register it automatically.

        Args:
            _target_: The name of the object (class or function) to
                instantiate. It can be the class name or the full
                class name. Supports name resolution for registered
                objects.
            *args: Positional arguments to pass to the class
                constructor or function.
            _init_: The function or method to use to create the object.
                If ``"__init__"`` (default), the object is created by
                calling the constructor. Can also be ``"__new__"`` or
                the name of a class method.
            **kwargs: Keyword arguments to pass to the class
                constructor or function.

        Returns:
            The instantiated object with the given parameters.

        Raises:
            AbstractClassAbstractFactoryError: when an abstract
                class is instantiated.
            UnregisteredClassAbstractFactoryError: when the target
                is not found.

        Example usage:

        ```pycon

        >>> from objectory import AbstractFactory
        >>> class BaseClass(metaclass=AbstractFactory):
        ...     pass
        ...
        >>> class MyClass(BaseClass):
        ...     pass
        ...
        >>> obj = BaseClass.factory("MyClass")
        >>> obj
        <....MyClass object at 0x...>

        ```
        """
        return instantiate_object(
            cls._abstractfactory_get_target_from_name(_target_), *args, _init_=_init_, **kwargs
        )

    def register_object(cls, obj: type | Callable) -> None:
        r"""Register a class or function to the factory.

        This method manually registers a class or function with the
        factory, making it available for instantiation. This is
        particularly useful when working with third-party libraries
        where you cannot modify the source code to inherit from the
        factory. The object is registered using its fully qualified
        name. If an object with the same name already exists, it will
        be replaced with a warning.

        Args:
            obj: The class or function to register to the factory.
                Must be a valid class or function object (not a lambda
                function).

        Raises:
            IncorrectObjectAbstractFactoryError: if the object is not
                a class or function, or if it is a lambda function.

        Example usage:

        ```pycon

        >>> from objectory import AbstractFactory
        >>> class BaseClass(metaclass=AbstractFactory):
        ...     pass
        ...
        >>> class MyClass:
        ...     pass
        ...
        >>> BaseClass.register_object(MyClass)
        >>> BaseClass.inheritors
        {...}

        ```
        """
        cls._abstractfactory_check_object(obj)
        name = get_fully_qualified_name(obj)
        if (
            cls._abstractfactory_is_name_registered(name)
            and cls._abstractfactory_inheritors[name] != obj
        ):
            logger.warning(f"The class {name} already exists. The new class replaces the old one")

        cls._abstractfactory_inheritors[name] = obj

    def unregister(cls, name: str) -> None:
        r"""Remove a registered object from the factory.

        This method removes a class or function from the factory's
        registry. The object will no longer be available for
        instantiation through the factory. This is an experimental
        function and may change in the future.

        Args:
            name: The name of the object to remove. Can be either the
                short name (e.g., "MyClass") or the fully qualified
                name (e.g., "mymodule.MyClass"). This function uses
                the name resolution mechanism to find the full name if
                only the short name is given.

        Example usage:

        ```pycon

        >>> from objectory import AbstractFactory
        >>> class BaseClass(metaclass=AbstractFactory):
        ...     pass
        ...
        >>> class MyClass:
        ...     pass
        ...
        >>> BaseClass.register_object(MyClass)
        >>> BaseClass.unregister("MyClass")
        >>> BaseClass.inheritors
        {'....BaseClass': <class '....BaseClass'>}

        ```
        """
        resolved_name = cls._abstractfactory_resolve_name(name)
        if resolved_name is None or not cls._abstractfactory_is_name_registered(resolved_name):
            msg = (
                f"It is not possible to remove an object which is not registered (received: {name})"
            )
            raise UnregisteredObjectFactoryError(msg)
        cls._abstractfactory_inheritors.pop(resolved_name)

    def _abstractfactory_get_target_from_name(cls, name: str) -> type | Callable:
        """Get the class or function to use given its name.

        Args:
            name: The name of the class or function.

        Returns:
            The class or function.

        Raises:
            UnregisteredObjectFactoryError: if it is not possible
                to find the target.
        """
        resolved_name = cls._abstractfactory_resolve_name(name)
        if resolved_name is None:
            msg = (
                f"Unable to create the object `{name}` because it is not registered. "
                f"Registered objects of {cls.__qualname__} "
                f"are {set(cls._abstractfactory_inheritors.keys())}"
            )
            raise UnregisteredObjectFactoryError(msg)
        if not cls._abstractfactory_is_name_registered(resolved_name):
            cls.register_object(import_object(resolved_name))
        return cls._abstractfactory_inheritors[resolved_name]

    def _abstractfactory_resolve_name(cls, name: str) -> str | None:
        r"""Try to resolve the name.

        This function will look at if it can find an object which
        match with the given name. It is quite useful because there
        are several ways to load an object but only one can be
        registered. If you specify a full name (module path +
        class/function name), it will try to import the module
        and registered it if it is not registered yet.

        Args:
            name: The name of the class or function to resolve.

        Returns:
            The name to use to get the object if the
                resolution was successful, otherwise ``None``.
        """
        return resolve_name(name, set(cls._abstractfactory_inheritors.keys()))

    def _abstractfactory_is_name_registered(cls, name: str) -> bool:
        r"""Indicate if the name exists or not in the factory.

        Args:
            name: The name to check.

        Returns:
            ``True`` if the name exists, otherwise ``False``.
        """
        return name in cls._abstractfactory_inheritors

    def _abstractfactory_check_object(cls, obj: type | Callable) -> None:
        r"""Check if the object is valid for this factory before
        registering it.

        This function will raise an exception if the object is not
        valid.

        Args:
            obj: The object to check.

        Raises:
            IncorrectObjectFactoryError: if it is an invalid
                object for this factory.
        """
        if not (inspect.isclass(obj) or inspect.isfunction(obj)):
            msg = f"It is possible to register only a class or a function (received: {obj})"
            raise IncorrectObjectFactoryError(msg)
        if is_lambda_function(obj):
            msg = (
                "It is not possible to register a lambda function. "
                "Please use a regular function instead"
            )
            raise IncorrectObjectFactoryError(msg)


def register(cls: AbstractFactory) -> Callable:
    r"""Define a decorator to register a function to a factory.

    This decorator is designed to register functions that return
    an object of a class registered in the factory.

    Args:
        cls: The class where to register the function. Must be a
            class that uses the ``AbstractFactory`` metaclass.

    Returns:
        The decorated function.

    Example usage:

    ```pycon

    >>> from objectory.abstract_factory import AbstractFactory, register
    >>> class BaseClass(metaclass=AbstractFactory):
    ...     pass
    ...
    >>> @register(BaseClass)
    ... def function_to_register(value: int) -> int:
    ...     return value + 2
    ...
    >>> BaseClass.factory("function_to_register", 40)
    42

    ```
    """

    def wrapped(func: Callable) -> Callable:
        cls.register_object(func)
        return func

    return wrapped


def register_child_classes(
    factory_cls: AbstractFactory | type, cls: type, ignore_abstract_class: bool = True
) -> None:
    r"""Register the given class and its child classes.

    This function registers all the child classes including the child
    classes of the child classes, etc.

    Args:
        factory_cls: The factory class. The child classes will be
            registered to this class.
        cls: The class to register along with its child classes.
        ignore_abstract_class: Indicate if the abstract classes
            should be ignored or not. By default, the abstract classes
            are not registered because they cannot be instantiated.

    Raises:
        AbstractFactoryTypeError: if the factory class does not
            implement the ``AbstractFactory`` metaclass.

    Example usage:

    ```pycon

    >>> from objectory.abstract_factory import AbstractFactory, register_child_classes
    >>> class BaseClass(metaclass=AbstractFactory):
    ...     pass
    ...
    >>> register_child_classes(BaseClass, dict)

    ```
    """
    if not is_abstract_factory(factory_cls):
        msg = (
            "It is not possible to register child classes because the factory class does "
            f"not implement the {AbstractFactory.__qualname__} metaclass"
        )
        raise AbstractFactoryTypeError(msg)

    for class_to_register in [cls, *list(all_child_classes(cls))]:
        if ignore_abstract_class and inspect.isabstract(class_to_register):
            continue
        factory_cls.register_object(class_to_register)


def is_abstract_factory(cls: Any) -> bool:
    r"""Indicate if a class implements the ``AbstractFactory`` metaclass.

    Args:
        cls: The class to check.

    Returns:
        ``True`` if the class implements the ``AbstractFactory``
            metaclass, otherwise ``False``.

    Example usage:

    ```pycon

    >>> from objectory.abstract_factory import AbstractFactory, is_abstract_factory
    >>> class BaseClass(metaclass=AbstractFactory):
    ...     pass
    ...
    >>> is_abstract_factory(BaseClass)
    True
    >>> is_abstract_factory(int)
    False

    ```
    """
    return isinstance(cls, AbstractFactory)
