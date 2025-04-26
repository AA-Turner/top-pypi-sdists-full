r'''
# `datadog_integration_gcp_sts`

Refer to the Terraform Registry for docs: [`datadog_integration_gcp_sts`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts).
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


class IntegrationGcpSts(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.integrationGcpSts.IntegrationGcpSts",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts datadog_integration_gcp_sts}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        client_email: builtins.str,
        account_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        automute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cloud_run_revision_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
        host_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
        is_cspm_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_resource_change_collection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_security_command_center_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metric_namespace_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationGcpStsMetricNamespaceConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_collection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts datadog_integration_gcp_sts} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param client_email: Your service account email address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#client_email IntegrationGcpSts#client_email}
        :param account_tags: Tags to be associated with GCP metrics and service checks from your account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#account_tags IntegrationGcpSts#account_tags}
        :param automute: Silence monitors for expected GCE instance shutdowns. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#automute IntegrationGcpSts#automute}
        :param cloud_run_revision_filters: Tags to filter which Cloud Run revisions are imported into Datadog. Only revisions that meet specified criteria are monitored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#cloud_run_revision_filters IntegrationGcpSts#cloud_run_revision_filters}
        :param host_filters: Your Host Filters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#host_filters IntegrationGcpSts#host_filters}
        :param is_cspm_enabled: Whether Datadog collects cloud security posture management resources from your GCP project. If enabled, requires ``resource_collection_enabled`` to also be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#is_cspm_enabled IntegrationGcpSts#is_cspm_enabled}
        :param is_resource_change_collection_enabled: When enabled, Datadog scans for all resource change data in your Google Cloud environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#is_resource_change_collection_enabled IntegrationGcpSts#is_resource_change_collection_enabled}
        :param is_security_command_center_enabled: When enabled, Datadog will attempt to collect Security Command Center Findings. Note: This requires additional permissions on the service account. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#is_security_command_center_enabled IntegrationGcpSts#is_security_command_center_enabled}
        :param metric_namespace_configs: Configuration for a GCP metric namespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#metric_namespace_configs IntegrationGcpSts#metric_namespace_configs}
        :param resource_collection_enabled: When enabled, Datadog scans for all resources in your GCP environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#resource_collection_enabled IntegrationGcpSts#resource_collection_enabled}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c84867de42e3fa7da3b4d8f5f78c139a5e41ee55b2c9a2be7c8182f563abc4da)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = IntegrationGcpStsConfig(
            client_email=client_email,
            account_tags=account_tags,
            automute=automute,
            cloud_run_revision_filters=cloud_run_revision_filters,
            host_filters=host_filters,
            is_cspm_enabled=is_cspm_enabled,
            is_resource_change_collection_enabled=is_resource_change_collection_enabled,
            is_security_command_center_enabled=is_security_command_center_enabled,
            metric_namespace_configs=metric_namespace_configs,
            resource_collection_enabled=resource_collection_enabled,
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
        '''Generates CDKTF code for importing a IntegrationGcpSts resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IntegrationGcpSts to import.
        :param import_from_id: The id of the existing IntegrationGcpSts that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IntegrationGcpSts to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee3060a3e8684bb11742f8a1ad06ae355ab15ea0ca49195e0c77b66ba959230)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMetricNamespaceConfigs")
    def put_metric_namespace_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationGcpStsMetricNamespaceConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29d44c84b23c18e0b0c673e1e5f4d9991f79d99e2d33478d12a4f88f56456948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetricNamespaceConfigs", [value]))

    @jsii.member(jsii_name="resetAccountTags")
    def reset_account_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountTags", []))

    @jsii.member(jsii_name="resetAutomute")
    def reset_automute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomute", []))

    @jsii.member(jsii_name="resetCloudRunRevisionFilters")
    def reset_cloud_run_revision_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudRunRevisionFilters", []))

    @jsii.member(jsii_name="resetHostFilters")
    def reset_host_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostFilters", []))

    @jsii.member(jsii_name="resetIsCspmEnabled")
    def reset_is_cspm_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsCspmEnabled", []))

    @jsii.member(jsii_name="resetIsResourceChangeCollectionEnabled")
    def reset_is_resource_change_collection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsResourceChangeCollectionEnabled", []))

    @jsii.member(jsii_name="resetIsSecurityCommandCenterEnabled")
    def reset_is_security_command_center_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsSecurityCommandCenterEnabled", []))

    @jsii.member(jsii_name="resetMetricNamespaceConfigs")
    def reset_metric_namespace_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricNamespaceConfigs", []))

    @jsii.member(jsii_name="resetResourceCollectionEnabled")
    def reset_resource_collection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceCollectionEnabled", []))

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
    @jsii.member(jsii_name="delegateAccountEmail")
    def delegate_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delegateAccountEmail"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="metricNamespaceConfigs")
    def metric_namespace_configs(self) -> "IntegrationGcpStsMetricNamespaceConfigsList":
        return typing.cast("IntegrationGcpStsMetricNamespaceConfigsList", jsii.get(self, "metricNamespaceConfigs"))

    @builtins.property
    @jsii.member(jsii_name="accountTagsInput")
    def account_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accountTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="automuteInput")
    def automute_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "automuteInput"))

    @builtins.property
    @jsii.member(jsii_name="clientEmailInput")
    def client_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudRunRevisionFiltersInput")
    def cloud_run_revision_filters_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cloudRunRevisionFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="hostFiltersInput")
    def host_filters_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "hostFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="isCspmEnabledInput")
    def is_cspm_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isCspmEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isResourceChangeCollectionEnabledInput")
    def is_resource_change_collection_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isResourceChangeCollectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isSecurityCommandCenterEnabledInput")
    def is_security_command_center_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isSecurityCommandCenterEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="metricNamespaceConfigsInput")
    def metric_namespace_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationGcpStsMetricNamespaceConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationGcpStsMetricNamespaceConfigs"]]], jsii.get(self, "metricNamespaceConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceCollectionEnabledInput")
    def resource_collection_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "resourceCollectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="accountTags")
    def account_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accountTags"))

    @account_tags.setter
    def account_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__357c8ee4107d1b3cb77bc620352d1e197ae23b25682ab2e03d6bc0b5dff51097)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="automute")
    def automute(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "automute"))

    @automute.setter
    def automute(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27a8f9a944a51365a1dd2ce19c81c35529fbd678fc8cf8cc8ec0273414a9633a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientEmail")
    def client_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientEmail"))

    @client_email.setter
    def client_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12c21dc8acdfb06b23bac0e0fedb5aea82e4579b2ef99b4733f39a5f5191c818)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudRunRevisionFilters")
    def cloud_run_revision_filters(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cloudRunRevisionFilters"))

    @cloud_run_revision_filters.setter
    def cloud_run_revision_filters(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9383909133aaa2c5ae18ca18293c41d30b27765bee59667cd2e243e726d85e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudRunRevisionFilters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostFilters")
    def host_filters(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hostFilters"))

    @host_filters.setter
    def host_filters(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcad0f772d194d3fc8ee59bb6180a20b17c096433e6294220f4d23eda3682de9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostFilters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isCspmEnabled")
    def is_cspm_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isCspmEnabled"))

    @is_cspm_enabled.setter
    def is_cspm_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22c0becf70fda5f78813b575856ad7fec76c001aeb5f7e26586b7d2c8402b03c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isCspmEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isResourceChangeCollectionEnabled")
    def is_resource_change_collection_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isResourceChangeCollectionEnabled"))

    @is_resource_change_collection_enabled.setter
    def is_resource_change_collection_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__180fdb211813b8cbf93b3a5ee5d6635dc791187cba96d3fb48cfc7b1662d69d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isResourceChangeCollectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isSecurityCommandCenterEnabled")
    def is_security_command_center_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isSecurityCommandCenterEnabled"))

    @is_security_command_center_enabled.setter
    def is_security_command_center_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e40d49893059132a75398ab7fe573292b213de1a0ef8e31c26cb2de3ab2f97b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSecurityCommandCenterEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceCollectionEnabled")
    def resource_collection_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "resourceCollectionEnabled"))

    @resource_collection_enabled.setter
    def resource_collection_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fee374c6b5764e388878170c7cac3bff30a8c964e091047f5dd3b28a55c110cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceCollectionEnabled", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.integrationGcpSts.IntegrationGcpStsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "client_email": "clientEmail",
        "account_tags": "accountTags",
        "automute": "automute",
        "cloud_run_revision_filters": "cloudRunRevisionFilters",
        "host_filters": "hostFilters",
        "is_cspm_enabled": "isCspmEnabled",
        "is_resource_change_collection_enabled": "isResourceChangeCollectionEnabled",
        "is_security_command_center_enabled": "isSecurityCommandCenterEnabled",
        "metric_namespace_configs": "metricNamespaceConfigs",
        "resource_collection_enabled": "resourceCollectionEnabled",
    },
)
class IntegrationGcpStsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        client_email: builtins.str,
        account_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        automute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cloud_run_revision_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
        host_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
        is_cspm_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_resource_change_collection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_security_command_center_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metric_namespace_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IntegrationGcpStsMetricNamespaceConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_collection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param client_email: Your service account email address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#client_email IntegrationGcpSts#client_email}
        :param account_tags: Tags to be associated with GCP metrics and service checks from your account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#account_tags IntegrationGcpSts#account_tags}
        :param automute: Silence monitors for expected GCE instance shutdowns. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#automute IntegrationGcpSts#automute}
        :param cloud_run_revision_filters: Tags to filter which Cloud Run revisions are imported into Datadog. Only revisions that meet specified criteria are monitored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#cloud_run_revision_filters IntegrationGcpSts#cloud_run_revision_filters}
        :param host_filters: Your Host Filters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#host_filters IntegrationGcpSts#host_filters}
        :param is_cspm_enabled: Whether Datadog collects cloud security posture management resources from your GCP project. If enabled, requires ``resource_collection_enabled`` to also be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#is_cspm_enabled IntegrationGcpSts#is_cspm_enabled}
        :param is_resource_change_collection_enabled: When enabled, Datadog scans for all resource change data in your Google Cloud environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#is_resource_change_collection_enabled IntegrationGcpSts#is_resource_change_collection_enabled}
        :param is_security_command_center_enabled: When enabled, Datadog will attempt to collect Security Command Center Findings. Note: This requires additional permissions on the service account. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#is_security_command_center_enabled IntegrationGcpSts#is_security_command_center_enabled}
        :param metric_namespace_configs: Configuration for a GCP metric namespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#metric_namespace_configs IntegrationGcpSts#metric_namespace_configs}
        :param resource_collection_enabled: When enabled, Datadog scans for all resources in your GCP environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#resource_collection_enabled IntegrationGcpSts#resource_collection_enabled}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa91227355a177c54847e7cb6b3524e1b745fc8a420062472100b328e10e8825)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument client_email", value=client_email, expected_type=type_hints["client_email"])
            check_type(argname="argument account_tags", value=account_tags, expected_type=type_hints["account_tags"])
            check_type(argname="argument automute", value=automute, expected_type=type_hints["automute"])
            check_type(argname="argument cloud_run_revision_filters", value=cloud_run_revision_filters, expected_type=type_hints["cloud_run_revision_filters"])
            check_type(argname="argument host_filters", value=host_filters, expected_type=type_hints["host_filters"])
            check_type(argname="argument is_cspm_enabled", value=is_cspm_enabled, expected_type=type_hints["is_cspm_enabled"])
            check_type(argname="argument is_resource_change_collection_enabled", value=is_resource_change_collection_enabled, expected_type=type_hints["is_resource_change_collection_enabled"])
            check_type(argname="argument is_security_command_center_enabled", value=is_security_command_center_enabled, expected_type=type_hints["is_security_command_center_enabled"])
            check_type(argname="argument metric_namespace_configs", value=metric_namespace_configs, expected_type=type_hints["metric_namespace_configs"])
            check_type(argname="argument resource_collection_enabled", value=resource_collection_enabled, expected_type=type_hints["resource_collection_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_email": client_email,
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
        if automute is not None:
            self._values["automute"] = automute
        if cloud_run_revision_filters is not None:
            self._values["cloud_run_revision_filters"] = cloud_run_revision_filters
        if host_filters is not None:
            self._values["host_filters"] = host_filters
        if is_cspm_enabled is not None:
            self._values["is_cspm_enabled"] = is_cspm_enabled
        if is_resource_change_collection_enabled is not None:
            self._values["is_resource_change_collection_enabled"] = is_resource_change_collection_enabled
        if is_security_command_center_enabled is not None:
            self._values["is_security_command_center_enabled"] = is_security_command_center_enabled
        if metric_namespace_configs is not None:
            self._values["metric_namespace_configs"] = metric_namespace_configs
        if resource_collection_enabled is not None:
            self._values["resource_collection_enabled"] = resource_collection_enabled

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
    def client_email(self) -> builtins.str:
        '''Your service account email address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#client_email IntegrationGcpSts#client_email}
        '''
        result = self._values.get("client_email")
        assert result is not None, "Required property 'client_email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags to be associated with GCP metrics and service checks from your account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#account_tags IntegrationGcpSts#account_tags}
        '''
        result = self._values.get("account_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def automute(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Silence monitors for expected GCE instance shutdowns.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#automute IntegrationGcpSts#automute}
        '''
        result = self._values.get("automute")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cloud_run_revision_filters(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags to filter which Cloud Run revisions are imported into Datadog. Only revisions that meet specified criteria are monitored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#cloud_run_revision_filters IntegrationGcpSts#cloud_run_revision_filters}
        '''
        result = self._values.get("cloud_run_revision_filters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def host_filters(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Your Host Filters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#host_filters IntegrationGcpSts#host_filters}
        '''
        result = self._values.get("host_filters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def is_cspm_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Datadog collects cloud security posture management resources from your GCP project.

        If enabled, requires ``resource_collection_enabled`` to also be enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#is_cspm_enabled IntegrationGcpSts#is_cspm_enabled}
        '''
        result = self._values.get("is_cspm_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_resource_change_collection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled, Datadog scans for all resource change data in your Google Cloud environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#is_resource_change_collection_enabled IntegrationGcpSts#is_resource_change_collection_enabled}
        '''
        result = self._values.get("is_resource_change_collection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_security_command_center_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled, Datadog will attempt to collect Security Command Center Findings.

        Note: This requires additional permissions on the service account. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#is_security_command_center_enabled IntegrationGcpSts#is_security_command_center_enabled}
        '''
        result = self._values.get("is_security_command_center_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metric_namespace_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationGcpStsMetricNamespaceConfigs"]]]:
        '''Configuration for a GCP metric namespace.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#metric_namespace_configs IntegrationGcpSts#metric_namespace_configs}
        '''
        result = self._values.get("metric_namespace_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IntegrationGcpStsMetricNamespaceConfigs"]]], result)

    @builtins.property
    def resource_collection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled, Datadog scans for all resources in your GCP environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#resource_collection_enabled IntegrationGcpSts#resource_collection_enabled}
        '''
        result = self._values.get("resource_collection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationGcpStsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.integrationGcpSts.IntegrationGcpStsMetricNamespaceConfigs",
    jsii_struct_bases=[],
    name_mapping={"disabled": "disabled", "id": "id"},
)
class IntegrationGcpStsMetricNamespaceConfigs:
    def __init__(
        self,
        *,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#disabled IntegrationGcpSts#disabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#id IntegrationGcpSts#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52e62b2ef8ed8a5c49a7fe48301a92873f89ecad65ce4a045cc7f61e1a18eaf9)
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disabled is not None:
            self._values["disabled"] = disabled
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#disabled IntegrationGcpSts#disabled}.'''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp_sts#id IntegrationGcpSts#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationGcpStsMetricNamespaceConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IntegrationGcpStsMetricNamespaceConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.integrationGcpSts.IntegrationGcpStsMetricNamespaceConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f35c7e0db7aebab8f0778b4f249b95b707c4230e1573e47505f3944bb5df440f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IntegrationGcpStsMetricNamespaceConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c3e5093f5900f0b9937de3d7a59f3b92b0695ce387ddc7f9406ef177178f0fd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IntegrationGcpStsMetricNamespaceConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85e3131768c4f0214384a5dd975cd39f896ee8052a52634dd82a1b08313fb1b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19f5c192b8fc0b4ab5092fb0af483cf5ff5f8bc760b2f943ac975ea81592e09c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d04c3cf96f68ab98419af7cd6df060bafabd0a41d8fac641f453b31c41913956)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationGcpStsMetricNamespaceConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationGcpStsMetricNamespaceConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationGcpStsMetricNamespaceConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aafe63a0bd09c3c6ef2bca87e286e389bb5b6668ca3dd2986344ec1ce00811f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IntegrationGcpStsMetricNamespaceConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.integrationGcpSts.IntegrationGcpStsMetricNamespaceConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a81d750bbf18fdedae9935b848e10a8c68dd9d830cbe35b7cc6ac2196ded13f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d69961b9b839cf3109bfcdaf210f89123874776e52f32535d8969b6a7a00efe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__debe80e20c5b99f202927e393164023a1722433dba244b093506ab2c836fe01c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationGcpStsMetricNamespaceConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationGcpStsMetricNamespaceConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationGcpStsMetricNamespaceConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c269b205ee2093a48fa04a03093b94ca5566d8cc36f0205590f5c190471fd572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "IntegrationGcpSts",
    "IntegrationGcpStsConfig",
    "IntegrationGcpStsMetricNamespaceConfigs",
    "IntegrationGcpStsMetricNamespaceConfigsList",
    "IntegrationGcpStsMetricNamespaceConfigsOutputReference",
]

publication.publish()

def _typecheckingstub__c84867de42e3fa7da3b4d8f5f78c139a5e41ee55b2c9a2be7c8182f563abc4da(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    client_email: builtins.str,
    account_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    automute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cloud_run_revision_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
    host_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
    is_cspm_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_resource_change_collection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_security_command_center_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metric_namespace_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationGcpStsMetricNamespaceConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resource_collection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__0ee3060a3e8684bb11742f8a1ad06ae355ab15ea0ca49195e0c77b66ba959230(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29d44c84b23c18e0b0c673e1e5f4d9991f79d99e2d33478d12a4f88f56456948(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationGcpStsMetricNamespaceConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__357c8ee4107d1b3cb77bc620352d1e197ae23b25682ab2e03d6bc0b5dff51097(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27a8f9a944a51365a1dd2ce19c81c35529fbd678fc8cf8cc8ec0273414a9633a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12c21dc8acdfb06b23bac0e0fedb5aea82e4579b2ef99b4733f39a5f5191c818(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9383909133aaa2c5ae18ca18293c41d30b27765bee59667cd2e243e726d85e9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcad0f772d194d3fc8ee59bb6180a20b17c096433e6294220f4d23eda3682de9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c0becf70fda5f78813b575856ad7fec76c001aeb5f7e26586b7d2c8402b03c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180fdb211813b8cbf93b3a5ee5d6635dc791187cba96d3fb48cfc7b1662d69d3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e40d49893059132a75398ab7fe573292b213de1a0ef8e31c26cb2de3ab2f97b2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fee374c6b5764e388878170c7cac3bff30a8c964e091047f5dd3b28a55c110cc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa91227355a177c54847e7cb6b3524e1b745fc8a420062472100b328e10e8825(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    client_email: builtins.str,
    account_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    automute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cloud_run_revision_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
    host_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
    is_cspm_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_resource_change_collection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_security_command_center_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metric_namespace_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IntegrationGcpStsMetricNamespaceConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resource_collection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52e62b2ef8ed8a5c49a7fe48301a92873f89ecad65ce4a045cc7f61e1a18eaf9(
    *,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f35c7e0db7aebab8f0778b4f249b95b707c4230e1573e47505f3944bb5df440f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c3e5093f5900f0b9937de3d7a59f3b92b0695ce387ddc7f9406ef177178f0fd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e3131768c4f0214384a5dd975cd39f896ee8052a52634dd82a1b08313fb1b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f5c192b8fc0b4ab5092fb0af483cf5ff5f8bc760b2f943ac975ea81592e09c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04c3cf96f68ab98419af7cd6df060bafabd0a41d8fac641f453b31c41913956(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aafe63a0bd09c3c6ef2bca87e286e389bb5b6668ca3dd2986344ec1ce00811f5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IntegrationGcpStsMetricNamespaceConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a81d750bbf18fdedae9935b848e10a8c68dd9d830cbe35b7cc6ac2196ded13f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d69961b9b839cf3109bfcdaf210f89123874776e52f32535d8969b6a7a00efe0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__debe80e20c5b99f202927e393164023a1722433dba244b093506ab2c836fe01c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c269b205ee2093a48fa04a03093b94ca5566d8cc36f0205590f5c190471fd572(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IntegrationGcpStsMetricNamespaceConfigs]],
) -> None:
    """Type checking stubs"""
    pass
