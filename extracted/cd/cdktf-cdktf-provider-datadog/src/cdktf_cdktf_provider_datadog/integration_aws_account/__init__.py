r'''
# `datadog_integration_aws_account`

Refer to the Terraform Registry for docs: [`datadog_integration_aws_account`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account).
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


class IntegrationAwsAccount(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccount",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account datadog_integration_aws_account}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        aws_account_id: builtins.str,
        aws_partition: builtins.str,
        account_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        auth_config: typing.Optional[typing.Union["IntegrationAwsAccountAuthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_regions: typing.Optional[typing.Union["IntegrationAwsAccountAwsRegions", typing.Dict[builtins.str, typing.Any]]] = None,
        logs_config: typing.Optional[typing.Union["IntegrationAwsAccountLogsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        metrics_config: typing.Optional[typing.Union["IntegrationAwsAccountMetricsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        resources_config: typing.Optional[typing.Union["IntegrationAwsAccountResourcesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        traces_config: typing.Optional[typing.Union["IntegrationAwsAccountTracesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account datadog_integration_aws_account} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param aws_account_id: Your AWS Account ID without dashes. Invalid aws_account_id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#aws_account_id IntegrationAwsAccount#aws_account_id}
        :param aws_partition: AWS Account partition. Valid values are ``aws``, ``aws-cn``, ``aws-us-gov``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#aws_partition IntegrationAwsAccount#aws_partition}
        :param account_tags: Tags to apply to all metrics in the account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#account_tags IntegrationAwsAccount#account_tags}
        :param auth_config: auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#auth_config IntegrationAwsAccount#auth_config}
        :param aws_regions: aws_regions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#aws_regions IntegrationAwsAccount#aws_regions}
        :param logs_config: logs_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#logs_config IntegrationAwsAccount#logs_config}
        :param metrics_config: metrics_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#metrics_config IntegrationAwsAccount#metrics_config}
        :param resources_config: resources_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#resources_config IntegrationAwsAccount#resources_config}
        :param traces_config: traces_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#traces_config IntegrationAwsAccount#traces_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcd63bc0d287e84fdf49342387a0d0779d4e91bae2231475b2431639338c336b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = IntegrationAwsAccountConfig(
            aws_account_id=aws_account_id,
            aws_partition=aws_partition,
            account_tags=account_tags,
            auth_config=auth_config,
            aws_regions=aws_regions,
            logs_config=logs_config,
            metrics_config=metrics_config,
            resources_config=resources_config,
            traces_config=traces_config,
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
        '''Generates CDKTF code for importing a IntegrationAwsAccount resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IntegrationAwsAccount to import.
        :param import_from_id: The id of the existing IntegrationAwsAccount that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IntegrationAwsAccount to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5e8bdfd6ea50b7317165530d43a3bc038672e5c67ca891ca7581f6c4903aabf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAuthConfig")
    def put_auth_config(
        self,
        *,
        aws_auth_config_keys: typing.Optional[typing.Union["IntegrationAwsAccountAuthConfigAwsAuthConfigKeys", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_auth_config_role: typing.Optional[typing.Union["IntegrationAwsAccountAuthConfigAwsAuthConfigRole", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws_auth_config_keys: aws_auth_config_keys block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#aws_auth_config_keys IntegrationAwsAccount#aws_auth_config_keys}
        :param aws_auth_config_role: aws_auth_config_role block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#aws_auth_config_role IntegrationAwsAccount#aws_auth_config_role}
        '''
        value = IntegrationAwsAccountAuthConfig(
            aws_auth_config_keys=aws_auth_config_keys,
            aws_auth_config_role=aws_auth_config_role,
        )

        return typing.cast(None, jsii.invoke(self, "putAuthConfig", [value]))

    @jsii.member(jsii_name="putAwsRegions")
    def put_aws_regions(
        self,
        *,
        include_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_only: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param include_all: Include all regions. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#include_all IntegrationAwsAccount#include_all}
        :param include_only: Include only these regions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#include_only IntegrationAwsAccount#include_only}
        '''
        value = IntegrationAwsAccountAwsRegions(
            include_all=include_all, include_only=include_only
        )

        return typing.cast(None, jsii.invoke(self, "putAwsRegions", [value]))

    @jsii.member(jsii_name="putLogsConfig")
    def put_logs_config(
        self,
        *,
        lambda_forwarder: typing.Optional[typing.Union["IntegrationAwsAccountLogsConfigLambdaForwarder", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param lambda_forwarder: lambda_forwarder block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#lambda_forwarder IntegrationAwsAccount#lambda_forwarder}
        '''
        value = IntegrationAwsAccountLogsConfig(lambda_forwarder=lambda_forwarder)

        return typing.cast(None, jsii.invoke(self, "putLogsConfig", [value]))

    @jsii.member(jsii_name="putMetricsConfig")
    def put_metrics_config(
        self,
        *,
        automute_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        collect_cloudwatch_alarms: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        collect_custom_metrics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        namespace_filters: typing.Optional[typing.Union["IntegrationAwsAccountMetricsConfigNamespaceFilters", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationAwsAccountMetricsConfigTagFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param automute_enabled: Enable EC2 automute for AWS metrics Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#automute_enabled IntegrationAwsAccount#automute_enabled}
        :param collect_cloudwatch_alarms: Enable CloudWatch alarms collection Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#collect_cloudwatch_alarms IntegrationAwsAccount#collect_cloudwatch_alarms}
        :param collect_custom_metrics: Enable custom metrics collection Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#collect_custom_metrics IntegrationAwsAccount#collect_custom_metrics}
        :param enabled: Enable AWS metrics collection Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#enabled IntegrationAwsAccount#enabled}
        :param namespace_filters: namespace_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#namespace_filters IntegrationAwsAccount#namespace_filters}
        :param tag_filters: tag_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#tag_filters IntegrationAwsAccount#tag_filters}
        '''
        value = IntegrationAwsAccountMetricsConfig(
            automute_enabled=automute_enabled,
            collect_cloudwatch_alarms=collect_cloudwatch_alarms,
            collect_custom_metrics=collect_custom_metrics,
            enabled=enabled,
            namespace_filters=namespace_filters,
            tag_filters=tag_filters,
        )

        return typing.cast(None, jsii.invoke(self, "putMetricsConfig", [value]))

    @jsii.member(jsii_name="putResourcesConfig")
    def put_resources_config(
        self,
        *,
        cloud_security_posture_management_collection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        extended_collection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cloud_security_posture_management_collection: Enable Cloud Security Management to scan AWS resources for vulnerabilities, misconfigurations, identity risks, and compliance violations. Requires ``extended_collection`` to be set to ``true``. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#cloud_security_posture_management_collection IntegrationAwsAccount#cloud_security_posture_management_collection}
        :param extended_collection: Whether Datadog collects additional attributes and configuration information about the resources in your AWS account. Required for ``cloud_security_posture_management_collection``. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#extended_collection IntegrationAwsAccount#extended_collection}
        '''
        value = IntegrationAwsAccountResourcesConfig(
            cloud_security_posture_management_collection=cloud_security_posture_management_collection,
            extended_collection=extended_collection,
        )

        return typing.cast(None, jsii.invoke(self, "putResourcesConfig", [value]))

    @jsii.member(jsii_name="putTracesConfig")
    def put_traces_config(
        self,
        *,
        xray_services: typing.Optional[typing.Union["IntegrationAwsAccountTracesConfigXrayServices", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param xray_services: xray_services block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#xray_services IntegrationAwsAccount#xray_services}
        '''
        value = IntegrationAwsAccountTracesConfig(xray_services=xray_services)

        return typing.cast(None, jsii.invoke(self, "putTracesConfig", [value]))

    @jsii.member(jsii_name="resetAccountTags")
    def reset_account_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountTags", []))

    @jsii.member(jsii_name="resetAuthConfig")
    def reset_auth_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthConfig", []))

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetLogsConfig")
    def reset_logs_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogsConfig", []))

    @jsii.member(jsii_name="resetMetricsConfig")
    def reset_metrics_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsConfig", []))

    @jsii.member(jsii_name="resetResourcesConfig")
    def reset_resources_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourcesConfig", []))

    @jsii.member(jsii_name="resetTracesConfig")
    def reset_traces_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTracesConfig", []))

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
    @jsii.member(jsii_name="authConfig")
    def auth_config(self) -> "IntegrationAwsAccountAuthConfigOutputReference":
        return typing.cast("IntegrationAwsAccountAuthConfigOutputReference", jsii.get(self, "authConfig"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> "IntegrationAwsAccountAwsRegionsOutputReference":
        return typing.cast("IntegrationAwsAccountAwsRegionsOutputReference", jsii.get(self, "awsRegions"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="logsConfig")
    def logs_config(self) -> "IntegrationAwsAccountLogsConfigOutputReference":
        return typing.cast("IntegrationAwsAccountLogsConfigOutputReference", jsii.get(self, "logsConfig"))

    @builtins.property
    @jsii.member(jsii_name="metricsConfig")
    def metrics_config(self) -> "IntegrationAwsAccountMetricsConfigOutputReference":
        return typing.cast("IntegrationAwsAccountMetricsConfigOutputReference", jsii.get(self, "metricsConfig"))

    @builtins.property
    @jsii.member(jsii_name="resourcesConfig")
    def resources_config(self) -> "IntegrationAwsAccountResourcesConfigOutputReference":
        return typing.cast("IntegrationAwsAccountResourcesConfigOutputReference", jsii.get(self, "resourcesConfig"))

    @builtins.property
    @jsii.member(jsii_name="tracesConfig")
    def traces_config(self) -> "IntegrationAwsAccountTracesConfigOutputReference":
        return typing.cast("IntegrationAwsAccountTracesConfigOutputReference", jsii.get(self, "tracesConfig"))

    @builtins.property
    @jsii.member(jsii_name="accountTagsInput")
    def account_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accountTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="authConfigInput")
    def auth_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IntegrationAwsAccountAuthConfig"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IntegrationAwsAccountAuthConfig"]], jsii.get(self, "authConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountIdInput")
    def aws_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="awsPartitionInput")
    def aws_partition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsPartitionInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IntegrationAwsAccountAwsRegions"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IntegrationAwsAccountAwsRegions"]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="logsConfigInput")
    def logs_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IntegrationAwsAccountLogsConfig"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IntegrationAwsAccountLogsConfig"]], jsii.get(self, "logsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsConfigInput")
    def metrics_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IntegrationAwsAccountMetricsConfig"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IntegrationAwsAccountMetricsConfig"]], jsii.get(self, "metricsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesConfigInput")
    def resources_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IntegrationAwsAccountResourcesConfig"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IntegrationAwsAccountResourcesConfig"]], jsii.get(self, "resourcesConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="tracesConfigInput")
    def traces_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IntegrationAwsAccountTracesConfig"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IntegrationAwsAccountTracesConfig"]], jsii.get(self, "tracesConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="accountTags")
    def account_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accountTags"))

    @account_tags.setter
    def account_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef9f7982a5101f71f9bdaf9cc100c53d94234abc324495e573035cb39d8a31c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsAccountId"))

    @aws_account_id.setter
    def aws_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d81516a536e9b3b59e713dee845b0765aac48a879e943786fc729f5e4072eba7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="awsPartition")
    def aws_partition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsPartition"))

    @aws_partition.setter
    def aws_partition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7066b0a08aa786814c118bce1ebe8daa0218cefe9ea4ef1ff407f8606fb1f55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsPartition", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountAuthConfig",
    jsii_struct_bases=[],
    name_mapping={
        "aws_auth_config_keys": "awsAuthConfigKeys",
        "aws_auth_config_role": "awsAuthConfigRole",
    },
)
class IntegrationAwsAccountAuthConfig:
    def __init__(
        self,
        *,
        aws_auth_config_keys: typing.Optional[typing.Union["IntegrationAwsAccountAuthConfigAwsAuthConfigKeys", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_auth_config_role: typing.Optional[typing.Union["IntegrationAwsAccountAuthConfigAwsAuthConfigRole", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws_auth_config_keys: aws_auth_config_keys block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#aws_auth_config_keys IntegrationAwsAccount#aws_auth_config_keys}
        :param aws_auth_config_role: aws_auth_config_role block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#aws_auth_config_role IntegrationAwsAccount#aws_auth_config_role}
        '''
        if isinstance(aws_auth_config_keys, dict):
            aws_auth_config_keys = IntegrationAwsAccountAuthConfigAwsAuthConfigKeys(**aws_auth_config_keys)
        if isinstance(aws_auth_config_role, dict):
            aws_auth_config_role = IntegrationAwsAccountAuthConfigAwsAuthConfigRole(**aws_auth_config_role)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8854dc09dbc7970de1b7ba0d5434e7e175bd663d7605291a5d3640c098ac1cf3)
            check_type(argname="argument aws_auth_config_keys", value=aws_auth_config_keys, expected_type=type_hints["aws_auth_config_keys"])
            check_type(argname="argument aws_auth_config_role", value=aws_auth_config_role, expected_type=type_hints["aws_auth_config_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_auth_config_keys is not None:
            self._values["aws_auth_config_keys"] = aws_auth_config_keys
        if aws_auth_config_role is not None:
            self._values["aws_auth_config_role"] = aws_auth_config_role

    @builtins.property
    def aws_auth_config_keys(
        self,
    ) -> typing.Optional["IntegrationAwsAccountAuthConfigAwsAuthConfigKeys"]:
        '''aws_auth_config_keys block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#aws_auth_config_keys IntegrationAwsAccount#aws_auth_config_keys}
        '''
        result = self._values.get("aws_auth_config_keys")
        return typing.cast(typing.Optional["IntegrationAwsAccountAuthConfigAwsAuthConfigKeys"], result)

    @builtins.property
    def aws_auth_config_role(
        self,
    ) -> typing.Optional["IntegrationAwsAccountAuthConfigAwsAuthConfigRole"]:
        '''aws_auth_config_role block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#aws_auth_config_role IntegrationAwsAccount#aws_auth_config_role}
        '''
        result = self._values.get("aws_auth_config_role")
        return typing.cast(typing.Optional["IntegrationAwsAccountAuthConfigAwsAuthConfigRole"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationAwsAccountAuthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountAuthConfigAwsAuthConfigKeys",
    jsii_struct_bases=[],
    name_mapping={
        "access_key_id": "accessKeyId",
        "secret_access_key": "secretAccessKey",
    },
)
class IntegrationAwsAccountAuthConfigAwsAuthConfigKeys:
    def __init__(
        self,
        *,
        access_key_id: typing.Optional[builtins.str] = None,
        secret_access_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_key_id: AWS Access Key ID. Invalid access_key_id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#access_key_id IntegrationAwsAccount#access_key_id}
        :param secret_access_key: AWS Secret Access Key. This value is write-only; changes made outside of Terraform will not be drift-detected. Secret_access_key must be non-empty and not contain whitespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#secret_access_key IntegrationAwsAccount#secret_access_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc06718dc917d2bf3477581cfc9c69a929e4df5b4a9cfcd4435a87f45269d801)
            check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
            check_type(argname="argument secret_access_key", value=secret_access_key, expected_type=type_hints["secret_access_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_key_id is not None:
            self._values["access_key_id"] = access_key_id
        if secret_access_key is not None:
            self._values["secret_access_key"] = secret_access_key

    @builtins.property
    def access_key_id(self) -> typing.Optional[builtins.str]:
        '''AWS Access Key ID. Invalid access_key_id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#access_key_id IntegrationAwsAccount#access_key_id}
        '''
        result = self._values.get("access_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_access_key(self) -> typing.Optional[builtins.str]:
        '''AWS Secret Access Key.

        This value is write-only; changes made outside of Terraform will not be drift-detected. Secret_access_key must be non-empty and not contain whitespace.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#secret_access_key IntegrationAwsAccount#secret_access_key}
        '''
        result = self._values.get("secret_access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationAwsAccountAuthConfigAwsAuthConfigKeys(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationAwsAccountAuthConfigAwsAuthConfigKeysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountAuthConfigAwsAuthConfigKeysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69c4a96896e63648e1dbd2126dcf371fea65dba902c0c2c53aab4d24b0001050)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccessKeyId")
    def reset_access_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessKeyId", []))

    @jsii.member(jsii_name="resetSecretAccessKey")
    def reset_secret_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretAccessKey", []))

    @builtins.property
    @jsii.member(jsii_name="accessKeyIdInput")
    def access_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="secretAccessKeyInput")
    def secret_access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKeyId")
    def access_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessKeyId"))

    @access_key_id.setter
    def access_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c9a2610afa7168a8da2124acd0324476d5ac9fa99eeb1097666e140f76de1c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretAccessKey")
    def secret_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretAccessKey"))

    @secret_access_key.setter
    def secret_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d821ae4e8211b31e00a4623b655c4c41f015d55d3c299516b015e3f098e4efac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretAccessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountAuthConfigAwsAuthConfigKeys]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountAuthConfigAwsAuthConfigKeys]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountAuthConfigAwsAuthConfigKeys]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a48b33198a191f290f2ecedba9604854b03411563472741ac8e622dfe34058)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountAuthConfigAwsAuthConfigRole",
    jsii_struct_bases=[],
    name_mapping={"external_id": "externalId", "role_name": "roleName"},
)
class IntegrationAwsAccountAuthConfigAwsAuthConfigRole:
    def __init__(
        self,
        *,
        external_id: typing.Optional[builtins.str] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param external_id: AWS IAM External ID for associated role. If omitted, one will be generated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#external_id IntegrationAwsAccount#external_id}
        :param role_name: AWS IAM Role name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#role_name IntegrationAwsAccount#role_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d626e454dadf9277683f1383d7e5edef28b638bc3dd2ba210237ddf54165a731)
            check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if external_id is not None:
            self._values["external_id"] = external_id
        if role_name is not None:
            self._values["role_name"] = role_name

    @builtins.property
    def external_id(self) -> typing.Optional[builtins.str]:
        '''AWS IAM External ID for associated role. If omitted, one will be generated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#external_id IntegrationAwsAccount#external_id}
        '''
        result = self._values.get("external_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''AWS IAM Role name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#role_name IntegrationAwsAccount#role_name}
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationAwsAccountAuthConfigAwsAuthConfigRole(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationAwsAccountAuthConfigAwsAuthConfigRoleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountAuthConfigAwsAuthConfigRoleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c95e946cd8a6386085c2aeede46a928d2b251abd350316284148238b89323528)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExternalId")
    def reset_external_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalId", []))

    @jsii.member(jsii_name="resetRoleName")
    def reset_role_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoleName", []))

    @builtins.property
    @jsii.member(jsii_name="externalIdInput")
    def external_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalIdInput"))

    @builtins.property
    @jsii.member(jsii_name="roleNameInput")
    def role_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="externalId")
    def external_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalId"))

    @external_id.setter
    def external_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__644043ed3e604224437c0aad9b3837a84c8f8d36184932573aac4f2b42327c2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleName"))

    @role_name.setter
    def role_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__107a107c2f516d476a9d9441fcba61ed4e1325b045bae7d57c255b1ab2f03cd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountAuthConfigAwsAuthConfigRole]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountAuthConfigAwsAuthConfigRole]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountAuthConfigAwsAuthConfigRole]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa1926e03fb6d230774c1fafad179c4e883232e6372172f8aff34c1bca45fd71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationAwsAccountAuthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountAuthConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a3e6ae886c07d770b35d61ffa58b43f761f2ef19dfb5720d927f697cfc292b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAwsAuthConfigKeys")
    def put_aws_auth_config_keys(
        self,
        *,
        access_key_id: typing.Optional[builtins.str] = None,
        secret_access_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_key_id: AWS Access Key ID. Invalid access_key_id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#access_key_id IntegrationAwsAccount#access_key_id}
        :param secret_access_key: AWS Secret Access Key. This value is write-only; changes made outside of Terraform will not be drift-detected. Secret_access_key must be non-empty and not contain whitespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#secret_access_key IntegrationAwsAccount#secret_access_key}
        '''
        value = IntegrationAwsAccountAuthConfigAwsAuthConfigKeys(
            access_key_id=access_key_id, secret_access_key=secret_access_key
        )

        return typing.cast(None, jsii.invoke(self, "putAwsAuthConfigKeys", [value]))

    @jsii.member(jsii_name="putAwsAuthConfigRole")
    def put_aws_auth_config_role(
        self,
        *,
        external_id: typing.Optional[builtins.str] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param external_id: AWS IAM External ID for associated role. If omitted, one will be generated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#external_id IntegrationAwsAccount#external_id}
        :param role_name: AWS IAM Role name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#role_name IntegrationAwsAccount#role_name}
        '''
        value = IntegrationAwsAccountAuthConfigAwsAuthConfigRole(
            external_id=external_id, role_name=role_name
        )

        return typing.cast(None, jsii.invoke(self, "putAwsAuthConfigRole", [value]))

    @jsii.member(jsii_name="resetAwsAuthConfigKeys")
    def reset_aws_auth_config_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAuthConfigKeys", []))

    @jsii.member(jsii_name="resetAwsAuthConfigRole")
    def reset_aws_auth_config_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAuthConfigRole", []))

    @builtins.property
    @jsii.member(jsii_name="awsAuthConfigKeys")
    def aws_auth_config_keys(
        self,
    ) -> IntegrationAwsAccountAuthConfigAwsAuthConfigKeysOutputReference:
        return typing.cast(IntegrationAwsAccountAuthConfigAwsAuthConfigKeysOutputReference, jsii.get(self, "awsAuthConfigKeys"))

    @builtins.property
    @jsii.member(jsii_name="awsAuthConfigRole")
    def aws_auth_config_role(
        self,
    ) -> IntegrationAwsAccountAuthConfigAwsAuthConfigRoleOutputReference:
        return typing.cast(IntegrationAwsAccountAuthConfigAwsAuthConfigRoleOutputReference, jsii.get(self, "awsAuthConfigRole"))

    @builtins.property
    @jsii.member(jsii_name="awsAuthConfigKeysInput")
    def aws_auth_config_keys_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountAuthConfigAwsAuthConfigKeys]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountAuthConfigAwsAuthConfigKeys]], jsii.get(self, "awsAuthConfigKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="awsAuthConfigRoleInput")
    def aws_auth_config_role_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountAuthConfigAwsAuthConfigRole]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountAuthConfigAwsAuthConfigRole]], jsii.get(self, "awsAuthConfigRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountAuthConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountAuthConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountAuthConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9b807e487820cc949ea9ca59f09362d15e9270a2e0e660a79b5355f37153eaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountAwsRegions",
    jsii_struct_bases=[],
    name_mapping={"include_all": "includeAll", "include_only": "includeOnly"},
)
class IntegrationAwsAccountAwsRegions:
    def __init__(
        self,
        *,
        include_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_only: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param include_all: Include all regions. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#include_all IntegrationAwsAccount#include_all}
        :param include_only: Include only these regions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#include_only IntegrationAwsAccount#include_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ee3328c9dac34e5af1ed5b7fa9f87820001fc86dc410de363a41c6be3f02d3)
            check_type(argname="argument include_all", value=include_all, expected_type=type_hints["include_all"])
            check_type(argname="argument include_only", value=include_only, expected_type=type_hints["include_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if include_all is not None:
            self._values["include_all"] = include_all
        if include_only is not None:
            self._values["include_only"] = include_only

    @builtins.property
    def include_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Include all regions. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#include_all IntegrationAwsAccount#include_all}
        '''
        result = self._values.get("include_all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_only(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Include only these regions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#include_only IntegrationAwsAccount#include_only}
        '''
        result = self._values.get("include_only")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationAwsAccountAwsRegions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationAwsAccountAwsRegionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountAwsRegionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__575feb53129cda7a05548fd415c0169b24bd5f788bf43317157219cad1769a3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludeAll")
    def reset_include_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeAll", []))

    @jsii.member(jsii_name="resetIncludeOnly")
    def reset_include_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeOnly", []))

    @builtins.property
    @jsii.member(jsii_name="includeAllInput")
    def include_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeAllInput"))

    @builtins.property
    @jsii.member(jsii_name="includeOnlyInput")
    def include_only_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includeOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="includeAll")
    def include_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeAll"))

    @include_all.setter
    def include_all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebde66177eb41e0233cd163cef7ff18f905f1f35a075d3e6e1a0f0e3a0138e48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeOnly")
    def include_only(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeOnly"))

    @include_only.setter
    def include_only(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c9cc5b3668cbe76c79b247d413eb40c3b47fabd6a45208c5906eaa932e78e40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountAwsRegions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountAwsRegions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountAwsRegions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9287520622a6ba183bd09cde0a1cc4702c059a3213faa94e7496e8c4f2df0cde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountConfig",
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
        "aws_partition": "awsPartition",
        "account_tags": "accountTags",
        "auth_config": "authConfig",
        "aws_regions": "awsRegions",
        "logs_config": "logsConfig",
        "metrics_config": "metricsConfig",
        "resources_config": "resourcesConfig",
        "traces_config": "tracesConfig",
    },
)
class IntegrationAwsAccountConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        aws_partition: builtins.str,
        account_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        auth_config: typing.Optional[typing.Union[IntegrationAwsAccountAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_regions: typing.Optional[typing.Union[IntegrationAwsAccountAwsRegions, typing.Dict[builtins.str, typing.Any]]] = None,
        logs_config: typing.Optional[typing.Union["IntegrationAwsAccountLogsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        metrics_config: typing.Optional[typing.Union["IntegrationAwsAccountMetricsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        resources_config: typing.Optional[typing.Union["IntegrationAwsAccountResourcesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        traces_config: typing.Optional[typing.Union["IntegrationAwsAccountTracesConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param aws_account_id: Your AWS Account ID without dashes. Invalid aws_account_id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#aws_account_id IntegrationAwsAccount#aws_account_id}
        :param aws_partition: AWS Account partition. Valid values are ``aws``, ``aws-cn``, ``aws-us-gov``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#aws_partition IntegrationAwsAccount#aws_partition}
        :param account_tags: Tags to apply to all metrics in the account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#account_tags IntegrationAwsAccount#account_tags}
        :param auth_config: auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#auth_config IntegrationAwsAccount#auth_config}
        :param aws_regions: aws_regions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#aws_regions IntegrationAwsAccount#aws_regions}
        :param logs_config: logs_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#logs_config IntegrationAwsAccount#logs_config}
        :param metrics_config: metrics_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#metrics_config IntegrationAwsAccount#metrics_config}
        :param resources_config: resources_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#resources_config IntegrationAwsAccount#resources_config}
        :param traces_config: traces_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#traces_config IntegrationAwsAccount#traces_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(auth_config, dict):
            auth_config = IntegrationAwsAccountAuthConfig(**auth_config)
        if isinstance(aws_regions, dict):
            aws_regions = IntegrationAwsAccountAwsRegions(**aws_regions)
        if isinstance(logs_config, dict):
            logs_config = IntegrationAwsAccountLogsConfig(**logs_config)
        if isinstance(metrics_config, dict):
            metrics_config = IntegrationAwsAccountMetricsConfig(**metrics_config)
        if isinstance(resources_config, dict):
            resources_config = IntegrationAwsAccountResourcesConfig(**resources_config)
        if isinstance(traces_config, dict):
            traces_config = IntegrationAwsAccountTracesConfig(**traces_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb60d90ebef85a4be14b24f6958d1232bc396dc25a4d3214f0ba0c7fe29d76e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
            check_type(argname="argument aws_partition", value=aws_partition, expected_type=type_hints["aws_partition"])
            check_type(argname="argument account_tags", value=account_tags, expected_type=type_hints["account_tags"])
            check_type(argname="argument auth_config", value=auth_config, expected_type=type_hints["auth_config"])
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument logs_config", value=logs_config, expected_type=type_hints["logs_config"])
            check_type(argname="argument metrics_config", value=metrics_config, expected_type=type_hints["metrics_config"])
            check_type(argname="argument resources_config", value=resources_config, expected_type=type_hints["resources_config"])
            check_type(argname="argument traces_config", value=traces_config, expected_type=type_hints["traces_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_account_id": aws_account_id,
            "aws_partition": aws_partition,
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
        if account_tags is not None:
            self._values["account_tags"] = account_tags
        if auth_config is not None:
            self._values["auth_config"] = auth_config
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if logs_config is not None:
            self._values["logs_config"] = logs_config
        if metrics_config is not None:
            self._values["metrics_config"] = metrics_config
        if resources_config is not None:
            self._values["resources_config"] = resources_config
        if traces_config is not None:
            self._values["traces_config"] = traces_config

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
        '''Your AWS Account ID without dashes. Invalid aws_account_id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#aws_account_id IntegrationAwsAccount#aws_account_id}
        '''
        result = self._values.get("aws_account_id")
        assert result is not None, "Required property 'aws_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_partition(self) -> builtins.str:
        '''AWS Account partition. Valid values are ``aws``, ``aws-cn``, ``aws-us-gov``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#aws_partition IntegrationAwsAccount#aws_partition}
        '''
        result = self._values.get("aws_partition")
        assert result is not None, "Required property 'aws_partition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags to apply to all metrics in the account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#account_tags IntegrationAwsAccount#account_tags}
        '''
        result = self._values.get("account_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def auth_config(self) -> typing.Optional[IntegrationAwsAccountAuthConfig]:
        '''auth_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#auth_config IntegrationAwsAccount#auth_config}
        '''
        result = self._values.get("auth_config")
        return typing.cast(typing.Optional[IntegrationAwsAccountAuthConfig], result)

    @builtins.property
    def aws_regions(self) -> typing.Optional[IntegrationAwsAccountAwsRegions]:
        '''aws_regions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#aws_regions IntegrationAwsAccount#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[IntegrationAwsAccountAwsRegions], result)

    @builtins.property
    def logs_config(self) -> typing.Optional["IntegrationAwsAccountLogsConfig"]:
        '''logs_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#logs_config IntegrationAwsAccount#logs_config}
        '''
        result = self._values.get("logs_config")
        return typing.cast(typing.Optional["IntegrationAwsAccountLogsConfig"], result)

    @builtins.property
    def metrics_config(self) -> typing.Optional["IntegrationAwsAccountMetricsConfig"]:
        '''metrics_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#metrics_config IntegrationAwsAccount#metrics_config}
        '''
        result = self._values.get("metrics_config")
        return typing.cast(typing.Optional["IntegrationAwsAccountMetricsConfig"], result)

    @builtins.property
    def resources_config(
        self,
    ) -> typing.Optional["IntegrationAwsAccountResourcesConfig"]:
        '''resources_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#resources_config IntegrationAwsAccount#resources_config}
        '''
        result = self._values.get("resources_config")
        return typing.cast(typing.Optional["IntegrationAwsAccountResourcesConfig"], result)

    @builtins.property
    def traces_config(self) -> typing.Optional["IntegrationAwsAccountTracesConfig"]:
        '''traces_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#traces_config IntegrationAwsAccount#traces_config}
        '''
        result = self._values.get("traces_config")
        return typing.cast(typing.Optional["IntegrationAwsAccountTracesConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationAwsAccountConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountLogsConfig",
    jsii_struct_bases=[],
    name_mapping={"lambda_forwarder": "lambdaForwarder"},
)
class IntegrationAwsAccountLogsConfig:
    def __init__(
        self,
        *,
        lambda_forwarder: typing.Optional[typing.Union["IntegrationAwsAccountLogsConfigLambdaForwarder", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param lambda_forwarder: lambda_forwarder block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#lambda_forwarder IntegrationAwsAccount#lambda_forwarder}
        '''
        if isinstance(lambda_forwarder, dict):
            lambda_forwarder = IntegrationAwsAccountLogsConfigLambdaForwarder(**lambda_forwarder)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89598ce79d841e21c4cd2437255dc24a42161234eca587a391607c0c1dabb40c)
            check_type(argname="argument lambda_forwarder", value=lambda_forwarder, expected_type=type_hints["lambda_forwarder"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if lambda_forwarder is not None:
            self._values["lambda_forwarder"] = lambda_forwarder

    @builtins.property
    def lambda_forwarder(
        self,
    ) -> typing.Optional["IntegrationAwsAccountLogsConfigLambdaForwarder"]:
        '''lambda_forwarder block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#lambda_forwarder IntegrationAwsAccount#lambda_forwarder}
        '''
        result = self._values.get("lambda_forwarder")
        return typing.cast(typing.Optional["IntegrationAwsAccountLogsConfigLambdaForwarder"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationAwsAccountLogsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountLogsConfigLambdaForwarder",
    jsii_struct_bases=[],
    name_mapping={"lambdas": "lambdas", "sources": "sources"},
)
class IntegrationAwsAccountLogsConfigLambdaForwarder:
    def __init__(
        self,
        *,
        lambdas: typing.Optional[typing.Sequence[builtins.str]] = None,
        sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param lambdas: List of Datadog Lambda Log Forwarder ARNs in your AWS account. Defaults to ``[]``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#lambdas IntegrationAwsAccount#lambdas}
        :param sources: List of service IDs set to enable automatic log collection. Use ```datadog_integration_aws_available_logs_services`` data source <https://registry.terraform.io/providers/DataDog/datadog/latest/docs/data-sources/integration_aws_available_logs_services>`_ to get allowed values. Defaults to ``[]``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#sources IntegrationAwsAccount#sources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14500237736f303d5eb0ac8b04eae7f87cdc87620e16c35ab01ea1c32c6e21d6)
            check_type(argname="argument lambdas", value=lambdas, expected_type=type_hints["lambdas"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if lambdas is not None:
            self._values["lambdas"] = lambdas
        if sources is not None:
            self._values["sources"] = sources

    @builtins.property
    def lambdas(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of Datadog Lambda Log Forwarder ARNs in your AWS account. Defaults to ``[]``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#lambdas IntegrationAwsAccount#lambdas}
        '''
        result = self._values.get("lambdas")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of service IDs set to enable automatic log collection.

        Use ```datadog_integration_aws_available_logs_services`` data source <https://registry.terraform.io/providers/DataDog/datadog/latest/docs/data-sources/integration_aws_available_logs_services>`_ to get allowed values. Defaults to ``[]``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#sources IntegrationAwsAccount#sources}
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationAwsAccountLogsConfigLambdaForwarder(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationAwsAccountLogsConfigLambdaForwarderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountLogsConfigLambdaForwarderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f70f0ae94a9fde6797e913880422b1a54421e28f5dad8349deebbf8e61117baf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLambdas")
    def reset_lambdas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdas", []))

    @jsii.member(jsii_name="resetSources")
    def reset_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSources", []))

    @builtins.property
    @jsii.member(jsii_name="lambdasInput")
    def lambdas_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "lambdasInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdas")
    def lambdas(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "lambdas"))

    @lambdas.setter
    def lambdas(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98e62c20d94a9f76a7955c2c00c76b00c6b1238ebf5632a02eae340000f42369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40fdd9eaf272408e82f06c1120a3a2382a03c9750178f8ad187ebf7d049e720e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountLogsConfigLambdaForwarder]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountLogsConfigLambdaForwarder]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountLogsConfigLambdaForwarder]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cb9dae77d955f4de34348bc75d0144054bf966ce893a561bec87a3cd3c6faf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationAwsAccountLogsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountLogsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aec5c2f38e338b8ffdbac74b7de1132fbe01257241e4800030c65364a79f5ee1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLambdaForwarder")
    def put_lambda_forwarder(
        self,
        *,
        lambdas: typing.Optional[typing.Sequence[builtins.str]] = None,
        sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param lambdas: List of Datadog Lambda Log Forwarder ARNs in your AWS account. Defaults to ``[]``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#lambdas IntegrationAwsAccount#lambdas}
        :param sources: List of service IDs set to enable automatic log collection. Use ```datadog_integration_aws_available_logs_services`` data source <https://registry.terraform.io/providers/DataDog/datadog/latest/docs/data-sources/integration_aws_available_logs_services>`_ to get allowed values. Defaults to ``[]``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#sources IntegrationAwsAccount#sources}
        '''
        value = IntegrationAwsAccountLogsConfigLambdaForwarder(
            lambdas=lambdas, sources=sources
        )

        return typing.cast(None, jsii.invoke(self, "putLambdaForwarder", [value]))

    @jsii.member(jsii_name="resetLambdaForwarder")
    def reset_lambda_forwarder(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaForwarder", []))

    @builtins.property
    @jsii.member(jsii_name="lambdaForwarder")
    def lambda_forwarder(
        self,
    ) -> IntegrationAwsAccountLogsConfigLambdaForwarderOutputReference:
        return typing.cast(IntegrationAwsAccountLogsConfigLambdaForwarderOutputReference, jsii.get(self, "lambdaForwarder"))

    @builtins.property
    @jsii.member(jsii_name="lambdaForwarderInput")
    def lambda_forwarder_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountLogsConfigLambdaForwarder]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountLogsConfigLambdaForwarder]], jsii.get(self, "lambdaForwarderInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountLogsConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountLogsConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountLogsConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__546b36a133955ad3b9bb494d64b5960e7ddc5fa13b19e7facb5e8bd420bd7aaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountMetricsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "automute_enabled": "automuteEnabled",
        "collect_cloudwatch_alarms": "collectCloudwatchAlarms",
        "collect_custom_metrics": "collectCustomMetrics",
        "enabled": "enabled",
        "namespace_filters": "namespaceFilters",
        "tag_filters": "tagFilters",
    },
)
class IntegrationAwsAccountMetricsConfig:
    def __init__(
        self,
        *,
        automute_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        collect_cloudwatch_alarms: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        collect_custom_metrics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        namespace_filters: typing.Optional[typing.Union["IntegrationAwsAccountMetricsConfigNamespaceFilters", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationAwsAccountMetricsConfigTagFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param automute_enabled: Enable EC2 automute for AWS metrics Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#automute_enabled IntegrationAwsAccount#automute_enabled}
        :param collect_cloudwatch_alarms: Enable CloudWatch alarms collection Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#collect_cloudwatch_alarms IntegrationAwsAccount#collect_cloudwatch_alarms}
        :param collect_custom_metrics: Enable custom metrics collection Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#collect_custom_metrics IntegrationAwsAccount#collect_custom_metrics}
        :param enabled: Enable AWS metrics collection Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#enabled IntegrationAwsAccount#enabled}
        :param namespace_filters: namespace_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#namespace_filters IntegrationAwsAccount#namespace_filters}
        :param tag_filters: tag_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#tag_filters IntegrationAwsAccount#tag_filters}
        '''
        if isinstance(namespace_filters, dict):
            namespace_filters = IntegrationAwsAccountMetricsConfigNamespaceFilters(**namespace_filters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c3755f11f62852da42d8b80325f3029517c61e410ef0ae892c9650f35700938)
            check_type(argname="argument automute_enabled", value=automute_enabled, expected_type=type_hints["automute_enabled"])
            check_type(argname="argument collect_cloudwatch_alarms", value=collect_cloudwatch_alarms, expected_type=type_hints["collect_cloudwatch_alarms"])
            check_type(argname="argument collect_custom_metrics", value=collect_custom_metrics, expected_type=type_hints["collect_custom_metrics"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument namespace_filters", value=namespace_filters, expected_type=type_hints["namespace_filters"])
            check_type(argname="argument tag_filters", value=tag_filters, expected_type=type_hints["tag_filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if automute_enabled is not None:
            self._values["automute_enabled"] = automute_enabled
        if collect_cloudwatch_alarms is not None:
            self._values["collect_cloudwatch_alarms"] = collect_cloudwatch_alarms
        if collect_custom_metrics is not None:
            self._values["collect_custom_metrics"] = collect_custom_metrics
        if enabled is not None:
            self._values["enabled"] = enabled
        if namespace_filters is not None:
            self._values["namespace_filters"] = namespace_filters
        if tag_filters is not None:
            self._values["tag_filters"] = tag_filters

    @builtins.property
    def automute_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable EC2 automute for AWS metrics Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#automute_enabled IntegrationAwsAccount#automute_enabled}
        '''
        result = self._values.get("automute_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def collect_cloudwatch_alarms(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable CloudWatch alarms collection Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#collect_cloudwatch_alarms IntegrationAwsAccount#collect_cloudwatch_alarms}
        '''
        result = self._values.get("collect_cloudwatch_alarms")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def collect_custom_metrics(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable custom metrics collection Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#collect_custom_metrics IntegrationAwsAccount#collect_custom_metrics}
        '''
        result = self._values.get("collect_custom_metrics")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable AWS metrics collection Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#enabled IntegrationAwsAccount#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def namespace_filters(
        self,
    ) -> typing.Optional["IntegrationAwsAccountMetricsConfigNamespaceFilters"]:
        '''namespace_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#namespace_filters IntegrationAwsAccount#namespace_filters}
        '''
        result = self._values.get("namespace_filters")
        return typing.cast(typing.Optional["IntegrationAwsAccountMetricsConfigNamespaceFilters"], result)

    @builtins.property
    def tag_filters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationAwsAccountMetricsConfigTagFilters"]]]:
        '''tag_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#tag_filters IntegrationAwsAccount#tag_filters}
        '''
        result = self._values.get("tag_filters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationAwsAccountMetricsConfigTagFilters"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationAwsAccountMetricsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountMetricsConfigNamespaceFilters",
    jsii_struct_bases=[],
    name_mapping={"exclude_only": "excludeOnly", "include_only": "includeOnly"},
)
class IntegrationAwsAccountMetricsConfigNamespaceFilters:
    def __init__(
        self,
        *,
        exclude_only: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_only: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param exclude_only: Exclude only these namespaces from metrics collection. Use ```datadog_integration_aws_available_namespaces`` data source <https://registry.terraform.io/providers/DataDog/datadog/latest/docs/data-sources/integration_aws_available_namespaces>`_ to get allowed values. Defaults to ``["AWS/SQS", "AWS/ElasticMapReduce"]``. ``AWS/SQS`` and ``AWS/ElasticMapReduce`` are excluded by default to reduce your AWS CloudWatch costs from ``GetMetricData`` API calls. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#exclude_only IntegrationAwsAccount#exclude_only}
        :param include_only: Include only these namespaces for metrics collection. Use ```datadog_integration_aws_available_namespaces`` data source <https://registry.terraform.io/providers/DataDog/datadog/latest/docs/data-sources/integration_aws_available_namespaces>`_ to get allowed values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#include_only IntegrationAwsAccount#include_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e284be53f1b4a8befee78c5a290174aa133053282a58c837dadbc2403938cf63)
            check_type(argname="argument exclude_only", value=exclude_only, expected_type=type_hints["exclude_only"])
            check_type(argname="argument include_only", value=include_only, expected_type=type_hints["include_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude_only is not None:
            self._values["exclude_only"] = exclude_only
        if include_only is not None:
            self._values["include_only"] = include_only

    @builtins.property
    def exclude_only(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Exclude only these namespaces from metrics collection.

        Use ```datadog_integration_aws_available_namespaces`` data source <https://registry.terraform.io/providers/DataDog/datadog/latest/docs/data-sources/integration_aws_available_namespaces>`_ to get allowed values. Defaults to ``["AWS/SQS", "AWS/ElasticMapReduce"]``. ``AWS/SQS`` and ``AWS/ElasticMapReduce`` are excluded by default to reduce your AWS CloudWatch costs from ``GetMetricData`` API calls.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#exclude_only IntegrationAwsAccount#exclude_only}
        '''
        result = self._values.get("exclude_only")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_only(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Include only these namespaces for metrics collection. Use ```datadog_integration_aws_available_namespaces`` data source <https://registry.terraform.io/providers/DataDog/datadog/latest/docs/data-sources/integration_aws_available_namespaces>`_ to get allowed values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#include_only IntegrationAwsAccount#include_only}
        '''
        result = self._values.get("include_only")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationAwsAccountMetricsConfigNamespaceFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationAwsAccountMetricsConfigNamespaceFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountMetricsConfigNamespaceFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00a42c3ab69ed62a9c223b7e99ff4f7dc99a52c5a19c4f40578d8f051c53d258)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludeOnly")
    def reset_exclude_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeOnly", []))

    @jsii.member(jsii_name="resetIncludeOnly")
    def reset_include_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeOnly", []))

    @builtins.property
    @jsii.member(jsii_name="excludeOnlyInput")
    def exclude_only_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludeOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="includeOnlyInput")
    def include_only_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includeOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeOnly")
    def exclude_only(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludeOnly"))

    @exclude_only.setter
    def exclude_only(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edeafd10fa4dd699d06b05f53f6852f4065bca0d2ea5b4bcf757831526d26ec6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeOnly")
    def include_only(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeOnly"))

    @include_only.setter
    def include_only(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54496068acc6f1fea0df733c20cf7987ab00f574b9245eb7d8818df71339069e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountMetricsConfigNamespaceFilters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountMetricsConfigNamespaceFilters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountMetricsConfigNamespaceFilters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f69004b0bc42d44c3bdbc68d963ceab4a696b00bd1abed59d5042f6087ae8947)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationAwsAccountMetricsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountMetricsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26960653ee389067d4ab9bf2d54ff8520a8a1aaab5685a703fb3bc4e263780f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNamespaceFilters")
    def put_namespace_filters(
        self,
        *,
        exclude_only: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_only: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param exclude_only: Exclude only these namespaces from metrics collection. Use ```datadog_integration_aws_available_namespaces`` data source <https://registry.terraform.io/providers/DataDog/datadog/latest/docs/data-sources/integration_aws_available_namespaces>`_ to get allowed values. Defaults to ``["AWS/SQS", "AWS/ElasticMapReduce"]``. ``AWS/SQS`` and ``AWS/ElasticMapReduce`` are excluded by default to reduce your AWS CloudWatch costs from ``GetMetricData`` API calls. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#exclude_only IntegrationAwsAccount#exclude_only}
        :param include_only: Include only these namespaces for metrics collection. Use ```datadog_integration_aws_available_namespaces`` data source <https://registry.terraform.io/providers/DataDog/datadog/latest/docs/data-sources/integration_aws_available_namespaces>`_ to get allowed values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#include_only IntegrationAwsAccount#include_only}
        '''
        value = IntegrationAwsAccountMetricsConfigNamespaceFilters(
            exclude_only=exclude_only, include_only=include_only
        )

        return typing.cast(None, jsii.invoke(self, "putNamespaceFilters", [value]))

    @jsii.member(jsii_name="putTagFilters")
    def put_tag_filters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationAwsAccountMetricsConfigTagFilters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae19542728d9cb9085e0d61362c93f2b0c3cefbeadeadbed7766473e1a535eff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTagFilters", [value]))

    @jsii.member(jsii_name="resetAutomuteEnabled")
    def reset_automute_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomuteEnabled", []))

    @jsii.member(jsii_name="resetCollectCloudwatchAlarms")
    def reset_collect_cloudwatch_alarms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollectCloudwatchAlarms", []))

    @jsii.member(jsii_name="resetCollectCustomMetrics")
    def reset_collect_custom_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollectCustomMetrics", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetNamespaceFilters")
    def reset_namespace_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespaceFilters", []))

    @jsii.member(jsii_name="resetTagFilters")
    def reset_tag_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagFilters", []))

    @builtins.property
    @jsii.member(jsii_name="namespaceFilters")
    def namespace_filters(
        self,
    ) -> IntegrationAwsAccountMetricsConfigNamespaceFiltersOutputReference:
        return typing.cast(IntegrationAwsAccountMetricsConfigNamespaceFiltersOutputReference, jsii.get(self, "namespaceFilters"))

    @builtins.property
    @jsii.member(jsii_name="tagFilters")
    def tag_filters(self) -> "IntegrationAwsAccountMetricsConfigTagFiltersList":
        return typing.cast("IntegrationAwsAccountMetricsConfigTagFiltersList", jsii.get(self, "tagFilters"))

    @builtins.property
    @jsii.member(jsii_name="automuteEnabledInput")
    def automute_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "automuteEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="collectCloudwatchAlarmsInput")
    def collect_cloudwatch_alarms_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "collectCloudwatchAlarmsInput"))

    @builtins.property
    @jsii.member(jsii_name="collectCustomMetricsInput")
    def collect_custom_metrics_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "collectCustomMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceFiltersInput")
    def namespace_filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountMetricsConfigNamespaceFilters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountMetricsConfigNamespaceFilters]], jsii.get(self, "namespaceFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="tagFiltersInput")
    def tag_filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationAwsAccountMetricsConfigTagFilters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationAwsAccountMetricsConfigTagFilters"]]], jsii.get(self, "tagFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="automuteEnabled")
    def automute_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "automuteEnabled"))

    @automute_enabled.setter
    def automute_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e58240c3e92cad23930d727f2ad32df758b1b86b7aca575d43adfa372bfd9721)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automuteEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="collectCloudwatchAlarms")
    def collect_cloudwatch_alarms(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "collectCloudwatchAlarms"))

    @collect_cloudwatch_alarms.setter
    def collect_cloudwatch_alarms(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2711cd7145467bc5cb682df6901ab112aa945c6d4be2730e632053f680416c4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collectCloudwatchAlarms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="collectCustomMetrics")
    def collect_custom_metrics(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "collectCustomMetrics"))

    @collect_custom_metrics.setter
    def collect_custom_metrics(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99ed1e8e3dc1408eb9dc816083aca02ab21915f5e9585bbc9d157e0cd477640f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collectCustomMetrics", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__097f4b463f35fa9fb70b833f3955ff9d7972c5b5c1ee81b18fdd335b89d391d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountMetricsConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountMetricsConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountMetricsConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a3fbf9bf74a7c2d39c50f75282f252814afdb1f7bda8f16da252b1355ad660)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountMetricsConfigTagFilters",
    jsii_struct_bases=[],
    name_mapping={"namespace": "namespace", "tags": "tags"},
)
class IntegrationAwsAccountMetricsConfigTagFilters:
    def __init__(
        self,
        *,
        namespace: builtins.str,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param namespace: The AWS service for which the tag filters defined in ``tags`` will be applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#namespace IntegrationAwsAccount#namespace}
        :param tags: The AWS resource tags to filter on for the service specified by ``namespace``. Defaults to ``[]``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#tags IntegrationAwsAccount#tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__026a54da580ae94914a09169cc207d9f136925663dc3fa2e9c98ce86557a7182)
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespace": namespace,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def namespace(self) -> builtins.str:
        '''The AWS service for which the tag filters defined in ``tags`` will be applied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#namespace IntegrationAwsAccount#namespace}
        '''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The AWS resource tags to filter on for the service specified by ``namespace``. Defaults to ``[]``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#tags IntegrationAwsAccount#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationAwsAccountMetricsConfigTagFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationAwsAccountMetricsConfigTagFiltersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountMetricsConfigTagFiltersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40e76d2d8628768c98832cfb3dc06a68eacbb4c1eaf8d2f8ced2844d637675d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IntegrationAwsAccountMetricsConfigTagFiltersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc1a337055c8e5cb9e58d3d8f85f6fac09017a4edb2013693aad400db16013dd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IntegrationAwsAccountMetricsConfigTagFiltersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1165217240d9982dc61341269b8d60ac5d7d71a0a124006cd5df3fcf56551aa8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__806efd57ec799f2df867ccb7040e60cc702ef547e16cea9cfe95e8054ebdbf89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b310d6d098c0aa08bdaa5ef1fff6643243e68a3d287536daf77b54ec90cca207)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationAwsAccountMetricsConfigTagFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationAwsAccountMetricsConfigTagFilters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationAwsAccountMetricsConfigTagFilters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7543f12b4e1aab974782abf3cb9dae9d353840de9f3b3531f634aaece5d905a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationAwsAccountMetricsConfigTagFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountMetricsConfigTagFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dad3dc3eb2324d50ad1033a5d992e7cf2e168f8f75348373810793c585e33664)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c83b22d3d1be4698c1eb9e102770038e820e39d2f0e680525c69a26788db50d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da426ee51f2955044acdb696201cb795f40b41b4c9d6d103fb4a5dd49dc8d50e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountMetricsConfigTagFilters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountMetricsConfigTagFilters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountMetricsConfigTagFilters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__566e7adf57c004cca54c6e77e6b9e7a0412efcda52411de5ad94765ab5e95913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountResourcesConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_security_posture_management_collection": "cloudSecurityPostureManagementCollection",
        "extended_collection": "extendedCollection",
    },
)
class IntegrationAwsAccountResourcesConfig:
    def __init__(
        self,
        *,
        cloud_security_posture_management_collection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        extended_collection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cloud_security_posture_management_collection: Enable Cloud Security Management to scan AWS resources for vulnerabilities, misconfigurations, identity risks, and compliance violations. Requires ``extended_collection`` to be set to ``true``. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#cloud_security_posture_management_collection IntegrationAwsAccount#cloud_security_posture_management_collection}
        :param extended_collection: Whether Datadog collects additional attributes and configuration information about the resources in your AWS account. Required for ``cloud_security_posture_management_collection``. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#extended_collection IntegrationAwsAccount#extended_collection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b856d8bb78fb3ef8469b2b5aa1aadd0e08321fc05a3afd35e6c7e85d1497f7d)
            check_type(argname="argument cloud_security_posture_management_collection", value=cloud_security_posture_management_collection, expected_type=type_hints["cloud_security_posture_management_collection"])
            check_type(argname="argument extended_collection", value=extended_collection, expected_type=type_hints["extended_collection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_security_posture_management_collection is not None:
            self._values["cloud_security_posture_management_collection"] = cloud_security_posture_management_collection
        if extended_collection is not None:
            self._values["extended_collection"] = extended_collection

    @builtins.property
    def cloud_security_posture_management_collection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable Cloud Security Management to scan AWS resources for vulnerabilities, misconfigurations, identity risks, and compliance violations.

        Requires ``extended_collection`` to be set to ``true``. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#cloud_security_posture_management_collection IntegrationAwsAccount#cloud_security_posture_management_collection}
        '''
        result = self._values.get("cloud_security_posture_management_collection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def extended_collection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Datadog collects additional attributes and configuration information about the resources in your AWS account.

        Required for ``cloud_security_posture_management_collection``. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#extended_collection IntegrationAwsAccount#extended_collection}
        '''
        result = self._values.get("extended_collection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationAwsAccountResourcesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationAwsAccountResourcesConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountResourcesConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25d9eab0e555b96077e6abe52ff05b61677ca29077b38798fbb657668def6798)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCloudSecurityPostureManagementCollection")
    def reset_cloud_security_posture_management_collection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudSecurityPostureManagementCollection", []))

    @jsii.member(jsii_name="resetExtendedCollection")
    def reset_extended_collection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtendedCollection", []))

    @builtins.property
    @jsii.member(jsii_name="cloudSecurityPostureManagementCollectionInput")
    def cloud_security_posture_management_collection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cloudSecurityPostureManagementCollectionInput"))

    @builtins.property
    @jsii.member(jsii_name="extendedCollectionInput")
    def extended_collection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "extendedCollectionInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudSecurityPostureManagementCollection")
    def cloud_security_posture_management_collection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cloudSecurityPostureManagementCollection"))

    @cloud_security_posture_management_collection.setter
    def cloud_security_posture_management_collection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15df3f57c40713b36ae378762fd16519b2968cb7bfc36be35b154bb71a2a275e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudSecurityPostureManagementCollection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extendedCollection")
    def extended_collection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "extendedCollection"))

    @extended_collection.setter
    def extended_collection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc62e3afb40739ecab3c3b528549fbee44eee21a34356bf7d6fb776e4f0d8cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendedCollection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountResourcesConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountResourcesConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountResourcesConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0011c741b8840214f285d7d040877f53433bce84089c3625e2f929f84c61f0f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountTracesConfig",
    jsii_struct_bases=[],
    name_mapping={"xray_services": "xrayServices"},
)
class IntegrationAwsAccountTracesConfig:
    def __init__(
        self,
        *,
        xray_services: typing.Optional[typing.Union["IntegrationAwsAccountTracesConfigXrayServices", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param xray_services: xray_services block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#xray_services IntegrationAwsAccount#xray_services}
        '''
        if isinstance(xray_services, dict):
            xray_services = IntegrationAwsAccountTracesConfigXrayServices(**xray_services)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c519297662c2190142196f1d6d0e24b17175f6aa5f8154b7fa1fa6a6d8882fc8)
            check_type(argname="argument xray_services", value=xray_services, expected_type=type_hints["xray_services"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if xray_services is not None:
            self._values["xray_services"] = xray_services

    @builtins.property
    def xray_services(
        self,
    ) -> typing.Optional["IntegrationAwsAccountTracesConfigXrayServices"]:
        '''xray_services block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#xray_services IntegrationAwsAccount#xray_services}
        '''
        result = self._values.get("xray_services")
        return typing.cast(typing.Optional["IntegrationAwsAccountTracesConfigXrayServices"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationAwsAccountTracesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationAwsAccountTracesConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountTracesConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81373bac28b871d35bb950c2fdbe9311985bea5fcb5ec2c143718bcef05faa55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putXrayServices")
    def put_xray_services(
        self,
        *,
        include_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_only: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param include_all: Include all services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#include_all IntegrationAwsAccount#include_all}
        :param include_only: Include only these services. Defaults to ``[]``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#include_only IntegrationAwsAccount#include_only}
        '''
        value = IntegrationAwsAccountTracesConfigXrayServices(
            include_all=include_all, include_only=include_only
        )

        return typing.cast(None, jsii.invoke(self, "putXrayServices", [value]))

    @jsii.member(jsii_name="resetXrayServices")
    def reset_xray_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXrayServices", []))

    @builtins.property
    @jsii.member(jsii_name="xrayServices")
    def xray_services(
        self,
    ) -> "IntegrationAwsAccountTracesConfigXrayServicesOutputReference":
        return typing.cast("IntegrationAwsAccountTracesConfigXrayServicesOutputReference", jsii.get(self, "xrayServices"))

    @builtins.property
    @jsii.member(jsii_name="xrayServicesInput")
    def xray_services_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IntegrationAwsAccountTracesConfigXrayServices"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IntegrationAwsAccountTracesConfigXrayServices"]], jsii.get(self, "xrayServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountTracesConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountTracesConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountTracesConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6f71d1901e2eb511a77915fbe9b9fa951e5b27b5f2b6cc2d723edb307ef3424)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountTracesConfigXrayServices",
    jsii_struct_bases=[],
    name_mapping={"include_all": "includeAll", "include_only": "includeOnly"},
)
class IntegrationAwsAccountTracesConfigXrayServices:
    def __init__(
        self,
        *,
        include_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_only: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param include_all: Include all services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#include_all IntegrationAwsAccount#include_all}
        :param include_only: Include only these services. Defaults to ``[]``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#include_only IntegrationAwsAccount#include_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0694af8f33001e26147e2dcc1438d2ce9960a015c3e8cd6dc49879b8cfff194)
            check_type(argname="argument include_all", value=include_all, expected_type=type_hints["include_all"])
            check_type(argname="argument include_only", value=include_only, expected_type=type_hints["include_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if include_all is not None:
            self._values["include_all"] = include_all
        if include_only is not None:
            self._values["include_only"] = include_only

    @builtins.property
    def include_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Include all services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#include_all IntegrationAwsAccount#include_all}
        '''
        result = self._values.get("include_all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_only(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Include only these services. Defaults to ``[]``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws_account#include_only IntegrationAwsAccount#include_only}
        '''
        result = self._values.get("include_only")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationAwsAccountTracesConfigXrayServices(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationAwsAccountTracesConfigXrayServicesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.integrationAwsAccount.IntegrationAwsAccountTracesConfigXrayServicesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b72dc9571b19c4181e2e0a1258660cb461d3cbc1aae21d17264243d7ecef341c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludeAll")
    def reset_include_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeAll", []))

    @jsii.member(jsii_name="resetIncludeOnly")
    def reset_include_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeOnly", []))

    @builtins.property
    @jsii.member(jsii_name="includeAllInput")
    def include_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeAllInput"))

    @builtins.property
    @jsii.member(jsii_name="includeOnlyInput")
    def include_only_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includeOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="includeAll")
    def include_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeAll"))

    @include_all.setter
    def include_all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7fff512f0955d9a6f7b0b876e2dd76c85d80cf9a262c2d3b3d1644da64d2a89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeOnly")
    def include_only(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includeOnly"))

    @include_only.setter
    def include_only(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bca101bf8d35d8c9c3ce1a3feade0332595c286e83aa9bad0d4c0792fa0c105)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountTracesConfigXrayServices]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountTracesConfigXrayServices]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountTracesConfigXrayServices]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea7edbff26e5fa54ed9c1ff532ee15bad85e5f2153d52c9738a90a561b326ff6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "IntegrationAwsAccount",
    "IntegrationAwsAccountAuthConfig",
    "IntegrationAwsAccountAuthConfigAwsAuthConfigKeys",
    "IntegrationAwsAccountAuthConfigAwsAuthConfigKeysOutputReference",
    "IntegrationAwsAccountAuthConfigAwsAuthConfigRole",
    "IntegrationAwsAccountAuthConfigAwsAuthConfigRoleOutputReference",
    "IntegrationAwsAccountAuthConfigOutputReference",
    "IntegrationAwsAccountAwsRegions",
    "IntegrationAwsAccountAwsRegionsOutputReference",
    "IntegrationAwsAccountConfig",
    "IntegrationAwsAccountLogsConfig",
    "IntegrationAwsAccountLogsConfigLambdaForwarder",
    "IntegrationAwsAccountLogsConfigLambdaForwarderOutputReference",
    "IntegrationAwsAccountLogsConfigOutputReference",
    "IntegrationAwsAccountMetricsConfig",
    "IntegrationAwsAccountMetricsConfigNamespaceFilters",
    "IntegrationAwsAccountMetricsConfigNamespaceFiltersOutputReference",
    "IntegrationAwsAccountMetricsConfigOutputReference",
    "IntegrationAwsAccountMetricsConfigTagFilters",
    "IntegrationAwsAccountMetricsConfigTagFiltersList",
    "IntegrationAwsAccountMetricsConfigTagFiltersOutputReference",
    "IntegrationAwsAccountResourcesConfig",
    "IntegrationAwsAccountResourcesConfigOutputReference",
    "IntegrationAwsAccountTracesConfig",
    "IntegrationAwsAccountTracesConfigOutputReference",
    "IntegrationAwsAccountTracesConfigXrayServices",
    "IntegrationAwsAccountTracesConfigXrayServicesOutputReference",
]

publication.publish()

def _typecheckingstub__bcd63bc0d287e84fdf49342387a0d0779d4e91bae2231475b2431639338c336b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    aws_account_id: builtins.str,
    aws_partition: builtins.str,
    account_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    auth_config: typing.Optional[typing.Union[IntegrationAwsAccountAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_regions: typing.Optional[typing.Union[IntegrationAwsAccountAwsRegions, typing.Dict[builtins.str, typing.Any]]] = None,
    logs_config: typing.Optional[typing.Union[IntegrationAwsAccountLogsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    metrics_config: typing.Optional[typing.Union[IntegrationAwsAccountMetricsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    resources_config: typing.Optional[typing.Union[IntegrationAwsAccountResourcesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    traces_config: typing.Optional[typing.Union[IntegrationAwsAccountTracesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d5e8bdfd6ea50b7317165530d43a3bc038672e5c67ca891ca7581f6c4903aabf(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef9f7982a5101f71f9bdaf9cc100c53d94234abc324495e573035cb39d8a31c0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d81516a536e9b3b59e713dee845b0765aac48a879e943786fc729f5e4072eba7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7066b0a08aa786814c118bce1ebe8daa0218cefe9ea4ef1ff407f8606fb1f55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8854dc09dbc7970de1b7ba0d5434e7e175bd663d7605291a5d3640c098ac1cf3(
    *,
    aws_auth_config_keys: typing.Optional[typing.Union[IntegrationAwsAccountAuthConfigAwsAuthConfigKeys, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_auth_config_role: typing.Optional[typing.Union[IntegrationAwsAccountAuthConfigAwsAuthConfigRole, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc06718dc917d2bf3477581cfc9c69a929e4df5b4a9cfcd4435a87f45269d801(
    *,
    access_key_id: typing.Optional[builtins.str] = None,
    secret_access_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c4a96896e63648e1dbd2126dcf371fea65dba902c0c2c53aab4d24b0001050(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c9a2610afa7168a8da2124acd0324476d5ac9fa99eeb1097666e140f76de1c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d821ae4e8211b31e00a4623b655c4c41f015d55d3c299516b015e3f098e4efac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a48b33198a191f290f2ecedba9604854b03411563472741ac8e622dfe34058(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountAuthConfigAwsAuthConfigKeys]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d626e454dadf9277683f1383d7e5edef28b638bc3dd2ba210237ddf54165a731(
    *,
    external_id: typing.Optional[builtins.str] = None,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c95e946cd8a6386085c2aeede46a928d2b251abd350316284148238b89323528(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__644043ed3e604224437c0aad9b3837a84c8f8d36184932573aac4f2b42327c2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__107a107c2f516d476a9d9441fcba61ed4e1325b045bae7d57c255b1ab2f03cd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa1926e03fb6d230774c1fafad179c4e883232e6372172f8aff34c1bca45fd71(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountAuthConfigAwsAuthConfigRole]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a3e6ae886c07d770b35d61ffa58b43f761f2ef19dfb5720d927f697cfc292b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b807e487820cc949ea9ca59f09362d15e9270a2e0e660a79b5355f37153eaf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountAuthConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ee3328c9dac34e5af1ed5b7fa9f87820001fc86dc410de363a41c6be3f02d3(
    *,
    include_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_only: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__575feb53129cda7a05548fd415c0169b24bd5f788bf43317157219cad1769a3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebde66177eb41e0233cd163cef7ff18f905f1f35a075d3e6e1a0f0e3a0138e48(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9cc5b3668cbe76c79b247d413eb40c3b47fabd6a45208c5906eaa932e78e40(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9287520622a6ba183bd09cde0a1cc4702c059a3213faa94e7496e8c4f2df0cde(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountAwsRegions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb60d90ebef85a4be14b24f6958d1232bc396dc25a4d3214f0ba0c7fe29d76e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    aws_account_id: builtins.str,
    aws_partition: builtins.str,
    account_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    auth_config: typing.Optional[typing.Union[IntegrationAwsAccountAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_regions: typing.Optional[typing.Union[IntegrationAwsAccountAwsRegions, typing.Dict[builtins.str, typing.Any]]] = None,
    logs_config: typing.Optional[typing.Union[IntegrationAwsAccountLogsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    metrics_config: typing.Optional[typing.Union[IntegrationAwsAccountMetricsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    resources_config: typing.Optional[typing.Union[IntegrationAwsAccountResourcesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    traces_config: typing.Optional[typing.Union[IntegrationAwsAccountTracesConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89598ce79d841e21c4cd2437255dc24a42161234eca587a391607c0c1dabb40c(
    *,
    lambda_forwarder: typing.Optional[typing.Union[IntegrationAwsAccountLogsConfigLambdaForwarder, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14500237736f303d5eb0ac8b04eae7f87cdc87620e16c35ab01ea1c32c6e21d6(
    *,
    lambdas: typing.Optional[typing.Sequence[builtins.str]] = None,
    sources: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f70f0ae94a9fde6797e913880422b1a54421e28f5dad8349deebbf8e61117baf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e62c20d94a9f76a7955c2c00c76b00c6b1238ebf5632a02eae340000f42369(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40fdd9eaf272408e82f06c1120a3a2382a03c9750178f8ad187ebf7d049e720e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cb9dae77d955f4de34348bc75d0144054bf966ce893a561bec87a3cd3c6faf9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountLogsConfigLambdaForwarder]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec5c2f38e338b8ffdbac74b7de1132fbe01257241e4800030c65364a79f5ee1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__546b36a133955ad3b9bb494d64b5960e7ddc5fa13b19e7facb5e8bd420bd7aaf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountLogsConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3755f11f62852da42d8b80325f3029517c61e410ef0ae892c9650f35700938(
    *,
    automute_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    collect_cloudwatch_alarms: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    collect_custom_metrics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    namespace_filters: typing.Optional[typing.Union[IntegrationAwsAccountMetricsConfigNamespaceFilters, typing.Dict[builtins.str, typing.Any]]] = None,
    tag_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationAwsAccountMetricsConfigTagFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e284be53f1b4a8befee78c5a290174aa133053282a58c837dadbc2403938cf63(
    *,
    exclude_only: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_only: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00a42c3ab69ed62a9c223b7e99ff4f7dc99a52c5a19c4f40578d8f051c53d258(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edeafd10fa4dd699d06b05f53f6852f4065bca0d2ea5b4bcf757831526d26ec6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54496068acc6f1fea0df733c20cf7987ab00f574b9245eb7d8818df71339069e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f69004b0bc42d44c3bdbc68d963ceab4a696b00bd1abed59d5042f6087ae8947(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountMetricsConfigNamespaceFilters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26960653ee389067d4ab9bf2d54ff8520a8a1aaab5685a703fb3bc4e263780f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae19542728d9cb9085e0d61362c93f2b0c3cefbeadeadbed7766473e1a535eff(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationAwsAccountMetricsConfigTagFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58240c3e92cad23930d727f2ad32df758b1b86b7aca575d43adfa372bfd9721(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2711cd7145467bc5cb682df6901ab112aa945c6d4be2730e632053f680416c4d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ed1e8e3dc1408eb9dc816083aca02ab21915f5e9585bbc9d157e0cd477640f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__097f4b463f35fa9fb70b833f3955ff9d7972c5b5c1ee81b18fdd335b89d391d4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a3fbf9bf74a7c2d39c50f75282f252814afdb1f7bda8f16da252b1355ad660(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountMetricsConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__026a54da580ae94914a09169cc207d9f136925663dc3fa2e9c98ce86557a7182(
    *,
    namespace: builtins.str,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e76d2d8628768c98832cfb3dc06a68eacbb4c1eaf8d2f8ced2844d637675d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1a337055c8e5cb9e58d3d8f85f6fac09017a4edb2013693aad400db16013dd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1165217240d9982dc61341269b8d60ac5d7d71a0a124006cd5df3fcf56551aa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806efd57ec799f2df867ccb7040e60cc702ef547e16cea9cfe95e8054ebdbf89(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b310d6d098c0aa08bdaa5ef1fff6643243e68a3d287536daf77b54ec90cca207(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7543f12b4e1aab974782abf3cb9dae9d353840de9f3b3531f634aaece5d905a6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationAwsAccountMetricsConfigTagFilters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dad3dc3eb2324d50ad1033a5d992e7cf2e168f8f75348373810793c585e33664(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83b22d3d1be4698c1eb9e102770038e820e39d2f0e680525c69a26788db50d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da426ee51f2955044acdb696201cb795f40b41b4c9d6d103fb4a5dd49dc8d50e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__566e7adf57c004cca54c6e77e6b9e7a0412efcda52411de5ad94765ab5e95913(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountMetricsConfigTagFilters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b856d8bb78fb3ef8469b2b5aa1aadd0e08321fc05a3afd35e6c7e85d1497f7d(
    *,
    cloud_security_posture_management_collection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    extended_collection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d9eab0e555b96077e6abe52ff05b61677ca29077b38798fbb657668def6798(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15df3f57c40713b36ae378762fd16519b2968cb7bfc36be35b154bb71a2a275e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc62e3afb40739ecab3c3b528549fbee44eee21a34356bf7d6fb776e4f0d8cd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0011c741b8840214f285d7d040877f53433bce84089c3625e2f929f84c61f0f2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountResourcesConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c519297662c2190142196f1d6d0e24b17175f6aa5f8154b7fa1fa6a6d8882fc8(
    *,
    xray_services: typing.Optional[typing.Union[IntegrationAwsAccountTracesConfigXrayServices, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81373bac28b871d35bb950c2fdbe9311985bea5fcb5ec2c143718bcef05faa55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f71d1901e2eb511a77915fbe9b9fa951e5b27b5f2b6cc2d723edb307ef3424(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountTracesConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0694af8f33001e26147e2dcc1438d2ce9960a015c3e8cd6dc49879b8cfff194(
    *,
    include_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_only: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b72dc9571b19c4181e2e0a1258660cb461d3cbc1aae21d17264243d7ecef341c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7fff512f0955d9a6f7b0b876e2dd76c85d80cf9a262c2d3b3d1644da64d2a89(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bca101bf8d35d8c9c3ce1a3feade0332595c286e83aa9bad0d4c0792fa0c105(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea7edbff26e5fa54ed9c1ff532ee15bad85e5f2153d52c9738a90a561b326ff6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationAwsAccountTracesConfigXrayServices]],
) -> None:
    """Type checking stubs"""
    pass
