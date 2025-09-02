"""States module for managing Secretsmanager Secrets."""
import copy
import sys
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

from dict_tools import differ

if sys.version_info < (3, 9):
    from typing import Union

    # ByteString Behaves slightly differently in python3.8, which causes issues with the latest pop/idem.
    ByteString = Union[bytes, bytearray]
else:
    from typing import ByteString


__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    client_request_token: str = None,
    description: str = None,
    kms_key_id: str = None,
    secret_binary: ByteString = None,
    secret_string: str = None,
    tags: Dict[str, str] = None,
    add_replica_regions: List[
        make_dataclass(
            "ReplicaRegionType",
            [
                ("Region", str, field(default=None)),
                ("KmsKeyId", str, field(default=None)),
            ],
        )
    ] = None,
    force_overwrite_replica_secret: bool = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """
    Creates a new secret. A secret can be a password, a set of credentials such as a user name and password, an
    OAuth token, or other secret information that you store in an encrypted form in Secrets Manager. The secret also
    includes the connection information to access a database or other service, which Secrets Manager doesn't
    encrypt. A secret in Secrets Manager consists of both the protected secret data and the important information
    needed to manage the secret. For secrets that use managed rotation, you need to create the secret through the
    managing service. For more information, see Secrets Manager secrets managed by other Amazon Web Services
    services.  For information about creating a secret in the console, see Create a secret. To create a secret, you
    can provide the secret value to be encrypted in either the SecretString parameter or the SecretBinary parameter,
    but not both. If you include SecretString or SecretBinary then Secrets Manager creates an initial secret version
    and automatically attaches the staging label AWSCURRENT to it. For database credentials you want to rotate, for
    Secrets Manager to be able to rotate the secret, you must make sure the JSON you store in the SecretString
    matches the JSON structure of a database secret. If you don't specify an KMS encryption key, Secrets Manager
    uses the Amazon Web Services managed key aws/secretsmanager. If this key doesn't already exist in your account,
    then Secrets Manager creates it for you automatically. All users and roles in the Amazon Web Services account
    automatically have access to use aws/secretsmanager. Creating aws/secretsmanager can result in a one-time
    significant delay in returning the result. If the secret is in a different Amazon Web Services account from the
    credentials calling the API, then you can't use aws/secretsmanager to encrypt the secret, and you must create
    and use a customer managed KMS key.  Secrets Manager generates a CloudTrail log entry when you call this action.
    Do not include sensitive information in request parameters except SecretBinary or SecretString because it might
    be logged. For more information, see Logging Secrets Manager events with CloudTrail.  Required permissions:
    secretsmanager:CreateSecret. If you include tags in the secret, you also need secretsmanager:TagResource. For
    more information, see  IAM policy actions for Secrets Manager and Authentication and access control in Secrets
    Manager.  To encrypt the secret with a KMS key other than aws/secretsmanager, you need kms:GenerateDataKey and
    kms:Decrypt permission to the key.

    Args:
        name(str): Idem name of the resource.

        client_request_token(str, Optional): If you include SecretString or SecretBinary, then Secrets Manager creates an initial version for
            the secret, and this parameter specifies the unique identifier for the new version.   If you use
            the Amazon Web Services CLI or one of the Amazon Web Services SDKs to call this operation, then
            you can leave this parameter empty. The CLI or SDK generates a random UUID for you and includes
            it as the value for this parameter in the request. If you don't use the SDK and instead generate
            a raw HTTP request to the Secrets Manager service endpoint, then you must generate a
            ClientRequestToken yourself for the new version and include the value in the request.  This
            value helps ensure idempotency. Secrets Manager uses this value to prevent the accidental
            creation of duplicate versions if there are failures and retries during a rotation. We recommend
            that you generate a UUID-type value to ensure uniqueness of your versions within the specified
            secret.    If the ClientRequestToken value isn't already associated with a version of the secret
            then a new version of the secret is created.    If a version with this value already exists and
            the version SecretString and SecretBinary values are the same as those in the request, then the
            request is ignored.   If a version with this value already exists and that version's
            SecretString and SecretBinary values are different from those in the request, then the request
            fails because you cannot modify an existing version. Instead, use PutSecretValue to create a new
            version.   This value becomes the VersionId of the new version. Defaults to None.

        description(str, Optional): The description of the secret. Defaults to None.

        kms_key_id(str, Optional): The ARN, key ID, or alias of the KMS key that Secrets Manager uses to encrypt the secret value
            in the secret. An alias is always prefixed by alias/, for example alias/aws/secretsmanager. For
            more information, see About aliases. To use a KMS key in a different account, use the key ARN or
            the alias ARN. If you don't specify this value, then Secrets Manager uses the key
            aws/secretsmanager. If that key doesn't yet exist, then Secrets Manager creates it for you
            automatically the first time it encrypts the secret value. If the secret is in a different
            Amazon Web Services account from the credentials calling the API, then you can't use
            aws/secretsmanager to encrypt the secret, and you must create and use a customer managed KMS
            key. Defaults to None.

        secret_binary(ByteString, Optional): The binary data to encrypt and store in the new version of the secret. We recommend that you
            store your binary data in a file and then pass the contents of the file as a parameter. Either
            SecretString or SecretBinary must have a value, but not both. This parameter is not available in
            the Secrets Manager console. Defaults to None.

        secret_string(str, Optional): The text data to encrypt and store in this new version of the secret. We recommend you use a
            JSON structure of key/value pairs for your secret value. Either SecretString or SecretBinary
            must have a value, but not both. If you create a secret by using the Secrets Manager console
            then Secrets Manager puts the protected secret text in only the SecretString parameter. The
            Secrets Manager console stores the information as a JSON structure of key/value pairs that a
            Lambda rotation function can parse. Defaults to None.

        tags(Dict[str, str], Optional): The tags to apply to the resource. Defaults to None.

        add_replica_regions(List[dict[str, Any]], Optional): A list of Regions and KMS keys to replicate secrets. Defaults to None.

            * Region (str, Optional): A Region code. For a list of Region codes, see Name and code of Regions.

            * KmsKeyId (str, Optional): The ARN, key ID, or alias of the KMS key to encrypt the secret. If you don't include this field,
            Secrets Manager uses aws/secretsmanager.

        force_overwrite_replica_secret(bool, Optional): Specifies whether to overwrite a secret with the same name in the destination Region. By
            default, secrets aren't overwritten. Defaults to None.

        resource_id(str, Optional): Secret unique ID. Defaults to None.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls


          idem_test_aws_auto.secretsmanager.secret_is_present:
              aws_auto.aws_auto.secretsmanager.secret.present:
              - client_request_token: string
              - description: string
              - kms_key_id: string
              - secret_binary: ByteString
              - secret_string: string
              - tags:
                - key: string
                  value: string
              - add_replica_regions:
                - kms_key_id: string
                  region: string
              - force_overwrite_replica_secret: bool


    """

    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "kwargs", "result") and v is not None
    }

    current_state = None

    if resource_id:
        before = await hub.exec.aws.secretsmanager.secret.get(
            ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = current_state = copy.deepcopy(before["ret"])
        result["comment"] += hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.secretsmanager.secret", name=name
        )

    if current_state:
        changes = differ.deep_diff(
            current_state if current_state else {}, desired_state
        )
        if bool(changes.get("new")):
            if ctx.test:
                result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                    enforced_state={}, desired_state=desired_state
                )
                result["comment"] += hub.tool.aws.comment_utils.update_comment(
                    resource_type="aws.secretsmanager.secret", name=name
                )
                return result
            else:
                # Update the resource
                update_ret = await hub.exec.aws.secretsmanager.secret.update(
                    ctx, **desired_state, current_tags=current_state.get("tags", None)
                )
                result["result"] = update_ret["result"]

                if result["result"]:
                    result["comment"] += hub.tool.aws.comment_utils.update_comment(
                        resource_type="aws.secretsmanager.secret", name=name
                    )
                else:
                    result["comment"] += update_ret["comment"]
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={}, desired_state=desired_state
            )
            result["comment"] += hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.secretsmanager.secret", name=name
            )
            return result

        create_ret = await hub.exec.aws.secretsmanager.secret.create(
            ctx,
            **desired_state,
        )
        result["result"] = create_ret["result"]

        if result["result"]:
            result["comment"] = hub.tool.aws.comment_utils.create_comment(
                resource_type="aws.secretsmanager.secret", name=name
            )
            resource_id = create_ret["ret"].get("resource_id")
            # Safeguard for any future errors so that the resource_id is saved in the ESM
            result["new_state"] = dict(name=name, resource_id=resource_id)
        else:
            result["comment"].append(create_ret["comment"])

    if not result["result"]:
        # If there is any failure in create/update, it should reconcile.
        # The type of data is less important here to use default reconciliation
        # If there are no changes for 3 runs with rerun_data, then it will come out of execution
        result["rerun_data"] = dict(name=name, resource_id=resource_id)

    after = await hub.exec.aws.secretsmanager.secret.get(
        ctx, name=name, resource_id=resource_id
    )
    result["new_state"] = after.ret
    return result


