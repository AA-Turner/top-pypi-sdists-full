from orionis.container.providers.service_provider import ServiceProvider
from orionis.failure.catch import Catch
from orionis.failure.contracts.catch import ICatch

class CathcProvider(ServiceProvider):

    def register(self) -> None:
        """
        Registers the Catch service as a singleton in the application container.

        This method binds the `ICatch` interface to the `Catch` implementation as a singleton,
        using a specific alias. This ensures that only one instance of `Catch` is created and
        shared throughout the application's lifecycle. The binding allows the application to
        resolve dependencies on `ICatch` with the registered `Catch` instance.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It performs the registration as a side effect.
        """

        # Register the Catch implementation as a singleton for the ICatch interface
        # The alias allows for explicit resolution by name if needed
        self.app.singleton(ICatch, Catch, alias="x-orionis.failure.contracts.catch.ICatch")