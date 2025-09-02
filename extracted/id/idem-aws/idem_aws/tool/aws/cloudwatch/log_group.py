from typing import Dict


async def search_raw(hub, ctx, name, resource_id: str = None) -> Dict:
    """
    Fetch one or more log groups from AWS. The return will be in the same format as what the boto3 api returns.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str, Optional):
            Aws logGroupNamePrefix (The prefix to match.)

    Returns:
        {"result": True|False, "comment": A message List, "ret": Dict}
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.exec.boto3.client.logs.describe_log_groups(
        ctx,
        logGroupNamePrefix=resource_id if resource_id else None,
    )
    result["result"] = ret["result"]
    result["comment"] = list(ret["comment"])
    result["ret"] = ret["ret"]
    return result
