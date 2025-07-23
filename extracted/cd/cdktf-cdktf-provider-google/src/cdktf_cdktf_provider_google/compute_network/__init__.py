r'''
# `google_compute_network`

Refer to the Terraform Registry for docs: [`google_compute_network`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network).
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


class ComputeNetwork(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNetwork.ComputeNetwork",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network google_compute_network}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        auto_create_subnetworks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bgp_always_compare_med: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bgp_best_path_selection_mode: typing.Optional[builtins.str] = None,
        bgp_inter_region_cost: typing.Optional[builtins.str] = None,
        delete_default_routes_on_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_ula_internal_ipv6: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        internal_ipv6_range: typing.Optional[builtins.str] = None,
        mtu: typing.Optional[jsii.Number] = None,
        network_firewall_policy_enforcement_order: typing.Optional[builtins.str] = None,
        network_profile: typing.Optional[builtins.str] = None,
        params: typing.Optional[typing.Union["ComputeNetworkParams", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        routing_mode: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeNetworkTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network google_compute_network} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#name ComputeNetwork#name}
        :param auto_create_subnetworks: When set to 'true', the network is created in "auto subnet mode" and it will create a subnet for each region automatically across the '10.128.0.0/9' address range. When set to 'false', the network is created in "custom subnet mode" so the user can explicitly connect subnetwork resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#auto_create_subnetworks ComputeNetwork#auto_create_subnetworks}
        :param bgp_always_compare_med: Enables/disables the comparison of MED across routes with different Neighbor ASNs. This value can only be set if the --bgp-best-path-selection-mode is STANDARD Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#bgp_always_compare_med ComputeNetwork#bgp_always_compare_med}
        :param bgp_best_path_selection_mode: The BGP best selection algorithm to be employed. MODE can be LEGACY or STANDARD. Possible values: ["LEGACY", "STANDARD"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#bgp_best_path_selection_mode ComputeNetwork#bgp_best_path_selection_mode}
        :param bgp_inter_region_cost: Choice of the behavior of inter-regional cost and MED in the BPS algorithm. Possible values: ["DEFAULT", "ADD_COST_TO_MED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#bgp_inter_region_cost ComputeNetwork#bgp_inter_region_cost}
        :param delete_default_routes_on_create: If set to 'true', default routes ('0.0.0.0/0') will be deleted immediately after network creation. Defaults to 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#delete_default_routes_on_create ComputeNetwork#delete_default_routes_on_create}
        :param description: An optional description of this resource. The resource must be recreated to modify this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#description ComputeNetwork#description}
        :param enable_ula_internal_ipv6: Enable ULA internal ipv6 on this network. Enabling this feature will assign a /48 from google defined ULA prefix fd20::/20. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#enable_ula_internal_ipv6 ComputeNetwork#enable_ula_internal_ipv6}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#id ComputeNetwork#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param internal_ipv6_range: When enabling ula internal ipv6, caller optionally can specify the /48 range they want from the google defined ULA prefix fd20::/20. The input must be a valid /48 ULA IPv6 address and must be within the fd20::/20. Operation will fail if the speficied /48 is already in used by another resource. If the field is not speficied, then a /48 range will be randomly allocated from fd20::/20 and returned via this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#internal_ipv6_range ComputeNetwork#internal_ipv6_range}
        :param mtu: Maximum Transmission Unit in bytes. The default value is 1460 bytes. The minimum value for this field is 1300 and the maximum value is 8896 bytes (jumbo frames). Note that packets larger than 1500 bytes (standard Ethernet) can be subject to TCP-MSS clamping or dropped with an ICMP 'Fragmentation-Needed' message if the packets are routed to the Internet or other VPCs with varying MTUs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#mtu ComputeNetwork#mtu}
        :param network_firewall_policy_enforcement_order: Set the order that Firewall Rules and Firewall Policies are evaluated. Default value: "AFTER_CLASSIC_FIREWALL" Possible values: ["BEFORE_CLASSIC_FIREWALL", "AFTER_CLASSIC_FIREWALL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#network_firewall_policy_enforcement_order ComputeNetwork#network_firewall_policy_enforcement_order}
        :param network_profile: A full or partial URL of the network profile to apply to this network. This field can be set only at resource creation time. For example, the following are valid URLs: - https://www.googleapis.com/compute/v1/projects/{projectId}/global/networkProfiles/{network_profile_name} - projects/{projectId}/global/networkProfiles/{network_profile_name} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#network_profile ComputeNetwork#network_profile}
        :param params: params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#params ComputeNetwork#params}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#project ComputeNetwork#project}.
        :param routing_mode: The network-wide routing mode to use. If set to 'REGIONAL', this network's cloud routers will only advertise routes with subnetworks of this network in the same region as the router. If set to 'GLOBAL', this network's cloud routers will advertise routes with all subnetworks of this network, across regions. Possible values: ["REGIONAL", "GLOBAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#routing_mode ComputeNetwork#routing_mode}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#timeouts ComputeNetwork#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__740237e7efcc1703fc5dd2c3e87a1670166215fd1c76df5125c094157d114d5c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeNetworkConfig(
            name=name,
            auto_create_subnetworks=auto_create_subnetworks,
            bgp_always_compare_med=bgp_always_compare_med,
            bgp_best_path_selection_mode=bgp_best_path_selection_mode,
            bgp_inter_region_cost=bgp_inter_region_cost,
            delete_default_routes_on_create=delete_default_routes_on_create,
            description=description,
            enable_ula_internal_ipv6=enable_ula_internal_ipv6,
            id=id,
            internal_ipv6_range=internal_ipv6_range,
            mtu=mtu,
            network_firewall_policy_enforcement_order=network_firewall_policy_enforcement_order,
            network_profile=network_profile,
            params=params,
            project=project,
            routing_mode=routing_mode,
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
        '''Generates CDKTF code for importing a ComputeNetwork resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeNetwork to import.
        :param import_from_id: The id of the existing ComputeNetwork that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeNetwork to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d6647a45faab4f0e7fedfcc7f008855c0fdc42300056000433eba9a45bada3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putParams")
    def put_params(
        self,
        *,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param resource_manager_tags: Resource manager tags to be bound to the network. Tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#resource_manager_tags ComputeNetwork#resource_manager_tags}
        '''
        value = ComputeNetworkParams(resource_manager_tags=resource_manager_tags)

        return typing.cast(None, jsii.invoke(self, "putParams", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#create ComputeNetwork#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#delete ComputeNetwork#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#update ComputeNetwork#update}.
        '''
        value = ComputeNetworkTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAutoCreateSubnetworks")
    def reset_auto_create_subnetworks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoCreateSubnetworks", []))

    @jsii.member(jsii_name="resetBgpAlwaysCompareMed")
    def reset_bgp_always_compare_med(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBgpAlwaysCompareMed", []))

    @jsii.member(jsii_name="resetBgpBestPathSelectionMode")
    def reset_bgp_best_path_selection_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBgpBestPathSelectionMode", []))

    @jsii.member(jsii_name="resetBgpInterRegionCost")
    def reset_bgp_inter_region_cost(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBgpInterRegionCost", []))

    @jsii.member(jsii_name="resetDeleteDefaultRoutesOnCreate")
    def reset_delete_default_routes_on_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteDefaultRoutesOnCreate", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnableUlaInternalIpv6")
    def reset_enable_ula_internal_ipv6(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableUlaInternalIpv6", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInternalIpv6Range")
    def reset_internal_ipv6_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternalIpv6Range", []))

    @jsii.member(jsii_name="resetMtu")
    def reset_mtu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMtu", []))

    @jsii.member(jsii_name="resetNetworkFirewallPolicyEnforcementOrder")
    def reset_network_firewall_policy_enforcement_order(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkFirewallPolicyEnforcementOrder", []))

    @jsii.member(jsii_name="resetNetworkProfile")
    def reset_network_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkProfile", []))

    @jsii.member(jsii_name="resetParams")
    def reset_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParams", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRoutingMode")
    def reset_routing_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingMode", []))

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
    @jsii.member(jsii_name="gatewayIpv4")
    def gateway_ipv4(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayIpv4"))

    @builtins.property
    @jsii.member(jsii_name="networkId")
    def network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkId"))

    @builtins.property
    @jsii.member(jsii_name="numericId")
    def numeric_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "numericId"))

    @builtins.property
    @jsii.member(jsii_name="params")
    def params(self) -> "ComputeNetworkParamsOutputReference":
        return typing.cast("ComputeNetworkParamsOutputReference", jsii.get(self, "params"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeNetworkTimeoutsOutputReference":
        return typing.cast("ComputeNetworkTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="autoCreateSubnetworksInput")
    def auto_create_subnetworks_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoCreateSubnetworksInput"))

    @builtins.property
    @jsii.member(jsii_name="bgpAlwaysCompareMedInput")
    def bgp_always_compare_med_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bgpAlwaysCompareMedInput"))

    @builtins.property
    @jsii.member(jsii_name="bgpBestPathSelectionModeInput")
    def bgp_best_path_selection_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bgpBestPathSelectionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="bgpInterRegionCostInput")
    def bgp_inter_region_cost_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bgpInterRegionCostInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteDefaultRoutesOnCreateInput")
    def delete_default_routes_on_create_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteDefaultRoutesOnCreateInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableUlaInternalIpv6Input")
    def enable_ula_internal_ipv6_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableUlaInternalIpv6Input"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="internalIpv6RangeInput")
    def internal_ipv6_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "internalIpv6RangeInput"))

    @builtins.property
    @jsii.member(jsii_name="mtuInput")
    def mtu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "mtuInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkFirewallPolicyEnforcementOrderInput")
    def network_firewall_policy_enforcement_order_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkFirewallPolicyEnforcementOrderInput"))

    @builtins.property
    @jsii.member(jsii_name="networkProfileInput")
    def network_profile_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="paramsInput")
    def params_input(self) -> typing.Optional["ComputeNetworkParams"]:
        return typing.cast(typing.Optional["ComputeNetworkParams"], jsii.get(self, "paramsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="routingModeInput")
    def routing_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeNetworkTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeNetworkTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoCreateSubnetworks")
    def auto_create_subnetworks(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoCreateSubnetworks"))

    @auto_create_subnetworks.setter
    def auto_create_subnetworks(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e58b575152605c278478888b7cd8a3289b6e4fdec819d1a0867b5bd686cbc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoCreateSubnetworks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bgpAlwaysCompareMed")
    def bgp_always_compare_med(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bgpAlwaysCompareMed"))

    @bgp_always_compare_med.setter
    def bgp_always_compare_med(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eacea4aef7af096c2729405b2e70eb1da16b47c945943ef7a83ad27b5f0b29c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bgpAlwaysCompareMed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bgpBestPathSelectionMode")
    def bgp_best_path_selection_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bgpBestPathSelectionMode"))

    @bgp_best_path_selection_mode.setter
    def bgp_best_path_selection_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f948782f8cc38ed009b023dd6ff50d70580bdec11ea6c922faf76ed0e6ed0b8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bgpBestPathSelectionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bgpInterRegionCost")
    def bgp_inter_region_cost(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bgpInterRegionCost"))

    @bgp_inter_region_cost.setter
    def bgp_inter_region_cost(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aef998dd6a471ce39ee23a91e4934d9a47538bdc7479f817699e1499dbee0e71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bgpInterRegionCost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteDefaultRoutesOnCreate")
    def delete_default_routes_on_create(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteDefaultRoutesOnCreate"))

    @delete_default_routes_on_create.setter
    def delete_default_routes_on_create(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43adfcf2a30cf2123cad16a7f3564a9fce4fbbeed63502a0ef9f572c2e6ebf99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteDefaultRoutesOnCreate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d88eacc8fbe5a680ca055ab2f688e54f0e0a5dec43958bb3699fd74ac3cd0986)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableUlaInternalIpv6")
    def enable_ula_internal_ipv6(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableUlaInternalIpv6"))

    @enable_ula_internal_ipv6.setter
    def enable_ula_internal_ipv6(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ffe5cabcc405b1c5957178fa4b7fa79b31fa4723c996de40810cf3bf814abe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableUlaInternalIpv6", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67cd79aa62a218d6ce384e8b8b8462aba31fea2998566bd1439a34bb30179b6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalIpv6Range")
    def internal_ipv6_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "internalIpv6Range"))

    @internal_ipv6_range.setter
    def internal_ipv6_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ccab6ceb7fb86e69f74fc54bd10f58856a6bc107a3e3737fb307cd57d841e5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalIpv6Range", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mtu")
    def mtu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mtu"))

    @mtu.setter
    def mtu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a63ee52c70cb769b7bd1a09dcc0636c2015de3ac400439edd9eed0ac87d4aab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mtu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5491eb5f392744ef50845b1011cf6b6220e6243fc5eeecaf8a38b868b924f5bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkFirewallPolicyEnforcementOrder")
    def network_firewall_policy_enforcement_order(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkFirewallPolicyEnforcementOrder"))

    @network_firewall_policy_enforcement_order.setter
    def network_firewall_policy_enforcement_order(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab7d02f0fc462019a4576f8a5a82b64ab8b9a7bb913443c05f1696cec6647f34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkFirewallPolicyEnforcementOrder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkProfile")
    def network_profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkProfile"))

    @network_profile.setter
    def network_profile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae8acfa0315d971e7724dbe3a05e132043142e5a1cb34f50f42f2945839dcf3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkProfile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56537e5d7a3cbf2a1e4f0bacc3fe087a9c1fdef3ef863b4954c9c061c306ec76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingMode")
    def routing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingMode"))

    @routing_mode.setter
    def routing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0b106d6cd3d8ef26ff7e17815c609f650e04c7bda797bc19a4297a2ba8bdfa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingMode", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNetwork.ComputeNetworkConfig",
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
        "auto_create_subnetworks": "autoCreateSubnetworks",
        "bgp_always_compare_med": "bgpAlwaysCompareMed",
        "bgp_best_path_selection_mode": "bgpBestPathSelectionMode",
        "bgp_inter_region_cost": "bgpInterRegionCost",
        "delete_default_routes_on_create": "deleteDefaultRoutesOnCreate",
        "description": "description",
        "enable_ula_internal_ipv6": "enableUlaInternalIpv6",
        "id": "id",
        "internal_ipv6_range": "internalIpv6Range",
        "mtu": "mtu",
        "network_firewall_policy_enforcement_order": "networkFirewallPolicyEnforcementOrder",
        "network_profile": "networkProfile",
        "params": "params",
        "project": "project",
        "routing_mode": "routingMode",
        "timeouts": "timeouts",
    },
)
class ComputeNetworkConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        auto_create_subnetworks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bgp_always_compare_med: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bgp_best_path_selection_mode: typing.Optional[builtins.str] = None,
        bgp_inter_region_cost: typing.Optional[builtins.str] = None,
        delete_default_routes_on_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_ula_internal_ipv6: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        internal_ipv6_range: typing.Optional[builtins.str] = None,
        mtu: typing.Optional[jsii.Number] = None,
        network_firewall_policy_enforcement_order: typing.Optional[builtins.str] = None,
        network_profile: typing.Optional[builtins.str] = None,
        params: typing.Optional[typing.Union["ComputeNetworkParams", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        routing_mode: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeNetworkTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#name ComputeNetwork#name}
        :param auto_create_subnetworks: When set to 'true', the network is created in "auto subnet mode" and it will create a subnet for each region automatically across the '10.128.0.0/9' address range. When set to 'false', the network is created in "custom subnet mode" so the user can explicitly connect subnetwork resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#auto_create_subnetworks ComputeNetwork#auto_create_subnetworks}
        :param bgp_always_compare_med: Enables/disables the comparison of MED across routes with different Neighbor ASNs. This value can only be set if the --bgp-best-path-selection-mode is STANDARD Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#bgp_always_compare_med ComputeNetwork#bgp_always_compare_med}
        :param bgp_best_path_selection_mode: The BGP best selection algorithm to be employed. MODE can be LEGACY or STANDARD. Possible values: ["LEGACY", "STANDARD"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#bgp_best_path_selection_mode ComputeNetwork#bgp_best_path_selection_mode}
        :param bgp_inter_region_cost: Choice of the behavior of inter-regional cost and MED in the BPS algorithm. Possible values: ["DEFAULT", "ADD_COST_TO_MED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#bgp_inter_region_cost ComputeNetwork#bgp_inter_region_cost}
        :param delete_default_routes_on_create: If set to 'true', default routes ('0.0.0.0/0') will be deleted immediately after network creation. Defaults to 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#delete_default_routes_on_create ComputeNetwork#delete_default_routes_on_create}
        :param description: An optional description of this resource. The resource must be recreated to modify this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#description ComputeNetwork#description}
        :param enable_ula_internal_ipv6: Enable ULA internal ipv6 on this network. Enabling this feature will assign a /48 from google defined ULA prefix fd20::/20. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#enable_ula_internal_ipv6 ComputeNetwork#enable_ula_internal_ipv6}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#id ComputeNetwork#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param internal_ipv6_range: When enabling ula internal ipv6, caller optionally can specify the /48 range they want from the google defined ULA prefix fd20::/20. The input must be a valid /48 ULA IPv6 address and must be within the fd20::/20. Operation will fail if the speficied /48 is already in used by another resource. If the field is not speficied, then a /48 range will be randomly allocated from fd20::/20 and returned via this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#internal_ipv6_range ComputeNetwork#internal_ipv6_range}
        :param mtu: Maximum Transmission Unit in bytes. The default value is 1460 bytes. The minimum value for this field is 1300 and the maximum value is 8896 bytes (jumbo frames). Note that packets larger than 1500 bytes (standard Ethernet) can be subject to TCP-MSS clamping or dropped with an ICMP 'Fragmentation-Needed' message if the packets are routed to the Internet or other VPCs with varying MTUs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#mtu ComputeNetwork#mtu}
        :param network_firewall_policy_enforcement_order: Set the order that Firewall Rules and Firewall Policies are evaluated. Default value: "AFTER_CLASSIC_FIREWALL" Possible values: ["BEFORE_CLASSIC_FIREWALL", "AFTER_CLASSIC_FIREWALL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#network_firewall_policy_enforcement_order ComputeNetwork#network_firewall_policy_enforcement_order}
        :param network_profile: A full or partial URL of the network profile to apply to this network. This field can be set only at resource creation time. For example, the following are valid URLs: - https://www.googleapis.com/compute/v1/projects/{projectId}/global/networkProfiles/{network_profile_name} - projects/{projectId}/global/networkProfiles/{network_profile_name} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#network_profile ComputeNetwork#network_profile}
        :param params: params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#params ComputeNetwork#params}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#project ComputeNetwork#project}.
        :param routing_mode: The network-wide routing mode to use. If set to 'REGIONAL', this network's cloud routers will only advertise routes with subnetworks of this network in the same region as the router. If set to 'GLOBAL', this network's cloud routers will advertise routes with all subnetworks of this network, across regions. Possible values: ["REGIONAL", "GLOBAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#routing_mode ComputeNetwork#routing_mode}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#timeouts ComputeNetwork#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(params, dict):
            params = ComputeNetworkParams(**params)
        if isinstance(timeouts, dict):
            timeouts = ComputeNetworkTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0f86a4e3992b05dc0f6ec8711908acb3b6f98a7600dc7b844dae0c8f80d54fd)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument auto_create_subnetworks", value=auto_create_subnetworks, expected_type=type_hints["auto_create_subnetworks"])
            check_type(argname="argument bgp_always_compare_med", value=bgp_always_compare_med, expected_type=type_hints["bgp_always_compare_med"])
            check_type(argname="argument bgp_best_path_selection_mode", value=bgp_best_path_selection_mode, expected_type=type_hints["bgp_best_path_selection_mode"])
            check_type(argname="argument bgp_inter_region_cost", value=bgp_inter_region_cost, expected_type=type_hints["bgp_inter_region_cost"])
            check_type(argname="argument delete_default_routes_on_create", value=delete_default_routes_on_create, expected_type=type_hints["delete_default_routes_on_create"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_ula_internal_ipv6", value=enable_ula_internal_ipv6, expected_type=type_hints["enable_ula_internal_ipv6"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument internal_ipv6_range", value=internal_ipv6_range, expected_type=type_hints["internal_ipv6_range"])
            check_type(argname="argument mtu", value=mtu, expected_type=type_hints["mtu"])
            check_type(argname="argument network_firewall_policy_enforcement_order", value=network_firewall_policy_enforcement_order, expected_type=type_hints["network_firewall_policy_enforcement_order"])
            check_type(argname="argument network_profile", value=network_profile, expected_type=type_hints["network_profile"])
            check_type(argname="argument params", value=params, expected_type=type_hints["params"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument routing_mode", value=routing_mode, expected_type=type_hints["routing_mode"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
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
        if auto_create_subnetworks is not None:
            self._values["auto_create_subnetworks"] = auto_create_subnetworks
        if bgp_always_compare_med is not None:
            self._values["bgp_always_compare_med"] = bgp_always_compare_med
        if bgp_best_path_selection_mode is not None:
            self._values["bgp_best_path_selection_mode"] = bgp_best_path_selection_mode
        if bgp_inter_region_cost is not None:
            self._values["bgp_inter_region_cost"] = bgp_inter_region_cost
        if delete_default_routes_on_create is not None:
            self._values["delete_default_routes_on_create"] = delete_default_routes_on_create
        if description is not None:
            self._values["description"] = description
        if enable_ula_internal_ipv6 is not None:
            self._values["enable_ula_internal_ipv6"] = enable_ula_internal_ipv6
        if id is not None:
            self._values["id"] = id
        if internal_ipv6_range is not None:
            self._values["internal_ipv6_range"] = internal_ipv6_range
        if mtu is not None:
            self._values["mtu"] = mtu
        if network_firewall_policy_enforcement_order is not None:
            self._values["network_firewall_policy_enforcement_order"] = network_firewall_policy_enforcement_order
        if network_profile is not None:
            self._values["network_profile"] = network_profile
        if params is not None:
            self._values["params"] = params
        if project is not None:
            self._values["project"] = project
        if routing_mode is not None:
            self._values["routing_mode"] = routing_mode
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
        '''Name of the resource.

        Provided by the client when the resource is
        created. The name must be 1-63 characters long, and comply with
        RFC1035. Specifically, the name must be 1-63 characters long and match
        the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the
        first character must be a lowercase letter, and all following
        characters must be a dash, lowercase letter, or digit, except the last
        character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#name ComputeNetwork#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_create_subnetworks(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When set to 'true', the network is created in "auto subnet mode" and it will create a subnet for each region automatically across the '10.128.0.0/9' address range.

        When set to 'false', the network is created in "custom subnet mode" so
        the user can explicitly connect subnetwork resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#auto_create_subnetworks ComputeNetwork#auto_create_subnetworks}
        '''
        result = self._values.get("auto_create_subnetworks")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def bgp_always_compare_med(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables/disables the comparison of MED across routes with different Neighbor ASNs.

        This value can only be set if the --bgp-best-path-selection-mode is STANDARD

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#bgp_always_compare_med ComputeNetwork#bgp_always_compare_med}
        '''
        result = self._values.get("bgp_always_compare_med")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def bgp_best_path_selection_mode(self) -> typing.Optional[builtins.str]:
        '''The BGP best selection algorithm to be employed. MODE can be LEGACY or STANDARD. Possible values: ["LEGACY", "STANDARD"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#bgp_best_path_selection_mode ComputeNetwork#bgp_best_path_selection_mode}
        '''
        result = self._values.get("bgp_best_path_selection_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bgp_inter_region_cost(self) -> typing.Optional[builtins.str]:
        '''Choice of the behavior of inter-regional cost and MED in the BPS algorithm. Possible values: ["DEFAULT", "ADD_COST_TO_MED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#bgp_inter_region_cost ComputeNetwork#bgp_inter_region_cost}
        '''
        result = self._values.get("bgp_inter_region_cost")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete_default_routes_on_create(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to 'true', default routes ('0.0.0.0/0') will be deleted immediately after network creation. Defaults to 'false'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#delete_default_routes_on_create ComputeNetwork#delete_default_routes_on_create}
        '''
        result = self._values.get("delete_default_routes_on_create")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. The resource must be recreated to modify this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#description ComputeNetwork#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_ula_internal_ipv6(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable ULA internal ipv6 on this network. Enabling this feature will assign a /48 from google defined ULA prefix fd20::/20.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#enable_ula_internal_ipv6 ComputeNetwork#enable_ula_internal_ipv6}
        '''
        result = self._values.get("enable_ula_internal_ipv6")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#id ComputeNetwork#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def internal_ipv6_range(self) -> typing.Optional[builtins.str]:
        '''When enabling ula internal ipv6, caller optionally can specify the /48 range they want from the google defined ULA prefix fd20::/20.

        The input must be a
        valid /48 ULA IPv6 address and must be within the fd20::/20. Operation will
        fail if the speficied /48 is already in used by another resource.
        If the field is not speficied, then a /48 range will be randomly allocated from fd20::/20 and returned via this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#internal_ipv6_range ComputeNetwork#internal_ipv6_range}
        '''
        result = self._values.get("internal_ipv6_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mtu(self) -> typing.Optional[jsii.Number]:
        '''Maximum Transmission Unit in bytes.

        The default value is 1460 bytes.
        The minimum value for this field is 1300 and the maximum value is 8896 bytes (jumbo frames).
        Note that packets larger than 1500 bytes (standard Ethernet) can be subject to TCP-MSS clamping or dropped
        with an ICMP 'Fragmentation-Needed' message if the packets are routed to the Internet or other VPCs
        with varying MTUs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#mtu ComputeNetwork#mtu}
        '''
        result = self._values.get("mtu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def network_firewall_policy_enforcement_order(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Set the order that Firewall Rules and Firewall Policies are evaluated. Default value: "AFTER_CLASSIC_FIREWALL" Possible values: ["BEFORE_CLASSIC_FIREWALL", "AFTER_CLASSIC_FIREWALL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#network_firewall_policy_enforcement_order ComputeNetwork#network_firewall_policy_enforcement_order}
        '''
        result = self._values.get("network_firewall_policy_enforcement_order")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_profile(self) -> typing.Optional[builtins.str]:
        '''A full or partial URL of the network profile to apply to this network.

        This field can be set only at resource creation time. For example, the
        following are valid URLs:

        - https://www.googleapis.com/compute/v1/projects/{projectId}/global/networkProfiles/{network_profile_name}
        - projects/{projectId}/global/networkProfiles/{network_profile_name}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#network_profile ComputeNetwork#network_profile}
        '''
        result = self._values.get("network_profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def params(self) -> typing.Optional["ComputeNetworkParams"]:
        '''params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#params ComputeNetwork#params}
        '''
        result = self._values.get("params")
        return typing.cast(typing.Optional["ComputeNetworkParams"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#project ComputeNetwork#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_mode(self) -> typing.Optional[builtins.str]:
        '''The network-wide routing mode to use.

        If set to 'REGIONAL', this
        network's cloud routers will only advertise routes with subnetworks
        of this network in the same region as the router. If set to 'GLOBAL',
        this network's cloud routers will advertise routes with all
        subnetworks of this network, across regions. Possible values: ["REGIONAL", "GLOBAL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#routing_mode ComputeNetwork#routing_mode}
        '''
        result = self._values.get("routing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeNetworkTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#timeouts ComputeNetwork#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeNetworkTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNetwork.ComputeNetworkParams",
    jsii_struct_bases=[],
    name_mapping={"resource_manager_tags": "resourceManagerTags"},
)
class ComputeNetworkParams:
    def __init__(
        self,
        *,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param resource_manager_tags: Resource manager tags to be bound to the network. Tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#resource_manager_tags ComputeNetwork#resource_manager_tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__355135b9950af107296ff2c712e6ac978b1ad1e6962a226e8a81a9b92fc65840)
            check_type(argname="argument resource_manager_tags", value=resource_manager_tags, expected_type=type_hints["resource_manager_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_manager_tags is not None:
            self._values["resource_manager_tags"] = resource_manager_tags

    @builtins.property
    def resource_manager_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Resource manager tags to be bound to the network.

        Tag keys and values have the
        same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id},
        and values are in the format tagValues/456.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#resource_manager_tags ComputeNetwork#resource_manager_tags}
        '''
        result = self._values.get("resource_manager_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNetworkParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeNetworkParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNetwork.ComputeNetworkParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b267e9b7d490d370fabe1b6c0286b7e822f505d0d279e946c8c2ccf8a75f0f78)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5547ebef1bcd32523d45812dd32c1fdd7f0fd68f2f6d805474e3b011d3705451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceManagerTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeNetworkParams]:
        return typing.cast(typing.Optional[ComputeNetworkParams], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ComputeNetworkParams]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51c098b2b9cda8603440ba9e4a5844ff09b28f978c144349c7dd73f861dc77cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeNetwork.ComputeNetworkTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeNetworkTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#create ComputeNetwork#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#delete ComputeNetwork#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#update ComputeNetwork#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b157c9db6a18415c8bc4c5ba574318a8982dfe23fe9289fe8db736d9f4cb0350)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#create ComputeNetwork#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#delete ComputeNetwork#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_network#update ComputeNetwork#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeNetworkTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeNetworkTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeNetwork.ComputeNetworkTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84e0c2efc71af6e3116a0caa463c41838a6bbd587c3e0ff72b71284ba5d5e10c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a887ff689d0843f5f7d22fa84462368e3b67d8b413a0f44907727194f72210c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7c3d6783d67cee546b5f9727e3dc01bc9a3baf23dfaab2f55a1779ef9629bd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7598f8b95b72c0461830ff93139167764e7911cdbb4cb2fc7744ece38c0dbd55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNetworkTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNetworkTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNetworkTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b6127bf1e1340bd0d0a6a89518c4d41ab32ef563b41b119dbbedda36d10c488)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeNetwork",
    "ComputeNetworkConfig",
    "ComputeNetworkParams",
    "ComputeNetworkParamsOutputReference",
    "ComputeNetworkTimeouts",
    "ComputeNetworkTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__740237e7efcc1703fc5dd2c3e87a1670166215fd1c76df5125c094157d114d5c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    auto_create_subnetworks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bgp_always_compare_med: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bgp_best_path_selection_mode: typing.Optional[builtins.str] = None,
    bgp_inter_region_cost: typing.Optional[builtins.str] = None,
    delete_default_routes_on_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_ula_internal_ipv6: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    internal_ipv6_range: typing.Optional[builtins.str] = None,
    mtu: typing.Optional[jsii.Number] = None,
    network_firewall_policy_enforcement_order: typing.Optional[builtins.str] = None,
    network_profile: typing.Optional[builtins.str] = None,
    params: typing.Optional[typing.Union[ComputeNetworkParams, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    routing_mode: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeNetworkTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__14d6647a45faab4f0e7fedfcc7f008855c0fdc42300056000433eba9a45bada3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e58b575152605c278478888b7cd8a3289b6e4fdec819d1a0867b5bd686cbc1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eacea4aef7af096c2729405b2e70eb1da16b47c945943ef7a83ad27b5f0b29c9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f948782f8cc38ed009b023dd6ff50d70580bdec11ea6c922faf76ed0e6ed0b8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aef998dd6a471ce39ee23a91e4934d9a47538bdc7479f817699e1499dbee0e71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43adfcf2a30cf2123cad16a7f3564a9fce4fbbeed63502a0ef9f572c2e6ebf99(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88eacc8fbe5a680ca055ab2f688e54f0e0a5dec43958bb3699fd74ac3cd0986(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ffe5cabcc405b1c5957178fa4b7fa79b31fa4723c996de40810cf3bf814abe5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67cd79aa62a218d6ce384e8b8b8462aba31fea2998566bd1439a34bb30179b6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ccab6ceb7fb86e69f74fc54bd10f58856a6bc107a3e3737fb307cd57d841e5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a63ee52c70cb769b7bd1a09dcc0636c2015de3ac400439edd9eed0ac87d4aab(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5491eb5f392744ef50845b1011cf6b6220e6243fc5eeecaf8a38b868b924f5bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab7d02f0fc462019a4576f8a5a82b64ab8b9a7bb913443c05f1696cec6647f34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8acfa0315d971e7724dbe3a05e132043142e5a1cb34f50f42f2945839dcf3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56537e5d7a3cbf2a1e4f0bacc3fe087a9c1fdef3ef863b4954c9c061c306ec76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0b106d6cd3d8ef26ff7e17815c609f650e04c7bda797bc19a4297a2ba8bdfa4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0f86a4e3992b05dc0f6ec8711908acb3b6f98a7600dc7b844dae0c8f80d54fd(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    auto_create_subnetworks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bgp_always_compare_med: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bgp_best_path_selection_mode: typing.Optional[builtins.str] = None,
    bgp_inter_region_cost: typing.Optional[builtins.str] = None,
    delete_default_routes_on_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_ula_internal_ipv6: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    internal_ipv6_range: typing.Optional[builtins.str] = None,
    mtu: typing.Optional[jsii.Number] = None,
    network_firewall_policy_enforcement_order: typing.Optional[builtins.str] = None,
    network_profile: typing.Optional[builtins.str] = None,
    params: typing.Optional[typing.Union[ComputeNetworkParams, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    routing_mode: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeNetworkTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__355135b9950af107296ff2c712e6ac978b1ad1e6962a226e8a81a9b92fc65840(
    *,
    resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b267e9b7d490d370fabe1b6c0286b7e822f505d0d279e946c8c2ccf8a75f0f78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5547ebef1bcd32523d45812dd32c1fdd7f0fd68f2f6d805474e3b011d3705451(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51c098b2b9cda8603440ba9e4a5844ff09b28f978c144349c7dd73f861dc77cb(
    value: typing.Optional[ComputeNetworkParams],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b157c9db6a18415c8bc4c5ba574318a8982dfe23fe9289fe8db736d9f4cb0350(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e0c2efc71af6e3116a0caa463c41838a6bbd587c3e0ff72b71284ba5d5e10c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a887ff689d0843f5f7d22fa84462368e3b67d8b413a0f44907727194f72210c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c3d6783d67cee546b5f9727e3dc01bc9a3baf23dfaab2f55a1779ef9629bd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7598f8b95b72c0461830ff93139167764e7911cdbb4cb2fc7744ece38c0dbd55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6127bf1e1340bd0d0a6a89518c4d41ab32ef563b41b119dbbedda36d10c488(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeNetworkTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
