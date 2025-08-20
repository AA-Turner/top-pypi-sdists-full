from orionis.console.contracts.schedule import ISchedule
from orionis.console.tasks.schedule import Scheduler
from orionis.container.providers.service_provider import ServiceProvider

class ScheduleProvider(ServiceProvider):
    """
    Service provider responsible for registering and bootstrapping the application's scheduling system.

    The ScheduleProvider binds the ISchedule interface to the Scheduler implementation as a singleton
    within the application's service container. It also provides an alias for convenient access.
    Override the `boot` method to configure and register scheduled tasks or jobs required by the application.

    Methods
    -------
    register() :
        Registers the Scheduler as a singleton service and binds it to the ISchedule interface.
    boot() :
        Initializes and configures scheduled tasks; intended to be overridden for custom jobs.
    """

    def register(self) -> None:
        """
        Register the Scheduler as a singleton service in the application container.

        This method binds the ISchedule interface to the Scheduler implementation,
        making it available as a singleton throughout the application's lifecycle.
        An alias "x-orionis.console.contracts.schedule" is also provided for
        convenient access.

        Returns
        -------
        None
            This method does not return any value.
        """
        # Bind Scheduler as a singleton to the ISchedule interface with an alias
        self.app.singleton(ISchedule, Scheduler, alias="x-orionis.console.contracts.schedule")

    def boot(self) -> None:
        """
        Initialize and configure any scheduled tasks or jobs required by the application.

        This method is called automatically during the application's bootstrapping process.
        Override this method to register custom scheduled tasks.

        Returns
        -------
        None
            This method does not return any value.
        """
        # No scheduled tasks are registered by default; override to add custom jobs
        pass
