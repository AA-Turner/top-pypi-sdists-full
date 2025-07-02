r'''
# `azurerm_mobile_network_sim`

Refer to the Terraform Registry for docs: [`azurerm_mobile_network_sim`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim).
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


class MobileNetworkSim(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkSim.MobileNetworkSim",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim azurerm_mobile_network_sim}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        authentication_key: builtins.str,
        integrated_circuit_card_identifier: builtins.str,
        international_mobile_subscriber_identity: builtins.str,
        mobile_network_sim_group_id: builtins.str,
        name: builtins.str,
        operator_key_code: builtins.str,
        device_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        sim_policy_id: typing.Optional[builtins.str] = None,
        static_ip_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MobileNetworkSimStaticIpConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["MobileNetworkSimTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim azurerm_mobile_network_sim} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param authentication_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#authentication_key MobileNetworkSim#authentication_key}.
        :param integrated_circuit_card_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#integrated_circuit_card_identifier MobileNetworkSim#integrated_circuit_card_identifier}.
        :param international_mobile_subscriber_identity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#international_mobile_subscriber_identity MobileNetworkSim#international_mobile_subscriber_identity}.
        :param mobile_network_sim_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#mobile_network_sim_group_id MobileNetworkSim#mobile_network_sim_group_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#name MobileNetworkSim#name}.
        :param operator_key_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#operator_key_code MobileNetworkSim#operator_key_code}.
        :param device_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#device_type MobileNetworkSim#device_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#id MobileNetworkSim#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param sim_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#sim_policy_id MobileNetworkSim#sim_policy_id}.
        :param static_ip_configuration: static_ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#static_ip_configuration MobileNetworkSim#static_ip_configuration}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#timeouts MobileNetworkSim#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f25d5adfd4476b5cebc8f16cce1b2c066621ae1a075aef229daae69afe4f87d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MobileNetworkSimConfig(
            authentication_key=authentication_key,
            integrated_circuit_card_identifier=integrated_circuit_card_identifier,
            international_mobile_subscriber_identity=international_mobile_subscriber_identity,
            mobile_network_sim_group_id=mobile_network_sim_group_id,
            name=name,
            operator_key_code=operator_key_code,
            device_type=device_type,
            id=id,
            sim_policy_id=sim_policy_id,
            static_ip_configuration=static_ip_configuration,
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
        '''Generates CDKTF code for importing a MobileNetworkSim resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MobileNetworkSim to import.
        :param import_from_id: The id of the existing MobileNetworkSim that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MobileNetworkSim to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fdf0c9ae8d79be14932e762221315df98462c8cd414b78872dfe7900a3d2274)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putStaticIpConfiguration")
    def put_static_ip_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MobileNetworkSimStaticIpConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__190160648cef54373f3f3d2669a26442728738aea12fda28a5a8b45ba84ab254)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStaticIpConfiguration", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#create MobileNetworkSim#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#delete MobileNetworkSim#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#read MobileNetworkSim#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#update MobileNetworkSim#update}.
        '''
        value = MobileNetworkSimTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDeviceType")
    def reset_device_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceType", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSimPolicyId")
    def reset_sim_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSimPolicyId", []))

    @jsii.member(jsii_name="resetStaticIpConfiguration")
    def reset_static_ip_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStaticIpConfiguration", []))

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
    @jsii.member(jsii_name="simState")
    def sim_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "simState"))

    @builtins.property
    @jsii.member(jsii_name="staticIpConfiguration")
    def static_ip_configuration(self) -> "MobileNetworkSimStaticIpConfigurationList":
        return typing.cast("MobileNetworkSimStaticIpConfigurationList", jsii.get(self, "staticIpConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MobileNetworkSimTimeoutsOutputReference":
        return typing.cast("MobileNetworkSimTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vendorKeyFingerprint")
    def vendor_key_fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vendorKeyFingerprint"))

    @builtins.property
    @jsii.member(jsii_name="vendorName")
    def vendor_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vendorName"))

    @builtins.property
    @jsii.member(jsii_name="authenticationKeyInput")
    def authentication_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceTypeInput")
    def device_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="integratedCircuitCardIdentifierInput")
    def integrated_circuit_card_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integratedCircuitCardIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="internationalMobileSubscriberIdentityInput")
    def international_mobile_subscriber_identity_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "internationalMobileSubscriberIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="mobileNetworkSimGroupIdInput")
    def mobile_network_sim_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mobileNetworkSimGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorKeyCodeInput")
    def operator_key_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorKeyCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="simPolicyIdInput")
    def sim_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "simPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="staticIpConfigurationInput")
    def static_ip_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MobileNetworkSimStaticIpConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MobileNetworkSimStaticIpConfiguration"]]], jsii.get(self, "staticIpConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MobileNetworkSimTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MobileNetworkSimTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationKey")
    def authentication_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationKey"))

    @authentication_key.setter
    def authentication_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c3ef722974cc328d60bad1b6075d1c04d24efbe20ba6ac4d93170e8032dd0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceType")
    def device_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceType"))

    @device_type.setter
    def device_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da7f76001c0894726614f25bb49209747dae66ddae71fdb765d2564d0d8caa57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa5049f0841ecee87cfe1e7fb411a9f42424f6d68d9c19b0646b7ed9e62b2749)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integratedCircuitCardIdentifier")
    def integrated_circuit_card_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "integratedCircuitCardIdentifier"))

    @integrated_circuit_card_identifier.setter
    def integrated_circuit_card_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf4b9c618404ad155b8aa11bfdf78fc52046185461372037fc0cb591bf75b64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integratedCircuitCardIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internationalMobileSubscriberIdentity")
    def international_mobile_subscriber_identity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "internationalMobileSubscriberIdentity"))

    @international_mobile_subscriber_identity.setter
    def international_mobile_subscriber_identity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__331cd556f316a64b18e808e006dcfb9de7a1fcfc8d37f0339a8b00d9a4ccee73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internationalMobileSubscriberIdentity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mobileNetworkSimGroupId")
    def mobile_network_sim_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mobileNetworkSimGroupId"))

    @mobile_network_sim_group_id.setter
    def mobile_network_sim_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc40c88e625e2d77f4561209d10d27e8f1695370928e2e4b3ee808e4a653bcc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mobileNetworkSimGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__733063db2283dcdd94d34d4891c8dcebfd505967238bd7de4042bc6615c8faf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operatorKeyCode")
    def operator_key_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operatorKeyCode"))

    @operator_key_code.setter
    def operator_key_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e03cbc9add8332f57e6114652eeb0f6e58c168ef06696e4e110b65a8b317109e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operatorKeyCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="simPolicyId")
    def sim_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "simPolicyId"))

    @sim_policy_id.setter
    def sim_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f866c40fcdc4b5295b14b7ef30c4eb9ff28d08e790d85242192b1a2a2a73b1e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "simPolicyId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkSim.MobileNetworkSimConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "authentication_key": "authenticationKey",
        "integrated_circuit_card_identifier": "integratedCircuitCardIdentifier",
        "international_mobile_subscriber_identity": "internationalMobileSubscriberIdentity",
        "mobile_network_sim_group_id": "mobileNetworkSimGroupId",
        "name": "name",
        "operator_key_code": "operatorKeyCode",
        "device_type": "deviceType",
        "id": "id",
        "sim_policy_id": "simPolicyId",
        "static_ip_configuration": "staticIpConfiguration",
        "timeouts": "timeouts",
    },
)
class MobileNetworkSimConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        authentication_key: builtins.str,
        integrated_circuit_card_identifier: builtins.str,
        international_mobile_subscriber_identity: builtins.str,
        mobile_network_sim_group_id: builtins.str,
        name: builtins.str,
        operator_key_code: builtins.str,
        device_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        sim_policy_id: typing.Optional[builtins.str] = None,
        static_ip_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MobileNetworkSimStaticIpConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["MobileNetworkSimTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param authentication_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#authentication_key MobileNetworkSim#authentication_key}.
        :param integrated_circuit_card_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#integrated_circuit_card_identifier MobileNetworkSim#integrated_circuit_card_identifier}.
        :param international_mobile_subscriber_identity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#international_mobile_subscriber_identity MobileNetworkSim#international_mobile_subscriber_identity}.
        :param mobile_network_sim_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#mobile_network_sim_group_id MobileNetworkSim#mobile_network_sim_group_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#name MobileNetworkSim#name}.
        :param operator_key_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#operator_key_code MobileNetworkSim#operator_key_code}.
        :param device_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#device_type MobileNetworkSim#device_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#id MobileNetworkSim#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param sim_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#sim_policy_id MobileNetworkSim#sim_policy_id}.
        :param static_ip_configuration: static_ip_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#static_ip_configuration MobileNetworkSim#static_ip_configuration}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#timeouts MobileNetworkSim#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = MobileNetworkSimTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__782c9ef7a3615a4b3c7e4ac3cb2f1684697b302ab6e5fdf5add3550782d24ebc)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument authentication_key", value=authentication_key, expected_type=type_hints["authentication_key"])
            check_type(argname="argument integrated_circuit_card_identifier", value=integrated_circuit_card_identifier, expected_type=type_hints["integrated_circuit_card_identifier"])
            check_type(argname="argument international_mobile_subscriber_identity", value=international_mobile_subscriber_identity, expected_type=type_hints["international_mobile_subscriber_identity"])
            check_type(argname="argument mobile_network_sim_group_id", value=mobile_network_sim_group_id, expected_type=type_hints["mobile_network_sim_group_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument operator_key_code", value=operator_key_code, expected_type=type_hints["operator_key_code"])
            check_type(argname="argument device_type", value=device_type, expected_type=type_hints["device_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument sim_policy_id", value=sim_policy_id, expected_type=type_hints["sim_policy_id"])
            check_type(argname="argument static_ip_configuration", value=static_ip_configuration, expected_type=type_hints["static_ip_configuration"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authentication_key": authentication_key,
            "integrated_circuit_card_identifier": integrated_circuit_card_identifier,
            "international_mobile_subscriber_identity": international_mobile_subscriber_identity,
            "mobile_network_sim_group_id": mobile_network_sim_group_id,
            "name": name,
            "operator_key_code": operator_key_code,
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
        if device_type is not None:
            self._values["device_type"] = device_type
        if id is not None:
            self._values["id"] = id
        if sim_policy_id is not None:
            self._values["sim_policy_id"] = sim_policy_id
        if static_ip_configuration is not None:
            self._values["static_ip_configuration"] = static_ip_configuration
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
    def authentication_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#authentication_key MobileNetworkSim#authentication_key}.'''
        result = self._values.get("authentication_key")
        assert result is not None, "Required property 'authentication_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def integrated_circuit_card_identifier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#integrated_circuit_card_identifier MobileNetworkSim#integrated_circuit_card_identifier}.'''
        result = self._values.get("integrated_circuit_card_identifier")
        assert result is not None, "Required property 'integrated_circuit_card_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def international_mobile_subscriber_identity(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#international_mobile_subscriber_identity MobileNetworkSim#international_mobile_subscriber_identity}.'''
        result = self._values.get("international_mobile_subscriber_identity")
        assert result is not None, "Required property 'international_mobile_subscriber_identity' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mobile_network_sim_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#mobile_network_sim_group_id MobileNetworkSim#mobile_network_sim_group_id}.'''
        result = self._values.get("mobile_network_sim_group_id")
        assert result is not None, "Required property 'mobile_network_sim_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#name MobileNetworkSim#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator_key_code(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#operator_key_code MobileNetworkSim#operator_key_code}.'''
        result = self._values.get("operator_key_code")
        assert result is not None, "Required property 'operator_key_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def device_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#device_type MobileNetworkSim#device_type}.'''
        result = self._values.get("device_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#id MobileNetworkSim#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sim_policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#sim_policy_id MobileNetworkSim#sim_policy_id}.'''
        result = self._values.get("sim_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def static_ip_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MobileNetworkSimStaticIpConfiguration"]]]:
        '''static_ip_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#static_ip_configuration MobileNetworkSim#static_ip_configuration}
        '''
        result = self._values.get("static_ip_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MobileNetworkSimStaticIpConfiguration"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MobileNetworkSimTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#timeouts MobileNetworkSim#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MobileNetworkSimTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkSimConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkSim.MobileNetworkSimStaticIpConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "attached_data_network_id": "attachedDataNetworkId",
        "slice_id": "sliceId",
        "static_ipv4_address": "staticIpv4Address",
    },
)
class MobileNetworkSimStaticIpConfiguration:
    def __init__(
        self,
        *,
        attached_data_network_id: builtins.str,
        slice_id: builtins.str,
        static_ipv4_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param attached_data_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#attached_data_network_id MobileNetworkSim#attached_data_network_id}.
        :param slice_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#slice_id MobileNetworkSim#slice_id}.
        :param static_ipv4_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#static_ipv4_address MobileNetworkSim#static_ipv4_address}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49ec76a041f24378d04eb2a0d8fc261c984b39683d1e6879d856d30aa7747301)
            check_type(argname="argument attached_data_network_id", value=attached_data_network_id, expected_type=type_hints["attached_data_network_id"])
            check_type(argname="argument slice_id", value=slice_id, expected_type=type_hints["slice_id"])
            check_type(argname="argument static_ipv4_address", value=static_ipv4_address, expected_type=type_hints["static_ipv4_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attached_data_network_id": attached_data_network_id,
            "slice_id": slice_id,
        }
        if static_ipv4_address is not None:
            self._values["static_ipv4_address"] = static_ipv4_address

    @builtins.property
    def attached_data_network_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#attached_data_network_id MobileNetworkSim#attached_data_network_id}.'''
        result = self._values.get("attached_data_network_id")
        assert result is not None, "Required property 'attached_data_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slice_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#slice_id MobileNetworkSim#slice_id}.'''
        result = self._values.get("slice_id")
        assert result is not None, "Required property 'slice_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def static_ipv4_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#static_ipv4_address MobileNetworkSim#static_ipv4_address}.'''
        result = self._values.get("static_ipv4_address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkSimStaticIpConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MobileNetworkSimStaticIpConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkSim.MobileNetworkSimStaticIpConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cc27a9e478d6b1c3b1b02c7479115cffcd6a528bfbf62b6de04e93b81997090)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MobileNetworkSimStaticIpConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac8cf91b294869d2bb3b57d9cbf9146e2db46bbd463b8b147dffd1bf2db9ac75)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MobileNetworkSimStaticIpConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be338e5c9f9bcaafa7df5b5efbbea6ba8a7400e95e31b944ba12e4fe34d23c30)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0fc84a4ad49d809d0b1d037eddd32ef9d6b7c3255db6b3a03c4b2b490dd3139)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee46826f2486c45ff4ae8d91ab1d976664b4b3e286b4c0e2524f4508efdce061)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MobileNetworkSimStaticIpConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MobileNetworkSimStaticIpConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MobileNetworkSimStaticIpConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98a5f2af143a19d1b495e2a37b72e0ef99ae5cfbfa2ed8c987f2c31123fea568)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MobileNetworkSimStaticIpConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkSim.MobileNetworkSimStaticIpConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f607bc412b7b692863586d59d491584a2cf376b36ab127e7c32385bc4411c6c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetStaticIpv4Address")
    def reset_static_ipv4_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStaticIpv4Address", []))

    @builtins.property
    @jsii.member(jsii_name="attachedDataNetworkIdInput")
    def attached_data_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attachedDataNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sliceIdInput")
    def slice_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sliceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="staticIpv4AddressInput")
    def static_ipv4_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "staticIpv4AddressInput"))

    @builtins.property
    @jsii.member(jsii_name="attachedDataNetworkId")
    def attached_data_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attachedDataNetworkId"))

    @attached_data_network_id.setter
    def attached_data_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a2364da5cb8a83d043ebb5811512e8f780c6fb3be037188d2912a3a9c465115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attachedDataNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sliceId")
    def slice_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sliceId"))

    @slice_id.setter
    def slice_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d49d20740c857ed3c530226fff59c2254b1d8df7ed0b018fb579f7a375ddfa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sliceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="staticIpv4Address")
    def static_ipv4_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "staticIpv4Address"))

    @static_ipv4_address.setter
    def static_ipv4_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c12c3688f840fceef6f64ebadb9d90ee7b8fea773e8543b3a122c18daf31cdc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "staticIpv4Address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkSimStaticIpConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkSimStaticIpConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkSimStaticIpConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c268585070c5ed0b0057d1f632453f757617e2c02d72e89dcc2e08405f7d9ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkSim.MobileNetworkSimTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MobileNetworkSimTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#create MobileNetworkSim#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#delete MobileNetworkSim#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#read MobileNetworkSim#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#update MobileNetworkSim#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b0baa0a2ff013c9764c30df3a8325e6b13310ce39bf5e7f4d512243bd211336)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#create MobileNetworkSim#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#delete MobileNetworkSim#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#read MobileNetworkSim#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim#update MobileNetworkSim#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkSimTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MobileNetworkSimTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkSim.MobileNetworkSimTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3e54dd455fa73023679e683616ef45fc0d8cee195ffc58a2609284bac64f4ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__447df89038d558581a738958fbd73111462290dc8e0d79b5b7355d740bca4586)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ac6553a8c7b7b3909837cca3acec680213e81e4ff663b0b72b2487605f185db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed74441cec92acf1b8086ce116c0dc4e5ec864a23cea81118b287b2cdec6e7e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ffd30f1484e2a0fbe0e7b0c9c86ed5ccda53be3a5d62e2dc5db611cde2cfbe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkSimTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkSimTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkSimTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e95f39e098c7e0d321f0518d6f4b89cefe66bf35caa2da1a0b7f370490e6ded9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MobileNetworkSim",
    "MobileNetworkSimConfig",
    "MobileNetworkSimStaticIpConfiguration",
    "MobileNetworkSimStaticIpConfigurationList",
    "MobileNetworkSimStaticIpConfigurationOutputReference",
    "MobileNetworkSimTimeouts",
    "MobileNetworkSimTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__1f25d5adfd4476b5cebc8f16cce1b2c066621ae1a075aef229daae69afe4f87d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    authentication_key: builtins.str,
    integrated_circuit_card_identifier: builtins.str,
    international_mobile_subscriber_identity: builtins.str,
    mobile_network_sim_group_id: builtins.str,
    name: builtins.str,
    operator_key_code: builtins.str,
    device_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    sim_policy_id: typing.Optional[builtins.str] = None,
    static_ip_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MobileNetworkSimStaticIpConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[MobileNetworkSimTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3fdf0c9ae8d79be14932e762221315df98462c8cd414b78872dfe7900a3d2274(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__190160648cef54373f3f3d2669a26442728738aea12fda28a5a8b45ba84ab254(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MobileNetworkSimStaticIpConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c3ef722974cc328d60bad1b6075d1c04d24efbe20ba6ac4d93170e8032dd0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da7f76001c0894726614f25bb49209747dae66ddae71fdb765d2564d0d8caa57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa5049f0841ecee87cfe1e7fb411a9f42424f6d68d9c19b0646b7ed9e62b2749(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf4b9c618404ad155b8aa11bfdf78fc52046185461372037fc0cb591bf75b64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__331cd556f316a64b18e808e006dcfb9de7a1fcfc8d37f0339a8b00d9a4ccee73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc40c88e625e2d77f4561209d10d27e8f1695370928e2e4b3ee808e4a653bcc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__733063db2283dcdd94d34d4891c8dcebfd505967238bd7de4042bc6615c8faf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e03cbc9add8332f57e6114652eeb0f6e58c168ef06696e4e110b65a8b317109e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f866c40fcdc4b5295b14b7ef30c4eb9ff28d08e790d85242192b1a2a2a73b1e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__782c9ef7a3615a4b3c7e4ac3cb2f1684697b302ab6e5fdf5add3550782d24ebc(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    authentication_key: builtins.str,
    integrated_circuit_card_identifier: builtins.str,
    international_mobile_subscriber_identity: builtins.str,
    mobile_network_sim_group_id: builtins.str,
    name: builtins.str,
    operator_key_code: builtins.str,
    device_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    sim_policy_id: typing.Optional[builtins.str] = None,
    static_ip_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MobileNetworkSimStaticIpConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[MobileNetworkSimTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49ec76a041f24378d04eb2a0d8fc261c984b39683d1e6879d856d30aa7747301(
    *,
    attached_data_network_id: builtins.str,
    slice_id: builtins.str,
    static_ipv4_address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc27a9e478d6b1c3b1b02c7479115cffcd6a528bfbf62b6de04e93b81997090(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac8cf91b294869d2bb3b57d9cbf9146e2db46bbd463b8b147dffd1bf2db9ac75(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be338e5c9f9bcaafa7df5b5efbbea6ba8a7400e95e31b944ba12e4fe34d23c30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0fc84a4ad49d809d0b1d037eddd32ef9d6b7c3255db6b3a03c4b2b490dd3139(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee46826f2486c45ff4ae8d91ab1d976664b4b3e286b4c0e2524f4508efdce061(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a5f2af143a19d1b495e2a37b72e0ef99ae5cfbfa2ed8c987f2c31123fea568(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MobileNetworkSimStaticIpConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f607bc412b7b692863586d59d491584a2cf376b36ab127e7c32385bc4411c6c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2364da5cb8a83d043ebb5811512e8f780c6fb3be037188d2912a3a9c465115(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d49d20740c857ed3c530226fff59c2254b1d8df7ed0b018fb579f7a375ddfa2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c12c3688f840fceef6f64ebadb9d90ee7b8fea773e8543b3a122c18daf31cdc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c268585070c5ed0b0057d1f632453f757617e2c02d72e89dcc2e08405f7d9ac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkSimStaticIpConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b0baa0a2ff013c9764c30df3a8325e6b13310ce39bf5e7f4d512243bd211336(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e54dd455fa73023679e683616ef45fc0d8cee195ffc58a2609284bac64f4ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__447df89038d558581a738958fbd73111462290dc8e0d79b5b7355d740bca4586(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac6553a8c7b7b3909837cca3acec680213e81e4ff663b0b72b2487605f185db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed74441cec92acf1b8086ce116c0dc4e5ec864a23cea81118b287b2cdec6e7e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ffd30f1484e2a0fbe0e7b0c9c86ed5ccda53be3a5d62e2dc5db611cde2cfbe8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e95f39e098c7e0d321f0518d6f4b89cefe66bf35caa2da1a0b7f370490e6ded9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkSimTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
