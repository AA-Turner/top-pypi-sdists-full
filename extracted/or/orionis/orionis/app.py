from orionis.foundation.application import Application, IApplication

def Orionis() -> IApplication:
    """
    Initialize and return the main Orionis application instance.

    Initializes the core application object that implements the `IApplication` interface.
    This function acts as the entry point for creating and accessing the main application instance.

    Returns
    -------
    IApplication
        The initialized application instance implementing the `IApplication` interface.
    """

    # Instantiate and return the main application object
    return Application()
