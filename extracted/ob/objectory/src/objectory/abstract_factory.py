r"""Implement the ``AbstractFactory`` metaclass used to create abstract
factories."""

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
    full_object_name,
    import_object,
    instantiate_object,
    is_lambda_function,
    resolve_name,
)

if TYPE_CHECKING:
    from collections.abc import Callable

logger = logging.getLogger(__name__)


class AbstractFactory(ABCMeta):  # noqa: B024
    r"""Implement the abstract factory metaclass to create automatically
    factories.

    Please read the documentation about this abstract factory to
    learn how it works and how to use it.

    To avoid potential conflicts with the other classes, all the
    non-public attributes or functions starts with
    ``_abstractfactory_****`` where ``****`` is the name of the
    attribute or the function.

    Args:
        name: Specifies the class name. This becomes the
            ``__name__`` attribute of the class.
        bases: Specifies a tuple of the base classes from
            which the class inherits.
            This becomes the ``__bases__`` attribute of the class.
        dct: Specifies a namespace dictionary containing
            definitions for the class body.
            This becomes the ``__dict__`` attribute of the class.

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

    def __init__(cls, name: str, bases: tuple, dct: dict) -> None:
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

        Please read the documentation for more information.

        Args:
            _target_: Specifies the name of the object
                (class or function) to instantiate.
                It can be the class name or the full class name.
            *args: Variable length argument list.
            _init_: Specifies the function to use to create the object.
                If ``"__init__"``, the object is created by calling
                the constructor.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The instantiated object with the given parameters.

        Raises:
            AbstractClassAbstractFactoryError: if you try to
                instantiate an abstract class.
            UnregisteredClassAbstractFactoryError: if the target
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
        r"""Register a class or function to the factory. It is useful if
        you are using a 3rd party library.

        For example, you use a 3rd party library, and you cannot
        modify the classes to add ``AbstractFactory``. You can use
        this function to register some classes or functions of a
        3rd party library.

        Args:
            obj: Specifies the class or function to register to the
                factory.

        Raises:
            IncorrectObjectAbstractFactoryError: if the object
                is not a class.

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
        name = full_object_name(obj)
        if (
            cls._abstractfactory_is_name_registered(name)
            and cls._abstractfactory_inheritors[name] != obj
        ):
            logger.warning(f"The class {name} already exists. The new class replaces the old one")

        cls._abstractfactory_inheritors[name] = obj

    def unregister(cls, name: str) -> None:
        r"""Remove a registered object from the factory.

        This is an experimental function and may change in the future.

        Args:
            name: Specifies the name of the object to remove.
                This function uses the name resolution mechanism to
                find the full name if only the short name is given.

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
        """Get the class or function to used given its name.

        Args:
            name: Specifies the name of the class or function.

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
            name: Specifies the name of the class or function
                to resolve.

        Returns:
            It returns the name to use to get the object if the
                resolution was successful, otherwise ``None``.
        """
        return resolve_name(name, set(cls._abstractfactory_inheritors.keys()))

    def _abstractfactory_is_name_registered(cls, name: str) -> bool:
        r"""Indicate if the name exists or not in the factory .

        Args:
            name: Specifies the name to check.

        Returns:
            ``True`` if the name exists otherwise ``False``.
        """
        return name in cls._abstractfactory_inheritors

    def _abstractfactory_check_object(cls, obj: type) -> None:
        r"""Check if the object is valid for this factory before to
        register it.

        This function will raise an exception if the object is not
        valid.

        Args:
            obj: Specifies the object to check.

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

    This decorator is designed to register functions that returns
    an object of a class registered in the factory.

    Args:
        cls (objectory.AbstractFactory): Specifies the class where to
            register the function.

    Returns:
        collections.abc.Callable: The decorated function.

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
    r"""Register the given class and its child classes of a given class.

    This function registers all the child classes including the child
    classes of the child classes, etc.

    Args:
        factory_cls: Specifies the factory class. The child classes
            will be registered to this class.
        cls: Specifies the class to register its child classes.
        ignore_abstract_class: Indicate if the abstract class
            should be ignored or not. Be default, the abstract classes
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

    for class_to_register in [cls] + list(all_child_classes(cls)):
        if ignore_abstract_class and inspect.isabstract(class_to_register):
            continue
        factory_cls.register_object(class_to_register)


def is_abstract_factory(cls: Any) -> bool:
    r"""Indicate if a class implements the ``AbstractFactory`` metaclass.

    Args:
        cls: Specifies the class to check.

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
