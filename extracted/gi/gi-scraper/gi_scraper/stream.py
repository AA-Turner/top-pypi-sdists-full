from .handler import Response, Lookup
from typing import Generator, Any
from .cache import Cache
from queue import Queue
import time


class QueueStream:
    """
    Represents a stream for processing items from a queue.

    Parameters:
    - queue (Queue): The queue to process items from.
    - cache (Cache): The cache instance to cache responses.
    - timeout (int): The timeout for waiting for items in the queue.
    - initial_timeout (int): The initial timeout for waiting for items in the queue.

    Attributes:
    - __queue (Queue): The queue to process items from.
    - __cache (Cache): The cache instance to cache responses.
    - __timeout (int): The timeout for waiting for items in the queue.
    - __initial_timeout (int): The initial timeout for waiting for items in the queue.

    Methods:
    - get(): Generator method for retrieving items from the queue as Response objects.

    Yields:
    - Response: An instance of the Response class.
    """

    def __init__(
        self, queue: Queue, cache: Cache, timeout: int = 10, initial_timeout: int = 30
    ) -> None:
        self.__queue = queue
        self.__cache = cache
        self.__timeout = timeout
        self.__initial_timeout = initial_timeout

    def get(self) -> Generator[Response, Any, None]:
        """
        Generator method for retrieving items from the queue as Response objects.

        Yields:
        - Response: An instance of the Response class.
        """

        self.__cache.erase_last_checked()

        last_fetch = time.time()
        wait_time = 0

        timeout = self.__initial_timeout

        while wait_time < timeout:
            if not self.__queue.empty():
                timeout = self.__timeout
                item = self.__queue.get()
                if item is None:
                    self.__cache.commit()
                    break
                yield item
                last_fetch = time.time()
                wait_time = 0
            else:
                wait_time = time.time() - last_fetch


class CacheStream:
    """
    Represents a stream for processing items from a cached list of responses.

    Parameters:
    - cache (Cache): The cache instance to cache responses.
    - lookup (Lookup): The lookup instance holding query details.

    Attributes:
    - __cache (Cache): The cache instance to cache responses.
    - __lookup (Lookup): The lookup instance holding query details.

    Methods:
    - get(): Generator method for retrieving items from the cached responses as Response objects.

    Yields:
    - Response: An instance of the Response class.
    """

    def __init__(self, cache: Cache, lookup: Lookup) -> None:
        self.__cache = cache
        self.__lookup = lookup

    def get(self) -> Generator[Response, Any, None]:
        """
        Generator method for retrieving items from the cached responses as Response objects.

        Yields:
        - Response: An instance of the Response class.
        """

        responses = self.__cache.fetch(self.__cache.get_last_checked())
        last_index = min(len(responses), self.__lookup.count)

        for item in responses[:last_index]:
            yield Response(**item)
