class UnsupportedConfigItemError(Exception):
    """
    Unsupported config item error.

    The manifest and configuration specified an item which the SDK is incapable of handling yet.
    """

    pass


class MissingRequiredConfigItemError(Exception):
    """
    Missing required config item error.

    A config item was invoked as required, but missing in the configuration item store.
    """

    pass


class InaccessibleConfigItemError(Exception):
    """
    Inaccessible config item error.

    A config item linked resource was inaccessible (the caller does not have permissions).
    """

    pass


class ConfigItemLinkedResourceError(Exception):
    """
    Config item linked resource error.

    A config item is not a type that has an associated linked resource.
    """

    pass
