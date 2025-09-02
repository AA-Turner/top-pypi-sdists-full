"""Exec module for managing Secretsmanager Secrets."""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import ByteString
from typing import Dict
from typing import List

__contracts__ = ["soft_fail"]

__func_alias__ = {"list_": "list"}


async def get(hub, ctx, resource_id: str, name: str = None) -> Dict[str, Any]:
    """

    Retrieves the details of a secret. It does not include the encrypted secret value. Secrets Manager only returns
    fields that have a value in the response.  Secrets Manager generates a CloudTrail log entry when you call this
    action. Do not include sensitive information in request parameters because it might be logged. For more
    information, see Logging Secrets Manager events with CloudTrail.  Required permissions:
    secretsmanager:DescribeSecret. For more information, see  IAM policy actions for Secrets Manager and
    Authentication and access control in Secrets Manager.

    Args:

        resource_id(str): The ARN of the secret.  For an ARN, we recommend that you specify a complete ARN rather
            than a partial ARN. See Finding a secret from a partial ARN.

        name(str, Optional): Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            unmanaged_resource:
              exec.run:
                - path: aws.secretsmanager.secret.get
                - kwargs:
                  resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.secretsmanager.secret.get resource_id=value
    """

    result = dict(comment=[], ret=None, result=True)

    secret_get = await hub.exec.boto3.client.secretsmanager.describe_secret(
        ctx=ctx, SecretId=resource_id
    )

    # Case: Error
    if not secret_get["result"]:
        # Do not return success=false when it is not found.
        # Most of the resources would return "*NotFound*" type of exception when it is 404
        if "ResourceNotFoundException" in str(secret_get["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.secretsmanager.secret", name=name
                )
            )
            result["comment"].append(secret_get["comment"])
            return result

        result["comment"].append(secret_get["comment"])
        result["result"] = False
        return result

    # Case: Empty results
    if not secret_get["ret"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.secretsmanager.secret", name=name
            )
        )
        return result

    raw_resource = secret_get["ret"]

    result[
        "ret"
    ] = await hub.tool.aws.secretsmanager.secret.convert_raw_resource_to_present_async(
        ctx=ctx,
        resource_id=resource_id,
        raw_resource=raw_resource,
        idem_resource_name=name,
    )

    return result


async def list_(
    hub,
    ctx,
    include_planned_deletion: bool = None,
    filters: List[
        make_dataclass(
            "Filter",
            [
                ("Key", str, field(default=None)),
                ("Values", List[str], field(default=None)),
            ],
        )
    ] = None,
    sort_order: str = None,
    name: str = None,
) -> Dict[str, Any]:
    """
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

    Args:
        include_planned_deletion(bool, Optional): Specifies whether to include secrets scheduled for deletion. By default, secrets scheduled for
            deletion aren't included. Defaults to None.

        filters(List[dict[str, Any]], Optional): The filters to apply to the list of secrets. Defaults to None.

            * Key (str, Optional): The following are keys you can use:    description: Prefix match, not case-sensitive.    name:
            Prefix match, case-sensitive.    tag-key: Prefix match, case-sensitive.    tag-value: Prefix
            match, case-sensitive.    primary-region: Prefix match, case-sensitive.    owning-service:
            Prefix match, case-sensitive.    all: Breaks the filter value string into words and then
            searches all attributes for matches. Not case-sensitive.

            * Values (List[str], Optional): The keyword to filter for. You can prefix your search value with an exclamation mark (!) in
            order to perform negation filters.

        sort_order(str, Optional): Secrets are listed by CreatedDate. Defaults to None.

        name(str, Optional): Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:

        Resource State:

        .. code-block:: sls

            unmanaged_resources:
              exec.run:
                - path: aws.secretsmanager.secret.list
                - kwargs:


        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.secretsmanager.secret.list

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe aws.secretsmanager.secret

    """

    result = dict(comment=[], ret=[], result=True)

    ret = await hub.exec.boto3.client.secretsmanager.list_secrets(
        ctx=ctx,
        IncludePlannedDeletion=include_planned_deletion,
        Filters=filters,
        SortOrder=sort_order,
    )

    if not ret["result"]:
        result["comment"].append(ret["comment"])
        result["result"] = False
        return result

    if not ret["ret"].get("SecretList"):
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.secretsmanager.secret", name=name
            )
        )
        return result

    for resource in ret["ret"]["SecretList"]:
        result["ret"].append(
            await hub.tool.aws.secretsmanager.secret.convert_raw_resource_to_present_async(
                ctx=ctx,
                resource_id=resource["ARN"],
                raw_resource=resource,
                idem_resource_name=name,
            )
        )
    return result


