r'''
# `google_compute_network`

Refer to the Terraform Registry for docs: [`google_compute_network`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network).
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


class GoogleComputeNetwork(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeNetwork.GoogleComputeNetwork",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network google_compute_network}.'''

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
        project: typing.Optional[builtins.str] = None,
        routing_mode: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeNetworkTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network google_compute_network} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#name GoogleComputeNetwork#name}
        :param auto_create_subnetworks: When set to 'true', the network is created in "auto subnet mode" and it will create a subnet for each region automatically across the '10.128.0.0/9' address range. When set to 'false', the network is created in "custom subnet mode" so the user can explicitly connect subnetwork resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#auto_create_subnetworks GoogleComputeNetwork#auto_create_subnetworks}
        :param bgp_always_compare_med: Enables/disables the comparison of MED across routes with different Neighbor ASNs. This value can only be set if the --bgp-best-path-selection-mode is STANDARD Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#bgp_always_compare_med GoogleComputeNetwork#bgp_always_compare_med}
        :param bgp_best_path_selection_mode: The BGP best selection algorithm to be employed. MODE can be LEGACY or STANDARD. Possible values: ["LEGACY", "STANDARD"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#bgp_best_path_selection_mode GoogleComputeNetwork#bgp_best_path_selection_mode}
        :param bgp_inter_region_cost: Choice of the behavior of inter-regional cost and MED in the BPS algorithm. Possible values: ["DEFAULT", "ADD_COST_TO_MED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#bgp_inter_region_cost GoogleComputeNetwork#bgp_inter_region_cost}
        :param delete_default_routes_on_create: If set to 'true', default routes ('0.0.0.0/0') will be deleted immediately after network creation. Defaults to 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#delete_default_routes_on_create GoogleComputeNetwork#delete_default_routes_on_create}
        :param description: An optional description of this resource. The resource must be recreated to modify this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#description GoogleComputeNetwork#description}
        :param enable_ula_internal_ipv6: Enable ULA internal ipv6 on this network. Enabling this feature will assign a /48 from google defined ULA prefix fd20::/20. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#enable_ula_internal_ipv6 GoogleComputeNetwork#enable_ula_internal_ipv6}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#id GoogleComputeNetwork#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param internal_ipv6_range: When enabling ula internal ipv6, caller optionally can specify the /48 range they want from the google defined ULA prefix fd20::/20. The input must be a valid /48 ULA IPv6 address and must be within the fd20::/20. Operation will fail if the speficied /48 is already in used by another resource. If the field is not speficied, then a /48 range will be randomly allocated from fd20::/20 and returned via this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#internal_ipv6_range GoogleComputeNetwork#internal_ipv6_range}
        :param mtu: Maximum Transmission Unit in bytes. The default value is 1460 bytes. The minimum value for this field is 1300 and the maximum value is 8896 bytes (jumbo frames). Note that packets larger than 1500 bytes (standard Ethernet) can be subject to TCP-MSS clamping or dropped with an ICMP 'Fragmentation-Needed' message if the packets are routed to the Internet or other VPCs with varying MTUs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#mtu GoogleComputeNetwork#mtu}
        :param network_firewall_policy_enforcement_order: Set the order that Firewall Rules and Firewall Policies are evaluated. Default value: "AFTER_CLASSIC_FIREWALL" Possible values: ["BEFORE_CLASSIC_FIREWALL", "AFTER_CLASSIC_FIREWALL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#network_firewall_policy_enforcement_order GoogleComputeNetwork#network_firewall_policy_enforcement_order}
        :param network_profile: A full or partial URL of the network profile to apply to this network. This field can be set only at resource creation time. For example, the following are valid URLs: - https://www.googleapis.com/compute/v1/projects/{projectId}/global/networkProfiles/{network_profile_name} - projects/{projectId}/global/networkProfiles/{network_profile_name} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#network_profile GoogleComputeNetwork#network_profile}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#project GoogleComputeNetwork#project}.
        :param routing_mode: The network-wide routing mode to use. If set to 'REGIONAL', this network's cloud routers will only advertise routes with subnetworks of this network in the same region as the router. If set to 'GLOBAL', this network's cloud routers will advertise routes with all subnetworks of this network, across regions. Possible values: ["REGIONAL", "GLOBAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#routing_mode GoogleComputeNetwork#routing_mode}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#timeouts GoogleComputeNetwork#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efcbc0bc1556ea86f9b0c20e56c1160b5b1f9d276259bab777ac416d80e88aa6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleComputeNetworkConfig(
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
        '''Generates CDKTF code for importing a GoogleComputeNetwork resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleComputeNetwork to import.
        :param import_from_id: The id of the existing GoogleComputeNetwork that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleComputeNetwork to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33ecea2c352744d94bc36340f93ae14e3f779a3b9379d2fa258c36328f88bd13)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#create GoogleComputeNetwork#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#delete GoogleComputeNetwork#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#update GoogleComputeNetwork#update}.
        '''
        value = GoogleComputeNetworkTimeouts(
            create=create, delete=delete, update=update
        )

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
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleComputeNetworkTimeoutsOutputReference":
        return typing.cast("GoogleComputeNetworkTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeNetworkTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeNetworkTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7930acfa2dc14bc66546390cf7d7d90aa3a4594f960dd6ad0dd7478a72bb0099)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbd9e9635da780dfe723b2cea9a75976e2a82371a37d74fff757325644dd8974)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bgpAlwaysCompareMed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bgpBestPathSelectionMode")
    def bgp_best_path_selection_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bgpBestPathSelectionMode"))

    @bgp_best_path_selection_mode.setter
    def bgp_best_path_selection_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1af66c80fd0e53d47b9669079fafcae60c873fb4078d3610b503558878a5304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bgpBestPathSelectionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bgpInterRegionCost")
    def bgp_inter_region_cost(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bgpInterRegionCost"))

    @bgp_inter_region_cost.setter
    def bgp_inter_region_cost(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__026a4cf4121a437c79cb759e6255b4fe0956a8a788f0e97d41fb96430c2e01dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c79534591740b15b20007ac3f736147e027f8847faa3d4525d527e0ab97af25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteDefaultRoutesOnCreate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8450118f83a79e61a091f3dd83e6627b4adaa7bf91034638406b30a492cfb0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09b272f5cacae7e68691dc52a98568b8d39d894659f2ec2185c1fb68d2f10308)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableUlaInternalIpv6", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb987011c73f46a8e467e2346a1e9358f8297e73abd7b0d5efe21c539be758f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalIpv6Range")
    def internal_ipv6_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "internalIpv6Range"))

    @internal_ipv6_range.setter
    def internal_ipv6_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__905a6a5ad902772df8c5d3afb84e4d7050bf4f171aa113804e6ee2a4eca418aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalIpv6Range", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mtu")
    def mtu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mtu"))

    @mtu.setter
    def mtu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e55be36500d249a973f92facb99afc3f88a9d6e592aad825d83e848b3727afe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mtu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fa45d477b933179a0142c6d22f9a6a6418e36d2d54a8165a984a7b9a1bde64f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkFirewallPolicyEnforcementOrder")
    def network_firewall_policy_enforcement_order(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkFirewallPolicyEnforcementOrder"))

    @network_firewall_policy_enforcement_order.setter
    def network_firewall_policy_enforcement_order(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9191b17f7d525f096e7ab45dc234ed7293f8cd695215298cfa369631b5a78e96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkFirewallPolicyEnforcementOrder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkProfile")
    def network_profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkProfile"))

    @network_profile.setter
    def network_profile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__911105c0d7187163e52e53941da45de12c323cbfdc52343340244513ee4d34f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkProfile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f1b6ec06f0933076045d76cc9fc3d77e45cd72804239f3b5a987b39ba5d14fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingMode")
    def routing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routingMode"))

    @routing_mode.setter
    def routing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cdd6bd396b96e39bb0aa7ce9984013a183244734aa18b73fff3aaf680841dc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingMode", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeNetwork.GoogleComputeNetworkConfig",
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
        "project": "project",
        "routing_mode": "routingMode",
        "timeouts": "timeouts",
    },
)
class GoogleComputeNetworkConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        project: typing.Optional[builtins.str] = None,
        routing_mode: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeNetworkTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#name GoogleComputeNetwork#name}
        :param auto_create_subnetworks: When set to 'true', the network is created in "auto subnet mode" and it will create a subnet for each region automatically across the '10.128.0.0/9' address range. When set to 'false', the network is created in "custom subnet mode" so the user can explicitly connect subnetwork resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#auto_create_subnetworks GoogleComputeNetwork#auto_create_subnetworks}
        :param bgp_always_compare_med: Enables/disables the comparison of MED across routes with different Neighbor ASNs. This value can only be set if the --bgp-best-path-selection-mode is STANDARD Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#bgp_always_compare_med GoogleComputeNetwork#bgp_always_compare_med}
        :param bgp_best_path_selection_mode: The BGP best selection algorithm to be employed. MODE can be LEGACY or STANDARD. Possible values: ["LEGACY", "STANDARD"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#bgp_best_path_selection_mode GoogleComputeNetwork#bgp_best_path_selection_mode}
        :param bgp_inter_region_cost: Choice of the behavior of inter-regional cost and MED in the BPS algorithm. Possible values: ["DEFAULT", "ADD_COST_TO_MED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#bgp_inter_region_cost GoogleComputeNetwork#bgp_inter_region_cost}
        :param delete_default_routes_on_create: If set to 'true', default routes ('0.0.0.0/0') will be deleted immediately after network creation. Defaults to 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#delete_default_routes_on_create GoogleComputeNetwork#delete_default_routes_on_create}
        :param description: An optional description of this resource. The resource must be recreated to modify this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#description GoogleComputeNetwork#description}
        :param enable_ula_internal_ipv6: Enable ULA internal ipv6 on this network. Enabling this feature will assign a /48 from google defined ULA prefix fd20::/20. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#enable_ula_internal_ipv6 GoogleComputeNetwork#enable_ula_internal_ipv6}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#id GoogleComputeNetwork#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param internal_ipv6_range: When enabling ula internal ipv6, caller optionally can specify the /48 range they want from the google defined ULA prefix fd20::/20. The input must be a valid /48 ULA IPv6 address and must be within the fd20::/20. Operation will fail if the speficied /48 is already in used by another resource. If the field is not speficied, then a /48 range will be randomly allocated from fd20::/20 and returned via this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#internal_ipv6_range GoogleComputeNetwork#internal_ipv6_range}
        :param mtu: Maximum Transmission Unit in bytes. The default value is 1460 bytes. The minimum value for this field is 1300 and the maximum value is 8896 bytes (jumbo frames). Note that packets larger than 1500 bytes (standard Ethernet) can be subject to TCP-MSS clamping or dropped with an ICMP 'Fragmentation-Needed' message if the packets are routed to the Internet or other VPCs with varying MTUs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#mtu GoogleComputeNetwork#mtu}
        :param network_firewall_policy_enforcement_order: Set the order that Firewall Rules and Firewall Policies are evaluated. Default value: "AFTER_CLASSIC_FIREWALL" Possible values: ["BEFORE_CLASSIC_FIREWALL", "AFTER_CLASSIC_FIREWALL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#network_firewall_policy_enforcement_order GoogleComputeNetwork#network_firewall_policy_enforcement_order}
        :param network_profile: A full or partial URL of the network profile to apply to this network. This field can be set only at resource creation time. For example, the following are valid URLs: - https://www.googleapis.com/compute/v1/projects/{projectId}/global/networkProfiles/{network_profile_name} - projects/{projectId}/global/networkProfiles/{network_profile_name} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#network_profile GoogleComputeNetwork#network_profile}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#project GoogleComputeNetwork#project}.
        :param routing_mode: The network-wide routing mode to use. If set to 'REGIONAL', this network's cloud routers will only advertise routes with subnetworks of this network in the same region as the router. If set to 'GLOBAL', this network's cloud routers will advertise routes with all subnetworks of this network, across regions. Possible values: ["REGIONAL", "GLOBAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#routing_mode GoogleComputeNetwork#routing_mode}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#timeouts GoogleComputeNetwork#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = GoogleComputeNetworkTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82181717c6e04daeded1ac8cd59e4618d70781cf3ecb330413f82e335eb530b3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#name GoogleComputeNetwork#name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#auto_create_subnetworks GoogleComputeNetwork#auto_create_subnetworks}
        '''
        result = self._values.get("auto_create_subnetworks")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def bgp_always_compare_med(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables/disables the comparison of MED across routes with different Neighbor ASNs.

        This value can only be set if the --bgp-best-path-selection-mode is STANDARD

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#bgp_always_compare_med GoogleComputeNetwork#bgp_always_compare_med}
        '''
        result = self._values.get("bgp_always_compare_med")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def bgp_best_path_selection_mode(self) -> typing.Optional[builtins.str]:
        '''The BGP best selection algorithm to be employed. MODE can be LEGACY or STANDARD. Possible values: ["LEGACY", "STANDARD"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#bgp_best_path_selection_mode GoogleComputeNetwork#bgp_best_path_selection_mode}
        '''
        result = self._values.get("bgp_best_path_selection_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bgp_inter_region_cost(self) -> typing.Optional[builtins.str]:
        '''Choice of the behavior of inter-regional cost and MED in the BPS algorithm. Possible values: ["DEFAULT", "ADD_COST_TO_MED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#bgp_inter_region_cost GoogleComputeNetwork#bgp_inter_region_cost}
        '''
        result = self._values.get("bgp_inter_region_cost")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete_default_routes_on_create(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to 'true', default routes ('0.0.0.0/0') will be deleted immediately after network creation. Defaults to 'false'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#delete_default_routes_on_create GoogleComputeNetwork#delete_default_routes_on_create}
        '''
        result = self._values.get("delete_default_routes_on_create")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. The resource must be recreated to modify this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#description GoogleComputeNetwork#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_ula_internal_ipv6(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable ULA internal ipv6 on this network. Enabling this feature will assign a /48 from google defined ULA prefix fd20::/20.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#enable_ula_internal_ipv6 GoogleComputeNetwork#enable_ula_internal_ipv6}
        '''
        result = self._values.get("enable_ula_internal_ipv6")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#id GoogleComputeNetwork#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#internal_ipv6_range GoogleComputeNetwork#internal_ipv6_range}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#mtu GoogleComputeNetwork#mtu}
        '''
        result = self._values.get("mtu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def network_firewall_policy_enforcement_order(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Set the order that Firewall Rules and Firewall Policies are evaluated. Default value: "AFTER_CLASSIC_FIREWALL" Possible values: ["BEFORE_CLASSIC_FIREWALL", "AFTER_CLASSIC_FIREWALL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#network_firewall_policy_enforcement_order GoogleComputeNetwork#network_firewall_policy_enforcement_order}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#network_profile GoogleComputeNetwork#network_profile}
        '''
        result = self._values.get("network_profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#project GoogleComputeNetwork#project}.'''
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#routing_mode GoogleComputeNetwork#routing_mode}
        '''
        result = self._values.get("routing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleComputeNetworkTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#timeouts GoogleComputeNetwork#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleComputeNetworkTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeNetwork.GoogleComputeNetworkTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleComputeNetworkTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#create GoogleComputeNetwork#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#delete GoogleComputeNetwork#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#update GoogleComputeNetwork#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a77485fffc0ceb439fdb08aef066716225f22b2c83de6b2ad81380a4dd3d435c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#create GoogleComputeNetwork#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#delete GoogleComputeNetwork#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_network#update GoogleComputeNetwork#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeNetworkTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeNetworkTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeNetwork.GoogleComputeNetworkTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3219bd1f8006142bec95776bc67c52e3d82db5127ad55f9c1510df66e0a52a76)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebe1c7e75900f41cd188f470ccfcf668a988c6736179422001fc09e09c07dfe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__891b69df1e726dd7095b0e3101f173c62d64ca872539c5cc9e49b15dd469c9f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e6931f17c4513bd42a5e18f542d6605c71c42580bccd6fdd845192b0626e707)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeNetworkTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeNetworkTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeNetworkTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec38535d242ab7671788d5c229b917cdabb0f03a377b75439959d2b739839397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleComputeNetwork",
    "GoogleComputeNetworkConfig",
    "GoogleComputeNetworkTimeouts",
    "GoogleComputeNetworkTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__efcbc0bc1556ea86f9b0c20e56c1160b5b1f9d276259bab777ac416d80e88aa6(
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
    project: typing.Optional[builtins.str] = None,
    routing_mode: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeNetworkTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__33ecea2c352744d94bc36340f93ae14e3f779a3b9379d2fa258c36328f88bd13(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7930acfa2dc14bc66546390cf7d7d90aa3a4594f960dd6ad0dd7478a72bb0099(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbd9e9635da780dfe723b2cea9a75976e2a82371a37d74fff757325644dd8974(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1af66c80fd0e53d47b9669079fafcae60c873fb4078d3610b503558878a5304(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__026a4cf4121a437c79cb759e6255b4fe0956a8a788f0e97d41fb96430c2e01dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c79534591740b15b20007ac3f736147e027f8847faa3d4525d527e0ab97af25(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8450118f83a79e61a091f3dd83e6627b4adaa7bf91034638406b30a492cfb0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b272f5cacae7e68691dc52a98568b8d39d894659f2ec2185c1fb68d2f10308(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb987011c73f46a8e467e2346a1e9358f8297e73abd7b0d5efe21c539be758f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__905a6a5ad902772df8c5d3afb84e4d7050bf4f171aa113804e6ee2a4eca418aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e55be36500d249a973f92facb99afc3f88a9d6e592aad825d83e848b3727afe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fa45d477b933179a0142c6d22f9a6a6418e36d2d54a8165a984a7b9a1bde64f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9191b17f7d525f096e7ab45dc234ed7293f8cd695215298cfa369631b5a78e96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__911105c0d7187163e52e53941da45de12c323cbfdc52343340244513ee4d34f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f1b6ec06f0933076045d76cc9fc3d77e45cd72804239f3b5a987b39ba5d14fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cdd6bd396b96e39bb0aa7ce9984013a183244734aa18b73fff3aaf680841dc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82181717c6e04daeded1ac8cd59e4618d70781cf3ecb330413f82e335eb530b3(
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
    project: typing.Optional[builtins.str] = None,
    routing_mode: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeNetworkTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a77485fffc0ceb439fdb08aef066716225f22b2c83de6b2ad81380a4dd3d435c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3219bd1f8006142bec95776bc67c52e3d82db5127ad55f9c1510df66e0a52a76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe1c7e75900f41cd188f470ccfcf668a988c6736179422001fc09e09c07dfe7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__891b69df1e726dd7095b0e3101f173c62d64ca872539c5cc9e49b15dd469c9f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e6931f17c4513bd42a5e18f542d6605c71c42580bccd6fdd845192b0626e707(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec38535d242ab7671788d5c229b917cdabb0f03a377b75439959d2b739839397(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeNetworkTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
