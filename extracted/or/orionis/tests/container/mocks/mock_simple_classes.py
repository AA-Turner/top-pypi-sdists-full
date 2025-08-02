from abc import ABC, abstractmethod

class ICar(ABC):
    """
    ICar is an interface that defines the structure for car objects.
    It includes methods for starting and stopping the car.
    """

    @abstractmethod
    def start(self) -> str:
        """
        Starts the car and returns a message indicating the car has started.
        """
        pass

    @abstractmethod
    def stop(self) -> str:
        """
        Stops the car and returns a message indicating the car has stopped.
        """
        pass

class Car(ICar):
    def __init__(self, brand: str = 'a', model: str = 'b'):
        self.brand = brand
        self.model = model

    def start(self):
        return f"{self.brand} {self.model} is starting."

    def stop(self):
        return f"{self.brand} {self.model} is stopping."