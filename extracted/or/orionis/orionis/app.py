from orionis.foundation.application import Application, IApplication

def Orionis() -> IApplication:
    """
    Instantiates and returns the main application object implementing the IApplication interface.

    This function serves as a factory for creating the core Application instance, which manages
    the lifecycle, configuration, and services of the Orionis framework.

    Returns
    -------
    IApplication
        An initialized instance of the Application class that implements the IApplication interface.
    """

    # Create and return the main Application instance
    return Application()