from abc import ABC, abstractmethod
import asyncio
import time

class IPerformanceService(ABC):
    """
    Interface for a performance service that provides both synchronous and asynchronous operations.

    Methods
    -------
    sync_operation() -> str
        Performs a synchronous operation and returns the result as a string.
    async async_operation() -> str
        Performs an asynchronous operation and returns the result as a string.
    """

    @abstractmethod
    def sync_operation(self) -> str:
        """
        Performs a synchronous operation.

        Returns
        -------
        str
            A string representing the result of the synchronous operation.
        """
        pass  # To be implemented by subclasses

    @abstractmethod
    async def async_operation(self) -> str:
        """
        Performs an asynchronous operation.

        Returns
        -------
        str
            A string representing the result of the asynchronous operation.
        """
        pass  # To be implemented by subclasses

class PerformanceService(IPerformanceService):
    """
    Mock implementation of the IPerformanceService interface for testing performance-related tasks.

    This class provides both synchronous and asynchronous operations to simulate performance scenarios.
    It is intended for use in test environments where simulating delays and asynchronous behavior is required.

    Methods
    -------
    sync_operation() -> str
        Simulates a synchronous operation with a delay and returns a completion message.
    async async_operation() -> str
        Simulates an asynchronous operation with a delay and returns a completion message.
    """

    def sync_operation(self) -> str:
        """
        Simulates a synchronous operation by introducing a short blocking delay.

        The method blocks the current thread for a brief period to mimic a time-consuming synchronous task.

        Returns
        -------
        str
            A message indicating that the synchronous operation has completed.
        """
        time.sleep(0.1)  # Simulate a blocking delay
        return "Sync operation completed"

    async def async_operation(self) -> str:
        """
        Simulates an asynchronous operation by introducing a short non-blocking delay.

        The method asynchronously waits for a brief period to mimic a time-consuming asynchronous task.

        Returns
        -------
        str
            A message indicating that the asynchronous operation has completed.
        """
        await asyncio.sleep(0.1)  # Simulate a non-blocking delay
        return "Async operation completed"

class ErrorService:
    """
    Service for simulating error scenarios in both synchronous and asynchronous contexts.

    This class provides methods that intentionally raise exceptions, useful for testing error handling
    in synchronous and asynchronous code paths.

    Methods
    -------
    sync_error_method()
        Synchronously raises a ValueError to simulate an error in synchronous code.
    async async_error_method()
        Asynchronously raises a ValueError after a short delay to simulate an error in asynchronous code.
    """

    def sync_error_method(self):
        """
        Synchronously raises a ValueError to simulate an error in synchronous code.

        Raises
        ------
        ValueError
            Always raised with the message "Sync error occurred".

        Returns
        -------
        None
            This method does not return; it always raises an exception.
        """
        # Raise a synchronous error for testing purposes
        raise ValueError("Sync error occurred")

    async def async_error_method(self):
        """
        Asynchronously raises a ValueError after a short delay to simulate an error in asynchronous code.

        The method awaits for 0.1 seconds before raising the exception, mimicking asynchronous error scenarios.

        Raises
        ------
        ValueError
            Always raised with the message "Async error occurred" after a 0.1 second delay.

        Returns
        -------
        None
            This method does not return; it always raises an exception.
        """
        # Simulate asynchronous delay before raising the error
        await asyncio.sleep(0.1)
        raise ValueError("Async error occurred")

class SyncDependency:
    """
    Mock synchronous dependency for testing synchronous code paths.

    This class simulates a simple synchronous dependency that returns a fixed string value.
    It is intended for use in test scenarios where a synchronous service or resource is required.

    Methods
    -------
    get_data() -> str
        Returns a fixed string representing synchronous data.
    """

    def get_data(self) -> str:
        """
        Retrieve a fixed string representing synchronous data.

        This method simulates fetching data from a synchronous resource or service.
        It always returns the same string value for testing purposes.

        Returns
        -------
        str
            The string "sync data", representing the synchronous data provided by this dependency.
        """

        # Return a fixed string to simulate synchronous data retrieval
        return "sync data"

