import logging

import chalk.utils.log_with_context


class _UserLoggerFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.is_user_logger = True
        return True


# Named to "chalk.clogging.chalk_logger" for backwards compatibility
# The name must begin with `chalk` so it will be picked up by the logging filters
chalk_logger = chalk.utils.log_with_context.get_logger("chalk.clogging.chalk_logger")
"""A logger for use in resolvers.

Examples
--------
>>> from chalk.features import online
>>> from chalk.logging import chalk_logger
>>> @online
... def get_user_feature(User.id) -> User.name:
...     chalk_logger.info("running")
...     return ...
"""
chalk_logger.addFilter(_UserLoggerFilter())
