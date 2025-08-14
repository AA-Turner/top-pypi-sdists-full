r'''
# `datadog_agentless_scanning_aws_scan_options`

Refer to the Terraform Registry for docs: [`datadog_agentless_scanning_aws_scan_options`](https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/agentless_scanning_aws_scan_options).
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


class AgentlessScanningAwsScanOptions(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.agentlessScanningAwsScanOptions.AgentlessScanningAwsScanOptions",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/agentless_scanning_aws_scan_options datadog_agentless_scanning_aws_scan_options}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        aws_account_id: builtins.str,
        lambda_: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        sensitive_data: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        vuln_containers_os: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        vuln_host_os: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/agentless_scanning_aws_scan_options datadog_agentless_scanning_aws_scan_options} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param aws_account_id: The AWS Account ID for which agentless scanning is configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/agentless_scanning_aws_scan_options#aws_account_id AgentlessScanningAwsScanOptions#aws_account_id}
        :param lambda_: Indicates if scanning of Lambda functions is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/agentless_scanning_aws_scan_options#lambda AgentlessScanningAwsScanOptions#lambda}
        :param sensitive_data: Indicates if scanning for sensitive data is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/agentless_scanning_aws_scan_options#sensitive_data AgentlessScanningAwsScanOptions#sensitive_data}
        :param vuln_containers_os: Indicates if scanning for vulnerabilities in containers is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/agentless_scanning_aws_scan_options#vuln_containers_os AgentlessScanningAwsScanOptions#vuln_containers_os}
        :param vuln_host_os: Indicates if scanning for vulnerabilities in hosts is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/agentless_scanning_aws_scan_options#vuln_host_os AgentlessScanningAwsScanOptions#vuln_host_os}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c0c27c499b86e09b78d84793cbba0b00dde29733cb496ecf7dfba98e14e29d4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = AgentlessScanningAwsScanOptionsConfig(
            aws_account_id=aws_account_id,
            lambda_=lambda_,
            sensitive_data=sensitive_data,
            vuln_containers_os=vuln_containers_os,
            vuln_host_os=vuln_host_os,
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
        '''Generates CDKTF code for importing a AgentlessScanningAwsScanOptions resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AgentlessScanningAwsScanOptions to import.
        :param import_from_id: The id of the existing AgentlessScanningAwsScanOptions that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/agentless_scanning_aws_scan_options#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AgentlessScanningAwsScanOptions to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceb3ea7689e48a5ce55a413d54c5896359cc137402d6fd2f879346c925149180)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountIdInput")
    def aws_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaInput")
    def lambda_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "lambdaInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitiveDataInput")
    def sensitive_data_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sensitiveDataInput"))

    @builtins.property
    @jsii.member(jsii_name="vulnContainersOsInput")
    def vuln_containers_os_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "vulnContainersOsInput"))

    @builtins.property
    @jsii.member(jsii_name="vulnHostOsInput")
    def vuln_host_os_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "vulnHostOsInput"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsAccountId"))

    @aws_account_id.setter
    def aws_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ac9c76cbd745e838847656a5963c2db6bb635a2d3244ea03cd20a0dbf7a6f82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "lambda"))

    @lambda_.setter
    def lambda_(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63cfdb2897f26b37f3a1b2af57614de4a9ca387a2311e946a2b46e1e9f0feb5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambda", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sensitiveData")
    def sensitive_data(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sensitiveData"))

    @sensitive_data.setter
    def sensitive_data(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87a5a98346fefa9660e8c017092ccf243d3650352bfde3e797a4e6f8ea51dd30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sensitiveData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vulnContainersOs")
    def vuln_containers_os(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "vulnContainersOs"))

    @vuln_containers_os.setter
    def vuln_containers_os(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0917f92ff1210f27c63a48bd19ebb9cc18f77cc9a8b7e9903f868922d765d5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vulnContainersOs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vulnHostOs")
    def vuln_host_os(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "vulnHostOs"))

    @vuln_host_os.setter
    def vuln_host_os(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce1278c2d65e12dbece6202a980fd9632c5629f450bcceb3a67f0bbd04c8211a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vulnHostOs", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.agentlessScanningAwsScanOptions.AgentlessScanningAwsScanOptionsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "aws_account_id": "awsAccountId",
        "lambda_": "lambda",
        "sensitive_data": "sensitiveData",
        "vuln_containers_os": "vulnContainersOs",
        "vuln_host_os": "vulnHostOs",
    },
)
class AgentlessScanningAwsScanOptionsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        aws_account_id: builtins.str,
        lambda_: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        sensitive_data: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        vuln_containers_os: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        vuln_host_os: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param aws_account_id: The AWS Account ID for which agentless scanning is configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/agentless_scanning_aws_scan_options#aws_account_id AgentlessScanningAwsScanOptions#aws_account_id}
        :param lambda_: Indicates if scanning of Lambda functions is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/agentless_scanning_aws_scan_options#lambda AgentlessScanningAwsScanOptions#lambda}
        :param sensitive_data: Indicates if scanning for sensitive data is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/agentless_scanning_aws_scan_options#sensitive_data AgentlessScanningAwsScanOptions#sensitive_data}
        :param vuln_containers_os: Indicates if scanning for vulnerabilities in containers is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/agentless_scanning_aws_scan_options#vuln_containers_os AgentlessScanningAwsScanOptions#vuln_containers_os}
        :param vuln_host_os: Indicates if scanning for vulnerabilities in hosts is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/agentless_scanning_aws_scan_options#vuln_host_os AgentlessScanningAwsScanOptions#vuln_host_os}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67324059635ce9bf6eb88bca856cb1bdc4b5d6c523c50b018fe6a629f2edfd2c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
            check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
            check_type(argname="argument sensitive_data", value=sensitive_data, expected_type=type_hints["sensitive_data"])
            check_type(argname="argument vuln_containers_os", value=vuln_containers_os, expected_type=type_hints["vuln_containers_os"])
            check_type(argname="argument vuln_host_os", value=vuln_host_os, expected_type=type_hints["vuln_host_os"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_account_id": aws_account_id,
            "lambda_": lambda_,
            "sensitive_data": sensitive_data,
            "vuln_containers_os": vuln_containers_os,
            "vuln_host_os": vuln_host_os,
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
    def aws_account_id(self) -> builtins.str:
        '''The AWS Account ID for which agentless scanning is configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/agentless_scanning_aws_scan_options#aws_account_id AgentlessScanningAwsScanOptions#aws_account_id}
        '''
        result = self._values.get("aws_account_id")
        assert result is not None, "Required property 'aws_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lambda_(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Indicates if scanning of Lambda functions is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/agentless_scanning_aws_scan_options#lambda AgentlessScanningAwsScanOptions#lambda}
        '''
        result = self._values.get("lambda_")
        assert result is not None, "Required property 'lambda_' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def sensitive_data(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Indicates if scanning for sensitive data is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/agentless_scanning_aws_scan_options#sensitive_data AgentlessScanningAwsScanOptions#sensitive_data}
        '''
        result = self._values.get("sensitive_data")
        assert result is not None, "Required property 'sensitive_data' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def vuln_containers_os(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Indicates if scanning for vulnerabilities in containers is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/agentless_scanning_aws_scan_options#vuln_containers_os AgentlessScanningAwsScanOptions#vuln_containers_os}
        '''
        result = self._values.get("vuln_containers_os")
        assert result is not None, "Required property 'vuln_containers_os' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def vuln_host_os(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Indicates if scanning for vulnerabilities in hosts is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/agentless_scanning_aws_scan_options#vuln_host_os AgentlessScanningAwsScanOptions#vuln_host_os}
        '''
        result = self._values.get("vuln_host_os")
        assert result is not None, "Required property 'vuln_host_os' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentlessScanningAwsScanOptionsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AgentlessScanningAwsScanOptions",
    "AgentlessScanningAwsScanOptionsConfig",
]

publication.publish()

def _typecheckingstub__5c0c27c499b86e09b78d84793cbba0b00dde29733cb496ecf7dfba98e14e29d4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    aws_account_id: builtins.str,
    lambda_: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    sensitive_data: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    vuln_containers_os: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    vuln_host_os: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
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

def _typecheckingstub__ceb3ea7689e48a5ce55a413d54c5896359cc137402d6fd2f879346c925149180(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ac9c76cbd745e838847656a5963c2db6bb635a2d3244ea03cd20a0dbf7a6f82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63cfdb2897f26b37f3a1b2af57614de4a9ca387a2311e946a2b46e1e9f0feb5c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a5a98346fefa9660e8c017092ccf243d3650352bfde3e797a4e6f8ea51dd30(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0917f92ff1210f27c63a48bd19ebb9cc18f77cc9a8b7e9903f868922d765d5b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce1278c2d65e12dbece6202a980fd9632c5629f450bcceb3a67f0bbd04c8211a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67324059635ce9bf6eb88bca856cb1bdc4b5d6c523c50b018fe6a629f2edfd2c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    aws_account_id: builtins.str,
    lambda_: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    sensitive_data: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    vuln_containers_os: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    vuln_host_os: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass
