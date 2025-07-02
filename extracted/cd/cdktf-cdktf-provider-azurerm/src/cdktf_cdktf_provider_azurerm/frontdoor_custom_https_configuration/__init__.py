r'''
# `azurerm_frontdoor_custom_https_configuration`

Refer to the Terraform Registry for docs: [`azurerm_frontdoor_custom_https_configuration`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration).
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


class FrontdoorCustomHttpsConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoorCustomHttpsConfiguration.FrontdoorCustomHttpsConfiguration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration azurerm_frontdoor_custom_https_configuration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        custom_https_provisioning_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        frontend_endpoint_id: builtins.str,
        custom_https_configuration: typing.Optional[typing.Union["FrontdoorCustomHttpsConfigurationCustomHttpsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["FrontdoorCustomHttpsConfigurationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration azurerm_frontdoor_custom_https_configuration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param custom_https_provisioning_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#custom_https_provisioning_enabled FrontdoorCustomHttpsConfiguration#custom_https_provisioning_enabled}.
        :param frontend_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#frontend_endpoint_id FrontdoorCustomHttpsConfiguration#frontend_endpoint_id}.
        :param custom_https_configuration: custom_https_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#custom_https_configuration FrontdoorCustomHttpsConfiguration#custom_https_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#id FrontdoorCustomHttpsConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#timeouts FrontdoorCustomHttpsConfiguration#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c42101118e592c3f14f281e03c98fb9292eafa2cdda335d4392259cb94ee9805)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FrontdoorCustomHttpsConfigurationConfig(
            custom_https_provisioning_enabled=custom_https_provisioning_enabled,
            frontend_endpoint_id=frontend_endpoint_id,
            custom_https_configuration=custom_https_configuration,
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
        '''Generates CDKTF code for importing a FrontdoorCustomHttpsConfiguration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the FrontdoorCustomHttpsConfiguration to import.
        :param import_from_id: The id of the existing FrontdoorCustomHttpsConfiguration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the FrontdoorCustomHttpsConfiguration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b3cfa1a2c4b79f75b9cf14a8829eb94d44d6d871f02e1cefe2d13db4aae599e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCustomHttpsConfiguration")
    def put_custom_https_configuration(
        self,
        *,
        azure_key_vault_certificate_secret_name: typing.Optional[builtins.str] = None,
        azure_key_vault_certificate_secret_version: typing.Optional[builtins.str] = None,
        azure_key_vault_certificate_vault_id: typing.Optional[builtins.str] = None,
        certificate_source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param azure_key_vault_certificate_secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#azure_key_vault_certificate_secret_name FrontdoorCustomHttpsConfiguration#azure_key_vault_certificate_secret_name}.
        :param azure_key_vault_certificate_secret_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#azure_key_vault_certificate_secret_version FrontdoorCustomHttpsConfiguration#azure_key_vault_certificate_secret_version}.
        :param azure_key_vault_certificate_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#azure_key_vault_certificate_vault_id FrontdoorCustomHttpsConfiguration#azure_key_vault_certificate_vault_id}.
        :param certificate_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#certificate_source FrontdoorCustomHttpsConfiguration#certificate_source}.
        '''
        value = FrontdoorCustomHttpsConfigurationCustomHttpsConfiguration(
            azure_key_vault_certificate_secret_name=azure_key_vault_certificate_secret_name,
            azure_key_vault_certificate_secret_version=azure_key_vault_certificate_secret_version,
            azure_key_vault_certificate_vault_id=azure_key_vault_certificate_vault_id,
            certificate_source=certificate_source,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomHttpsConfiguration", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#create FrontdoorCustomHttpsConfiguration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#delete FrontdoorCustomHttpsConfiguration#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#read FrontdoorCustomHttpsConfiguration#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#update FrontdoorCustomHttpsConfiguration#update}.
        '''
        value = FrontdoorCustomHttpsConfigurationTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCustomHttpsConfiguration")
    def reset_custom_https_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomHttpsConfiguration", []))

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
    @jsii.member(jsii_name="customHttpsConfiguration")
    def custom_https_configuration(
        self,
    ) -> "FrontdoorCustomHttpsConfigurationCustomHttpsConfigurationOutputReference":
        return typing.cast("FrontdoorCustomHttpsConfigurationCustomHttpsConfigurationOutputReference", jsii.get(self, "customHttpsConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "FrontdoorCustomHttpsConfigurationTimeoutsOutputReference":
        return typing.cast("FrontdoorCustomHttpsConfigurationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="customHttpsConfigurationInput")
    def custom_https_configuration_input(
        self,
    ) -> typing.Optional["FrontdoorCustomHttpsConfigurationCustomHttpsConfiguration"]:
        return typing.cast(typing.Optional["FrontdoorCustomHttpsConfigurationCustomHttpsConfiguration"], jsii.get(self, "customHttpsConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="customHttpsProvisioningEnabledInput")
    def custom_https_provisioning_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "customHttpsProvisioningEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="frontendEndpointIdInput")
    def frontend_endpoint_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frontendEndpointIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FrontdoorCustomHttpsConfigurationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FrontdoorCustomHttpsConfigurationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="customHttpsProvisioningEnabled")
    def custom_https_provisioning_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "customHttpsProvisioningEnabled"))

    @custom_https_provisioning_enabled.setter
    def custom_https_provisioning_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c8680002e53a97e147f4ed01c14aaabbec1cfe411730a8d8b006cced5738db8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customHttpsProvisioningEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frontendEndpointId")
    def frontend_endpoint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frontendEndpointId"))

    @frontend_endpoint_id.setter
    def frontend_endpoint_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2850033a6a85563798b8be97da8c016cae5fe149c3806df05406a2bdc42c9795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frontendEndpointId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__863ef3d35e402cb9c79f1395f480148930de9bf0464129436bd3929a89fb4f7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.frontdoorCustomHttpsConfiguration.FrontdoorCustomHttpsConfigurationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "custom_https_provisioning_enabled": "customHttpsProvisioningEnabled",
        "frontend_endpoint_id": "frontendEndpointId",
        "custom_https_configuration": "customHttpsConfiguration",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class FrontdoorCustomHttpsConfigurationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        custom_https_provisioning_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        frontend_endpoint_id: builtins.str,
        custom_https_configuration: typing.Optional[typing.Union["FrontdoorCustomHttpsConfigurationCustomHttpsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["FrontdoorCustomHttpsConfigurationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param custom_https_provisioning_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#custom_https_provisioning_enabled FrontdoorCustomHttpsConfiguration#custom_https_provisioning_enabled}.
        :param frontend_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#frontend_endpoint_id FrontdoorCustomHttpsConfiguration#frontend_endpoint_id}.
        :param custom_https_configuration: custom_https_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#custom_https_configuration FrontdoorCustomHttpsConfiguration#custom_https_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#id FrontdoorCustomHttpsConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#timeouts FrontdoorCustomHttpsConfiguration#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(custom_https_configuration, dict):
            custom_https_configuration = FrontdoorCustomHttpsConfigurationCustomHttpsConfiguration(**custom_https_configuration)
        if isinstance(timeouts, dict):
            timeouts = FrontdoorCustomHttpsConfigurationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2edc5d3d7e26fad2dba43a177c8f77249dfc6ee9a5e62cf441bcc5b870094e5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument custom_https_provisioning_enabled", value=custom_https_provisioning_enabled, expected_type=type_hints["custom_https_provisioning_enabled"])
            check_type(argname="argument frontend_endpoint_id", value=frontend_endpoint_id, expected_type=type_hints["frontend_endpoint_id"])
            check_type(argname="argument custom_https_configuration", value=custom_https_configuration, expected_type=type_hints["custom_https_configuration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "custom_https_provisioning_enabled": custom_https_provisioning_enabled,
            "frontend_endpoint_id": frontend_endpoint_id,
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
        if custom_https_configuration is not None:
            self._values["custom_https_configuration"] = custom_https_configuration
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
    def custom_https_provisioning_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#custom_https_provisioning_enabled FrontdoorCustomHttpsConfiguration#custom_https_provisioning_enabled}.'''
        result = self._values.get("custom_https_provisioning_enabled")
        assert result is not None, "Required property 'custom_https_provisioning_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def frontend_endpoint_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#frontend_endpoint_id FrontdoorCustomHttpsConfiguration#frontend_endpoint_id}.'''
        result = self._values.get("frontend_endpoint_id")
        assert result is not None, "Required property 'frontend_endpoint_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_https_configuration(
        self,
    ) -> typing.Optional["FrontdoorCustomHttpsConfigurationCustomHttpsConfiguration"]:
        '''custom_https_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#custom_https_configuration FrontdoorCustomHttpsConfiguration#custom_https_configuration}
        '''
        result = self._values.get("custom_https_configuration")
        return typing.cast(typing.Optional["FrontdoorCustomHttpsConfigurationCustomHttpsConfiguration"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#id FrontdoorCustomHttpsConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["FrontdoorCustomHttpsConfigurationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#timeouts FrontdoorCustomHttpsConfiguration#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["FrontdoorCustomHttpsConfigurationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FrontdoorCustomHttpsConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.frontdoorCustomHttpsConfiguration.FrontdoorCustomHttpsConfigurationCustomHttpsConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "azure_key_vault_certificate_secret_name": "azureKeyVaultCertificateSecretName",
        "azure_key_vault_certificate_secret_version": "azureKeyVaultCertificateSecretVersion",
        "azure_key_vault_certificate_vault_id": "azureKeyVaultCertificateVaultId",
        "certificate_source": "certificateSource",
    },
)
class FrontdoorCustomHttpsConfigurationCustomHttpsConfiguration:
    def __init__(
        self,
        *,
        azure_key_vault_certificate_secret_name: typing.Optional[builtins.str] = None,
        azure_key_vault_certificate_secret_version: typing.Optional[builtins.str] = None,
        azure_key_vault_certificate_vault_id: typing.Optional[builtins.str] = None,
        certificate_source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param azure_key_vault_certificate_secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#azure_key_vault_certificate_secret_name FrontdoorCustomHttpsConfiguration#azure_key_vault_certificate_secret_name}.
        :param azure_key_vault_certificate_secret_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#azure_key_vault_certificate_secret_version FrontdoorCustomHttpsConfiguration#azure_key_vault_certificate_secret_version}.
        :param azure_key_vault_certificate_vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#azure_key_vault_certificate_vault_id FrontdoorCustomHttpsConfiguration#azure_key_vault_certificate_vault_id}.
        :param certificate_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#certificate_source FrontdoorCustomHttpsConfiguration#certificate_source}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ac2474b7757e423af166e0865bc1aa2862ae1f8a3390d875bbdcffa3424d401)
            check_type(argname="argument azure_key_vault_certificate_secret_name", value=azure_key_vault_certificate_secret_name, expected_type=type_hints["azure_key_vault_certificate_secret_name"])
            check_type(argname="argument azure_key_vault_certificate_secret_version", value=azure_key_vault_certificate_secret_version, expected_type=type_hints["azure_key_vault_certificate_secret_version"])
            check_type(argname="argument azure_key_vault_certificate_vault_id", value=azure_key_vault_certificate_vault_id, expected_type=type_hints["azure_key_vault_certificate_vault_id"])
            check_type(argname="argument certificate_source", value=certificate_source, expected_type=type_hints["certificate_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if azure_key_vault_certificate_secret_name is not None:
            self._values["azure_key_vault_certificate_secret_name"] = azure_key_vault_certificate_secret_name
        if azure_key_vault_certificate_secret_version is not None:
            self._values["azure_key_vault_certificate_secret_version"] = azure_key_vault_certificate_secret_version
        if azure_key_vault_certificate_vault_id is not None:
            self._values["azure_key_vault_certificate_vault_id"] = azure_key_vault_certificate_vault_id
        if certificate_source is not None:
            self._values["certificate_source"] = certificate_source

    @builtins.property
    def azure_key_vault_certificate_secret_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#azure_key_vault_certificate_secret_name FrontdoorCustomHttpsConfiguration#azure_key_vault_certificate_secret_name}.'''
        result = self._values.get("azure_key_vault_certificate_secret_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def azure_key_vault_certificate_secret_version(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#azure_key_vault_certificate_secret_version FrontdoorCustomHttpsConfiguration#azure_key_vault_certificate_secret_version}.'''
        result = self._values.get("azure_key_vault_certificate_secret_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def azure_key_vault_certificate_vault_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#azure_key_vault_certificate_vault_id FrontdoorCustomHttpsConfiguration#azure_key_vault_certificate_vault_id}.'''
        result = self._values.get("azure_key_vault_certificate_vault_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#certificate_source FrontdoorCustomHttpsConfiguration#certificate_source}.'''
        result = self._values.get("certificate_source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FrontdoorCustomHttpsConfigurationCustomHttpsConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FrontdoorCustomHttpsConfigurationCustomHttpsConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoorCustomHttpsConfiguration.FrontdoorCustomHttpsConfigurationCustomHttpsConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea6dc2ab9a1250b02fa5d00cd955f01c5ddc0052af54bf95b04228bccba475a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAzureKeyVaultCertificateSecretName")
    def reset_azure_key_vault_certificate_secret_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureKeyVaultCertificateSecretName", []))

    @jsii.member(jsii_name="resetAzureKeyVaultCertificateSecretVersion")
    def reset_azure_key_vault_certificate_secret_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureKeyVaultCertificateSecretVersion", []))

    @jsii.member(jsii_name="resetAzureKeyVaultCertificateVaultId")
    def reset_azure_key_vault_certificate_vault_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureKeyVaultCertificateVaultId", []))

    @jsii.member(jsii_name="resetCertificateSource")
    def reset_certificate_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateSource", []))

    @builtins.property
    @jsii.member(jsii_name="minimumTlsVersion")
    def minimum_tls_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumTlsVersion"))

    @builtins.property
    @jsii.member(jsii_name="provisioningState")
    def provisioning_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "provisioningState"))

    @builtins.property
    @jsii.member(jsii_name="provisioningSubstate")
    def provisioning_substate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "provisioningSubstate"))

    @builtins.property
    @jsii.member(jsii_name="azureKeyVaultCertificateSecretNameInput")
    def azure_key_vault_certificate_secret_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "azureKeyVaultCertificateSecretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="azureKeyVaultCertificateSecretVersionInput")
    def azure_key_vault_certificate_secret_version_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "azureKeyVaultCertificateSecretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="azureKeyVaultCertificateVaultIdInput")
    def azure_key_vault_certificate_vault_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "azureKeyVaultCertificateVaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateSourceInput")
    def certificate_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="azureKeyVaultCertificateSecretName")
    def azure_key_vault_certificate_secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azureKeyVaultCertificateSecretName"))

    @azure_key_vault_certificate_secret_name.setter
    def azure_key_vault_certificate_secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__817dcffcdb92590e1961a7545104cb830598210a4e324e5ca1a7676b46a51cc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureKeyVaultCertificateSecretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="azureKeyVaultCertificateSecretVersion")
    def azure_key_vault_certificate_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azureKeyVaultCertificateSecretVersion"))

    @azure_key_vault_certificate_secret_version.setter
    def azure_key_vault_certificate_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5029bb6b430ade68a7342ed2825a7be77f5a21320a97cef9d7ad83ed6a0360cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureKeyVaultCertificateSecretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="azureKeyVaultCertificateVaultId")
    def azure_key_vault_certificate_vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azureKeyVaultCertificateVaultId"))

    @azure_key_vault_certificate_vault_id.setter
    def azure_key_vault_certificate_vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8c50efcd19d0a28a1fe56193930110cdacd77ae6c240c32be45ad3011ce82aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureKeyVaultCertificateVaultId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificateSource")
    def certificate_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateSource"))

    @certificate_source.setter
    def certificate_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69fc3f2b4cedb32cb300503c4d26cfbaf05ed33f53bcaacd6ac19be5bed9f4d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FrontdoorCustomHttpsConfigurationCustomHttpsConfiguration]:
        return typing.cast(typing.Optional[FrontdoorCustomHttpsConfigurationCustomHttpsConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FrontdoorCustomHttpsConfigurationCustomHttpsConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5693c8ec79d2ac7936999c7226507297a53611ea26d09cad523522cdce8a97fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.frontdoorCustomHttpsConfiguration.FrontdoorCustomHttpsConfigurationTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class FrontdoorCustomHttpsConfigurationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#create FrontdoorCustomHttpsConfiguration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#delete FrontdoorCustomHttpsConfiguration#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#read FrontdoorCustomHttpsConfiguration#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#update FrontdoorCustomHttpsConfiguration#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cafa098067c2b863202f7be5695d289072b3781b6515c8c7204c60bd4d50bc6c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#create FrontdoorCustomHttpsConfiguration#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#delete FrontdoorCustomHttpsConfiguration#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#read FrontdoorCustomHttpsConfiguration#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/frontdoor_custom_https_configuration#update FrontdoorCustomHttpsConfiguration#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FrontdoorCustomHttpsConfigurationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FrontdoorCustomHttpsConfigurationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.frontdoorCustomHttpsConfiguration.FrontdoorCustomHttpsConfigurationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59b56a8c56374b8bf593ca82eedc4f571bc23338a015d0a8da63526022fe5039)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6d797fcbbb2b5282aa9ec522b653bb27bff4bfdcdaa80cd763ca92d75e65de8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__032f5dfdcf8755516a24173ff520d02bdb6c4b3639c162796833b085b26c7db4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c7696b1aa208aa12fb80e7335898272d674dd970b8c7d03d867609a79646878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__911f554d914a9c915d8aa37f4cb36780b87d98210177a096b65a4df8007ee907)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorCustomHttpsConfigurationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorCustomHttpsConfigurationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorCustomHttpsConfigurationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d112ba5592828afc860242c9acfcc564fde56d4afcf3e7fab67a947bc48197ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "FrontdoorCustomHttpsConfiguration",
    "FrontdoorCustomHttpsConfigurationConfig",
    "FrontdoorCustomHttpsConfigurationCustomHttpsConfiguration",
    "FrontdoorCustomHttpsConfigurationCustomHttpsConfigurationOutputReference",
    "FrontdoorCustomHttpsConfigurationTimeouts",
    "FrontdoorCustomHttpsConfigurationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c42101118e592c3f14f281e03c98fb9292eafa2cdda335d4392259cb94ee9805(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    custom_https_provisioning_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    frontend_endpoint_id: builtins.str,
    custom_https_configuration: typing.Optional[typing.Union[FrontdoorCustomHttpsConfigurationCustomHttpsConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[FrontdoorCustomHttpsConfigurationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__1b3cfa1a2c4b79f75b9cf14a8829eb94d44d6d871f02e1cefe2d13db4aae599e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8680002e53a97e147f4ed01c14aaabbec1cfe411730a8d8b006cced5738db8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2850033a6a85563798b8be97da8c016cae5fe149c3806df05406a2bdc42c9795(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__863ef3d35e402cb9c79f1395f480148930de9bf0464129436bd3929a89fb4f7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2edc5d3d7e26fad2dba43a177c8f77249dfc6ee9a5e62cf441bcc5b870094e5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_https_provisioning_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    frontend_endpoint_id: builtins.str,
    custom_https_configuration: typing.Optional[typing.Union[FrontdoorCustomHttpsConfigurationCustomHttpsConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[FrontdoorCustomHttpsConfigurationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac2474b7757e423af166e0865bc1aa2862ae1f8a3390d875bbdcffa3424d401(
    *,
    azure_key_vault_certificate_secret_name: typing.Optional[builtins.str] = None,
    azure_key_vault_certificate_secret_version: typing.Optional[builtins.str] = None,
    azure_key_vault_certificate_vault_id: typing.Optional[builtins.str] = None,
    certificate_source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea6dc2ab9a1250b02fa5d00cd955f01c5ddc0052af54bf95b04228bccba475a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__817dcffcdb92590e1961a7545104cb830598210a4e324e5ca1a7676b46a51cc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5029bb6b430ade68a7342ed2825a7be77f5a21320a97cef9d7ad83ed6a0360cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8c50efcd19d0a28a1fe56193930110cdacd77ae6c240c32be45ad3011ce82aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69fc3f2b4cedb32cb300503c4d26cfbaf05ed33f53bcaacd6ac19be5bed9f4d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5693c8ec79d2ac7936999c7226507297a53611ea26d09cad523522cdce8a97fe(
    value: typing.Optional[FrontdoorCustomHttpsConfigurationCustomHttpsConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cafa098067c2b863202f7be5695d289072b3781b6515c8c7204c60bd4d50bc6c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59b56a8c56374b8bf593ca82eedc4f571bc23338a015d0a8da63526022fe5039(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6d797fcbbb2b5282aa9ec522b653bb27bff4bfdcdaa80cd763ca92d75e65de8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__032f5dfdcf8755516a24173ff520d02bdb6c4b3639c162796833b085b26c7db4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c7696b1aa208aa12fb80e7335898272d674dd970b8c7d03d867609a79646878(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__911f554d914a9c915d8aa37f4cb36780b87d98210177a096b65a4df8007ee907(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d112ba5592828afc860242c9acfcc564fde56d4afcf3e7fab67a947bc48197ee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FrontdoorCustomHttpsConfigurationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
