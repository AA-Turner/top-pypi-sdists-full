"""OSO Energy Helper code."""


class OSOEnergyHelper:  # pylint: disable=too-few-public-methods
    """OSO Energy helper class."""

    def __init__(self, session: object = None):
        """OSO Energy Helper.

        Args:
            session (object, optional): Interact with OSO Energy. Defaults to None.
        """
        self.session = session

    def device_recovered(self, n_id: str):
        """Register that device has recovered from being offline.

        Args:
            n_id (str): ID of the device
        """
        if n_id in self.session.config.error_list:
            self.session.config.error_list.pop(n_id)
