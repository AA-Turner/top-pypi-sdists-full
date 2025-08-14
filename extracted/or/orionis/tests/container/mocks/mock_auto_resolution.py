class MockAppService:
    """
    Mock service that can be auto-resolved by the dependency injection container.

    This class simulates a basic application service with no external dependencies,
    making it suitable for testing automatic resolution scenarios.
    """

    def __init__(self):
        # Set service identifier
        self.name = "MockAppService"
        # Mark as properly initialized
        self.initialized = True

class MockDependency:
    """
    Mock dependency for testing dependency injection scenarios.

    This class represents a simple dependency that can be injected into other
    services during container resolution testing.
    """

    def __init__(self):
        # Set a test value that can be verified in dependent services
        self.value = "dependency_value"

class MockServiceWithDependency:
    """
    Mock service that depends on another service for dependency injection testing.

    This class demonstrates single dependency injection where the container
    must resolve and inject the required MockDependency instance.

    Parameters
    ----------
    dependency : MockDependency
        The dependency instance to be injected by the container.
    """

    def __init__(self, dependency: MockDependency):
        # Store the injected dependency
        self.dependency = dependency
        # Set service identifier
        self.name = "MockServiceWithDependency"

class MockServiceWithMultipleDependencies:
    """
    Mock service with multiple dependencies for complex injection testing.

    This class tests the container's ability to resolve and inject multiple
    dependencies simultaneously in the correct order.

    Parameters
    ----------
    dependency : MockDependency
        The primary dependency instance to be injected.
    app_service : MockAppService
        The application service instance to be injected.
    """

    def __init__(self, dependency: MockDependency, app_service: MockAppService):
        # Store the primary dependency
        self.dependency = dependency
        # Store the application service dependency
        self.app_service = app_service
        # Set service identifier
        self.name = "MockServiceWithMultipleDependencies"

class MockServiceWithDefaultParam:
    """
    Mock service with a default parameter for optional dependency testing.

    This class tests the container's handling of services that have both
    required dependencies and optional parameters with default values.
        Parameters
    ----------
    dependency : MockDependency
        The required dependency instance to be injected.
    optional_param : str, default "default_value"
        An optional parameter that should not be resolved by the container.
    """

    def __init__(self, dependency: MockDependency, optional_param: str = "default_value"):
        # Store the required dependency
        self.dependency = dependency
        # Store the optional parameter (should use default if not provided)
        self.optional_param = optional_param

class MockServiceWithUnresolvableDependency:
    """
    Mock service with a dependency that cannot be resolved by the container.

    This class is used to test error handling when the container encounters
    dependencies that cannot be automatically resolved (primitive types, etc.).

    Parameters
    ----------
    unresolvable_param : int
        A primitive type parameter that cannot be auto-resolved by the container.
    """

    def __init__(self, unresolvable_param: int):
        # Store the unresolvable parameter
        self.unresolvable_param = unresolvable_param

class MockServiceWithMethodDependencies:
    """
    Mock service with methods that have dependencies for method injection testing.

    This class tests the container's ability to resolve dependencies for
    specific method calls rather than just constructor injection.
    """

    def __init__(self):
        # Set service identifier
        self.name = "MockServiceWithMethodDependencies"

    def process_data(self, dependency: MockDependency, data: str = "default") -> str:
        """
        Process data using an injected dependency.

        This method demonstrates dependency injection at the method level,
        where the container must resolve the dependency parameter while
        preserving optional parameters.

        Parameters
        ----------
        dependency : MockDependency
            The dependency instance to be injected for data processing.
        data : str, default "default"
            The data string to be processed.

        Returns
        -------
        str
            A formatted string containing the processed data and dependency value.
        """
        # Combine the input data with the dependency's value
        return f"Processed {data} with {dependency.value}"

    def complex_operation(self, dependency: MockDependency, app_service: MockAppService) -> dict:
        """
        Perform a complex operation using multiple injected dependencies.

        This method tests multiple dependency injection at the method level,
        ensuring the container can resolve multiple dependencies simultaneously.

        Parameters
        ----------
        dependency : MockDependency
            The primary dependency instance to be injected.
        app_service : MockAppService
            The application service instance to be injected.

        Returns
        -------
        dict
            A dictionary containing the dependency values and operation result.
        """

        # Return a structured result containing information from both dependencies
        return {
            "dependency": dependency.value,
            "app_service": app_service.name,
            "result": "complex_operation_result"
        }

# Non-resolvable classes (outside valid namespaces)
class ExternalLibraryClass:
    """
    Simulates an external library class that shouldn't be auto-resolved.

    This class represents dependencies from external libraries that should
    not be automatically resolved by the container due to namespace restrictions.
    """

    def __init__(self):
        # External classes typically have their own initialization logic
        pass

# Configure module paths to simulate valid application namespaces
# These assignments make the classes appear to be in valid app namespaces for testing
MockAppService.__module__ = 'app.services.mock_app_service'
MockDependency.__module__ = 'app.dependencies.mock_dependency'
MockServiceWithDependency.__module__ = 'app.services.mock_service_with_dependency'
MockServiceWithMultipleDependencies.__module__ = 'app.services.mock_service_with_multiple_dependencies'
MockServiceWithDefaultParam.__module__ = 'app.services.mock_service_with_default_param'
MockServiceWithUnresolvableDependency.__module__ = 'app.services.mock_service_with_unresolvable_dependency'
MockServiceWithMethodDependencies.__module__ = 'app.services.mock_service_with_method_dependencies'

# External class should not be auto-resolved due to invalid namespace
ExternalLibraryClass.__module__ = 'external_library.some_module'