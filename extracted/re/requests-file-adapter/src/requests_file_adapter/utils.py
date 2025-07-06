#!/usr/bin/env python3
"""
Utilities.
"""


import requests

from .adapter import FileAdapter


def get_session():
    """
    Get a requests.Session object with support for URI file schemes.
    """
    session = requests.Session()
    session.mount("file://", FileAdapter())
    return session
