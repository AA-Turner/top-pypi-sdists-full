r"""Implement the registry class."""

from __future__ import annotations

__all__ = ["Registry"]

import inspect
import logging
from typing import Any, Callable, TypeVar

from objectory.errors import (
    IncorrectObjectFactoryError,
    InvalidAttributeRegistryError,
    InvalidNameFactoryError,
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

logger = logging.getLogger(__name__)

T = TypeVar("T")


class Registry:
    r"""Implement the registry class.

    This class can be used to register some objects and instantiate an
    object from its configuration.

    Example usage:

    ```pycon
    >>> from objectory import Registry
    >>> from collections import Counter
    >>> registry = Registry()
    >>> registry.register_object(Counter)
    >>> registry.factory("collections.Counter")
    Counter()

    ```
    """

    _CLASS_FILTER = "class_filter"

    def __init__(self) -> None:
        self._state = {}
        self._filters = {}

    def __getattr__(self, key: str) -> Registry | type:
        r"""Get the registry associated to a key.

        Args:
            key: Specifies the key.

        Returns:
            The registry associated to the key.

        Raises:
            InvalidAttributeRegistryError: if the associated attribute
                is not a registry.

        Example usage:

        ```pycon
        >>> from collections import Counter
        >>> registry = Registry()
        >>> registry.other.register_object(Counter)

        ```
        """
        if key not in self._state:
            self._state[key] = Registry()
        if self._is_registry(key):
            return self._state[key]
        msg = (
            f"The attribute `{key}` is not a registry. You can use this function only to access "
            "a Registry object."
        )
        raise InvalidAttributeRegistryError(msg)

    def __len__(self) -> int:
        r"""Return the number of registered objects.

        Returns:
            The number of registered objects.

        Example usage:

        ```pycon
        >>> from objectory import Registry
        >>> from collections import Counter
        >>> registry = Registry()
        >>> registry.register_object(Counter)
        >>> len(registry)
        1

        ```
        """
        return len(self._state)

    def clear(self, nested: bool = False) -> None:
        r"""Clear the registry.

        This functions removes all the registered objects in the
        registry.

        Args:
            nested: Indicates if the sub-registries should be
                cleared or not.

        Example usage:

        ```pycon
        >>> from objectory import Registry
        >>> registry = Registry()
        >>> # Clear the main registry.
        >>> registry.clear()
        >>> # Clear only the sub-registry other.
        >>> registry.other.clear()
        >>> # Clear the main registry and its sub-registries.
        >>> registry.clear(nested=True)

        ```
        """
        if nested:  # If True, clear all the sub-registries.
            for value in self._state.values():
                if isinstance(value, Registry):
                    value.clear(nested)
        self._state.clear()

    def clear_filters(self, nested: bool = False) -> None:
        r"""Clear all the filters of the registry.

        Args:
            nested: Indicates if the filters of all the sub-registries
                should be cleared or not.

        Example usage:

        ```pycon
        >>> from objectory import Registry
        >>> registry = Registry()
        >>> # Clear the filters of the main registry.
        >>> registry.clear_filters()
        >>> # Clear the filters of the sub-registry other.
        >>> registry.other.clear_filters()
        >>> # Clear the filters of the main registry and all its sub-registries.
        >>> registry.clear_filters(nested=True)

        ```
        """
        if nested:  # If True, clear all the sub-registries.
            for value in self._state.values():
                if isinstance(value, Registry):
                    value.clear_filters(nested)
        self._filters.clear()

    def factory(self, _target_: str, *args: Any, _init_: str = "__init__", **kwargs: Any) -> Any:
        r"""Instantiate dynamically an object given its configuration.

        Please read the documentation for more information.

        Args:
            _target_ : Specifies the name of the object
                (class or function) to instantiate.
                It can be the class name or the full class name.
            *args: Variable length argument list.
            _init_: Specifies the function to use to
                create the object. If ``"__init__"``, the object is
                created by calling the constructor.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The instantiated object with the given parameters.

        Raises:
            AbstractClassAbstractFactoryError: if you try to
                instantiate an abstract class.
            UnregisteredClassAbstractFactoryError: if the target
                name is not found.

        Example usage:

        ```pycon
        >>> from objectory import Registry
        >>> registry = Registry()
        >>> @registry.register()
        ... class MyClass:
        ...     pass
        ...
        >>> registry.factory("MyClass")
        <....MyClass object at 0x...>

        ```
        """
        return instantiate_object(
            self._get_target_from_name(_target_), *args, _init_=_init_, **kwargs
        )

    def register(self, name: str | None = None) -> Callable:
        r"""Define a decorator to add a class or a function to the
        registry.

        Args:
            name: Specifies the name to use to register the object.
                If ``None``, the full name of the object is used as
                name.

        Returns:
            The decorated object.

        Example usage:

        ```pycon
        >>> from objectory import Registry
        >>> registry = Registry()
        >>> @registry.register()
        ... class ClassToRegister:
        ...     pass
        ...
        >>> registry.registered_names()
        {'....ClassToRegister'}
        >>> @registry.register()
        ... def function_to_register(*args, **kwargs):
        ...     pass
        ...
        >>> registry.registered_names()
        {...}

        ```
        """

        def function_wrapper(obj: T) -> T:
            self.register_object(obj=obj, name=name)
            return obj

        return function_wrapper

    def register_child_classes(self, cls: type, ignore_abstract_class: bool = True) -> None:
        r"""Register a given class and its child classes of a given
        class.

        This function registers all the child classes including the
        child classes of the child classes, etc. If you use this
        function, you cannot choose the names used to register the
        objects. It will use the full name of each object.

        Args:
            cls: Specifies the class to register its child classes.
            ignore_abstract_class: Indicate if the abstract
                class should be ignored or not. Be default, the
                abstract classes are not registered because they
                cannot be instantiated.

        Example usage:

        ```pycon
        >>> from objectory import Registry
        >>> registry = Registry()
        >>> registry.register_child_classes(dict)
        >>> registry.registered_names()
        {...}

        ```
        """
        for class_to_register in [cls] + list(all_child_classes(cls)):
            if ignore_abstract_class and inspect.isabstract(class_to_register):
                continue
            self.register_object(class_to_register)

    def register_object(self, obj: type | Callable, name: str | None = None) -> None:
        r"""Register an object.

        Please read the documentation for more information.

        Args:
            obj: Specifies the object to register. The object is
                expected to be a class or a function.
            name: Specifies the name to use to register the object.
                If ``None``, the full name of the object is used as
                name.

        Example usage:

        ```pycon
        >>> from objectory import Registry
        >>> registry = Registry()
        >>> class ClassToRegister:
        ...     pass
        ...
        >>> registry.register_object(ClassToRegister)
        >>> registry.registered_names()
        {'....ClassToRegister'}
        >>> def function_to_register(*args, **kwargs):
        ...     pass
        ...
        >>> registry.register_object(function_to_register)
        >>> registry.registered_names()
        {...}

        ```
        """
        self._check_object(obj)
        if name is None:
            name = full_object_name(obj)
        elif not isinstance(name, str):
            msg = f"The name has to be a string (received: {name})"
            raise TypeError(msg)

        if name in self._state:
            if self._is_registry(name):
                msg = f"The name `{name}` is already used by a sub-registry"
                raise InvalidNameFactoryError(msg)
            if self._state[name] != obj:
                logger.warning(
                    f"The name `{name}` already exists and its value will be replaced by {obj}"
                )

        self._state[name] = obj

    def registered_names(self, include_registry: bool = True) -> set[str]:
        r"""Get the names of all the registered objects.

        Args:
            include_registry: Specifies if the other (sub-)registries
                should be included in the set. By default, the other
                (sub-)registries are included.

        Returns:
            set: The names of the registered objects.

        Example usage:

        ```pycon
        >>> from objectory import Registry
        >>> registry = Registry()
        >>> registry.registered_names()
        >>> # Show name of all the registered objects except the sub-registries.
        >>> registry.registered_names(include_registry=False)

        ```
        """
        if include_registry:
            return set(self._state.keys())

        names = set()
        for key, value in self._state.items():
            if not isinstance(value, Registry):
                names.add(key)
        return names

    def unregister(self, name: str) -> None:
        r"""Remove a registered object.

        Args:
            name: Specifies the name of the object to remove.
                This function uses the name resolution mechanism to
                find the full name if only the short name is given.

        Raises:
            UnregisteredObjectFactoryError: if the name does not
                exist in the registry.

        Example usage:

        ```pycon
        >>> from objectory import Registry
        >>> from collections import Counter
        >>> registry = Registry()
        >>> registry.register_object(Counter)
        >>> registry.unregister("collections.Counter")

        ```
        """
        resolved_name = self._resolve_name(name)
        if resolved_name is None or not self._is_name_registered(resolved_name):
            msg = (
                f"It is not possible to remove an object which is not registered (received: {name})"
            )
            raise UnregisteredObjectFactoryError(msg)
        self._state.pop(resolved_name)

    def set_class_filter(self, cls: type | None) -> None:
        r"""Set the class filter so only the child classes of this class
        can be registered.

        If you set this filter, you cannot register functions.
        To unset this filter, you can use ``set_class_filter(None)``.

        Args:
            cls: Specifies the class to use as filter. Only the child
                classes of this class can be registered.

        Raises:
            TypeError: if the input is not a class or ``None``.

        Example usage:

        ```pycon
        >>> from collections import Counter, OrderedDict
        >>> from objectory import Registry
        >>> registry = Registry()
        >>> registry.mapping.set_class_filter(dict)
        >>> registry.mapping.register_object(OrderedDict)
        >>> registry.mapping.registered_names()
        {'collections.OrderedDict'}

        ```
        """
        if cls is None:
            self._filters.pop(self._CLASS_FILTER, None)
            return

        if not inspect.isclass(cls):
            msg = f"The class filter has to be a class (received: {cls})"
            raise TypeError(msg)
        self._filters[self._CLASS_FILTER] = cls

    def _check_object(self, obj: type | Callable) -> None:
        r"""Check if the object is valid for this registry before to
        register it.

        This function will raise an exception if the object is not
        valid.

        Args:
            obj: Specifies the object to check.

        Raises:
            IncorrectObjectFactoryError: if it is an invalid
                object for this factory.
        """
        if is_lambda_function(obj):
            msg = (
                "It is not possible to register a lambda function. "
                "Please use a regular function instead"
            )
            raise IncorrectObjectFactoryError(msg)

        filter_class = self._filters.get(self._CLASS_FILTER, None)
        if filter_class is not None and not issubclass(obj, filter_class):
            class_name = full_object_name(filter_class)
            msg = f"All the registered objects should inherit {class_name} class (received {obj})"
            raise IncorrectObjectFactoryError(msg)

    def _get_target_from_name(self, name: str) -> Any:
        r"""Get the class or function to used given its name.

        Args:
            name: Specifies the name of the class or function.

        Returns:
            The class or function.

        Raises:
            UnregisteredObjectFactoryError: if it is not possible
                to find the target.
        """
        resolved_name = self._resolve_name(name)
        if resolved_name is None:
            msg = (
                f"Unable to create the object `{name}` because it is not registered. "
                f"Registered objects of {self.__name__} are "
                f"{self.registered_names(include_registry=False)}."
            )
            raise UnregisteredObjectFactoryError(msg)
        if not self._is_name_registered(resolved_name):
            self.register_object(import_object(resolved_name))
        return self._state[resolved_name]

    def _is_name_registered(self, name: str) -> bool:
        r"""Indicate if the name exists or not in the registry .

        Args:
            name: Specifies the name to check.

        Returns:
            ``True`` if the name exists, otherwise ``False``.
        """
        return name in self._state

    def _is_registry(self, name: str) -> bool:
        r"""Indicate if the given is used as sub-registry.

        Args:
            name: Specifies the name to check.

        Returns:
            ``True`` if the name is used as sub-registry,
                otherwise ``False``.
        """
        return isinstance(self._state[name], Registry)

    def _resolve_name(self, name: str) -> str | None:
        r"""Try to resolve the name.

        This function will look at if it can find an object which
        match with the given name. It is quite useful because there
        are several ways to load an object but only one can be
        registered. If you specify a full name (module path +
        class/function name), it will try to import the module
        and registered it if it is not registered yet.

        Args:
            name: Specifies the name to resolve.

        Returns:
            It returns the name to use to get the
                object if the resolution was successful,
                otherwise ``None``.
        """
        return resolve_name(name, self.registered_names(include_registry=False))
