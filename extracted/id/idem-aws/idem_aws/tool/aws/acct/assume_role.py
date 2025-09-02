from typing import Any
from typing import Dict

import dict_tools.data


async def modify(
    hub, name: str, raw_profile: Dict[str, Any], new_profile: Dict[str, Any]
):
    """
    Assume a role using the credentials in the raw_profile.
    Create a new profile with keys and ids based on the assumed role.
    If assuming the role fails, the new_profile is made completely unusable.
    """
    if "assume_role" not in raw_profile:
        return

    # Get new access credentials for the assumed role
    assume_role_obj = raw_profile.pop("assume_role", {})

    ctx = dict_tools.data.NamespaceDict(acct=raw_profile, test=False)

    try:
        credentials = await hub.exec.aws.sts.assume_role.credentials(
            ctx, **assume_role_obj
        )
    except Exception as e:
        raise ConnectionError(f"Failed to assume role: {e.__class__.__name__}:{e}")

    if not credentials.result:
        # Failed to assume the role, don't allow a half-baked profile to be used
        new_profile.clear()
        raise ConnectionError(f"Failed to assume role: {credentials.comment}")

    # Overwrite the credentials for the profile with the ones from the assumed role
    new_profile["aws_access_key_id"] = credentials.ret["AccessKeyId"]
    new_profile["aws_secret_access_key"] = credentials.ret["SecretAccessKey"]
    new_profile["aws_session_token"] = credentials.ret["SessionToken"]
