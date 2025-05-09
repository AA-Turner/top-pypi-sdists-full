# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import builtins
import copy
import warnings
import sys
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
if sys.version_info >= (3, 11):
    from typing import NotRequired, TypedDict, TypeAlias
else:
    from typing_extensions import NotRequired, TypedDict, TypeAlias
from .. import _utilities
from . import outputs
from .. import outputs as _root_outputs
from ._enums import *

__all__ = [
    'GetPolicyResult',
    'AwaitableGetPolicyResult',
    'get_policy',
    'get_policy_output',
]

@pulumi.output_type
class GetPolicyResult:
    def __init__(__self__, arn=None, exclude_map=None, exclude_resource_tags=None, id=None, include_map=None, policy_description=None, policy_name=None, remediation_enabled=None, resource_set_ids=None, resource_tag_logical_operator=None, resource_tags=None, resource_type=None, resource_type_list=None, resources_clean_up=None, security_service_policy_data=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if exclude_map and not isinstance(exclude_map, dict):
            raise TypeError("Expected argument 'exclude_map' to be a dict")
        pulumi.set(__self__, "exclude_map", exclude_map)
        if exclude_resource_tags and not isinstance(exclude_resource_tags, bool):
            raise TypeError("Expected argument 'exclude_resource_tags' to be a bool")
        pulumi.set(__self__, "exclude_resource_tags", exclude_resource_tags)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if include_map and not isinstance(include_map, dict):
            raise TypeError("Expected argument 'include_map' to be a dict")
        pulumi.set(__self__, "include_map", include_map)
        if policy_description and not isinstance(policy_description, str):
            raise TypeError("Expected argument 'policy_description' to be a str")
        pulumi.set(__self__, "policy_description", policy_description)
        if policy_name and not isinstance(policy_name, str):
            raise TypeError("Expected argument 'policy_name' to be a str")
        pulumi.set(__self__, "policy_name", policy_name)
        if remediation_enabled and not isinstance(remediation_enabled, bool):
            raise TypeError("Expected argument 'remediation_enabled' to be a bool")
        pulumi.set(__self__, "remediation_enabled", remediation_enabled)
        if resource_set_ids and not isinstance(resource_set_ids, list):
            raise TypeError("Expected argument 'resource_set_ids' to be a list")
        pulumi.set(__self__, "resource_set_ids", resource_set_ids)
        if resource_tag_logical_operator and not isinstance(resource_tag_logical_operator, str):
            raise TypeError("Expected argument 'resource_tag_logical_operator' to be a str")
        pulumi.set(__self__, "resource_tag_logical_operator", resource_tag_logical_operator)
        if resource_tags and not isinstance(resource_tags, list):
            raise TypeError("Expected argument 'resource_tags' to be a list")
        pulumi.set(__self__, "resource_tags", resource_tags)
        if resource_type and not isinstance(resource_type, str):
            raise TypeError("Expected argument 'resource_type' to be a str")
        pulumi.set(__self__, "resource_type", resource_type)
        if resource_type_list and not isinstance(resource_type_list, list):
            raise TypeError("Expected argument 'resource_type_list' to be a list")
        pulumi.set(__self__, "resource_type_list", resource_type_list)
        if resources_clean_up and not isinstance(resources_clean_up, bool):
            raise TypeError("Expected argument 'resources_clean_up' to be a bool")
        pulumi.set(__self__, "resources_clean_up", resources_clean_up)
        if security_service_policy_data and not isinstance(security_service_policy_data, dict):
            raise TypeError("Expected argument 'security_service_policy_data' to be a dict")
        pulumi.set(__self__, "security_service_policy_data", security_service_policy_data)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[builtins.str]:
        """
        The Amazon Resource Name (ARN) of the policy.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="excludeMap")
    def exclude_map(self) -> Optional['outputs.PolicyIeMap']:
        """
        Specifies the AWS account IDs and AWS Organizations organizational units (OUs) to exclude from the policy. Specifying an OU is the equivalent of specifying all accounts in the OU and in any of its child OUs, including any child OUs and accounts that are added at a later time.

        You can specify inclusions or exclusions, but not both. If you specify an `IncludeMap` , AWS Firewall Manager applies the policy to all accounts specified by the `IncludeMap` , and does not evaluate any `ExcludeMap` specifications. If you do not specify an `IncludeMap` , then Firewall Manager applies the policy to all accounts except for those specified by the `ExcludeMap` .

        You can specify account IDs, OUs, or a combination:

        - Specify account IDs by setting the key to `ACCOUNT` . For example, the following is a valid map: `{"ACCOUNT" : ["accountID1", "accountID2"]}` .
        - Specify OUs by setting the key to `ORGUNIT` . For example, the following is a valid map: `{"ORGUNIT" : ["ouid111", "ouid112"]}` .
        - Specify accounts and OUs together in a single map, separated with a comma. For example, the following is a valid map: `{"ACCOUNT" : ["accountID1", "accountID2"], "ORGUNIT" : ["ouid111", "ouid112"]}` .
        """
        return pulumi.get(self, "exclude_map")

    @property
    @pulumi.getter(name="excludeResourceTags")
    def exclude_resource_tags(self) -> Optional[builtins.bool]:
        """
        Used only when tags are specified in the `ResourceTags` property. If this property is `True` , resources with the specified tags are not in scope of the policy. If it's `False` , only resources with the specified tags are in scope of the policy.
        """
        return pulumi.get(self, "exclude_resource_tags")

    @property
    @pulumi.getter
    def id(self) -> Optional[builtins.str]:
        """
        The ID of the policy.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="includeMap")
    def include_map(self) -> Optional['outputs.PolicyIeMap']:
        """
        Specifies the AWS account IDs and AWS Organizations organizational units (OUs) to include in the policy. Specifying an OU is the equivalent of specifying all accounts in the OU and in any of its child OUs, including any child OUs and accounts that are added at a later time.

        You can specify inclusions or exclusions, but not both. If you specify an `IncludeMap` , AWS Firewall Manager applies the policy to all accounts specified by the `IncludeMap` , and does not evaluate any `ExcludeMap` specifications. If you do not specify an `IncludeMap` , then Firewall Manager applies the policy to all accounts except for those specified by the `ExcludeMap` .

        You can specify account IDs, OUs, or a combination:

        - Specify account IDs by setting the key to `ACCOUNT` . For example, the following is a valid map: `{"ACCOUNT" : ["accountID1", "accountID2"]}` .
        - Specify OUs by setting the key to `ORGUNIT` . For example, the following is a valid map: `{"ORGUNIT" : ["ouid111", "ouid112"]}` .
        - Specify accounts and OUs together in a single map, separated with a comma. For example, the following is a valid map: `{"ACCOUNT" : ["accountID1", "accountID2"], "ORGUNIT" : ["ouid111", "ouid112"]}` .
        """
        return pulumi.get(self, "include_map")

    @property
    @pulumi.getter(name="policyDescription")
    def policy_description(self) -> Optional[builtins.str]:
        """
        Your description of the AWS Firewall Manager policy.
        """
        return pulumi.get(self, "policy_description")

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> Optional[builtins.str]:
        """
        The name of the AWS Firewall Manager policy.
        """
        return pulumi.get(self, "policy_name")

    @property
    @pulumi.getter(name="remediationEnabled")
    def remediation_enabled(self) -> Optional[builtins.bool]:
        """
        Indicates if the policy should be automatically applied to new resources.
        """
        return pulumi.get(self, "remediation_enabled")

    @property
    @pulumi.getter(name="resourceSetIds")
    def resource_set_ids(self) -> Optional[Sequence[builtins.str]]:
        """
        The unique identifiers of the resource sets used by the policy.
        """
        return pulumi.get(self, "resource_set_ids")

    @property
    @pulumi.getter(name="resourceTagLogicalOperator")
    def resource_tag_logical_operator(self) -> Optional['PolicyResourceTagLogicalOperator']:
        """
        Specifies whether to combine multiple resource tags with AND, so that a resource must have all tags to be included or excluded, or OR, so that a resource must have at least one tag.

        Default: `AND`
        """
        return pulumi.get(self, "resource_tag_logical_operator")

    @property
    @pulumi.getter(name="resourceTags")
    def resource_tags(self) -> Optional[Sequence['outputs.PolicyResourceTag']]:
        """
        An array of `ResourceTag` objects, used to explicitly include resources in the policy scope or explicitly exclude them. If this isn't set, then tags aren't used to modify policy scope. See also `ExcludeResourceTags` .
        """
        return pulumi.get(self, "resource_tags")

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> Optional[builtins.str]:
        """
        The type of resource protected by or in scope of the policy. This is in the format shown in the [AWS Resource Types Reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html) . To apply this policy to multiple resource types, specify a resource type of `ResourceTypeList` and then specify the resource types in a `ResourceTypeList` .

        The following are valid resource types for each Firewall Manager policy type:

        - AWS WAF Classic - `AWS::ApiGateway::Stage` , `AWS::CloudFront::Distribution` , and `AWS::ElasticLoadBalancingV2::LoadBalancer` .
        - AWS WAF - `AWS::ApiGateway::Stage` , `AWS::ElasticLoadBalancingV2::LoadBalancer` , and `AWS::CloudFront::Distribution` .
        - Shield Advanced - `AWS::ElasticLoadBalancingV2::LoadBalancer` , `AWS::ElasticLoadBalancing::LoadBalancer` , `AWS::EC2::EIP` , and `AWS::CloudFront::Distribution` .
        - Network ACL - `AWS::EC2::Subnet` .
        - Security group usage audit - `AWS::EC2::SecurityGroup` .
        - Security group content audit - `AWS::EC2::SecurityGroup` , `AWS::EC2::NetworkInterface` , and `AWS::EC2::Instance` .
        - DNS Firewall, AWS Network Firewall , and third-party firewall - `AWS::EC2::VPC` .
        """
        return pulumi.get(self, "resource_type")

    @property
    @pulumi.getter(name="resourceTypeList")
    def resource_type_list(self) -> Optional[Sequence[builtins.str]]:
        """
        An array of `ResourceType` objects. Use this only to specify multiple resource types. To specify a single resource type, use `ResourceType` .
        """
        return pulumi.get(self, "resource_type_list")

    @property
    @pulumi.getter(name="resourcesCleanUp")
    def resources_clean_up(self) -> Optional[builtins.bool]:
        """
        Indicates whether AWS Firewall Manager should automatically remove protections from resources that leave the policy scope and clean up resources that Firewall Manager is managing for accounts when those accounts leave policy scope. For example, Firewall Manager will disassociate a Firewall Manager managed web ACL from a protected customer resource when the customer resource leaves policy scope.

        By default, Firewall Manager doesn't remove protections or delete Firewall Manager managed resources.

        This option is not available for Shield Advanced or AWS WAF Classic policies.
        """
        return pulumi.get(self, "resources_clean_up")

    @property
    @pulumi.getter(name="securityServicePolicyData")
    def security_service_policy_data(self) -> Optional['outputs.PolicySecurityServicePolicyData']:
        """
        Details about the security service that is being used to protect the resources.

        This contains the following settings:

        - Type - Indicates the service type that the policy uses to protect the resource. For security group policies, Firewall Manager supports one security group for each common policy and for each content audit policy. This is an adjustable limit that you can increase by contacting  .

        Valid values: `DNS_FIREWALL` | `NETWORK_FIREWALL` | `SECURITY_GROUPS_COMMON` | `SECURITY_GROUPS_CONTENT_AUDIT` | `SECURITY_GROUPS_USAGE_AUDIT` | `SHIELD_ADVANCED` | `THIRD_PARTY_FIREWALL` | `WAFV2` | `WAF`
        - ManagedServiceData - Details about the service that are specific to the service type, in JSON format.

        - Example: `DNS_FIREWALL`

        `"{\\"type\\":\\"DNS_FIREWALL\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupId\\":\\"rslvr-frg-1\\",\\"priority\\":10}],\\"postProcessRuleGroups\\":[{\\"ruleGroupId\\":\\"rslvr-frg-2\\",\\"priority\\":9911}]}"`

        > Valid values for `preProcessRuleGroups` are between 1 and 99. Valid values for `postProcessRuleGroups` are between 9901 and 10000.
        - Example: `NETWORK_FIREWALL` - Centralized deployment model

        `"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"awsNetworkFirewallConfig\\":{\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}},\\"firewallDeploymentModel\\":{\\"centralizedFirewallDeploymentModel\\":{\\"centralizedFirewallOrchestrationConfig\\":{\\"inspectionVpcIds\\":[{\\"resourceId\\":\\"vpc-1234\\",\\"accountId\\":\\"123456789011\\"}],\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneId\\":null,\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"allowedIPV4CidrList\\":[]}}}}"`

        To use the distributed deployment model, you must set [FirewallDeploymentModel](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html) to `DISTRIBUTED` .
        - Example: `NETWORK_FIREWALL` - Distributed deployment model with automatic Availability Zone configuration

        `"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\",\\"192.168.0.0/28\\"],\\"routeManagementAction\\":\\"OFF\\"},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}}"`

        With automatic Availbility Zone configuration, Firewall Manager chooses which Availability Zones to create the endpoints in. To use the distributed deployment model, you must set [FirewallDeploymentModel](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html) to `DISTRIBUTED` .
        - Example: `NETWORK_FIREWALL` - Distributed deployment model with automatic Availability Zone configuration and route management

        `"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\",\\"192.168.0.0/28\\"],\\"routeManagementAction\\":\\"MONITOR\\",\\"routeManagementTargetTypes\\":[\\"InternetGateway\\"]},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\": \\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}}"`

        To use the distributed deployment model, you must set [FirewallDeploymentModel](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html) to `DISTRIBUTED` .
        - Example: `NETWORK_FIREWALL` - Distributed deployment model with custom Availability Zone configuration

        `"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"fragmentcustomactionname\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\", \\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}},{\\"actionName\\":\\"fragmentcustomactionname\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"fragmentmetricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{ \\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]},{\\"availabilityZoneName\\":\\"us-east-1b\\",\\"allowedIPV4CidrList\\":[ \\"10.0.0.0/28\\"]}]} },\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":null,\\"routeManagementAction\\":\\"OFF\\",\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":boolean}}"`

        With custom Availability Zone configuration, you define which specific Availability Zones to create endpoints in by configuring `firewallCreationConfig` . To configure the Availability Zones in `firewallCreationConfig` , specify either the `availabilityZoneName` or `availabilityZoneId` parameter, not both parameters.

        To use the distributed deployment model, you must set [FirewallDeploymentModel](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html) to `DISTRIBUTED` .
        - Example: `NETWORK_FIREWALL` - Distributed deployment model with custom Availability Zone configuration and route management

        `"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"fragmentcustomactionname\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}},{\\"actionName\\":\\"fragmentcustomactionname\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"fragmentmetricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]},{\\"availabilityZoneName\\":\\"us-east-1b\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":null,\\"routeManagementAction\\":\\"MONITOR\\",\\"routeManagementTargetTypes\\":[\\"InternetGateway\\"],\\"routeManagementConfig\\":{\\"allowCrossAZTrafficIfNoEndpoint\\":true}},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":boolean}}"`

        To use the distributed deployment model, you must set [FirewallDeploymentModel](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html) to `DISTRIBUTED` .
        - Example: `THIRD_PARTY_FIREWALL` - Palo Alto Networks Cloud Next-Generation Firewall centralized deployment model

        `"{ \\"type\\":\\"THIRD_PARTY_FIREWALL\\", \\"thirdPartyFirewall\\":\\"PALO_ALTO_NETWORKS_CLOUD_NGFW\\", \\"thirdPartyFirewallConfig\\":{ \\"thirdPartyFirewallPolicyList\\":[\\"global-1\\"] },\\"firewallDeploymentModel\\":{\\"centralizedFirewallDeploymentModel\\":{\\"centralizedFirewallOrchestrationConfig\\":{\\"inspectionVpcIds\\":[{\\"resourceId\\":\\"vpc-1234\\",\\"accountId\\":\\"123456789011\\"}],\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneId\\":null,\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"allowedIPV4CidrList\\":[]}}}}"`

        To use the distributed deployment model, you must set [FirewallDeploymentModel](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html) to `CENTRALIZED` .
        - Example: `THIRD_PARTY_FIREWALL` - Palo Alto Networks Cloud Next-Generation Firewall distributed deployment model

        `"{\\"type\\":\\"THIRD_PARTY_FIREWALL\\",\\"thirdPartyFirewall\\":\\"PALO_ALTO_NETWORKS_CLOUD_NGFW\\",\\"thirdPartyFirewallConfig\\":{\\"thirdPartyFirewallPolicyList\\":[\\"global-1\\"] },\\"firewallDeploymentModel\\":{ \\"distributedFirewallDeploymentModel\\":{ \\"distributedFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{\\"endpointLocation\\":{ \\"availabilityZoneConfigList\\":[ {\\"availabilityZoneName\\":\\"${AvailabilityZone}\\" } ] } }, \\"allowedIPV4CidrList\\":[ ] } } } }"`

        To use the distributed deployment model, you must set [FirewallDeploymentModel](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html) to `DISTRIBUTED` .
        - Specification for `SHIELD_ADVANCED` for Amazon CloudFront distributions

        `"{\\"type\\":\\"SHIELD_ADVANCED\\",\\"automaticResponseConfiguration\\": {\\"automaticResponseStatus\\":\\"ENABLED|IGNORED|DISABLED\\", \\"automaticResponseAction\\":\\"BLOCK|COUNT\\"}, \\"overrideCustomerWebaclClassic\\":true|false}"`

        For example: `"{\\"type\\":\\"SHIELD_ADVANCED\\",\\"automaticResponseConfiguration\\": {\\"automaticResponseStatus\\":\\"ENABLED\\", \\"automaticResponseAction\\":\\"COUNT\\"}}"`

        The default value for `automaticResponseStatus` is `IGNORED` . The value for `automaticResponseAction` is only required when `automaticResponseStatus` is set to `ENABLED` . The default value for `overrideCustomerWebaclClassic` is `false` .

        For other resource types that you can protect with a Shield Advanced policy, this `ManagedServiceData` configuration is an empty string.
        - Example: `WAFV2`

        `"{\\"type\\":\\"WAFV2\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupArn\\":null,\\"overrideAction\\":{\\"type\\":\\"NONE\\"},\\"managedRuleGroupIdentifier\\":{\\"version\\":null,\\"vendorName\\":\\"AWS\\",\\"managedRuleGroupName\\":\\"AWSManagedRulesAmazonIpReputationList\\"},\\"ruleGroupType\\":\\"ManagedRuleGroup\\",\\"excludeRules\\":[{\\"name\\":\\"NoUserAgent_HEADER\\"}]}],\\"postProcessRuleGroups\\":[],\\"defaultAction\\":{\\"type\\":\\"ALLOW\\"},\\"overrideCustomerWebACLAssociation\\":false,\\"loggingConfiguration\\":{\\"logDestinationConfigs\\":[\\"arn:aws:firehose:us-west-2:12345678912:deliverystream/aws-waf-logs-fms-admin-destination\\"],\\"redactedFields\\":[{\\"redactedFieldType\\":\\"SingleHeader\\",\\"redactedFieldValue\\":\\"Cookies\\"},{\\"redactedFieldType\\":\\"Method\\"}]}}"`

        In the `loggingConfiguration` , you can specify one `logDestinationConfigs` , you can optionally provide up to 20 `redactedFields` , and the `RedactedFieldType` must be one of `URI` , `QUERY_STRING` , `HEADER` , or `METHOD` .
        - Example: `AWS WAF Classic`

        `"{\\"type\\": \\"WAF\\", \\"ruleGroups\\": [{\\"id\\":\\"12345678-1bcd-9012-efga-0987654321ab\\", \\"overrideAction\\" : {\\"type\\": \\"COUNT\\"}}], \\"defaultAction\\": {\\"type\\": \\"BLOCK\\"}}"`
        - Example: `WAFV2` - AWS Firewall Manager support for AWS WAF managed rule group versioning

        `"{\\"type\\":\\"WAFV2\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupArn\\":null,\\"overrideAction\\":{\\"type\\":\\"NONE\\"},\\"managedRuleGroupIdentifier\\":{\\"versionEnabled\\":true,\\"version\\":\\"Version_2.0\\",\\"vendorName\\":\\"AWS\\",\\"managedRuleGroupName\\":\\"AWSManagedRulesCommonRuleSet\\"},\\"ruleGroupType\\":\\"ManagedRuleGroup\\",\\"excludeRules\\":[{\\"name\\":\\"NoUserAgent_HEADER\\"}]}],\\"postProcessRuleGroups\\":[],\\"defaultAction\\":{\\"type\\":\\"ALLOW\\"},\\"overrideCustomerWebACLAssociation\\":false,\\"loggingConfiguration\\":{\\"logDestinationConfigs\\":[\\"arn:aws:firehose:us-west-2:12345678912:deliverystream/aws-waf-logs-fms-admin-destination\\"],\\"redactedFields\\":[{\\"redactedFieldType\\":\\"SingleHeader\\",\\"redactedFieldValue\\":\\"Cookies\\"},{\\"redactedFieldType\\":\\"Method\\"}]}}"`

        To use a specific version of a AWS WAF managed rule group in your Firewall Manager policy, you must set `versionEnabled` to `true` , and set `version` to the version you'd like to use. If you don't set `versionEnabled` to `true` , or if you omit `versionEnabled` , then Firewall Manager uses the default version of the AWS WAF managed rule group.
        - Example: `SECURITY_GROUPS_COMMON`

        `"{\\"type\\":\\"SECURITY_GROUPS_COMMON\\",\\"revertManualSecurityGroupChanges\\":false,\\"exclusiveResourceSecurityGroupManagement\\":false, \\"applyToAllEC2InstanceENIs\\":false,\\"securityGroups\\":[{\\"id\\":\\" sg-000e55995d61a06bd\\"}]}"`
        - Example: Shared VPCs. Apply the preceding policy to resources in shared VPCs as well as to those in VPCs that the account owns

        `"{\\"type\\":\\"SECURITY_GROUPS_COMMON\\",\\"revertManualSecurityGroupChanges\\":false,\\"exclusiveResourceSecurityGroupManagement\\":false, \\"applyToAllEC2InstanceENIs\\":false,\\"includeSharedVPC\\":true,\\"securityGroups\\":[{\\"id\\":\\" sg-000e55995d61a06bd\\"}]}"`
        - Example: `SECURITY_GROUPS_CONTENT_AUDIT`

        `"{\\"type\\":\\"SECURITY_GROUPS_CONTENT_AUDIT\\",\\"securityGroups\\":[{\\"id\\":\\"sg-000e55995d61a06bd\\"}],\\"securityGroupAction\\":{\\"type\\":\\"ALLOW\\"}}"`

        The security group action for content audit can be `ALLOW` or `DENY` . For `ALLOW` , all in-scope security group rules must be within the allowed range of the policy's security group rules. For `DENY` , all in-scope security group rules must not contain a value or a range that matches a rule value or range in the policy security group.
        - Example: `SECURITY_GROUPS_USAGE_AUDIT`

        `"{\\"type\\":\\"SECURITY_GROUPS_USAGE_AUDIT\\",\\"deleteUnusedSecurityGroups\\":true,\\"coalesceRedundantSecurityGroups\\":true}"`
        """
        return pulumi.get(self, "security_service_policy_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        A collection of key:value pairs associated with an AWS resource. The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetPolicyResult(GetPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPolicyResult(
            arn=self.arn,
            exclude_map=self.exclude_map,
            exclude_resource_tags=self.exclude_resource_tags,
            id=self.id,
            include_map=self.include_map,
            policy_description=self.policy_description,
            policy_name=self.policy_name,
            remediation_enabled=self.remediation_enabled,
            resource_set_ids=self.resource_set_ids,
            resource_tag_logical_operator=self.resource_tag_logical_operator,
            resource_tags=self.resource_tags,
            resource_type=self.resource_type,
            resource_type_list=self.resource_type_list,
            resources_clean_up=self.resources_clean_up,
            security_service_policy_data=self.security_service_policy_data,
            tags=self.tags)


