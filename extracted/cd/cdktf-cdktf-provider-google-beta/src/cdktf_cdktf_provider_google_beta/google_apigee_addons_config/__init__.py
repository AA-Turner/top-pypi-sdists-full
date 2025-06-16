r'''
# `google_apigee_addons_config`

Refer to the Terraform Registry for docs: [`google_apigee_addons_config`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config).
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


class GoogleApigeeAddonsConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeAddonsConfig.GoogleApigeeAddonsConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config google_apigee_addons_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        org: builtins.str,
        addons_config: typing.Optional[typing.Union["GoogleApigeeAddonsConfigAddonsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleApigeeAddonsConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config google_apigee_addons_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param org: Name of the Apigee organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#org GoogleApigeeAddonsConfig#org}
        :param addons_config: addons_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#addons_config GoogleApigeeAddonsConfig#addons_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#id GoogleApigeeAddonsConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#timeouts GoogleApigeeAddonsConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7faa98c571f89d825bc59b7728233e87bb1be4c131e392db3ca70b1fa7bce55)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleApigeeAddonsConfigConfig(
            org=org,
            addons_config=addons_config,
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
        '''Generates CDKTF code for importing a GoogleApigeeAddonsConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleApigeeAddonsConfig to import.
        :param import_from_id: The id of the existing GoogleApigeeAddonsConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleApigeeAddonsConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a94c231854038b03c6791912b9c2dcdf777b5f16b6373205570f35a02e263d20)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAddonsConfig")
    def put_addons_config(
        self,
        *,
        advanced_api_ops_config: typing.Optional[typing.Union["GoogleApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        api_security_config: typing.Optional[typing.Union["GoogleApigeeAddonsConfigAddonsConfigApiSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connectors_platform_config: typing.Optional[typing.Union["GoogleApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        integration_config: typing.Optional[typing.Union["GoogleApigeeAddonsConfigAddonsConfigIntegrationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        monetization_config: typing.Optional[typing.Union["GoogleApigeeAddonsConfigAddonsConfigMonetizationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_api_ops_config: advanced_api_ops_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#advanced_api_ops_config GoogleApigeeAddonsConfig#advanced_api_ops_config}
        :param api_security_config: api_security_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#api_security_config GoogleApigeeAddonsConfig#api_security_config}
        :param connectors_platform_config: connectors_platform_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#connectors_platform_config GoogleApigeeAddonsConfig#connectors_platform_config}
        :param integration_config: integration_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#integration_config GoogleApigeeAddonsConfig#integration_config}
        :param monetization_config: monetization_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#monetization_config GoogleApigeeAddonsConfig#monetization_config}
        '''
        value = GoogleApigeeAddonsConfigAddonsConfig(
            advanced_api_ops_config=advanced_api_ops_config,
            api_security_config=api_security_config,
            connectors_platform_config=connectors_platform_config,
            integration_config=integration_config,
            monetization_config=monetization_config,
        )

        return typing.cast(None, jsii.invoke(self, "putAddonsConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#create GoogleApigeeAddonsConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#delete GoogleApigeeAddonsConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#update GoogleApigeeAddonsConfig#update}.
        '''
        value = GoogleApigeeAddonsConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAddonsConfig")
    def reset_addons_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddonsConfig", []))

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
    @jsii.member(jsii_name="addonsConfig")
    def addons_config(self) -> "GoogleApigeeAddonsConfigAddonsConfigOutputReference":
        return typing.cast("GoogleApigeeAddonsConfigAddonsConfigOutputReference", jsii.get(self, "addonsConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleApigeeAddonsConfigTimeoutsOutputReference":
        return typing.cast("GoogleApigeeAddonsConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="addonsConfigInput")
    def addons_config_input(
        self,
    ) -> typing.Optional["GoogleApigeeAddonsConfigAddonsConfig"]:
        return typing.cast(typing.Optional["GoogleApigeeAddonsConfigAddonsConfig"], jsii.get(self, "addonsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleApigeeAddonsConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleApigeeAddonsConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__171375282b85a97a4ba71af35e41bfaf1c7250bc42b8fa17dd4550b51759b8ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__894d36d1abe28161f8be009cbdb9974d5082c84acaf56d3c76026029dab11700)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeAddonsConfig.GoogleApigeeAddonsConfigAddonsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "advanced_api_ops_config": "advancedApiOpsConfig",
        "api_security_config": "apiSecurityConfig",
        "connectors_platform_config": "connectorsPlatformConfig",
        "integration_config": "integrationConfig",
        "monetization_config": "monetizationConfig",
    },
)
class GoogleApigeeAddonsConfigAddonsConfig:
    def __init__(
        self,
        *,
        advanced_api_ops_config: typing.Optional[typing.Union["GoogleApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        api_security_config: typing.Optional[typing.Union["GoogleApigeeAddonsConfigAddonsConfigApiSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connectors_platform_config: typing.Optional[typing.Union["GoogleApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        integration_config: typing.Optional[typing.Union["GoogleApigeeAddonsConfigAddonsConfigIntegrationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        monetization_config: typing.Optional[typing.Union["GoogleApigeeAddonsConfigAddonsConfigMonetizationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_api_ops_config: advanced_api_ops_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#advanced_api_ops_config GoogleApigeeAddonsConfig#advanced_api_ops_config}
        :param api_security_config: api_security_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#api_security_config GoogleApigeeAddonsConfig#api_security_config}
        :param connectors_platform_config: connectors_platform_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#connectors_platform_config GoogleApigeeAddonsConfig#connectors_platform_config}
        :param integration_config: integration_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#integration_config GoogleApigeeAddonsConfig#integration_config}
        :param monetization_config: monetization_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#monetization_config GoogleApigeeAddonsConfig#monetization_config}
        '''
        if isinstance(advanced_api_ops_config, dict):
            advanced_api_ops_config = GoogleApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig(**advanced_api_ops_config)
        if isinstance(api_security_config, dict):
            api_security_config = GoogleApigeeAddonsConfigAddonsConfigApiSecurityConfig(**api_security_config)
        if isinstance(connectors_platform_config, dict):
            connectors_platform_config = GoogleApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig(**connectors_platform_config)
        if isinstance(integration_config, dict):
            integration_config = GoogleApigeeAddonsConfigAddonsConfigIntegrationConfig(**integration_config)
        if isinstance(monetization_config, dict):
            monetization_config = GoogleApigeeAddonsConfigAddonsConfigMonetizationConfig(**monetization_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a9d0f0bbe769d3820fcf8f752e544e716d2f145773681992743a3385cd9c846)
            check_type(argname="argument advanced_api_ops_config", value=advanced_api_ops_config, expected_type=type_hints["advanced_api_ops_config"])
            check_type(argname="argument api_security_config", value=api_security_config, expected_type=type_hints["api_security_config"])
            check_type(argname="argument connectors_platform_config", value=connectors_platform_config, expected_type=type_hints["connectors_platform_config"])
            check_type(argname="argument integration_config", value=integration_config, expected_type=type_hints["integration_config"])
            check_type(argname="argument monetization_config", value=monetization_config, expected_type=type_hints["monetization_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if advanced_api_ops_config is not None:
            self._values["advanced_api_ops_config"] = advanced_api_ops_config
        if api_security_config is not None:
            self._values["api_security_config"] = api_security_config
        if connectors_platform_config is not None:
            self._values["connectors_platform_config"] = connectors_platform_config
        if integration_config is not None:
            self._values["integration_config"] = integration_config
        if monetization_config is not None:
            self._values["monetization_config"] = monetization_config

    @builtins.property
    def advanced_api_ops_config(
        self,
    ) -> typing.Optional["GoogleApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig"]:
        '''advanced_api_ops_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#advanced_api_ops_config GoogleApigeeAddonsConfig#advanced_api_ops_config}
        '''
        result = self._values.get("advanced_api_ops_config")
        return typing.cast(typing.Optional["GoogleApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig"], result)

    @builtins.property
    def api_security_config(
        self,
    ) -> typing.Optional["GoogleApigeeAddonsConfigAddonsConfigApiSecurityConfig"]:
        '''api_security_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#api_security_config GoogleApigeeAddonsConfig#api_security_config}
        '''
        result = self._values.get("api_security_config")
        return typing.cast(typing.Optional["GoogleApigeeAddonsConfigAddonsConfigApiSecurityConfig"], result)

    @builtins.property
    def connectors_platform_config(
        self,
    ) -> typing.Optional["GoogleApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig"]:
        '''connectors_platform_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#connectors_platform_config GoogleApigeeAddonsConfig#connectors_platform_config}
        '''
        result = self._values.get("connectors_platform_config")
        return typing.cast(typing.Optional["GoogleApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig"], result)

    @builtins.property
    def integration_config(
        self,
    ) -> typing.Optional["GoogleApigeeAddonsConfigAddonsConfigIntegrationConfig"]:
        '''integration_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#integration_config GoogleApigeeAddonsConfig#integration_config}
        '''
        result = self._values.get("integration_config")
        return typing.cast(typing.Optional["GoogleApigeeAddonsConfigAddonsConfigIntegrationConfig"], result)

    @builtins.property
    def monetization_config(
        self,
    ) -> typing.Optional["GoogleApigeeAddonsConfigAddonsConfigMonetizationConfig"]:
        '''monetization_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#monetization_config GoogleApigeeAddonsConfig#monetization_config}
        '''
        result = self._values.get("monetization_config")
        return typing.cast(typing.Optional["GoogleApigeeAddonsConfigAddonsConfigMonetizationConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeAddonsConfigAddonsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeAddonsConfig.GoogleApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Flag that specifies whether the Advanced API Ops add-on is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#enabled GoogleApigeeAddonsConfig#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4038fbea3ddce7e57cbec33387815704b666e861d5e05ac681c203bc291af2bf)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag that specifies whether the Advanced API Ops add-on is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#enabled GoogleApigeeAddonsConfig#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeAddonsConfig.GoogleApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e86814004c49c696e3442d757beeaef7c2efb943f9f51ea424a55ed9dc1b301f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b0e55044573784214782416db5a77a3025900793379ff7e95395624f7fc95fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig]:
        return typing.cast(typing.Optional[GoogleApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7326540067b7f6d58f3b01683b438583a2aae88702a0fba21e89a1c6b3e0c6b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeAddonsConfig.GoogleApigeeAddonsConfigAddonsConfigApiSecurityConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleApigeeAddonsConfigAddonsConfigApiSecurityConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Flag that specifies whether the API security add-on is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#enabled GoogleApigeeAddonsConfig#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7e17eb90f795f6cc7d7819492adf793760bdc9b3a08cc49c1c90a3158121a26)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag that specifies whether the API security add-on is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#enabled GoogleApigeeAddonsConfig#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeAddonsConfigAddonsConfigApiSecurityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeAddonsConfigAddonsConfigApiSecurityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeAddonsConfig.GoogleApigeeAddonsConfigAddonsConfigApiSecurityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72b6fdf8e46e47b092e957de6588b3300024743b91abc360af17073f0a52119b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="expiresAt")
    def expires_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiresAt"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e4ab16f267557190d9b2dea671324453c206db280d1bfdab53526038982cde0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApigeeAddonsConfigAddonsConfigApiSecurityConfig]:
        return typing.cast(typing.Optional[GoogleApigeeAddonsConfigAddonsConfigApiSecurityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeAddonsConfigAddonsConfigApiSecurityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cad68d33b2b83e78345ca99f03b75f879069cd23f0bdbbbec4d840eb9e3117f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeAddonsConfig.GoogleApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Flag that specifies whether the Connectors Platform add-on is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#enabled GoogleApigeeAddonsConfig#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__702bb693575fc8d6cdc0f23f8ceeffd2df355219468641386eb114acd2ecb544)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag that specifies whether the Connectors Platform add-on is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#enabled GoogleApigeeAddonsConfig#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeAddonsConfigAddonsConfigConnectorsPlatformConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeAddonsConfig.GoogleApigeeAddonsConfigAddonsConfigConnectorsPlatformConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12a57dc53d62f978e1d395dc6c46f3df3cba2c6c8ff837ed493382c86b2d6eb8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="expiresAt")
    def expires_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiresAt"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a4e015f8edb3336d527b5212a69a6ec7e4b8d4292856cd2d0baf13c962665f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig]:
        return typing.cast(typing.Optional[GoogleApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0272d8e34ab0c83d50772f258d37dc6db3757ef28a8d7c09685936328e40e238)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeAddonsConfig.GoogleApigeeAddonsConfigAddonsConfigIntegrationConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleApigeeAddonsConfigAddonsConfigIntegrationConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Flag that specifies whether the Integration add-on is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#enabled GoogleApigeeAddonsConfig#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de3ef30203ee2a4856c2c336e27e51a93d8d6a2e8074523bba69d5ca1f279c2f)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag that specifies whether the Integration add-on is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#enabled GoogleApigeeAddonsConfig#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeAddonsConfigAddonsConfigIntegrationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeAddonsConfigAddonsConfigIntegrationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeAddonsConfig.GoogleApigeeAddonsConfigAddonsConfigIntegrationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__965868f309888731eadbdf1912257e19d83275b11fbf7251eb8b085de11f6261)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1393485fc371da117024661e6a8a496ccf7a6954ed8a6007128db3820f802782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApigeeAddonsConfigAddonsConfigIntegrationConfig]:
        return typing.cast(typing.Optional[GoogleApigeeAddonsConfigAddonsConfigIntegrationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeAddonsConfigAddonsConfigIntegrationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d695134bdf4be1861f1cf79a709e1d4dab1c7dd9ec7d863bc50a4afa5f6f2c67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeAddonsConfig.GoogleApigeeAddonsConfigAddonsConfigMonetizationConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleApigeeAddonsConfigAddonsConfigMonetizationConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Flag that specifies whether the Monetization add-on is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#enabled GoogleApigeeAddonsConfig#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb74b1b7779b7d204bc7962ddbcd77f922c28ee8d02772ffcffa3397e65e641)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag that specifies whether the Monetization add-on is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#enabled GoogleApigeeAddonsConfig#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeAddonsConfigAddonsConfigMonetizationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeAddonsConfigAddonsConfigMonetizationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeAddonsConfig.GoogleApigeeAddonsConfigAddonsConfigMonetizationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1cf2588ffa79bb8325aee94b604d889f22926006d437781d547bcc1d66278f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c041f6a4fdee75ba962566cdb7fd5457946fa095fa2873d02977e76e325c079e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApigeeAddonsConfigAddonsConfigMonetizationConfig]:
        return typing.cast(typing.Optional[GoogleApigeeAddonsConfigAddonsConfigMonetizationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeAddonsConfigAddonsConfigMonetizationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fece17a38dc2aad29e54b296f82a07075202439ef64e702e1ec74150e7aa6297)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeAddonsConfigAddonsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeAddonsConfig.GoogleApigeeAddonsConfigAddonsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4dd6dcdbb3aed273f415ff2913e3b09c67668c3596193d2c4a467dad86ea4812)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdvancedApiOpsConfig")
    def put_advanced_api_ops_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Flag that specifies whether the Advanced API Ops add-on is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#enabled GoogleApigeeAddonsConfig#enabled}
        '''
        value = GoogleApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedApiOpsConfig", [value]))

    @jsii.member(jsii_name="putApiSecurityConfig")
    def put_api_security_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Flag that specifies whether the API security add-on is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#enabled GoogleApigeeAddonsConfig#enabled}
        '''
        value = GoogleApigeeAddonsConfigAddonsConfigApiSecurityConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putApiSecurityConfig", [value]))

    @jsii.member(jsii_name="putConnectorsPlatformConfig")
    def put_connectors_platform_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Flag that specifies whether the Connectors Platform add-on is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#enabled GoogleApigeeAddonsConfig#enabled}
        '''
        value = GoogleApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putConnectorsPlatformConfig", [value]))

    @jsii.member(jsii_name="putIntegrationConfig")
    def put_integration_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Flag that specifies whether the Integration add-on is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#enabled GoogleApigeeAddonsConfig#enabled}
        '''
        value = GoogleApigeeAddonsConfigAddonsConfigIntegrationConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putIntegrationConfig", [value]))

    @jsii.member(jsii_name="putMonetizationConfig")
    def put_monetization_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Flag that specifies whether the Monetization add-on is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#enabled GoogleApigeeAddonsConfig#enabled}
        '''
        value = GoogleApigeeAddonsConfigAddonsConfigMonetizationConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putMonetizationConfig", [value]))

    @jsii.member(jsii_name="resetAdvancedApiOpsConfig")
    def reset_advanced_api_ops_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedApiOpsConfig", []))

    @jsii.member(jsii_name="resetApiSecurityConfig")
    def reset_api_security_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiSecurityConfig", []))

    @jsii.member(jsii_name="resetConnectorsPlatformConfig")
    def reset_connectors_platform_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectorsPlatformConfig", []))

    @jsii.member(jsii_name="resetIntegrationConfig")
    def reset_integration_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegrationConfig", []))

    @jsii.member(jsii_name="resetMonetizationConfig")
    def reset_monetization_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonetizationConfig", []))

    @builtins.property
    @jsii.member(jsii_name="advancedApiOpsConfig")
    def advanced_api_ops_config(
        self,
    ) -> GoogleApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfigOutputReference:
        return typing.cast(GoogleApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfigOutputReference, jsii.get(self, "advancedApiOpsConfig"))

    @builtins.property
    @jsii.member(jsii_name="apiSecurityConfig")
    def api_security_config(
        self,
    ) -> GoogleApigeeAddonsConfigAddonsConfigApiSecurityConfigOutputReference:
        return typing.cast(GoogleApigeeAddonsConfigAddonsConfigApiSecurityConfigOutputReference, jsii.get(self, "apiSecurityConfig"))

    @builtins.property
    @jsii.member(jsii_name="connectorsPlatformConfig")
    def connectors_platform_config(
        self,
    ) -> GoogleApigeeAddonsConfigAddonsConfigConnectorsPlatformConfigOutputReference:
        return typing.cast(GoogleApigeeAddonsConfigAddonsConfigConnectorsPlatformConfigOutputReference, jsii.get(self, "connectorsPlatformConfig"))

    @builtins.property
    @jsii.member(jsii_name="integrationConfig")
    def integration_config(
        self,
    ) -> GoogleApigeeAddonsConfigAddonsConfigIntegrationConfigOutputReference:
        return typing.cast(GoogleApigeeAddonsConfigAddonsConfigIntegrationConfigOutputReference, jsii.get(self, "integrationConfig"))

    @builtins.property
    @jsii.member(jsii_name="monetizationConfig")
    def monetization_config(
        self,
    ) -> GoogleApigeeAddonsConfigAddonsConfigMonetizationConfigOutputReference:
        return typing.cast(GoogleApigeeAddonsConfigAddonsConfigMonetizationConfigOutputReference, jsii.get(self, "monetizationConfig"))

    @builtins.property
    @jsii.member(jsii_name="advancedApiOpsConfigInput")
    def advanced_api_ops_config_input(
        self,
    ) -> typing.Optional[GoogleApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig]:
        return typing.cast(typing.Optional[GoogleApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig], jsii.get(self, "advancedApiOpsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="apiSecurityConfigInput")
    def api_security_config_input(
        self,
    ) -> typing.Optional[GoogleApigeeAddonsConfigAddonsConfigApiSecurityConfig]:
        return typing.cast(typing.Optional[GoogleApigeeAddonsConfigAddonsConfigApiSecurityConfig], jsii.get(self, "apiSecurityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorsPlatformConfigInput")
    def connectors_platform_config_input(
        self,
    ) -> typing.Optional[GoogleApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig]:
        return typing.cast(typing.Optional[GoogleApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig], jsii.get(self, "connectorsPlatformConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="integrationConfigInput")
    def integration_config_input(
        self,
    ) -> typing.Optional[GoogleApigeeAddonsConfigAddonsConfigIntegrationConfig]:
        return typing.cast(typing.Optional[GoogleApigeeAddonsConfigAddonsConfigIntegrationConfig], jsii.get(self, "integrationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="monetizationConfigInput")
    def monetization_config_input(
        self,
    ) -> typing.Optional[GoogleApigeeAddonsConfigAddonsConfigMonetizationConfig]:
        return typing.cast(typing.Optional[GoogleApigeeAddonsConfigAddonsConfigMonetizationConfig], jsii.get(self, "monetizationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleApigeeAddonsConfigAddonsConfig]:
        return typing.cast(typing.Optional[GoogleApigeeAddonsConfigAddonsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeAddonsConfigAddonsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f935eca74e86af9f510a184010cf74726b1c18773d25a743277100765b071a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeAddonsConfig.GoogleApigeeAddonsConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "org": "org",
        "addons_config": "addonsConfig",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class GoogleApigeeAddonsConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        org: builtins.str,
        addons_config: typing.Optional[typing.Union[GoogleApigeeAddonsConfigAddonsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleApigeeAddonsConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param org: Name of the Apigee organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#org GoogleApigeeAddonsConfig#org}
        :param addons_config: addons_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#addons_config GoogleApigeeAddonsConfig#addons_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#id GoogleApigeeAddonsConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#timeouts GoogleApigeeAddonsConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(addons_config, dict):
            addons_config = GoogleApigeeAddonsConfigAddonsConfig(**addons_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleApigeeAddonsConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c0359d9ee5222e03121f6277d51ba6bd43c6bedd93f5e105bca3ea441e70292)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument addons_config", value=addons_config, expected_type=type_hints["addons_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "org": org,
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
        if addons_config is not None:
            self._values["addons_config"] = addons_config
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
    def org(self) -> builtins.str:
        '''Name of the Apigee organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#org GoogleApigeeAddonsConfig#org}
        '''
        result = self._values.get("org")
        assert result is not None, "Required property 'org' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def addons_config(self) -> typing.Optional[GoogleApigeeAddonsConfigAddonsConfig]:
        '''addons_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#addons_config GoogleApigeeAddonsConfig#addons_config}
        '''
        result = self._values.get("addons_config")
        return typing.cast(typing.Optional[GoogleApigeeAddonsConfigAddonsConfig], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#id GoogleApigeeAddonsConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleApigeeAddonsConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#timeouts GoogleApigeeAddonsConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleApigeeAddonsConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeAddonsConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeAddonsConfig.GoogleApigeeAddonsConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleApigeeAddonsConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#create GoogleApigeeAddonsConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#delete GoogleApigeeAddonsConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#update GoogleApigeeAddonsConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__820cd8e4415ed0c7e0dd3ad08c7dad6169624bda831298c527602beecf879453)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#create GoogleApigeeAddonsConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#delete GoogleApigeeAddonsConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_addons_config#update GoogleApigeeAddonsConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeAddonsConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeAddonsConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeAddonsConfig.GoogleApigeeAddonsConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__890c5b1baf6168d2405314c730f0a2f06181d97255cc07e6b01deeac8c1cec6d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd597ab324dbbb88e9dcce66776541820e09b95f9f208b9a4355a8e7a6f1f272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5b0955edca4565508cb35259499c92f89b80e198bba02a635892b5541e48247)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__229f42f88a0a3d131b961fc0f98f8cfd95db2542662a63f409e7d76a46e71103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeAddonsConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeAddonsConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeAddonsConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e4f4e92aa0b529fba8e064207833757e0687b636c4abf3000639d710767d537)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleApigeeAddonsConfig",
    "GoogleApigeeAddonsConfigAddonsConfig",
    "GoogleApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig",
    "GoogleApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfigOutputReference",
    "GoogleApigeeAddonsConfigAddonsConfigApiSecurityConfig",
    "GoogleApigeeAddonsConfigAddonsConfigApiSecurityConfigOutputReference",
    "GoogleApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig",
    "GoogleApigeeAddonsConfigAddonsConfigConnectorsPlatformConfigOutputReference",
    "GoogleApigeeAddonsConfigAddonsConfigIntegrationConfig",
    "GoogleApigeeAddonsConfigAddonsConfigIntegrationConfigOutputReference",
    "GoogleApigeeAddonsConfigAddonsConfigMonetizationConfig",
    "GoogleApigeeAddonsConfigAddonsConfigMonetizationConfigOutputReference",
    "GoogleApigeeAddonsConfigAddonsConfigOutputReference",
    "GoogleApigeeAddonsConfigConfig",
    "GoogleApigeeAddonsConfigTimeouts",
    "GoogleApigeeAddonsConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f7faa98c571f89d825bc59b7728233e87bb1be4c131e392db3ca70b1fa7bce55(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    org: builtins.str,
    addons_config: typing.Optional[typing.Union[GoogleApigeeAddonsConfigAddonsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleApigeeAddonsConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__a94c231854038b03c6791912b9c2dcdf777b5f16b6373205570f35a02e263d20(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171375282b85a97a4ba71af35e41bfaf1c7250bc42b8fa17dd4550b51759b8ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__894d36d1abe28161f8be009cbdb9974d5082c84acaf56d3c76026029dab11700(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a9d0f0bbe769d3820fcf8f752e544e716d2f145773681992743a3385cd9c846(
    *,
    advanced_api_ops_config: typing.Optional[typing.Union[GoogleApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    api_security_config: typing.Optional[typing.Union[GoogleApigeeAddonsConfigAddonsConfigApiSecurityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    connectors_platform_config: typing.Optional[typing.Union[GoogleApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    integration_config: typing.Optional[typing.Union[GoogleApigeeAddonsConfigAddonsConfigIntegrationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    monetization_config: typing.Optional[typing.Union[GoogleApigeeAddonsConfigAddonsConfigMonetizationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4038fbea3ddce7e57cbec33387815704b666e861d5e05ac681c203bc291af2bf(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e86814004c49c696e3442d757beeaef7c2efb943f9f51ea424a55ed9dc1b301f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0e55044573784214782416db5a77a3025900793379ff7e95395624f7fc95fc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7326540067b7f6d58f3b01683b438583a2aae88702a0fba21e89a1c6b3e0c6b5(
    value: typing.Optional[GoogleApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7e17eb90f795f6cc7d7819492adf793760bdc9b3a08cc49c1c90a3158121a26(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b6fdf8e46e47b092e957de6588b3300024743b91abc360af17073f0a52119b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e4ab16f267557190d9b2dea671324453c206db280d1bfdab53526038982cde0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cad68d33b2b83e78345ca99f03b75f879069cd23f0bdbbbec4d840eb9e3117f(
    value: typing.Optional[GoogleApigeeAddonsConfigAddonsConfigApiSecurityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__702bb693575fc8d6cdc0f23f8ceeffd2df355219468641386eb114acd2ecb544(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a57dc53d62f978e1d395dc6c46f3df3cba2c6c8ff837ed493382c86b2d6eb8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a4e015f8edb3336d527b5212a69a6ec7e4b8d4292856cd2d0baf13c962665f3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0272d8e34ab0c83d50772f258d37dc6db3757ef28a8d7c09685936328e40e238(
    value: typing.Optional[GoogleApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3ef30203ee2a4856c2c336e27e51a93d8d6a2e8074523bba69d5ca1f279c2f(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__965868f309888731eadbdf1912257e19d83275b11fbf7251eb8b085de11f6261(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1393485fc371da117024661e6a8a496ccf7a6954ed8a6007128db3820f802782(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d695134bdf4be1861f1cf79a709e1d4dab1c7dd9ec7d863bc50a4afa5f6f2c67(
    value: typing.Optional[GoogleApigeeAddonsConfigAddonsConfigIntegrationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb74b1b7779b7d204bc7962ddbcd77f922c28ee8d02772ffcffa3397e65e641(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1cf2588ffa79bb8325aee94b604d889f22926006d437781d547bcc1d66278f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c041f6a4fdee75ba962566cdb7fd5457946fa095fa2873d02977e76e325c079e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fece17a38dc2aad29e54b296f82a07075202439ef64e702e1ec74150e7aa6297(
    value: typing.Optional[GoogleApigeeAddonsConfigAddonsConfigMonetizationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dd6dcdbb3aed273f415ff2913e3b09c67668c3596193d2c4a467dad86ea4812(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f935eca74e86af9f510a184010cf74726b1c18773d25a743277100765b071a2(
    value: typing.Optional[GoogleApigeeAddonsConfigAddonsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c0359d9ee5222e03121f6277d51ba6bd43c6bedd93f5e105bca3ea441e70292(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    org: builtins.str,
    addons_config: typing.Optional[typing.Union[GoogleApigeeAddonsConfigAddonsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleApigeeAddonsConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__820cd8e4415ed0c7e0dd3ad08c7dad6169624bda831298c527602beecf879453(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__890c5b1baf6168d2405314c730f0a2f06181d97255cc07e6b01deeac8c1cec6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd597ab324dbbb88e9dcce66776541820e09b95f9f208b9a4355a8e7a6f1f272(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b0955edca4565508cb35259499c92f89b80e198bba02a635892b5541e48247(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__229f42f88a0a3d131b961fc0f98f8cfd95db2542662a63f409e7d76a46e71103(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4f4e92aa0b529fba8e064207833757e0687b636c4abf3000639d710767d537(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeAddonsConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
