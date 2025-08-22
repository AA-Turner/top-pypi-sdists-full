from orionis.container.providers.service_provider import ServiceProvider
from orionis.failure.catch import Catch
from orionis.failure.contracts.catch import ICatch

class CathcProvider(ServiceProvider):
    """
    Provides and registers the Catch service within the application container.

    This service provider is responsible for binding the ICatch interface to its concrete
    implementation, Catch, as a singleton. By doing so, it ensures that a single shared
    instance of Catch is available for dependency injection throughout the application.

    Returns
    -------
    None
        This class does not return a value; it is used for service registration.
    """

    def register(self) -> None:
        """
        Register the Catch service as a singleton in the application container.

        This method binds the ICatch interface to the Catch implementation with an alias,
        ensuring that only one instance of Catch is created and shared.

        Returns
        -------
        None
            This method does not return any value.
        """

        # Bind ICatch to Catch as a singleton with a specific alias
        self.app.singleton(ICatch, Catch, alias="x-orionis.failure.catch")

    def boot(self) -> None:
        """
        Perform any actions required after all providers have been registered.

        This method is called after the register phase and can be used to perform
        additional initialization if needed.

        Returns
        -------
        None
            This method does not return any value.
        """

        # No additional boot logic required for this provider
        pass