async def absent(
    hub,
    ctx,
    name: str,
    recovery_window_in_days: int = None,
    force_delete_without_recovery: bool = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """

    Deletes a secret and all of its versions. You can specify a recovery window during which you can restore the
    secret. The minimum recovery window is 7 days. The default recovery window is 30 days. Secrets Manager attaches
    a DeletionDate stamp to the secret that specifies the end of the recovery window. At the end of the recovery
    window, Secrets Manager deletes the secret permanently. You can't delete a primary secret that is replicated to
    other Regions. You must first delete the replicas using RemoveRegionsFromReplication, and then delete the
    primary secret. When you delete a replica, it is deleted immediately. You can't directly delete a version of a
    secret. Instead, you remove all staging labels from the version using UpdateSecretVersionStage. This marks the
    version as deprecated, and then Secrets Manager can automatically delete the version in the background. To
    determine whether an application still uses a secret, you can create an Amazon CloudWatch alarm to alert you to
    any attempts to access a secret during the recovery window. For more information, see  Monitor secrets scheduled
    for deletion. Secrets Manager performs the permanent secret deletion at the end of the waiting period as a
    background task with low priority. There is no guarantee of a specific time after the recovery window for the
    permanent delete to occur. At any time before recovery window ends, you can use RestoreSecret to remove the
    DeletionDate and cancel the deletion of the secret. When a secret is scheduled for deletion, you cannot retrieve
    the secret value. You must first cancel the deletion with RestoreSecret and then you can retrieve the secret.
    Secrets Manager generates a CloudTrail log entry when you call this action. Do not include sensitive information
    in request parameters because it might be logged. For more information, see Logging Secrets Manager events with
    CloudTrail.  Required permissions:  secretsmanager:DeleteSecret. For more information, see  IAM policy actions
    for Secrets Manager and Authentication and access control in Secrets Manager.

    Args:

        name(str): Idem name of the resource.

        resource_id(str): The ARN or name of the secret to delete. For an ARN, we recommend that you specify a complete
            ARN rather than a partial ARN. See Finding a secret from a partial ARN.

        recovery_window_in_days(int, Optional): The number of days from 7 to 30 that Secrets Manager waits before permanently deleting the
            secret. You can't use both this parameter and ForceDeleteWithoutRecovery in the same call. If
            you don't use either, then by default Secrets Manager uses a 30 day recovery window. Defaults to None.

        force_delete_without_recovery(bool, Optional): Specifies whether to delete the secret without any recovery window. You can't use both this
            parameter and RecoveryWindowInDays in the same call. If you don't use either, then by default
            Secrets Manager uses a 30 day recovery window. Secrets Manager performs the actual deletion with
            an asynchronous background process, so there might be a short delay before the secret is
            permanently deleted. If you delete a secret and then immediately create a secret with the same
            name, use appropriate back off and retry logic. If you forcibly delete an already deleted or
            nonexistent secret, the operation does not return ResourceNotFoundException.  Use this parameter
            with caution. This parameter causes the operation to skip the normal recovery window before the
            permanent deletion that Secrets Manager would normally impose with the RecoveryWindowInDays
            parameter. If you delete a secret with the ForceDeleteWithoutRecovery parameter, then you have
            no opportunity to recover the secret. You lose the secret permanently. Defaults to None.


    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls


            idem_test_aws_auto.secretsmanager.secret_is_absent:
              aws_auto.aws_auto.secretsmanager.secret.absent:
              - secret_id: string
              - recovery_window_in_days: int
              - force_delete_without_recovery: bool


    """

    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    if not resource_id:
        resource_id = (ctx.old_state or {}).get("resource_id")

    # This is to make absent idempotent. If absent is run again, it would be a no-op
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.secretsmanager.secret", name=name
        )
        return result

    before = await hub.exec.aws.secretsmanager.secret.get(
        ctx, name=name, resource_id=resource_id
    )

    # Case: Error
    if not before["result"]:
        result["result"] = False
        result["comment"] = before["comment"]
        return result

    # Case: Not Found
    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.secretsmanager.secret", name=name
        )
        return result

    result["old_state"] = before["ret"]
    if ctx.get("test", False):
        result["comment"] += hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.secretsmanager.secret", name=name
        )
        return result

    delete_ret = await hub.exec.aws.secretsmanager.secret.delete(
        ctx,
        name=name,
        resource_id=resource_id,
        recovery_window_in_days=recovery_window_in_days,
        force_delete_without_recovery=force_delete_without_recovery,
    )
    if not delete_ret["result"]:
        if "InvalidRequestException" in str(delete_ret["comment"]):
            result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
                resource_type="aws.secretsmanager.secret", name=name
            )
            return result
        # If there is any failure in delete, it should reconcile.
        # The type of data is less important here to use default reconciliation
        # If there are no changes for 3 runs with rerun_data, then it will come out of execution
        result["result"] = delete_ret["result"]
        result["rerun_data"] = resource_id
        result["comment"].append(delete_ret["result"])
        return result

    result["comment"] += hub.tool.aws.comment_utils.delete_comment(
        resource_type="aws.secretsmanager.secret", name=name
    )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function


    Lists the secrets that are stored by Secrets Manager in the Amazon Web Services account, not including secrets
    that are marked for deletion. To see secrets marked for deletion, use the Secrets Manager console. ListSecrets
    is eventually consistent, however it might not reflect changes from the last five minutes. To get the latest
    information for a specific secret, use DescribeSecret. To list the versions of a secret, use
    ListSecretVersionIds. To get the secret value from SecretString or SecretBinary, call GetSecretValue. For
    information about finding secrets in the console, see Find secrets in Secrets Manager. Secrets Manager generates
    a CloudTrail log entry when you call this action. Do not include sensitive information in request parameters
    because it might be logged. For more information, see Logging Secrets Manager events with CloudTrail.  Required
    permissions:  secretsmanager:ListSecrets. For more information, see  IAM policy actions for Secrets Manager and
    Authentication and access control in Secrets Manager.

    Returns:
        Dict[str, Any]

    Example:

        .. code-block:: bash

            $ idem describe aws_auto.secretsmanager.secret
    """

    result = {}

    ret = await hub.exec.aws.secretsmanager.secret.list(ctx)

    if not ret or not ret["result"]:
        hub.log.warning(
            f"Could not describe aws.secretsmanager.secret {ret['comment']}"
        )
        return result

    for resource in ret["ret"]:
        resource_id = resource.get("resource_id")
        result[resource_id] = {
            "aws.secretsmanager.secret.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result
