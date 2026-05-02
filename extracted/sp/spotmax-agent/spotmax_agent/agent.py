#!/usr/bin/env python

import logging.handlers
import signal
import sys
# from os.path import join
from .taskmanager import TaskManager


def run_agent(debug=False, verbose=True):
    # Initialize Logging
    log = logging.getLogger('spotmax-agent')
    log.setLevel(logging.INFO)  # Configure Logging Format

    if verbose is True:
        log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] [%(threadName)s] %(message)s')

    # Configure Log File handler - 20Mb x 5 files
    file_handler = logging.handlers.RotatingFileHandler('/var/log/spotmax/spotmax-agent.log', 'a', maxBytes=20000000,
                                                        backupCount=5)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    log.addHandler(file_handler)

    stdout_handler = logging.StreamHandler(sys.stdout)
    log.addHandler(stdout_handler)

    r = TaskManager(True, 20, "instance_details")

    def sigint_handler(signum, frame):
        # Log
        log.debug("Signal Received: %d" % signum)
        # Stop Agent
        r.stop()

        # Set the signal handler
        signal.signal(signal.SIGINT, sigint_handler)  # Run Agent

    # Set the signal handlers
    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGTERM, sigint_handler)

    r.start()


if __name__ == '__main__':
    run_agent()
