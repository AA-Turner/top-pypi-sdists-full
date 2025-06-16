r'''
# `google_compute_router_nat`

Refer to the Terraform Registry for docs: [`google_compute_router_nat`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat).
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


class GoogleComputeRouterNat(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterNat.GoogleComputeRouterNat",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat google_compute_router_nat}.'''

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
        log_config: typing.Optional[typing.Union["GoogleComputeRouterNatLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        max_ports_per_vm: typing.Optional[jsii.Number] = None,
        min_ports_per_vm: typing.Optional[jsii.Number] = None,
        nat64_subnetwork: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRouterNatNat64Subnetwork", typing.Dict[builtins.str, typing.Any]]]]] = None,
        nat_ip_allocate_option: typing.Optional[builtins.str] = None,
        nat_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRouterNatRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source_subnetwork_ip_ranges_to_nat64: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRouterNatSubnetwork", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tcp_established_idle_timeout_sec: typing.Optional[jsii.Number] = None,
        tcp_time_wait_timeout_sec: typing.Optional[jsii.Number] = None,
        tcp_transitory_idle_timeout_sec: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeRouterNatTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat google_compute_router_nat} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the NAT service. The name must be 1-63 characters long and comply with RFC1035. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#name GoogleComputeRouterNat#name}
        :param router: The name of the Cloud Router in which this NAT will be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#router GoogleComputeRouterNat#router}
        :param source_subnetwork_ip_ranges_to_nat: How NAT should be configured per Subnetwork. If 'ALL_SUBNETWORKS_ALL_IP_RANGES', all of the IP ranges in every Subnetwork are allowed to Nat. If 'ALL_SUBNETWORKS_ALL_PRIMARY_IP_RANGES', all of the primary IP ranges in every Subnetwork are allowed to Nat. 'LIST_OF_SUBNETWORKS': A list of Subnetworks are allowed to Nat (specified in the field subnetwork below). Note that if this field contains ALL_SUBNETWORKS_ALL_IP_RANGES or ALL_SUBNETWORKS_ALL_PRIMARY_IP_RANGES, then there should not be any other RouterNat section in any Router for this network in this region. Possible values: ["ALL_SUBNETWORKS_ALL_IP_RANGES", "ALL_SUBNETWORKS_ALL_PRIMARY_IP_RANGES", "LIST_OF_SUBNETWORKS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#source_subnetwork_ip_ranges_to_nat GoogleComputeRouterNat#source_subnetwork_ip_ranges_to_nat}
        :param auto_network_tier: The network tier to use when automatically reserving NAT IP addresses. Must be one of: PREMIUM, STANDARD. If not specified, then the current project-level default tier is used. Possible values: ["PREMIUM", "STANDARD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#auto_network_tier GoogleComputeRouterNat#auto_network_tier}
        :param drain_nat_ips: A list of URLs of the IP resources to be drained. These IPs must be valid static external IPs that have been assigned to the NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#drain_nat_ips GoogleComputeRouterNat#drain_nat_ips}
        :param enable_dynamic_port_allocation: Enable Dynamic Port Allocation. If minPortsPerVm is set, minPortsPerVm must be set to a power of two greater than or equal to 32. If minPortsPerVm is not set, a minimum of 32 ports will be allocated to a VM from this NAT config. If maxPortsPerVm is set, maxPortsPerVm must be set to a power of two greater than minPortsPerVm. If maxPortsPerVm is not set, a maximum of 65536 ports will be allocated to a VM from this NAT config. Mutually exclusive with enableEndpointIndependentMapping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#enable_dynamic_port_allocation GoogleComputeRouterNat#enable_dynamic_port_allocation}
        :param enable_endpoint_independent_mapping: Enable endpoint independent mapping. For more information see the `official documentation <https://cloud.google.com/nat/docs/overview#specs-rfcs>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#enable_endpoint_independent_mapping GoogleComputeRouterNat#enable_endpoint_independent_mapping}
        :param endpoint_types: Specifies the endpoint Types supported by the NAT Gateway. Supported values include: 'ENDPOINT_TYPE_VM', 'ENDPOINT_TYPE_SWG', 'ENDPOINT_TYPE_MANAGED_PROXY_LB'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#endpoint_types GoogleComputeRouterNat#endpoint_types}
        :param icmp_idle_timeout_sec: Timeout (in seconds) for ICMP connections. Defaults to 30s if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#icmp_idle_timeout_sec GoogleComputeRouterNat#icmp_idle_timeout_sec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#id GoogleComputeRouterNat#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_nat_ips: Self-links of NAT IPs to be used as initial value for creation alongside a RouterNatAddress resource. Conflicts with natIps and drainNatIps. Only valid if natIpAllocateOption is set to MANUAL_ONLY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#initial_nat_ips GoogleComputeRouterNat#initial_nat_ips}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#log_config GoogleComputeRouterNat#log_config}
        :param max_ports_per_vm: Maximum number of ports allocated to a VM from this NAT. This field can only be set when enableDynamicPortAllocation is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#max_ports_per_vm GoogleComputeRouterNat#max_ports_per_vm}
        :param min_ports_per_vm: Minimum number of ports allocated to a VM from this NAT. Defaults to 64 for static port allocation and 32 dynamic port allocation if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#min_ports_per_vm GoogleComputeRouterNat#min_ports_per_vm}
        :param nat64_subnetwork: nat64_subnetwork block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#nat64_subnetwork GoogleComputeRouterNat#nat64_subnetwork}
        :param nat_ip_allocate_option: How external IPs should be allocated for this NAT. Valid values are 'AUTO_ONLY' for only allowing NAT IPs allocated by Google Cloud Platform, or 'MANUAL_ONLY' for only user-allocated NAT IP addresses. Possible values: ["MANUAL_ONLY", "AUTO_ONLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#nat_ip_allocate_option GoogleComputeRouterNat#nat_ip_allocate_option}
        :param nat_ips: Self-links of NAT IPs. Only valid if natIpAllocateOption is set to MANUAL_ONLY. If this field is used alongside with a count created list of address resources 'google_compute_address.foobar.*.self_link', the access level resource for the address resource must have a 'lifecycle' block with 'create_before_destroy = true' so the number of resources can be increased/decreased without triggering the 'resourceInUseByAnotherResource' error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#nat_ips GoogleComputeRouterNat#nat_ips}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#project GoogleComputeRouterNat#project}.
        :param region: Region where the router and NAT reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#region GoogleComputeRouterNat#region}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#rules GoogleComputeRouterNat#rules}
        :param source_subnetwork_ip_ranges_to_nat64: Specify the Nat option for NAT64, which can take one of the following values: ALL_IPV6_SUBNETWORKS: All of the IP ranges in every Subnetwork are allowed to Nat. LIST_OF_IPV6_SUBNETWORKS: A list of Subnetworks are allowed to Nat (specified in the field nat64Subnetwork below). Note that if this field contains NAT64_ALL_V6_SUBNETWORKS no other Router.Nat section in this region can also enable NAT64 for any Subnetworks in this network. Other Router.Nat sections can still be present to enable NAT44 only. Possible values: ["ALL_IPV6_SUBNETWORKS", "LIST_OF_IPV6_SUBNETWORKS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#source_subnetwork_ip_ranges_to_nat64 GoogleComputeRouterNat#source_subnetwork_ip_ranges_to_nat64}
        :param subnetwork: subnetwork block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#subnetwork GoogleComputeRouterNat#subnetwork}
        :param tcp_established_idle_timeout_sec: Timeout (in seconds) for TCP established connections. Defaults to 1200s if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#tcp_established_idle_timeout_sec GoogleComputeRouterNat#tcp_established_idle_timeout_sec}
        :param tcp_time_wait_timeout_sec: Timeout (in seconds) for TCP connections that are in TIME_WAIT state. Defaults to 120s if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#tcp_time_wait_timeout_sec GoogleComputeRouterNat#tcp_time_wait_timeout_sec}
        :param tcp_transitory_idle_timeout_sec: Timeout (in seconds) for TCP transitory connections. Defaults to 30s if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#tcp_transitory_idle_timeout_sec GoogleComputeRouterNat#tcp_transitory_idle_timeout_sec}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#timeouts GoogleComputeRouterNat#timeouts}
        :param type: Indicates whether this NAT is used for public or private IP translation. If unspecified, it defaults to PUBLIC. If 'PUBLIC' NAT used for public IP translation. If 'PRIVATE' NAT used for private IP translation. Default value: "PUBLIC" Possible values: ["PUBLIC", "PRIVATE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#type GoogleComputeRouterNat#type}
        :param udp_idle_timeout_sec: Timeout (in seconds) for UDP connections. Defaults to 30s if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#udp_idle_timeout_sec GoogleComputeRouterNat#udp_idle_timeout_sec}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e89b9fe6ed7d9979dbdab3f63c94e00ac1bac28a570d54057f2abe0bf1427ac9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleComputeRouterNatConfig(
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
        '''Generates CDKTF code for importing a GoogleComputeRouterNat resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleComputeRouterNat to import.
        :param import_from_id: The id of the existing GoogleComputeRouterNat that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleComputeRouterNat to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12697b391f2ac71424f9f6cfc62722e95b087fbe13c84a5152bc7fe91d909b0d)
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
        :param enable: Indicates whether or not to export logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#enable GoogleComputeRouterNat#enable}
        :param filter: Specifies the desired filtering of logs on this NAT. Possible values: ["ERRORS_ONLY", "TRANSLATIONS_ONLY", "ALL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#filter GoogleComputeRouterNat#filter}
        '''
        value = GoogleComputeRouterNatLogConfig(enable=enable, filter=filter)

        return typing.cast(None, jsii.invoke(self, "putLogConfig", [value]))

    @jsii.member(jsii_name="putNat64Subnetwork")
    def put_nat64_subnetwork(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRouterNatNat64Subnetwork", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1612dbd889ee7c3ed8d7de67d4cc89a2a313a2aead0ca22d797d153c67370d1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNat64Subnetwork", [value]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRouterNatRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81582edc60e5d799962b3f7a5101c1d3aaebd6bf8fa122a4fa815faace4b7a72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="putSubnetwork")
    def put_subnetwork(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRouterNatSubnetwork", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88d4770269e76ca5ccc755322b004c2312af6d4a00b13da0659de545108a155d)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#create GoogleComputeRouterNat#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#delete GoogleComputeRouterNat#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#update GoogleComputeRouterNat#update}.
        '''
        value = GoogleComputeRouterNatTimeouts(
            create=create, delete=delete, update=update
        )

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
    def log_config(self) -> "GoogleComputeRouterNatLogConfigOutputReference":
        return typing.cast("GoogleComputeRouterNatLogConfigOutputReference", jsii.get(self, "logConfig"))

    @builtins.property
    @jsii.member(jsii_name="nat64Subnetwork")
    def nat64_subnetwork(self) -> "GoogleComputeRouterNatNat64SubnetworkList":
        return typing.cast("GoogleComputeRouterNatNat64SubnetworkList", jsii.get(self, "nat64Subnetwork"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "GoogleComputeRouterNatRulesList":
        return typing.cast("GoogleComputeRouterNatRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> "GoogleComputeRouterNatSubnetworkList":
        return typing.cast("GoogleComputeRouterNatSubnetworkList", jsii.get(self, "subnetwork"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleComputeRouterNatTimeoutsOutputReference":
        return typing.cast("GoogleComputeRouterNatTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    def log_config_input(self) -> typing.Optional["GoogleComputeRouterNatLogConfig"]:
        return typing.cast(typing.Optional["GoogleComputeRouterNatLogConfig"], jsii.get(self, "logConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRouterNatNat64Subnetwork"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRouterNatNat64Subnetwork"]]], jsii.get(self, "nat64SubnetworkInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRouterNatRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRouterNatRules"]]], jsii.get(self, "rulesInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRouterNatSubnetwork"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRouterNatSubnetwork"]]], jsii.get(self, "subnetworkInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeRouterNatTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeRouterNatTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7358875aa3a04f7710c467bcb04f295c20624b5c9f5dfb0a6e747e83d5a718c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoNetworkTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="drainNatIps")
    def drain_nat_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "drainNatIps"))

    @drain_nat_ips.setter
    def drain_nat_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4db3145c733e4c5d1db92fd4f31d24c62566c30c7fa121082bb9ff75e748b94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f606451ba1fa5c90820d0e75c86eda7361065c21ad8d7dda6b5012953999d749)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f6a5bcdb19ce26c90a8e73dabd8d2775615fbf681fc546527884efc81abbc16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableEndpointIndependentMapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpointTypes")
    def endpoint_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "endpointTypes"))

    @endpoint_types.setter
    def endpoint_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d860c742b512f6eec907130c2e5da3a1217d52f3497e63f2f438a9f702868bf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="icmpIdleTimeoutSec")
    def icmp_idle_timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "icmpIdleTimeoutSec"))

    @icmp_idle_timeout_sec.setter
    def icmp_idle_timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20c211d19b456418b127536032a69a69bc6e90133943b3f6934a7315d4e0bc1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "icmpIdleTimeoutSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1902eb16606f4540070efba19028f207b88282563644f3e5134302b6637912fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialNatIps")
    def initial_nat_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "initialNatIps"))

    @initial_nat_ips.setter
    def initial_nat_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783c2dd2e9fa64923e095f4e17b10c9653ca1300f450885bc8b7974d6bf699c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialNatIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxPortsPerVm")
    def max_ports_per_vm(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPortsPerVm"))

    @max_ports_per_vm.setter
    def max_ports_per_vm(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bc875c7364e6df051ddf812b4c38c544c8f32cff9b1be392afc7e275c6eee79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPortsPerVm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minPortsPerVm")
    def min_ports_per_vm(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minPortsPerVm"))

    @min_ports_per_vm.setter
    def min_ports_per_vm(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d672b9a611ece0d6eeb7fd77ccd4c285f67eb14fc9128930d488d5abdb6b80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minPortsPerVm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e1cb7ff1597e5b8053255a0a4403277baa95dcaaac8546a66b83c12c5ac055d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="natIpAllocateOption")
    def nat_ip_allocate_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "natIpAllocateOption"))

    @nat_ip_allocate_option.setter
    def nat_ip_allocate_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce9b2335637825c0d87ca29327fb1174506d3bd799a1419dfe6649bff37e36a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "natIpAllocateOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="natIps")
    def nat_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "natIps"))

    @nat_ips.setter
    def nat_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecb4ec04d0cc2d251571015698d26df8fea80092f4a5b2ca66d4996963abdd4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "natIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf9798687877694c2357c76adb4342e004b050e9f20b09f9b5f9d754284a4538)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1549bdb3c304bd260d810bf6f2c4ab83353889906135101ac2ebfce1dd0992e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="router")
    def router(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "router"))

    @router.setter
    def router(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0be29a9be53ae5e3081a4bcd524694e2aebfd2d5d375ec7b44cb0493c5ddef2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "router", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceSubnetworkIpRangesToNat")
    def source_subnetwork_ip_ranges_to_nat(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceSubnetworkIpRangesToNat"))

    @source_subnetwork_ip_ranges_to_nat.setter
    def source_subnetwork_ip_ranges_to_nat(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__577ff110c2de3261e2b986d55ab3f79abeb2fb0c04698d2cd96148a0752b6aff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceSubnetworkIpRangesToNat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceSubnetworkIpRangesToNat64")
    def source_subnetwork_ip_ranges_to_nat64(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceSubnetworkIpRangesToNat64"))

    @source_subnetwork_ip_ranges_to_nat64.setter
    def source_subnetwork_ip_ranges_to_nat64(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7db610488d6edae04c727623179b86e616f1d85eba67c48d848e4f46bea121dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceSubnetworkIpRangesToNat64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tcpEstablishedIdleTimeoutSec")
    def tcp_established_idle_timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tcpEstablishedIdleTimeoutSec"))

    @tcp_established_idle_timeout_sec.setter
    def tcp_established_idle_timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85b826637bbf5d293481337ea75777cac253f7c11baa2dfed8d3a6baa4a38668)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tcpEstablishedIdleTimeoutSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tcpTimeWaitTimeoutSec")
    def tcp_time_wait_timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tcpTimeWaitTimeoutSec"))

    @tcp_time_wait_timeout_sec.setter
    def tcp_time_wait_timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__321bcd63f91b4913546cdfff21bc3ad61853b29eb2d20f8a61ed87c0bcd24f3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tcpTimeWaitTimeoutSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tcpTransitoryIdleTimeoutSec")
    def tcp_transitory_idle_timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tcpTransitoryIdleTimeoutSec"))

    @tcp_transitory_idle_timeout_sec.setter
    def tcp_transitory_idle_timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68d9a25e1d88296efe8a1352d367c8ff08f6f807e1f20f169e46c3278f196f66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tcpTransitoryIdleTimeoutSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74df9764453471e1e3db4729583048009847e527b0a4254b12653f4d0206db93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="udpIdleTimeoutSec")
    def udp_idle_timeout_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "udpIdleTimeoutSec"))

    @udp_idle_timeout_sec.setter
    def udp_idle_timeout_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__624e7e16deb8b13a4c7bf0d19a8217525cb068c0f0aa0cab5f6e6a8a3f70e09d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "udpIdleTimeoutSec", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterNat.GoogleComputeRouterNatConfig",
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
class GoogleComputeRouterNatConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        log_config: typing.Optional[typing.Union["GoogleComputeRouterNatLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        max_ports_per_vm: typing.Optional[jsii.Number] = None,
        min_ports_per_vm: typing.Optional[jsii.Number] = None,
        nat64_subnetwork: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRouterNatNat64Subnetwork", typing.Dict[builtins.str, typing.Any]]]]] = None,
        nat_ip_allocate_option: typing.Optional[builtins.str] = None,
        nat_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRouterNatRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source_subnetwork_ip_ranges_to_nat64: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRouterNatSubnetwork", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tcp_established_idle_timeout_sec: typing.Optional[jsii.Number] = None,
        tcp_time_wait_timeout_sec: typing.Optional[jsii.Number] = None,
        tcp_transitory_idle_timeout_sec: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeRouterNatTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param name: Name of the NAT service. The name must be 1-63 characters long and comply with RFC1035. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#name GoogleComputeRouterNat#name}
        :param router: The name of the Cloud Router in which this NAT will be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#router GoogleComputeRouterNat#router}
        :param source_subnetwork_ip_ranges_to_nat: How NAT should be configured per Subnetwork. If 'ALL_SUBNETWORKS_ALL_IP_RANGES', all of the IP ranges in every Subnetwork are allowed to Nat. If 'ALL_SUBNETWORKS_ALL_PRIMARY_IP_RANGES', all of the primary IP ranges in every Subnetwork are allowed to Nat. 'LIST_OF_SUBNETWORKS': A list of Subnetworks are allowed to Nat (specified in the field subnetwork below). Note that if this field contains ALL_SUBNETWORKS_ALL_IP_RANGES or ALL_SUBNETWORKS_ALL_PRIMARY_IP_RANGES, then there should not be any other RouterNat section in any Router for this network in this region. Possible values: ["ALL_SUBNETWORKS_ALL_IP_RANGES", "ALL_SUBNETWORKS_ALL_PRIMARY_IP_RANGES", "LIST_OF_SUBNETWORKS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#source_subnetwork_ip_ranges_to_nat GoogleComputeRouterNat#source_subnetwork_ip_ranges_to_nat}
        :param auto_network_tier: The network tier to use when automatically reserving NAT IP addresses. Must be one of: PREMIUM, STANDARD. If not specified, then the current project-level default tier is used. Possible values: ["PREMIUM", "STANDARD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#auto_network_tier GoogleComputeRouterNat#auto_network_tier}
        :param drain_nat_ips: A list of URLs of the IP resources to be drained. These IPs must be valid static external IPs that have been assigned to the NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#drain_nat_ips GoogleComputeRouterNat#drain_nat_ips}
        :param enable_dynamic_port_allocation: Enable Dynamic Port Allocation. If minPortsPerVm is set, minPortsPerVm must be set to a power of two greater than or equal to 32. If minPortsPerVm is not set, a minimum of 32 ports will be allocated to a VM from this NAT config. If maxPortsPerVm is set, maxPortsPerVm must be set to a power of two greater than minPortsPerVm. If maxPortsPerVm is not set, a maximum of 65536 ports will be allocated to a VM from this NAT config. Mutually exclusive with enableEndpointIndependentMapping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#enable_dynamic_port_allocation GoogleComputeRouterNat#enable_dynamic_port_allocation}
        :param enable_endpoint_independent_mapping: Enable endpoint independent mapping. For more information see the `official documentation <https://cloud.google.com/nat/docs/overview#specs-rfcs>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#enable_endpoint_independent_mapping GoogleComputeRouterNat#enable_endpoint_independent_mapping}
        :param endpoint_types: Specifies the endpoint Types supported by the NAT Gateway. Supported values include: 'ENDPOINT_TYPE_VM', 'ENDPOINT_TYPE_SWG', 'ENDPOINT_TYPE_MANAGED_PROXY_LB'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#endpoint_types GoogleComputeRouterNat#endpoint_types}
        :param icmp_idle_timeout_sec: Timeout (in seconds) for ICMP connections. Defaults to 30s if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#icmp_idle_timeout_sec GoogleComputeRouterNat#icmp_idle_timeout_sec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#id GoogleComputeRouterNat#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_nat_ips: Self-links of NAT IPs to be used as initial value for creation alongside a RouterNatAddress resource. Conflicts with natIps and drainNatIps. Only valid if natIpAllocateOption is set to MANUAL_ONLY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#initial_nat_ips GoogleComputeRouterNat#initial_nat_ips}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#log_config GoogleComputeRouterNat#log_config}
        :param max_ports_per_vm: Maximum number of ports allocated to a VM from this NAT. This field can only be set when enableDynamicPortAllocation is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#max_ports_per_vm GoogleComputeRouterNat#max_ports_per_vm}
        :param min_ports_per_vm: Minimum number of ports allocated to a VM from this NAT. Defaults to 64 for static port allocation and 32 dynamic port allocation if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#min_ports_per_vm GoogleComputeRouterNat#min_ports_per_vm}
        :param nat64_subnetwork: nat64_subnetwork block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#nat64_subnetwork GoogleComputeRouterNat#nat64_subnetwork}
        :param nat_ip_allocate_option: How external IPs should be allocated for this NAT. Valid values are 'AUTO_ONLY' for only allowing NAT IPs allocated by Google Cloud Platform, or 'MANUAL_ONLY' for only user-allocated NAT IP addresses. Possible values: ["MANUAL_ONLY", "AUTO_ONLY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#nat_ip_allocate_option GoogleComputeRouterNat#nat_ip_allocate_option}
        :param nat_ips: Self-links of NAT IPs. Only valid if natIpAllocateOption is set to MANUAL_ONLY. If this field is used alongside with a count created list of address resources 'google_compute_address.foobar.*.self_link', the access level resource for the address resource must have a 'lifecycle' block with 'create_before_destroy = true' so the number of resources can be increased/decreased without triggering the 'resourceInUseByAnotherResource' error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#nat_ips GoogleComputeRouterNat#nat_ips}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#project GoogleComputeRouterNat#project}.
        :param region: Region where the router and NAT reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#region GoogleComputeRouterNat#region}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#rules GoogleComputeRouterNat#rules}
        :param source_subnetwork_ip_ranges_to_nat64: Specify the Nat option for NAT64, which can take one of the following values: ALL_IPV6_SUBNETWORKS: All of the IP ranges in every Subnetwork are allowed to Nat. LIST_OF_IPV6_SUBNETWORKS: A list of Subnetworks are allowed to Nat (specified in the field nat64Subnetwork below). Note that if this field contains NAT64_ALL_V6_SUBNETWORKS no other Router.Nat section in this region can also enable NAT64 for any Subnetworks in this network. Other Router.Nat sections can still be present to enable NAT44 only. Possible values: ["ALL_IPV6_SUBNETWORKS", "LIST_OF_IPV6_SUBNETWORKS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#source_subnetwork_ip_ranges_to_nat64 GoogleComputeRouterNat#source_subnetwork_ip_ranges_to_nat64}
        :param subnetwork: subnetwork block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#subnetwork GoogleComputeRouterNat#subnetwork}
        :param tcp_established_idle_timeout_sec: Timeout (in seconds) for TCP established connections. Defaults to 1200s if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#tcp_established_idle_timeout_sec GoogleComputeRouterNat#tcp_established_idle_timeout_sec}
        :param tcp_time_wait_timeout_sec: Timeout (in seconds) for TCP connections that are in TIME_WAIT state. Defaults to 120s if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#tcp_time_wait_timeout_sec GoogleComputeRouterNat#tcp_time_wait_timeout_sec}
        :param tcp_transitory_idle_timeout_sec: Timeout (in seconds) for TCP transitory connections. Defaults to 30s if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#tcp_transitory_idle_timeout_sec GoogleComputeRouterNat#tcp_transitory_idle_timeout_sec}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#timeouts GoogleComputeRouterNat#timeouts}
        :param type: Indicates whether this NAT is used for public or private IP translation. If unspecified, it defaults to PUBLIC. If 'PUBLIC' NAT used for public IP translation. If 'PRIVATE' NAT used for private IP translation. Default value: "PUBLIC" Possible values: ["PUBLIC", "PRIVATE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#type GoogleComputeRouterNat#type}
        :param udp_idle_timeout_sec: Timeout (in seconds) for UDP connections. Defaults to 30s if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#udp_idle_timeout_sec GoogleComputeRouterNat#udp_idle_timeout_sec}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(log_config, dict):
            log_config = GoogleComputeRouterNatLogConfig(**log_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleComputeRouterNatTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e23c7ecbb1c5e52f3baf9117670313ebceb677af82ebc66f26e9e8430b8c8cb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#name GoogleComputeRouterNat#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def router(self) -> builtins.str:
        '''The name of the Cloud Router in which this NAT will be configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#router GoogleComputeRouterNat#router}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#source_subnetwork_ip_ranges_to_nat GoogleComputeRouterNat#source_subnetwork_ip_ranges_to_nat}
        '''
        result = self._values.get("source_subnetwork_ip_ranges_to_nat")
        assert result is not None, "Required property 'source_subnetwork_ip_ranges_to_nat' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_network_tier(self) -> typing.Optional[builtins.str]:
        '''The network tier to use when automatically reserving NAT IP addresses.

        Must be one of: PREMIUM, STANDARD. If not specified, then the current
        project-level default tier is used. Possible values: ["PREMIUM", "STANDARD"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#auto_network_tier GoogleComputeRouterNat#auto_network_tier}
        '''
        result = self._values.get("auto_network_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def drain_nat_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of URLs of the IP resources to be drained.

        These IPs must be
        valid static external IPs that have been assigned to the NAT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#drain_nat_ips GoogleComputeRouterNat#drain_nat_ips}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#enable_dynamic_port_allocation GoogleComputeRouterNat#enable_dynamic_port_allocation}
        '''
        result = self._values.get("enable_dynamic_port_allocation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_endpoint_independent_mapping(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable endpoint independent mapping. For more information see the `official documentation <https://cloud.google.com/nat/docs/overview#specs-rfcs>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#enable_endpoint_independent_mapping GoogleComputeRouterNat#enable_endpoint_independent_mapping}
        '''
        result = self._values.get("enable_endpoint_independent_mapping")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def endpoint_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the endpoint Types supported by the NAT Gateway.

        Supported values include:
        'ENDPOINT_TYPE_VM', 'ENDPOINT_TYPE_SWG',
        'ENDPOINT_TYPE_MANAGED_PROXY_LB'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#endpoint_types GoogleComputeRouterNat#endpoint_types}
        '''
        result = self._values.get("endpoint_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def icmp_idle_timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''Timeout (in seconds) for ICMP connections. Defaults to 30s if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#icmp_idle_timeout_sec GoogleComputeRouterNat#icmp_idle_timeout_sec}
        '''
        result = self._values.get("icmp_idle_timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#id GoogleComputeRouterNat#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_nat_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Self-links of NAT IPs to be used as initial value for creation alongside a RouterNatAddress resource.

        Conflicts with natIps and drainNatIps. Only valid if natIpAllocateOption is set to MANUAL_ONLY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#initial_nat_ips GoogleComputeRouterNat#initial_nat_ips}
        '''
        result = self._values.get("initial_nat_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def log_config(self) -> typing.Optional["GoogleComputeRouterNatLogConfig"]:
        '''log_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#log_config GoogleComputeRouterNat#log_config}
        '''
        result = self._values.get("log_config")
        return typing.cast(typing.Optional["GoogleComputeRouterNatLogConfig"], result)

    @builtins.property
    def max_ports_per_vm(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of ports allocated to a VM from this NAT.

        This field can only be set when enableDynamicPortAllocation is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#max_ports_per_vm GoogleComputeRouterNat#max_ports_per_vm}
        '''
        result = self._values.get("max_ports_per_vm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_ports_per_vm(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of ports allocated to a VM from this NAT.

        Defaults to 64 for static port allocation and 32 dynamic port allocation if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#min_ports_per_vm GoogleComputeRouterNat#min_ports_per_vm}
        '''
        result = self._values.get("min_ports_per_vm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nat64_subnetwork(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRouterNatNat64Subnetwork"]]]:
        '''nat64_subnetwork block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#nat64_subnetwork GoogleComputeRouterNat#nat64_subnetwork}
        '''
        result = self._values.get("nat64_subnetwork")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRouterNatNat64Subnetwork"]]], result)

    @builtins.property
    def nat_ip_allocate_option(self) -> typing.Optional[builtins.str]:
        '''How external IPs should be allocated for this NAT.

        Valid values are
        'AUTO_ONLY' for only allowing NAT IPs allocated by Google Cloud
        Platform, or 'MANUAL_ONLY' for only user-allocated NAT IP addresses. Possible values: ["MANUAL_ONLY", "AUTO_ONLY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#nat_ip_allocate_option GoogleComputeRouterNat#nat_ip_allocate_option}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#nat_ips GoogleComputeRouterNat#nat_ips}
        '''
        result = self._values.get("nat_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#project GoogleComputeRouterNat#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where the router and NAT reside.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#region GoogleComputeRouterNat#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRouterNatRules"]]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#rules GoogleComputeRouterNat#rules}
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRouterNatRules"]]], result)

    @builtins.property
    def source_subnetwork_ip_ranges_to_nat64(self) -> typing.Optional[builtins.str]:
        '''Specify the Nat option for NAT64, which can take one of the following values: ALL_IPV6_SUBNETWORKS: All of the IP ranges in every Subnetwork are allowed to Nat.

        LIST_OF_IPV6_SUBNETWORKS: A list of Subnetworks are allowed to Nat (specified in the field nat64Subnetwork below).
        Note that if this field contains NAT64_ALL_V6_SUBNETWORKS no other Router.Nat section in this region can also enable NAT64 for any Subnetworks in this network.
        Other Router.Nat sections can still be present to enable NAT44 only. Possible values: ["ALL_IPV6_SUBNETWORKS", "LIST_OF_IPV6_SUBNETWORKS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#source_subnetwork_ip_ranges_to_nat64 GoogleComputeRouterNat#source_subnetwork_ip_ranges_to_nat64}
        '''
        result = self._values.get("source_subnetwork_ip_ranges_to_nat64")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRouterNatSubnetwork"]]]:
        '''subnetwork block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#subnetwork GoogleComputeRouterNat#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRouterNatSubnetwork"]]], result)

    @builtins.property
    def tcp_established_idle_timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''Timeout (in seconds) for TCP established connections. Defaults to 1200s if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#tcp_established_idle_timeout_sec GoogleComputeRouterNat#tcp_established_idle_timeout_sec}
        '''
        result = self._values.get("tcp_established_idle_timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tcp_time_wait_timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''Timeout (in seconds) for TCP connections that are in TIME_WAIT state. Defaults to 120s if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#tcp_time_wait_timeout_sec GoogleComputeRouterNat#tcp_time_wait_timeout_sec}
        '''
        result = self._values.get("tcp_time_wait_timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tcp_transitory_idle_timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''Timeout (in seconds) for TCP transitory connections. Defaults to 30s if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#tcp_transitory_idle_timeout_sec GoogleComputeRouterNat#tcp_transitory_idle_timeout_sec}
        '''
        result = self._values.get("tcp_transitory_idle_timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleComputeRouterNatTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#timeouts GoogleComputeRouterNat#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleComputeRouterNatTimeouts"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Indicates whether this NAT is used for public or private IP translation.

        If unspecified, it defaults to PUBLIC.
        If 'PUBLIC' NAT used for public IP translation.
        If 'PRIVATE' NAT used for private IP translation. Default value: "PUBLIC" Possible values: ["PUBLIC", "PRIVATE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#type GoogleComputeRouterNat#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def udp_idle_timeout_sec(self) -> typing.Optional[jsii.Number]:
        '''Timeout (in seconds) for UDP connections. Defaults to 30s if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#udp_idle_timeout_sec GoogleComputeRouterNat#udp_idle_timeout_sec}
        '''
        result = self._values.get("udp_idle_timeout_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRouterNatConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterNat.GoogleComputeRouterNatLogConfig",
    jsii_struct_bases=[],
    name_mapping={"enable": "enable", "filter": "filter"},
)
class GoogleComputeRouterNatLogConfig:
    def __init__(
        self,
        *,
        enable: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        filter: builtins.str,
    ) -> None:
        '''
        :param enable: Indicates whether or not to export logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#enable GoogleComputeRouterNat#enable}
        :param filter: Specifies the desired filtering of logs on this NAT. Possible values: ["ERRORS_ONLY", "TRANSLATIONS_ONLY", "ALL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#filter GoogleComputeRouterNat#filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7851e19286f9848a6154dd01e64c9ead24aa5ba728fe28af26d0c2dbdcb20eeb)
            check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable": enable,
            "filter": filter,
        }

    @builtins.property
    def enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Indicates whether or not to export logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#enable GoogleComputeRouterNat#enable}
        '''
        result = self._values.get("enable")
        assert result is not None, "Required property 'enable' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def filter(self) -> builtins.str:
        '''Specifies the desired filtering of logs on this NAT. Possible values: ["ERRORS_ONLY", "TRANSLATIONS_ONLY", "ALL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#filter GoogleComputeRouterNat#filter}
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRouterNatLogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRouterNatLogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterNat.GoogleComputeRouterNatLogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13c23a6d667a0857f2567ca28d1f9f9034c115faabc04457a9d90d99da187577)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bb8335565230905046f8005c3a4c7cecbcc8717a79078f6552781b18fe03709)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filter"))

    @filter.setter
    def filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9301ab671cffc194507e35c490d7c616004212a9c0b7b4347ad8cfa3029ad645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleComputeRouterNatLogConfig]:
        return typing.cast(typing.Optional[GoogleComputeRouterNatLogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRouterNatLogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb98a325815a7924a47ffe21145ea2f9bad8e91a96db0c013c785a4e57b9c442)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterNat.GoogleComputeRouterNatNat64Subnetwork",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GoogleComputeRouterNatNat64Subnetwork:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Self-link of the subnetwork resource that will use NAT64. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#name GoogleComputeRouterNat#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e92da51bce397a31a9b268aa25324dad92e57c329e7a7d985b3552a4975b4b9f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Self-link of the subnetwork resource that will use NAT64.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#name GoogleComputeRouterNat#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRouterNatNat64Subnetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRouterNatNat64SubnetworkList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterNat.GoogleComputeRouterNatNat64SubnetworkList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15f7a7a546a5192906257db0b0f8504133519f44e1e42c3455b769d79b43f349)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeRouterNatNat64SubnetworkOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71ba18d2ff799eb0ca71e981d75c63da1b12231846b0ba80e961b245d55f4c40)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeRouterNatNat64SubnetworkOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b767d81a702a4ecbf98e4e5098e99e1cf52fda226527bce72e881437771c338c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93229a303c56148bcaae63e0569492ac289b8d90c42bc432ce162a541cd06aaa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c3347823d3a914359aabf6633ab9942b3385738a1c2c7e28eab894e7759862a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRouterNatNat64Subnetwork]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRouterNatNat64Subnetwork]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRouterNatNat64Subnetwork]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__193b4e1530225f6b47a9335bd4d1aa97f30edf353b0c4cd8eb0f76a58bd52d22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRouterNatNat64SubnetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterNat.GoogleComputeRouterNatNat64SubnetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2a6114363209734af574b3dee9b9556d3a18a4d021f1323ea5ad6746ddfeaf0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cb03c48312e09c65b608bb729bda9e3aff5cae9f6552fa9ce9664ae3afc0b51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterNatNat64Subnetwork]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterNatNat64Subnetwork]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterNatNat64Subnetwork]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2628f58369f82268f0e0c144f22d067f7d064029a5fb45dd3b6c0b360f7f7344)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterNat.GoogleComputeRouterNatRules",
    jsii_struct_bases=[],
    name_mapping={
        "match": "match",
        "rule_number": "ruleNumber",
        "action": "action",
        "description": "description",
    },
)
class GoogleComputeRouterNatRules:
    def __init__(
        self,
        *,
        match: builtins.str,
        rule_number: jsii.Number,
        action: typing.Optional[typing.Union["GoogleComputeRouterNatRulesAction", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param match: CEL expression that specifies the match condition that egress traffic from a VM is evaluated against. If it evaluates to true, the corresponding action is enforced. The following examples are valid match expressions for public NAT: "inIpRange(destination.ip, '1.1.0.0/16') || inIpRange(destination.ip, '2.2.0.0/16')" "destination.ip == '1.1.0.1' || destination.ip == '8.8.8.8'" The following example is a valid match expression for private NAT: "nexthop.hub == 'https://networkconnectivity.googleapis.com/v1alpha1/projects/my-project/global/hub/hub-1'" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#match GoogleComputeRouterNat#match}
        :param rule_number: An integer uniquely identifying a rule in the list. The rule number must be a positive value between 0 and 65000, and must be unique among rules within a NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#rule_number GoogleComputeRouterNat#rule_number}
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#action GoogleComputeRouterNat#action}
        :param description: An optional description of this rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#description GoogleComputeRouterNat#description}
        '''
        if isinstance(action, dict):
            action = GoogleComputeRouterNatRulesAction(**action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7069d07f3da1def43b683db25df9bb12513a393a34c7173afb2485b9e0976186)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#match GoogleComputeRouterNat#match}
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_number(self) -> jsii.Number:
        '''An integer uniquely identifying a rule in the list.

        The rule number must be a positive value between 0 and 65000, and must be unique among rules within a NAT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#rule_number GoogleComputeRouterNat#rule_number}
        '''
        result = self._values.get("rule_number")
        assert result is not None, "Required property 'rule_number' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def action(self) -> typing.Optional["GoogleComputeRouterNatRulesAction"]:
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#action GoogleComputeRouterNat#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional["GoogleComputeRouterNatRulesAction"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#description GoogleComputeRouterNat#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRouterNatRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterNat.GoogleComputeRouterNatRulesAction",
    jsii_struct_bases=[],
    name_mapping={
        "source_nat_active_ips": "sourceNatActiveIps",
        "source_nat_active_ranges": "sourceNatActiveRanges",
        "source_nat_drain_ips": "sourceNatDrainIps",
        "source_nat_drain_ranges": "sourceNatDrainRanges",
    },
)
class GoogleComputeRouterNatRulesAction:
    def __init__(
        self,
        *,
        source_nat_active_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_nat_active_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_nat_drain_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        source_nat_drain_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param source_nat_active_ips: A list of URLs of the IP resources used for this NAT rule. These IP addresses must be valid static external IP addresses assigned to the project. This field is used for public NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#source_nat_active_ips GoogleComputeRouterNat#source_nat_active_ips}
        :param source_nat_active_ranges: A list of URLs of the subnetworks used as source ranges for this NAT Rule. These subnetworks must have purpose set to PRIVATE_NAT. This field is used for private NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#source_nat_active_ranges GoogleComputeRouterNat#source_nat_active_ranges}
        :param source_nat_drain_ips: A list of URLs of the IP resources to be drained. These IPs must be valid static external IPs that have been assigned to the NAT. These IPs should be used for updating/patching a NAT rule only. This field is used for public NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#source_nat_drain_ips GoogleComputeRouterNat#source_nat_drain_ips}
        :param source_nat_drain_ranges: A list of URLs of subnetworks representing source ranges to be drained. This is only supported on patch/update, and these subnetworks must have previously been used as active ranges in this NAT Rule. This field is used for private NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#source_nat_drain_ranges GoogleComputeRouterNat#source_nat_drain_ranges}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39b87590f4956db95bbddf8927cc9c37de4c957938ec0efd62f8283ecc9e0e7e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#source_nat_active_ips GoogleComputeRouterNat#source_nat_active_ips}
        '''
        result = self._values.get("source_nat_active_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source_nat_active_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of URLs of the subnetworks used as source ranges for this NAT Rule.

        These subnetworks must have purpose set to PRIVATE_NAT.
        This field is used for private NAT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#source_nat_active_ranges GoogleComputeRouterNat#source_nat_active_ranges}
        '''
        result = self._values.get("source_nat_active_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source_nat_drain_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of URLs of the IP resources to be drained.

        These IPs must be valid static external IPs that have been assigned to the NAT.
        These IPs should be used for updating/patching a NAT rule only.
        This field is used for public NAT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#source_nat_drain_ips GoogleComputeRouterNat#source_nat_drain_ips}
        '''
        result = self._values.get("source_nat_drain_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source_nat_drain_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of URLs of subnetworks representing source ranges to be drained.

        This is only supported on patch/update, and these subnetworks must have previously been used as active ranges in this NAT Rule.
        This field is used for private NAT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#source_nat_drain_ranges GoogleComputeRouterNat#source_nat_drain_ranges}
        '''
        result = self._values.get("source_nat_drain_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRouterNatRulesAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRouterNatRulesActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterNat.GoogleComputeRouterNatRulesActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cf1e4388d8877993624a72f9e2de28c1f1f950509c8372d781ef1835a6aaa6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11d00bf97783d9840e9cc4597f3ad6cb57470847d61eaff5354723a72c97ed91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceNatActiveIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceNatActiveRanges")
    def source_nat_active_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceNatActiveRanges"))

    @source_nat_active_ranges.setter
    def source_nat_active_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22934c2f52e1cc6d3b70911d94ca53758374e5244b53133ce35b36a2e15217e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceNatActiveRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceNatDrainIps")
    def source_nat_drain_ips(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceNatDrainIps"))

    @source_nat_drain_ips.setter
    def source_nat_drain_ips(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4076e5d2ba2d1bbab84a17d7ffb52867a95e122c21d9ff3ae5b1463563e668c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceNatDrainIps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceNatDrainRanges")
    def source_nat_drain_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceNatDrainRanges"))

    @source_nat_drain_ranges.setter
    def source_nat_drain_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c44b4984bd7f2a60c9e2a52e842a1263bc86066426a1709d8727ceb07b490c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceNatDrainRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleComputeRouterNatRulesAction]:
        return typing.cast(typing.Optional[GoogleComputeRouterNatRulesAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRouterNatRulesAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6346ba9ca294d1543da460cd1894ab19373e834799131ae3511e9deb239a55f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRouterNatRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterNat.GoogleComputeRouterNatRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f69fb4b3d6574127a7b8e10eceed5600f7aad0b46a10db120ad99069911d32d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GoogleComputeRouterNatRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ffe5d4ed49c967e93831a449e279ae8d8adca4261092be897b7f04659539456)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeRouterNatRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8197a706187ca324ccd6ddfe5d1f640975dd8cac3ba3a20d571ad3ba1675230)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3343de108e5bb60ac48cb8f113da5a7f7abc21251e2d04cfa5a317938a62c39c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ed776382b4b0e40faeeb8b3aeab14aa40b2af9ad8e03ccdddeb3830b6bb1819)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRouterNatRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRouterNatRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRouterNatRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7b42b717df61f8eb0ae554a123eb786311565e118bb1055add1e0eb2d94882b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRouterNatRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterNat.GoogleComputeRouterNatRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e82f3a28d569ecbf03121d865ddf8511e74c02f8a62c372c52a39fa01b737d6c)
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
        :param source_nat_active_ips: A list of URLs of the IP resources used for this NAT rule. These IP addresses must be valid static external IP addresses assigned to the project. This field is used for public NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#source_nat_active_ips GoogleComputeRouterNat#source_nat_active_ips}
        :param source_nat_active_ranges: A list of URLs of the subnetworks used as source ranges for this NAT Rule. These subnetworks must have purpose set to PRIVATE_NAT. This field is used for private NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#source_nat_active_ranges GoogleComputeRouterNat#source_nat_active_ranges}
        :param source_nat_drain_ips: A list of URLs of the IP resources to be drained. These IPs must be valid static external IPs that have been assigned to the NAT. These IPs should be used for updating/patching a NAT rule only. This field is used for public NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#source_nat_drain_ips GoogleComputeRouterNat#source_nat_drain_ips}
        :param source_nat_drain_ranges: A list of URLs of subnetworks representing source ranges to be drained. This is only supported on patch/update, and these subnetworks must have previously been used as active ranges in this NAT Rule. This field is used for private NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#source_nat_drain_ranges GoogleComputeRouterNat#source_nat_drain_ranges}
        '''
        value = GoogleComputeRouterNatRulesAction(
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
    def action(self) -> GoogleComputeRouterNatRulesActionOutputReference:
        return typing.cast(GoogleComputeRouterNatRulesActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[GoogleComputeRouterNatRulesAction]:
        return typing.cast(typing.Optional[GoogleComputeRouterNatRulesAction], jsii.get(self, "actionInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e76fec3af9c41a079745ffcfda7a4bb4b13bcf4086891d69ea6f576de83c01c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "match"))

    @match.setter
    def match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5ea45768a07863ab294a246dc88880bea3ee15f0e1154b126a03ed78b1ec03e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "match", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleNumber")
    def rule_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ruleNumber"))

    @rule_number.setter
    def rule_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43cfa7bed4920856b43edd0b00b1c1a9b32a2ffb650ec322f6257bd81283227a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterNatRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterNatRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterNatRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73bea08f515509971689c2aeb968f15ff91ed4c17532d4d6f78089bc51d3a6fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterNat.GoogleComputeRouterNatSubnetwork",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "source_ip_ranges_to_nat": "sourceIpRangesToNat",
        "secondary_ip_range_names": "secondaryIpRangeNames",
    },
)
class GoogleComputeRouterNatSubnetwork:
    def __init__(
        self,
        *,
        name: builtins.str,
        source_ip_ranges_to_nat: typing.Sequence[builtins.str],
        secondary_ip_range_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: Self-link of subnetwork to NAT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#name GoogleComputeRouterNat#name}
        :param source_ip_ranges_to_nat: List of options for which source IPs in the subnetwork should have NAT enabled. Supported values include: 'ALL_IP_RANGES', 'LIST_OF_SECONDARY_IP_RANGES', 'PRIMARY_IP_RANGE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#source_ip_ranges_to_nat GoogleComputeRouterNat#source_ip_ranges_to_nat}
        :param secondary_ip_range_names: List of the secondary ranges of the subnetwork that are allowed to use NAT. This can be populated only if 'LIST_OF_SECONDARY_IP_RANGES' is one of the values in sourceIpRangesToNat Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#secondary_ip_range_names GoogleComputeRouterNat#secondary_ip_range_names}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a067285fc3b824d5a2daa4af286be17bb0b7a82c2426bc7c1353b016e13436d8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#name GoogleComputeRouterNat#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_ip_ranges_to_nat(self) -> typing.List[builtins.str]:
        '''List of options for which source IPs in the subnetwork should have NAT enabled. Supported values include: 'ALL_IP_RANGES', 'LIST_OF_SECONDARY_IP_RANGES', 'PRIMARY_IP_RANGE'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#source_ip_ranges_to_nat GoogleComputeRouterNat#source_ip_ranges_to_nat}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#secondary_ip_range_names GoogleComputeRouterNat#secondary_ip_range_names}
        '''
        result = self._values.get("secondary_ip_range_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRouterNatSubnetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRouterNatSubnetworkList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterNat.GoogleComputeRouterNatSubnetworkList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdae915eaadca404d74a25a24beedfaac257ccd5467ccf922a79c9c6a8801c57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeRouterNatSubnetworkOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d98a9bec5484cbfccb39b1ba2c61627325e6b7038ac433d9a48b7f34efe02160)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeRouterNatSubnetworkOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4265bdb3699645c5076925a9b49aeb669f7496063157fcd26d6e0ea04af6be5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c622d4445cc0156b691b7c7be14200b10a72e9b0b6bc13bd75dc9315718406f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed992de7f8b0b47e9ba35767015c776768c863e062d77e1cd75893618f4ebd4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRouterNatSubnetwork]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRouterNatSubnetwork]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRouterNatSubnetwork]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10eb11cf32b0b680dddb792563750d17a31ffadbad053ca8f0070658e7e7268d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeRouterNatSubnetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterNat.GoogleComputeRouterNatSubnetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1be8ee9ac9af0489b94d453e732c86695f1f309d2f658045c071b6826b46369)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24fe3af641604b77cb46dafaf8622ab426cd73e694e3a45e804b276b33182c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secondaryIpRangeNames")
    def secondary_ip_range_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "secondaryIpRangeNames"))

    @secondary_ip_range_names.setter
    def secondary_ip_range_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc8a4789b44898d131248dcae0fda580882ad8d0f1ca99e7f878ba296d5f2be9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryIpRangeNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceIpRangesToNat")
    def source_ip_ranges_to_nat(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceIpRangesToNat"))

    @source_ip_ranges_to_nat.setter
    def source_ip_ranges_to_nat(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21c81b96a6a634392318df7310d3fe130b5c553adbb51fa8d8207bfa2a96f23c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceIpRangesToNat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterNatSubnetwork]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterNatSubnetwork]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterNatSubnetwork]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17d1f909e9b891c27bf8f8d1340b1d696baa9f826b976cd0c02273070516a9ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterNat.GoogleComputeRouterNatTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleComputeRouterNatTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#create GoogleComputeRouterNat#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#delete GoogleComputeRouterNat#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#update GoogleComputeRouterNat#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fa9147ae68f5e2463d7db4d69958484bffd8b4b92bf57d72a479dd261acb9c9)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#create GoogleComputeRouterNat#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#delete GoogleComputeRouterNat#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_router_nat#update GoogleComputeRouterNat#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRouterNatTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRouterNatTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterNat.GoogleComputeRouterNatTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf1a18e3424d4e52e1671787353175a79360fa0ee2829dc322b078918c8b36a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c79855e4f4270d1ade71097c26ee347e892e5e2d6b6a02dbacfca606ef40b110)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3f527d8ecb934a32b1459cd095a45291d2ce33506735c5cd3d6cd029daeb4e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f52eec4d76faa886c5da47a398278203970c74f4451d9fededd86271f646620b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterNatTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterNatTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterNatTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__165efc929b09ce8336783e108f6e49791b5bca010dbadcad6ff87cd70b0c0608)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleComputeRouterNat",
    "GoogleComputeRouterNatConfig",
    "GoogleComputeRouterNatLogConfig",
    "GoogleComputeRouterNatLogConfigOutputReference",
    "GoogleComputeRouterNatNat64Subnetwork",
    "GoogleComputeRouterNatNat64SubnetworkList",
    "GoogleComputeRouterNatNat64SubnetworkOutputReference",
    "GoogleComputeRouterNatRules",
    "GoogleComputeRouterNatRulesAction",
    "GoogleComputeRouterNatRulesActionOutputReference",
    "GoogleComputeRouterNatRulesList",
    "GoogleComputeRouterNatRulesOutputReference",
    "GoogleComputeRouterNatSubnetwork",
    "GoogleComputeRouterNatSubnetworkList",
    "GoogleComputeRouterNatSubnetworkOutputReference",
    "GoogleComputeRouterNatTimeouts",
    "GoogleComputeRouterNatTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__e89b9fe6ed7d9979dbdab3f63c94e00ac1bac28a570d54057f2abe0bf1427ac9(
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
    log_config: typing.Optional[typing.Union[GoogleComputeRouterNatLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    max_ports_per_vm: typing.Optional[jsii.Number] = None,
    min_ports_per_vm: typing.Optional[jsii.Number] = None,
    nat64_subnetwork: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRouterNatNat64Subnetwork, typing.Dict[builtins.str, typing.Any]]]]] = None,
    nat_ip_allocate_option: typing.Optional[builtins.str] = None,
    nat_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRouterNatRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    source_subnetwork_ip_ranges_to_nat64: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRouterNatSubnetwork, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tcp_established_idle_timeout_sec: typing.Optional[jsii.Number] = None,
    tcp_time_wait_timeout_sec: typing.Optional[jsii.Number] = None,
    tcp_transitory_idle_timeout_sec: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeRouterNatTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__12697b391f2ac71424f9f6cfc62722e95b087fbe13c84a5152bc7fe91d909b0d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1612dbd889ee7c3ed8d7de67d4cc89a2a313a2aead0ca22d797d153c67370d1a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRouterNatNat64Subnetwork, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81582edc60e5d799962b3f7a5101c1d3aaebd6bf8fa122a4fa815faace4b7a72(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRouterNatRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88d4770269e76ca5ccc755322b004c2312af6d4a00b13da0659de545108a155d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRouterNatSubnetwork, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7358875aa3a04f7710c467bcb04f295c20624b5c9f5dfb0a6e747e83d5a718c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4db3145c733e4c5d1db92fd4f31d24c62566c30c7fa121082bb9ff75e748b94(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f606451ba1fa5c90820d0e75c86eda7361065c21ad8d7dda6b5012953999d749(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f6a5bcdb19ce26c90a8e73dabd8d2775615fbf681fc546527884efc81abbc16(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d860c742b512f6eec907130c2e5da3a1217d52f3497e63f2f438a9f702868bf8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c211d19b456418b127536032a69a69bc6e90133943b3f6934a7315d4e0bc1a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1902eb16606f4540070efba19028f207b88282563644f3e5134302b6637912fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783c2dd2e9fa64923e095f4e17b10c9653ca1300f450885bc8b7974d6bf699c2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bc875c7364e6df051ddf812b4c38c544c8f32cff9b1be392afc7e275c6eee79(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d672b9a611ece0d6eeb7fd77ccd4c285f67eb14fc9128930d488d5abdb6b80(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e1cb7ff1597e5b8053255a0a4403277baa95dcaaac8546a66b83c12c5ac055d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce9b2335637825c0d87ca29327fb1174506d3bd799a1419dfe6649bff37e36a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb4ec04d0cc2d251571015698d26df8fea80092f4a5b2ca66d4996963abdd4f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf9798687877694c2357c76adb4342e004b050e9f20b09f9b5f9d754284a4538(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1549bdb3c304bd260d810bf6f2c4ab83353889906135101ac2ebfce1dd0992e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be29a9be53ae5e3081a4bcd524694e2aebfd2d5d375ec7b44cb0493c5ddef2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__577ff110c2de3261e2b986d55ab3f79abeb2fb0c04698d2cd96148a0752b6aff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7db610488d6edae04c727623179b86e616f1d85eba67c48d848e4f46bea121dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b826637bbf5d293481337ea75777cac253f7c11baa2dfed8d3a6baa4a38668(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__321bcd63f91b4913546cdfff21bc3ad61853b29eb2d20f8a61ed87c0bcd24f3d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68d9a25e1d88296efe8a1352d367c8ff08f6f807e1f20f169e46c3278f196f66(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74df9764453471e1e3db4729583048009847e527b0a4254b12653f4d0206db93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624e7e16deb8b13a4c7bf0d19a8217525cb068c0f0aa0cab5f6e6a8a3f70e09d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e23c7ecbb1c5e52f3baf9117670313ebceb677af82ebc66f26e9e8430b8c8cb(
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
    log_config: typing.Optional[typing.Union[GoogleComputeRouterNatLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    max_ports_per_vm: typing.Optional[jsii.Number] = None,
    min_ports_per_vm: typing.Optional[jsii.Number] = None,
    nat64_subnetwork: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRouterNatNat64Subnetwork, typing.Dict[builtins.str, typing.Any]]]]] = None,
    nat_ip_allocate_option: typing.Optional[builtins.str] = None,
    nat_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRouterNatRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    source_subnetwork_ip_ranges_to_nat64: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRouterNatSubnetwork, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tcp_established_idle_timeout_sec: typing.Optional[jsii.Number] = None,
    tcp_time_wait_timeout_sec: typing.Optional[jsii.Number] = None,
    tcp_transitory_idle_timeout_sec: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeRouterNatTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
    udp_idle_timeout_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7851e19286f9848a6154dd01e64c9ead24aa5ba728fe28af26d0c2dbdcb20eeb(
    *,
    enable: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    filter: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c23a6d667a0857f2567ca28d1f9f9034c115faabc04457a9d90d99da187577(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bb8335565230905046f8005c3a4c7cecbcc8717a79078f6552781b18fe03709(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9301ab671cffc194507e35c490d7c616004212a9c0b7b4347ad8cfa3029ad645(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb98a325815a7924a47ffe21145ea2f9bad8e91a96db0c013c785a4e57b9c442(
    value: typing.Optional[GoogleComputeRouterNatLogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e92da51bce397a31a9b268aa25324dad92e57c329e7a7d985b3552a4975b4b9f(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15f7a7a546a5192906257db0b0f8504133519f44e1e42c3455b769d79b43f349(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71ba18d2ff799eb0ca71e981d75c63da1b12231846b0ba80e961b245d55f4c40(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b767d81a702a4ecbf98e4e5098e99e1cf52fda226527bce72e881437771c338c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93229a303c56148bcaae63e0569492ac289b8d90c42bc432ce162a541cd06aaa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c3347823d3a914359aabf6633ab9942b3385738a1c2c7e28eab894e7759862a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__193b4e1530225f6b47a9335bd4d1aa97f30edf353b0c4cd8eb0f76a58bd52d22(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRouterNatNat64Subnetwork]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2a6114363209734af574b3dee9b9556d3a18a4d021f1323ea5ad6746ddfeaf0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb03c48312e09c65b608bb729bda9e3aff5cae9f6552fa9ce9664ae3afc0b51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2628f58369f82268f0e0c144f22d067f7d064029a5fb45dd3b6c0b360f7f7344(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterNatNat64Subnetwork]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7069d07f3da1def43b683db25df9bb12513a393a34c7173afb2485b9e0976186(
    *,
    match: builtins.str,
    rule_number: jsii.Number,
    action: typing.Optional[typing.Union[GoogleComputeRouterNatRulesAction, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b87590f4956db95bbddf8927cc9c37de4c957938ec0efd62f8283ecc9e0e7e(
    *,
    source_nat_active_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_nat_active_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_nat_drain_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_nat_drain_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cf1e4388d8877993624a72f9e2de28c1f1f950509c8372d781ef1835a6aaa6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d00bf97783d9840e9cc4597f3ad6cb57470847d61eaff5354723a72c97ed91(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22934c2f52e1cc6d3b70911d94ca53758374e5244b53133ce35b36a2e15217e6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4076e5d2ba2d1bbab84a17d7ffb52867a95e122c21d9ff3ae5b1463563e668c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c44b4984bd7f2a60c9e2a52e842a1263bc86066426a1709d8727ceb07b490c8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6346ba9ca294d1543da460cd1894ab19373e834799131ae3511e9deb239a55f(
    value: typing.Optional[GoogleComputeRouterNatRulesAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f69fb4b3d6574127a7b8e10eceed5600f7aad0b46a10db120ad99069911d32d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ffe5d4ed49c967e93831a449e279ae8d8adca4261092be897b7f04659539456(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8197a706187ca324ccd6ddfe5d1f640975dd8cac3ba3a20d571ad3ba1675230(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3343de108e5bb60ac48cb8f113da5a7f7abc21251e2d04cfa5a317938a62c39c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ed776382b4b0e40faeeb8b3aeab14aa40b2af9ad8e03ccdddeb3830b6bb1819(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b42b717df61f8eb0ae554a123eb786311565e118bb1055add1e0eb2d94882b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRouterNatRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e82f3a28d569ecbf03121d865ddf8511e74c02f8a62c372c52a39fa01b737d6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e76fec3af9c41a079745ffcfda7a4bb4b13bcf4086891d69ea6f576de83c01c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5ea45768a07863ab294a246dc88880bea3ee15f0e1154b126a03ed78b1ec03e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43cfa7bed4920856b43edd0b00b1c1a9b32a2ffb650ec322f6257bd81283227a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73bea08f515509971689c2aeb968f15ff91ed4c17532d4d6f78089bc51d3a6fc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterNatRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a067285fc3b824d5a2daa4af286be17bb0b7a82c2426bc7c1353b016e13436d8(
    *,
    name: builtins.str,
    source_ip_ranges_to_nat: typing.Sequence[builtins.str],
    secondary_ip_range_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdae915eaadca404d74a25a24beedfaac257ccd5467ccf922a79c9c6a8801c57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d98a9bec5484cbfccb39b1ba2c61627325e6b7038ac433d9a48b7f34efe02160(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4265bdb3699645c5076925a9b49aeb669f7496063157fcd26d6e0ea04af6be5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c622d4445cc0156b691b7c7be14200b10a72e9b0b6bc13bd75dc9315718406f4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed992de7f8b0b47e9ba35767015c776768c863e062d77e1cd75893618f4ebd4c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10eb11cf32b0b680dddb792563750d17a31ffadbad053ca8f0070658e7e7268d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRouterNatSubnetwork]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1be8ee9ac9af0489b94d453e732c86695f1f309d2f658045c071b6826b46369(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24fe3af641604b77cb46dafaf8622ab426cd73e694e3a45e804b276b33182c32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc8a4789b44898d131248dcae0fda580882ad8d0f1ca99e7f878ba296d5f2be9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21c81b96a6a634392318df7310d3fe130b5c553adbb51fa8d8207bfa2a96f23c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17d1f909e9b891c27bf8f8d1340b1d696baa9f826b976cd0c02273070516a9ca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterNatSubnetwork]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa9147ae68f5e2463d7db4d69958484bffd8b4b92bf57d72a479dd261acb9c9(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf1a18e3424d4e52e1671787353175a79360fa0ee2829dc322b078918c8b36a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79855e4f4270d1ade71097c26ee347e892e5e2d6b6a02dbacfca606ef40b110(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f527d8ecb934a32b1459cd095a45291d2ce33506735c5cd3d6cd029daeb4e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52eec4d76faa886c5da47a398278203970c74f4451d9fededd86271f646620b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__165efc929b09ce8336783e108f6e49791b5bca010dbadcad6ff87cd70b0c0608(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterNatTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
