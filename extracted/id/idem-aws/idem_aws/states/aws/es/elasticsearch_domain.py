"""State module for managing Amazon Elasticsearch Service Domain"""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    domain_name: str,
    elastic_search_version: str,
    perform_check_only: bool = None,
    elastic_search_cluster_config: make_dataclass(
        """Configuration to specify the instance type and number of instances in the domain cluster."""
        "ElasticsearchClusterConfig",
        [
            ("InstanceType", str, field(default=None)),
            ("InstanceCount", str, field(default=None)),
            ("DedicatedMasterEnabled", bool, field(default=None)),
            ("ZoneAwarenessEnabled", bool, field(default=None)),
            (
                "ZoneAwarenessConfig",
                make_dataclass(
                    "ZoneAwarenessConfig",
                    [("AvailabilityZoneCount", int, field(default=None))],
                ),
                field(default=None),
            ),
            ("DedicatedMasterType", str, field(default=None)),
            ("DedicatedMasterCount", int, field(default=None)),
            ("WarmEnabled", bool, field(default=None)),
            ("WarmType", str, field(default=None)),
            ("WarmCount", int, field(default=None)),
            (
                "ColdStorageOptions",
                make_dataclass(
                    "ColdStorageOptions",
                    [("Enabled", bool)],
                ),
                field(default=None),
            ),
            ("OnFailure", Dict, field(default=None)),
        ],
    ) = None,
    ebs_options: make_dataclass(
        """Options to enable, disable and specify the type and size of EBS storage volumes."""
        "EBSOptions",
        [
            ("EBSEnabled", bool, field(default=None)),
            ("VolumeType", str, field(default=None)),
            ("VolumeSize", int, field(default=None)),
            ("Iops", int, field(default=None)),
            ("Throughput", int, field(default=None)),
        ],
    ) = None,
    access_policies: str = None,
    snapshot_options: make_dataclass(
        """Option to set time, in UTC format, of the daily automated snapshot. Default value is 0 hours."""
        "SnapshotOptions",
        [
            ("AutomatedSnapshotStartHour", int, field(default=None)),
        ],
    ) = None,
    vpc_options: make_dataclass(
        """Options to specify the subnets and security groups for VPC endpoint"""
        "VPCOptions",
        [
            ("SubnetIds", List[str], field(default=None)),
            ("SecurityGroupIds", List[str], field(default=None)),
        ],
    ) = None,
    cognito_options: make_dataclass(
        """Options to specify the Cognito user and identity pools for Kibana authentication."""
        "CognitoOptions",
        [
            ("Enabled", bool, field(default=None)),
            ("UserPoolId", str, field(default=None)),
            ("IdentityPoolId", str, field(default=None)),
            ("RoleArn", str, field(default=None)),
        ],
    ) = None,
    encryption_at_rest_options: make_dataclass(
        """Encryption At Rest Options.""" "EncryptionAtRestOptions",
        [
            ("Enabled", bool, field(default=None)),
            ("KmsKeyId", str, field(default=None)),
        ],
    ) = None,
    node_to_node_encryption_options: make_dataclass(
        """Specifies the NodeToNodeEncryptionOptions.""" "NodeToNodeEncryptionOptions",
        [
            ("Enabled", bool, field(default=None)),
        ],
    ) = None,
    advanced_options: Dict[str, str] = None,
    log_publishing_options: Dict[str, Any] = None,
    domain_endpoint_options: make_dataclass(
        """Options to specify configuration that will be applied to the domain endpoint."""
        "DomainEndpointOptions",
        [
            ("EnforceHTTPS", bool, field(default=None)),
            ("TLSSecurityPolicy", str, field(default=None)),
            ("CustomEndpointEnabled", bool, field(default=None)),
            ("CustomEndpoint", str, field(default=None)),
            ("CustomEndpointCertificateArn", str, field(default=None)),
        ],
    ) = None,
    advanced_security_options: make_dataclass(
        """Specify advanced security options.""" "AdvancedSecurityOptions",
        [
            ("Enabled", bool, field(default=None)),
            ("InternalUserDatabaseEnabled", bool, field(default=None)),
            (
                "MasterUserOptions",
                make_dataclass(
                    "MasterUserOptions",
                    [
                        ("MasterUserARN", str, field(default=None)),
                        ("MasterUserName", str, field(default=None)),
                        ("MasterUserPassword", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "SAMLOptions",
                make_dataclass(
                    "SAMLOptions",
                    [
                        ("Enabled", bool, field(default=None)),
                        (
                            "Idp",
                            make_dataclass(
                                "Idp",
                                [
                                    ("MetadataContent", str),
                                    ("EntityId", str),
                                ],
                            ),
                            field(default=None),
                        ),
                        ("MasterUserName", str, field(default=None)),
                        ("MasterBackendRole", str, field(default=None)),
                        ("SubjectKey", str, field(default=None)),
                        ("RolesKey", str, field(default=None)),
                        ("SessionTimeoutMinutes", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("AnonymousAuthEnabled", bool, field(default=None)),
        ],
    ) = None,
    auto_tune_options: make_dataclass(
        """Specifies Auto-Tune options.""" "AutoTuneOptions",
        [
            ("DesiredState", str, field(default=None)),
            (
                "MaintenanceSchedules",
                List[
                    make_dataclass(
                        "MaintenanceSchedules",
                        [
                            ("StartAt", str, field(default=None)),
                            (
                                "Duration",
                                make_dataclass(
                                    "Duration",
                                    [
                                        ("Value", int, field(default=None)),
                                        ("Unit", str, field(default=None)),
                                    ],
                                ),
                                field(default=None),
                            ),
                            ("CronExpressionForRecurrence", str, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
            ("RollbackOnDisable", str, field(default=None)),
        ],
    ) = None,
    dry_run: bool = None,
    tags: Dict[str, str] = None,
    timeout: make_dataclass(
        "Timeout",
        [
            (
                "create",
                make_dataclass(
                    "CreateTimeout",
                    [
                        ("delay", int, field(default=30)),
                        ("max_attempts", int, field(default=60)),
                    ],
                ),
                field(default=None),
            ),
            (
                "update",
                make_dataclass(
                    "UpdateTimeout",
                    [
                        ("delay", int, field(default=30)),
                        ("max_attempts", int, field(default=60)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Creates a new Elasticsearch domain.

    Args:
        name(str): An Idem name of the resource.
        domain_name(str):
            The name of the Elasticsearch domain that you are creating. Domain names are unique across the domains owned
            by an account within an AWS region. Domain names must start with a lowercase letter and can contain the
            following characters: a-z (lowercase), 0-9, and - (hyphen).
        elastic_search_version(str):
            String of format X.Y to specify version for the Elasticsearch domain
            eg. "1.5" or "2.3".
        perform_check_only(bool):
            This flag, when set to True, indicates that an Upgrade Eligibility Check needs to be performed. This will not actually perform the Upgrade.

                .. note::
                    This property can only be applied when `elastic_search_version` is upgraded
        elastic_search_cluster_config(dict, Optional):
            Configuration options for an Elasticsearch domain. Specifies the instance type and number of instances in the domain cluster.
                * InstanceType(str, Optional): The instance type for an Elasticsearch cluster. UltraWarm instance types are not supported for data instances.
                * InstanceCount(int, Optional): The number of instances in the specified domain cluster.
                * DedicatedMasterEnabled(bool, Optional): A boolean value to indicate whether a dedicated master node is enabled.
                * ZoneAwarenessEnabled(bool, Optional): A boolean value to indicate whether zone awareness is enabled.
                * ZoneAwarenessConfig(dict, Optional):
                    Specifies the zone awareness configuration for a domain when zone awareness is enabled.
                        * AvailabilityZoneCount(int, Optional): An integer value to indicate the number of availability zones for a domain when zone awareness is enabled. This should be equal to number of subnets if VPC endpoints is enabled
                * DedicatedMasterType(str, Optional): The instance type for a dedicated master node.
                * DedicatedMasterCount(int, Optional): Total number of dedicated master nodes, active and on standby, for the cluster.
                * WarmEnabled(bool, Optional): True to enable warm storage.
                * WarmType(str, Optional): The instance type for the Elasticsearch cluster's warm nodes.
                * WarmCount(int, Optional): The number of warm nodes in the cluster.
                * ColdStorageOptions(dict, Optional):
                    Specifies the ColdStorageOptions config for Elasticsearch Domain
                        * Enabled(bool): Enable cold storage option. Accepted values true or false
        ebs_options(dict, Optional):
            Options to enable, disable and specify the type and size of EBS storage volumes.
                * EBSEnabled(bool, Optional): Specifies whether EBS-based storage is enabled.
                * VolumeType(str, Optional): Specifies the volume type for EBS-based storage.
                * VolumeSize(int, Optional): Integer to specify the size of an EBS volume.
                * Iops(int, Optional): Specifies the IOPS for Provisioned IOPS And GP3 EBS volume (SSD).
                * Throughput(int, Optional): Specifies the Throughput for GP3 EBS volume (SSD).
        access_policies(str, Optional): IAM access policy as a JSON-formatted string.
        snapshot_options(dict, Optional):
            Option to set time, in UTC format, of the daily automated snapshot. Default value is 0 hours.
                * AutomatedSnapshotStartHour(int, Optional): Specifies the time, in UTC format, when the service takes a daily automated snapshot of the specified Elasticsearch domain. Default value is 0 hours.
        vpc_options(dict, Optional):
            Options to specify the subnets and security groups for VPC endpoint.
                * SubnetIds (list[str], Optional): Specifies the subnets for VPC endpoint.
                * SecurityGroupIds (list[str], Optional): Specifies the security groups for VPC endpoint.
        cognito_options(dict, Optional):
            Options to specify the Cognito user and identity pools for Kibana authentication.
                * Enabled(bool, Optional): Specifies the option to enable Cognito for Kibana authentication.
                * UserPoolId(str, Optional): Specifies the Cognito user pool ID for Kibana authentication.
                * IdentityPoolId(str, Optional): Specifies the Cognito identity pool ID for Kibana authentication.
                * RoleArn(str, Optional): Specifies the role ARN that provides Elasticsearch permissions for accessing Cognito resources.
        encryption_at_rest_options(dict, Optional):
            Specifies the Encryption At Rest Options.
                * Enabled(bool, Optional): Specifies the option to enable Encryption At Rest.
                * KmsKeyId(str, Optional): Specifies the KMS Key ID for Encryption At Rest options.
        node_to_node_encryption_options(dict, Optional):
            Specifies the NodeToNodeEncryptionOptions.
                * Enabled(bool, Optional): Specify true to enable node-to-node encryption.
        advanced_options(dict, Optional): Option to allow references to indices in an HTTP request body. Must be false when configuring access to individual sub-resources. By default, the value is true.
        log_publishing_options(dict, Optional):
            Map of LogType and LogPublishingOption , each containing options to publish a given type of Elasticsearch log.
            Type of Log File, it can be one of the following:
            * INDEX_SLOW_LOGS: Index slow logs contain insert requests that took more time than configured index query log threshold to execute.
            * SEARCH_SLOW_LOGS: Search slow logs contain search queries that took more time than configured search query log threshold to execute.
            * ES_APPLICATION_LOGS: Elasticsearch application logs contain information about errors and warnings raised during the operation of the service and can be useful for troubleshooting.
            * AUDIT_LOGS: Audit logs contain records of user requests for access from the domain.
            Log Publishing option that is set for given domain. Attributes and their details:
            * CloudWatchLogsLogGroupArn: ARN of the Cloudwatch log group to which log needs to be published.
            * Enabled: Specifies whether given log publishing option is enabled or not.
        domain_endpoint_options(dict, Optional):
            Options to specify configuration that will be applied to the domain endpoint.
                * EnforceHTTPS(bool, Optional): Specify if only HTTPS endpoint should be enabled for the Elasticsearch domain.
                * TLSSecurityPolicy(str, Optional):
                    Specify the TLS security policy that needs to be applied to the HTTPS endpoint of Elasticsearch domain. It can be one of the following values:
                        Policy-Min-TLS-1-0-2019-07: TLS security policy which supports TLSv1.0 and higher.
                        Policy-Min-TLS-1-2-2019-07: TLS security policy which supports only TLSv1.2
                * CustomEndpointEnabled(bool, Optional): Specify if custom endpoint should be enabled for the Elasticsearch domain.
                * CustomEndpoint(str, Optional): Specify the fully qualified domain for your custom endpoint.
                * CustomEndpointCertificateArn(str, Optional): Specify ACM certificate ARN for your custom endpoint..
        advanced_security_options(dict, Optional):
            Specifies advanced security options.
                * Enabled(bool, Optional): True if advanced security is enabled.
                * InternalUserDatabaseEnabled(bool, Optional): True if the internal user database is enabled.
                * MasterUserOptions(dict, Optional):
                    Credentials for the master user: username and password, ARN, or both.
                        * MasterUserARN(str, Optional): ARN for the master user (if IAM is enabled).
                        * MasterUserName(str, Optional): The master user's username, which is stored in the Amazon Elasticsearch Service domain's internal database.
                        * MasterUserPassword(str, Optional): The master user's password, which is stored in the Amazon Elasticsearch Service domain's internal database.
                * SAMLOptions(dict, Optional):
                    Specifies the SAML application configuration for the domain.
                        * Enabled(bool, Optional): True if SAML is enabled.
                        * Idp(dict, Optional):
                            Specifies the SAML Identity Provider's information.
                                * MetadataContent(str): The Metadata of the SAML application in xml format.
                                * EntityId(str): The unique Entity ID of the application in SAML Identity Provider.
                        * MasterUserName(str, Optional): The SAML master username, which is stored in the Amazon Elasticsearch Service domain's internal database.
                        * MasterBackendRole(str, Optional): The backend role to which the SAML master user is mapped to.
                        * SubjectKey(str, Optional): The key to use for matching the SAML Subject attribute.
                        * MasterUserName(str, Optional): The SAML master username, which is stored in the Amazon Elasticsearch Service domain's internal database.
                        * MasterBackendRole(str, Optional): The backend role to which the SAML master user is mapped to.
                        * SubjectKey(str, Optional): The key to use for matching the SAML Subject attribute.
                        * RolesKey(str, Optional): The key to use for matching the SAML Roles attribute
                        * SessionTimeoutMinutes(int, Optional): The duration, in minutes, after which a user session becomes inactive. Acceptable values are between 1 and 1440, and the default value is 60.
                * AnonymousAuthEnabled(bool, Optional): True if Anonymous auth is enabled. Anonymous auth can be enabled only when AdvancedSecurity is enabled on existing domains.
        auto_tune_options(dict, Optional):
            Specifies Auto-Tune options.
                * DesiredState(str, Optional): Specifies the Auto-Tune desired state. Valid values are ENABLED, DISABLED.
                * RollbackOnDisable(str, Optional):
                    Specifies the rollback state while disabling Auto-Tune for the domain. Valid values are NO_ROLLBACK, DEFAULT_ROLLBACK.

                    .. note::
                        This property is only applied on Update of the resource
                * MaintenanceSchedules(list[dict[str, Any]], Optional):
                    Specifies list of maintenance schedules.
                        * StartAt(datetime, Optional): Specifies timestamp at which Auto-Tune maintenance schedule start.
                        * Duration(dict, Optional):
                            Specifies maintenance schedule duration: duration value and duration unit.
                                * Value(int, Optional): Integer to specify the value of a maintenance schedule duration.
                                * Unit(str, Optional): Specifies the unit of a maintenance schedule duration. Valid value is HOURS.
                        * CronExpressionForRecurrence(str, Optional): Specifies cron expression for a recurring maintenance schedule.
        dry_run(bool, Optional):
            This flag, when set to True, specifies whether the update request should return the results of validation checks without actually applying the change. This will not actually perform the Update.

            .. note::
                This property is only applied on Update of the resource
        tags(dict, Optional):
            Dict in the format of {tag-key: tag-value} Tag keys must be unique for the Elasticsearch domain to which they are attached.
            Tag values can be null and do not have to be unique in a tag set. For example, you can have a key value pair in a tag set of ``project : Trinity`` and ``cost-center : Trinity``
            Defaults to None.
        timeout(dict, Optional):
            Timeout configuration for create/update of AWS Elasticsearch domain
                * create(dict, Optional):
                    Timeout configuration for creating AWS Elasticsearch domain
                        * delay(int, Optional): The amount of time in seconds to wait between attempts. Default value is ``30``.
                        * max_attempts(int, Optional): Customized timeout configuration containing delay and max attempts. Default value is ``60``.
                * update(dict, Optional):
                    Timeout configuration for updating AWS Elasticsearch domain
                        * delay(int, Optional): The amount of time in seconds to wait between attempts. Default value is ``30``.
                        * max_attempts(int, Optional): Customized timeout configuration containing delay and max attempts. Default value is ``60``.
        resource_id(str, Optional): The name of the Elasticsearch domain. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:

         .. code-block:: sls

             resource_is_present:
                  aws.es.elasticsearch_domain.present:
                    - name: value
                    - domain_name: value
                    - elastic_search_version: value

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    tags_updated = False

    if resource_id:
        before = await hub.exec.aws.es.elasticsearch_domain.get(
            ctx, name=name, resource_id=resource_id
        )
        if not (before["result"] and before["ret"]):
            result["comment"] = list(before["comment"])
            result["result"] = False
            return result
        result["old_state"] = copy.deepcopy(before["ret"])
        result["new_state"] = copy.deepcopy(result["old_state"])
        desired_resource_parameters = {
            "domain_name": domain_name,
            "elastic_search_version": elastic_search_version,
            "perform_check_only": perform_check_only,
            "elastic_search_cluster_config": elastic_search_cluster_config,
            "ebs_options": ebs_options,
            "access_policies": access_policies,
            "snapshot_options": snapshot_options,
            "vpc_options": vpc_options,
            "cognito_options": cognito_options,
            "encryption_at_rest_options": encryption_at_rest_options,
            "node_to_node_encryption_options": node_to_node_encryption_options,
            "advanced_options": advanced_options,
            "log_publishing_options": log_publishing_options,
            "domain_endpoint_options": domain_endpoint_options,
            "advanced_security_options": advanced_security_options,
            "auto_tune_options": auto_tune_options,
            "dry_run": dry_run,
        }
        update_elasticsearch_domain_ret = (
            await hub.tool.aws.es.elasticsearch_domain.update_elasticsearch_domain(
                ctx,
                resource_id=resource_id,
                current_state=result["old_state"],
                desired_state=desired_resource_parameters,
                timeout=timeout,
            )
        )
        if not update_elasticsearch_domain_ret["result"]:
            result["result"] = False
            result["comment"] = list(update_elasticsearch_domain_ret["comment"])
            return result
        result["comment"] = list(update_elasticsearch_domain_ret["comment"])

        resource_updated = bool(update_elasticsearch_domain_ret["ret"])

        if tags is not None and tags != result["old_state"].get("tags"):
            # Update tags
            update_tags = await hub.tool.aws.es.tag.update(
                ctx=ctx,
                resource_id=resource_id,
                old_tags=result["old_state"].get("tags"),
                new_tags=tags,
            )
            result["comment"] += list(update_tags["comment"])
            result["result"] = update_tags["result"]
            if update_tags["ret"] is not None:
                tags_updated = True

        if ctx.get("test", False):
            if resource_updated:
                result["new_state"].update(update_elasticsearch_domain_ret["ret"])
            if tags_updated:
                result["new_state"].update({"tags": update_tags["ret"]})
            return result

    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "domain_name": domain_name,
                    "elastic_search_version": elastic_search_version,
                    "elastic_search_cluster_config": elastic_search_cluster_config,
                    "ebs_options": ebs_options,
                    "access_policies": access_policies,
                    "snapshot_options": snapshot_options,
                    "vpc_options": vpc_options,
                    "cognito_options": cognito_options,
                    "encryption_at_rest_options": encryption_at_rest_options,
                    "node_to_node_encryption_options": node_to_node_encryption_options,
                    "advanced_options": advanced_options,
                    "log_publishing_options": log_publishing_options,
                    "domain_endpoint_options": domain_endpoint_options,
                    "advanced_security_options": advanced_security_options,
                    "auto_tune_options": auto_tune_options,
                    "tags": tags,
                },
            )
            result["comment"] = list(
                hub.tool.aws.comment_utils.would_create_comment(
                    resource_type="aws.es.elasticsearch_domain", name=name
                )
            )
            return result

        create_ret = await hub.exec.boto3.client.es.create_elasticsearch_domain(
            ctx,
            DomainName=domain_name,
            ElasticsearchVersion=elastic_search_version,
            ElasticsearchClusterConfig=elastic_search_cluster_config,
            EBSOptions=ebs_options,
            AccessPolicies=access_policies,
            SnapshotOptions=snapshot_options,
            VPCOptions=vpc_options,
            CognitoOptions=cognito_options,
            EncryptionAtRestOptions=encryption_at_rest_options,
            NodeToNodeEncryptionOptions=node_to_node_encryption_options,
            AdvancedOptions=advanced_options,
            LogPublishingOptions=log_publishing_options,
            DomainEndpointOptions=domain_endpoint_options,
            AdvancedSecurityOptions=advanced_security_options,
            AutoTuneOptions=auto_tune_options,
            TagList=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags=tags),
        )
        result["result"] = create_ret["result"]
        if not result["result"]:
            result["comment"] = list(create_ret["comment"])
            return result
        result["comment"] = list(
            hub.tool.aws.comment_utils.create_comment(
                resource_type="aws.es.elasticsearch_domain", name=name
            )
        )
        elasticsearch_domain = create_ret["ret"].get("DomainStatus")
        resource_id = elasticsearch_domain.get("DomainName")

        create_waiter_acceptors = [
            {
                "matcher": "path",
                "expected": True,
                "state": "success",
                "argument": "DomainStatus.Created",
            },
            {
                "matcher": "path",
                "expected": False,
                "state": "retry",
                "argument": "DomainStatus.Created",
            },
        ]

        waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
            default_delay=30,
            default_max_attempts=60,
            timeout_config=timeout.get("create") if timeout else None,
        )

        create_domain_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
            name="ElasticsearchDomainCreate",
            operation="DescribeElasticsearchDomain",
            argument=["DomainStatus.Created"],
            acceptors=create_waiter_acceptors,
            client=await hub.tool.boto3.client.get_client(ctx, "es"),
        )
        try:
            await hub.tool.boto3.client.wait(
                ctx,
                "es",
                "ElasticsearchDomainCreate",
                create_domain_waiter,
                DomainName=resource_id,
                WaiterConfig=waiter_config,
            )
        except Exception as e:
            result["comment"] += [str(e)]
            result["result"] = False
            return result

    if (not before) or resource_updated or tags_updated:
        after = await hub.exec.aws.es.elasticsearch_domain.get(
            ctx, name=name, resource_id=resource_id
        )
        if not (after["result"] and after["ret"]):
            result["result"] = False
            result["comment"] += list(after["comment"])
            return result
        result["new_state"] = copy.deepcopy(after["ret"])

    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    timeout: make_dataclass(
        """Specifies timeout for deletion of domain.""" "Timeout",
        [
            (
                "delete",
                make_dataclass(
                    "DeleteTimeout",
                    [
                        ("delay", int, field(default=30)),
                        ("max_attempts", int, field(default=60)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
) -> Dict[str, Any]:
    """Deletes the specified Elasticsearch domain and all of its data. Once a domain is deleted, it cannot be recovered.

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): The name of the domain. Idem automatically considers this
            resource being absent if this field is not specified.
        timeout(Dict, Optional):
            Timeout configuration for AWS Elasticsearch domain
                * delete(Dict, Optional):
                    Timeout configuration when deleting an AWS Elasticsearch domain
                        * delay(int, Optional) -- The amount of time in seconds to wait between attempts. Default value is ``30``.
                        * max_attempts(int, Optional) -- Max attempts of waiting for change. Default value is ``60``.

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            test-domain-name:
              aws.es.elasticsearch_domain.absent:
                - name: test-domain-name
                - resource_id: test-domain-name
    """
    already_absent_msg = hub.tool.aws.comment_utils.already_absent_comment(
        resource_type="aws.es.elasticsearch_domain", name=name
    )
    result = dict(
        comment=already_absent_msg,
        old_state=None,
        new_state=None,
        name=name,
        result=True,
    )

    if not resource_id:
        return result

    before = await hub.exec.aws.es.elasticsearch_domain.get(
        ctx, name=name, resource_id=resource_id
    )
    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result

    if before["ret"]:
        result["old_state"] = before["ret"]
        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
                resource_type="aws.es.elasticsearch_domain", name=name
            )
        else:
            ret = await hub.exec.boto3.client.es.delete_elasticsearch_domain(
                ctx, DomainName=resource_id
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.es.elasticsearch_domain", name=name
            )
            delete_waiter_acceptors = [
                {
                    "matcher": "path",
                    "expected": False,
                    "state": "retry",
                    "argument": "DomainStatus.Deleted",
                },
                {
                    "matcher": "path",
                    "expected": True,
                    "state": "retry",
                    "argument": "DomainStatus.Deleted",
                },
                {
                    "matcher": "error",
                    "expected": "ResourceNotFoundException",
                    "state": "success",
                    "argument": "Error.Code",
                },
            ]

            delete_waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
                default_delay=30,
                default_max_attempts=60,
                timeout_config=timeout.get("delete") if timeout else None,
            )

            delete_domain_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
                name="ElasticsearchDomainDelete",
                operation="DescribeElasticsearchDomain",
                argument=["DomainStatus.Deleted"],
                acceptors=delete_waiter_acceptors,
                client=await hub.tool.boto3.client.get_client(ctx, "es"),
            )
            try:
                await hub.tool.boto3.client.wait(
                    ctx,
                    "es",
                    "ElasticsearchDomainDelete",
                    delete_domain_waiter,
                    DomainName=resource_id,
                    WaiterConfig=delete_waiter_config,
                )
            except Exception as e:
                result["comment"] += [str(e)]
                result["result"] = False

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Retrieves a list of domain configuration information of type "Elasticsearch"

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.es.elasticsearch_domain
    """
    result = {}
    # Returns the domain names of type Elasticsearch. Opensearch domains cannot be managed using this resource state functions
    get_domain_names_ret = await hub.exec.boto3.client.es.list_domain_names(
        ctx, EngineType="Elasticsearch"
    )

    if not get_domain_names_ret["result"]:
        hub.log.warning(
            f"Could not list domain names {get_domain_names_ret['comment']}"
        )
        return result

    for domain in get_domain_names_ret["ret"]["DomainNames"]:
        domain_name = domain.get("DomainName")
        get_elasticsearch_domain_ret = await hub.exec.aws.es.elasticsearch_domain.get(
            ctx, name=domain_name, resource_id=domain_name
        )

        if not (
            get_elasticsearch_domain_ret["result"]
            and get_elasticsearch_domain_ret["ret"]
        ):
            hub.log.debug(
                f"Could not get domain configuration information for the Elasticsearch domain '{domain_name}': "
                f"{get_elasticsearch_domain_ret['comment']}. Describe will skip this domain and continue."
            )
            continue

        result[domain_name] = {
            "aws.es.elasticsearch_domain.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in get_elasticsearch_domain_ret[
                    "ret"
                ].items()
            ]
        }
    return result