async def create(
    hub,
    ctx,
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
    name: str = None,
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
        client_request_token(str, Optional): If you include SecretString or SecretBinary, then Secrets Manager creates
            an initial version for the secret, and this parameter specifies the unique identifier for the new version.
            If you use the Amazon Web Services CLI or one of the Amazon Web Services SDKs to call this operation, then
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

        kms_key_id(str, Optional): The ARN, key ID, or alias of the KMS key that Secrets Manager uses to encrypt the
            secret value in the secret. An alias is always prefixed by alias/, for example alias/aws/secretsmanager. For
            more information, see About aliases. To use a KMS key in a different account, use the key ARN or
            the alias ARN. If you don't specify this value, then Secrets Manager uses the key
            aws/secretsmanager. If that key doesn't yet exist, then Secrets Manager creates it for you
            automatically the first time it encrypts the secret value. If the secret is in a different
            Amazon Web Services account from the credentials calling the API, then you can't use
            aws/secretsmanager to encrypt the secret, and you must create and use a customer managed KMS
            key. Defaults to None.

        secret_binary(ByteString, Optional): The binary data to encrypt and store in the new version of the secret.
            We recommend that you store your binary data in a file and then pass the contents of the file as a parameter.
            Either SecretString or SecretBinary must have a value, but not both. This parameter is not available in
            the Secrets Manager console. Defaults to None.

        secret_string(str, Optional): The text data to encrypt and store in this new version of the secret.
            We recommend you use a JSON structure of key/value pairs for your secret value. Either SecretString
            or SecretBinary must have a value, but not both. If you create a secret by using the Secrets Manager console
            then Secrets Manager puts the protected secret text in only the SecretString parameter. The
            Secrets Manager console stores the information as a JSON structure of key/value pairs that a
            Lambda rotation function can parse. Defaults to None.

        tags(Dist[str, str], Optional): The tags to apply to the resource.

        add_replica_regions(List[dict[str, Any]], Optional): A list of Regions and KMS keys to replicate secrets. Defaults to None.

            * Region (str, Optional): A Region code. For a list of Region codes, see Name and code of Regions.

            * KmsKeyId (str, Optional): The ARN, key ID, or alias of the KMS key to encrypt the secret. If you don't include this field,
            Secrets Manager uses aws/secretsmanager.

        force_overwrite_replica_secret(bool, Optional): Specifies whether to overwrite a secret with the same name in the destination Region. By
            default, secrets aren't overwritten. Defaults to None.

        resource_id(str, Optional): Secret unique ID. Defaults to None.

        name(str, Optional): Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              aws.secretsmanager.secret.present:
                -

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.secretsmanager.secret.create
    """

    result = dict(comment=[], ret={}, result=True)

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "kwargs", "result") and v is not None
    }

    resource_to_raw_input_mapping = {
        "client_request_token": "ClientRequestToken",
        "description": "Description",
        "kms_key_id": "KmsKeyId",
        "secret_binary": "SecretBinary",
        "secret_string": "SecretString",
        "add_replica_regions": "AddReplicaRegions",
        "force_overwrite_replica_secret": "ForceOverwriteReplicaSecret",
        "name": "Name",
    }

    payload = {}
    for key, value in desired_state.items():
        if key in resource_to_raw_input_mapping.keys() and value is not None:
            payload[resource_to_raw_input_mapping[key]] = desired_state.get(key)

    if tags:
        payload["Tags"] = hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)

    ret = await hub.exec.boto3.client.secretsmanager.create_secret(ctx, **payload)

    result["result"] = ret["result"]
    if not result["result"]:
        result["comment"].append(ret["comment"])
        return result

    result["comment"] += hub.tool.aws.comment_utils.create_comment(
        resource_type="aws.secretsmanager.secret", name=name
    )

    raw_resource = ret["ret"]
    result["ret"]["resource_id"] = raw_resource.get("ARN")
    result["ret"]["name"] = name

    return result


async def update(
    hub,
    ctx,
    resource_id: str,
    tags: Dict[str, str] = None,
    current_tags: Dict[str, str] = None,
    client_request_token: str = None,
    description: str = None,
    kms_key_id: str = None,
    secret_binary: ByteString = None,
    secret_string: str = None,
    name: str = None,
) -> Dict[str, Any]:
    """
    Modifies the details of a secret, including metadata and the secret value. To change the secret value, you can
    also use PutSecretValue. To change the rotation configuration of a secret, use RotateSecret instead. To change a
    secret so that it is managed by another service, you need to recreate the secret in that service. See Secrets
    Manager secrets managed by other Amazon Web Services services. We recommend you avoid calling UpdateSecret at a
    sustained rate of more than once every 10 minutes. When you call UpdateSecret to update the secret value,
    Secrets Manager creates a new version of the secret. Secrets Manager removes outdated versions when there are
    more than 100, but it does not remove versions created less than 24 hours ago. If you update the secret value
    more than once every 10 minutes, you create more versions than Secrets Manager removes, and you will reach the
    quota for secret versions. If you include SecretString or SecretBinary to create a new secret version, Secrets
    Manager automatically moves the staging label AWSCURRENT to the new version. Then it attaches the label
    AWSPREVIOUS to the version that AWSCURRENT was removed from. If you call this operation with a
    ClientRequestToken that matches an existing version's VersionId, the operation results in an error. You can't
    modify an existing version, you can only create a new version. To remove a version, remove all staging labels
    from it. See UpdateSecretVersionStage. Secrets Manager generates a CloudTrail log entry when you call this
    action. Do not include sensitive information in request parameters except SecretBinary or SecretString because
    it might be logged. For more information, see Logging Secrets Manager events with CloudTrail.  Required
    permissions:  secretsmanager:UpdateSecret. For more information, see  IAM policy actions for Secrets Manager and
    Authentication and access control in Secrets Manager. If you use a customer managed key, you must also have
    kms:GenerateDataKey and kms:Decrypt permissions on the key. For more information, see  Secret encryption and
    decryption.

    Args:

        resource_id(str): The ARN of the secret.  For an ARN, we recommend that you specify a complete ARN rather
            than a partial ARN. See Finding a secret from a partial ARN.

        tags(Dict[str, str], Optional): The tags to apply to the resource. Defaults to None.

        current_tags(Dict[str, str], Optional): Existing tags of the resource

        client_request_token(str, Optional): If you include SecretString or SecretBinary, then Secrets Manager creates a new version for the
            secret, and this parameter specifies the unique identifier for the new version.  If you use the
            Amazon Web Services CLI or one of the Amazon Web Services SDKs to call this operation, then you
            can leave this parameter empty. The CLI or SDK generates a random UUID for you and includes it
            as the value for this parameter in the request. If you don't use the SDK and instead generate a
            raw HTTP request to the Secrets Manager service endpoint, then you must generate a
            ClientRequestToken yourself for the new version and include the value in the request.  This
            value becomes the VersionId of the new version. Defaults to None.

        description(str, Optional): The description of the secret. Defaults to None.

        kms_key_id(str, Optional): The ARN, key ID, or alias of the KMS key that Secrets Manager uses to encrypt new secret
            versions as well as any existing versions with the staging labels AWSCURRENT, AWSPENDING, or
            AWSPREVIOUS. For more information about versions and staging labels, see Concepts: Version. A
            key alias is always prefixed by alias/, for example alias/aws/secretsmanager. For more
            information, see About aliases. If you set this to an empty string, Secrets Manager uses the
            Amazon Web Services managed key aws/secretsmanager. If this key doesn't already exist in your
            account, then Secrets Manager creates it for you automatically. All users and roles in the
            Amazon Web Services account automatically have access to use aws/secretsmanager. Creating
            aws/secretsmanager can result in a one-time significant delay in returning the result.   You can
            only use the Amazon Web Services managed key aws/secretsmanager if you call this operation using
            credentials from the same Amazon Web Services account that owns the secret. If the secret is in
            a different account, then you must use a customer managed key and provide the ARN of that KMS
            key in this field. The user making the call must have permissions to both the secret and the KMS
            key in their respective accounts. Defaults to None.

        secret_binary(ByteString, Optional): The binary data to encrypt and store in the new version of the secret. We recommend that you
            store your binary data in a file and then pass the contents of the file as a parameter.  Either
            SecretBinary or SecretString must have a value, but not both. You can't access this parameter in
            the Secrets Manager console. Defaults to None.

        secret_string(str, Optional): The text data to encrypt and store in the new version of the secret. We recommend you use a JSON
            structure of key/value pairs for your secret value.  Either SecretBinary or SecretString must
            have a value, but not both. Defaults to None.

        name(str, Optional): Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              aws.secretsmanager.secret.present:
                - secret_id: value
                - tags: value
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.secretsmanager.secret.update tags=value, resource_id=value
    """

    result = dict(comment=[], ret={}, result=True)

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "kwargs", "result") and v is not None
    }

    payload = {}

    resource_to_raw_input_mapping = {
        "resource_id": "SecretId",
        "client_request_token": "ClientRequestToken",
        "description": "Description",
        "kms_key_id": "KmsKeyId",
        "secret_binary": "SecretBinary",
        "secret_string": "SecretString",
    }

    for key, value in desired_state.items():
        if key in resource_to_raw_input_mapping.keys() and value is not None:
            payload[resource_to_raw_input_mapping[key]] = desired_state.get(key)

    if payload:
        ret = await hub.exec.boto3.client.secretsmanager.update_secret(ctx, **payload)
        if not ret["result"]:
            result["result"] = False
            result["comment"].append(
                f"Could not update aws.secretsmanager.secret '{name}'",
            )
            result["comment"].append(ret["comment"])
            return result

        result["comment"] += hub.tool.aws.comment_utils.update_comment(
            resource_type="aws.secretsmanager.secret", name=name
        )

        update_tags_ret = await hub.tool.aws.secretsmanager.tag.update_tags(
            ctx, resource_id=resource_id, old_tags=current_tags, new_tags=tags
        )
        if not update_tags_ret["result"]:
            result["result"] = False
            result["comment"] += update_tags_ret["comment"]
            return result

        result["ret"]["resource_id"] = resource_id
        result["ret"]["name"] = name
    return result


async def delete(
    hub,
    ctx,
    resource_id: str,
    recovery_window_in_days: int = None,
    force_delete_without_recovery: bool = None,
    name: str = None,
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

        name(str, Optional): Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            resource_is_absent:
              aws.secretsmanager.secret.absent:
                - secret_id: value
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.secretsmanager.secret.delete secret_id=value, resource_id=value
    """

    result = dict(comment=[], ret=None, result=True)
    delete_ret = await hub.exec.boto3.client.secretsmanager.delete_secret(
        ctx,
        **{
            "SecretId": resource_id,
            "RecoveryWindowInDays": recovery_window_in_days,
            "ForceDeleteWithoutRecovery": force_delete_without_recovery,
        },
    )

    result["result"] = delete_ret["result"]

    if not result["result"]:
        result["comment"] = delete_ret["comment"]
        result["result"] = False
        return result

    result["comment"] += hub.tool.aws.comment_utils.delete_comment(
        resource_type="aws.secretsmanager.secret", name=name
    )

    return result
