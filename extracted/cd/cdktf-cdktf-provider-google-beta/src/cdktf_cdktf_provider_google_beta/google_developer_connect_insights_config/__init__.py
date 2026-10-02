r'''
# `google_developer_connect_insights_config`

Refer to the Terraform Registry for docs: [`google_developer_connect_insights_config`](https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config).
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


class GoogleDeveloperConnectInsightsConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config google_developer_connect_insights_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        app_hub_application: builtins.str,
        insights_config_id: builtins.str,
        location: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        artifact_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDeveloperConnectInsightsConfigArtifactConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDeveloperConnectInsightsConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config google_developer_connect_insights_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param app_hub_application: The name of the App Hub Application. Format: projects/{project}/locations/{location}/applications/{application}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#app_hub_application GoogleDeveloperConnectInsightsConfig#app_hub_application}
        :param insights_config_id: ID of the requesting InsightsConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#insights_config_id GoogleDeveloperConnectInsightsConfig#insights_config_id}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#location GoogleDeveloperConnectInsightsConfig#location}
        :param annotations: User specified annotations. See https://google.aip.dev/148#annotations for more details such as format and size limitations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#annotations GoogleDeveloperConnectInsightsConfig#annotations}
        :param artifact_configs: artifact_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#artifact_configs GoogleDeveloperConnectInsightsConfig#artifact_configs}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#id GoogleDeveloperConnectInsightsConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of labels associated with an InsightsConfig. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#labels GoogleDeveloperConnectInsightsConfig#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#project GoogleDeveloperConnectInsightsConfig#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#timeouts GoogleDeveloperConnectInsightsConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f996d8a5492fc45d380145068d9d84a0b03e33bc51e73c4362350a35509e4750)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDeveloperConnectInsightsConfigConfig(
            app_hub_application=app_hub_application,
            insights_config_id=insights_config_id,
            location=location,
            annotations=annotations,
            artifact_configs=artifact_configs,
            id=id,
            labels=labels,
            project=project,
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
        '''Generates CDKTF code for importing a GoogleDeveloperConnectInsightsConfig resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDeveloperConnectInsightsConfig to import.
        :param import_from_id: The id of the existing GoogleDeveloperConnectInsightsConfig that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDeveloperConnectInsightsConfig to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f20810b8b4e2ca68fc1c29934343d5f0d807117a7aa9a814e31221a3192daa79)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putArtifactConfigs")
    def put_artifact_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDeveloperConnectInsightsConfigArtifactConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f000cc6d56f9bc578dd78c09c9878bc8351de54167d5ef0c8acc24d2a447f75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putArtifactConfigs", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#create GoogleDeveloperConnectInsightsConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#delete GoogleDeveloperConnectInsightsConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#update GoogleDeveloperConnectInsightsConfig#update}.
        '''
        value = GoogleDeveloperConnectInsightsConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetArtifactConfigs")
    def reset_artifact_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArtifactConfigs", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="artifactConfigs")
    def artifact_configs(
        self,
    ) -> "GoogleDeveloperConnectInsightsConfigArtifactConfigsList":
        return typing.cast("GoogleDeveloperConnectInsightsConfigArtifactConfigsList", jsii.get(self, "artifactConfigs"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="errors")
    def errors(self) -> "GoogleDeveloperConnectInsightsConfigErrorsList":
        return typing.cast("GoogleDeveloperConnectInsightsConfigErrorsList", jsii.get(self, "errors"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="runtimeConfigs")
    def runtime_configs(
        self,
    ) -> "GoogleDeveloperConnectInsightsConfigRuntimeConfigsList":
        return typing.cast("GoogleDeveloperConnectInsightsConfigRuntimeConfigsList", jsii.get(self, "runtimeConfigs"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleDeveloperConnectInsightsConfigTimeoutsOutputReference":
        return typing.cast("GoogleDeveloperConnectInsightsConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="appHubApplicationInput")
    def app_hub_application_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appHubApplicationInput"))

    @builtins.property
    @jsii.member(jsii_name="artifactConfigsInput")
    def artifact_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDeveloperConnectInsightsConfigArtifactConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDeveloperConnectInsightsConfigArtifactConfigs"]]], jsii.get(self, "artifactConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="insightsConfigIdInput")
    def insights_config_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "insightsConfigIdInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDeveloperConnectInsightsConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDeveloperConnectInsightsConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a49e4750586c6639ee95d4ed1b96cbe8d12bc5785e42999627ce780732436f49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appHubApplication")
    def app_hub_application(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appHubApplication"))

    @app_hub_application.setter
    def app_hub_application(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1c9503e45f67fa063a87d9634d6195773a8cd3bcd5a810261cbcba9c6d5c2ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appHubApplication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a7634f6d8baf2eac61c91bfdd5d0d03330925d013038fc2fa130bbe52bb403c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="insightsConfigId")
    def insights_config_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "insightsConfigId"))

    @insights_config_id.setter
    def insights_config_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79a284895eeff384e470e5e813fa12a9d7d568ce7024d136c4b82b931aece915)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insightsConfigId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0263ee70bf9ddeeef13c2b229122eb7d5c16421d377933400d18424222c0754)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__272517b4b99afea74dcdcbc032860837a2cdb9780a1fb5778548573e5edd991c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c0ce7c4d158b55ea3beef18063e3c9479d12f371400b8721cb6a737100d4ce9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigArtifactConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "google_artifact_analysis": "googleArtifactAnalysis",
        "google_artifact_registry": "googleArtifactRegistry",
        "uri": "uri",
    },
)
class GoogleDeveloperConnectInsightsConfigArtifactConfigs:
    def __init__(
        self,
        *,
        google_artifact_analysis: typing.Optional[typing.Union["GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactAnalysis", typing.Dict[builtins.str, typing.Any]]] = None,
        google_artifact_registry: typing.Optional[typing.Union["GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactRegistry", typing.Dict[builtins.str, typing.Any]]] = None,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param google_artifact_analysis: google_artifact_analysis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#google_artifact_analysis GoogleDeveloperConnectInsightsConfig#google_artifact_analysis}
        :param google_artifact_registry: google_artifact_registry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#google_artifact_registry GoogleDeveloperConnectInsightsConfig#google_artifact_registry}
        :param uri: The URI of the artifact that is deployed. e.g. 'us-docker.pkg.dev/my-project/my-repo/image'. The URI does not include the tag / digest because it captures a lineage of artifacts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#uri GoogleDeveloperConnectInsightsConfig#uri}
        '''
        if isinstance(google_artifact_analysis, dict):
            google_artifact_analysis = GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactAnalysis(**google_artifact_analysis)
        if isinstance(google_artifact_registry, dict):
            google_artifact_registry = GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactRegistry(**google_artifact_registry)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08f429d2caa885f1c7a786f53d3592a1f609923dec521a4c7becced8f3d00c99)
            check_type(argname="argument google_artifact_analysis", value=google_artifact_analysis, expected_type=type_hints["google_artifact_analysis"])
            check_type(argname="argument google_artifact_registry", value=google_artifact_registry, expected_type=type_hints["google_artifact_registry"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if google_artifact_analysis is not None:
            self._values["google_artifact_analysis"] = google_artifact_analysis
        if google_artifact_registry is not None:
            self._values["google_artifact_registry"] = google_artifact_registry
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def google_artifact_analysis(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactAnalysis"]:
        '''google_artifact_analysis block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#google_artifact_analysis GoogleDeveloperConnectInsightsConfig#google_artifact_analysis}
        '''
        result = self._values.get("google_artifact_analysis")
        return typing.cast(typing.Optional["GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactAnalysis"], result)

    @builtins.property
    def google_artifact_registry(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactRegistry"]:
        '''google_artifact_registry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#google_artifact_registry GoogleDeveloperConnectInsightsConfig#google_artifact_registry}
        '''
        result = self._values.get("google_artifact_registry")
        return typing.cast(typing.Optional["GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactRegistry"], result)

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''The URI of the artifact that is deployed.

        e.g. 'us-docker.pkg.dev/my-project/my-repo/image'.
        The URI does not include the tag / digest because it captures a lineage of
        artifacts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#uri GoogleDeveloperConnectInsightsConfig#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectInsightsConfigArtifactConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactAnalysis",
    jsii_struct_bases=[],
    name_mapping={"project_id": "projectId"},
)
class GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactAnalysis:
    def __init__(self, *, project_id: builtins.str) -> None:
        '''
        :param project_id: The project id of the project where the provenance is stored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#project_id GoogleDeveloperConnectInsightsConfig#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1269c08591eb73155542100939fee37ac43b0a7e2e4f94df6a2cf1e3d91d0718)
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project_id": project_id,
        }

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The project id of the project where the provenance is stored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#project_id GoogleDeveloperConnectInsightsConfig#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactAnalysis(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactAnalysisOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactAnalysisOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e82c3c3878878f2ab7e478e696486a682901adfd602a9042ab70fbd5c7c8160)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ac403181e7ce0959b211644253fa736c6cd90d50e20f8d79234f1a722875cc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactAnalysis]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactAnalysis], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactAnalysis],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ca571461fc75555dbc984f2bf74121ece5d5a062f2ac54fc4932119b61f7b40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactRegistry",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_registry_package": "artifactRegistryPackage",
        "project_id": "projectId",
    },
)
class GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactRegistry:
    def __init__(
        self,
        *,
        artifact_registry_package: builtins.str,
        project_id: builtins.str,
    ) -> None:
        '''
        :param artifact_registry_package: The name of the artifact registry package. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#artifact_registry_package GoogleDeveloperConnectInsightsConfig#artifact_registry_package}
        :param project_id: The host project of Artifact Registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#project_id GoogleDeveloperConnectInsightsConfig#project_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9797b40785f9669e0a819fc1926a4e61f503b29ee8d30e2901da6875d2ed2724)
            check_type(argname="argument artifact_registry_package", value=artifact_registry_package, expected_type=type_hints["artifact_registry_package"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifact_registry_package": artifact_registry_package,
            "project_id": project_id,
        }

    @builtins.property
    def artifact_registry_package(self) -> builtins.str:
        '''The name of the artifact registry package.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#artifact_registry_package GoogleDeveloperConnectInsightsConfig#artifact_registry_package}
        '''
        result = self._values.get("artifact_registry_package")
        assert result is not None, "Required property 'artifact_registry_package' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The host project of Artifact Registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#project_id GoogleDeveloperConnectInsightsConfig#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactRegistry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactRegistryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactRegistryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a7d10f9b012538b49b2eb5d170fb6515dae69423971b70c128c145d1ef37382)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="artifactRegistryPackageInput")
    def artifact_registry_package_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "artifactRegistryPackageInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="artifactRegistryPackage")
    def artifact_registry_package(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "artifactRegistryPackage"))

    @artifact_registry_package.setter
    def artifact_registry_package(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b942fabc837fdba19c90edc02fee625d92ecc5e40d6d303587049654c7f8e6ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "artifactRegistryPackage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87184dcde1cc8a0cdd4f2bf4efb84f95d93737ac001d85d8d638113e3290e1e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactRegistry]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactRegistry], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactRegistry],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c9e00325a8bbe3d6cecff2768ef561a97b2de6ef5c16e6d1b3386f1fab9d110)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDeveloperConnectInsightsConfigArtifactConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigArtifactConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ca8aad72ef79499afbc000df0c9e2840d69352f3b4ed7db5570b3823ae73d97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDeveloperConnectInsightsConfigArtifactConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d080b3867f9b012685ceef208ad10b9c3002c5d37570665ec04cc3a2850e407)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDeveloperConnectInsightsConfigArtifactConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c61c3f0b62f52d7e018c018a7eb635e370fa043f3785d0175b7ac0241688806c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c27c283def8a1bd11456da055994cda6390ae51ac4360c101a8d7dc8b6a26dc9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__04dbbdff7a4e956e37fe5175938941a77e5864bb993b9875b0961babd6e086ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDeveloperConnectInsightsConfigArtifactConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDeveloperConnectInsightsConfigArtifactConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDeveloperConnectInsightsConfigArtifactConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33a16c7608172156e90780efc2011ceca8757afb75d07389b0428ca0e09a5ea0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDeveloperConnectInsightsConfigArtifactConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigArtifactConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1de5b71eac959aa928759566e6b3375506e84b6bf904af7232d6b26b26918115)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putGoogleArtifactAnalysis")
    def put_google_artifact_analysis(self, *, project_id: builtins.str) -> None:
        '''
        :param project_id: The project id of the project where the provenance is stored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#project_id GoogleDeveloperConnectInsightsConfig#project_id}
        '''
        value = GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactAnalysis(
            project_id=project_id
        )

        return typing.cast(None, jsii.invoke(self, "putGoogleArtifactAnalysis", [value]))

    @jsii.member(jsii_name="putGoogleArtifactRegistry")
    def put_google_artifact_registry(
        self,
        *,
        artifact_registry_package: builtins.str,
        project_id: builtins.str,
    ) -> None:
        '''
        :param artifact_registry_package: The name of the artifact registry package. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#artifact_registry_package GoogleDeveloperConnectInsightsConfig#artifact_registry_package}
        :param project_id: The host project of Artifact Registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#project_id GoogleDeveloperConnectInsightsConfig#project_id}
        '''
        value = GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactRegistry(
            artifact_registry_package=artifact_registry_package, project_id=project_id
        )

        return typing.cast(None, jsii.invoke(self, "putGoogleArtifactRegistry", [value]))

    @jsii.member(jsii_name="resetGoogleArtifactAnalysis")
    def reset_google_artifact_analysis(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoogleArtifactAnalysis", []))

    @jsii.member(jsii_name="resetGoogleArtifactRegistry")
    def reset_google_artifact_registry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoogleArtifactRegistry", []))

    @jsii.member(jsii_name="resetUri")
    def reset_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUri", []))

    @builtins.property
    @jsii.member(jsii_name="googleArtifactAnalysis")
    def google_artifact_analysis(
        self,
    ) -> GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactAnalysisOutputReference:
        return typing.cast(GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactAnalysisOutputReference, jsii.get(self, "googleArtifactAnalysis"))

    @builtins.property
    @jsii.member(jsii_name="googleArtifactRegistry")
    def google_artifact_registry(
        self,
    ) -> GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactRegistryOutputReference:
        return typing.cast(GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactRegistryOutputReference, jsii.get(self, "googleArtifactRegistry"))

    @builtins.property
    @jsii.member(jsii_name="googleArtifactAnalysisInput")
    def google_artifact_analysis_input(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactAnalysis]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactAnalysis], jsii.get(self, "googleArtifactAnalysisInput"))

    @builtins.property
    @jsii.member(jsii_name="googleArtifactRegistryInput")
    def google_artifact_registry_input(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactRegistry]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactRegistry], jsii.get(self, "googleArtifactRegistryInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e26d08e1a82ba1940739c0274b35069ed964cb87562a2641310933f3f5eafac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDeveloperConnectInsightsConfigArtifactConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDeveloperConnectInsightsConfigArtifactConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDeveloperConnectInsightsConfigArtifactConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a39afba5173cd733b88647abf1179812cdb3e192b9c5a1b9cf5fe71df0d86bf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "app_hub_application": "appHubApplication",
        "insights_config_id": "insightsConfigId",
        "location": "location",
        "annotations": "annotations",
        "artifact_configs": "artifactConfigs",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleDeveloperConnectInsightsConfigConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        app_hub_application: builtins.str,
        insights_config_id: builtins.str,
        location: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        artifact_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDeveloperConnectInsightsConfigArtifactConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDeveloperConnectInsightsConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param app_hub_application: The name of the App Hub Application. Format: projects/{project}/locations/{location}/applications/{application}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#app_hub_application GoogleDeveloperConnectInsightsConfig#app_hub_application}
        :param insights_config_id: ID of the requesting InsightsConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#insights_config_id GoogleDeveloperConnectInsightsConfig#insights_config_id}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#location GoogleDeveloperConnectInsightsConfig#location}
        :param annotations: User specified annotations. See https://google.aip.dev/148#annotations for more details such as format and size limitations. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#annotations GoogleDeveloperConnectInsightsConfig#annotations}
        :param artifact_configs: artifact_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#artifact_configs GoogleDeveloperConnectInsightsConfig#artifact_configs}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#id GoogleDeveloperConnectInsightsConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of labels associated with an InsightsConfig. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#labels GoogleDeveloperConnectInsightsConfig#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#project GoogleDeveloperConnectInsightsConfig#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#timeouts GoogleDeveloperConnectInsightsConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = GoogleDeveloperConnectInsightsConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37822d7238a38e9be2cfe64c407a3fabbf7d762bbc90be37d8ffa3908d059f42)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument app_hub_application", value=app_hub_application, expected_type=type_hints["app_hub_application"])
            check_type(argname="argument insights_config_id", value=insights_config_id, expected_type=type_hints["insights_config_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument artifact_configs", value=artifact_configs, expected_type=type_hints["artifact_configs"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_hub_application": app_hub_application,
            "insights_config_id": insights_config_id,
            "location": location,
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
        if annotations is not None:
            self._values["annotations"] = annotations
        if artifact_configs is not None:
            self._values["artifact_configs"] = artifact_configs
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
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
    def app_hub_application(self) -> builtins.str:
        '''The name of the App Hub Application. Format: projects/{project}/locations/{location}/applications/{application}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#app_hub_application GoogleDeveloperConnectInsightsConfig#app_hub_application}
        '''
        result = self._values.get("app_hub_application")
        assert result is not None, "Required property 'app_hub_application' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def insights_config_id(self) -> builtins.str:
        '''ID of the requesting InsightsConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#insights_config_id GoogleDeveloperConnectInsightsConfig#insights_config_id}
        '''
        result = self._values.get("insights_config_id")
        assert result is not None, "Required property 'insights_config_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#location GoogleDeveloperConnectInsightsConfig#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User specified annotations. See https://google.aip.dev/148#annotations for more details such as format and size limitations.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#annotations GoogleDeveloperConnectInsightsConfig#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def artifact_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDeveloperConnectInsightsConfigArtifactConfigs]]]:
        '''artifact_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#artifact_configs GoogleDeveloperConnectInsightsConfig#artifact_configs}
        '''
        result = self._values.get("artifact_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDeveloperConnectInsightsConfigArtifactConfigs]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#id GoogleDeveloperConnectInsightsConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Set of labels associated with an InsightsConfig.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#labels GoogleDeveloperConnectInsightsConfig#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#project GoogleDeveloperConnectInsightsConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleDeveloperConnectInsightsConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#timeouts GoogleDeveloperConnectInsightsConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDeveloperConnectInsightsConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectInsightsConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigErrors",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDeveloperConnectInsightsConfigErrors:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectInsightsConfigErrors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigErrorsDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDeveloperConnectInsightsConfigErrorsDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectInsightsConfigErrorsDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDeveloperConnectInsightsConfigErrorsDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigErrorsDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28fd01cac898d050bc730b0fffaa9dfca53c3cc10f25573187fe94fdcfa45d2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDeveloperConnectInsightsConfigErrorsDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f4d9672753902d66baa1e5196a5306c9a844169a59714edb62e9b965e37ce5a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDeveloperConnectInsightsConfigErrorsDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40eb51428facd04dc91cca51b1ec1fddf195d4912494c45d2133f897eb0c7c2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca1d5dbf92a7f8242eb1495749fa9ed04ee0100030dc54fad269a6463056c12d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2547707ac07bfb33847589fe184cacc15b941d7d3f749c7c05b1b6cd90e79708)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDeveloperConnectInsightsConfigErrorsDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigErrorsDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44e82b30add16339e2e37fa8f84c79ec97927f7c54a009f5c669e4eb2188f9ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="detailMessage")
    def detail_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "detailMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectInsightsConfigErrorsDetails]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectInsightsConfigErrorsDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectInsightsConfigErrorsDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f9bae7455ca133558da28701ced3ec52496b97192ced0f766b88c2e97f294f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDeveloperConnectInsightsConfigErrorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigErrorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de8d04b4161fb582131bb460c946eb5c8e157445e06e3b418bc54e5a43c32b5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDeveloperConnectInsightsConfigErrorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c609496eb574e34a0bebad816316d8e2aed144a31b11557da2236a93d1253674)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDeveloperConnectInsightsConfigErrorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec3ec9762b910272fe623c61d2552f0c0b0e45449275daeee3ce56c59dc53e2f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4c298bdd6d3734d810101f57570e2f08c1e6347bb5220cba5259494b60f89a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__facb649595cb2b57ce43aed6abe2a5e9dc89890ecb2db2a33e8401a6b1f95270)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDeveloperConnectInsightsConfigErrorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigErrorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__511a54e719acceee91b2a26281223a3030803e7783c96a2cd29a1b790b7ae79a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "code"))

    @builtins.property
    @jsii.member(jsii_name="details")
    def details(self) -> GoogleDeveloperConnectInsightsConfigErrorsDetailsList:
        return typing.cast(GoogleDeveloperConnectInsightsConfigErrorsDetailsList, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectInsightsConfigErrors]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectInsightsConfigErrors], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectInsightsConfigErrors],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ff85572e868d0d4008c6050c0cc456a5ecb4052b60005635e86952231f806f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigRuntimeConfigs",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDeveloperConnectInsightsConfigRuntimeConfigs:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectInsightsConfigRuntimeConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigRuntimeConfigsAppHubWorkload",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDeveloperConnectInsightsConfigRuntimeConfigsAppHubWorkload:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectInsightsConfigRuntimeConfigsAppHubWorkload(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDeveloperConnectInsightsConfigRuntimeConfigsAppHubWorkloadList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigRuntimeConfigsAppHubWorkloadList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d344d5cccd480dce754923c03332a189f7e77b5141289096bf83a6cfe734503a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDeveloperConnectInsightsConfigRuntimeConfigsAppHubWorkloadOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70f62ac0e0ebfa75edc71e530f71b336efdaadb51a7d419aec069a0a1da70636)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDeveloperConnectInsightsConfigRuntimeConfigsAppHubWorkloadOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8512073e70ba9644eb8e683bae193dc8b5e6b502219cc561e2589a38b5d1f2fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d30a36aa9a132b0bd9c7d1e7e548cefb7a4fbd9513aa7878e25fffbd2951bd7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc9521cb7a7d6c04d2ef381283563067efe38ddf502f6f4c105182be500b4b41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDeveloperConnectInsightsConfigRuntimeConfigsAppHubWorkloadOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigRuntimeConfigsAppHubWorkloadOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f2198605ea0362bf71ff41a4a528f147155f297b7a288565d1361ccf91eb758)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="criticality")
    def criticality(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "criticality"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="workload")
    def workload(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workload"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectInsightsConfigRuntimeConfigsAppHubWorkload]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectInsightsConfigRuntimeConfigsAppHubWorkload], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectInsightsConfigRuntimeConfigsAppHubWorkload],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__240ada19343009ea25eb00ea2e3163e2056cc82c9a1ad3bbad9811e037cfae7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigRuntimeConfigsGkeWorkload",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDeveloperConnectInsightsConfigRuntimeConfigsGkeWorkload:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectInsightsConfigRuntimeConfigsGkeWorkload(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDeveloperConnectInsightsConfigRuntimeConfigsGkeWorkloadList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigRuntimeConfigsGkeWorkloadList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e0191a03b963bdb742ecf0d5e1dc1720f27beb2c79016deb26fbfc1442ede57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDeveloperConnectInsightsConfigRuntimeConfigsGkeWorkloadOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86e6d5fbf48b0215048e0ee5b933e186a048a3da0e527001306e77e7d9462c47)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDeveloperConnectInsightsConfigRuntimeConfigsGkeWorkloadOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62c7d39668651704f526be26299fb8c2297584c78e04ea4ff05ff5f1146dcc81)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2059a551d49dd421d8f71de20628bb2c87098cc6b724f836289e1618c1300b75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fe0fffbbaf3ded703e936a7711f11d74cc57897655982a912e39b45be1b4d6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDeveloperConnectInsightsConfigRuntimeConfigsGkeWorkloadOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigRuntimeConfigsGkeWorkloadOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a2ca49eafcc3075878e8dbd3afb96dc2c34fc9f31dfeb91a7f6e6079ef95b61)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="deployment")
    def deployment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deployment"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectInsightsConfigRuntimeConfigsGkeWorkload]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectInsightsConfigRuntimeConfigsGkeWorkload], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectInsightsConfigRuntimeConfigsGkeWorkload],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1099dad28ddcb95ede3349612eef6535d7afff0eaf64d568727cb458891ebe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDeveloperConnectInsightsConfigRuntimeConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigRuntimeConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29b0793227d804ce28091317ed0786a2aa9fd9d68a0c93ff51228ab5586723b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDeveloperConnectInsightsConfigRuntimeConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c911a7c3f82163d8bed8199a7aa0c031a634e3081bf54fc9d65252df600fa8a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDeveloperConnectInsightsConfigRuntimeConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b20b75a26d09b7fc1046298693aedf31be8a7c8046f668e3ca8c4f4252bb7e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01876567b29dc0392d4464c9bf800abdd5d897b84ee6b4485aa5d7e47374d764)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49bc93a6b916a5c476ddda8aa436a8dbddfa29f0a709422b2e3131541b6cc687)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDeveloperConnectInsightsConfigRuntimeConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigRuntimeConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b263f9439038f98dc9a18c6aa94ad90a40ca22bb6b6e8d013990262648a31202)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="appHubWorkload")
    def app_hub_workload(
        self,
    ) -> GoogleDeveloperConnectInsightsConfigRuntimeConfigsAppHubWorkloadList:
        return typing.cast(GoogleDeveloperConnectInsightsConfigRuntimeConfigsAppHubWorkloadList, jsii.get(self, "appHubWorkload"))

    @builtins.property
    @jsii.member(jsii_name="gkeWorkload")
    def gke_workload(
        self,
    ) -> GoogleDeveloperConnectInsightsConfigRuntimeConfigsGkeWorkloadList:
        return typing.cast(GoogleDeveloperConnectInsightsConfigRuntimeConfigsGkeWorkloadList, jsii.get(self, "gkeWorkload"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDeveloperConnectInsightsConfigRuntimeConfigs]:
        return typing.cast(typing.Optional[GoogleDeveloperConnectInsightsConfigRuntimeConfigs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDeveloperConnectInsightsConfigRuntimeConfigs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__728e056582c52135a8f0251d50e910d66e4db20af4090bbb01835361cffe544e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDeveloperConnectInsightsConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#create GoogleDeveloperConnectInsightsConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#delete GoogleDeveloperConnectInsightsConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#update GoogleDeveloperConnectInsightsConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fa6b060123d182aea93a3fcb1c4c9d2f940d7a764da8ab7fc1f6c9017e3a22f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#create GoogleDeveloperConnectInsightsConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#delete GoogleDeveloperConnectInsightsConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_developer_connect_insights_config#update GoogleDeveloperConnectInsightsConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDeveloperConnectInsightsConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDeveloperConnectInsightsConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDeveloperConnectInsightsConfig.GoogleDeveloperConnectInsightsConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91f0a53bab1c0ab1f5a7aa78cc6c9ce36e5b609f9ab8f470099c36be70582973)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1293f62dd6d99ad72f7eb4547d62e181301bd4e4b7538e43bde0d98dfebaaf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1401306e6815b6d2e0c566c4f86863b89c40cd4d0bcc6ffe43b212c4504635f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eead00ad1f4df16ae00f334e64420fb886482996e288983928ff02d14b1d928b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDeveloperConnectInsightsConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDeveloperConnectInsightsConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDeveloperConnectInsightsConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a64a70d68b0e0aa552ab225744f1d70027d251e58fd850e00e4f2e3a11deddcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDeveloperConnectInsightsConfig",
    "GoogleDeveloperConnectInsightsConfigArtifactConfigs",
    "GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactAnalysis",
    "GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactAnalysisOutputReference",
    "GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactRegistry",
    "GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactRegistryOutputReference",
    "GoogleDeveloperConnectInsightsConfigArtifactConfigsList",
    "GoogleDeveloperConnectInsightsConfigArtifactConfigsOutputReference",
    "GoogleDeveloperConnectInsightsConfigConfig",
    "GoogleDeveloperConnectInsightsConfigErrors",
    "GoogleDeveloperConnectInsightsConfigErrorsDetails",
    "GoogleDeveloperConnectInsightsConfigErrorsDetailsList",
    "GoogleDeveloperConnectInsightsConfigErrorsDetailsOutputReference",
    "GoogleDeveloperConnectInsightsConfigErrorsList",
    "GoogleDeveloperConnectInsightsConfigErrorsOutputReference",
    "GoogleDeveloperConnectInsightsConfigRuntimeConfigs",
    "GoogleDeveloperConnectInsightsConfigRuntimeConfigsAppHubWorkload",
    "GoogleDeveloperConnectInsightsConfigRuntimeConfigsAppHubWorkloadList",
    "GoogleDeveloperConnectInsightsConfigRuntimeConfigsAppHubWorkloadOutputReference",
    "GoogleDeveloperConnectInsightsConfigRuntimeConfigsGkeWorkload",
    "GoogleDeveloperConnectInsightsConfigRuntimeConfigsGkeWorkloadList",
    "GoogleDeveloperConnectInsightsConfigRuntimeConfigsGkeWorkloadOutputReference",
    "GoogleDeveloperConnectInsightsConfigRuntimeConfigsList",
    "GoogleDeveloperConnectInsightsConfigRuntimeConfigsOutputReference",
    "GoogleDeveloperConnectInsightsConfigTimeouts",
    "GoogleDeveloperConnectInsightsConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f996d8a5492fc45d380145068d9d84a0b03e33bc51e73c4362350a35509e4750(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    app_hub_application: builtins.str,
    insights_config_id: builtins.str,
    location: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    artifact_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDeveloperConnectInsightsConfigArtifactConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDeveloperConnectInsightsConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f20810b8b4e2ca68fc1c29934343d5f0d807117a7aa9a814e31221a3192daa79(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f000cc6d56f9bc578dd78c09c9878bc8351de54167d5ef0c8acc24d2a447f75(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDeveloperConnectInsightsConfigArtifactConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a49e4750586c6639ee95d4ed1b96cbe8d12bc5785e42999627ce780732436f49(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c9503e45f67fa063a87d9634d6195773a8cd3bcd5a810261cbcba9c6d5c2ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7634f6d8baf2eac61c91bfdd5d0d03330925d013038fc2fa130bbe52bb403c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79a284895eeff384e470e5e813fa12a9d7d568ce7024d136c4b82b931aece915(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0263ee70bf9ddeeef13c2b229122eb7d5c16421d377933400d18424222c0754(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__272517b4b99afea74dcdcbc032860837a2cdb9780a1fb5778548573e5edd991c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c0ce7c4d158b55ea3beef18063e3c9479d12f371400b8721cb6a737100d4ce9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08f429d2caa885f1c7a786f53d3592a1f609923dec521a4c7becced8f3d00c99(
    *,
    google_artifact_analysis: typing.Optional[typing.Union[GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactAnalysis, typing.Dict[builtins.str, typing.Any]]] = None,
    google_artifact_registry: typing.Optional[typing.Union[GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactRegistry, typing.Dict[builtins.str, typing.Any]]] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1269c08591eb73155542100939fee37ac43b0a7e2e4f94df6a2cf1e3d91d0718(
    *,
    project_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e82c3c3878878f2ab7e478e696486a682901adfd602a9042ab70fbd5c7c8160(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac403181e7ce0959b211644253fa736c6cd90d50e20f8d79234f1a722875cc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca571461fc75555dbc984f2bf74121ece5d5a062f2ac54fc4932119b61f7b40(
    value: typing.Optional[GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactAnalysis],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9797b40785f9669e0a819fc1926a4e61f503b29ee8d30e2901da6875d2ed2724(
    *,
    artifact_registry_package: builtins.str,
    project_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a7d10f9b012538b49b2eb5d170fb6515dae69423971b70c128c145d1ef37382(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b942fabc837fdba19c90edc02fee625d92ecc5e40d6d303587049654c7f8e6ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87184dcde1cc8a0cdd4f2bf4efb84f95d93737ac001d85d8d638113e3290e1e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9e00325a8bbe3d6cecff2768ef561a97b2de6ef5c16e6d1b3386f1fab9d110(
    value: typing.Optional[GoogleDeveloperConnectInsightsConfigArtifactConfigsGoogleArtifactRegistry],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca8aad72ef79499afbc000df0c9e2840d69352f3b4ed7db5570b3823ae73d97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d080b3867f9b012685ceef208ad10b9c3002c5d37570665ec04cc3a2850e407(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c61c3f0b62f52d7e018c018a7eb635e370fa043f3785d0175b7ac0241688806c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27c283def8a1bd11456da055994cda6390ae51ac4360c101a8d7dc8b6a26dc9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04dbbdff7a4e956e37fe5175938941a77e5864bb993b9875b0961babd6e086ef(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a16c7608172156e90780efc2011ceca8757afb75d07389b0428ca0e09a5ea0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDeveloperConnectInsightsConfigArtifactConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de5b71eac959aa928759566e6b3375506e84b6bf904af7232d6b26b26918115(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e26d08e1a82ba1940739c0274b35069ed964cb87562a2641310933f3f5eafac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39afba5173cd733b88647abf1179812cdb3e192b9c5a1b9cf5fe71df0d86bf2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDeveloperConnectInsightsConfigArtifactConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37822d7238a38e9be2cfe64c407a3fabbf7d762bbc90be37d8ffa3908d059f42(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    app_hub_application: builtins.str,
    insights_config_id: builtins.str,
    location: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    artifact_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDeveloperConnectInsightsConfigArtifactConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDeveloperConnectInsightsConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28fd01cac898d050bc730b0fffaa9dfca53c3cc10f25573187fe94fdcfa45d2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f4d9672753902d66baa1e5196a5306c9a844169a59714edb62e9b965e37ce5a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40eb51428facd04dc91cca51b1ec1fddf195d4912494c45d2133f897eb0c7c2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca1d5dbf92a7f8242eb1495749fa9ed04ee0100030dc54fad269a6463056c12d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2547707ac07bfb33847589fe184cacc15b941d7d3f749c7c05b1b6cd90e79708(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44e82b30add16339e2e37fa8f84c79ec97927f7c54a009f5c669e4eb2188f9ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f9bae7455ca133558da28701ced3ec52496b97192ced0f766b88c2e97f294f0(
    value: typing.Optional[GoogleDeveloperConnectInsightsConfigErrorsDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8d04b4161fb582131bb460c946eb5c8e157445e06e3b418bc54e5a43c32b5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c609496eb574e34a0bebad816316d8e2aed144a31b11557da2236a93d1253674(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec3ec9762b910272fe623c61d2552f0c0b0e45449275daeee3ce56c59dc53e2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c298bdd6d3734d810101f57570e2f08c1e6347bb5220cba5259494b60f89a4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__facb649595cb2b57ce43aed6abe2a5e9dc89890ecb2db2a33e8401a6b1f95270(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__511a54e719acceee91b2a26281223a3030803e7783c96a2cd29a1b790b7ae79a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff85572e868d0d4008c6050c0cc456a5ecb4052b60005635e86952231f806f0(
    value: typing.Optional[GoogleDeveloperConnectInsightsConfigErrors],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d344d5cccd480dce754923c03332a189f7e77b5141289096bf83a6cfe734503a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f62ac0e0ebfa75edc71e530f71b336efdaadb51a7d419aec069a0a1da70636(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8512073e70ba9644eb8e683bae193dc8b5e6b502219cc561e2589a38b5d1f2fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d30a36aa9a132b0bd9c7d1e7e548cefb7a4fbd9513aa7878e25fffbd2951bd7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc9521cb7a7d6c04d2ef381283563067efe38ddf502f6f4c105182be500b4b41(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f2198605ea0362bf71ff41a4a528f147155f297b7a288565d1361ccf91eb758(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__240ada19343009ea25eb00ea2e3163e2056cc82c9a1ad3bbad9811e037cfae7a(
    value: typing.Optional[GoogleDeveloperConnectInsightsConfigRuntimeConfigsAppHubWorkload],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0191a03b963bdb742ecf0d5e1dc1720f27beb2c79016deb26fbfc1442ede57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86e6d5fbf48b0215048e0ee5b933e186a048a3da0e527001306e77e7d9462c47(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c7d39668651704f526be26299fb8c2297584c78e04ea4ff05ff5f1146dcc81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2059a551d49dd421d8f71de20628bb2c87098cc6b724f836289e1618c1300b75(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fe0fffbbaf3ded703e936a7711f11d74cc57897655982a912e39b45be1b4d6c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a2ca49eafcc3075878e8dbd3afb96dc2c34fc9f31dfeb91a7f6e6079ef95b61(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1099dad28ddcb95ede3349612eef6535d7afff0eaf64d568727cb458891ebe5(
    value: typing.Optional[GoogleDeveloperConnectInsightsConfigRuntimeConfigsGkeWorkload],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29b0793227d804ce28091317ed0786a2aa9fd9d68a0c93ff51228ab5586723b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c911a7c3f82163d8bed8199a7aa0c031a634e3081bf54fc9d65252df600fa8a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b20b75a26d09b7fc1046298693aedf31be8a7c8046f668e3ca8c4f4252bb7e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01876567b29dc0392d4464c9bf800abdd5d897b84ee6b4485aa5d7e47374d764(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49bc93a6b916a5c476ddda8aa436a8dbddfa29f0a709422b2e3131541b6cc687(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b263f9439038f98dc9a18c6aa94ad90a40ca22bb6b6e8d013990262648a31202(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__728e056582c52135a8f0251d50e910d66e4db20af4090bbb01835361cffe544e(
    value: typing.Optional[GoogleDeveloperConnectInsightsConfigRuntimeConfigs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa6b060123d182aea93a3fcb1c4c9d2f940d7a764da8ab7fc1f6c9017e3a22f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f0a53bab1c0ab1f5a7aa78cc6c9ce36e5b609f9ab8f470099c36be70582973(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1293f62dd6d99ad72f7eb4547d62e181301bd4e4b7538e43bde0d98dfebaaf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1401306e6815b6d2e0c566c4f86863b89c40cd4d0bcc6ffe43b212c4504635f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eead00ad1f4df16ae00f334e64420fb886482996e288983928ff02d14b1d928b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a64a70d68b0e0aa552ab225744f1d70027d251e58fd850e00e4f2e3a11deddcd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDeveloperConnectInsightsConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
