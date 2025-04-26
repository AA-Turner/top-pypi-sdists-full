r'''
# `datadog_integration_aws`

Refer to the Terraform Registry for docs: [`datadog_integration_aws`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws).
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


class IntegrationAws(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.integrationAws.IntegrationAws",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws datadog_integration_aws}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        access_key_id: typing.Optional[builtins.str] = None,
        account_id: typing.Optional[builtins.str] = None,
        account_specific_namespace_rules: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]] = None,
        cspm_resource_collection_enabled: typing.Optional[builtins.str] = None,
        excluded_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        extended_resource_collection_enabled: typing.Optional[builtins.str] = None,
        filter_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        host_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        metrics_collection_enabled: typing.Optional[builtins.str] = None,
        resource_collection_enabled: typing.Optional[builtins.str] = None,
        role_name: typing.Optional[builtins.str] = None,
        secret_access_key: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws datadog_integration_aws} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param access_key_id: Your AWS access key ID. Only required if your AWS account is a GovCloud or China account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#access_key_id IntegrationAws#access_key_id}
        :param account_id: Your AWS Account ID without dashes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#account_id IntegrationAws#account_id}
        :param account_specific_namespace_rules: Enables or disables metric collection for specific AWS namespaces for this AWS account only. A list of namespaces can be found at the `available namespace rules API endpoint <https://docs.datadoghq.com/api/v1/aws-integration/#list-namespace-rules>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#account_specific_namespace_rules IntegrationAws#account_specific_namespace_rules}
        :param cspm_resource_collection_enabled: Whether Datadog collects cloud security posture management resources from your AWS account. This includes additional resources not covered under the general resource_collection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#cspm_resource_collection_enabled IntegrationAws#cspm_resource_collection_enabled}
        :param excluded_regions: An array of AWS regions to exclude from metrics collection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#excluded_regions IntegrationAws#excluded_regions}
        :param extended_resource_collection_enabled: Whether Datadog collects additional attributes and configuration information about the resources in your AWS account. Required for ``cspm_resource_collection_enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#extended_resource_collection_enabled IntegrationAws#extended_resource_collection_enabled}
        :param filter_tags: Array of EC2 tags (in the form ``key:value``) defines a filter that Datadog uses when collecting metrics from EC2. Wildcards, such as ``?`` (for single characters) and ``*`` (for multiple characters) can also be used. Only hosts that match one of the defined tags will be imported into Datadog. The rest will be ignored. Host matching a given tag can also be excluded by adding ``!`` before the tag. e.x. ``env:production,instance-type:c1.*,!region:us-east-1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#filter_tags IntegrationAws#filter_tags}
        :param host_tags: Array of tags (in the form ``key:value``) to add to all hosts and metrics reporting through this integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#host_tags IntegrationAws#host_tags}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#id IntegrationAws#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metrics_collection_enabled: Whether Datadog collects metrics for this AWS account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#metrics_collection_enabled IntegrationAws#metrics_collection_enabled}
        :param resource_collection_enabled: Whether Datadog collects a standard set of resources from your AWS account. **Deprecated.** Deprecated in favor of ``extended_resource_collection_enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#resource_collection_enabled IntegrationAws#resource_collection_enabled}
        :param role_name: Your Datadog role delegation name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#role_name IntegrationAws#role_name}
        :param secret_access_key: Your AWS secret access key. Only required if your AWS account is a GovCloud or China account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#secret_access_key IntegrationAws#secret_access_key}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a617f0a32936a69c8f25c2eabdad2705c450da76d119c0bcd25dbaeaa36b81e6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IntegrationAwsConfig(
            access_key_id=access_key_id,
            account_id=account_id,
            account_specific_namespace_rules=account_specific_namespace_rules,
            cspm_resource_collection_enabled=cspm_resource_collection_enabled,
            excluded_regions=excluded_regions,
            extended_resource_collection_enabled=extended_resource_collection_enabled,
            filter_tags=filter_tags,
            host_tags=host_tags,
            id=id,
            metrics_collection_enabled=metrics_collection_enabled,
            resource_collection_enabled=resource_collection_enabled,
            role_name=role_name,
            secret_access_key=secret_access_key,
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
        '''Generates CDKTF code for importing a IntegrationAws resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IntegrationAws to import.
        :param import_from_id: The id of the existing IntegrationAws that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IntegrationAws to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3416177ccd4521f5e456208b7b129017e471c701aabed8f44a01950ef012c7ef)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAccessKeyId")
    def reset_access_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessKeyId", []))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetAccountSpecificNamespaceRules")
    def reset_account_specific_namespace_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountSpecificNamespaceRules", []))

    @jsii.member(jsii_name="resetCspmResourceCollectionEnabled")
    def reset_cspm_resource_collection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCspmResourceCollectionEnabled", []))

    @jsii.member(jsii_name="resetExcludedRegions")
    def reset_excluded_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedRegions", []))

    @jsii.member(jsii_name="resetExtendedResourceCollectionEnabled")
    def reset_extended_resource_collection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtendedResourceCollectionEnabled", []))

    @jsii.member(jsii_name="resetFilterTags")
    def reset_filter_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterTags", []))

    @jsii.member(jsii_name="resetHostTags")
    def reset_host_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostTags", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMetricsCollectionEnabled")
    def reset_metrics_collection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsCollectionEnabled", []))

    @jsii.member(jsii_name="resetResourceCollectionEnabled")
    def reset_resource_collection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceCollectionEnabled", []))

    @jsii.member(jsii_name="resetRoleName")
    def reset_role_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoleName", []))

    @jsii.member(jsii_name="resetSecretAccessKey")
    def reset_secret_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretAccessKey", []))

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
    @jsii.member(jsii_name="externalId")
    def external_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalId"))

    @builtins.property
    @jsii.member(jsii_name="accessKeyIdInput")
    def access_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accountSpecificNamespaceRulesInput")
    def account_specific_namespace_rules_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]], jsii.get(self, "accountSpecificNamespaceRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="cspmResourceCollectionEnabledInput")
    def cspm_resource_collection_enabled_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cspmResourceCollectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedRegionsInput")
    def excluded_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="extendedResourceCollectionEnabledInput")
    def extended_resource_collection_enabled_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "extendedResourceCollectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="filterTagsInput")
    def filter_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "filterTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="hostTagsInput")
    def host_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "hostTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsCollectionEnabledInput")
    def metrics_collection_enabled_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricsCollectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceCollectionEnabledInput")
    def resource_collection_enabled_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceCollectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="roleNameInput")
    def role_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleNameInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6f6dcb85f3075e33c73fb58cefa27e73abea81789bb70b7922559f826fc46f5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b39f406e0cdb694edff5b8c2ebffb7498b8db4c866a7cd0faeba4c15c64fd5e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accountSpecificNamespaceRules")
    def account_specific_namespace_rules(
        self,
    ) -> typing.Mapping[builtins.str, typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Mapping[builtins.str, typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "accountSpecificNamespaceRules"))

    @account_specific_namespace_rules.setter
    def account_specific_namespace_rules(
        self,
        value: typing.Mapping[builtins.str, typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87244a4ad3e495aabbe1d9fe69c66109cf8661c3b66dae559eda98c0b67973b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountSpecificNamespaceRules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cspmResourceCollectionEnabled")
    def cspm_resource_collection_enabled(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cspmResourceCollectionEnabled"))

    @cspm_resource_collection_enabled.setter
    def cspm_resource_collection_enabled(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5bd2fd03628563973b946001200160fb7aa336fa97000411c013e70d314ccee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cspmResourceCollectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedRegions")
    def excluded_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedRegions"))

    @excluded_regions.setter
    def excluded_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92be2de9e75c851f484a77a005d4873a2c565cd19cb6879fea74775ae5536549)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extendedResourceCollectionEnabled")
    def extended_resource_collection_enabled(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "extendedResourceCollectionEnabled"))

    @extended_resource_collection_enabled.setter
    def extended_resource_collection_enabled(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a034b6ddfb9672d29c97fb5a134caa2ff1195c2319a8ed581740631eba72083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendedResourceCollectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterTags")
    def filter_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "filterTags"))

    @filter_tags.setter
    def filter_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba835a33f1323682fff000a96e365930c7827325b110b758b52901eb0f8ca1d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostTags")
    def host_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hostTags"))

    @host_tags.setter
    def host_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2339dd2dbde1fc371deb5852019ea169da2f10ec9649f16554ab13cd3b18d183)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52dcd679d6d7bc49e7e79c4c97841cf4d1ebd1c8eeb211549fb1ea9a52629a82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsCollectionEnabled")
    def metrics_collection_enabled(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricsCollectionEnabled"))

    @metrics_collection_enabled.setter
    def metrics_collection_enabled(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10bb9a15a622a5771ed22a2ada2285aaffc22074da649d9b9ae979530f95bb43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsCollectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceCollectionEnabled")
    def resource_collection_enabled(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceCollectionEnabled"))

    @resource_collection_enabled.setter
    def resource_collection_enabled(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0df0651e2938dae9f329da9956313fb6f7acbff094153ee7174e95fc4c0579f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceCollectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleName"))

    @role_name.setter
    def role_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__942dc8ef8796ca36dbe9f21563c2bfb4876a5f9cdd3bce2ca5841ccd5ed3b55a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretAccessKey")
    def secret_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretAccessKey"))

    @secret_access_key.setter
    def secret_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1267b4b06d7174959f17dc21f5f2d80b372738e48bb392d98ee9190f96797c3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretAccessKey", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.integrationAws.IntegrationAwsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "access_key_id": "accessKeyId",
        "account_id": "accountId",
        "account_specific_namespace_rules": "accountSpecificNamespaceRules",
        "cspm_resource_collection_enabled": "cspmResourceCollectionEnabled",
        "excluded_regions": "excludedRegions",
        "extended_resource_collection_enabled": "extendedResourceCollectionEnabled",
        "filter_tags": "filterTags",
        "host_tags": "hostTags",
        "id": "id",
        "metrics_collection_enabled": "metricsCollectionEnabled",
        "resource_collection_enabled": "resourceCollectionEnabled",
        "role_name": "roleName",
        "secret_access_key": "secretAccessKey",
    },
)
class IntegrationAwsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        access_key_id: typing.Optional[builtins.str] = None,
        account_id: typing.Optional[builtins.str] = None,
        account_specific_namespace_rules: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]] = None,
        cspm_resource_collection_enabled: typing.Optional[builtins.str] = None,
        excluded_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        extended_resource_collection_enabled: typing.Optional[builtins.str] = None,
        filter_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        host_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        metrics_collection_enabled: typing.Optional[builtins.str] = None,
        resource_collection_enabled: typing.Optional[builtins.str] = None,
        role_name: typing.Optional[builtins.str] = None,
        secret_access_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param access_key_id: Your AWS access key ID. Only required if your AWS account is a GovCloud or China account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#access_key_id IntegrationAws#access_key_id}
        :param account_id: Your AWS Account ID without dashes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#account_id IntegrationAws#account_id}
        :param account_specific_namespace_rules: Enables or disables metric collection for specific AWS namespaces for this AWS account only. A list of namespaces can be found at the `available namespace rules API endpoint <https://docs.datadoghq.com/api/v1/aws-integration/#list-namespace-rules>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#account_specific_namespace_rules IntegrationAws#account_specific_namespace_rules}
        :param cspm_resource_collection_enabled: Whether Datadog collects cloud security posture management resources from your AWS account. This includes additional resources not covered under the general resource_collection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#cspm_resource_collection_enabled IntegrationAws#cspm_resource_collection_enabled}
        :param excluded_regions: An array of AWS regions to exclude from metrics collection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#excluded_regions IntegrationAws#excluded_regions}
        :param extended_resource_collection_enabled: Whether Datadog collects additional attributes and configuration information about the resources in your AWS account. Required for ``cspm_resource_collection_enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#extended_resource_collection_enabled IntegrationAws#extended_resource_collection_enabled}
        :param filter_tags: Array of EC2 tags (in the form ``key:value``) defines a filter that Datadog uses when collecting metrics from EC2. Wildcards, such as ``?`` (for single characters) and ``*`` (for multiple characters) can also be used. Only hosts that match one of the defined tags will be imported into Datadog. The rest will be ignored. Host matching a given tag can also be excluded by adding ``!`` before the tag. e.x. ``env:production,instance-type:c1.*,!region:us-east-1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#filter_tags IntegrationAws#filter_tags}
        :param host_tags: Array of tags (in the form ``key:value``) to add to all hosts and metrics reporting through this integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#host_tags IntegrationAws#host_tags}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#id IntegrationAws#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param metrics_collection_enabled: Whether Datadog collects metrics for this AWS account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#metrics_collection_enabled IntegrationAws#metrics_collection_enabled}
        :param resource_collection_enabled: Whether Datadog collects a standard set of resources from your AWS account. **Deprecated.** Deprecated in favor of ``extended_resource_collection_enabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#resource_collection_enabled IntegrationAws#resource_collection_enabled}
        :param role_name: Your Datadog role delegation name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#role_name IntegrationAws#role_name}
        :param secret_access_key: Your AWS secret access key. Only required if your AWS account is a GovCloud or China account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#secret_access_key IntegrationAws#secret_access_key}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a54f9a704634a5e7bb08ff9e57ca0ee42044f3b072b0b81f14052ea53af98d46)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument account_specific_namespace_rules", value=account_specific_namespace_rules, expected_type=type_hints["account_specific_namespace_rules"])
            check_type(argname="argument cspm_resource_collection_enabled", value=cspm_resource_collection_enabled, expected_type=type_hints["cspm_resource_collection_enabled"])
            check_type(argname="argument excluded_regions", value=excluded_regions, expected_type=type_hints["excluded_regions"])
            check_type(argname="argument extended_resource_collection_enabled", value=extended_resource_collection_enabled, expected_type=type_hints["extended_resource_collection_enabled"])
            check_type(argname="argument filter_tags", value=filter_tags, expected_type=type_hints["filter_tags"])
            check_type(argname="argument host_tags", value=host_tags, expected_type=type_hints["host_tags"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument metrics_collection_enabled", value=metrics_collection_enabled, expected_type=type_hints["metrics_collection_enabled"])
            check_type(argname="argument resource_collection_enabled", value=resource_collection_enabled, expected_type=type_hints["resource_collection_enabled"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
            check_type(argname="argument secret_access_key", value=secret_access_key, expected_type=type_hints["secret_access_key"])
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
        if access_key_id is not None:
            self._values["access_key_id"] = access_key_id
        if account_id is not None:
            self._values["account_id"] = account_id
        if account_specific_namespace_rules is not None:
            self._values["account_specific_namespace_rules"] = account_specific_namespace_rules
        if cspm_resource_collection_enabled is not None:
            self._values["cspm_resource_collection_enabled"] = cspm_resource_collection_enabled
        if excluded_regions is not None:
            self._values["excluded_regions"] = excluded_regions
        if extended_resource_collection_enabled is not None:
            self._values["extended_resource_collection_enabled"] = extended_resource_collection_enabled
        if filter_tags is not None:
            self._values["filter_tags"] = filter_tags
        if host_tags is not None:
            self._values["host_tags"] = host_tags
        if id is not None:
            self._values["id"] = id
        if metrics_collection_enabled is not None:
            self._values["metrics_collection_enabled"] = metrics_collection_enabled
        if resource_collection_enabled is not None:
            self._values["resource_collection_enabled"] = resource_collection_enabled
        if role_name is not None:
            self._values["role_name"] = role_name
        if secret_access_key is not None:
            self._values["secret_access_key"] = secret_access_key

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
    def access_key_id(self) -> typing.Optional[builtins.str]:
        '''Your AWS access key ID. Only required if your AWS account is a GovCloud or China account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#access_key_id IntegrationAws#access_key_id}
        '''
        result = self._values.get("access_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''Your AWS Account ID without dashes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#account_id IntegrationAws#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def account_specific_namespace_rules(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]]:
        '''Enables or disables metric collection for specific AWS namespaces for this AWS account only.

        A list of namespaces can be found at the `available namespace rules API endpoint <https://docs.datadoghq.com/api/v1/aws-integration/#list-namespace-rules>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#account_specific_namespace_rules IntegrationAws#account_specific_namespace_rules}
        '''
        result = self._values.get("account_specific_namespace_rules")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]], result)

    @builtins.property
    def cspm_resource_collection_enabled(self) -> typing.Optional[builtins.str]:
        '''Whether Datadog collects cloud security posture management resources from your AWS account.

        This includes additional resources not covered under the general resource_collection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#cspm_resource_collection_enabled IntegrationAws#cspm_resource_collection_enabled}
        '''
        result = self._values.get("cspm_resource_collection_enabled")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def excluded_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of AWS regions to exclude from metrics collection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#excluded_regions IntegrationAws#excluded_regions}
        '''
        result = self._values.get("excluded_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def extended_resource_collection_enabled(self) -> typing.Optional[builtins.str]:
        '''Whether Datadog collects additional attributes and configuration information about the resources in your AWS account. Required for ``cspm_resource_collection_enabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#extended_resource_collection_enabled IntegrationAws#extended_resource_collection_enabled}
        '''
        result = self._values.get("extended_resource_collection_enabled")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Array of EC2 tags (in the form ``key:value``) defines a filter that Datadog uses when collecting metrics from EC2.

        Wildcards, such as ``?`` (for single characters) and ``*`` (for multiple characters) can also be used. Only hosts that match one of the defined tags will be imported into Datadog. The rest will be ignored. Host matching a given tag can also be excluded by adding ``!`` before the tag. e.x. ``env:production,instance-type:c1.*,!region:us-east-1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#filter_tags IntegrationAws#filter_tags}
        '''
        result = self._values.get("filter_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def host_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Array of tags (in the form ``key:value``) to add to all hosts and metrics reporting through this integration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#host_tags IntegrationAws#host_tags}
        '''
        result = self._values.get("host_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#id IntegrationAws#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metrics_collection_enabled(self) -> typing.Optional[builtins.str]:
        '''Whether Datadog collects metrics for this AWS account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#metrics_collection_enabled IntegrationAws#metrics_collection_enabled}
        '''
        result = self._values.get("metrics_collection_enabled")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_collection_enabled(self) -> typing.Optional[builtins.str]:
        '''Whether Datadog collects a standard set of resources from your AWS account. **Deprecated.** Deprecated in favor of ``extended_resource_collection_enabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#resource_collection_enabled IntegrationAws#resource_collection_enabled}
        '''
        result = self._values.get("resource_collection_enabled")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''Your Datadog role delegation name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#role_name IntegrationAws#role_name}
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_access_key(self) -> typing.Optional[builtins.str]:
        '''Your AWS secret access key. Only required if your AWS account is a GovCloud or China account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_aws#secret_access_key IntegrationAws#secret_access_key}
        '''
        result = self._values.get("secret_access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationAwsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IntegrationAws",
    "IntegrationAwsConfig",
]

publication.publish()

def _typecheckingstub__a617f0a32936a69c8f25c2eabdad2705c450da76d119c0bcd25dbaeaa36b81e6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    access_key_id: typing.Optional[builtins.str] = None,
    account_id: typing.Optional[builtins.str] = None,
    account_specific_namespace_rules: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]] = None,
    cspm_resource_collection_enabled: typing.Optional[builtins.str] = None,
    excluded_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    extended_resource_collection_enabled: typing.Optional[builtins.str] = None,
    filter_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    host_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    metrics_collection_enabled: typing.Optional[builtins.str] = None,
    resource_collection_enabled: typing.Optional[builtins.str] = None,
    role_name: typing.Optional[builtins.str] = None,
    secret_access_key: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__3416177ccd4521f5e456208b7b129017e471c701aabed8f44a01950ef012c7ef(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f6dcb85f3075e33c73fb58cefa27e73abea81789bb70b7922559f826fc46f5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39f406e0cdb694edff5b8c2ebffb7498b8db4c866a7cd0faeba4c15c64fd5e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87244a4ad3e495aabbe1d9fe69c66109cf8661c3b66dae559eda98c0b67973b0(
    value: typing.Mapping[builtins.str, typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5bd2fd03628563973b946001200160fb7aa336fa97000411c013e70d314ccee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92be2de9e75c851f484a77a005d4873a2c565cd19cb6879fea74775ae5536549(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a034b6ddfb9672d29c97fb5a134caa2ff1195c2319a8ed581740631eba72083(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba835a33f1323682fff000a96e365930c7827325b110b758b52901eb0f8ca1d6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2339dd2dbde1fc371deb5852019ea169da2f10ec9649f16554ab13cd3b18d183(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52dcd679d6d7bc49e7e79c4c97841cf4d1ebd1c8eeb211549fb1ea9a52629a82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10bb9a15a622a5771ed22a2ada2285aaffc22074da649d9b9ae979530f95bb43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0df0651e2938dae9f329da9956313fb6f7acbff094153ee7174e95fc4c0579f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__942dc8ef8796ca36dbe9f21563c2bfb4876a5f9cdd3bce2ca5841ccd5ed3b55a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1267b4b06d7174959f17dc21f5f2d80b372738e48bb392d98ee9190f96797c3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54f9a704634a5e7bb08ff9e57ca0ee42044f3b072b0b81f14052ea53af98d46(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    access_key_id: typing.Optional[builtins.str] = None,
    account_id: typing.Optional[builtins.str] = None,
    account_specific_namespace_rules: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]] = None,
    cspm_resource_collection_enabled: typing.Optional[builtins.str] = None,
    excluded_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    extended_resource_collection_enabled: typing.Optional[builtins.str] = None,
    filter_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    host_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    metrics_collection_enabled: typing.Optional[builtins.str] = None,
    resource_collection_enabled: typing.Optional[builtins.str] = None,
    role_name: typing.Optional[builtins.str] = None,
    secret_access_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
