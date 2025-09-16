from orionis.container.facades.facade import Facade

class Workers(Facade):

    @classmethod
    def getFacadeAccessor(cls):
        """
        Returns the binding key used to resolve the workers service implementation from the service container.

        This method specifies the unique identifier (binding key) that the service container uses to locate
        and provide the appropriate implementation of the workers service. It acts as the connection point
        between the facade and the underlying service registration in the container.

        Returns
        -------
        str
            The string 'x-orionis.services.system.contracts.workers.IWorkers', which is the binding key
            identifying the workers service implementation in the service container.
        """

        # Return the binding key for the workers service in the service container
        return "x-orionis.services.system.contracts.workers.IWorkers"
