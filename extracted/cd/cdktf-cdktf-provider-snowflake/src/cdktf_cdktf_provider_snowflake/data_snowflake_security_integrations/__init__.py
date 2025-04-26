r'''
# `data_snowflake_security_integrations`

Refer to the Terraform Registry for docs: [`data_snowflake_security_integrations`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/security_integrations).
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


class DataSnowflakeSecurityIntegrations(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrations",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/security_integrations snowflake_security_integrations}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        id: typing.Optional[builtins.str] = None,
        like: typing.Optional[builtins.str] = None,
        with_describe: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/security_integrations snowflake_security_integrations} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/security_integrations#id DataSnowflakeSecurityIntegrations#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param like: Filters the output with **case-insensitive** pattern, with support for SQL wildcard characters (``%`` and ``_``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/security_integrations#like DataSnowflakeSecurityIntegrations#like}
        :param with_describe: Runs DESC SECURITY INTEGRATION for each security integration returned by SHOW SECURITY INTEGRATIONS. The output of describe is saved to the description field. By default this value is set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/security_integrations#with_describe DataSnowflakeSecurityIntegrations#with_describe}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fda935dfd98c2be64ec6125dd21308121a313c3c74ebfeb8112d377a15ba3ee1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataSnowflakeSecurityIntegrationsConfig(
            id=id,
            like=like,
            with_describe=with_describe,
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
        '''Generates CDKTF code for importing a DataSnowflakeSecurityIntegrations resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataSnowflakeSecurityIntegrations to import.
        :param import_from_id: The id of the existing DataSnowflakeSecurityIntegrations that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/security_integrations#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataSnowflakeSecurityIntegrations to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b85d53e1cbeaa68951a75c4c16bb948fec5f3e554a9141606dd27bdda2b43b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLike")
    def reset_like(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLike", []))

    @jsii.member(jsii_name="resetWithDescribe")
    def reset_with_describe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWithDescribe", []))

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
    @jsii.member(jsii_name="securityIntegrations")
    def security_integrations(
        self,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsList":
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsList", jsii.get(self, "securityIntegrations"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="likeInput")
    def like_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "likeInput"))

    @builtins.property
    @jsii.member(jsii_name="withDescribeInput")
    def with_describe_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "withDescribeInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b86b5d69d361b6248014b005cfab9c18da0af08c47e3b33001c9664c2110eef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="like")
    def like(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "like"))

    @like.setter
    def like(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48abc963008219363f3a75ab0c357501511980a9473f481cc113412c8d9cd30c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "like", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="withDescribe")
    def with_describe(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "withDescribe"))

    @with_describe.setter
    def with_describe(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be8efc3a9e0ff7eeb4436cc6308fe2e3afe3ac422b3241c877f8873735ad031a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withDescribe", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "id": "id",
        "like": "like",
        "with_describe": "withDescribe",
    },
)
class DataSnowflakeSecurityIntegrationsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        id: typing.Optional[builtins.str] = None,
        like: typing.Optional[builtins.str] = None,
        with_describe: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/security_integrations#id DataSnowflakeSecurityIntegrations#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param like: Filters the output with **case-insensitive** pattern, with support for SQL wildcard characters (``%`` and ``_``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/security_integrations#like DataSnowflakeSecurityIntegrations#like}
        :param with_describe: Runs DESC SECURITY INTEGRATION for each security integration returned by SHOW SECURITY INTEGRATIONS. The output of describe is saved to the description field. By default this value is set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/security_integrations#with_describe DataSnowflakeSecurityIntegrations#with_describe}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24cdf6b2d36a7ec18f5701b2c8a0cc9b6d24ea83606a73439debe9aa634804ee)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument like", value=like, expected_type=type_hints["like"])
            check_type(argname="argument with_describe", value=with_describe, expected_type=type_hints["with_describe"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if like is not None:
            self._values["like"] = like
        if with_describe is not None:
            self._values["with_describe"] = with_describe

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
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/security_integrations#id DataSnowflakeSecurityIntegrations#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def like(self) -> typing.Optional[builtins.str]:
        '''Filters the output with **case-insensitive** pattern, with support for SQL wildcard characters (``%`` and ``_``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/security_integrations#like DataSnowflakeSecurityIntegrations#like}
        '''
        result = self._values.get("like")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def with_describe(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Runs DESC SECURITY INTEGRATION for each security integration returned by SHOW SECURITY INTEGRATIONS.

        The output of describe is saved to the description field. By default this value is set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/security_integrations#with_describe DataSnowflakeSecurityIntegrations#with_describe}
        '''
        result = self._values.get("with_describe")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrations",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrations:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedEmailPatterns",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedEmailPatterns:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedEmailPatterns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedEmailPatternsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedEmailPatternsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1aa22f7835a6719021f05c72d4802d449b14a7dab10a777e4860e9f9afa1bf8c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedEmailPatternsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac3c05bac2f3c83231e3ab0460b2a26a445d6f76508152056b666b1acbc0d9fd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedEmailPatternsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a91fcc409cbc2c41da066c152bb3df7a8e38f0a3768215503bd88372fa4d0f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fb4ad63ba192d587c1c44a09ffa4f316ce470deba295283ee7c5274b163e860)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cda7f109408515fef3e8a214c0687bb2cd27e2b68e1f3c22577d4e6ded11d662)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedEmailPatternsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedEmailPatternsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a401bc73bb7ed3f741a789edccffa5737384ab3f3aff7f93a77ca49a73a6babf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedEmailPatterns]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedEmailPatterns], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedEmailPatterns],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4240277936a8a8d10ec1366210c8968261b1cbeb3f7a7549083af4529927d3f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedUserDomains",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedUserDomains:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedUserDomains(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedUserDomainsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedUserDomainsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec7e93907e4d40e232c2f15576c47ec11c426e21fbba4ad5902426bde14a8a9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedUserDomainsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2edf1fe38606d1e2a32314bd2283691c275853c3a9ba94d7d08eed0767cdb54)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedUserDomainsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__614ccc84099141d778586e22effac0a87c6ef804371e14114d955ea01f9c15ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd174720c3274529648a129e7ed1e0a8ba4f4f75559ca6715a12066f3f766e24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89d6d94572987a016a022ca835e2497613ff4ccceaef7fb6757a14886be2516f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedUserDomainsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedUserDomainsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e49527046fc9f32aeff5f064d4a30421eb6bc38ba366d44e20c280223eee1cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedUserDomains]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedUserDomains], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedUserDomains],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a8e99d1b1c21033edc47782066e2e61818d5b0f000d91199b40fb478dd8f230)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAuthType",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAuthType:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAuthType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAuthTypeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAuthTypeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d0a06f64e67ade2762a1e5f9260c94fe243520ea2e4ad256f81738717b54c5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAuthTypeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5ba903c1d013b1e4372d13bcc3e9365fb602eca816c18333e8621e777ccd5bd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAuthTypeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f77a2e2e573705bd2be0f229a45c7548db93b1a7dc73dbbaff49212c5c83362)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d975ae16472a352e69a63f5e2085fdddbeb9df866e4d0ec365ce6b644f0d3831)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22c2dddaa3a8b9b902e20a72ef6370c12e1c84a3d2f0c3c354f09bbfb2ea9eae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAuthTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAuthTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad421f1dce83b159da2feb84dfc7ce3ed88d7dc3267f96ba2e1a57d4f64e92ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAuthType]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAuthType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAuthType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de4b219e1bd9497859acbb228328030b59584af39a799f9fea4182b3e14a18a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputBlockedRolesListStruct",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputBlockedRolesListStruct:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputBlockedRolesListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputBlockedRolesListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputBlockedRolesListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f80c857e905494d6b98352fa4b37302f58e8975833658d98584425fc9dab0198)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputBlockedRolesListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef8d80c8859a8f2562bc5df81c12e29744df94b6a3269b0ca1f35b3888038142)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputBlockedRolesListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a8c4a0680fb57a02e9bdb3e675be275887114d57c62a1fd2be47feeedd9f9ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ffe47f49c9e20d9a9488976765dd21df4f590902494b771d96cea2a0911e19d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bec82ed0f16cbb70d03657276316cac6c9eb5a1b351a9476247f547c73f9cf82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputBlockedRolesListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputBlockedRolesListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e884014faef640b01da8c58fee9b37a6beeb976fbb017af0600e346dd4834b1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputBlockedRolesListStruct]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputBlockedRolesListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputBlockedRolesListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10eecbfa4ca1cb355f692b888ff312c521c6bbc810cf10eec3cb7efcf242854d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputComment",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputComment:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputComment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputCommentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputCommentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d503826772a2f11991a35f849a60281e1335c1c3f30594a8ee357943599b8395)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputCommentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6b081706e73f6f239793651c203ad64a87c8177050cee652b6e4b1c16df548d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputCommentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f4b036beacde5c2da2a5144117c74e39eb7aebe46fc5e1444189cf67ce7e8a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6adabfe877811eb3786b35f32259a7e9b05777ccc7d5a316f07f6e5ca1bf7ddd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f8e892e52537c3fe58825161d151e6a6facb7d939a57d8e288dd47340d7426d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputCommentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputCommentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0dee3b89e03ab23fed87c607d17e57ca287e0ba0bcc96a207a8050aac9bb3d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputComment]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputComment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputComment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72db83ba58ba543fc6090ca094bfdbc0489d90366117267fcd1b2fb983c4bbc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputEnabled",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputEnabled:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputEnabled(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputEnabledList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputEnabledList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db9f6269fedd6f86e3081c7dfdeb077ad78b041e04a12ba850d6108ff4f2d9ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputEnabledOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64e68ffb03f4d3bb2f8d9a3fca2d9addec66bf79b56cb3ffc90ef20b17429f7e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputEnabledOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16df40abd0f9d3b0d8c6af8d35952bc4acfb7055aac4ef7eb2ffa84d3d8adc91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c9c893293a48ffc8db9f2bb2751c008c6817d9d558328ea565b8f3d718b106e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d12e8a760ae5729d29d34a61a0625fb0594709c72822f8166392c270b8424157)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputEnabledOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputEnabledOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad5370eae603e3c5049a755976ffaf0b00a558d99cf50d69fbcb5acaad24b2ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputEnabled]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputEnabled], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputEnabled],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__377afac12a14aa751617c83896a642e112d5eec4c5577f236b37bafaaf7ae041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAllowedRolesListStruct",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAllowedRolesListStruct:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAllowedRolesListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAllowedRolesListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAllowedRolesListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33bd332f9ae26626bf0a8bfece2b65e48986ee8e94edffbf88a4d5e67f9b808f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAllowedRolesListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__060cebf26c57fa6ba6ec2c1132d4e81d95402cb6d3ac978497774e8e953f8efc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAllowedRolesListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__625786b14777e90e460624352e8e4161cbae4aaead97d1dc5a0daf80ba560b03)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5019aeabb9defaa46eebb080aa6e96fcd257ede62440dd81e5b0001b6029cb8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3d485041c08a72f686b6d1bb749bbdcba987d55552fd37b8cf05ef27325a2e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAllowedRolesListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAllowedRolesListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c83d1b825eb962aa0ae5829fe0b5b087c4e590e7e39174699123e2e57f5ebe9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAllowedRolesListStruct]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAllowedRolesListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAllowedRolesListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fece2b59f521dda28b5ebde47a2361d980a33a7774deb6012b6cddc48d045560)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAnyRoleMode",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAnyRoleMode:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAnyRoleMode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAnyRoleModeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAnyRoleModeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab9d955e45035e095a4614a7a72b507041f5762f2e88e4a1e34f51b01b872064)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAnyRoleModeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d75a321049adabbafac62a91f5131fb6f3de5d855096a8ef8aa4ad1a210a669e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAnyRoleModeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2fdcb2aef0a62df68823c20e9bb24f9477203b481e48d6130037453f34bcbc9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7fb5a92d77c3127912b64bfb2e29384f3b2bebe7d4f7e90fa602ded493c3b8d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6042ecbfb7b16171adfc722a7e3ef984c4b07344fcac36e98f741b188e44be01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAnyRoleModeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAnyRoleModeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ace76009cb09a85715884b4868550346d6f9695f26ae307f434627373e464911)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAnyRoleMode]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAnyRoleMode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAnyRoleMode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d9df4ba4c71fce3ea1399dc82aaf0cbed1611e7d4fd43bde6950843d7619bb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAudienceListStruct",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAudienceListStruct:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAudienceListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAudienceListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAudienceListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f49d5690f1cdc92d9080445c0f505f9d8a3203142a7abe20049f506fef165a28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAudienceListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b00ef2695e0a65636eab65db7e8b050091b2384301abc3d911043a96949e624)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAudienceListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3abb7962fe2c211fcda3e50c9306a407cbf5d235b93dfa75e6d07bb6a77d43a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7757df85d0cec1ff95011da894a33ecb8be29c79f12d4fe76cc389bf6d1dc4cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__458923ebaee16df28d88c64488d787dc06b2f78ba046c63b31dd374f96addaa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAudienceListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAudienceListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__423ccd096f0217c19b3340b5aca2d6a4c354b9458599981bde2ef087f5d8f198)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAudienceListStruct]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAudienceListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAudienceListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__164a9fc3a307bd1c9a1f270e9a2de6370854c212dbbfb5b01342cd974b355eee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthBlockedRolesListStruct",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthBlockedRolesListStruct:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthBlockedRolesListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthBlockedRolesListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthBlockedRolesListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50292f4b791c55cb526973fe9f87e87c663ef02831cca0aff7ab95935f575055)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthBlockedRolesListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cc2e93b32f26b78607f4d109aaa608e2676127223886ec905a5e6c1baa3a16a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthBlockedRolesListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19862027fcd7fecd6b869ebb9b9d45d9e09b60a165fff94b7218a13c339b2bb7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b589e2a5943ac40b25d987bc8d272cf188c7220aaf72f9ad1ba6c7eb6f4ad074)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bf4bbfb6d580fa11d38b1164cf79ec08ba4d858156c569483c7bf99460fe410)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthBlockedRolesListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthBlockedRolesListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a178511bc3b35338b9325e7a43c2f3a599b42a7758879570dccfd40048aaf18)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthBlockedRolesListStruct]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthBlockedRolesListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthBlockedRolesListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__105ababa00c04fa71fa0428f7928d3d97a38761f75307a4e5dd2f84eb6c3c08c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthIssuer",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthIssuer:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthIssuer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthIssuerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthIssuerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f1848869359a1d952c22f9d004df5d4496ae1353497390bb2f0db9a228027e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthIssuerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__662a5ff8a6ecd464921ad75e9f5a006ea07091604d53877f51a528d897077c58)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthIssuerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44be0ea14b025ae8b27549075c6e5c7dfd6d5cdd1fcc7d4dce5c0d41f7097eaa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccf2dd4b479a681eecf6018b99564dfe66aef66c10a17a076b7fb7547f19403c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c3a1659db8d75077ee3858f24e9125bfaac44fbe921eac2525a1d243b892655)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthIssuerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthIssuerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e31126bef8a03e6bfad365acbdeac71bae4f5e1eaaaaff0ce0bc988197277ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthIssuer]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthIssuer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthIssuer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c7cb27918f490760a69ea327cbee74f29ec603b850d9ce469d21f3175611c39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthJwsKeysUrl",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthJwsKeysUrl:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthJwsKeysUrl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthJwsKeysUrlList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthJwsKeysUrlList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7618af8beaf7e5bd2ec19b1a75a4a6cee5992fd7a430c55a5c21e21112093ebc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthJwsKeysUrlOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73c98121d3b79d51685125c17f2ea26a7d4949fca5e0d3f2ca780d3a07792b57)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthJwsKeysUrlOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ecddcee0c4e749adcbe30fdc00eb987e66968457d3105595d14ab7e9d3cca5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c387bd1571e0432322ef9d16ebab3e1bafd6cc6d25625c694a5ce2ea4b4efc9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__016625775fc33824367511a8ed96539ba8c0397f2282f9495f4fdd22321670b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthJwsKeysUrlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthJwsKeysUrlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b99a6999d10ffa329fae8ce1b6c88ad60c6ac67ecabb00f15fbed89759b16665)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthJwsKeysUrl]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthJwsKeysUrl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthJwsKeysUrl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f10140f98c054ea077a9aecdcf8458e8974e72f55bb367d5238ccb73afcff911)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey2",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey2:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey2List(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey2List",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ec13950b22609348963c207e24345e8989411789e69f733e20021073a49bd80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey2OutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__806c790a47818e28c5246e9dd59d98fa0ddc3f141e359fb456911569f2b28358)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey2OutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__361501b568d6e903429f811694dc5ffaa4e1e521eec984eba688fd60298c0267)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44ff2af04395dd13b7494cbe47be9feda04ce14e9b03c3dbfc7a251f48184b85)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b5d916fc97b1ba60cc12393234eedb9e084e3cadc7a3b76a2eded6f346d216b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04ee18c84757d55b57689ddef0ace705b0ab3cf968484adc2cb995dfdf45f856)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey2]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40771a9ec16c52273e91158ba7878895ee134740cd3a6f17446f3f95af5b6303)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKeyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKeyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1efb6fdbff17bcab679cea2f21015eba1dfaab26c96ee4a8738831deef4f63d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKeyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bac97013f6a6fcf2395883bd463626ef16c35ba54b68bea5db8b2343eef65a00)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKeyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50188b2ef3784519f9b2e79224fbf63a6435cce6c9185a6b734be2f265e37d48)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3434f9e9baa217b11427d58c8625b57fd9fba9b2d0a9e29c9c8eff339adf5239)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aaa09a843e5513fe184d71961f85afccee1ed64e045a4f033aedd16c6bebeddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae4153ff203279ca6693087d52f9b66dc10fdd60bdaa0bc4920ba990bb6c6418)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5c3768ad0302f0d8539bb60a75c7cd70954cec6020e342199f3d99457f9d429)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthScopeDelimiter",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthScopeDelimiter:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthScopeDelimiter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthScopeDelimiterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthScopeDelimiterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27ca8daa2c728926ff82d4e1255e4df28bede21193055957868211a1ea194d02)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthScopeDelimiterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1a8b471ae0e7045968ae5af0982cb3185298e17d9c722515dcc9beba189367b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthScopeDelimiterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__076c91f62c216cc53fc0db9ba10c688c5b12594fc7d2defdb258a66108bbd66e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b81189306b293e50d9d7e2811a8c427fa40d286eaec599e7481420d802a9afb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__beb579d0366cdc1b5bba0897c194b0c74b11516bcfecc494e1364f4f60eda7fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthScopeDelimiterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthScopeDelimiterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55a018a7428f6651e308ea93c49acb22f22adf72a9481457e92f093f9e7f4350)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthScopeDelimiter]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthScopeDelimiter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthScopeDelimiter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__204522b07e6b5ae2bb76ab860a5c505c554b9313fb9c4714f2f8cf4feedf513a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthSnowflakeUserMappingAttribute",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthSnowflakeUserMappingAttribute:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthSnowflakeUserMappingAttribute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthSnowflakeUserMappingAttributeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthSnowflakeUserMappingAttributeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72850307b59617c187f882bc32bb1210efd8bcccdfdfaad84900b57022b2b226)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthSnowflakeUserMappingAttributeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e168a1519121d3f3bb9a05090423eebc30330d7b5fa78dbd1143acdfe631c10)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthSnowflakeUserMappingAttributeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da5243d2eb1c9350883f8b9f925691601aec7a3ccb2a4a4f7bb7e8eb03d56cdb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e722f5efdc6cec83577e2f8a55fd7b9816b404015c6d2d23aa76ff4bcaf0c116)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb3b42b7859261cc2235f5961e1278bbc7c4a086bf07400de6f7030a77cabd3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthSnowflakeUserMappingAttributeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthSnowflakeUserMappingAttributeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d2746576f0b3eb539fe5f32403ae809cf6e0986accabad37744ee574b46be1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthSnowflakeUserMappingAttribute]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthSnowflakeUserMappingAttribute], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthSnowflakeUserMappingAttribute],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__103a08ac919b0a2e3db885942b4b410bfc5055ea13b84ff777e35a09f2d9e090)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthTokenUserMappingClaim",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthTokenUserMappingClaim:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthTokenUserMappingClaim(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthTokenUserMappingClaimList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthTokenUserMappingClaimList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c87ca449900e70249e48f909b02362b4e352a2aac5bbc7a586c74228471ab9cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthTokenUserMappingClaimOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a4c998be96fcec40815bbada601edd64563260a771b91960bc7f502d0b56b94)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthTokenUserMappingClaimOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a88b31b50aba2c10978db9296b54bd8686f84d8f6ab55bfe96c9193f38c50877)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f850f2fb557b4585ae8306ea2ead399eda3f8f47c25b0be8809c8f155bbd528f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdc2b4e6d8cefe89c880b578705524514cac49efbb712a500e4588c69d2a4a5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthTokenUserMappingClaimOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthTokenUserMappingClaimOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd352c565397b01604321ada7458d0740c61668ecac1c8acce631d7762ac8ecd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthTokenUserMappingClaim]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthTokenUserMappingClaim], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthTokenUserMappingClaim],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2681e234146dbc23a3d92be52eb0bd2c62e3ceb059cfefe4f929992ef2b84cb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f19093e5bdc124ad5cb79d6f6aa5c8a1563f3a1c5268f408c27cf9f8efed9f0e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a0a4c4e9e53b079c2f43dd99af83218dfe8187633ec22c383014efff8f00422)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4da4af23431a1751a386de5f8486e8bbee3681c2a1ed9751bc0fcc4a9ea7312)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d76bbf0ac8759b5306ef31d4930adba6e91fa2e84c2b259f55c98e243aff3095)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22fa3ee1f6641346e757ce6abfb1cada7c12492ab2eca2451d698b5a7c53a8d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputNetworkPolicy",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputNetworkPolicy:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputNetworkPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputNetworkPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputNetworkPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6eff399786b1fe12281b459c625f20426666ff3bb102b4320b363ba2b2ee758e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputNetworkPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdcbffecc790acd13933e7137165625b723cb8aa23146619ca5d08a9a7a5a251)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputNetworkPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4513ce27e2ddd116ec82e4401480ae881f80d4c63c65149e573ae6bd77b51f8d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__124492547bc57684a9f2269ccbc31d8357ed0454fd3af7cbdfee730d997969c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e5b2a0487057d69fa5a319961768961fc23881baa6c8e54cf4c289a993bd821)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputNetworkPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputNetworkPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7878a43a05686a53337cd3fc28cf1cff73142791a776ce8c550ed01151e654e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputNetworkPolicy]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputNetworkPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputNetworkPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d862091bdcb2facb0aa6fed75a03890640d081ecfabd0b362d3de74a3a467ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAccessTokenValidity",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAccessTokenValidity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAccessTokenValidity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAccessTokenValidityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAccessTokenValidityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c41ac5368e38a976f5f9904fe42fb487743fa241e3eafd342eeece4a1fe01ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAccessTokenValidityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35c691bbeead4c8b2a0db540e1e2fc9ce7b2119ef6b6e4c099deba3ce15f9540)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAccessTokenValidityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff20591d4e86d0a0283bfa54ebb36d716027968da3ceec73070b285f287e3a53)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29e364514e1d4f0d2f6f87aa1e323f89323544341318b396ae9e6a5d64bbe670)
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
            type_hints = typing.get_type_hints(_typecheckingstub__073d4d84cdd355e115196e803fd316b3afd0014513c96ea185590a99ea15ff0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAccessTokenValidityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAccessTokenValidityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fade4aa0079aad4a8318cdb3c594af7edd445a3dfdcc5948564c176dbe5edb1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAccessTokenValidity]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAccessTokenValidity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAccessTokenValidity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0ddf13793dcbae79fa4515bd6d2c47e03464fa1d1aab5d44fcf97c60c201270)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowNonTlsRedirectUri",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowNonTlsRedirectUri:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowNonTlsRedirectUri(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowNonTlsRedirectUriList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowNonTlsRedirectUriList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4324b21226fd47afc79e3a7819ca25f3340233b03cd5fce5f2bd88b57298619b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowNonTlsRedirectUriOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d38aa2bac7803d2104b12495d1aa2e7f663bbdff9ad9fbd41b73ffb7d1d688b5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowNonTlsRedirectUriOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f8945bd92da2936436802d0bca5cbb21d2e35ec0a00bf21f1aa98da88ea03ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53f6dd0eddfa11197dfd433c2cccd5667af1c5485a7a3e08e79dca17343b7289)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e418f61597f57f43fa26aa377ce3982ada1fe0b0f371d6ed7ec73d67a7bfe1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowNonTlsRedirectUriOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowNonTlsRedirectUriOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18cd350d1afdb81cb8004119625c589bae700a454311e0e7052c7e48e2df327e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowNonTlsRedirectUri]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowNonTlsRedirectUri], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowNonTlsRedirectUri],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__088f47e4af780967fc2f5efacd349e8e2be54f6b78e8c9305c152732dcbb2e2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedAuthorizationEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedAuthorizationEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedAuthorizationEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedAuthorizationEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedAuthorizationEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e02f4e90648e5970723c1eac66ff17f867c89ee20103fd666b58e59713fdeaad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedAuthorizationEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a86e8622a4989eecd8aa8339164324aaa52bd46b4ed9cac8a05f92e80101579)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedAuthorizationEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edcab4e4452f19871fa40328b6ae774572a59e38fa92edbf744e8c471c0c9c3b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9d2260ce69450d46acf9ea83618bf8a0f8657b7b4d8fe07a9bb7597b5c2a7ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__301d5657bf1f05dc8fd962b78cecbec03ab8b42aa3cb43cda272da44996dc821)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedAuthorizationEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedAuthorizationEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1d19be79fc74e4e80fc3516b47f3f32ee87485bebf5373b923f4f0286ce1a24)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedAuthorizationEndpoints]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedAuthorizationEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedAuthorizationEndpoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54760ff023dbb7449ffdd00bfa9e34e279fe5d266bee8f2dc35a0c9415a57b8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedScopes",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedScopes:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedScopes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedScopesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedScopesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b7986b456ed785528d0831fc8d3457249ace6465d0d57f0b8c4fd1f70c28e36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedScopesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c52e8eb0011e75de0949dec45024dd986167ab473a6cddfc78c738507037bb4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedScopesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0423a0898afd333dbba61b80ebc9739aefeb25b8ff6869508be4a3d8b726e40)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63ade108b8910427aa88aba5e09920fc5042587c6193ec1de780cf9f42b4a1ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90dec1d582fe263db29e2098c0d504dc4719e1e774cf921be46a6aae10be3682)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedScopesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedScopesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4daf4c9079ddd8b6cc09b471877105517e3ffe3618c14410ca9de0af51b32ecb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedScopes]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedScopes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedScopes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99ed389012cc8a371de3893ce7d58b6342a4dcada826b2a804489b35f60687cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedTokenEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedTokenEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedTokenEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedTokenEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedTokenEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7e50f8a879e9599f98d363c66d873ba3ca93ca0f67e95d0320f7d3f30e1c824)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedTokenEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ae511e79127b6a341fb4979d7ef5c7a34ab2b99d6a9bdd6e54903b6b200ce8b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedTokenEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__916bf0c7dfb6792b86853f8889349848a35e1c06554586e9a50d8c23c06af34b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bff4d9c4dd28156ca4561646dbe40d2124f7c7c865e4c42eb6a39e889c0603f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__085a5ec73e13ed1f699d96869ed335a67b3f36a26da694d296dce4d6d16543ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedTokenEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedTokenEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbf3e83504c834bb5d9312f388879d213d5bb3f8e579f64d4c95005dbc530a41)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedTokenEndpoints]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedTokenEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedTokenEndpoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d82a6c928beaadcaa34575c6b6cccb1345923f577f7648e62624b3fe94fa24a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAuthorizationEndpoint",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAuthorizationEndpoint:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAuthorizationEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAuthorizationEndpointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAuthorizationEndpointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bf20db655c0a037881de1352368fad9da26cf5bac62ae650245bc0336d5f41f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAuthorizationEndpointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef83ecc3420bea1b2725a52eb8759f9cbb3e237c3a9d07fc82bfc7d2cc3031c9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAuthorizationEndpointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e3cf6b5bae15b17831db934620af333459a9d7a3fffee049a38b6050cecc5d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b49cf5fb3f3cca0652f5dd854bb85e57f5760513fcd81d166db64bb06852a6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9dc816a66784ad8d9cabddb7ddb004233a896e14c0c070801bda36fe3c67b97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAuthorizationEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAuthorizationEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85d34f76353a940c9319bf66f37e25cb96fd42bffc78eeba78ee91d7b40f90cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAuthorizationEndpoint]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAuthorizationEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAuthorizationEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90088cf567b15f9e3745f250cbdaa19b71860687c47d62da24e81fd154ab09ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientAuthMethod",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientAuthMethod:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientAuthMethod(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientAuthMethodList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientAuthMethodList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f1f65fdd093fb9970bccf2957d28469af05dab4e94daf56b21fbe4807267a46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientAuthMethodOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79c20bb9dbeec7c05d65ec521f19597069ca9bedf64a1f725545dfcab90e497c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientAuthMethodOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90ca15c15c45f73af1aa487053bb63678f0031f93c3271ff7111542756aa295c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fa5a22defa06c520d3d0e85f2a2cb832eadec2f90c4b0799cc1b747ea66b97f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__317a246821ddfe58a6d5be09dae63670431bf32fd0e41d2646172a2834256558)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientAuthMethodOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientAuthMethodOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__174993dab92c23ff565963fc48ecdb3d693e94111dd962724a587b6d1d2bfb60)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientAuthMethod]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientAuthMethod], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientAuthMethod],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d22e93b52ba1fb44e1d991731e95debc4482709cee1cac61455c26933e33eff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientId",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientId:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientIdList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientIdList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9f12fce51a7cf4c9106ffe6a2b2b8c4af04e869e42b41be76fe1b792f81df01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientIdOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d1fefb5e381e615808e92cb3b38c6dbf64b242f58faa37226c2c235f68032f0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientIdOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73811b90729a02a8666dd7ca0e9827262bde644335196f46ec57ae468866b298)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f25a1c1dde3ffcea3aa45066cf9edd579794311310771b191257ba877718427)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3610519df400d1ab438caf986320ed3d4db3af593a7deb7bb3e4c390a5bdabb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee3ec00ad80bb3a30a9fa9ad6540af7da8779d6407b29e4eced029e642fe59b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientId]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d31d8dfe62d2a2291e9843acaeb819afde579c689053c3b4123957b917cd78eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKey2Fp",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKey2Fp:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKey2Fp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKey2FpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKey2FpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c03a63a2a10841e993f30d3bbf7e135094f8ea7a8a26bd5b90e5d46226bf7d81)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKey2FpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f53f0c23db75be56d37b9d4c5a02d28f12470cc886faf0b3673863e24256d2b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKey2FpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__202b19e8bf30bbe425e811178874b19256a4aacd321918a29f621f8023b240e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b73a4f67cfc08568f820959650a1bc1d7127ce9bbe20ab29c6ef0f5886d3cba8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b08fdfe1737af0f15c73049bc16e8720125c9a3dfa4e2da68b2715f4c021fb95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKey2FpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKey2FpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1439c33001404706e0ad41d46119710a6fd59df14d9e316e9bedffaa631d3ec6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKey2Fp]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKey2Fp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKey2Fp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca7b5b3d0e136af2c4234d13627d090e3a8bd50425cc86afaa8ca48528c1efd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKeyFp",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKeyFp:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKeyFp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKeyFpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKeyFpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e967f226cac296aebb032a26036bb2ec349ace7201600bd5e3b2979ff5c7da3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKeyFpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bea39ee5ba3a28c488173f6b8719f770c08634cd80356d76d75f3d6a1b425e66)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKeyFpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d223c359ae5eca8b435f8c37da081a3b60e99842787aa1c9d2d4ac57392a212)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7476e4d7fe0bf83f06966dda5bc366d150f301b62411d8eb1c16a58e8c2a2a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e17044296319bfba8958dc77ecbd979d1cf72eb0634056bdba2fd45bd08810f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKeyFpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKeyFpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b50d95950b872b5ca70a6704542e11937bd2cf4020b4b1b766acb36657e6226c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKeyFp]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKeyFp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKeyFp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__183031661998505a3e9e99925a2b9163185281219badc7175f3a77666c5fc9a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientType",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientType:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientTypeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientTypeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2575c9bf13a0eaf001931b6a446166d8bb216fe8b0a7ab348adebe7d090eea71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientTypeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48d98bcc2703761309e2c1bcd46ba5318f999599edf0ce1d8e2c524ceed7eddf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientTypeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a40fa59086a63e79d9ee3d1e5abab2691e3f30ea173696f80858a1e81ce8b55)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7633c83dc9be901ee04a77da2073044f79994d0889bbd7e3ac3f3ae4a175bbff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00b7b9f26218bf804a80d27c3f900f40caffb3dfa87cac551d46b53725a91c90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__005f6491ab36e300464e5c969dbb1853e8701aad98649aa367dabc9dc7b59ac8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientType]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25d0e84cdc1795106f89dbdaa4ea903c409a29582e0e95308bbcbc8aeaa17029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthEnforcePkce",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthEnforcePkce:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthEnforcePkce(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthEnforcePkceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthEnforcePkceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8f422159369e6346e7e6d31688529e1b18094b48161e8429ce10aa2166028f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthEnforcePkceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__966013a316b52b8b4cd65138e851c63cf12723cb487924b9f9514da2085cd397)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthEnforcePkceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19442408338c2d3de03fb525ea5b1a7c3b56a5aa899e7a00c8cd38c2c5ee2987)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8bb3d37979edeccaf787f1d63ec4be495dad53957cfb6cda70ebb22d228bab5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd46b4ff1bae791fd4760bc3e1a0b81a975a9c9ce736946a24c3ff3a069e01f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthEnforcePkceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthEnforcePkceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f891ec477eae35733cffb48689c6d1425d1b0cacaaf716c819d7f9d8f9cfbe96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthEnforcePkce]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthEnforcePkce], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthEnforcePkce],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c28693a4f67d6225c9631ee45aaf8a176e0cf836cd275dd2d9fbd8ffe31bc01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthGrant",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthGrant:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthGrant(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthGrantList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthGrantList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8ddd3601b6bc3cdc6d913ac1a585a684cc55c9023fb6a8eb69385cf2a10f41c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthGrantOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dc0c8624232292c21b868cbf7f9c21a6f73a2d1451efbc767ba88bb8cb162c0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthGrantOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e5f2f6e398b5e44a9251d4edbf1a338962545b86539202608539f5467b5b698)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44abaaf4fb219892e9d4c33fafa88914f5ad67745b9da4b4c100e0bce1d8d884)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b429da5b7f1964effe563176cc2f925aded0d96eb25fa1f58565c269ec494b0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthGrantOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthGrantOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15a0a10c538bac04f0a7b251398d456b291cc4a0aafd5887cbbaf0f57f096a8b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthGrant]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthGrant], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthGrant],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ac526e51076fcda0bd63a98042ce4a034b3cb7aac158ffa5b0d633009515548)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthIssueRefreshTokens",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthIssueRefreshTokens:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthIssueRefreshTokens(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthIssueRefreshTokensList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthIssueRefreshTokensList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__048f3b27e0a42691eeb3632bed8af50d3bafeb7a9fe31eb9d306dd5ef2c97145)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthIssueRefreshTokensOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5411d0c4e6c8445d0e92031d3ecf6ecbf14a56813b43c3d1961c4222de56dfe5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthIssueRefreshTokensOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12b1da7394f3b4558a1f4ebc005df5073977ed51825108dadd0524bbd79ce1a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6361a71d6e0e7603d1263df44aa5c029dbf9c507e5a8b033daa7bd758392fdc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45be1bf1c7db7feead17444100007ac7918d4df9954453d0eac2cff2258d8825)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthIssueRefreshTokensOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthIssueRefreshTokensOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e64a84b5306ad05aff6b6b0c44f6e480f1f4040dba6e0d91796d327f21ae207)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthIssueRefreshTokens]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthIssueRefreshTokens], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthIssueRefreshTokens],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28004a4b7d5fb01a9e37ee23557d7878bc8eda69e806667dbad7b46eb3487dbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRedirectUri",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRedirectUri:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRedirectUri(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRedirectUriList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRedirectUriList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c05f302a5bf715a811832020751c46ddbbe5d8e9fa361332709818ea22130e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRedirectUriOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aa3430d46cc910370a4f005f3b732e2e721e51266557a73dbf326751bd7b219)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRedirectUriOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e97582020444dbf8e38c1af6b4449a1a2677383745a2a4cf572b72448ad7b0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f6535a976539c8e25138a77b27329a4b0cf8a861bb6ed82bdd5b8855ead380d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b74d997055a501db82943116f43559ffd2122db62f8af18e565605e0e5c6494e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRedirectUriOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRedirectUriOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfb41d2a1b054a0ec9ee425dd602fc4017b34f399ac3c200e3580e2172fbbaff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRedirectUri]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRedirectUri], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRedirectUri],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3af0a28f57c4b2255150cd894cdd31f81f46193563ced90922628ba5e90e4c11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRefreshTokenValidity",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRefreshTokenValidity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRefreshTokenValidity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRefreshTokenValidityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRefreshTokenValidityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed631c4f20bac2ef080585b2dbb0cd2c5c4df0c8eb7d4feb14d2d1ef529d7a04)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRefreshTokenValidityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ad5c96ceca1a457a4f125adfd4929c7ed31c1b68a0852a49b21ca2d1cfde905)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRefreshTokenValidityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc6aa6a516c9a13aad10d012b37d2efacc2dcdd30c69b4739755e9176e92cd0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccbe0c977d74c9491176444aaa32658706c065754bc96649b2b9998f364ef68f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b051a0c40ef6954d5d93bab2c2ecb00edfcfee7d1ac3b406d938a65af633de44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRefreshTokenValidityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRefreshTokenValidityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f733bbed1d7b9b25483f57a8de2459b69479fb28965ce53e67f29fb838ccb399)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRefreshTokenValidity]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRefreshTokenValidity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRefreshTokenValidity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32b6239e4e34af1eabdc00040daadd937a9bddb9c0af2b002713701a2b095af8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthTokenEndpoint",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthTokenEndpoint:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthTokenEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthTokenEndpointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthTokenEndpointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc774b4b396ad980c6e51f1841df7b712bb7a7510b0eb39ccf5be58ca461756b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthTokenEndpointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bddd3580d3b4cf3f67dcf8408f56040b8e82ff9b5f81bd943a7551a96462b3b6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthTokenEndpointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b732a64726f314851f25555aed999cee7d284180a91649f16ea8e09f310edef3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b3b6ff78fb1b32da72e1bc9d8c860c8e44dc49b28b304f36a9cc4a4f7a76462)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1d9c91c3c882b4817c04429754c2592cd55ff8b438c33cefdbd5ac4d28c9052)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthTokenEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthTokenEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f5f77e51005e7b9531e9c6cbb9d3c08c0468114927343a807179ddb18764d5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthTokenEndpoint]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthTokenEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthTokenEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42482b6405d91d01e5db6c2f81b3e4e32a1f5248d8d3a551a01c89e047036dae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthUseSecondaryRoles",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthUseSecondaryRoles:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthUseSecondaryRoles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthUseSecondaryRolesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthUseSecondaryRolesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5f3ef77690f76a24604ad48a04e14104f60bf3336bc92047cdd52279f48802e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthUseSecondaryRolesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__677fd444fc5250fbb50cc664c1b5fa5aa7d9e8de86b63358e457b21b1c975115)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthUseSecondaryRolesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bb3ebdd8a528eb71d268592d67267ac6ae0faeb247e7418c7cfd1495fe1883a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c60bc3d394f52415e280485286e8c88ef117377a839423e4e68fb78aedcf457)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ef3dc955f994ba143fbbedfbc05f94bd68122c44a6edf457d322c06071f8cd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthUseSecondaryRolesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthUseSecondaryRolesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__950f1b0832b8045533d684a24769e4ba06fb96a8f13cd187ff651b4b60bc807e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthUseSecondaryRoles]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthUseSecondaryRoles], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthUseSecondaryRoles],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__346f715b60cd9c91b9b7dc69e3f8cd0c06c62be420a8faf8eb35a927b080d932)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26060cfdda4f55047dd6ab5a2f341e55b460c66b64612f765920aa5651c1543c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allowedEmailPatterns")
    def allowed_email_patterns(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedEmailPatternsList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedEmailPatternsList, jsii.get(self, "allowedEmailPatterns"))

    @builtins.property
    @jsii.member(jsii_name="allowedUserDomains")
    def allowed_user_domains(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedUserDomainsList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedUserDomainsList, jsii.get(self, "allowedUserDomains"))

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAuthTypeList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAuthTypeList, jsii.get(self, "authType"))

    @builtins.property
    @jsii.member(jsii_name="blockedRolesList")
    def blocked_roles_list(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputBlockedRolesListStructList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputBlockedRolesListStructList, jsii.get(self, "blockedRolesList"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputCommentList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputCommentList, jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputEnabledList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputEnabledList, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthAllowedRolesList")
    def external_oauth_allowed_roles_list(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAllowedRolesListStructList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAllowedRolesListStructList, jsii.get(self, "externalOauthAllowedRolesList"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthAnyRoleMode")
    def external_oauth_any_role_mode(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAnyRoleModeList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAnyRoleModeList, jsii.get(self, "externalOauthAnyRoleMode"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthAudienceList")
    def external_oauth_audience_list(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAudienceListStructList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAudienceListStructList, jsii.get(self, "externalOauthAudienceList"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthBlockedRolesList")
    def external_oauth_blocked_roles_list(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthBlockedRolesListStructList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthBlockedRolesListStructList, jsii.get(self, "externalOauthBlockedRolesList"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthIssuer")
    def external_oauth_issuer(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthIssuerList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthIssuerList, jsii.get(self, "externalOauthIssuer"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthJwsKeysUrl")
    def external_oauth_jws_keys_url(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthJwsKeysUrlList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthJwsKeysUrlList, jsii.get(self, "externalOauthJwsKeysUrl"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthRsaPublicKey")
    def external_oauth_rsa_public_key(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKeyList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKeyList, jsii.get(self, "externalOauthRsaPublicKey"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthRsaPublicKey2")
    def external_oauth_rsa_public_key2(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey2List:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey2List, jsii.get(self, "externalOauthRsaPublicKey2"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthScopeDelimiter")
    def external_oauth_scope_delimiter(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthScopeDelimiterList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthScopeDelimiterList, jsii.get(self, "externalOauthScopeDelimiter"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthSnowflakeUserMappingAttribute")
    def external_oauth_snowflake_user_mapping_attribute(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthSnowflakeUserMappingAttributeList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthSnowflakeUserMappingAttributeList, jsii.get(self, "externalOauthSnowflakeUserMappingAttribute"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthTokenUserMappingClaim")
    def external_oauth_token_user_mapping_claim(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthTokenUserMappingClaimList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthTokenUserMappingClaimList, jsii.get(self, "externalOauthTokenUserMappingClaim"))

    @builtins.property
    @jsii.member(jsii_name="networkPolicy")
    def network_policy(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputNetworkPolicyList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputNetworkPolicyList, jsii.get(self, "networkPolicy"))

    @builtins.property
    @jsii.member(jsii_name="oauthAccessTokenValidity")
    def oauth_access_token_validity(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAccessTokenValidityList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAccessTokenValidityList, jsii.get(self, "oauthAccessTokenValidity"))

    @builtins.property
    @jsii.member(jsii_name="oauthAllowedAuthorizationEndpoints")
    def oauth_allowed_authorization_endpoints(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedAuthorizationEndpointsList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedAuthorizationEndpointsList, jsii.get(self, "oauthAllowedAuthorizationEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="oauthAllowedScopes")
    def oauth_allowed_scopes(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedScopesList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedScopesList, jsii.get(self, "oauthAllowedScopes"))

    @builtins.property
    @jsii.member(jsii_name="oauthAllowedTokenEndpoints")
    def oauth_allowed_token_endpoints(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedTokenEndpointsList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedTokenEndpointsList, jsii.get(self, "oauthAllowedTokenEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="oauthAllowNonTlsRedirectUri")
    def oauth_allow_non_tls_redirect_uri(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowNonTlsRedirectUriList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowNonTlsRedirectUriList, jsii.get(self, "oauthAllowNonTlsRedirectUri"))

    @builtins.property
    @jsii.member(jsii_name="oauthAuthorizationEndpoint")
    def oauth_authorization_endpoint(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAuthorizationEndpointList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAuthorizationEndpointList, jsii.get(self, "oauthAuthorizationEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientAuthMethod")
    def oauth_client_auth_method(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientAuthMethodList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientAuthMethodList, jsii.get(self, "oauthClientAuthMethod"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientId")
    def oauth_client_id(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientIdList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientIdList, jsii.get(self, "oauthClientId"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientRsaPublicKey2Fp")
    def oauth_client_rsa_public_key2_fp(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKey2FpList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKey2FpList, jsii.get(self, "oauthClientRsaPublicKey2Fp"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientRsaPublicKeyFp")
    def oauth_client_rsa_public_key_fp(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKeyFpList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKeyFpList, jsii.get(self, "oauthClientRsaPublicKeyFp"))

    @builtins.property
    @jsii.member(jsii_name="oauthClientType")
    def oauth_client_type(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientTypeList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientTypeList, jsii.get(self, "oauthClientType"))

    @builtins.property
    @jsii.member(jsii_name="oauthEnforcePkce")
    def oauth_enforce_pkce(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthEnforcePkceList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthEnforcePkceList, jsii.get(self, "oauthEnforcePkce"))

    @builtins.property
    @jsii.member(jsii_name="oauthGrant")
    def oauth_grant(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthGrantList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthGrantList, jsii.get(self, "oauthGrant"))

    @builtins.property
    @jsii.member(jsii_name="oauthIssueRefreshTokens")
    def oauth_issue_refresh_tokens(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthIssueRefreshTokensList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthIssueRefreshTokensList, jsii.get(self, "oauthIssueRefreshTokens"))

    @builtins.property
    @jsii.member(jsii_name="oauthRedirectUri")
    def oauth_redirect_uri(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRedirectUriList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRedirectUriList, jsii.get(self, "oauthRedirectUri"))

    @builtins.property
    @jsii.member(jsii_name="oauthRefreshTokenValidity")
    def oauth_refresh_token_validity(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRefreshTokenValidityList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRefreshTokenValidityList, jsii.get(self, "oauthRefreshTokenValidity"))

    @builtins.property
    @jsii.member(jsii_name="oauthTokenEndpoint")
    def oauth_token_endpoint(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthTokenEndpointList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthTokenEndpointList, jsii.get(self, "oauthTokenEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="oauthUseSecondaryRoles")
    def oauth_use_secondary_roles(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthUseSecondaryRolesList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthUseSecondaryRolesList, jsii.get(self, "oauthUseSecondaryRoles"))

    @builtins.property
    @jsii.member(jsii_name="parentIntegration")
    def parent_integration(
        self,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputParentIntegrationList":
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputParentIntegrationList", jsii.get(self, "parentIntegration"))

    @builtins.property
    @jsii.member(jsii_name="preAuthorizedRolesList")
    def pre_authorized_roles_list(
        self,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputPreAuthorizedRolesListStructList":
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputPreAuthorizedRolesListStructList", jsii.get(self, "preAuthorizedRolesList"))

    @builtins.property
    @jsii.member(jsii_name="runAsRole")
    def run_as_role(
        self,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputRunAsRoleList":
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputRunAsRoleList", jsii.get(self, "runAsRole"))

    @builtins.property
    @jsii.member(jsii_name="saml2DigestMethodsUsed")
    def saml2_digest_methods_used(
        self,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2DigestMethodsUsedList":
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2DigestMethodsUsedList", jsii.get(self, "saml2DigestMethodsUsed"))

    @builtins.property
    @jsii.member(jsii_name="saml2EnableSpInitiated")
    def saml2_enable_sp_initiated(
        self,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2EnableSpInitiatedList":
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2EnableSpInitiatedList", jsii.get(self, "saml2EnableSpInitiated"))

    @builtins.property
    @jsii.member(jsii_name="saml2ForceAuthn")
    def saml2_force_authn(
        self,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ForceAuthnList":
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ForceAuthnList", jsii.get(self, "saml2ForceAuthn"))

    @builtins.property
    @jsii.member(jsii_name="saml2Issuer")
    def saml2_issuer(
        self,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2IssuerList":
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2IssuerList", jsii.get(self, "saml2Issuer"))

    @builtins.property
    @jsii.member(jsii_name="saml2PostLogoutRedirectUrl")
    def saml2_post_logout_redirect_url(
        self,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2PostLogoutRedirectUrlList":
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2PostLogoutRedirectUrlList", jsii.get(self, "saml2PostLogoutRedirectUrl"))

    @builtins.property
    @jsii.member(jsii_name="saml2Provider")
    def saml2_provider(
        self,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ProviderList":
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ProviderList", jsii.get(self, "saml2Provider"))

    @builtins.property
    @jsii.member(jsii_name="saml2RequestedNameidFormat")
    def saml2_requested_nameid_format(
        self,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2RequestedNameidFormatList":
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2RequestedNameidFormatList", jsii.get(self, "saml2RequestedNameidFormat"))

    @builtins.property
    @jsii.member(jsii_name="saml2SignatureMethodsUsed")
    def saml2_signature_methods_used(
        self,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignatureMethodsUsedList":
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignatureMethodsUsedList", jsii.get(self, "saml2SignatureMethodsUsed"))

    @builtins.property
    @jsii.member(jsii_name="saml2SignRequest")
    def saml2_sign_request(
        self,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignRequestList":
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignRequestList", jsii.get(self, "saml2SignRequest"))

    @builtins.property
    @jsii.member(jsii_name="saml2SnowflakeAcsUrl")
    def saml2_snowflake_acs_url(
        self,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeAcsUrlList":
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeAcsUrlList", jsii.get(self, "saml2SnowflakeAcsUrl"))

    @builtins.property
    @jsii.member(jsii_name="saml2SnowflakeIssuerUrl")
    def saml2_snowflake_issuer_url(
        self,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeIssuerUrlList":
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeIssuerUrlList", jsii.get(self, "saml2SnowflakeIssuerUrl"))

    @builtins.property
    @jsii.member(jsii_name="saml2SnowflakeMetadata")
    def saml2_snowflake_metadata(
        self,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeMetadataList":
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeMetadataList", jsii.get(self, "saml2SnowflakeMetadata"))

    @builtins.property
    @jsii.member(jsii_name="saml2SnowflakeX509Cert")
    def saml2_snowflake_x509_cert(
        self,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeX509CertList":
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeX509CertList", jsii.get(self, "saml2SnowflakeX509Cert"))

    @builtins.property
    @jsii.member(jsii_name="saml2SpInitiatedLoginPageLabel")
    def saml2_sp_initiated_login_page_label(
        self,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SpInitiatedLoginPageLabelList":
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SpInitiatedLoginPageLabelList", jsii.get(self, "saml2SpInitiatedLoginPageLabel"))

    @builtins.property
    @jsii.member(jsii_name="saml2SsoUrl")
    def saml2_sso_url(
        self,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SsoUrlList":
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SsoUrlList", jsii.get(self, "saml2SsoUrl"))

    @builtins.property
    @jsii.member(jsii_name="saml2X509Cert")
    def saml2_x509_cert(
        self,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2X509CertList":
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2X509CertList", jsii.get(self, "saml2X509Cert"))

    @builtins.property
    @jsii.member(jsii_name="syncPassword")
    def sync_password(
        self,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSyncPasswordList":
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSyncPasswordList", jsii.get(self, "syncPassword"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutput]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35df92f838e580f09ac05210cb6f9163d88f5577f80ec14671632f0b868b2ea5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputParentIntegration",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputParentIntegration:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputParentIntegration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputParentIntegrationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputParentIntegrationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c33777ccf4219c87d04a96f54d6dbebe88fd90d7fe068c872c5044fc619781ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputParentIntegrationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__975ac1c4b0343b14377e8ec59aff5280414cb13410da69a876a1594ec367248c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputParentIntegrationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f465916f8dd108e2ea81ff9ed864653a8b0d8fa564df251f70484aa36ff69c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae3ab44c9c16af7a71ab6aceb13868c58b2b4889b35e1372b902b7bade3cae4d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8410b458c6d9393b9a250eec9b106a5efaa400d49c81a629b2fa71c6038e15d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputParentIntegrationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputParentIntegrationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1898c6e85441bc6fa6a10e13be9313c876acdfa660abe890dcd8e41c5c35b30)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputParentIntegration]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputParentIntegration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputParentIntegration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96d6563b917e7903e5516217c4e0a8b3557897f3fb1d8a68b140266cb9f5a870)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputPreAuthorizedRolesListStruct",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputPreAuthorizedRolesListStruct:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputPreAuthorizedRolesListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputPreAuthorizedRolesListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputPreAuthorizedRolesListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b954fba4a0e840c0a0eb10c30aa7896267aa5afa21badb11d042ee87ac07296)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputPreAuthorizedRolesListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c2739f047d3e870ec4c3d08f0f59cc8ceb55ed36692ba2ed59c7156be4df30e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputPreAuthorizedRolesListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e1f07c700ce98a3f6db5567a4410a51a4ed8c65c4a2c5d8ce60ee6817ecbc00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59fef248f82800e23bb530f980a2730d5be7e570db8761408561d1aca2ab8d8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__04f2d64994e921897c475f9e73e3180a071cae63855505f3a34468d57c8b1560)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputPreAuthorizedRolesListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputPreAuthorizedRolesListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__960e8ecca4b63b082f55c6995ba187e281f40d1cc7dee25eda386a2974de286e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputPreAuthorizedRolesListStruct]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputPreAuthorizedRolesListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputPreAuthorizedRolesListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42830aa2f2a4c2b7a760d43436da32f791167cf640aa8f5fe9dd22072a3004ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputRunAsRole",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputRunAsRole:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputRunAsRole(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputRunAsRoleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputRunAsRoleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2fff7646f99f3e0b9fa5f79f6a4d83dc6ca092506210b063149d23fb6c96847)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputRunAsRoleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4762f7eb94d6df3c46825ff15b289b9176de47c7fb5d1fe7c7d238a7db709ef8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputRunAsRoleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e68f74a9ba8bbad493c5522f970b2ad0eacf216d04a77ef01e49130c9af117b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0493e2b421d96a7ede89b75c6395bb076a380839576069becc3285a0b03c6d31)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f0dd03ac99a48a89f6d685b14c220d9ace8917d2c670c791ddd6106b7b67978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputRunAsRoleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputRunAsRoleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7471e591270bca74193da9dab5f14ff79d080e9df7cf515a5faf0398dbf61a87)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputRunAsRole]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputRunAsRole], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputRunAsRole],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__315343ef4438bc696454d3fc88f877ebe5c85a046d1d87627fe7e348604974a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2DigestMethodsUsed",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2DigestMethodsUsed:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2DigestMethodsUsed(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2DigestMethodsUsedList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2DigestMethodsUsedList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9d66a28cfc72e1498d59d2db3511fb3b5d550b8b9afa71cd15ca591c49d911c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2DigestMethodsUsedOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b706b26f532a673ea37db8b119eea43a9e23496a009bf9b6c447167f4c845f9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2DigestMethodsUsedOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f496841191ebbffe5a1b84b21190f99a1293a00819c140700881ca2fe6ba175a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24475066063d1c97cf958035baa3e89df97ae35f15f5cacebc12e2a76bed05bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bbadc4af83905789df2fe1e08127a0fa08ad187739d322cfce3564e99fa26d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2DigestMethodsUsedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2DigestMethodsUsedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f262e0d040618c37a39a6e6feaaafb11e058c76c0b7f61fb9bfb4a76d5bde6ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2DigestMethodsUsed]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2DigestMethodsUsed], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2DigestMethodsUsed],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66417e9e5e1e32ae0e7268c9c0ddfa130299b5a5e8ee62c4cfe1c71ce5a05115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2EnableSpInitiated",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2EnableSpInitiated:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2EnableSpInitiated(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2EnableSpInitiatedList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2EnableSpInitiatedList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__131a89f03f3d0d7ff0ba1b711eefc2b73541c3d9fe06dfe2a2356783abc62f13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2EnableSpInitiatedOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4106e15b97a48a30e5c7c640ca20d1d7c29b76fb7a44b19975b2ddafd214407)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2EnableSpInitiatedOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b743722784264b2dcdd23c3e67ea6a6d9199442812a9672cb7fb9126245339cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__730d3aed5fef44e73dc1bb436eb07580798287b5c26f8af7c0fc4bfe634f33bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74b52a8b598fbe548f6410813b5883c542c7791dcedf0bc892207291eb18e326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2EnableSpInitiatedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2EnableSpInitiatedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8fde491e09810573a1dc37c3b2481548689a69379ecbf8001a41998f724b770)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2EnableSpInitiated]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2EnableSpInitiated], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2EnableSpInitiated],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ff7d59e51133990fca07ed13e0aa2fcbb009df783cfb365533f3588a2ece306)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ForceAuthn",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ForceAuthn:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ForceAuthn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ForceAuthnList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ForceAuthnList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1218f1249b5cd17926bbb0ef0fc9c86f7d58c9bb9be22afae5a6a9f3a5e2e171)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ForceAuthnOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fcad2a51977ba658126b4c4040ff40859abad8c64f86c64e76cb97704abb433)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ForceAuthnOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11b2b19fb0a0f77e681ecabb51f3bd05e34022f0b6922754ad4531e7ef364397)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67c6e774d0de9c22a86f857fc3c5bc64d83c34478447f7d5273e121a8781f59a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8660596d25929474303fb0758f8d0ddc16d7958af46201fa2fb63083e833af39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ForceAuthnOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ForceAuthnOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eef7cec26f49e8d13271ee2be3c44aa2a8e5babdde80a8bc37060c7835a059da)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ForceAuthn]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ForceAuthn], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ForceAuthn],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a8794218588317b6b7da44749e0214d1dd5400579199ed7c9f39099c5957490)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2Issuer",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2Issuer:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2Issuer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2IssuerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2IssuerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03fed3e7f42ffcd6c0d466fbd28d5953bd33e9e688d6eced3b44eb254d756b75)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2IssuerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03de32ff72161ecf676d7420dcbd3de3a7a9c642c078bc17a8f8351093103513)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2IssuerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d41415294db2d9b645aff5f02e3f087b5f0c8ae93601051432b44764d22bcc0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cb8b2ad65df9f1a1e1b84245150dbfd3f96d5cdc6773556017fbd2125199795)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43515213a454cba3ff50d913cf2f318a7ff241c2143bc5e28d58e53942f9c22b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2IssuerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2IssuerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cb5a1ea7eea835877258c9a0ad8de0018ee71cb18ff7bb3a177d97549aee89d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2Issuer]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2Issuer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2Issuer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76966b25c112450c128100cb93c5f64c8197ed8d6649e32ca092cd8a51a92501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2PostLogoutRedirectUrl",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2PostLogoutRedirectUrl:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2PostLogoutRedirectUrl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2PostLogoutRedirectUrlList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2PostLogoutRedirectUrlList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32dc41bb25961d37e7803e6cb77af57a21a2cc93164706432b4086550b507f71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2PostLogoutRedirectUrlOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5febd750d3f5aa580d5c960d9a2c819448e9ffc8cc567c9f674911e000e678f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2PostLogoutRedirectUrlOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12b08c1971fb179375e16faec0c736c40c93c89f1d1e6d9d3771d1ffd09c8fa7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b4b2424df497e2f8d75b57f716724b7e2af99a4d97d150351926f2a7973b496)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f82a60eb42401d482209c84dfe9bbfcaa5d1ff695a07d9a5348d993d77809cfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2PostLogoutRedirectUrlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2PostLogoutRedirectUrlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2602beee8e5bd1a615e8d1adcc207f8b36c6ceeb787ede5d24d759482f214280)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2PostLogoutRedirectUrl]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2PostLogoutRedirectUrl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2PostLogoutRedirectUrl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13d296b715107268b107ed9a47e5da334d838db76c7cbf9b3646e30814c3d4cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2Provider",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2Provider:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2Provider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ProviderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ProviderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10e2508869664a1d18a246d4597023300a837ea0e3501a913876bb91658cb212)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ProviderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8301097c10c08ab31e1cda9c24741e55dec9db4a23d342b90819dc9c7752c1bf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ProviderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30ee67fe5b4b690b4f3d3548e92f9d026f31cff38ab151a9c0e11196fcf33db7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fec2de299c4aa9ff940f62e8a771d15a4a0b6287766e0ac947efcd3992c6e4a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea8f00eb28b9343bf2dcbf1bcc585590ecd764459ac10684b7d2e84ce5845f1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ProviderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ProviderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1b1d0f0194a4992e9c020bff4199d418f963f017426cd48e33fc3d7b7cbc331)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2Provider]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2Provider], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2Provider],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6645314bbcac5e99318cd279d0867d636eade3d8f7a1ffeec7e090d15f41c908)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2RequestedNameidFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2RequestedNameidFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2RequestedNameidFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2RequestedNameidFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2RequestedNameidFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f87dd8fe7fc7b9d689ffd968d2ac900316ecacf76e3813242825d36049bd7c69)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2RequestedNameidFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19984ab0c12cff67762e19092f428f14d294f14cf257d0a903893044e13ff47)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2RequestedNameidFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73d520d0afe242d1015c1609e61c1049bf973c4228e753a2b89f300e7c951c9a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea99a6cd8358ae5308d1abc32ef05bc1b69389c038ed7a78796a356289a23c9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e716ab31c1a97db89232f85c969599118c82baceeb7ce692346e83499ed2977f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2RequestedNameidFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2RequestedNameidFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56e86200f03379944eedd219401c384de3ecd199b2f4bf8f61e5902318353776)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2RequestedNameidFormat]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2RequestedNameidFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2RequestedNameidFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9382af949fb12e6861c1efb06ef5f225f681243da10a57c037be426d63169086)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignRequest",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignRequest:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignRequestList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignRequestList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92c439feed55c84eae06b1fad268910e1a08bbe26dd515a50eeee3962621dbb8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignRequestOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ac6705a66846a4aafa612a810356c11c07e34f8811335e9951fa00d3bd5cb75)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignRequestOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d1b5d3d8798bfe47df60349548c905145b2154cca462a34720c05fa3c9c3ed5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c8737789d637d70c57caef38b29815d4068fbe639951658922205364b961e7e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d1fd00d577447dc21aae45b9891c74aaba5f3fad6a0d9b436d6c3092c4bd516)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a2c01b174ae9783f3290628fd81ee3786686bc8f2e2e20935a7f30aace667ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignRequest]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e037a79bbfaaf9b798ce7f1f2efdd0129096be24a178d285bbd33b9745a52c15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignatureMethodsUsed",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignatureMethodsUsed:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignatureMethodsUsed(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignatureMethodsUsedList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignatureMethodsUsedList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3819a5a681297953653e2c4d5d033ceddaef593ebac8fd36a99f5435ec5bc9ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignatureMethodsUsedOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__840c0b399a3fd4629c8e2e7015d6556738e1f3063a4e91dfc4f1b8a5583e9943)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignatureMethodsUsedOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59c541111629bae41ffe8375b7f7d3800b3575871459289f0529f6127b169651)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5dae65bc1ac8615d3ac2fe533f73e43584833ba9b4c8e9cf593102511b907161)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fbeb342819849e4ce228c57ef8135fc6af63e5e37c40d8ad023dc15b62ffac7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignatureMethodsUsedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignatureMethodsUsedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ee44307b5da4341d0b2c4692880c9fb0de9d9d5def78ea95c1e34ca78cdca18)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignatureMethodsUsed]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignatureMethodsUsed], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignatureMethodsUsed],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fde0e67ca89de6d58b9cb2186ff7d11ab7ddcf138a78a2271b659023c324763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeAcsUrl",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeAcsUrl:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeAcsUrl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeAcsUrlList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeAcsUrlList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac8dfbb20bdb688b236e1375ab1d68ee422275bfef5de317da755332f265e709)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeAcsUrlOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de70e91fd54c2b479a74d800531f87015422e79227a27ee9219534ea9dbfca69)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeAcsUrlOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd523b791e21be38b98013c09c5d4541010884f0a970518b341b30c3015e93e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c20a03c0e3ad1e47967b495dbf59a9c947062cae6e822ac159b72f02355dd142)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8449a0b965963ed122b9e50ae01460afb208aa0ea334924b154db5e9538c57b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeAcsUrlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeAcsUrlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9dafa31af1572a9577200cc078c3188f12bba7fcf8a83cfab87be0d917d933f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeAcsUrl]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeAcsUrl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeAcsUrl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__582122220e214c25033b524e061d2e2e9f2d6b1040e539ec2cef2db175feaa93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeIssuerUrl",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeIssuerUrl:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeIssuerUrl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeIssuerUrlList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeIssuerUrlList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb719effa6ef2e9ff6955b146e45336037c84af6e424a5500a94bed79b923f21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeIssuerUrlOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50f24780080eaf69f439ee13eeee6459626fed0085952d9c9996ce4ec5567e98)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeIssuerUrlOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6faa70e1f8297f6793e8edaa4dbda0a06b2572e771d32a11ca6413cc0a4ff66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ed3de7bf88b8bbd82074b2ad27b400658389c4f4654fdacfee9a85573dd40a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e297d48f420be921788e144174135ad8a7d2021f49c6656307fde5e544c79cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeIssuerUrlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeIssuerUrlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16176f174f6ed2cae5a926b1fb1dd0bfb3760997ca7356ca4acef5a19411d249)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeIssuerUrl]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeIssuerUrl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeIssuerUrl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ced74f110a0bcfeee3970ac644eceac67c6da0d43de806fee9a325cbc1fbd20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeMetadata",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeMetadata:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeMetadataList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeMetadataList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a770b752265f2f30b27b0d57c041534b3eb12076a349252f4e14e381265c973a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeMetadataOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f1eae83fb9ebcb80f4f196e3ad145410a7192c30e9961131933a67debf7ad2e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeMetadataOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39c8ded4a27a8c828552a32231559e049df5e268b8ffeaa981d39e05440d745c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10d649f356e4c0b943cd2eaab6a0aac9c6e2a71351ecbfa81916b601f44aef39)
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
            type_hints = typing.get_type_hints(_typecheckingstub__728265e06319c864d3c48415568375528b43bc2de1ae9ebf24a19db9f82ef31c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f6db52b5f820783f5438f2021e517789ed340d456f2379b03c0214c0dbbf1b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeMetadata]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeMetadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae9c0a69de8a3ec961c29d91bb2e5e6434429c4f5d10acc82d64e41cbe95dac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeX509Cert",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeX509Cert:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeX509Cert(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeX509CertList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeX509CertList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ddcefbb92b596023983d290084a5db087c6448e5cb51e20b3eea50332e53436)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeX509CertOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__832e0902a97e4b41b5e8cf2938e5617b6dee4fca896749b4ae0c3a19120c2b5d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeX509CertOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f8c2267f47071e15c9684d1c3c30f389371ca050cf2936e63a81f93c5f99ed6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__988b5830f7f2847c0fee536247dace27bf58dbe115ce5116cc370a79aaa3bb40)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8f619913fa64ad3a21c588c458255ad962f689cd7d892cc028b6b9568da54d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeX509CertOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeX509CertOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba068687c33f92d0fe10fe147609402766082214d602c533ff6ded6737c28cec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeX509Cert]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeX509Cert], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeX509Cert],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceeac051f6dcb513ee276402abf75a4784e67d4c44b141fccf72e9845ee76b47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SpInitiatedLoginPageLabel",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SpInitiatedLoginPageLabel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SpInitiatedLoginPageLabel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SpInitiatedLoginPageLabelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SpInitiatedLoginPageLabelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b253674b4465e8baf7e14195e2dd9b4ad3294cbb9e7dde9102256060d5bc161)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SpInitiatedLoginPageLabelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__151f1d6b5671a66719c039caac1ff66882b394c0d8db801544614a8d9a27c753)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SpInitiatedLoginPageLabelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eef44db681d7da38c1affdfa9916dd78a8de2f444915c28132bca55b1084ed8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5af9ed88d8501906ccbc3c97b77832cd0f06ddfa13938fb56c24c775652c3e75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b44d5374cb8201870e2ac19c8646d8fbd6b20b831506fc577526f4bbcd471886)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SpInitiatedLoginPageLabelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SpInitiatedLoginPageLabelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd7dfa060d8c6a8207dfaba73a46776dd716436ed923aebfe8deb82e36367ce1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SpInitiatedLoginPageLabel]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SpInitiatedLoginPageLabel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SpInitiatedLoginPageLabel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a5c1e790e7ef5715b105df55c751a5553609c2acbeafbca0633fb3c68f1be52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SsoUrl",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SsoUrl:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SsoUrl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SsoUrlList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SsoUrlList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a07bf3bc9faf96ede63fd6b1304015ec16b305aec66439cf9888e95e0859d3f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SsoUrlOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66710f44c82949b7a92ecb60c141f86a53733d41a9994cca6230235b1cc47a0c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SsoUrlOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af3f9b8d7ff926a4add28f987bef2507b7159cf37dc41305f03a634661ccfa77)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61f6eb0be6fd551125c793a2e1a6ff3bf60d2104fa3edef721ae79f8d7028417)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce95a1efdc18f28bb6140afe51e9c62bc3c31aa0345c7170d2f43403fb39bb8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SsoUrlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SsoUrlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d9b9841409241904a18df80a62b164423082dd6227362218f30c87a224dbd51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SsoUrl]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SsoUrl], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SsoUrl],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b077da7f57ffbbbc4dfa38604920cc54aeb3bea9ddbbf0616aec9d3581891f05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2X509Cert",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2X509Cert:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2X509Cert(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2X509CertList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2X509CertList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af34415d23a25998b282fc9105aa1105576a027c31c4759b400173dc63aae1d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2X509CertOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9debd1bca042e2016d32d695ccd708bdbc68c20b9d08db41cbb2cbcf3aefa9a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2X509CertOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ea63e4800d2a628ea29cf0f751ca408ae0e92d06ffcadf2f41c0fd149142053)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57903864dc26947121f031673e7e96c4cda8a459e886672824a1ff62a70bdb80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5163c3ec5afd80007fb1bb46457f2c11df4f139948ad734949c5e442936b6d4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2X509CertOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2X509CertOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f078369bc92357f27c5f1755b8c07b4e123271bf637c88cd6f4830834c83aa8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2X509Cert]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2X509Cert], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2X509Cert],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41860a6ff51a6ae3a9a9935f456d91ce3bfc55321291297649a067cd96d82424)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSyncPassword",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSyncPassword:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSyncPassword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSyncPasswordList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSyncPasswordList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d8fb17fdc0869e1801ee1656265259b6839910ff95e83acc875557d039957ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSyncPasswordOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e79687a8c802e60d3ce539453647dcf63a5bebed404b3f5c279fef63e1d44185)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSyncPasswordOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__219d30177d52c15e224e6402aafec1f012a13af736649d187cc68a75e771e7cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__75a4fbadfb7e69d18f8657d53e3e4939365d06392e39254ba15b9e7f05b3c4ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__534a13f8ce2d14294f2fd48a3ec12c4e45aef83df5ce79c794a69e100cce1c5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSyncPasswordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSyncPasswordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2c17f08dd1bbc44322e0309608cd0c72e2b60b5062c51d20f24c33746070f92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSyncPassword]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSyncPassword], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSyncPassword],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6d326c2db0712e0e5e2d35885f790fc656fada23fbb39c7a43ae6f04ff8dcd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e0634fff0f9522b9839ef4a9f1b6e62631572cac33032c446b5d522ad73b865)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6fec854948de45f3b7e7897535080c7c55c028b7e30d1e59350acf17c05884f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__019dab347823cfd346ae86d7f216d403897cf11fc6374c5800cc1478b8073b48)
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
            type_hints = typing.get_type_hints(_typecheckingstub__897abf88e7968672294e0a1b6752ba5ae24b6be689125b357418a82e1e6acfe1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b42343faa60762a19e0452367fb1cff5752f5ea04b93859a29cc5a6f0cb91da5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f805d8f1d47b5364db1f8011235ad22f1d1664f90769ad646091e5e2c3142f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="describeOutput")
    def describe_output(
        self,
    ) -> DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputList:
        return typing.cast(DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputList, jsii.get(self, "describeOutput"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(
        self,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsShowOutputList":
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsShowOutputList", jsii.get(self, "showOutput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrations]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35075a23952eba2424c02655327d41da0dfc276786f0443afb62b131caab90b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSecurityIntegrationsSecurityIntegrationsShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSecurityIntegrationsSecurityIntegrationsShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34c07eb81b34ceb3a57ef1534716bc8155e6159496aa3984606d8d68b9e7477e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSecurityIntegrationsSecurityIntegrationsShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b51b3f19ed95bf18aaec23f83c2e015ebc426641778be9a805860c528820129c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSecurityIntegrationsSecurityIntegrationsShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fe48da15354345342a6ff36e5c9cfa9f78aa9a250e9129a0205da2b3cd8399e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da6aa6bc0ce85beb8be8c70b3954b55fd36b1fdf70915e123c8f3915b2c18ca0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ebaf3900a4bfcca2f721b1ac6b9482ba2cbb0f9fcc28c7d244b6494dcfc304a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSecurityIntegrationsSecurityIntegrationsShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSecurityIntegrations.DataSnowflakeSecurityIntegrationsSecurityIntegrationsShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a6e0938ba9360e510093171593a21e595286a76b617903ac18b3c0b2b677742)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "category"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="integrationType")
    def integration_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "integrationType"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsShowOutput]:
        return typing.cast(typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsShowOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0346ac2ba2accd051e9a6ed2db8d28ee53bdc633adbb7b9fb1910a0b1588e628)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataSnowflakeSecurityIntegrations",
    "DataSnowflakeSecurityIntegrationsConfig",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrations",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutput",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedEmailPatterns",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedEmailPatternsList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedEmailPatternsOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedUserDomains",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedUserDomainsList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedUserDomainsOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAuthType",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAuthTypeList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAuthTypeOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputBlockedRolesListStruct",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputBlockedRolesListStructList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputBlockedRolesListStructOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputComment",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputCommentList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputCommentOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputEnabled",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputEnabledList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputEnabledOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAllowedRolesListStruct",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAllowedRolesListStructList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAllowedRolesListStructOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAnyRoleMode",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAnyRoleModeList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAnyRoleModeOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAudienceListStruct",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAudienceListStructList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAudienceListStructOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthBlockedRolesListStruct",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthBlockedRolesListStructList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthBlockedRolesListStructOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthIssuer",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthIssuerList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthIssuerOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthJwsKeysUrl",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthJwsKeysUrlList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthJwsKeysUrlOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey2",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey2List",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey2OutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKeyList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKeyOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthScopeDelimiter",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthScopeDelimiterList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthScopeDelimiterOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthSnowflakeUserMappingAttribute",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthSnowflakeUserMappingAttributeList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthSnowflakeUserMappingAttributeOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthTokenUserMappingClaim",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthTokenUserMappingClaimList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthTokenUserMappingClaimOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputNetworkPolicy",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputNetworkPolicyList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputNetworkPolicyOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAccessTokenValidity",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAccessTokenValidityList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAccessTokenValidityOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowNonTlsRedirectUri",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowNonTlsRedirectUriList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowNonTlsRedirectUriOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedAuthorizationEndpoints",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedAuthorizationEndpointsList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedAuthorizationEndpointsOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedScopes",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedScopesList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedScopesOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedTokenEndpoints",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedTokenEndpointsList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedTokenEndpointsOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAuthorizationEndpoint",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAuthorizationEndpointList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAuthorizationEndpointOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientAuthMethod",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientAuthMethodList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientAuthMethodOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientId",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientIdList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientIdOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKey2Fp",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKey2FpList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKey2FpOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKeyFp",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKeyFpList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKeyFpOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientType",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientTypeList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientTypeOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthEnforcePkce",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthEnforcePkceList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthEnforcePkceOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthGrant",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthGrantList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthGrantOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthIssueRefreshTokens",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthIssueRefreshTokensList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthIssueRefreshTokensOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRedirectUri",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRedirectUriList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRedirectUriOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRefreshTokenValidity",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRefreshTokenValidityList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRefreshTokenValidityOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthTokenEndpoint",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthTokenEndpointList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthTokenEndpointOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthUseSecondaryRoles",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthUseSecondaryRolesList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthUseSecondaryRolesOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputParentIntegration",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputParentIntegrationList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputParentIntegrationOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputPreAuthorizedRolesListStruct",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputPreAuthorizedRolesListStructList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputPreAuthorizedRolesListStructOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputRunAsRole",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputRunAsRoleList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputRunAsRoleOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2DigestMethodsUsed",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2DigestMethodsUsedList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2DigestMethodsUsedOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2EnableSpInitiated",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2EnableSpInitiatedList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2EnableSpInitiatedOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ForceAuthn",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ForceAuthnList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ForceAuthnOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2Issuer",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2IssuerList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2IssuerOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2PostLogoutRedirectUrl",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2PostLogoutRedirectUrlList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2PostLogoutRedirectUrlOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2Provider",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ProviderList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ProviderOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2RequestedNameidFormat",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2RequestedNameidFormatList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2RequestedNameidFormatOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignRequest",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignRequestList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignRequestOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignatureMethodsUsed",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignatureMethodsUsedList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignatureMethodsUsedOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeAcsUrl",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeAcsUrlList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeAcsUrlOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeIssuerUrl",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeIssuerUrlList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeIssuerUrlOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeMetadata",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeMetadataList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeMetadataOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeX509Cert",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeX509CertList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeX509CertOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SpInitiatedLoginPageLabel",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SpInitiatedLoginPageLabelList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SpInitiatedLoginPageLabelOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SsoUrl",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SsoUrlList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SsoUrlOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2X509Cert",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2X509CertList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2X509CertOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSyncPassword",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSyncPasswordList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSyncPasswordOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsOutputReference",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsShowOutput",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsShowOutputList",
    "DataSnowflakeSecurityIntegrationsSecurityIntegrationsShowOutputOutputReference",
]

publication.publish()

def _typecheckingstub__fda935dfd98c2be64ec6125dd21308121a313c3c74ebfeb8112d377a15ba3ee1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    id: typing.Optional[builtins.str] = None,
    like: typing.Optional[builtins.str] = None,
    with_describe: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__81b85d53e1cbeaa68951a75c4c16bb948fec5f3e554a9141606dd27bdda2b43b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b86b5d69d361b6248014b005cfab9c18da0af08c47e3b33001c9664c2110eef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48abc963008219363f3a75ab0c357501511980a9473f481cc113412c8d9cd30c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be8efc3a9e0ff7eeb4436cc6308fe2e3afe3ac422b3241c877f8873735ad031a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24cdf6b2d36a7ec18f5701b2c8a0cc9b6d24ea83606a73439debe9aa634804ee(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    like: typing.Optional[builtins.str] = None,
    with_describe: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aa22f7835a6719021f05c72d4802d449b14a7dab10a777e4860e9f9afa1bf8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac3c05bac2f3c83231e3ab0460b2a26a445d6f76508152056b666b1acbc0d9fd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a91fcc409cbc2c41da066c152bb3df7a8e38f0a3768215503bd88372fa4d0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb4ad63ba192d587c1c44a09ffa4f316ce470deba295283ee7c5274b163e860(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda7f109408515fef3e8a214c0687bb2cd27e2b68e1f3c22577d4e6ded11d662(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a401bc73bb7ed3f741a789edccffa5737384ab3f3aff7f93a77ca49a73a6babf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4240277936a8a8d10ec1366210c8968261b1cbeb3f7a7549083af4529927d3f9(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedEmailPatterns],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec7e93907e4d40e232c2f15576c47ec11c426e21fbba4ad5902426bde14a8a9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2edf1fe38606d1e2a32314bd2283691c275853c3a9ba94d7d08eed0767cdb54(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__614ccc84099141d778586e22effac0a87c6ef804371e14114d955ea01f9c15ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd174720c3274529648a129e7ed1e0a8ba4f4f75559ca6715a12066f3f766e24(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89d6d94572987a016a022ca835e2497613ff4ccceaef7fb6757a14886be2516f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e49527046fc9f32aeff5f064d4a30421eb6bc38ba366d44e20c280223eee1cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a8e99d1b1c21033edc47782066e2e61818d5b0f000d91199b40fb478dd8f230(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAllowedUserDomains],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0a06f64e67ade2762a1e5f9260c94fe243520ea2e4ad256f81738717b54c5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5ba903c1d013b1e4372d13bcc3e9365fb602eca816c18333e8621e777ccd5bd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f77a2e2e573705bd2be0f229a45c7548db93b1a7dc73dbbaff49212c5c83362(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d975ae16472a352e69a63f5e2085fdddbeb9df866e4d0ec365ce6b644f0d3831(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c2dddaa3a8b9b902e20a72ef6370c12e1c84a3d2f0c3c354f09bbfb2ea9eae(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad421f1dce83b159da2feb84dfc7ce3ed88d7dc3267f96ba2e1a57d4f64e92ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de4b219e1bd9497859acbb228328030b59584af39a799f9fea4182b3e14a18a6(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputAuthType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f80c857e905494d6b98352fa4b37302f58e8975833658d98584425fc9dab0198(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef8d80c8859a8f2562bc5df81c12e29744df94b6a3269b0ca1f35b3888038142(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a8c4a0680fb57a02e9bdb3e675be275887114d57c62a1fd2be47feeedd9f9ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ffe47f49c9e20d9a9488976765dd21df4f590902494b771d96cea2a0911e19d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec82ed0f16cbb70d03657276316cac6c9eb5a1b351a9476247f547c73f9cf82(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e884014faef640b01da8c58fee9b37a6beeb976fbb017af0600e346dd4834b1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10eecbfa4ca1cb355f692b888ff312c521c6bbc810cf10eec3cb7efcf242854d(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputBlockedRolesListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d503826772a2f11991a35f849a60281e1335c1c3f30594a8ee357943599b8395(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b081706e73f6f239793651c203ad64a87c8177050cee652b6e4b1c16df548d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f4b036beacde5c2da2a5144117c74e39eb7aebe46fc5e1444189cf67ce7e8a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6adabfe877811eb3786b35f32259a7e9b05777ccc7d5a316f07f6e5ca1bf7ddd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f8e892e52537c3fe58825161d151e6a6facb7d939a57d8e288dd47340d7426d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0dee3b89e03ab23fed87c607d17e57ca287e0ba0bcc96a207a8050aac9bb3d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72db83ba58ba543fc6090ca094bfdbc0489d90366117267fcd1b2fb983c4bbc8(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputComment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9f6269fedd6f86e3081c7dfdeb077ad78b041e04a12ba850d6108ff4f2d9ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e68ffb03f4d3bb2f8d9a3fca2d9addec66bf79b56cb3ffc90ef20b17429f7e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16df40abd0f9d3b0d8c6af8d35952bc4acfb7055aac4ef7eb2ffa84d3d8adc91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c9c893293a48ffc8db9f2bb2751c008c6817d9d558328ea565b8f3d718b106e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12e8a760ae5729d29d34a61a0625fb0594709c72822f8166392c270b8424157(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad5370eae603e3c5049a755976ffaf0b00a558d99cf50d69fbcb5acaad24b2ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__377afac12a14aa751617c83896a642e112d5eec4c5577f236b37bafaaf7ae041(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputEnabled],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33bd332f9ae26626bf0a8bfece2b65e48986ee8e94edffbf88a4d5e67f9b808f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__060cebf26c57fa6ba6ec2c1132d4e81d95402cb6d3ac978497774e8e953f8efc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__625786b14777e90e460624352e8e4161cbae4aaead97d1dc5a0daf80ba560b03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5019aeabb9defaa46eebb080aa6e96fcd257ede62440dd81e5b0001b6029cb8f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d485041c08a72f686b6d1bb749bbdcba987d55552fd37b8cf05ef27325a2e4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83d1b825eb962aa0ae5829fe0b5b087c4e590e7e39174699123e2e57f5ebe9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fece2b59f521dda28b5ebde47a2361d980a33a7774deb6012b6cddc48d045560(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAllowedRolesListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab9d955e45035e095a4614a7a72b507041f5762f2e88e4a1e34f51b01b872064(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75a321049adabbafac62a91f5131fb6f3de5d855096a8ef8aa4ad1a210a669e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2fdcb2aef0a62df68823c20e9bb24f9477203b481e48d6130037453f34bcbc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7fb5a92d77c3127912b64bfb2e29384f3b2bebe7d4f7e90fa602ded493c3b8d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6042ecbfb7b16171adfc722a7e3ef984c4b07344fcac36e98f741b188e44be01(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ace76009cb09a85715884b4868550346d6f9695f26ae307f434627373e464911(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d9df4ba4c71fce3ea1399dc82aaf0cbed1611e7d4fd43bde6950843d7619bb5(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAnyRoleMode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f49d5690f1cdc92d9080445c0f505f9d8a3203142a7abe20049f506fef165a28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b00ef2695e0a65636eab65db7e8b050091b2384301abc3d911043a96949e624(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3abb7962fe2c211fcda3e50c9306a407cbf5d235b93dfa75e6d07bb6a77d43a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7757df85d0cec1ff95011da894a33ecb8be29c79f12d4fe76cc389bf6d1dc4cb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__458923ebaee16df28d88c64488d787dc06b2f78ba046c63b31dd374f96addaa9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__423ccd096f0217c19b3340b5aca2d6a4c354b9458599981bde2ef087f5d8f198(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__164a9fc3a307bd1c9a1f270e9a2de6370854c212dbbfb5b01342cd974b355eee(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthAudienceListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50292f4b791c55cb526973fe9f87e87c663ef02831cca0aff7ab95935f575055(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cc2e93b32f26b78607f4d109aaa608e2676127223886ec905a5e6c1baa3a16a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19862027fcd7fecd6b869ebb9b9d45d9e09b60a165fff94b7218a13c339b2bb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b589e2a5943ac40b25d987bc8d272cf188c7220aaf72f9ad1ba6c7eb6f4ad074(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bf4bbfb6d580fa11d38b1164cf79ec08ba4d858156c569483c7bf99460fe410(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a178511bc3b35338b9325e7a43c2f3a599b42a7758879570dccfd40048aaf18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__105ababa00c04fa71fa0428f7928d3d97a38761f75307a4e5dd2f84eb6c3c08c(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthBlockedRolesListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f1848869359a1d952c22f9d004df5d4496ae1353497390bb2f0db9a228027e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__662a5ff8a6ecd464921ad75e9f5a006ea07091604d53877f51a528d897077c58(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44be0ea14b025ae8b27549075c6e5c7dfd6d5cdd1fcc7d4dce5c0d41f7097eaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf2dd4b479a681eecf6018b99564dfe66aef66c10a17a076b7fb7547f19403c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3a1659db8d75077ee3858f24e9125bfaac44fbe921eac2525a1d243b892655(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e31126bef8a03e6bfad365acbdeac71bae4f5e1eaaaaff0ce0bc988197277ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7cb27918f490760a69ea327cbee74f29ec603b850d9ce469d21f3175611c39(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthIssuer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7618af8beaf7e5bd2ec19b1a75a4a6cee5992fd7a430c55a5c21e21112093ebc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c98121d3b79d51685125c17f2ea26a7d4949fca5e0d3f2ca780d3a07792b57(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ecddcee0c4e749adcbe30fdc00eb987e66968457d3105595d14ab7e9d3cca5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c387bd1571e0432322ef9d16ebab3e1bafd6cc6d25625c694a5ce2ea4b4efc9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016625775fc33824367511a8ed96539ba8c0397f2282f9495f4fdd22321670b5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b99a6999d10ffa329fae8ce1b6c88ad60c6ac67ecabb00f15fbed89759b16665(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10140f98c054ea077a9aecdcf8458e8974e72f55bb367d5238ccb73afcff911(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthJwsKeysUrl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec13950b22609348963c207e24345e8989411789e69f733e20021073a49bd80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806c790a47818e28c5246e9dd59d98fa0ddc3f141e359fb456911569f2b28358(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361501b568d6e903429f811694dc5ffaa4e1e521eec984eba688fd60298c0267(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ff2af04395dd13b7494cbe47be9feda04ce14e9b03c3dbfc7a251f48184b85(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b5d916fc97b1ba60cc12393234eedb9e084e3cadc7a3b76a2eded6f346d216b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ee18c84757d55b57689ddef0ace705b0ab3cf968484adc2cb995dfdf45f856(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40771a9ec16c52273e91158ba7878895ee134740cd3a6f17446f3f95af5b6303(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1efb6fdbff17bcab679cea2f21015eba1dfaab26c96ee4a8738831deef4f63d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac97013f6a6fcf2395883bd463626ef16c35ba54b68bea5db8b2343eef65a00(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50188b2ef3784519f9b2e79224fbf63a6435cce6c9185a6b734be2f265e37d48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3434f9e9baa217b11427d58c8625b57fd9fba9b2d0a9e29c9c8eff339adf5239(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaa09a843e5513fe184d71961f85afccee1ed64e045a4f033aedd16c6bebeddf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae4153ff203279ca6693087d52f9b66dc10fdd60bdaa0bc4920ba990bb6c6418(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c3768ad0302f0d8539bb60a75c7cd70954cec6020e342199f3d99457f9d429(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthRsaPublicKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ca8daa2c728926ff82d4e1255e4df28bede21193055957868211a1ea194d02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1a8b471ae0e7045968ae5af0982cb3185298e17d9c722515dcc9beba189367b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__076c91f62c216cc53fc0db9ba10c688c5b12594fc7d2defdb258a66108bbd66e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b81189306b293e50d9d7e2811a8c427fa40d286eaec599e7481420d802a9afb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb579d0366cdc1b5bba0897c194b0c74b11516bcfecc494e1364f4f60eda7fe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55a018a7428f6651e308ea93c49acb22f22adf72a9481457e92f093f9e7f4350(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__204522b07e6b5ae2bb76ab860a5c505c554b9313fb9c4714f2f8cf4feedf513a(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthScopeDelimiter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72850307b59617c187f882bc32bb1210efd8bcccdfdfaad84900b57022b2b226(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e168a1519121d3f3bb9a05090423eebc30330d7b5fa78dbd1143acdfe631c10(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da5243d2eb1c9350883f8b9f925691601aec7a3ccb2a4a4f7bb7e8eb03d56cdb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e722f5efdc6cec83577e2f8a55fd7b9816b404015c6d2d23aa76ff4bcaf0c116(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb3b42b7859261cc2235f5961e1278bbc7c4a086bf07400de6f7030a77cabd3e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d2746576f0b3eb539fe5f32403ae809cf6e0986accabad37744ee574b46be1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__103a08ac919b0a2e3db885942b4b410bfc5055ea13b84ff777e35a09f2d9e090(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthSnowflakeUserMappingAttribute],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c87ca449900e70249e48f909b02362b4e352a2aac5bbc7a586c74228471ab9cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a4c998be96fcec40815bbada601edd64563260a771b91960bc7f502d0b56b94(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a88b31b50aba2c10978db9296b54bd8686f84d8f6ab55bfe96c9193f38c50877(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f850f2fb557b4585ae8306ea2ead399eda3f8f47c25b0be8809c8f155bbd528f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdc2b4e6d8cefe89c880b578705524514cac49efbb712a500e4588c69d2a4a5d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd352c565397b01604321ada7458d0740c61668ecac1c8acce631d7762ac8ecd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2681e234146dbc23a3d92be52eb0bd2c62e3ceb059cfefe4f929992ef2b84cb4(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputExternalOauthTokenUserMappingClaim],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19093e5bdc124ad5cb79d6f6aa5c8a1563f3a1c5268f408c27cf9f8efed9f0e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a0a4c4e9e53b079c2f43dd99af83218dfe8187633ec22c383014efff8f00422(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4da4af23431a1751a386de5f8486e8bbee3681c2a1ed9751bc0fcc4a9ea7312(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76bbf0ac8759b5306ef31d4930adba6e91fa2e84c2b259f55c98e243aff3095(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22fa3ee1f6641346e757ce6abfb1cada7c12492ab2eca2451d698b5a7c53a8d5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eff399786b1fe12281b459c625f20426666ff3bb102b4320b363ba2b2ee758e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdcbffecc790acd13933e7137165625b723cb8aa23146619ca5d08a9a7a5a251(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4513ce27e2ddd116ec82e4401480ae881f80d4c63c65149e573ae6bd77b51f8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__124492547bc57684a9f2269ccbc31d8357ed0454fd3af7cbdfee730d997969c0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e5b2a0487057d69fa5a319961768961fc23881baa6c8e54cf4c289a993bd821(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7878a43a05686a53337cd3fc28cf1cff73142791a776ce8c550ed01151e654e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d862091bdcb2facb0aa6fed75a03890640d081ecfabd0b362d3de74a3a467ce(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputNetworkPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c41ac5368e38a976f5f9904fe42fb487743fa241e3eafd342eeece4a1fe01ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35c691bbeead4c8b2a0db540e1e2fc9ce7b2119ef6b6e4c099deba3ce15f9540(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff20591d4e86d0a0283bfa54ebb36d716027968da3ceec73070b285f287e3a53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29e364514e1d4f0d2f6f87aa1e323f89323544341318b396ae9e6a5d64bbe670(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073d4d84cdd355e115196e803fd316b3afd0014513c96ea185590a99ea15ff0f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fade4aa0079aad4a8318cdb3c594af7edd445a3dfdcc5948564c176dbe5edb1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0ddf13793dcbae79fa4515bd6d2c47e03464fa1d1aab5d44fcf97c60c201270(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAccessTokenValidity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4324b21226fd47afc79e3a7819ca25f3340233b03cd5fce5f2bd88b57298619b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d38aa2bac7803d2104b12495d1aa2e7f663bbdff9ad9fbd41b73ffb7d1d688b5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f8945bd92da2936436802d0bca5cbb21d2e35ec0a00bf21f1aa98da88ea03ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f6dd0eddfa11197dfd433c2cccd5667af1c5485a7a3e08e79dca17343b7289(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e418f61597f57f43fa26aa377ce3982ada1fe0b0f371d6ed7ec73d67a7bfe1d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18cd350d1afdb81cb8004119625c589bae700a454311e0e7052c7e48e2df327e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088f47e4af780967fc2f5efacd349e8e2be54f6b78e8c9305c152732dcbb2e2c(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowNonTlsRedirectUri],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e02f4e90648e5970723c1eac66ff17f867c89ee20103fd666b58e59713fdeaad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a86e8622a4989eecd8aa8339164324aaa52bd46b4ed9cac8a05f92e80101579(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edcab4e4452f19871fa40328b6ae774572a59e38fa92edbf744e8c471c0c9c3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d2260ce69450d46acf9ea83618bf8a0f8657b7b4d8fe07a9bb7597b5c2a7ee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__301d5657bf1f05dc8fd962b78cecbec03ab8b42aa3cb43cda272da44996dc821(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d19be79fc74e4e80fc3516b47f3f32ee87485bebf5373b923f4f0286ce1a24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54760ff023dbb7449ffdd00bfa9e34e279fe5d266bee8f2dc35a0c9415a57b8c(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedAuthorizationEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b7986b456ed785528d0831fc8d3457249ace6465d0d57f0b8c4fd1f70c28e36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c52e8eb0011e75de0949dec45024dd986167ab473a6cddfc78c738507037bb4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0423a0898afd333dbba61b80ebc9739aefeb25b8ff6869508be4a3d8b726e40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ade108b8910427aa88aba5e09920fc5042587c6193ec1de780cf9f42b4a1ed(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90dec1d582fe263db29e2098c0d504dc4719e1e774cf921be46a6aae10be3682(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4daf4c9079ddd8b6cc09b471877105517e3ffe3618c14410ca9de0af51b32ecb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ed389012cc8a371de3893ce7d58b6342a4dcada826b2a804489b35f60687cd(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedScopes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7e50f8a879e9599f98d363c66d873ba3ca93ca0f67e95d0320f7d3f30e1c824(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae511e79127b6a341fb4979d7ef5c7a34ab2b99d6a9bdd6e54903b6b200ce8b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__916bf0c7dfb6792b86853f8889349848a35e1c06554586e9a50d8c23c06af34b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bff4d9c4dd28156ca4561646dbe40d2124f7c7c865e4c42eb6a39e889c0603f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085a5ec73e13ed1f699d96869ed335a67b3f36a26da694d296dce4d6d16543ca(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbf3e83504c834bb5d9312f388879d213d5bb3f8e579f64d4c95005dbc530a41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d82a6c928beaadcaa34575c6b6cccb1345923f577f7648e62624b3fe94fa24a5(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAllowedTokenEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bf20db655c0a037881de1352368fad9da26cf5bac62ae650245bc0336d5f41f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef83ecc3420bea1b2725a52eb8759f9cbb3e237c3a9d07fc82bfc7d2cc3031c9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e3cf6b5bae15b17831db934620af333459a9d7a3fffee049a38b6050cecc5d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b49cf5fb3f3cca0652f5dd854bb85e57f5760513fcd81d166db64bb06852a6a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9dc816a66784ad8d9cabddb7ddb004233a896e14c0c070801bda36fe3c67b97(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d34f76353a940c9319bf66f37e25cb96fd42bffc78eeba78ee91d7b40f90cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90088cf567b15f9e3745f250cbdaa19b71860687c47d62da24e81fd154ab09ed(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthAuthorizationEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f1f65fdd093fb9970bccf2957d28469af05dab4e94daf56b21fbe4807267a46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79c20bb9dbeec7c05d65ec521f19597069ca9bedf64a1f725545dfcab90e497c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ca15c15c45f73af1aa487053bb63678f0031f93c3271ff7111542756aa295c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa5a22defa06c520d3d0e85f2a2cb832eadec2f90c4b0799cc1b747ea66b97f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__317a246821ddfe58a6d5be09dae63670431bf32fd0e41d2646172a2834256558(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__174993dab92c23ff565963fc48ecdb3d693e94111dd962724a587b6d1d2bfb60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d22e93b52ba1fb44e1d991731e95debc4482709cee1cac61455c26933e33eff(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientAuthMethod],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f12fce51a7cf4c9106ffe6a2b2b8c4af04e869e42b41be76fe1b792f81df01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d1fefb5e381e615808e92cb3b38c6dbf64b242f58faa37226c2c235f68032f0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73811b90729a02a8666dd7ca0e9827262bde644335196f46ec57ae468866b298(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f25a1c1dde3ffcea3aa45066cf9edd579794311310771b191257ba877718427(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3610519df400d1ab438caf986320ed3d4db3af593a7deb7bb3e4c390a5bdabb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee3ec00ad80bb3a30a9fa9ad6540af7da8779d6407b29e4eced029e642fe59b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d31d8dfe62d2a2291e9843acaeb819afde579c689053c3b4123957b917cd78eb(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c03a63a2a10841e993f30d3bbf7e135094f8ea7a8a26bd5b90e5d46226bf7d81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f53f0c23db75be56d37b9d4c5a02d28f12470cc886faf0b3673863e24256d2b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__202b19e8bf30bbe425e811178874b19256a4aacd321918a29f621f8023b240e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b73a4f67cfc08568f820959650a1bc1d7127ce9bbe20ab29c6ef0f5886d3cba8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b08fdfe1737af0f15c73049bc16e8720125c9a3dfa4e2da68b2715f4c021fb95(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1439c33001404706e0ad41d46119710a6fd59df14d9e316e9bedffaa631d3ec6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca7b5b3d0e136af2c4234d13627d090e3a8bd50425cc86afaa8ca48528c1efd5(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKey2Fp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e967f226cac296aebb032a26036bb2ec349ace7201600bd5e3b2979ff5c7da3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bea39ee5ba3a28c488173f6b8719f770c08634cd80356d76d75f3d6a1b425e66(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d223c359ae5eca8b435f8c37da081a3b60e99842787aa1c9d2d4ac57392a212(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7476e4d7fe0bf83f06966dda5bc366d150f301b62411d8eb1c16a58e8c2a2a6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e17044296319bfba8958dc77ecbd979d1cf72eb0634056bdba2fd45bd08810f5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50d95950b872b5ca70a6704542e11937bd2cf4020b4b1b766acb36657e6226c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__183031661998505a3e9e99925a2b9163185281219badc7175f3a77666c5fc9a8(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientRsaPublicKeyFp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2575c9bf13a0eaf001931b6a446166d8bb216fe8b0a7ab348adebe7d090eea71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d98bcc2703761309e2c1bcd46ba5318f999599edf0ce1d8e2c524ceed7eddf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a40fa59086a63e79d9ee3d1e5abab2691e3f30ea173696f80858a1e81ce8b55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7633c83dc9be901ee04a77da2073044f79994d0889bbd7e3ac3f3ae4a175bbff(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b7b9f26218bf804a80d27c3f900f40caffb3dfa87cac551d46b53725a91c90(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__005f6491ab36e300464e5c969dbb1853e8701aad98649aa367dabc9dc7b59ac8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d0e84cdc1795106f89dbdaa4ea903c409a29582e0e95308bbcbc8aeaa17029(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthClientType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8f422159369e6346e7e6d31688529e1b18094b48161e8429ce10aa2166028f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__966013a316b52b8b4cd65138e851c63cf12723cb487924b9f9514da2085cd397(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19442408338c2d3de03fb525ea5b1a7c3b56a5aa899e7a00c8cd38c2c5ee2987(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8bb3d37979edeccaf787f1d63ec4be495dad53957cfb6cda70ebb22d228bab5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd46b4ff1bae791fd4760bc3e1a0b81a975a9c9ce736946a24c3ff3a069e01f6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f891ec477eae35733cffb48689c6d1425d1b0cacaaf716c819d7f9d8f9cfbe96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c28693a4f67d6225c9631ee45aaf8a176e0cf836cd275dd2d9fbd8ffe31bc01(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthEnforcePkce],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ddd3601b6bc3cdc6d913ac1a585a684cc55c9023fb6a8eb69385cf2a10f41c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dc0c8624232292c21b868cbf7f9c21a6f73a2d1451efbc767ba88bb8cb162c0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e5f2f6e398b5e44a9251d4edbf1a338962545b86539202608539f5467b5b698(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44abaaf4fb219892e9d4c33fafa88914f5ad67745b9da4b4c100e0bce1d8d884(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b429da5b7f1964effe563176cc2f925aded0d96eb25fa1f58565c269ec494b0b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a0a10c538bac04f0a7b251398d456b291cc4a0aafd5887cbbaf0f57f096a8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac526e51076fcda0bd63a98042ce4a034b3cb7aac158ffa5b0d633009515548(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthGrant],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__048f3b27e0a42691eeb3632bed8af50d3bafeb7a9fe31eb9d306dd5ef2c97145(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5411d0c4e6c8445d0e92031d3ecf6ecbf14a56813b43c3d1961c4222de56dfe5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b1da7394f3b4558a1f4ebc005df5073977ed51825108dadd0524bbd79ce1a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6361a71d6e0e7603d1263df44aa5c029dbf9c507e5a8b033daa7bd758392fdc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45be1bf1c7db7feead17444100007ac7918d4df9954453d0eac2cff2258d8825(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e64a84b5306ad05aff6b6b0c44f6e480f1f4040dba6e0d91796d327f21ae207(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28004a4b7d5fb01a9e37ee23557d7878bc8eda69e806667dbad7b46eb3487dbe(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthIssueRefreshTokens],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c05f302a5bf715a811832020751c46ddbbe5d8e9fa361332709818ea22130e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aa3430d46cc910370a4f005f3b732e2e721e51266557a73dbf326751bd7b219(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e97582020444dbf8e38c1af6b4449a1a2677383745a2a4cf572b72448ad7b0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6535a976539c8e25138a77b27329a4b0cf8a861bb6ed82bdd5b8855ead380d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74d997055a501db82943116f43559ffd2122db62f8af18e565605e0e5c6494e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfb41d2a1b054a0ec9ee425dd602fc4017b34f399ac3c200e3580e2172fbbaff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af0a28f57c4b2255150cd894cdd31f81f46193563ced90922628ba5e90e4c11(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRedirectUri],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed631c4f20bac2ef080585b2dbb0cd2c5c4df0c8eb7d4feb14d2d1ef529d7a04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ad5c96ceca1a457a4f125adfd4929c7ed31c1b68a0852a49b21ca2d1cfde905(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc6aa6a516c9a13aad10d012b37d2efacc2dcdd30c69b4739755e9176e92cd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccbe0c977d74c9491176444aaa32658706c065754bc96649b2b9998f364ef68f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b051a0c40ef6954d5d93bab2c2ecb00edfcfee7d1ac3b406d938a65af633de44(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f733bbed1d7b9b25483f57a8de2459b69479fb28965ce53e67f29fb838ccb399(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32b6239e4e34af1eabdc00040daadd937a9bddb9c0af2b002713701a2b095af8(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthRefreshTokenValidity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc774b4b396ad980c6e51f1841df7b712bb7a7510b0eb39ccf5be58ca461756b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bddd3580d3b4cf3f67dcf8408f56040b8e82ff9b5f81bd943a7551a96462b3b6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b732a64726f314851f25555aed999cee7d284180a91649f16ea8e09f310edef3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3b6ff78fb1b32da72e1bc9d8c860c8e44dc49b28b304f36a9cc4a4f7a76462(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d9c91c3c882b4817c04429754c2592cd55ff8b438c33cefdbd5ac4d28c9052(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f5f77e51005e7b9531e9c6cbb9d3c08c0468114927343a807179ddb18764d5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42482b6405d91d01e5db6c2f81b3e4e32a1f5248d8d3a551a01c89e047036dae(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthTokenEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f3ef77690f76a24604ad48a04e14104f60bf3336bc92047cdd52279f48802e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__677fd444fc5250fbb50cc664c1b5fa5aa7d9e8de86b63358e457b21b1c975115(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb3ebdd8a528eb71d268592d67267ac6ae0faeb247e7418c7cfd1495fe1883a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c60bc3d394f52415e280485286e8c88ef117377a839423e4e68fb78aedcf457(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ef3dc955f994ba143fbbedfbc05f94bd68122c44a6edf457d322c06071f8cd5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__950f1b0832b8045533d684a24769e4ba06fb96a8f13cd187ff651b4b60bc807e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__346f715b60cd9c91b9b7dc69e3f8cd0c06c62be420a8faf8eb35a927b080d932(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputOauthUseSecondaryRoles],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26060cfdda4f55047dd6ab5a2f341e55b460c66b64612f765920aa5651c1543c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35df92f838e580f09ac05210cb6f9163d88f5577f80ec14671632f0b868b2ea5(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33777ccf4219c87d04a96f54d6dbebe88fd90d7fe068c872c5044fc619781ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975ac1c4b0343b14377e8ec59aff5280414cb13410da69a876a1594ec367248c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f465916f8dd108e2ea81ff9ed864653a8b0d8fa564df251f70484aa36ff69c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae3ab44c9c16af7a71ab6aceb13868c58b2b4889b35e1372b902b7bade3cae4d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8410b458c6d9393b9a250eec9b106a5efaa400d49c81a629b2fa71c6038e15d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1898c6e85441bc6fa6a10e13be9313c876acdfa660abe890dcd8e41c5c35b30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d6563b917e7903e5516217c4e0a8b3557897f3fb1d8a68b140266cb9f5a870(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputParentIntegration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b954fba4a0e840c0a0eb10c30aa7896267aa5afa21badb11d042ee87ac07296(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2739f047d3e870ec4c3d08f0f59cc8ceb55ed36692ba2ed59c7156be4df30e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1f07c700ce98a3f6db5567a4410a51a4ed8c65c4a2c5d8ce60ee6817ecbc00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59fef248f82800e23bb530f980a2730d5be7e570db8761408561d1aca2ab8d8c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f2d64994e921897c475f9e73e3180a071cae63855505f3a34468d57c8b1560(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__960e8ecca4b63b082f55c6995ba187e281f40d1cc7dee25eda386a2974de286e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42830aa2f2a4c2b7a760d43436da32f791167cf640aa8f5fe9dd22072a3004ad(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputPreAuthorizedRolesListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2fff7646f99f3e0b9fa5f79f6a4d83dc6ca092506210b063149d23fb6c96847(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4762f7eb94d6df3c46825ff15b289b9176de47c7fb5d1fe7c7d238a7db709ef8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e68f74a9ba8bbad493c5522f970b2ad0eacf216d04a77ef01e49130c9af117b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0493e2b421d96a7ede89b75c6395bb076a380839576069becc3285a0b03c6d31(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f0dd03ac99a48a89f6d685b14c220d9ace8917d2c670c791ddd6106b7b67978(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7471e591270bca74193da9dab5f14ff79d080e9df7cf515a5faf0398dbf61a87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__315343ef4438bc696454d3fc88f877ebe5c85a046d1d87627fe7e348604974a1(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputRunAsRole],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9d66a28cfc72e1498d59d2db3511fb3b5d550b8b9afa71cd15ca591c49d911c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b706b26f532a673ea37db8b119eea43a9e23496a009bf9b6c447167f4c845f9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f496841191ebbffe5a1b84b21190f99a1293a00819c140700881ca2fe6ba175a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24475066063d1c97cf958035baa3e89df97ae35f15f5cacebc12e2a76bed05bb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbadc4af83905789df2fe1e08127a0fa08ad187739d322cfce3564e99fa26d4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f262e0d040618c37a39a6e6feaaafb11e058c76c0b7f61fb9bfb4a76d5bde6ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66417e9e5e1e32ae0e7268c9c0ddfa130299b5a5e8ee62c4cfe1c71ce5a05115(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2DigestMethodsUsed],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__131a89f03f3d0d7ff0ba1b711eefc2b73541c3d9fe06dfe2a2356783abc62f13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4106e15b97a48a30e5c7c640ca20d1d7c29b76fb7a44b19975b2ddafd214407(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b743722784264b2dcdd23c3e67ea6a6d9199442812a9672cb7fb9126245339cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__730d3aed5fef44e73dc1bb436eb07580798287b5c26f8af7c0fc4bfe634f33bb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b52a8b598fbe548f6410813b5883c542c7791dcedf0bc892207291eb18e326(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8fde491e09810573a1dc37c3b2481548689a69379ecbf8001a41998f724b770(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ff7d59e51133990fca07ed13e0aa2fcbb009df783cfb365533f3588a2ece306(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2EnableSpInitiated],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1218f1249b5cd17926bbb0ef0fc9c86f7d58c9bb9be22afae5a6a9f3a5e2e171(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fcad2a51977ba658126b4c4040ff40859abad8c64f86c64e76cb97704abb433(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11b2b19fb0a0f77e681ecabb51f3bd05e34022f0b6922754ad4531e7ef364397(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67c6e774d0de9c22a86f857fc3c5bc64d83c34478447f7d5273e121a8781f59a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8660596d25929474303fb0758f8d0ddc16d7958af46201fa2fb63083e833af39(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eef7cec26f49e8d13271ee2be3c44aa2a8e5babdde80a8bc37060c7835a059da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a8794218588317b6b7da44749e0214d1dd5400579199ed7c9f39099c5957490(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2ForceAuthn],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03fed3e7f42ffcd6c0d466fbd28d5953bd33e9e688d6eced3b44eb254d756b75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03de32ff72161ecf676d7420dcbd3de3a7a9c642c078bc17a8f8351093103513(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d41415294db2d9b645aff5f02e3f087b5f0c8ae93601051432b44764d22bcc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb8b2ad65df9f1a1e1b84245150dbfd3f96d5cdc6773556017fbd2125199795(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43515213a454cba3ff50d913cf2f318a7ff241c2143bc5e28d58e53942f9c22b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cb5a1ea7eea835877258c9a0ad8de0018ee71cb18ff7bb3a177d97549aee89d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76966b25c112450c128100cb93c5f64c8197ed8d6649e32ca092cd8a51a92501(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2Issuer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32dc41bb25961d37e7803e6cb77af57a21a2cc93164706432b4086550b507f71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5febd750d3f5aa580d5c960d9a2c819448e9ffc8cc567c9f674911e000e678f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b08c1971fb179375e16faec0c736c40c93c89f1d1e6d9d3771d1ffd09c8fa7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b4b2424df497e2f8d75b57f716724b7e2af99a4d97d150351926f2a7973b496(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f82a60eb42401d482209c84dfe9bbfcaa5d1ff695a07d9a5348d993d77809cfc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2602beee8e5bd1a615e8d1adcc207f8b36c6ceeb787ede5d24d759482f214280(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d296b715107268b107ed9a47e5da334d838db76c7cbf9b3646e30814c3d4cd(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2PostLogoutRedirectUrl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e2508869664a1d18a246d4597023300a837ea0e3501a913876bb91658cb212(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8301097c10c08ab31e1cda9c24741e55dec9db4a23d342b90819dc9c7752c1bf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ee67fe5b4b690b4f3d3548e92f9d026f31cff38ab151a9c0e11196fcf33db7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fec2de299c4aa9ff940f62e8a771d15a4a0b6287766e0ac947efcd3992c6e4a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea8f00eb28b9343bf2dcbf1bcc585590ecd764459ac10684b7d2e84ce5845f1d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b1d0f0194a4992e9c020bff4199d418f963f017426cd48e33fc3d7b7cbc331(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6645314bbcac5e99318cd279d0867d636eade3d8f7a1ffeec7e090d15f41c908(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2Provider],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f87dd8fe7fc7b9d689ffd968d2ac900316ecacf76e3813242825d36049bd7c69(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19984ab0c12cff67762e19092f428f14d294f14cf257d0a903893044e13ff47(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73d520d0afe242d1015c1609e61c1049bf973c4228e753a2b89f300e7c951c9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea99a6cd8358ae5308d1abc32ef05bc1b69389c038ed7a78796a356289a23c9e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e716ab31c1a97db89232f85c969599118c82baceeb7ce692346e83499ed2977f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56e86200f03379944eedd219401c384de3ecd199b2f4bf8f61e5902318353776(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9382af949fb12e6861c1efb06ef5f225f681243da10a57c037be426d63169086(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2RequestedNameidFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c439feed55c84eae06b1fad268910e1a08bbe26dd515a50eeee3962621dbb8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ac6705a66846a4aafa612a810356c11c07e34f8811335e9951fa00d3bd5cb75(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d1b5d3d8798bfe47df60349548c905145b2154cca462a34720c05fa3c9c3ed5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8737789d637d70c57caef38b29815d4068fbe639951658922205364b961e7e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1fd00d577447dc21aae45b9891c74aaba5f3fad6a0d9b436d6c3092c4bd516(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2c01b174ae9783f3290628fd81ee3786686bc8f2e2e20935a7f30aace667ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e037a79bbfaaf9b798ce7f1f2efdd0129096be24a178d285bbd33b9745a52c15(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3819a5a681297953653e2c4d5d033ceddaef593ebac8fd36a99f5435ec5bc9ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__840c0b399a3fd4629c8e2e7015d6556738e1f3063a4e91dfc4f1b8a5583e9943(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c541111629bae41ffe8375b7f7d3800b3575871459289f0529f6127b169651(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dae65bc1ac8615d3ac2fe533f73e43584833ba9b4c8e9cf593102511b907161(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fbeb342819849e4ce228c57ef8135fc6af63e5e37c40d8ad023dc15b62ffac7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee44307b5da4341d0b2c4692880c9fb0de9d9d5def78ea95c1e34ca78cdca18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fde0e67ca89de6d58b9cb2186ff7d11ab7ddcf138a78a2271b659023c324763(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SignatureMethodsUsed],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac8dfbb20bdb688b236e1375ab1d68ee422275bfef5de317da755332f265e709(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de70e91fd54c2b479a74d800531f87015422e79227a27ee9219534ea9dbfca69(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd523b791e21be38b98013c09c5d4541010884f0a970518b341b30c3015e93e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c20a03c0e3ad1e47967b495dbf59a9c947062cae6e822ac159b72f02355dd142(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8449a0b965963ed122b9e50ae01460afb208aa0ea334924b154db5e9538c57b1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dafa31af1572a9577200cc078c3188f12bba7fcf8a83cfab87be0d917d933f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__582122220e214c25033b524e061d2e2e9f2d6b1040e539ec2cef2db175feaa93(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeAcsUrl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb719effa6ef2e9ff6955b146e45336037c84af6e424a5500a94bed79b923f21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50f24780080eaf69f439ee13eeee6459626fed0085952d9c9996ce4ec5567e98(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6faa70e1f8297f6793e8edaa4dbda0a06b2572e771d32a11ca6413cc0a4ff66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed3de7bf88b8bbd82074b2ad27b400658389c4f4654fdacfee9a85573dd40a7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e297d48f420be921788e144174135ad8a7d2021f49c6656307fde5e544c79cd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16176f174f6ed2cae5a926b1fb1dd0bfb3760997ca7356ca4acef5a19411d249(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ced74f110a0bcfeee3970ac644eceac67c6da0d43de806fee9a325cbc1fbd20(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeIssuerUrl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a770b752265f2f30b27b0d57c041534b3eb12076a349252f4e14e381265c973a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1eae83fb9ebcb80f4f196e3ad145410a7192c30e9961131933a67debf7ad2e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c8ded4a27a8c828552a32231559e049df5e268b8ffeaa981d39e05440d745c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10d649f356e4c0b943cd2eaab6a0aac9c6e2a71351ecbfa81916b601f44aef39(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__728265e06319c864d3c48415568375528b43bc2de1ae9ebf24a19db9f82ef31c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6db52b5f820783f5438f2021e517789ed340d456f2379b03c0214c0dbbf1b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae9c0a69de8a3ec961c29d91bb2e5e6434429c4f5d10acc82d64e41cbe95dac(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeMetadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ddcefbb92b596023983d290084a5db087c6448e5cb51e20b3eea50332e53436(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832e0902a97e4b41b5e8cf2938e5617b6dee4fca896749b4ae0c3a19120c2b5d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f8c2267f47071e15c9684d1c3c30f389371ca050cf2936e63a81f93c5f99ed6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__988b5830f7f2847c0fee536247dace27bf58dbe115ce5116cc370a79aaa3bb40(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8f619913fa64ad3a21c588c458255ad962f689cd7d892cc028b6b9568da54d4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba068687c33f92d0fe10fe147609402766082214d602c533ff6ded6737c28cec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceeac051f6dcb513ee276402abf75a4784e67d4c44b141fccf72e9845ee76b47(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SnowflakeX509Cert],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b253674b4465e8baf7e14195e2dd9b4ad3294cbb9e7dde9102256060d5bc161(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151f1d6b5671a66719c039caac1ff66882b394c0d8db801544614a8d9a27c753(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eef44db681d7da38c1affdfa9916dd78a8de2f444915c28132bca55b1084ed8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af9ed88d8501906ccbc3c97b77832cd0f06ddfa13938fb56c24c775652c3e75(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b44d5374cb8201870e2ac19c8646d8fbd6b20b831506fc577526f4bbcd471886(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd7dfa060d8c6a8207dfaba73a46776dd716436ed923aebfe8deb82e36367ce1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a5c1e790e7ef5715b105df55c751a5553609c2acbeafbca0633fb3c68f1be52(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SpInitiatedLoginPageLabel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a07bf3bc9faf96ede63fd6b1304015ec16b305aec66439cf9888e95e0859d3f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66710f44c82949b7a92ecb60c141f86a53733d41a9994cca6230235b1cc47a0c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3f9b8d7ff926a4add28f987bef2507b7159cf37dc41305f03a634661ccfa77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f6eb0be6fd551125c793a2e1a6ff3bf60d2104fa3edef721ae79f8d7028417(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce95a1efdc18f28bb6140afe51e9c62bc3c31aa0345c7170d2f43403fb39bb8e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d9b9841409241904a18df80a62b164423082dd6227362218f30c87a224dbd51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b077da7f57ffbbbc4dfa38604920cc54aeb3bea9ddbbf0616aec9d3581891f05(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2SsoUrl],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af34415d23a25998b282fc9105aa1105576a027c31c4759b400173dc63aae1d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9debd1bca042e2016d32d695ccd708bdbc68c20b9d08db41cbb2cbcf3aefa9a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ea63e4800d2a628ea29cf0f751ca408ae0e92d06ffcadf2f41c0fd149142053(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57903864dc26947121f031673e7e96c4cda8a459e886672824a1ff62a70bdb80(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5163c3ec5afd80007fb1bb46457f2c11df4f139948ad734949c5e442936b6d4e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f078369bc92357f27c5f1755b8c07b4e123271bf637c88cd6f4830834c83aa8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41860a6ff51a6ae3a9a9935f456d91ce3bfc55321291297649a067cd96d82424(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSaml2X509Cert],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d8fb17fdc0869e1801ee1656265259b6839910ff95e83acc875557d039957ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e79687a8c802e60d3ce539453647dcf63a5bebed404b3f5c279fef63e1d44185(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__219d30177d52c15e224e6402aafec1f012a13af736649d187cc68a75e771e7cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a4fbadfb7e69d18f8657d53e3e4939365d06392e39254ba15b9e7f05b3c4ae(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__534a13f8ce2d14294f2fd48a3ec12c4e45aef83df5ce79c794a69e100cce1c5b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c17f08dd1bbc44322e0309608cd0c72e2b60b5062c51d20f24c33746070f92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6d326c2db0712e0e5e2d35885f790fc656fada23fbb39c7a43ae6f04ff8dcd2(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsDescribeOutputSyncPassword],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e0634fff0f9522b9839ef4a9f1b6e62631572cac33032c446b5d522ad73b865(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6fec854948de45f3b7e7897535080c7c55c028b7e30d1e59350acf17c05884f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__019dab347823cfd346ae86d7f216d403897cf11fc6374c5800cc1478b8073b48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__897abf88e7968672294e0a1b6752ba5ae24b6be689125b357418a82e1e6acfe1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42343faa60762a19e0452367fb1cff5752f5ea04b93859a29cc5a6f0cb91da5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f805d8f1d47b5364db1f8011235ad22f1d1664f90769ad646091e5e2c3142f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35075a23952eba2424c02655327d41da0dfc276786f0443afb62b131caab90b5(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34c07eb81b34ceb3a57ef1534716bc8155e6159496aa3984606d8d68b9e7477e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b51b3f19ed95bf18aaec23f83c2e015ebc426641778be9a805860c528820129c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe48da15354345342a6ff36e5c9cfa9f78aa9a250e9129a0205da2b3cd8399e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da6aa6bc0ce85beb8be8c70b3954b55fd36b1fdf70915e123c8f3915b2c18ca0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ebaf3900a4bfcca2f721b1ac6b9482ba2cbb0f9fcc28c7d244b6494dcfc304a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a6e0938ba9360e510093171593a21e595286a76b617903ac18b3c0b2b677742(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0346ac2ba2accd051e9a6ed2db8d28ee53bdc633adbb7b9fb1910a0b1588e628(
    value: typing.Optional[DataSnowflakeSecurityIntegrationsSecurityIntegrationsShowOutput],
) -> None:
    """Type checking stubs"""
    pass
