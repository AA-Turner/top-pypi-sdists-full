#!/usr/bin/env python3
"""
IP functions.
"""

import logging
import socket

import psutil


LOGGER = logging.getLogger(__name__)


def local_ip_addresses():
    """
    A generator over local IP addresses. Note that some of these may refer to IP
    addresses of hosted containers, which may break assumptions about mapping
    file URIs to the host file system.
    """
    for addr_data in psutil.net_if_addrs().values():
        for item in addr_data:
            yield item.address


def is_localhost(host):
    """
    Check if a host appears to be localhost.

    Args:
        host:
            A hostname or IP address.
    """
    try:
        host = socket.gethostbyname(host)
    except socket.gaierror as err:
        LOGGER.debug('Failed to resolve host "%s": %s', host, err)
    return host in local_ip_addresses()
