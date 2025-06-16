r'''
# `google_compute_subnetwork`

Refer to the Terraform Registry for docs: [`google_compute_subnetwork`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork).
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


class GoogleComputeSubnetwork(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSubnetwork.GoogleComputeSubnetwork",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork google_compute_subnetwork}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        network: builtins.str,
        allow_subnet_cidr_routes_overlap: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_flow_logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_ipv6_prefix: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_cidr_range: typing.Optional[builtins.str] = None,
        ip_collection: typing.Optional[builtins.str] = None,
        ipv6_access_type: typing.Optional[builtins.str] = None,
        log_config: typing.Optional[typing.Union["GoogleComputeSubnetworkLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        private_ip_google_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_ipv6_google_access: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        purpose: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        reserved_internal_range: typing.Optional[builtins.str] = None,
        role: typing.Optional[builtins.str] = None,
        secondary_ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSubnetworkSecondaryIpRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        send_secondary_ip_range_if_empty: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        stack_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeSubnetworkTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork google_compute_subnetwork} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the resource, provided by the client when initially creating the resource. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#name GoogleComputeSubnetwork#name}
        :param network: The network this subnet belongs to. Only networks that are in the distributed mode can have subnetworks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#network GoogleComputeSubnetwork#network}
        :param allow_subnet_cidr_routes_overlap: Typically packets destined to IPs within the subnetwork range that do not match existing resources are dropped and prevented from leaving the VPC. Setting this field to true will allow these packets to match dynamic routes injected via BGP even if their destinations match existing subnet ranges. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#allow_subnet_cidr_routes_overlap GoogleComputeSubnetwork#allow_subnet_cidr_routes_overlap}
        :param description: An optional description of this resource. Provide this property when you create the resource. This field can be set only at resource creation time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#description GoogleComputeSubnetwork#description}
        :param enable_flow_logs: Whether to enable flow logging for this subnetwork. If this field is not explicitly set, it will not appear in get listings. If not set the default behavior is determined by the org policy, if there is no org policy specified, then it will default to disabled. This field isn't supported if the subnet purpose field is set to REGIONAL_MANAGED_PROXY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#enable_flow_logs GoogleComputeSubnetwork#enable_flow_logs}
        :param external_ipv6_prefix: The range of external IPv6 addresses that are owned by this subnetwork. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#external_ipv6_prefix GoogleComputeSubnetwork#external_ipv6_prefix}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#id GoogleComputeSubnetwork#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_cidr_range: The range of internal addresses that are owned by this subnetwork. Provide this property when you create the subnetwork. For example, 10.0.0.0/8 or 192.168.0.0/16. Ranges must be unique and non-overlapping within a network. Only IPv4 is supported. Field is optional when 'reserved_internal_range' is defined, otherwise required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#ip_cidr_range GoogleComputeSubnetwork#ip_cidr_range}
        :param ip_collection: Resource reference of a PublicDelegatedPrefix. The PDP must be a sub-PDP in EXTERNAL_IPV6_SUBNETWORK_CREATION mode. Use one of the following formats to specify a sub-PDP when creating an IPv6 NetLB forwarding rule using BYOIP: Full resource URL, as in: - 'https://www.googleapis.com/compute/v1/projects/{{projectId}}/regions/{{region}}/publicDelegatedPrefixes/{{sub-pdp-name}}' Partial URL, as in: - 'projects/{{projectId}}/regions/region/publicDelegatedPrefixes/{{sub-pdp-name}}' - 'regions/{{region}}/publicDelegatedPrefixes/{{sub-pdp-name}}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#ip_collection GoogleComputeSubnetwork#ip_collection}
        :param ipv6_access_type: The access type of IPv6 address this subnet holds. It's immutable and can only be specified during creation or the first time the subnet is updated into IPV4_IPV6 dual stack. If the ipv6_type is EXTERNAL then this subnet cannot enable direct path. Possible values: ["EXTERNAL", "INTERNAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#ipv6_access_type GoogleComputeSubnetwork#ipv6_access_type}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#log_config GoogleComputeSubnetwork#log_config}
        :param private_ip_google_access: When enabled, VMs in this subnetwork without external IP addresses can access Google APIs and services by using Private Google Access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#private_ip_google_access GoogleComputeSubnetwork#private_ip_google_access}
        :param private_ipv6_google_access: The private IPv6 google access type for the VMs in this subnet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#private_ipv6_google_access GoogleComputeSubnetwork#private_ipv6_google_access}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#project GoogleComputeSubnetwork#project}.
        :param purpose: The purpose of the resource. This field can be either 'PRIVATE', 'REGIONAL_MANAGED_PROXY', 'GLOBAL_MANAGED_PROXY', 'PRIVATE_SERVICE_CONNECT', 'PEER_MIGRATION' or 'PRIVATE_NAT'(`Beta <https://terraform.io/docs/providers/google/guides/provider_versions.html>`_). A subnet with purpose set to 'REGIONAL_MANAGED_PROXY' is a user-created subnetwork that is reserved for regional Envoy-based load balancers. A subnetwork in a given region with purpose set to 'GLOBAL_MANAGED_PROXY' is a proxy-only subnet and is shared between all the cross-regional Envoy-based load balancers. A subnetwork with purpose set to 'PRIVATE_SERVICE_CONNECT' reserves the subnet for hosting a Private Service Connect published service. A subnetwork with purpose set to 'PEER_MIGRATION' is a user created subnetwork that is reserved for migrating resources from one peered network to another. A subnetwork with purpose set to 'PRIVATE_NAT' is used as source range for Private NAT gateways. Note that 'REGIONAL_MANAGED_PROXY' is the preferred setting for all regional Envoy load balancers. If unspecified, the purpose defaults to 'PRIVATE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#purpose GoogleComputeSubnetwork#purpose}
        :param region: The GCP region for this subnetwork. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#region GoogleComputeSubnetwork#region}
        :param reserved_internal_range: The ID of the reserved internal range. Must be prefixed with 'networkconnectivity.googleapis.com' E.g. 'networkconnectivity.googleapis.com/projects/{project}/locations/global/internalRanges/{rangeId}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#reserved_internal_range GoogleComputeSubnetwork#reserved_internal_range}
        :param role: The role of subnetwork. Currently, this field is only used when 'purpose' is 'REGIONAL_MANAGED_PROXY'. The value can be set to 'ACTIVE' or 'BACKUP'. An 'ACTIVE' subnetwork is one that is currently being used for Envoy-based load balancers in a region. A 'BACKUP' subnetwork is one that is ready to be promoted to 'ACTIVE' or is currently draining. Possible values: ["ACTIVE", "BACKUP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#role GoogleComputeSubnetwork#role}
        :param secondary_ip_range: secondary_ip_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#secondary_ip_range GoogleComputeSubnetwork#secondary_ip_range}
        :param send_secondary_ip_range_if_empty: Controls the removal behavior of secondary_ip_range. When false, removing secondary_ip_range from config will not produce a diff as the provider will default to the API's value. When true, the provider will treat removing secondary_ip_range as sending an empty list of secondary IP ranges to the API. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#send_secondary_ip_range_if_empty GoogleComputeSubnetwork#send_secondary_ip_range_if_empty}
        :param stack_type: The stack type for this subnet to identify whether the IPv6 feature is enabled or not. If not specified IPV4_ONLY will be used. Possible values: ["IPV4_ONLY", "IPV4_IPV6", "IPV6_ONLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#stack_type GoogleComputeSubnetwork#stack_type}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#timeouts GoogleComputeSubnetwork#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa2e0719972ae42ff6668cc201c87b78c5aad82b2d6be09df14ab5cc3cd06b39)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleComputeSubnetworkConfig(
            name=name,
            network=network,
            allow_subnet_cidr_routes_overlap=allow_subnet_cidr_routes_overlap,
            description=description,
            enable_flow_logs=enable_flow_logs,
            external_ipv6_prefix=external_ipv6_prefix,
            id=id,
            ip_cidr_range=ip_cidr_range,
            ip_collection=ip_collection,
            ipv6_access_type=ipv6_access_type,
            log_config=log_config,
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
        '''Generates CDKTF code for importing a GoogleComputeSubnetwork resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleComputeSubnetwork to import.
        :param import_from_id: The id of the existing GoogleComputeSubnetwork that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleComputeSubnetwork to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7722aaa7e6b59faf27e3bc2d0471ba428a9072ddd94a92cfda44c5629974f7f1)
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
        :param aggregation_interval: Can only be specified if VPC flow logging for this subnetwork is enabled. Toggles the aggregation interval for collecting flow logs. Increasing the interval time will reduce the amount of generated flow logs for long lasting connections. Default is an interval of 5 seconds per connection. Default value: "INTERVAL_5_SEC" Possible values: ["INTERVAL_5_SEC", "INTERVAL_30_SEC", "INTERVAL_1_MIN", "INTERVAL_5_MIN", "INTERVAL_10_MIN", "INTERVAL_15_MIN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#aggregation_interval GoogleComputeSubnetwork#aggregation_interval}
        :param filter_expr: Export filter used to define which VPC flow logs should be logged, as as CEL expression. See https://cloud.google.com/vpc/docs/flow-logs#filtering for details on how to format this field. The default value is 'true', which evaluates to include everything. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#filter_expr GoogleComputeSubnetwork#filter_expr}
        :param flow_sampling: Can only be specified if VPC flow logging for this subnetwork is enabled. The value of the field must be in [0, 1]. Set the sampling rate of VPC flow logs within the subnetwork where 1.0 means all collected logs are reported and 0.0 means no logs are reported. Default is 0.5 which means half of all collected logs are reported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#flow_sampling GoogleComputeSubnetwork#flow_sampling}
        :param metadata: Can only be specified if VPC flow logging for this subnetwork is enabled. Configures whether metadata fields should be added to the reported VPC flow logs. Default value: "INCLUDE_ALL_METADATA" Possible values: ["EXCLUDE_ALL_METADATA", "INCLUDE_ALL_METADATA", "CUSTOM_METADATA"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#metadata GoogleComputeSubnetwork#metadata}
        :param metadata_fields: List of metadata fields that should be added to reported logs. Can only be specified if VPC flow logs for this subnetwork is enabled and "metadata" is set to CUSTOM_METADATA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#metadata_fields GoogleComputeSubnetwork#metadata_fields}
        '''
        value = GoogleComputeSubnetworkLogConfig(
            aggregation_interval=aggregation_interval,
            filter_expr=filter_expr,
            flow_sampling=flow_sampling,
            metadata=metadata,
            metadata_fields=metadata_fields,
        )

        return typing.cast(None, jsii.invoke(self, "putLogConfig", [value]))

    @jsii.member(jsii_name="putSecondaryIpRange")
    def put_secondary_ip_range(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSubnetworkSecondaryIpRange", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe6c6b14b8ba2dd51c9d40d983416bf9bb35d9886f27ccde949ef6d883361413)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#create GoogleComputeSubnetwork#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#delete GoogleComputeSubnetwork#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#update GoogleComputeSubnetwork#update}.
        '''
        value = GoogleComputeSubnetworkTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAllowSubnetCidrRoutesOverlap")
    def reset_allow_subnet_cidr_routes_overlap(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowSubnetCidrRoutesOverlap", []))

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
    def log_config(self) -> "GoogleComputeSubnetworkLogConfigOutputReference":
        return typing.cast("GoogleComputeSubnetworkLogConfigOutputReference", jsii.get(self, "logConfig"))

    @builtins.property
    @jsii.member(jsii_name="secondaryIpRange")
    def secondary_ip_range(self) -> "GoogleComputeSubnetworkSecondaryIpRangeList":
        return typing.cast("GoogleComputeSubnetworkSecondaryIpRangeList", jsii.get(self, "secondaryIpRange"))

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
    def timeouts(self) -> "GoogleComputeSubnetworkTimeoutsOutputReference":
        return typing.cast("GoogleComputeSubnetworkTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="allowSubnetCidrRoutesOverlapInput")
    def allow_subnet_cidr_routes_overlap_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowSubnetCidrRoutesOverlapInput"))

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
    def log_config_input(self) -> typing.Optional["GoogleComputeSubnetworkLogConfig"]:
        return typing.cast(typing.Optional["GoogleComputeSubnetworkLogConfig"], jsii.get(self, "logConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSubnetworkSecondaryIpRange"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSubnetworkSecondaryIpRange"]]], jsii.get(self, "secondaryIpRangeInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeSubnetworkTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeSubnetworkTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowSubnetCidrRoutesOverlap")
    def allow_subnet_cidr_routes_overlap(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowSubnetCidrRoutesOverlap"))

    @allow_subnet_cidr_routes_overlap.setter
    def allow_subnet_cidr_routes_overlap(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b6a06212198ad0392ae2928dbdeca2d56ced3ed96bdf66afc382ef96d97ba27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowSubnetCidrRoutesOverlap", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f72ae70a4f18794ead2a169c0b75ed75c5cfb403a175e33a16d520b5d481a8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c580cf60946bbd4f68895a1efb6399cb47d3020082f3a23c2584b895d49c6ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableFlowLogs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalIpv6Prefix")
    def external_ipv6_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalIpv6Prefix"))

    @external_ipv6_prefix.setter
    def external_ipv6_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5ddd22956b8bef78afea6d030da61bfae1a038004b54e257581b2e48060ffb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalIpv6Prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a5e64c3b5d7bfe323deb9fba25479614e83cd60146f6116faeef78bffae8ea3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipCidrRange")
    def ip_cidr_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipCidrRange"))

    @ip_cidr_range.setter
    def ip_cidr_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f6ab889de10b13b40bcbeb39b423a3f59295c461a4e72b36260fb4e509604de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipCidrRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipCollection")
    def ip_collection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipCollection"))

    @ip_collection.setter
    def ip_collection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edbe39a711aee6b54bddfcb46989443958fdcab942d485ed81de0da83ce8270a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipCollection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv6AccessType")
    def ipv6_access_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6AccessType"))

    @ipv6_access_type.setter
    def ipv6_access_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d4b70825c7f90b057cffe25b6fd40d2de58deffbbcc32db60053dd529485bde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6AccessType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b3f4d4b5d081e2b8eb9e9708ed6fa83cf5d23e3a78b567de172fd86fe3bbaaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80078676d805c96993b70a704c9e4e92d02239805ae3ad3730eafa7c847d7e66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1eeeca86bcaf77b744e79ebab0757f8b1145035beb77dafa5d35077c33f01af0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpGoogleAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIpv6GoogleAccess")
    def private_ipv6_google_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpv6GoogleAccess"))

    @private_ipv6_google_access.setter
    def private_ipv6_google_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5621ea0d6b532984da9956a79c9a543c7306ac51db7b968795915bf9f58abde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpv6GoogleAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c66078c6339c05d8d82fe085a0176cd777657b049da37e93470c82a6347472a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="purpose")
    def purpose(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "purpose"))

    @purpose.setter
    def purpose(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd4376966a33a93530a12428cf38ebbe0eff5d8754bfe1ac610128d89255f379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "purpose", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__014ba8b5b8cb9a4d3761ef6573813d7dc71dc27e6d14191b259c0089ceab138a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reservedInternalRange")
    def reserved_internal_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reservedInternalRange"))

    @reserved_internal_range.setter
    def reserved_internal_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f96f8d9e17cc5d34a2dded26ff486b408d37d41c0a22b66524d00deed592d93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservedInternalRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0103f6f6f9292360f15f87ee55b54a61ebf9c7769b26a89c89534632a0d1a81c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c325b25b230459b67c032f9968b14e0c9972c702feff756cad587cf769d6ab9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendSecondaryIpRangeIfEmpty", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stackType")
    def stack_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stackType"))

    @stack_type.setter
    def stack_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__653932d77e90f2754fdf6376d75cfbda4d3a61c0487f7b0c7a3606706ab23a81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stackType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSubnetwork.GoogleComputeSubnetworkConfig",
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
        "allow_subnet_cidr_routes_overlap": "allowSubnetCidrRoutesOverlap",
        "description": "description",
        "enable_flow_logs": "enableFlowLogs",
        "external_ipv6_prefix": "externalIpv6Prefix",
        "id": "id",
        "ip_cidr_range": "ipCidrRange",
        "ip_collection": "ipCollection",
        "ipv6_access_type": "ipv6AccessType",
        "log_config": "logConfig",
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
class GoogleComputeSubnetworkConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        allow_subnet_cidr_routes_overlap: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_flow_logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_ipv6_prefix: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_cidr_range: typing.Optional[builtins.str] = None,
        ip_collection: typing.Optional[builtins.str] = None,
        ipv6_access_type: typing.Optional[builtins.str] = None,
        log_config: typing.Optional[typing.Union["GoogleComputeSubnetworkLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        private_ip_google_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        private_ipv6_google_access: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        purpose: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        reserved_internal_range: typing.Optional[builtins.str] = None,
        role: typing.Optional[builtins.str] = None,
        secondary_ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeSubnetworkSecondaryIpRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        send_secondary_ip_range_if_empty: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        stack_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeSubnetworkTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the resource, provided by the client when initially creating the resource. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#name GoogleComputeSubnetwork#name}
        :param network: The network this subnet belongs to. Only networks that are in the distributed mode can have subnetworks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#network GoogleComputeSubnetwork#network}
        :param allow_subnet_cidr_routes_overlap: Typically packets destined to IPs within the subnetwork range that do not match existing resources are dropped and prevented from leaving the VPC. Setting this field to true will allow these packets to match dynamic routes injected via BGP even if their destinations match existing subnet ranges. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#allow_subnet_cidr_routes_overlap GoogleComputeSubnetwork#allow_subnet_cidr_routes_overlap}
        :param description: An optional description of this resource. Provide this property when you create the resource. This field can be set only at resource creation time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#description GoogleComputeSubnetwork#description}
        :param enable_flow_logs: Whether to enable flow logging for this subnetwork. If this field is not explicitly set, it will not appear in get listings. If not set the default behavior is determined by the org policy, if there is no org policy specified, then it will default to disabled. This field isn't supported if the subnet purpose field is set to REGIONAL_MANAGED_PROXY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#enable_flow_logs GoogleComputeSubnetwork#enable_flow_logs}
        :param external_ipv6_prefix: The range of external IPv6 addresses that are owned by this subnetwork. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#external_ipv6_prefix GoogleComputeSubnetwork#external_ipv6_prefix}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#id GoogleComputeSubnetwork#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_cidr_range: The range of internal addresses that are owned by this subnetwork. Provide this property when you create the subnetwork. For example, 10.0.0.0/8 or 192.168.0.0/16. Ranges must be unique and non-overlapping within a network. Only IPv4 is supported. Field is optional when 'reserved_internal_range' is defined, otherwise required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#ip_cidr_range GoogleComputeSubnetwork#ip_cidr_range}
        :param ip_collection: Resource reference of a PublicDelegatedPrefix. The PDP must be a sub-PDP in EXTERNAL_IPV6_SUBNETWORK_CREATION mode. Use one of the following formats to specify a sub-PDP when creating an IPv6 NetLB forwarding rule using BYOIP: Full resource URL, as in: - 'https://www.googleapis.com/compute/v1/projects/{{projectId}}/regions/{{region}}/publicDelegatedPrefixes/{{sub-pdp-name}}' Partial URL, as in: - 'projects/{{projectId}}/regions/region/publicDelegatedPrefixes/{{sub-pdp-name}}' - 'regions/{{region}}/publicDelegatedPrefixes/{{sub-pdp-name}}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#ip_collection GoogleComputeSubnetwork#ip_collection}
        :param ipv6_access_type: The access type of IPv6 address this subnet holds. It's immutable and can only be specified during creation or the first time the subnet is updated into IPV4_IPV6 dual stack. If the ipv6_type is EXTERNAL then this subnet cannot enable direct path. Possible values: ["EXTERNAL", "INTERNAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#ipv6_access_type GoogleComputeSubnetwork#ipv6_access_type}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#log_config GoogleComputeSubnetwork#log_config}
        :param private_ip_google_access: When enabled, VMs in this subnetwork without external IP addresses can access Google APIs and services by using Private Google Access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#private_ip_google_access GoogleComputeSubnetwork#private_ip_google_access}
        :param private_ipv6_google_access: The private IPv6 google access type for the VMs in this subnet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#private_ipv6_google_access GoogleComputeSubnetwork#private_ipv6_google_access}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#project GoogleComputeSubnetwork#project}.
        :param purpose: The purpose of the resource. This field can be either 'PRIVATE', 'REGIONAL_MANAGED_PROXY', 'GLOBAL_MANAGED_PROXY', 'PRIVATE_SERVICE_CONNECT', 'PEER_MIGRATION' or 'PRIVATE_NAT'(`Beta <https://terraform.io/docs/providers/google/guides/provider_versions.html>`_). A subnet with purpose set to 'REGIONAL_MANAGED_PROXY' is a user-created subnetwork that is reserved for regional Envoy-based load balancers. A subnetwork in a given region with purpose set to 'GLOBAL_MANAGED_PROXY' is a proxy-only subnet and is shared between all the cross-regional Envoy-based load balancers. A subnetwork with purpose set to 'PRIVATE_SERVICE_CONNECT' reserves the subnet for hosting a Private Service Connect published service. A subnetwork with purpose set to 'PEER_MIGRATION' is a user created subnetwork that is reserved for migrating resources from one peered network to another. A subnetwork with purpose set to 'PRIVATE_NAT' is used as source range for Private NAT gateways. Note that 'REGIONAL_MANAGED_PROXY' is the preferred setting for all regional Envoy load balancers. If unspecified, the purpose defaults to 'PRIVATE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#purpose GoogleComputeSubnetwork#purpose}
        :param region: The GCP region for this subnetwork. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#region GoogleComputeSubnetwork#region}
        :param reserved_internal_range: The ID of the reserved internal range. Must be prefixed with 'networkconnectivity.googleapis.com' E.g. 'networkconnectivity.googleapis.com/projects/{project}/locations/global/internalRanges/{rangeId}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#reserved_internal_range GoogleComputeSubnetwork#reserved_internal_range}
        :param role: The role of subnetwork. Currently, this field is only used when 'purpose' is 'REGIONAL_MANAGED_PROXY'. The value can be set to 'ACTIVE' or 'BACKUP'. An 'ACTIVE' subnetwork is one that is currently being used for Envoy-based load balancers in a region. A 'BACKUP' subnetwork is one that is ready to be promoted to 'ACTIVE' or is currently draining. Possible values: ["ACTIVE", "BACKUP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#role GoogleComputeSubnetwork#role}
        :param secondary_ip_range: secondary_ip_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#secondary_ip_range GoogleComputeSubnetwork#secondary_ip_range}
        :param send_secondary_ip_range_if_empty: Controls the removal behavior of secondary_ip_range. When false, removing secondary_ip_range from config will not produce a diff as the provider will default to the API's value. When true, the provider will treat removing secondary_ip_range as sending an empty list of secondary IP ranges to the API. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#send_secondary_ip_range_if_empty GoogleComputeSubnetwork#send_secondary_ip_range_if_empty}
        :param stack_type: The stack type for this subnet to identify whether the IPv6 feature is enabled or not. If not specified IPV4_ONLY will be used. Possible values: ["IPV4_ONLY", "IPV4_IPV6", "IPV6_ONLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#stack_type GoogleComputeSubnetwork#stack_type}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#timeouts GoogleComputeSubnetwork#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(log_config, dict):
            log_config = GoogleComputeSubnetworkLogConfig(**log_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleComputeSubnetworkTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__845f5e103c79cbe7a01bd75482955102898db4ee47798b11fed7e90ba767e73b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument allow_subnet_cidr_routes_overlap", value=allow_subnet_cidr_routes_overlap, expected_type=type_hints["allow_subnet_cidr_routes_overlap"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_flow_logs", value=enable_flow_logs, expected_type=type_hints["enable_flow_logs"])
            check_type(argname="argument external_ipv6_prefix", value=external_ipv6_prefix, expected_type=type_hints["external_ipv6_prefix"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_cidr_range", value=ip_cidr_range, expected_type=type_hints["ip_cidr_range"])
            check_type(argname="argument ip_collection", value=ip_collection, expected_type=type_hints["ip_collection"])
            check_type(argname="argument ipv6_access_type", value=ipv6_access_type, expected_type=type_hints["ipv6_access_type"])
            check_type(argname="argument log_config", value=log_config, expected_type=type_hints["log_config"])
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
        if allow_subnet_cidr_routes_overlap is not None:
            self._values["allow_subnet_cidr_routes_overlap"] = allow_subnet_cidr_routes_overlap
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#name GoogleComputeSubnetwork#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network(self) -> builtins.str:
        '''The network this subnet belongs to. Only networks that are in the distributed mode can have subnetworks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#network GoogleComputeSubnetwork#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_subnet_cidr_routes_overlap(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Typically packets destined to IPs within the subnetwork range that do not match existing resources are dropped and prevented from leaving the VPC.

        Setting this field to true will allow these packets to match dynamic routes injected
        via BGP even if their destinations match existing subnet ranges.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#allow_subnet_cidr_routes_overlap GoogleComputeSubnetwork#allow_subnet_cidr_routes_overlap}
        '''
        result = self._values.get("allow_subnet_cidr_routes_overlap")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Provide this property when
        you create the resource. This field can be set only at resource
        creation time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#description GoogleComputeSubnetwork#description}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#enable_flow_logs GoogleComputeSubnetwork#enable_flow_logs}
        '''
        result = self._values.get("enable_flow_logs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def external_ipv6_prefix(self) -> typing.Optional[builtins.str]:
        '''The range of external IPv6 addresses that are owned by this subnetwork.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#external_ipv6_prefix GoogleComputeSubnetwork#external_ipv6_prefix}
        '''
        result = self._values.get("external_ipv6_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#id GoogleComputeSubnetwork#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#ip_cidr_range GoogleComputeSubnetwork#ip_cidr_range}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#ip_collection GoogleComputeSubnetwork#ip_collection}
        '''
        result = self._values.get("ip_collection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv6_access_type(self) -> typing.Optional[builtins.str]:
        '''The access type of IPv6 address this subnet holds.

        It's immutable and can only be specified during creation
        or the first time the subnet is updated into IPV4_IPV6 dual stack. If the ipv6_type is EXTERNAL then this subnet
        cannot enable direct path. Possible values: ["EXTERNAL", "INTERNAL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#ipv6_access_type GoogleComputeSubnetwork#ipv6_access_type}
        '''
        result = self._values.get("ipv6_access_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_config(self) -> typing.Optional["GoogleComputeSubnetworkLogConfig"]:
        '''log_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#log_config GoogleComputeSubnetwork#log_config}
        '''
        result = self._values.get("log_config")
        return typing.cast(typing.Optional["GoogleComputeSubnetworkLogConfig"], result)

    @builtins.property
    def private_ip_google_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled, VMs in this subnetwork without external IP addresses can access Google APIs and services by using Private Google Access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#private_ip_google_access GoogleComputeSubnetwork#private_ip_google_access}
        '''
        result = self._values.get("private_ip_google_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def private_ipv6_google_access(self) -> typing.Optional[builtins.str]:
        '''The private IPv6 google access type for the VMs in this subnet.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#private_ipv6_google_access GoogleComputeSubnetwork#private_ipv6_google_access}
        '''
        result = self._values.get("private_ipv6_google_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#project GoogleComputeSubnetwork#project}.'''
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#purpose GoogleComputeSubnetwork#purpose}
        '''
        result = self._values.get("purpose")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The GCP region for this subnetwork.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#region GoogleComputeSubnetwork#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reserved_internal_range(self) -> typing.Optional[builtins.str]:
        '''The ID of the reserved internal range. Must be prefixed with 'networkconnectivity.googleapis.com' E.g. 'networkconnectivity.googleapis.com/projects/{project}/locations/global/internalRanges/{rangeId}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#reserved_internal_range GoogleComputeSubnetwork#reserved_internal_range}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#role GoogleComputeSubnetwork#role}
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_ip_range(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSubnetworkSecondaryIpRange"]]]:
        '''secondary_ip_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#secondary_ip_range GoogleComputeSubnetwork#secondary_ip_range}
        '''
        result = self._values.get("secondary_ip_range")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeSubnetworkSecondaryIpRange"]]], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#send_secondary_ip_range_if_empty GoogleComputeSubnetwork#send_secondary_ip_range_if_empty}
        '''
        result = self._values.get("send_secondary_ip_range_if_empty")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def stack_type(self) -> typing.Optional[builtins.str]:
        '''The stack type for this subnet to identify whether the IPv6 feature is enabled or not.

        If not specified IPV4_ONLY will be used. Possible values: ["IPV4_ONLY", "IPV4_IPV6", "IPV6_ONLY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#stack_type GoogleComputeSubnetwork#stack_type}
        '''
        result = self._values.get("stack_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleComputeSubnetworkTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#timeouts GoogleComputeSubnetwork#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleComputeSubnetworkTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSubnetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSubnetwork.GoogleComputeSubnetworkLogConfig",
    jsii_struct_bases=[],
    name_mapping={
        "aggregation_interval": "aggregationInterval",
        "filter_expr": "filterExpr",
        "flow_sampling": "flowSampling",
        "metadata": "metadata",
        "metadata_fields": "metadataFields",
    },
)
class GoogleComputeSubnetworkLogConfig:
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
        :param aggregation_interval: Can only be specified if VPC flow logging for this subnetwork is enabled. Toggles the aggregation interval for collecting flow logs. Increasing the interval time will reduce the amount of generated flow logs for long lasting connections. Default is an interval of 5 seconds per connection. Default value: "INTERVAL_5_SEC" Possible values: ["INTERVAL_5_SEC", "INTERVAL_30_SEC", "INTERVAL_1_MIN", "INTERVAL_5_MIN", "INTERVAL_10_MIN", "INTERVAL_15_MIN"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#aggregation_interval GoogleComputeSubnetwork#aggregation_interval}
        :param filter_expr: Export filter used to define which VPC flow logs should be logged, as as CEL expression. See https://cloud.google.com/vpc/docs/flow-logs#filtering for details on how to format this field. The default value is 'true', which evaluates to include everything. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#filter_expr GoogleComputeSubnetwork#filter_expr}
        :param flow_sampling: Can only be specified if VPC flow logging for this subnetwork is enabled. The value of the field must be in [0, 1]. Set the sampling rate of VPC flow logs within the subnetwork where 1.0 means all collected logs are reported and 0.0 means no logs are reported. Default is 0.5 which means half of all collected logs are reported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#flow_sampling GoogleComputeSubnetwork#flow_sampling}
        :param metadata: Can only be specified if VPC flow logging for this subnetwork is enabled. Configures whether metadata fields should be added to the reported VPC flow logs. Default value: "INCLUDE_ALL_METADATA" Possible values: ["EXCLUDE_ALL_METADATA", "INCLUDE_ALL_METADATA", "CUSTOM_METADATA"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#metadata GoogleComputeSubnetwork#metadata}
        :param metadata_fields: List of metadata fields that should be added to reported logs. Can only be specified if VPC flow logs for this subnetwork is enabled and "metadata" is set to CUSTOM_METADATA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#metadata_fields GoogleComputeSubnetwork#metadata_fields}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cefebab1ada692c167082a0e8caa8d11191cbb0d9e4efbe2066341df07c98d04)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#aggregation_interval GoogleComputeSubnetwork#aggregation_interval}
        '''
        result = self._values.get("aggregation_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_expr(self) -> typing.Optional[builtins.str]:
        '''Export filter used to define which VPC flow logs should be logged, as as CEL expression.

        See
        https://cloud.google.com/vpc/docs/flow-logs#filtering for details on how to format this field.
        The default value is 'true', which evaluates to include everything.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#filter_expr GoogleComputeSubnetwork#filter_expr}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#flow_sampling GoogleComputeSubnetwork#flow_sampling}
        '''
        result = self._values.get("flow_sampling")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metadata(self) -> typing.Optional[builtins.str]:
        '''Can only be specified if VPC flow logging for this subnetwork is enabled.

        Configures whether metadata fields should be added to the reported VPC
        flow logs. Default value: "INCLUDE_ALL_METADATA" Possible values: ["EXCLUDE_ALL_METADATA", "INCLUDE_ALL_METADATA", "CUSTOM_METADATA"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#metadata GoogleComputeSubnetwork#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of metadata fields that should be added to reported logs.

        Can only be specified if VPC flow logs for this subnetwork is enabled and "metadata" is set to CUSTOM_METADATA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#metadata_fields GoogleComputeSubnetwork#metadata_fields}
        '''
        result = self._values.get("metadata_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSubnetworkLogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSubnetworkLogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSubnetwork.GoogleComputeSubnetworkLogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10e546fe44ae7c510e0f80815a1204590eed93b53c55ceb0b7c3314b95d005e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b75fd07ef44aa167cfe2b4995a374e13ecd1bd0f8e8a1017321d701a148ae440)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregationInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterExpr")
    def filter_expr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterExpr"))

    @filter_expr.setter
    def filter_expr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67b60b4d17c0cd3d83f6ce4d856200ba69a16db4ffd1603daadb8dc3e4cec0e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterExpr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flowSampling")
    def flow_sampling(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "flowSampling"))

    @flow_sampling.setter
    def flow_sampling(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d07d35349b2367130597de140355689b694f46789daaac6930128b7c71a4fa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flowSampling", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de51b0d3d98750e06f51d9fd08f5b52ba7570f50b3a5e3af7ed7815f8a4a6fdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadataFields")
    def metadata_fields(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "metadataFields"))

    @metadata_fields.setter
    def metadata_fields(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd52444274e1a46ea44e3e64236b4cbfc2cbf8c4d9ae5aadaea9f519eb146ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataFields", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleComputeSubnetworkLogConfig]:
        return typing.cast(typing.Optional[GoogleComputeSubnetworkLogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeSubnetworkLogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67a5565f5522d8f40e74f1d2fe815d4515bb64a00a1c180897771610c45f05f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSubnetwork.GoogleComputeSubnetworkSecondaryIpRange",
    jsii_struct_bases=[],
    name_mapping={
        "range_name": "rangeName",
        "ip_cidr_range": "ipCidrRange",
        "reserved_internal_range": "reservedInternalRange",
    },
)
class GoogleComputeSubnetworkSecondaryIpRange:
    def __init__(
        self,
        *,
        range_name: builtins.str,
        ip_cidr_range: typing.Optional[builtins.str] = None,
        reserved_internal_range: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param range_name: The name associated with this subnetwork secondary range, used when adding an alias IP range to a VM instance. The name must be 1-63 characters long, and comply with RFC1035. The name must be unique within the subnetwork. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#range_name GoogleComputeSubnetwork#range_name}
        :param ip_cidr_range: The range of IP addresses belonging to this subnetwork secondary range. Provide this property when you create the subnetwork. Ranges must be unique and non-overlapping with all primary and secondary IP ranges within a network. Only IPv4 is supported. Field is optional when 'reserved_internal_range' is defined, otherwise required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#ip_cidr_range GoogleComputeSubnetwork#ip_cidr_range}
        :param reserved_internal_range: The ID of the reserved internal range. Must be prefixed with 'networkconnectivity.googleapis.com' E.g. 'networkconnectivity.googleapis.com/projects/{project}/locations/global/internalRanges/{rangeId}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#reserved_internal_range GoogleComputeSubnetwork#reserved_internal_range}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe219973ff60a2174a52378b9123754084bd1918fecf1c69d7d4c7cd2944df01)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#range_name GoogleComputeSubnetwork#range_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#ip_cidr_range GoogleComputeSubnetwork#ip_cidr_range}
        '''
        result = self._values.get("ip_cidr_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reserved_internal_range(self) -> typing.Optional[builtins.str]:
        '''The ID of the reserved internal range. Must be prefixed with 'networkconnectivity.googleapis.com' E.g. 'networkconnectivity.googleapis.com/projects/{project}/locations/global/internalRanges/{rangeId}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#reserved_internal_range GoogleComputeSubnetwork#reserved_internal_range}
        '''
        result = self._values.get("reserved_internal_range")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSubnetworkSecondaryIpRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSubnetworkSecondaryIpRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSubnetwork.GoogleComputeSubnetworkSecondaryIpRangeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__387dfca7d248e2b50d5484f60efa3980245726811b1a1309b813fd331e239b58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeSubnetworkSecondaryIpRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7942345aa57e88bfe55c4c190adbc393751cdb753ea7dc11126cfbdde98f959)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeSubnetworkSecondaryIpRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4cff7e3fc0e052ebbc3d19ced4350a97d2dbfd478689f359f00de2f80795a65)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b9cbcd4a90de5d835c5ffa41b3213d375e5026ae30a9b7765fa933f1819ce16)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85ee0ba094e582927b7f6f74f939686b277fe284b64bb1020475270c225159a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSubnetworkSecondaryIpRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSubnetworkSecondaryIpRange]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSubnetworkSecondaryIpRange]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b63e7567acb202d35704bbb3bb6430a664e8164ff5d82f66eb12cb2ff5b69e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeSubnetworkSecondaryIpRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSubnetwork.GoogleComputeSubnetworkSecondaryIpRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__210ee7e4b980d1fb810fb573b5cc106f89fa0a4a3790c9e8a02ac5fd38455269)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6db9b77decb40e1b184378d5df2ee13a6312894b86e25335b57c6691f7d490ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipCidrRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rangeName")
    def range_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rangeName"))

    @range_name.setter
    def range_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2cebe2844c13c669aeca94b51d67a0e684dede3f19e7c9789f0275056f7e0bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rangeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reservedInternalRange")
    def reserved_internal_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reservedInternalRange"))

    @reserved_internal_range.setter
    def reserved_internal_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a856199516b869df86fd269d51ee5cdfa4e19f579ee5faeda5ad0428f3b75f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservedInternalRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSubnetworkSecondaryIpRange]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSubnetworkSecondaryIpRange]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSubnetworkSecondaryIpRange]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a18ed5c26ee6a4a95bedc0e0076e46377d63819b62b12a0c6b1d486a66b8cf76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeSubnetwork.GoogleComputeSubnetworkTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleComputeSubnetworkTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#create GoogleComputeSubnetwork#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#delete GoogleComputeSubnetwork#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#update GoogleComputeSubnetwork#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e746b7ac9135c8c217f38c1b35d89e997c5146dcb495c9a7c6992c01e886b33)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#create GoogleComputeSubnetwork#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#delete GoogleComputeSubnetwork#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_subnetwork#update GoogleComputeSubnetwork#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeSubnetworkTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeSubnetworkTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeSubnetwork.GoogleComputeSubnetworkTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f029ea5f6f75800d1610862cf7a16ebc5ae9dc44f51f5709d602589e737510d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9cb8f0a991d7931ad1cc3b4650c1a5eb34f45e771ec30f4e15063b5dd82deeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2a7efa36e4062c64c613cb91da52126a99cfaf2e4f67ce23daaef5f611ddefe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fe7d8efe0f5ad3bc06cec182eb336771ac02f745f042f195f7da48b394f3b2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSubnetworkTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSubnetworkTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSubnetworkTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37eaeace23fa98c0ffe6bea3759a9cff09c23de79f77fd0390882e6e57c81416)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleComputeSubnetwork",
    "GoogleComputeSubnetworkConfig",
    "GoogleComputeSubnetworkLogConfig",
    "GoogleComputeSubnetworkLogConfigOutputReference",
    "GoogleComputeSubnetworkSecondaryIpRange",
    "GoogleComputeSubnetworkSecondaryIpRangeList",
    "GoogleComputeSubnetworkSecondaryIpRangeOutputReference",
    "GoogleComputeSubnetworkTimeouts",
    "GoogleComputeSubnetworkTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__fa2e0719972ae42ff6668cc201c87b78c5aad82b2d6be09df14ab5cc3cd06b39(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    network: builtins.str,
    allow_subnet_cidr_routes_overlap: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_flow_logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_ipv6_prefix: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_cidr_range: typing.Optional[builtins.str] = None,
    ip_collection: typing.Optional[builtins.str] = None,
    ipv6_access_type: typing.Optional[builtins.str] = None,
    log_config: typing.Optional[typing.Union[GoogleComputeSubnetworkLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    private_ip_google_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_ipv6_google_access: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    purpose: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    reserved_internal_range: typing.Optional[builtins.str] = None,
    role: typing.Optional[builtins.str] = None,
    secondary_ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSubnetworkSecondaryIpRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
    send_secondary_ip_range_if_empty: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    stack_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeSubnetworkTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7722aaa7e6b59faf27e3bc2d0471ba428a9072ddd94a92cfda44c5629974f7f1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe6c6b14b8ba2dd51c9d40d983416bf9bb35d9886f27ccde949ef6d883361413(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSubnetworkSecondaryIpRange, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b6a06212198ad0392ae2928dbdeca2d56ced3ed96bdf66afc382ef96d97ba27(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f72ae70a4f18794ead2a169c0b75ed75c5cfb403a175e33a16d520b5d481a8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c580cf60946bbd4f68895a1efb6399cb47d3020082f3a23c2584b895d49c6ed(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5ddd22956b8bef78afea6d030da61bfae1a038004b54e257581b2e48060ffb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5e64c3b5d7bfe323deb9fba25479614e83cd60146f6116faeef78bffae8ea3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f6ab889de10b13b40bcbeb39b423a3f59295c461a4e72b36260fb4e509604de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edbe39a711aee6b54bddfcb46989443958fdcab942d485ed81de0da83ce8270a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d4b70825c7f90b057cffe25b6fd40d2de58deffbbcc32db60053dd529485bde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b3f4d4b5d081e2b8eb9e9708ed6fa83cf5d23e3a78b567de172fd86fe3bbaaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80078676d805c96993b70a704c9e4e92d02239805ae3ad3730eafa7c847d7e66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eeeca86bcaf77b744e79ebab0757f8b1145035beb77dafa5d35077c33f01af0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5621ea0d6b532984da9956a79c9a543c7306ac51db7b968795915bf9f58abde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c66078c6339c05d8d82fe085a0176cd777657b049da37e93470c82a6347472a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd4376966a33a93530a12428cf38ebbe0eff5d8754bfe1ac610128d89255f379(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014ba8b5b8cb9a4d3761ef6573813d7dc71dc27e6d14191b259c0089ceab138a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f96f8d9e17cc5d34a2dded26ff486b408d37d41c0a22b66524d00deed592d93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0103f6f6f9292360f15f87ee55b54a61ebf9c7769b26a89c89534632a0d1a81c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c325b25b230459b67c032f9968b14e0c9972c702feff756cad587cf769d6ab9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653932d77e90f2754fdf6376d75cfbda4d3a61c0487f7b0c7a3606706ab23a81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__845f5e103c79cbe7a01bd75482955102898db4ee47798b11fed7e90ba767e73b(
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
    allow_subnet_cidr_routes_overlap: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_flow_logs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_ipv6_prefix: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_cidr_range: typing.Optional[builtins.str] = None,
    ip_collection: typing.Optional[builtins.str] = None,
    ipv6_access_type: typing.Optional[builtins.str] = None,
    log_config: typing.Optional[typing.Union[GoogleComputeSubnetworkLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    private_ip_google_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    private_ipv6_google_access: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    purpose: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    reserved_internal_range: typing.Optional[builtins.str] = None,
    role: typing.Optional[builtins.str] = None,
    secondary_ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeSubnetworkSecondaryIpRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
    send_secondary_ip_range_if_empty: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    stack_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeSubnetworkTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cefebab1ada692c167082a0e8caa8d11191cbb0d9e4efbe2066341df07c98d04(
    *,
    aggregation_interval: typing.Optional[builtins.str] = None,
    filter_expr: typing.Optional[builtins.str] = None,
    flow_sampling: typing.Optional[jsii.Number] = None,
    metadata: typing.Optional[builtins.str] = None,
    metadata_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e546fe44ae7c510e0f80815a1204590eed93b53c55ceb0b7c3314b95d005e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b75fd07ef44aa167cfe2b4995a374e13ecd1bd0f8e8a1017321d701a148ae440(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67b60b4d17c0cd3d83f6ce4d856200ba69a16db4ffd1603daadb8dc3e4cec0e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d07d35349b2367130597de140355689b694f46789daaac6930128b7c71a4fa3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de51b0d3d98750e06f51d9fd08f5b52ba7570f50b3a5e3af7ed7815f8a4a6fdb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd52444274e1a46ea44e3e64236b4cbfc2cbf8c4d9ae5aadaea9f519eb146ab(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67a5565f5522d8f40e74f1d2fe815d4515bb64a00a1c180897771610c45f05f2(
    value: typing.Optional[GoogleComputeSubnetworkLogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe219973ff60a2174a52378b9123754084bd1918fecf1c69d7d4c7cd2944df01(
    *,
    range_name: builtins.str,
    ip_cidr_range: typing.Optional[builtins.str] = None,
    reserved_internal_range: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__387dfca7d248e2b50d5484f60efa3980245726811b1a1309b813fd331e239b58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7942345aa57e88bfe55c4c190adbc393751cdb753ea7dc11126cfbdde98f959(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4cff7e3fc0e052ebbc3d19ced4350a97d2dbfd478689f359f00de2f80795a65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b9cbcd4a90de5d835c5ffa41b3213d375e5026ae30a9b7765fa933f1819ce16(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85ee0ba094e582927b7f6f74f939686b277fe284b64bb1020475270c225159a5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b63e7567acb202d35704bbb3bb6430a664e8164ff5d82f66eb12cb2ff5b69e3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeSubnetworkSecondaryIpRange]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__210ee7e4b980d1fb810fb573b5cc106f89fa0a4a3790c9e8a02ac5fd38455269(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db9b77decb40e1b184378d5df2ee13a6312894b86e25335b57c6691f7d490ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2cebe2844c13c669aeca94b51d67a0e684dede3f19e7c9789f0275056f7e0bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a856199516b869df86fd269d51ee5cdfa4e19f579ee5faeda5ad0428f3b75f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a18ed5c26ee6a4a95bedc0e0076e46377d63819b62b12a0c6b1d486a66b8cf76(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSubnetworkSecondaryIpRange]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e746b7ac9135c8c217f38c1b35d89e997c5146dcb495c9a7c6992c01e886b33(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f029ea5f6f75800d1610862cf7a16ebc5ae9dc44f51f5709d602589e737510d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9cb8f0a991d7931ad1cc3b4650c1a5eb34f45e771ec30f4e15063b5dd82deeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2a7efa36e4062c64c613cb91da52126a99cfaf2e4f67ce23daaef5f611ddefe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fe7d8efe0f5ad3bc06cec182eb336771ac02f745f042f195f7da48b394f3b2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37eaeace23fa98c0ffe6bea3759a9cff09c23de79f77fd0390882e6e57c81416(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeSubnetworkTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
