"""Custom Logging Module."""

import inspect
from datetime import datetime


class Logger:
    """Custom Logging Code."""

    def __init__(self, session=None):
        """Initialise the logger class."""
        self.session = session

    async def error(self, error="UNKNOWN"):
        """Process and unexpected error."""
        self.session.logger.error(
            f"An unexpected error has occurred whilst"
            f" executing {inspect.stack()[1][3]}"
            f" with exception {error.__class__} {error}"
        )

    async def error_check(self, n_id, error_type):
        """Error has occurred."""
        message = None

        if error_type is False:
            message = "Device offline could not update entity - " + n_id
            if n_id not in self.session.config.error_list:
                self.session.logger.warning(message)
                self.session.config.error_list.update({n_id: datetime.now()})
        elif error_type == "Failed":
            message = "ERROR - No data found for device - " + n_id
            if n_id not in self.session.config.error_list:
                self.session.logger.error(message)
                self.session.config.error_list.update({n_id: datetime.now()})
