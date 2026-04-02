r'''
# `google_vertex_ai_endpoint_with_model_garden_deployment`

Refer to the Terraform Registry for docs: [`google_vertex_ai_endpoint_with_model_garden_deployment`](https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment).
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


class GoogleVertexAiEndpointWithModelGardenDeployment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeployment",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment google_vertex_ai_endpoint_with_model_garden_deployment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        deploy_config: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_config: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        hugging_face_model_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        model_config: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        publisher_model_name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment google_vertex_ai_endpoint_with_model_garden_deployment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Resource ID segment making up resource 'location'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#location GoogleVertexAiEndpointWithModelGardenDeployment#location}
        :param deploy_config: deploy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#deploy_config GoogleVertexAiEndpointWithModelGardenDeployment#deploy_config}
        :param endpoint_config: endpoint_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#endpoint_config GoogleVertexAiEndpointWithModelGardenDeployment#endpoint_config}
        :param hugging_face_model_id: The Hugging Face model to deploy. Format: Hugging Face model ID like 'google/gemma-2-2b-it'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#hugging_face_model_id GoogleVertexAiEndpointWithModelGardenDeployment#hugging_face_model_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#id GoogleVertexAiEndpointWithModelGardenDeployment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param model_config: model_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#model_config GoogleVertexAiEndpointWithModelGardenDeployment#model_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#project GoogleVertexAiEndpointWithModelGardenDeployment#project}.
        :param publisher_model_name: The Model Garden model to deploy. Format: 'publishers/{publisher}/models/{publisher_model}@{version_id}', or 'publishers/hf-{hugging-face-author}/models/{hugging-face-model-name}@001'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#publisher_model_name GoogleVertexAiEndpointWithModelGardenDeployment#publisher_model_name}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#timeouts GoogleVertexAiEndpointWithModelGardenDeployment#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e36345ae504a4576c9ba4b770802811e995e835d35bb3b289bf165930790f044)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleVertexAiEndpointWithModelGardenDeploymentConfig(
            location=location,
            deploy_config=deploy_config,
            endpoint_config=endpoint_config,
            hugging_face_model_id=hugging_face_model_id,
            id=id,
            model_config=model_config,
            project=project,
            publisher_model_name=publisher_model_name,
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
        '''Generates CDKTF code for importing a GoogleVertexAiEndpointWithModelGardenDeployment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleVertexAiEndpointWithModelGardenDeployment to import.
        :param import_from_id: The id of the existing GoogleVertexAiEndpointWithModelGardenDeployment that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleVertexAiEndpointWithModelGardenDeployment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab97e97ee3997a40957dfe189f61cb02f772b494f70322abe60a7ccb32704441)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDeployConfig")
    def put_deploy_config(
        self,
        *,
        dedicated_resources: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources", typing.Dict[builtins.str, typing.Any]]] = None,
        fast_tryout_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        system_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param dedicated_resources: dedicated_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#dedicated_resources GoogleVertexAiEndpointWithModelGardenDeployment#dedicated_resources}
        :param fast_tryout_enabled: If true, enable the QMT fast tryout feature for this model if possible. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#fast_tryout_enabled GoogleVertexAiEndpointWithModelGardenDeployment#fast_tryout_enabled}
        :param system_labels: System labels for Model Garden deployments. These labels are managed by Google and for tracking purposes only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#system_labels GoogleVertexAiEndpointWithModelGardenDeployment#system_labels}
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfig(
            dedicated_resources=dedicated_resources,
            fast_tryout_enabled=fast_tryout_enabled,
            system_labels=system_labels,
        )

        return typing.cast(None, jsii.invoke(self, "putDeployConfig", [value]))

    @jsii.member(jsii_name="putEndpointConfig")
    def put_endpoint_config(
        self,
        *,
        dedicated_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        endpoint_display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dedicated_endpoint_enabled: If true, the endpoint will be exposed through a dedicated DNS [Endpoint.dedicated_endpoint_dns]. Your request to the dedicated DNS will be isolated from other users' traffic and will have better performance and reliability. Note: Once you enabled dedicated endpoint, you won't be able to send request to the shared DNS {region}-aiplatform.googleapis.com. The limitations will be removed soon. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#dedicated_endpoint_enabled GoogleVertexAiEndpointWithModelGardenDeployment#dedicated_endpoint_enabled}
        :param endpoint_display_name: The user-specified display name of the endpoint. If not set, a default name will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#endpoint_display_name GoogleVertexAiEndpointWithModelGardenDeployment#endpoint_display_name}
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfig(
            dedicated_endpoint_enabled=dedicated_endpoint_enabled,
            endpoint_display_name=endpoint_display_name,
        )

        return typing.cast(None, jsii.invoke(self, "putEndpointConfig", [value]))

    @jsii.member(jsii_name="putModelConfig")
    def put_model_config(
        self,
        *,
        accept_eula: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        container_spec: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        hugging_face_access_token: typing.Optional[builtins.str] = None,
        hugging_face_cache_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        model_display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accept_eula: Whether the user accepts the End User License Agreement (EULA) for the model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#accept_eula GoogleVertexAiEndpointWithModelGardenDeployment#accept_eula}
        :param container_spec: container_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#container_spec GoogleVertexAiEndpointWithModelGardenDeployment#container_spec}
        :param hugging_face_access_token: The Hugging Face read access token used to access the model artifacts of gated models. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#hugging_face_access_token GoogleVertexAiEndpointWithModelGardenDeployment#hugging_face_access_token}
        :param hugging_face_cache_enabled: If true, the model will deploy with a cached version instead of directly downloading the model artifacts from Hugging Face. This is suitable for VPC-SC users with limited internet access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#hugging_face_cache_enabled GoogleVertexAiEndpointWithModelGardenDeployment#hugging_face_cache_enabled}
        :param model_display_name: The user-specified display name of the uploaded model. If not set, a default name will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#model_display_name GoogleVertexAiEndpointWithModelGardenDeployment#model_display_name}
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfig(
            accept_eula=accept_eula,
            container_spec=container_spec,
            hugging_face_access_token=hugging_face_access_token,
            hugging_face_cache_enabled=hugging_face_cache_enabled,
            model_display_name=model_display_name,
        )

        return typing.cast(None, jsii.invoke(self, "putModelConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#create GoogleVertexAiEndpointWithModelGardenDeployment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#delete GoogleVertexAiEndpointWithModelGardenDeployment#delete}.
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentTimeouts(
            create=create, delete=delete
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDeployConfig")
    def reset_deploy_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeployConfig", []))

    @jsii.member(jsii_name="resetEndpointConfig")
    def reset_endpoint_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointConfig", []))

    @jsii.member(jsii_name="resetHuggingFaceModelId")
    def reset_hugging_face_model_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHuggingFaceModelId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetModelConfig")
    def reset_model_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPublisherModelName")
    def reset_publisher_model_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublisherModelName", []))

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
    @jsii.member(jsii_name="deployConfig")
    def deploy_config(
        self,
    ) -> "GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigOutputReference":
        return typing.cast("GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigOutputReference", jsii.get(self, "deployConfig"))

    @builtins.property
    @jsii.member(jsii_name="deployedModelDisplayName")
    def deployed_model_display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deployedModelDisplayName"))

    @builtins.property
    @jsii.member(jsii_name="deployedModelId")
    def deployed_model_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deployedModelId"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="endpointConfig")
    def endpoint_config(
        self,
    ) -> "GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfigOutputReference":
        return typing.cast("GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfigOutputReference", jsii.get(self, "endpointConfig"))

    @builtins.property
    @jsii.member(jsii_name="modelConfig")
    def model_config(
        self,
    ) -> "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigOutputReference":
        return typing.cast("GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigOutputReference", jsii.get(self, "modelConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleVertexAiEndpointWithModelGardenDeploymentTimeoutsOutputReference":
        return typing.cast("GoogleVertexAiEndpointWithModelGardenDeploymentTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="deployConfigInput")
    def deploy_config_input(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfig"]:
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfig"], jsii.get(self, "deployConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointConfigInput")
    def endpoint_config_input(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfig"]:
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfig"], jsii.get(self, "endpointConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="huggingFaceModelIdInput")
    def hugging_face_model_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "huggingFaceModelIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="modelConfigInput")
    def model_config_input(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfig"]:
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfig"], jsii.get(self, "modelConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="publisherModelNameInput")
    def publisher_model_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publisherModelNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleVertexAiEndpointWithModelGardenDeploymentTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleVertexAiEndpointWithModelGardenDeploymentTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="huggingFaceModelId")
    def hugging_face_model_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "huggingFaceModelId"))

    @hugging_face_model_id.setter
    def hugging_face_model_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7d61c5a8fdea5d5fc7c730ad9e4a3f67b3befc6b2523a7be7b4f32a019c0264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "huggingFaceModelId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dc89a957dac0675224616c41bd2644f53365411de59e90eb3bd19f6c3652fc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7752cb99fe5bd6dd32b7edbd32bfce3822f6492d8b9a7b0465f8c0d409b0268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62aadee89fe3769e21e59ab8cadf5152730fbf17abc4dd9f01abed41580c2bb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publisherModelName")
    def publisher_model_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisherModelName"))

    @publisher_model_name.setter
    def publisher_model_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9cae99eb3b293d1aea926d4e235f73b21f854ef7257d51f97c232922efc6d74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publisherModelName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "deploy_config": "deployConfig",
        "endpoint_config": "endpointConfig",
        "hugging_face_model_id": "huggingFaceModelId",
        "id": "id",
        "model_config": "modelConfig",
        "project": "project",
        "publisher_model_name": "publisherModelName",
        "timeouts": "timeouts",
    },
)
class GoogleVertexAiEndpointWithModelGardenDeploymentConfig(
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
        location: builtins.str,
        deploy_config: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_config: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        hugging_face_model_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        model_config: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        publisher_model_name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Resource ID segment making up resource 'location'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#location GoogleVertexAiEndpointWithModelGardenDeployment#location}
        :param deploy_config: deploy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#deploy_config GoogleVertexAiEndpointWithModelGardenDeployment#deploy_config}
        :param endpoint_config: endpoint_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#endpoint_config GoogleVertexAiEndpointWithModelGardenDeployment#endpoint_config}
        :param hugging_face_model_id: The Hugging Face model to deploy. Format: Hugging Face model ID like 'google/gemma-2-2b-it'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#hugging_face_model_id GoogleVertexAiEndpointWithModelGardenDeployment#hugging_face_model_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#id GoogleVertexAiEndpointWithModelGardenDeployment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param model_config: model_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#model_config GoogleVertexAiEndpointWithModelGardenDeployment#model_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#project GoogleVertexAiEndpointWithModelGardenDeployment#project}.
        :param publisher_model_name: The Model Garden model to deploy. Format: 'publishers/{publisher}/models/{publisher_model}@{version_id}', or 'publishers/hf-{hugging-face-author}/models/{hugging-face-model-name}@001'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#publisher_model_name GoogleVertexAiEndpointWithModelGardenDeployment#publisher_model_name}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#timeouts GoogleVertexAiEndpointWithModelGardenDeployment#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(deploy_config, dict):
            deploy_config = GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfig(**deploy_config)
        if isinstance(endpoint_config, dict):
            endpoint_config = GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfig(**endpoint_config)
        if isinstance(model_config, dict):
            model_config = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfig(**model_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleVertexAiEndpointWithModelGardenDeploymentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fa8ad4a7727366f0f4663dca6b797fe19144b6ead9feb5aae8aded1e031de26)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument deploy_config", value=deploy_config, expected_type=type_hints["deploy_config"])
            check_type(argname="argument endpoint_config", value=endpoint_config, expected_type=type_hints["endpoint_config"])
            check_type(argname="argument hugging_face_model_id", value=hugging_face_model_id, expected_type=type_hints["hugging_face_model_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument model_config", value=model_config, expected_type=type_hints["model_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument publisher_model_name", value=publisher_model_name, expected_type=type_hints["publisher_model_name"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if deploy_config is not None:
            self._values["deploy_config"] = deploy_config
        if endpoint_config is not None:
            self._values["endpoint_config"] = endpoint_config
        if hugging_face_model_id is not None:
            self._values["hugging_face_model_id"] = hugging_face_model_id
        if id is not None:
            self._values["id"] = id
        if model_config is not None:
            self._values["model_config"] = model_config
        if project is not None:
            self._values["project"] = project
        if publisher_model_name is not None:
            self._values["publisher_model_name"] = publisher_model_name
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
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'location'. It identifies the resource within its parent collection as described in https://google.aip.dev/122.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#location GoogleVertexAiEndpointWithModelGardenDeployment#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deploy_config(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfig"]:
        '''deploy_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#deploy_config GoogleVertexAiEndpointWithModelGardenDeployment#deploy_config}
        '''
        result = self._values.get("deploy_config")
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfig"], result)

    @builtins.property
    def endpoint_config(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfig"]:
        '''endpoint_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#endpoint_config GoogleVertexAiEndpointWithModelGardenDeployment#endpoint_config}
        '''
        result = self._values.get("endpoint_config")
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfig"], result)

    @builtins.property
    def hugging_face_model_id(self) -> typing.Optional[builtins.str]:
        '''The Hugging Face model to deploy. Format: Hugging Face model ID like 'google/gemma-2-2b-it'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#hugging_face_model_id GoogleVertexAiEndpointWithModelGardenDeployment#hugging_face_model_id}
        '''
        result = self._values.get("hugging_face_model_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#id GoogleVertexAiEndpointWithModelGardenDeployment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model_config(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfig"]:
        '''model_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#model_config GoogleVertexAiEndpointWithModelGardenDeployment#model_config}
        '''
        result = self._values.get("model_config")
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#project GoogleVertexAiEndpointWithModelGardenDeployment#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publisher_model_name(self) -> typing.Optional[builtins.str]:
        '''The Model Garden model to deploy. Format: 'publishers/{publisher}/models/{publisher_model}@{version_id}', or 'publishers/hf-{hugging-face-author}/models/{hugging-face-model-name}@001'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#publisher_model_name GoogleVertexAiEndpointWithModelGardenDeployment#publisher_model_name}
        '''
        result = self._values.get("publisher_model_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#timeouts GoogleVertexAiEndpointWithModelGardenDeployment#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfig",
    jsii_struct_bases=[],
    name_mapping={
        "dedicated_resources": "dedicatedResources",
        "fast_tryout_enabled": "fastTryoutEnabled",
        "system_labels": "systemLabels",
    },
)
class GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfig:
    def __init__(
        self,
        *,
        dedicated_resources: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources", typing.Dict[builtins.str, typing.Any]]] = None,
        fast_tryout_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        system_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param dedicated_resources: dedicated_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#dedicated_resources GoogleVertexAiEndpointWithModelGardenDeployment#dedicated_resources}
        :param fast_tryout_enabled: If true, enable the QMT fast tryout feature for this model if possible. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#fast_tryout_enabled GoogleVertexAiEndpointWithModelGardenDeployment#fast_tryout_enabled}
        :param system_labels: System labels for Model Garden deployments. These labels are managed by Google and for tracking purposes only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#system_labels GoogleVertexAiEndpointWithModelGardenDeployment#system_labels}
        '''
        if isinstance(dedicated_resources, dict):
            dedicated_resources = GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources(**dedicated_resources)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45184ad8c53bde4aa50e99a4a6550bbe5f371bd46755e58cacd08610046508c0)
            check_type(argname="argument dedicated_resources", value=dedicated_resources, expected_type=type_hints["dedicated_resources"])
            check_type(argname="argument fast_tryout_enabled", value=fast_tryout_enabled, expected_type=type_hints["fast_tryout_enabled"])
            check_type(argname="argument system_labels", value=system_labels, expected_type=type_hints["system_labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dedicated_resources is not None:
            self._values["dedicated_resources"] = dedicated_resources
        if fast_tryout_enabled is not None:
            self._values["fast_tryout_enabled"] = fast_tryout_enabled
        if system_labels is not None:
            self._values["system_labels"] = system_labels

    @builtins.property
    def dedicated_resources(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources"]:
        '''dedicated_resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#dedicated_resources GoogleVertexAiEndpointWithModelGardenDeployment#dedicated_resources}
        '''
        result = self._values.get("dedicated_resources")
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources"], result)

    @builtins.property
    def fast_tryout_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, enable the QMT fast tryout feature for this model if possible.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#fast_tryout_enabled GoogleVertexAiEndpointWithModelGardenDeployment#fast_tryout_enabled}
        '''
        result = self._values.get("fast_tryout_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def system_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''System labels for Model Garden deployments. These labels are managed by Google and for tracking purposes only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#system_labels GoogleVertexAiEndpointWithModelGardenDeployment#system_labels}
        '''
        result = self._values.get("system_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources",
    jsii_struct_bases=[],
    name_mapping={
        "machine_spec": "machineSpec",
        "min_replica_count": "minReplicaCount",
        "autoscaling_metric_specs": "autoscalingMetricSpecs",
        "max_replica_count": "maxReplicaCount",
        "required_replica_count": "requiredReplicaCount",
        "spot": "spot",
    },
)
class GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources:
    def __init__(
        self,
        *,
        machine_spec: typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec", typing.Dict[builtins.str, typing.Any]],
        min_replica_count: jsii.Number,
        autoscaling_metric_specs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_replica_count: typing.Optional[jsii.Number] = None,
        required_replica_count: typing.Optional[jsii.Number] = None,
        spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param machine_spec: machine_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#machine_spec GoogleVertexAiEndpointWithModelGardenDeployment#machine_spec}
        :param min_replica_count: The minimum number of machine replicas that will be always deployed on. This value must be greater than or equal to 1. If traffic increases, it may dynamically be deployed onto more replicas, and as traffic decreases, some of these extra replicas may be freed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#min_replica_count GoogleVertexAiEndpointWithModelGardenDeployment#min_replica_count}
        :param autoscaling_metric_specs: autoscaling_metric_specs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#autoscaling_metric_specs GoogleVertexAiEndpointWithModelGardenDeployment#autoscaling_metric_specs}
        :param max_replica_count: The maximum number of replicas that may be deployed on when the traffic against it increases. If the requested value is too large, the deployment will error, but if deployment succeeds then the ability to scale to that many replicas is guaranteed (barring service outages). If traffic increases beyond what its replicas at maximum may handle, a portion of the traffic will be dropped. If this value is not provided, will use min_replica_count as the default value. The value of this field impacts the charge against Vertex CPU and GPU quotas. Specifically, you will be charged for (max_replica_count * number of cores in the selected machine type) and (max_replica_count * number of GPUs per replica in the selected machine type). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#max_replica_count GoogleVertexAiEndpointWithModelGardenDeployment#max_replica_count}
        :param required_replica_count: Number of required available replicas for the deployment to succeed. This field is only needed when partial deployment/mutation is desired. If set, the deploy/mutate operation will succeed once available_replica_count reaches required_replica_count, and the rest of the replicas will be retried. If not set, the default required_replica_count will be min_replica_count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#required_replica_count GoogleVertexAiEndpointWithModelGardenDeployment#required_replica_count}
        :param spot: If true, schedule the deployment workload on `spot VMs <https://cloud.google.com/kubernetes-engine/docs/concepts/spot-vms>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#spot GoogleVertexAiEndpointWithModelGardenDeployment#spot}
        '''
        if isinstance(machine_spec, dict):
            machine_spec = GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec(**machine_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74a1edbea95f0baab86e3959cce20def457c0c65137b3d3c7a9f6053d4ca7b7b)
            check_type(argname="argument machine_spec", value=machine_spec, expected_type=type_hints["machine_spec"])
            check_type(argname="argument min_replica_count", value=min_replica_count, expected_type=type_hints["min_replica_count"])
            check_type(argname="argument autoscaling_metric_specs", value=autoscaling_metric_specs, expected_type=type_hints["autoscaling_metric_specs"])
            check_type(argname="argument max_replica_count", value=max_replica_count, expected_type=type_hints["max_replica_count"])
            check_type(argname="argument required_replica_count", value=required_replica_count, expected_type=type_hints["required_replica_count"])
            check_type(argname="argument spot", value=spot, expected_type=type_hints["spot"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "machine_spec": machine_spec,
            "min_replica_count": min_replica_count,
        }
        if autoscaling_metric_specs is not None:
            self._values["autoscaling_metric_specs"] = autoscaling_metric_specs
        if max_replica_count is not None:
            self._values["max_replica_count"] = max_replica_count
        if required_replica_count is not None:
            self._values["required_replica_count"] = required_replica_count
        if spot is not None:
            self._values["spot"] = spot

    @builtins.property
    def machine_spec(
        self,
    ) -> "GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec":
        '''machine_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#machine_spec GoogleVertexAiEndpointWithModelGardenDeployment#machine_spec}
        '''
        result = self._values.get("machine_spec")
        assert result is not None, "Required property 'machine_spec' is missing"
        return typing.cast("GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec", result)

    @builtins.property
    def min_replica_count(self) -> jsii.Number:
        '''The minimum number of machine replicas that will be always deployed on.

        This value must be greater than or equal to 1.

        If traffic increases, it may dynamically be deployed onto more replicas,
        and as traffic decreases, some of these extra replicas may be freed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#min_replica_count GoogleVertexAiEndpointWithModelGardenDeployment#min_replica_count}
        '''
        result = self._values.get("min_replica_count")
        assert result is not None, "Required property 'min_replica_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def autoscaling_metric_specs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs"]]]:
        '''autoscaling_metric_specs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#autoscaling_metric_specs GoogleVertexAiEndpointWithModelGardenDeployment#autoscaling_metric_specs}
        '''
        result = self._values.get("autoscaling_metric_specs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs"]]], result)

    @builtins.property
    def max_replica_count(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of replicas that may be deployed on when the traffic against it increases.

        If the requested value is too large, the deployment
        will error, but if deployment succeeds then the ability to scale to that
        many replicas is guaranteed (barring service outages). If traffic increases
        beyond what its replicas at maximum may handle, a portion of the traffic
        will be dropped. If this value is not provided, will use
        min_replica_count as the default value.

        The value of this field impacts the charge against Vertex CPU and GPU
        quotas. Specifically, you will be charged for (max_replica_count *
        number of cores in the selected machine type) and (max_replica_count *
        number of GPUs per replica in the selected machine type).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#max_replica_count GoogleVertexAiEndpointWithModelGardenDeployment#max_replica_count}
        '''
        result = self._values.get("max_replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def required_replica_count(self) -> typing.Optional[jsii.Number]:
        '''Number of required available replicas for the deployment to succeed.

        This field is only needed when partial deployment/mutation is
        desired. If set, the deploy/mutate operation will succeed once
        available_replica_count reaches required_replica_count, and the rest of
        the replicas will be retried. If not set, the default
        required_replica_count will be min_replica_count.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#required_replica_count GoogleVertexAiEndpointWithModelGardenDeployment#required_replica_count}
        '''
        result = self._values.get("required_replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def spot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, schedule the deployment workload on `spot VMs <https://cloud.google.com/kubernetes-engine/docs/concepts/spot-vms>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#spot GoogleVertexAiEndpointWithModelGardenDeployment#spot}
        '''
        result = self._values.get("spot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs",
    jsii_struct_bases=[],
    name_mapping={"metric_name": "metricName", "target": "target"},
)
class GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs:
    def __init__(
        self,
        *,
        metric_name: builtins.str,
        target: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metric_name: The resource metric name. Supported metrics:. - For Online Prediction: - 'aiplatform.googleapis.com/prediction/online/accelerator/duty_cycle' - 'aiplatform.googleapis.com/prediction/online/cpu/utilization' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#metric_name GoogleVertexAiEndpointWithModelGardenDeployment#metric_name}
        :param target: The target resource utilization in percentage (1% - 100%) for the given metric; once the real usage deviates from the target by a certain percentage, the machine replicas change. The default value is 60 (representing 60%) if not provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#target GoogleVertexAiEndpointWithModelGardenDeployment#target}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08daef2643beac7b8547479c1e8959f0356cec1425c347ec3c5d95c7c14f6a57)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric_name": metric_name,
        }
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''The resource metric name. Supported metrics:.

        - For Online Prediction:
        - 'aiplatform.googleapis.com/prediction/online/accelerator/duty_cycle'
        - 'aiplatform.googleapis.com/prediction/online/cpu/utilization'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#metric_name GoogleVertexAiEndpointWithModelGardenDeployment#metric_name}
        '''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> typing.Optional[jsii.Number]:
        '''The target resource utilization in percentage (1% - 100%) for the given metric;

        once the real usage deviates from the target by a certain
        percentage, the machine replicas change. The default value is 60
        (representing 60%) if not provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#target GoogleVertexAiEndpointWithModelGardenDeployment#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fd253b05e4e0cf577e9b7549004b0814ffe48ffd455348ded2c762df1ba27ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35670e29ffda3ef005f79e2a4e4ffbd7c94b3e10d6c1f9cd118f40beade3d828)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f17f499ad46fcebe3ed634342edb042205b6f5cbb93c7066793744524453804c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66e4654ab6c52f614f7100d802e926fc85e206f94bf642a5120875a29b4105e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf0bd2c7a0224f5065efb269ff4177298e3c4d02ba441434b9d9198fbce8eca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a376ec9b23f75cc0ed37ab7f9821545bffb8adfed23820e2b5dfdfeb2efc3b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d42d49516f05ff409fb25464d4d4576cfad338ac881d36a35819bad72234ff7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @builtins.property
    @jsii.member(jsii_name="metricNameInput")
    def metric_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricNameInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricName"))

    @metric_name.setter
    def metric_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__479b900b24435f33dedefa02c4987d6734323fc793ca6d5f3659841cfb83b5bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "target"))

    @target.setter
    def target(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__957bad2182f1c3c68551db7f3995d3705e0344e0688a92594e03eb9dcd9a1333)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f2d0b5041a37cbe1b8d8cae681886a78bffa0074d90b7821584a1126d968b87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_count": "acceleratorCount",
        "accelerator_type": "acceleratorType",
        "machine_type": "machineType",
        "multihost_gpu_node_count": "multihostGpuNodeCount",
        "reservation_affinity": "reservationAffinity",
        "tpu_topology": "tpuTopology",
    },
)
class GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec:
    def __init__(
        self,
        *,
        accelerator_count: typing.Optional[jsii.Number] = None,
        accelerator_type: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        multihost_gpu_node_count: typing.Optional[jsii.Number] = None,
        reservation_affinity: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
        tpu_topology: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerator_count: The number of accelerators to attach to the machine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#accelerator_count GoogleVertexAiEndpointWithModelGardenDeployment#accelerator_count}
        :param accelerator_type: Possible values: ACCELERATOR_TYPE_UNSPECIFIED NVIDIA_TESLA_K80 NVIDIA_TESLA_P100 NVIDIA_TESLA_V100 NVIDIA_TESLA_P4 NVIDIA_TESLA_T4 NVIDIA_TESLA_A100 NVIDIA_A100_80GB NVIDIA_L4 NVIDIA_H100_80GB NVIDIA_H100_MEGA_80GB NVIDIA_H200_141GB NVIDIA_B200 TPU_V2 TPU_V3 TPU_V4_POD TPU_V5_LITEPOD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#accelerator_type GoogleVertexAiEndpointWithModelGardenDeployment#accelerator_type}
        :param machine_type: The type of the machine. See the `list of machine types supported for prediction <https://cloud.google.com/vertex-ai/docs/predictions/configure-compute#machine-types>`_ See the `list of machine types supported for custom training <https://cloud.google.com/vertex-ai/docs/training/configure-compute#machine-types>`_. For DeployedModel this field is optional, and the default value is 'n1-standard-2'. For BatchPredictionJob or as part of WorkerPoolSpec this field is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#machine_type GoogleVertexAiEndpointWithModelGardenDeployment#machine_type}
        :param multihost_gpu_node_count: The number of nodes per replica for multihost GPU deployments. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#multihost_gpu_node_count GoogleVertexAiEndpointWithModelGardenDeployment#multihost_gpu_node_count}
        :param reservation_affinity: reservation_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#reservation_affinity GoogleVertexAiEndpointWithModelGardenDeployment#reservation_affinity}
        :param tpu_topology: The topology of the TPUs. Corresponds to the TPU topologies available from GKE. (Example: tpu_topology: "2x2x1"). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#tpu_topology GoogleVertexAiEndpointWithModelGardenDeployment#tpu_topology}
        '''
        if isinstance(reservation_affinity, dict):
            reservation_affinity = GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity(**reservation_affinity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e65ec7f9af2b52baf19b82b419afc8e92ed7b80b14d124194dc3a81f334e5de)
            check_type(argname="argument accelerator_count", value=accelerator_count, expected_type=type_hints["accelerator_count"])
            check_type(argname="argument accelerator_type", value=accelerator_type, expected_type=type_hints["accelerator_type"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument multihost_gpu_node_count", value=multihost_gpu_node_count, expected_type=type_hints["multihost_gpu_node_count"])
            check_type(argname="argument reservation_affinity", value=reservation_affinity, expected_type=type_hints["reservation_affinity"])
            check_type(argname="argument tpu_topology", value=tpu_topology, expected_type=type_hints["tpu_topology"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerator_count is not None:
            self._values["accelerator_count"] = accelerator_count
        if accelerator_type is not None:
            self._values["accelerator_type"] = accelerator_type
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if multihost_gpu_node_count is not None:
            self._values["multihost_gpu_node_count"] = multihost_gpu_node_count
        if reservation_affinity is not None:
            self._values["reservation_affinity"] = reservation_affinity
        if tpu_topology is not None:
            self._values["tpu_topology"] = tpu_topology

    @builtins.property
    def accelerator_count(self) -> typing.Optional[jsii.Number]:
        '''The number of accelerators to attach to the machine.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#accelerator_count GoogleVertexAiEndpointWithModelGardenDeployment#accelerator_count}
        '''
        result = self._values.get("accelerator_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def accelerator_type(self) -> typing.Optional[builtins.str]:
        '''Possible values: ACCELERATOR_TYPE_UNSPECIFIED NVIDIA_TESLA_K80 NVIDIA_TESLA_P100 NVIDIA_TESLA_V100 NVIDIA_TESLA_P4 NVIDIA_TESLA_T4 NVIDIA_TESLA_A100 NVIDIA_A100_80GB NVIDIA_L4 NVIDIA_H100_80GB NVIDIA_H100_MEGA_80GB NVIDIA_H200_141GB NVIDIA_B200 TPU_V2 TPU_V3 TPU_V4_POD TPU_V5_LITEPOD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#accelerator_type GoogleVertexAiEndpointWithModelGardenDeployment#accelerator_type}
        '''
        result = self._values.get("accelerator_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The type of the machine.

        See the `list of machine types supported for
        prediction <https://cloud.google.com/vertex-ai/docs/predictions/configure-compute#machine-types>`_

        See the `list of machine types supported for custom
        training <https://cloud.google.com/vertex-ai/docs/training/configure-compute#machine-types>`_.

        For DeployedModel this field is optional, and the default
        value is 'n1-standard-2'. For BatchPredictionJob or as part of
        WorkerPoolSpec this field is required.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#machine_type GoogleVertexAiEndpointWithModelGardenDeployment#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multihost_gpu_node_count(self) -> typing.Optional[jsii.Number]:
        '''The number of nodes per replica for multihost GPU deployments.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#multihost_gpu_node_count GoogleVertexAiEndpointWithModelGardenDeployment#multihost_gpu_node_count}
        '''
        result = self._values.get("multihost_gpu_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def reservation_affinity(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity"]:
        '''reservation_affinity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#reservation_affinity GoogleVertexAiEndpointWithModelGardenDeployment#reservation_affinity}
        '''
        result = self._values.get("reservation_affinity")
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity"], result)

    @builtins.property
    def tpu_topology(self) -> typing.Optional[builtins.str]:
        '''The topology of the TPUs. Corresponds to the TPU topologies available from GKE. (Example: tpu_topology: "2x2x1").

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#tpu_topology GoogleVertexAiEndpointWithModelGardenDeployment#tpu_topology}
        '''
        result = self._values.get("tpu_topology")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48e521d27cf176d7699d38eeb616c9ea32b490006de902cc28f04173a25828df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putReservationAffinity")
    def put_reservation_affinity(
        self,
        *,
        reservation_affinity_type: builtins.str,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param reservation_affinity_type: Specifies the reservation affinity type. Possible values: TYPE_UNSPECIFIED NO_RESERVATION ANY_RESERVATION SPECIFIC_RESERVATION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#reservation_affinity_type GoogleVertexAiEndpointWithModelGardenDeployment#reservation_affinity_type}
        :param key: Corresponds to the label key of a reservation resource. To target a SPECIFIC_RESERVATION by name, use 'compute.googleapis.com/reservation-name' as the key and specify the name of your reservation as its value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#key GoogleVertexAiEndpointWithModelGardenDeployment#key}
        :param values: Corresponds to the label values of a reservation resource. This must be the full resource name of the reservation or reservation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#values GoogleVertexAiEndpointWithModelGardenDeployment#values}
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity(
            reservation_affinity_type=reservation_affinity_type, key=key, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putReservationAffinity", [value]))

    @jsii.member(jsii_name="resetAcceleratorCount")
    def reset_accelerator_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorCount", []))

    @jsii.member(jsii_name="resetAcceleratorType")
    def reset_accelerator_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorType", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetMultihostGpuNodeCount")
    def reset_multihost_gpu_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultihostGpuNodeCount", []))

    @jsii.member(jsii_name="resetReservationAffinity")
    def reset_reservation_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservationAffinity", []))

    @jsii.member(jsii_name="resetTpuTopology")
    def reset_tpu_topology(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpuTopology", []))

    @builtins.property
    @jsii.member(jsii_name="reservationAffinity")
    def reservation_affinity(
        self,
    ) -> "GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinityOutputReference":
        return typing.cast("GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinityOutputReference", jsii.get(self, "reservationAffinity"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorCountInput")
    def accelerator_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "acceleratorCountInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTypeInput")
    def accelerator_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceleratorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="multihostGpuNodeCountInput")
    def multihost_gpu_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "multihostGpuNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="reservationAffinityInput")
    def reservation_affinity_input(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity"]:
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity"], jsii.get(self, "reservationAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="tpuTopologyInput")
    def tpu_topology_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tpuTopologyInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorCount")
    def accelerator_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "acceleratorCount"))

    @accelerator_count.setter
    def accelerator_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17ffab9b2a4605e30e50f89ab36f67383eaf0ae76d4e4c0d052c953fdf8e64f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d17591c39a8e5ad250fb4af7c23252d6f4bc1ba6c3156ec1c353343b7f30ad65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f79c123d782f7f025f536706ca0782b1fe43e4ea028b3c3cf30e0c07da8cb47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multihostGpuNodeCount")
    def multihost_gpu_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "multihostGpuNodeCount"))

    @multihost_gpu_node_count.setter
    def multihost_gpu_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57d423b65008003fdb293e772e92367c0aae71adbe42fc3a2868b3b50be8cde2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multihostGpuNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tpuTopology")
    def tpu_topology(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpuTopology"))

    @tpu_topology.setter
    def tpu_topology(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd4e34d91ec6dd74d5f3fb7152177b7495e58114f3b9907fe551d46e9387c0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpuTopology", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b807d7ec9a6abefa735716bf342ed5afed62ad736e02a1d19579444af45ed0ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity",
    jsii_struct_bases=[],
    name_mapping={
        "reservation_affinity_type": "reservationAffinityType",
        "key": "key",
        "values": "values",
    },
)
class GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity:
    def __init__(
        self,
        *,
        reservation_affinity_type: builtins.str,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param reservation_affinity_type: Specifies the reservation affinity type. Possible values: TYPE_UNSPECIFIED NO_RESERVATION ANY_RESERVATION SPECIFIC_RESERVATION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#reservation_affinity_type GoogleVertexAiEndpointWithModelGardenDeployment#reservation_affinity_type}
        :param key: Corresponds to the label key of a reservation resource. To target a SPECIFIC_RESERVATION by name, use 'compute.googleapis.com/reservation-name' as the key and specify the name of your reservation as its value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#key GoogleVertexAiEndpointWithModelGardenDeployment#key}
        :param values: Corresponds to the label values of a reservation resource. This must be the full resource name of the reservation or reservation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#values GoogleVertexAiEndpointWithModelGardenDeployment#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4753ce0a499f4fb8236fae62be03ea78e0bd58568bd7e9c86c4e910ad3295ff4)
            check_type(argname="argument reservation_affinity_type", value=reservation_affinity_type, expected_type=type_hints["reservation_affinity_type"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "reservation_affinity_type": reservation_affinity_type,
        }
        if key is not None:
            self._values["key"] = key
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def reservation_affinity_type(self) -> builtins.str:
        '''Specifies the reservation affinity type. Possible values: TYPE_UNSPECIFIED NO_RESERVATION ANY_RESERVATION SPECIFIC_RESERVATION.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#reservation_affinity_type GoogleVertexAiEndpointWithModelGardenDeployment#reservation_affinity_type}
        '''
        result = self._values.get("reservation_affinity_type")
        assert result is not None, "Required property 'reservation_affinity_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Corresponds to the label key of a reservation resource.

        To target a
        SPECIFIC_RESERVATION by name, use 'compute.googleapis.com/reservation-name'
        as the key and specify the name of your reservation as its value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#key GoogleVertexAiEndpointWithModelGardenDeployment#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Corresponds to the label values of a reservation resource.

        This must be the
        full resource name of the reservation or reservation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#values GoogleVertexAiEndpointWithModelGardenDeployment#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3574bcc42975f7e410cae1377f869276b8a519c2fbf93f47a4650bab30908544)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="reservationAffinityTypeInput")
    def reservation_affinity_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reservationAffinityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65ffd6f467aa03fff23131c8fd577561fbc8a6f5ae076faf5498340b766afad1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reservationAffinityType")
    def reservation_affinity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reservationAffinityType"))

    @reservation_affinity_type.setter
    def reservation_affinity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a2a18368ea52f7b3dad6e7518c4c4a228a719437fdec58bd8c9637eda7a6447)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservationAffinityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19c2a5ea4c5c2a71b32dd23c5baa7f2346be53b94c64375b49acfc29ec7b829b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e92ac375a5f9777d8ff7ce7a37883219eb0d7ae5468f829ae763afa454f9c710)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3367ac31026afcf7d46b066b9cd2096735bb3f7cb1dd37b30c998562c70a582)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscalingMetricSpecs")
    def put_autoscaling_metric_specs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd038719acc0643dac7c85bace9e20d576805a7c59f5180f1254d0df4a71be6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAutoscalingMetricSpecs", [value]))

    @jsii.member(jsii_name="putMachineSpec")
    def put_machine_spec(
        self,
        *,
        accelerator_count: typing.Optional[jsii.Number] = None,
        accelerator_type: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        multihost_gpu_node_count: typing.Optional[jsii.Number] = None,
        reservation_affinity: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
        tpu_topology: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerator_count: The number of accelerators to attach to the machine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#accelerator_count GoogleVertexAiEndpointWithModelGardenDeployment#accelerator_count}
        :param accelerator_type: Possible values: ACCELERATOR_TYPE_UNSPECIFIED NVIDIA_TESLA_K80 NVIDIA_TESLA_P100 NVIDIA_TESLA_V100 NVIDIA_TESLA_P4 NVIDIA_TESLA_T4 NVIDIA_TESLA_A100 NVIDIA_A100_80GB NVIDIA_L4 NVIDIA_H100_80GB NVIDIA_H100_MEGA_80GB NVIDIA_H200_141GB NVIDIA_B200 TPU_V2 TPU_V3 TPU_V4_POD TPU_V5_LITEPOD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#accelerator_type GoogleVertexAiEndpointWithModelGardenDeployment#accelerator_type}
        :param machine_type: The type of the machine. See the `list of machine types supported for prediction <https://cloud.google.com/vertex-ai/docs/predictions/configure-compute#machine-types>`_ See the `list of machine types supported for custom training <https://cloud.google.com/vertex-ai/docs/training/configure-compute#machine-types>`_. For DeployedModel this field is optional, and the default value is 'n1-standard-2'. For BatchPredictionJob or as part of WorkerPoolSpec this field is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#machine_type GoogleVertexAiEndpointWithModelGardenDeployment#machine_type}
        :param multihost_gpu_node_count: The number of nodes per replica for multihost GPU deployments. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#multihost_gpu_node_count GoogleVertexAiEndpointWithModelGardenDeployment#multihost_gpu_node_count}
        :param reservation_affinity: reservation_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#reservation_affinity GoogleVertexAiEndpointWithModelGardenDeployment#reservation_affinity}
        :param tpu_topology: The topology of the TPUs. Corresponds to the TPU topologies available from GKE. (Example: tpu_topology: "2x2x1"). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#tpu_topology GoogleVertexAiEndpointWithModelGardenDeployment#tpu_topology}
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec(
            accelerator_count=accelerator_count,
            accelerator_type=accelerator_type,
            machine_type=machine_type,
            multihost_gpu_node_count=multihost_gpu_node_count,
            reservation_affinity=reservation_affinity,
            tpu_topology=tpu_topology,
        )

        return typing.cast(None, jsii.invoke(self, "putMachineSpec", [value]))

    @jsii.member(jsii_name="resetAutoscalingMetricSpecs")
    def reset_autoscaling_metric_specs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscalingMetricSpecs", []))

    @jsii.member(jsii_name="resetMaxReplicaCount")
    def reset_max_replica_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxReplicaCount", []))

    @jsii.member(jsii_name="resetRequiredReplicaCount")
    def reset_required_replica_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredReplicaCount", []))

    @jsii.member(jsii_name="resetSpot")
    def reset_spot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpot", []))

    @builtins.property
    @jsii.member(jsii_name="autoscalingMetricSpecs")
    def autoscaling_metric_specs(
        self,
    ) -> GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecsList:
        return typing.cast(GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecsList, jsii.get(self, "autoscalingMetricSpecs"))

    @builtins.property
    @jsii.member(jsii_name="machineSpec")
    def machine_spec(
        self,
    ) -> GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecOutputReference:
        return typing.cast(GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecOutputReference, jsii.get(self, "machineSpec"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingMetricSpecsInput")
    def autoscaling_metric_specs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs]]], jsii.get(self, "autoscalingMetricSpecsInput"))

    @builtins.property
    @jsii.member(jsii_name="machineSpecInput")
    def machine_spec_input(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec], jsii.get(self, "machineSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="maxReplicaCountInput")
    def max_replica_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxReplicaCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minReplicaCountInput")
    def min_replica_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minReplicaCountInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredReplicaCountInput")
    def required_replica_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "requiredReplicaCountInput"))

    @builtins.property
    @jsii.member(jsii_name="spotInput")
    def spot_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "spotInput"))

    @builtins.property
    @jsii.member(jsii_name="maxReplicaCount")
    def max_replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxReplicaCount"))

    @max_replica_count.setter
    def max_replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ea4b506e296db0a28d41d5d8896754f1aa3bea43825d43ea7344b6cda62d0e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxReplicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minReplicaCount")
    def min_replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReplicaCount"))

    @min_replica_count.setter
    def min_replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57f1fc0dee805b4055752d1b440cc9e60afeda26d6325ab21ed0d3ae85d788ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minReplicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requiredReplicaCount")
    def required_replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "requiredReplicaCount"))

    @required_replica_count.setter
    def required_replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb1cc2e0725f74767cc1050d031f4c6b4b1e9d19fad0fee6f559f86fcbd2ef5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiredReplicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="spot")
    def spot(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "spot"))

    @spot.setter
    def spot(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3216683f0095f8b9c5f0272c04fa260bb15f96b7ddc3067220ca53dd5f9533c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cff0dd3fd8241a4a444c1263b7e6172baebc33d3bf7526c580b922c7002f138a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a63b83c32275e238e3334202c31d91fdbccc6a90194eaa5809fed0dc4f276698)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDedicatedResources")
    def put_dedicated_resources(
        self,
        *,
        machine_spec: typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec, typing.Dict[builtins.str, typing.Any]],
        min_replica_count: jsii.Number,
        autoscaling_metric_specs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs, typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_replica_count: typing.Optional[jsii.Number] = None,
        required_replica_count: typing.Optional[jsii.Number] = None,
        spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param machine_spec: machine_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#machine_spec GoogleVertexAiEndpointWithModelGardenDeployment#machine_spec}
        :param min_replica_count: The minimum number of machine replicas that will be always deployed on. This value must be greater than or equal to 1. If traffic increases, it may dynamically be deployed onto more replicas, and as traffic decreases, some of these extra replicas may be freed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#min_replica_count GoogleVertexAiEndpointWithModelGardenDeployment#min_replica_count}
        :param autoscaling_metric_specs: autoscaling_metric_specs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#autoscaling_metric_specs GoogleVertexAiEndpointWithModelGardenDeployment#autoscaling_metric_specs}
        :param max_replica_count: The maximum number of replicas that may be deployed on when the traffic against it increases. If the requested value is too large, the deployment will error, but if deployment succeeds then the ability to scale to that many replicas is guaranteed (barring service outages). If traffic increases beyond what its replicas at maximum may handle, a portion of the traffic will be dropped. If this value is not provided, will use min_replica_count as the default value. The value of this field impacts the charge against Vertex CPU and GPU quotas. Specifically, you will be charged for (max_replica_count * number of cores in the selected machine type) and (max_replica_count * number of GPUs per replica in the selected machine type). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#max_replica_count GoogleVertexAiEndpointWithModelGardenDeployment#max_replica_count}
        :param required_replica_count: Number of required available replicas for the deployment to succeed. This field is only needed when partial deployment/mutation is desired. If set, the deploy/mutate operation will succeed once available_replica_count reaches required_replica_count, and the rest of the replicas will be retried. If not set, the default required_replica_count will be min_replica_count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#required_replica_count GoogleVertexAiEndpointWithModelGardenDeployment#required_replica_count}
        :param spot: If true, schedule the deployment workload on `spot VMs <https://cloud.google.com/kubernetes-engine/docs/concepts/spot-vms>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#spot GoogleVertexAiEndpointWithModelGardenDeployment#spot}
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources(
            machine_spec=machine_spec,
            min_replica_count=min_replica_count,
            autoscaling_metric_specs=autoscaling_metric_specs,
            max_replica_count=max_replica_count,
            required_replica_count=required_replica_count,
            spot=spot,
        )

        return typing.cast(None, jsii.invoke(self, "putDedicatedResources", [value]))

    @jsii.member(jsii_name="resetDedicatedResources")
    def reset_dedicated_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDedicatedResources", []))

    @jsii.member(jsii_name="resetFastTryoutEnabled")
    def reset_fast_tryout_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFastTryoutEnabled", []))

    @jsii.member(jsii_name="resetSystemLabels")
    def reset_system_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemLabels", []))

    @builtins.property
    @jsii.member(jsii_name="dedicatedResources")
    def dedicated_resources(
        self,
    ) -> GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesOutputReference:
        return typing.cast(GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesOutputReference, jsii.get(self, "dedicatedResources"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedResourcesInput")
    def dedicated_resources_input(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources], jsii.get(self, "dedicatedResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="fastTryoutEnabledInput")
    def fast_tryout_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fastTryoutEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="systemLabelsInput")
    def system_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "systemLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="fastTryoutEnabled")
    def fast_tryout_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fastTryoutEnabled"))

    @fast_tryout_enabled.setter
    def fast_tryout_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8956a0421257e4ec681bc7f25a19bcd4a47d08ab01312dab7e7eda7590e56519)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fastTryoutEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemLabels")
    def system_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "systemLabels"))

    @system_labels.setter
    def system_labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1658cd0626a2e1987d6656e1004c93f9a03f754bace9d2bea96ced3c70fa4458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__138510dff63d92ec51f9f91324518d456617b59cc492a2cfbbcdf0ce66c48b57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfig",
    jsii_struct_bases=[],
    name_mapping={
        "dedicated_endpoint_enabled": "dedicatedEndpointEnabled",
        "endpoint_display_name": "endpointDisplayName",
    },
)
class GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfig:
    def __init__(
        self,
        *,
        dedicated_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        endpoint_display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dedicated_endpoint_enabled: If true, the endpoint will be exposed through a dedicated DNS [Endpoint.dedicated_endpoint_dns]. Your request to the dedicated DNS will be isolated from other users' traffic and will have better performance and reliability. Note: Once you enabled dedicated endpoint, you won't be able to send request to the shared DNS {region}-aiplatform.googleapis.com. The limitations will be removed soon. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#dedicated_endpoint_enabled GoogleVertexAiEndpointWithModelGardenDeployment#dedicated_endpoint_enabled}
        :param endpoint_display_name: The user-specified display name of the endpoint. If not set, a default name will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#endpoint_display_name GoogleVertexAiEndpointWithModelGardenDeployment#endpoint_display_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea007539474fe556a679c57d89c5a036d2d2ede16dbc19436168294dec4875d1)
            check_type(argname="argument dedicated_endpoint_enabled", value=dedicated_endpoint_enabled, expected_type=type_hints["dedicated_endpoint_enabled"])
            check_type(argname="argument endpoint_display_name", value=endpoint_display_name, expected_type=type_hints["endpoint_display_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dedicated_endpoint_enabled is not None:
            self._values["dedicated_endpoint_enabled"] = dedicated_endpoint_enabled
        if endpoint_display_name is not None:
            self._values["endpoint_display_name"] = endpoint_display_name

    @builtins.property
    def dedicated_endpoint_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the endpoint will be exposed through a dedicated DNS [Endpoint.dedicated_endpoint_dns]. Your request to the dedicated DNS will be isolated from other users' traffic and will have better performance and reliability. Note: Once you enabled dedicated endpoint, you won't be able to send request to the shared DNS {region}-aiplatform.googleapis.com. The limitations will be removed soon.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#dedicated_endpoint_enabled GoogleVertexAiEndpointWithModelGardenDeployment#dedicated_endpoint_enabled}
        '''
        result = self._values.get("dedicated_endpoint_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def endpoint_display_name(self) -> typing.Optional[builtins.str]:
        '''The user-specified display name of the endpoint. If not set, a default name will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#endpoint_display_name GoogleVertexAiEndpointWithModelGardenDeployment#endpoint_display_name}
        '''
        result = self._values.get("endpoint_display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3526892a6131b2df4c614d01676423e87225d224c6f701b09705a8e99e7356c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDedicatedEndpointEnabled")
    def reset_dedicated_endpoint_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDedicatedEndpointEnabled", []))

    @jsii.member(jsii_name="resetEndpointDisplayName")
    def reset_endpoint_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointDisplayName", []))

    @builtins.property
    @jsii.member(jsii_name="dedicatedEndpointEnabledInput")
    def dedicated_endpoint_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dedicatedEndpointEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointDisplayNameInput")
    def endpoint_display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointDisplayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedEndpointEnabled")
    def dedicated_endpoint_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dedicatedEndpointEnabled"))

    @dedicated_endpoint_enabled.setter
    def dedicated_endpoint_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f2ac22173bbc6756bf402c735e0df739a36064fbfe8fca4e40bab6a777e054)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dedicatedEndpointEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpointDisplayName")
    def endpoint_display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointDisplayName"))

    @endpoint_display_name.setter
    def endpoint_display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d60ca4fc1ffc3ec1365ccee8a5d40d21c782e7219949504b0a5a24c9ff7aa43e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointDisplayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e89a82c648fc1b8ceb9884d8c84ed80d4bd8ea6e92687a0710384df616f88943)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfig",
    jsii_struct_bases=[],
    name_mapping={
        "accept_eula": "acceptEula",
        "container_spec": "containerSpec",
        "hugging_face_access_token": "huggingFaceAccessToken",
        "hugging_face_cache_enabled": "huggingFaceCacheEnabled",
        "model_display_name": "modelDisplayName",
    },
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfig:
    def __init__(
        self,
        *,
        accept_eula: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        container_spec: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        hugging_face_access_token: typing.Optional[builtins.str] = None,
        hugging_face_cache_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        model_display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accept_eula: Whether the user accepts the End User License Agreement (EULA) for the model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#accept_eula GoogleVertexAiEndpointWithModelGardenDeployment#accept_eula}
        :param container_spec: container_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#container_spec GoogleVertexAiEndpointWithModelGardenDeployment#container_spec}
        :param hugging_face_access_token: The Hugging Face read access token used to access the model artifacts of gated models. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#hugging_face_access_token GoogleVertexAiEndpointWithModelGardenDeployment#hugging_face_access_token}
        :param hugging_face_cache_enabled: If true, the model will deploy with a cached version instead of directly downloading the model artifacts from Hugging Face. This is suitable for VPC-SC users with limited internet access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#hugging_face_cache_enabled GoogleVertexAiEndpointWithModelGardenDeployment#hugging_face_cache_enabled}
        :param model_display_name: The user-specified display name of the uploaded model. If not set, a default name will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#model_display_name GoogleVertexAiEndpointWithModelGardenDeployment#model_display_name}
        '''
        if isinstance(container_spec, dict):
            container_spec = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec(**container_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bc2461b4658d615952c693a5e73e854c6ab0af93d2a2b435647630faa58bb6b)
            check_type(argname="argument accept_eula", value=accept_eula, expected_type=type_hints["accept_eula"])
            check_type(argname="argument container_spec", value=container_spec, expected_type=type_hints["container_spec"])
            check_type(argname="argument hugging_face_access_token", value=hugging_face_access_token, expected_type=type_hints["hugging_face_access_token"])
            check_type(argname="argument hugging_face_cache_enabled", value=hugging_face_cache_enabled, expected_type=type_hints["hugging_face_cache_enabled"])
            check_type(argname="argument model_display_name", value=model_display_name, expected_type=type_hints["model_display_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accept_eula is not None:
            self._values["accept_eula"] = accept_eula
        if container_spec is not None:
            self._values["container_spec"] = container_spec
        if hugging_face_access_token is not None:
            self._values["hugging_face_access_token"] = hugging_face_access_token
        if hugging_face_cache_enabled is not None:
            self._values["hugging_face_cache_enabled"] = hugging_face_cache_enabled
        if model_display_name is not None:
            self._values["model_display_name"] = model_display_name

    @builtins.property
    def accept_eula(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the user accepts the End User License Agreement (EULA) for the model.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#accept_eula GoogleVertexAiEndpointWithModelGardenDeployment#accept_eula}
        '''
        result = self._values.get("accept_eula")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def container_spec(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec"]:
        '''container_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#container_spec GoogleVertexAiEndpointWithModelGardenDeployment#container_spec}
        '''
        result = self._values.get("container_spec")
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec"], result)

    @builtins.property
    def hugging_face_access_token(self) -> typing.Optional[builtins.str]:
        '''The Hugging Face read access token used to access the model artifacts of gated models.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#hugging_face_access_token GoogleVertexAiEndpointWithModelGardenDeployment#hugging_face_access_token}
        '''
        result = self._values.get("hugging_face_access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hugging_face_cache_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the model will deploy with a cached version instead of directly downloading the model artifacts from Hugging Face.

        This is suitable for
        VPC-SC users with limited internet access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#hugging_face_cache_enabled GoogleVertexAiEndpointWithModelGardenDeployment#hugging_face_cache_enabled}
        '''
        result = self._values.get("hugging_face_cache_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def model_display_name(self) -> typing.Optional[builtins.str]:
        '''The user-specified display name of the uploaded model. If not set, a default name will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#model_display_name GoogleVertexAiEndpointWithModelGardenDeployment#model_display_name}
        '''
        result = self._values.get("model_display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec",
    jsii_struct_bases=[],
    name_mapping={
        "image_uri": "imageUri",
        "args": "args",
        "command": "command",
        "deployment_timeout": "deploymentTimeout",
        "env": "env",
        "grpc_ports": "grpcPorts",
        "health_probe": "healthProbe",
        "health_route": "healthRoute",
        "liveness_probe": "livenessProbe",
        "ports": "ports",
        "predict_route": "predictRoute",
        "shared_memory_size_mb": "sharedMemorySizeMb",
        "startup_probe": "startupProbe",
    },
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec:
    def __init__(
        self,
        *,
        image_uri: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        deployment_timeout: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv", typing.Dict[builtins.str, typing.Any]]]]] = None,
        grpc_ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        health_probe: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe", typing.Dict[builtins.str, typing.Any]]] = None,
        health_route: typing.Optional[builtins.str] = None,
        liveness_probe: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe", typing.Dict[builtins.str, typing.Any]]] = None,
        ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        predict_route: typing.Optional[builtins.str] = None,
        shared_memory_size_mb: typing.Optional[builtins.str] = None,
        startup_probe: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param image_uri: URI of the Docker image to be used as the custom container for serving predictions. This URI must identify an image in Artifact Registry or Container Registry. Learn more about the `container publishing requirements <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#publishing>`_, including permissions requirements for the Vertex AI Service Agent. The container image is ingested upon ModelService.UploadModel, stored internally, and this original path is afterwards not used. To learn about the requirements for the Docker image itself, see `Custom container requirements <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#>`_. You can use the URI to one of Vertex AI's `pre-built container images for prediction <https://cloud.google.com/vertex-ai/docs/predictions/pre-built-containers>`_ in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#image_uri GoogleVertexAiEndpointWithModelGardenDeployment#image_uri}
        :param args: Specifies arguments for the command that runs when the container starts. This overrides the container's `'CMD' <https://docs.docker.com/engine/reference/builder/#cmd>`_. Specify this field as an array of executable and arguments, similar to a Docker 'CMD''s "default parameters" form. If you don't specify this field but do specify the command field, then the command from the 'command' field runs without any additional arguments. See the `Kubernetes documentation about how the 'command' and 'args' fields interact with a container's 'ENTRYPOINT' and 'CMD' <https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#notes>`_. If you don't specify this field and don't specify the 'command' field, then the container's `'ENTRYPOINT' <https://docs.docker.com/engine/reference/builder/#cmd>`_ and 'CMD' determine what runs based on their default behavior. See the Docker documentation about `how 'CMD' and 'ENTRYPOINT' interact <https://docs.docker.com/engine/reference/builder/#understand-how-cmd-and-entrypoint-interact>`_. In this field, you can reference `environment variables set by Vertex AI <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_ and environment variables set in the env field. You cannot reference environment variables set in the Docker image. In order for environment variables to be expanded, reference them by using the following syntax:$(VARIABLE_NAME) Note that this differs from Bash variable expansion, which does not use parentheses. If a variable cannot be resolved, the reference in the input string is used unchanged. To avoid variable expansion, you can escape this syntax with '$$'; for example:$$(VARIABLE_NAME) This field corresponds to the 'args' field of the Kubernetes Containers `v1 core API <https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.23/#container-v1-core>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#args GoogleVertexAiEndpointWithModelGardenDeployment#args}
        :param command: Specifies the command that runs when the container starts. This overrides the container's `ENTRYPOINT <https://docs.docker.com/engine/reference/builder/#entrypoint>`_. Specify this field as an array of executable and arguments, similar to a Docker 'ENTRYPOINT''s "exec" form, not its "shell" form. If you do not specify this field, then the container's 'ENTRYPOINT' runs, in conjunction with the args field or the container's `'CMD' <https://docs.docker.com/engine/reference/builder/#cmd>`_, if either exists. If this field is not specified and the container does not have an 'ENTRYPOINT', then refer to the Docker documentation about `how 'CMD' and 'ENTRYPOINT' interact <https://docs.docker.com/engine/reference/builder/#understand-how-cmd-and-entrypoint-interact>`_. If you specify this field, then you can also specify the 'args' field to provide additional arguments for this command. However, if you specify this field, then the container's 'CMD' is ignored. See the `Kubernetes documentation about how the 'command' and 'args' fields interact with a container's 'ENTRYPOINT' and 'CMD' <https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#notes>`_. In this field, you can reference `environment variables set by Vertex AI <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_ and environment variables set in the env field. You cannot reference environment variables set in the Docker image. In order for environment variables to be expanded, reference them by using the following syntax:$(VARIABLE_NAME) Note that this differs from Bash variable expansion, which does not use parentheses. If a variable cannot be resolved, the reference in the input string is used unchanged. To avoid variable expansion, you can escape this syntax with '$$'; for example:$$(VARIABLE_NAME) This field corresponds to the 'command' field of the Kubernetes Containers `v1 core API <https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.23/#container-v1-core>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#command GoogleVertexAiEndpointWithModelGardenDeployment#command}
        :param deployment_timeout: Deployment timeout. Limit for deployment timeout is 2 hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#deployment_timeout GoogleVertexAiEndpointWithModelGardenDeployment#deployment_timeout}
        :param env: env block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#env GoogleVertexAiEndpointWithModelGardenDeployment#env}
        :param grpc_ports: grpc_ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#grpc_ports GoogleVertexAiEndpointWithModelGardenDeployment#grpc_ports}
        :param health_probe: health_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#health_probe GoogleVertexAiEndpointWithModelGardenDeployment#health_probe}
        :param health_route: HTTP path on the container to send health checks to. Vertex AI intermittently sends GET requests to this path on the container's IP address and port to check that the container is healthy. Read more about `health checks <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#health>`_. For example, if you set this field to '/bar', then Vertex AI intermittently sends a GET request to the '/bar' path on the port of your container specified by the first value of this 'ModelContainerSpec''s ports field. If you don't specify this field, it defaults to the following value when you deploy this Model to an Endpoint:/v1/endpoints/ENDPOINT/deployedModels/DEPLOYED_MODEL:predict The placeholders in this value are replaced as follows: - ENDPOINT: The last segment (following 'endpoints/')of the Endpoint.name][] field of the Endpoint where this Model has been deployed. (Vertex AI makes this value available to your container code as the `'AIP_ENDPOINT_ID' environment variable <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_.) - DEPLOYED_MODEL: DeployedModel.id of the 'DeployedModel'. (Vertex AI makes this value available to your container code as the `'AIP_DEPLOYED_MODEL_ID' environment variable <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_.) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#health_route GoogleVertexAiEndpointWithModelGardenDeployment#health_route}
        :param liveness_probe: liveness_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#liveness_probe GoogleVertexAiEndpointWithModelGardenDeployment#liveness_probe}
        :param ports: ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#ports GoogleVertexAiEndpointWithModelGardenDeployment#ports}
        :param predict_route: HTTP path on the container to send prediction requests to. Vertex AI forwards requests sent using projects.locations.endpoints.predict to this path on the container's IP address and port. Vertex AI then returns the container's response in the API response. For example, if you set this field to '/foo', then when Vertex AI receives a prediction request, it forwards the request body in a POST request to the '/foo' path on the port of your container specified by the first value of this 'ModelContainerSpec''s ports field. If you don't specify this field, it defaults to the following value when you deploy this Model to an Endpoint:/v1/endpoints/ENDPOINT/deployedModels/DEPLOYED_MODEL:predict The placeholders in this value are replaced as follows: - ENDPOINT: The last segment (following 'endpoints/')of the Endpoint.name][] field of the Endpoint where this Model has been deployed. (Vertex AI makes this value available to your container code as the `'AIP_ENDPOINT_ID' environment variable <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_.) - DEPLOYED_MODEL: DeployedModel.id of the 'DeployedModel'. (Vertex AI makes this value available to your container code as the `'AIP_DEPLOYED_MODEL_ID' environment variable <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_.) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#predict_route GoogleVertexAiEndpointWithModelGardenDeployment#predict_route}
        :param shared_memory_size_mb: The amount of the VM memory to reserve as the shared memory for the model in megabytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#shared_memory_size_mb GoogleVertexAiEndpointWithModelGardenDeployment#shared_memory_size_mb}
        :param startup_probe: startup_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#startup_probe GoogleVertexAiEndpointWithModelGardenDeployment#startup_probe}
        '''
        if isinstance(health_probe, dict):
            health_probe = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe(**health_probe)
        if isinstance(liveness_probe, dict):
            liveness_probe = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe(**liveness_probe)
        if isinstance(startup_probe, dict):
            startup_probe = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe(**startup_probe)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09b10856b38253843a2527a890910dcd5c59dd6482d5a2c68f3a10e629025100)
            check_type(argname="argument image_uri", value=image_uri, expected_type=type_hints["image_uri"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument deployment_timeout", value=deployment_timeout, expected_type=type_hints["deployment_timeout"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument grpc_ports", value=grpc_ports, expected_type=type_hints["grpc_ports"])
            check_type(argname="argument health_probe", value=health_probe, expected_type=type_hints["health_probe"])
            check_type(argname="argument health_route", value=health_route, expected_type=type_hints["health_route"])
            check_type(argname="argument liveness_probe", value=liveness_probe, expected_type=type_hints["liveness_probe"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
            check_type(argname="argument predict_route", value=predict_route, expected_type=type_hints["predict_route"])
            check_type(argname="argument shared_memory_size_mb", value=shared_memory_size_mb, expected_type=type_hints["shared_memory_size_mb"])
            check_type(argname="argument startup_probe", value=startup_probe, expected_type=type_hints["startup_probe"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_uri": image_uri,
        }
        if args is not None:
            self._values["args"] = args
        if command is not None:
            self._values["command"] = command
        if deployment_timeout is not None:
            self._values["deployment_timeout"] = deployment_timeout
        if env is not None:
            self._values["env"] = env
        if grpc_ports is not None:
            self._values["grpc_ports"] = grpc_ports
        if health_probe is not None:
            self._values["health_probe"] = health_probe
        if health_route is not None:
            self._values["health_route"] = health_route
        if liveness_probe is not None:
            self._values["liveness_probe"] = liveness_probe
        if ports is not None:
            self._values["ports"] = ports
        if predict_route is not None:
            self._values["predict_route"] = predict_route
        if shared_memory_size_mb is not None:
            self._values["shared_memory_size_mb"] = shared_memory_size_mb
        if startup_probe is not None:
            self._values["startup_probe"] = startup_probe

    @builtins.property
    def image_uri(self) -> builtins.str:
        '''URI of the Docker image to be used as the custom container for serving predictions.

        This URI must identify an image in Artifact Registry or
        Container Registry. Learn more about the `container publishing
        requirements <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#publishing>`_,
        including permissions requirements for the Vertex AI Service Agent.

        The container image is ingested upon ModelService.UploadModel, stored
        internally, and this original path is afterwards not used.

        To learn about the requirements for the Docker image itself, see
        `Custom container
        requirements <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#>`_.

        You can use the URI to one of Vertex AI's `pre-built container images for
        prediction <https://cloud.google.com/vertex-ai/docs/predictions/pre-built-containers>`_
        in this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#image_uri GoogleVertexAiEndpointWithModelGardenDeployment#image_uri}
        '''
        result = self._values.get("image_uri")
        assert result is not None, "Required property 'image_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies arguments for the command that runs when the container starts.

        This overrides the container's
        `'CMD' <https://docs.docker.com/engine/reference/builder/#cmd>`_. Specify
        this field as an array of executable and arguments, similar to a Docker
        'CMD''s "default parameters" form.

        If you don't specify this field but do specify the
        command field, then the command from the
        'command' field runs without any additional arguments. See the
        `Kubernetes documentation about how the
        'command' and 'args' fields interact with a container's 'ENTRYPOINT' and
        'CMD' <https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#notes>`_.

        If you don't specify this field and don't specify the 'command' field,
        then the container's
        `'ENTRYPOINT' <https://docs.docker.com/engine/reference/builder/#cmd>`_ and
        'CMD' determine what runs based on their default behavior. See the Docker
        documentation about `how 'CMD' and 'ENTRYPOINT'
        interact <https://docs.docker.com/engine/reference/builder/#understand-how-cmd-and-entrypoint-interact>`_.

        In this field, you can reference `environment variables
        set by Vertex
        AI <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_
        and environment variables set in the env field.
        You cannot reference environment variables set in the Docker image. In
        order for environment variables to be expanded, reference them by using the
        following syntax:$(VARIABLE_NAME)
        Note that this differs from Bash variable expansion, which does not use
        parentheses. If a variable cannot be resolved, the reference in the input
        string is used unchanged. To avoid variable expansion, you can escape this
        syntax with '$$'; for example:$$(VARIABLE_NAME)
        This field corresponds to the 'args' field of the Kubernetes Containers
        `v1 core
        API <https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.23/#container-v1-core>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#args GoogleVertexAiEndpointWithModelGardenDeployment#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the command that runs when the container starts.

        This overrides
        the container's
        `ENTRYPOINT <https://docs.docker.com/engine/reference/builder/#entrypoint>`_.
        Specify this field as an array of executable and arguments, similar to a
        Docker 'ENTRYPOINT''s "exec" form, not its "shell" form.

        If you do not specify this field, then the container's 'ENTRYPOINT' runs,
        in conjunction with the args field or the
        container's `'CMD' <https://docs.docker.com/engine/reference/builder/#cmd>`_,
        if either exists. If this field is not specified and the container does not
        have an 'ENTRYPOINT', then refer to the Docker documentation about `how
        'CMD' and 'ENTRYPOINT'
        interact <https://docs.docker.com/engine/reference/builder/#understand-how-cmd-and-entrypoint-interact>`_.

        If you specify this field, then you can also specify the 'args' field to
        provide additional arguments for this command. However, if you specify this
        field, then the container's 'CMD' is ignored. See the
        `Kubernetes documentation about how the
        'command' and 'args' fields interact with a container's 'ENTRYPOINT' and
        'CMD' <https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#notes>`_.

        In this field, you can reference `environment variables set by Vertex
        AI <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_
        and environment variables set in the env field.
        You cannot reference environment variables set in the Docker image. In
        order for environment variables to be expanded, reference them by using the
        following syntax:$(VARIABLE_NAME)
        Note that this differs from Bash variable expansion, which does not use
        parentheses. If a variable cannot be resolved, the reference in the input
        string is used unchanged. To avoid variable expansion, you can escape this
        syntax with '$$'; for example:$$(VARIABLE_NAME)
        This field corresponds to the 'command' field of the Kubernetes Containers
        `v1 core
        API <https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.23/#container-v1-core>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#command GoogleVertexAiEndpointWithModelGardenDeployment#command}
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deployment_timeout(self) -> typing.Optional[builtins.str]:
        '''Deployment timeout. Limit for deployment timeout is 2 hours.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#deployment_timeout GoogleVertexAiEndpointWithModelGardenDeployment#deployment_timeout}
        '''
        result = self._values.get("deployment_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv"]]]:
        '''env block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#env GoogleVertexAiEndpointWithModelGardenDeployment#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv"]]], result)

    @builtins.property
    def grpc_ports(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts"]]]:
        '''grpc_ports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#grpc_ports GoogleVertexAiEndpointWithModelGardenDeployment#grpc_ports}
        '''
        result = self._values.get("grpc_ports")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts"]]], result)

    @builtins.property
    def health_probe(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe"]:
        '''health_probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#health_probe GoogleVertexAiEndpointWithModelGardenDeployment#health_probe}
        '''
        result = self._values.get("health_probe")
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe"], result)

    @builtins.property
    def health_route(self) -> typing.Optional[builtins.str]:
        '''HTTP path on the container to send health checks to.

        Vertex AI
        intermittently sends GET requests to this path on the container's IP
        address and port to check that the container is healthy. Read more about
        `health
        checks <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#health>`_.

        For example, if you set this field to '/bar', then Vertex AI
        intermittently sends a GET request to the '/bar' path on the port of your
        container specified by the first value of this 'ModelContainerSpec''s
        ports field.

        If you don't specify this field, it defaults to the following value when
        you deploy this Model to an Endpoint:/v1/endpoints/ENDPOINT/deployedModels/DEPLOYED_MODEL:predict
        The placeholders in this value are replaced as follows:

        - ENDPOINT: The last segment (following 'endpoints/')of the
          Endpoint.name][] field of the Endpoint where this Model has been
          deployed. (Vertex AI makes this value available to your container code
          as the `'AIP_ENDPOINT_ID' environment
          variable <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_.)
        - DEPLOYED_MODEL: DeployedModel.id of the 'DeployedModel'.
          (Vertex AI makes this value available to your container code as the
          `'AIP_DEPLOYED_MODEL_ID' environment
          variable <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_.)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#health_route GoogleVertexAiEndpointWithModelGardenDeployment#health_route}
        '''
        result = self._values.get("health_route")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def liveness_probe(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe"]:
        '''liveness_probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#liveness_probe GoogleVertexAiEndpointWithModelGardenDeployment#liveness_probe}
        '''
        result = self._values.get("liveness_probe")
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe"], result)

    @builtins.property
    def ports(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts"]]]:
        '''ports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#ports GoogleVertexAiEndpointWithModelGardenDeployment#ports}
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts"]]], result)

    @builtins.property
    def predict_route(self) -> typing.Optional[builtins.str]:
        '''HTTP path on the container to send prediction requests to.

        Vertex AI
        forwards requests sent using
        projects.locations.endpoints.predict to this
        path on the container's IP address and port. Vertex AI then returns the
        container's response in the API response.

        For example, if you set this field to '/foo', then when Vertex AI
        receives a prediction request, it forwards the request body in a POST
        request to the '/foo' path on the port of your container specified by the
        first value of this 'ModelContainerSpec''s
        ports field.

        If you don't specify this field, it defaults to the following value when
        you deploy this Model to an Endpoint:/v1/endpoints/ENDPOINT/deployedModels/DEPLOYED_MODEL:predict
        The placeholders in this value are replaced as follows:

        - ENDPOINT: The last segment (following 'endpoints/')of the
          Endpoint.name][] field of the Endpoint where this Model has been
          deployed. (Vertex AI makes this value available to your container code
          as the `'AIP_ENDPOINT_ID' environment
          variable <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_.)
        - DEPLOYED_MODEL: DeployedModel.id of the 'DeployedModel'.
          (Vertex AI makes this value available to your container code
          as the `'AIP_DEPLOYED_MODEL_ID' environment
          variable <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_.)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#predict_route GoogleVertexAiEndpointWithModelGardenDeployment#predict_route}
        '''
        result = self._values.get("predict_route")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shared_memory_size_mb(self) -> typing.Optional[builtins.str]:
        '''The amount of the VM memory to reserve as the shared memory for the model in megabytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#shared_memory_size_mb GoogleVertexAiEndpointWithModelGardenDeployment#shared_memory_size_mb}
        '''
        result = self._values.get("shared_memory_size_mb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def startup_probe(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe"]:
        '''startup_probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#startup_probe GoogleVertexAiEndpointWithModelGardenDeployment#startup_probe}
        '''
        result = self._values.get("startup_probe")
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Name of the environment variable. Must be a valid C identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#name GoogleVertexAiEndpointWithModelGardenDeployment#name}
        :param value: Variables that reference a $(VAR_NAME) are expanded using the previous defined environment variables in the container and any service environment variables. If a variable cannot be resolved, the reference in the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, regardless of whether the variable exists or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#value GoogleVertexAiEndpointWithModelGardenDeployment#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60feb6cbc5b07cf0928ff9f3d50d0640f705ec9d873e2364f857da7504af54a5)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the environment variable. Must be a valid C identifier.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#name GoogleVertexAiEndpointWithModelGardenDeployment#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Variables that reference a $(VAR_NAME) are expanded using the previous defined environment variables in the container and any service environment variables.

        If a variable cannot be resolved,
        the reference in the input string will be unchanged. The $(VAR_NAME)
        syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped
        references will never be expanded, regardless of whether the variable
        exists or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#value GoogleVertexAiEndpointWithModelGardenDeployment#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnvList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnvList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fed7f6851155fd1a74fd46e77ea5bfcbc3ce82a84a05140adf4b14654979fc18)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnvOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb865f63eb8b2fe6abea8f7df4c22bec6d785b1489e07d5c16b579743f37d032)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnvOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f9d2a5ebe6a866b485ff807658076b0cefe150c00a7856892031e8c4ad766b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87d4b4f3aebb436e992eeac612a6e0c259dd5aa40722e0ff7b5f54f41e33c224)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63e45f5832a1fa272b706265e14fe6161cb7c0d444ee99d1d1826805ca1622a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f67fcd6e4ae3539191a684ed74864d33033d7974d80529c87ea75f0fb62a0f13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnvOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnvOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40872ada3923231f08f064b2b343bd1c85427d5a2917fd3dcd18a88ae112965c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d61f319ac485fc41c841a16c8ae58e0f41e03d0db2498428d865e7e87e37786)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__758cc4c7adebcb45b7edfcb6ad528b069175c8653098148402e45d1568ae2532)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb588a806a72432209f8c07f8450abdf8c13343b4e84630bd593eff4f171746c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts",
    jsii_struct_bases=[],
    name_mapping={"container_port": "containerPort"},
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts:
    def __init__(self, *, container_port: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param container_port: The number of the port to expose on the pod's IP address. Must be a valid port number, between 1 and 65535 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#container_port GoogleVertexAiEndpointWithModelGardenDeployment#container_port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__392082e2055c5046f1700f584677c8d32defb428ce18473fa32631c800c9880d)
            check_type(argname="argument container_port", value=container_port, expected_type=type_hints["container_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_port is not None:
            self._values["container_port"] = container_port

    @builtins.property
    def container_port(self) -> typing.Optional[jsii.Number]:
        '''The number of the port to expose on the pod's IP address.

        Must be a valid port number, between 1 and 65535 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#container_port GoogleVertexAiEndpointWithModelGardenDeployment#container_port}
        '''
        result = self._values.get("container_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPortsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPortsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa6e2a21dc8b9935630de145b49cd74a17795c5022fa2718516aa6d5fea9a340)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPortsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af83c0e43c8af1bfc8720f09444537fbb84827fc80f8b01e0bd693d582466905)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPortsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6b79459da33c68f0ce8aab447c8bd776582ed4baac0aebca483a3c8f0a21cff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f52c9db839f29bc4eb370704435e190e14907746d7cdfc591b0496681fce8262)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2465ef4a37bdc899bec25f3440fdebe07ab90ebce823700f399b1b69b7c2c0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9722d793a5b608ead3641cad5f7e814655fcce66fe0de7bf458a90f66d0af7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPortsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPortsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14d3732193c6b0a3d161543e9012f499329f06b3457ad223080722712f631ac8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContainerPort")
    def reset_container_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerPort", []))

    @builtins.property
    @jsii.member(jsii_name="containerPortInput")
    def container_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "containerPortInput"))

    @builtins.property
    @jsii.member(jsii_name="containerPort")
    def container_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerPort"))

    @container_port.setter
    def container_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5824ae0344c2e24cf44313c107755cf7cf2948da397a624a024ef517422025b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4cec00c97c7fd188c3f00e38f627bbe2e8d59152cfd72065703750e52659a51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe",
    jsii_struct_bases=[],
    name_mapping={
        "exec": "exec",
        "failure_threshold": "failureThreshold",
        "grpc": "grpc",
        "http_get": "httpGet",
        "initial_delay_seconds": "initialDelaySeconds",
        "period_seconds": "periodSeconds",
        "success_threshold": "successThreshold",
        "tcp_socket": "tcpSocket",
        "timeout_seconds": "timeoutSeconds",
    },
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe:
    def __init__(
        self,
        *,
        exec: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec", typing.Dict[builtins.str, typing.Any]]] = None,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        success_threshold: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param exec: exec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#exec GoogleVertexAiEndpointWithModelGardenDeployment#exec}
        :param failure_threshold: Number of consecutive failures before the probe is considered failed. Defaults to 3. Minimum value is 1. Maps to Kubernetes probe argument 'failureThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#failure_threshold GoogleVertexAiEndpointWithModelGardenDeployment#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#grpc GoogleVertexAiEndpointWithModelGardenDeployment#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#http_get GoogleVertexAiEndpointWithModelGardenDeployment#http_get}
        :param initial_delay_seconds: Number of seconds to wait before starting the probe. Defaults to 0. Minimum value is 0. Maps to Kubernetes probe argument 'initialDelaySeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#initial_delay_seconds GoogleVertexAiEndpointWithModelGardenDeployment#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Must be less than timeout_seconds. Maps to Kubernetes probe argument 'periodSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#period_seconds GoogleVertexAiEndpointWithModelGardenDeployment#period_seconds}
        :param success_threshold: Number of consecutive successes before the probe is considered successful. Defaults to 1. Minimum value is 1. Maps to Kubernetes probe argument 'successThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#success_threshold GoogleVertexAiEndpointWithModelGardenDeployment#success_threshold}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#tcp_socket GoogleVertexAiEndpointWithModelGardenDeployment#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Must be greater or equal to period_seconds. Maps to Kubernetes probe argument 'timeoutSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#timeout_seconds GoogleVertexAiEndpointWithModelGardenDeployment#timeout_seconds}
        '''
        if isinstance(exec, dict):
            exec = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec(**exec)
        if isinstance(grpc, dict):
            grpc = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc(**grpc)
        if isinstance(http_get, dict):
            http_get = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet(**http_get)
        if isinstance(tcp_socket, dict):
            tcp_socket = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket(**tcp_socket)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23b17bc98233523d13a7810cfc95ad7b273059b721acec8352a5075a1fbd33a1)
            check_type(argname="argument exec", value=exec, expected_type=type_hints["exec"])
            check_type(argname="argument failure_threshold", value=failure_threshold, expected_type=type_hints["failure_threshold"])
            check_type(argname="argument grpc", value=grpc, expected_type=type_hints["grpc"])
            check_type(argname="argument http_get", value=http_get, expected_type=type_hints["http_get"])
            check_type(argname="argument initial_delay_seconds", value=initial_delay_seconds, expected_type=type_hints["initial_delay_seconds"])
            check_type(argname="argument period_seconds", value=period_seconds, expected_type=type_hints["period_seconds"])
            check_type(argname="argument success_threshold", value=success_threshold, expected_type=type_hints["success_threshold"])
            check_type(argname="argument tcp_socket", value=tcp_socket, expected_type=type_hints["tcp_socket"])
            check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exec is not None:
            self._values["exec"] = exec
        if failure_threshold is not None:
            self._values["failure_threshold"] = failure_threshold
        if grpc is not None:
            self._values["grpc"] = grpc
        if http_get is not None:
            self._values["http_get"] = http_get
        if initial_delay_seconds is not None:
            self._values["initial_delay_seconds"] = initial_delay_seconds
        if period_seconds is not None:
            self._values["period_seconds"] = period_seconds
        if success_threshold is not None:
            self._values["success_threshold"] = success_threshold
        if tcp_socket is not None:
            self._values["tcp_socket"] = tcp_socket
        if timeout_seconds is not None:
            self._values["timeout_seconds"] = timeout_seconds

    @builtins.property
    def exec(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec"]:
        '''exec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#exec GoogleVertexAiEndpointWithModelGardenDeployment#exec}
        '''
        result = self._values.get("exec")
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec"], result)

    @builtins.property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        '''Number of consecutive failures before the probe is considered failed. Defaults to 3. Minimum value is 1.

        Maps to Kubernetes probe argument 'failureThreshold'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#failure_threshold GoogleVertexAiEndpointWithModelGardenDeployment#failure_threshold}
        '''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def grpc(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc"]:
        '''grpc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#grpc GoogleVertexAiEndpointWithModelGardenDeployment#grpc}
        '''
        result = self._values.get("grpc")
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc"], result)

    @builtins.property
    def http_get(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet"]:
        '''http_get block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#http_get GoogleVertexAiEndpointWithModelGardenDeployment#http_get}
        '''
        result = self._values.get("http_get")
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet"], result)

    @builtins.property
    def initial_delay_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds to wait before starting the probe. Defaults to 0. Minimum value is 0.

        Maps to Kubernetes probe argument 'initialDelaySeconds'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#initial_delay_seconds GoogleVertexAiEndpointWithModelGardenDeployment#initial_delay_seconds}
        '''
        result = self._values.get("initial_delay_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period_seconds(self) -> typing.Optional[jsii.Number]:
        '''How often (in seconds) to perform the probe.

        Default to 10 seconds.
        Minimum value is 1. Must be less than timeout_seconds.

        Maps to Kubernetes probe argument 'periodSeconds'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#period_seconds GoogleVertexAiEndpointWithModelGardenDeployment#period_seconds}
        '''
        result = self._values.get("period_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def success_threshold(self) -> typing.Optional[jsii.Number]:
        '''Number of consecutive successes before the probe is considered successful. Defaults to 1. Minimum value is 1.

        Maps to Kubernetes probe argument 'successThreshold'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#success_threshold GoogleVertexAiEndpointWithModelGardenDeployment#success_threshold}
        '''
        result = self._values.get("success_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tcp_socket(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket"]:
        '''tcp_socket block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#tcp_socket GoogleVertexAiEndpointWithModelGardenDeployment#tcp_socket}
        '''
        result = self._values.get("tcp_socket")
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket"], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after which the probe times out.

        Defaults to 1 second.
        Minimum value is 1. Must be greater or equal to period_seconds.

        Maps to Kubernetes probe argument 'timeoutSeconds'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#timeout_seconds GoogleVertexAiEndpointWithModelGardenDeployment#timeout_seconds}
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec",
    jsii_struct_bases=[],
    name_mapping={"command": "command"},
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec:
    def __init__(
        self,
        *,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param command: Command is the command line to execute inside the container, the working directory for the command is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#command GoogleVertexAiEndpointWithModelGardenDeployment#command}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d2b15a0ba6bcb593960e0a1ec120bc8d7918564e9f6bfd29b7d4c9fdc962adc)
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if command is not None:
            self._values["command"] = command

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Command is the command line to execute inside the container, the working directory for the command is root ('/') in the container's filesystem.

        The command is simply exec'd, it is not run inside a shell, so
        traditional shell instructions ('|', etc) won't work. To use a shell, you
        need to explicitly call out to that shell. Exit status of 0 is treated as
        live/healthy and non-zero is unhealthy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#command GoogleVertexAiEndpointWithModelGardenDeployment#command}
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8d8460be6fd7eb99393747cf0e3643cc14a92d574f7738948f8e8166be7eb20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCommand")
    def reset_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommand", []))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42589fcc422d0cb79fde0365640b1688a676d2de7f196eeba80346d6f8e61ef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__077ce4d669933ef6c5ef1978705143b40e3dbece8bf98b05512fde45088eec8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "service": "service"},
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc:
    def __init__(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number of the gRPC service. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        :param service: Service is the name of the service to place in the gRPC HealthCheckRequest. See https://github.com/grpc/grpc/blob/master/doc/health-checking.md. If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#service GoogleVertexAiEndpointWithModelGardenDeployment#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__981661ece7ab23afef8f22c1dded8436ea803bf2ae672e637c254c452aba4216)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if port is not None:
            self._values["port"] = port
        if service is not None:
            self._values["service"] = service

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number of the gRPC service. Number must be in the range 1 to 65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''Service is the name of the service to place in the gRPC HealthCheckRequest. See https://github.com/grpc/grpc/blob/master/doc/health-checking.md.

        If this is not specified, the default behavior is defined by gRPC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#service GoogleVertexAiEndpointWithModelGardenDeployment#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8d22eb3fd6a335d8afd72c1fd3bec253faa472367092940e8284671d4634eef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetService")
    def reset_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetService", []))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1448367a66fd8f87943f2334b250ecdc63419c4554380d9f85867d712cce076)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d12cfc62af8b1d79595a7f60c6b8d1ad1c66491bd9ea7cbbd1d8cae1170ee91d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc0e82ac5ec6fa6db282355d81ff91375cea34e1421f0faaeadc191d00a14951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "http_headers": "httpHeaders",
        "path": "path",
        "port": "port",
        "scheme": "scheme",
    },
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        scheme: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: Host name to connect to, defaults to the model serving container's IP. You probably want to set "Host" in httpHeaders instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#host GoogleVertexAiEndpointWithModelGardenDeployment#host}
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#http_headers GoogleVertexAiEndpointWithModelGardenDeployment#http_headers}
        :param path: Path to access on the HTTP server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#path GoogleVertexAiEndpointWithModelGardenDeployment#path}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        :param scheme: Scheme to use for connecting to the host. Defaults to HTTP. Acceptable values are "HTTP" or "HTTPS". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#scheme GoogleVertexAiEndpointWithModelGardenDeployment#scheme}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7015f705f4750b4fd73965e72f60fe1cdb55df01ebc47e10b32285a65bb1ada)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument http_headers", value=http_headers, expected_type=type_hints["http_headers"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument scheme", value=scheme, expected_type=type_hints["scheme"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if host is not None:
            self._values["host"] = host
        if http_headers is not None:
            self._values["http_headers"] = http_headers
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port
        if scheme is not None:
            self._values["scheme"] = scheme

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Host name to connect to, defaults to the model serving container's IP.

        You probably want to set "Host" in httpHeaders instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#host GoogleVertexAiEndpointWithModelGardenDeployment#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders"]]]:
        '''http_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#http_headers GoogleVertexAiEndpointWithModelGardenDeployment#http_headers}
        '''
        result = self._values.get("http_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders"]]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to access on the HTTP server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#path GoogleVertexAiEndpointWithModelGardenDeployment#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Number of the port to access on the container. Number must be in the range 1 to 65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scheme(self) -> typing.Optional[builtins.str]:
        '''Scheme to use for connecting to the host. Defaults to HTTP. Acceptable values are "HTTP" or "HTTPS".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#scheme GoogleVertexAiEndpointWithModelGardenDeployment#scheme}
        '''
        result = self._values.get("scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The header field name. This will be canonicalized upon output, so case-variant names will be understood as the same header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#name GoogleVertexAiEndpointWithModelGardenDeployment#name}
        :param value: The header field value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#value GoogleVertexAiEndpointWithModelGardenDeployment#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64c858167251a7839fa7ca243613a7c3ffd1d378dc386929cb904dd892300d80)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The header field name. This will be canonicalized upon output, so case-variant names will be understood as the same header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#name GoogleVertexAiEndpointWithModelGardenDeployment#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The header field value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#value GoogleVertexAiEndpointWithModelGardenDeployment#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28ade7ec639ca7baa0361faa025bd8916a306daf8f135761b91ccdba249e3154)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f984feed4b43d77911736c4ef17e2d203d71e28abb28a4953b78c73d7337fb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72fef7c7f90c6e7008fe91f2eafbae0b82070b262049026c891c0b7fd093ce00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b7bc4dd17a1fdfdf55bcc8fae3a0e909f17195f197bba5beb885663f9ec6fee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50f64635bc29e6daed7b17471de8d1cda931775615a15004ca1591e0ddfce2fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aa5fc8aa0063d6edc9ae9555de4284d736fd54768935f70e907529e39e392f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4cb4d1cb2b6de3a4ffd4f9e7ae19a57361bf04ab912f8a3a8ae9c6407863daa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__899be8f3cc3164e899c54b59569a8ece1edec81275080cb568202390ed78db8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30d959de7e7a8bb793a40bb3643126228f1a729fe860abc2400505a249e3cfd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93a5f2f4724fa1f9b2dec37a9301d20f61a326d8b8b568a11e7a1beb573d2819)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55b11c5b4ce8def437af6df63dca64c75d4ecc707a28b071a54e048dc5a0c354)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpHeaders")
    def put_http_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef34a6b2f9ccc265f951fb2909c912fdf4f7a7af4e0755e4fb6ca96c9285b5f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttpHeaders", [value]))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetHttpHeaders")
    def reset_http_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpHeaders", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetScheme")
    def reset_scheme(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheme", []))

    @builtins.property
    @jsii.member(jsii_name="httpHeaders")
    def http_headers(
        self,
    ) -> GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeadersList:
        return typing.cast(GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeadersList, jsii.get(self, "httpHeaders"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="httpHeadersInput")
    def http_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders]]], jsii.get(self, "httpHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="schemeInput")
    def scheme_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemeInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__531b9474ad3ca8715f2dd9d111692bf824ead21b0a4d0a92867501dd495713f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff94ac3778a1bcc0a2ef45f8e372faa9239dc1181f23a6c2206cfbe08d9e1a12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c545a329fb34727d5049fee2c780d281a379cc327a9e9f1831115acbb1101ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheme")
    def scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheme"))

    @scheme.setter
    def scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7459e74056a4f3de35dc2e3797d04cb75d1034a11a2d8ffe5df4b29f3af46a8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fad5ff7da59f28909fab5d440dde277361afa004e345ea5f1e448a7059bd3df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d55b28c5b74f4f08ace09eca4935738f31390ac2d0ccbd5beeca1db5edd13156)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExec")
    def put_exec(
        self,
        *,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param command: Command is the command line to execute inside the container, the working directory for the command is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#command GoogleVertexAiEndpointWithModelGardenDeployment#command}
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec(
            command=command
        )

        return typing.cast(None, jsii.invoke(self, "putExec", [value]))

    @jsii.member(jsii_name="putGrpc")
    def put_grpc(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number of the gRPC service. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        :param service: Service is the name of the service to place in the gRPC HealthCheckRequest. See https://github.com/grpc/grpc/blob/master/doc/health-checking.md. If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#service GoogleVertexAiEndpointWithModelGardenDeployment#service}
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc(
            port=port, service=service
        )

        return typing.cast(None, jsii.invoke(self, "putGrpc", [value]))

    @jsii.member(jsii_name="putHttpGet")
    def put_http_get(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        scheme: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: Host name to connect to, defaults to the model serving container's IP. You probably want to set "Host" in httpHeaders instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#host GoogleVertexAiEndpointWithModelGardenDeployment#host}
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#http_headers GoogleVertexAiEndpointWithModelGardenDeployment#http_headers}
        :param path: Path to access on the HTTP server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#path GoogleVertexAiEndpointWithModelGardenDeployment#path}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        :param scheme: Scheme to use for connecting to the host. Defaults to HTTP. Acceptable values are "HTTP" or "HTTPS". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#scheme GoogleVertexAiEndpointWithModelGardenDeployment#scheme}
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet(
            host=host, http_headers=http_headers, path=path, port=port, scheme=scheme
        )

        return typing.cast(None, jsii.invoke(self, "putHttpGet", [value]))

    @jsii.member(jsii_name="putTcpSocket")
    def put_tcp_socket(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param host: Optional: Host name to connect to, defaults to the model serving container's IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#host GoogleVertexAiEndpointWithModelGardenDeployment#host}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket(
            host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putTcpSocket", [value]))

    @jsii.member(jsii_name="resetExec")
    def reset_exec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExec", []))

    @jsii.member(jsii_name="resetFailureThreshold")
    def reset_failure_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureThreshold", []))

    @jsii.member(jsii_name="resetGrpc")
    def reset_grpc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpc", []))

    @jsii.member(jsii_name="resetHttpGet")
    def reset_http_get(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpGet", []))

    @jsii.member(jsii_name="resetInitialDelaySeconds")
    def reset_initial_delay_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialDelaySeconds", []))

    @jsii.member(jsii_name="resetPeriodSeconds")
    def reset_period_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriodSeconds", []))

    @jsii.member(jsii_name="resetSuccessThreshold")
    def reset_success_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessThreshold", []))

    @jsii.member(jsii_name="resetTcpSocket")
    def reset_tcp_socket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpSocket", []))

    @jsii.member(jsii_name="resetTimeoutSeconds")
    def reset_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="exec")
    def exec(
        self,
    ) -> GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExecOutputReference:
        return typing.cast(GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExecOutputReference, jsii.get(self, "exec"))

    @builtins.property
    @jsii.member(jsii_name="grpc")
    def grpc(
        self,
    ) -> GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpcOutputReference:
        return typing.cast(GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpcOutputReference, jsii.get(self, "grpc"))

    @builtins.property
    @jsii.member(jsii_name="httpGet")
    def http_get(
        self,
    ) -> GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetOutputReference:
        return typing.cast(GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetOutputReference, jsii.get(self, "httpGet"))

    @builtins.property
    @jsii.member(jsii_name="tcpSocket")
    def tcp_socket(
        self,
    ) -> "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocketOutputReference":
        return typing.cast("GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocketOutputReference", jsii.get(self, "tcpSocket"))

    @builtins.property
    @jsii.member(jsii_name="execInput")
    def exec_input(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec], jsii.get(self, "execInput"))

    @builtins.property
    @jsii.member(jsii_name="failureThresholdInput")
    def failure_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcInput")
    def grpc_input(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc], jsii.get(self, "grpcInput"))

    @builtins.property
    @jsii.member(jsii_name="httpGetInput")
    def http_get_input(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet], jsii.get(self, "httpGetInput"))

    @builtins.property
    @jsii.member(jsii_name="initialDelaySecondsInput")
    def initial_delay_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialDelaySecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="periodSecondsInput")
    def period_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "periodSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="successThresholdInput")
    def success_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "successThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpSocketInput")
    def tcp_socket_input(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket"]:
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket"], jsii.get(self, "tcpSocketInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecondsInput")
    def timeout_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="failureThreshold")
    def failure_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failureThreshold"))

    @failure_threshold.setter
    def failure_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__882fbecc83e920bcd3d8b69dd2c72532e2ccede97e3741326d883faa2a541e2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelaySeconds")
    def initial_delay_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelaySeconds"))

    @initial_delay_seconds.setter
    def initial_delay_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e438f625e8c7ab234956154faaaf6379c1049a5df063bc95cb71a04273d567e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelaySeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodSeconds")
    def period_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodSeconds"))

    @period_seconds.setter
    def period_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2dfca596cae12843949e5ee4a280e87d1524db99d9bf21fde9ab3fb4a795fa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successThreshold")
    def success_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successThreshold"))

    @success_threshold.setter
    def success_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e58ff90946c77c1efe56a098fd97864e4502f39f817d36e64ac846ec38fbd172)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e158eb46d17dd2968aa48246815a89a9f62c1097ebcb0a4a6a434aa26a38ab3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d4e17b90ebee869b2316ff1e172845822e2725ee8cb17dd76d655f6e91a30a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket",
    jsii_struct_bases=[],
    name_mapping={"host": "host", "port": "port"},
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param host: Optional: Host name to connect to, defaults to the model serving container's IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#host GoogleVertexAiEndpointWithModelGardenDeployment#host}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acf64b3268a92e75b3d91932b14c9c9ed56133ba48e0baa569818fa4217207b0)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if host is not None:
            self._values["host"] = host
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Optional: Host name to connect to, defaults to the model serving container's IP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#host GoogleVertexAiEndpointWithModelGardenDeployment#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Number of the port to access on the container. Number must be in the range 1 to 65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocketOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocketOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d417c862f82ee870143934a9f7053e5f0ba8534ad1faafe5ae45e443adf71b06)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f736ef3a80cace1c9ebbffe7a182e8187e8bfa12decf96268f4fd761cd2975e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c37ba352c8957c23427f86e2a9d351604370830a487dd76f13d48b37997efdcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__477ed1a9dcfb85d5763f1cf15775e7b9de8a55aec2e24dfe5225ab129d1a9d64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe",
    jsii_struct_bases=[],
    name_mapping={
        "exec": "exec",
        "failure_threshold": "failureThreshold",
        "grpc": "grpc",
        "http_get": "httpGet",
        "initial_delay_seconds": "initialDelaySeconds",
        "period_seconds": "periodSeconds",
        "success_threshold": "successThreshold",
        "tcp_socket": "tcpSocket",
        "timeout_seconds": "timeoutSeconds",
    },
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe:
    def __init__(
        self,
        *,
        exec: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec", typing.Dict[builtins.str, typing.Any]]] = None,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        success_threshold: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param exec: exec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#exec GoogleVertexAiEndpointWithModelGardenDeployment#exec}
        :param failure_threshold: Number of consecutive failures before the probe is considered failed. Defaults to 3. Minimum value is 1. Maps to Kubernetes probe argument 'failureThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#failure_threshold GoogleVertexAiEndpointWithModelGardenDeployment#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#grpc GoogleVertexAiEndpointWithModelGardenDeployment#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#http_get GoogleVertexAiEndpointWithModelGardenDeployment#http_get}
        :param initial_delay_seconds: Number of seconds to wait before starting the probe. Defaults to 0. Minimum value is 0. Maps to Kubernetes probe argument 'initialDelaySeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#initial_delay_seconds GoogleVertexAiEndpointWithModelGardenDeployment#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Must be less than timeout_seconds. Maps to Kubernetes probe argument 'periodSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#period_seconds GoogleVertexAiEndpointWithModelGardenDeployment#period_seconds}
        :param success_threshold: Number of consecutive successes before the probe is considered successful. Defaults to 1. Minimum value is 1. Maps to Kubernetes probe argument 'successThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#success_threshold GoogleVertexAiEndpointWithModelGardenDeployment#success_threshold}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#tcp_socket GoogleVertexAiEndpointWithModelGardenDeployment#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Must be greater or equal to period_seconds. Maps to Kubernetes probe argument 'timeoutSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#timeout_seconds GoogleVertexAiEndpointWithModelGardenDeployment#timeout_seconds}
        '''
        if isinstance(exec, dict):
            exec = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec(**exec)
        if isinstance(grpc, dict):
            grpc = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc(**grpc)
        if isinstance(http_get, dict):
            http_get = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet(**http_get)
        if isinstance(tcp_socket, dict):
            tcp_socket = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket(**tcp_socket)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__138010664c6c0ec88aefb8cc7ab81600b69ca28d188079953e2d687c4947e04d)
            check_type(argname="argument exec", value=exec, expected_type=type_hints["exec"])
            check_type(argname="argument failure_threshold", value=failure_threshold, expected_type=type_hints["failure_threshold"])
            check_type(argname="argument grpc", value=grpc, expected_type=type_hints["grpc"])
            check_type(argname="argument http_get", value=http_get, expected_type=type_hints["http_get"])
            check_type(argname="argument initial_delay_seconds", value=initial_delay_seconds, expected_type=type_hints["initial_delay_seconds"])
            check_type(argname="argument period_seconds", value=period_seconds, expected_type=type_hints["period_seconds"])
            check_type(argname="argument success_threshold", value=success_threshold, expected_type=type_hints["success_threshold"])
            check_type(argname="argument tcp_socket", value=tcp_socket, expected_type=type_hints["tcp_socket"])
            check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exec is not None:
            self._values["exec"] = exec
        if failure_threshold is not None:
            self._values["failure_threshold"] = failure_threshold
        if grpc is not None:
            self._values["grpc"] = grpc
        if http_get is not None:
            self._values["http_get"] = http_get
        if initial_delay_seconds is not None:
            self._values["initial_delay_seconds"] = initial_delay_seconds
        if period_seconds is not None:
            self._values["period_seconds"] = period_seconds
        if success_threshold is not None:
            self._values["success_threshold"] = success_threshold
        if tcp_socket is not None:
            self._values["tcp_socket"] = tcp_socket
        if timeout_seconds is not None:
            self._values["timeout_seconds"] = timeout_seconds

    @builtins.property
    def exec(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec"]:
        '''exec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#exec GoogleVertexAiEndpointWithModelGardenDeployment#exec}
        '''
        result = self._values.get("exec")
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec"], result)

    @builtins.property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        '''Number of consecutive failures before the probe is considered failed. Defaults to 3. Minimum value is 1.

        Maps to Kubernetes probe argument 'failureThreshold'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#failure_threshold GoogleVertexAiEndpointWithModelGardenDeployment#failure_threshold}
        '''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def grpc(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc"]:
        '''grpc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#grpc GoogleVertexAiEndpointWithModelGardenDeployment#grpc}
        '''
        result = self._values.get("grpc")
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc"], result)

    @builtins.property
    def http_get(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet"]:
        '''http_get block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#http_get GoogleVertexAiEndpointWithModelGardenDeployment#http_get}
        '''
        result = self._values.get("http_get")
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet"], result)

    @builtins.property
    def initial_delay_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds to wait before starting the probe. Defaults to 0. Minimum value is 0.

        Maps to Kubernetes probe argument 'initialDelaySeconds'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#initial_delay_seconds GoogleVertexAiEndpointWithModelGardenDeployment#initial_delay_seconds}
        '''
        result = self._values.get("initial_delay_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period_seconds(self) -> typing.Optional[jsii.Number]:
        '''How often (in seconds) to perform the probe.

        Default to 10 seconds.
        Minimum value is 1. Must be less than timeout_seconds.

        Maps to Kubernetes probe argument 'periodSeconds'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#period_seconds GoogleVertexAiEndpointWithModelGardenDeployment#period_seconds}
        '''
        result = self._values.get("period_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def success_threshold(self) -> typing.Optional[jsii.Number]:
        '''Number of consecutive successes before the probe is considered successful. Defaults to 1. Minimum value is 1.

        Maps to Kubernetes probe argument 'successThreshold'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#success_threshold GoogleVertexAiEndpointWithModelGardenDeployment#success_threshold}
        '''
        result = self._values.get("success_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tcp_socket(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket"]:
        '''tcp_socket block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#tcp_socket GoogleVertexAiEndpointWithModelGardenDeployment#tcp_socket}
        '''
        result = self._values.get("tcp_socket")
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket"], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after which the probe times out.

        Defaults to 1 second.
        Minimum value is 1. Must be greater or equal to period_seconds.

        Maps to Kubernetes probe argument 'timeoutSeconds'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#timeout_seconds GoogleVertexAiEndpointWithModelGardenDeployment#timeout_seconds}
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec",
    jsii_struct_bases=[],
    name_mapping={"command": "command"},
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec:
    def __init__(
        self,
        *,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param command: Command is the command line to execute inside the container, the working directory for the command is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#command GoogleVertexAiEndpointWithModelGardenDeployment#command}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb472b0d84f16220c1070ee806c22747b79ac0a87f53ef6c5f851e9db9689150)
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if command is not None:
            self._values["command"] = command

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Command is the command line to execute inside the container, the working directory for the command is root ('/') in the container's filesystem.

        The command is simply exec'd, it is not run inside a shell, so
        traditional shell instructions ('|', etc) won't work. To use a shell, you
        need to explicitly call out to that shell. Exit status of 0 is treated as
        live/healthy and non-zero is unhealthy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#command GoogleVertexAiEndpointWithModelGardenDeployment#command}
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a06d260893bbf5cccf22e9a5991d84b5607074655b20274ab6847d668531afe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCommand")
    def reset_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommand", []))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b5c26c99dd04c5d970b61442b510a39ee67d4be0482e550b6b1d43e87f27232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e0c5195de666b1849ea5b9e5ecf36ca1a3d5b1c7b3a5974b82234454d8700bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "service": "service"},
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc:
    def __init__(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number of the gRPC service. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        :param service: Service is the name of the service to place in the gRPC HealthCheckRequest. See https://github.com/grpc/grpc/blob/master/doc/health-checking.md. If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#service GoogleVertexAiEndpointWithModelGardenDeployment#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4afa6901b8d699926c3af59d63477c4ed933b119e961a536b562be0d4169881)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if port is not None:
            self._values["port"] = port
        if service is not None:
            self._values["service"] = service

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number of the gRPC service. Number must be in the range 1 to 65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''Service is the name of the service to place in the gRPC HealthCheckRequest. See https://github.com/grpc/grpc/blob/master/doc/health-checking.md.

        If this is not specified, the default behavior is defined by gRPC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#service GoogleVertexAiEndpointWithModelGardenDeployment#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52286c3b4d8a7f43181803081a3fef0b4b1ce5c3d4eb6af5cd416c0fa3976e8d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetService")
    def reset_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetService", []))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__127679a83515bfac2e9ea7fe149671933e4a682ab11f57a7b1222603a5eae4a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdbe0447ec386053b9cf8615e1b5614609b415288f3f3c08a0f4570f2f0e62d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba90f60851b9837b8090ec59b9231f6194982723750305d2c8f186591e680358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "http_headers": "httpHeaders",
        "path": "path",
        "port": "port",
        "scheme": "scheme",
    },
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        scheme: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: Host name to connect to, defaults to the model serving container's IP. You probably want to set "Host" in httpHeaders instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#host GoogleVertexAiEndpointWithModelGardenDeployment#host}
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#http_headers GoogleVertexAiEndpointWithModelGardenDeployment#http_headers}
        :param path: Path to access on the HTTP server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#path GoogleVertexAiEndpointWithModelGardenDeployment#path}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        :param scheme: Scheme to use for connecting to the host. Defaults to HTTP. Acceptable values are "HTTP" or "HTTPS". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#scheme GoogleVertexAiEndpointWithModelGardenDeployment#scheme}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71cf8f1a06192cd2ce648e035e7053ca9dffbfa36777e2012b4dbc6825cd52e1)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument http_headers", value=http_headers, expected_type=type_hints["http_headers"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument scheme", value=scheme, expected_type=type_hints["scheme"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if host is not None:
            self._values["host"] = host
        if http_headers is not None:
            self._values["http_headers"] = http_headers
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port
        if scheme is not None:
            self._values["scheme"] = scheme

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Host name to connect to, defaults to the model serving container's IP.

        You probably want to set "Host" in httpHeaders instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#host GoogleVertexAiEndpointWithModelGardenDeployment#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders"]]]:
        '''http_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#http_headers GoogleVertexAiEndpointWithModelGardenDeployment#http_headers}
        '''
        result = self._values.get("http_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders"]]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to access on the HTTP server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#path GoogleVertexAiEndpointWithModelGardenDeployment#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Number of the port to access on the container. Number must be in the range 1 to 65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scheme(self) -> typing.Optional[builtins.str]:
        '''Scheme to use for connecting to the host. Defaults to HTTP. Acceptable values are "HTTP" or "HTTPS".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#scheme GoogleVertexAiEndpointWithModelGardenDeployment#scheme}
        '''
        result = self._values.get("scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The header field name. This will be canonicalized upon output, so case-variant names will be understood as the same header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#name GoogleVertexAiEndpointWithModelGardenDeployment#name}
        :param value: The header field value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#value GoogleVertexAiEndpointWithModelGardenDeployment#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34ce76d30eec4e1e2a0c5218d5a9e8357893e4ac911aea1534d53e20a819f6f4)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The header field name. This will be canonicalized upon output, so case-variant names will be understood as the same header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#name GoogleVertexAiEndpointWithModelGardenDeployment#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The header field value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#value GoogleVertexAiEndpointWithModelGardenDeployment#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5a99749d7f1eba810256a613c6d3ff0da46a8651339a3bea29803fdf5f1b280)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3216579f36baa61eec01ba3aabf64c4ed90cf5e2d3a5c96934cdf2516547eff0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__026bc5a5523aa070e4cc8e2d9c25eadf77258980ecc29fcd6d0ad78e7619425f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__def9175b48ad188d7c4cd081a525d5341b6b9c01d2d4ebeec66a905b28fad074)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cb7b10e82b11852bda5e4cdc909c91a2db5a78b1b34ab4f8ffe8adb3023de61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15ca3f0d448349f37a5871620d626400996e9ce1752448a78ca6c8b5e1d3c733)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae487bd0ba0784b534732fac8527d75734b10be7ccccc5e7f1a93dd79a747102)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52569f3b4f3f184bdcfbecab047505da066987ab6bf4f7233922ece90776e24b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f34b3a6c090c2fef954362582ec4dbd6d57a32e8798d29459f0d9b21f1f02476)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e8509ca6e51021dce08b03db1205f9f9e2df89b5cb55de5269f9242db391647)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d95ce3395ee8a6f11772a78c2b4b6cecbe07d505c86da0fd726c8e90c77d8b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpHeaders")
    def put_http_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a27bf3e3f4ff5ff4d25bb703d86dede449e48e7b0025b5453f42796adf32ce4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttpHeaders", [value]))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetHttpHeaders")
    def reset_http_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpHeaders", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetScheme")
    def reset_scheme(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheme", []))

    @builtins.property
    @jsii.member(jsii_name="httpHeaders")
    def http_headers(
        self,
    ) -> GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeadersList:
        return typing.cast(GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeadersList, jsii.get(self, "httpHeaders"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="httpHeadersInput")
    def http_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders]]], jsii.get(self, "httpHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="schemeInput")
    def scheme_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemeInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__441a04d9e34929b235ef6abac2ff6a1f5f09bbc0a227ab963e203c68e415bc60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5b154354f29c98e9c6cf405fcdf8bd39a0c27ef7a025ddfea08131f29cc169f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__776274a13cae7ce2f87c557effbb84639a0018ffa759e1fac221176a4faa2a44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheme")
    def scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheme"))

    @scheme.setter
    def scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e526590a8a179d0c60f21145d98fe575a6c9e6e5ca0a51f38aafbc82209f6a44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d58465ed5d76042b8f99d558ed294f7371da796974aeedb631b16134e7719843)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34b4399fbe62eee93d809b1c6c2a3a04f225cb1db49737566e85bf4ab55bde6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExec")
    def put_exec(
        self,
        *,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param command: Command is the command line to execute inside the container, the working directory for the command is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#command GoogleVertexAiEndpointWithModelGardenDeployment#command}
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec(
            command=command
        )

        return typing.cast(None, jsii.invoke(self, "putExec", [value]))

    @jsii.member(jsii_name="putGrpc")
    def put_grpc(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number of the gRPC service. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        :param service: Service is the name of the service to place in the gRPC HealthCheckRequest. See https://github.com/grpc/grpc/blob/master/doc/health-checking.md. If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#service GoogleVertexAiEndpointWithModelGardenDeployment#service}
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc(
            port=port, service=service
        )

        return typing.cast(None, jsii.invoke(self, "putGrpc", [value]))

    @jsii.member(jsii_name="putHttpGet")
    def put_http_get(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        scheme: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: Host name to connect to, defaults to the model serving container's IP. You probably want to set "Host" in httpHeaders instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#host GoogleVertexAiEndpointWithModelGardenDeployment#host}
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#http_headers GoogleVertexAiEndpointWithModelGardenDeployment#http_headers}
        :param path: Path to access on the HTTP server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#path GoogleVertexAiEndpointWithModelGardenDeployment#path}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        :param scheme: Scheme to use for connecting to the host. Defaults to HTTP. Acceptable values are "HTTP" or "HTTPS". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#scheme GoogleVertexAiEndpointWithModelGardenDeployment#scheme}
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet(
            host=host, http_headers=http_headers, path=path, port=port, scheme=scheme
        )

        return typing.cast(None, jsii.invoke(self, "putHttpGet", [value]))

    @jsii.member(jsii_name="putTcpSocket")
    def put_tcp_socket(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param host: Optional: Host name to connect to, defaults to the model serving container's IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#host GoogleVertexAiEndpointWithModelGardenDeployment#host}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket(
            host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putTcpSocket", [value]))

    @jsii.member(jsii_name="resetExec")
    def reset_exec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExec", []))

    @jsii.member(jsii_name="resetFailureThreshold")
    def reset_failure_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureThreshold", []))

    @jsii.member(jsii_name="resetGrpc")
    def reset_grpc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpc", []))

    @jsii.member(jsii_name="resetHttpGet")
    def reset_http_get(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpGet", []))

    @jsii.member(jsii_name="resetInitialDelaySeconds")
    def reset_initial_delay_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialDelaySeconds", []))

    @jsii.member(jsii_name="resetPeriodSeconds")
    def reset_period_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriodSeconds", []))

    @jsii.member(jsii_name="resetSuccessThreshold")
    def reset_success_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessThreshold", []))

    @jsii.member(jsii_name="resetTcpSocket")
    def reset_tcp_socket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpSocket", []))

    @jsii.member(jsii_name="resetTimeoutSeconds")
    def reset_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="exec")
    def exec(
        self,
    ) -> GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExecOutputReference:
        return typing.cast(GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExecOutputReference, jsii.get(self, "exec"))

    @builtins.property
    @jsii.member(jsii_name="grpc")
    def grpc(
        self,
    ) -> GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpcOutputReference:
        return typing.cast(GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpcOutputReference, jsii.get(self, "grpc"))

    @builtins.property
    @jsii.member(jsii_name="httpGet")
    def http_get(
        self,
    ) -> GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetOutputReference:
        return typing.cast(GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetOutputReference, jsii.get(self, "httpGet"))

    @builtins.property
    @jsii.member(jsii_name="tcpSocket")
    def tcp_socket(
        self,
    ) -> "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocketOutputReference":
        return typing.cast("GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocketOutputReference", jsii.get(self, "tcpSocket"))

    @builtins.property
    @jsii.member(jsii_name="execInput")
    def exec_input(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec], jsii.get(self, "execInput"))

    @builtins.property
    @jsii.member(jsii_name="failureThresholdInput")
    def failure_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcInput")
    def grpc_input(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc], jsii.get(self, "grpcInput"))

    @builtins.property
    @jsii.member(jsii_name="httpGetInput")
    def http_get_input(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet], jsii.get(self, "httpGetInput"))

    @builtins.property
    @jsii.member(jsii_name="initialDelaySecondsInput")
    def initial_delay_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialDelaySecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="periodSecondsInput")
    def period_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "periodSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="successThresholdInput")
    def success_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "successThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpSocketInput")
    def tcp_socket_input(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket"]:
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket"], jsii.get(self, "tcpSocketInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecondsInput")
    def timeout_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="failureThreshold")
    def failure_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failureThreshold"))

    @failure_threshold.setter
    def failure_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5f969cc151cde8058fc8d5c253946a6bc3e0bf7b4e780ee42f46ee856d6260e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelaySeconds")
    def initial_delay_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelaySeconds"))

    @initial_delay_seconds.setter
    def initial_delay_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1757c58ca9660857d69c01f8ceffee6e16f9aaf421e69ac0bc3042c4a6dc4800)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelaySeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodSeconds")
    def period_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodSeconds"))

    @period_seconds.setter
    def period_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72cd07704db5ddf847cb796bb63e1bec5988595d235407a90e94e8c587487659)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successThreshold")
    def success_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successThreshold"))

    @success_threshold.setter
    def success_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__485e69b47335c3079789f4d8773c3c5640ef489ea9efdcdb1064a9529e9b0205)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62b51f74c99e3765b34c77b1918dad5abf20f0235b6afa81321e56823ba41f52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fec5b6140f3268c88f1a74bd05ecedafc2edd8ddfad7f13c77ab3aae936ae88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket",
    jsii_struct_bases=[],
    name_mapping={"host": "host", "port": "port"},
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param host: Optional: Host name to connect to, defaults to the model serving container's IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#host GoogleVertexAiEndpointWithModelGardenDeployment#host}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8499000ff64f1231d2191275b013358e1a9e14a1a84a1baf8c17482b80bb532)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if host is not None:
            self._values["host"] = host
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Optional: Host name to connect to, defaults to the model serving container's IP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#host GoogleVertexAiEndpointWithModelGardenDeployment#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Number of the port to access on the container. Number must be in the range 1 to 65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocketOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocketOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f360184aab76b2b17367ee14636809b3a915738a8095dc3ad03d19ae268f450e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a1980ad966e7460fbcabc5b4650b5da07710382c16c677d8878f75fee9ca5ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a0861e3fa49eafa4ad52a7a512f5f5f4e651b083342a395e1cf8c6a2e4410f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e09f9545eaf8216fc2f947417650ab07c7a646f3cd0ea6029d5a9123fe965de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__297889be42cd0ccc13efa742a650870fa7d8e778d92b7926dec35874b1bebc1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEnv")
    def put_env(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__970a693c3b2f4309241082618367be714074a2d946597b6be6690f56a5992954)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnv", [value]))

    @jsii.member(jsii_name="putGrpcPorts")
    def put_grpc_ports(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd35c98590ed8c142be1bbe0e4e88a2ec770516a8567f5719936917fe7c23cc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGrpcPorts", [value]))

    @jsii.member(jsii_name="putHealthProbe")
    def put_health_probe(
        self,
        *,
        exec: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec, typing.Dict[builtins.str, typing.Any]]] = None,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        success_threshold: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param exec: exec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#exec GoogleVertexAiEndpointWithModelGardenDeployment#exec}
        :param failure_threshold: Number of consecutive failures before the probe is considered failed. Defaults to 3. Minimum value is 1. Maps to Kubernetes probe argument 'failureThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#failure_threshold GoogleVertexAiEndpointWithModelGardenDeployment#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#grpc GoogleVertexAiEndpointWithModelGardenDeployment#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#http_get GoogleVertexAiEndpointWithModelGardenDeployment#http_get}
        :param initial_delay_seconds: Number of seconds to wait before starting the probe. Defaults to 0. Minimum value is 0. Maps to Kubernetes probe argument 'initialDelaySeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#initial_delay_seconds GoogleVertexAiEndpointWithModelGardenDeployment#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Must be less than timeout_seconds. Maps to Kubernetes probe argument 'periodSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#period_seconds GoogleVertexAiEndpointWithModelGardenDeployment#period_seconds}
        :param success_threshold: Number of consecutive successes before the probe is considered successful. Defaults to 1. Minimum value is 1. Maps to Kubernetes probe argument 'successThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#success_threshold GoogleVertexAiEndpointWithModelGardenDeployment#success_threshold}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#tcp_socket GoogleVertexAiEndpointWithModelGardenDeployment#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Must be greater or equal to period_seconds. Maps to Kubernetes probe argument 'timeoutSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#timeout_seconds GoogleVertexAiEndpointWithModelGardenDeployment#timeout_seconds}
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe(
            exec=exec,
            failure_threshold=failure_threshold,
            grpc=grpc,
            http_get=http_get,
            initial_delay_seconds=initial_delay_seconds,
            period_seconds=period_seconds,
            success_threshold=success_threshold,
            tcp_socket=tcp_socket,
            timeout_seconds=timeout_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putHealthProbe", [value]))

    @jsii.member(jsii_name="putLivenessProbe")
    def put_liveness_probe(
        self,
        *,
        exec: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec, typing.Dict[builtins.str, typing.Any]]] = None,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        success_threshold: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param exec: exec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#exec GoogleVertexAiEndpointWithModelGardenDeployment#exec}
        :param failure_threshold: Number of consecutive failures before the probe is considered failed. Defaults to 3. Minimum value is 1. Maps to Kubernetes probe argument 'failureThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#failure_threshold GoogleVertexAiEndpointWithModelGardenDeployment#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#grpc GoogleVertexAiEndpointWithModelGardenDeployment#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#http_get GoogleVertexAiEndpointWithModelGardenDeployment#http_get}
        :param initial_delay_seconds: Number of seconds to wait before starting the probe. Defaults to 0. Minimum value is 0. Maps to Kubernetes probe argument 'initialDelaySeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#initial_delay_seconds GoogleVertexAiEndpointWithModelGardenDeployment#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Must be less than timeout_seconds. Maps to Kubernetes probe argument 'periodSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#period_seconds GoogleVertexAiEndpointWithModelGardenDeployment#period_seconds}
        :param success_threshold: Number of consecutive successes before the probe is considered successful. Defaults to 1. Minimum value is 1. Maps to Kubernetes probe argument 'successThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#success_threshold GoogleVertexAiEndpointWithModelGardenDeployment#success_threshold}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#tcp_socket GoogleVertexAiEndpointWithModelGardenDeployment#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Must be greater or equal to period_seconds. Maps to Kubernetes probe argument 'timeoutSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#timeout_seconds GoogleVertexAiEndpointWithModelGardenDeployment#timeout_seconds}
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe(
            exec=exec,
            failure_threshold=failure_threshold,
            grpc=grpc,
            http_get=http_get,
            initial_delay_seconds=initial_delay_seconds,
            period_seconds=period_seconds,
            success_threshold=success_threshold,
            tcp_socket=tcp_socket,
            timeout_seconds=timeout_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putLivenessProbe", [value]))

    @jsii.member(jsii_name="putPorts")
    def put_ports(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beb3c6af1f91093fae10cac2652333e393f11b1b0126e51382e33da5a6427469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPorts", [value]))

    @jsii.member(jsii_name="putStartupProbe")
    def put_startup_probe(
        self,
        *,
        exec: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec", typing.Dict[builtins.str, typing.Any]]] = None,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        success_threshold: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param exec: exec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#exec GoogleVertexAiEndpointWithModelGardenDeployment#exec}
        :param failure_threshold: Number of consecutive failures before the probe is considered failed. Defaults to 3. Minimum value is 1. Maps to Kubernetes probe argument 'failureThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#failure_threshold GoogleVertexAiEndpointWithModelGardenDeployment#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#grpc GoogleVertexAiEndpointWithModelGardenDeployment#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#http_get GoogleVertexAiEndpointWithModelGardenDeployment#http_get}
        :param initial_delay_seconds: Number of seconds to wait before starting the probe. Defaults to 0. Minimum value is 0. Maps to Kubernetes probe argument 'initialDelaySeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#initial_delay_seconds GoogleVertexAiEndpointWithModelGardenDeployment#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Must be less than timeout_seconds. Maps to Kubernetes probe argument 'periodSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#period_seconds GoogleVertexAiEndpointWithModelGardenDeployment#period_seconds}
        :param success_threshold: Number of consecutive successes before the probe is considered successful. Defaults to 1. Minimum value is 1. Maps to Kubernetes probe argument 'successThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#success_threshold GoogleVertexAiEndpointWithModelGardenDeployment#success_threshold}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#tcp_socket GoogleVertexAiEndpointWithModelGardenDeployment#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Must be greater or equal to period_seconds. Maps to Kubernetes probe argument 'timeoutSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#timeout_seconds GoogleVertexAiEndpointWithModelGardenDeployment#timeout_seconds}
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe(
            exec=exec,
            failure_threshold=failure_threshold,
            grpc=grpc,
            http_get=http_get,
            initial_delay_seconds=initial_delay_seconds,
            period_seconds=period_seconds,
            success_threshold=success_threshold,
            tcp_socket=tcp_socket,
            timeout_seconds=timeout_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putStartupProbe", [value]))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetCommand")
    def reset_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommand", []))

    @jsii.member(jsii_name="resetDeploymentTimeout")
    def reset_deployment_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentTimeout", []))

    @jsii.member(jsii_name="resetEnv")
    def reset_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnv", []))

    @jsii.member(jsii_name="resetGrpcPorts")
    def reset_grpc_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpcPorts", []))

    @jsii.member(jsii_name="resetHealthProbe")
    def reset_health_probe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthProbe", []))

    @jsii.member(jsii_name="resetHealthRoute")
    def reset_health_route(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthRoute", []))

    @jsii.member(jsii_name="resetLivenessProbe")
    def reset_liveness_probe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLivenessProbe", []))

    @jsii.member(jsii_name="resetPorts")
    def reset_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPorts", []))

    @jsii.member(jsii_name="resetPredictRoute")
    def reset_predict_route(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPredictRoute", []))

    @jsii.member(jsii_name="resetSharedMemorySizeMb")
    def reset_shared_memory_size_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedMemorySizeMb", []))

    @jsii.member(jsii_name="resetStartupProbe")
    def reset_startup_probe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartupProbe", []))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(
        self,
    ) -> GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnvList:
        return typing.cast(GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnvList, jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="grpcPorts")
    def grpc_ports(
        self,
    ) -> GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPortsList:
        return typing.cast(GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPortsList, jsii.get(self, "grpcPorts"))

    @builtins.property
    @jsii.member(jsii_name="healthProbe")
    def health_probe(
        self,
    ) -> GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeOutputReference:
        return typing.cast(GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeOutputReference, jsii.get(self, "healthProbe"))

    @builtins.property
    @jsii.member(jsii_name="livenessProbe")
    def liveness_probe(
        self,
    ) -> GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeOutputReference:
        return typing.cast(GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeOutputReference, jsii.get(self, "livenessProbe"))

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(
        self,
    ) -> "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPortsList":
        return typing.cast("GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPortsList", jsii.get(self, "ports"))

    @builtins.property
    @jsii.member(jsii_name="startupProbe")
    def startup_probe(
        self,
    ) -> "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeOutputReference":
        return typing.cast("GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeOutputReference", jsii.get(self, "startupProbe"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentTimeoutInput")
    def deployment_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv]]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcPortsInput")
    def grpc_ports_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts]]], jsii.get(self, "grpcPortsInput"))

    @builtins.property
    @jsii.member(jsii_name="healthProbeInput")
    def health_probe_input(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe], jsii.get(self, "healthProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="healthRouteInput")
    def health_route_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthRouteInput"))

    @builtins.property
    @jsii.member(jsii_name="imageUriInput")
    def image_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageUriInput"))

    @builtins.property
    @jsii.member(jsii_name="livenessProbeInput")
    def liveness_probe_input(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe], jsii.get(self, "livenessProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts"]]], jsii.get(self, "portsInput"))

    @builtins.property
    @jsii.member(jsii_name="predictRouteInput")
    def predict_route_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "predictRouteInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedMemorySizeMbInput")
    def shared_memory_size_mb_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sharedMemorySizeMbInput"))

    @builtins.property
    @jsii.member(jsii_name="startupProbeInput")
    def startup_probe_input(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe"]:
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe"], jsii.get(self, "startupProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbc659cd5d7e3d4db48695c9214e7b6704b7ba136e50eef38c1e8411867e8227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__976bdcec2a190bb624576e9a63a5f0baf57817e21a51b10131fb9594c39076d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deploymentTimeout")
    def deployment_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentTimeout"))

    @deployment_timeout.setter
    def deployment_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d0bfacdefe00b7a9f34a1f46f08a5211d7613a50cb10c9ca1f611f270a51dd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthRoute")
    def health_route(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthRoute"))

    @health_route.setter
    def health_route(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8deec4c43f0dbc388bd7eafec7973e18a3c472fa816863bf570b04b2a45c0575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthRoute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageUri")
    def image_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageUri"))

    @image_uri.setter
    def image_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7f8c96b318d7ea0f53841e340b0383c5c3e090b774056c3adfd825a90a4f451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="predictRoute")
    def predict_route(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "predictRoute"))

    @predict_route.setter
    def predict_route(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc7d8f24377720e53840257aebbc5e1ce5d5f40cca36237a68af5d3d19e483ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predictRoute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sharedMemorySizeMb")
    def shared_memory_size_mb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sharedMemorySizeMb"))

    @shared_memory_size_mb.setter
    def shared_memory_size_mb(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c1629ea1571f42e718fc92f0346ebc02986718a8931e83631a8825e995c1dca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedMemorySizeMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27d9a9d9a46ce029a1d0593e44cdac5d2a27ad1ce684c17473ef6fe9c56630b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts",
    jsii_struct_bases=[],
    name_mapping={"container_port": "containerPort"},
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts:
    def __init__(self, *, container_port: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param container_port: The number of the port to expose on the pod's IP address. Must be a valid port number, between 1 and 65535 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#container_port GoogleVertexAiEndpointWithModelGardenDeployment#container_port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__774cd66a68f6821d8c8ec5cd6fec04a4b68205381f272972b2d79f3584dd3fdb)
            check_type(argname="argument container_port", value=container_port, expected_type=type_hints["container_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_port is not None:
            self._values["container_port"] = container_port

    @builtins.property
    def container_port(self) -> typing.Optional[jsii.Number]:
        '''The number of the port to expose on the pod's IP address.

        Must be a valid port number, between 1 and 65535 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#container_port GoogleVertexAiEndpointWithModelGardenDeployment#container_port}
        '''
        result = self._values.get("container_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPortsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPortsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b34677d8c14d79caaa0044f9eeba8940f903013b67f9575a36f15fde4a3f15f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPortsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb2c69114e033ed80aefb51619330cb4a487c1fb4c448cf1f8c924976685b67f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPortsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dd0edafceef661378e82d08f1cbd8377f3780bc595fbf508e6fd6bbdd42dbe6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e09d4beea876036709e02cbd52bd2dfdffa5c3f5acd79a13741ef677ce62d9d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9c7d2dcd1f95d999186a3a0f30432123f3901e16c2301ba944e4f916e8116ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e208f12c72b4a31bbb4ef5857052c8468c6ab34e57d58109335611f82840a9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPortsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPortsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f486d7947f3e0d2edd77cccaf21de8594dfa7f137971f7a3b598ed86ef27b144)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContainerPort")
    def reset_container_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerPort", []))

    @builtins.property
    @jsii.member(jsii_name="containerPortInput")
    def container_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "containerPortInput"))

    @builtins.property
    @jsii.member(jsii_name="containerPort")
    def container_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerPort"))

    @container_port.setter
    def container_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c76c976a91bfbe2349e6786d9cca237e845d9e97d4b63e8b7d3edd9a48db4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5cf79a69fa60a154c73eb242ebece7acea05e92ce3277ccb3d3977ce22a7caa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe",
    jsii_struct_bases=[],
    name_mapping={
        "exec": "exec",
        "failure_threshold": "failureThreshold",
        "grpc": "grpc",
        "http_get": "httpGet",
        "initial_delay_seconds": "initialDelaySeconds",
        "period_seconds": "periodSeconds",
        "success_threshold": "successThreshold",
        "tcp_socket": "tcpSocket",
        "timeout_seconds": "timeoutSeconds",
    },
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe:
    def __init__(
        self,
        *,
        exec: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec", typing.Dict[builtins.str, typing.Any]]] = None,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        success_threshold: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param exec: exec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#exec GoogleVertexAiEndpointWithModelGardenDeployment#exec}
        :param failure_threshold: Number of consecutive failures before the probe is considered failed. Defaults to 3. Minimum value is 1. Maps to Kubernetes probe argument 'failureThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#failure_threshold GoogleVertexAiEndpointWithModelGardenDeployment#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#grpc GoogleVertexAiEndpointWithModelGardenDeployment#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#http_get GoogleVertexAiEndpointWithModelGardenDeployment#http_get}
        :param initial_delay_seconds: Number of seconds to wait before starting the probe. Defaults to 0. Minimum value is 0. Maps to Kubernetes probe argument 'initialDelaySeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#initial_delay_seconds GoogleVertexAiEndpointWithModelGardenDeployment#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Must be less than timeout_seconds. Maps to Kubernetes probe argument 'periodSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#period_seconds GoogleVertexAiEndpointWithModelGardenDeployment#period_seconds}
        :param success_threshold: Number of consecutive successes before the probe is considered successful. Defaults to 1. Minimum value is 1. Maps to Kubernetes probe argument 'successThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#success_threshold GoogleVertexAiEndpointWithModelGardenDeployment#success_threshold}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#tcp_socket GoogleVertexAiEndpointWithModelGardenDeployment#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Must be greater or equal to period_seconds. Maps to Kubernetes probe argument 'timeoutSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#timeout_seconds GoogleVertexAiEndpointWithModelGardenDeployment#timeout_seconds}
        '''
        if isinstance(exec, dict):
            exec = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec(**exec)
        if isinstance(grpc, dict):
            grpc = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc(**grpc)
        if isinstance(http_get, dict):
            http_get = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet(**http_get)
        if isinstance(tcp_socket, dict):
            tcp_socket = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket(**tcp_socket)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4f1f7311ed370b64f86474bd3eb7438c9f74dee3259c98f9deded6ed9f4a94)
            check_type(argname="argument exec", value=exec, expected_type=type_hints["exec"])
            check_type(argname="argument failure_threshold", value=failure_threshold, expected_type=type_hints["failure_threshold"])
            check_type(argname="argument grpc", value=grpc, expected_type=type_hints["grpc"])
            check_type(argname="argument http_get", value=http_get, expected_type=type_hints["http_get"])
            check_type(argname="argument initial_delay_seconds", value=initial_delay_seconds, expected_type=type_hints["initial_delay_seconds"])
            check_type(argname="argument period_seconds", value=period_seconds, expected_type=type_hints["period_seconds"])
            check_type(argname="argument success_threshold", value=success_threshold, expected_type=type_hints["success_threshold"])
            check_type(argname="argument tcp_socket", value=tcp_socket, expected_type=type_hints["tcp_socket"])
            check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exec is not None:
            self._values["exec"] = exec
        if failure_threshold is not None:
            self._values["failure_threshold"] = failure_threshold
        if grpc is not None:
            self._values["grpc"] = grpc
        if http_get is not None:
            self._values["http_get"] = http_get
        if initial_delay_seconds is not None:
            self._values["initial_delay_seconds"] = initial_delay_seconds
        if period_seconds is not None:
            self._values["period_seconds"] = period_seconds
        if success_threshold is not None:
            self._values["success_threshold"] = success_threshold
        if tcp_socket is not None:
            self._values["tcp_socket"] = tcp_socket
        if timeout_seconds is not None:
            self._values["timeout_seconds"] = timeout_seconds

    @builtins.property
    def exec(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec"]:
        '''exec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#exec GoogleVertexAiEndpointWithModelGardenDeployment#exec}
        '''
        result = self._values.get("exec")
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec"], result)

    @builtins.property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        '''Number of consecutive failures before the probe is considered failed. Defaults to 3. Minimum value is 1.

        Maps to Kubernetes probe argument 'failureThreshold'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#failure_threshold GoogleVertexAiEndpointWithModelGardenDeployment#failure_threshold}
        '''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def grpc(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc"]:
        '''grpc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#grpc GoogleVertexAiEndpointWithModelGardenDeployment#grpc}
        '''
        result = self._values.get("grpc")
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc"], result)

    @builtins.property
    def http_get(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet"]:
        '''http_get block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#http_get GoogleVertexAiEndpointWithModelGardenDeployment#http_get}
        '''
        result = self._values.get("http_get")
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet"], result)

    @builtins.property
    def initial_delay_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds to wait before starting the probe. Defaults to 0. Minimum value is 0.

        Maps to Kubernetes probe argument 'initialDelaySeconds'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#initial_delay_seconds GoogleVertexAiEndpointWithModelGardenDeployment#initial_delay_seconds}
        '''
        result = self._values.get("initial_delay_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period_seconds(self) -> typing.Optional[jsii.Number]:
        '''How often (in seconds) to perform the probe.

        Default to 10 seconds.
        Minimum value is 1. Must be less than timeout_seconds.

        Maps to Kubernetes probe argument 'periodSeconds'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#period_seconds GoogleVertexAiEndpointWithModelGardenDeployment#period_seconds}
        '''
        result = self._values.get("period_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def success_threshold(self) -> typing.Optional[jsii.Number]:
        '''Number of consecutive successes before the probe is considered successful. Defaults to 1. Minimum value is 1.

        Maps to Kubernetes probe argument 'successThreshold'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#success_threshold GoogleVertexAiEndpointWithModelGardenDeployment#success_threshold}
        '''
        result = self._values.get("success_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tcp_socket(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket"]:
        '''tcp_socket block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#tcp_socket GoogleVertexAiEndpointWithModelGardenDeployment#tcp_socket}
        '''
        result = self._values.get("tcp_socket")
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket"], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after which the probe times out.

        Defaults to 1 second.
        Minimum value is 1. Must be greater or equal to period_seconds.

        Maps to Kubernetes probe argument 'timeoutSeconds'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#timeout_seconds GoogleVertexAiEndpointWithModelGardenDeployment#timeout_seconds}
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec",
    jsii_struct_bases=[],
    name_mapping={"command": "command"},
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec:
    def __init__(
        self,
        *,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param command: Command is the command line to execute inside the container, the working directory for the command is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#command GoogleVertexAiEndpointWithModelGardenDeployment#command}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5113d0fc1526fbc88af3fad124beaf8a17f3241a38699c75d3a52abcdb2b6d5e)
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if command is not None:
            self._values["command"] = command

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Command is the command line to execute inside the container, the working directory for the command is root ('/') in the container's filesystem.

        The command is simply exec'd, it is not run inside a shell, so
        traditional shell instructions ('|', etc) won't work. To use a shell, you
        need to explicitly call out to that shell. Exit status of 0 is treated as
        live/healthy and non-zero is unhealthy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#command GoogleVertexAiEndpointWithModelGardenDeployment#command}
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__143d7c18d581e5f1f0c494716d613e59b30eca0ff97a45bf7381ba5b86c98cb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCommand")
    def reset_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommand", []))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03b8141c0dbef6743842e67ad8562ab43a9eecf6e0a0f9f47d46c79fb8360283)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef4cc85b22f0fc3719507ccf71d0f5c70a7be76b4b7ccfcab849aa68f9b7c02f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "service": "service"},
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc:
    def __init__(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number of the gRPC service. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        :param service: Service is the name of the service to place in the gRPC HealthCheckRequest. See https://github.com/grpc/grpc/blob/master/doc/health-checking.md. If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#service GoogleVertexAiEndpointWithModelGardenDeployment#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14f40ccae1230ebebc5684881ba48ad748868919851833406ef32eef1f231bf1)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if port is not None:
            self._values["port"] = port
        if service is not None:
            self._values["service"] = service

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number of the gRPC service. Number must be in the range 1 to 65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''Service is the name of the service to place in the gRPC HealthCheckRequest. See https://github.com/grpc/grpc/blob/master/doc/health-checking.md.

        If this is not specified, the default behavior is defined by gRPC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#service GoogleVertexAiEndpointWithModelGardenDeployment#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__152e83c19d045ff15798cfa2f4c8de49c2a5b71b7784d0b7c7d1da13645a4be3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetService")
    def reset_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetService", []))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47a6bba92047f7bd2d927fd0c1ec956ef6593a120da7804bf3ce2a9329d78ed6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66ebccea8074be76466a3d5feafb7a1f1495249aa9c69bd141268e8e597b86a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2e162d8d2e3ce578eb62f60879533b038f2ebec01be4108da95b9f127ac7444)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "http_headers": "httpHeaders",
        "path": "path",
        "port": "port",
        "scheme": "scheme",
    },
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        scheme: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: Host name to connect to, defaults to the model serving container's IP. You probably want to set "Host" in httpHeaders instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#host GoogleVertexAiEndpointWithModelGardenDeployment#host}
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#http_headers GoogleVertexAiEndpointWithModelGardenDeployment#http_headers}
        :param path: Path to access on the HTTP server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#path GoogleVertexAiEndpointWithModelGardenDeployment#path}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        :param scheme: Scheme to use for connecting to the host. Defaults to HTTP. Acceptable values are "HTTP" or "HTTPS". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#scheme GoogleVertexAiEndpointWithModelGardenDeployment#scheme}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9fa989a22bd2eea4c416626f71401fee2f743dd31ddaecfd57da17c2bc4d0f6)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument http_headers", value=http_headers, expected_type=type_hints["http_headers"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument scheme", value=scheme, expected_type=type_hints["scheme"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if host is not None:
            self._values["host"] = host
        if http_headers is not None:
            self._values["http_headers"] = http_headers
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port
        if scheme is not None:
            self._values["scheme"] = scheme

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Host name to connect to, defaults to the model serving container's IP.

        You probably want to set "Host" in httpHeaders instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#host GoogleVertexAiEndpointWithModelGardenDeployment#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders"]]]:
        '''http_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#http_headers GoogleVertexAiEndpointWithModelGardenDeployment#http_headers}
        '''
        result = self._values.get("http_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders"]]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to access on the HTTP server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#path GoogleVertexAiEndpointWithModelGardenDeployment#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Number of the port to access on the container. Number must be in the range 1 to 65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scheme(self) -> typing.Optional[builtins.str]:
        '''Scheme to use for connecting to the host. Defaults to HTTP. Acceptable values are "HTTP" or "HTTPS".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#scheme GoogleVertexAiEndpointWithModelGardenDeployment#scheme}
        '''
        result = self._values.get("scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The header field name. This will be canonicalized upon output, so case-variant names will be understood as the same header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#name GoogleVertexAiEndpointWithModelGardenDeployment#name}
        :param value: The header field value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#value GoogleVertexAiEndpointWithModelGardenDeployment#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2afb7b770b33b73fb8578d0b8bae3dd70bfc74e23bcedc4231f404cabb6f9502)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The header field name. This will be canonicalized upon output, so case-variant names will be understood as the same header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#name GoogleVertexAiEndpointWithModelGardenDeployment#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The header field value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#value GoogleVertexAiEndpointWithModelGardenDeployment#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a42bb6732bd9c6cd0d79b82b63c31e3f7cc71a446ad28c4e01e8ef655b48280)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27d8c532af684925f0ba5a8279a243e5a4ad43354c4b495c101b7c58730ae009)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__151126f4767b8b683d3a00644f8afa76df712c62113e42fa01024b4b069cc678)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c5c1d79c3c0764205253f42031169c875e31026aaba6641bab5f0320568ff41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80d62aad65ec3f4599a0537fb735df15a0748762747f82a2a28f232bf59d4e07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c69102acb90b7686fd8a56bdc4f18502c7462bf0f31b7a0e7f10291f443d73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bbdd7f34ddaf1c423b0c289c23959b53490d1fc92b1948fafa34873f8541c13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f388aa84def199c5296c68b1ed95f78e3dd108ce7cf356b34398c2c8266cdfd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d599bf091cd20b6673c0bcb36e36fa2c84ff9d90d63ccad2db9ab77b7dc14a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a880d689affa4d6ebb7a9446febd467bc807ba9081ada2d4b846822a8b6d2aa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b407cd1e9e242e73be5575838d860e41e228b54f69dbf25b3cf5850c99846a16)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpHeaders")
    def put_http_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a66c0e6d31c9f588e3eccffe7bea2c5075e451c2753dd7106616b775b0884a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttpHeaders", [value]))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetHttpHeaders")
    def reset_http_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpHeaders", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetScheme")
    def reset_scheme(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheme", []))

    @builtins.property
    @jsii.member(jsii_name="httpHeaders")
    def http_headers(
        self,
    ) -> GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeadersList:
        return typing.cast(GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeadersList, jsii.get(self, "httpHeaders"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="httpHeadersInput")
    def http_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders]]], jsii.get(self, "httpHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="schemeInput")
    def scheme_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemeInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d7b139d8928d8e4293fda1623296fdc65e385ddb323a6b275b6bffff86fd878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d52fed98bd2ccad13a4e3920ebdd2bdfb8d050ad302773692c6bf7c7956890b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__770af3f7b223384caf377bcdf1f8bac28c5b496c87492b7673230235e6865891)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheme")
    def scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheme"))

    @scheme.setter
    def scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b1143b0a1e77292924a151359fe314106d9b89b8567297cfb47d525a71c2eac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06cf3219b30544a745bdc2338fa09e92275889ee4410466b1918bea5ab80f096)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96315acd040c16a9a4173e45375ea60d9ca4fdf6afed2ad3da78a9b214062e7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExec")
    def put_exec(
        self,
        *,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param command: Command is the command line to execute inside the container, the working directory for the command is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#command GoogleVertexAiEndpointWithModelGardenDeployment#command}
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec(
            command=command
        )

        return typing.cast(None, jsii.invoke(self, "putExec", [value]))

    @jsii.member(jsii_name="putGrpc")
    def put_grpc(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number of the gRPC service. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        :param service: Service is the name of the service to place in the gRPC HealthCheckRequest. See https://github.com/grpc/grpc/blob/master/doc/health-checking.md. If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#service GoogleVertexAiEndpointWithModelGardenDeployment#service}
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc(
            port=port, service=service
        )

        return typing.cast(None, jsii.invoke(self, "putGrpc", [value]))

    @jsii.member(jsii_name="putHttpGet")
    def put_http_get(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        scheme: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: Host name to connect to, defaults to the model serving container's IP. You probably want to set "Host" in httpHeaders instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#host GoogleVertexAiEndpointWithModelGardenDeployment#host}
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#http_headers GoogleVertexAiEndpointWithModelGardenDeployment#http_headers}
        :param path: Path to access on the HTTP server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#path GoogleVertexAiEndpointWithModelGardenDeployment#path}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        :param scheme: Scheme to use for connecting to the host. Defaults to HTTP. Acceptable values are "HTTP" or "HTTPS". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#scheme GoogleVertexAiEndpointWithModelGardenDeployment#scheme}
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet(
            host=host, http_headers=http_headers, path=path, port=port, scheme=scheme
        )

        return typing.cast(None, jsii.invoke(self, "putHttpGet", [value]))

    @jsii.member(jsii_name="putTcpSocket")
    def put_tcp_socket(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param host: Optional: Host name to connect to, defaults to the model serving container's IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#host GoogleVertexAiEndpointWithModelGardenDeployment#host}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket(
            host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putTcpSocket", [value]))

    @jsii.member(jsii_name="resetExec")
    def reset_exec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExec", []))

    @jsii.member(jsii_name="resetFailureThreshold")
    def reset_failure_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureThreshold", []))

    @jsii.member(jsii_name="resetGrpc")
    def reset_grpc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpc", []))

    @jsii.member(jsii_name="resetHttpGet")
    def reset_http_get(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpGet", []))

    @jsii.member(jsii_name="resetInitialDelaySeconds")
    def reset_initial_delay_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialDelaySeconds", []))

    @jsii.member(jsii_name="resetPeriodSeconds")
    def reset_period_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriodSeconds", []))

    @jsii.member(jsii_name="resetSuccessThreshold")
    def reset_success_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessThreshold", []))

    @jsii.member(jsii_name="resetTcpSocket")
    def reset_tcp_socket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpSocket", []))

    @jsii.member(jsii_name="resetTimeoutSeconds")
    def reset_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="exec")
    def exec(
        self,
    ) -> GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExecOutputReference:
        return typing.cast(GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExecOutputReference, jsii.get(self, "exec"))

    @builtins.property
    @jsii.member(jsii_name="grpc")
    def grpc(
        self,
    ) -> GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpcOutputReference:
        return typing.cast(GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpcOutputReference, jsii.get(self, "grpc"))

    @builtins.property
    @jsii.member(jsii_name="httpGet")
    def http_get(
        self,
    ) -> GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetOutputReference:
        return typing.cast(GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetOutputReference, jsii.get(self, "httpGet"))

    @builtins.property
    @jsii.member(jsii_name="tcpSocket")
    def tcp_socket(
        self,
    ) -> "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocketOutputReference":
        return typing.cast("GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocketOutputReference", jsii.get(self, "tcpSocket"))

    @builtins.property
    @jsii.member(jsii_name="execInput")
    def exec_input(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec], jsii.get(self, "execInput"))

    @builtins.property
    @jsii.member(jsii_name="failureThresholdInput")
    def failure_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcInput")
    def grpc_input(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc], jsii.get(self, "grpcInput"))

    @builtins.property
    @jsii.member(jsii_name="httpGetInput")
    def http_get_input(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet], jsii.get(self, "httpGetInput"))

    @builtins.property
    @jsii.member(jsii_name="initialDelaySecondsInput")
    def initial_delay_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialDelaySecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="periodSecondsInput")
    def period_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "periodSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="successThresholdInput")
    def success_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "successThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpSocketInput")
    def tcp_socket_input(
        self,
    ) -> typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket"]:
        return typing.cast(typing.Optional["GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket"], jsii.get(self, "tcpSocketInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecondsInput")
    def timeout_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="failureThreshold")
    def failure_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failureThreshold"))

    @failure_threshold.setter
    def failure_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43af110759a1f7f0e71d6448fbb669dfe02440946bdbdc8ccf7b44799f6e9046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelaySeconds")
    def initial_delay_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelaySeconds"))

    @initial_delay_seconds.setter
    def initial_delay_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b77c2247385ed17a815e1ec85e220f2d99ecc6e3a251f7b66d296efc1b4e1e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelaySeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodSeconds")
    def period_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodSeconds"))

    @period_seconds.setter
    def period_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a92b6fa77972c5e5aa8e591a4d65139f1872183c3c776ae9c2c76794d8a180a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successThreshold")
    def success_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successThreshold"))

    @success_threshold.setter
    def success_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b710a2cf70be7c942d1018a5247ed179dfbf70957affbff3c07f6449485e95fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77e4be356a463940163954b432ea9b3847c574c8d9af7329c89937ccebaad056)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa7e6518fdcb9216b7b1edaf27f965dfb4fa96d454305ce39a8971e4e9f10ae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket",
    jsii_struct_bases=[],
    name_mapping={"host": "host", "port": "port"},
)
class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param host: Optional: Host name to connect to, defaults to the model serving container's IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#host GoogleVertexAiEndpointWithModelGardenDeployment#host}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dfe3d5ee4e2f661b9829d5fb856b55fc69b072d7eb31ebf3521540ca379882a)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if host is not None:
            self._values["host"] = host
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Optional: Host name to connect to, defaults to the model serving container's IP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#host GoogleVertexAiEndpointWithModelGardenDeployment#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Number of the port to access on the container. Number must be in the range 1 to 65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#port GoogleVertexAiEndpointWithModelGardenDeployment#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocketOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocketOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47e5abea638d4c981089d6166242646427ce1851be354df278202b41cd7021c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb4774a5939c09ab7e2bf33386ec9cdbcf7ba828c30792df53964af1df540631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd5a22aa8565075d9740200ec060f2c3607e0ce8bac04570617a0ae17be381b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c143203de9764721e1555ad86db1d960607e4825addf7688cd2b06fcb2f4dc43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b6c36a77160d98dc5302576803d7a7ab6545b553ff189029bcf586314ed1ad9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContainerSpec")
    def put_container_spec(
        self,
        *,
        image_uri: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        deployment_timeout: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv, typing.Dict[builtins.str, typing.Any]]]]] = None,
        grpc_ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts, typing.Dict[builtins.str, typing.Any]]]]] = None,
        health_probe: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe, typing.Dict[builtins.str, typing.Any]]] = None,
        health_route: typing.Optional[builtins.str] = None,
        liveness_probe: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe, typing.Dict[builtins.str, typing.Any]]] = None,
        ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts, typing.Dict[builtins.str, typing.Any]]]]] = None,
        predict_route: typing.Optional[builtins.str] = None,
        shared_memory_size_mb: typing.Optional[builtins.str] = None,
        startup_probe: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param image_uri: URI of the Docker image to be used as the custom container for serving predictions. This URI must identify an image in Artifact Registry or Container Registry. Learn more about the `container publishing requirements <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#publishing>`_, including permissions requirements for the Vertex AI Service Agent. The container image is ingested upon ModelService.UploadModel, stored internally, and this original path is afterwards not used. To learn about the requirements for the Docker image itself, see `Custom container requirements <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#>`_. You can use the URI to one of Vertex AI's `pre-built container images for prediction <https://cloud.google.com/vertex-ai/docs/predictions/pre-built-containers>`_ in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#image_uri GoogleVertexAiEndpointWithModelGardenDeployment#image_uri}
        :param args: Specifies arguments for the command that runs when the container starts. This overrides the container's `'CMD' <https://docs.docker.com/engine/reference/builder/#cmd>`_. Specify this field as an array of executable and arguments, similar to a Docker 'CMD''s "default parameters" form. If you don't specify this field but do specify the command field, then the command from the 'command' field runs without any additional arguments. See the `Kubernetes documentation about how the 'command' and 'args' fields interact with a container's 'ENTRYPOINT' and 'CMD' <https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#notes>`_. If you don't specify this field and don't specify the 'command' field, then the container's `'ENTRYPOINT' <https://docs.docker.com/engine/reference/builder/#cmd>`_ and 'CMD' determine what runs based on their default behavior. See the Docker documentation about `how 'CMD' and 'ENTRYPOINT' interact <https://docs.docker.com/engine/reference/builder/#understand-how-cmd-and-entrypoint-interact>`_. In this field, you can reference `environment variables set by Vertex AI <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_ and environment variables set in the env field. You cannot reference environment variables set in the Docker image. In order for environment variables to be expanded, reference them by using the following syntax:$(VARIABLE_NAME) Note that this differs from Bash variable expansion, which does not use parentheses. If a variable cannot be resolved, the reference in the input string is used unchanged. To avoid variable expansion, you can escape this syntax with '$$'; for example:$$(VARIABLE_NAME) This field corresponds to the 'args' field of the Kubernetes Containers `v1 core API <https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.23/#container-v1-core>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#args GoogleVertexAiEndpointWithModelGardenDeployment#args}
        :param command: Specifies the command that runs when the container starts. This overrides the container's `ENTRYPOINT <https://docs.docker.com/engine/reference/builder/#entrypoint>`_. Specify this field as an array of executable and arguments, similar to a Docker 'ENTRYPOINT''s "exec" form, not its "shell" form. If you do not specify this field, then the container's 'ENTRYPOINT' runs, in conjunction with the args field or the container's `'CMD' <https://docs.docker.com/engine/reference/builder/#cmd>`_, if either exists. If this field is not specified and the container does not have an 'ENTRYPOINT', then refer to the Docker documentation about `how 'CMD' and 'ENTRYPOINT' interact <https://docs.docker.com/engine/reference/builder/#understand-how-cmd-and-entrypoint-interact>`_. If you specify this field, then you can also specify the 'args' field to provide additional arguments for this command. However, if you specify this field, then the container's 'CMD' is ignored. See the `Kubernetes documentation about how the 'command' and 'args' fields interact with a container's 'ENTRYPOINT' and 'CMD' <https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#notes>`_. In this field, you can reference `environment variables set by Vertex AI <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_ and environment variables set in the env field. You cannot reference environment variables set in the Docker image. In order for environment variables to be expanded, reference them by using the following syntax:$(VARIABLE_NAME) Note that this differs from Bash variable expansion, which does not use parentheses. If a variable cannot be resolved, the reference in the input string is used unchanged. To avoid variable expansion, you can escape this syntax with '$$'; for example:$$(VARIABLE_NAME) This field corresponds to the 'command' field of the Kubernetes Containers `v1 core API <https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.23/#container-v1-core>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#command GoogleVertexAiEndpointWithModelGardenDeployment#command}
        :param deployment_timeout: Deployment timeout. Limit for deployment timeout is 2 hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#deployment_timeout GoogleVertexAiEndpointWithModelGardenDeployment#deployment_timeout}
        :param env: env block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#env GoogleVertexAiEndpointWithModelGardenDeployment#env}
        :param grpc_ports: grpc_ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#grpc_ports GoogleVertexAiEndpointWithModelGardenDeployment#grpc_ports}
        :param health_probe: health_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#health_probe GoogleVertexAiEndpointWithModelGardenDeployment#health_probe}
        :param health_route: HTTP path on the container to send health checks to. Vertex AI intermittently sends GET requests to this path on the container's IP address and port to check that the container is healthy. Read more about `health checks <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#health>`_. For example, if you set this field to '/bar', then Vertex AI intermittently sends a GET request to the '/bar' path on the port of your container specified by the first value of this 'ModelContainerSpec''s ports field. If you don't specify this field, it defaults to the following value when you deploy this Model to an Endpoint:/v1/endpoints/ENDPOINT/deployedModels/DEPLOYED_MODEL:predict The placeholders in this value are replaced as follows: - ENDPOINT: The last segment (following 'endpoints/')of the Endpoint.name][] field of the Endpoint where this Model has been deployed. (Vertex AI makes this value available to your container code as the `'AIP_ENDPOINT_ID' environment variable <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_.) - DEPLOYED_MODEL: DeployedModel.id of the 'DeployedModel'. (Vertex AI makes this value available to your container code as the `'AIP_DEPLOYED_MODEL_ID' environment variable <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_.) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#health_route GoogleVertexAiEndpointWithModelGardenDeployment#health_route}
        :param liveness_probe: liveness_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#liveness_probe GoogleVertexAiEndpointWithModelGardenDeployment#liveness_probe}
        :param ports: ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#ports GoogleVertexAiEndpointWithModelGardenDeployment#ports}
        :param predict_route: HTTP path on the container to send prediction requests to. Vertex AI forwards requests sent using projects.locations.endpoints.predict to this path on the container's IP address and port. Vertex AI then returns the container's response in the API response. For example, if you set this field to '/foo', then when Vertex AI receives a prediction request, it forwards the request body in a POST request to the '/foo' path on the port of your container specified by the first value of this 'ModelContainerSpec''s ports field. If you don't specify this field, it defaults to the following value when you deploy this Model to an Endpoint:/v1/endpoints/ENDPOINT/deployedModels/DEPLOYED_MODEL:predict The placeholders in this value are replaced as follows: - ENDPOINT: The last segment (following 'endpoints/')of the Endpoint.name][] field of the Endpoint where this Model has been deployed. (Vertex AI makes this value available to your container code as the `'AIP_ENDPOINT_ID' environment variable <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_.) - DEPLOYED_MODEL: DeployedModel.id of the 'DeployedModel'. (Vertex AI makes this value available to your container code as the `'AIP_DEPLOYED_MODEL_ID' environment variable <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_.) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#predict_route GoogleVertexAiEndpointWithModelGardenDeployment#predict_route}
        :param shared_memory_size_mb: The amount of the VM memory to reserve as the shared memory for the model in megabytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#shared_memory_size_mb GoogleVertexAiEndpointWithModelGardenDeployment#shared_memory_size_mb}
        :param startup_probe: startup_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#startup_probe GoogleVertexAiEndpointWithModelGardenDeployment#startup_probe}
        '''
        value = GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec(
            image_uri=image_uri,
            args=args,
            command=command,
            deployment_timeout=deployment_timeout,
            env=env,
            grpc_ports=grpc_ports,
            health_probe=health_probe,
            health_route=health_route,
            liveness_probe=liveness_probe,
            ports=ports,
            predict_route=predict_route,
            shared_memory_size_mb=shared_memory_size_mb,
            startup_probe=startup_probe,
        )

        return typing.cast(None, jsii.invoke(self, "putContainerSpec", [value]))

    @jsii.member(jsii_name="resetAcceptEula")
    def reset_accept_eula(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceptEula", []))

    @jsii.member(jsii_name="resetContainerSpec")
    def reset_container_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerSpec", []))

    @jsii.member(jsii_name="resetHuggingFaceAccessToken")
    def reset_hugging_face_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHuggingFaceAccessToken", []))

    @jsii.member(jsii_name="resetHuggingFaceCacheEnabled")
    def reset_hugging_face_cache_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHuggingFaceCacheEnabled", []))

    @jsii.member(jsii_name="resetModelDisplayName")
    def reset_model_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelDisplayName", []))

    @builtins.property
    @jsii.member(jsii_name="containerSpec")
    def container_spec(
        self,
    ) -> GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecOutputReference:
        return typing.cast(GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecOutputReference, jsii.get(self, "containerSpec"))

    @builtins.property
    @jsii.member(jsii_name="acceptEulaInput")
    def accept_eula_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "acceptEulaInput"))

    @builtins.property
    @jsii.member(jsii_name="containerSpecInput")
    def container_spec_input(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec], jsii.get(self, "containerSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="huggingFaceAccessTokenInput")
    def hugging_face_access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "huggingFaceAccessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="huggingFaceCacheEnabledInput")
    def hugging_face_cache_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "huggingFaceCacheEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="modelDisplayNameInput")
    def model_display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelDisplayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="acceptEula")
    def accept_eula(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "acceptEula"))

    @accept_eula.setter
    def accept_eula(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__862db1bf8629830c5837e112822a256c7cc87f3331737f605fa8478231858383)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptEula", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="huggingFaceAccessToken")
    def hugging_face_access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "huggingFaceAccessToken"))

    @hugging_face_access_token.setter
    def hugging_face_access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52d9c733789c9f5e6793cc81804122046f9ffec6e926bc9bab4570f6912d3a54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "huggingFaceAccessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="huggingFaceCacheEnabled")
    def hugging_face_cache_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "huggingFaceCacheEnabled"))

    @hugging_face_cache_enabled.setter
    def hugging_face_cache_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eac4c90a747c765caf65b586dec6ce767f056f21155b59fcc867c8b1a7fb20bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "huggingFaceCacheEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelDisplayName")
    def model_display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelDisplayName"))

    @model_display_name.setter
    def model_display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52ac93ea24b03cae353ab6d66645377727633da8181a22a9fdf3e29dfa33f102)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelDisplayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5123586c7f6a4bce6e780837a08d50bd6bc206ab63744d00e17ffa59d2100365)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class GoogleVertexAiEndpointWithModelGardenDeploymentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#create GoogleVertexAiEndpointWithModelGardenDeployment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#delete GoogleVertexAiEndpointWithModelGardenDeployment#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1025d569617dd6a6844f97365c130e8964f42e09ea9f6e90378bb8e96f33f7df)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#create GoogleVertexAiEndpointWithModelGardenDeployment#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_vertex_ai_endpoint_with_model_garden_deployment#delete GoogleVertexAiEndpointWithModelGardenDeployment#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiEndpointWithModelGardenDeploymentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiEndpointWithModelGardenDeploymentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiEndpointWithModelGardenDeployment.GoogleVertexAiEndpointWithModelGardenDeploymentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d00ef17381c9aecfdfe798de585e786aa30a1272618b5ddb2b0c008b378685a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0dab0e8b8c672dc2685f9e46a1b8a2ef42c76fa3801cd8974ea653b12ed8e6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aaaddfd332c647259769d5374b640fbeca1c53fd2abcaa092e0e14975072647)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cd23493132e5e062d5181dbdceeb55d6af5b6a5d87aa62b3aef44b7cb5d0648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleVertexAiEndpointWithModelGardenDeployment",
    "GoogleVertexAiEndpointWithModelGardenDeploymentConfig",
    "GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfig",
    "GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources",
    "GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs",
    "GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecsList",
    "GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecsOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec",
    "GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity",
    "GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinityOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfig",
    "GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfigOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfig",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnvList",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnvOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPortsList",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPortsOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExecOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpcOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeadersList",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeadersOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocketOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExecOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpcOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeadersList",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeadersOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocketOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPortsList",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPortsOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExecOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpcOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeadersList",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeadersOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocketOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigOutputReference",
    "GoogleVertexAiEndpointWithModelGardenDeploymentTimeouts",
    "GoogleVertexAiEndpointWithModelGardenDeploymentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__e36345ae504a4576c9ba4b770802811e995e835d35bb3b289bf165930790f044(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    deploy_config: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoint_config: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    hugging_face_model_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    model_config: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    publisher_model_name: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ab97e97ee3997a40957dfe189f61cb02f772b494f70322abe60a7ccb32704441(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d61c5a8fdea5d5fc7c730ad9e4a3f67b3befc6b2523a7be7b4f32a019c0264(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dc89a957dac0675224616c41bd2644f53365411de59e90eb3bd19f6c3652fc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7752cb99fe5bd6dd32b7edbd32bfce3822f6492d8b9a7b0465f8c0d409b0268(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62aadee89fe3769e21e59ab8cadf5152730fbf17abc4dd9f01abed41580c2bb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9cae99eb3b293d1aea926d4e235f73b21f854ef7257d51f97c232922efc6d74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa8ad4a7727366f0f4663dca6b797fe19144b6ead9feb5aae8aded1e031de26(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    deploy_config: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoint_config: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    hugging_face_model_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    model_config: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    publisher_model_name: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45184ad8c53bde4aa50e99a4a6550bbe5f371bd46755e58cacd08610046508c0(
    *,
    dedicated_resources: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources, typing.Dict[builtins.str, typing.Any]]] = None,
    fast_tryout_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    system_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a1edbea95f0baab86e3959cce20def457c0c65137b3d3c7a9f6053d4ca7b7b(
    *,
    machine_spec: typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec, typing.Dict[builtins.str, typing.Any]],
    min_replica_count: jsii.Number,
    autoscaling_metric_specs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max_replica_count: typing.Optional[jsii.Number] = None,
    required_replica_count: typing.Optional[jsii.Number] = None,
    spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08daef2643beac7b8547479c1e8959f0356cec1425c347ec3c5d95c7c14f6a57(
    *,
    metric_name: builtins.str,
    target: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd253b05e4e0cf577e9b7549004b0814ffe48ffd455348ded2c762df1ba27ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35670e29ffda3ef005f79e2a4e4ffbd7c94b3e10d6c1f9cd118f40beade3d828(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17f499ad46fcebe3ed634342edb042205b6f5cbb93c7066793744524453804c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66e4654ab6c52f614f7100d802e926fc85e206f94bf642a5120875a29b4105e3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf0bd2c7a0224f5065efb269ff4177298e3c4d02ba441434b9d9198fbce8eca8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a376ec9b23f75cc0ed37ab7f9821545bffb8adfed23820e2b5dfdfeb2efc3b8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d42d49516f05ff409fb25464d4d4576cfad338ac881d36a35819bad72234ff7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__479b900b24435f33dedefa02c4987d6734323fc793ca6d5f3659841cfb83b5bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__957bad2182f1c3c68551db7f3995d3705e0344e0688a92594e03eb9dcd9a1333(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f2d0b5041a37cbe1b8d8cae681886a78bffa0074d90b7821584a1126d968b87(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e65ec7f9af2b52baf19b82b419afc8e92ed7b80b14d124194dc3a81f334e5de(
    *,
    accelerator_count: typing.Optional[jsii.Number] = None,
    accelerator_type: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    multihost_gpu_node_count: typing.Optional[jsii.Number] = None,
    reservation_affinity: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
    tpu_topology: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48e521d27cf176d7699d38eeb616c9ea32b490006de902cc28f04173a25828df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17ffab9b2a4605e30e50f89ab36f67383eaf0ae76d4e4c0d052c953fdf8e64f4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d17591c39a8e5ad250fb4af7c23252d6f4bc1ba6c3156ec1c353343b7f30ad65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f79c123d782f7f025f536706ca0782b1fe43e4ea028b3c3cf30e0c07da8cb47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57d423b65008003fdb293e772e92367c0aae71adbe42fc3a2868b3b50be8cde2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd4e34d91ec6dd74d5f3fb7152177b7495e58114f3b9907fe551d46e9387c0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b807d7ec9a6abefa735716bf342ed5afed62ad736e02a1d19579444af45ed0ec(
    value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4753ce0a499f4fb8236fae62be03ea78e0bd58568bd7e9c86c4e910ad3295ff4(
    *,
    reservation_affinity_type: builtins.str,
    key: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3574bcc42975f7e410cae1377f869276b8a519c2fbf93f47a4650bab30908544(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65ffd6f467aa03fff23131c8fd577561fbc8a6f5ae076faf5498340b766afad1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2a18368ea52f7b3dad6e7518c4c4a228a719437fdec58bd8c9637eda7a6447(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c2a5ea4c5c2a71b32dd23c5baa7f2346be53b94c64375b49acfc29ec7b829b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e92ac375a5f9777d8ff7ce7a37883219eb0d7ae5468f829ae763afa454f9c710(
    value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3367ac31026afcf7d46b066b9cd2096735bb3f7cb1dd37b30c998562c70a582(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd038719acc0643dac7c85bace9e20d576805a7c59f5180f1254d0df4a71be6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ea4b506e296db0a28d41d5d8896754f1aa3bea43825d43ea7344b6cda62d0e5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f1fc0dee805b4055752d1b440cc9e60afeda26d6325ab21ed0d3ae85d788ae(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb1cc2e0725f74767cc1050d031f4c6b4b1e9d19fad0fee6f559f86fcbd2ef5d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3216683f0095f8b9c5f0272c04fa260bb15f96b7ddc3067220ca53dd5f9533c5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cff0dd3fd8241a4a444c1263b7e6172baebc33d3bf7526c580b922c7002f138a(
    value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a63b83c32275e238e3334202c31d91fdbccc6a90194eaa5809fed0dc4f276698(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8956a0421257e4ec681bc7f25a19bcd4a47d08ab01312dab7e7eda7590e56519(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1658cd0626a2e1987d6656e1004c93f9a03f754bace9d2bea96ced3c70fa4458(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138510dff63d92ec51f9f91324518d456617b59cc492a2cfbbcdf0ce66c48b57(
    value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentDeployConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea007539474fe556a679c57d89c5a036d2d2ede16dbc19436168294dec4875d1(
    *,
    dedicated_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    endpoint_display_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3526892a6131b2df4c614d01676423e87225d224c6f701b09705a8e99e7356c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f2ac22173bbc6756bf402c735e0df739a36064fbfe8fca4e40bab6a777e054(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60ca4fc1ffc3ec1365ccee8a5d40d21c782e7219949504b0a5a24c9ff7aa43e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e89a82c648fc1b8ceb9884d8c84ed80d4bd8ea6e92687a0710384df616f88943(
    value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentEndpointConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bc2461b4658d615952c693a5e73e854c6ab0af93d2a2b435647630faa58bb6b(
    *,
    accept_eula: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    container_spec: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    hugging_face_access_token: typing.Optional[builtins.str] = None,
    hugging_face_cache_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    model_display_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b10856b38253843a2527a890910dcd5c59dd6482d5a2c68f3a10e629025100(
    *,
    image_uri: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    deployment_timeout: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv, typing.Dict[builtins.str, typing.Any]]]]] = None,
    grpc_ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    health_probe: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe, typing.Dict[builtins.str, typing.Any]]] = None,
    health_route: typing.Optional[builtins.str] = None,
    liveness_probe: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe, typing.Dict[builtins.str, typing.Any]]] = None,
    ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    predict_route: typing.Optional[builtins.str] = None,
    shared_memory_size_mb: typing.Optional[builtins.str] = None,
    startup_probe: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60feb6cbc5b07cf0928ff9f3d50d0640f705ec9d873e2364f857da7504af54a5(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed7f6851155fd1a74fd46e77ea5bfcbc3ce82a84a05140adf4b14654979fc18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb865f63eb8b2fe6abea8f7df4c22bec6d785b1489e07d5c16b579743f37d032(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f9d2a5ebe6a866b485ff807658076b0cefe150c00a7856892031e8c4ad766b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d4b4f3aebb436e992eeac612a6e0c259dd5aa40722e0ff7b5f54f41e33c224(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63e45f5832a1fa272b706265e14fe6161cb7c0d444ee99d1d1826805ca1622a5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f67fcd6e4ae3539191a684ed74864d33033d7974d80529c87ea75f0fb62a0f13(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40872ada3923231f08f064b2b343bd1c85427d5a2917fd3dcd18a88ae112965c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d61f319ac485fc41c841a16c8ae58e0f41e03d0db2498428d865e7e87e37786(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758cc4c7adebcb45b7edfcb6ad528b069175c8653098148402e45d1568ae2532(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb588a806a72432209f8c07f8450abdf8c13343b4e84630bd593eff4f171746c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__392082e2055c5046f1700f584677c8d32defb428ce18473fa32631c800c9880d(
    *,
    container_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa6e2a21dc8b9935630de145b49cd74a17795c5022fa2718516aa6d5fea9a340(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af83c0e43c8af1bfc8720f09444537fbb84827fc80f8b01e0bd693d582466905(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b79459da33c68f0ce8aab447c8bd776582ed4baac0aebca483a3c8f0a21cff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52c9db839f29bc4eb370704435e190e14907746d7cdfc591b0496681fce8262(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2465ef4a37bdc899bec25f3440fdebe07ab90ebce823700f399b1b69b7c2c0d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9722d793a5b608ead3641cad5f7e814655fcce66fe0de7bf458a90f66d0af7d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d3732193c6b0a3d161543e9012f499329f06b3457ad223080722712f631ac8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5824ae0344c2e24cf44313c107755cf7cf2948da397a624a024ef517422025b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4cec00c97c7fd188c3f00e38f627bbe2e8d59152cfd72065703750e52659a51(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b17bc98233523d13a7810cfc95ad7b273059b721acec8352a5075a1fbd33a1(
    *,
    exec: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec, typing.Dict[builtins.str, typing.Any]]] = None,
    failure_threshold: typing.Optional[jsii.Number] = None,
    grpc: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
    http_get: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
    initial_delay_seconds: typing.Optional[jsii.Number] = None,
    period_seconds: typing.Optional[jsii.Number] = None,
    success_threshold: typing.Optional[jsii.Number] = None,
    tcp_socket: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d2b15a0ba6bcb593960e0a1ec120bc8d7918564e9f6bfd29b7d4c9fdc962adc(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8d8460be6fd7eb99393747cf0e3643cc14a92d574f7738948f8e8166be7eb20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42589fcc422d0cb79fde0365640b1688a676d2de7f196eeba80346d6f8e61ef6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077ce4d669933ef6c5ef1978705143b40e3dbece8bf98b05512fde45088eec8e(
    value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__981661ece7ab23afef8f22c1dded8436ea803bf2ae672e637c254c452aba4216(
    *,
    port: typing.Optional[jsii.Number] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d22eb3fd6a335d8afd72c1fd3bec253faa472367092940e8284671d4634eef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1448367a66fd8f87943f2334b250ecdc63419c4554380d9f85867d712cce076(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12cfc62af8b1d79595a7f60c6b8d1ad1c66491bd9ea7cbbd1d8cae1170ee91d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc0e82ac5ec6fa6db282355d81ff91375cea34e1421f0faaeadc191d00a14951(
    value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7015f705f4750b4fd73965e72f60fe1cdb55df01ebc47e10b32285a65bb1ada(
    *,
    host: typing.Optional[builtins.str] = None,
    http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    scheme: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c858167251a7839fa7ca243613a7c3ffd1d378dc386929cb904dd892300d80(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ade7ec639ca7baa0361faa025bd8916a306daf8f135761b91ccdba249e3154(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f984feed4b43d77911736c4ef17e2d203d71e28abb28a4953b78c73d7337fb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72fef7c7f90c6e7008fe91f2eafbae0b82070b262049026c891c0b7fd093ce00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7bc4dd17a1fdfdf55bcc8fae3a0e909f17195f197bba5beb885663f9ec6fee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50f64635bc29e6daed7b17471de8d1cda931775615a15004ca1591e0ddfce2fd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa5fc8aa0063d6edc9ae9555de4284d736fd54768935f70e907529e39e392f2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4cb4d1cb2b6de3a4ffd4f9e7ae19a57361bf04ab912f8a3a8ae9c6407863daa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__899be8f3cc3164e899c54b59569a8ece1edec81275080cb568202390ed78db8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30d959de7e7a8bb793a40bb3643126228f1a729fe860abc2400505a249e3cfd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a5f2f4724fa1f9b2dec37a9301d20f61a326d8b8b568a11e7a1beb573d2819(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55b11c5b4ce8def437af6df63dca64c75d4ecc707a28b071a54e048dc5a0c354(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef34a6b2f9ccc265f951fb2909c912fdf4f7a7af4e0755e4fb6ca96c9285b5f4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__531b9474ad3ca8715f2dd9d111692bf824ead21b0a4d0a92867501dd495713f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff94ac3778a1bcc0a2ef45f8e372faa9239dc1181f23a6c2206cfbe08d9e1a12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c545a329fb34727d5049fee2c780d281a379cc327a9e9f1831115acbb1101ce(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7459e74056a4f3de35dc2e3797d04cb75d1034a11a2d8ffe5df4b29f3af46a8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fad5ff7da59f28909fab5d440dde277361afa004e345ea5f1e448a7059bd3df(
    value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d55b28c5b74f4f08ace09eca4935738f31390ac2d0ccbd5beeca1db5edd13156(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882fbecc83e920bcd3d8b69dd2c72532e2ccede97e3741326d883faa2a541e2f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e438f625e8c7ab234956154faaaf6379c1049a5df063bc95cb71a04273d567e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2dfca596cae12843949e5ee4a280e87d1524db99d9bf21fde9ab3fb4a795fa8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58ff90946c77c1efe56a098fd97864e4502f39f817d36e64ac846ec38fbd172(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e158eb46d17dd2968aa48246815a89a9f62c1097ebcb0a4a6a434aa26a38ab3b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d4e17b90ebee869b2316ff1e172845822e2725ee8cb17dd76d655f6e91a30a(
    value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf64b3268a92e75b3d91932b14c9c9ed56133ba48e0baa569818fa4217207b0(
    *,
    host: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d417c862f82ee870143934a9f7053e5f0ba8534ad1faafe5ae45e443adf71b06(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f736ef3a80cace1c9ebbffe7a182e8187e8bfa12decf96268f4fd761cd2975e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37ba352c8957c23427f86e2a9d351604370830a487dd76f13d48b37997efdcc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__477ed1a9dcfb85d5763f1cf15775e7b9de8a55aec2e24dfe5225ab129d1a9d64(
    value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138010664c6c0ec88aefb8cc7ab81600b69ca28d188079953e2d687c4947e04d(
    *,
    exec: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec, typing.Dict[builtins.str, typing.Any]]] = None,
    failure_threshold: typing.Optional[jsii.Number] = None,
    grpc: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
    http_get: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
    initial_delay_seconds: typing.Optional[jsii.Number] = None,
    period_seconds: typing.Optional[jsii.Number] = None,
    success_threshold: typing.Optional[jsii.Number] = None,
    tcp_socket: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb472b0d84f16220c1070ee806c22747b79ac0a87f53ef6c5f851e9db9689150(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a06d260893bbf5cccf22e9a5991d84b5607074655b20274ab6847d668531afe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b5c26c99dd04c5d970b61442b510a39ee67d4be0482e550b6b1d43e87f27232(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e0c5195de666b1849ea5b9e5ecf36ca1a3d5b1c7b3a5974b82234454d8700bc(
    value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4afa6901b8d699926c3af59d63477c4ed933b119e961a536b562be0d4169881(
    *,
    port: typing.Optional[jsii.Number] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52286c3b4d8a7f43181803081a3fef0b4b1ce5c3d4eb6af5cd416c0fa3976e8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__127679a83515bfac2e9ea7fe149671933e4a682ab11f57a7b1222603a5eae4a1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdbe0447ec386053b9cf8615e1b5614609b415288f3f3c08a0f4570f2f0e62d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba90f60851b9837b8090ec59b9231f6194982723750305d2c8f186591e680358(
    value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71cf8f1a06192cd2ce648e035e7053ca9dffbfa36777e2012b4dbc6825cd52e1(
    *,
    host: typing.Optional[builtins.str] = None,
    http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    scheme: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ce76d30eec4e1e2a0c5218d5a9e8357893e4ac911aea1534d53e20a819f6f4(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a99749d7f1eba810256a613c6d3ff0da46a8651339a3bea29803fdf5f1b280(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3216579f36baa61eec01ba3aabf64c4ed90cf5e2d3a5c96934cdf2516547eff0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__026bc5a5523aa070e4cc8e2d9c25eadf77258980ecc29fcd6d0ad78e7619425f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def9175b48ad188d7c4cd081a525d5341b6b9c01d2d4ebeec66a905b28fad074(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb7b10e82b11852bda5e4cdc909c91a2db5a78b1b34ab4f8ffe8adb3023de61(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ca3f0d448349f37a5871620d626400996e9ce1752448a78ca6c8b5e1d3c733(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae487bd0ba0784b534732fac8527d75734b10be7ccccc5e7f1a93dd79a747102(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52569f3b4f3f184bdcfbecab047505da066987ab6bf4f7233922ece90776e24b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34b3a6c090c2fef954362582ec4dbd6d57a32e8798d29459f0d9b21f1f02476(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e8509ca6e51021dce08b03db1205f9f9e2df89b5cb55de5269f9242db391647(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d95ce3395ee8a6f11772a78c2b4b6cecbe07d505c86da0fd726c8e90c77d8b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a27bf3e3f4ff5ff4d25bb703d86dede449e48e7b0025b5453f42796adf32ce4a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441a04d9e34929b235ef6abac2ff6a1f5f09bbc0a227ab963e203c68e415bc60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5b154354f29c98e9c6cf405fcdf8bd39a0c27ef7a025ddfea08131f29cc169f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__776274a13cae7ce2f87c557effbb84639a0018ffa759e1fac221176a4faa2a44(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e526590a8a179d0c60f21145d98fe575a6c9e6e5ca0a51f38aafbc82209f6a44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58465ed5d76042b8f99d558ed294f7371da796974aeedb631b16134e7719843(
    value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b4399fbe62eee93d809b1c6c2a3a04f225cb1db49737566e85bf4ab55bde6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f969cc151cde8058fc8d5c253946a6bc3e0bf7b4e780ee42f46ee856d6260e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1757c58ca9660857d69c01f8ceffee6e16f9aaf421e69ac0bc3042c4a6dc4800(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72cd07704db5ddf847cb796bb63e1bec5988595d235407a90e94e8c587487659(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__485e69b47335c3079789f4d8773c3c5640ef489ea9efdcdb1064a9529e9b0205(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b51f74c99e3765b34c77b1918dad5abf20f0235b6afa81321e56823ba41f52(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fec5b6140f3268c88f1a74bd05ecedafc2edd8ddfad7f13c77ab3aae936ae88(
    value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8499000ff64f1231d2191275b013358e1a9e14a1a84a1baf8c17482b80bb532(
    *,
    host: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f360184aab76b2b17367ee14636809b3a915738a8095dc3ad03d19ae268f450e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a1980ad966e7460fbcabc5b4650b5da07710382c16c677d8878f75fee9ca5ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a0861e3fa49eafa4ad52a7a512f5f5f4e651b083342a395e1cf8c6a2e4410f7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e09f9545eaf8216fc2f947417650ab07c7a646f3cd0ea6029d5a9123fe965de(
    value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297889be42cd0ccc13efa742a650870fa7d8e778d92b7926dec35874b1bebc1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__970a693c3b2f4309241082618367be714074a2d946597b6be6690f56a5992954(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd35c98590ed8c142be1bbe0e4e88a2ec770516a8567f5719936917fe7c23cc8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb3c6af1f91093fae10cac2652333e393f11b1b0126e51382e33da5a6427469(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbc659cd5d7e3d4db48695c9214e7b6704b7ba136e50eef38c1e8411867e8227(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976bdcec2a190bb624576e9a63a5f0baf57817e21a51b10131fb9594c39076d9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d0bfacdefe00b7a9f34a1f46f08a5211d7613a50cb10c9ca1f611f270a51dd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8deec4c43f0dbc388bd7eafec7973e18a3c472fa816863bf570b04b2a45c0575(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7f8c96b318d7ea0f53841e340b0383c5c3e090b774056c3adfd825a90a4f451(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc7d8f24377720e53840257aebbc5e1ce5d5f40cca36237a68af5d3d19e483ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c1629ea1571f42e718fc92f0346ebc02986718a8931e83631a8825e995c1dca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27d9a9d9a46ce029a1d0593e44cdac5d2a27ad1ce684c17473ef6fe9c56630b2(
    value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__774cd66a68f6821d8c8ec5cd6fec04a4b68205381f272972b2d79f3584dd3fdb(
    *,
    container_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b34677d8c14d79caaa0044f9eeba8940f903013b67f9575a36f15fde4a3f15f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb2c69114e033ed80aefb51619330cb4a487c1fb4c448cf1f8c924976685b67f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd0edafceef661378e82d08f1cbd8377f3780bc595fbf508e6fd6bbdd42dbe6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e09d4beea876036709e02cbd52bd2dfdffa5c3f5acd79a13741ef677ce62d9d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9c7d2dcd1f95d999186a3a0f30432123f3901e16c2301ba944e4f916e8116ef(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e208f12c72b4a31bbb4ef5857052c8468c6ab34e57d58109335611f82840a9a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f486d7947f3e0d2edd77cccaf21de8594dfa7f137971f7a3b598ed86ef27b144(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c76c976a91bfbe2349e6786d9cca237e845d9e97d4b63e8b7d3edd9a48db4d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5cf79a69fa60a154c73eb242ebece7acea05e92ce3277ccb3d3977ce22a7caa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4f1f7311ed370b64f86474bd3eb7438c9f74dee3259c98f9deded6ed9f4a94(
    *,
    exec: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec, typing.Dict[builtins.str, typing.Any]]] = None,
    failure_threshold: typing.Optional[jsii.Number] = None,
    grpc: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
    http_get: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
    initial_delay_seconds: typing.Optional[jsii.Number] = None,
    period_seconds: typing.Optional[jsii.Number] = None,
    success_threshold: typing.Optional[jsii.Number] = None,
    tcp_socket: typing.Optional[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5113d0fc1526fbc88af3fad124beaf8a17f3241a38699c75d3a52abcdb2b6d5e(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__143d7c18d581e5f1f0c494716d613e59b30eca0ff97a45bf7381ba5b86c98cb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b8141c0dbef6743842e67ad8562ab43a9eecf6e0a0f9f47d46c79fb8360283(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef4cc85b22f0fc3719507ccf71d0f5c70a7be76b4b7ccfcab849aa68f9b7c02f(
    value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14f40ccae1230ebebc5684881ba48ad748868919851833406ef32eef1f231bf1(
    *,
    port: typing.Optional[jsii.Number] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__152e83c19d045ff15798cfa2f4c8de49c2a5b71b7784d0b7c7d1da13645a4be3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a6bba92047f7bd2d927fd0c1ec956ef6593a120da7804bf3ce2a9329d78ed6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66ebccea8074be76466a3d5feafb7a1f1495249aa9c69bd141268e8e597b86a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e162d8d2e3ce578eb62f60879533b038f2ebec01be4108da95b9f127ac7444(
    value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fa989a22bd2eea4c416626f71401fee2f743dd31ddaecfd57da17c2bc4d0f6(
    *,
    host: typing.Optional[builtins.str] = None,
    http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    scheme: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2afb7b770b33b73fb8578d0b8bae3dd70bfc74e23bcedc4231f404cabb6f9502(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a42bb6732bd9c6cd0d79b82b63c31e3f7cc71a446ad28c4e01e8ef655b48280(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27d8c532af684925f0ba5a8279a243e5a4ad43354c4b495c101b7c58730ae009(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151126f4767b8b683d3a00644f8afa76df712c62113e42fa01024b4b069cc678(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c5c1d79c3c0764205253f42031169c875e31026aaba6641bab5f0320568ff41(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d62aad65ec3f4599a0537fb735df15a0748762747f82a2a28f232bf59d4e07(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c69102acb90b7686fd8a56bdc4f18502c7462bf0f31b7a0e7f10291f443d73(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bbdd7f34ddaf1c423b0c289c23959b53490d1fc92b1948fafa34873f8541c13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f388aa84def199c5296c68b1ed95f78e3dd108ce7cf356b34398c2c8266cdfd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d599bf091cd20b6673c0bcb36e36fa2c84ff9d90d63ccad2db9ab77b7dc14a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a880d689affa4d6ebb7a9446febd467bc807ba9081ada2d4b846822a8b6d2aa6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b407cd1e9e242e73be5575838d860e41e228b54f69dbf25b3cf5850c99846a16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a66c0e6d31c9f588e3eccffe7bea2c5075e451c2753dd7106616b775b0884a6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d7b139d8928d8e4293fda1623296fdc65e385ddb323a6b275b6bffff86fd878(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d52fed98bd2ccad13a4e3920ebdd2bdfb8d050ad302773692c6bf7c7956890b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__770af3f7b223384caf377bcdf1f8bac28c5b496c87492b7673230235e6865891(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b1143b0a1e77292924a151359fe314106d9b89b8567297cfb47d525a71c2eac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06cf3219b30544a745bdc2338fa09e92275889ee4410466b1918bea5ab80f096(
    value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96315acd040c16a9a4173e45375ea60d9ca4fdf6afed2ad3da78a9b214062e7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43af110759a1f7f0e71d6448fbb669dfe02440946bdbdc8ccf7b44799f6e9046(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b77c2247385ed17a815e1ec85e220f2d99ecc6e3a251f7b66d296efc1b4e1e0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a92b6fa77972c5e5aa8e591a4d65139f1872183c3c776ae9c2c76794d8a180a8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b710a2cf70be7c942d1018a5247ed179dfbf70957affbff3c07f6449485e95fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77e4be356a463940163954b432ea9b3847c574c8d9af7329c89937ccebaad056(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7e6518fdcb9216b7b1edaf27f965dfb4fa96d454305ce39a8971e4e9f10ae4(
    value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dfe3d5ee4e2f661b9829d5fb856b55fc69b072d7eb31ebf3521540ca379882a(
    *,
    host: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47e5abea638d4c981089d6166242646427ce1851be354df278202b41cd7021c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb4774a5939c09ab7e2bf33386ec9cdbcf7ba828c30792df53964af1df540631(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd5a22aa8565075d9740200ec060f2c3607e0ce8bac04570617a0ae17be381b1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c143203de9764721e1555ad86db1d960607e4825addf7688cd2b06fcb2f4dc43(
    value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6c36a77160d98dc5302576803d7a7ab6545b553ff189029bcf586314ed1ad9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__862db1bf8629830c5837e112822a256c7cc87f3331737f605fa8478231858383(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52d9c733789c9f5e6793cc81804122046f9ffec6e926bc9bab4570f6912d3a54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac4c90a747c765caf65b586dec6ce767f056f21155b59fcc867c8b1a7fb20bd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ac93ea24b03cae353ab6d66645377727633da8181a22a9fdf3e29dfa33f102(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5123586c7f6a4bce6e780837a08d50bd6bc206ab63744d00e17ffa59d2100365(
    value: typing.Optional[GoogleVertexAiEndpointWithModelGardenDeploymentModelConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1025d569617dd6a6844f97365c130e8964f42e09ea9f6e90378bb8e96f33f7df(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d00ef17381c9aecfdfe798de585e786aa30a1272618b5ddb2b0c008b378685a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0dab0e8b8c672dc2685f9e46a1b8a2ef42c76fa3801cd8974ea653b12ed8e6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aaaddfd332c647259769d5374b640fbeca1c53fd2abcaa092e0e14975072647(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cd23493132e5e062d5181dbdceeb55d6af5b6a5d87aa62b3aef44b7cb5d0648(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiEndpointWithModelGardenDeploymentTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
