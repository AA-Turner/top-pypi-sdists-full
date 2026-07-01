#
# Copyright 2026 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.

from __future__ import annotations

from typing import Optional
from urllib.parse import urlparse

import requests

from datarobot import client as dr_client
from datarobot.errors import ClientError


def supports_range_requests(url: str, client: Optional[requests.Session] = None) -> bool:
    """
    Check if server supports range requests for the given URL.

    Parameters
    ----------
    url:
        The URL to check.
    client:
        The requests session to use for the request. Defaults to a new session.

    Returns
    -------
    bool
        True if the server supports range requests, False otherwise.
    """
    if not client:
        client = requests.Session()
    try:
        response = client.get(url, headers={"Range": "bytes=0-0"}, stream=True)
        response.close()
        return response.status_code == 206 or response.headers.get("Accept-Ranges", "").lower() == "bytes"
    except (requests.RequestException, ClientError):
        return False


def is_datarobot_url(url: str) -> bool:
    """
    Check if a URL is from the configured DataRobot instance.

    Parameters
    ----------
    url:
        The URL to check.

    Returns
    -------
    bool
        True if the URL is from the DataRobot instance, False otherwise.
    """
    try:
        client = dr_client.get_client()
        parsed_url = urlparse(url)
        url_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        return url_domain == client.domain
    except Exception:
        return False
