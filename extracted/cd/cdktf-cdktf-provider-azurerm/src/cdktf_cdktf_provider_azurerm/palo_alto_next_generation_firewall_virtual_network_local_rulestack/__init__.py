r'''
# `azurerm_palo_alto_next_generation_firewall_virtual_network_local_rulestack`

Refer to the Terraform Registry for docs: [`azurerm_palo_alto_next_generation_firewall_virtual_network_local_rulestack`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack).
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


class PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkLocalRulestack.PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack azurerm_palo_alto_next_generation_firewall_virtual_network_local_rulestack}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        network_profile: typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfile", typing.Dict[builtins.str, typing.Any]],
        resource_group_name: builtins.str,
        rulestack_id: builtins.str,
        destination_nat: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNat", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dns_settings: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        marketplace_offer_id: typing.Optional[builtins.str] = None,
        plan_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack azurerm_palo_alto_next_generation_firewall_virtual_network_local_rulestack} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#name PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#name}.
        :param network_profile: network_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#network_profile PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#network_profile}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#resource_group_name PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#resource_group_name}.
        :param rulestack_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#rulestack_id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#rulestack_id}.
        :param destination_nat: destination_nat block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#destination_nat PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#destination_nat}
        :param dns_settings: dns_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#dns_settings PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#dns_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param marketplace_offer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#marketplace_offer_id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#marketplace_offer_id}.
        :param plan_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#plan_id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#plan_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#tags PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#timeouts PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fabd81024a74db6a62184909967a01279646784aed96c2847754cab8e82d482e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackConfig(
            name=name,
            network_profile=network_profile,
            resource_group_name=resource_group_name,
            rulestack_id=rulestack_id,
            destination_nat=destination_nat,
            dns_settings=dns_settings,
            id=id,
            marketplace_offer_id=marketplace_offer_id,
            plan_id=plan_id,
            tags=tags,
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
        '''Generates CDKTF code for importing a PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack to import.
        :param import_from_id: The id of the existing PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeac54cc15dd1d30b34ac146e79ebfd163322a9e6f0efb415a3deb8aca947d63)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDestinationNat")
    def put_destination_nat(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNat", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0889f5ebe339980bccea36967617616944fbb1d9333ecf737fcb08a08f0bec3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDestinationNat", [value]))

    @jsii.member(jsii_name="putDnsSettings")
    def put_dns_settings(
        self,
        *,
        dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        use_azure_dns: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param dns_servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#dns_servers PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#dns_servers}.
        :param use_azure_dns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#use_azure_dns PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#use_azure_dns}.
        '''
        value = PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettings(
            dns_servers=dns_servers, use_azure_dns=use_azure_dns
        )

        return typing.cast(None, jsii.invoke(self, "putDnsSettings", [value]))

    @jsii.member(jsii_name="putNetworkProfile")
    def put_network_profile(
        self,
        *,
        public_ip_address_ids: typing.Sequence[builtins.str],
        vnet_configuration: typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileVnetConfiguration", typing.Dict[builtins.str, typing.Any]],
        egress_nat_ip_address_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        trusted_address_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param public_ip_address_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#public_ip_address_ids PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#public_ip_address_ids}.
        :param vnet_configuration: vnet_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#vnet_configuration PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#vnet_configuration}
        :param egress_nat_ip_address_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#egress_nat_ip_address_ids PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#egress_nat_ip_address_ids}.
        :param trusted_address_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#trusted_address_ranges PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#trusted_address_ranges}.
        '''
        value = PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfile(
            public_ip_address_ids=public_ip_address_ids,
            vnet_configuration=vnet_configuration,
            egress_nat_ip_address_ids=egress_nat_ip_address_ids,
            trusted_address_ranges=trusted_address_ranges,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkProfile", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#create PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#delete PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#read PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#update PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#update}.
        '''
        value = PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDestinationNat")
    def reset_destination_nat(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationNat", []))

    @jsii.member(jsii_name="resetDnsSettings")
    def reset_dns_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsSettings", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMarketplaceOfferId")
    def reset_marketplace_offer_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMarketplaceOfferId", []))

    @jsii.member(jsii_name="resetPlanId")
    def reset_plan_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlanId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="destinationNat")
    def destination_nat(
        self,
    ) -> "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatList":
        return typing.cast("PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatList", jsii.get(self, "destinationNat"))

    @builtins.property
    @jsii.member(jsii_name="dnsSettings")
    def dns_settings(
        self,
    ) -> "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettingsOutputReference":
        return typing.cast("PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettingsOutputReference", jsii.get(self, "dnsSettings"))

    @builtins.property
    @jsii.member(jsii_name="networkProfile")
    def network_profile(
        self,
    ) -> "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileOutputReference":
        return typing.cast("PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileOutputReference", jsii.get(self, "networkProfile"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeoutsOutputReference":
        return typing.cast("PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="destinationNatInput")
    def destination_nat_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNat"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNat"]]], jsii.get(self, "destinationNatInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsSettingsInput")
    def dns_settings_input(
        self,
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettings"]:
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettings"], jsii.get(self, "dnsSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="marketplaceOfferIdInput")
    def marketplace_offer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "marketplaceOfferIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkProfileInput")
    def network_profile_input(
        self,
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfile"]:
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfile"], jsii.get(self, "networkProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="planIdInput")
    def plan_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "planIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rulestackIdInput")
    def rulestack_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rulestackIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a1498122ae67241b1cef56753aa9f149f2cc2986dea11fe7fe3c062380bd8b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="marketplaceOfferId")
    def marketplace_offer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "marketplaceOfferId"))

    @marketplace_offer_id.setter
    def marketplace_offer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__611194c41c5a92ca35aa8e562120eef36b0b5fd0e4bbc8ff4e8f77a582e36357)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "marketplaceOfferId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba2e986fb9987030ea770a28c7a803f4aa3091f7da10603c33a3937094e5efd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="planId")
    def plan_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "planId"))

    @plan_id.setter
    def plan_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ab33260f1689e76eceaeda84804766793c7d13e38f04402d30bcc3df7db2a43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "planId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__697c99dcefb782c8bfed40c6c13a214bb45130192a94e7b611d39a3fc36b2cd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rulestackId")
    def rulestack_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rulestackId"))

    @rulestack_id.setter
    def rulestack_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1f42569e76646ad9e6abe850d243d5b7efe00dc1ffc368548194878619d0acb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rulestackId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__758b834b63b3ab2e4c47bcfcf65f06804e28ef36c8ece4eb9d43725f0fb46436)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkLocalRulestack.PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackConfig",
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
        "network_profile": "networkProfile",
        "resource_group_name": "resourceGroupName",
        "rulestack_id": "rulestackId",
        "destination_nat": "destinationNat",
        "dns_settings": "dnsSettings",
        "id": "id",
        "marketplace_offer_id": "marketplaceOfferId",
        "plan_id": "planId",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        network_profile: typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfile", typing.Dict[builtins.str, typing.Any]],
        resource_group_name: builtins.str,
        rulestack_id: builtins.str,
        destination_nat: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNat", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dns_settings: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        marketplace_offer_id: typing.Optional[builtins.str] = None,
        plan_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#name PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#name}.
        :param network_profile: network_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#network_profile PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#network_profile}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#resource_group_name PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#resource_group_name}.
        :param rulestack_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#rulestack_id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#rulestack_id}.
        :param destination_nat: destination_nat block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#destination_nat PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#destination_nat}
        :param dns_settings: dns_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#dns_settings PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#dns_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param marketplace_offer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#marketplace_offer_id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#marketplace_offer_id}.
        :param plan_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#plan_id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#plan_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#tags PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#timeouts PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(network_profile, dict):
            network_profile = PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfile(**network_profile)
        if isinstance(dns_settings, dict):
            dns_settings = PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettings(**dns_settings)
        if isinstance(timeouts, dict):
            timeouts = PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c742b16fe6bc26d67f794c07d501182a2fd6a0c6a4ce098027d72c88c0d28eaa)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_profile", value=network_profile, expected_type=type_hints["network_profile"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument rulestack_id", value=rulestack_id, expected_type=type_hints["rulestack_id"])
            check_type(argname="argument destination_nat", value=destination_nat, expected_type=type_hints["destination_nat"])
            check_type(argname="argument dns_settings", value=dns_settings, expected_type=type_hints["dns_settings"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument marketplace_offer_id", value=marketplace_offer_id, expected_type=type_hints["marketplace_offer_id"])
            check_type(argname="argument plan_id", value=plan_id, expected_type=type_hints["plan_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "network_profile": network_profile,
            "resource_group_name": resource_group_name,
            "rulestack_id": rulestack_id,
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
        if destination_nat is not None:
            self._values["destination_nat"] = destination_nat
        if dns_settings is not None:
            self._values["dns_settings"] = dns_settings
        if id is not None:
            self._values["id"] = id
        if marketplace_offer_id is not None:
            self._values["marketplace_offer_id"] = marketplace_offer_id
        if plan_id is not None:
            self._values["plan_id"] = plan_id
        if tags is not None:
            self._values["tags"] = tags
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#name PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_profile(
        self,
    ) -> "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfile":
        '''network_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#network_profile PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#network_profile}
        '''
        result = self._values.get("network_profile")
        assert result is not None, "Required property 'network_profile' is missing"
        return typing.cast("PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfile", result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#resource_group_name PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rulestack_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#rulestack_id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#rulestack_id}.'''
        result = self._values.get("rulestack_id")
        assert result is not None, "Required property 'rulestack_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_nat(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNat"]]]:
        '''destination_nat block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#destination_nat PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#destination_nat}
        '''
        result = self._values.get("destination_nat")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNat"]]], result)

    @builtins.property
    def dns_settings(
        self,
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettings"]:
        '''dns_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#dns_settings PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#dns_settings}
        '''
        result = self._values.get("dns_settings")
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettings"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def marketplace_offer_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#marketplace_offer_id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#marketplace_offer_id}.'''
        result = self._values.get("marketplace_offer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plan_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#plan_id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#plan_id}.'''
        result = self._values.get("plan_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#tags PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#timeouts PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkLocalRulestack.PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNat",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "protocol": "protocol",
        "backend_config": "backendConfig",
        "frontend_config": "frontendConfig",
    },
)
class PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNat:
    def __init__(
        self,
        *,
        name: builtins.str,
        protocol: builtins.str,
        backend_config: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatBackendConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        frontend_config: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatFrontendConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#name PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#name}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#protocol PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#protocol}.
        :param backend_config: backend_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#backend_config PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#backend_config}
        :param frontend_config: frontend_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#frontend_config PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#frontend_config}
        '''
        if isinstance(backend_config, dict):
            backend_config = PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatBackendConfig(**backend_config)
        if isinstance(frontend_config, dict):
            frontend_config = PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatFrontendConfig(**frontend_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c8f3ac0819a70360ac436085491fcec0c5d4fa2193a1a73e08b29ed108ba3eb)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument backend_config", value=backend_config, expected_type=type_hints["backend_config"])
            check_type(argname="argument frontend_config", value=frontend_config, expected_type=type_hints["frontend_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "protocol": protocol,
        }
        if backend_config is not None:
            self._values["backend_config"] = backend_config
        if frontend_config is not None:
            self._values["frontend_config"] = frontend_config

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#name PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#protocol PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backend_config(
        self,
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatBackendConfig"]:
        '''backend_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#backend_config PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#backend_config}
        '''
        result = self._values.get("backend_config")
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatBackendConfig"], result)

    @builtins.property
    def frontend_config(
        self,
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatFrontendConfig"]:
        '''frontend_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#frontend_config PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#frontend_config}
        '''
        result = self._values.get("frontend_config")
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatFrontendConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkLocalRulestack.PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatBackendConfig",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "public_ip_address": "publicIpAddress"},
)
class PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatBackendConfig:
    def __init__(self, *, port: jsii.Number, public_ip_address: builtins.str) -> None:
        '''
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#port PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#port}.
        :param public_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#public_ip_address PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#public_ip_address}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a8001c98f44ff406effc177c0c382872597f6f69bd12b3b5986c938953cd419)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument public_ip_address", value=public_ip_address, expected_type=type_hints["public_ip_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
            "public_ip_address": public_ip_address,
        }

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#port PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def public_ip_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#public_ip_address PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#public_ip_address}.'''
        result = self._values.get("public_ip_address")
        assert result is not None, "Required property 'public_ip_address' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatBackendConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatBackendConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkLocalRulestack.PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatBackendConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66a25f4739cf5e5aeb62f818bd95af52f5110ae2b8be69dc408f55e2f30da79e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="publicIpAddressInput")
    def public_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a41c1c36084693e891103cb8a535a3e559af6ab4e348f5c5ade63ff2aba34d23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicIpAddress")
    def public_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIpAddress"))

    @public_ip_address.setter
    def public_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bbcf27bb4f8ecec4b921891fab41df91de7f5d4d3277dac4aae07452cd0ce1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatBackendConfig]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatBackendConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatBackendConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85ef0dd5766a7335005cd8ccae680f94065d92ff933a1a9540efdf9eed4bfd7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkLocalRulestack.PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatFrontendConfig",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "public_ip_address_id": "publicIpAddressId"},
)
class PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatFrontendConfig:
    def __init__(
        self,
        *,
        port: jsii.Number,
        public_ip_address_id: builtins.str,
    ) -> None:
        '''
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#port PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#port}.
        :param public_ip_address_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#public_ip_address_id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#public_ip_address_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5311e31c94c66fa1b2da74869e2cd7c11ef10f19d21db180a6f4e8aa8e0e6136)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument public_ip_address_id", value=public_ip_address_id, expected_type=type_hints["public_ip_address_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
            "public_ip_address_id": public_ip_address_id,
        }

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#port PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def public_ip_address_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#public_ip_address_id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#public_ip_address_id}.'''
        result = self._values.get("public_ip_address_id")
        assert result is not None, "Required property 'public_ip_address_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatFrontendConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatFrontendConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkLocalRulestack.PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatFrontendConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ea58a5e580746a392b59b6ee98b4a419016d0883aa6ca0689ed487077032c74)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="publicIpAddressIdInput")
    def public_ip_address_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicIpAddressIdInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78fd718618f85fa28089202838e92170a1c329e3c220734cb562155360fdf56e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicIpAddressId")
    def public_ip_address_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIpAddressId"))

    @public_ip_address_id.setter
    def public_ip_address_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__125c02c26b7cc6cbafac3ca8d2ca6241c5356fe6464316a7d44910b0ecfb447d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpAddressId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatFrontendConfig]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatFrontendConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatFrontendConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__528683e2928fad4cfceb4b346d97dc3b8b5f3ed3094820a0f9d8c4625df9ac7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkLocalRulestack.PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85a89a91991b5d60e7a93f90863e7599dc98d38853ac7cd15df0d0b12e83e7f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__778c11368043eef4bfd02e6621c2e53124ea0a1653916b0ee007551f98989ef5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__097d30a00d5e77a2c9bd4ce0cb9014948f773b114fd3906f1509278441ebe11a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__679d443f5c0bfa14dd5563f476a06c95705cd591837af8b1ae6f511b0c15ef98)
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
            type_hints = typing.get_type_hints(_typecheckingstub__456fd25d0048e0719eb18da58e78e7d1a7bfdcf0047e1b3ad12f36b0f6c40e0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNat]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNat]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNat]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdf06a1b0429b7ebdb360ccc8f2a3ca9a0ec1ca210e4bf73422ea9d601b3db09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkLocalRulestack.PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de035221dc200e7385b508f37a0453c645fa54a42815915ca46c1b6cda21cc85)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putBackendConfig")
    def put_backend_config(
        self,
        *,
        port: jsii.Number,
        public_ip_address: builtins.str,
    ) -> None:
        '''
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#port PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#port}.
        :param public_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#public_ip_address PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#public_ip_address}.
        '''
        value = PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatBackendConfig(
            port=port, public_ip_address=public_ip_address
        )

        return typing.cast(None, jsii.invoke(self, "putBackendConfig", [value]))

    @jsii.member(jsii_name="putFrontendConfig")
    def put_frontend_config(
        self,
        *,
        port: jsii.Number,
        public_ip_address_id: builtins.str,
    ) -> None:
        '''
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#port PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#port}.
        :param public_ip_address_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#public_ip_address_id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#public_ip_address_id}.
        '''
        value = PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatFrontendConfig(
            port=port, public_ip_address_id=public_ip_address_id
        )

        return typing.cast(None, jsii.invoke(self, "putFrontendConfig", [value]))

    @jsii.member(jsii_name="resetBackendConfig")
    def reset_backend_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackendConfig", []))

    @jsii.member(jsii_name="resetFrontendConfig")
    def reset_frontend_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrontendConfig", []))

    @builtins.property
    @jsii.member(jsii_name="backendConfig")
    def backend_config(
        self,
    ) -> PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatBackendConfigOutputReference:
        return typing.cast(PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatBackendConfigOutputReference, jsii.get(self, "backendConfig"))

    @builtins.property
    @jsii.member(jsii_name="frontendConfig")
    def frontend_config(
        self,
    ) -> PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatFrontendConfigOutputReference:
        return typing.cast(PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatFrontendConfigOutputReference, jsii.get(self, "frontendConfig"))

    @builtins.property
    @jsii.member(jsii_name="backendConfigInput")
    def backend_config_input(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatBackendConfig]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatBackendConfig], jsii.get(self, "backendConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="frontendConfigInput")
    def frontend_config_input(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatFrontendConfig]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatFrontendConfig], jsii.get(self, "frontendConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffcd0c2feab6555ce1e79f09130629c6400a2349d31ff333eba8d067b83cdc57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c8edcd4b36089183c633dafe0bef914b3f4d850945730362d11cc59d7672cfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNat]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNat]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNat]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f6342b106a16cb386ad9bd1014eab2086f265f964dcff3045198a1ff8637418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkLocalRulestack.PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettings",
    jsii_struct_bases=[],
    name_mapping={"dns_servers": "dnsServers", "use_azure_dns": "useAzureDns"},
)
class PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettings:
    def __init__(
        self,
        *,
        dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        use_azure_dns: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param dns_servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#dns_servers PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#dns_servers}.
        :param use_azure_dns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#use_azure_dns PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#use_azure_dns}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc45fe84a27bc0734134475175e7a425251428f55415702ef9a0da2fceeebaa4)
            check_type(argname="argument dns_servers", value=dns_servers, expected_type=type_hints["dns_servers"])
            check_type(argname="argument use_azure_dns", value=use_azure_dns, expected_type=type_hints["use_azure_dns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dns_servers is not None:
            self._values["dns_servers"] = dns_servers
        if use_azure_dns is not None:
            self._values["use_azure_dns"] = use_azure_dns

    @builtins.property
    def dns_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#dns_servers PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#dns_servers}.'''
        result = self._values.get("dns_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def use_azure_dns(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#use_azure_dns PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#use_azure_dns}.'''
        result = self._values.get("use_azure_dns")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkLocalRulestack.PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d358ac937e1cd3484f7b50802d063df0b5da294762650c3b46f295a0edd165ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDnsServers")
    def reset_dns_servers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsServers", []))

    @jsii.member(jsii_name="resetUseAzureDns")
    def reset_use_azure_dns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseAzureDns", []))

    @builtins.property
    @jsii.member(jsii_name="azureDnsServers")
    def azure_dns_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "azureDnsServers"))

    @builtins.property
    @jsii.member(jsii_name="dnsServersInput")
    def dns_servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dnsServersInput"))

    @builtins.property
    @jsii.member(jsii_name="useAzureDnsInput")
    def use_azure_dns_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useAzureDnsInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsServers")
    def dns_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsServers"))

    @dns_servers.setter
    def dns_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1898f4e54667fb101f5aa2345b7bd9e2c26518063af96900c1b2966e2da68c29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useAzureDns")
    def use_azure_dns(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useAzureDns"))

    @use_azure_dns.setter
    def use_azure_dns(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0cf9af7b02c93221854951be260df0cb3f53db26e423077ac23ec6a88d7cc93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useAzureDns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettings]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b5b7f3bb9c57345006546048df029ef69d8ad360e9430b9c0b166d32520a388)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkLocalRulestack.PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfile",
    jsii_struct_bases=[],
    name_mapping={
        "public_ip_address_ids": "publicIpAddressIds",
        "vnet_configuration": "vnetConfiguration",
        "egress_nat_ip_address_ids": "egressNatIpAddressIds",
        "trusted_address_ranges": "trustedAddressRanges",
    },
)
class PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfile:
    def __init__(
        self,
        *,
        public_ip_address_ids: typing.Sequence[builtins.str],
        vnet_configuration: typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileVnetConfiguration", typing.Dict[builtins.str, typing.Any]],
        egress_nat_ip_address_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        trusted_address_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param public_ip_address_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#public_ip_address_ids PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#public_ip_address_ids}.
        :param vnet_configuration: vnet_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#vnet_configuration PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#vnet_configuration}
        :param egress_nat_ip_address_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#egress_nat_ip_address_ids PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#egress_nat_ip_address_ids}.
        :param trusted_address_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#trusted_address_ranges PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#trusted_address_ranges}.
        '''
        if isinstance(vnet_configuration, dict):
            vnet_configuration = PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileVnetConfiguration(**vnet_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a407627e1149e7b66b0a6bf8b79903476c93d5032c15f641b6dca24be92d11b)
            check_type(argname="argument public_ip_address_ids", value=public_ip_address_ids, expected_type=type_hints["public_ip_address_ids"])
            check_type(argname="argument vnet_configuration", value=vnet_configuration, expected_type=type_hints["vnet_configuration"])
            check_type(argname="argument egress_nat_ip_address_ids", value=egress_nat_ip_address_ids, expected_type=type_hints["egress_nat_ip_address_ids"])
            check_type(argname="argument trusted_address_ranges", value=trusted_address_ranges, expected_type=type_hints["trusted_address_ranges"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "public_ip_address_ids": public_ip_address_ids,
            "vnet_configuration": vnet_configuration,
        }
        if egress_nat_ip_address_ids is not None:
            self._values["egress_nat_ip_address_ids"] = egress_nat_ip_address_ids
        if trusted_address_ranges is not None:
            self._values["trusted_address_ranges"] = trusted_address_ranges

    @builtins.property
    def public_ip_address_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#public_ip_address_ids PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#public_ip_address_ids}.'''
        result = self._values.get("public_ip_address_ids")
        assert result is not None, "Required property 'public_ip_address_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def vnet_configuration(
        self,
    ) -> "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileVnetConfiguration":
        '''vnet_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#vnet_configuration PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#vnet_configuration}
        '''
        result = self._values.get("vnet_configuration")
        assert result is not None, "Required property 'vnet_configuration' is missing"
        return typing.cast("PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileVnetConfiguration", result)

    @builtins.property
    def egress_nat_ip_address_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#egress_nat_ip_address_ids PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#egress_nat_ip_address_ids}.'''
        result = self._values.get("egress_nat_ip_address_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def trusted_address_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#trusted_address_ranges PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#trusted_address_ranges}.'''
        result = self._values.get("trusted_address_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkLocalRulestack.PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bff8dc431809d17d2882e2c28b6a53c3c9b9d738933967ef1b8892def99f1eef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVnetConfiguration")
    def put_vnet_configuration(
        self,
        *,
        virtual_network_id: builtins.str,
        trusted_subnet_id: typing.Optional[builtins.str] = None,
        untrusted_subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#virtual_network_id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#virtual_network_id}.
        :param trusted_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#trusted_subnet_id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#trusted_subnet_id}.
        :param untrusted_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#untrusted_subnet_id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#untrusted_subnet_id}.
        '''
        value = PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileVnetConfiguration(
            virtual_network_id=virtual_network_id,
            trusted_subnet_id=trusted_subnet_id,
            untrusted_subnet_id=untrusted_subnet_id,
        )

        return typing.cast(None, jsii.invoke(self, "putVnetConfiguration", [value]))

    @jsii.member(jsii_name="resetEgressNatIpAddressIds")
    def reset_egress_nat_ip_address_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgressNatIpAddressIds", []))

    @jsii.member(jsii_name="resetTrustedAddressRanges")
    def reset_trusted_address_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedAddressRanges", []))

    @builtins.property
    @jsii.member(jsii_name="egressNatIpAddresses")
    def egress_nat_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "egressNatIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="publicIpAddresses")
    def public_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "publicIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="vnetConfiguration")
    def vnet_configuration(
        self,
    ) -> "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileVnetConfigurationOutputReference":
        return typing.cast("PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileVnetConfigurationOutputReference", jsii.get(self, "vnetConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="egressNatIpAddressIdsInput")
    def egress_nat_ip_address_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "egressNatIpAddressIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="publicIpAddressIdsInput")
    def public_ip_address_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "publicIpAddressIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedAddressRangesInput")
    def trusted_address_ranges_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "trustedAddressRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="vnetConfigurationInput")
    def vnet_configuration_input(
        self,
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileVnetConfiguration"]:
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileVnetConfiguration"], jsii.get(self, "vnetConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="egressNatIpAddressIds")
    def egress_nat_ip_address_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "egressNatIpAddressIds"))

    @egress_nat_ip_address_ids.setter
    def egress_nat_ip_address_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df6880faeb05e739d926f098f4340099c0f7048509d0191d9b10f60943552c43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "egressNatIpAddressIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicIpAddressIds")
    def public_ip_address_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "publicIpAddressIds"))

    @public_ip_address_ids.setter
    def public_ip_address_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08991152b0e39d4d000a87bad3eec23a9b44396e8f8a76dfaa78d6b1a922315d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpAddressIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustedAddressRanges")
    def trusted_address_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "trustedAddressRanges"))

    @trusted_address_ranges.setter
    def trusted_address_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2df6df858e84e5716af3d222669e3f2c43b2552b80ba86a6052239e4c5f677d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustedAddressRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfile]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81165bcfd435c473a7782d35b29cd5cbd15d42b4bb284b759ae49974a4f36ed7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkLocalRulestack.PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileVnetConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "virtual_network_id": "virtualNetworkId",
        "trusted_subnet_id": "trustedSubnetId",
        "untrusted_subnet_id": "untrustedSubnetId",
    },
)
class PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileVnetConfiguration:
    def __init__(
        self,
        *,
        virtual_network_id: builtins.str,
        trusted_subnet_id: typing.Optional[builtins.str] = None,
        untrusted_subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#virtual_network_id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#virtual_network_id}.
        :param trusted_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#trusted_subnet_id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#trusted_subnet_id}.
        :param untrusted_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#untrusted_subnet_id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#untrusted_subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14130a01ad92c2041a551a3a06177cc3ecacfe14c51d0dfe7a9ff9d94a34250e)
            check_type(argname="argument virtual_network_id", value=virtual_network_id, expected_type=type_hints["virtual_network_id"])
            check_type(argname="argument trusted_subnet_id", value=trusted_subnet_id, expected_type=type_hints["trusted_subnet_id"])
            check_type(argname="argument untrusted_subnet_id", value=untrusted_subnet_id, expected_type=type_hints["untrusted_subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "virtual_network_id": virtual_network_id,
        }
        if trusted_subnet_id is not None:
            self._values["trusted_subnet_id"] = trusted_subnet_id
        if untrusted_subnet_id is not None:
            self._values["untrusted_subnet_id"] = untrusted_subnet_id

    @builtins.property
    def virtual_network_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#virtual_network_id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#virtual_network_id}.'''
        result = self._values.get("virtual_network_id")
        assert result is not None, "Required property 'virtual_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trusted_subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#trusted_subnet_id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#trusted_subnet_id}.'''
        result = self._values.get("trusted_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def untrusted_subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#untrusted_subnet_id PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#untrusted_subnet_id}.'''
        result = self._values.get("untrusted_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileVnetConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileVnetConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkLocalRulestack.PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileVnetConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0635858d979df0003ccd917d776bfc34aa939f2851aa89a6fb79a9aa92ec5563)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTrustedSubnetId")
    def reset_trusted_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedSubnetId", []))

    @jsii.member(jsii_name="resetUntrustedSubnetId")
    def reset_untrusted_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUntrustedSubnetId", []))

    @builtins.property
    @jsii.member(jsii_name="ipOfTrustForUserDefinedRoutes")
    def ip_of_trust_for_user_defined_routes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipOfTrustForUserDefinedRoutes"))

    @builtins.property
    @jsii.member(jsii_name="trustedSubnetIdInput")
    def trusted_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trustedSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="untrustedSubnetIdInput")
    def untrusted_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "untrustedSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkIdInput")
    def virtual_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedSubnetId")
    def trusted_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trustedSubnetId"))

    @trusted_subnet_id.setter
    def trusted_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9874ad4cfdfbb2976ded1c2e2c0cb2c05048281b0620f526cb11240434042a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustedSubnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="untrustedSubnetId")
    def untrusted_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "untrustedSubnetId"))

    @untrusted_subnet_id.setter
    def untrusted_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ede39859e687f0e32c5001ff5045214adc1a7960bd6d25b24c44cc711ea571)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "untrustedSubnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2692ac8957dbf5920f2b20debeaa002330ba8b6138b25f34c48379a60312d3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileVnetConfiguration]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileVnetConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileVnetConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96ee4da578a1e0cd663c94e9ec06f5ad9da19ed35a4e25f6a33b88357fb5cc3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkLocalRulestack.PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#create PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#delete PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#read PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#update PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbb3a6552419d2b837ecd20cee544af357548431ecf12beea0c32bce5eb825e1)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#create PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#delete PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#read PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_local_rulestack#update PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkLocalRulestack.PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92fce38e641324ce97e3322b93eefc54dc42ca96c0bca13fe558a60a93d668c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__8358f7db0ca79f818325cb1a57c72d74852407baf9e8a127d7077585799c9965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba2e507a5ac0615d3e40852695b048eca29f0cf42729bf886e3d3d60f89f3b04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8239787a78e5cf2348152009e915361911724e1616844cfca0596445520293b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0741fa67cd307faa12e97db26a31ebfc0974a1f931e279732854fa899e2847f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__877ff13d7e128afb76d290b41fd77629de02333a41ca9f825fe59c8d0ea58b58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestack",
    "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackConfig",
    "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNat",
    "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatBackendConfig",
    "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatBackendConfigOutputReference",
    "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatFrontendConfig",
    "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatFrontendConfigOutputReference",
    "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatList",
    "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatOutputReference",
    "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettings",
    "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettingsOutputReference",
    "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfile",
    "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileOutputReference",
    "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileVnetConfiguration",
    "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileVnetConfigurationOutputReference",
    "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeouts",
    "PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__fabd81024a74db6a62184909967a01279646784aed96c2847754cab8e82d482e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    network_profile: typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfile, typing.Dict[builtins.str, typing.Any]],
    resource_group_name: builtins.str,
    rulestack_id: builtins.str,
    destination_nat: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNat, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns_settings: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    marketplace_offer_id: typing.Optional[builtins.str] = None,
    plan_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__aeac54cc15dd1d30b34ac146e79ebfd163322a9e6f0efb415a3deb8aca947d63(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0889f5ebe339980bccea36967617616944fbb1d9333ecf737fcb08a08f0bec3a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNat, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a1498122ae67241b1cef56753aa9f149f2cc2986dea11fe7fe3c062380bd8b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__611194c41c5a92ca35aa8e562120eef36b0b5fd0e4bbc8ff4e8f77a582e36357(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2e986fb9987030ea770a28c7a803f4aa3091f7da10603c33a3937094e5efd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ab33260f1689e76eceaeda84804766793c7d13e38f04402d30bcc3df7db2a43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__697c99dcefb782c8bfed40c6c13a214bb45130192a94e7b611d39a3fc36b2cd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1f42569e76646ad9e6abe850d243d5b7efe00dc1ffc368548194878619d0acb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758b834b63b3ab2e4c47bcfcf65f06804e28ef36c8ece4eb9d43725f0fb46436(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c742b16fe6bc26d67f794c07d501182a2fd6a0c6a4ce098027d72c88c0d28eaa(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    network_profile: typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfile, typing.Dict[builtins.str, typing.Any]],
    resource_group_name: builtins.str,
    rulestack_id: builtins.str,
    destination_nat: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNat, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns_settings: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    marketplace_offer_id: typing.Optional[builtins.str] = None,
    plan_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c8f3ac0819a70360ac436085491fcec0c5d4fa2193a1a73e08b29ed108ba3eb(
    *,
    name: builtins.str,
    protocol: builtins.str,
    backend_config: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatBackendConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    frontend_config: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatFrontendConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a8001c98f44ff406effc177c0c382872597f6f69bd12b3b5986c938953cd419(
    *,
    port: jsii.Number,
    public_ip_address: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a25f4739cf5e5aeb62f818bd95af52f5110ae2b8be69dc408f55e2f30da79e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41c1c36084693e891103cb8a535a3e559af6ab4e348f5c5ade63ff2aba34d23(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bbcf27bb4f8ecec4b921891fab41df91de7f5d4d3277dac4aae07452cd0ce1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85ef0dd5766a7335005cd8ccae680f94065d92ff933a1a9540efdf9eed4bfd7d(
    value: typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatBackendConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5311e31c94c66fa1b2da74869e2cd7c11ef10f19d21db180a6f4e8aa8e0e6136(
    *,
    port: jsii.Number,
    public_ip_address_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ea58a5e580746a392b59b6ee98b4a419016d0883aa6ca0689ed487077032c74(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78fd718618f85fa28089202838e92170a1c329e3c220734cb562155360fdf56e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125c02c26b7cc6cbafac3ca8d2ca6241c5356fe6464316a7d44910b0ecfb447d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528683e2928fad4cfceb4b346d97dc3b8b5f3ed3094820a0f9d8c4625df9ac7f(
    value: typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNatFrontendConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85a89a91991b5d60e7a93f90863e7599dc98d38853ac7cd15df0d0b12e83e7f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__778c11368043eef4bfd02e6621c2e53124ea0a1653916b0ee007551f98989ef5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__097d30a00d5e77a2c9bd4ce0cb9014948f773b114fd3906f1509278441ebe11a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__679d443f5c0bfa14dd5563f476a06c95705cd591837af8b1ae6f511b0c15ef98(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__456fd25d0048e0719eb18da58e78e7d1a7bfdcf0047e1b3ad12f36b0f6c40e0e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf06a1b0429b7ebdb360ccc8f2a3ca9a0ec1ca210e4bf73422ea9d601b3db09(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNat]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de035221dc200e7385b508f37a0453c645fa54a42815915ca46c1b6cda21cc85(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffcd0c2feab6555ce1e79f09130629c6400a2349d31ff333eba8d067b83cdc57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c8edcd4b36089183c633dafe0bef914b3f4d850945730362d11cc59d7672cfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f6342b106a16cb386ad9bd1014eab2086f265f964dcff3045198a1ff8637418(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDestinationNat]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc45fe84a27bc0734134475175e7a425251428f55415702ef9a0da2fceeebaa4(
    *,
    dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    use_azure_dns: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d358ac937e1cd3484f7b50802d063df0b5da294762650c3b46f295a0edd165ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1898f4e54667fb101f5aa2345b7bd9e2c26518063af96900c1b2966e2da68c29(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0cf9af7b02c93221854951be260df0cb3f53db26e423077ac23ec6a88d7cc93(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b5b7f3bb9c57345006546048df029ef69d8ad360e9430b9c0b166d32520a388(
    value: typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackDnsSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a407627e1149e7b66b0a6bf8b79903476c93d5032c15f641b6dca24be92d11b(
    *,
    public_ip_address_ids: typing.Sequence[builtins.str],
    vnet_configuration: typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileVnetConfiguration, typing.Dict[builtins.str, typing.Any]],
    egress_nat_ip_address_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    trusted_address_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bff8dc431809d17d2882e2c28b6a53c3c9b9d738933967ef1b8892def99f1eef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df6880faeb05e739d926f098f4340099c0f7048509d0191d9b10f60943552c43(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08991152b0e39d4d000a87bad3eec23a9b44396e8f8a76dfaa78d6b1a922315d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2df6df858e84e5716af3d222669e3f2c43b2552b80ba86a6052239e4c5f677d0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81165bcfd435c473a7782d35b29cd5cbd15d42b4bb284b759ae49974a4f36ed7(
    value: typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14130a01ad92c2041a551a3a06177cc3ecacfe14c51d0dfe7a9ff9d94a34250e(
    *,
    virtual_network_id: builtins.str,
    trusted_subnet_id: typing.Optional[builtins.str] = None,
    untrusted_subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0635858d979df0003ccd917d776bfc34aa939f2851aa89a6fb79a9aa92ec5563(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9874ad4cfdfbb2976ded1c2e2c0cb2c05048281b0620f526cb11240434042a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ede39859e687f0e32c5001ff5045214adc1a7960bd6d25b24c44cc711ea571(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2692ac8957dbf5920f2b20debeaa002330ba8b6138b25f34c48379a60312d3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ee4da578a1e0cd663c94e9ec06f5ad9da19ed35a4e25f6a33b88357fb5cc3a(
    value: typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackNetworkProfileVnetConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb3a6552419d2b837ecd20cee544af357548431ecf12beea0c32bce5eb825e1(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92fce38e641324ce97e3322b93eefc54dc42ca96c0bca13fe558a60a93d668c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8358f7db0ca79f818325cb1a57c72d74852407baf9e8a127d7077585799c9965(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2e507a5ac0615d3e40852695b048eca29f0cf42729bf886e3d3d60f89f3b04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8239787a78e5cf2348152009e915361911724e1616844cfca0596445520293b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0741fa67cd307faa12e97db26a31ebfc0974a1f931e279732854fa899e2847f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__877ff13d7e128afb76d290b41fd77629de02333a41ca9f825fe59c8d0ea58b58(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualNetworkLocalRulestackTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
