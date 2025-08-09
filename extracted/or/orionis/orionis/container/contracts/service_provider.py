from abc import ABC, abstractmethod

class IServiceProvider(ABC):

    @abstractmethod
    async def register(self) -> None:
        """
        Register services into the application container.

        Notes
        -----
        This asynchronous method must be implemented by subclasses.
        It is responsible for binding services, configurations, or other
        components to the application container.

        Raises
        ------
        NotImplementedError
            If the method is not implemented by a subclass.
        """
        pass

    @abstractmethod
    async def boot(self) -> None:
        """
        Perform post-registration bootstrapping or initialization.

        Notes
        -----
        This asynchronous method is called after all services have been registered.
        Subclasses should override this method to initialize services, set up
        event listeners, or perform other operations required at boot time.
        """
        pass