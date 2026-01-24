from abc import ABC, abstractmethod
from requests import Session


class HttpClientProvider(ABC):
    """Defines a contract for providing HTTP client configuration.

    Classes implementing this interface are expected to supply a configured
    HTTP session and timeout value that will be used by the SDK's internal
    HTTP layer when making network requests.

    This allows developers to inject their own custom HTTP clients while
    maintaining compatibility with the SDK's request/response handling.
    """

    @property
    @abstractmethod
    def timeout(self) -> float:
        """The default request timeout in seconds.

        Returns:
            float: The timeout duration to apply to all outgoing HTTP requests.
        """

    @property
    @abstractmethod
    def session(self) -> Session:
        """The underlying HTTP session instance.

        Returns:
            Session: A configured ``requests.Session`` object used to perform
                network operations such as GET, POST, and PUT calls.
        """
