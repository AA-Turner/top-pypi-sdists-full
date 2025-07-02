r'''
# `azurerm_express_route_port`

Refer to the Terraform Registry for docs: [`azurerm_express_route_port`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port).
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


class ExpressRoutePort(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.expressRoutePort.ExpressRoutePort",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port azurerm_express_route_port}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        bandwidth_in_gbps: jsii.Number,
        encapsulation: builtins.str,
        location: builtins.str,
        name: builtins.str,
        peering_location: builtins.str,
        resource_group_name: builtins.str,
        billing_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["ExpressRoutePortIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        link1: typing.Optional[typing.Union["ExpressRoutePortLink1", typing.Dict[builtins.str, typing.Any]]] = None,
        link2: typing.Optional[typing.Union["ExpressRoutePortLink2", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ExpressRoutePortTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port azurerm_express_route_port} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bandwidth_in_gbps: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#bandwidth_in_gbps ExpressRoutePort#bandwidth_in_gbps}.
        :param encapsulation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#encapsulation ExpressRoutePort#encapsulation}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#location ExpressRoutePort#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#name ExpressRoutePort#name}.
        :param peering_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#peering_location ExpressRoutePort#peering_location}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#resource_group_name ExpressRoutePort#resource_group_name}.
        :param billing_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#billing_type ExpressRoutePort#billing_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#id ExpressRoutePort#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#identity ExpressRoutePort#identity}
        :param link1: link1 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#link1 ExpressRoutePort#link1}
        :param link2: link2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#link2 ExpressRoutePort#link2}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#tags ExpressRoutePort#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#timeouts ExpressRoutePort#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee4b4c61b07aaf89a9c03a3efa7b448ff2a3520c2331665037f6dc808b76d6d1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ExpressRoutePortConfig(
            bandwidth_in_gbps=bandwidth_in_gbps,
            encapsulation=encapsulation,
            location=location,
            name=name,
            peering_location=peering_location,
            resource_group_name=resource_group_name,
            billing_type=billing_type,
            id=id,
            identity=identity,
            link1=link1,
            link2=link2,
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
        '''Generates CDKTF code for importing a ExpressRoutePort resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ExpressRoutePort to import.
        :param import_from_id: The id of the existing ExpressRoutePort that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ExpressRoutePort to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eb2fdd19c8e9359e0f4c23c677cffb43009f24f82948d018d06a835408aa254)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#type ExpressRoutePort#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#identity_ids ExpressRoutePort#identity_ids}.
        '''
        value = ExpressRoutePortIdentity(type=type, identity_ids=identity_ids)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putLink1")
    def put_link1(
        self,
        *,
        admin_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        macsec_cak_keyvault_secret_id: typing.Optional[builtins.str] = None,
        macsec_cipher: typing.Optional[builtins.str] = None,
        macsec_ckn_keyvault_secret_id: typing.Optional[builtins.str] = None,
        macsec_sci_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param admin_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#admin_enabled ExpressRoutePort#admin_enabled}.
        :param macsec_cak_keyvault_secret_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_cak_keyvault_secret_id ExpressRoutePort#macsec_cak_keyvault_secret_id}.
        :param macsec_cipher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_cipher ExpressRoutePort#macsec_cipher}.
        :param macsec_ckn_keyvault_secret_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_ckn_keyvault_secret_id ExpressRoutePort#macsec_ckn_keyvault_secret_id}.
        :param macsec_sci_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_sci_enabled ExpressRoutePort#macsec_sci_enabled}.
        '''
        value = ExpressRoutePortLink1(
            admin_enabled=admin_enabled,
            macsec_cak_keyvault_secret_id=macsec_cak_keyvault_secret_id,
            macsec_cipher=macsec_cipher,
            macsec_ckn_keyvault_secret_id=macsec_ckn_keyvault_secret_id,
            macsec_sci_enabled=macsec_sci_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putLink1", [value]))

    @jsii.member(jsii_name="putLink2")
    def put_link2(
        self,
        *,
        admin_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        macsec_cak_keyvault_secret_id: typing.Optional[builtins.str] = None,
        macsec_cipher: typing.Optional[builtins.str] = None,
        macsec_ckn_keyvault_secret_id: typing.Optional[builtins.str] = None,
        macsec_sci_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param admin_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#admin_enabled ExpressRoutePort#admin_enabled}.
        :param macsec_cak_keyvault_secret_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_cak_keyvault_secret_id ExpressRoutePort#macsec_cak_keyvault_secret_id}.
        :param macsec_cipher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_cipher ExpressRoutePort#macsec_cipher}.
        :param macsec_ckn_keyvault_secret_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_ckn_keyvault_secret_id ExpressRoutePort#macsec_ckn_keyvault_secret_id}.
        :param macsec_sci_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_sci_enabled ExpressRoutePort#macsec_sci_enabled}.
        '''
        value = ExpressRoutePortLink2(
            admin_enabled=admin_enabled,
            macsec_cak_keyvault_secret_id=macsec_cak_keyvault_secret_id,
            macsec_cipher=macsec_cipher,
            macsec_ckn_keyvault_secret_id=macsec_ckn_keyvault_secret_id,
            macsec_sci_enabled=macsec_sci_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putLink2", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#create ExpressRoutePort#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#delete ExpressRoutePort#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#read ExpressRoutePort#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#update ExpressRoutePort#update}.
        '''
        value = ExpressRoutePortTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBillingType")
    def reset_billing_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBillingType", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetLink1")
    def reset_link1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLink1", []))

    @jsii.member(jsii_name="resetLink2")
    def reset_link2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLink2", []))

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
    @jsii.member(jsii_name="ethertype")
    def ethertype(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ethertype"))

    @builtins.property
    @jsii.member(jsii_name="guid")
    def guid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "guid"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "ExpressRoutePortIdentityOutputReference":
        return typing.cast("ExpressRoutePortIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="link1")
    def link1(self) -> "ExpressRoutePortLink1OutputReference":
        return typing.cast("ExpressRoutePortLink1OutputReference", jsii.get(self, "link1"))

    @builtins.property
    @jsii.member(jsii_name="link2")
    def link2(self) -> "ExpressRoutePortLink2OutputReference":
        return typing.cast("ExpressRoutePortLink2OutputReference", jsii.get(self, "link2"))

    @builtins.property
    @jsii.member(jsii_name="mtu")
    def mtu(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mtu"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ExpressRoutePortTimeoutsOutputReference":
        return typing.cast("ExpressRoutePortTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthInGbpsInput")
    def bandwidth_in_gbps_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bandwidthInGbpsInput"))

    @builtins.property
    @jsii.member(jsii_name="billingTypeInput")
    def billing_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "billingTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="encapsulationInput")
    def encapsulation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encapsulationInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["ExpressRoutePortIdentity"]:
        return typing.cast(typing.Optional["ExpressRoutePortIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="link1Input")
    def link1_input(self) -> typing.Optional["ExpressRoutePortLink1"]:
        return typing.cast(typing.Optional["ExpressRoutePortLink1"], jsii.get(self, "link1Input"))

    @builtins.property
    @jsii.member(jsii_name="link2Input")
    def link2_input(self) -> typing.Optional["ExpressRoutePortLink2"]:
        return typing.cast(typing.Optional["ExpressRoutePortLink2"], jsii.get(self, "link2Input"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="peeringLocationInput")
    def peering_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peeringLocationInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ExpressRoutePortTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ExpressRoutePortTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthInGbps")
    def bandwidth_in_gbps(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bandwidthInGbps"))

    @bandwidth_in_gbps.setter
    def bandwidth_in_gbps(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df533cc0a24047143f750e6c4ef341c6c686e8fdfcd5456e74e23646d375d314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthInGbps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="billingType")
    def billing_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "billingType"))

    @billing_type.setter
    def billing_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4809013305fbd7fdcb3b078b1238560eebd1723475626e145b181369edc1012)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encapsulation")
    def encapsulation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encapsulation"))

    @encapsulation.setter
    def encapsulation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f84cbc9c754a084eb3dfdb3c07f96d688845b3260fd7413e54929e6a8f647da7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encapsulation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e54048717cea24824c85bd8c5f6f4cd8cd1843bcb93afd8ccaf0d6e431aed7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f34de08a602c4fc3a4e0710132c42a0b07ae49e236d156e60dba91de8b5d3fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b74cf31688eec419b2c41d5e949797a17b9beeadc22902c4a8d79636cca4b50e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peeringLocation")
    def peering_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peeringLocation"))

    @peering_location.setter
    def peering_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe611fefe7a96dcb489adc23ac5020f23c93916f7ccfe0bc882986dd28030361)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peeringLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef1b55584a80bcfa09758120aee2dd6c493e15c2c60a8c9ac86a5e1780001c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72ad848b11faaa197f821dc6243b717d9890d5ea3ce62c950d72e2fad3ce66a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.expressRoutePort.ExpressRoutePortConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bandwidth_in_gbps": "bandwidthInGbps",
        "encapsulation": "encapsulation",
        "location": "location",
        "name": "name",
        "peering_location": "peeringLocation",
        "resource_group_name": "resourceGroupName",
        "billing_type": "billingType",
        "id": "id",
        "identity": "identity",
        "link1": "link1",
        "link2": "link2",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class ExpressRoutePortConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bandwidth_in_gbps: jsii.Number,
        encapsulation: builtins.str,
        location: builtins.str,
        name: builtins.str,
        peering_location: builtins.str,
        resource_group_name: builtins.str,
        billing_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["ExpressRoutePortIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        link1: typing.Optional[typing.Union["ExpressRoutePortLink1", typing.Dict[builtins.str, typing.Any]]] = None,
        link2: typing.Optional[typing.Union["ExpressRoutePortLink2", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ExpressRoutePortTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bandwidth_in_gbps: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#bandwidth_in_gbps ExpressRoutePort#bandwidth_in_gbps}.
        :param encapsulation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#encapsulation ExpressRoutePort#encapsulation}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#location ExpressRoutePort#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#name ExpressRoutePort#name}.
        :param peering_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#peering_location ExpressRoutePort#peering_location}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#resource_group_name ExpressRoutePort#resource_group_name}.
        :param billing_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#billing_type ExpressRoutePort#billing_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#id ExpressRoutePort#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#identity ExpressRoutePort#identity}
        :param link1: link1 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#link1 ExpressRoutePort#link1}
        :param link2: link2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#link2 ExpressRoutePort#link2}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#tags ExpressRoutePort#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#timeouts ExpressRoutePort#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(identity, dict):
            identity = ExpressRoutePortIdentity(**identity)
        if isinstance(link1, dict):
            link1 = ExpressRoutePortLink1(**link1)
        if isinstance(link2, dict):
            link2 = ExpressRoutePortLink2(**link2)
        if isinstance(timeouts, dict):
            timeouts = ExpressRoutePortTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfbe3e2d0d9e47699116218164d78da9d99e06b50573359d439601ba18f0afff)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument bandwidth_in_gbps", value=bandwidth_in_gbps, expected_type=type_hints["bandwidth_in_gbps"])
            check_type(argname="argument encapsulation", value=encapsulation, expected_type=type_hints["encapsulation"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument peering_location", value=peering_location, expected_type=type_hints["peering_location"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument billing_type", value=billing_type, expected_type=type_hints["billing_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument link1", value=link1, expected_type=type_hints["link1"])
            check_type(argname="argument link2", value=link2, expected_type=type_hints["link2"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bandwidth_in_gbps": bandwidth_in_gbps,
            "encapsulation": encapsulation,
            "location": location,
            "name": name,
            "peering_location": peering_location,
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
        if billing_type is not None:
            self._values["billing_type"] = billing_type
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if link1 is not None:
            self._values["link1"] = link1
        if link2 is not None:
            self._values["link2"] = link2
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
    def bandwidth_in_gbps(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#bandwidth_in_gbps ExpressRoutePort#bandwidth_in_gbps}.'''
        result = self._values.get("bandwidth_in_gbps")
        assert result is not None, "Required property 'bandwidth_in_gbps' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def encapsulation(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#encapsulation ExpressRoutePort#encapsulation}.'''
        result = self._values.get("encapsulation")
        assert result is not None, "Required property 'encapsulation' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#location ExpressRoutePort#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#name ExpressRoutePort#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peering_location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#peering_location ExpressRoutePort#peering_location}.'''
        result = self._values.get("peering_location")
        assert result is not None, "Required property 'peering_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#resource_group_name ExpressRoutePort#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def billing_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#billing_type ExpressRoutePort#billing_type}.'''
        result = self._values.get("billing_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#id ExpressRoutePort#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["ExpressRoutePortIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#identity ExpressRoutePort#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["ExpressRoutePortIdentity"], result)

    @builtins.property
    def link1(self) -> typing.Optional["ExpressRoutePortLink1"]:
        '''link1 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#link1 ExpressRoutePort#link1}
        '''
        result = self._values.get("link1")
        return typing.cast(typing.Optional["ExpressRoutePortLink1"], result)

    @builtins.property
    def link2(self) -> typing.Optional["ExpressRoutePortLink2"]:
        '''link2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#link2 ExpressRoutePort#link2}
        '''
        result = self._values.get("link2")
        return typing.cast(typing.Optional["ExpressRoutePortLink2"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#tags ExpressRoutePort#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ExpressRoutePortTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#timeouts ExpressRoutePort#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ExpressRoutePortTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExpressRoutePortConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.expressRoutePort.ExpressRoutePortIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class ExpressRoutePortIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#type ExpressRoutePort#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#identity_ids ExpressRoutePort#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ea83ae6b5f3312f5f90636d82f41041c986f2b91bb78a8b81f99399cc86e0ba)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#type ExpressRoutePort#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#identity_ids ExpressRoutePort#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExpressRoutePortIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExpressRoutePortIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.expressRoutePort.ExpressRoutePortIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dede2e3d8234093a3c5d14ca0ca02a264b66fbd8b12ae0974a40a53bad8f4a27)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIdentityIds")
    def reset_identity_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityIds", []))

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__28e8346590af029b3d1d045883b716b8e0d48f1070797af809e658d0798fada8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f14c0c7d3aa99fc7eca8dfcc26b31364345082d32bebd4676343bf550154995)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ExpressRoutePortIdentity]:
        return typing.cast(typing.Optional[ExpressRoutePortIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ExpressRoutePortIdentity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a4ad92922d38da05494e017536d1eff43f2e184a55dd0ffa1262009fc1de62a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.expressRoutePort.ExpressRoutePortLink1",
    jsii_struct_bases=[],
    name_mapping={
        "admin_enabled": "adminEnabled",
        "macsec_cak_keyvault_secret_id": "macsecCakKeyvaultSecretId",
        "macsec_cipher": "macsecCipher",
        "macsec_ckn_keyvault_secret_id": "macsecCknKeyvaultSecretId",
        "macsec_sci_enabled": "macsecSciEnabled",
    },
)
class ExpressRoutePortLink1:
    def __init__(
        self,
        *,
        admin_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        macsec_cak_keyvault_secret_id: typing.Optional[builtins.str] = None,
        macsec_cipher: typing.Optional[builtins.str] = None,
        macsec_ckn_keyvault_secret_id: typing.Optional[builtins.str] = None,
        macsec_sci_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param admin_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#admin_enabled ExpressRoutePort#admin_enabled}.
        :param macsec_cak_keyvault_secret_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_cak_keyvault_secret_id ExpressRoutePort#macsec_cak_keyvault_secret_id}.
        :param macsec_cipher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_cipher ExpressRoutePort#macsec_cipher}.
        :param macsec_ckn_keyvault_secret_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_ckn_keyvault_secret_id ExpressRoutePort#macsec_ckn_keyvault_secret_id}.
        :param macsec_sci_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_sci_enabled ExpressRoutePort#macsec_sci_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c67060b74b0de0dfd163490963870f8c461ea306a8b29556685fd486ff61dc9)
            check_type(argname="argument admin_enabled", value=admin_enabled, expected_type=type_hints["admin_enabled"])
            check_type(argname="argument macsec_cak_keyvault_secret_id", value=macsec_cak_keyvault_secret_id, expected_type=type_hints["macsec_cak_keyvault_secret_id"])
            check_type(argname="argument macsec_cipher", value=macsec_cipher, expected_type=type_hints["macsec_cipher"])
            check_type(argname="argument macsec_ckn_keyvault_secret_id", value=macsec_ckn_keyvault_secret_id, expected_type=type_hints["macsec_ckn_keyvault_secret_id"])
            check_type(argname="argument macsec_sci_enabled", value=macsec_sci_enabled, expected_type=type_hints["macsec_sci_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if admin_enabled is not None:
            self._values["admin_enabled"] = admin_enabled
        if macsec_cak_keyvault_secret_id is not None:
            self._values["macsec_cak_keyvault_secret_id"] = macsec_cak_keyvault_secret_id
        if macsec_cipher is not None:
            self._values["macsec_cipher"] = macsec_cipher
        if macsec_ckn_keyvault_secret_id is not None:
            self._values["macsec_ckn_keyvault_secret_id"] = macsec_ckn_keyvault_secret_id
        if macsec_sci_enabled is not None:
            self._values["macsec_sci_enabled"] = macsec_sci_enabled

    @builtins.property
    def admin_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#admin_enabled ExpressRoutePort#admin_enabled}.'''
        result = self._values.get("admin_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def macsec_cak_keyvault_secret_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_cak_keyvault_secret_id ExpressRoutePort#macsec_cak_keyvault_secret_id}.'''
        result = self._values.get("macsec_cak_keyvault_secret_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def macsec_cipher(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_cipher ExpressRoutePort#macsec_cipher}.'''
        result = self._values.get("macsec_cipher")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def macsec_ckn_keyvault_secret_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_ckn_keyvault_secret_id ExpressRoutePort#macsec_ckn_keyvault_secret_id}.'''
        result = self._values.get("macsec_ckn_keyvault_secret_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def macsec_sci_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_sci_enabled ExpressRoutePort#macsec_sci_enabled}.'''
        result = self._values.get("macsec_sci_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExpressRoutePortLink1(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExpressRoutePortLink1OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.expressRoutePort.ExpressRoutePortLink1OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72d732f0b85071fb0af05c4e8671d37cd094307b3ec39c3c20a860eed32948f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdminEnabled")
    def reset_admin_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminEnabled", []))

    @jsii.member(jsii_name="resetMacsecCakKeyvaultSecretId")
    def reset_macsec_cak_keyvault_secret_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMacsecCakKeyvaultSecretId", []))

    @jsii.member(jsii_name="resetMacsecCipher")
    def reset_macsec_cipher(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMacsecCipher", []))

    @jsii.member(jsii_name="resetMacsecCknKeyvaultSecretId")
    def reset_macsec_ckn_keyvault_secret_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMacsecCknKeyvaultSecretId", []))

    @jsii.member(jsii_name="resetMacsecSciEnabled")
    def reset_macsec_sci_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMacsecSciEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="connectorType")
    def connector_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorType"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="interfaceName")
    def interface_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interfaceName"))

    @builtins.property
    @jsii.member(jsii_name="patchPanelId")
    def patch_panel_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "patchPanelId"))

    @builtins.property
    @jsii.member(jsii_name="rackId")
    def rack_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rackId"))

    @builtins.property
    @jsii.member(jsii_name="routerName")
    def router_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routerName"))

    @builtins.property
    @jsii.member(jsii_name="adminEnabledInput")
    def admin_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "adminEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="macsecCakKeyvaultSecretIdInput")
    def macsec_cak_keyvault_secret_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "macsecCakKeyvaultSecretIdInput"))

    @builtins.property
    @jsii.member(jsii_name="macsecCipherInput")
    def macsec_cipher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "macsecCipherInput"))

    @builtins.property
    @jsii.member(jsii_name="macsecCknKeyvaultSecretIdInput")
    def macsec_ckn_keyvault_secret_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "macsecCknKeyvaultSecretIdInput"))

    @builtins.property
    @jsii.member(jsii_name="macsecSciEnabledInput")
    def macsec_sci_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "macsecSciEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="adminEnabled")
    def admin_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "adminEnabled"))

    @admin_enabled.setter
    def admin_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a05315d6e5245193aff10dfdc09c176e75501dbed030673280adb82068e9463)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="macsecCakKeyvaultSecretId")
    def macsec_cak_keyvault_secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "macsecCakKeyvaultSecretId"))

    @macsec_cak_keyvault_secret_id.setter
    def macsec_cak_keyvault_secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e04b0cd56c06ca43bc7a6c459183d3fcac088f9e040fee6c30a49b56f7978f4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "macsecCakKeyvaultSecretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="macsecCipher")
    def macsec_cipher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "macsecCipher"))

    @macsec_cipher.setter
    def macsec_cipher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac5ee69112c30af8830f4c85fbf805ef46ebc746afeea72946ca2b911ac60e53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "macsecCipher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="macsecCknKeyvaultSecretId")
    def macsec_ckn_keyvault_secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "macsecCknKeyvaultSecretId"))

    @macsec_ckn_keyvault_secret_id.setter
    def macsec_ckn_keyvault_secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f1af047d9ff3db71b6033b623ccbb916665a28f9575e96fe853ffb955946f55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "macsecCknKeyvaultSecretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="macsecSciEnabled")
    def macsec_sci_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "macsecSciEnabled"))

    @macsec_sci_enabled.setter
    def macsec_sci_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cee285bcd8c22db8405ef230d5a2d933deee50ba32cad3d69d827908d7a573f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "macsecSciEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ExpressRoutePortLink1]:
        return typing.cast(typing.Optional[ExpressRoutePortLink1], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ExpressRoutePortLink1]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a93b7961f45bd03d8b5a2946b7fc8a3b6c66a745169d5d37c692aaf06a03ef48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.expressRoutePort.ExpressRoutePortLink2",
    jsii_struct_bases=[],
    name_mapping={
        "admin_enabled": "adminEnabled",
        "macsec_cak_keyvault_secret_id": "macsecCakKeyvaultSecretId",
        "macsec_cipher": "macsecCipher",
        "macsec_ckn_keyvault_secret_id": "macsecCknKeyvaultSecretId",
        "macsec_sci_enabled": "macsecSciEnabled",
    },
)
class ExpressRoutePortLink2:
    def __init__(
        self,
        *,
        admin_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        macsec_cak_keyvault_secret_id: typing.Optional[builtins.str] = None,
        macsec_cipher: typing.Optional[builtins.str] = None,
        macsec_ckn_keyvault_secret_id: typing.Optional[builtins.str] = None,
        macsec_sci_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param admin_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#admin_enabled ExpressRoutePort#admin_enabled}.
        :param macsec_cak_keyvault_secret_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_cak_keyvault_secret_id ExpressRoutePort#macsec_cak_keyvault_secret_id}.
        :param macsec_cipher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_cipher ExpressRoutePort#macsec_cipher}.
        :param macsec_ckn_keyvault_secret_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_ckn_keyvault_secret_id ExpressRoutePort#macsec_ckn_keyvault_secret_id}.
        :param macsec_sci_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_sci_enabled ExpressRoutePort#macsec_sci_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a433ae3389c67f777eccd54a36caa148fbb62db20daab34d787bfdcb35c40e7)
            check_type(argname="argument admin_enabled", value=admin_enabled, expected_type=type_hints["admin_enabled"])
            check_type(argname="argument macsec_cak_keyvault_secret_id", value=macsec_cak_keyvault_secret_id, expected_type=type_hints["macsec_cak_keyvault_secret_id"])
            check_type(argname="argument macsec_cipher", value=macsec_cipher, expected_type=type_hints["macsec_cipher"])
            check_type(argname="argument macsec_ckn_keyvault_secret_id", value=macsec_ckn_keyvault_secret_id, expected_type=type_hints["macsec_ckn_keyvault_secret_id"])
            check_type(argname="argument macsec_sci_enabled", value=macsec_sci_enabled, expected_type=type_hints["macsec_sci_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if admin_enabled is not None:
            self._values["admin_enabled"] = admin_enabled
        if macsec_cak_keyvault_secret_id is not None:
            self._values["macsec_cak_keyvault_secret_id"] = macsec_cak_keyvault_secret_id
        if macsec_cipher is not None:
            self._values["macsec_cipher"] = macsec_cipher
        if macsec_ckn_keyvault_secret_id is not None:
            self._values["macsec_ckn_keyvault_secret_id"] = macsec_ckn_keyvault_secret_id
        if macsec_sci_enabled is not None:
            self._values["macsec_sci_enabled"] = macsec_sci_enabled

    @builtins.property
    def admin_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#admin_enabled ExpressRoutePort#admin_enabled}.'''
        result = self._values.get("admin_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def macsec_cak_keyvault_secret_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_cak_keyvault_secret_id ExpressRoutePort#macsec_cak_keyvault_secret_id}.'''
        result = self._values.get("macsec_cak_keyvault_secret_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def macsec_cipher(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_cipher ExpressRoutePort#macsec_cipher}.'''
        result = self._values.get("macsec_cipher")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def macsec_ckn_keyvault_secret_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_ckn_keyvault_secret_id ExpressRoutePort#macsec_ckn_keyvault_secret_id}.'''
        result = self._values.get("macsec_ckn_keyvault_secret_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def macsec_sci_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#macsec_sci_enabled ExpressRoutePort#macsec_sci_enabled}.'''
        result = self._values.get("macsec_sci_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExpressRoutePortLink2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExpressRoutePortLink2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.expressRoutePort.ExpressRoutePortLink2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c46c2a2dbff807bca6cf5cb9e5ad704407e729819194264b146668953f1cd921)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdminEnabled")
    def reset_admin_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminEnabled", []))

    @jsii.member(jsii_name="resetMacsecCakKeyvaultSecretId")
    def reset_macsec_cak_keyvault_secret_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMacsecCakKeyvaultSecretId", []))

    @jsii.member(jsii_name="resetMacsecCipher")
    def reset_macsec_cipher(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMacsecCipher", []))

    @jsii.member(jsii_name="resetMacsecCknKeyvaultSecretId")
    def reset_macsec_ckn_keyvault_secret_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMacsecCknKeyvaultSecretId", []))

    @jsii.member(jsii_name="resetMacsecSciEnabled")
    def reset_macsec_sci_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMacsecSciEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="connectorType")
    def connector_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorType"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="interfaceName")
    def interface_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interfaceName"))

    @builtins.property
    @jsii.member(jsii_name="patchPanelId")
    def patch_panel_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "patchPanelId"))

    @builtins.property
    @jsii.member(jsii_name="rackId")
    def rack_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rackId"))

    @builtins.property
    @jsii.member(jsii_name="routerName")
    def router_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routerName"))

    @builtins.property
    @jsii.member(jsii_name="adminEnabledInput")
    def admin_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "adminEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="macsecCakKeyvaultSecretIdInput")
    def macsec_cak_keyvault_secret_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "macsecCakKeyvaultSecretIdInput"))

    @builtins.property
    @jsii.member(jsii_name="macsecCipherInput")
    def macsec_cipher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "macsecCipherInput"))

    @builtins.property
    @jsii.member(jsii_name="macsecCknKeyvaultSecretIdInput")
    def macsec_ckn_keyvault_secret_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "macsecCknKeyvaultSecretIdInput"))

    @builtins.property
    @jsii.member(jsii_name="macsecSciEnabledInput")
    def macsec_sci_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "macsecSciEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="adminEnabled")
    def admin_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "adminEnabled"))

    @admin_enabled.setter
    def admin_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52538e9ba4c7516e9237c7b1218abccec3d59a32b6f9b680c1dae21e05693c74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="macsecCakKeyvaultSecretId")
    def macsec_cak_keyvault_secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "macsecCakKeyvaultSecretId"))

    @macsec_cak_keyvault_secret_id.setter
    def macsec_cak_keyvault_secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f782e53f1add78b7a32567bcb1a42d83ac11c4888af2255ad9d0766b63174cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "macsecCakKeyvaultSecretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="macsecCipher")
    def macsec_cipher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "macsecCipher"))

    @macsec_cipher.setter
    def macsec_cipher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a61dcaa30f25d7af51bee40cefeb90e664132992a35474976f4596b8e64e11b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "macsecCipher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="macsecCknKeyvaultSecretId")
    def macsec_ckn_keyvault_secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "macsecCknKeyvaultSecretId"))

    @macsec_ckn_keyvault_secret_id.setter
    def macsec_ckn_keyvault_secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce482233a635a4dbe43a2a156df73df88b4ed7f671675c44c71c60d8e2dde78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "macsecCknKeyvaultSecretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="macsecSciEnabled")
    def macsec_sci_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "macsecSciEnabled"))

    @macsec_sci_enabled.setter
    def macsec_sci_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93aaf9a1a80ff08d50c6276de17c36ed00e34608ac8fb6cdd7f6a08240ae4a35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "macsecSciEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ExpressRoutePortLink2]:
        return typing.cast(typing.Optional[ExpressRoutePortLink2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ExpressRoutePortLink2]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddc5ef610036ee5e4c46ce5ae1ff5a5c04d0441926a08e86bf1cf356dfc85637)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.expressRoutePort.ExpressRoutePortTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ExpressRoutePortTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#create ExpressRoutePort#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#delete ExpressRoutePort#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#read ExpressRoutePort#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#update ExpressRoutePort#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0b8546549452c14e47f4928d216d931b81ac637e2e0f1da69654f48a35a9a71)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#create ExpressRoutePort#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#delete ExpressRoutePort#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#read ExpressRoutePort#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/express_route_port#update ExpressRoutePort#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExpressRoutePortTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExpressRoutePortTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.expressRoutePort.ExpressRoutePortTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__415e0bc6f2f65aef131ba04a91cb27e16cb122735bf9d0101ef367bda3b89808)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f666d6df5af801d5125c960beab280d549eaffdb5831bf5aeacf49ea8e22e159)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cc9cd070c8ad0b67b2083c7855b3014afd751d53b1da05c06b3f3cccbfcbcac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e91ea0f5da74d35a01d2c67f6e201d51058252aa3ef1b1f605cfc666550216)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8461f1cfcb77a204851d51d77dbe71a4201bebbd5c4faf3e96e356bf68394644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExpressRoutePortTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExpressRoutePortTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExpressRoutePortTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a19811413f7c9c0daadab3255b86e13eaa18954da478689b3c944bcb0f647a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ExpressRoutePort",
    "ExpressRoutePortConfig",
    "ExpressRoutePortIdentity",
    "ExpressRoutePortIdentityOutputReference",
    "ExpressRoutePortLink1",
    "ExpressRoutePortLink1OutputReference",
    "ExpressRoutePortLink2",
    "ExpressRoutePortLink2OutputReference",
    "ExpressRoutePortTimeouts",
    "ExpressRoutePortTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ee4b4c61b07aaf89a9c03a3efa7b448ff2a3520c2331665037f6dc808b76d6d1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    bandwidth_in_gbps: jsii.Number,
    encapsulation: builtins.str,
    location: builtins.str,
    name: builtins.str,
    peering_location: builtins.str,
    resource_group_name: builtins.str,
    billing_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[ExpressRoutePortIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    link1: typing.Optional[typing.Union[ExpressRoutePortLink1, typing.Dict[builtins.str, typing.Any]]] = None,
    link2: typing.Optional[typing.Union[ExpressRoutePortLink2, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ExpressRoutePortTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2eb2fdd19c8e9359e0f4c23c677cffb43009f24f82948d018d06a835408aa254(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df533cc0a24047143f750e6c4ef341c6c686e8fdfcd5456e74e23646d375d314(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4809013305fbd7fdcb3b078b1238560eebd1723475626e145b181369edc1012(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f84cbc9c754a084eb3dfdb3c07f96d688845b3260fd7413e54929e6a8f647da7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e54048717cea24824c85bd8c5f6f4cd8cd1843bcb93afd8ccaf0d6e431aed7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f34de08a602c4fc3a4e0710132c42a0b07ae49e236d156e60dba91de8b5d3fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74cf31688eec419b2c41d5e949797a17b9beeadc22902c4a8d79636cca4b50e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe611fefe7a96dcb489adc23ac5020f23c93916f7ccfe0bc882986dd28030361(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef1b55584a80bcfa09758120aee2dd6c493e15c2c60a8c9ac86a5e1780001c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ad848b11faaa197f821dc6243b717d9890d5ea3ce62c950d72e2fad3ce66a8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfbe3e2d0d9e47699116218164d78da9d99e06b50573359d439601ba18f0afff(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bandwidth_in_gbps: jsii.Number,
    encapsulation: builtins.str,
    location: builtins.str,
    name: builtins.str,
    peering_location: builtins.str,
    resource_group_name: builtins.str,
    billing_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[ExpressRoutePortIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    link1: typing.Optional[typing.Union[ExpressRoutePortLink1, typing.Dict[builtins.str, typing.Any]]] = None,
    link2: typing.Optional[typing.Union[ExpressRoutePortLink2, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ExpressRoutePortTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea83ae6b5f3312f5f90636d82f41041c986f2b91bb78a8b81f99399cc86e0ba(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dede2e3d8234093a3c5d14ca0ca02a264b66fbd8b12ae0974a40a53bad8f4a27(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e8346590af029b3d1d045883b716b8e0d48f1070797af809e658d0798fada8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f14c0c7d3aa99fc7eca8dfcc26b31364345082d32bebd4676343bf550154995(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a4ad92922d38da05494e017536d1eff43f2e184a55dd0ffa1262009fc1de62a(
    value: typing.Optional[ExpressRoutePortIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c67060b74b0de0dfd163490963870f8c461ea306a8b29556685fd486ff61dc9(
    *,
    admin_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    macsec_cak_keyvault_secret_id: typing.Optional[builtins.str] = None,
    macsec_cipher: typing.Optional[builtins.str] = None,
    macsec_ckn_keyvault_secret_id: typing.Optional[builtins.str] = None,
    macsec_sci_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72d732f0b85071fb0af05c4e8671d37cd094307b3ec39c3c20a860eed32948f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a05315d6e5245193aff10dfdc09c176e75501dbed030673280adb82068e9463(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e04b0cd56c06ca43bc7a6c459183d3fcac088f9e040fee6c30a49b56f7978f4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac5ee69112c30af8830f4c85fbf805ef46ebc746afeea72946ca2b911ac60e53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1af047d9ff3db71b6033b623ccbb916665a28f9575e96fe853ffb955946f55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cee285bcd8c22db8405ef230d5a2d933deee50ba32cad3d69d827908d7a573f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a93b7961f45bd03d8b5a2946b7fc8a3b6c66a745169d5d37c692aaf06a03ef48(
    value: typing.Optional[ExpressRoutePortLink1],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a433ae3389c67f777eccd54a36caa148fbb62db20daab34d787bfdcb35c40e7(
    *,
    admin_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    macsec_cak_keyvault_secret_id: typing.Optional[builtins.str] = None,
    macsec_cipher: typing.Optional[builtins.str] = None,
    macsec_ckn_keyvault_secret_id: typing.Optional[builtins.str] = None,
    macsec_sci_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c46c2a2dbff807bca6cf5cb9e5ad704407e729819194264b146668953f1cd921(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52538e9ba4c7516e9237c7b1218abccec3d59a32b6f9b680c1dae21e05693c74(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f782e53f1add78b7a32567bcb1a42d83ac11c4888af2255ad9d0766b63174cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a61dcaa30f25d7af51bee40cefeb90e664132992a35474976f4596b8e64e11b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce482233a635a4dbe43a2a156df73df88b4ed7f671675c44c71c60d8e2dde78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93aaf9a1a80ff08d50c6276de17c36ed00e34608ac8fb6cdd7f6a08240ae4a35(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddc5ef610036ee5e4c46ce5ae1ff5a5c04d0441926a08e86bf1cf356dfc85637(
    value: typing.Optional[ExpressRoutePortLink2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0b8546549452c14e47f4928d216d931b81ac637e2e0f1da69654f48a35a9a71(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415e0bc6f2f65aef131ba04a91cb27e16cb122735bf9d0101ef367bda3b89808(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f666d6df5af801d5125c960beab280d549eaffdb5831bf5aeacf49ea8e22e159(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc9cd070c8ad0b67b2083c7855b3014afd751d53b1da05c06b3f3cccbfcbcac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e91ea0f5da74d35a01d2c67f6e201d51058252aa3ef1b1f605cfc666550216(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8461f1cfcb77a204851d51d77dbe71a4201bebbd5c4faf3e96e356bf68394644(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a19811413f7c9c0daadab3255b86e13eaa18954da478689b3c944bcb0f647a1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExpressRoutePortTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
