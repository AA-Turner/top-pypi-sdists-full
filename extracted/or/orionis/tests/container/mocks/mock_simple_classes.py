from abc import ABC, abstractmethod

class ICar(ABC):
    """
    Interface for car objects.

    Defines the required methods for car objects, including starting and stopping the car.

    Methods
    -------
    start() -> str
        Start the car and return a message indicating the car has started.
    stop() -> str
        Stop the car and return a message indicating the car has stopped.
    """

    @abstractmethod
    def start(self) -> str:
        """
        Start the car.

        Returns
        -------
        str
            Message indicating the car has started.
        """
        pass

    @abstractmethod
    def stop(self) -> str:
        """
        Stop the car.

        Returns
        -------
        str
            Message indicating the car has stopped.
        """
        pass

class Car(ICar):
    """
    Concrete implementation of the ICar interface.

    Parameters
    ----------
    brand : str, optional
        The brand of the car (default is 'a').
    model : str, optional
        The model of the car (default is 'b').

    Attributes
    ----------
    brand : str
        The brand of the car.
    model : str
        The model of the car.
    """

    def __init__(self, brand: str = 'a', model: str = 'b'):
        """
        Initialize a new Car instance with the specified brand and model.

        Parameters
        ----------
        brand : str, optional
            The brand of the car. Default is 'a'.
        model : str, optional
            The model of the car. Default is 'b'.

        Notes
        -----
        This constructor sets the brand and model attributes for the Car object.
        """
        self.brand = brand  # Set the brand of the car
        self.model = model  # Set the model of the car

    def start(self):
        """
        Start the car.

        Returns
        -------
        str
            Message indicating the car is starting.
        """
        return f"{self.brand} {self.model} is starting."

    def stop(self):
        """
        Stop the car.

        Returns
        -------
        str
            Message indicating the car is stopping.
        """
        return f"{self.brand} {self.model} is stopping."