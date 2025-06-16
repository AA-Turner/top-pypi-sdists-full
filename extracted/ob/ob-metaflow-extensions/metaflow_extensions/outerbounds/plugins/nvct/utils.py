import os
import json
import requests
from urllib.parse import urlparse
from metaflow.metaflow_config import SERVICE_URL
from metaflow.metaflow_config_funcs import init_config


def get_ngc_api_key():
    conf = init_config()
    if "OBP_AUTH_SERVER" in conf:
        auth_host = conf["OBP_AUTH_SERVER"]
    else:
        auth_host = "auth." + urlparse(SERVICE_URL).hostname.split(".", 1)[1]

    # NOTE: reusing the same auth_host as the one used in NimMetadata,
    # however, user should not need to use nim container to use @nvct.
    # May want to refactor this to a common endpoint.
    nim_info_url = "https://" + auth_host + "/generate/nim"

    if "METAFLOW_SERVICE_AUTH_KEY" in conf:
        headers = {"x-api-key": conf["METAFLOW_SERVICE_AUTH_KEY"]}
        res = requests.get(nim_info_url, headers=headers)
    else:
        headers = json.loads(os.environ.get("METAFLOW_SERVICE_HEADERS"))
        res = requests.get(nim_info_url, headers=headers)

    res.raise_for_status()
    return res.json()["nvcf"]["api_key"]
