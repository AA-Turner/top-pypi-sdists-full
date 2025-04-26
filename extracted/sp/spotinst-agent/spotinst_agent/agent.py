#!/usr/bin/env python

"""Executor:  execute remote scripts periodically.

Usage:  spotinst-agent [options]
--verbose           verbose logs
--debug                run with dummy credentials for debug purposes
"""

import logging.handlers
import signal
import sys
import yaml
from os.path import join
from time import sleep
from agentinit import init__configuration
from taskmanager import TaskManager


def run_agent(debug=False, verbose=True):
    # Initialize Config
    cfg_file = join('/etc/spotinst/agent/config/spotinst-agent.yml')
    with open(cfg_file) as f:
        try:
            config = yaml.load(f)
        except yaml.YAMLError:
            print("ERROR: Config file: %s does not exist." % cfg_file)
            sys.exit(1)

    cloud_provider = get_cloud_provider(config)

    # Initialize Logging
    log = logging.getLogger('spotinst-agent')
    log.setLevel(logging.INFO)  # Configure Logging Format

    if verbose is True:
        log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] [%(threadName)s] %(message)s')

    # Configure Log File handler - 20Mb x 5 files
    file_handler = logging.handlers.RotatingFileHandler('/var/log/spotinst/spotinst-agent.log', 'a', maxBytes=20000000,
                                                        backupCount=5)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    log.addHandler(file_handler)

    stdout_handler = logging.StreamHandler(sys.stdout)
    log.addHandler(stdout_handler)

    instance_details = init__configuration(config, cloud_provider, debug)

    try_num = 1
    while not instance_details and try_num < 3:
        sleep(60)
        log.info("trying to init configuration again (retry {})".format(try_num))
        try_num += 1
        instance_details = init__configuration(config, cloud_provider, debug)

    if not instance_details:
        log.error("init failed")
        exit(1)

    log.info("Start")
    r = TaskManager(config['enable'], config['reload_interval'], instance_details)

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


def get_cloud_provider(config):
    cloud_provider_file = None
    response = 'AWS'
    try:
        cloud_provider_file = open(config['cloud_provider_path'], 'r')
        response = cloud_provider_file.read().strip('\n')
        cloud_provider_file.close()
        if response.lower() == 'azure':
            response = 'Azure'
        elif response.lower() == 'azure_spot':
            response = 'Azure_Spot'
        elif response.lower() == 'gcp':
            response = 'GCP'
        else:
            response = 'AWS'
    except IOError:
        if cloud_provider_file is not None:
            cloud_provider_file.close()
    return response

if __name__ == '__main__':
    run_agent()
