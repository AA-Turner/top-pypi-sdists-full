r'''
# `google_compute_subnetwork`

Refer to the Terraform Registry for docs: [`google_compute_subnetwork`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class ComputeSubnetwork(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSubnetwork.ComputeSubnetwork",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork google_compute_subnetwork}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        network: builtins.str,
        description: typing.Optional[builtins.str] = None,
        enable_flow_logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_ipv6_prefix: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_cidr_range: typing.Optional[builtins.str] = None,
        ip_collection: typing.Optional[builtins.str] = None,
        ipv6_access_type: typing.Optional[builtins.str] = None,
        log_config: typing.Optional[typing.Union["ComputeSubnetworkLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        params: typing.Optional[typing.Union["ComputeSubnetworkParams", typing.Dict[builtins.str, typing.Any]]] = None,
        private_ip_google_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_ipv6_google_access: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        purpose: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        reserved_internal_range: typing.Optional[builtins.str] = None,
        role: typing.Optional[builtins.str] = None,
        secondary_ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSubnetworkSecondaryIpRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        send_secondary_ip_range_if_empty: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        stack_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeSubnetworkTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork google_compute_subnetwork} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the resource, provided by the client when initially creating the resource. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#name ComputeSubnetwork#name}
        :param network: The network this subnet belongs to. Only networks that are in the distributed mode can have subnetworks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#network ComputeSubnetwork#network}
        :param description: An optional description of this resource. Provide this property when you create the resource. This field can be set only at resource creation time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#description ComputeSubnetwork#description}
        :param enable_flow_logs: Whether to enable flow logging for this subnetwork. If this field is not explicitly set, it will not appear in get listings. If not set the default behavior is determined by the org policy, if there is no org policy specified, then it will default to disabled. This field isn't supported if the subnet purpose field is set to REGIONAL_MANAGED_PROXY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#enable_flow_logs ComputeSubnetwork#enable_flow_logs}
        :param external_ipv6_prefix: The range of external IPv6 addresses that are owned by this subnetwork. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#external_ipv6_prefix ComputeSubnetwork#external_ipv6_prefix}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#id ComputeSubnetwork#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_cidr_range: The range of internal addresses that are owned by this subnetwork. Provide this property when you create the subnetwork. For example, 10.0.0.0/8 or 192.168.0.0/16. Ranges must be unique and non-overlapping within a network. Only IPv4 is supported. Field is optional when 'reserved_internal_range' is defined, otherwise required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#ip_cidr_range ComputeSubnetwork#ip_cidr_range}
        :param ip_collection: Resource reference of a PublicDelegatedPrefix. The PDP must be a sub-PDP in EXTERNAL_IPV6_SUBNETWORK_CREATION mode. Use one of the following formats to specify a sub-PDP when creating an IPv6 NetLB forwarding rule using BYOIP: Full resource URL, as in: - 'https://www.googleapis.com/compute/v1/projects/{{projectId}}/regions/{{region}}/publicDelegatedPrefixes/{{sub-pdp-name}}' Partial URL, as in: - 'projects/{{projectId}}/regions/region/publicDelegatedPrefixes/{{sub-pdp-name}}' - 'regions/{{region}}/publicDelegatedPrefixes/{{sub-pdp-name}}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#ip_collection ComputeSubnetwork#ip_collection}
        :param ipv6_access_type: The access type of IPv6 address this subnet holds. It's immutable and can only be specified during creation or the first time the subnet is updated into IPV4_IPV6 dual stack. If the ipv6_type is EXTERNAL then this subnet cannot enable direct path. Possible values: ["EXTERNAL", "INTERNAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#ipv6_access_type ComputeSubnetwork#ipv6_access_type}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#log_config ComputeSubnetwork#log_config}
        :param params: params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#params ComputeSubnetwork#params}
        :param private_ip_google_access: When enabled, VMs in this subnetwork without external IP addresses can access Google APIs and services by using Private Google Access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#private_ip_google_access ComputeSubnetwork#private_ip_google_access}
        :param private_ipv6_google_access: The private IPv6 google access type for the VMs in this subnet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#private_ipv6_google_access ComputeSubnetwork#private_ipv6_google_access}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#project ComputeSubnetwork#project}.
        :param purpose: The purpose of the resource. This field can be either 'PRIVATE', 'REGIONAL_MANAGED_PROXY', 'GLOBAL_MANAGED_PROXY', 'PRIVATE_SERVICE_CONNECT', 'PEER_MIGRATION' or 'PRIVATE_NAT'(`Beta <https://terraform.io/docs/providers/google/guides/provider_versions.html>`_). A subnet with purpose set to 'REGIONAL_MANAGED_PROXY' is a user-created subnetwork that is reserved for regional Envoy-based load balancers. A subnetwork in a given region with purpose set to 'GLOBAL_MANAGED_PROXY' is a proxy-only subnet and is shared between all the cross-regional Envoy-based load balancers. A subnetwork with purpose set to 'PRIVATE_SERVICE_CONNECT' reserves the subnet for hosting a Private Service Connect published service. A subnetwork with purpose set to 'PEER_MIGRATION' is a user created subnetwork that is reserved for migrating resources from one peered network to another. A subnetwork with purpose set to 'PRIVATE_NAT' is used as source range for Private NAT gateways. Note that 'REGIONAL_MANAGED_PROXY' is the preferred setting for all regional Envoy load balancers. If unspecified, the purpose defaults to 'PRIVATE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#purpose ComputeSubnetwork#purpose}
        :param region: The GCP region for this subnetwork. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#region ComputeSubnetwork#region}
        :param reserved_internal_range: The ID of the reserved internal range. Must be prefixed with 'networkconnectivity.googleapis.com' E.g. 'networkconnectivity.googleapis.com/projects/{project}/locations/global/internalRanges/{rangeId}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#reserved_internal_range ComputeSubnetwork#reserved_internal_range}
        :param role: The role of subnetwork. Currently, this field is only used when 'purpose' is 'REGIONAL_MANAGED_PROXY'. The value can be set to 'ACTIVE' or 'BACKUP'. An 'ACTIVE' subnetwork is one that is currently being used for Envoy-based load balancers in a region. A 'BACKUP' subnetwork is one that is ready to be promoted to 'ACTIVE' or is currently draining. Possible values: ["ACTIVE", "BACKUP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#role ComputeSubnetwork#role}
        :param secondary_ip_range: secondary_ip_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#secondary_ip_range ComputeSubnetwork#secondary_ip_range}
        :param send_secondary_ip_range_if_empty: Controls the removal behavior of secondary_ip_range. When false, removing secondary_ip_range from config will not produce a diff as the provider will default to the API's value. When true, the provider will treat removing secondary_ip_range as sending an empty list of secondary IP ranges to the API. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#send_secondary_ip_range_if_empty ComputeSubnetwork#send_secondary_ip_range_if_empty}
        :param stack_type: The stack type for this subnet to identify whether the IPv6 feature is enabled or not. If not specified IPV4_ONLY will be used. Possible values: ["IPV4_ONLY", "IPV4_IPV6", "IPV6_ONLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#stack_type ComputeSubnetwork#stack_type}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#timeouts ComputeSubnetwork#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01fd1c59fbdcd905b899f4bc7d27175967e82edddf94d2b4fde01f211ebeb0e0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeSubnetworkConfig(
            name=name,
            network=network,
            description=description,
            enable_flow_logs=enable_flow_logs,
            external_ipv6_prefix=external_ipv6_prefix,
            id=id,
            ip_cidr_range=ip_cidr_range,
            ip_collection=ip_collection,
            ipv6_access_type=ipv6_access_type,
            log_config=log_config,
            params=params,
            private_ip_google_access=private_ip_google_access,
            private_ipv6_google_access=private_ipv6_google_access,
            project=project,
            purpose=purpose,
            region=region,
            reserved_internal_range=reserved_internal_range,
            role=role,
            secondary_ip_range=secondary_ip_range,
            send_secondary_ip_range_if_empty=send_secondary_ip_range_if_empty,
            stack_type=stack_type,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a ComputeSubnetwork resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeSubnetwork to import.
        :param import_from_id: The id of the existing ComputeSubnetwork that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeSubnetwork to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__031a7c53cbbac42bac029930c8f0b7c8b95c6b044ddf91faa0a8d5c4b834d1e6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLogConfig")
    def put_log_config(
        self,
        *,
        aggregation_interval: typing.Optional[builtins.str] = None,
        filter_expr: typing.Optional[builtins.str] = None,
        flow_sampling: typing.Optional[jsii.Number] = None,
        metadata: typing.Optional[builtins.str] = None,
        metadata_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param aggregation_interval: Can only be specified if VPC flow logging for this subnetwork is enabled. Toggles the aggregation interval for collecting flow logs. Increasing the interval time will reduce the amount of generated flow logs for long lasting connections. Default is an interval of 5 seconds per connection. Default value: "INTERVAL_5_SEC" Possible values: ["INTERVAL_5_SEC", "INTERVAL_30_SEC", "INTERVAL_1_MIN", "INTERVAL_5_MIN", "INTERVAL_10_MIN", "INTERVAL_15_MIN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#aggregation_interval ComputeSubnetwork#aggregation_interval}
        :param filter_expr: Export filter used to define which VPC flow logs should be logged, as as CEL expression. See https://cloud.google.com/vpc/docs/flow-logs#filtering for details on how to format this field. The default value is 'true', which evaluates to include everything. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#filter_expr ComputeSubnetwork#filter_expr}
        :param flow_sampling: Can only be specified if VPC flow logging for this subnetwork is enabled. The value of the field must be in [0, 1]. Set the sampling rate of VPC flow logs within the subnetwork where 1.0 means all collected logs are reported and 0.0 means no logs are reported. Default is 0.5 which means half of all collected logs are reported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#flow_sampling ComputeSubnetwork#flow_sampling}
        :param metadata: Can only be specified if VPC flow logging for this subnetwork is enabled. Configures whether metadata fields should be added to the reported VPC flow logs. Default value: "INCLUDE_ALL_METADATA" Possible values: ["EXCLUDE_ALL_METADATA", "INCLUDE_ALL_METADATA", "CUSTOM_METADATA"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#metadata ComputeSubnetwork#metadata}
        :param metadata_fields: List of metadata fields that should be added to reported logs. Can only be specified if VPC flow logs for this subnetwork is enabled and "metadata" is set to CUSTOM_METADATA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#metadata_fields ComputeSubnetwork#metadata_fields}
        '''
        value = ComputeSubnetworkLogConfig(
            aggregation_interval=aggregation_interval,
            filter_expr=filter_expr,
            flow_sampling=flow_sampling,
            metadata=metadata,
            metadata_fields=metadata_fields,
        )

        return typing.cast(None, jsii.invoke(self, "putLogConfig", [value]))

    @jsii.member(jsii_name="putParams")
    def put_params(
        self,
        *,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param resource_manager_tags: Resource manager tags to be bound to the subnetwork. Tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored when empty. The field is immutable and causes resource replacement when mutated. This field is only set at create time and modifying this field after creation will trigger recreation. To apply tags to an existing resource, see the google_tags_tag_binding resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#resource_manager_tags ComputeSubnetwork#resource_manager_tags}
        '''
        value = ComputeSubnetworkParams(resource_manager_tags=resource_manager_tags)

        return typing.cast(None, jsii.invoke(self, "putParams", [value]))

    @jsii.member(jsii_name="putSecondaryIpRange")
    def put_secondary_ip_range(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSubnetworkSecondaryIpRange", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad28ca287c36ce160f111925adccb0f84f9aba4d09bb520316167bce929b9795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecondaryIpRange", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#create ComputeSubnetwork#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#delete ComputeSubnetwork#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#update ComputeSubnetwork#update}.
        '''
        value = ComputeSubnetworkTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnableFlowLogs")
    def reset_enable_flow_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableFlowLogs", []))

    @jsii.member(jsii_name="resetExternalIpv6Prefix")
    def reset_external_ipv6_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalIpv6Prefix", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpCidrRange")
    def reset_ip_cidr_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpCidrRange", []))

    @jsii.member(jsii_name="resetIpCollection")
    def reset_ip_collection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpCollection", []))

    @jsii.member(jsii_name="resetIpv6AccessType")
    def reset_ipv6_access_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6AccessType", []))

    @jsii.member(jsii_name="resetLogConfig")
    def reset_log_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogConfig", []))

    @jsii.member(jsii_name="resetParams")
    def reset_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParams", []))

    @jsii.member(jsii_name="resetPrivateIpGoogleAccess")
    def reset_private_ip_google_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIpGoogleAccess", []))

    @jsii.member(jsii_name="resetPrivateIpv6GoogleAccess")
    def reset_private_ipv6_google_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIpv6GoogleAccess", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPurpose")
    def reset_purpose(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPurpose", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetReservedInternalRange")
    def reset_reserved_internal_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservedInternalRange", []))

    @jsii.member(jsii_name="resetRole")
    def reset_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRole", []))

    @jsii.member(jsii_name="resetSecondaryIpRange")
    def reset_secondary_ip_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryIpRange", []))

    @jsii.member(jsii_name="resetSendSecondaryIpRangeIfEmpty")
    def reset_send_secondary_ip_range_if_empty(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendSecondaryIpRangeIfEmpty", []))

    @jsii.member(jsii_name="resetStackType")
    def reset_stack_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStackType", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="fingerprint")
    def fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fingerprint"))

    @builtins.property
    @jsii.member(jsii_name="gatewayAddress")
    def gateway_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayAddress"))

    @builtins.property
    @jsii.member(jsii_name="internalIpv6Prefix")
    def internal_ipv6_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "internalIpv6Prefix"))

    @builtins.property
    @jsii.member(jsii_name="ipv6CidrRange")
    def ipv6_cidr_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6CidrRange"))

    @builtins.property
    @jsii.member(jsii_name="ipv6GceEndpoint")
    def ipv6_gce_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6GceEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="logConfig")
    def log_config(self) -> "ComputeSubnetworkLogConfigOutputReference":
        return typing.cast("ComputeSubnetworkLogConfigOutputReference", jsii.get(self, "logConfig"))

    @builtins.property
    @jsii.member(jsii_name="params")
    def params(self) -> "ComputeSubnetworkParamsOutputReference":
        return typing.cast("ComputeSubnetworkParamsOutputReference", jsii.get(self, "params"))

    @builtins.property
    @jsii.member(jsii_name="secondaryIpRange")
    def secondary_ip_range(self) -> "ComputeSubnetworkSecondaryIpRangeList":
        return typing.cast("ComputeSubnetworkSecondaryIpRangeList", jsii.get(self, "secondaryIpRange"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkId")
    def subnetwork_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "subnetworkId"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeSubnetworkTimeoutsOutputReference":
        return typing.cast("ComputeSubnetworkTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableFlowLogsInput")
    def enable_flow_logs_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableFlowLogsInput"))

    @builtins.property
    @jsii.member(jsii_name="externalIpv6PrefixInput")
    def external_ipv6_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalIpv6PrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipCidrRangeInput")
    def ip_cidr_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipCidrRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="ipCollectionInput")
    def ip_collection_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipCollectionInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6AccessTypeInput")
    def ipv6_access_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv6AccessTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="logConfigInput")
    def log_config_input(self) -> typing.Optional["ComputeSubnetworkLogConfig"]:
        return typing.cast(typing.Optional["ComputeSubnetworkLogConfig"], jsii.get(self, "logConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="paramsInput")
    def params_input(self) -> typing.Optional["ComputeSubnetworkParams"]:
        return typing.cast(typing.Optional["ComputeSubnetworkParams"], jsii.get(self, "paramsInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpGoogleAccessInput")
    def private_ip_google_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "privateIpGoogleAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpv6GoogleAccessInput")
    def private_ipv6_google_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpv6GoogleAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="purposeInput")
    def purpose_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "purposeInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="reservedInternalRangeInput")
    def reserved_internal_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reservedInternalRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="roleInput")
    def role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryIpRangeInput")
    def secondary_ip_range_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSubnetworkSecondaryIpRange"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSubnetworkSecondaryIpRange"]]], jsii.get(self, "secondaryIpRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="sendSecondaryIpRangeIfEmptyInput")
    def send_secondary_ip_range_if_empty_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendSecondaryIpRangeIfEmptyInput"))

    @builtins.property
    @jsii.member(jsii_name="stackTypeInput")
    def stack_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stackTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeSubnetworkTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeSubnetworkTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86bad37f5c67c7afd2233f46410b3f8f28bec0e613b1a74d141375d7e6d62b39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableFlowLogs")
    def enable_flow_logs(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableFlowLogs"))

    @enable_flow_logs.setter
    def enable_flow_logs(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f701d7f23bb1bbc9e19d7c0d47339b7d3f0b6669e91b99d61d8d0e4c716c287)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableFlowLogs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalIpv6Prefix")
    def external_ipv6_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalIpv6Prefix"))

    @external_ipv6_prefix.setter
    def external_ipv6_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b72d44f871993033179b8ca28f1444e5adb8301b5218c5b388875530564b2c3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalIpv6Prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d080d26436de885eddb22c28df35b51d9916ac6f6caf549d4892759693e0a7c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipCidrRange")
    def ip_cidr_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipCidrRange"))

    @ip_cidr_range.setter
    def ip_cidr_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2ebf3a83259961af9502d2a2ac40d29be32471d7f85a700c8e68c96ba756c20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipCidrRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipCollection")
    def ip_collection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipCollection"))

    @ip_collection.setter
    def ip_collection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__445cdee46239834b389c4ca7027de593dd781278f0e464f888276dac37660fad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipCollection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv6AccessType")
    def ipv6_access_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6AccessType"))

    @ipv6_access_type.setter
    def ipv6_access_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3be079515323e0453d5620d393bf9096a1f15feb029d7808e2e9f51981e2075b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6AccessType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e66b56122974ea4e216fdf396fd774abfc6f1eeb195ee4be091c5f500a1f884)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e0ec593bcba254fe1159921d7be42cea751a07ba1eac8c35fc1cb421160b83b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIpGoogleAccess")
    def private_ip_google_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "privateIpGoogleAccess"))

    @private_ip_google_access.setter
    def private_ip_google_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a402ba23908fbbb7b6d530fbf646e1510e3d3c654755bf94ccb74483ece916c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpGoogleAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIpv6GoogleAccess")
    def private_ipv6_google_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpv6GoogleAccess"))

    @private_ipv6_google_access.setter
    def private_ipv6_google_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6acb602e4fb08411793ffe3147e6b3b37f0cd9bc3e72a674067325a0ce84ff3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpv6GoogleAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8a9e071fd98237c230795d301adcc09a1591aeb401ef656afd9c2e1f6dab65e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="purpose")
    def purpose(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "purpose"))

    @purpose.setter
    def purpose(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__244cd42cc57e180dbcf8317d170227ce000ce6a71d17c55f4c43eb98b6ae18a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "purpose", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b877e4e78db1787f7706bb059c38da47877f7bc75be426b17d0d49fe1001f7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reservedInternalRange")
    def reserved_internal_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reservedInternalRange"))

    @reserved_internal_range.setter
    def reserved_internal_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70782ebfac80c688953c975faad7b02e23991f8e53d60758dfacd22b679411a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservedInternalRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5438473aba032b02489e8f51a6798405708ea87f592b69ef25b4c14a8049865)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sendSecondaryIpRangeIfEmpty")
    def send_secondary_ip_range_if_empty(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendSecondaryIpRangeIfEmpty"))

    @send_secondary_ip_range_if_empty.setter
    def send_secondary_ip_range_if_empty(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__004a54875403cc2254f7cb7b6f0c691ea4841cc0025b7fbc89e748a37bb1e7c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendSecondaryIpRangeIfEmpty", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stackType")
    def stack_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stackType"))

    @stack_type.setter
    def stack_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcfe7050221f869a980a61de29f8f20442ccee3364b53112745ca6496d3cac28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stackType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSubnetwork.ComputeSubnetworkConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "network": "network",
        "description": "description",
        "enable_flow_logs": "enableFlowLogs",
        "external_ipv6_prefix": "externalIpv6Prefix",
        "id": "id",
        "ip_cidr_range": "ipCidrRange",
        "ip_collection": "ipCollection",
        "ipv6_access_type": "ipv6AccessType",
        "log_config": "logConfig",
        "params": "params",
        "private_ip_google_access": "privateIpGoogleAccess",
        "private_ipv6_google_access": "privateIpv6GoogleAccess",
        "project": "project",
        "purpose": "purpose",
        "region": "region",
        "reserved_internal_range": "reservedInternalRange",
        "role": "role",
        "secondary_ip_range": "secondaryIpRange",
        "send_secondary_ip_range_if_empty": "sendSecondaryIpRangeIfEmpty",
        "stack_type": "stackType",
        "timeouts": "timeouts",
    },
)
class ComputeSubnetworkConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        name: builtins.str,
        network: builtins.str,
        description: typing.Optional[builtins.str] = None,
        enable_flow_logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_ipv6_prefix: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_cidr_range: typing.Optional[builtins.str] = None,
        ip_collection: typing.Optional[builtins.str] = None,
        ipv6_access_type: typing.Optional[builtins.str] = None,
        log_config: typing.Optional[typing.Union["ComputeSubnetworkLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        params: typing.Optional[typing.Union["ComputeSubnetworkParams", typing.Dict[builtins.str, typing.Any]]] = None,
        private_ip_google_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_ipv6_google_access: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        purpose: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        reserved_internal_range: typing.Optional[builtins.str] = None,
        role: typing.Optional[builtins.str] = None,
        secondary_ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeSubnetworkSecondaryIpRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        send_secondary_ip_range_if_empty: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        stack_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeSubnetworkTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the resource, provided by the client when initially creating the resource. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#name ComputeSubnetwork#name}
        :param network: The network this subnet belongs to. Only networks that are in the distributed mode can have subnetworks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#network ComputeSubnetwork#network}
        :param description: An optional description of this resource. Provide this property when you create the resource. This field can be set only at resource creation time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#description ComputeSubnetwork#description}
        :param enable_flow_logs: Whether to enable flow logging for this subnetwork. If this field is not explicitly set, it will not appear in get listings. If not set the default behavior is determined by the org policy, if there is no org policy specified, then it will default to disabled. This field isn't supported if the subnet purpose field is set to REGIONAL_MANAGED_PROXY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#enable_flow_logs ComputeSubnetwork#enable_flow_logs}
        :param external_ipv6_prefix: The range of external IPv6 addresses that are owned by this subnetwork. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#external_ipv6_prefix ComputeSubnetwork#external_ipv6_prefix}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#id ComputeSubnetwork#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_cidr_range: The range of internal addresses that are owned by this subnetwork. Provide this property when you create the subnetwork. For example, 10.0.0.0/8 or 192.168.0.0/16. Ranges must be unique and non-overlapping within a network. Only IPv4 is supported. Field is optional when 'reserved_internal_range' is defined, otherwise required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#ip_cidr_range ComputeSubnetwork#ip_cidr_range}
        :param ip_collection: Resource reference of a PublicDelegatedPrefix. The PDP must be a sub-PDP in EXTERNAL_IPV6_SUBNETWORK_CREATION mode. Use one of the following formats to specify a sub-PDP when creating an IPv6 NetLB forwarding rule using BYOIP: Full resource URL, as in: - 'https://www.googleapis.com/compute/v1/projects/{{projectId}}/regions/{{region}}/publicDelegatedPrefixes/{{sub-pdp-name}}' Partial URL, as in: - 'projects/{{projectId}}/regions/region/publicDelegatedPrefixes/{{sub-pdp-name}}' - 'regions/{{region}}/publicDelegatedPrefixes/{{sub-pdp-name}}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#ip_collection ComputeSubnetwork#ip_collection}
        :param ipv6_access_type: The access type of IPv6 address this subnet holds. It's immutable and can only be specified during creation or the first time the subnet is updated into IPV4_IPV6 dual stack. If the ipv6_type is EXTERNAL then this subnet cannot enable direct path. Possible values: ["EXTERNAL", "INTERNAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#ipv6_access_type ComputeSubnetwork#ipv6_access_type}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#log_config ComputeSubnetwork#log_config}
        :param params: params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#params ComputeSubnetwork#params}
        :param private_ip_google_access: When enabled, VMs in this subnetwork without external IP addresses can access Google APIs and services by using Private Google Access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#private_ip_google_access ComputeSubnetwork#private_ip_google_access}
        :param private_ipv6_google_access: The private IPv6 google access type for the VMs in this subnet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#private_ipv6_google_access ComputeSubnetwork#private_ipv6_google_access}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#project ComputeSubnetwork#project}.
        :param purpose: The purpose of the resource. This field can be either 'PRIVATE', 'REGIONAL_MANAGED_PROXY', 'GLOBAL_MANAGED_PROXY', 'PRIVATE_SERVICE_CONNECT', 'PEER_MIGRATION' or 'PRIVATE_NAT'(`Beta <https://terraform.io/docs/providers/google/guides/provider_versions.html>`_). A subnet with purpose set to 'REGIONAL_MANAGED_PROXY' is a user-created subnetwork that is reserved for regional Envoy-based load balancers. A subnetwork in a given region with purpose set to 'GLOBAL_MANAGED_PROXY' is a proxy-only subnet and is shared between all the cross-regional Envoy-based load balancers. A subnetwork with purpose set to 'PRIVATE_SERVICE_CONNECT' reserves the subnet for hosting a Private Service Connect published service. A subnetwork with purpose set to 'PEER_MIGRATION' is a user created subnetwork that is reserved for migrating resources from one peered network to another. A subnetwork with purpose set to 'PRIVATE_NAT' is used as source range for Private NAT gateways. Note that 'REGIONAL_MANAGED_PROXY' is the preferred setting for all regional Envoy load balancers. If unspecified, the purpose defaults to 'PRIVATE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#purpose ComputeSubnetwork#purpose}
        :param region: The GCP region for this subnetwork. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#region ComputeSubnetwork#region}
        :param reserved_internal_range: The ID of the reserved internal range. Must be prefixed with 'networkconnectivity.googleapis.com' E.g. 'networkconnectivity.googleapis.com/projects/{project}/locations/global/internalRanges/{rangeId}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#reserved_internal_range ComputeSubnetwork#reserved_internal_range}
        :param role: The role of subnetwork. Currently, this field is only used when 'purpose' is 'REGIONAL_MANAGED_PROXY'. The value can be set to 'ACTIVE' or 'BACKUP'. An 'ACTIVE' subnetwork is one that is currently being used for Envoy-based load balancers in a region. A 'BACKUP' subnetwork is one that is ready to be promoted to 'ACTIVE' or is currently draining. Possible values: ["ACTIVE", "BACKUP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#role ComputeSubnetwork#role}
        :param secondary_ip_range: secondary_ip_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#secondary_ip_range ComputeSubnetwork#secondary_ip_range}
        :param send_secondary_ip_range_if_empty: Controls the removal behavior of secondary_ip_range. When false, removing secondary_ip_range from config will not produce a diff as the provider will default to the API's value. When true, the provider will treat removing secondary_ip_range as sending an empty list of secondary IP ranges to the API. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#send_secondary_ip_range_if_empty ComputeSubnetwork#send_secondary_ip_range_if_empty}
        :param stack_type: The stack type for this subnet to identify whether the IPv6 feature is enabled or not. If not specified IPV4_ONLY will be used. Possible values: ["IPV4_ONLY", "IPV4_IPV6", "IPV6_ONLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#stack_type ComputeSubnetwork#stack_type}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#timeouts ComputeSubnetwork#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(log_config, dict):
            log_config = ComputeSubnetworkLogConfig(**log_config)
        if isinstance(params, dict):
            params = ComputeSubnetworkParams(**params)
        if isinstance(timeouts, dict):
            timeouts = ComputeSubnetworkTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57fe536116c8c97bd7f1d3e816c1b715d826753e00563b003eb323f75b073e6f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_flow_logs", value=enable_flow_logs, expected_type=type_hints["enable_flow_logs"])
            check_type(argname="argument external_ipv6_prefix", value=external_ipv6_prefix, expected_type=type_hints["external_ipv6_prefix"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_cidr_range", value=ip_cidr_range, expected_type=type_hints["ip_cidr_range"])
            check_type(argname="argument ip_collection", value=ip_collection, expected_type=type_hints["ip_collection"])
            check_type(argname="argument ipv6_access_type", value=ipv6_access_type, expected_type=type_hints["ipv6_access_type"])
            check_type(argname="argument log_config", value=log_config, expected_type=type_hints["log_config"])
            check_type(argname="argument params", value=params, expected_type=type_hints["params"])
            check_type(argname="argument private_ip_google_access", value=private_ip_google_access, expected_type=type_hints["private_ip_google_access"])
            check_type(argname="argument private_ipv6_google_access", value=private_ipv6_google_access, expected_type=type_hints["private_ipv6_google_access"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument purpose", value=purpose, expected_type=type_hints["purpose"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument reserved_internal_range", value=reserved_internal_range, expected_type=type_hints["reserved_internal_range"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument secondary_ip_range", value=secondary_ip_range, expected_type=type_hints["secondary_ip_range"])
            check_type(argname="argument send_secondary_ip_range_if_empty", value=send_secondary_ip_range_if_empty, expected_type=type_hints["send_secondary_ip_range_if_empty"])
            check_type(argname="argument stack_type", value=stack_type, expected_type=type_hints["stack_type"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "network": network,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if description is not None:
            self._values["description"] = description
        if enable_flow_logs is not None:
            self._values["enable_flow_logs"] = enable_flow_logs
        if external_ipv6_prefix is not None:
            self._values["external_ipv6_prefix"] = external_ipv6_prefix
        if id is not None:
            self._values["id"] = id
        if ip_cidr_range is not None:
            self._values["ip_cidr_range"] = ip_cidr_range
        if ip_collection is not None:
            self._values["ip_collection"] = ip_collection
        if ipv6_access_type is not None:
            self._values["ipv6_access_type"] = ipv6_access_type
        if log_config is not None:
            self._values["log_config"] = log_config
        if params is not None:
            self._values["params"] = params
        if private_ip_google_access is not None:
            self._values["private_ip_google_access"] = private_ip_google_access
        if private_ipv6_google_access is not None:
            self._values["private_ipv6_google_access"] = private_ipv6_google_access
        if project is not None:
            self._values["project"] = project
        if purpose is not None:
            self._values["purpose"] = purpose
        if region is not None:
            self._values["region"] = region
        if reserved_internal_range is not None:
            self._values["reserved_internal_range"] = reserved_internal_range
        if role is not None:
            self._values["role"] = role
        if secondary_ip_range is not None:
            self._values["secondary_ip_range"] = secondary_ip_range
        if send_secondary_ip_range_if_empty is not None:
            self._values["send_secondary_ip_range_if_empty"] = send_secondary_ip_range_if_empty
        if stack_type is not None:
            self._values["stack_type"] = stack_type
        if timeouts is not None:
            self._values["timeouts"] = timeouts

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the resource, provided by the client when initially creating the resource.

        The name must be 1-63 characters long, and
        comply with RFC1035. Specifically, the name must be 1-63 characters
        long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which
        means the first character must be a lowercase letter, and all
        following characters must be a dash, lowercase letter, or digit,
        except the last character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#name ComputeSubnetwork#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network(self) -> builtins.str:
        '''The network this subnet belongs to. Only networks that are in the distributed mode can have subnetworks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#network ComputeSubnetwork#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Provide this property when
        you create the resource. This field can be set only at resource
        creation time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#description ComputeSubnetwork#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_flow_logs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to enable flow logging for this subnetwork.

        If this field is not explicitly set,
        it will not appear in get listings. If not set the default behavior is determined by the
        org policy, if there is no org policy specified, then it will default to disabled.
        This field isn't supported if the subnet purpose field is set to REGIONAL_MANAGED_PROXY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#enable_flow_logs ComputeSubnetwork#enable_flow_logs}
        '''
        result = self._values.get("enable_flow_logs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def external_ipv6_prefix(self) -> typing.Optional[builtins.str]:
        '''The range of external IPv6 addresses that are owned by this subnetwork.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#external_ipv6_prefix ComputeSubnetwork#external_ipv6_prefix}
        '''
        result = self._values.get("external_ipv6_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#id ComputeSubnetwork#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_cidr_range(self) -> typing.Optional[builtins.str]:
        '''The range of internal addresses that are owned by this subnetwork.

        Provide this property when you create the subnetwork. For example,
        10.0.0.0/8 or 192.168.0.0/16. Ranges must be unique and
        non-overlapping within a network. Only IPv4 is supported.
        Field is optional when 'reserved_internal_range' is defined, otherwise required.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#ip_cidr_range ComputeSubnetwork#ip_cidr_range}
        '''
        result = self._values.get("ip_cidr_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_collection(self) -> typing.Optional[builtins.str]:
        '''Resource reference of a PublicDelegatedPrefix.

        The PDP must be a sub-PDP
        in EXTERNAL_IPV6_SUBNETWORK_CREATION mode.
        Use one of the following formats to specify a sub-PDP when creating an
        IPv6 NetLB forwarding rule using BYOIP:
        Full resource URL, as in:

        - 'https://www.googleapis.com/compute/v1/projects/{{projectId}}/regions/{{region}}/publicDelegatedPrefixes/{{sub-pdp-name}}'
          Partial URL, as in:
        - 'projects/{{projectId}}/regions/region/publicDelegatedPrefixes/{{sub-pdp-name}}'
        - 'regions/{{region}}/publicDelegatedPrefixes/{{sub-pdp-name}}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#ip_collection ComputeSubnetwork#ip_collection}
        '''
        result = self._values.get("ip_collection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv6_access_type(self) -> typing.Optional[builtins.str]:
        '''The access type of IPv6 address this subnet holds.

        It's immutable and can only be specified during creation
        or the first time the subnet is updated into IPV4_IPV6 dual stack. If the ipv6_type is EXTERNAL then this subnet
        cannot enable direct path. Possible values: ["EXTERNAL", "INTERNAL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#ipv6_access_type ComputeSubnetwork#ipv6_access_type}
        '''
        result = self._values.get("ipv6_access_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_config(self) -> typing.Optional["ComputeSubnetworkLogConfig"]:
        '''log_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#log_config ComputeSubnetwork#log_config}
        '''
        result = self._values.get("log_config")
        return typing.cast(typing.Optional["ComputeSubnetworkLogConfig"], result)

    @builtins.property
    def params(self) -> typing.Optional["ComputeSubnetworkParams"]:
        '''params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#params ComputeSubnetwork#params}
        '''
        result = self._values.get("params")
        return typing.cast(typing.Optional["ComputeSubnetworkParams"], result)

    @builtins.property
    def private_ip_google_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled, VMs in this subnetwork without external IP addresses can access Google APIs and services by using Private Google Access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#private_ip_google_access ComputeSubnetwork#private_ip_google_access}
        '''
        result = self._values.get("private_ip_google_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def private_ipv6_google_access(self) -> typing.Optional[builtins.str]:
        '''The private IPv6 google access type for the VMs in this subnet.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#private_ipv6_google_access ComputeSubnetwork#private_ipv6_google_access}
        '''
        result = self._values.get("private_ipv6_google_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#project ComputeSubnetwork#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def purpose(self) -> typing.Optional[builtins.str]:
        '''The purpose of the resource.

        This field can be either 'PRIVATE', 'REGIONAL_MANAGED_PROXY', 'GLOBAL_MANAGED_PROXY', 'PRIVATE_SERVICE_CONNECT', 'PEER_MIGRATION' or 'PRIVATE_NAT'(`Beta <https://terraform.io/docs/providers/google/guides/provider_versions.html>`_).
        A subnet with purpose set to 'REGIONAL_MANAGED_PROXY' is a user-created subnetwork that is reserved for regional Envoy-based load balancers.
        A subnetwork in a given region with purpose set to 'GLOBAL_MANAGED_PROXY' is a proxy-only subnet and is shared between all the cross-regional Envoy-based load balancers.
        A subnetwork with purpose set to 'PRIVATE_SERVICE_CONNECT' reserves the subnet for hosting a Private Service Connect published service.
        A subnetwork with purpose set to 'PEER_MIGRATION' is a user created subnetwork that is reserved for migrating resources from one peered network to another.
        A subnetwork with purpose set to 'PRIVATE_NAT' is used as source range for Private NAT gateways.
        Note that 'REGIONAL_MANAGED_PROXY' is the preferred setting for all regional Envoy load balancers.
        If unspecified, the purpose defaults to 'PRIVATE'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#purpose ComputeSubnetwork#purpose}
        '''
        result = self._values.get("purpose")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The GCP region for this subnetwork.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#region ComputeSubnetwork#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reserved_internal_range(self) -> typing.Optional[builtins.str]:
        '''The ID of the reserved internal range. Must be prefixed with 'networkconnectivity.googleapis.com' E.g. 'networkconnectivity.googleapis.com/projects/{project}/locations/global/internalRanges/{rangeId}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#reserved_internal_range ComputeSubnetwork#reserved_internal_range}
        '''
        result = self._values.get("reserved_internal_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''The role of subnetwork.

        Currently, this field is only used when 'purpose' is 'REGIONAL_MANAGED_PROXY'.
        The value can be set to 'ACTIVE' or 'BACKUP'.
        An 'ACTIVE' subnetwork is one that is currently being used for Envoy-based load balancers in a region.
        A 'BACKUP' subnetwork is one that is ready to be promoted to 'ACTIVE' or is currently draining. Possible values: ["ACTIVE", "BACKUP"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#role ComputeSubnetwork#role}
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_ip_range(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSubnetworkSecondaryIpRange"]]]:
        '''secondary_ip_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#secondary_ip_range ComputeSubnetwork#secondary_ip_range}
        '''
        result = self._values.get("secondary_ip_range")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeSubnetworkSecondaryIpRange"]]], result)

    @builtins.property
    def send_secondary_ip_range_if_empty(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Controls the removal behavior of secondary_ip_range.

        When false, removing secondary_ip_range from config will not produce a diff as
        the provider will default to the API's value.
        When true, the provider will treat removing secondary_ip_range as sending an
        empty list of secondary IP ranges to the API.
        Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#send_secondary_ip_range_if_empty ComputeSubnetwork#send_secondary_ip_range_if_empty}
        '''
        result = self._values.get("send_secondary_ip_range_if_empty")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def stack_type(self) -> typing.Optional[builtins.str]:
        '''The stack type for this subnet to identify whether the IPv6 feature is enabled or not.

        If not specified IPV4_ONLY will be used. Possible values: ["IPV4_ONLY", "IPV4_IPV6", "IPV6_ONLY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#stack_type ComputeSubnetwork#stack_type}
        '''
        result = self._values.get("stack_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeSubnetworkTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#timeouts ComputeSubnetwork#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeSubnetworkTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSubnetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSubnetwork.ComputeSubnetworkLogConfig",
    jsii_struct_bases=[],
    name_mapping={
        "aggregation_interval": "aggregationInterval",
        "filter_expr": "filterExpr",
        "flow_sampling": "flowSampling",
        "metadata": "metadata",
        "metadata_fields": "metadataFields",
    },
)
class ComputeSubnetworkLogConfig:
    def __init__(
        self,
        *,
        aggregation_interval: typing.Optional[builtins.str] = None,
        filter_expr: typing.Optional[builtins.str] = None,
        flow_sampling: typing.Optional[jsii.Number] = None,
        metadata: typing.Optional[builtins.str] = None,
        metadata_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param aggregation_interval: Can only be specified if VPC flow logging for this subnetwork is enabled. Toggles the aggregation interval for collecting flow logs. Increasing the interval time will reduce the amount of generated flow logs for long lasting connections. Default is an interval of 5 seconds per connection. Default value: "INTERVAL_5_SEC" Possible values: ["INTERVAL_5_SEC", "INTERVAL_30_SEC", "INTERVAL_1_MIN", "INTERVAL_5_MIN", "INTERVAL_10_MIN", "INTERVAL_15_MIN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#aggregation_interval ComputeSubnetwork#aggregation_interval}
        :param filter_expr: Export filter used to define which VPC flow logs should be logged, as as CEL expression. See https://cloud.google.com/vpc/docs/flow-logs#filtering for details on how to format this field. The default value is 'true', which evaluates to include everything. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#filter_expr ComputeSubnetwork#filter_expr}
        :param flow_sampling: Can only be specified if VPC flow logging for this subnetwork is enabled. The value of the field must be in [0, 1]. Set the sampling rate of VPC flow logs within the subnetwork where 1.0 means all collected logs are reported and 0.0 means no logs are reported. Default is 0.5 which means half of all collected logs are reported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#flow_sampling ComputeSubnetwork#flow_sampling}
        :param metadata: Can only be specified if VPC flow logging for this subnetwork is enabled. Configures whether metadata fields should be added to the reported VPC flow logs. Default value: "INCLUDE_ALL_METADATA" Possible values: ["EXCLUDE_ALL_METADATA", "INCLUDE_ALL_METADATA", "CUSTOM_METADATA"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#metadata ComputeSubnetwork#metadata}
        :param metadata_fields: List of metadata fields that should be added to reported logs. Can only be specified if VPC flow logs for this subnetwork is enabled and "metadata" is set to CUSTOM_METADATA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#metadata_fields ComputeSubnetwork#metadata_fields}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08c6021542bbc73bf5dc755d04be7a976606ce52b7701669e1ff70c507f439eb)
            check_type(argname="argument aggregation_interval", value=aggregation_interval, expected_type=type_hints["aggregation_interval"])
            check_type(argname="argument filter_expr", value=filter_expr, expected_type=type_hints["filter_expr"])
            check_type(argname="argument flow_sampling", value=flow_sampling, expected_type=type_hints["flow_sampling"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument metadata_fields", value=metadata_fields, expected_type=type_hints["metadata_fields"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aggregation_interval is not None:
            self._values["aggregation_interval"] = aggregation_interval
        if filter_expr is not None:
            self._values["filter_expr"] = filter_expr
        if flow_sampling is not None:
            self._values["flow_sampling"] = flow_sampling
        if metadata is not None:
            self._values["metadata"] = metadata
        if metadata_fields is not None:
            self._values["metadata_fields"] = metadata_fields

    @builtins.property
    def aggregation_interval(self) -> typing.Optional[builtins.str]:
        '''Can only be specified if VPC flow logging for this subnetwork is enabled.

        Toggles the aggregation interval for collecting flow logs. Increasing the
        interval time will reduce the amount of generated flow logs for long
        lasting connections. Default is an interval of 5 seconds per connection. Default value: "INTERVAL_5_SEC" Possible values: ["INTERVAL_5_SEC", "INTERVAL_30_SEC", "INTERVAL_1_MIN", "INTERVAL_5_MIN", "INTERVAL_10_MIN", "INTERVAL_15_MIN"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#aggregation_interval ComputeSubnetwork#aggregation_interval}
        '''
        result = self._values.get("aggregation_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_expr(self) -> typing.Optional[builtins.str]:
        '''Export filter used to define which VPC flow logs should be logged, as as CEL expression.

        See
        https://cloud.google.com/vpc/docs/flow-logs#filtering for details on how to format this field.
        The default value is 'true', which evaluates to include everything.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#filter_expr ComputeSubnetwork#filter_expr}
        '''
        result = self._values.get("filter_expr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flow_sampling(self) -> typing.Optional[jsii.Number]:
        '''Can only be specified if VPC flow logging for this subnetwork is enabled.

        The value of the field must be in [0, 1]. Set the sampling rate of VPC
        flow logs within the subnetwork where 1.0 means all collected logs are
        reported and 0.0 means no logs are reported. Default is 0.5 which means
        half of all collected logs are reported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#flow_sampling ComputeSubnetwork#flow_sampling}
        '''
        result = self._values.get("flow_sampling")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metadata(self) -> typing.Optional[builtins.str]:
        '''Can only be specified if VPC flow logging for this subnetwork is enabled.

        Configures whether metadata fields should be added to the reported VPC
        flow logs. Default value: "INCLUDE_ALL_METADATA" Possible values: ["EXCLUDE_ALL_METADATA", "INCLUDE_ALL_METADATA", "CUSTOM_METADATA"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#metadata ComputeSubnetwork#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of metadata fields that should be added to reported logs.

        Can only be specified if VPC flow logs for this subnetwork is enabled and "metadata" is set to CUSTOM_METADATA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#metadata_fields ComputeSubnetwork#metadata_fields}
        '''
        result = self._values.get("metadata_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSubnetworkLogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSubnetworkLogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSubnetwork.ComputeSubnetworkLogConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b08be993cc6fd0651c25b3969678e663fc82b57b08889ee83b08474e89ba2dfe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAggregationInterval")
    def reset_aggregation_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregationInterval", []))

    @jsii.member(jsii_name="resetFilterExpr")
    def reset_filter_expr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterExpr", []))

    @jsii.member(jsii_name="resetFlowSampling")
    def reset_flow_sampling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlowSampling", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetMetadataFields")
    def reset_metadata_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataFields", []))

    @builtins.property
    @jsii.member(jsii_name="aggregationIntervalInput")
    def aggregation_interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aggregationIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="filterExprInput")
    def filter_expr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterExprInput"))

    @builtins.property
    @jsii.member(jsii_name="flowSamplingInput")
    def flow_sampling_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "flowSamplingInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataFieldsInput")
    def metadata_fields_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "metadataFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregationInterval")
    def aggregation_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aggregationInterval"))

    @aggregation_interval.setter
    def aggregation_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa9b9e10df19b85443d543c3bf2855c673e396634b0e9218de03dba3c1445ae3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregationInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterExpr")
    def filter_expr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterExpr"))

    @filter_expr.setter
    def filter_expr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4de5fa722e393433651f5404bd81fd843d6c1b79ea3475012c3ee78aa53a4e31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterExpr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flowSampling")
    def flow_sampling(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "flowSampling"))

    @flow_sampling.setter
    def flow_sampling(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d69dad9f173c196b46de727a7624c6889faa3d75e85186796a5016fb563c7e97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flowSampling", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7baf4024b6eee7b1c11fdf870db1e0011f422663c1753f19c19ccd56d1c3695a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadataFields")
    def metadata_fields(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "metadataFields"))

    @metadata_fields.setter
    def metadata_fields(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__971c5142c3c80f2c49b32a4db581bca831e4efc2636b7c1bdc753553477ab5c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataFields", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeSubnetworkLogConfig]:
        return typing.cast(typing.Optional[ComputeSubnetworkLogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeSubnetworkLogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__918c18bf617e0cee8f14f11c62a747b29049365142ebe70dde543497a899dc62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSubnetwork.ComputeSubnetworkParams",
    jsii_struct_bases=[],
    name_mapping={"resource_manager_tags": "resourceManagerTags"},
)
class ComputeSubnetworkParams:
    def __init__(
        self,
        *,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param resource_manager_tags: Resource manager tags to be bound to the subnetwork. Tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored when empty. The field is immutable and causes resource replacement when mutated. This field is only set at create time and modifying this field after creation will trigger recreation. To apply tags to an existing resource, see the google_tags_tag_binding resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#resource_manager_tags ComputeSubnetwork#resource_manager_tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__680b1a568f4a4b44efe9075d6373b5ab34415f0874a621edff2aa2cfdf8b2c65)
            check_type(argname="argument resource_manager_tags", value=resource_manager_tags, expected_type=type_hints["resource_manager_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_manager_tags is not None:
            self._values["resource_manager_tags"] = resource_manager_tags

    @builtins.property
    def resource_manager_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Resource manager tags to be bound to the subnetwork.

        Tag keys and values have the
        same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id},
        and values are in the format tagValues/456. The field is ignored when empty.
        The field is immutable and causes resource replacement when mutated. This field is only
        set at create time and modifying this field after creation will trigger recreation.
        To apply tags to an existing resource, see the google_tags_tag_binding resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#resource_manager_tags ComputeSubnetwork#resource_manager_tags}
        '''
        result = self._values.get("resource_manager_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSubnetworkParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSubnetworkParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSubnetwork.ComputeSubnetworkParamsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ac6b5150e130ec28c694264147f84485f7d7e0199b1c512a4569079eae7b0f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetResourceManagerTags")
    def reset_resource_manager_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceManagerTags", []))

    @builtins.property
    @jsii.member(jsii_name="resourceManagerTagsInput")
    def resource_manager_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "resourceManagerTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceManagerTags")
    def resource_manager_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "resourceManagerTags"))

    @resource_manager_tags.setter
    def resource_manager_tags(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b83e61afa1e398f25733b0c2a785a9f5987c5e51059b0a0335368f38d446a115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceManagerTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeSubnetworkParams]:
        return typing.cast(typing.Optional[ComputeSubnetworkParams], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ComputeSubnetworkParams]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b2b20031f7320f4701d868c6694c867785219c2c92ad85cbdd4f2b06186ba4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSubnetwork.ComputeSubnetworkSecondaryIpRange",
    jsii_struct_bases=[],
    name_mapping={
        "range_name": "rangeName",
        "ip_cidr_range": "ipCidrRange",
        "reserved_internal_range": "reservedInternalRange",
    },
)
class ComputeSubnetworkSecondaryIpRange:
    def __init__(
        self,
        *,
        range_name: builtins.str,
        ip_cidr_range: typing.Optional[builtins.str] = None,
        reserved_internal_range: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param range_name: The name associated with this subnetwork secondary range, used when adding an alias IP range to a VM instance. The name must be 1-63 characters long, and comply with RFC1035. The name must be unique within the subnetwork. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#range_name ComputeSubnetwork#range_name}
        :param ip_cidr_range: The range of IP addresses belonging to this subnetwork secondary range. Provide this property when you create the subnetwork. Ranges must be unique and non-overlapping with all primary and secondary IP ranges within a network. Only IPv4 is supported. Field is optional when 'reserved_internal_range' is defined, otherwise required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#ip_cidr_range ComputeSubnetwork#ip_cidr_range}
        :param reserved_internal_range: The ID of the reserved internal range. Must be prefixed with 'networkconnectivity.googleapis.com' E.g. 'networkconnectivity.googleapis.com/projects/{project}/locations/global/internalRanges/{rangeId}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#reserved_internal_range ComputeSubnetwork#reserved_internal_range}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c664771b99c4fc96f80c4281bbf01a2ad29dd472eea04a1265cd37929a6450f)
            check_type(argname="argument range_name", value=range_name, expected_type=type_hints["range_name"])
            check_type(argname="argument ip_cidr_range", value=ip_cidr_range, expected_type=type_hints["ip_cidr_range"])
            check_type(argname="argument reserved_internal_range", value=reserved_internal_range, expected_type=type_hints["reserved_internal_range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "range_name": range_name,
        }
        if ip_cidr_range is not None:
            self._values["ip_cidr_range"] = ip_cidr_range
        if reserved_internal_range is not None:
            self._values["reserved_internal_range"] = reserved_internal_range

    @builtins.property
    def range_name(self) -> builtins.str:
        '''The name associated with this subnetwork secondary range, used when adding an alias IP range to a VM instance.

        The name must
        be 1-63 characters long, and comply with RFC1035. The name
        must be unique within the subnetwork.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#range_name ComputeSubnetwork#range_name}
        '''
        result = self._values.get("range_name")
        assert result is not None, "Required property 'range_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_cidr_range(self) -> typing.Optional[builtins.str]:
        '''The range of IP addresses belonging to this subnetwork secondary range.

        Provide this property when you create the subnetwork.
        Ranges must be unique and non-overlapping with all primary and
        secondary IP ranges within a network. Only IPv4 is supported.
        Field is optional when 'reserved_internal_range' is defined, otherwise required.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#ip_cidr_range ComputeSubnetwork#ip_cidr_range}
        '''
        result = self._values.get("ip_cidr_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reserved_internal_range(self) -> typing.Optional[builtins.str]:
        '''The ID of the reserved internal range. Must be prefixed with 'networkconnectivity.googleapis.com' E.g. 'networkconnectivity.googleapis.com/projects/{project}/locations/global/internalRanges/{rangeId}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#reserved_internal_range ComputeSubnetwork#reserved_internal_range}
        '''
        result = self._values.get("reserved_internal_range")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSubnetworkSecondaryIpRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSubnetworkSecondaryIpRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSubnetwork.ComputeSubnetworkSecondaryIpRangeList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bedff57297ecc1d345bb499ed8a486431761b3c535223e69e7548d02a271592)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeSubnetworkSecondaryIpRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83dbf523bfdb0ec8fe31b18acdf3d983739ab95e3a8dbad0630110693bf1de18)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeSubnetworkSecondaryIpRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffe227d7ccbaeee15d4dcc9c15de4082d274480984311e9addbceda344eea922)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87449a53b448a0cb73d8367362681a16bbd31e77826149268ec1160e519e4cfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95d8ef14e9543f6f4418f5dec405580b26d9580fac2d78d3cb9f6342ab6ecbf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSubnetworkSecondaryIpRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSubnetworkSecondaryIpRange]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSubnetworkSecondaryIpRange]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf7cc8867c8c001fcaced80f67be11719d30bd2c2e18994062593ad114bf1e61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeSubnetworkSecondaryIpRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSubnetwork.ComputeSubnetworkSecondaryIpRangeOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00ddd0df506ff2a0f6c7695554aa20cfb83027b236522b5177d3b20dd82ba84e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIpCidrRange")
    def reset_ip_cidr_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpCidrRange", []))

    @jsii.member(jsii_name="resetReservedInternalRange")
    def reset_reserved_internal_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservedInternalRange", []))

    @builtins.property
    @jsii.member(jsii_name="ipCidrRangeInput")
    def ip_cidr_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipCidrRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeNameInput")
    def range_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rangeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="reservedInternalRangeInput")
    def reserved_internal_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reservedInternalRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="ipCidrRange")
    def ip_cidr_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipCidrRange"))

    @ip_cidr_range.setter
    def ip_cidr_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc9bdb74e0c9ad0a1f88f0f5f18807ce48fbf810a3f05262268368a9263173ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipCidrRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rangeName")
    def range_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rangeName"))

    @range_name.setter
    def range_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__492e0440b6590be865f6b27c698885f00d4bc260643a0ca77a54340ba470dc35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rangeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reservedInternalRange")
    def reserved_internal_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reservedInternalRange"))

    @reserved_internal_range.setter
    def reserved_internal_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f050ea8469be18345da640847a2667d7b5a5f1e8c80b3273dd92e876ee2a7fcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservedInternalRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSubnetworkSecondaryIpRange]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSubnetworkSecondaryIpRange]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSubnetworkSecondaryIpRange]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__123aa63e704fbff095894cc630ed44653c5079fdc4fecc5e37aaaae0499fd881)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeSubnetwork.ComputeSubnetworkTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeSubnetworkTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#create ComputeSubnetwork#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#delete ComputeSubnetwork#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#update ComputeSubnetwork#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__974314b2200fdab8d8a76495f2e0edf0085798899912f6caa1fa5687e903fb49)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#create ComputeSubnetwork#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#delete ComputeSubnetwork#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_subnetwork#update ComputeSubnetwork#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeSubnetworkTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeSubnetworkTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeSubnetwork.ComputeSubnetworkTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a24718479b1037024f01eb5c2bb05a11d9f3a5b7bce10cd234c35aa9785e36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09d69f13a79c7d6d057c652593d870f1ab065ecbec78ce3066fd2ab121ac04ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60a3063c3e917bb7990644bf19e4454ecef85da51c4e44b10589f0b085a9a4a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58921f01794b8a43896d6a13de53eb84407666bc75b3ddd0e0c1b3d4c589692b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSubnetworkTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSubnetworkTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSubnetworkTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b34934cf7baa70030433a35b7c79e9006ad906875c223fd79af15217278ac04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeSubnetwork",
    "ComputeSubnetworkConfig",
    "ComputeSubnetworkLogConfig",
    "ComputeSubnetworkLogConfigOutputReference",
    "ComputeSubnetworkParams",
    "ComputeSubnetworkParamsOutputReference",
    "ComputeSubnetworkSecondaryIpRange",
    "ComputeSubnetworkSecondaryIpRangeList",
    "ComputeSubnetworkSecondaryIpRangeOutputReference",
    "ComputeSubnetworkTimeouts",
    "ComputeSubnetworkTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__01fd1c59fbdcd905b899f4bc7d27175967e82edddf94d2b4fde01f211ebeb0e0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    network: builtins.str,
    description: typing.Optional[builtins.str] = None,
    enable_flow_logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_ipv6_prefix: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_cidr_range: typing.Optional[builtins.str] = None,
    ip_collection: typing.Optional[builtins.str] = None,
    ipv6_access_type: typing.Optional[builtins.str] = None,
    log_config: typing.Optional[typing.Union[ComputeSubnetworkLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    params: typing.Optional[typing.Union[ComputeSubnetworkParams, typing.Dict[builtins.str, typing.Any]]] = None,
    private_ip_google_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_ipv6_google_access: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    purpose: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    reserved_internal_range: typing.Optional[builtins.str] = None,
    role: typing.Optional[builtins.str] = None,
    secondary_ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSubnetworkSecondaryIpRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
    send_secondary_ip_range_if_empty: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    stack_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeSubnetworkTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__031a7c53cbbac42bac029930c8f0b7c8b95c6b044ddf91faa0a8d5c4b834d1e6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad28ca287c36ce160f111925adccb0f84f9aba4d09bb520316167bce929b9795(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSubnetworkSecondaryIpRange, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86bad37f5c67c7afd2233f46410b3f8f28bec0e613b1a74d141375d7e6d62b39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f701d7f23bb1bbc9e19d7c0d47339b7d3f0b6669e91b99d61d8d0e4c716c287(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b72d44f871993033179b8ca28f1444e5adb8301b5218c5b388875530564b2c3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d080d26436de885eddb22c28df35b51d9916ac6f6caf549d4892759693e0a7c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ebf3a83259961af9502d2a2ac40d29be32471d7f85a700c8e68c96ba756c20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__445cdee46239834b389c4ca7027de593dd781278f0e464f888276dac37660fad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3be079515323e0453d5620d393bf9096a1f15feb029d7808e2e9f51981e2075b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e66b56122974ea4e216fdf396fd774abfc6f1eeb195ee4be091c5f500a1f884(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0ec593bcba254fe1159921d7be42cea751a07ba1eac8c35fc1cb421160b83b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a402ba23908fbbb7b6d530fbf646e1510e3d3c654755bf94ccb74483ece916c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6acb602e4fb08411793ffe3147e6b3b37f0cd9bc3e72a674067325a0ce84ff3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a9e071fd98237c230795d301adcc09a1591aeb401ef656afd9c2e1f6dab65e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244cd42cc57e180dbcf8317d170227ce000ce6a71d17c55f4c43eb98b6ae18a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b877e4e78db1787f7706bb059c38da47877f7bc75be426b17d0d49fe1001f7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70782ebfac80c688953c975faad7b02e23991f8e53d60758dfacd22b679411a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5438473aba032b02489e8f51a6798405708ea87f592b69ef25b4c14a8049865(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__004a54875403cc2254f7cb7b6f0c691ea4841cc0025b7fbc89e748a37bb1e7c5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcfe7050221f869a980a61de29f8f20442ccee3364b53112745ca6496d3cac28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57fe536116c8c97bd7f1d3e816c1b715d826753e00563b003eb323f75b073e6f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    network: builtins.str,
    description: typing.Optional[builtins.str] = None,
    enable_flow_logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_ipv6_prefix: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_cidr_range: typing.Optional[builtins.str] = None,
    ip_collection: typing.Optional[builtins.str] = None,
    ipv6_access_type: typing.Optional[builtins.str] = None,
    log_config: typing.Optional[typing.Union[ComputeSubnetworkLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    params: typing.Optional[typing.Union[ComputeSubnetworkParams, typing.Dict[builtins.str, typing.Any]]] = None,
    private_ip_google_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_ipv6_google_access: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    purpose: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    reserved_internal_range: typing.Optional[builtins.str] = None,
    role: typing.Optional[builtins.str] = None,
    secondary_ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeSubnetworkSecondaryIpRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
    send_secondary_ip_range_if_empty: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    stack_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeSubnetworkTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08c6021542bbc73bf5dc755d04be7a976606ce52b7701669e1ff70c507f439eb(
    *,
    aggregation_interval: typing.Optional[builtins.str] = None,
    filter_expr: typing.Optional[builtins.str] = None,
    flow_sampling: typing.Optional[jsii.Number] = None,
    metadata: typing.Optional[builtins.str] = None,
    metadata_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b08be993cc6fd0651c25b3969678e663fc82b57b08889ee83b08474e89ba2dfe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa9b9e10df19b85443d543c3bf2855c673e396634b0e9218de03dba3c1445ae3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4de5fa722e393433651f5404bd81fd843d6c1b79ea3475012c3ee78aa53a4e31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d69dad9f173c196b46de727a7624c6889faa3d75e85186796a5016fb563c7e97(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7baf4024b6eee7b1c11fdf870db1e0011f422663c1753f19c19ccd56d1c3695a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__971c5142c3c80f2c49b32a4db581bca831e4efc2636b7c1bdc753553477ab5c5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__918c18bf617e0cee8f14f11c62a747b29049365142ebe70dde543497a899dc62(
    value: typing.Optional[ComputeSubnetworkLogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__680b1a568f4a4b44efe9075d6373b5ab34415f0874a621edff2aa2cfdf8b2c65(
    *,
    resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ac6b5150e130ec28c694264147f84485f7d7e0199b1c512a4569079eae7b0f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83e61afa1e398f25733b0c2a785a9f5987c5e51059b0a0335368f38d446a115(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b2b20031f7320f4701d868c6694c867785219c2c92ad85cbdd4f2b06186ba4b(
    value: typing.Optional[ComputeSubnetworkParams],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c664771b99c4fc96f80c4281bbf01a2ad29dd472eea04a1265cd37929a6450f(
    *,
    range_name: builtins.str,
    ip_cidr_range: typing.Optional[builtins.str] = None,
    reserved_internal_range: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bedff57297ecc1d345bb499ed8a486431761b3c535223e69e7548d02a271592(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83dbf523bfdb0ec8fe31b18acdf3d983739ab95e3a8dbad0630110693bf1de18(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffe227d7ccbaeee15d4dcc9c15de4082d274480984311e9addbceda344eea922(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87449a53b448a0cb73d8367362681a16bbd31e77826149268ec1160e519e4cfa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d8ef14e9543f6f4418f5dec405580b26d9580fac2d78d3cb9f6342ab6ecbf3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf7cc8867c8c001fcaced80f67be11719d30bd2c2e18994062593ad114bf1e61(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeSubnetworkSecondaryIpRange]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ddd0df506ff2a0f6c7695554aa20cfb83027b236522b5177d3b20dd82ba84e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc9bdb74e0c9ad0a1f88f0f5f18807ce48fbf810a3f05262268368a9263173ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492e0440b6590be865f6b27c698885f00d4bc260643a0ca77a54340ba470dc35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f050ea8469be18345da640847a2667d7b5a5f1e8c80b3273dd92e876ee2a7fcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123aa63e704fbff095894cc630ed44653c5079fdc4fecc5e37aaaae0499fd881(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSubnetworkSecondaryIpRange]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__974314b2200fdab8d8a76495f2e0edf0085798899912f6caa1fa5687e903fb49(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a24718479b1037024f01eb5c2bb05a11d9f3a5b7bce10cd234c35aa9785e36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d69f13a79c7d6d057c652593d870f1ab065ecbec78ce3066fd2ab121ac04ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60a3063c3e917bb7990644bf19e4454ecef85da51c4e44b10589f0b085a9a4a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58921f01794b8a43896d6a13de53eb84407666bc75b3ddd0e0c1b3d4c589692b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b34934cf7baa70030433a35b7c79e9006ad906875c223fd79af15217278ac04(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeSubnetworkTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
