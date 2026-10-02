# flake8: noqa: I003

from fabric.functions.user_data_functions import UserDataFunctions
from .fabric_business_events import FabricBusinessEventsClient
from .business_events_provider import BusinessEventsClientProvider


def use_business_events(udf: UserDataFunctions):
    """Register the BusinessEventsClientProvider with the UserDataFunctions instance.
    
    Args:
        udf: The UserDataFunctions instance to register the provider with
    """
    udf.register_provider(FabricBusinessEventsClient, BusinessEventsClientProvider)
