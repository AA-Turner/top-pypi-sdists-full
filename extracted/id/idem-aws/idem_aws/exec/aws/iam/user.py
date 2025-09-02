__func_alias__ = {"list_": "list"}


async def list_(hub, ctx):
    """Lists AWS IAM Users.

    Returns:
        Dict[bool, list, dict or None]:

        result(bool):
            Whether the result of the function has been successful (``True``) or not (``False``).
        comment(list):
            A list of messages.
        ret(dict or None):
           The IAM Policies in "present" format.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.iam.user.list

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.iam.user.list
    """
    ret = await hub.exec.boto3.client.iam.list_users(ctx)

    if not ret["result"]:
        return {
            "result": False,
            "ret": [],
            "comment": f"Can not list users: {ret['comment']}",
        }

    users = []
    for user_raw in ret["ret"]["Users"]:
        # we're using this function for the camel case to snake case
        user = hub.tool.aws.iam.conversion_utils.convert_raw_user_to_present(user_raw)
        users.append(user)

    return {"result": True, "ret": users}
