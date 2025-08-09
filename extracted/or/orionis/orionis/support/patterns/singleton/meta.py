import threading
import asyncio
from typing import Dict, Type, Any, TypeVar

T = TypeVar('T')

class Singleton(type):
    """
    Metaclass for implementing thread-safe and async-safe singleton pattern.

    This metaclass ensures that only one instance of a class exists, regardless of
    whether the code is running in a synchronous or asynchronous context. It provides
    both synchronous and asynchronous mechanisms for instance creation, using appropriate
    locking to prevent race conditions in multi-threaded or async environments.

    Attributes
    ----------
    _instances : Dict[Type[T], T]
        Dictionary storing singleton instances for each class using this metaclass.
    _lock : threading.Lock
        Thread lock for synchronizing instance creation in synchronous contexts.
    _async_lock : asyncio.Lock
        Async lock for synchronizing instance creation in asynchronous contexts.
    """

    _instances: Dict[Type[T], T] = {}
    _lock = threading.Lock()
    _async_lock = asyncio.Lock()

    def __call__(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        """
        Synchronously create or retrieve the singleton instance.

        Ensures that only one instance of the class is created in a thread-safe manner.
        If the instance does not exist, acquires a thread lock to prevent race conditions,
        creates the instance, and stores it in the class-level `_instances` dictionary.
        If the instance already exists, returns the existing instance.

        Parameters
        ----------
        *args : Any
            Positional arguments to pass to the class constructor.
        **kwargs : Any
            Keyword arguments to pass to the class constructor.

        Returns
        -------
        T
            The singleton instance of the class.
        """

        # Check if the instance already exists
        if cls not in cls._instances:

            # Acquire the thread lock to ensure thread safety
            with cls._lock:

                # Double-check if the instance was created while waiting for the lock
                if cls not in cls._instances:

                    # Create and store the singleton instance
                    cls._instances[cls] = super().__call__(*args, **kwargs)

        # Return the singleton instance
        return cls._instances[cls]

    async def __acall__(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        """
        Asynchronously create or retrieve the singleton instance.

        Ensures that only one instance of the class is created in an async-safe manner.
        If the instance does not exist, acquires an asynchronous lock to prevent race
        conditions, creates the instance, and stores it in the class-level `_instances`
        dictionary. If the instance already exists, returns the existing instance.

        Parameters
        ----------
        *args : Any
            Positional arguments to pass to the class constructor.
        **kwargs : Any
            Keyword arguments to pass to the class constructor.

        Returns
        -------
        T
            The singleton instance of the class.
        """

        # Check if the instance already exists
        if cls not in cls._instances:

            # Acquire the asynchronous lock to ensure async safety
            async with cls._async_lock:

                # Double-check if the instance was created while waiting for the lock
                if cls not in cls._instances:

                    # Create and store the singleton instance
                    cls._instances[cls] = super().__call__(*args, **kwargs)

        # Return the singleton instance
        return cls._instances[cls]
