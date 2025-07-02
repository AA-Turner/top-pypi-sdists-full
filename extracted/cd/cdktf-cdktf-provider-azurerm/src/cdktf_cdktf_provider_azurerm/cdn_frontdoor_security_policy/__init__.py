r'''
# `azurerm_cdn_frontdoor_security_policy`

Refer to the Terraform Registry for docs: [`azurerm_cdn_frontdoor_security_policy`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy).
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


class CdnFrontdoorSecurityPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorSecurityPolicy.CdnFrontdoorSecurityPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy azurerm_cdn_frontdoor_security_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cdn_frontdoor_profile_id: builtins.str,
        name: builtins.str,
        security_policies: typing.Union["CdnFrontdoorSecurityPolicySecurityPolicies", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CdnFrontdoorSecurityPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy azurerm_cdn_frontdoor_security_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cdn_frontdoor_profile_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#cdn_frontdoor_profile_id CdnFrontdoorSecurityPolicy#cdn_frontdoor_profile_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#name CdnFrontdoorSecurityPolicy#name}.
        :param security_policies: security_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#security_policies CdnFrontdoorSecurityPolicy#security_policies}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#id CdnFrontdoorSecurityPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#timeouts CdnFrontdoorSecurityPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ead37dd26749e1a982209e297d24bdba25b81e1b42e188f45d03cc8cea3500d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CdnFrontdoorSecurityPolicyConfig(
            cdn_frontdoor_profile_id=cdn_frontdoor_profile_id,
            name=name,
            security_policies=security_policies,
            id=id,
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
        '''Generates CDKTF code for importing a CdnFrontdoorSecurityPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CdnFrontdoorSecurityPolicy to import.
        :param import_from_id: The id of the existing CdnFrontdoorSecurityPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CdnFrontdoorSecurityPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cde5476f746b79db096bdbbf7de923832cfefd0a5a9dd84968ce8a95939d7e6f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSecurityPolicies")
    def put_security_policies(
        self,
        *,
        firewall: typing.Union["CdnFrontdoorSecurityPolicySecurityPoliciesFirewall", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param firewall: firewall block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#firewall CdnFrontdoorSecurityPolicy#firewall}
        '''
        value = CdnFrontdoorSecurityPolicySecurityPolicies(firewall=firewall)

        return typing.cast(None, jsii.invoke(self, "putSecurityPolicies", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#create CdnFrontdoorSecurityPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#delete CdnFrontdoorSecurityPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#read CdnFrontdoorSecurityPolicy#read}.
        '''
        value = CdnFrontdoorSecurityPolicyTimeouts(
            create=create, delete=delete, read=read
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="securityPolicies")
    def security_policies(
        self,
    ) -> "CdnFrontdoorSecurityPolicySecurityPoliciesOutputReference":
        return typing.cast("CdnFrontdoorSecurityPolicySecurityPoliciesOutputReference", jsii.get(self, "securityPolicies"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CdnFrontdoorSecurityPolicyTimeoutsOutputReference":
        return typing.cast("CdnFrontdoorSecurityPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorProfileIdInput")
    def cdn_frontdoor_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cdnFrontdoorProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="securityPoliciesInput")
    def security_policies_input(
        self,
    ) -> typing.Optional["CdnFrontdoorSecurityPolicySecurityPolicies"]:
        return typing.cast(typing.Optional["CdnFrontdoorSecurityPolicySecurityPolicies"], jsii.get(self, "securityPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CdnFrontdoorSecurityPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CdnFrontdoorSecurityPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorProfileId")
    def cdn_frontdoor_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cdnFrontdoorProfileId"))

    @cdn_frontdoor_profile_id.setter
    def cdn_frontdoor_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f441d53b6337fbce44c88865a91b248d1ecbfe30183c8a5c89d3cd6407143f52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdnFrontdoorProfileId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bc727dd1276987c2ae5229ffb1137828f0508ace6cedf64214cf182e13ebb24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51d9dba91dd4e3db265ab6061eb33e6bd7b233631f06e0a5e1131ff1ce55c293)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorSecurityPolicy.CdnFrontdoorSecurityPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cdn_frontdoor_profile_id": "cdnFrontdoorProfileId",
        "name": "name",
        "security_policies": "securityPolicies",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class CdnFrontdoorSecurityPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cdn_frontdoor_profile_id: builtins.str,
        name: builtins.str,
        security_policies: typing.Union["CdnFrontdoorSecurityPolicySecurityPolicies", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CdnFrontdoorSecurityPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cdn_frontdoor_profile_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#cdn_frontdoor_profile_id CdnFrontdoorSecurityPolicy#cdn_frontdoor_profile_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#name CdnFrontdoorSecurityPolicy#name}.
        :param security_policies: security_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#security_policies CdnFrontdoorSecurityPolicy#security_policies}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#id CdnFrontdoorSecurityPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#timeouts CdnFrontdoorSecurityPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(security_policies, dict):
            security_policies = CdnFrontdoorSecurityPolicySecurityPolicies(**security_policies)
        if isinstance(timeouts, dict):
            timeouts = CdnFrontdoorSecurityPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ae0d20ff3260c75e78b54e951792c9711ccaece6045aa2ba384d6ef178838f7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cdn_frontdoor_profile_id", value=cdn_frontdoor_profile_id, expected_type=type_hints["cdn_frontdoor_profile_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument security_policies", value=security_policies, expected_type=type_hints["security_policies"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cdn_frontdoor_profile_id": cdn_frontdoor_profile_id,
            "name": name,
            "security_policies": security_policies,
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
        if id is not None:
            self._values["id"] = id
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
    def cdn_frontdoor_profile_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#cdn_frontdoor_profile_id CdnFrontdoorSecurityPolicy#cdn_frontdoor_profile_id}.'''
        result = self._values.get("cdn_frontdoor_profile_id")
        assert result is not None, "Required property 'cdn_frontdoor_profile_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#name CdnFrontdoorSecurityPolicy#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_policies(self) -> "CdnFrontdoorSecurityPolicySecurityPolicies":
        '''security_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#security_policies CdnFrontdoorSecurityPolicy#security_policies}
        '''
        result = self._values.get("security_policies")
        assert result is not None, "Required property 'security_policies' is missing"
        return typing.cast("CdnFrontdoorSecurityPolicySecurityPolicies", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#id CdnFrontdoorSecurityPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CdnFrontdoorSecurityPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#timeouts CdnFrontdoorSecurityPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CdnFrontdoorSecurityPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorSecurityPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorSecurityPolicy.CdnFrontdoorSecurityPolicySecurityPolicies",
    jsii_struct_bases=[],
    name_mapping={"firewall": "firewall"},
)
class CdnFrontdoorSecurityPolicySecurityPolicies:
    def __init__(
        self,
        *,
        firewall: typing.Union["CdnFrontdoorSecurityPolicySecurityPoliciesFirewall", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param firewall: firewall block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#firewall CdnFrontdoorSecurityPolicy#firewall}
        '''
        if isinstance(firewall, dict):
            firewall = CdnFrontdoorSecurityPolicySecurityPoliciesFirewall(**firewall)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ed656088b91b67182081743436fc4d95acfecada07be15fc41a83663b4adf8)
            check_type(argname="argument firewall", value=firewall, expected_type=type_hints["firewall"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "firewall": firewall,
        }

    @builtins.property
    def firewall(self) -> "CdnFrontdoorSecurityPolicySecurityPoliciesFirewall":
        '''firewall block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#firewall CdnFrontdoorSecurityPolicy#firewall}
        '''
        result = self._values.get("firewall")
        assert result is not None, "Required property 'firewall' is missing"
        return typing.cast("CdnFrontdoorSecurityPolicySecurityPoliciesFirewall", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorSecurityPolicySecurityPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorSecurityPolicy.CdnFrontdoorSecurityPolicySecurityPoliciesFirewall",
    jsii_struct_bases=[],
    name_mapping={
        "association": "association",
        "cdn_frontdoor_firewall_policy_id": "cdnFrontdoorFirewallPolicyId",
    },
)
class CdnFrontdoorSecurityPolicySecurityPoliciesFirewall:
    def __init__(
        self,
        *,
        association: typing.Union["CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociation", typing.Dict[builtins.str, typing.Any]],
        cdn_frontdoor_firewall_policy_id: builtins.str,
    ) -> None:
        '''
        :param association: association block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#association CdnFrontdoorSecurityPolicy#association}
        :param cdn_frontdoor_firewall_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#cdn_frontdoor_firewall_policy_id CdnFrontdoorSecurityPolicy#cdn_frontdoor_firewall_policy_id}.
        '''
        if isinstance(association, dict):
            association = CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociation(**association)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3d52047157fcf70b33f48f8d271232d06268e9c301b8e301406fd9533322091)
            check_type(argname="argument association", value=association, expected_type=type_hints["association"])
            check_type(argname="argument cdn_frontdoor_firewall_policy_id", value=cdn_frontdoor_firewall_policy_id, expected_type=type_hints["cdn_frontdoor_firewall_policy_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "association": association,
            "cdn_frontdoor_firewall_policy_id": cdn_frontdoor_firewall_policy_id,
        }

    @builtins.property
    def association(
        self,
    ) -> "CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociation":
        '''association block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#association CdnFrontdoorSecurityPolicy#association}
        '''
        result = self._values.get("association")
        assert result is not None, "Required property 'association' is missing"
        return typing.cast("CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociation", result)

    @builtins.property
    def cdn_frontdoor_firewall_policy_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#cdn_frontdoor_firewall_policy_id CdnFrontdoorSecurityPolicy#cdn_frontdoor_firewall_policy_id}.'''
        result = self._values.get("cdn_frontdoor_firewall_policy_id")
        assert result is not None, "Required property 'cdn_frontdoor_firewall_policy_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorSecurityPolicySecurityPoliciesFirewall(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorSecurityPolicy.CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociation",
    jsii_struct_bases=[],
    name_mapping={"domain": "domain", "patterns_to_match": "patternsToMatch"},
)
class CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociation:
    def __init__(
        self,
        *,
        domain: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomain", typing.Dict[builtins.str, typing.Any]]]],
        patterns_to_match: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param domain: domain block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#domain CdnFrontdoorSecurityPolicy#domain}
        :param patterns_to_match: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#patterns_to_match CdnFrontdoorSecurityPolicy#patterns_to_match}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__745466c72e376322dcdf2521432aa9eb81d0c20cf50a04f8d7756d39fa231303)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument patterns_to_match", value=patterns_to_match, expected_type=type_hints["patterns_to_match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain": domain,
            "patterns_to_match": patterns_to_match,
        }

    @builtins.property
    def domain(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomain"]]:
        '''domain block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#domain CdnFrontdoorSecurityPolicy#domain}
        '''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomain"]], result)

    @builtins.property
    def patterns_to_match(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#patterns_to_match CdnFrontdoorSecurityPolicy#patterns_to_match}.'''
        result = self._values.get("patterns_to_match")
        assert result is not None, "Required property 'patterns_to_match' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorSecurityPolicy.CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomain",
    jsii_struct_bases=[],
    name_mapping={"cdn_frontdoor_domain_id": "cdnFrontdoorDomainId"},
)
class CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomain:
    def __init__(self, *, cdn_frontdoor_domain_id: builtins.str) -> None:
        '''
        :param cdn_frontdoor_domain_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#cdn_frontdoor_domain_id CdnFrontdoorSecurityPolicy#cdn_frontdoor_domain_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf9069971224d8c9cb6632be61236a04c1b6e4e618ff33d3ea73785f4d5c758b)
            check_type(argname="argument cdn_frontdoor_domain_id", value=cdn_frontdoor_domain_id, expected_type=type_hints["cdn_frontdoor_domain_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cdn_frontdoor_domain_id": cdn_frontdoor_domain_id,
        }

    @builtins.property
    def cdn_frontdoor_domain_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#cdn_frontdoor_domain_id CdnFrontdoorSecurityPolicy#cdn_frontdoor_domain_id}.'''
        result = self._values.get("cdn_frontdoor_domain_id")
        assert result is not None, "Required property 'cdn_frontdoor_domain_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomain(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomainList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorSecurityPolicy.CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomainList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32db3778b2dfc8f8e2829aba1e74d918bbb6a4a402bc93d3df5d1ceb241a036f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomainOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7a7e138785d4fba3e4bce2e791d52c29570a92ce7528fb8c285496abe4b87a5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomainOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40639c145c7e856e2e72ee9a149290966b4f26d7452c9c81f80291058a225384)
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
            type_hints = typing.get_type_hints(_typecheckingstub__436a9864dc362e1a36c278499265939b370600d302fafff8f7c27cc5269871e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02faba04f33c616af1ea3dc2db1f6129c8bd7102f86bf33a64501559448c0bbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomain]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomain]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomain]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__352ef035a59c4b127cb34b0182f0f452a5085e4aab65462545a24d0b0fe5be06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomainOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorSecurityPolicy.CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomainOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77ef778f6d4bdef8f2af12affa90bdb8a01704b94dee8f30319929fee21fcfa7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="active")
    def active(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "active"))

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorDomainIdInput")
    def cdn_frontdoor_domain_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cdnFrontdoorDomainIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorDomainId")
    def cdn_frontdoor_domain_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cdnFrontdoorDomainId"))

    @cdn_frontdoor_domain_id.setter
    def cdn_frontdoor_domain_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e201378face74c21f587d8abbf2759667b1e1a930c5ffe4ada123be4e94f86c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdnFrontdoorDomainId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomain]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomain]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomain]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73c5d1259dba3e71a9d2b1adcbc72bd01a648427ac1c0d703fb7209b86a9ef28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorSecurityPolicy.CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ceb0939e5847f3b615a308076d0b3242381eacd84cee3cc16a3253188fcef34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDomain")
    def put_domain(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomain, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__420e3f7b4f526fe5dbf1706903cb0fca9dcbc8e056db381e45aab5df514b5d2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDomain", [value]))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(
        self,
    ) -> CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomainList:
        return typing.cast(CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomainList, jsii.get(self, "domain"))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomain]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomain]]], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="patternsToMatchInput")
    def patterns_to_match_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "patternsToMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="patternsToMatch")
    def patterns_to_match(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "patternsToMatch"))

    @patterns_to_match.setter
    def patterns_to_match(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__539ccd87f38c5d2ccec143fe94b5026ec7ebc5a82d09834a7624a433cc767064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "patternsToMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociation]:
        return typing.cast(typing.Optional[CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3936005cd4f23685474bb5a837a1e846f8070680e23f2c9b87e2cef77b9e6c50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorSecurityPolicySecurityPoliciesFirewallOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorSecurityPolicy.CdnFrontdoorSecurityPolicySecurityPoliciesFirewallOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6eb629a25c86b1a283ac3505114c621047f454f36e8c33e514e14f0c61b74a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAssociation")
    def put_association(
        self,
        *,
        domain: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomain, typing.Dict[builtins.str, typing.Any]]]],
        patterns_to_match: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param domain: domain block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#domain CdnFrontdoorSecurityPolicy#domain}
        :param patterns_to_match: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#patterns_to_match CdnFrontdoorSecurityPolicy#patterns_to_match}.
        '''
        value = CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociation(
            domain=domain, patterns_to_match=patterns_to_match
        )

        return typing.cast(None, jsii.invoke(self, "putAssociation", [value]))

    @builtins.property
    @jsii.member(jsii_name="association")
    def association(
        self,
    ) -> CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationOutputReference:
        return typing.cast(CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationOutputReference, jsii.get(self, "association"))

    @builtins.property
    @jsii.member(jsii_name="associationInput")
    def association_input(
        self,
    ) -> typing.Optional[CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociation]:
        return typing.cast(typing.Optional[CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociation], jsii.get(self, "associationInput"))

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorFirewallPolicyIdInput")
    def cdn_frontdoor_firewall_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cdnFrontdoorFirewallPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cdnFrontdoorFirewallPolicyId")
    def cdn_frontdoor_firewall_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cdnFrontdoorFirewallPolicyId"))

    @cdn_frontdoor_firewall_policy_id.setter
    def cdn_frontdoor_firewall_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7596d74972fdcf4d19b7553b39b3f68640324f902f9cbad6ba701777ae4eb8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdnFrontdoorFirewallPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CdnFrontdoorSecurityPolicySecurityPoliciesFirewall]:
        return typing.cast(typing.Optional[CdnFrontdoorSecurityPolicySecurityPoliciesFirewall], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CdnFrontdoorSecurityPolicySecurityPoliciesFirewall],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e1b4ccd73d6d5ac10e7462f27bca23e950214118f8bc5b7d3895b4a24077761)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CdnFrontdoorSecurityPolicySecurityPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorSecurityPolicy.CdnFrontdoorSecurityPolicySecurityPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c968037e23e856411fc2a1a9ecb346c3e102b2e62d9d7a08d99a7f3362e6fe7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFirewall")
    def put_firewall(
        self,
        *,
        association: typing.Union[CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociation, typing.Dict[builtins.str, typing.Any]],
        cdn_frontdoor_firewall_policy_id: builtins.str,
    ) -> None:
        '''
        :param association: association block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#association CdnFrontdoorSecurityPolicy#association}
        :param cdn_frontdoor_firewall_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#cdn_frontdoor_firewall_policy_id CdnFrontdoorSecurityPolicy#cdn_frontdoor_firewall_policy_id}.
        '''
        value = CdnFrontdoorSecurityPolicySecurityPoliciesFirewall(
            association=association,
            cdn_frontdoor_firewall_policy_id=cdn_frontdoor_firewall_policy_id,
        )

        return typing.cast(None, jsii.invoke(self, "putFirewall", [value]))

    @builtins.property
    @jsii.member(jsii_name="firewall")
    def firewall(
        self,
    ) -> CdnFrontdoorSecurityPolicySecurityPoliciesFirewallOutputReference:
        return typing.cast(CdnFrontdoorSecurityPolicySecurityPoliciesFirewallOutputReference, jsii.get(self, "firewall"))

    @builtins.property
    @jsii.member(jsii_name="firewallInput")
    def firewall_input(
        self,
    ) -> typing.Optional[CdnFrontdoorSecurityPolicySecurityPoliciesFirewall]:
        return typing.cast(typing.Optional[CdnFrontdoorSecurityPolicySecurityPoliciesFirewall], jsii.get(self, "firewallInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CdnFrontdoorSecurityPolicySecurityPolicies]:
        return typing.cast(typing.Optional[CdnFrontdoorSecurityPolicySecurityPolicies], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CdnFrontdoorSecurityPolicySecurityPolicies],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb15bd45c660016e9fd93e35fba202829b3a58cbd7a4ad04cef414470879f66c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorSecurityPolicy.CdnFrontdoorSecurityPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "read": "read"},
)
class CdnFrontdoorSecurityPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#create CdnFrontdoorSecurityPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#delete CdnFrontdoorSecurityPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#read CdnFrontdoorSecurityPolicy#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94014d28d58f24dd207791c0736b565859c0d4f62e032eb275f1ab4cf4023fd7)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#create CdnFrontdoorSecurityPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#delete CdnFrontdoorSecurityPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/cdn_frontdoor_security_policy#read CdnFrontdoorSecurityPolicy#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdnFrontdoorSecurityPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdnFrontdoorSecurityPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.cdnFrontdoorSecurityPolicy.CdnFrontdoorSecurityPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cc5d3039f51ec56699e8e8934802df87b2d26ef84725c546836091ae87249f5)
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
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72105ca36f425d5db5de02f7c3034d664d8d9beea72671233f661da71089a06c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2256be8774c902999b9305c16e82af9f4cdb1121f196cd1851360934fdad981)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1decbd226a642bcf6a800446256d0e63109e4f7f652f9ae4011786a5f6ea066)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorSecurityPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorSecurityPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorSecurityPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba34015cefefe7e4ad768b1346eb763d7cc08cde394d4514d25366f9d74e92a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CdnFrontdoorSecurityPolicy",
    "CdnFrontdoorSecurityPolicyConfig",
    "CdnFrontdoorSecurityPolicySecurityPolicies",
    "CdnFrontdoorSecurityPolicySecurityPoliciesFirewall",
    "CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociation",
    "CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomain",
    "CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomainList",
    "CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomainOutputReference",
    "CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationOutputReference",
    "CdnFrontdoorSecurityPolicySecurityPoliciesFirewallOutputReference",
    "CdnFrontdoorSecurityPolicySecurityPoliciesOutputReference",
    "CdnFrontdoorSecurityPolicyTimeouts",
    "CdnFrontdoorSecurityPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__8ead37dd26749e1a982209e297d24bdba25b81e1b42e188f45d03cc8cea3500d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cdn_frontdoor_profile_id: builtins.str,
    name: builtins.str,
    security_policies: typing.Union[CdnFrontdoorSecurityPolicySecurityPolicies, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CdnFrontdoorSecurityPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__cde5476f746b79db096bdbbf7de923832cfefd0a5a9dd84968ce8a95939d7e6f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f441d53b6337fbce44c88865a91b248d1ecbfe30183c8a5c89d3cd6407143f52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bc727dd1276987c2ae5229ffb1137828f0508ace6cedf64214cf182e13ebb24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51d9dba91dd4e3db265ab6061eb33e6bd7b233631f06e0a5e1131ff1ce55c293(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae0d20ff3260c75e78b54e951792c9711ccaece6045aa2ba384d6ef178838f7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cdn_frontdoor_profile_id: builtins.str,
    name: builtins.str,
    security_policies: typing.Union[CdnFrontdoorSecurityPolicySecurityPolicies, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CdnFrontdoorSecurityPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ed656088b91b67182081743436fc4d95acfecada07be15fc41a83663b4adf8(
    *,
    firewall: typing.Union[CdnFrontdoorSecurityPolicySecurityPoliciesFirewall, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d52047157fcf70b33f48f8d271232d06268e9c301b8e301406fd9533322091(
    *,
    association: typing.Union[CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociation, typing.Dict[builtins.str, typing.Any]],
    cdn_frontdoor_firewall_policy_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__745466c72e376322dcdf2521432aa9eb81d0c20cf50a04f8d7756d39fa231303(
    *,
    domain: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomain, typing.Dict[builtins.str, typing.Any]]]],
    patterns_to_match: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf9069971224d8c9cb6632be61236a04c1b6e4e618ff33d3ea73785f4d5c758b(
    *,
    cdn_frontdoor_domain_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32db3778b2dfc8f8e2829aba1e74d918bbb6a4a402bc93d3df5d1ceb241a036f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7a7e138785d4fba3e4bce2e791d52c29570a92ce7528fb8c285496abe4b87a5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40639c145c7e856e2e72ee9a149290966b4f26d7452c9c81f80291058a225384(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__436a9864dc362e1a36c278499265939b370600d302fafff8f7c27cc5269871e9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02faba04f33c616af1ea3dc2db1f6129c8bd7102f86bf33a64501559448c0bbb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__352ef035a59c4b127cb34b0182f0f452a5085e4aab65462545a24d0b0fe5be06(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomain]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77ef778f6d4bdef8f2af12affa90bdb8a01704b94dee8f30319929fee21fcfa7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e201378face74c21f587d8abbf2759667b1e1a930c5ffe4ada123be4e94f86c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c5d1259dba3e71a9d2b1adcbc72bd01a648427ac1c0d703fb7209b86a9ef28(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomain]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ceb0939e5847f3b615a308076d0b3242381eacd84cee3cc16a3253188fcef34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__420e3f7b4f526fe5dbf1706903cb0fca9dcbc8e056db381e45aab5df514b5d2f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociationDomain, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__539ccd87f38c5d2ccec143fe94b5026ec7ebc5a82d09834a7624a433cc767064(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3936005cd4f23685474bb5a837a1e846f8070680e23f2c9b87e2cef77b9e6c50(
    value: typing.Optional[CdnFrontdoorSecurityPolicySecurityPoliciesFirewallAssociation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6eb629a25c86b1a283ac3505114c621047f454f36e8c33e514e14f0c61b74a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7596d74972fdcf4d19b7553b39b3f68640324f902f9cbad6ba701777ae4eb8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e1b4ccd73d6d5ac10e7462f27bca23e950214118f8bc5b7d3895b4a24077761(
    value: typing.Optional[CdnFrontdoorSecurityPolicySecurityPoliciesFirewall],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c968037e23e856411fc2a1a9ecb346c3e102b2e62d9d7a08d99a7f3362e6fe7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb15bd45c660016e9fd93e35fba202829b3a58cbd7a4ad04cef414470879f66c(
    value: typing.Optional[CdnFrontdoorSecurityPolicySecurityPolicies],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94014d28d58f24dd207791c0736b565859c0d4f62e032eb275f1ab4cf4023fd7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc5d3039f51ec56699e8e8934802df87b2d26ef84725c546836091ae87249f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72105ca36f425d5db5de02f7c3034d664d8d9beea72671233f661da71089a06c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2256be8774c902999b9305c16e82af9f4cdb1121f196cd1851360934fdad981(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1decbd226a642bcf6a800446256d0e63109e4f7f652f9ae4011786a5f6ea066(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba34015cefefe7e4ad768b1346eb763d7cc08cde394d4514d25366f9d74e92a1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CdnFrontdoorSecurityPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
