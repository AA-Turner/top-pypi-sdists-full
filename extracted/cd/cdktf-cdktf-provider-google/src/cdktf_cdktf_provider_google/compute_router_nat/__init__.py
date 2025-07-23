r'''
# `google_compute_router_nat`

Refer to the Terraform Registry for docs: [`google_compute_router_nat`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat).
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


class ComputeRouterNat(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouterNat.ComputeRouterNat",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat google_compute_router_nat}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        router: builtins.str,
        source_subnetwork_ip_ranges_to_nat: builtins.str,
        auto_network_tier: typing.Optional[builtins.str] = None,
        drain_nat_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_dynamic_port_allocation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_endpoint_independent_mapping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        endpoint_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        icmp_idle_timeout_sec: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        initial_nat_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_config: typing.Optional[typing.Union["ComputeRouterNatLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        max_ports_per_vm: typing.Optional[jsii.Number] = None,
        min_ports_per_vm: typing.Optional[jsii.Number] = None,
        nat64_subnetwork: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRouterNatNat64Subnetwork", typing.Dict[builtins.str, typing.Any]]]]] = None,
        nat_ip_allocate_option: typing.Optional[builtins.str] = None,
        nat_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRouterNatRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source_subnetwork_ip_ranges_to_nat64: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRouterNatSubnetwork", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tcp_established_idle_timeout_sec: typing.Optional[jsii.Number] = None,
        tcp_time_wait_timeout_sec: typing.Optional[jsii.Number] = None,
        tcp_transitory_idle_timeout_sec: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["ComputeRouterNatTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        udp_idle_timeout_sec: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat google_compute_router_nat} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the NAT service. The name must be 1-63 characters long and comply with RFC1035. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#name ComputeRouterNat#name}
        :param router: The name of the Cloud Router in which this NAT will be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#router ComputeRouterNat#router}
        :param source_subnetwork_ip_ranges_to_nat: How NAT should be configured per Subnetwork. If 'ALL_SUBNETWORKS_ALL_IP_RANGES', all of the IP ranges in every Subnetwork are allowed to Nat. If 'ALL_SUBNETWORKS_ALL_PRIMARY_IP_RANGES', all of the primary IP ranges in every Subnetwork are allowed to Nat. 'LIST_OF_SUBNETWORKS': A list of Subnetworks are allowed to Nat (specified in the field subnetwork below). Note that if this field contains ALL_SUBNETWORKS_ALL_IP_RANGES or ALL_SUBNETWORKS_ALL_PRIMARY_IP_RANGES, then there should not be any other RouterNat section in any Router for this network in this region. Possible values: ["ALL_SUBNETWORKS_ALL_IP_RANGES", "ALL_SUBNETWORKS_ALL_PRIMARY_IP_RANGES", "LIST_OF_SUBNETWORKS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#source_subnetwork_ip_ranges_to_nat ComputeRouterNat#source_subnetwork_ip_ranges_to_nat}
        :param auto_network_tier: The network tier to use when automatically reserving NAT IP addresses. Must be one of: PREMIUM, STANDARD. If not specified, then the current project-level default tier is used. Possible values: ["PREMIUM", "STANDARD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#auto_network_tier ComputeRouterNat#auto_network_tier}
        :param drain_nat_ips: A list of URLs of the IP resources to be drained. These IPs must be valid static external IPs that have been assigned to the NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#drain_nat_ips ComputeRouterNat#drain_nat_ips}
        :param enable_dynamic_port_allocation: Enable Dynamic Port Allocation. If minPortsPerVm is set, minPortsPerVm must be set to a power of two greater than or equal to 32. If minPortsPerVm is not set, a minimum of 32 ports will be allocated to a VM from this NAT config. If maxPortsPerVm is set, maxPortsPerVm must be set to a power of two greater than minPortsPerVm. If maxPortsPerVm is not set, a maximum of 65536 ports will be allocated to a VM from this NAT config. Mutually exclusive with enableEndpointIndependentMapping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#enable_dynamic_port_allocation ComputeRouterNat#enable_dynamic_port_allocation}
        :param enable_endpoint_independent_mapping: Enable endpoint independent mapping. For more information see the `official documentation <https://cloud.google.com/nat/docs/overview#specs-rfcs>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#enable_endpoint_independent_mapping ComputeRouterNat#enable_endpoint_independent_mapping}
        :param endpoint_types: Specifies the endpoint Types supported by the NAT Gateway. Supported values include: 'ENDPOINT_TYPE_VM', 'ENDPOINT_TYPE_SWG', 'ENDPOINT_TYPE_MANAGED_PROXY_LB'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#endpoint_types ComputeRouterNat#endpoint_types}
        :param icmp_idle_timeout_sec: Timeout (in seconds) for ICMP connections. Defaults to 30s if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#icmp_idle_timeout_sec ComputeRouterNat#icmp_idle_timeout_sec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#id ComputeRouterNat#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_nat_ips: Self-links of NAT IPs to be used as initial value for creation alongside a RouterNatAddress resource. Conflicts with natIps and drainNatIps. Only valid if natIpAllocateOption is set to MANUAL_ONLY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#initial_nat_ips ComputeRouterNat#initial_nat_ips}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#log_config ComputeRouterNat#log_config}
        :param max_ports_per_vm: Maximum number of ports allocated to a VM from this NAT. This field can only be set when enableDynamicPortAllocation is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#max_ports_per_vm ComputeRouterNat#max_ports_per_vm}
        :param min_ports_per_vm: Minimum number of ports allocated to a VM from this NAT. Defaults to 64 for static port allocation and 32 dynamic port allocation if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#min_ports_per_vm ComputeRouterNat#min_ports_per_vm}
        :param nat64_subnetwork: nat64_subnetwork block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#nat64_subnetwork ComputeRouterNat#nat64_subnetwork}
        :param nat_ip_allocate_option: How external IPs should be allocated for this NAT. Valid values are 'AUTO_ONLY' for only allowing NAT IPs allocated by Google Cloud Platform, or 'MANUAL_ONLY' for only user-allocated NAT IP addresses. Possible values: ["MANUAL_ONLY", "AUTO_ONLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#nat_ip_allocate_option ComputeRouterNat#nat_ip_allocate_option}
        :param nat_ips: Self-links of NAT IPs. Only valid if natIpAllocateOption is set to MANUAL_ONLY. If this field is used alongside with a count created list of address resources 'google_compute_address.foobar.*.self_link', the access level resource for the address resource must have a 'lifecycle' block with 'create_before_destroy = true' so the number of resources can be increased/decreased without triggering the 'resourceInUseByAnotherResource' error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#nat_ips ComputeRouterNat#nat_ips}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#project ComputeRouterNat#project}.
        :param region: Region where the router and NAT reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#region ComputeRouterNat#region}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#rules ComputeRouterNat#rules}
        :param source_subnetwork_ip_ranges_to_nat64: Specify the Nat option for NAT64, which can take one of the following values: ALL_IPV6_SUBNETWORKS: All of the IP ranges in every Subnetwork are allowed to Nat. LIST_OF_IPV6_SUBNETWORKS: A list of Subnetworks are allowed to Nat (specified in the field nat64Subnetwork below). Note that if this field contains NAT64_ALL_V6_SUBNETWORKS no other Router.Nat section in this region can also enable NAT64 for any Subnetworks in this network. Other Router.Nat sections can still be present to enable NAT44 only. Possible values: ["ALL_IPV6_SUBNETWORKS", "LIST_OF_IPV6_SUBNETWORKS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#source_subnetwork_ip_ranges_to_nat64 ComputeRouterNat#source_subnetwork_ip_ranges_to_nat64}
        :param subnetwork: subnetwork block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#subnetwork ComputeRouterNat#subnetwork}
        :param tcp_established_idle_timeout_sec: Timeout (in seconds) for TCP established connections. Defaults to 1200s if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#tcp_established_idle_timeout_sec ComputeRouterNat#tcp_established_idle_timeout_sec}
        :param tcp_time_wait_timeout_sec: Timeout (in seconds) for TCP connections that are in TIME_WAIT state. Defaults to 120s if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#tcp_time_wait_timeout_sec ComputeRouterNat#tcp_time_wait_timeout_sec}
        :param tcp_transitory_idle_timeout_sec: Timeout (in seconds) for TCP transitory connections. Defaults to 30s if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#tcp_transitory_idle_timeout_sec ComputeRouterNat#tcp_transitory_idle_timeout_sec}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#timeouts ComputeRouterNat#timeouts}
        :param type: Indicates whether this NAT is used for public or private IP translation. If unspecified, it defaults to PUBLIC. If 'PUBLIC' NAT used for public IP translation. If 'PRIVATE' NAT used for private IP translation. Default value: "PUBLIC" Possible values: ["PUBLIC", "PRIVATE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#type ComputeRouterNat#type}
        :param udp_idle_timeout_sec: Timeout (in seconds) for UDP connections. Defaults to 30s if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#udp_idle_timeout_sec ComputeRouterNat#udp_idle_timeout_sec}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae60cc72bda42e6a3f764beb311fa2ef6b29ace4eae8271a19188ee7973b2c11)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeRouterNatConfig(
            name=name,
            router=router,
            source_subnetwork_ip_ranges_to_nat=source_subnetwork_ip_ranges_to_nat,
            auto_network_tier=auto_network_tier,
            drain_nat_ips=drain_nat_ips,
            enable_dynamic_port_allocation=enable_dynamic_port_allocation,
            enable_endpoint_independent_mapping=enable_endpoint_independent_mapping,
            endpoint_types=endpoint_types,
            icmp_idle_timeout_sec=icmp_idle_timeout_sec,
            id=id,
            initial_nat_ips=initial_nat_ips,
            log_config=log_config,
            max_ports_per_vm=max_ports_per_vm,
            min_ports_per_vm=min_ports_per_vm,
            nat64_subnetwork=nat64_subnetwork,
            nat_ip_allocate_option=nat_ip_allocate_option,
            nat_ips=nat_ips,
            project=project,
            region=region,
            rules=rules,
            source_subnetwork_ip_ranges_to_nat64=source_subnetwork_ip_ranges_to_nat64,
            subnetwork=subnetwork,
            tcp_established_idle_timeout_sec=tcp_established_idle_timeout_sec,
            tcp_time_wait_timeout_sec=tcp_time_wait_timeout_sec,
            tcp_transitory_idle_timeout_sec=tcp_transitory_idle_timeout_sec,
            timeouts=timeouts,
            type=type,
            udp_idle_timeout_sec=udp_idle_timeout_sec,
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
        '''Generates CDKTF code for importing a ComputeRouterNat resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeRouterNat to import.
        :param import_from_id: The id of the existing ComputeRouterNat that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeRouterNat to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5f5e6d62a05f472fbe0a7a14aba0e0f23ca591a317261aa38c0281efa65f06f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLogConfig")
    def put_log_config(
        self,
        *,
        enable: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        filter: builtins.str,
    ) -> None:
        '''
        :param enable: Indicates whether or not to export logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#enable ComputeRouterNat#enable}
        :param filter: Specifies the desired filtering of logs on this NAT. Possible values: ["ERRORS_ONLY", "TRANSLATIONS_ONLY", "ALL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#filter ComputeRouterNat#filter}
        '''
        value = ComputeRouterNatLogConfig(enable=enable, filter=filter)

        return typing.cast(None, jsii.invoke(self, "putLogConfig", [value]))

    @jsii.member(jsii_name="putNat64Subnetwork")
    def put_nat64_subnetwork(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRouterNatNat64Subnetwork", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dabed10e1bc13360dd44a355a367148ad239ea59874bc7f701573fa4f7b00c72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNat64Subnetwork", [value]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRouterNatRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14798c64093f3a8d3bfe8218b6aee4754e854a8c99d6e2532ca28a9b7ce471a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="putSubnetwork")
    def put_subnetwork(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRouterNatSubnetwork", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2474fa845c12a738bfe47f448ff473e2057e07a650fc7d48157890ab12853b87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSubnetwork", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#create ComputeRouterNat#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#delete ComputeRouterNat#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#update ComputeRouterNat#update}.
        '''
        value = ComputeRouterNatTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAutoNetworkTier")
    def reset_auto_network_tier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoNetworkTier", []))

    @jsii.member(jsii_name="resetDrainNatIps")
    def reset_drain_nat_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDrainNatIps", []))

    @jsii.member(jsii_name="resetEnableDynamicPortAllocation")
    def reset_enable_dynamic_port_allocation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableDynamicPortAllocation", []))

    @jsii.member(jsii_name="resetEnableEndpointIndependentMapping")
    def reset_enable_endpoint_independent_mapping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableEndpointIndependentMapping", []))

    @jsii.member(jsii_name="resetEndpointTypes")
    def reset_endpoint_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointTypes", []))

    @jsii.member(jsii_name="resetIcmpIdleTimeoutSec")
    def reset_icmp_idle_timeout_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIcmpIdleTimeoutSec", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInitialNatIps")
    def reset_initial_nat_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialNatIps", []))

    @jsii.member(jsii_name="resetLogConfig")
    def reset_log_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogConfig", []))

    @jsii.member(jsii_name="resetMaxPortsPerVm")
    def reset_max_ports_per_vm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxPortsPerVm", []))

    @jsii.member(jsii_name="resetMinPortsPerVm")
    def reset_min_ports_per_vm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinPortsPerVm", []))

    @jsii.member(jsii_name="resetNat64Subnetwork")
    def reset_nat64_subnetwork(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNat64Subnetwork", []))

    @jsii.member(jsii_name="resetNatIpAllocateOption")
    def reset_nat_ip_allocate_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNatIpAllocateOption", []))

    @jsii.member(jsii_name="resetNatIps")
    def reset_nat_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNatIps", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRules")
    def reset_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRules", []))

    @jsii.member(jsii_name="resetSourceSubnetworkIpRangesToNat64")
    def reset_source_subnetwork_ip_ranges_to_nat64(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceSubnetworkIpRangesToNat64", []))

    @jsii.member(jsii_name="resetSubnetwork")
    def reset_subnetwork(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetwork", []))

    @jsii.member(jsii_name="resetTcpEstablishedIdleTimeoutSec")
    def reset_tcp_established_idle_timeout_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpEstablishedIdleTimeoutSec", []))

    @jsii.member(jsii_name="resetTcpTimeWaitTimeoutSec")
    def reset_tcp_time_wait_timeout_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpTimeWaitTimeoutSec", []))

    @jsii.member(jsii_name="resetTcpTransitoryIdleTimeoutSec")
    def reset_tcp_transitory_idle_timeout_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpTransitoryIdleTimeoutSec", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUdpIdleTimeoutSec")
    def reset_udp_idle_timeout_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUdpIdleTimeoutSec", []))

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
    @jsii.member(jsii_name="logConfig")
    def log_config(self) -> "ComputeRouterNatLogConfigOutputReference":
        return typing.cast("ComputeRouterNatLogConfigOutputReference", jsii.get(self, "logConfig"))

    @builtins.property
    @jsii.member(jsii_name="nat64Subnetwork")
    def nat64_subnetwork(self) -> "ComputeRouterNatNat64SubnetworkList":
        return typing.cast("ComputeRouterNatNat64SubnetworkList", jsii.get(self, "nat64Subnetwork"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "ComputeRouterNatRulesList":
        return typing.cast("ComputeRouterNatRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> "ComputeRouterNatSubnetworkList":
        return typing.cast("ComputeRouterNatSubnetworkList", jsii.get(self, "subnetwork"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeRouterNatTimeoutsOutputReference":
        return typing.cast("ComputeRouterNatTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="autoNetworkTierInput")
    def auto_network_tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoNetworkTierInput"))

    @builtins.property
    @jsii.member(jsii_name="drainNatIpsInput")
    def drain_nat_ips_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "drainNatIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="enableDynamicPortAllocationInput")
    def enable_dynamic_port_allocation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableDynamicPortAllocationInput"))

    @builtins.property
    @jsii.member(jsii_name="enableEndpointIndependentMappingInput")
    def enable_endpoint_independent_mapping_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableEndpointIndependentMappingInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointTypesInput")
    def endpoint_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "endpointTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="icmpIdleTimeoutSecInput")
    def icmp_idle_timeout_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "icmpIdleTimeoutSecInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="initialNatIpsInput")
    def initial_nat_ips_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "initialNatIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="logConfigInput")
    def log_config_input(self) -> typing.Optional["ComputeRouterNatLogConfig"]:
        return typing.cast(typing.Optional["ComputeRouterNatLogConfig"], jsii.get(self, "logConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPortsPerVmInput")
    def max_ports_per_vm_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPortsPerVmInput"))

    @builtins.property
    @jsii.member(jsii_name="minPortsPerVmInput")
    def min_ports_per_vm_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minPortsPerVmInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nat64SubnetworkInput")
    def nat64_subnetwork_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRouterNatNat64Subnetwork"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRouterNatNat64Subnetwork"]]], jsii.get(self, "nat64SubnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="natIpAllocateOptionInput")
    def nat_ip_allocate_option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "natIpAllocateOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="natIpsInput")
    def nat_ips_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "natIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="routerInput")
    def router_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routerInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRouterNatRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRouterNatRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceSubnetworkIpRangesToNat64Input")
    def source_subnetwork_ip_ranges_to_nat64_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceSubnetworkIpRangesToNat64Input"))

    @builtins.property
    @jsii.member(jsii_name="sourceSubnetworkIpRangesToNatInput")
    def source_subnetwork_ip_ranges_to_nat_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceSubnetworkIpRangesToNatInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkInput")
    def subnetwork_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRouterNatSubnetwork"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRouterNatSubnetwork"]]], jsii.get(self, "subnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpEstablishedIdleTimeoutSecInput")
    def tcp_established_idle_timeout_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tcpEstablishedIdleTimeoutSecInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpTimeWaitTimeoutSecInput")
    def tcp_time_wait_timeout_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tcpTimeWaitTimeoutSecInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpTransitoryIdleTimeoutSecInput")
    def tcp_transitory_idle_timeout_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tcpTransitoryIdleTimeoutSecInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRouterNatTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRouterNatTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="udpIdleTimeoutSecInput")
    def udp_idle_timeout_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "udpIdleTimeoutSecInput"))

    @builtins.property
    @jsii.member(jsii_name="autoNetworkTier")
    def auto_network_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoNetworkTier"))

    @auto_network_tier.setter
    def auto_network_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12eca6bde0cd0ada177aec90164a139fe0a851523d63ae5aee3a994f896f2bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoNetworkTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="drainNatIps")
    def drain_nat_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "drainNatIps"))

    @drain_nat_ips.setter
    def drain_nat_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcc9cc1772f159edad8dc41e7a0f701519b8736e9c7b4b69966a7d6aad814ba3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "drainNatIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableDynamicPortAllocation")
    def enable_dynamic_port_allocation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableDynamicPortAllocation"))

    @enable_dynamic_port_allocation.setter
    def enable_dynamic_port_allocation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4d6e31a6f1d8550af8f1888d4df0bc7cd10d96ffce2e1f5b72857cbd439b6d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableDynamicPortAllocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableEndpointIndependentMapping")
    def enable_endpoint_independent_mapping(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableEndpointIndependentMapping"))

    @enable_endpoint_independent_mapping.setter
    def enable_endpoint_independent_mapping(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd0821791e185b9c36403e11bdd9c15548e4d00009ff4c92eb08c7164787c98a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableEndpointIndependentMapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpointTypes")
    def endpoint_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "endpointTypes"))

    @endpoint_types.setter
    def endpoint_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__400e45afc8738e6b7b0a351755172aa58f06a20e3cc6c51ebb7852a84720f31b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="icmpIdleTimeoutSec")
    def icmp_idle_timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "icmpIdleTimeoutSec"))

    @icmp_idle_timeout_sec.setter
    def icmp_idle_timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b29077df3ddec6c418574f2073361a97ed7a8944c60945ddd01bad17ae6e249f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "icmpIdleTimeoutSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7110ba283d65153c95d63e400c964c6333d3781b74b9922a76ba2a4a46f8d5ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialNatIps")
    def initial_nat_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "initialNatIps"))

    @initial_nat_ips.setter
    def initial_nat_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a021e855b6f7bf11b611d6af0628307841d8bcfb95323b34ee1d2b7df3d3edf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialNatIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxPortsPerVm")
    def max_ports_per_vm(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPortsPerVm"))

    @max_ports_per_vm.setter
    def max_ports_per_vm(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cc367c2fd4477af7863b73fcf388bb811bd08565138d6493894041b880aa8f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPortsPerVm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minPortsPerVm")
    def min_ports_per_vm(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minPortsPerVm"))

    @min_ports_per_vm.setter
    def min_ports_per_vm(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2cdcf6ba429f282c3eef56ee64156890a77f009332b5ec9a8c8d8adc9a9c238)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minPortsPerVm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f25d7b4b6922e9bd1c7a879887c973a8c98075aab34fc0d78937075afe45ee14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="natIpAllocateOption")
    def nat_ip_allocate_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "natIpAllocateOption"))

    @nat_ip_allocate_option.setter
    def nat_ip_allocate_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92e673586211464907d1ea42a8cb806fe48eab01b885594a069f0ffa12f557b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "natIpAllocateOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="natIps")
    def nat_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "natIps"))

    @nat_ips.setter
    def nat_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aabea739aa81c0d0eed08df7bffcbdd43ead305b3d6a176713be13b2e1fe994)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "natIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b071a36d0749b256f23fb47e93759346510036a843f6d46361f07e403339129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e299727e9fe12bb79bcf94e7315c71f9a62849fb8d836d667942c37da9328d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="router")
    def router(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "router"))

    @router.setter
    def router(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34d6d4f7d24be3937bffab37fe1b3b07976830894d855a9ba41efac3a2deb956)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "router", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceSubnetworkIpRangesToNat")
    def source_subnetwork_ip_ranges_to_nat(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceSubnetworkIpRangesToNat"))

    @source_subnetwork_ip_ranges_to_nat.setter
    def source_subnetwork_ip_ranges_to_nat(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e40da5030a63141d60a16677492f8d9cbae12d769e030bb1d1da087ebd8df9d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceSubnetworkIpRangesToNat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceSubnetworkIpRangesToNat64")
    def source_subnetwork_ip_ranges_to_nat64(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceSubnetworkIpRangesToNat64"))

    @source_subnetwork_ip_ranges_to_nat64.setter
    def source_subnetwork_ip_ranges_to_nat64(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9e40b9930689f1a0cd1093396c6b641262f96d5d6bf2f7169dc184a3576b05c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceSubnetworkIpRangesToNat64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tcpEstablishedIdleTimeoutSec")
    def tcp_established_idle_timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tcpEstablishedIdleTimeoutSec"))

    @tcp_established_idle_timeout_sec.setter
    def tcp_established_idle_timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__039b6b7adcf7809a7c98536a8198975185ecae8c6b99322702c053f61ee8ba30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tcpEstablishedIdleTimeoutSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tcpTimeWaitTimeoutSec")
    def tcp_time_wait_timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tcpTimeWaitTimeoutSec"))

    @tcp_time_wait_timeout_sec.setter
    def tcp_time_wait_timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36eb23ad55510fd4532eeb9dd86e907ffe94eaa4e6aca65cc627d3d82791a0fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tcpTimeWaitTimeoutSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tcpTransitoryIdleTimeoutSec")
    def tcp_transitory_idle_timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tcpTransitoryIdleTimeoutSec"))

    @tcp_transitory_idle_timeout_sec.setter
    def tcp_transitory_idle_timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ea0bcaf6cf830ea2add2b3f439c2c79671b4e265f22d10a5f88a7ba3cc5816d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tcpTransitoryIdleTimeoutSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b34b2679a1d3bf3fe9151a18bd231245edb8cf1721ae170bd4beb423f16a1370)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="udpIdleTimeoutSec")
    def udp_idle_timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "udpIdleTimeoutSec"))

    @udp_idle_timeout_sec.setter
    def udp_idle_timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71a30703e4061ef2ec85681bbcbdb739c943ed590c1ef039d8bec0e663a61e62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "udpIdleTimeoutSec", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRouterNat.ComputeRouterNatConfig",
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
        "router": "router",
        "source_subnetwork_ip_ranges_to_nat": "sourceSubnetworkIpRangesToNat",
        "auto_network_tier": "autoNetworkTier",
        "drain_nat_ips": "drainNatIps",
        "enable_dynamic_port_allocation": "enableDynamicPortAllocation",
        "enable_endpoint_independent_mapping": "enableEndpointIndependentMapping",
        "endpoint_types": "endpointTypes",
        "icmp_idle_timeout_sec": "icmpIdleTimeoutSec",
        "id": "id",
        "initial_nat_ips": "initialNatIps",
        "log_config": "logConfig",
        "max_ports_per_vm": "maxPortsPerVm",
        "min_ports_per_vm": "minPortsPerVm",
        "nat64_subnetwork": "nat64Subnetwork",
        "nat_ip_allocate_option": "natIpAllocateOption",
        "nat_ips": "natIps",
        "project": "project",
        "region": "region",
        "rules": "rules",
        "source_subnetwork_ip_ranges_to_nat64": "sourceSubnetworkIpRangesToNat64",
        "subnetwork": "subnetwork",
        "tcp_established_idle_timeout_sec": "tcpEstablishedIdleTimeoutSec",
        "tcp_time_wait_timeout_sec": "tcpTimeWaitTimeoutSec",
        "tcp_transitory_idle_timeout_sec": "tcpTransitoryIdleTimeoutSec",
        "timeouts": "timeouts",
        "type": "type",
        "udp_idle_timeout_sec": "udpIdleTimeoutSec",
    },
)
class ComputeRouterNatConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        router: builtins.str,
        source_subnetwork_ip_ranges_to_nat: builtins.str,
        auto_network_tier: typing.Optional[builtins.str] = None,
        drain_nat_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_dynamic_port_allocation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_endpoint_independent_mapping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        endpoint_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        icmp_idle_timeout_sec: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        initial_nat_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_config: typing.Optional[typing.Union["ComputeRouterNatLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        max_ports_per_vm: typing.Optional[jsii.Number] = None,
        min_ports_per_vm: typing.Optional[jsii.Number] = None,
        nat64_subnetwork: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRouterNatNat64Subnetwork", typing.Dict[builtins.str, typing.Any]]]]] = None,
        nat_ip_allocate_option: typing.Optional[builtins.str] = None,
        nat_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRouterNatRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source_subnetwork_ip_ranges_to_nat64: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRouterNatSubnetwork", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tcp_established_idle_timeout_sec: typing.Optional[jsii.Number] = None,
        tcp_time_wait_timeout_sec: typing.Optional[jsii.Number] = None,
        tcp_transitory_idle_timeout_sec: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["ComputeRouterNatTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        udp_idle_timeout_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the NAT service. The name must be 1-63 characters long and comply with RFC1035. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#name ComputeRouterNat#name}
        :param router: The name of the Cloud Router in which this NAT will be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#router ComputeRouterNat#router}
        :param source_subnetwork_ip_ranges_to_nat: How NAT should be configured per Subnetwork. If 'ALL_SUBNETWORKS_ALL_IP_RANGES', all of the IP ranges in every Subnetwork are allowed to Nat. If 'ALL_SUBNETWORKS_ALL_PRIMARY_IP_RANGES', all of the primary IP ranges in every Subnetwork are allowed to Nat. 'LIST_OF_SUBNETWORKS': A list of Subnetworks are allowed to Nat (specified in the field subnetwork below). Note that if this field contains ALL_SUBNETWORKS_ALL_IP_RANGES or ALL_SUBNETWORKS_ALL_PRIMARY_IP_RANGES, then there should not be any other RouterNat section in any Router for this network in this region. Possible values: ["ALL_SUBNETWORKS_ALL_IP_RANGES", "ALL_SUBNETWORKS_ALL_PRIMARY_IP_RANGES", "LIST_OF_SUBNETWORKS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#source_subnetwork_ip_ranges_to_nat ComputeRouterNat#source_subnetwork_ip_ranges_to_nat}
        :param auto_network_tier: The network tier to use when automatically reserving NAT IP addresses. Must be one of: PREMIUM, STANDARD. If not specified, then the current project-level default tier is used. Possible values: ["PREMIUM", "STANDARD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#auto_network_tier ComputeRouterNat#auto_network_tier}
        :param drain_nat_ips: A list of URLs of the IP resources to be drained. These IPs must be valid static external IPs that have been assigned to the NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#drain_nat_ips ComputeRouterNat#drain_nat_ips}
        :param enable_dynamic_port_allocation: Enable Dynamic Port Allocation. If minPortsPerVm is set, minPortsPerVm must be set to a power of two greater than or equal to 32. If minPortsPerVm is not set, a minimum of 32 ports will be allocated to a VM from this NAT config. If maxPortsPerVm is set, maxPortsPerVm must be set to a power of two greater than minPortsPerVm. If maxPortsPerVm is not set, a maximum of 65536 ports will be allocated to a VM from this NAT config. Mutually exclusive with enableEndpointIndependentMapping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#enable_dynamic_port_allocation ComputeRouterNat#enable_dynamic_port_allocation}
        :param enable_endpoint_independent_mapping: Enable endpoint independent mapping. For more information see the `official documentation <https://cloud.google.com/nat/docs/overview#specs-rfcs>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#enable_endpoint_independent_mapping ComputeRouterNat#enable_endpoint_independent_mapping}
        :param endpoint_types: Specifies the endpoint Types supported by the NAT Gateway. Supported values include: 'ENDPOINT_TYPE_VM', 'ENDPOINT_TYPE_SWG', 'ENDPOINT_TYPE_MANAGED_PROXY_LB'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#endpoint_types ComputeRouterNat#endpoint_types}
        :param icmp_idle_timeout_sec: Timeout (in seconds) for ICMP connections. Defaults to 30s if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#icmp_idle_timeout_sec ComputeRouterNat#icmp_idle_timeout_sec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#id ComputeRouterNat#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_nat_ips: Self-links of NAT IPs to be used as initial value for creation alongside a RouterNatAddress resource. Conflicts with natIps and drainNatIps. Only valid if natIpAllocateOption is set to MANUAL_ONLY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#initial_nat_ips ComputeRouterNat#initial_nat_ips}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#log_config ComputeRouterNat#log_config}
        :param max_ports_per_vm: Maximum number of ports allocated to a VM from this NAT. This field can only be set when enableDynamicPortAllocation is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#max_ports_per_vm ComputeRouterNat#max_ports_per_vm}
        :param min_ports_per_vm: Minimum number of ports allocated to a VM from this NAT. Defaults to 64 for static port allocation and 32 dynamic port allocation if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#min_ports_per_vm ComputeRouterNat#min_ports_per_vm}
        :param nat64_subnetwork: nat64_subnetwork block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#nat64_subnetwork ComputeRouterNat#nat64_subnetwork}
        :param nat_ip_allocate_option: How external IPs should be allocated for this NAT. Valid values are 'AUTO_ONLY' for only allowing NAT IPs allocated by Google Cloud Platform, or 'MANUAL_ONLY' for only user-allocated NAT IP addresses. Possible values: ["MANUAL_ONLY", "AUTO_ONLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#nat_ip_allocate_option ComputeRouterNat#nat_ip_allocate_option}
        :param nat_ips: Self-links of NAT IPs. Only valid if natIpAllocateOption is set to MANUAL_ONLY. If this field is used alongside with a count created list of address resources 'google_compute_address.foobar.*.self_link', the access level resource for the address resource must have a 'lifecycle' block with 'create_before_destroy = true' so the number of resources can be increased/decreased without triggering the 'resourceInUseByAnotherResource' error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#nat_ips ComputeRouterNat#nat_ips}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#project ComputeRouterNat#project}.
        :param region: Region where the router and NAT reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#region ComputeRouterNat#region}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#rules ComputeRouterNat#rules}
        :param source_subnetwork_ip_ranges_to_nat64: Specify the Nat option for NAT64, which can take one of the following values: ALL_IPV6_SUBNETWORKS: All of the IP ranges in every Subnetwork are allowed to Nat. LIST_OF_IPV6_SUBNETWORKS: A list of Subnetworks are allowed to Nat (specified in the field nat64Subnetwork below). Note that if this field contains NAT64_ALL_V6_SUBNETWORKS no other Router.Nat section in this region can also enable NAT64 for any Subnetworks in this network. Other Router.Nat sections can still be present to enable NAT44 only. Possible values: ["ALL_IPV6_SUBNETWORKS", "LIST_OF_IPV6_SUBNETWORKS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#source_subnetwork_ip_ranges_to_nat64 ComputeRouterNat#source_subnetwork_ip_ranges_to_nat64}
        :param subnetwork: subnetwork block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#subnetwork ComputeRouterNat#subnetwork}
        :param tcp_established_idle_timeout_sec: Timeout (in seconds) for TCP established connections. Defaults to 1200s if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#tcp_established_idle_timeout_sec ComputeRouterNat#tcp_established_idle_timeout_sec}
        :param tcp_time_wait_timeout_sec: Timeout (in seconds) for TCP connections that are in TIME_WAIT state. Defaults to 120s if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#tcp_time_wait_timeout_sec ComputeRouterNat#tcp_time_wait_timeout_sec}
        :param tcp_transitory_idle_timeout_sec: Timeout (in seconds) for TCP transitory connections. Defaults to 30s if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#tcp_transitory_idle_timeout_sec ComputeRouterNat#tcp_transitory_idle_timeout_sec}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#timeouts ComputeRouterNat#timeouts}
        :param type: Indicates whether this NAT is used for public or private IP translation. If unspecified, it defaults to PUBLIC. If 'PUBLIC' NAT used for public IP translation. If 'PRIVATE' NAT used for private IP translation. Default value: "PUBLIC" Possible values: ["PUBLIC", "PRIVATE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#type ComputeRouterNat#type}
        :param udp_idle_timeout_sec: Timeout (in seconds) for UDP connections. Defaults to 30s if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#udp_idle_timeout_sec ComputeRouterNat#udp_idle_timeout_sec}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(log_config, dict):
            log_config = ComputeRouterNatLogConfig(**log_config)
        if isinstance(timeouts, dict):
            timeouts = ComputeRouterNatTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4206e3123f14db114b0b184e0ac18276ac7bd0ccd157247ee559a26008a293ea)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument router", value=router, expected_type=type_hints["router"])
            check_type(argname="argument source_subnetwork_ip_ranges_to_nat", value=source_subnetwork_ip_ranges_to_nat, expected_type=type_hints["source_subnetwork_ip_ranges_to_nat"])
            check_type(argname="argument auto_network_tier", value=auto_network_tier, expected_type=type_hints["auto_network_tier"])
            check_type(argname="argument drain_nat_ips", value=drain_nat_ips, expected_type=type_hints["drain_nat_ips"])
            check_type(argname="argument enable_dynamic_port_allocation", value=enable_dynamic_port_allocation, expected_type=type_hints["enable_dynamic_port_allocation"])
            check_type(argname="argument enable_endpoint_independent_mapping", value=enable_endpoint_independent_mapping, expected_type=type_hints["enable_endpoint_independent_mapping"])
            check_type(argname="argument endpoint_types", value=endpoint_types, expected_type=type_hints["endpoint_types"])
            check_type(argname="argument icmp_idle_timeout_sec", value=icmp_idle_timeout_sec, expected_type=type_hints["icmp_idle_timeout_sec"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument initial_nat_ips", value=initial_nat_ips, expected_type=type_hints["initial_nat_ips"])
            check_type(argname="argument log_config", value=log_config, expected_type=type_hints["log_config"])
            check_type(argname="argument max_ports_per_vm", value=max_ports_per_vm, expected_type=type_hints["max_ports_per_vm"])
            check_type(argname="argument min_ports_per_vm", value=min_ports_per_vm, expected_type=type_hints["min_ports_per_vm"])
            check_type(argname="argument nat64_subnetwork", value=nat64_subnetwork, expected_type=type_hints["nat64_subnetwork"])
            check_type(argname="argument nat_ip_allocate_option", value=nat_ip_allocate_option, expected_type=type_hints["nat_ip_allocate_option"])
            check_type(argname="argument nat_ips", value=nat_ips, expected_type=type_hints["nat_ips"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument source_subnetwork_ip_ranges_to_nat64", value=source_subnetwork_ip_ranges_to_nat64, expected_type=type_hints["source_subnetwork_ip_ranges_to_nat64"])
            check_type(argname="argument subnetwork", value=subnetwork, expected_type=type_hints["subnetwork"])
            check_type(argname="argument tcp_established_idle_timeout_sec", value=tcp_established_idle_timeout_sec, expected_type=type_hints["tcp_established_idle_timeout_sec"])
            check_type(argname="argument tcp_time_wait_timeout_sec", value=tcp_time_wait_timeout_sec, expected_type=type_hints["tcp_time_wait_timeout_sec"])
            check_type(argname="argument tcp_transitory_idle_timeout_sec", value=tcp_transitory_idle_timeout_sec, expected_type=type_hints["tcp_transitory_idle_timeout_sec"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument udp_idle_timeout_sec", value=udp_idle_timeout_sec, expected_type=type_hints["udp_idle_timeout_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "router": router,
            "source_subnetwork_ip_ranges_to_nat": source_subnetwork_ip_ranges_to_nat,
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
        if auto_network_tier is not None:
            self._values["auto_network_tier"] = auto_network_tier
        if drain_nat_ips is not None:
            self._values["drain_nat_ips"] = drain_nat_ips
        if enable_dynamic_port_allocation is not None:
            self._values["enable_dynamic_port_allocation"] = enable_dynamic_port_allocation
        if enable_endpoint_independent_mapping is not None:
            self._values["enable_endpoint_independent_mapping"] = enable_endpoint_independent_mapping
        if endpoint_types is not None:
            self._values["endpoint_types"] = endpoint_types
        if icmp_idle_timeout_sec is not None:
            self._values["icmp_idle_timeout_sec"] = icmp_idle_timeout_sec
        if id is not None:
            self._values["id"] = id
        if initial_nat_ips is not None:
            self._values["initial_nat_ips"] = initial_nat_ips
        if log_config is not None:
            self._values["log_config"] = log_config
        if max_ports_per_vm is not None:
            self._values["max_ports_per_vm"] = max_ports_per_vm
        if min_ports_per_vm is not None:
            self._values["min_ports_per_vm"] = min_ports_per_vm
        if nat64_subnetwork is not None:
            self._values["nat64_subnetwork"] = nat64_subnetwork
        if nat_ip_allocate_option is not None:
            self._values["nat_ip_allocate_option"] = nat_ip_allocate_option
        if nat_ips is not None:
            self._values["nat_ips"] = nat_ips
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if rules is not None:
            self._values["rules"] = rules
        if source_subnetwork_ip_ranges_to_nat64 is not None:
            self._values["source_subnetwork_ip_ranges_to_nat64"] = source_subnetwork_ip_ranges_to_nat64
        if subnetwork is not None:
            self._values["subnetwork"] = subnetwork
        if tcp_established_idle_timeout_sec is not None:
            self._values["tcp_established_idle_timeout_sec"] = tcp_established_idle_timeout_sec
        if tcp_time_wait_timeout_sec is not None:
            self._values["tcp_time_wait_timeout_sec"] = tcp_time_wait_timeout_sec
        if tcp_transitory_idle_timeout_sec is not None:
            self._values["tcp_transitory_idle_timeout_sec"] = tcp_transitory_idle_timeout_sec
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if type is not None:
            self._values["type"] = type
        if udp_idle_timeout_sec is not None:
            self._values["udp_idle_timeout_sec"] = udp_idle_timeout_sec

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
        '''Name of the NAT service. The name must be 1-63 characters long and comply with RFC1035.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#name ComputeRouterNat#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def router(self) -> builtins.str:
        '''The name of the Cloud Router in which this NAT will be configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#router ComputeRouterNat#router}
        '''
        result = self._values.get("router")
        assert result is not None, "Required property 'router' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_subnetwork_ip_ranges_to_nat(self) -> builtins.str:
        '''How NAT should be configured per Subnetwork.

        If 'ALL_SUBNETWORKS_ALL_IP_RANGES', all of the
        IP ranges in every Subnetwork are allowed to Nat.
        If 'ALL_SUBNETWORKS_ALL_PRIMARY_IP_RANGES', all of the primary IP
        ranges in every Subnetwork are allowed to Nat.
        'LIST_OF_SUBNETWORKS': A list of Subnetworks are allowed to Nat
        (specified in the field subnetwork below). Note that if this field
        contains ALL_SUBNETWORKS_ALL_IP_RANGES or
        ALL_SUBNETWORKS_ALL_PRIMARY_IP_RANGES, then there should not be any
        other RouterNat section in any Router for this network in this region. Possible values: ["ALL_SUBNETWORKS_ALL_IP_RANGES", "ALL_SUBNETWORKS_ALL_PRIMARY_IP_RANGES", "LIST_OF_SUBNETWORKS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#source_subnetwork_ip_ranges_to_nat ComputeRouterNat#source_subnetwork_ip_ranges_to_nat}
        '''
        result = self._values.get("source_subnetwork_ip_ranges_to_nat")
        assert result is not None, "Required property 'source_subnetwork_ip_ranges_to_nat' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_network_tier(self) -> typing.Optional[builtins.str]:
        '''The network tier to use when automatically reserving NAT IP addresses.

        Must be one of: PREMIUM, STANDARD. If not specified, then the current
        project-level default tier is used. Possible values: ["PREMIUM", "STANDARD"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#auto_network_tier ComputeRouterNat#auto_network_tier}
        '''
        result = self._values.get("auto_network_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def drain_nat_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of URLs of the IP resources to be drained.

        These IPs must be
        valid static external IPs that have been assigned to the NAT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#drain_nat_ips ComputeRouterNat#drain_nat_ips}
        '''
        result = self._values.get("drain_nat_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable_dynamic_port_allocation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable Dynamic Port Allocation.

        If minPortsPerVm is set, minPortsPerVm must be set to a power of two greater than or equal to 32.
        If minPortsPerVm is not set, a minimum of 32 ports will be allocated to a VM from this NAT config.
        If maxPortsPerVm is set, maxPortsPerVm must be set to a power of two greater than minPortsPerVm.
        If maxPortsPerVm is not set, a maximum of 65536 ports will be allocated to a VM from this NAT config.

        Mutually exclusive with enableEndpointIndependentMapping.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#enable_dynamic_port_allocation ComputeRouterNat#enable_dynamic_port_allocation}
        '''
        result = self._values.get("enable_dynamic_port_allocation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_endpoint_independent_mapping(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable endpoint independent mapping. For more information see the `official documentation <https://cloud.google.com/nat/docs/overview#specs-rfcs>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#enable_endpoint_independent_mapping ComputeRouterNat#enable_endpoint_independent_mapping}
        '''
        result = self._values.get("enable_endpoint_independent_mapping")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def endpoint_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the endpoint Types supported by the NAT Gateway.

        Supported values include:
        'ENDPOINT_TYPE_VM', 'ENDPOINT_TYPE_SWG',
        'ENDPOINT_TYPE_MANAGED_PROXY_LB'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#endpoint_types ComputeRouterNat#endpoint_types}
        '''
        result = self._values.get("endpoint_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def icmp_idle_timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''Timeout (in seconds) for ICMP connections. Defaults to 30s if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#icmp_idle_timeout_sec ComputeRouterNat#icmp_idle_timeout_sec}
        '''
        result = self._values.get("icmp_idle_timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#id ComputeRouterNat#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_nat_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Self-links of NAT IPs to be used as initial value for creation alongside a RouterNatAddress resource.

        Conflicts with natIps and drainNatIps. Only valid if natIpAllocateOption is set to MANUAL_ONLY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#initial_nat_ips ComputeRouterNat#initial_nat_ips}
        '''
        result = self._values.get("initial_nat_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def log_config(self) -> typing.Optional["ComputeRouterNatLogConfig"]:
        '''log_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#log_config ComputeRouterNat#log_config}
        '''
        result = self._values.get("log_config")
        return typing.cast(typing.Optional["ComputeRouterNatLogConfig"], result)

    @builtins.property
    def max_ports_per_vm(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of ports allocated to a VM from this NAT.

        This field can only be set when enableDynamicPortAllocation is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#max_ports_per_vm ComputeRouterNat#max_ports_per_vm}
        '''
        result = self._values.get("max_ports_per_vm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_ports_per_vm(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of ports allocated to a VM from this NAT.

        Defaults to 64 for static port allocation and 32 dynamic port allocation if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#min_ports_per_vm ComputeRouterNat#min_ports_per_vm}
        '''
        result = self._values.get("min_ports_per_vm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nat64_subnetwork(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRouterNatNat64Subnetwork"]]]:
        '''nat64_subnetwork block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#nat64_subnetwork ComputeRouterNat#nat64_subnetwork}
        '''
        result = self._values.get("nat64_subnetwork")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRouterNatNat64Subnetwork"]]], result)

    @builtins.property
    def nat_ip_allocate_option(self) -> typing.Optional[builtins.str]:
        '''How external IPs should be allocated for this NAT.

        Valid values are
        'AUTO_ONLY' for only allowing NAT IPs allocated by Google Cloud
        Platform, or 'MANUAL_ONLY' for only user-allocated NAT IP addresses. Possible values: ["MANUAL_ONLY", "AUTO_ONLY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#nat_ip_allocate_option ComputeRouterNat#nat_ip_allocate_option}
        '''
        result = self._values.get("nat_ip_allocate_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nat_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Self-links of NAT IPs.

        Only valid if natIpAllocateOption
        is set to MANUAL_ONLY.
        If this field is used alongside with a count created list of address resources 'google_compute_address.foobar.*.self_link',
        the access level resource for the address resource must have a 'lifecycle' block with 'create_before_destroy = true' so
        the number of resources can be increased/decreased without triggering the 'resourceInUseByAnotherResource' error.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#nat_ips ComputeRouterNat#nat_ips}
        '''
        result = self._values.get("nat_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#project ComputeRouterNat#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where the router and NAT reside.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#region ComputeRouterNat#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRouterNatRules"]]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#rules ComputeRouterNat#rules}
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRouterNatRules"]]], result)

    @builtins.property
    def source_subnetwork_ip_ranges_to_nat64(self) -> typing.Optional[builtins.str]:
        '''Specify the Nat option for NAT64, which can take one of the following values: ALL_IPV6_SUBNETWORKS: All of the IP ranges in every Subnetwork are allowed to Nat.

        LIST_OF_IPV6_SUBNETWORKS: A list of Subnetworks are allowed to Nat (specified in the field nat64Subnetwork below).
        Note that if this field contains NAT64_ALL_V6_SUBNETWORKS no other Router.Nat section in this region can also enable NAT64 for any Subnetworks in this network.
        Other Router.Nat sections can still be present to enable NAT44 only. Possible values: ["ALL_IPV6_SUBNETWORKS", "LIST_OF_IPV6_SUBNETWORKS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#source_subnetwork_ip_ranges_to_nat64 ComputeRouterNat#source_subnetwork_ip_ranges_to_nat64}
        '''
        result = self._values.get("source_subnetwork_ip_ranges_to_nat64")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRouterNatSubnetwork"]]]:
        '''subnetwork block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#subnetwork ComputeRouterNat#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRouterNatSubnetwork"]]], result)

    @builtins.property
    def tcp_established_idle_timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''Timeout (in seconds) for TCP established connections. Defaults to 1200s if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#tcp_established_idle_timeout_sec ComputeRouterNat#tcp_established_idle_timeout_sec}
        '''
        result = self._values.get("tcp_established_idle_timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tcp_time_wait_timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''Timeout (in seconds) for TCP connections that are in TIME_WAIT state. Defaults to 120s if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#tcp_time_wait_timeout_sec ComputeRouterNat#tcp_time_wait_timeout_sec}
        '''
        result = self._values.get("tcp_time_wait_timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tcp_transitory_idle_timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''Timeout (in seconds) for TCP transitory connections. Defaults to 30s if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#tcp_transitory_idle_timeout_sec ComputeRouterNat#tcp_transitory_idle_timeout_sec}
        '''
        result = self._values.get("tcp_transitory_idle_timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeRouterNatTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#timeouts ComputeRouterNat#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeRouterNatTimeouts"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Indicates whether this NAT is used for public or private IP translation.

        If unspecified, it defaults to PUBLIC.
        If 'PUBLIC' NAT used for public IP translation.
        If 'PRIVATE' NAT used for private IP translation. Default value: "PUBLIC" Possible values: ["PUBLIC", "PRIVATE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#type ComputeRouterNat#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def udp_idle_timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''Timeout (in seconds) for UDP connections. Defaults to 30s if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#udp_idle_timeout_sec ComputeRouterNat#udp_idle_timeout_sec}
        '''
        result = self._values.get("udp_idle_timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouterNatConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRouterNat.ComputeRouterNatLogConfig",
    jsii_struct_bases=[],
    name_mapping={"enable": "enable", "filter": "filter"},
)
class ComputeRouterNatLogConfig:
    def __init__(
        self,
        *,
        enable: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        filter: builtins.str,
    ) -> None:
        '''
        :param enable: Indicates whether or not to export logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#enable ComputeRouterNat#enable}
        :param filter: Specifies the desired filtering of logs on this NAT. Possible values: ["ERRORS_ONLY", "TRANSLATIONS_ONLY", "ALL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#filter ComputeRouterNat#filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ac7e9111b29dd0c3195cf35bae9c3fd93f9c2cef0237e0b8ed89bc083a12df0)
            check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable": enable,
            "filter": filter,
        }

    @builtins.property
    def enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Indicates whether or not to export logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#enable ComputeRouterNat#enable}
        '''
        result = self._values.get("enable")
        assert result is not None, "Required property 'enable' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def filter(self) -> builtins.str:
        '''Specifies the desired filtering of logs on this NAT. Possible values: ["ERRORS_ONLY", "TRANSLATIONS_ONLY", "ALL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#filter ComputeRouterNat#filter}
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouterNatLogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRouterNatLogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouterNat.ComputeRouterNatLogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55daea8be85cb0f5082b02bac8d58cacdc31b20dbd01efe1e4d471d934b74701)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enableInput")
    def enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="enable")
    def enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enable"))

    @enable.setter
    def enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceadc783fbef85cffb93bc9b1aee5eaf4e3b19bab7a21a903935af7a354e6b39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filter"))

    @filter.setter
    def filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c69bb065015c9dde1d1f36db98ae2df780331561f5a2ee78c27b8385009c2ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeRouterNatLogConfig]:
        return typing.cast(typing.Optional[ComputeRouterNatLogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ComputeRouterNatLogConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a4ccfa44d87a0e056e8745c1911fc29e9163a655b0551407ee550b59731849f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRouterNat.ComputeRouterNatNat64Subnetwork",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class ComputeRouterNatNat64Subnetwork:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Self-link of the subnetwork resource that will use NAT64. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#name ComputeRouterNat#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58881a9600e55d739b5c3f410f9be5cdaa6437d561f6cc81ec85f03745d31b4a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Self-link of the subnetwork resource that will use NAT64.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#name ComputeRouterNat#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouterNatNat64Subnetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRouterNatNat64SubnetworkList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouterNat.ComputeRouterNatNat64SubnetworkList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29ab0d5f45eec4626b95d414010c4f4f3e979b9afbc0c73f02d85e6dd38876ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRouterNatNat64SubnetworkOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b85d4b46312ef9ff3c34aeac44c49ddc063754e83577e89843847e3794c0239c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRouterNatNat64SubnetworkOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__059095611602b77af2a55d60f80bf4c8d9d4b386d9f4f305e7112fb5e08acf9d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ec6338c0e9ad4453b8665666c08a6e190964f990f22d24abdc22c300e109456)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51bb7cb5adb9872a772eaa483a6016e6796379ac3a934e5d411d838b44beaba7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterNatNat64Subnetwork]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterNatNat64Subnetwork]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterNatNat64Subnetwork]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55899cab8c0e6a1184fbccbfa1a597ca61880a2a7dcbca7ae1750d30248c579e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRouterNatNat64SubnetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouterNat.ComputeRouterNatNat64SubnetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cc2b13ed57f84162840960fa11d060107ff39df81879759a7484564a6fa0047)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c8e9dbaab70fcc7611c3aaf1c5a74b554e64716d0fe81c642d657c59b2945d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterNatNat64Subnetwork]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterNatNat64Subnetwork]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterNatNat64Subnetwork]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a12fd2a41d11cb700b55dfda0336965b08f9da8c033ace4737667911a4fc5a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRouterNat.ComputeRouterNatRules",
    jsii_struct_bases=[],
    name_mapping={
        "match": "match",
        "rule_number": "ruleNumber",
        "action": "action",
        "description": "description",
    },
)
class ComputeRouterNatRules:
    def __init__(
        self,
        *,
        match: builtins.str,
        rule_number: jsii.Number,
        action: typing.Optional[typing.Union["ComputeRouterNatRulesAction", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param match: CEL expression that specifies the match condition that egress traffic from a VM is evaluated against. If it evaluates to true, the corresponding action is enforced. The following examples are valid match expressions for public NAT: "inIpRange(destination.ip, '1.1.0.0/16') || inIpRange(destination.ip, '2.2.0.0/16')" "destination.ip == '1.1.0.1' || destination.ip == '8.8.8.8'" The following example is a valid match expression for private NAT: "nexthop.hub == 'https://networkconnectivity.googleapis.com/v1alpha1/projects/my-project/global/hub/hub-1'" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#match ComputeRouterNat#match}
        :param rule_number: An integer uniquely identifying a rule in the list. The rule number must be a positive value between 0 and 65000, and must be unique among rules within a NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#rule_number ComputeRouterNat#rule_number}
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#action ComputeRouterNat#action}
        :param description: An optional description of this rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#description ComputeRouterNat#description}
        '''
        if isinstance(action, dict):
            action = ComputeRouterNatRulesAction(**action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd6597aead9ae6e2adc194d40a2424ed6b0500df7df8518006948f71e5ae16f0)
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument rule_number", value=rule_number, expected_type=type_hints["rule_number"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "match": match,
            "rule_number": rule_number,
        }
        if action is not None:
            self._values["action"] = action
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def match(self) -> builtins.str:
        '''CEL expression that specifies the match condition that egress traffic from a VM is evaluated against.

        If it evaluates to true, the corresponding action is enforced.

        The following examples are valid match expressions for public NAT:

        "inIpRange(destination.ip, '1.1.0.0/16') || inIpRange(destination.ip, '2.2.0.0/16')"

        "destination.ip == '1.1.0.1' || destination.ip == '8.8.8.8'"

        The following example is a valid match expression for private NAT:

        "nexthop.hub == 'https://networkconnectivity.googleapis.com/v1alpha1/projects/my-project/global/hub/hub-1'"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#match ComputeRouterNat#match}
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_number(self) -> jsii.Number:
        '''An integer uniquely identifying a rule in the list.

        The rule number must be a positive value between 0 and 65000, and must be unique among rules within a NAT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#rule_number ComputeRouterNat#rule_number}
        '''
        result = self._values.get("rule_number")
        assert result is not None, "Required property 'rule_number' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def action(self) -> typing.Optional["ComputeRouterNatRulesAction"]:
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#action ComputeRouterNat#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional["ComputeRouterNatRulesAction"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#description ComputeRouterNat#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouterNatRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRouterNat.ComputeRouterNatRulesAction",
    jsii_struct_bases=[],
    name_mapping={
        "source_nat_active_ips": "sourceNatActiveIps",
        "source_nat_active_ranges": "sourceNatActiveRanges",
        "source_nat_drain_ips": "sourceNatDrainIps",
        "source_nat_drain_ranges": "sourceNatDrainRanges",
    },
)
class ComputeRouterNatRulesAction:
    def __init__(
        self,
        *,
        source_nat_active_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_nat_active_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_nat_drain_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_nat_drain_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param source_nat_active_ips: A list of URLs of the IP resources used for this NAT rule. These IP addresses must be valid static external IP addresses assigned to the project. This field is used for public NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#source_nat_active_ips ComputeRouterNat#source_nat_active_ips}
        :param source_nat_active_ranges: A list of URLs of the subnetworks used as source ranges for this NAT Rule. These subnetworks must have purpose set to PRIVATE_NAT. This field is used for private NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#source_nat_active_ranges ComputeRouterNat#source_nat_active_ranges}
        :param source_nat_drain_ips: A list of URLs of the IP resources to be drained. These IPs must be valid static external IPs that have been assigned to the NAT. These IPs should be used for updating/patching a NAT rule only. This field is used for public NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#source_nat_drain_ips ComputeRouterNat#source_nat_drain_ips}
        :param source_nat_drain_ranges: A list of URLs of subnetworks representing source ranges to be drained. This is only supported on patch/update, and these subnetworks must have previously been used as active ranges in this NAT Rule. This field is used for private NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#source_nat_drain_ranges ComputeRouterNat#source_nat_drain_ranges}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2ad1aa18d1d1653ddbd93335602de2a80da3cf76047fbb80604bfe924a3973c)
            check_type(argname="argument source_nat_active_ips", value=source_nat_active_ips, expected_type=type_hints["source_nat_active_ips"])
            check_type(argname="argument source_nat_active_ranges", value=source_nat_active_ranges, expected_type=type_hints["source_nat_active_ranges"])
            check_type(argname="argument source_nat_drain_ips", value=source_nat_drain_ips, expected_type=type_hints["source_nat_drain_ips"])
            check_type(argname="argument source_nat_drain_ranges", value=source_nat_drain_ranges, expected_type=type_hints["source_nat_drain_ranges"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if source_nat_active_ips is not None:
            self._values["source_nat_active_ips"] = source_nat_active_ips
        if source_nat_active_ranges is not None:
            self._values["source_nat_active_ranges"] = source_nat_active_ranges
        if source_nat_drain_ips is not None:
            self._values["source_nat_drain_ips"] = source_nat_drain_ips
        if source_nat_drain_ranges is not None:
            self._values["source_nat_drain_ranges"] = source_nat_drain_ranges

    @builtins.property
    def source_nat_active_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of URLs of the IP resources used for this NAT rule.

        These IP addresses must be valid static external IP addresses assigned to the project.
        This field is used for public NAT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#source_nat_active_ips ComputeRouterNat#source_nat_active_ips}
        '''
        result = self._values.get("source_nat_active_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source_nat_active_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of URLs of the subnetworks used as source ranges for this NAT Rule.

        These subnetworks must have purpose set to PRIVATE_NAT.
        This field is used for private NAT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#source_nat_active_ranges ComputeRouterNat#source_nat_active_ranges}
        '''
        result = self._values.get("source_nat_active_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source_nat_drain_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of URLs of the IP resources to be drained.

        These IPs must be valid static external IPs that have been assigned to the NAT.
        These IPs should be used for updating/patching a NAT rule only.
        This field is used for public NAT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#source_nat_drain_ips ComputeRouterNat#source_nat_drain_ips}
        '''
        result = self._values.get("source_nat_drain_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source_nat_drain_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of URLs of subnetworks representing source ranges to be drained.

        This is only supported on patch/update, and these subnetworks must have previously been used as active ranges in this NAT Rule.
        This field is used for private NAT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#source_nat_drain_ranges ComputeRouterNat#source_nat_drain_ranges}
        '''
        result = self._values.get("source_nat_drain_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouterNatRulesAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRouterNatRulesActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouterNat.ComputeRouterNatRulesActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__751d01489c4228e735e0cfaeef2e753e585a2f9d08580fdd90d95016a66320ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSourceNatActiveIps")
    def reset_source_nat_active_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceNatActiveIps", []))

    @jsii.member(jsii_name="resetSourceNatActiveRanges")
    def reset_source_nat_active_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceNatActiveRanges", []))

    @jsii.member(jsii_name="resetSourceNatDrainIps")
    def reset_source_nat_drain_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceNatDrainIps", []))

    @jsii.member(jsii_name="resetSourceNatDrainRanges")
    def reset_source_nat_drain_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceNatDrainRanges", []))

    @builtins.property
    @jsii.member(jsii_name="sourceNatActiveIpsInput")
    def source_nat_active_ips_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourceNatActiveIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceNatActiveRangesInput")
    def source_nat_active_ranges_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourceNatActiveRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceNatDrainIpsInput")
    def source_nat_drain_ips_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourceNatDrainIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceNatDrainRangesInput")
    def source_nat_drain_ranges_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourceNatDrainRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceNatActiveIps")
    def source_nat_active_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceNatActiveIps"))

    @source_nat_active_ips.setter
    def source_nat_active_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a40aa2591c6e1df179f0c323f98cf06f313219c040158e9c111add6179f1d87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceNatActiveIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceNatActiveRanges")
    def source_nat_active_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceNatActiveRanges"))

    @source_nat_active_ranges.setter
    def source_nat_active_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40fab51639c7f14d856acf8e8b45467ddb2636002102d843dd8d1a4c9c17b0ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceNatActiveRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceNatDrainIps")
    def source_nat_drain_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceNatDrainIps"))

    @source_nat_drain_ips.setter
    def source_nat_drain_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ebfdc5991e4c910d63fd266cadfdb77593d80978e5b25130dade8ac0b7fc48e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceNatDrainIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceNatDrainRanges")
    def source_nat_drain_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceNatDrainRanges"))

    @source_nat_drain_ranges.setter
    def source_nat_drain_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ed6ce492c58bb40a308fdc5d9d56ff8882ddb7378591196dc61fb5ea0eca097)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceNatDrainRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeRouterNatRulesAction]:
        return typing.cast(typing.Optional[ComputeRouterNatRulesAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRouterNatRulesAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38aa2e8a3cebd677be28f9119bfbba4dcc336029002ad5599f5724ba94dec208)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRouterNatRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouterNat.ComputeRouterNatRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f89ef64c59ce72987a6e5a3c79d295a8eb124cae4b44df1637163831cad9abf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ComputeRouterNatRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac540cd3d9388c7c5bffbf5faf6213bcdb734134e18173c18e361028ddf457ef)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRouterNatRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79315f24468f30e8c36d7ba2e0c6709d55706dd0ae9cd995b4d6af17cddb040d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4b62006888045c9f7fa4f3fcd36703d6a4bb7847f0624ab012b011b01ff927d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5faae896d53f78179a3ef7a7a294c104bc94907b82a75e9a06ed9dd6cfa281cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterNatRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterNatRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterNatRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8316490e94566ae8cdd9b03f3ca0662c847d51c6a59d2dfd9b602588183f6c57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRouterNatRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouterNat.ComputeRouterNatRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__698367689473579720b79787b3d85670cfab436b91be28d0f5e50512a9397e57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        *,
        source_nat_active_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_nat_active_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_nat_drain_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_nat_drain_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param source_nat_active_ips: A list of URLs of the IP resources used for this NAT rule. These IP addresses must be valid static external IP addresses assigned to the project. This field is used for public NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#source_nat_active_ips ComputeRouterNat#source_nat_active_ips}
        :param source_nat_active_ranges: A list of URLs of the subnetworks used as source ranges for this NAT Rule. These subnetworks must have purpose set to PRIVATE_NAT. This field is used for private NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#source_nat_active_ranges ComputeRouterNat#source_nat_active_ranges}
        :param source_nat_drain_ips: A list of URLs of the IP resources to be drained. These IPs must be valid static external IPs that have been assigned to the NAT. These IPs should be used for updating/patching a NAT rule only. This field is used for public NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#source_nat_drain_ips ComputeRouterNat#source_nat_drain_ips}
        :param source_nat_drain_ranges: A list of URLs of subnetworks representing source ranges to be drained. This is only supported on patch/update, and these subnetworks must have previously been used as active ranges in this NAT Rule. This field is used for private NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#source_nat_drain_ranges ComputeRouterNat#source_nat_drain_ranges}
        '''
        value = ComputeRouterNatRulesAction(
            source_nat_active_ips=source_nat_active_ips,
            source_nat_active_ranges=source_nat_active_ranges,
            source_nat_drain_ips=source_nat_drain_ips,
            source_nat_drain_ranges=source_nat_drain_ranges,
        )

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> ComputeRouterNatRulesActionOutputReference:
        return typing.cast(ComputeRouterNatRulesActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[ComputeRouterNatRulesAction]:
        return typing.cast(typing.Optional[ComputeRouterNatRulesAction], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleNumberInput")
    def rule_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ruleNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd073c44ba2401c5ce5646984893a95a37880a9a05a50df6b9d4fda2cb324c44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "match"))

    @match.setter
    def match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09fa32220ef53e9edd16d0927a4922aebee83ff73eac014f0bb9d2ec288aa399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "match", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleNumber")
    def rule_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ruleNumber"))

    @rule_number.setter
    def rule_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9075e803ea7b53072e3a8147ce31ec7e6480f2e8cfe8b23f2b9f7faa403a67d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterNatRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterNatRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterNatRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15ed335c6d17ac0962030069a097dceb2ad358729052401d2546069ad53bfed5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRouterNat.ComputeRouterNatSubnetwork",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "source_ip_ranges_to_nat": "sourceIpRangesToNat",
        "secondary_ip_range_names": "secondaryIpRangeNames",
    },
)
class ComputeRouterNatSubnetwork:
    def __init__(
        self,
        *,
        name: builtins.str,
        source_ip_ranges_to_nat: typing.Sequence[builtins.str],
        secondary_ip_range_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: Self-link of subnetwork to NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#name ComputeRouterNat#name}
        :param source_ip_ranges_to_nat: List of options for which source IPs in the subnetwork should have NAT enabled. Supported values include: 'ALL_IP_RANGES', 'LIST_OF_SECONDARY_IP_RANGES', 'PRIMARY_IP_RANGE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#source_ip_ranges_to_nat ComputeRouterNat#source_ip_ranges_to_nat}
        :param secondary_ip_range_names: List of the secondary ranges of the subnetwork that are allowed to use NAT. This can be populated only if 'LIST_OF_SECONDARY_IP_RANGES' is one of the values in sourceIpRangesToNat Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#secondary_ip_range_names ComputeRouterNat#secondary_ip_range_names}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__359abc45e51d4ac084be009d4fa980c89340e830a3fbcc7518add50cc03fd1d1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source_ip_ranges_to_nat", value=source_ip_ranges_to_nat, expected_type=type_hints["source_ip_ranges_to_nat"])
            check_type(argname="argument secondary_ip_range_names", value=secondary_ip_range_names, expected_type=type_hints["secondary_ip_range_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "source_ip_ranges_to_nat": source_ip_ranges_to_nat,
        }
        if secondary_ip_range_names is not None:
            self._values["secondary_ip_range_names"] = secondary_ip_range_names

    @builtins.property
    def name(self) -> builtins.str:
        '''Self-link of subnetwork to NAT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#name ComputeRouterNat#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_ip_ranges_to_nat(self) -> typing.List[builtins.str]:
        '''List of options for which source IPs in the subnetwork should have NAT enabled. Supported values include: 'ALL_IP_RANGES', 'LIST_OF_SECONDARY_IP_RANGES', 'PRIMARY_IP_RANGE'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#source_ip_ranges_to_nat ComputeRouterNat#source_ip_ranges_to_nat}
        '''
        result = self._values.get("source_ip_ranges_to_nat")
        assert result is not None, "Required property 'source_ip_ranges_to_nat' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def secondary_ip_range_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of the secondary ranges of the subnetwork that are allowed to use NAT.

        This can be populated only if
        'LIST_OF_SECONDARY_IP_RANGES' is one of the values in
        sourceIpRangesToNat

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#secondary_ip_range_names ComputeRouterNat#secondary_ip_range_names}
        '''
        result = self._values.get("secondary_ip_range_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouterNatSubnetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRouterNatSubnetworkList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouterNat.ComputeRouterNatSubnetworkList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__559b00251e7e8e7d55298938a9ac53c454c9db99f0a0d188f123ce098255d9b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ComputeRouterNatSubnetworkOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2020c27ccd5d5d9ba78c3f61d2eea7d2cb2051489772b19045ea6480abc071c7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRouterNatSubnetworkOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9adc117e6e4487ae7c8156598cdb0171fb386c24b921c2bf4a592d00a4bb1750)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3c08162985e6edd3e693c0d80c6794ca8c3df751a04b4ef1488e0ca39313f72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8602596f16bc82a82c28c2f28a8f60b1c7c201e87140b68f83384897797d10eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterNatSubnetwork]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterNatSubnetwork]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterNatSubnetwork]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf4d6be86a507eac9e4b93079ea72d3ea8be6d39ce0c6a821a1395e1870d87e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRouterNatSubnetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouterNat.ComputeRouterNatSubnetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07d2ef900bd1467ea6785467504823335e27a90f979ebeb7e70bc35142305215)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSecondaryIpRangeNames")
    def reset_secondary_ip_range_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryIpRangeNames", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryIpRangeNamesInput")
    def secondary_ip_range_names_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "secondaryIpRangeNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceIpRangesToNatInput")
    def source_ip_ranges_to_nat_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourceIpRangesToNatInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__184ded61c6bdeb0bc1fdb7f9054ab6b13076cec5539a31e472e0d91fcd2d0a77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secondaryIpRangeNames")
    def secondary_ip_range_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "secondaryIpRangeNames"))

    @secondary_ip_range_names.setter
    def secondary_ip_range_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a02ad46a3d866e8d19b7fb2372cf3214369829594f2c15b6eacf77b97e175b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryIpRangeNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceIpRangesToNat")
    def source_ip_ranges_to_nat(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceIpRangesToNat"))

    @source_ip_ranges_to_nat.setter
    def source_ip_ranges_to_nat(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d58798ef93079871726f890d8a00339613d98a2ac9e06520a9be55428c94dddb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceIpRangesToNat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterNatSubnetwork]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterNatSubnetwork]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterNatSubnetwork]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bfaee9c62b88ef6bad82b187dc0e3ae91c21b637c93ae76725800535962e36c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRouterNat.ComputeRouterNatTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeRouterNatTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#create ComputeRouterNat#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#delete ComputeRouterNat#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#update ComputeRouterNat#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af7f86c8a0c5e314fb956845df5a83f13e9a1542c72cc8a7b6e0116e308fffbf)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#create ComputeRouterNat#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#delete ComputeRouterNat#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router_nat#update ComputeRouterNat#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouterNatTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRouterNatTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouterNat.ComputeRouterNatTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6482a5459461ddabb44b57aa15ffdad441106d3f466a682f3bda85dddf8e7f1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdb0415b11bafa647042049cc9b507f60ad4f141289d661d9e609557567fc93a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20e71bcaca147e74256e0747cea7b603a81a52eeaeacb5db238d95347822c07a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b77d522593f04322c2343772e8e56e66f290c58cb3fa56b904fa3b7d3bc37f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterNatTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterNatTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterNatTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40ab7fecf136e02a33c3c0e9b06f2e3fe492a5752f9ca212779a3b6c87f426f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeRouterNat",
    "ComputeRouterNatConfig",
    "ComputeRouterNatLogConfig",
    "ComputeRouterNatLogConfigOutputReference",
    "ComputeRouterNatNat64Subnetwork",
    "ComputeRouterNatNat64SubnetworkList",
    "ComputeRouterNatNat64SubnetworkOutputReference",
    "ComputeRouterNatRules",
    "ComputeRouterNatRulesAction",
    "ComputeRouterNatRulesActionOutputReference",
    "ComputeRouterNatRulesList",
    "ComputeRouterNatRulesOutputReference",
    "ComputeRouterNatSubnetwork",
    "ComputeRouterNatSubnetworkList",
    "ComputeRouterNatSubnetworkOutputReference",
    "ComputeRouterNatTimeouts",
    "ComputeRouterNatTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ae60cc72bda42e6a3f764beb311fa2ef6b29ace4eae8271a19188ee7973b2c11(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    router: builtins.str,
    source_subnetwork_ip_ranges_to_nat: builtins.str,
    auto_network_tier: typing.Optional[builtins.str] = None,
    drain_nat_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_dynamic_port_allocation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_endpoint_independent_mapping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    endpoint_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    icmp_idle_timeout_sec: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    initial_nat_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    log_config: typing.Optional[typing.Union[ComputeRouterNatLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    max_ports_per_vm: typing.Optional[jsii.Number] = None,
    min_ports_per_vm: typing.Optional[jsii.Number] = None,
    nat64_subnetwork: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRouterNatNat64Subnetwork, typing.Dict[builtins.str, typing.Any]]]]] = None,
    nat_ip_allocate_option: typing.Optional[builtins.str] = None,
    nat_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRouterNatRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    source_subnetwork_ip_ranges_to_nat64: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRouterNatSubnetwork, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tcp_established_idle_timeout_sec: typing.Optional[jsii.Number] = None,
    tcp_time_wait_timeout_sec: typing.Optional[jsii.Number] = None,
    tcp_transitory_idle_timeout_sec: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[ComputeRouterNatTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
    udp_idle_timeout_sec: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__b5f5e6d62a05f472fbe0a7a14aba0e0f23ca591a317261aa38c0281efa65f06f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dabed10e1bc13360dd44a355a367148ad239ea59874bc7f701573fa4f7b00c72(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRouterNatNat64Subnetwork, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14798c64093f3a8d3bfe8218b6aee4754e854a8c99d6e2532ca28a9b7ce471a7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRouterNatRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2474fa845c12a738bfe47f448ff473e2057e07a650fc7d48157890ab12853b87(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRouterNatSubnetwork, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12eca6bde0cd0ada177aec90164a139fe0a851523d63ae5aee3a994f896f2bb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc9cc1772f159edad8dc41e7a0f701519b8736e9c7b4b69966a7d6aad814ba3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d6e31a6f1d8550af8f1888d4df0bc7cd10d96ffce2e1f5b72857cbd439b6d3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd0821791e185b9c36403e11bdd9c15548e4d00009ff4c92eb08c7164787c98a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400e45afc8738e6b7b0a351755172aa58f06a20e3cc6c51ebb7852a84720f31b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b29077df3ddec6c418574f2073361a97ed7a8944c60945ddd01bad17ae6e249f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7110ba283d65153c95d63e400c964c6333d3781b74b9922a76ba2a4a46f8d5ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a021e855b6f7bf11b611d6af0628307841d8bcfb95323b34ee1d2b7df3d3edf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc367c2fd4477af7863b73fcf388bb811bd08565138d6493894041b880aa8f6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2cdcf6ba429f282c3eef56ee64156890a77f009332b5ec9a8c8d8adc9a9c238(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25d7b4b6922e9bd1c7a879887c973a8c98075aab34fc0d78937075afe45ee14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e673586211464907d1ea42a8cb806fe48eab01b885594a069f0ffa12f557b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aabea739aa81c0d0eed08df7bffcbdd43ead305b3d6a176713be13b2e1fe994(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b071a36d0749b256f23fb47e93759346510036a843f6d46361f07e403339129(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e299727e9fe12bb79bcf94e7315c71f9a62849fb8d836d667942c37da9328d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34d6d4f7d24be3937bffab37fe1b3b07976830894d855a9ba41efac3a2deb956(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e40da5030a63141d60a16677492f8d9cbae12d769e030bb1d1da087ebd8df9d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e40b9930689f1a0cd1093396c6b641262f96d5d6bf2f7169dc184a3576b05c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__039b6b7adcf7809a7c98536a8198975185ecae8c6b99322702c053f61ee8ba30(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36eb23ad55510fd4532eeb9dd86e907ffe94eaa4e6aca65cc627d3d82791a0fa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ea0bcaf6cf830ea2add2b3f439c2c79671b4e265f22d10a5f88a7ba3cc5816d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b34b2679a1d3bf3fe9151a18bd231245edb8cf1721ae170bd4beb423f16a1370(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71a30703e4061ef2ec85681bbcbdb739c943ed590c1ef039d8bec0e663a61e62(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4206e3123f14db114b0b184e0ac18276ac7bd0ccd157247ee559a26008a293ea(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    router: builtins.str,
    source_subnetwork_ip_ranges_to_nat: builtins.str,
    auto_network_tier: typing.Optional[builtins.str] = None,
    drain_nat_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_dynamic_port_allocation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_endpoint_independent_mapping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    endpoint_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    icmp_idle_timeout_sec: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    initial_nat_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    log_config: typing.Optional[typing.Union[ComputeRouterNatLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    max_ports_per_vm: typing.Optional[jsii.Number] = None,
    min_ports_per_vm: typing.Optional[jsii.Number] = None,
    nat64_subnetwork: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRouterNatNat64Subnetwork, typing.Dict[builtins.str, typing.Any]]]]] = None,
    nat_ip_allocate_option: typing.Optional[builtins.str] = None,
    nat_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRouterNatRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    source_subnetwork_ip_ranges_to_nat64: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRouterNatSubnetwork, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tcp_established_idle_timeout_sec: typing.Optional[jsii.Number] = None,
    tcp_time_wait_timeout_sec: typing.Optional[jsii.Number] = None,
    tcp_transitory_idle_timeout_sec: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[ComputeRouterNatTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
    udp_idle_timeout_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac7e9111b29dd0c3195cf35bae9c3fd93f9c2cef0237e0b8ed89bc083a12df0(
    *,
    enable: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    filter: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55daea8be85cb0f5082b02bac8d58cacdc31b20dbd01efe1e4d471d934b74701(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceadc783fbef85cffb93bc9b1aee5eaf4e3b19bab7a21a903935af7a354e6b39(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c69bb065015c9dde1d1f36db98ae2df780331561f5a2ee78c27b8385009c2ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a4ccfa44d87a0e056e8745c1911fc29e9163a655b0551407ee550b59731849f(
    value: typing.Optional[ComputeRouterNatLogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58881a9600e55d739b5c3f410f9be5cdaa6437d561f6cc81ec85f03745d31b4a(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29ab0d5f45eec4626b95d414010c4f4f3e979b9afbc0c73f02d85e6dd38876ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b85d4b46312ef9ff3c34aeac44c49ddc063754e83577e89843847e3794c0239c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__059095611602b77af2a55d60f80bf4c8d9d4b386d9f4f305e7112fb5e08acf9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ec6338c0e9ad4453b8665666c08a6e190964f990f22d24abdc22c300e109456(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51bb7cb5adb9872a772eaa483a6016e6796379ac3a934e5d411d838b44beaba7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55899cab8c0e6a1184fbccbfa1a597ca61880a2a7dcbca7ae1750d30248c579e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterNatNat64Subnetwork]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc2b13ed57f84162840960fa11d060107ff39df81879759a7484564a6fa0047(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c8e9dbaab70fcc7611c3aaf1c5a74b554e64716d0fe81c642d657c59b2945d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a12fd2a41d11cb700b55dfda0336965b08f9da8c033ace4737667911a4fc5a6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterNatNat64Subnetwork]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd6597aead9ae6e2adc194d40a2424ed6b0500df7df8518006948f71e5ae16f0(
    *,
    match: builtins.str,
    rule_number: jsii.Number,
    action: typing.Optional[typing.Union[ComputeRouterNatRulesAction, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ad1aa18d1d1653ddbd93335602de2a80da3cf76047fbb80604bfe924a3973c(
    *,
    source_nat_active_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_nat_active_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_nat_drain_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_nat_drain_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__751d01489c4228e735e0cfaeef2e753e585a2f9d08580fdd90d95016a66320ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a40aa2591c6e1df179f0c323f98cf06f313219c040158e9c111add6179f1d87(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40fab51639c7f14d856acf8e8b45467ddb2636002102d843dd8d1a4c9c17b0ed(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ebfdc5991e4c910d63fd266cadfdb77593d80978e5b25130dade8ac0b7fc48e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed6ce492c58bb40a308fdc5d9d56ff8882ddb7378591196dc61fb5ea0eca097(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38aa2e8a3cebd677be28f9119bfbba4dcc336029002ad5599f5724ba94dec208(
    value: typing.Optional[ComputeRouterNatRulesAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f89ef64c59ce72987a6e5a3c79d295a8eb124cae4b44df1637163831cad9abf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac540cd3d9388c7c5bffbf5faf6213bcdb734134e18173c18e361028ddf457ef(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79315f24468f30e8c36d7ba2e0c6709d55706dd0ae9cd995b4d6af17cddb040d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b62006888045c9f7fa4f3fcd36703d6a4bb7847f0624ab012b011b01ff927d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5faae896d53f78179a3ef7a7a294c104bc94907b82a75e9a06ed9dd6cfa281cb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8316490e94566ae8cdd9b03f3ca0662c847d51c6a59d2dfd9b602588183f6c57(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterNatRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__698367689473579720b79787b3d85670cfab436b91be28d0f5e50512a9397e57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd073c44ba2401c5ce5646984893a95a37880a9a05a50df6b9d4fda2cb324c44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09fa32220ef53e9edd16d0927a4922aebee83ff73eac014f0bb9d2ec288aa399(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9075e803ea7b53072e3a8147ce31ec7e6480f2e8cfe8b23f2b9f7faa403a67d6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ed335c6d17ac0962030069a097dceb2ad358729052401d2546069ad53bfed5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterNatRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__359abc45e51d4ac084be009d4fa980c89340e830a3fbcc7518add50cc03fd1d1(
    *,
    name: builtins.str,
    source_ip_ranges_to_nat: typing.Sequence[builtins.str],
    secondary_ip_range_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__559b00251e7e8e7d55298938a9ac53c454c9db99f0a0d188f123ce098255d9b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2020c27ccd5d5d9ba78c3f61d2eea7d2cb2051489772b19045ea6480abc071c7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9adc117e6e4487ae7c8156598cdb0171fb386c24b921c2bf4a592d00a4bb1750(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c08162985e6edd3e693c0d80c6794ca8c3df751a04b4ef1488e0ca39313f72(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8602596f16bc82a82c28c2f28a8f60b1c7c201e87140b68f83384897797d10eb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4d6be86a507eac9e4b93079ea72d3ea8be6d39ce0c6a821a1395e1870d87e6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterNatSubnetwork]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07d2ef900bd1467ea6785467504823335e27a90f979ebeb7e70bc35142305215(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__184ded61c6bdeb0bc1fdb7f9054ab6b13076cec5539a31e472e0d91fcd2d0a77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a02ad46a3d866e8d19b7fb2372cf3214369829594f2c15b6eacf77b97e175b3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58798ef93079871726f890d8a00339613d98a2ac9e06520a9be55428c94dddb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bfaee9c62b88ef6bad82b187dc0e3ae91c21b637c93ae76725800535962e36c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterNatSubnetwork]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7f86c8a0c5e314fb956845df5a83f13e9a1542c72cc8a7b6e0116e308fffbf(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6482a5459461ddabb44b57aa15ffdad441106d3f466a682f3bda85dddf8e7f1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdb0415b11bafa647042049cc9b507f60ad4f141289d661d9e609557567fc93a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20e71bcaca147e74256e0747cea7b603a81a52eeaeacb5db238d95347822c07a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b77d522593f04322c2343772e8e56e66f290c58cb3fa56b904fa3b7d3bc37f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ab7fecf136e02a33c3c0e9b06f2e3fe492a5752f9ca212779a3b6c87f426f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterNatTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