def get_policy(id: Optional[builtins.str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPolicyResult:
    """
    Creates an AWS Firewall Manager policy.


    :param builtins.str id: The ID of the policy.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:fms:getPolicy', __args__, opts=opts, typ=GetPolicyResult).value

    return AwaitableGetPolicyResult(
        arn=pulumi.get(__ret__, 'arn'),
        exclude_map=pulumi.get(__ret__, 'exclude_map'),
        exclude_resource_tags=pulumi.get(__ret__, 'exclude_resource_tags'),
        id=pulumi.get(__ret__, 'id'),
        include_map=pulumi.get(__ret__, 'include_map'),
        policy_description=pulumi.get(__ret__, 'policy_description'),
        policy_name=pulumi.get(__ret__, 'policy_name'),
        remediation_enabled=pulumi.get(__ret__, 'remediation_enabled'),
        resource_set_ids=pulumi.get(__ret__, 'resource_set_ids'),
        resource_tag_logical_operator=pulumi.get(__ret__, 'resource_tag_logical_operator'),
        resource_tags=pulumi.get(__ret__, 'resource_tags'),
        resource_type=pulumi.get(__ret__, 'resource_type'),
        resource_type_list=pulumi.get(__ret__, 'resource_type_list'),
        resources_clean_up=pulumi.get(__ret__, 'resources_clean_up'),
        security_service_policy_data=pulumi.get(__ret__, 'security_service_policy_data'),
        tags=pulumi.get(__ret__, 'tags'))
def get_policy_output(id: Optional[pulumi.Input[builtins.str]] = None,
                      opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetPolicyResult]:
    """
    Creates an AWS Firewall Manager policy.


    :param builtins.str id: The ID of the policy.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:fms:getPolicy', __args__, opts=opts, typ=GetPolicyResult)
    return __ret__.apply(lambda __response__: GetPolicyResult(
        arn=pulumi.get(__response__, 'arn'),
        exclude_map=pulumi.get(__response__, 'exclude_map'),
        exclude_resource_tags=pulumi.get(__response__, 'exclude_resource_tags'),
        id=pulumi.get(__response__, 'id'),
        include_map=pulumi.get(__response__, 'include_map'),
        policy_description=pulumi.get(__response__, 'policy_description'),
        policy_name=pulumi.get(__response__, 'policy_name'),
        remediation_enabled=pulumi.get(__response__, 'remediation_enabled'),
        resource_set_ids=pulumi.get(__response__, 'resource_set_ids'),
        resource_tag_logical_operator=pulumi.get(__response__, 'resource_tag_logical_operator'),
        resource_tags=pulumi.get(__response__, 'resource_tags'),
        resource_type=pulumi.get(__response__, 'resource_type'),
        resource_type_list=pulumi.get(__response__, 'resource_type_list'),
        resources_clean_up=pulumi.get(__response__, 'resources_clean_up'),
        security_service_policy_data=pulumi.get(__response__, 'security_service_policy_data'),
        tags=pulumi.get(__response__, 'tags')))
