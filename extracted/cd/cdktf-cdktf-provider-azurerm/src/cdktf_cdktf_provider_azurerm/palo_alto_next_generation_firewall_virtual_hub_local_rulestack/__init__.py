r'''
# `azurerm_palo_alto_next_generation_firewall_virtual_hub_local_rulestack`

Refer to the Terraform Registry for docs: [`azurerm_palo_alto_next_generation_firewall_virtual_hub_local_rulestack`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack).
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


class PaloAltoNextGenerationFirewallVirtualHubLocalRulestack(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubLocalRulestack.PaloAltoNextGenerationFirewallVirtualHubLocalRulestack",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack azurerm_palo_alto_next_generation_firewall_virtual_hub_local_rulestack}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        network_profile: typing.Union["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfile", typing.Dict[builtins.str, typing.Any]],
        resource_group_name: builtins.str,
        rulestack_id: builtins.str,
        destination_nat: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNat", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dns_settings: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        marketplace_offer_id: typing.Optional[builtins.str] = None,
        plan_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack azurerm_palo_alto_next_generation_firewall_virtual_hub_local_rulestack} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#name PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#name}.
        :param network_profile: network_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#network_profile PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#network_profile}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#resource_group_name PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#resource_group_name}.
        :param rulestack_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#rulestack_id PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#rulestack_id}.
        :param destination_nat: destination_nat block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#destination_nat PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#destination_nat}
        :param dns_settings: dns_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#dns_settings PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#dns_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#id PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param marketplace_offer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#marketplace_offer_id PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#marketplace_offer_id}.
        :param plan_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#plan_id PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#plan_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#tags PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#timeouts PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c348f3047a1dbb80a020fb94b9c31bbcdb136348bd1fd920ea5a2ec623a8d7f6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PaloAltoNextGenerationFirewallVirtualHubLocalRulestackConfig(
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
        '''Generates CDKTF code for importing a PaloAltoNextGenerationFirewallVirtualHubLocalRulestack resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PaloAltoNextGenerationFirewallVirtualHubLocalRulestack to import.
        :param import_from_id: The id of the existing PaloAltoNextGenerationFirewallVirtualHubLocalRulestack that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PaloAltoNextGenerationFirewallVirtualHubLocalRulestack to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__617956a7cd168ce5f7cbe39bfbd5973f4671040ab19986238224d29e2e70a53d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDestinationNat")
    def put_destination_nat(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNat", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__048fd49b8a0ae9891791950085b3e57e8aa6c1490669a5eb650b56c1b40caa3d)
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
        :param dns_servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#dns_servers PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#dns_servers}.
        :param use_azure_dns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#use_azure_dns PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#use_azure_dns}.
        '''
        value = PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettings(
            dns_servers=dns_servers, use_azure_dns=use_azure_dns
        )

        return typing.cast(None, jsii.invoke(self, "putDnsSettings", [value]))

    @jsii.member(jsii_name="putNetworkProfile")
    def put_network_profile(
        self,
        *,
        network_virtual_appliance_id: builtins.str,
        public_ip_address_ids: typing.Sequence[builtins.str],
        virtual_hub_id: builtins.str,
        egress_nat_ip_address_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        trusted_address_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param network_virtual_appliance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#network_virtual_appliance_id PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#network_virtual_appliance_id}.
        :param public_ip_address_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#public_ip_address_ids PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#public_ip_address_ids}.
        :param virtual_hub_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#virtual_hub_id PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#virtual_hub_id}.
        :param egress_nat_ip_address_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#egress_nat_ip_address_ids PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#egress_nat_ip_address_ids}.
        :param trusted_address_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#trusted_address_ranges PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#trusted_address_ranges}.
        '''
        value = PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfile(
            network_virtual_appliance_id=network_virtual_appliance_id,
            public_ip_address_ids=public_ip_address_ids,
            virtual_hub_id=virtual_hub_id,
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#create PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#delete PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#read PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#update PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#update}.
        '''
        value = PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeouts(
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
    ) -> "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatList":
        return typing.cast("PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatList", jsii.get(self, "destinationNat"))

    @builtins.property
    @jsii.member(jsii_name="dnsSettings")
    def dns_settings(
        self,
    ) -> "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettingsOutputReference":
        return typing.cast("PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettingsOutputReference", jsii.get(self, "dnsSettings"))

    @builtins.property
    @jsii.member(jsii_name="networkProfile")
    def network_profile(
        self,
    ) -> "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfileOutputReference":
        return typing.cast("PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfileOutputReference", jsii.get(self, "networkProfile"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeoutsOutputReference":
        return typing.cast("PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="destinationNatInput")
    def destination_nat_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNat"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNat"]]], jsii.get(self, "destinationNatInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsSettingsInput")
    def dns_settings_input(
        self,
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettings"]:
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettings"], jsii.get(self, "dnsSettingsInput"))

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
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfile"]:
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfile"], jsii.get(self, "networkProfileInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1d56881783945e4bbe6898997f2693f4464943011121c8f1e03f4967acde6b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="marketplaceOfferId")
    def marketplace_offer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "marketplaceOfferId"))

    @marketplace_offer_id.setter
    def marketplace_offer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f67a87fd7dc5bf715a6ad22f741cbb501bf679762558c9cefb2ae26fcab0e3d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "marketplaceOfferId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8bbee4b249d19ada82ec0ac0a9dcbea2cfdaa8b5329ef01aae30d0fac8fabe9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="planId")
    def plan_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "planId"))

    @plan_id.setter
    def plan_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0a4898fe5e87fa64917520f7469768bdd0bc6f7711fd1ca71fa3706e564bd4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "planId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d213517816ef8e022bbe79ce6f3d3662d8cc625afa4f886ca38738e0ade847c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rulestackId")
    def rulestack_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rulestackId"))

    @rulestack_id.setter
    def rulestack_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aadf923b6eea9c514df85de8f3f6fd50aca92e7a465dbe1770c357ef6561f4c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rulestackId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22757833b9fe5f03c3bf9c5008e629ccc94d670df6382b16178a9e841c7a179d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubLocalRulestack.PaloAltoNextGenerationFirewallVirtualHubLocalRulestackConfig",
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
class PaloAltoNextGenerationFirewallVirtualHubLocalRulestackConfig(
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
        network_profile: typing.Union["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfile", typing.Dict[builtins.str, typing.Any]],
        resource_group_name: builtins.str,
        rulestack_id: builtins.str,
        destination_nat: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNat", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dns_settings: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        marketplace_offer_id: typing.Optional[builtins.str] = None,
        plan_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#name PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#name}.
        :param network_profile: network_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#network_profile PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#network_profile}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#resource_group_name PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#resource_group_name}.
        :param rulestack_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#rulestack_id PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#rulestack_id}.
        :param destination_nat: destination_nat block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#destination_nat PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#destination_nat}
        :param dns_settings: dns_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#dns_settings PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#dns_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#id PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param marketplace_offer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#marketplace_offer_id PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#marketplace_offer_id}.
        :param plan_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#plan_id PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#plan_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#tags PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#timeouts PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(network_profile, dict):
            network_profile = PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfile(**network_profile)
        if isinstance(dns_settings, dict):
            dns_settings = PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettings(**dns_settings)
        if isinstance(timeouts, dict):
            timeouts = PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06cb03fc410958e536d824a471e2c9c17b3aeca85ce307f49876a99312c7b511)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#name PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_profile(
        self,
    ) -> "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfile":
        '''network_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#network_profile PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#network_profile}
        '''
        result = self._values.get("network_profile")
        assert result is not None, "Required property 'network_profile' is missing"
        return typing.cast("PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfile", result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#resource_group_name PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rulestack_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#rulestack_id PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#rulestack_id}.'''
        result = self._values.get("rulestack_id")
        assert result is not None, "Required property 'rulestack_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_nat(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNat"]]]:
        '''destination_nat block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#destination_nat PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#destination_nat}
        '''
        result = self._values.get("destination_nat")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNat"]]], result)

    @builtins.property
    def dns_settings(
        self,
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettings"]:
        '''dns_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#dns_settings PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#dns_settings}
        '''
        result = self._values.get("dns_settings")
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettings"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#id PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def marketplace_offer_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#marketplace_offer_id PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#marketplace_offer_id}.'''
        result = self._values.get("marketplace_offer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plan_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#plan_id PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#plan_id}.'''
        result = self._values.get("plan_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#tags PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#timeouts PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubLocalRulestack.PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNat",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "protocol": "protocol",
        "backend_config": "backendConfig",
        "frontend_config": "frontendConfig",
    },
)
class PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNat:
    def __init__(
        self,
        *,
        name: builtins.str,
        protocol: builtins.str,
        backend_config: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatBackendConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        frontend_config: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatFrontendConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#name PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#name}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#protocol PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#protocol}.
        :param backend_config: backend_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#backend_config PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#backend_config}
        :param frontend_config: frontend_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#frontend_config PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#frontend_config}
        '''
        if isinstance(backend_config, dict):
            backend_config = PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatBackendConfig(**backend_config)
        if isinstance(frontend_config, dict):
            frontend_config = PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatFrontendConfig(**frontend_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0cafa6bbcc792be11c2c962e2d0172332bb7e0cbe74c6a77201978001dbeda4)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#name PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#protocol PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backend_config(
        self,
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatBackendConfig"]:
        '''backend_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#backend_config PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#backend_config}
        '''
        result = self._values.get("backend_config")
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatBackendConfig"], result)

    @builtins.property
    def frontend_config(
        self,
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatFrontendConfig"]:
        '''frontend_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#frontend_config PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#frontend_config}
        '''
        result = self._values.get("frontend_config")
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatFrontendConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubLocalRulestack.PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatBackendConfig",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "public_ip_address": "publicIpAddress"},
)
class PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatBackendConfig:
    def __init__(self, *, port: jsii.Number, public_ip_address: builtins.str) -> None:
        '''
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#port PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#port}.
        :param public_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#public_ip_address PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#public_ip_address}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6e5d6f2512e4feb9bf2ba25ea650e861fc9758d2729f66a9c80290d20da74f3)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument public_ip_address", value=public_ip_address, expected_type=type_hints["public_ip_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
            "public_ip_address": public_ip_address,
        }

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#port PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def public_ip_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#public_ip_address PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#public_ip_address}.'''
        result = self._values.get("public_ip_address")
        assert result is not None, "Required property 'public_ip_address' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatBackendConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatBackendConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubLocalRulestack.PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatBackendConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f0214b1b5f4937e480afd8ad4167479974ab6570025f80fa6f5636b954851f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f918ed66d1062f8bb67200df30a496daa3859038074590359acc0ec4f98eb860)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicIpAddress")
    def public_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIpAddress"))

    @public_ip_address.setter
    def public_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84e9c171da2f951e34b1f214a71f830177f9c89542462ee9fdb16cc2b9fa37ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatBackendConfig]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatBackendConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatBackendConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac467990365d4fee6dda53982aadfa296d827becb8a7642ce4a3128ea25668ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubLocalRulestack.PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatFrontendConfig",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "public_ip_address_id": "publicIpAddressId"},
)
class PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatFrontendConfig:
    def __init__(
        self,
        *,
        port: jsii.Number,
        public_ip_address_id: builtins.str,
    ) -> None:
        '''
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#port PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#port}.
        :param public_ip_address_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#public_ip_address_id PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#public_ip_address_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b78cc45db478c0a6a947876eb89e8a57b65da8848b5479024b6aeaf899bf3e72)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument public_ip_address_id", value=public_ip_address_id, expected_type=type_hints["public_ip_address_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
            "public_ip_address_id": public_ip_address_id,
        }

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#port PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def public_ip_address_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#public_ip_address_id PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#public_ip_address_id}.'''
        result = self._values.get("public_ip_address_id")
        assert result is not None, "Required property 'public_ip_address_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatFrontendConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatFrontendConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubLocalRulestack.PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatFrontendConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e2fd13f9d3626e649e258eea73cbea2bd145a3cb23f26f9c6d6ce6dcd316854)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22bf6f311399772eb7088f04b6ad633b1a82eb2f63df7207700aef5f45657afc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicIpAddressId")
    def public_ip_address_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIpAddressId"))

    @public_ip_address_id.setter
    def public_ip_address_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5357b760fa506cbe8d3ad64ffcda8f7703c15b1f42c7a54f2b9bb7b1b4e0cc87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpAddressId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatFrontendConfig]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatFrontendConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatFrontendConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf16554835710593d8e145a6a4d4dba4ab07be481220dae8f416a82a5a4d6813)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubLocalRulestack.PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__454a73f96cd93bcf930179536135906e65918d12124052cce6dbf17969507b3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0487e359de5e0d752d691e25d5db1539b54232d3e46eff7516f1fe4812ce15f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daec0255884c932a497dc9371973c8006b049dafd0e4bf57737c6ba3932be97f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db3acc379ac3ab260ef49ec0b93ac7d80740607cef206b4b1cd17cc78fb1b218)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfda31521778ee300217dee2825b0ae6015a9e5b08bc9a25f433f0494fca4a4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNat]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNat]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNat]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8365a06136033af843ac0c12e27a87fdb998e9490f3cd921e070739be2a73946)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubLocalRulestack.PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27fec7f116c179230840fed30e2f14c2ec2361c5ad6d15377c979f93c894b3c7)
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
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#port PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#port}.
        :param public_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#public_ip_address PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#public_ip_address}.
        '''
        value = PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatBackendConfig(
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
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#port PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#port}.
        :param public_ip_address_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#public_ip_address_id PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#public_ip_address_id}.
        '''
        value = PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatFrontendConfig(
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
    ) -> PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatBackendConfigOutputReference:
        return typing.cast(PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatBackendConfigOutputReference, jsii.get(self, "backendConfig"))

    @builtins.property
    @jsii.member(jsii_name="frontendConfig")
    def frontend_config(
        self,
    ) -> PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatFrontendConfigOutputReference:
        return typing.cast(PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatFrontendConfigOutputReference, jsii.get(self, "frontendConfig"))

    @builtins.property
    @jsii.member(jsii_name="backendConfigInput")
    def backend_config_input(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatBackendConfig]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatBackendConfig], jsii.get(self, "backendConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="frontendConfigInput")
    def frontend_config_input(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatFrontendConfig]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatFrontendConfig], jsii.get(self, "frontendConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__442e26d36cc2c71e176658fa3a255e718dde8456926b5870c89eb996798d722e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__697ebc2706930d6b149b3ac56775d0c3c7ef94e45e31f1e4651af4570c8717d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNat]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNat]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNat]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c32cfabac2369d137cd8b8503e1425757fbfdbf0530e585a439b13d43ad9c988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubLocalRulestack.PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettings",
    jsii_struct_bases=[],
    name_mapping={"dns_servers": "dnsServers", "use_azure_dns": "useAzureDns"},
)
class PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettings:
    def __init__(
        self,
        *,
        dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        use_azure_dns: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param dns_servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#dns_servers PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#dns_servers}.
        :param use_azure_dns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#use_azure_dns PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#use_azure_dns}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42b436dba5955590a939157e82455974387d195f0b590fc7750ee5fbe2c52c41)
            check_type(argname="argument dns_servers", value=dns_servers, expected_type=type_hints["dns_servers"])
            check_type(argname="argument use_azure_dns", value=use_azure_dns, expected_type=type_hints["use_azure_dns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dns_servers is not None:
            self._values["dns_servers"] = dns_servers
        if use_azure_dns is not None:
            self._values["use_azure_dns"] = use_azure_dns

    @builtins.property
    def dns_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#dns_servers PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#dns_servers}.'''
        result = self._values.get("dns_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def use_azure_dns(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#use_azure_dns PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#use_azure_dns}.'''
        result = self._values.get("use_azure_dns")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubLocalRulestack.PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18987a224d95dcfc154f98fcffd5c79b9d2787685a71ce476b92f5aec38d2ab8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1ec4168fb7946cb5ec185a9bd50f00124120f20257c2467283bcee02b57f021)
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
            type_hints = typing.get_type_hints(_typecheckingstub__283d6f6144c32a8241b967d1b580b44ddf6ef91fefb0bf58bc593f6e9bfd18f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useAzureDns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettings]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffafaf220c150574121e727f9feb531a0563cf82e8c9cc421d86e6923e7d2bef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubLocalRulestack.PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfile",
    jsii_struct_bases=[],
    name_mapping={
        "network_virtual_appliance_id": "networkVirtualApplianceId",
        "public_ip_address_ids": "publicIpAddressIds",
        "virtual_hub_id": "virtualHubId",
        "egress_nat_ip_address_ids": "egressNatIpAddressIds",
        "trusted_address_ranges": "trustedAddressRanges",
    },
)
class PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfile:
    def __init__(
        self,
        *,
        network_virtual_appliance_id: builtins.str,
        public_ip_address_ids: typing.Sequence[builtins.str],
        virtual_hub_id: builtins.str,
        egress_nat_ip_address_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        trusted_address_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param network_virtual_appliance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#network_virtual_appliance_id PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#network_virtual_appliance_id}.
        :param public_ip_address_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#public_ip_address_ids PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#public_ip_address_ids}.
        :param virtual_hub_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#virtual_hub_id PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#virtual_hub_id}.
        :param egress_nat_ip_address_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#egress_nat_ip_address_ids PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#egress_nat_ip_address_ids}.
        :param trusted_address_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#trusted_address_ranges PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#trusted_address_ranges}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b130e7feeefe167602d8374ed61dd325c119710cf9a9983dc01fcd49411487fc)
            check_type(argname="argument network_virtual_appliance_id", value=network_virtual_appliance_id, expected_type=type_hints["network_virtual_appliance_id"])
            check_type(argname="argument public_ip_address_ids", value=public_ip_address_ids, expected_type=type_hints["public_ip_address_ids"])
            check_type(argname="argument virtual_hub_id", value=virtual_hub_id, expected_type=type_hints["virtual_hub_id"])
            check_type(argname="argument egress_nat_ip_address_ids", value=egress_nat_ip_address_ids, expected_type=type_hints["egress_nat_ip_address_ids"])
            check_type(argname="argument trusted_address_ranges", value=trusted_address_ranges, expected_type=type_hints["trusted_address_ranges"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_virtual_appliance_id": network_virtual_appliance_id,
            "public_ip_address_ids": public_ip_address_ids,
            "virtual_hub_id": virtual_hub_id,
        }
        if egress_nat_ip_address_ids is not None:
            self._values["egress_nat_ip_address_ids"] = egress_nat_ip_address_ids
        if trusted_address_ranges is not None:
            self._values["trusted_address_ranges"] = trusted_address_ranges

    @builtins.property
    def network_virtual_appliance_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#network_virtual_appliance_id PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#network_virtual_appliance_id}.'''
        result = self._values.get("network_virtual_appliance_id")
        assert result is not None, "Required property 'network_virtual_appliance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def public_ip_address_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#public_ip_address_ids PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#public_ip_address_ids}.'''
        result = self._values.get("public_ip_address_ids")
        assert result is not None, "Required property 'public_ip_address_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def virtual_hub_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#virtual_hub_id PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#virtual_hub_id}.'''
        result = self._values.get("virtual_hub_id")
        assert result is not None, "Required property 'virtual_hub_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def egress_nat_ip_address_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#egress_nat_ip_address_ids PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#egress_nat_ip_address_ids}.'''
        result = self._values.get("egress_nat_ip_address_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def trusted_address_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#trusted_address_ranges PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#trusted_address_ranges}.'''
        result = self._values.get("trusted_address_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubLocalRulestack.PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__643741dbf22094ab8fbe39bd9b1e0bbbc1bad676fa7315cd5bfa53fb340d99b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
    @jsii.member(jsii_name="ipOfTrustForUserDefinedRoutes")
    def ip_of_trust_for_user_defined_routes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipOfTrustForUserDefinedRoutes"))

    @builtins.property
    @jsii.member(jsii_name="publicIpAddresses")
    def public_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "publicIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="trustedSubnetId")
    def trusted_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trustedSubnetId"))

    @builtins.property
    @jsii.member(jsii_name="untrustedSubnetId")
    def untrusted_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "untrustedSubnetId"))

    @builtins.property
    @jsii.member(jsii_name="egressNatIpAddressIdsInput")
    def egress_nat_ip_address_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "egressNatIpAddressIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="networkVirtualApplianceIdInput")
    def network_virtual_appliance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkVirtualApplianceIdInput"))

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
    @jsii.member(jsii_name="virtualHubIdInput")
    def virtual_hub_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualHubIdInput"))

    @builtins.property
    @jsii.member(jsii_name="egressNatIpAddressIds")
    def egress_nat_ip_address_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "egressNatIpAddressIds"))

    @egress_nat_ip_address_ids.setter
    def egress_nat_ip_address_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c8abd6e9a0f872d3098076f3e395fbb65e46653296a91d85922e1863836501d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "egressNatIpAddressIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkVirtualApplianceId")
    def network_virtual_appliance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkVirtualApplianceId"))

    @network_virtual_appliance_id.setter
    def network_virtual_appliance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e91869876120adb0026249243a5904db64720b5e48d7f0b66b2ed350372423f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkVirtualApplianceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicIpAddressIds")
    def public_ip_address_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "publicIpAddressIds"))

    @public_ip_address_ids.setter
    def public_ip_address_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da9a08794a5ee47e1e6ca9cde7eb4ee09c433f66cae13bad5c65cc00a62ce4a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpAddressIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustedAddressRanges")
    def trusted_address_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "trustedAddressRanges"))

    @trusted_address_ranges.setter
    def trusted_address_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8954654f665def0fee12d860212785dfe88248fd3e65e3a9d2c5519a29acd6cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustedAddressRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualHubId")
    def virtual_hub_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualHubId"))

    @virtual_hub_id.setter
    def virtual_hub_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc8c27ece4bad8b46bd90f0b0846412e6d2043cb96a367bda0d2f9ca9885c920)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualHubId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfile]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3ef96b07de080c158a7c0ddf50f4535bee68f5a626f772813fd151e92b564c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubLocalRulestack.PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#create PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#delete PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#read PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#update PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d91dee9090efb9f37a4d1b3c2d50221a6cd51329811ba993f1744a8d4f37a757)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#create PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#delete PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#read PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_local_rulestack#update PaloAltoNextGenerationFirewallVirtualHubLocalRulestack#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubLocalRulestack.PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd0355845fcf0a697179a55cf075bfbbee2b4ac659fa790a86e83a64c7de3f2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8c82bfafa8d091ab727b72c1a42f133ae375336afd6a8e6c6cebb9fc46f0ec3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c74c73a264714e6b76c50637f64a21e6a590be152d02e92ee200e3483d7d5b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c27bb5799b5ac76803c0eab0d17ee6c8d7ce6ef59d8429c2b8caba0bc05d0e04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4a9ea2dc13afef6a7d4d890a7b030e67f12a34606222dac7dcf41ad766ec7f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a3c197502d9a41cea52d9ffd9391a1a98a637f66e62e181fdf740789c572645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "PaloAltoNextGenerationFirewallVirtualHubLocalRulestack",
    "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackConfig",
    "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNat",
    "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatBackendConfig",
    "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatBackendConfigOutputReference",
    "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatFrontendConfig",
    "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatFrontendConfigOutputReference",
    "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatList",
    "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatOutputReference",
    "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettings",
    "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettingsOutputReference",
    "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfile",
    "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfileOutputReference",
    "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeouts",
    "PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c348f3047a1dbb80a020fb94b9c31bbcdb136348bd1fd920ea5a2ec623a8d7f6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    network_profile: typing.Union[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfile, typing.Dict[builtins.str, typing.Any]],
    resource_group_name: builtins.str,
    rulestack_id: builtins.str,
    destination_nat: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNat, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns_settings: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    marketplace_offer_id: typing.Optional[builtins.str] = None,
    plan_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__617956a7cd168ce5f7cbe39bfbd5973f4671040ab19986238224d29e2e70a53d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__048fd49b8a0ae9891791950085b3e57e8aa6c1490669a5eb650b56c1b40caa3d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNat, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d56881783945e4bbe6898997f2693f4464943011121c8f1e03f4967acde6b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f67a87fd7dc5bf715a6ad22f741cbb501bf679762558c9cefb2ae26fcab0e3d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8bbee4b249d19ada82ec0ac0a9dcbea2cfdaa8b5329ef01aae30d0fac8fabe9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0a4898fe5e87fa64917520f7469768bdd0bc6f7711fd1ca71fa3706e564bd4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d213517816ef8e022bbe79ce6f3d3662d8cc625afa4f886ca38738e0ade847c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aadf923b6eea9c514df85de8f3f6fd50aca92e7a465dbe1770c357ef6561f4c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22757833b9fe5f03c3bf9c5008e629ccc94d670df6382b16178a9e841c7a179d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06cb03fc410958e536d824a471e2c9c17b3aeca85ce307f49876a99312c7b511(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    network_profile: typing.Union[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfile, typing.Dict[builtins.str, typing.Any]],
    resource_group_name: builtins.str,
    rulestack_id: builtins.str,
    destination_nat: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNat, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns_settings: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    marketplace_offer_id: typing.Optional[builtins.str] = None,
    plan_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0cafa6bbcc792be11c2c962e2d0172332bb7e0cbe74c6a77201978001dbeda4(
    *,
    name: builtins.str,
    protocol: builtins.str,
    backend_config: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatBackendConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    frontend_config: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatFrontendConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e5d6f2512e4feb9bf2ba25ea650e861fc9758d2729f66a9c80290d20da74f3(
    *,
    port: jsii.Number,
    public_ip_address: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0214b1b5f4937e480afd8ad4167479974ab6570025f80fa6f5636b954851f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f918ed66d1062f8bb67200df30a496daa3859038074590359acc0ec4f98eb860(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e9c171da2f951e34b1f214a71f830177f9c89542462ee9fdb16cc2b9fa37ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac467990365d4fee6dda53982aadfa296d827becb8a7642ce4a3128ea25668ec(
    value: typing.Optional[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatBackendConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b78cc45db478c0a6a947876eb89e8a57b65da8848b5479024b6aeaf899bf3e72(
    *,
    port: jsii.Number,
    public_ip_address_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e2fd13f9d3626e649e258eea73cbea2bd145a3cb23f26f9c6d6ce6dcd316854(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22bf6f311399772eb7088f04b6ad633b1a82eb2f63df7207700aef5f45657afc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5357b760fa506cbe8d3ad64ffcda8f7703c15b1f42c7a54f2b9bb7b1b4e0cc87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf16554835710593d8e145a6a4d4dba4ab07be481220dae8f416a82a5a4d6813(
    value: typing.Optional[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNatFrontendConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__454a73f96cd93bcf930179536135906e65918d12124052cce6dbf17969507b3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0487e359de5e0d752d691e25d5db1539b54232d3e46eff7516f1fe4812ce15f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daec0255884c932a497dc9371973c8006b049dafd0e4bf57737c6ba3932be97f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db3acc379ac3ab260ef49ec0b93ac7d80740607cef206b4b1cd17cc78fb1b218(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfda31521778ee300217dee2825b0ae6015a9e5b08bc9a25f433f0494fca4a4c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8365a06136033af843ac0c12e27a87fdb998e9490f3cd921e070739be2a73946(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNat]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27fec7f116c179230840fed30e2f14c2ec2361c5ad6d15377c979f93c894b3c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__442e26d36cc2c71e176658fa3a255e718dde8456926b5870c89eb996798d722e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__697ebc2706930d6b149b3ac56775d0c3c7ef94e45e31f1e4651af4570c8717d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c32cfabac2369d137cd8b8503e1425757fbfdbf0530e585a439b13d43ad9c988(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDestinationNat]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42b436dba5955590a939157e82455974387d195f0b590fc7750ee5fbe2c52c41(
    *,
    dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    use_azure_dns: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18987a224d95dcfc154f98fcffd5c79b9d2787685a71ce476b92f5aec38d2ab8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ec4168fb7946cb5ec185a9bd50f00124120f20257c2467283bcee02b57f021(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283d6f6144c32a8241b967d1b580b44ddf6ef91fefb0bf58bc593f6e9bfd18f6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffafaf220c150574121e727f9feb531a0563cf82e8c9cc421d86e6923e7d2bef(
    value: typing.Optional[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackDnsSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b130e7feeefe167602d8374ed61dd325c119710cf9a9983dc01fcd49411487fc(
    *,
    network_virtual_appliance_id: builtins.str,
    public_ip_address_ids: typing.Sequence[builtins.str],
    virtual_hub_id: builtins.str,
    egress_nat_ip_address_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    trusted_address_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643741dbf22094ab8fbe39bd9b1e0bbbc1bad676fa7315cd5bfa53fb340d99b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c8abd6e9a0f872d3098076f3e395fbb65e46653296a91d85922e1863836501d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e91869876120adb0026249243a5904db64720b5e48d7f0b66b2ed350372423f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da9a08794a5ee47e1e6ca9cde7eb4ee09c433f66cae13bad5c65cc00a62ce4a1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8954654f665def0fee12d860212785dfe88248fd3e65e3a9d2c5519a29acd6cd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc8c27ece4bad8b46bd90f0b0846412e6d2043cb96a367bda0d2f9ca9885c920(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3ef96b07de080c158a7c0ddf50f4535bee68f5a626f772813fd151e92b564c(
    value: typing.Optional[PaloAltoNextGenerationFirewallVirtualHubLocalRulestackNetworkProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d91dee9090efb9f37a4d1b3c2d50221a6cd51329811ba993f1744a8d4f37a757(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0355845fcf0a697179a55cf075bfbbee2b4ac659fa790a86e83a64c7de3f2d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8c82bfafa8d091ab727b72c1a42f133ae375336afd6a8e6c6cebb9fc46f0ec3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c74c73a264714e6b76c50637f64a21e6a590be152d02e92ee200e3483d7d5b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27bb5799b5ac76803c0eab0d17ee6c8d7ce6ef59d8429c2b8caba0bc05d0e04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4a9ea2dc13afef6a7d4d890a7b030e67f12a34606222dac7dcf41ad766ec7f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a3c197502d9a41cea52d9ffd9391a1a98a637f66e62e181fdf740789c572645(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualHubLocalRulestackTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
