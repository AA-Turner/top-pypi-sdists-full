# flake8: noqa: I005
from typing_extensions import deprecated
from fabric.functions.user_data_functions import UserDataFunctions


@deprecated("This class is deprecated. Please use 'UserDataFunctions' instead.")
class FabricApp(UserDataFunctions):
    """
    This class is deprecated. Please use 'UserDataFunctions' instead.
    """

    def __init__(self):
        """
        """
        
        super().__init__()