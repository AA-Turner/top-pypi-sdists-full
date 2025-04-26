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
>>> @online
... def fn() -> User.name:
...     chalk_logger.info("running")
...     return ...
"""
chalk_logger.addFilter(_UserLoggerFilter())
