from abc import ABC, abstractmethod

class IEventListener(ABC):
    """
    Interface for event listeners that handle various stages of event processing.
    """

    @abstractmethod
    def before(self, event):
        """
        Hook method called before the main event handling logic.

        Parameters
        ----------
        event : object
            The event object that is about to be processed.

        Returns
        -------
        None
            This method does not return anything.

        Notes
        -----
        Override this method to implement logic that should run before the event is handled.
        """
        pass

    @abstractmethod
    def after(self, event):
        """
        Hook method called after an event is processed.

        Parameters
        ----------
        event : object
            The event object that was processed.

        Returns
        -------
        None
            This method does not return anything.

        Notes
        -----
        Override this method to implement logic that should run after the event is handled.
        """
        pass

    @abstractmethod
    def onSuccess(self, event):
        """
        Handle actions to be performed when an event is successfully processed.

        Parameters
        ----------
        event : object
            The event object that triggered the success callback.

        Returns
        -------
        None
            This method does not return anything.

        Notes
        -----
        Override this method to define actions on successful event processing.
        """
        pass

    @abstractmethod
    def onFailure(self, event):
        """
        Handle the event when a failure occurs during event processing.

        Parameters
        ----------
        event : object
            The event object containing information about the failure.

        Returns
        -------
        None
            This method does not return anything.

        Notes
        -----
        Override this method to define actions when event processing fails.
        """
        pass

    @abstractmethod
    def onMissed(self, event):
        """
        Handle the event when an expected event is missed.

        Parameters
        ----------
        event : object
            The event object that was missed.

        Returns
        -------
        None
            This method does not return anything.

        Notes
        -----
        Override this method to define actions when an event is missed.
        """
        pass

    @abstractmethod
    def onMaxInstances(self, event):
        """
        Handles the event triggered when the maximum number of instances is reached.

        Parameters
        ----------
        event : object
            The event object containing information about the max instances event.

        Returns
        -------
        None
            This method does not return anything.

        Notes
        -----
        Override this method to define actions when the maximum number of instances is reached.
        """
        pass