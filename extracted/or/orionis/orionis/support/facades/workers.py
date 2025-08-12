from orionis.container.facades.facade import Facade

class Workers(Facade):

    @classmethod
    def getFacadeAccessor(cls):
        """
        Get the registered name of the component in the service container.

        This method provides the binding key that the service container uses to 
        resolve the workers service implementation. It serves as the bridge between 
        the facade and the underlying service registration.

        Returns
        -------
        str
            The service container binding key 'x-orionis.services.system.workers' 
            that identifies the workers service implementation.
        """

        return "x-orionis.services.system.workers"