class AsyncDependency:
    """
    An asynchronous dependency class that provides async data.

    Methods
    -------
    get_async_data() -> str
        Asynchronously retrieves a string representing data after a short delay.
    """

    async def get_async_data(self) -> str:
        """
        Asynchronously retrieves data after a short delay.

        This method simulates an asynchronous operation by waiting for a brief period
        before returning a fixed string value. It is useful for testing asynchronous
        code paths where a non-blocking dependency is required.

        Returns
        -------
        str
            The string "async data", representing the asynchronously retrieved data.
        """

        # Simulate a short asynchronous delay
        await asyncio.sleep(0.05)

        # Return a fixed string to represent async data retrieval
        return "async data"

class MixedConsumer:
    """
    A consumer class that demonstrates usage of both synchronous and asynchronous dependencies.

    Parameters
    ----------
    sync_dep : SyncDependency
        A synchronous dependency providing data via `get_data()`.
    async_dep : AsyncDependency
        An asynchronous dependency providing data via `get_async_data()`.

    Methods
    -------
    sync_method() -> str
        Returns a string containing data from the synchronous dependency.
    async async_method() -> str
        Asynchronously retrieves data from the async dependency and combines it with data from the sync dependency.
    async complex_method(multiplier: int = 2) -> str
        Asynchronously retrieves data from the async dependency and returns a string with the data multiplied by the given multiplier.
    """

    def __init__(self, sync_dep: SyncDependency, async_dep: AsyncDependency):
        """
        Initialize MixedConsumer with synchronous and asynchronous dependencies.

        Parameters
        ----------
        sync_dep : SyncDependency
            The synchronous dependency to be injected.
        async_dep : AsyncDependency
            The asynchronous dependency to be injected.
        """
        self.sync_dep = sync_dep
        self.async_dep = async_dep

    def sync_method(self) -> str:
        """
        Retrieve data synchronously from the synchronous dependency and return it as a formatted string.

        Returns
        -------
        str
            A formatted string containing data from the synchronous dependency in the format 'Sync: <sync_data>'.
        """

        # Get data from the synchronous dependency and format it
        return f"Sync: {self.sync_dep.get_data()}"

    async def async_method(self) -> str:
        """
        Asynchronously retrieve data from both asynchronous and synchronous dependencies,
        and return a formatted string containing both results.

        Returns
        -------
        str
            A string containing both synchronous and asynchronous data in the format
            'Mixed: sync=<sync_data>, async=<async_data>'.
        """

        # Await data from the asynchronous dependency
        async_data = await self.async_dep.get_async_data()

        # Get data from the synchronous dependency
        sync_data = self.sync_dep.get_data()

        # Combine both pieces of data into a formatted string
        return f"Mixed: sync={sync_data}, async={async_data}"

    async def complex_method(self, multiplier: int = 2) -> str:
        """
        Asynchronously retrieve data from the asynchronous dependency and return a formatted string
        that includes the data and the multiplier value.

        Parameters
        ----------
        multiplier : int, optional
            The value to multiply the async data by. Defaults to 2.

        Returns
        -------
        str
            A formatted string containing the async data and the multiplier in the format
            'Complex: <async_data> * <multiplier>'.
        """

        # Await data from the asynchronous dependency
        async_data = await self.async_dep.get_async_data()

        # Return the formatted string with the async data and multiplier
        return f"Complex: {async_data} * {multiplier}"

def sync_returns_coroutine():
    """
    Returns a coroutine object that performs an asynchronous sleep and yields a string result.

    This function is a synchronous callable that, when invoked, returns a coroutine object.
    The returned coroutine, when awaited, will asynchronously sleep for 0.05 seconds before
    returning a specific string. This pattern is useful for testing scenarios where a
    synchronous function is expected to return an awaitable.

    Returns
    -------
    coroutine
        A coroutine object that, when awaited, sleeps asynchronously for 0.05 seconds and
        returns the string "Sync function returning coroutine".
    """

    # Define an inner asynchronous function to perform the async operation
    async def inner():

        # Asynchronously sleep for 0.05 seconds
        await asyncio.sleep(0.05)

        # Return a fixed string after the delay
        return "Sync function returning coroutine"

    # Return the coroutine object (not awaited here)
    return inner()

async def simple_async():
    """
    Asynchronously sleeps for a short duration and returns a fixed string message.

    This asynchronous function demonstrates a simple async operation by awaiting a short
    delay before returning a message indicating successful execution.

    Returns
    -------
    str
        The string "Simple async callable" after a 0.05 second asynchronous delay.
    """

    # Asynchronously sleep for 0.05 seconds
    await asyncio.sleep(0.05)

    # Return a fixed string after the delay
    return "Simple async callable"