from orionis.foundation.application import Application, IApplication

def Orionis() -> IApplication:
    """
    Creates and returns an instance of the Orionis application.

    This function initializes the core application object, which implements
    the `IApplication` interface. It serves as the entry point for setting up
    and accessing the main application instance.

    Returns
    -------
    IApplication
        An instance of the application implementing the `IApplication` interface.
    """

    # Instantiate and return the main application object
    return Application()