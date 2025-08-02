r'''
# `opentelekomcloud_direct_connect_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_direct_connect_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2).
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


class DirectConnectV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.directConnectV2.DirectConnectV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2 opentelekomcloud_direct_connect_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        provider_name: builtins.str,
        admin_state_up: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bandwidth: typing.Optional[jsii.Number] = None,
        charge_mode: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        device_id: typing.Optional[builtins.str] = None,
        hosting_id: typing.Optional[builtins.str] = None,
        interface_name: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        order_id: typing.Optional[builtins.str] = None,
        peer_location: typing.Optional[builtins.str] = None,
        port_type: typing.Optional[builtins.str] = None,
        product_id: typing.Optional[builtins.str] = None,
        provider_status: typing.Optional[builtins.str] = None,
        redundant_id: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DirectConnectV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        vlan: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2 opentelekomcloud_direct_connect_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param provider_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#provider_name DirectConnectV2#provider_name}.
        :param admin_state_up: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#admin_state_up DirectConnectV2#admin_state_up}.
        :param bandwidth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#bandwidth DirectConnectV2#bandwidth}.
        :param charge_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#charge_mode DirectConnectV2#charge_mode}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#description DirectConnectV2#description}.
        :param device_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#device_id DirectConnectV2#device_id}.
        :param hosting_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#hosting_id DirectConnectV2#hosting_id}.
        :param interface_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#interface_name DirectConnectV2#interface_name}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#location DirectConnectV2#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#name DirectConnectV2#name}.
        :param order_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#order_id DirectConnectV2#order_id}.
        :param peer_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#peer_location DirectConnectV2#peer_location}.
        :param port_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#port_type DirectConnectV2#port_type}.
        :param product_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#product_id DirectConnectV2#product_id}.
        :param provider_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#provider_status DirectConnectV2#provider_status}.
        :param redundant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#redundant_id DirectConnectV2#redundant_id}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#status DirectConnectV2#status}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#tenant_id DirectConnectV2#tenant_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#timeouts DirectConnectV2#timeouts}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#type DirectConnectV2#type}.
        :param vlan: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#vlan DirectConnectV2#vlan}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a36d60a6d84916c3c4ef76a746c3541aadc09187df670213fc3f8629cab66174)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DirectConnectV2Config(
            provider_name=provider_name,
            admin_state_up=admin_state_up,
            bandwidth=bandwidth,
            charge_mode=charge_mode,
            description=description,
            device_id=device_id,
            hosting_id=hosting_id,
            interface_name=interface_name,
            location=location,
            name=name,
            order_id=order_id,
            peer_location=peer_location,
            port_type=port_type,
            product_id=product_id,
            provider_status=provider_status,
            redundant_id=redundant_id,
            status=status,
            tenant_id=tenant_id,
            timeouts=timeouts,
            type=type,
            vlan=vlan,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a DirectConnectV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DirectConnectV2 to import.
        :param import_from_id: The id of the existing DirectConnectV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DirectConnectV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31e9b04b3404ecca10e8697b4ead76b025daaeb79a858c1dffca63dcdc757271)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#create DirectConnectV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#delete DirectConnectV2#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#update DirectConnectV2#update}.
        '''
        value = DirectConnectV2Timeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdminStateUp")
    def reset_admin_state_up(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminStateUp", []))

    @jsii.member(jsii_name="resetBandwidth")
    def reset_bandwidth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidth", []))

    @jsii.member(jsii_name="resetChargeMode")
    def reset_charge_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChargeMode", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDeviceId")
    def reset_device_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceId", []))

    @jsii.member(jsii_name="resetHostingId")
    def reset_hosting_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostingId", []))

    @jsii.member(jsii_name="resetInterfaceName")
    def reset_interface_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterfaceName", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOrderId")
    def reset_order_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrderId", []))

    @jsii.member(jsii_name="resetPeerLocation")
    def reset_peer_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerLocation", []))

    @jsii.member(jsii_name="resetPortType")
    def reset_port_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortType", []))

    @jsii.member(jsii_name="resetProductId")
    def reset_product_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProductId", []))

    @jsii.member(jsii_name="resetProviderStatus")
    def reset_provider_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProviderStatus", []))

    @jsii.member(jsii_name="resetRedundantId")
    def reset_redundant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedundantId", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetTenantId")
    def reset_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetVlan")
    def reset_vlan(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVlan", []))

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
    @jsii.member(jsii_name="applicant")
    def applicant(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicant"))

    @builtins.property
    @jsii.member(jsii_name="applyTime")
    def apply_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applyTime"))

    @builtins.property
    @jsii.member(jsii_name="buildingLineProductId")
    def building_line_product_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildingLineProductId"))

    @builtins.property
    @jsii.member(jsii_name="cableLabel")
    def cable_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cableLabel"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="deleteTime")
    def delete_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteTime"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="lagId")
    def lag_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lagId"))

    @builtins.property
    @jsii.member(jsii_name="lastOnestopProductId")
    def last_onestop_product_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastOnestopProductId"))

    @builtins.property
    @jsii.member(jsii_name="mobile")
    def mobile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mobile"))

    @builtins.property
    @jsii.member(jsii_name="onestopProductId")
    def onestop_product_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onestopProductId"))

    @builtins.property
    @jsii.member(jsii_name="peerPortType")
    def peer_port_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerPortType"))

    @builtins.property
    @jsii.member(jsii_name="peerProvider")
    def peer_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerProvider"))

    @builtins.property
    @jsii.member(jsii_name="periodNum")
    def period_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodNum"))

    @builtins.property
    @jsii.member(jsii_name="periodType")
    def period_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodType"))

    @builtins.property
    @jsii.member(jsii_name="reason")
    def reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reason"))

    @builtins.property
    @jsii.member(jsii_name="regionId")
    def region_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionId"))

    @builtins.property
    @jsii.member(jsii_name="serviceKey")
    def service_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceKey"))

    @builtins.property
    @jsii.member(jsii_name="specCode")
    def spec_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "specCode"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DirectConnectV2TimeoutsOutputReference":
        return typing.cast("DirectConnectV2TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vgwType")
    def vgw_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vgwType"))

    @builtins.property
    @jsii.member(jsii_name="adminStateUpInput")
    def admin_state_up_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "adminStateUpInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthInput")
    def bandwidth_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bandwidthInput"))

    @builtins.property
    @jsii.member(jsii_name="chargeModeInput")
    def charge_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "chargeModeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceIdInput")
    def device_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="hostingIdInput")
    def hosting_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostingIdInput"))

    @builtins.property
    @jsii.member(jsii_name="interfaceNameInput")
    def interface_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interfaceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="orderIdInput")
    def order_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="peerLocationInput")
    def peer_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="portTypeInput")
    def port_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="productIdInput")
    def product_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "productIdInput"))

    @builtins.property
    @jsii.member(jsii_name="providerNameInput")
    def provider_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="providerStatusInput")
    def provider_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="redundantIdInput")
    def redundant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redundantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DirectConnectV2Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DirectConnectV2Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="vlanInput")
    def vlan_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vlanInput"))

    @builtins.property
    @jsii.member(jsii_name="adminStateUp")
    def admin_state_up(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "adminStateUp"))

    @admin_state_up.setter
    def admin_state_up(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ecfc61f430bbbddb7ce33f59b7bae93eafd2d8b3485ddd65078c5c8e3a02a0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminStateUp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bandwidth")
    def bandwidth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bandwidth"))

    @bandwidth.setter
    def bandwidth(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1999b97167945da30863de82941ec3996be1ca2e45c3ae6f05601b311a13b6f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="chargeMode")
    def charge_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "chargeMode"))

    @charge_mode.setter
    def charge_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd021f05abff8d8e84983a8e4581f395ddda139c05e2319dfbf658e5b76895f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "chargeMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b436360ac8f1dde48ad7ababa2b6870d077ead4d2734c6b94bf1f2b1ec589e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceId")
    def device_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceId"))

    @device_id.setter
    def device_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a55315c89cbaba2764e1f165f7b8289041c40c5ad27ff31134feb50ea6b94dbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostingId")
    def hosting_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostingId"))

    @hosting_id.setter
    def hosting_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51d9f080ee1af2bbb8f61377a3232fecd385719b3f5eb351237165058563c289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostingId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interfaceName")
    def interface_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interfaceName"))

    @interface_name.setter
    def interface_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__822ebf31ce409959c33f340482f2c922d50f1fbf6769f44e4631d66c349708b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interfaceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f26b1aa3664a600d8c5c43dbe01b652d7a03e0ea89dfdc35730a427c367f9266)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__654061cae9a0ce6080e34f4d7704d79eb03840ba207eae2843b1dc7aea1042ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orderId")
    def order_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orderId"))

    @order_id.setter
    def order_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a37e9559c1c63094f47d7ac4bb0a17b302c6ffeeae99f9ed2a21c6cc21ab0f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orderId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerLocation")
    def peer_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerLocation"))

    @peer_location.setter
    def peer_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3dbb8c07d3d3fe036e44e7d3777ce0d5eaacdc8a8cf5ee8bca49781e36875b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portType")
    def port_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portType"))

    @port_type.setter
    def port_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61759444ec02c931b72bccf5062aa65687f25f2ed5f4825d30b8fbe6fd9f09f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="productId")
    def product_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "productId"))

    @product_id.setter
    def product_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51041fcea9a17ceecb8ba2aa3b6ffd2875efdb3cca229b47ad612729eb035a03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerName"))

    @provider_name.setter
    def provider_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__214e1c3236292df988c3167f0f871f7a9d196501012f1fb6ce7a911bd1741bcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="providerStatus")
    def provider_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerStatus"))

    @provider_status.setter
    def provider_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eac2a38b8047a9ed74a453b1c3dfe87c8a3f38a21d6469689cc78113ff0413f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="redundantId")
    def redundant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redundantId"))

    @redundant_id.setter
    def redundant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63604ce494ebdb645a6644ed152e1548da036ce01309b9735d998725fe36b67f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redundantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99faa23ea491647fdb830e3de906627cb8acd2b1e9d1191bda72fb14f4d24fcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6acd1ab570bdfcb11cfbacd8e511f599b6bb9c1175704fbc6c28df574827e31d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__920cf5d1f0be79d6c76e6bfb2839335f31bff73ee0ac8b33be933049a208cf09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vlan")
    def vlan(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vlan"))

    @vlan.setter
    def vlan(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4e51a6f84ff7bb63fe769e103e6b267a75a88032bc73a7d2fdf136b4e9d9c82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vlan", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.directConnectV2.DirectConnectV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "provider_name": "providerName",
        "admin_state_up": "adminStateUp",
        "bandwidth": "bandwidth",
        "charge_mode": "chargeMode",
        "description": "description",
        "device_id": "deviceId",
        "hosting_id": "hostingId",
        "interface_name": "interfaceName",
        "location": "location",
        "name": "name",
        "order_id": "orderId",
        "peer_location": "peerLocation",
        "port_type": "portType",
        "product_id": "productId",
        "provider_status": "providerStatus",
        "redundant_id": "redundantId",
        "status": "status",
        "tenant_id": "tenantId",
        "timeouts": "timeouts",
        "type": "type",
        "vlan": "vlan",
    },
)
class DirectConnectV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        provider_name: builtins.str,
        admin_state_up: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bandwidth: typing.Optional[jsii.Number] = None,
        charge_mode: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        device_id: typing.Optional[builtins.str] = None,
        hosting_id: typing.Optional[builtins.str] = None,
        interface_name: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        order_id: typing.Optional[builtins.str] = None,
        peer_location: typing.Optional[builtins.str] = None,
        port_type: typing.Optional[builtins.str] = None,
        product_id: typing.Optional[builtins.str] = None,
        provider_status: typing.Optional[builtins.str] = None,
        redundant_id: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DirectConnectV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        vlan: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param provider_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#provider_name DirectConnectV2#provider_name}.
        :param admin_state_up: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#admin_state_up DirectConnectV2#admin_state_up}.
        :param bandwidth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#bandwidth DirectConnectV2#bandwidth}.
        :param charge_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#charge_mode DirectConnectV2#charge_mode}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#description DirectConnectV2#description}.
        :param device_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#device_id DirectConnectV2#device_id}.
        :param hosting_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#hosting_id DirectConnectV2#hosting_id}.
        :param interface_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#interface_name DirectConnectV2#interface_name}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#location DirectConnectV2#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#name DirectConnectV2#name}.
        :param order_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#order_id DirectConnectV2#order_id}.
        :param peer_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#peer_location DirectConnectV2#peer_location}.
        :param port_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#port_type DirectConnectV2#port_type}.
        :param product_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#product_id DirectConnectV2#product_id}.
        :param provider_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#provider_status DirectConnectV2#provider_status}.
        :param redundant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#redundant_id DirectConnectV2#redundant_id}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#status DirectConnectV2#status}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#tenant_id DirectConnectV2#tenant_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#timeouts DirectConnectV2#timeouts}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#type DirectConnectV2#type}.
        :param vlan: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#vlan DirectConnectV2#vlan}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DirectConnectV2Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a445141274699c3e2f8d58d6f7765dc8a47b8223b7b87eb935aa45a9519ae3f4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument provider_name", value=provider_name, expected_type=type_hints["provider_name"])
            check_type(argname="argument admin_state_up", value=admin_state_up, expected_type=type_hints["admin_state_up"])
            check_type(argname="argument bandwidth", value=bandwidth, expected_type=type_hints["bandwidth"])
            check_type(argname="argument charge_mode", value=charge_mode, expected_type=type_hints["charge_mode"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument device_id", value=device_id, expected_type=type_hints["device_id"])
            check_type(argname="argument hosting_id", value=hosting_id, expected_type=type_hints["hosting_id"])
            check_type(argname="argument interface_name", value=interface_name, expected_type=type_hints["interface_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument order_id", value=order_id, expected_type=type_hints["order_id"])
            check_type(argname="argument peer_location", value=peer_location, expected_type=type_hints["peer_location"])
            check_type(argname="argument port_type", value=port_type, expected_type=type_hints["port_type"])
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
            check_type(argname="argument provider_status", value=provider_status, expected_type=type_hints["provider_status"])
            check_type(argname="argument redundant_id", value=redundant_id, expected_type=type_hints["redundant_id"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument vlan", value=vlan, expected_type=type_hints["vlan"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "provider_name": provider_name,
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
        if admin_state_up is not None:
            self._values["admin_state_up"] = admin_state_up
        if bandwidth is not None:
            self._values["bandwidth"] = bandwidth
        if charge_mode is not None:
            self._values["charge_mode"] = charge_mode
        if description is not None:
            self._values["description"] = description
        if device_id is not None:
            self._values["device_id"] = device_id
        if hosting_id is not None:
            self._values["hosting_id"] = hosting_id
        if interface_name is not None:
            self._values["interface_name"] = interface_name
        if location is not None:
            self._values["location"] = location
        if name is not None:
            self._values["name"] = name
        if order_id is not None:
            self._values["order_id"] = order_id
        if peer_location is not None:
            self._values["peer_location"] = peer_location
        if port_type is not None:
            self._values["port_type"] = port_type
        if product_id is not None:
            self._values["product_id"] = product_id
        if provider_status is not None:
            self._values["provider_status"] = provider_status
        if redundant_id is not None:
            self._values["redundant_id"] = redundant_id
        if status is not None:
            self._values["status"] = status
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if type is not None:
            self._values["type"] = type
        if vlan is not None:
            self._values["vlan"] = vlan

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
    def provider_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#provider_name DirectConnectV2#provider_name}.'''
        result = self._values.get("provider_name")
        assert result is not None, "Required property 'provider_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def admin_state_up(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#admin_state_up DirectConnectV2#admin_state_up}.'''
        result = self._values.get("admin_state_up")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def bandwidth(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#bandwidth DirectConnectV2#bandwidth}.'''
        result = self._values.get("bandwidth")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def charge_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#charge_mode DirectConnectV2#charge_mode}.'''
        result = self._values.get("charge_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#description DirectConnectV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#device_id DirectConnectV2#device_id}.'''
        result = self._values.get("device_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hosting_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#hosting_id DirectConnectV2#hosting_id}.'''
        result = self._values.get("hosting_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interface_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#interface_name DirectConnectV2#interface_name}.'''
        result = self._values.get("interface_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#location DirectConnectV2#location}.'''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#name DirectConnectV2#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def order_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#order_id DirectConnectV2#order_id}.'''
        result = self._values.get("order_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#peer_location DirectConnectV2#peer_location}.'''
        result = self._values.get("peer_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#port_type DirectConnectV2#port_type}.'''
        result = self._values.get("port_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def product_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#product_id DirectConnectV2#product_id}.'''
        result = self._values.get("product_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#provider_status DirectConnectV2#provider_status}.'''
        result = self._values.get("provider_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redundant_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#redundant_id DirectConnectV2#redundant_id}.'''
        result = self._values.get("redundant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#status DirectConnectV2#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#tenant_id DirectConnectV2#tenant_id}.'''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DirectConnectV2Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#timeouts DirectConnectV2#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DirectConnectV2Timeouts"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#type DirectConnectV2#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vlan(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#vlan DirectConnectV2#vlan}.'''
        result = self._values.get("vlan")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DirectConnectV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.directConnectV2.DirectConnectV2Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DirectConnectV2Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#create DirectConnectV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#delete DirectConnectV2#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#update DirectConnectV2#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da5fad7489259c6ff6c8424a7fe83149ad5d5d1324dd835f7fd721afa043d2db)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#create DirectConnectV2#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#delete DirectConnectV2#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/direct_connect_v2#update DirectConnectV2#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DirectConnectV2Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DirectConnectV2TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.directConnectV2.DirectConnectV2TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09c3fe9c7c0914d3d3eb34e92ef2fd463847561b855b06bf9235954f6b826d46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7539ef0db460624d3be7bdd36bc65cd50bea2e054a6295ce8eff91198e9cb019)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63db447bc9db4c9ce640e0ead579b12fbaeddbd0d811dfa69032c333b099d3fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6bd2238fbb1abf20478080d824fc52d6037a94514fde49ce0bdc3e3f4af4b82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DirectConnectV2Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DirectConnectV2Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DirectConnectV2Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e0dbc3ed40f0bb53cc2a23847eed93852c8ffaba0848fc87b44ecce60b06299)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DirectConnectV2",
    "DirectConnectV2Config",
    "DirectConnectV2Timeouts",
    "DirectConnectV2TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a36d60a6d84916c3c4ef76a746c3541aadc09187df670213fc3f8629cab66174(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    provider_name: builtins.str,
    admin_state_up: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bandwidth: typing.Optional[jsii.Number] = None,
    charge_mode: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    device_id: typing.Optional[builtins.str] = None,
    hosting_id: typing.Optional[builtins.str] = None,
    interface_name: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    order_id: typing.Optional[builtins.str] = None,
    peer_location: typing.Optional[builtins.str] = None,
    port_type: typing.Optional[builtins.str] = None,
    product_id: typing.Optional[builtins.str] = None,
    provider_status: typing.Optional[builtins.str] = None,
    redundant_id: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DirectConnectV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
    vlan: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__31e9b04b3404ecca10e8697b4ead76b025daaeb79a858c1dffca63dcdc757271(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ecfc61f430bbbddb7ce33f59b7bae93eafd2d8b3485ddd65078c5c8e3a02a0f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1999b97167945da30863de82941ec3996be1ca2e45c3ae6f05601b311a13b6f8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd021f05abff8d8e84983a8e4581f395ddda139c05e2319dfbf658e5b76895f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b436360ac8f1dde48ad7ababa2b6870d077ead4d2734c6b94bf1f2b1ec589e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55315c89cbaba2764e1f165f7b8289041c40c5ad27ff31134feb50ea6b94dbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51d9f080ee1af2bbb8f61377a3232fecd385719b3f5eb351237165058563c289(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__822ebf31ce409959c33f340482f2c922d50f1fbf6769f44e4631d66c349708b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f26b1aa3664a600d8c5c43dbe01b652d7a03e0ea89dfdc35730a427c367f9266(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__654061cae9a0ce6080e34f4d7704d79eb03840ba207eae2843b1dc7aea1042ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a37e9559c1c63094f47d7ac4bb0a17b302c6ffeeae99f9ed2a21c6cc21ab0f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3dbb8c07d3d3fe036e44e7d3777ce0d5eaacdc8a8cf5ee8bca49781e36875b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61759444ec02c931b72bccf5062aa65687f25f2ed5f4825d30b8fbe6fd9f09f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51041fcea9a17ceecb8ba2aa3b6ffd2875efdb3cca229b47ad612729eb035a03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__214e1c3236292df988c3167f0f871f7a9d196501012f1fb6ce7a911bd1741bcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac2a38b8047a9ed74a453b1c3dfe87c8a3f38a21d6469689cc78113ff0413f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63604ce494ebdb645a6644ed152e1548da036ce01309b9735d998725fe36b67f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99faa23ea491647fdb830e3de906627cb8acd2b1e9d1191bda72fb14f4d24fcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6acd1ab570bdfcb11cfbacd8e511f599b6bb9c1175704fbc6c28df574827e31d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__920cf5d1f0be79d6c76e6bfb2839335f31bff73ee0ac8b33be933049a208cf09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4e51a6f84ff7bb63fe769e103e6b267a75a88032bc73a7d2fdf136b4e9d9c82(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a445141274699c3e2f8d58d6f7765dc8a47b8223b7b87eb935aa45a9519ae3f4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    provider_name: builtins.str,
    admin_state_up: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bandwidth: typing.Optional[jsii.Number] = None,
    charge_mode: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    device_id: typing.Optional[builtins.str] = None,
    hosting_id: typing.Optional[builtins.str] = None,
    interface_name: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    order_id: typing.Optional[builtins.str] = None,
    peer_location: typing.Optional[builtins.str] = None,
    port_type: typing.Optional[builtins.str] = None,
    product_id: typing.Optional[builtins.str] = None,
    provider_status: typing.Optional[builtins.str] = None,
    redundant_id: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DirectConnectV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
    vlan: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da5fad7489259c6ff6c8424a7fe83149ad5d5d1324dd835f7fd721afa043d2db(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09c3fe9c7c0914d3d3eb34e92ef2fd463847561b855b06bf9235954f6b826d46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7539ef0db460624d3be7bdd36bc65cd50bea2e054a6295ce8eff91198e9cb019(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63db447bc9db4c9ce640e0ead579b12fbaeddbd0d811dfa69032c333b099d3fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6bd2238fbb1abf20478080d824fc52d6037a94514fde49ce0bdc3e3f4af4b82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e0dbc3ed40f0bb53cc2a23847eed93852c8ffaba0848fc87b44ecce60b06299(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DirectConnectV2Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
