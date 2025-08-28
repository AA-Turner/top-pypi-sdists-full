from orionis.container.contracts.container import IContainer
from orionis.foundation.contracts.application import IApplication

class Application(IApplication, IContainer):
    """
    Application facade that provides a unified interface for application and container functionality.

    This class serves as the main application facade, combining the capabilities of both
    IApplication and IContainer interfaces. It acts as the central point for managing
    application lifecycle, service registration, dependency injection, and other
    core application concerns.

    The Application facade provides comprehensive access to:
    - Application configuration and environment settings management
    - Service container for dependency injection and service resolution
    - Application lifecycle management (bootstrap, startup, shutdown)
    - HTTP routing and middleware pipeline handling
    - Event dispatching, listening, and subscription management
    - Centralized logging, error handling, and exception management
    - Database connections and ORM integration
    - Cache management and session handling
    - Authentication and authorization services

    This facade implements the Facade design pattern to provide a simplified interface
    to the complex subsystems of the Orionis framework, making it easier for developers
    to interact with core application functionality without dealing with internal
    implementation details.

    Notes
    -----
    This is a type stub file (.pyi) that defines the interface contract for the
    Application facade implementation. The actual implementation should be found
    in the corresponding .py file.

    The class inherits from both IApplication and IContainer interfaces, ensuring
    it provides all methods required for application management and dependency
    injection container functionality.
    """

    # Type stub class - no implementation needed in .pyi files
    # The actual implementation will be provided in the corresponding .py file
    pass