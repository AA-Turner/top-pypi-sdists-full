from abc import ABC, abstractmethod
from orionis.services.introspection.dependencies.entities.class_dependencies import ClassDependency
from orionis.services.introspection.dependencies.entities.method_dependencies import MethodDependency

class IReflectDependencies(ABC):
    """
    Abstract interface for reflecting on class and method dependencies.

    This interface defines methods for retrieving dependency information from
    the constructor and methods of a class, distinguishing between resolved and
    unresolved dependencies.
    """

    @abstractmethod
    def getConstructorDependencies(self) -> ClassDependency:
        """
        Retrieve dependency information from the class constructor.

        Returns
        -------
        ClassDependency
            An object containing details about the constructor's dependencies.
            The object includes:
                - resolved : dict
                    Mapping of dependency names to their resolved values.
                - unresolved : list
                    List of dependency names that are unresolved (i.e., lacking
                    default values or type annotations).
        """
        pass

    def getMethodDependencies(self, method_name: str) -> MethodDependency:
        """
        Retrieve dependency information from a specified method.

        Parameters
        ----------
        method_name : str
            The name of the method whose dependencies are to be inspected.

        Returns
        -------
        MethodDependency
            An object containing details about the method's dependencies.
            The object includes:
                - resolved : dict
                    Mapping of dependency names to their resolved values.
                - unresolved : list
                    List of dependency names that are unresolved (i.e., lacking
                    default values or type annotations).
        """
        pass