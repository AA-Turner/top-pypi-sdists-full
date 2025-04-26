import os
import re
from typing import List
from urllib import parse

QUEUE_APP_ID = "app_queue_client"
UTF_QUEUE_REGION_MAP = {
    "aws-us-east-1": "central",
    "vmw-us-aus-1": "aus",
    "vmw-us-bos-1": "bos",
    "vmw-eu-bud-1": "bud",
    "vmw-ap-hyd-1": "hyd",
    "vmw-ca-yul-1": "yul",
}
UTF_QUEUE_SERVER_PREFIX = "utf-queue-"
UTF_QUEUE_SERVER_PATTERN = (
    "amqps://(.*):(.*)@"
    + rf"({UTF_QUEUE_SERVER_PREFIX}({'|'.join(UTF_QUEUE_REGION_MAP.values())}))"
    + r"\.(dev\.silabs\.net|silabs\.net):443"
)


def prepare_queue_central_url(username, password):
    if username is None or password is None:
        raise RuntimeError("username or password must be provided if using queue")
    hostname = os.environ.get("UTF_QUEUE_HOSTNAME", "utf-queue-central.silabs.net")
    scheme = os.environ.get("UTF_QUEUE_SCHEME", "amqps")
    port = os.environ.get("UTF_QUEUE_PORT", "443")
    virtual_host = os.environ.get("UTF_QUEUE_VIRTUAL_HOST", "%2f")
    return f"{scheme}://{username}:{parse.quote(password)}@{hostname}:{port}/{virtual_host}"


def get_closest_queue_region():
    """
    Return the correct value from the UTF_QUEUE_REGION_MAP dictionary
    based on the key contained in the NOMAD_DC environment variable (if it's defined).
    If NOMAD_DC is not defined or the key is not in UTF_QUEUE_REGION_MAP, we'll just
    return "central"
    """
    if "NOMAD_DC" in os.environ:
        dc = os.environ["NOMAD_DC"]
        if dc in UTF_QUEUE_REGION_MAP:
            return UTF_QUEUE_REGION_MAP[dc]

    return "central"


def get_queue_url_list(original_url: str) -> List[str]:
    """
    The purpose of this function is to return a list of alternative
    utf queue urls given a single original url.
    If 'original_url' matches the UTF_QUEUE_SERVER_PATTERN regex,
    return a list of urls based on the values in the UTF_QUEUE_REGION_MAP dict,
    where the order is determined by the NOMAD_DC environment variable.

    Example:
    1)  if original_url is "amqps://xxxx:yyyy@utf-queue-central.silabs.net:443/%2F"
        and NOMAD_DC is "vmw-ap-hyd-1",
        we'll return
        - amqps://xxxx:yyyy@utf-queue-hyd.silabs.net:443/%2F
        - amqps://xxxx:yyyy@utf-queue-central.silabs.net:443/%2F
        - amqps://xxxx:yyyy@utf-queue-aus.silabs.net:443/%2F
        - amqps://xxxx:yyyy@utf-queue-bos.silabs.net:443/%2F
          etc.
    2) if original_url is "amqps://xxxx:yyyy@utf-queue-central.silabs.net:443/%2F"
        and NOMAD_DC is not defined,
        we'll return
        - amqps://xxxx:yyyy@utf-queue-central.silabs.net:443/%2F
        - amqps://xxxx:yyyy@utf-queue-aus.silabs.net:443/%2F
        - amqps://xxxx:yyyy@utf-queue-bos.silabs.net:443/%2F
          etc.
    3) if original_url doesn't match the UTF_QUEUE_SERVER_PATTERN pattern
       we'll return a list containing original_url as the only item.
    """
    m = re.match(UTF_QUEUE_SERVER_PATTERN, original_url)
    if not m:
        return [original_url]

    hostname_base = m.group(3)
    domain = m.group(5)

    url_list = []
    region_list = [get_closest_queue_region()] + list(UTF_QUEUE_REGION_MAP.values())
    for region in region_list:
        url = original_url.replace(
            f"{hostname_base}.{domain}", f"{UTF_QUEUE_SERVER_PREFIX}{region}.{domain}"
        )
        url_list.append(url)
    return list(dict.fromkeys(url_list))
