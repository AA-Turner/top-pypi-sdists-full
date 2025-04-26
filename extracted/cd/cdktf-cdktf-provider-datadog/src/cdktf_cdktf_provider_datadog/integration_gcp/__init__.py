r'''
# `datadog_integration_gcp`

Refer to the Terraform Registry for docs: [`datadog_integration_gcp`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp).
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


class IntegrationGcp(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.integrationGcp.IntegrationGcp",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp datadog_integration_gcp}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        client_email: builtins.str,
        client_id: builtins.str,
        private_key: builtins.str,
        private_key_id: builtins.str,
        project_id: builtins.str,
        automute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cloud_run_revision_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
        cspm_resource_collection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_filters: typing.Optional[builtins.str] = None,
        is_resource_change_collection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_security_command_center_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        resource_collection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp datadog_integration_gcp} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param client_email: Your email found in your JSON service account key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#client_email IntegrationGcp#client_email}
        :param client_id: Your ID found in your JSON service account key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#client_id IntegrationGcp#client_id}
        :param private_key: Your private key name found in your JSON service account key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#private_key IntegrationGcp#private_key}
        :param private_key_id: Your private key ID found in your JSON service account key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#private_key_id IntegrationGcp#private_key_id}
        :param project_id: Your Google Cloud project ID found in your JSON service account key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#project_id IntegrationGcp#project_id}
        :param automute: Silence monitors for expected GCE instance shutdowns. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#automute IntegrationGcp#automute}
        :param cloud_run_revision_filters: Tags to filter which Cloud Run revisions are imported into Datadog. Only revisions that meet specified criteria are monitored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#cloud_run_revision_filters IntegrationGcp#cloud_run_revision_filters}
        :param cspm_resource_collection_enabled: Whether Datadog collects cloud security posture management resources from your GCP project. If enabled, requires ``resource_collection_enabled`` to also be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#cspm_resource_collection_enabled IntegrationGcp#cspm_resource_collection_enabled}
        :param host_filters: Limit the GCE instances that are pulled into Datadog by using tags. Only hosts that match one of the defined tags are imported into Datadog. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#host_filters IntegrationGcp#host_filters}
        :param is_resource_change_collection_enabled: When enabled, Datadog scans for all resource change data in your Google Cloud environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#is_resource_change_collection_enabled IntegrationGcp#is_resource_change_collection_enabled}
        :param is_security_command_center_enabled: When enabled, Datadog will attempt to collect Security Command Center Findings. Note: This requires additional permissions on the service account. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#is_security_command_center_enabled IntegrationGcp#is_security_command_center_enabled}
        :param resource_collection_enabled: When enabled, Datadog scans for all resources in your GCP environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#resource_collection_enabled IntegrationGcp#resource_collection_enabled}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc57a1ea03daadb5d0c15ad30327ce20c06b6d8439b07dfc0fd9550612acb1c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = IntegrationGcpConfig(
            client_email=client_email,
            client_id=client_id,
            private_key=private_key,
            private_key_id=private_key_id,
            project_id=project_id,
            automute=automute,
            cloud_run_revision_filters=cloud_run_revision_filters,
            cspm_resource_collection_enabled=cspm_resource_collection_enabled,
            host_filters=host_filters,
            is_resource_change_collection_enabled=is_resource_change_collection_enabled,
            is_security_command_center_enabled=is_security_command_center_enabled,
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
        '''Generates CDKTF code for importing a IntegrationGcp resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IntegrationGcp to import.
        :param import_from_id: The id of the existing IntegrationGcp that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IntegrationGcp to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ef0f727583ce7c18a919113e96bdf464103f7ef6e830faf228800aeadaa6c86)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAutomute")
    def reset_automute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomute", []))

    @jsii.member(jsii_name="resetCloudRunRevisionFilters")
    def reset_cloud_run_revision_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudRunRevisionFilters", []))

    @jsii.member(jsii_name="resetCspmResourceCollectionEnabled")
    def reset_cspm_resource_collection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCspmResourceCollectionEnabled", []))

    @jsii.member(jsii_name="resetHostFilters")
    def reset_host_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostFilters", []))

    @jsii.member(jsii_name="resetIsResourceChangeCollectionEnabled")
    def reset_is_resource_change_collection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsResourceChangeCollectionEnabled", []))

    @jsii.member(jsii_name="resetIsSecurityCommandCenterEnabled")
    def reset_is_security_command_center_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsSecurityCommandCenterEnabled", []))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

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
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudRunRevisionFiltersInput")
    def cloud_run_revision_filters_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cloudRunRevisionFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="cspmResourceCollectionEnabledInput")
    def cspm_resource_collection_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cspmResourceCollectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="hostFiltersInput")
    def host_filters_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostFiltersInput"))

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
    @jsii.member(jsii_name="privateKeyIdInput")
    def private_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyInput")
    def private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceCollectionEnabledInput")
    def resource_collection_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "resourceCollectionEnabledInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a8257f23c7c2c57573d4401bb70e01ea9bd716bdf5356eb78f2950ec9bf88322)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientEmail")
    def client_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientEmail"))

    @client_email.setter
    def client_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36a08ce27a1da51f10ab9d254c903abf30c10e358fa6ef0d014a0eb896b0a5c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5a7f423973fc20a16dca6db9249d75ef86bd96652e07136649e33f42514f44a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudRunRevisionFilters")
    def cloud_run_revision_filters(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cloudRunRevisionFilters"))

    @cloud_run_revision_filters.setter
    def cloud_run_revision_filters(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6918bd10152acfbc9033a3df86b3abcd351abda960e76013944f1cdd08720bd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudRunRevisionFilters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cspmResourceCollectionEnabled")
    def cspm_resource_collection_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cspmResourceCollectionEnabled"))

    @cspm_resource_collection_enabled.setter
    def cspm_resource_collection_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bae2566e3372da23dc6317431717220a97c3dfac640307089efac92a141746c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cspmResourceCollectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostFilters")
    def host_filters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostFilters"))

    @host_filters.setter
    def host_filters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd5e5e4d87be44c43cb245177a8c96c308f5713604d367af5dcf611c517fd8b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostFilters", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__e3c10dae6c99d64772b3ea095817be752b863a3a93cfb3293b29895f04642b93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f40dcdd912aff7a31a1cc9f1dd9a76cd05faa707c7c6ff52bf95af5925cb9ad7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSecurityCommandCenterEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c3e68e0e148b0d384c1ec64eb001370a263c0aebee1af1c39f3945d28dfe69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKeyId")
    def private_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKeyId"))

    @private_key_id.setter
    def private_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d79991e30108bd85fb4b9b0aa93e84dc97904db0dd119b9bc0ca86080196b2b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb270052fca8af40b300fd2b5d39ceffd51e7313b208468e9c7d91f343714f16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__18b89ad036e3961ff9f43ffcd937ea868213ae6e364492d54e58e3b713751f4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceCollectionEnabled", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.integrationGcp.IntegrationGcpConfig",
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
        "client_id": "clientId",
        "private_key": "privateKey",
        "private_key_id": "privateKeyId",
        "project_id": "projectId",
        "automute": "automute",
        "cloud_run_revision_filters": "cloudRunRevisionFilters",
        "cspm_resource_collection_enabled": "cspmResourceCollectionEnabled",
        "host_filters": "hostFilters",
        "is_resource_change_collection_enabled": "isResourceChangeCollectionEnabled",
        "is_security_command_center_enabled": "isSecurityCommandCenterEnabled",
        "resource_collection_enabled": "resourceCollectionEnabled",
    },
)
class IntegrationGcpConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        client_id: builtins.str,
        private_key: builtins.str,
        private_key_id: builtins.str,
        project_id: builtins.str,
        automute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cloud_run_revision_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
        cspm_resource_collection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_filters: typing.Optional[builtins.str] = None,
        is_resource_change_collection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_security_command_center_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
        :param client_email: Your email found in your JSON service account key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#client_email IntegrationGcp#client_email}
        :param client_id: Your ID found in your JSON service account key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#client_id IntegrationGcp#client_id}
        :param private_key: Your private key name found in your JSON service account key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#private_key IntegrationGcp#private_key}
        :param private_key_id: Your private key ID found in your JSON service account key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#private_key_id IntegrationGcp#private_key_id}
        :param project_id: Your Google Cloud project ID found in your JSON service account key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#project_id IntegrationGcp#project_id}
        :param automute: Silence monitors for expected GCE instance shutdowns. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#automute IntegrationGcp#automute}
        :param cloud_run_revision_filters: Tags to filter which Cloud Run revisions are imported into Datadog. Only revisions that meet specified criteria are monitored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#cloud_run_revision_filters IntegrationGcp#cloud_run_revision_filters}
        :param cspm_resource_collection_enabled: Whether Datadog collects cloud security posture management resources from your GCP project. If enabled, requires ``resource_collection_enabled`` to also be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#cspm_resource_collection_enabled IntegrationGcp#cspm_resource_collection_enabled}
        :param host_filters: Limit the GCE instances that are pulled into Datadog by using tags. Only hosts that match one of the defined tags are imported into Datadog. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#host_filters IntegrationGcp#host_filters}
        :param is_resource_change_collection_enabled: When enabled, Datadog scans for all resource change data in your Google Cloud environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#is_resource_change_collection_enabled IntegrationGcp#is_resource_change_collection_enabled}
        :param is_security_command_center_enabled: When enabled, Datadog will attempt to collect Security Command Center Findings. Note: This requires additional permissions on the service account. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#is_security_command_center_enabled IntegrationGcp#is_security_command_center_enabled}
        :param resource_collection_enabled: When enabled, Datadog scans for all resources in your GCP environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#resource_collection_enabled IntegrationGcp#resource_collection_enabled}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3995b4740b3ef99941fe59f37ba75c23f435badba6c448d0a5f6133aa6c57b5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument client_email", value=client_email, expected_type=type_hints["client_email"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument private_key_id", value=private_key_id, expected_type=type_hints["private_key_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument automute", value=automute, expected_type=type_hints["automute"])
            check_type(argname="argument cloud_run_revision_filters", value=cloud_run_revision_filters, expected_type=type_hints["cloud_run_revision_filters"])
            check_type(argname="argument cspm_resource_collection_enabled", value=cspm_resource_collection_enabled, expected_type=type_hints["cspm_resource_collection_enabled"])
            check_type(argname="argument host_filters", value=host_filters, expected_type=type_hints["host_filters"])
            check_type(argname="argument is_resource_change_collection_enabled", value=is_resource_change_collection_enabled, expected_type=type_hints["is_resource_change_collection_enabled"])
            check_type(argname="argument is_security_command_center_enabled", value=is_security_command_center_enabled, expected_type=type_hints["is_security_command_center_enabled"])
            check_type(argname="argument resource_collection_enabled", value=resource_collection_enabled, expected_type=type_hints["resource_collection_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_email": client_email,
            "client_id": client_id,
            "private_key": private_key,
            "private_key_id": private_key_id,
            "project_id": project_id,
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
        if automute is not None:
            self._values["automute"] = automute
        if cloud_run_revision_filters is not None:
            self._values["cloud_run_revision_filters"] = cloud_run_revision_filters
        if cspm_resource_collection_enabled is not None:
            self._values["cspm_resource_collection_enabled"] = cspm_resource_collection_enabled
        if host_filters is not None:
            self._values["host_filters"] = host_filters
        if is_resource_change_collection_enabled is not None:
            self._values["is_resource_change_collection_enabled"] = is_resource_change_collection_enabled
        if is_security_command_center_enabled is not None:
            self._values["is_security_command_center_enabled"] = is_security_command_center_enabled
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
        '''Your email found in your JSON service account key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#client_email IntegrationGcp#client_email}
        '''
        result = self._values.get("client_email")
        assert result is not None, "Required property 'client_email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Your ID found in your JSON service account key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#client_id IntegrationGcp#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def private_key(self) -> builtins.str:
        '''Your private key name found in your JSON service account key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#private_key IntegrationGcp#private_key}
        '''
        result = self._values.get("private_key")
        assert result is not None, "Required property 'private_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def private_key_id(self) -> builtins.str:
        '''Your private key ID found in your JSON service account key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#private_key_id IntegrationGcp#private_key_id}
        '''
        result = self._values.get("private_key_id")
        assert result is not None, "Required property 'private_key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''Your Google Cloud project ID found in your JSON service account key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#project_id IntegrationGcp#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def automute(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Silence monitors for expected GCE instance shutdowns. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#automute IntegrationGcp#automute}
        '''
        result = self._values.get("automute")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cloud_run_revision_filters(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags to filter which Cloud Run revisions are imported into Datadog. Only revisions that meet specified criteria are monitored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#cloud_run_revision_filters IntegrationGcp#cloud_run_revision_filters}
        '''
        result = self._values.get("cloud_run_revision_filters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cspm_resource_collection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Datadog collects cloud security posture management resources from your GCP project.

        If enabled, requires ``resource_collection_enabled`` to also be enabled. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#cspm_resource_collection_enabled IntegrationGcp#cspm_resource_collection_enabled}
        '''
        result = self._values.get("cspm_resource_collection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def host_filters(self) -> typing.Optional[builtins.str]:
        '''Limit the GCE instances that are pulled into Datadog by using tags.

        Only hosts that match one of the defined tags are imported into Datadog. Defaults to ``""``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#host_filters IntegrationGcp#host_filters}
        '''
        result = self._values.get("host_filters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_resource_change_collection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled, Datadog scans for all resource change data in your Google Cloud environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#is_resource_change_collection_enabled IntegrationGcp#is_resource_change_collection_enabled}
        '''
        result = self._values.get("is_resource_change_collection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_security_command_center_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled, Datadog will attempt to collect Security Command Center Findings.

        Note: This requires additional permissions on the service account. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#is_security_command_center_enabled IntegrationGcp#is_security_command_center_enabled}
        '''
        result = self._values.get("is_security_command_center_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def resource_collection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled, Datadog scans for all resources in your GCP environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/integration_gcp#resource_collection_enabled IntegrationGcp#resource_collection_enabled}
        '''
        result = self._values.get("resource_collection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegrationGcpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IntegrationGcp",
    "IntegrationGcpConfig",
]

publication.publish()

def _typecheckingstub__7fc57a1ea03daadb5d0c15ad30327ce20c06b6d8439b07dfc0fd9550612acb1c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    client_email: builtins.str,
    client_id: builtins.str,
    private_key: builtins.str,
    private_key_id: builtins.str,
    project_id: builtins.str,
    automute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cloud_run_revision_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
    cspm_resource_collection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host_filters: typing.Optional[builtins.str] = None,
    is_resource_change_collection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_security_command_center_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__1ef0f727583ce7c18a919113e96bdf464103f7ef6e830faf228800aeadaa6c86(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8257f23c7c2c57573d4401bb70e01ea9bd716bdf5356eb78f2950ec9bf88322(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a08ce27a1da51f10ab9d254c903abf30c10e358fa6ef0d014a0eb896b0a5c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5a7f423973fc20a16dca6db9249d75ef86bd96652e07136649e33f42514f44a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6918bd10152acfbc9033a3df86b3abcd351abda960e76013944f1cdd08720bd0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bae2566e3372da23dc6317431717220a97c3dfac640307089efac92a141746c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd5e5e4d87be44c43cb245177a8c96c308f5713604d367af5dcf611c517fd8b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3c10dae6c99d64772b3ea095817be752b863a3a93cfb3293b29895f04642b93(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f40dcdd912aff7a31a1cc9f1dd9a76cd05faa707c7c6ff52bf95af5925cb9ad7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c3e68e0e148b0d384c1ec64eb001370a263c0aebee1af1c39f3945d28dfe69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d79991e30108bd85fb4b9b0aa93e84dc97904db0dd119b9bc0ca86080196b2b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb270052fca8af40b300fd2b5d39ceffd51e7313b208468e9c7d91f343714f16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18b89ad036e3961ff9f43ffcd937ea868213ae6e364492d54e58e3b713751f4e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3995b4740b3ef99941fe59f37ba75c23f435badba6c448d0a5f6133aa6c57b5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    client_email: builtins.str,
    client_id: builtins.str,
    private_key: builtins.str,
    private_key_id: builtins.str,
    project_id: builtins.str,
    automute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cloud_run_revision_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
    cspm_resource_collection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host_filters: typing.Optional[builtins.str] = None,
    is_resource_change_collection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_security_command_center_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    resource_collection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
