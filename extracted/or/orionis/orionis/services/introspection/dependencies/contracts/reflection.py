from abc import ABC, abstractmethod
from orionis.services.introspection.dependencies.entities.class_dependencies import ClassDependency
from orionis.services.introspection.dependencies.entities.method_dependencies import MethodDependency

class IReflectDependencies(ABC):
    """
    Interface for reflecting dependencies of a given object.

    This interface provides methods to retrieve both resolved and unresolved
    dependencies from the constructor and methods of a class.
    """

    @abstractmethod
    def getConstructorDependencies(self) -> ClassDependency:
        """
        Retrieve dependencies from the constructor of the instance's class.

        Returns
        -------
        ClassDependency
            Structured representation of the constructor dependencies.

            - resolved : dict
                Dictionary of resolved dependencies with their names and values.
            - unresolved : list
                List of unresolved dependencies (parameter names without default values or annotations).
        """
        pass

    def getMethodDependencies(self, method_name: str) -> MethodDependency:
        """
        Retrieve dependencies from a method of the instance's class.

        Parameters
        ----------
        method_name : str
            Name of the method to inspect.

        Returns
        -------
        MethodDependency
            Structured representation of the method dependencies.

            - resolved : dict
                Dictionary of resolved dependencies with their names and values.
            - unresolved : list
                List of unresolved dependencies (parameter names without default values or annotations).
        """
        pass