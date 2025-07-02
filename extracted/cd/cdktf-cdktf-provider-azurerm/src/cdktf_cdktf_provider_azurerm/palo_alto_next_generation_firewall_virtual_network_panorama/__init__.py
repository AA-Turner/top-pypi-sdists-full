r'''
# `azurerm_palo_alto_next_generation_firewall_virtual_network_panorama`

Refer to the Terraform Registry for docs: [`azurerm_palo_alto_next_generation_firewall_virtual_network_panorama`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama).
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


class PaloAltoNextGenerationFirewallVirtualNetworkPanorama(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkPanorama.PaloAltoNextGenerationFirewallVirtualNetworkPanorama",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama azurerm_palo_alto_next_generation_firewall_virtual_network_panorama}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        network_profile: typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfile", typing.Dict[builtins.str, typing.Any]],
        panorama_base64_config: builtins.str,
        resource_group_name: builtins.str,
        destination_nat: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNat", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dns_settings: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        marketplace_offer_id: typing.Optional[builtins.str] = None,
        plan_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama azurerm_palo_alto_next_generation_firewall_virtual_network_panorama} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#location PaloAltoNextGenerationFirewallVirtualNetworkPanorama#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#name PaloAltoNextGenerationFirewallVirtualNetworkPanorama#name}.
        :param network_profile: network_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#network_profile PaloAltoNextGenerationFirewallVirtualNetworkPanorama#network_profile}
        :param panorama_base64_config: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#panorama_base64_config PaloAltoNextGenerationFirewallVirtualNetworkPanorama#panorama_base64_config}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#resource_group_name PaloAltoNextGenerationFirewallVirtualNetworkPanorama#resource_group_name}.
        :param destination_nat: destination_nat block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#destination_nat PaloAltoNextGenerationFirewallVirtualNetworkPanorama#destination_nat}
        :param dns_settings: dns_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#dns_settings PaloAltoNextGenerationFirewallVirtualNetworkPanorama#dns_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#id PaloAltoNextGenerationFirewallVirtualNetworkPanorama#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param marketplace_offer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#marketplace_offer_id PaloAltoNextGenerationFirewallVirtualNetworkPanorama#marketplace_offer_id}.
        :param plan_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#plan_id PaloAltoNextGenerationFirewallVirtualNetworkPanorama#plan_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#tags PaloAltoNextGenerationFirewallVirtualNetworkPanorama#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#timeouts PaloAltoNextGenerationFirewallVirtualNetworkPanorama#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__051b444f0f6f9f5c9826bfa7c9cf24c4af288d638f69efc5b415df56e6de0aac)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PaloAltoNextGenerationFirewallVirtualNetworkPanoramaConfig(
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
        '''Generates CDKTF code for importing a PaloAltoNextGenerationFirewallVirtualNetworkPanorama resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PaloAltoNextGenerationFirewallVirtualNetworkPanorama to import.
        :param import_from_id: The id of the existing PaloAltoNextGenerationFirewallVirtualNetworkPanorama that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PaloAltoNextGenerationFirewallVirtualNetworkPanorama to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99a2ae44e8acdf748eb784085fd237412be4e345e47e9c282ed4279e667cae75)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDestinationNat")
    def put_destination_nat(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNat", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0b5eb636868263eb0e0026ddaacbd03ecf7cdfb868683f983ce9cf3b1698129)
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
        :param dns_servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#dns_servers PaloAltoNextGenerationFirewallVirtualNetworkPanorama#dns_servers}.
        :param use_azure_dns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#use_azure_dns PaloAltoNextGenerationFirewallVirtualNetworkPanorama#use_azure_dns}.
        '''
        value = PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettings(
            dns_servers=dns_servers, use_azure_dns=use_azure_dns
        )

        return typing.cast(None, jsii.invoke(self, "putDnsSettings", [value]))

    @jsii.member(jsii_name="putNetworkProfile")
    def put_network_profile(
        self,
        *,
        public_ip_address_ids: typing.Sequence[builtins.str],
        vnet_configuration: typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileVnetConfiguration", typing.Dict[builtins.str, typing.Any]],
        egress_nat_ip_address_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        trusted_address_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param public_ip_address_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#public_ip_address_ids PaloAltoNextGenerationFirewallVirtualNetworkPanorama#public_ip_address_ids}.
        :param vnet_configuration: vnet_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#vnet_configuration PaloAltoNextGenerationFirewallVirtualNetworkPanorama#vnet_configuration}
        :param egress_nat_ip_address_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#egress_nat_ip_address_ids PaloAltoNextGenerationFirewallVirtualNetworkPanorama#egress_nat_ip_address_ids}.
        :param trusted_address_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#trusted_address_ranges PaloAltoNextGenerationFirewallVirtualNetworkPanorama#trusted_address_ranges}.
        '''
        value = PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfile(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#create PaloAltoNextGenerationFirewallVirtualNetworkPanorama#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#delete PaloAltoNextGenerationFirewallVirtualNetworkPanorama#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#read PaloAltoNextGenerationFirewallVirtualNetworkPanorama#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#update PaloAltoNextGenerationFirewallVirtualNetworkPanorama#update}.
        '''
        value = PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeouts(
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
    ) -> "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatList":
        return typing.cast("PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatList", jsii.get(self, "destinationNat"))

    @builtins.property
    @jsii.member(jsii_name="dnsSettings")
    def dns_settings(
        self,
    ) -> "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettingsOutputReference":
        return typing.cast("PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettingsOutputReference", jsii.get(self, "dnsSettings"))

    @builtins.property
    @jsii.member(jsii_name="networkProfile")
    def network_profile(
        self,
    ) -> "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileOutputReference":
        return typing.cast("PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileOutputReference", jsii.get(self, "networkProfile"))

    @builtins.property
    @jsii.member(jsii_name="panorama")
    def panorama(
        self,
    ) -> "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaPanoramaList":
        return typing.cast("PaloAltoNextGenerationFirewallVirtualNetworkPanoramaPanoramaList", jsii.get(self, "panorama"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeoutsOutputReference":
        return typing.cast("PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="destinationNatInput")
    def destination_nat_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNat"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNat"]]], jsii.get(self, "destinationNatInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsSettingsInput")
    def dns_settings_input(
        self,
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettings"]:
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettings"], jsii.get(self, "dnsSettingsInput"))

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
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfile"]:
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfile"], jsii.get(self, "networkProfileInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5efff977a4d1f69b21972132494acc0ae2c6ce9aa0624e6da4962b67e9535eeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceab16b5c9b49564799a30184423ca70791b82d72d2299951d2d59dd33e74b81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="marketplaceOfferId")
    def marketplace_offer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "marketplaceOfferId"))

    @marketplace_offer_id.setter
    def marketplace_offer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1588894ef15455db83ce1e17487bfc9b2c24b52f344bcfeca21d8427648431b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "marketplaceOfferId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39a13af17b5d6c4033d93109e4a0cdbc71e00823f9ed74a230dd18b15391b983)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="panoramaBase64Config")
    def panorama_base64_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "panoramaBase64Config"))

    @panorama_base64_config.setter
    def panorama_base64_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f61010ae5a269bd5452e80a6ea26be80c5830c5ba4acf44d788263c28f5b56ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "panoramaBase64Config", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="planId")
    def plan_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "planId"))

    @plan_id.setter
    def plan_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93cc90f78fbe14347c29b2e5ba7d4505d95bd52c53c3e46b4005928fe1160a0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "planId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a56e6c3750b951b5db80ce82d7c8b6e235dbedc74162e998352a380fc60966c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be3770276eec24a0a305ebb20024db0db9cb83e9d337ffb99bb1851406385b31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkPanorama.PaloAltoNextGenerationFirewallVirtualNetworkPanoramaConfig",
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
class PaloAltoNextGenerationFirewallVirtualNetworkPanoramaConfig(
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
        network_profile: typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfile", typing.Dict[builtins.str, typing.Any]],
        panorama_base64_config: builtins.str,
        resource_group_name: builtins.str,
        destination_nat: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNat", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dns_settings: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        marketplace_offer_id: typing.Optional[builtins.str] = None,
        plan_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#location PaloAltoNextGenerationFirewallVirtualNetworkPanorama#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#name PaloAltoNextGenerationFirewallVirtualNetworkPanorama#name}.
        :param network_profile: network_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#network_profile PaloAltoNextGenerationFirewallVirtualNetworkPanorama#network_profile}
        :param panorama_base64_config: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#panorama_base64_config PaloAltoNextGenerationFirewallVirtualNetworkPanorama#panorama_base64_config}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#resource_group_name PaloAltoNextGenerationFirewallVirtualNetworkPanorama#resource_group_name}.
        :param destination_nat: destination_nat block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#destination_nat PaloAltoNextGenerationFirewallVirtualNetworkPanorama#destination_nat}
        :param dns_settings: dns_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#dns_settings PaloAltoNextGenerationFirewallVirtualNetworkPanorama#dns_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#id PaloAltoNextGenerationFirewallVirtualNetworkPanorama#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param marketplace_offer_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#marketplace_offer_id PaloAltoNextGenerationFirewallVirtualNetworkPanorama#marketplace_offer_id}.
        :param plan_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#plan_id PaloAltoNextGenerationFirewallVirtualNetworkPanorama#plan_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#tags PaloAltoNextGenerationFirewallVirtualNetworkPanorama#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#timeouts PaloAltoNextGenerationFirewallVirtualNetworkPanorama#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(network_profile, dict):
            network_profile = PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfile(**network_profile)
        if isinstance(dns_settings, dict):
            dns_settings = PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettings(**dns_settings)
        if isinstance(timeouts, dict):
            timeouts = PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__114305e1bdd0576e774f48e00d25fcee42fac761b6f4ed9fd79f88ca954d02b6)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#location PaloAltoNextGenerationFirewallVirtualNetworkPanorama#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#name PaloAltoNextGenerationFirewallVirtualNetworkPanorama#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_profile(
        self,
    ) -> "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfile":
        '''network_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#network_profile PaloAltoNextGenerationFirewallVirtualNetworkPanorama#network_profile}
        '''
        result = self._values.get("network_profile")
        assert result is not None, "Required property 'network_profile' is missing"
        return typing.cast("PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfile", result)

    @builtins.property
    def panorama_base64_config(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#panorama_base64_config PaloAltoNextGenerationFirewallVirtualNetworkPanorama#panorama_base64_config}.'''
        result = self._values.get("panorama_base64_config")
        assert result is not None, "Required property 'panorama_base64_config' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#resource_group_name PaloAltoNextGenerationFirewallVirtualNetworkPanorama#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_nat(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNat"]]]:
        '''destination_nat block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#destination_nat PaloAltoNextGenerationFirewallVirtualNetworkPanorama#destination_nat}
        '''
        result = self._values.get("destination_nat")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNat"]]], result)

    @builtins.property
    def dns_settings(
        self,
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettings"]:
        '''dns_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#dns_settings PaloAltoNextGenerationFirewallVirtualNetworkPanorama#dns_settings}
        '''
        result = self._values.get("dns_settings")
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettings"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#id PaloAltoNextGenerationFirewallVirtualNetworkPanorama#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def marketplace_offer_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#marketplace_offer_id PaloAltoNextGenerationFirewallVirtualNetworkPanorama#marketplace_offer_id}.'''
        result = self._values.get("marketplace_offer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plan_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#plan_id PaloAltoNextGenerationFirewallVirtualNetworkPanorama#plan_id}.'''
        result = self._values.get("plan_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#tags PaloAltoNextGenerationFirewallVirtualNetworkPanorama#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#timeouts PaloAltoNextGenerationFirewallVirtualNetworkPanorama#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkPanorama.PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNat",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "protocol": "protocol",
        "backend_config": "backendConfig",
        "frontend_config": "frontendConfig",
    },
)
class PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNat:
    def __init__(
        self,
        *,
        name: builtins.str,
        protocol: builtins.str,
        backend_config: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatBackendConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        frontend_config: typing.Optional[typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatFrontendConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#name PaloAltoNextGenerationFirewallVirtualNetworkPanorama#name}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#protocol PaloAltoNextGenerationFirewallVirtualNetworkPanorama#protocol}.
        :param backend_config: backend_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#backend_config PaloAltoNextGenerationFirewallVirtualNetworkPanorama#backend_config}
        :param frontend_config: frontend_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#frontend_config PaloAltoNextGenerationFirewallVirtualNetworkPanorama#frontend_config}
        '''
        if isinstance(backend_config, dict):
            backend_config = PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatBackendConfig(**backend_config)
        if isinstance(frontend_config, dict):
            frontend_config = PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatFrontendConfig(**frontend_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6402097bee711d2140ac8a6283511cf53085dc0e576001806287aa004d52afd6)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#name PaloAltoNextGenerationFirewallVirtualNetworkPanorama#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#protocol PaloAltoNextGenerationFirewallVirtualNetworkPanorama#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backend_config(
        self,
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatBackendConfig"]:
        '''backend_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#backend_config PaloAltoNextGenerationFirewallVirtualNetworkPanorama#backend_config}
        '''
        result = self._values.get("backend_config")
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatBackendConfig"], result)

    @builtins.property
    def frontend_config(
        self,
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatFrontendConfig"]:
        '''frontend_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#frontend_config PaloAltoNextGenerationFirewallVirtualNetworkPanorama#frontend_config}
        '''
        result = self._values.get("frontend_config")
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatFrontendConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkPanorama.PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatBackendConfig",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "public_ip_address": "publicIpAddress"},
)
class PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatBackendConfig:
    def __init__(self, *, port: jsii.Number, public_ip_address: builtins.str) -> None:
        '''
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#port PaloAltoNextGenerationFirewallVirtualNetworkPanorama#port}.
        :param public_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#public_ip_address PaloAltoNextGenerationFirewallVirtualNetworkPanorama#public_ip_address}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1768ab12983a3c1ee26022a05b0ceb64ae69b5673c2af85099ac4a7e58ef4c)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument public_ip_address", value=public_ip_address, expected_type=type_hints["public_ip_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
            "public_ip_address": public_ip_address,
        }

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#port PaloAltoNextGenerationFirewallVirtualNetworkPanorama#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def public_ip_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#public_ip_address PaloAltoNextGenerationFirewallVirtualNetworkPanorama#public_ip_address}.'''
        result = self._values.get("public_ip_address")
        assert result is not None, "Required property 'public_ip_address' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatBackendConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatBackendConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkPanorama.PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatBackendConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__381f0549a502c386ce55e6ba38f83cb5f9e65a4b7003139868c41b2e2804282a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__411b82c86aa46cdcb6773680223924acbfa7046d42a689c57d1a42eed6534837)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicIpAddress")
    def public_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIpAddress"))

    @public_ip_address.setter
    def public_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff6b52c6cce0919b37e8aed5c882d066cd245e374bdb65671c664b0f0146b229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatBackendConfig]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatBackendConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatBackendConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46205aba7b5858b8893a3deb4f4dadef2b8b5a3ab42605c7c9c8d0b4fda741b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkPanorama.PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatFrontendConfig",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "public_ip_address_id": "publicIpAddressId"},
)
class PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatFrontendConfig:
    def __init__(
        self,
        *,
        port: jsii.Number,
        public_ip_address_id: builtins.str,
    ) -> None:
        '''
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#port PaloAltoNextGenerationFirewallVirtualNetworkPanorama#port}.
        :param public_ip_address_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#public_ip_address_id PaloAltoNextGenerationFirewallVirtualNetworkPanorama#public_ip_address_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44096152ad249a0d2f0076acab099534d4db2a6fb48ecd9197716765f26617bb)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument public_ip_address_id", value=public_ip_address_id, expected_type=type_hints["public_ip_address_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
            "public_ip_address_id": public_ip_address_id,
        }

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#port PaloAltoNextGenerationFirewallVirtualNetworkPanorama#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def public_ip_address_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#public_ip_address_id PaloAltoNextGenerationFirewallVirtualNetworkPanorama#public_ip_address_id}.'''
        result = self._values.get("public_ip_address_id")
        assert result is not None, "Required property 'public_ip_address_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatFrontendConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatFrontendConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkPanorama.PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatFrontendConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__311b880eb8aace9afaf196a77ee98572a1761dc6d1eeeac716cd2216a8d18634)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdec2ab8002780f51dfbda3ab3ac744b1454426a620b5906e682645fcb349f49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicIpAddressId")
    def public_ip_address_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIpAddressId"))

    @public_ip_address_id.setter
    def public_ip_address_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fe53c40ce2bde99b64a313efb86a2a601ccc9eb1a41298f8686fbbc6dcaf6ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpAddressId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatFrontendConfig]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatFrontendConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatFrontendConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dedf3093e4204e727eebf76a53d6f713cf39a89afa17cee0ac4f0643ae0dc0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkPanorama.PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca949186b2dac57169e8415e34a14b6c323d8ae2b793417d91e5f8325ea4e9aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d62fc134b5a600d1d176a5cb4469d4f402858e8b8f089cb92a2ef32cae1dd86e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6000837bd11520c2cfe84a820207146d4a5b86f40d6ccb3a707ab5121268cdc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f8cd9a0c8833579145554682274fe5b018ad3e13b70acf733a75199ec4549e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d769657627ab42aa9715a53188cb4c5a940455026d2fbc3bbfae1fc288b68c28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNat]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNat]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNat]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc2aa92ae86d9fab14e9c69c14847dcdfc9a42c401c42ba878ee9438767c3a35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkPanorama.PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__256ae0e06ceb0d761651b9343faf9d883a09fcfee8ea798f930b0e28ac7fc9a8)
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
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#port PaloAltoNextGenerationFirewallVirtualNetworkPanorama#port}.
        :param public_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#public_ip_address PaloAltoNextGenerationFirewallVirtualNetworkPanorama#public_ip_address}.
        '''
        value = PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatBackendConfig(
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
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#port PaloAltoNextGenerationFirewallVirtualNetworkPanorama#port}.
        :param public_ip_address_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#public_ip_address_id PaloAltoNextGenerationFirewallVirtualNetworkPanorama#public_ip_address_id}.
        '''
        value = PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatFrontendConfig(
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
    ) -> PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatBackendConfigOutputReference:
        return typing.cast(PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatBackendConfigOutputReference, jsii.get(self, "backendConfig"))

    @builtins.property
    @jsii.member(jsii_name="frontendConfig")
    def frontend_config(
        self,
    ) -> PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatFrontendConfigOutputReference:
        return typing.cast(PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatFrontendConfigOutputReference, jsii.get(self, "frontendConfig"))

    @builtins.property
    @jsii.member(jsii_name="backendConfigInput")
    def backend_config_input(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatBackendConfig]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatBackendConfig], jsii.get(self, "backendConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="frontendConfigInput")
    def frontend_config_input(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatFrontendConfig]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatFrontendConfig], jsii.get(self, "frontendConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d06d78cd47356c47ea036a276c19fbde72a16fb04917d8b79903ebe5c3e6bf7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__631bc8bfa8d0e4050aa5a12706f694516123d74ad6c7ba7653a5a6ec85860226)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNat]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNat]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNat]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55ead6cee9e7c57e3da7ae9d3f2dc6df50d9f9f0a8b456b2c082974f0dff5fd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkPanorama.PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettings",
    jsii_struct_bases=[],
    name_mapping={"dns_servers": "dnsServers", "use_azure_dns": "useAzureDns"},
)
class PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettings:
    def __init__(
        self,
        *,
        dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        use_azure_dns: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param dns_servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#dns_servers PaloAltoNextGenerationFirewallVirtualNetworkPanorama#dns_servers}.
        :param use_azure_dns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#use_azure_dns PaloAltoNextGenerationFirewallVirtualNetworkPanorama#use_azure_dns}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f034ee925c9f6963a0aca53cbd91f80e967e7bc771cffa28e5e6f492cbccebb1)
            check_type(argname="argument dns_servers", value=dns_servers, expected_type=type_hints["dns_servers"])
            check_type(argname="argument use_azure_dns", value=use_azure_dns, expected_type=type_hints["use_azure_dns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dns_servers is not None:
            self._values["dns_servers"] = dns_servers
        if use_azure_dns is not None:
            self._values["use_azure_dns"] = use_azure_dns

    @builtins.property
    def dns_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#dns_servers PaloAltoNextGenerationFirewallVirtualNetworkPanorama#dns_servers}.'''
        result = self._values.get("dns_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def use_azure_dns(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#use_azure_dns PaloAltoNextGenerationFirewallVirtualNetworkPanorama#use_azure_dns}.'''
        result = self._values.get("use_azure_dns")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkPanorama.PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de6cb623492aca96bd11824cf90b69e87a390a3cd53c189416328bb04ed702ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dae7dc15d44388d623cf47f439e24b707e6d3fd7ec1219fba77666f26b5dde37)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be9423ef6a49b999960bc85d7cd1b52a347cb43a87fda475576425859f5668db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useAzureDns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettings]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d02c44813c9b58f47cf161ebbd3785a5ad8e1f61bcffe64c2bc12157fc76892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkPanorama.PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfile",
    jsii_struct_bases=[],
    name_mapping={
        "public_ip_address_ids": "publicIpAddressIds",
        "vnet_configuration": "vnetConfiguration",
        "egress_nat_ip_address_ids": "egressNatIpAddressIds",
        "trusted_address_ranges": "trustedAddressRanges",
    },
)
class PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfile:
    def __init__(
        self,
        *,
        public_ip_address_ids: typing.Sequence[builtins.str],
        vnet_configuration: typing.Union["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileVnetConfiguration", typing.Dict[builtins.str, typing.Any]],
        egress_nat_ip_address_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        trusted_address_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param public_ip_address_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#public_ip_address_ids PaloAltoNextGenerationFirewallVirtualNetworkPanorama#public_ip_address_ids}.
        :param vnet_configuration: vnet_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#vnet_configuration PaloAltoNextGenerationFirewallVirtualNetworkPanorama#vnet_configuration}
        :param egress_nat_ip_address_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#egress_nat_ip_address_ids PaloAltoNextGenerationFirewallVirtualNetworkPanorama#egress_nat_ip_address_ids}.
        :param trusted_address_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#trusted_address_ranges PaloAltoNextGenerationFirewallVirtualNetworkPanorama#trusted_address_ranges}.
        '''
        if isinstance(vnet_configuration, dict):
            vnet_configuration = PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileVnetConfiguration(**vnet_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4f9be181bbee6af3c77c34cb78d4b3ea954c957b29665dccd6b20980f97127a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#public_ip_address_ids PaloAltoNextGenerationFirewallVirtualNetworkPanorama#public_ip_address_ids}.'''
        result = self._values.get("public_ip_address_ids")
        assert result is not None, "Required property 'public_ip_address_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def vnet_configuration(
        self,
    ) -> "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileVnetConfiguration":
        '''vnet_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#vnet_configuration PaloAltoNextGenerationFirewallVirtualNetworkPanorama#vnet_configuration}
        '''
        result = self._values.get("vnet_configuration")
        assert result is not None, "Required property 'vnet_configuration' is missing"
        return typing.cast("PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileVnetConfiguration", result)

    @builtins.property
    def egress_nat_ip_address_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#egress_nat_ip_address_ids PaloAltoNextGenerationFirewallVirtualNetworkPanorama#egress_nat_ip_address_ids}.'''
        result = self._values.get("egress_nat_ip_address_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def trusted_address_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#trusted_address_ranges PaloAltoNextGenerationFirewallVirtualNetworkPanorama#trusted_address_ranges}.'''
        result = self._values.get("trusted_address_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkPanorama.PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4378410c7a2888609320f763d3d0e646408a74aaa10faa786428a1c657ba3393)
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
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#virtual_network_id PaloAltoNextGenerationFirewallVirtualNetworkPanorama#virtual_network_id}.
        :param trusted_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#trusted_subnet_id PaloAltoNextGenerationFirewallVirtualNetworkPanorama#trusted_subnet_id}.
        :param untrusted_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#untrusted_subnet_id PaloAltoNextGenerationFirewallVirtualNetworkPanorama#untrusted_subnet_id}.
        '''
        value = PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileVnetConfiguration(
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
    ) -> "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileVnetConfigurationOutputReference":
        return typing.cast("PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileVnetConfigurationOutputReference", jsii.get(self, "vnetConfiguration"))

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
    ) -> typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileVnetConfiguration"]:
        return typing.cast(typing.Optional["PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileVnetConfiguration"], jsii.get(self, "vnetConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="egressNatIpAddressIds")
    def egress_nat_ip_address_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "egressNatIpAddressIds"))

    @egress_nat_ip_address_ids.setter
    def egress_nat_ip_address_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d9dcc0a1488dc2c439d5035b2c48e29dd017e6de6164da9858d6113fa8f0321)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "egressNatIpAddressIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicIpAddressIds")
    def public_ip_address_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "publicIpAddressIds"))

    @public_ip_address_ids.setter
    def public_ip_address_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__278efa1ff28f0b011964d17a934c5b51cbbaba4d435c10d4c91da04bb4ff0a3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpAddressIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustedAddressRanges")
    def trusted_address_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "trustedAddressRanges"))

    @trusted_address_ranges.setter
    def trusted_address_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42cbafbe266dd6c554fa8e0fae214302c1cc56974326ee471a797f754301c6e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustedAddressRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfile]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4d335d714da60e587f76c102e06836519ac83d02cb5abc65c94826761e2dc00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkPanorama.PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileVnetConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "virtual_network_id": "virtualNetworkId",
        "trusted_subnet_id": "trustedSubnetId",
        "untrusted_subnet_id": "untrustedSubnetId",
    },
)
class PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileVnetConfiguration:
    def __init__(
        self,
        *,
        virtual_network_id: builtins.str,
        trusted_subnet_id: typing.Optional[builtins.str] = None,
        untrusted_subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#virtual_network_id PaloAltoNextGenerationFirewallVirtualNetworkPanorama#virtual_network_id}.
        :param trusted_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#trusted_subnet_id PaloAltoNextGenerationFirewallVirtualNetworkPanorama#trusted_subnet_id}.
        :param untrusted_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#untrusted_subnet_id PaloAltoNextGenerationFirewallVirtualNetworkPanorama#untrusted_subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44a313835f20fa2442c84806eaff7a7c1f4dc13f3d74413c108bfdc65e0b518d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#virtual_network_id PaloAltoNextGenerationFirewallVirtualNetworkPanorama#virtual_network_id}.'''
        result = self._values.get("virtual_network_id")
        assert result is not None, "Required property 'virtual_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trusted_subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#trusted_subnet_id PaloAltoNextGenerationFirewallVirtualNetworkPanorama#trusted_subnet_id}.'''
        result = self._values.get("trusted_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def untrusted_subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#untrusted_subnet_id PaloAltoNextGenerationFirewallVirtualNetworkPanorama#untrusted_subnet_id}.'''
        result = self._values.get("untrusted_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileVnetConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileVnetConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkPanorama.PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileVnetConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f521f00d82218dc6e944291f0c9afcbfe67fc2b94f70c62718221ad7a1758bbc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1acd009ce804b01c63aa764329d68e77542b8f65379fc6e20ea35494f9a3fc38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustedSubnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="untrustedSubnetId")
    def untrusted_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "untrustedSubnetId"))

    @untrusted_subnet_id.setter
    def untrusted_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a72898d3bc979d6de01b651bd3f35008b172cf4c698f32e5576b279d4de8210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "untrustedSubnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bb99d674ee76435a315b23e7e96354d3037d13cfb9837ee20c11e6d999f628f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileVnetConfiguration]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileVnetConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileVnetConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bc7a09d04927065bfb4bd4e3ac7ca5fe7d8b9a2f42b4e1d1aecdd47428db042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkPanorama.PaloAltoNextGenerationFirewallVirtualNetworkPanoramaPanorama",
    jsii_struct_bases=[],
    name_mapping={},
)
class PaloAltoNextGenerationFirewallVirtualNetworkPanoramaPanorama:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaPanorama(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualNetworkPanoramaPanoramaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkPanorama.PaloAltoNextGenerationFirewallVirtualNetworkPanoramaPanoramaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf33175805a193b4e3040e1dda752479ba780f509fc72cfa1444793680447875)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaPanoramaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c916f3787d4e7002980792dd3bebac082fd3350206154b1a1d621039425d4dfd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PaloAltoNextGenerationFirewallVirtualNetworkPanoramaPanoramaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9b941c755ae0b903c19cb6196cd7e8d4c861c049bf466b926b1c845731376df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2469123b7958a263fccb58973e9826e4fa4a08ca561fce760714809ac9d3ebf4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e74145ece9cdbb69ddb56ed2f5f19f0fabe6e480bd09c50aa813f086ee534db7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class PaloAltoNextGenerationFirewallVirtualNetworkPanoramaPanoramaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkPanorama.PaloAltoNextGenerationFirewallVirtualNetworkPanoramaPanoramaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7acde019665b3ccbc581f270ed15eb2da2c59d2ecf942cef2b168247becdccc2)
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
    ) -> typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaPanorama]:
        return typing.cast(typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaPanorama], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaPanorama],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d8c298827581292a6861c9a679061c539c63867a15e82ac5ca0497d760bd60d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkPanorama.PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#create PaloAltoNextGenerationFirewallVirtualNetworkPanorama#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#delete PaloAltoNextGenerationFirewallVirtualNetworkPanorama#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#read PaloAltoNextGenerationFirewallVirtualNetworkPanorama#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#update PaloAltoNextGenerationFirewallVirtualNetworkPanorama#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4695095893c90d0a9f08c9e771cf12dfd745339839174a6773bd4ba4acc6cec8)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#create PaloAltoNextGenerationFirewallVirtualNetworkPanorama#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#delete PaloAltoNextGenerationFirewallVirtualNetworkPanorama#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#read PaloAltoNextGenerationFirewallVirtualNetworkPanorama#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_next_generation_firewall_virtual_network_panorama#update PaloAltoNextGenerationFirewallVirtualNetworkPanorama#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoNextGenerationFirewallVirtualNetworkPanorama.PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b49944e9f45286c58e8b8d3c40154cef4e16513e46531b6399709bc7bb49b6db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f7e9dae0dfc6f8f0825429c118fbbe88dc0fe6ad1a03be3f75ad6105ee111c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__968ed3bf01cac3a2417afb462897901f0a73c65a505deae3e1bdce7cf589b1e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e1c5580e32f4d8070a61ed3dc673e24f3e82bcf96558ba95fdfc57a9611810)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a0c868b89d9e6731af0b1a6e2d0eb45c51786014fc9a7cac58b4220a189e6cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e40b103f4e945b0039fa6781ebe83290cc288bffb199effa4ef5a2b278096474)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "PaloAltoNextGenerationFirewallVirtualNetworkPanorama",
    "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaConfig",
    "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNat",
    "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatBackendConfig",
    "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatBackendConfigOutputReference",
    "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatFrontendConfig",
    "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatFrontendConfigOutputReference",
    "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatList",
    "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatOutputReference",
    "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettings",
    "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettingsOutputReference",
    "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfile",
    "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileOutputReference",
    "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileVnetConfiguration",
    "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileVnetConfigurationOutputReference",
    "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaPanorama",
    "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaPanoramaList",
    "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaPanoramaOutputReference",
    "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeouts",
    "PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__051b444f0f6f9f5c9826bfa7c9cf24c4af288d638f69efc5b415df56e6de0aac(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    network_profile: typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfile, typing.Dict[builtins.str, typing.Any]],
    panorama_base64_config: builtins.str,
    resource_group_name: builtins.str,
    destination_nat: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNat, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns_settings: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    marketplace_offer_id: typing.Optional[builtins.str] = None,
    plan_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__99a2ae44e8acdf748eb784085fd237412be4e345e47e9c282ed4279e667cae75(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b5eb636868263eb0e0026ddaacbd03ecf7cdfb868683f983ce9cf3b1698129(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNat, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5efff977a4d1f69b21972132494acc0ae2c6ce9aa0624e6da4962b67e9535eeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceab16b5c9b49564799a30184423ca70791b82d72d2299951d2d59dd33e74b81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1588894ef15455db83ce1e17487bfc9b2c24b52f344bcfeca21d8427648431b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a13af17b5d6c4033d93109e4a0cdbc71e00823f9ed74a230dd18b15391b983(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f61010ae5a269bd5452e80a6ea26be80c5830c5ba4acf44d788263c28f5b56ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93cc90f78fbe14347c29b2e5ba7d4505d95bd52c53c3e46b4005928fe1160a0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a56e6c3750b951b5db80ce82d7c8b6e235dbedc74162e998352a380fc60966c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be3770276eec24a0a305ebb20024db0db9cb83e9d337ffb99bb1851406385b31(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__114305e1bdd0576e774f48e00d25fcee42fac761b6f4ed9fd79f88ca954d02b6(
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
    network_profile: typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfile, typing.Dict[builtins.str, typing.Any]],
    panorama_base64_config: builtins.str,
    resource_group_name: builtins.str,
    destination_nat: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNat, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns_settings: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    marketplace_offer_id: typing.Optional[builtins.str] = None,
    plan_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6402097bee711d2140ac8a6283511cf53085dc0e576001806287aa004d52afd6(
    *,
    name: builtins.str,
    protocol: builtins.str,
    backend_config: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatBackendConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    frontend_config: typing.Optional[typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatFrontendConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1768ab12983a3c1ee26022a05b0ceb64ae69b5673c2af85099ac4a7e58ef4c(
    *,
    port: jsii.Number,
    public_ip_address: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381f0549a502c386ce55e6ba38f83cb5f9e65a4b7003139868c41b2e2804282a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__411b82c86aa46cdcb6773680223924acbfa7046d42a689c57d1a42eed6534837(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff6b52c6cce0919b37e8aed5c882d066cd245e374bdb65671c664b0f0146b229(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46205aba7b5858b8893a3deb4f4dadef2b8b5a3ab42605c7c9c8d0b4fda741b2(
    value: typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatBackendConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44096152ad249a0d2f0076acab099534d4db2a6fb48ecd9197716765f26617bb(
    *,
    port: jsii.Number,
    public_ip_address_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__311b880eb8aace9afaf196a77ee98572a1761dc6d1eeeac716cd2216a8d18634(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdec2ab8002780f51dfbda3ab3ac744b1454426a620b5906e682645fcb349f49(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe53c40ce2bde99b64a313efb86a2a601ccc9eb1a41298f8686fbbc6dcaf6ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dedf3093e4204e727eebf76a53d6f713cf39a89afa17cee0ac4f0643ae0dc0f(
    value: typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNatFrontendConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca949186b2dac57169e8415e34a14b6c323d8ae2b793417d91e5f8325ea4e9aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d62fc134b5a600d1d176a5cb4469d4f402858e8b8f089cb92a2ef32cae1dd86e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6000837bd11520c2cfe84a820207146d4a5b86f40d6ccb3a707ab5121268cdc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f8cd9a0c8833579145554682274fe5b018ad3e13b70acf733a75199ec4549e0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d769657627ab42aa9715a53188cb4c5a940455026d2fbc3bbfae1fc288b68c28(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc2aa92ae86d9fab14e9c69c14847dcdfc9a42c401c42ba878ee9438767c3a35(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNat]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__256ae0e06ceb0d761651b9343faf9d883a09fcfee8ea798f930b0e28ac7fc9a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d06d78cd47356c47ea036a276c19fbde72a16fb04917d8b79903ebe5c3e6bf7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631bc8bfa8d0e4050aa5a12706f694516123d74ad6c7ba7653a5a6ec85860226(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55ead6cee9e7c57e3da7ae9d3f2dc6df50d9f9f0a8b456b2c082974f0dff5fd2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDestinationNat]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f034ee925c9f6963a0aca53cbd91f80e967e7bc771cffa28e5e6f492cbccebb1(
    *,
    dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    use_azure_dns: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de6cb623492aca96bd11824cf90b69e87a390a3cd53c189416328bb04ed702ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dae7dc15d44388d623cf47f439e24b707e6d3fd7ec1219fba77666f26b5dde37(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be9423ef6a49b999960bc85d7cd1b52a347cb43a87fda475576425859f5668db(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d02c44813c9b58f47cf161ebbd3785a5ad8e1f61bcffe64c2bc12157fc76892(
    value: typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaDnsSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4f9be181bbee6af3c77c34cb78d4b3ea954c957b29665dccd6b20980f97127a(
    *,
    public_ip_address_ids: typing.Sequence[builtins.str],
    vnet_configuration: typing.Union[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileVnetConfiguration, typing.Dict[builtins.str, typing.Any]],
    egress_nat_ip_address_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    trusted_address_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4378410c7a2888609320f763d3d0e646408a74aaa10faa786428a1c657ba3393(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d9dcc0a1488dc2c439d5035b2c48e29dd017e6de6164da9858d6113fa8f0321(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__278efa1ff28f0b011964d17a934c5b51cbbaba4d435c10d4c91da04bb4ff0a3f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42cbafbe266dd6c554fa8e0fae214302c1cc56974326ee471a797f754301c6e7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d335d714da60e587f76c102e06836519ac83d02cb5abc65c94826761e2dc00(
    value: typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a313835f20fa2442c84806eaff7a7c1f4dc13f3d74413c108bfdc65e0b518d(
    *,
    virtual_network_id: builtins.str,
    trusted_subnet_id: typing.Optional[builtins.str] = None,
    untrusted_subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f521f00d82218dc6e944291f0c9afcbfe67fc2b94f70c62718221ad7a1758bbc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1acd009ce804b01c63aa764329d68e77542b8f65379fc6e20ea35494f9a3fc38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a72898d3bc979d6de01b651bd3f35008b172cf4c698f32e5576b279d4de8210(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb99d674ee76435a315b23e7e96354d3037d13cfb9837ee20c11e6d999f628f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bc7a09d04927065bfb4bd4e3ac7ca5fe7d8b9a2f42b4e1d1aecdd47428db042(
    value: typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaNetworkProfileVnetConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf33175805a193b4e3040e1dda752479ba780f509fc72cfa1444793680447875(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c916f3787d4e7002980792dd3bebac082fd3350206154b1a1d621039425d4dfd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b941c755ae0b903c19cb6196cd7e8d4c861c049bf466b926b1c845731376df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2469123b7958a263fccb58973e9826e4fa4a08ca561fce760714809ac9d3ebf4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e74145ece9cdbb69ddb56ed2f5f19f0fabe6e480bd09c50aa813f086ee534db7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7acde019665b3ccbc581f270ed15eb2da2c59d2ecf942cef2b168247becdccc2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d8c298827581292a6861c9a679061c539c63867a15e82ac5ca0497d760bd60d(
    value: typing.Optional[PaloAltoNextGenerationFirewallVirtualNetworkPanoramaPanorama],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4695095893c90d0a9f08c9e771cf12dfd745339839174a6773bd4ba4acc6cec8(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b49944e9f45286c58e8b8d3c40154cef4e16513e46531b6399709bc7bb49b6db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7e9dae0dfc6f8f0825429c118fbbe88dc0fe6ad1a03be3f75ad6105ee111c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__968ed3bf01cac3a2417afb462897901f0a73c65a505deae3e1bdce7cf589b1e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e1c5580e32f4d8070a61ed3dc673e24f3e82bcf96558ba95fdfc57a9611810(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a0c868b89d9e6731af0b1a6e2d0eb45c51786014fc9a7cac58b4220a189e6cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e40b103f4e945b0039fa6781ebe83290cc288bffb199effa4ef5a2b278096474(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoNextGenerationFirewallVirtualNetworkPanoramaTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
