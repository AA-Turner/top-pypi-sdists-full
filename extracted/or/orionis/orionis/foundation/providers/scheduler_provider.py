from orionis.console.contracts.schedule import ISchedule
from orionis.console.tasks.schedule import Schedule
from orionis.container.providers.service_provider import ServiceProvider

class ScheduleProvider(ServiceProvider):

    def register(self) -> None:
        """
        Registers the Scheduler as a singleton service in the application container.

        This method binds the `ISchedule` interface to the `Schedule` implementation,
        ensuring that a single instance of the scheduler is used throughout the application's
        lifecycle. Additionally, it provides an alias
        ("x-orionis.console.contracts.schedule.ISchedule") for convenient access to the
        scheduler service.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It performs the registration as a side effect.
        """

        # Bind the Schedule implementation as a singleton to the ISchedule interface
        # and provide an alias for easier access within the application container.
        self.app.singleton(ISchedule, Schedule, alias="x-orionis.console.contracts.schedule.ISchedule")