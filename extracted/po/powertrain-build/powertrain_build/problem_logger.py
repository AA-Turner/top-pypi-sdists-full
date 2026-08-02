# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module containing a problem logger class."""


class ProblemLogger:
    """Log helper class.

    Inherit from class ProblemLogger to log problems.

    Please note that all methods listed below are class methods
    meaning that all objects of classes inheriting ProblemLogger share a common logging stream.
    """

    __critical = []
    __warning = []
    __log = None

    @classmethod
    def init_logger(cls, logger):
        """Associates a system logger instance with ProblemLogger."""
        logger.info('Init logger.')
        cls.__log = logger

    @classmethod
    def clear_log(cls):
        """Clear internal error and warning log."""
        cls.__critical = []
        cls.__warning = []

    @classmethod
    def critical(cls, string, *args):
        """Log critical error message."""
        cls.__critical.append(string % args)
        if cls.__log is not None:
            cls.__log.critical(string, *args)

    @classmethod
    def warning(cls, string, *args):
        """Log warning message."""
        cls.__warning.append(string % args)
        if cls.__log is not None:
            cls.__log.warning(string, *args)

    @classmethod
    def info(cls, string, *args):
        """Log information message."""
        if cls.__log is not None:
            cls.__log.info(string, *args)

    @classmethod
    def debug(cls, string, *args):
        """Log debug message."""
        if cls.__log is not None:
            cls.__log.debug(string, *args)

    @classmethod
    def errors(cls):
        """Check if critical errors have been logged.

        Returns (boolean): True if critical errors have been logged.
        """
        return len(cls.__critical) > 0

    @classmethod
    def get_problems(cls):
        """Get logged problems.

        Returns (dict): a dict with error and warning messages.
        """
        return {
            'critical': cls.__critical,
            'warning': cls.__warning
        }

    @classmethod
    def get_nbr_problems(cls):
        """Get number of logged problems.

        Returns (dict): a dict with error and warning message counts.
        """
        return {
            'critical': len(cls.__critical),
            'warning': len(cls.__warning)
        }
