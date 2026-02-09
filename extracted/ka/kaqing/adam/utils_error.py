from abc import abstractmethod

class ErrorAware:
    @abstractmethod
    def has_error() -> bool:
        pass