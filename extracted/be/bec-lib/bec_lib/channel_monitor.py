"""
This module provides a command line interface to monitor a channel.
"""

import argparse
import json
import re
import threading

from bec_lib.endpoints import MessageEndpoints
from bec_lib.redis_connector import RedisConnector


def channel_callback(msg, **_kwargs):
    """
    Callback for channel monitor.
    """
    msg = msg.get("data")
    if not msg:
        return
    out = {"msg_type": msg.msg_type, "content": msg.content, "metadata": msg.metadata}
    print(json.dumps(out, indent=4, default=lambda o: "<not serializable object>"))


def _start_register(redis_config, topic, callback, *args, **kwargs):
    connector = RedisConnector(redis_config)
    connector.register(topics=topic, cb=callback, **kwargs)
    event = threading.Event()
    event.wait()


def channel_monitor_launch():
    """
    Launch a channel monitor for a given channel.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--redis", default="localhost:6379", required=False, help="host:port of redis"
    )
    parser.add_argument(
        "--channel", required=True, help="channel name, e.g. internal/devices/read/samx"
    )
    clargs = parser.parse_args()
    redis_config = clargs.redis
    topic = clargs.channel

    _start_register(redis_config, topic, channel_callback)


def log_callback(msg, log_filter=None):
    """
    Callback for channel monitor.
    """
    msg = msg.get("data")
    if not msg:
        return

    print_msg = msg.log_msg["text"]
    if log_filter is not None:
        found = log_filter.lower() in print_msg.lower() or re.search(log_filter, print_msg)
        if found is None:
            return
    print(print_msg)


def log_monitor_launch():
    """
    Launch a log monitor.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--redis", default="localhost:6379", required=False, help="host:port of redis"
    )
    parser.add_argument("--filter", default=None, required=False, help="filter for log messages")
    clargs = parser.parse_args()
    redis_config = clargs.redis
    topic = MessageEndpoints.log()
    log_filter = clargs.filter

    _start_register(redis_config, topic, log_callback, log_filter=log_filter)


# if __name__ == "__main__":
#     import sys

#     sys.argv = ["", "--filter", "waveform"]
#     log_monitor_launch()
