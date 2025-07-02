r'''
# `azurerm_palo_alto_next_generation_firewall_virtual_hub_panorama`

Refer to the Terraform Registry for docs: [`azurerm_palo_alto_next_generation_firewall_virtual_hub_panorama`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama).
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


class PaloAltoNextGenerationFirewallVirtualHubPanorama(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubPanorama.PaloAltoNextGenerationFirewallVirtualHubPanorama",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama azurerm_palo_alto_next_generation_firewall_virtual_hub_panorama}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        network_profile: typing.Union["PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfile", typing.Dict[builtins.str, typing.Any]],
        panorama_base64_config: builtins.str,
        resource_group_name: builtins.str,
        destination_nat: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNat", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dns_settings: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        marketplace_offer_id: typing.Optional[builtins.str] = None,
        plan_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama azurerm_palo_alto_next_generation_firewall_virtual_hub_panorama} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#location PaloAltoNextGenerationFirewallVirtualHubPanorama#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#name PaloAltoNextGenerationFirewallVirtualHubPanorama#name}.
        :param network_profile: network_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#network_profile PaloAltoNextGenerationFirewallVirtualHubPanorama#network_profile}
        :param panorama_base64_config: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#panorama_base64_config PaloAltoNextGenerationFirewallVirtualHubPanorama#panorama_base64_config}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#resource_group_name PaloAltoNextGenerationFirewallVirtualHubPanorama#resource_group_name}.
        :param destination_nat: destination_nat block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#destination_nat PaloAltoNextGenerationFirewallVirtualHubPanorama#destination_nat}
        :param dns_settings: dns_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#dns_settings PaloAltoNextGenerationFirewallVirtualHubPanorama#dns_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#id PaloAltoNextGenerationFirewallVirtualHubPanorama#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param marketplace_offer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#marketplace_offer_id PaloAltoNextGenerationFirewallVirtualHubPanorama#marketplace_offer_id}.
        :param plan_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#plan_id PaloAltoNextGenerationFirewallVirtualHubPanorama#plan_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#tags PaloAltoNextGenerationFirewallVirtualHubPanorama#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#timeouts PaloAltoNextGenerationFirewallVirtualHubPanorama#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2081c298f262c74e27b286ee0f1adf628f9c840dca85afd93eb0111a44151643)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PaloAltoNextGenerationFirewallVirtualHubPanoramaConfig(
            location=location,
            name=name,
            network_profile=network_profile,
            panorama_base64_config=panorama_base64_config,
            resource_group_name=resource_group_name,
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
        '''Generates CDKTF code for importing a PaloAltoNextGenerationFirewallVirtualHubPanorama resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PaloAltoNextGenerationFirewallVirtualHubPanorama to import.
        :param import_from_id: The id of the existing PaloAltoNextGenerationFirewallVirtualHubPanorama that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PaloAltoNextGenerationFirewallVirtualHubPanorama to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f0231e819849bee60ece5da0533bc64a5452c84f49e25f7166de9bcb29fb067)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDestinationNat")
    def put_destination_nat(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNat", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6f59280fe73e388536dc2ade12148405efe1faf6b3984519d81b8fbc5c6b688)
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
        :param dns_servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#dns_servers PaloAltoNextGenerationFirewallVirtualHubPanorama#dns_servers}.
        :param use_azure_dns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#use_azure_dns PaloAltoNextGenerationFirewallVirtualHubPanorama#use_azure_dns}.
        '''
        value = PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettings(
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
        :param network_virtual_appliance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#network_virtual_appliance_id PaloAltoNextGenerationFirewallVirtualHubPanorama#network_virtual_appliance_id}.
        :param public_ip_address_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#public_ip_address_ids PaloAltoNextGenerationFirewallVirtualHubPanorama#public_ip_address_ids}.
        :param virtual_hub_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#virtual_hub_id PaloAltoNextGenerationFirewallVirtualHubPanorama#virtual_hub_id}.
        :param egress_nat_ip_address_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#egress_nat_ip_address_ids PaloAltoNextGenerationFirewallVirtualHubPanorama#egress_nat_ip_address_ids}.
        :param trusted_address_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#trusted_address_ranges PaloAltoNextGenerationFirewallVirtualHubPanorama#trusted_address_ranges}.
        '''
        value = PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfile(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#create PaloAltoNextGenerationFirewallVirtualHubPanorama#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#delete PaloAltoNextGenerationFirewallVirtualHubPanorama#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#read PaloAltoNextGenerationFirewallVirtualHubPanorama#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#update PaloAltoNextGenerationFirewallVirtualHubPanorama#update}.
        '''
        value = PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeouts(
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
    ) -> "PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatList":
        return typing.cast("PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatList", jsii.get(self, "destinationNat"))

    @builtins.property
    @jsii.member(jsii_name="dnsSettings")
    def dns_settings(
        self,
    ) -> "PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettingsOutputReference":
        return typing.cast("PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettingsOutputReference", jsii.get(self, "dnsSettings"))

    @builtins.property
    @jsii.member(jsii_name="networkProfile")
    def network_profile(
        self,
    ) -> "PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfileOutputReference":
        return typing.cast("PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfileOutputReference", jsii.get(self, "networkProfile"))

    @builtins.property
    @jsii.member(jsii_name="panorama")
    def panorama(
        self,
    ) -> "PaloAltoNextGenerationFirewallVirtualHubPanoramaPanoramaList":
        return typing.cast("PaloAltoNextGenerationFirewallVirtualHubPanoramaPanoramaList", jsii.get(self, "panorama"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeoutsOutputReference":
        return typing.cast("PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="destinationNatInput")
    def destination_nat_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNat"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNat"]]], jsii.get(self, "destinationNatInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsSettingsInput")
    def dns_settings_input(
        self,
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettings"]:
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettings"], jsii.get(self, "dnsSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

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
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfile"]:
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfile"], jsii.get(self, "networkProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="panoramaBase64ConfigInput")
    def panorama_base64_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "panoramaBase64ConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="planIdInput")
    def plan_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "planIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5dc655dd8063c0c27ba64204578b2950449d4cba4b012404b10e129e66ddacb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53553a672fa929486c7db2d5c7be675ec9abf79431f98654c9c6421b59ffa0b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="marketplaceOfferId")
    def marketplace_offer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "marketplaceOfferId"))

    @marketplace_offer_id.setter
    def marketplace_offer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5455e8f112c1029212e630464bdd1c31e864a45dd8ffc2ee3babb09503ee1e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "marketplaceOfferId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83e8af55a555c4dbec75cc3db6615c311301f7e229e13638f20852ecd73a4d34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="panoramaBase64Config")
    def panorama_base64_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "panoramaBase64Config"))

    @panorama_base64_config.setter
    def panorama_base64_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39dee80cd1ebdc71b9a81a0a45e8491a43f36d2743876bf4e6f37b4536f7aa7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "panoramaBase64Config", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="planId")
    def plan_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "planId"))

    @plan_id.setter
    def plan_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bc033f8047ccbe9c22f7a2e3de3f4cdf5ba45874c3290815ae6cb21ff1789dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "planId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc4be50ed9d704b3248fc5032102d0c1e74ac075106a10bc2237ba9fe081c025)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__612822ea8d51450aa6b3a5bc5a1f2a41981d5677f7b49294acf12ca50f441a3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubPanorama.PaloAltoNextGenerationFirewallVirtualHubPanoramaConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "network_profile": "networkProfile",
        "panorama_base64_config": "panoramaBase64Config",
        "resource_group_name": "resourceGroupName",
        "destination_nat": "destinationNat",
        "dns_settings": "dnsSettings",
        "id": "id",
        "marketplace_offer_id": "marketplaceOfferId",
        "plan_id": "planId",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class PaloAltoNextGenerationFirewallVirtualHubPanoramaConfig(
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
        location: builtins.str,
        name: builtins.str,
        network_profile: typing.Union["PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfile", typing.Dict[builtins.str, typing.Any]],
        panorama_base64_config: builtins.str,
        resource_group_name: builtins.str,
        destination_nat: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNat", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dns_settings: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        marketplace_offer_id: typing.Optional[builtins.str] = None,
        plan_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#location PaloAltoNextGenerationFirewallVirtualHubPanorama#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#name PaloAltoNextGenerationFirewallVirtualHubPanorama#name}.
        :param network_profile: network_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#network_profile PaloAltoNextGenerationFirewallVirtualHubPanorama#network_profile}
        :param panorama_base64_config: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#panorama_base64_config PaloAltoNextGenerationFirewallVirtualHubPanorama#panorama_base64_config}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#resource_group_name PaloAltoNextGenerationFirewallVirtualHubPanorama#resource_group_name}.
        :param destination_nat: destination_nat block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#destination_nat PaloAltoNextGenerationFirewallVirtualHubPanorama#destination_nat}
        :param dns_settings: dns_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#dns_settings PaloAltoNextGenerationFirewallVirtualHubPanorama#dns_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#id PaloAltoNextGenerationFirewallVirtualHubPanorama#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param marketplace_offer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#marketplace_offer_id PaloAltoNextGenerationFirewallVirtualHubPanorama#marketplace_offer_id}.
        :param plan_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#plan_id PaloAltoNextGenerationFirewallVirtualHubPanorama#plan_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#tags PaloAltoNextGenerationFirewallVirtualHubPanorama#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#timeouts PaloAltoNextGenerationFirewallVirtualHubPanorama#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(network_profile, dict):
            network_profile = PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfile(**network_profile)
        if isinstance(dns_settings, dict):
            dns_settings = PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettings(**dns_settings)
        if isinstance(timeouts, dict):
            timeouts = PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2526cf379bf7e9b308bb4b7813fd66719bca5a54e052ed8570d53d4f7f18bf40)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_profile", value=network_profile, expected_type=type_hints["network_profile"])
            check_type(argname="argument panorama_base64_config", value=panorama_base64_config, expected_type=type_hints["panorama_base64_config"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument destination_nat", value=destination_nat, expected_type=type_hints["destination_nat"])
            check_type(argname="argument dns_settings", value=dns_settings, expected_type=type_hints["dns_settings"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument marketplace_offer_id", value=marketplace_offer_id, expected_type=type_hints["marketplace_offer_id"])
            check_type(argname="argument plan_id", value=plan_id, expected_type=type_hints["plan_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "network_profile": network_profile,
            "panorama_base64_config": panorama_base64_config,
            "resource_group_name": resource_group_name,
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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#location PaloAltoNextGenerationFirewallVirtualHubPanorama#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#name PaloAltoNextGenerationFirewallVirtualHubPanorama#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_profile(
        self,
    ) -> "PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfile":
        '''network_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#network_profile PaloAltoNextGenerationFirewallVirtualHubPanorama#network_profile}
        '''
        result = self._values.get("network_profile")
        assert result is not None, "Required property 'network_profile' is missing"
        return typing.cast("PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfile", result)

    @builtins.property
    def panorama_base64_config(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#panorama_base64_config PaloAltoNextGenerationFirewallVirtualHubPanorama#panorama_base64_config}.'''
        result = self._values.get("panorama_base64_config")
        assert result is not None, "Required property 'panorama_base64_config' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#resource_group_name PaloAltoNextGenerationFirewallVirtualHubPanorama#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_nat(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNat"]]]:
        '''destination_nat block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#destination_nat PaloAltoNextGenerationFirewallVirtualHubPanorama#destination_nat}
        '''
        result = self._values.get("destination_nat")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNat"]]], result)

    @builtins.property
    def dns_settings(
        self,
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettings"]:
        '''dns_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#dns_settings PaloAltoNextGenerationFirewallVirtualHubPanorama#dns_settings}
        '''
        result = self._values.get("dns_settings")
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettings"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#id PaloAltoNextGenerationFirewallVirtualHubPanorama#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def marketplace_offer_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#marketplace_offer_id PaloAltoNextGenerationFirewallVirtualHubPanorama#marketplace_offer_id}.'''
        result = self._values.get("marketplace_offer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plan_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#plan_id PaloAltoNextGenerationFirewallVirtualHubPanorama#plan_id}.'''
        result = self._values.get("plan_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#tags PaloAltoNextGenerationFirewallVirtualHubPanorama#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#timeouts PaloAltoNextGenerationFirewallVirtualHubPanorama#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualHubPanoramaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubPanorama.PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNat",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "protocol": "protocol",
        "backend_config": "backendConfig",
        "frontend_config": "frontendConfig",
    },
)
class PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNat:
    def __init__(
        self,
        *,
        name: builtins.str,
        protocol: builtins.str,
        backend_config: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatBackendConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        frontend_config: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatFrontendConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#name PaloAltoNextGenerationFirewallVirtualHubPanorama#name}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#protocol PaloAltoNextGenerationFirewallVirtualHubPanorama#protocol}.
        :param backend_config: backend_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#backend_config PaloAltoNextGenerationFirewallVirtualHubPanorama#backend_config}
        :param frontend_config: frontend_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#frontend_config PaloAltoNextGenerationFirewallVirtualHubPanorama#frontend_config}
        '''
        if isinstance(backend_config, dict):
            backend_config = PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatBackendConfig(**backend_config)
        if isinstance(frontend_config, dict):
            frontend_config = PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatFrontendConfig(**frontend_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d50666fd4e893e7a0f4aa437bd999892981300df19629f665db63024182bf1a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#name PaloAltoNextGenerationFirewallVirtualHubPanorama#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#protocol PaloAltoNextGenerationFirewallVirtualHubPanorama#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backend_config(
        self,
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatBackendConfig"]:
        '''backend_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#backend_config PaloAltoNextGenerationFirewallVirtualHubPanorama#backend_config}
        '''
        result = self._values.get("backend_config")
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatBackendConfig"], result)

    @builtins.property
    def frontend_config(
        self,
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatFrontendConfig"]:
        '''frontend_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#frontend_config PaloAltoNextGenerationFirewallVirtualHubPanorama#frontend_config}
        '''
        result = self._values.get("frontend_config")
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatFrontendConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubPanorama.PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatBackendConfig",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "public_ip_address": "publicIpAddress"},
)
class PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatBackendConfig:
    def __init__(self, *, port: jsii.Number, public_ip_address: builtins.str) -> None:
        '''
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#port PaloAltoNextGenerationFirewallVirtualHubPanorama#port}.
        :param public_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#public_ip_address PaloAltoNextGenerationFirewallVirtualHubPanorama#public_ip_address}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e5876ea0e435a0d0d1f0e62c90a8b2452ee49bdd75a750c18bd7a62b466aaa9)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument public_ip_address", value=public_ip_address, expected_type=type_hints["public_ip_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
            "public_ip_address": public_ip_address,
        }

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#port PaloAltoNextGenerationFirewallVirtualHubPanorama#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def public_ip_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#public_ip_address PaloAltoNextGenerationFirewallVirtualHubPanorama#public_ip_address}.'''
        result = self._values.get("public_ip_address")
        assert result is not None, "Required property 'public_ip_address' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatBackendConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatBackendConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubPanorama.PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatBackendConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6eb3cd9b6f6867741c107a7c885bb600bbd9f3793f87ad38bc1464bb9fa1cbd0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff2db4643be14a92c3364d734c14b071f838213e3feb01a61de0f1b07f256aa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicIpAddress")
    def public_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIpAddress"))

    @public_ip_address.setter
    def public_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51154ce3e9e4c7be67f48bbbaa4f0200fcf6654f85181de8488e00272ad5f628)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatBackendConfig]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatBackendConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatBackendConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8ec5dd936ef7f91b311c3422645fdf148744f37d7b2d11255014898498897cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubPanorama.PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatFrontendConfig",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "public_ip_address_id": "publicIpAddressId"},
)
class PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatFrontendConfig:
    def __init__(
        self,
        *,
        port: jsii.Number,
        public_ip_address_id: builtins.str,
    ) -> None:
        '''
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#port PaloAltoNextGenerationFirewallVirtualHubPanorama#port}.
        :param public_ip_address_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#public_ip_address_id PaloAltoNextGenerationFirewallVirtualHubPanorama#public_ip_address_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd2898886c4cba418fa6a71121ce852bc99e20b2077cffd3a2053e5289e896b6)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument public_ip_address_id", value=public_ip_address_id, expected_type=type_hints["public_ip_address_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
            "public_ip_address_id": public_ip_address_id,
        }

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#port PaloAltoNextGenerationFirewallVirtualHubPanorama#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def public_ip_address_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#public_ip_address_id PaloAltoNextGenerationFirewallVirtualHubPanorama#public_ip_address_id}.'''
        result = self._values.get("public_ip_address_id")
        assert result is not None, "Required property 'public_ip_address_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatFrontendConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatFrontendConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubPanorama.PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatFrontendConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd2f8c53c08c34259cd3abb8fcb9117e6deea83352d384931f3b2801185f9d72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02c43e0e47ec7c22ead97350bd83caf2da75b5d5d50bcdc7672f429c332459b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicIpAddressId")
    def public_ip_address_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIpAddressId"))

    @public_ip_address_id.setter
    def public_ip_address_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0789743b007f76f6112d5d6321b420af15033f0fa031dedb4802dc889aaa9c1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpAddressId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatFrontendConfig]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatFrontendConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatFrontendConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebebccd218582d0d6a2e7cc1be59333df1101202ae4404589ec437763ec97f6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubPanorama.PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c273b3c58ec01b7da442f6c97cdff3ee73fc73818f29f130ab2682f587b4b4e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c09bf2ff38ec428372226513864bb44ad5e74097503e270175b53e71be6fca91)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b4634c15f1f92131f7f13c7462a28e780659d15eab5c81b93b674b52b5acc02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d99b5c718f58424f29c76f83d02ac40c116160c897328dbe85c5f09cce6c394)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c34be2e5fcf1558ad90c1de50a8ff27b70b8171e656ae210945a29f3b8f0d48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNat]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNat]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNat]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ac258cea64892b855c49aac68af113cc19e24302e1b86c7807f34d8347d50e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubPanorama.PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80ee409e0beef6f60c93c8585f11e6db6db0710e107b33dd80ccf21391aa3c8a)
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
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#port PaloAltoNextGenerationFirewallVirtualHubPanorama#port}.
        :param public_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#public_ip_address PaloAltoNextGenerationFirewallVirtualHubPanorama#public_ip_address}.
        '''
        value = PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatBackendConfig(
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
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#port PaloAltoNextGenerationFirewallVirtualHubPanorama#port}.
        :param public_ip_address_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#public_ip_address_id PaloAltoNextGenerationFirewallVirtualHubPanorama#public_ip_address_id}.
        '''
        value = PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatFrontendConfig(
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
    ) -> PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatBackendConfigOutputReference:
        return typing.cast(PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatBackendConfigOutputReference, jsii.get(self, "backendConfig"))

    @builtins.property
    @jsii.member(jsii_name="frontendConfig")
    def frontend_config(
        self,
    ) -> PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatFrontendConfigOutputReference:
        return typing.cast(PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatFrontendConfigOutputReference, jsii.get(self, "frontendConfig"))

    @builtins.property
    @jsii.member(jsii_name="backendConfigInput")
    def backend_config_input(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatBackendConfig]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatBackendConfig], jsii.get(self, "backendConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="frontendConfigInput")
    def frontend_config_input(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatFrontendConfig]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatFrontendConfig], jsii.get(self, "frontendConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1b616eaab3c1d4ce13bcea52a3f2d4955d8446c9f68e32ce7afab8f853b8cff6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e880e01f07e8db66a8f177422e7c3d7af2609ddc40127d84c091c4792098a0eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNat]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNat]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNat]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ade7d3b48ba4696d87f555564111fedf8d85cfb3cb6dba2b0ee3f6455432bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubPanorama.PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettings",
    jsii_struct_bases=[],
    name_mapping={"dns_servers": "dnsServers", "use_azure_dns": "useAzureDns"},
)
class PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettings:
    def __init__(
        self,
        *,
        dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        use_azure_dns: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param dns_servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#dns_servers PaloAltoNextGenerationFirewallVirtualHubPanorama#dns_servers}.
        :param use_azure_dns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#use_azure_dns PaloAltoNextGenerationFirewallVirtualHubPanorama#use_azure_dns}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1811650ed50cefbcdabe9fa2c13239d9fd2fe878335270c7257888ccd7d29b50)
            check_type(argname="argument dns_servers", value=dns_servers, expected_type=type_hints["dns_servers"])
            check_type(argname="argument use_azure_dns", value=use_azure_dns, expected_type=type_hints["use_azure_dns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dns_servers is not None:
            self._values["dns_servers"] = dns_servers
        if use_azure_dns is not None:
            self._values["use_azure_dns"] = use_azure_dns

    @builtins.property
    def dns_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#dns_servers PaloAltoNextGenerationFirewallVirtualHubPanorama#dns_servers}.'''
        result = self._values.get("dns_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def use_azure_dns(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#use_azure_dns PaloAltoNextGenerationFirewallVirtualHubPanorama#use_azure_dns}.'''
        result = self._values.get("use_azure_dns")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubPanorama.PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b02304254411d819d4d44e19f810010dff7b888341a2acd87321116305031c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb98b99718cb6595a886d6fdb0a1132df8d71c6f8ec1a5fe95e5aef2af989ec7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f03843a6b76b15bb5e06b23c713e08a8a0e0f21c86e472db9999e817f9092a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useAzureDns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettings]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bf5ee83357c5aebaf185201ce6907db7b6f18fc483a54c7bbdb613693789ec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubPanorama.PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfile",
    jsii_struct_bases=[],
    name_mapping={
        "network_virtual_appliance_id": "networkVirtualApplianceId",
        "public_ip_address_ids": "publicIpAddressIds",
        "virtual_hub_id": "virtualHubId",
        "egress_nat_ip_address_ids": "egressNatIpAddressIds",
        "trusted_address_ranges": "trustedAddressRanges",
    },
)
class PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfile:
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
        :param network_virtual_appliance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#network_virtual_appliance_id PaloAltoNextGenerationFirewallVirtualHubPanorama#network_virtual_appliance_id}.
        :param public_ip_address_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#public_ip_address_ids PaloAltoNextGenerationFirewallVirtualHubPanorama#public_ip_address_ids}.
        :param virtual_hub_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#virtual_hub_id PaloAltoNextGenerationFirewallVirtualHubPanorama#virtual_hub_id}.
        :param egress_nat_ip_address_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#egress_nat_ip_address_ids PaloAltoNextGenerationFirewallVirtualHubPanorama#egress_nat_ip_address_ids}.
        :param trusted_address_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#trusted_address_ranges PaloAltoNextGenerationFirewallVirtualHubPanorama#trusted_address_ranges}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb84056cd2df0814131d15d5969d9fe9b961edeecaf2aa81194841f60477b1be)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#network_virtual_appliance_id PaloAltoNextGenerationFirewallVirtualHubPanorama#network_virtual_appliance_id}.'''
        result = self._values.get("network_virtual_appliance_id")
        assert result is not None, "Required property 'network_virtual_appliance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def public_ip_address_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#public_ip_address_ids PaloAltoNextGenerationFirewallVirtualHubPanorama#public_ip_address_ids}.'''
        result = self._values.get("public_ip_address_ids")
        assert result is not None, "Required property 'public_ip_address_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def virtual_hub_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#virtual_hub_id PaloAltoNextGenerationFirewallVirtualHubPanorama#virtual_hub_id}.'''
        result = self._values.get("virtual_hub_id")
        assert result is not None, "Required property 'virtual_hub_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def egress_nat_ip_address_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#egress_nat_ip_address_ids PaloAltoNextGenerationFirewallVirtualHubPanorama#egress_nat_ip_address_ids}.'''
        result = self._values.get("egress_nat_ip_address_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def trusted_address_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#trusted_address_ranges PaloAltoNextGenerationFirewallVirtualHubPanorama#trusted_address_ranges}.'''
        result = self._values.get("trusted_address_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubPanorama.PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7bea5e766658dd0a9c0d4a074628ed7bfd4adeeeffd00c2df3dd75a97cd513a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f10f2ec03df2fa693f4cb4dad6ec4fbf16e2f846e7c9bd58c6af1ca9824f23b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "egressNatIpAddressIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkVirtualApplianceId")
    def network_virtual_appliance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkVirtualApplianceId"))

    @network_virtual_appliance_id.setter
    def network_virtual_appliance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0defc6663c41f4491555b97ef526f7f9c576e349af1cb0da31670bcdef6cf96d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkVirtualApplianceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicIpAddressIds")
    def public_ip_address_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "publicIpAddressIds"))

    @public_ip_address_ids.setter
    def public_ip_address_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01732ef57536723d0f50975d705966de943f2ccc88ab3255379460f81302da64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpAddressIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustedAddressRanges")
    def trusted_address_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "trustedAddressRanges"))

    @trusted_address_ranges.setter
    def trusted_address_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75d3f7d2c7a278342a47d45f4e3486fe96de917d0166efb2dd7b83543ea96570)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustedAddressRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualHubId")
    def virtual_hub_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualHubId"))

    @virtual_hub_id.setter
    def virtual_hub_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51538ccbaa6123dd496bcd4f6b7825971982c6aada41d04c5054ef560e06a9d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualHubId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfile]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb225be781920f2d28ff26e3561101b6f7c22bb1a8f9c13effb8907efabb344)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubPanorama.PaloAltoNextGenerationFirewallVirtualHubPanoramaPanorama",
    jsii_struct_bases=[],
    name_mapping={},
)
class PaloAltoNextGenerationFirewallVirtualHubPanoramaPanorama:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualHubPanoramaPanorama(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualHubPanoramaPanoramaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubPanorama.PaloAltoNextGenerationFirewallVirtualHubPanoramaPanoramaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d80577d1a84216f04281bedae05447dc83d7676d55637e0925451f1e0b7b9416)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PaloAltoNextGenerationFirewallVirtualHubPanoramaPanoramaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__166ef769efa940c93b04d0f4286f2522c27cb54fc42a04d8982b69d41f7467b4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PaloAltoNextGenerationFirewallVirtualHubPanoramaPanoramaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca58c28f09a1bcace2a0ae2e953c28f1d0b27aeb81f63ae9916712d4fbdd821)
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
            type_hints = typing.get_type_hints(_typecheckingstub__188c07bc6836923f5b0cbf8db9cd1a0f0d7886a5a665da17e8a78093981ee056)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b58da9408a04f5ed84de71a6ed8446c2b07208aa9116b9e535d698358fb9e05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class PaloAltoNextGenerationFirewallVirtualHubPanoramaPanoramaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubPanorama.PaloAltoNextGenerationFirewallVirtualHubPanoramaPanoramaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d3b2202db62392f93307bcd19de38cc2cb563052d90b170d1248d7c5756f74c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="deviceGroupName")
    def device_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceGroupName"))

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="panoramaServer1")
    def panorama_server1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "panoramaServer1"))

    @builtins.property
    @jsii.member(jsii_name="panoramaServer2")
    def panorama_server2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "panoramaServer2"))

    @builtins.property
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "templateName"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineSshKey")
    def virtual_machine_ssh_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualMachineSshKey"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaPanorama]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaPanorama], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaPanorama],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06240f2ba1227f152cbffc4da338613a1ffc244eb98303219f7514ffa1566d3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubPanorama.PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#create PaloAltoNextGenerationFirewallVirtualHubPanorama#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#delete PaloAltoNextGenerationFirewallVirtualHubPanorama#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#read PaloAltoNextGenerationFirewallVirtualHubPanorama#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#update PaloAltoNextGenerationFirewallVirtualHubPanorama#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__404bdbf53fbf512ab37e61a7438bd6d4d2c1b4f2e1f478b0c980b2d794f954bb)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#create PaloAltoNextGenerationFirewallVirtualHubPanorama#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#delete PaloAltoNextGenerationFirewallVirtualHubPanorama#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#read PaloAltoNextGenerationFirewallVirtualHubPanorama#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_hub_panorama#update PaloAltoNextGenerationFirewallVirtualHubPanorama#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualHubPanorama.PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1b515846e9ab7cdff38a48c9d1fc4407fc25a797d312c82a142c1783d9a244a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8be7162dd8636393fa95b90f1097a561fb445c8db97b630149d48df2e688006)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30e3a9bff285aa186929cc6441d4445fac765e4d1b6e8cbf323ca8b4b7a9b586)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c76fb1d249ea14feee21909d4395bf207cf832a71b6590b51e3d1d5457d07e60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8171c558868e8f3067d4330783461169a5114b7f1ad3f0762439e1417768963a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a9ec2fc5286b79d02c253bead66ad2aeaa0500c807aea02b8978f03cedb171d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "PaloAltoNextGenerationFirewallVirtualHubPanorama",
    "PaloAltoNextGenerationFirewallVirtualHubPanoramaConfig",
    "PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNat",
    "PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatBackendConfig",
    "PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatBackendConfigOutputReference",
    "PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatFrontendConfig",
    "PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatFrontendConfigOutputReference",
    "PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatList",
    "PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatOutputReference",
    "PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettings",
    "PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettingsOutputReference",
    "PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfile",
    "PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfileOutputReference",
    "PaloAltoNextGenerationFirewallVirtualHubPanoramaPanorama",
    "PaloAltoNextGenerationFirewallVirtualHubPanoramaPanoramaList",
    "PaloAltoNextGenerationFirewallVirtualHubPanoramaPanoramaOutputReference",
    "PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeouts",
    "PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__2081c298f262c74e27b286ee0f1adf628f9c840dca85afd93eb0111a44151643(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    network_profile: typing.Union[PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfile, typing.Dict[builtins.str, typing.Any]],
    panorama_base64_config: builtins.str,
    resource_group_name: builtins.str,
    destination_nat: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNat, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns_settings: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    marketplace_offer_id: typing.Optional[builtins.str] = None,
    plan_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8f0231e819849bee60ece5da0533bc64a5452c84f49e25f7166de9bcb29fb067(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f59280fe73e388536dc2ade12148405efe1faf6b3984519d81b8fbc5c6b688(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNat, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5dc655dd8063c0c27ba64204578b2950449d4cba4b012404b10e129e66ddacb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53553a672fa929486c7db2d5c7be675ec9abf79431f98654c9c6421b59ffa0b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5455e8f112c1029212e630464bdd1c31e864a45dd8ffc2ee3babb09503ee1e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e8af55a555c4dbec75cc3db6615c311301f7e229e13638f20852ecd73a4d34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39dee80cd1ebdc71b9a81a0a45e8491a43f36d2743876bf4e6f37b4536f7aa7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bc033f8047ccbe9c22f7a2e3de3f4cdf5ba45874c3290815ae6cb21ff1789dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc4be50ed9d704b3248fc5032102d0c1e74ac075106a10bc2237ba9fe081c025(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__612822ea8d51450aa6b3a5bc5a1f2a41981d5677f7b49294acf12ca50f441a3d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2526cf379bf7e9b308bb4b7813fd66719bca5a54e052ed8570d53d4f7f18bf40(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    network_profile: typing.Union[PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfile, typing.Dict[builtins.str, typing.Any]],
    panorama_base64_config: builtins.str,
    resource_group_name: builtins.str,
    destination_nat: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNat, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns_settings: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    marketplace_offer_id: typing.Optional[builtins.str] = None,
    plan_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d50666fd4e893e7a0f4aa437bd999892981300df19629f665db63024182bf1a(
    *,
    name: builtins.str,
    protocol: builtins.str,
    backend_config: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatBackendConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    frontend_config: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatFrontendConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5876ea0e435a0d0d1f0e62c90a8b2452ee49bdd75a750c18bd7a62b466aaa9(
    *,
    port: jsii.Number,
    public_ip_address: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eb3cd9b6f6867741c107a7c885bb600bbd9f3793f87ad38bc1464bb9fa1cbd0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff2db4643be14a92c3364d734c14b071f838213e3feb01a61de0f1b07f256aa4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51154ce3e9e4c7be67f48bbbaa4f0200fcf6654f85181de8488e00272ad5f628(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8ec5dd936ef7f91b311c3422645fdf148744f37d7b2d11255014898498897cb(
    value: typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatBackendConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2898886c4cba418fa6a71121ce852bc99e20b2077cffd3a2053e5289e896b6(
    *,
    port: jsii.Number,
    public_ip_address_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2f8c53c08c34259cd3abb8fcb9117e6deea83352d384931f3b2801185f9d72(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c43e0e47ec7c22ead97350bd83caf2da75b5d5d50bcdc7672f429c332459b3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0789743b007f76f6112d5d6321b420af15033f0fa031dedb4802dc889aaa9c1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebebccd218582d0d6a2e7cc1be59333df1101202ae4404589ec437763ec97f6e(
    value: typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNatFrontendConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c273b3c58ec01b7da442f6c97cdff3ee73fc73818f29f130ab2682f587b4b4e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c09bf2ff38ec428372226513864bb44ad5e74097503e270175b53e71be6fca91(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b4634c15f1f92131f7f13c7462a28e780659d15eab5c81b93b674b52b5acc02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d99b5c718f58424f29c76f83d02ac40c116160c897328dbe85c5f09cce6c394(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c34be2e5fcf1558ad90c1de50a8ff27b70b8171e656ae210945a29f3b8f0d48(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac258cea64892b855c49aac68af113cc19e24302e1b86c7807f34d8347d50e7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNat]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80ee409e0beef6f60c93c8585f11e6db6db0710e107b33dd80ccf21391aa3c8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b616eaab3c1d4ce13bcea52a3f2d4955d8446c9f68e32ce7afab8f853b8cff6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e880e01f07e8db66a8f177422e7c3d7af2609ddc40127d84c091c4792098a0eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ade7d3b48ba4696d87f555564111fedf8d85cfb3cb6dba2b0ee3f6455432bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualHubPanoramaDestinationNat]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1811650ed50cefbcdabe9fa2c13239d9fd2fe878335270c7257888ccd7d29b50(
    *,
    dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    use_azure_dns: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b02304254411d819d4d44e19f810010dff7b888341a2acd87321116305031c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb98b99718cb6595a886d6fdb0a1132df8d71c6f8ec1a5fe95e5aef2af989ec7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f03843a6b76b15bb5e06b23c713e08a8a0e0f21c86e472db9999e817f9092a3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bf5ee83357c5aebaf185201ce6907db7b6f18fc483a54c7bbdb613693789ec7(
    value: typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaDnsSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb84056cd2df0814131d15d5969d9fe9b961edeecaf2aa81194841f60477b1be(
    *,
    network_virtual_appliance_id: builtins.str,
    public_ip_address_ids: typing.Sequence[builtins.str],
    virtual_hub_id: builtins.str,
    egress_nat_ip_address_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    trusted_address_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7bea5e766658dd0a9c0d4a074628ed7bfd4adeeeffd00c2df3dd75a97cd513a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f10f2ec03df2fa693f4cb4dad6ec4fbf16e2f846e7c9bd58c6af1ca9824f23b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0defc6663c41f4491555b97ef526f7f9c576e349af1cb0da31670bcdef6cf96d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01732ef57536723d0f50975d705966de943f2ccc88ab3255379460f81302da64(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d3f7d2c7a278342a47d45f4e3486fe96de917d0166efb2dd7b83543ea96570(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51538ccbaa6123dd496bcd4f6b7825971982c6aada41d04c5054ef560e06a9d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb225be781920f2d28ff26e3561101b6f7c22bb1a8f9c13effb8907efabb344(
    value: typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaNetworkProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d80577d1a84216f04281bedae05447dc83d7676d55637e0925451f1e0b7b9416(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__166ef769efa940c93b04d0f4286f2522c27cb54fc42a04d8982b69d41f7467b4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca58c28f09a1bcace2a0ae2e953c28f1d0b27aeb81f63ae9916712d4fbdd821(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__188c07bc6836923f5b0cbf8db9cd1a0f0d7886a5a665da17e8a78093981ee056(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b58da9408a04f5ed84de71a6ed8446c2b07208aa9116b9e535d698358fb9e05(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d3b2202db62392f93307bcd19de38cc2cb563052d90b170d1248d7c5756f74c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06240f2ba1227f152cbffc4da338613a1ffc244eb98303219f7514ffa1566d3b(
    value: typing.Optional[PaloAltoNextGenerationFirewallVirtualHubPanoramaPanorama],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__404bdbf53fbf512ab37e61a7438bd6d4d2c1b4f2e1f478b0c980b2d794f954bb(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1b515846e9ab7cdff38a48c9d1fc4407fc25a797d312c82a142c1783d9a244a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8be7162dd8636393fa95b90f1097a561fb445c8db97b630149d48df2e688006(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e3a9bff285aa186929cc6441d4445fac765e4d1b6e8cbf323ca8b4b7a9b586(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c76fb1d249ea14feee21909d4395bf207cf832a71b6590b51e3d1d5457d07e60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8171c558868e8f3067d4330783461169a5114b7f1ad3f0762439e1417768963a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9ec2fc5286b79d02c253bead66ad2aeaa0500c807aea02b8978f03cedb171d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualHubPanoramaTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
