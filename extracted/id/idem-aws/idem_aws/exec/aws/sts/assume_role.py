"""Exec module for assume role."""
from typing import Any
from typing import Dict
from typing import List


async def credentials(
    hub,
    ctx,
    role_arn: str,
    role_session_name: str,
    *,
    policy_arns: List[Dict[str, Any]] = None,
    policy: str = None,
    duration_seconds: int = None,
    tags: List[Dict[str, str]] = None,
    transitive_tag_keys: List[str] = None,
    external_id: str = None,
    serial_number: str = None,
    token_code: str = None,
    source_identity: str = None,
) -> Dict[str, Any]:
    """Returns a set of temporary security credentials to access AWS resources that you might not normally have access to.

    Args:
        role_arn(str):
            The ARN of the role to assume to access AWS resources.

        role_session_name(str):
            An identifier for the assumed role session. Use  the  role  session name to uniquely identify
            a session when the same role is assumed by different principals or for  different  reasons.

        policy_arns(list[dict[str, Any]], Optional):
            The  ARNs of the IAM managed policies that you want to use as managed session policies. The policies
            must exist in the same account as the role.

        policy(str, Optional):
            An  IAM policy in JSON format that you want to use as an inline session policy.

        duration_seconds(int, Optional):
            The  duration,  in seconds, of the role session. By default, the value is set to 3600 seconds.
            The value specified can range from 900 seconds (15 minutes) up to  the  maximum  session
            duration  which can have a value from 1 hour to 12 hours.

        tags(list[dict[str, str]], Optional):
            A list of session tags that you want to pass in the format of ``[{"Key": tag-key, "Value": tag-value}]``.
            Each session tag  consists  of  a  key name and an associated value. You can pass up to 50 session tags.
            The plaintext session tag keys can't exceed 128 characters, and the  values can't exceed 256 characters.

            * Key (*str*):
                The key of the tag.
            * Value (*str*):
                The value of the tag.

        transitive_tag_keys(list(str), Optional):
            A list of keys for session tags that you want to set as  transitive. If  you set a tag key as transitive,
            the corresponding key and value passes to subsequent sessions in a role chain.

        external_id(str, Optional):
            A unique identifier that might be required when you assume a role in another  account.

        serial_number(str, Optional):
            The identification number of the MFA device that is associated  with the  user  who  is
            making the credentials call. Specify this value if the trust policy of the role being assumed
            includes a condition that requires  MFA  authentication.

        token_code(str, Optional):
            The  value  provided  by  the MFA device, if the trust policy of the role being assumed requires MFA.

        source_identity(str, Optional):
            The source identity specified by the principal that is  calling  the credential operation.

    Returns:
        Dict[str, Any]:
            The temporary security credentials, which include an access key ID, a secret access key, and
            a security (or session) token.

    Examples:
        Call from the CLI:

        .. code-block:: bash

            $ idem exec aws.sts.assume_role.credentials <role_arn> <role_session_name>

        Call from code:

        .. code-block:: python

            async def my_func(hub, ctx, role_arn:str, role_session_name:str):
                await hub.exec.aws.sts.assume_role.credentials(ctx, role_arn, role_session_name)

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.sts.assume_role.credentials
                - kwargs:
                    role_arn: role_arn
                    role_session_name: role_session_name

    """
    ret = dict(result=True, ret={}, comment="")
    hub.log.debug(f"Assume role configuration set for ARN {role_arn}")

    config = {"RoleArn": role_arn, "RoleSessionName": role_session_name}
    if external_id is not None:
        config["ExternalId"] = external_id
    if policy_arns is not None:
        config["PolicyArns"] = policy_arns
    if policy is not None:
        config["Policy"] = policy
    if tags is not None:
        config["Tags"] = tags
    if transitive_tag_keys is not None:
        config["TransitiveTagKeys"] = transitive_tag_keys
    if duration_seconds is not None:
        config["DurationSeconds"] = duration_seconds
    if serial_number is not None:
        config["SerialNumber"] = serial_number
    if token_code is not None:
        config["TokenCode"] = token_code
    if source_identity is not None:
        config["SourceIdentity"] = source_identity

    assumed_role_object = await hub.exec.boto3.client.sts.assume_role(ctx, **config)
    ret["result"] = assumed_role_object.result
    ret["comment"] = assumed_role_object.comment
    if assumed_role_object.result:
        ret["ret"] = assumed_role_object.ret["Credentials"]
    return ret
