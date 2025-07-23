r'''
# `google_apigee_addons_config`

Refer to the Terraform Registry for docs: [`google_apigee_addons_config`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config).
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


class ApigeeAddonsConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeAddonsConfig.ApigeeAddonsConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config google_apigee_addons_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        org: builtins.str,
        addons_config: typing.Optional[typing.Union["ApigeeAddonsConfigAddonsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApigeeAddonsConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config google_apigee_addons_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param org: Name of the Apigee organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#org ApigeeAddonsConfig#org}
        :param addons_config: addons_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#addons_config ApigeeAddonsConfig#addons_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#id ApigeeAddonsConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#timeouts ApigeeAddonsConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b37e39e3f2f7f105f8774d83e16f8a9fa0f48f9a1f908eab658cf150252d0560)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApigeeAddonsConfigConfig(
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
        '''Generates CDKTF code for importing a ApigeeAddonsConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApigeeAddonsConfig to import.
        :param import_from_id: The id of the existing ApigeeAddonsConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApigeeAddonsConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6bd77646f317e7168127f07d4f001371148be9b086ae857f8b04ed5d2508812)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAddonsConfig")
    def put_addons_config(
        self,
        *,
        advanced_api_ops_config: typing.Optional[typing.Union["ApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        api_security_config: typing.Optional[typing.Union["ApigeeAddonsConfigAddonsConfigApiSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connectors_platform_config: typing.Optional[typing.Union["ApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        integration_config: typing.Optional[typing.Union["ApigeeAddonsConfigAddonsConfigIntegrationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        monetization_config: typing.Optional[typing.Union["ApigeeAddonsConfigAddonsConfigMonetizationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_api_ops_config: advanced_api_ops_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#advanced_api_ops_config ApigeeAddonsConfig#advanced_api_ops_config}
        :param api_security_config: api_security_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#api_security_config ApigeeAddonsConfig#api_security_config}
        :param connectors_platform_config: connectors_platform_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#connectors_platform_config ApigeeAddonsConfig#connectors_platform_config}
        :param integration_config: integration_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#integration_config ApigeeAddonsConfig#integration_config}
        :param monetization_config: monetization_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#monetization_config ApigeeAddonsConfig#monetization_config}
        '''
        value = ApigeeAddonsConfigAddonsConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#create ApigeeAddonsConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#delete ApigeeAddonsConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#update ApigeeAddonsConfig#update}.
        '''
        value = ApigeeAddonsConfigTimeouts(create=create, delete=delete, update=update)

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
    def addons_config(self) -> "ApigeeAddonsConfigAddonsConfigOutputReference":
        return typing.cast("ApigeeAddonsConfigAddonsConfigOutputReference", jsii.get(self, "addonsConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApigeeAddonsConfigTimeoutsOutputReference":
        return typing.cast("ApigeeAddonsConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="addonsConfigInput")
    def addons_config_input(self) -> typing.Optional["ApigeeAddonsConfigAddonsConfig"]:
        return typing.cast(typing.Optional["ApigeeAddonsConfigAddonsConfig"], jsii.get(self, "addonsConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApigeeAddonsConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApigeeAddonsConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__654bae4af9c752cb48fd3b0f9e2f33caa76ce80002bd525445808efa9a239187)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb5f6a24589541f3303d968509ac48621852fa29b3f14448b7dc6767fcc7152b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeAddonsConfig.ApigeeAddonsConfigAddonsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "advanced_api_ops_config": "advancedApiOpsConfig",
        "api_security_config": "apiSecurityConfig",
        "connectors_platform_config": "connectorsPlatformConfig",
        "integration_config": "integrationConfig",
        "monetization_config": "monetizationConfig",
    },
)
class ApigeeAddonsConfigAddonsConfig:
    def __init__(
        self,
        *,
        advanced_api_ops_config: typing.Optional[typing.Union["ApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        api_security_config: typing.Optional[typing.Union["ApigeeAddonsConfigAddonsConfigApiSecurityConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connectors_platform_config: typing.Optional[typing.Union["ApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        integration_config: typing.Optional[typing.Union["ApigeeAddonsConfigAddonsConfigIntegrationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        monetization_config: typing.Optional[typing.Union["ApigeeAddonsConfigAddonsConfigMonetizationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_api_ops_config: advanced_api_ops_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#advanced_api_ops_config ApigeeAddonsConfig#advanced_api_ops_config}
        :param api_security_config: api_security_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#api_security_config ApigeeAddonsConfig#api_security_config}
        :param connectors_platform_config: connectors_platform_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#connectors_platform_config ApigeeAddonsConfig#connectors_platform_config}
        :param integration_config: integration_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#integration_config ApigeeAddonsConfig#integration_config}
        :param monetization_config: monetization_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#monetization_config ApigeeAddonsConfig#monetization_config}
        '''
        if isinstance(advanced_api_ops_config, dict):
            advanced_api_ops_config = ApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig(**advanced_api_ops_config)
        if isinstance(api_security_config, dict):
            api_security_config = ApigeeAddonsConfigAddonsConfigApiSecurityConfig(**api_security_config)
        if isinstance(connectors_platform_config, dict):
            connectors_platform_config = ApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig(**connectors_platform_config)
        if isinstance(integration_config, dict):
            integration_config = ApigeeAddonsConfigAddonsConfigIntegrationConfig(**integration_config)
        if isinstance(monetization_config, dict):
            monetization_config = ApigeeAddonsConfigAddonsConfigMonetizationConfig(**monetization_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69251d72d2ff0b7e689642bdcdeb7608477e3ded55c14a13b2545e878a609927)
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
    ) -> typing.Optional["ApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig"]:
        '''advanced_api_ops_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#advanced_api_ops_config ApigeeAddonsConfig#advanced_api_ops_config}
        '''
        result = self._values.get("advanced_api_ops_config")
        return typing.cast(typing.Optional["ApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig"], result)

    @builtins.property
    def api_security_config(
        self,
    ) -> typing.Optional["ApigeeAddonsConfigAddonsConfigApiSecurityConfig"]:
        '''api_security_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#api_security_config ApigeeAddonsConfig#api_security_config}
        '''
        result = self._values.get("api_security_config")
        return typing.cast(typing.Optional["ApigeeAddonsConfigAddonsConfigApiSecurityConfig"], result)

    @builtins.property
    def connectors_platform_config(
        self,
    ) -> typing.Optional["ApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig"]:
        '''connectors_platform_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#connectors_platform_config ApigeeAddonsConfig#connectors_platform_config}
        '''
        result = self._values.get("connectors_platform_config")
        return typing.cast(typing.Optional["ApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig"], result)

    @builtins.property
    def integration_config(
        self,
    ) -> typing.Optional["ApigeeAddonsConfigAddonsConfigIntegrationConfig"]:
        '''integration_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#integration_config ApigeeAddonsConfig#integration_config}
        '''
        result = self._values.get("integration_config")
        return typing.cast(typing.Optional["ApigeeAddonsConfigAddonsConfigIntegrationConfig"], result)

    @builtins.property
    def monetization_config(
        self,
    ) -> typing.Optional["ApigeeAddonsConfigAddonsConfigMonetizationConfig"]:
        '''monetization_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#monetization_config ApigeeAddonsConfig#monetization_config}
        '''
        result = self._values.get("monetization_config")
        return typing.cast(typing.Optional["ApigeeAddonsConfigAddonsConfigMonetizationConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeAddonsConfigAddonsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeAddonsConfig.ApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class ApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Flag that specifies whether the Advanced API Ops add-on is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#enabled ApigeeAddonsConfig#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a1a02b6f07ba94a34d0fe5ca667ab4971557ecde83d88ab90320fa3e239240e)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag that specifies whether the Advanced API Ops add-on is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#enabled ApigeeAddonsConfig#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeAddonsConfig.ApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bae6a7d54d1735721a7cf1143b1cfaffc5526beba6f855bf743cb453da5c24a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc114571a3a9a1894cb5a6d1e34b72a1945b8f9766db7a956ded59b95c9f8e7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig]:
        return typing.cast(typing.Optional[ApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e1e1f6cdb0ec72984def0dbe0006bfe0e1ad38f25b01ffbb68ce4553bf36832)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeAddonsConfig.ApigeeAddonsConfigAddonsConfigApiSecurityConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class ApigeeAddonsConfigAddonsConfigApiSecurityConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Flag that specifies whether the API security add-on is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#enabled ApigeeAddonsConfig#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__094e7de5aa503405b36f2e9f682e1b3cce9ece8ee9ca3543195c9cf1c9d86ac8)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag that specifies whether the API security add-on is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#enabled ApigeeAddonsConfig#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeAddonsConfigAddonsConfigApiSecurityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeAddonsConfigAddonsConfigApiSecurityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeAddonsConfig.ApigeeAddonsConfigAddonsConfigApiSecurityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18e32cf3697fadcc4082bd3dd3fb91870bc4865567c1b2ece135ef7b5c38c60d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05477f09d7eff6ddf747cbb38e1524125f298d651a17fcadb16b3bf7e1a277fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApigeeAddonsConfigAddonsConfigApiSecurityConfig]:
        return typing.cast(typing.Optional[ApigeeAddonsConfigAddonsConfigApiSecurityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeAddonsConfigAddonsConfigApiSecurityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2272c061e722f1b0470adc3fa19e69c86ec686575049873962cf2c9adf78b596)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeAddonsConfig.ApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class ApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Flag that specifies whether the Connectors Platform add-on is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#enabled ApigeeAddonsConfig#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe4ed8969be273376c68c2649520b7b6b4e4d21e766fbdf0c21c0f061faec47f)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag that specifies whether the Connectors Platform add-on is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#enabled ApigeeAddonsConfig#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeAddonsConfigAddonsConfigConnectorsPlatformConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeAddonsConfig.ApigeeAddonsConfigAddonsConfigConnectorsPlatformConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41c409135f0e3b0126a16bb832bc161b02b78febc9fcbcd9b1da092fbc5a44ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__029e5e956d0d1a20784a95bdd1ae02d581b80fc90cf9cd57c8043d139fcb289a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig]:
        return typing.cast(typing.Optional[ApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4f82c8e1aea438d64df93202ce625808dcaff2121f3d45606d6ebd51b823ffe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeAddonsConfig.ApigeeAddonsConfigAddonsConfigIntegrationConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class ApigeeAddonsConfigAddonsConfigIntegrationConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Flag that specifies whether the Integration add-on is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#enabled ApigeeAddonsConfig#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e6dd121256184de9dc9d69cf4bce7d46c3e36a1d2c75f5cbddba36bed6a7657)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag that specifies whether the Integration add-on is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#enabled ApigeeAddonsConfig#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeAddonsConfigAddonsConfigIntegrationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeAddonsConfigAddonsConfigIntegrationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeAddonsConfig.ApigeeAddonsConfigAddonsConfigIntegrationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b330d53341c40a4a8f858c65e043c5ef491e0f6d54761179b5a485f87bdc3186)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bb6b275fdf4b14cb779f4b9af2e83951c3200bbfa84b93c856fdf62fe1cd2cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApigeeAddonsConfigAddonsConfigIntegrationConfig]:
        return typing.cast(typing.Optional[ApigeeAddonsConfigAddonsConfigIntegrationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeAddonsConfigAddonsConfigIntegrationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f21b9687ca784310db45ca37aaca5aa7eea4b1684f1660dad24fcb729c7b22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeAddonsConfig.ApigeeAddonsConfigAddonsConfigMonetizationConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class ApigeeAddonsConfigAddonsConfigMonetizationConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Flag that specifies whether the Monetization add-on is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#enabled ApigeeAddonsConfig#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e509ef9706940604ead5ec5e40656924b88688f7a137a698867a52ae0b75a13b)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag that specifies whether the Monetization add-on is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#enabled ApigeeAddonsConfig#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeAddonsConfigAddonsConfigMonetizationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeAddonsConfigAddonsConfigMonetizationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeAddonsConfig.ApigeeAddonsConfigAddonsConfigMonetizationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20eede662792cae677bbb2f5832eafacb10a405b66044260036ff95acbaccd9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81e6f489d305b132d6fc8d44f501568610cf19e6947298c04ccc6feda7769148)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApigeeAddonsConfigAddonsConfigMonetizationConfig]:
        return typing.cast(typing.Optional[ApigeeAddonsConfigAddonsConfigMonetizationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeAddonsConfigAddonsConfigMonetizationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d427fb2fef316ef02dd7f4e60ed6a7bfd5cb881628536332adf577ba5c12e1bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeAddonsConfigAddonsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeAddonsConfig.ApigeeAddonsConfigAddonsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80d43ab4f26603577fa1cc86b0bb0e2ff710990ab1a52583945232180ce7e1ce)
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
        :param enabled: Flag that specifies whether the Advanced API Ops add-on is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#enabled ApigeeAddonsConfig#enabled}
        '''
        value = ApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putAdvancedApiOpsConfig", [value]))

    @jsii.member(jsii_name="putApiSecurityConfig")
    def put_api_security_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Flag that specifies whether the API security add-on is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#enabled ApigeeAddonsConfig#enabled}
        '''
        value = ApigeeAddonsConfigAddonsConfigApiSecurityConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putApiSecurityConfig", [value]))

    @jsii.member(jsii_name="putConnectorsPlatformConfig")
    def put_connectors_platform_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Flag that specifies whether the Connectors Platform add-on is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#enabled ApigeeAddonsConfig#enabled}
        '''
        value = ApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putConnectorsPlatformConfig", [value]))

    @jsii.member(jsii_name="putIntegrationConfig")
    def put_integration_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Flag that specifies whether the Integration add-on is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#enabled ApigeeAddonsConfig#enabled}
        '''
        value = ApigeeAddonsConfigAddonsConfigIntegrationConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putIntegrationConfig", [value]))

    @jsii.member(jsii_name="putMonetizationConfig")
    def put_monetization_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Flag that specifies whether the Monetization add-on is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#enabled ApigeeAddonsConfig#enabled}
        '''
        value = ApigeeAddonsConfigAddonsConfigMonetizationConfig(enabled=enabled)

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
    ) -> ApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfigOutputReference:
        return typing.cast(ApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfigOutputReference, jsii.get(self, "advancedApiOpsConfig"))

    @builtins.property
    @jsii.member(jsii_name="apiSecurityConfig")
    def api_security_config(
        self,
    ) -> ApigeeAddonsConfigAddonsConfigApiSecurityConfigOutputReference:
        return typing.cast(ApigeeAddonsConfigAddonsConfigApiSecurityConfigOutputReference, jsii.get(self, "apiSecurityConfig"))

    @builtins.property
    @jsii.member(jsii_name="connectorsPlatformConfig")
    def connectors_platform_config(
        self,
    ) -> ApigeeAddonsConfigAddonsConfigConnectorsPlatformConfigOutputReference:
        return typing.cast(ApigeeAddonsConfigAddonsConfigConnectorsPlatformConfigOutputReference, jsii.get(self, "connectorsPlatformConfig"))

    @builtins.property
    @jsii.member(jsii_name="integrationConfig")
    def integration_config(
        self,
    ) -> ApigeeAddonsConfigAddonsConfigIntegrationConfigOutputReference:
        return typing.cast(ApigeeAddonsConfigAddonsConfigIntegrationConfigOutputReference, jsii.get(self, "integrationConfig"))

    @builtins.property
    @jsii.member(jsii_name="monetizationConfig")
    def monetization_config(
        self,
    ) -> ApigeeAddonsConfigAddonsConfigMonetizationConfigOutputReference:
        return typing.cast(ApigeeAddonsConfigAddonsConfigMonetizationConfigOutputReference, jsii.get(self, "monetizationConfig"))

    @builtins.property
    @jsii.member(jsii_name="advancedApiOpsConfigInput")
    def advanced_api_ops_config_input(
        self,
    ) -> typing.Optional[ApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig]:
        return typing.cast(typing.Optional[ApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig], jsii.get(self, "advancedApiOpsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="apiSecurityConfigInput")
    def api_security_config_input(
        self,
    ) -> typing.Optional[ApigeeAddonsConfigAddonsConfigApiSecurityConfig]:
        return typing.cast(typing.Optional[ApigeeAddonsConfigAddonsConfigApiSecurityConfig], jsii.get(self, "apiSecurityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorsPlatformConfigInput")
    def connectors_platform_config_input(
        self,
    ) -> typing.Optional[ApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig]:
        return typing.cast(typing.Optional[ApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig], jsii.get(self, "connectorsPlatformConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="integrationConfigInput")
    def integration_config_input(
        self,
    ) -> typing.Optional[ApigeeAddonsConfigAddonsConfigIntegrationConfig]:
        return typing.cast(typing.Optional[ApigeeAddonsConfigAddonsConfigIntegrationConfig], jsii.get(self, "integrationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="monetizationConfigInput")
    def monetization_config_input(
        self,
    ) -> typing.Optional[ApigeeAddonsConfigAddonsConfigMonetizationConfig]:
        return typing.cast(typing.Optional[ApigeeAddonsConfigAddonsConfigMonetizationConfig], jsii.get(self, "monetizationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApigeeAddonsConfigAddonsConfig]:
        return typing.cast(typing.Optional[ApigeeAddonsConfigAddonsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeAddonsConfigAddonsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94b67d12e427ce5a95ea4ca85ac545f51aeccc02b5a77881e42d77931683549c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeAddonsConfig.ApigeeAddonsConfigConfig",
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
class ApigeeAddonsConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        addons_config: typing.Optional[typing.Union[ApigeeAddonsConfigAddonsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApigeeAddonsConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param org: Name of the Apigee organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#org ApigeeAddonsConfig#org}
        :param addons_config: addons_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#addons_config ApigeeAddonsConfig#addons_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#id ApigeeAddonsConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#timeouts ApigeeAddonsConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(addons_config, dict):
            addons_config = ApigeeAddonsConfigAddonsConfig(**addons_config)
        if isinstance(timeouts, dict):
            timeouts = ApigeeAddonsConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d5b4a8873f12d5946d7edee76cf222a3c3a8f4e720cd4543080139f6aa3fd9d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#org ApigeeAddonsConfig#org}
        '''
        result = self._values.get("org")
        assert result is not None, "Required property 'org' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def addons_config(self) -> typing.Optional[ApigeeAddonsConfigAddonsConfig]:
        '''addons_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#addons_config ApigeeAddonsConfig#addons_config}
        '''
        result = self._values.get("addons_config")
        return typing.cast(typing.Optional[ApigeeAddonsConfigAddonsConfig], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#id ApigeeAddonsConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApigeeAddonsConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#timeouts ApigeeAddonsConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApigeeAddonsConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeAddonsConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeAddonsConfig.ApigeeAddonsConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ApigeeAddonsConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#create ApigeeAddonsConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#delete ApigeeAddonsConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#update ApigeeAddonsConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8e7f73556b00a883722bbf23f7f587eec13d1f7a7cf949577694f9ff0df1255)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#create ApigeeAddonsConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#delete ApigeeAddonsConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_addons_config#update ApigeeAddonsConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeAddonsConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeAddonsConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeAddonsConfig.ApigeeAddonsConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__208fef8bef6758b3043fadb0c8bccc98370879e9e07b8c16dead93f2cb9cd7e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c698eb109abbbe4b8b52d04eed3541ac120c15a70c735f8a4daba3b41231417c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afaa31626f429b5459c0bb7d8ec834fe0f36c7c1759e925b2753ffe07e85e51c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2a3c7de2ed95d3414548c01c491070c9f3e061cf39dabe1666ec82e47765b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeAddonsConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeAddonsConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeAddonsConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d9538358d461e5e1675d8750d25d460d57a69ecfa11939393e68da6e6bc9cdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApigeeAddonsConfig",
    "ApigeeAddonsConfigAddonsConfig",
    "ApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig",
    "ApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfigOutputReference",
    "ApigeeAddonsConfigAddonsConfigApiSecurityConfig",
    "ApigeeAddonsConfigAddonsConfigApiSecurityConfigOutputReference",
    "ApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig",
    "ApigeeAddonsConfigAddonsConfigConnectorsPlatformConfigOutputReference",
    "ApigeeAddonsConfigAddonsConfigIntegrationConfig",
    "ApigeeAddonsConfigAddonsConfigIntegrationConfigOutputReference",
    "ApigeeAddonsConfigAddonsConfigMonetizationConfig",
    "ApigeeAddonsConfigAddonsConfigMonetizationConfigOutputReference",
    "ApigeeAddonsConfigAddonsConfigOutputReference",
    "ApigeeAddonsConfigConfig",
    "ApigeeAddonsConfigTimeouts",
    "ApigeeAddonsConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b37e39e3f2f7f105f8774d83e16f8a9fa0f48f9a1f908eab658cf150252d0560(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    org: builtins.str,
    addons_config: typing.Optional[typing.Union[ApigeeAddonsConfigAddonsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApigeeAddonsConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e6bd77646f317e7168127f07d4f001371148be9b086ae857f8b04ed5d2508812(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__654bae4af9c752cb48fd3b0f9e2f33caa76ce80002bd525445808efa9a239187(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb5f6a24589541f3303d968509ac48621852fa29b3f14448b7dc6767fcc7152b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69251d72d2ff0b7e689642bdcdeb7608477e3ded55c14a13b2545e878a609927(
    *,
    advanced_api_ops_config: typing.Optional[typing.Union[ApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    api_security_config: typing.Optional[typing.Union[ApigeeAddonsConfigAddonsConfigApiSecurityConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    connectors_platform_config: typing.Optional[typing.Union[ApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    integration_config: typing.Optional[typing.Union[ApigeeAddonsConfigAddonsConfigIntegrationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    monetization_config: typing.Optional[typing.Union[ApigeeAddonsConfigAddonsConfigMonetizationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1a02b6f07ba94a34d0fe5ca667ab4971557ecde83d88ab90320fa3e239240e(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bae6a7d54d1735721a7cf1143b1cfaffc5526beba6f855bf743cb453da5c24a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc114571a3a9a1894cb5a6d1e34b72a1945b8f9766db7a956ded59b95c9f8e7e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1e1f6cdb0ec72984def0dbe0006bfe0e1ad38f25b01ffbb68ce4553bf36832(
    value: typing.Optional[ApigeeAddonsConfigAddonsConfigAdvancedApiOpsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__094e7de5aa503405b36f2e9f682e1b3cce9ece8ee9ca3543195c9cf1c9d86ac8(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18e32cf3697fadcc4082bd3dd3fb91870bc4865567c1b2ece135ef7b5c38c60d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05477f09d7eff6ddf747cbb38e1524125f298d651a17fcadb16b3bf7e1a277fc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2272c061e722f1b0470adc3fa19e69c86ec686575049873962cf2c9adf78b596(
    value: typing.Optional[ApigeeAddonsConfigAddonsConfigApiSecurityConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4ed8969be273376c68c2649520b7b6b4e4d21e766fbdf0c21c0f061faec47f(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c409135f0e3b0126a16bb832bc161b02b78febc9fcbcd9b1da092fbc5a44ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029e5e956d0d1a20784a95bdd1ae02d581b80fc90cf9cd57c8043d139fcb289a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4f82c8e1aea438d64df93202ce625808dcaff2121f3d45606d6ebd51b823ffe(
    value: typing.Optional[ApigeeAddonsConfigAddonsConfigConnectorsPlatformConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e6dd121256184de9dc9d69cf4bce7d46c3e36a1d2c75f5cbddba36bed6a7657(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b330d53341c40a4a8f858c65e043c5ef491e0f6d54761179b5a485f87bdc3186(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb6b275fdf4b14cb779f4b9af2e83951c3200bbfa84b93c856fdf62fe1cd2cc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f21b9687ca784310db45ca37aaca5aa7eea4b1684f1660dad24fcb729c7b22(
    value: typing.Optional[ApigeeAddonsConfigAddonsConfigIntegrationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e509ef9706940604ead5ec5e40656924b88688f7a137a698867a52ae0b75a13b(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20eede662792cae677bbb2f5832eafacb10a405b66044260036ff95acbaccd9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81e6f489d305b132d6fc8d44f501568610cf19e6947298c04ccc6feda7769148(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d427fb2fef316ef02dd7f4e60ed6a7bfd5cb881628536332adf577ba5c12e1bc(
    value: typing.Optional[ApigeeAddonsConfigAddonsConfigMonetizationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d43ab4f26603577fa1cc86b0bb0e2ff710990ab1a52583945232180ce7e1ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94b67d12e427ce5a95ea4ca85ac545f51aeccc02b5a77881e42d77931683549c(
    value: typing.Optional[ApigeeAddonsConfigAddonsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d5b4a8873f12d5946d7edee76cf222a3c3a8f4e720cd4543080139f6aa3fd9d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    org: builtins.str,
    addons_config: typing.Optional[typing.Union[ApigeeAddonsConfigAddonsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApigeeAddonsConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8e7f73556b00a883722bbf23f7f587eec13d1f7a7cf949577694f9ff0df1255(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__208fef8bef6758b3043fadb0c8bccc98370879e9e07b8c16dead93f2cb9cd7e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c698eb109abbbe4b8b52d04eed3541ac120c15a70c735f8a4daba3b41231417c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afaa31626f429b5459c0bb7d8ec834fe0f36c7c1759e925b2753ffe07e85e51c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2a3c7de2ed95d3414548c01c491070c9f3e061cf39dabe1666ec82e47765b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d9538358d461e5e1675d8750d25d460d57a69ecfa11939393e68da6e6bc9cdc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeAddonsConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
