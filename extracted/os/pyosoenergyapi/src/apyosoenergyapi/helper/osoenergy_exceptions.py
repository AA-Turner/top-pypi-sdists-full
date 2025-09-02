"""OSO Energy exception class."""


class OSOEnergyApiError(Exception):
    """Api error.

    Args:
        Exception (object): Exception object to invoke
    """


class OSOEnergyReauthRequired(Exception):
    """Re-Authentication is required.

    Args:
        Exception (object): Exception object to invoke
    """


class OSOEnergyUnknownConfiguration(Exception):
    """Unknown OSO Energy Configuration.

    Args:
        Exception (object): Exception object to invoke
    """


class NoSubscriptionKey(Exception):
    """No Subscription key exception.

    Args:
        Exception (object): Exception object to invoke
    """
