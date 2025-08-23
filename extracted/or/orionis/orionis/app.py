from pathlib import Path
from orionis.foundation.application import Application, IApplication

def Orionis(basePath: str | Path = Path.cwd().resolve()) -> IApplication:
    """
    Initializes and returns the main Orionis application instance.

    This function creates the core application object that implements the `IApplication` interface.
    It acts as the primary entry point for setting up and accessing the main application instance,
    ensuring that the application is initialized with the specified base path.

    Parameters
    ----------
    basePath : str or Path, optional
        The base directory path for the application. Defaults to the current working directory.

    Returns
    -------
    IApplication
        The initialized `Application` instance implementing the `IApplication` interface,
        configured with the provided base path.
    """

    # Instantiate the main application object implementing IApplication
    app: IApplication = Application()

    # Set the base path for the application and return the configured instance
    return app.setBasePath(basePath)
