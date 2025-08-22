from abc import ABC, abstractmethod
from datetime import datetime
from orionis.console.contracts.schedule import ISchedule

class IBaseScheduler(ABC):

    # Pause Global Scheduler at a specific time
    PAUSE_AT: datetime = None

    # Resume Global Scheduler at a specific time
    RESUME_AT: datetime = None

    # Finalize Global Scheduler at a specific time
    FINALIZE_AT: datetime = None

    @abstractmethod
    def tasks(self, schedule: ISchedule):
        """
        Defines and registers scheduled tasks for the application.

        Parameters
        ----------
        schedule : ISchedule
            The schedule object used to define and register scheduled commands.

        Returns
        -------
        None
            This method does not return any value. It is intended to be overridden
            by subclasses to specify scheduled tasks.

        Notes
        -----
        This method should be implemented in subclasses to add specific tasks
        to the scheduler using the provided `schedule` object.
        """
        # This method should be overridden in subclasses to define scheduled tasks.
        pass