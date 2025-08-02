from abc import ABC, abstractmethod

class IServiceProvider(ABC):

    @abstractmethod
    async def register(self) -> None:
        """
        Register services into the application container.

        This method must be implemented by all concrete service providers.
        It should bind services, configurations, or other components
        to the application container.

        Raises
        ------
        NotImplementedError
            If the method is not overridden in a subclass.
        """
        pass

    @abstractmethod
    async def boot(self) -> None:
        """
        Perform any post-registration bootstrapping or initialization.

        This method is called after all services have been registered.
        Override this method to initialize services, set up event listeners,
        or perform other boot-time operations.
        """
        pass