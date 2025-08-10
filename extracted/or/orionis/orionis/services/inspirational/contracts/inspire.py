from abc import ABC, abstractmethod

class IInspire(ABC):

    @abstractmethod
    def random(self) -> dict:
        """
        Generate and return a random inspirational item.

        Returns
        -------
        dict
            A dictionary containing the details of the randomly selected inspirational item.
        """
        pass  # This method must be implemented by subclasses