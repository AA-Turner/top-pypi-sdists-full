import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

import click

from cnvrgv2.config import Config, GLOBAL_CNVRG_PATH


class CnvrgLogger:
    DEFAULT_KEEP_DURATION_DAYS = 7
    CLI_LOGGER = "cli-logger"
    LOGS_DIR = os.path.join(GLOBAL_CNVRG_PATH, "logs")
    LOG_FILE_NAME = "cnvrg.log"

    def __init__(self, click):
        # prepare command will create the config file if it does not exist
        config = Config()
        keep_duration_days = (
            config.keep_duration_days or
            CnvrgLogger.DEFAULT_KEEP_DURATION_DAYS
        )

        self.click = click
        self.logger = logging.getLogger(CnvrgLogger.CLI_LOGGER)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s \t [%(levelname)s] > %(message)s')

        if not os.path.isdir(CnvrgLogger.LOGS_DIR):
            os.makedirs(CnvrgLogger.LOGS_DIR)

        log_file_path = os.path.join(CnvrgLogger.LOGS_DIR, CnvrgLogger.LOG_FILE_NAME)
        handler = TimedRotatingFileHandler(log_file_path,
                                           when="midnight",
                                           backupCount=keep_duration_days)

        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

    def log_and_echo(self, message, error=False):
        """
        logs the message to the log file and prints it to stdout through click echo function
        @param message: The message to log
        @param error: Boolean. Whenever the log is an error. If it is, program will exit with status code 1
        @return: None
        """
        if error:
            self.click.secho(message, err=error, fg='red')
            self.logger.error(message)
            sys.exit(1)
        else:
            self.click.echo(message, err=error)
            self.logger.info(message)

    def __getattr__(self, item):
        return getattr(self.logger, item)

    @staticmethod
    @click.command()
    @click.option('--days',
                  default=7,
                  prompt='Please specify the number of days to keep logs',
                  help='Number of days to keep logs'
                  )
    def set_logs_keep_duration(days):
        """
        Sets the number of days to keep logs as backup
        """
        config = Config()
        config.keep_duration_days = days
        config.save()
