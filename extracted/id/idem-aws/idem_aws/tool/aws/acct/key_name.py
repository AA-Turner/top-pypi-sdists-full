from typing import Any
from typing import Dict

import botocore.config

BOTO_CONFIG_OPTS = (opt for opt in botocore.config.Config.OPTION_DEFAULTS.keys())


async def modify(
    hub, name: str, raw_profile: Dict[str, Any], new_profile: Dict[str, Any]
):
    """
    Conform the different possibilities for profile key values to exactly what is accepted by aws
    """
    config = raw_profile.get("config", {})
    if isinstance(config, Dict):
        # https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html
        kwargs = {}
        for k, v in config.items():
            if k in BOTO_CONFIG_OPTS:
                kwargs[k] = v
        config = botocore.config.Config(**kwargs)

    new_profile["region_name"] = _key_options(
        raw_profile, "region_name", "region", "location"
    )
    if new_profile["region_name"] is None:
        new_profile["region_name"] = hub.tool.boto3.region.get(ctx=None)
    new_profile["verify"] = raw_profile.get("verify", None)
    new_profile["use_ssl"] = raw_profile.get("use_ssl", True)
    new_profile["endpoint_url"] = _key_options(raw_profile, "endpoint_url", "endpoint")
    new_profile["aws_access_key_id"] = _key_options(
        raw_profile, "aws_access_key_id", "key_id", "id"
    )

    new_profile["aws_secret_access_key"] = _key_options(
        raw_profile, "aws_secret_access_key", "secret_access_key", "access_key", "key"
    )
    new_profile["aws_session_token"] = _key_options(
        raw_profile, "aws_session_token", "session_token", "token", "key"
    )
    new_profile["config"] = config


def _key_options(d: Dict[str, Any], *keys):
    """
    Return the first match for a given key
    """
    for key in keys:
        if key in d:
            return d[key]
    else:
        return None
