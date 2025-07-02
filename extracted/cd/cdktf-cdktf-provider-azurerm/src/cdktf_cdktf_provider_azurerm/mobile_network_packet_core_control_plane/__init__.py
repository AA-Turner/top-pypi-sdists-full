r'''
# `azurerm_mobile_network_packet_core_control_plane`

Refer to the Terraform Registry for docs: [`azurerm_mobile_network_packet_core_control_plane`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane).
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


class MobileNetworkPacketCoreControlPlane(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkPacketCoreControlPlane.MobileNetworkPacketCoreControlPlane",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane azurerm_mobile_network_packet_core_control_plane}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        local_diagnostics_access: typing.Union["MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccess", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        site_ids: typing.Sequence[builtins.str],
        sku: builtins.str,
        control_plane_access_ipv4_address: typing.Optional[builtins.str] = None,
        control_plane_access_ipv4_gateway: typing.Optional[builtins.str] = None,
        control_plane_access_ipv4_subnet: typing.Optional[builtins.str] = None,
        control_plane_access_name: typing.Optional[builtins.str] = None,
        core_network_technology: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["MobileNetworkPacketCoreControlPlaneIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        interoperability_settings_json: typing.Optional[builtins.str] = None,
        platform: typing.Optional[typing.Union["MobileNetworkPacketCoreControlPlanePlatform", typing.Dict[builtins.str, typing.Any]]] = None,
        software_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MobileNetworkPacketCoreControlPlaneTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_equipment_mtu_in_bytes: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane azurerm_mobile_network_packet_core_control_plane} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param local_diagnostics_access: local_diagnostics_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#local_diagnostics_access MobileNetworkPacketCoreControlPlane#local_diagnostics_access}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#location MobileNetworkPacketCoreControlPlane#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#name MobileNetworkPacketCoreControlPlane#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#resource_group_name MobileNetworkPacketCoreControlPlane#resource_group_name}.
        :param site_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#site_ids MobileNetworkPacketCoreControlPlane#site_ids}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#sku MobileNetworkPacketCoreControlPlane#sku}.
        :param control_plane_access_ipv4_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#control_plane_access_ipv4_address MobileNetworkPacketCoreControlPlane#control_plane_access_ipv4_address}.
        :param control_plane_access_ipv4_gateway: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#control_plane_access_ipv4_gateway MobileNetworkPacketCoreControlPlane#control_plane_access_ipv4_gateway}.
        :param control_plane_access_ipv4_subnet: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#control_plane_access_ipv4_subnet MobileNetworkPacketCoreControlPlane#control_plane_access_ipv4_subnet}.
        :param control_plane_access_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#control_plane_access_name MobileNetworkPacketCoreControlPlane#control_plane_access_name}.
        :param core_network_technology: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#core_network_technology MobileNetworkPacketCoreControlPlane#core_network_technology}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#id MobileNetworkPacketCoreControlPlane#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#identity MobileNetworkPacketCoreControlPlane#identity}
        :param interoperability_settings_json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#interoperability_settings_json MobileNetworkPacketCoreControlPlane#interoperability_settings_json}.
        :param platform: platform block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#platform MobileNetworkPacketCoreControlPlane#platform}
        :param software_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#software_version MobileNetworkPacketCoreControlPlane#software_version}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#tags MobileNetworkPacketCoreControlPlane#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#timeouts MobileNetworkPacketCoreControlPlane#timeouts}
        :param user_equipment_mtu_in_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#user_equipment_mtu_in_bytes MobileNetworkPacketCoreControlPlane#user_equipment_mtu_in_bytes}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5866ab3433446e08a892c543d1e04bffa0a2eeb5ce7b809c33bd65adeb8deb5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MobileNetworkPacketCoreControlPlaneConfig(
            local_diagnostics_access=local_diagnostics_access,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            site_ids=site_ids,
            sku=sku,
            control_plane_access_ipv4_address=control_plane_access_ipv4_address,
            control_plane_access_ipv4_gateway=control_plane_access_ipv4_gateway,
            control_plane_access_ipv4_subnet=control_plane_access_ipv4_subnet,
            control_plane_access_name=control_plane_access_name,
            core_network_technology=core_network_technology,
            id=id,
            identity=identity,
            interoperability_settings_json=interoperability_settings_json,
            platform=platform,
            software_version=software_version,
            tags=tags,
            timeouts=timeouts,
            user_equipment_mtu_in_bytes=user_equipment_mtu_in_bytes,
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
        '''Generates CDKTF code for importing a MobileNetworkPacketCoreControlPlane resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MobileNetworkPacketCoreControlPlane to import.
        :param import_from_id: The id of the existing MobileNetworkPacketCoreControlPlane that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MobileNetworkPacketCoreControlPlane to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46a20ebfd6c09daedfd93a54427f309fe85e3e90cb759192548461fbfda60f7f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        identity_ids: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#identity_ids MobileNetworkPacketCoreControlPlane#identity_ids}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#type MobileNetworkPacketCoreControlPlane#type}.
        '''
        value = MobileNetworkPacketCoreControlPlaneIdentity(
            identity_ids=identity_ids, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putLocalDiagnosticsAccess")
    def put_local_diagnostics_access(
        self,
        *,
        authentication_type: builtins.str,
        https_server_certificate_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#authentication_type MobileNetworkPacketCoreControlPlane#authentication_type}.
        :param https_server_certificate_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#https_server_certificate_url MobileNetworkPacketCoreControlPlane#https_server_certificate_url}.
        '''
        value = MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccess(
            authentication_type=authentication_type,
            https_server_certificate_url=https_server_certificate_url,
        )

        return typing.cast(None, jsii.invoke(self, "putLocalDiagnosticsAccess", [value]))

    @jsii.member(jsii_name="putPlatform")
    def put_platform(
        self,
        *,
        type: builtins.str,
        arc_kubernetes_cluster_id: typing.Optional[builtins.str] = None,
        custom_location_id: typing.Optional[builtins.str] = None,
        edge_device_id: typing.Optional[builtins.str] = None,
        stack_hci_cluster_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#type MobileNetworkPacketCoreControlPlane#type}.
        :param arc_kubernetes_cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#arc_kubernetes_cluster_id MobileNetworkPacketCoreControlPlane#arc_kubernetes_cluster_id}.
        :param custom_location_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#custom_location_id MobileNetworkPacketCoreControlPlane#custom_location_id}.
        :param edge_device_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#edge_device_id MobileNetworkPacketCoreControlPlane#edge_device_id}.
        :param stack_hci_cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#stack_hci_cluster_id MobileNetworkPacketCoreControlPlane#stack_hci_cluster_id}.
        '''
        value = MobileNetworkPacketCoreControlPlanePlatform(
            type=type,
            arc_kubernetes_cluster_id=arc_kubernetes_cluster_id,
            custom_location_id=custom_location_id,
            edge_device_id=edge_device_id,
            stack_hci_cluster_id=stack_hci_cluster_id,
        )

        return typing.cast(None, jsii.invoke(self, "putPlatform", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#create MobileNetworkPacketCoreControlPlane#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#delete MobileNetworkPacketCoreControlPlane#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#read MobileNetworkPacketCoreControlPlane#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#update MobileNetworkPacketCoreControlPlane#update}.
        '''
        value = MobileNetworkPacketCoreControlPlaneTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetControlPlaneAccessIpv4Address")
    def reset_control_plane_access_ipv4_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControlPlaneAccessIpv4Address", []))

    @jsii.member(jsii_name="resetControlPlaneAccessIpv4Gateway")
    def reset_control_plane_access_ipv4_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControlPlaneAccessIpv4Gateway", []))

    @jsii.member(jsii_name="resetControlPlaneAccessIpv4Subnet")
    def reset_control_plane_access_ipv4_subnet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControlPlaneAccessIpv4Subnet", []))

    @jsii.member(jsii_name="resetControlPlaneAccessName")
    def reset_control_plane_access_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControlPlaneAccessName", []))

    @jsii.member(jsii_name="resetCoreNetworkTechnology")
    def reset_core_network_technology(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoreNetworkTechnology", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetInteroperabilitySettingsJson")
    def reset_interoperability_settings_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInteroperabilitySettingsJson", []))

    @jsii.member(jsii_name="resetPlatform")
    def reset_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatform", []))

    @jsii.member(jsii_name="resetSoftwareVersion")
    def reset_software_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSoftwareVersion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUserEquipmentMtuInBytes")
    def reset_user_equipment_mtu_in_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserEquipmentMtuInBytes", []))

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
    @jsii.member(jsii_name="identity")
    def identity(self) -> "MobileNetworkPacketCoreControlPlaneIdentityOutputReference":
        return typing.cast("MobileNetworkPacketCoreControlPlaneIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="localDiagnosticsAccess")
    def local_diagnostics_access(
        self,
    ) -> "MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccessOutputReference":
        return typing.cast("MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccessOutputReference", jsii.get(self, "localDiagnosticsAccess"))

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> "MobileNetworkPacketCoreControlPlanePlatformOutputReference":
        return typing.cast("MobileNetworkPacketCoreControlPlanePlatformOutputReference", jsii.get(self, "platform"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MobileNetworkPacketCoreControlPlaneTimeoutsOutputReference":
        return typing.cast("MobileNetworkPacketCoreControlPlaneTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneAccessIpv4AddressInput")
    def control_plane_access_ipv4_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "controlPlaneAccessIpv4AddressInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneAccessIpv4GatewayInput")
    def control_plane_access_ipv4_gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "controlPlaneAccessIpv4GatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneAccessIpv4SubnetInput")
    def control_plane_access_ipv4_subnet_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "controlPlaneAccessIpv4SubnetInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneAccessNameInput")
    def control_plane_access_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "controlPlaneAccessNameInput"))

    @builtins.property
    @jsii.member(jsii_name="coreNetworkTechnologyInput")
    def core_network_technology_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "coreNetworkTechnologyInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(
        self,
    ) -> typing.Optional["MobileNetworkPacketCoreControlPlaneIdentity"]:
        return typing.cast(typing.Optional["MobileNetworkPacketCoreControlPlaneIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="interoperabilitySettingsJsonInput")
    def interoperability_settings_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interoperabilitySettingsJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="localDiagnosticsAccessInput")
    def local_diagnostics_access_input(
        self,
    ) -> typing.Optional["MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccess"]:
        return typing.cast(typing.Optional["MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccess"], jsii.get(self, "localDiagnosticsAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="platformInput")
    def platform_input(
        self,
    ) -> typing.Optional["MobileNetworkPacketCoreControlPlanePlatform"]:
        return typing.cast(typing.Optional["MobileNetworkPacketCoreControlPlanePlatform"], jsii.get(self, "platformInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="siteIdsInput")
    def site_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "siteIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="skuInput")
    def sku_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuInput"))

    @builtins.property
    @jsii.member(jsii_name="softwareVersionInput")
    def software_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "softwareVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MobileNetworkPacketCoreControlPlaneTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MobileNetworkPacketCoreControlPlaneTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userEquipmentMtuInBytesInput")
    def user_equipment_mtu_in_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "userEquipmentMtuInBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneAccessIpv4Address")
    def control_plane_access_ipv4_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "controlPlaneAccessIpv4Address"))

    @control_plane_access_ipv4_address.setter
    def control_plane_access_ipv4_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bd3569ac1257117a1c396fbd9f3bb65f2bd69a18211221c920e706742d0cde5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneAccessIpv4Address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="controlPlaneAccessIpv4Gateway")
    def control_plane_access_ipv4_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "controlPlaneAccessIpv4Gateway"))

    @control_plane_access_ipv4_gateway.setter
    def control_plane_access_ipv4_gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f650116fb36886d5fadd5bca6b9649262152706dd8a6f4e6bd60ddf906ce6b29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneAccessIpv4Gateway", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="controlPlaneAccessIpv4Subnet")
    def control_plane_access_ipv4_subnet(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "controlPlaneAccessIpv4Subnet"))

    @control_plane_access_ipv4_subnet.setter
    def control_plane_access_ipv4_subnet(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c08a346c5fa033e12c687d4d9c706322c3e6c115356c54d23d7a4e42e901a4a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneAccessIpv4Subnet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="controlPlaneAccessName")
    def control_plane_access_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "controlPlaneAccessName"))

    @control_plane_access_name.setter
    def control_plane_access_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6185d3270f48d0d9fb61cd5380501d8c49eb49c7c4a21fb21fcd34a26a1dfab5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlaneAccessName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="coreNetworkTechnology")
    def core_network_technology(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "coreNetworkTechnology"))

    @core_network_technology.setter
    def core_network_technology(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9682db61276738ec742730843267751089e246b79ede16a405757254cd71ef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coreNetworkTechnology", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6101c623d2d9d39e48a72e3ac6965edfec8b15a0fd2dba36942f2be9506fc711)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interoperabilitySettingsJson")
    def interoperability_settings_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interoperabilitySettingsJson"))

    @interoperability_settings_json.setter
    def interoperability_settings_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__149f093a31c85c6375c7a2091081f60950bc925d40b96eb50b940c14d7ac4cf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interoperabilitySettingsJson", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a36c6ffe49f39fff3cb16bd2d8e5aeceb7d1cba94ce3d808c211800b54c90241)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56ab8979676b6ece4335a2f220155ce901fe60d4f19d1d890d4811aa7d1f1d55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__341d1143d3145aa0a9bfe84be1163f8e495c107e62a146a8559588373a8dcac0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="siteIds")
    def site_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "siteIds"))

    @site_ids.setter
    def site_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4730bb48cec5dc36ee1064f014e7755f203713fdab7f87949cd4dbc415b4d50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "siteIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sku")
    def sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sku"))

    @sku.setter
    def sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c57c895182a416ed8e44e570f8ad47d08fb81cac93d6e3d8bfde10f69d38c00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sku", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="softwareVersion")
    def software_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "softwareVersion"))

    @software_version.setter
    def software_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b38897d6f048ce89def67fe28ea47bbb10af70141b36a636cdc636298efb93e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "softwareVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cfc4dd81032d86f79a4c94fd82152854df00fa887d2f260d199ddf370a876c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userEquipmentMtuInBytes")
    def user_equipment_mtu_in_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "userEquipmentMtuInBytes"))

    @user_equipment_mtu_in_bytes.setter
    def user_equipment_mtu_in_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4c034bc1cd1fddf5af3ae9afd1cf85b274c565691d28c3c0bb2ed2dde7ceed4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userEquipmentMtuInBytes", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkPacketCoreControlPlane.MobileNetworkPacketCoreControlPlaneConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "local_diagnostics_access": "localDiagnosticsAccess",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "site_ids": "siteIds",
        "sku": "sku",
        "control_plane_access_ipv4_address": "controlPlaneAccessIpv4Address",
        "control_plane_access_ipv4_gateway": "controlPlaneAccessIpv4Gateway",
        "control_plane_access_ipv4_subnet": "controlPlaneAccessIpv4Subnet",
        "control_plane_access_name": "controlPlaneAccessName",
        "core_network_technology": "coreNetworkTechnology",
        "id": "id",
        "identity": "identity",
        "interoperability_settings_json": "interoperabilitySettingsJson",
        "platform": "platform",
        "software_version": "softwareVersion",
        "tags": "tags",
        "timeouts": "timeouts",
        "user_equipment_mtu_in_bytes": "userEquipmentMtuInBytes",
    },
)
class MobileNetworkPacketCoreControlPlaneConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        local_diagnostics_access: typing.Union["MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccess", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        site_ids: typing.Sequence[builtins.str],
        sku: builtins.str,
        control_plane_access_ipv4_address: typing.Optional[builtins.str] = None,
        control_plane_access_ipv4_gateway: typing.Optional[builtins.str] = None,
        control_plane_access_ipv4_subnet: typing.Optional[builtins.str] = None,
        control_plane_access_name: typing.Optional[builtins.str] = None,
        core_network_technology: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["MobileNetworkPacketCoreControlPlaneIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        interoperability_settings_json: typing.Optional[builtins.str] = None,
        platform: typing.Optional[typing.Union["MobileNetworkPacketCoreControlPlanePlatform", typing.Dict[builtins.str, typing.Any]]] = None,
        software_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MobileNetworkPacketCoreControlPlaneTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_equipment_mtu_in_bytes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param local_diagnostics_access: local_diagnostics_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#local_diagnostics_access MobileNetworkPacketCoreControlPlane#local_diagnostics_access}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#location MobileNetworkPacketCoreControlPlane#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#name MobileNetworkPacketCoreControlPlane#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#resource_group_name MobileNetworkPacketCoreControlPlane#resource_group_name}.
        :param site_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#site_ids MobileNetworkPacketCoreControlPlane#site_ids}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#sku MobileNetworkPacketCoreControlPlane#sku}.
        :param control_plane_access_ipv4_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#control_plane_access_ipv4_address MobileNetworkPacketCoreControlPlane#control_plane_access_ipv4_address}.
        :param control_plane_access_ipv4_gateway: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#control_plane_access_ipv4_gateway MobileNetworkPacketCoreControlPlane#control_plane_access_ipv4_gateway}.
        :param control_plane_access_ipv4_subnet: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#control_plane_access_ipv4_subnet MobileNetworkPacketCoreControlPlane#control_plane_access_ipv4_subnet}.
        :param control_plane_access_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#control_plane_access_name MobileNetworkPacketCoreControlPlane#control_plane_access_name}.
        :param core_network_technology: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#core_network_technology MobileNetworkPacketCoreControlPlane#core_network_technology}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#id MobileNetworkPacketCoreControlPlane#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#identity MobileNetworkPacketCoreControlPlane#identity}
        :param interoperability_settings_json: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#interoperability_settings_json MobileNetworkPacketCoreControlPlane#interoperability_settings_json}.
        :param platform: platform block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#platform MobileNetworkPacketCoreControlPlane#platform}
        :param software_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#software_version MobileNetworkPacketCoreControlPlane#software_version}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#tags MobileNetworkPacketCoreControlPlane#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#timeouts MobileNetworkPacketCoreControlPlane#timeouts}
        :param user_equipment_mtu_in_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#user_equipment_mtu_in_bytes MobileNetworkPacketCoreControlPlane#user_equipment_mtu_in_bytes}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(local_diagnostics_access, dict):
            local_diagnostics_access = MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccess(**local_diagnostics_access)
        if isinstance(identity, dict):
            identity = MobileNetworkPacketCoreControlPlaneIdentity(**identity)
        if isinstance(platform, dict):
            platform = MobileNetworkPacketCoreControlPlanePlatform(**platform)
        if isinstance(timeouts, dict):
            timeouts = MobileNetworkPacketCoreControlPlaneTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93f9720385d983f8e2b63b330ac8b1b807548f37aeb7db285e5c780414e0048a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument local_diagnostics_access", value=local_diagnostics_access, expected_type=type_hints["local_diagnostics_access"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument site_ids", value=site_ids, expected_type=type_hints["site_ids"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument control_plane_access_ipv4_address", value=control_plane_access_ipv4_address, expected_type=type_hints["control_plane_access_ipv4_address"])
            check_type(argname="argument control_plane_access_ipv4_gateway", value=control_plane_access_ipv4_gateway, expected_type=type_hints["control_plane_access_ipv4_gateway"])
            check_type(argname="argument control_plane_access_ipv4_subnet", value=control_plane_access_ipv4_subnet, expected_type=type_hints["control_plane_access_ipv4_subnet"])
            check_type(argname="argument control_plane_access_name", value=control_plane_access_name, expected_type=type_hints["control_plane_access_name"])
            check_type(argname="argument core_network_technology", value=core_network_technology, expected_type=type_hints["core_network_technology"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument interoperability_settings_json", value=interoperability_settings_json, expected_type=type_hints["interoperability_settings_json"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument software_version", value=software_version, expected_type=type_hints["software_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument user_equipment_mtu_in_bytes", value=user_equipment_mtu_in_bytes, expected_type=type_hints["user_equipment_mtu_in_bytes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "local_diagnostics_access": local_diagnostics_access,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "site_ids": site_ids,
            "sku": sku,
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
        if control_plane_access_ipv4_address is not None:
            self._values["control_plane_access_ipv4_address"] = control_plane_access_ipv4_address
        if control_plane_access_ipv4_gateway is not None:
            self._values["control_plane_access_ipv4_gateway"] = control_plane_access_ipv4_gateway
        if control_plane_access_ipv4_subnet is not None:
            self._values["control_plane_access_ipv4_subnet"] = control_plane_access_ipv4_subnet
        if control_plane_access_name is not None:
            self._values["control_plane_access_name"] = control_plane_access_name
        if core_network_technology is not None:
            self._values["core_network_technology"] = core_network_technology
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if interoperability_settings_json is not None:
            self._values["interoperability_settings_json"] = interoperability_settings_json
        if platform is not None:
            self._values["platform"] = platform
        if software_version is not None:
            self._values["software_version"] = software_version
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if user_equipment_mtu_in_bytes is not None:
            self._values["user_equipment_mtu_in_bytes"] = user_equipment_mtu_in_bytes

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
    def local_diagnostics_access(
        self,
    ) -> "MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccess":
        '''local_diagnostics_access block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#local_diagnostics_access MobileNetworkPacketCoreControlPlane#local_diagnostics_access}
        '''
        result = self._values.get("local_diagnostics_access")
        assert result is not None, "Required property 'local_diagnostics_access' is missing"
        return typing.cast("MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccess", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#location MobileNetworkPacketCoreControlPlane#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#name MobileNetworkPacketCoreControlPlane#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#resource_group_name MobileNetworkPacketCoreControlPlane#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def site_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#site_ids MobileNetworkPacketCoreControlPlane#site_ids}.'''
        result = self._values.get("site_ids")
        assert result is not None, "Required property 'site_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def sku(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#sku MobileNetworkPacketCoreControlPlane#sku}.'''
        result = self._values.get("sku")
        assert result is not None, "Required property 'sku' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def control_plane_access_ipv4_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#control_plane_access_ipv4_address MobileNetworkPacketCoreControlPlane#control_plane_access_ipv4_address}.'''
        result = self._values.get("control_plane_access_ipv4_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def control_plane_access_ipv4_gateway(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#control_plane_access_ipv4_gateway MobileNetworkPacketCoreControlPlane#control_plane_access_ipv4_gateway}.'''
        result = self._values.get("control_plane_access_ipv4_gateway")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def control_plane_access_ipv4_subnet(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#control_plane_access_ipv4_subnet MobileNetworkPacketCoreControlPlane#control_plane_access_ipv4_subnet}.'''
        result = self._values.get("control_plane_access_ipv4_subnet")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def control_plane_access_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#control_plane_access_name MobileNetworkPacketCoreControlPlane#control_plane_access_name}.'''
        result = self._values.get("control_plane_access_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def core_network_technology(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#core_network_technology MobileNetworkPacketCoreControlPlane#core_network_technology}.'''
        result = self._values.get("core_network_technology")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#id MobileNetworkPacketCoreControlPlane#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(
        self,
    ) -> typing.Optional["MobileNetworkPacketCoreControlPlaneIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#identity MobileNetworkPacketCoreControlPlane#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["MobileNetworkPacketCoreControlPlaneIdentity"], result)

    @builtins.property
    def interoperability_settings_json(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#interoperability_settings_json MobileNetworkPacketCoreControlPlane#interoperability_settings_json}.'''
        result = self._values.get("interoperability_settings_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platform(
        self,
    ) -> typing.Optional["MobileNetworkPacketCoreControlPlanePlatform"]:
        '''platform block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#platform MobileNetworkPacketCoreControlPlane#platform}
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional["MobileNetworkPacketCoreControlPlanePlatform"], result)

    @builtins.property
    def software_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#software_version MobileNetworkPacketCoreControlPlane#software_version}.'''
        result = self._values.get("software_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#tags MobileNetworkPacketCoreControlPlane#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["MobileNetworkPacketCoreControlPlaneTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#timeouts MobileNetworkPacketCoreControlPlane#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MobileNetworkPacketCoreControlPlaneTimeouts"], result)

    @builtins.property
    def user_equipment_mtu_in_bytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#user_equipment_mtu_in_bytes MobileNetworkPacketCoreControlPlane#user_equipment_mtu_in_bytes}.'''
        result = self._values.get("user_equipment_mtu_in_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkPacketCoreControlPlaneConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkPacketCoreControlPlane.MobileNetworkPacketCoreControlPlaneIdentity",
    jsii_struct_bases=[],
    name_mapping={"identity_ids": "identityIds", "type": "type"},
)
class MobileNetworkPacketCoreControlPlaneIdentity:
    def __init__(
        self,
        *,
        identity_ids: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#identity_ids MobileNetworkPacketCoreControlPlane#identity_ids}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#type MobileNetworkPacketCoreControlPlane#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0557b408bece11221f25d38ca623b70853b82d8953f6a8e399d345f591698641)
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "identity_ids": identity_ids,
            "type": type,
        }

    @builtins.property
    def identity_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#identity_ids MobileNetworkPacketCoreControlPlane#identity_ids}.'''
        result = self._values.get("identity_ids")
        assert result is not None, "Required property 'identity_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#type MobileNetworkPacketCoreControlPlane#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkPacketCoreControlPlaneIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MobileNetworkPacketCoreControlPlaneIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkPacketCoreControlPlane.MobileNetworkPacketCoreControlPlaneIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb77a590eb46b72a8acff4f0f02fb87d8ea20ec93ae95efb79045b662cef526a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="identityIdsInput")
    def identity_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identityIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="identityIds")
    def identity_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identityIds"))

    @identity_ids.setter
    def identity_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c28da3d668910c42955fee504519fbcd9a3061d851e33a0dfd15306773ee91e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__425835c6765ba3de5de647dde046ca5bf1f71a7a25eb65f45d569df0956b2e1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MobileNetworkPacketCoreControlPlaneIdentity]:
        return typing.cast(typing.Optional[MobileNetworkPacketCoreControlPlaneIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MobileNetworkPacketCoreControlPlaneIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a0c031a9cd8de63007a5467bf61f539a6ce952149c30af017714fc5b77ee7e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkPacketCoreControlPlane.MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccess",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_type": "authenticationType",
        "https_server_certificate_url": "httpsServerCertificateUrl",
    },
)
class MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccess:
    def __init__(
        self,
        *,
        authentication_type: builtins.str,
        https_server_certificate_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#authentication_type MobileNetworkPacketCoreControlPlane#authentication_type}.
        :param https_server_certificate_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#https_server_certificate_url MobileNetworkPacketCoreControlPlane#https_server_certificate_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94dcaccc61f12b8c8edad97654a0082c58120efca4b807feda6d346c935a3b02)
            check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
            check_type(argname="argument https_server_certificate_url", value=https_server_certificate_url, expected_type=type_hints["https_server_certificate_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authentication_type": authentication_type,
        }
        if https_server_certificate_url is not None:
            self._values["https_server_certificate_url"] = https_server_certificate_url

    @builtins.property
    def authentication_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#authentication_type MobileNetworkPacketCoreControlPlane#authentication_type}.'''
        result = self._values.get("authentication_type")
        assert result is not None, "Required property 'authentication_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def https_server_certificate_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#https_server_certificate_url MobileNetworkPacketCoreControlPlane#https_server_certificate_url}.'''
        result = self._values.get("https_server_certificate_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkPacketCoreControlPlane.MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcefb54e5196b017376a7552154f5119d05b698cc62d0cdb2386ff510793aa3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHttpsServerCertificateUrl")
    def reset_https_server_certificate_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsServerCertificateUrl", []))

    @builtins.property
    @jsii.member(jsii_name="authenticationTypeInput")
    def authentication_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsServerCertificateUrlInput")
    def https_server_certificate_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpsServerCertificateUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationType")
    def authentication_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationType"))

    @authentication_type.setter
    def authentication_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__075c2ad3e14527f0a26c552f952f1f8f792e6d5a1da4f98fc285182bad4b5df2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsServerCertificateUrl")
    def https_server_certificate_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsServerCertificateUrl"))

    @https_server_certificate_url.setter
    def https_server_certificate_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bbe603fbbf7ccc49bd83dfbf6c3833da2ff8b13ae944b15d99928399b713097)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsServerCertificateUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccess]:
        return typing.cast(typing.Optional[MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86ac30eb31375e925a5f5171e4143e10cf10c4f704ff69478165e5394f19af35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkPacketCoreControlPlane.MobileNetworkPacketCoreControlPlanePlatform",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "arc_kubernetes_cluster_id": "arcKubernetesClusterId",
        "custom_location_id": "customLocationId",
        "edge_device_id": "edgeDeviceId",
        "stack_hci_cluster_id": "stackHciClusterId",
    },
)
class MobileNetworkPacketCoreControlPlanePlatform:
    def __init__(
        self,
        *,
        type: builtins.str,
        arc_kubernetes_cluster_id: typing.Optional[builtins.str] = None,
        custom_location_id: typing.Optional[builtins.str] = None,
        edge_device_id: typing.Optional[builtins.str] = None,
        stack_hci_cluster_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#type MobileNetworkPacketCoreControlPlane#type}.
        :param arc_kubernetes_cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#arc_kubernetes_cluster_id MobileNetworkPacketCoreControlPlane#arc_kubernetes_cluster_id}.
        :param custom_location_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#custom_location_id MobileNetworkPacketCoreControlPlane#custom_location_id}.
        :param edge_device_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#edge_device_id MobileNetworkPacketCoreControlPlane#edge_device_id}.
        :param stack_hci_cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#stack_hci_cluster_id MobileNetworkPacketCoreControlPlane#stack_hci_cluster_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c49746bca557a5346c79f9892ae217c9eac5226a4559fe17390798e50c8602a)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument arc_kubernetes_cluster_id", value=arc_kubernetes_cluster_id, expected_type=type_hints["arc_kubernetes_cluster_id"])
            check_type(argname="argument custom_location_id", value=custom_location_id, expected_type=type_hints["custom_location_id"])
            check_type(argname="argument edge_device_id", value=edge_device_id, expected_type=type_hints["edge_device_id"])
            check_type(argname="argument stack_hci_cluster_id", value=stack_hci_cluster_id, expected_type=type_hints["stack_hci_cluster_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if arc_kubernetes_cluster_id is not None:
            self._values["arc_kubernetes_cluster_id"] = arc_kubernetes_cluster_id
        if custom_location_id is not None:
            self._values["custom_location_id"] = custom_location_id
        if edge_device_id is not None:
            self._values["edge_device_id"] = edge_device_id
        if stack_hci_cluster_id is not None:
            self._values["stack_hci_cluster_id"] = stack_hci_cluster_id

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#type MobileNetworkPacketCoreControlPlane#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arc_kubernetes_cluster_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#arc_kubernetes_cluster_id MobileNetworkPacketCoreControlPlane#arc_kubernetes_cluster_id}.'''
        result = self._values.get("arc_kubernetes_cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_location_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#custom_location_id MobileNetworkPacketCoreControlPlane#custom_location_id}.'''
        result = self._values.get("custom_location_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edge_device_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#edge_device_id MobileNetworkPacketCoreControlPlane#edge_device_id}.'''
        result = self._values.get("edge_device_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stack_hci_cluster_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#stack_hci_cluster_id MobileNetworkPacketCoreControlPlane#stack_hci_cluster_id}.'''
        result = self._values.get("stack_hci_cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkPacketCoreControlPlanePlatform(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MobileNetworkPacketCoreControlPlanePlatformOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkPacketCoreControlPlane.MobileNetworkPacketCoreControlPlanePlatformOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5487452b25d242dd3a2f8952524c81780420c5bdb5ef6e3f61411d4fa2689051)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetArcKubernetesClusterId")
    def reset_arc_kubernetes_cluster_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArcKubernetesClusterId", []))

    @jsii.member(jsii_name="resetCustomLocationId")
    def reset_custom_location_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomLocationId", []))

    @jsii.member(jsii_name="resetEdgeDeviceId")
    def reset_edge_device_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdgeDeviceId", []))

    @jsii.member(jsii_name="resetStackHciClusterId")
    def reset_stack_hci_cluster_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStackHciClusterId", []))

    @builtins.property
    @jsii.member(jsii_name="arcKubernetesClusterIdInput")
    def arc_kubernetes_cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arcKubernetesClusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="customLocationIdInput")
    def custom_location_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customLocationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeDeviceIdInput")
    def edge_device_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeDeviceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="stackHciClusterIdInput")
    def stack_hci_cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stackHciClusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="arcKubernetesClusterId")
    def arc_kubernetes_cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arcKubernetesClusterId"))

    @arc_kubernetes_cluster_id.setter
    def arc_kubernetes_cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1486f69e8244dbaa817503bb4f6b6c778bda21752ec5ee0c94513190e95c9bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arcKubernetesClusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customLocationId")
    def custom_location_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customLocationId"))

    @custom_location_id.setter
    def custom_location_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__703dcc36d33d49efd260094cb52414232981bf23a7494ea9331b8cfc5abe4e92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customLocationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edgeDeviceId")
    def edge_device_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeDeviceId"))

    @edge_device_id.setter
    def edge_device_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b55d6fd18c8a2184f3e549324dc9e4a558cf090d17e3fed106bfea6b5d1d160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeDeviceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stackHciClusterId")
    def stack_hci_cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stackHciClusterId"))

    @stack_hci_cluster_id.setter
    def stack_hci_cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28cbd5c5a7d78cbe92e2615ed07c3134535a0692e76c51aecb15e8ef87b67775)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stackHciClusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bd6a7bb44b16edc994b41f8eaf883c088a5d11864a2205ae0793137cfda9b14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MobileNetworkPacketCoreControlPlanePlatform]:
        return typing.cast(typing.Optional[MobileNetworkPacketCoreControlPlanePlatform], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MobileNetworkPacketCoreControlPlanePlatform],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5035507910e264e4c286a88419c38c0c7bbad7765ec43db0a96f944e07077c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkPacketCoreControlPlane.MobileNetworkPacketCoreControlPlaneTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MobileNetworkPacketCoreControlPlaneTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#create MobileNetworkPacketCoreControlPlane#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#delete MobileNetworkPacketCoreControlPlane#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#read MobileNetworkPacketCoreControlPlane#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#update MobileNetworkPacketCoreControlPlane#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c601d5fe8b6c2abee8993aa0846989e42de013986f5655434a129ec5d3babe1)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#create MobileNetworkPacketCoreControlPlane#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#delete MobileNetworkPacketCoreControlPlane#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#read MobileNetworkPacketCoreControlPlane#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_control_plane#update MobileNetworkPacketCoreControlPlane#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkPacketCoreControlPlaneTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MobileNetworkPacketCoreControlPlaneTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkPacketCoreControlPlane.MobileNetworkPacketCoreControlPlaneTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75b21319188e1515eee24f390a98e22a251f816609e9fac93653bc0d6d670bb8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8234a49f9598be6098d0fc4950cec8a48bfc20d841f142fc41f1d01945110f35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41767ecce9985fa1641629aeb185868d203df35da494401b62095b27362b7ef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab4ca948de7d577eae226a2a45165ba48bace8e54515831336ff489acaf08d8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22328f94052aa11b02895ea47e262b52055687021d0a077d8ba9a0de55d2f17d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkPacketCoreControlPlaneTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkPacketCoreControlPlaneTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkPacketCoreControlPlaneTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6100460ab88dc211fc17d1225d79b428f9b414901a62d37450b6145f1a6f5b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MobileNetworkPacketCoreControlPlane",
    "MobileNetworkPacketCoreControlPlaneConfig",
    "MobileNetworkPacketCoreControlPlaneIdentity",
    "MobileNetworkPacketCoreControlPlaneIdentityOutputReference",
    "MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccess",
    "MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccessOutputReference",
    "MobileNetworkPacketCoreControlPlanePlatform",
    "MobileNetworkPacketCoreControlPlanePlatformOutputReference",
    "MobileNetworkPacketCoreControlPlaneTimeouts",
    "MobileNetworkPacketCoreControlPlaneTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c5866ab3433446e08a892c543d1e04bffa0a2eeb5ce7b809c33bd65adeb8deb5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    local_diagnostics_access: typing.Union[MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccess, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    site_ids: typing.Sequence[builtins.str],
    sku: builtins.str,
    control_plane_access_ipv4_address: typing.Optional[builtins.str] = None,
    control_plane_access_ipv4_gateway: typing.Optional[builtins.str] = None,
    control_plane_access_ipv4_subnet: typing.Optional[builtins.str] = None,
    control_plane_access_name: typing.Optional[builtins.str] = None,
    core_network_technology: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[MobileNetworkPacketCoreControlPlaneIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    interoperability_settings_json: typing.Optional[builtins.str] = None,
    platform: typing.Optional[typing.Union[MobileNetworkPacketCoreControlPlanePlatform, typing.Dict[builtins.str, typing.Any]]] = None,
    software_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MobileNetworkPacketCoreControlPlaneTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_equipment_mtu_in_bytes: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__46a20ebfd6c09daedfd93a54427f309fe85e3e90cb759192548461fbfda60f7f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd3569ac1257117a1c396fbd9f3bb65f2bd69a18211221c920e706742d0cde5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f650116fb36886d5fadd5bca6b9649262152706dd8a6f4e6bd60ddf906ce6b29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c08a346c5fa033e12c687d4d9c706322c3e6c115356c54d23d7a4e42e901a4a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6185d3270f48d0d9fb61cd5380501d8c49eb49c7c4a21fb21fcd34a26a1dfab5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9682db61276738ec742730843267751089e246b79ede16a405757254cd71ef6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6101c623d2d9d39e48a72e3ac6965edfec8b15a0fd2dba36942f2be9506fc711(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__149f093a31c85c6375c7a2091081f60950bc925d40b96eb50b940c14d7ac4cf6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a36c6ffe49f39fff3cb16bd2d8e5aeceb7d1cba94ce3d808c211800b54c90241(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56ab8979676b6ece4335a2f220155ce901fe60d4f19d1d890d4811aa7d1f1d55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__341d1143d3145aa0a9bfe84be1163f8e495c107e62a146a8559588373a8dcac0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4730bb48cec5dc36ee1064f014e7755f203713fdab7f87949cd4dbc415b4d50(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c57c895182a416ed8e44e570f8ad47d08fb81cac93d6e3d8bfde10f69d38c00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b38897d6f048ce89def67fe28ea47bbb10af70141b36a636cdc636298efb93e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cfc4dd81032d86f79a4c94fd82152854df00fa887d2f260d199ddf370a876c8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4c034bc1cd1fddf5af3ae9afd1cf85b274c565691d28c3c0bb2ed2dde7ceed4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f9720385d983f8e2b63b330ac8b1b807548f37aeb7db285e5c780414e0048a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    local_diagnostics_access: typing.Union[MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccess, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    site_ids: typing.Sequence[builtins.str],
    sku: builtins.str,
    control_plane_access_ipv4_address: typing.Optional[builtins.str] = None,
    control_plane_access_ipv4_gateway: typing.Optional[builtins.str] = None,
    control_plane_access_ipv4_subnet: typing.Optional[builtins.str] = None,
    control_plane_access_name: typing.Optional[builtins.str] = None,
    core_network_technology: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[MobileNetworkPacketCoreControlPlaneIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    interoperability_settings_json: typing.Optional[builtins.str] = None,
    platform: typing.Optional[typing.Union[MobileNetworkPacketCoreControlPlanePlatform, typing.Dict[builtins.str, typing.Any]]] = None,
    software_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MobileNetworkPacketCoreControlPlaneTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_equipment_mtu_in_bytes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0557b408bece11221f25d38ca623b70853b82d8953f6a8e399d345f591698641(
    *,
    identity_ids: typing.Sequence[builtins.str],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb77a590eb46b72a8acff4f0f02fb87d8ea20ec93ae95efb79045b662cef526a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c28da3d668910c42955fee504519fbcd9a3061d851e33a0dfd15306773ee91e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__425835c6765ba3de5de647dde046ca5bf1f71a7a25eb65f45d569df0956b2e1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a0c031a9cd8de63007a5467bf61f539a6ce952149c30af017714fc5b77ee7e6(
    value: typing.Optional[MobileNetworkPacketCoreControlPlaneIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94dcaccc61f12b8c8edad97654a0082c58120efca4b807feda6d346c935a3b02(
    *,
    authentication_type: builtins.str,
    https_server_certificate_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcefb54e5196b017376a7552154f5119d05b698cc62d0cdb2386ff510793aa3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__075c2ad3e14527f0a26c552f952f1f8f792e6d5a1da4f98fc285182bad4b5df2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bbe603fbbf7ccc49bd83dfbf6c3833da2ff8b13ae944b15d99928399b713097(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ac30eb31375e925a5f5171e4143e10cf10c4f704ff69478165e5394f19af35(
    value: typing.Optional[MobileNetworkPacketCoreControlPlaneLocalDiagnosticsAccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c49746bca557a5346c79f9892ae217c9eac5226a4559fe17390798e50c8602a(
    *,
    type: builtins.str,
    arc_kubernetes_cluster_id: typing.Optional[builtins.str] = None,
    custom_location_id: typing.Optional[builtins.str] = None,
    edge_device_id: typing.Optional[builtins.str] = None,
    stack_hci_cluster_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5487452b25d242dd3a2f8952524c81780420c5bdb5ef6e3f61411d4fa2689051(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1486f69e8244dbaa817503bb4f6b6c778bda21752ec5ee0c94513190e95c9bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__703dcc36d33d49efd260094cb52414232981bf23a7494ea9331b8cfc5abe4e92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b55d6fd18c8a2184f3e549324dc9e4a558cf090d17e3fed106bfea6b5d1d160(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28cbd5c5a7d78cbe92e2615ed07c3134535a0692e76c51aecb15e8ef87b67775(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd6a7bb44b16edc994b41f8eaf883c088a5d11864a2205ae0793137cfda9b14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5035507910e264e4c286a88419c38c0c7bbad7765ec43db0a96f944e07077c0(
    value: typing.Optional[MobileNetworkPacketCoreControlPlanePlatform],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c601d5fe8b6c2abee8993aa0846989e42de013986f5655434a129ec5d3babe1(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b21319188e1515eee24f390a98e22a251f816609e9fac93653bc0d6d670bb8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8234a49f9598be6098d0fc4950cec8a48bfc20d841f142fc41f1d01945110f35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41767ecce9985fa1641629aeb185868d203df35da494401b62095b27362b7ef6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab4ca948de7d577eae226a2a45165ba48bace8e54515831336ff489acaf08d8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22328f94052aa11b02895ea47e262b52055687021d0a077d8ba9a0de55d2f17d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6100460ab88dc211fc17d1225d79b428f9b414901a62d37450b6145f1a6f5b8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkPacketCoreControlPlaneTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
