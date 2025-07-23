r'''
# `google_vertex_ai_endpoint_with_model_garden_deployment`

Refer to the Terraform Registry for docs: [`google_vertex_ai_endpoint_with_model_garden_deployment`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment).
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


class VertexAiEndpointWithModelGardenDeployment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeployment",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment google_vertex_ai_endpoint_with_model_garden_deployment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        deploy_config: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentDeployConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_config: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentEndpointConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        hugging_face_model_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        model_config: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        publisher_model_name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment google_vertex_ai_endpoint_with_model_garden_deployment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Resource ID segment making up resource 'location'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#location VertexAiEndpointWithModelGardenDeployment#location}
        :param deploy_config: deploy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#deploy_config VertexAiEndpointWithModelGardenDeployment#deploy_config}
        :param endpoint_config: endpoint_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#endpoint_config VertexAiEndpointWithModelGardenDeployment#endpoint_config}
        :param hugging_face_model_id: The Hugging Face model to deploy. Format: Hugging Face model ID like 'google/gemma-2-2b-it'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#hugging_face_model_id VertexAiEndpointWithModelGardenDeployment#hugging_face_model_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#id VertexAiEndpointWithModelGardenDeployment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param model_config: model_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#model_config VertexAiEndpointWithModelGardenDeployment#model_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#project VertexAiEndpointWithModelGardenDeployment#project}.
        :param publisher_model_name: The Model Garden model to deploy. Format: 'publishers/{publisher}/models/{publisher_model}@{version_id}', or 'publishers/hf-{hugging-face-author}/models/{hugging-face-model-name}@001'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#publisher_model_name VertexAiEndpointWithModelGardenDeployment#publisher_model_name}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#timeouts VertexAiEndpointWithModelGardenDeployment#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c48ae63f271b6332a6896a67086dce4a13f91c775933b89a6516f21e916bedda)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VertexAiEndpointWithModelGardenDeploymentConfig(
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
        '''Generates CDKTF code for importing a VertexAiEndpointWithModelGardenDeployment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VertexAiEndpointWithModelGardenDeployment to import.
        :param import_from_id: The id of the existing VertexAiEndpointWithModelGardenDeployment that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VertexAiEndpointWithModelGardenDeployment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3be9181eeaf51cdee0b9dab6cfb3486a290688223b0a2b9a43cf3e0ea13f1c5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDeployConfig")
    def put_deploy_config(
        self,
        *,
        dedicated_resources: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources", typing.Dict[builtins.str, typing.Any]]] = None,
        fast_tryout_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        system_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param dedicated_resources: dedicated_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#dedicated_resources VertexAiEndpointWithModelGardenDeployment#dedicated_resources}
        :param fast_tryout_enabled: If true, enable the QMT fast tryout feature for this model if possible. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#fast_tryout_enabled VertexAiEndpointWithModelGardenDeployment#fast_tryout_enabled}
        :param system_labels: System labels for Model Garden deployments. These labels are managed by Google and for tracking purposes only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#system_labels VertexAiEndpointWithModelGardenDeployment#system_labels}
        '''
        value = VertexAiEndpointWithModelGardenDeploymentDeployConfig(
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
        :param dedicated_endpoint_enabled: If true, the endpoint will be exposed through a dedicated DNS [Endpoint.dedicated_endpoint_dns]. Your request to the dedicated DNS will be isolated from other users' traffic and will have better performance and reliability. Note: Once you enabled dedicated endpoint, you won't be able to send request to the shared DNS {region}-aiplatform.googleapis.com. The limitations will be removed soon. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#dedicated_endpoint_enabled VertexAiEndpointWithModelGardenDeployment#dedicated_endpoint_enabled}
        :param endpoint_display_name: The user-specified display name of the endpoint. If not set, a default name will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#endpoint_display_name VertexAiEndpointWithModelGardenDeployment#endpoint_display_name}
        '''
        value = VertexAiEndpointWithModelGardenDeploymentEndpointConfig(
            dedicated_endpoint_enabled=dedicated_endpoint_enabled,
            endpoint_display_name=endpoint_display_name,
        )

        return typing.cast(None, jsii.invoke(self, "putEndpointConfig", [value]))

    @jsii.member(jsii_name="putModelConfig")
    def put_model_config(
        self,
        *,
        accept_eula: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        container_spec: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        hugging_face_access_token: typing.Optional[builtins.str] = None,
        hugging_face_cache_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        model_display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accept_eula: Whether the user accepts the End User License Agreement (EULA) for the model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#accept_eula VertexAiEndpointWithModelGardenDeployment#accept_eula}
        :param container_spec: container_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#container_spec VertexAiEndpointWithModelGardenDeployment#container_spec}
        :param hugging_face_access_token: The Hugging Face read access token used to access the model artifacts of gated models. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#hugging_face_access_token VertexAiEndpointWithModelGardenDeployment#hugging_face_access_token}
        :param hugging_face_cache_enabled: If true, the model will deploy with a cached version instead of directly downloading the model artifacts from Hugging Face. This is suitable for VPC-SC users with limited internet access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#hugging_face_cache_enabled VertexAiEndpointWithModelGardenDeployment#hugging_face_cache_enabled}
        :param model_display_name: The user-specified display name of the uploaded model. If not set, a default name will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#model_display_name VertexAiEndpointWithModelGardenDeployment#model_display_name}
        '''
        value = VertexAiEndpointWithModelGardenDeploymentModelConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#create VertexAiEndpointWithModelGardenDeployment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#delete VertexAiEndpointWithModelGardenDeployment#delete}.
        '''
        value = VertexAiEndpointWithModelGardenDeploymentTimeouts(
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
    ) -> "VertexAiEndpointWithModelGardenDeploymentDeployConfigOutputReference":
        return typing.cast("VertexAiEndpointWithModelGardenDeploymentDeployConfigOutputReference", jsii.get(self, "deployConfig"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="endpointConfig")
    def endpoint_config(
        self,
    ) -> "VertexAiEndpointWithModelGardenDeploymentEndpointConfigOutputReference":
        return typing.cast("VertexAiEndpointWithModelGardenDeploymentEndpointConfigOutputReference", jsii.get(self, "endpointConfig"))

    @builtins.property
    @jsii.member(jsii_name="modelConfig")
    def model_config(
        self,
    ) -> "VertexAiEndpointWithModelGardenDeploymentModelConfigOutputReference":
        return typing.cast("VertexAiEndpointWithModelGardenDeploymentModelConfigOutputReference", jsii.get(self, "modelConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "VertexAiEndpointWithModelGardenDeploymentTimeoutsOutputReference":
        return typing.cast("VertexAiEndpointWithModelGardenDeploymentTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="deployConfigInput")
    def deploy_config_input(
        self,
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentDeployConfig"]:
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentDeployConfig"], jsii.get(self, "deployConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointConfigInput")
    def endpoint_config_input(
        self,
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentEndpointConfig"]:
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentEndpointConfig"], jsii.get(self, "endpointConfigInput"))

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
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfig"]:
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfig"], jsii.get(self, "modelConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VertexAiEndpointWithModelGardenDeploymentTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VertexAiEndpointWithModelGardenDeploymentTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="huggingFaceModelId")
    def hugging_face_model_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "huggingFaceModelId"))

    @hugging_face_model_id.setter
    def hugging_face_model_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb7416b80b46e12b794497361b8967966e4a34d448a486406ac88df2128c5773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "huggingFaceModelId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c1cf2b533cb8a3c18ce7057b739665079a9485dbf4973dae012b9966b12f112)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52abc607155069c26b2a9342dfbe4ae4c29ab9fa1a3af3dd0dec427b520ebf9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85f48f599e12cae43489669f9dded6300d1713ab6701f9f9002130f7e81b4f16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publisherModelName")
    def publisher_model_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisherModelName"))

    @publisher_model_name.setter
    def publisher_model_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b5d4c5d46b156509493c2cc8c75d8861fe14b644ed08435fd9fe616e450e448)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publisherModelName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentConfig",
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
class VertexAiEndpointWithModelGardenDeploymentConfig(
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
        deploy_config: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentDeployConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_config: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentEndpointConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        hugging_face_model_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        model_config: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        publisher_model_name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Resource ID segment making up resource 'location'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#location VertexAiEndpointWithModelGardenDeployment#location}
        :param deploy_config: deploy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#deploy_config VertexAiEndpointWithModelGardenDeployment#deploy_config}
        :param endpoint_config: endpoint_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#endpoint_config VertexAiEndpointWithModelGardenDeployment#endpoint_config}
        :param hugging_face_model_id: The Hugging Face model to deploy. Format: Hugging Face model ID like 'google/gemma-2-2b-it'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#hugging_face_model_id VertexAiEndpointWithModelGardenDeployment#hugging_face_model_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#id VertexAiEndpointWithModelGardenDeployment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param model_config: model_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#model_config VertexAiEndpointWithModelGardenDeployment#model_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#project VertexAiEndpointWithModelGardenDeployment#project}.
        :param publisher_model_name: The Model Garden model to deploy. Format: 'publishers/{publisher}/models/{publisher_model}@{version_id}', or 'publishers/hf-{hugging-face-author}/models/{hugging-face-model-name}@001'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#publisher_model_name VertexAiEndpointWithModelGardenDeployment#publisher_model_name}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#timeouts VertexAiEndpointWithModelGardenDeployment#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(deploy_config, dict):
            deploy_config = VertexAiEndpointWithModelGardenDeploymentDeployConfig(**deploy_config)
        if isinstance(endpoint_config, dict):
            endpoint_config = VertexAiEndpointWithModelGardenDeploymentEndpointConfig(**endpoint_config)
        if isinstance(model_config, dict):
            model_config = VertexAiEndpointWithModelGardenDeploymentModelConfig(**model_config)
        if isinstance(timeouts, dict):
            timeouts = VertexAiEndpointWithModelGardenDeploymentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36960e4dcb3c5d974fc4c7eeb506376c1b85011bee5698a4dfbd7bbf2214ce4c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#location VertexAiEndpointWithModelGardenDeployment#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deploy_config(
        self,
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentDeployConfig"]:
        '''deploy_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#deploy_config VertexAiEndpointWithModelGardenDeployment#deploy_config}
        '''
        result = self._values.get("deploy_config")
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentDeployConfig"], result)

    @builtins.property
    def endpoint_config(
        self,
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentEndpointConfig"]:
        '''endpoint_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#endpoint_config VertexAiEndpointWithModelGardenDeployment#endpoint_config}
        '''
        result = self._values.get("endpoint_config")
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentEndpointConfig"], result)

    @builtins.property
    def hugging_face_model_id(self) -> typing.Optional[builtins.str]:
        '''The Hugging Face model to deploy. Format: Hugging Face model ID like 'google/gemma-2-2b-it'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#hugging_face_model_id VertexAiEndpointWithModelGardenDeployment#hugging_face_model_id}
        '''
        result = self._values.get("hugging_face_model_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#id VertexAiEndpointWithModelGardenDeployment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model_config(
        self,
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfig"]:
        '''model_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#model_config VertexAiEndpointWithModelGardenDeployment#model_config}
        '''
        result = self._values.get("model_config")
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#project VertexAiEndpointWithModelGardenDeployment#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publisher_model_name(self) -> typing.Optional[builtins.str]:
        '''The Model Garden model to deploy. Format: 'publishers/{publisher}/models/{publisher_model}@{version_id}', or 'publishers/hf-{hugging-face-author}/models/{hugging-face-model-name}@001'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#publisher_model_name VertexAiEndpointWithModelGardenDeployment#publisher_model_name}
        '''
        result = self._values.get("publisher_model_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#timeouts VertexAiEndpointWithModelGardenDeployment#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentDeployConfig",
    jsii_struct_bases=[],
    name_mapping={
        "dedicated_resources": "dedicatedResources",
        "fast_tryout_enabled": "fastTryoutEnabled",
        "system_labels": "systemLabels",
    },
)
class VertexAiEndpointWithModelGardenDeploymentDeployConfig:
    def __init__(
        self,
        *,
        dedicated_resources: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources", typing.Dict[builtins.str, typing.Any]]] = None,
        fast_tryout_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        system_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param dedicated_resources: dedicated_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#dedicated_resources VertexAiEndpointWithModelGardenDeployment#dedicated_resources}
        :param fast_tryout_enabled: If true, enable the QMT fast tryout feature for this model if possible. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#fast_tryout_enabled VertexAiEndpointWithModelGardenDeployment#fast_tryout_enabled}
        :param system_labels: System labels for Model Garden deployments. These labels are managed by Google and for tracking purposes only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#system_labels VertexAiEndpointWithModelGardenDeployment#system_labels}
        '''
        if isinstance(dedicated_resources, dict):
            dedicated_resources = VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources(**dedicated_resources)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7113ecf351197087fb0c2b08300d9d1a9cce330beafce577d5a99f214511a0fa)
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
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources"]:
        '''dedicated_resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#dedicated_resources VertexAiEndpointWithModelGardenDeployment#dedicated_resources}
        '''
        result = self._values.get("dedicated_resources")
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources"], result)

    @builtins.property
    def fast_tryout_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, enable the QMT fast tryout feature for this model if possible.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#fast_tryout_enabled VertexAiEndpointWithModelGardenDeployment#fast_tryout_enabled}
        '''
        result = self._values.get("fast_tryout_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def system_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''System labels for Model Garden deployments. These labels are managed by Google and for tracking purposes only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#system_labels VertexAiEndpointWithModelGardenDeployment#system_labels}
        '''
        result = self._values.get("system_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentDeployConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources",
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
class VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources:
    def __init__(
        self,
        *,
        machine_spec: typing.Union["VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec", typing.Dict[builtins.str, typing.Any]],
        min_replica_count: jsii.Number,
        autoscaling_metric_specs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_replica_count: typing.Optional[jsii.Number] = None,
        required_replica_count: typing.Optional[jsii.Number] = None,
        spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param machine_spec: machine_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#machine_spec VertexAiEndpointWithModelGardenDeployment#machine_spec}
        :param min_replica_count: The minimum number of machine replicas that will be always deployed on. This value must be greater than or equal to 1. If traffic increases, it may dynamically be deployed onto more replicas, and as traffic decreases, some of these extra replicas may be freed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#min_replica_count VertexAiEndpointWithModelGardenDeployment#min_replica_count}
        :param autoscaling_metric_specs: autoscaling_metric_specs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#autoscaling_metric_specs VertexAiEndpointWithModelGardenDeployment#autoscaling_metric_specs}
        :param max_replica_count: The maximum number of replicas that may be deployed on when the traffic against it increases. If the requested value is too large, the deployment will error, but if deployment succeeds then the ability to scale to that many replicas is guaranteed (barring service outages). If traffic increases beyond what its replicas at maximum may handle, a portion of the traffic will be dropped. If this value is not provided, will use min_replica_count as the default value. The value of this field impacts the charge against Vertex CPU and GPU quotas. Specifically, you will be charged for (max_replica_count * number of cores in the selected machine type) and (max_replica_count * number of GPUs per replica in the selected machine type). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#max_replica_count VertexAiEndpointWithModelGardenDeployment#max_replica_count}
        :param required_replica_count: Number of required available replicas for the deployment to succeed. This field is only needed when partial deployment/mutation is desired. If set, the deploy/mutate operation will succeed once available_replica_count reaches required_replica_count, and the rest of the replicas will be retried. If not set, the default required_replica_count will be min_replica_count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#required_replica_count VertexAiEndpointWithModelGardenDeployment#required_replica_count}
        :param spot: If true, schedule the deployment workload on `spot VMs <https://cloud.google.com/kubernetes-engine/docs/concepts/spot-vms>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#spot VertexAiEndpointWithModelGardenDeployment#spot}
        '''
        if isinstance(machine_spec, dict):
            machine_spec = VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec(**machine_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e85343fe99c4717ad67cbbf474893174f9bc4c88a7a16da3ae0b0f37816090)
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
    ) -> "VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec":
        '''machine_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#machine_spec VertexAiEndpointWithModelGardenDeployment#machine_spec}
        '''
        result = self._values.get("machine_spec")
        assert result is not None, "Required property 'machine_spec' is missing"
        return typing.cast("VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec", result)

    @builtins.property
    def min_replica_count(self) -> jsii.Number:
        '''The minimum number of machine replicas that will be always deployed on.

        This value must be greater than or equal to 1.

        If traffic increases, it may dynamically be deployed onto more replicas,
        and as traffic decreases, some of these extra replicas may be freed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#min_replica_count VertexAiEndpointWithModelGardenDeployment#min_replica_count}
        '''
        result = self._values.get("min_replica_count")
        assert result is not None, "Required property 'min_replica_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def autoscaling_metric_specs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs"]]]:
        '''autoscaling_metric_specs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#autoscaling_metric_specs VertexAiEndpointWithModelGardenDeployment#autoscaling_metric_specs}
        '''
        result = self._values.get("autoscaling_metric_specs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs"]]], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#max_replica_count VertexAiEndpointWithModelGardenDeployment#max_replica_count}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#required_replica_count VertexAiEndpointWithModelGardenDeployment#required_replica_count}
        '''
        result = self._values.get("required_replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def spot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, schedule the deployment workload on `spot VMs <https://cloud.google.com/kubernetes-engine/docs/concepts/spot-vms>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#spot VertexAiEndpointWithModelGardenDeployment#spot}
        '''
        result = self._values.get("spot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs",
    jsii_struct_bases=[],
    name_mapping={"metric_name": "metricName", "target": "target"},
)
class VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs:
    def __init__(
        self,
        *,
        metric_name: builtins.str,
        target: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metric_name: The resource metric name. Supported metrics:. - For Online Prediction: - 'aiplatform.googleapis.com/prediction/online/accelerator/duty_cycle' - 'aiplatform.googleapis.com/prediction/online/cpu/utilization' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#metric_name VertexAiEndpointWithModelGardenDeployment#metric_name}
        :param target: The target resource utilization in percentage (1% - 100%) for the given metric; once the real usage deviates from the target by a certain percentage, the machine replicas change. The default value is 60 (representing 60%) if not provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#target VertexAiEndpointWithModelGardenDeployment#target}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20b8184ff8044b80f84cf0bfaa1032599512882a095867c7a6093d7a84fd6684)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#metric_name VertexAiEndpointWithModelGardenDeployment#metric_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#target VertexAiEndpointWithModelGardenDeployment#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__758f468b9368bd06a9983e7db386408f501dcd356b2b9b8e3444db7c1148103a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee14b09294fecdc9233927e3173e3872e00ef207ddfa7a528a9a84c91fef7806)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a54ee4fe1094acc4680df296376180800fd38e148b857756b722b2ce9820fd1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8578aeb7ddf3aad6720b80c84f53df8b3121e8598eb66e9bcea9cc5ceeff5c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bebd4ce710d3facf803ff0d08abbc273c54417e715243751a44dbf8dafe419b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61f50d05e951e1c8d116b2fc8dcde3db707daaebac50be90c4537635e9a419c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9778f0800b6db1650b6350b43be15d2cf9df580b59169466ef6e1fb7ccb91f51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e9ef6a63f9b9e29a436901547ba4bbfac5306286e9b0c63ff3d897d6ae04e6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "target"))

    @target.setter
    def target(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__022a1f5e4ac51ef4bcca777b954066c1109ac5eb3f0507700b801c57f8b047f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c316e51e67488c7fb657bb9be1d5a8dc751473ac264b7ebb07c1163849a7a529)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec",
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
class VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec:
    def __init__(
        self,
        *,
        accelerator_count: typing.Optional[jsii.Number] = None,
        accelerator_type: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        multihost_gpu_node_count: typing.Optional[jsii.Number] = None,
        reservation_affinity: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
        tpu_topology: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerator_count: The number of accelerators to attach to the machine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#accelerator_count VertexAiEndpointWithModelGardenDeployment#accelerator_count}
        :param accelerator_type: Possible values: ACCELERATOR_TYPE_UNSPECIFIED NVIDIA_TESLA_K80 NVIDIA_TESLA_P100 NVIDIA_TESLA_V100 NVIDIA_TESLA_P4 NVIDIA_TESLA_T4 NVIDIA_TESLA_A100 NVIDIA_A100_80GB NVIDIA_L4 NVIDIA_H100_80GB NVIDIA_H100_MEGA_80GB NVIDIA_H200_141GB NVIDIA_B200 TPU_V2 TPU_V3 TPU_V4_POD TPU_V5_LITEPOD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#accelerator_type VertexAiEndpointWithModelGardenDeployment#accelerator_type}
        :param machine_type: The type of the machine. See the `list of machine types supported for prediction <https://cloud.google.com/vertex-ai/docs/predictions/configure-compute#machine-types>`_ See the `list of machine types supported for custom training <https://cloud.google.com/vertex-ai/docs/training/configure-compute#machine-types>`_. For DeployedModel this field is optional, and the default value is 'n1-standard-2'. For BatchPredictionJob or as part of WorkerPoolSpec this field is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#machine_type VertexAiEndpointWithModelGardenDeployment#machine_type}
        :param multihost_gpu_node_count: The number of nodes per replica for multihost GPU deployments. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#multihost_gpu_node_count VertexAiEndpointWithModelGardenDeployment#multihost_gpu_node_count}
        :param reservation_affinity: reservation_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#reservation_affinity VertexAiEndpointWithModelGardenDeployment#reservation_affinity}
        :param tpu_topology: The topology of the TPUs. Corresponds to the TPU topologies available from GKE. (Example: tpu_topology: "2x2x1"). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#tpu_topology VertexAiEndpointWithModelGardenDeployment#tpu_topology}
        '''
        if isinstance(reservation_affinity, dict):
            reservation_affinity = VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity(**reservation_affinity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f1c42768ccfea6927f131cffb250a1a640a390cf4f083630c2ef8abd728fbde)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#accelerator_count VertexAiEndpointWithModelGardenDeployment#accelerator_count}
        '''
        result = self._values.get("accelerator_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def accelerator_type(self) -> typing.Optional[builtins.str]:
        '''Possible values: ACCELERATOR_TYPE_UNSPECIFIED NVIDIA_TESLA_K80 NVIDIA_TESLA_P100 NVIDIA_TESLA_V100 NVIDIA_TESLA_P4 NVIDIA_TESLA_T4 NVIDIA_TESLA_A100 NVIDIA_A100_80GB NVIDIA_L4 NVIDIA_H100_80GB NVIDIA_H100_MEGA_80GB NVIDIA_H200_141GB NVIDIA_B200 TPU_V2 TPU_V3 TPU_V4_POD TPU_V5_LITEPOD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#accelerator_type VertexAiEndpointWithModelGardenDeployment#accelerator_type}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#machine_type VertexAiEndpointWithModelGardenDeployment#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multihost_gpu_node_count(self) -> typing.Optional[jsii.Number]:
        '''The number of nodes per replica for multihost GPU deployments.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#multihost_gpu_node_count VertexAiEndpointWithModelGardenDeployment#multihost_gpu_node_count}
        '''
        result = self._values.get("multihost_gpu_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def reservation_affinity(
        self,
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity"]:
        '''reservation_affinity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#reservation_affinity VertexAiEndpointWithModelGardenDeployment#reservation_affinity}
        '''
        result = self._values.get("reservation_affinity")
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity"], result)

    @builtins.property
    def tpu_topology(self) -> typing.Optional[builtins.str]:
        '''The topology of the TPUs. Corresponds to the TPU topologies available from GKE. (Example: tpu_topology: "2x2x1").

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#tpu_topology VertexAiEndpointWithModelGardenDeployment#tpu_topology}
        '''
        result = self._values.get("tpu_topology")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4b42a40888bb1608ed634c4a0bb1c27ad5a7f75bcfb14bd357ff0b6cd39e961)
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
        :param reservation_affinity_type: Specifies the reservation affinity type. Possible values: TYPE_UNSPECIFIED NO_RESERVATION ANY_RESERVATION SPECIFIC_RESERVATION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#reservation_affinity_type VertexAiEndpointWithModelGardenDeployment#reservation_affinity_type}
        :param key: Corresponds to the label key of a reservation resource. To target a SPECIFIC_RESERVATION by name, use 'compute.googleapis.com/reservation-name' as the key and specify the name of your reservation as its value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#key VertexAiEndpointWithModelGardenDeployment#key}
        :param values: Corresponds to the label values of a reservation resource. This must be the full resource name of the reservation or reservation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#values VertexAiEndpointWithModelGardenDeployment#values}
        '''
        value = VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity(
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
    ) -> "VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinityOutputReference":
        return typing.cast("VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinityOutputReference", jsii.get(self, "reservationAffinity"))

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
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity"]:
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity"], jsii.get(self, "reservationAffinityInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7ef697940600037754b8aec9885efc57466ec2743701f0cdefde85ed152f42ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__748e6ebf74d0be33136f1deb69d14d6aa8f8ff1e586b2191724fe55201fa98d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7d2e10ad82fa9a3f7d6d00a18ab77953152019923036049c80d287d84aa8c0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multihostGpuNodeCount")
    def multihost_gpu_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "multihostGpuNodeCount"))

    @multihost_gpu_node_count.setter
    def multihost_gpu_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a6e95760f8b2831e01576057fafa29e8dc267689aac81c636ed03cda44d55df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multihostGpuNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tpuTopology")
    def tpu_topology(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpuTopology"))

    @tpu_topology.setter
    def tpu_topology(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a82726dd91be6517f06c07657a257eee205da2942bd0ad8b951f547df49af94b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpuTopology", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f4324e7a16c3f1c25fc6ae790504bc0cd16c93dad663d9d3007ca4ff938db28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity",
    jsii_struct_bases=[],
    name_mapping={
        "reservation_affinity_type": "reservationAffinityType",
        "key": "key",
        "values": "values",
    },
)
class VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity:
    def __init__(
        self,
        *,
        reservation_affinity_type: builtins.str,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param reservation_affinity_type: Specifies the reservation affinity type. Possible values: TYPE_UNSPECIFIED NO_RESERVATION ANY_RESERVATION SPECIFIC_RESERVATION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#reservation_affinity_type VertexAiEndpointWithModelGardenDeployment#reservation_affinity_type}
        :param key: Corresponds to the label key of a reservation resource. To target a SPECIFIC_RESERVATION by name, use 'compute.googleapis.com/reservation-name' as the key and specify the name of your reservation as its value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#key VertexAiEndpointWithModelGardenDeployment#key}
        :param values: Corresponds to the label values of a reservation resource. This must be the full resource name of the reservation or reservation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#values VertexAiEndpointWithModelGardenDeployment#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7801dcc3ea0e34735644b00c4d807eb91fe7f1b482c17664d9f34023688184b3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#reservation_affinity_type VertexAiEndpointWithModelGardenDeployment#reservation_affinity_type}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#key VertexAiEndpointWithModelGardenDeployment#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Corresponds to the label values of a reservation resource.

        This must be the
        full resource name of the reservation or reservation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#values VertexAiEndpointWithModelGardenDeployment#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ded6a31cdbf5c3b4a15b6b2f7b9499824e63087fb5157f6cd1f89fa54736187)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32bcbb37106487628a25e29f0019e5f580b98da5a23d36a4447bcb64d2da7e33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reservationAffinityType")
    def reservation_affinity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reservationAffinityType"))

    @reservation_affinity_type.setter
    def reservation_affinity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c816c27b332b1823e6f5dd8830bc4066e0ca9599d01fce11a9f67de18b9cee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservationAffinityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b4839e43afebd2714e3b2b7f56b5d1fa015cd16e36e1ca4ba455f34f2c734b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c54fcacff6bd731dda9c9313a402701887fa3c28bf9007b646a032b3689ba0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93ce78a1468e7b20f80c65b1d6a5f4ecb14cee7a15f4339ff5f8212b5c81928e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscalingMetricSpecs")
    def put_autoscaling_metric_specs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39ab58fda269e42b43f579056ff51479489ab9ad93013e3181f5c1fa188477e6)
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
        reservation_affinity: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
        tpu_topology: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerator_count: The number of accelerators to attach to the machine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#accelerator_count VertexAiEndpointWithModelGardenDeployment#accelerator_count}
        :param accelerator_type: Possible values: ACCELERATOR_TYPE_UNSPECIFIED NVIDIA_TESLA_K80 NVIDIA_TESLA_P100 NVIDIA_TESLA_V100 NVIDIA_TESLA_P4 NVIDIA_TESLA_T4 NVIDIA_TESLA_A100 NVIDIA_A100_80GB NVIDIA_L4 NVIDIA_H100_80GB NVIDIA_H100_MEGA_80GB NVIDIA_H200_141GB NVIDIA_B200 TPU_V2 TPU_V3 TPU_V4_POD TPU_V5_LITEPOD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#accelerator_type VertexAiEndpointWithModelGardenDeployment#accelerator_type}
        :param machine_type: The type of the machine. See the `list of machine types supported for prediction <https://cloud.google.com/vertex-ai/docs/predictions/configure-compute#machine-types>`_ See the `list of machine types supported for custom training <https://cloud.google.com/vertex-ai/docs/training/configure-compute#machine-types>`_. For DeployedModel this field is optional, and the default value is 'n1-standard-2'. For BatchPredictionJob or as part of WorkerPoolSpec this field is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#machine_type VertexAiEndpointWithModelGardenDeployment#machine_type}
        :param multihost_gpu_node_count: The number of nodes per replica for multihost GPU deployments. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#multihost_gpu_node_count VertexAiEndpointWithModelGardenDeployment#multihost_gpu_node_count}
        :param reservation_affinity: reservation_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#reservation_affinity VertexAiEndpointWithModelGardenDeployment#reservation_affinity}
        :param tpu_topology: The topology of the TPUs. Corresponds to the TPU topologies available from GKE. (Example: tpu_topology: "2x2x1"). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#tpu_topology VertexAiEndpointWithModelGardenDeployment#tpu_topology}
        '''
        value = VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec(
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
    ) -> VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecsList:
        return typing.cast(VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecsList, jsii.get(self, "autoscalingMetricSpecs"))

    @builtins.property
    @jsii.member(jsii_name="machineSpec")
    def machine_spec(
        self,
    ) -> VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecOutputReference:
        return typing.cast(VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecOutputReference, jsii.get(self, "machineSpec"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingMetricSpecsInput")
    def autoscaling_metric_specs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs]]], jsii.get(self, "autoscalingMetricSpecsInput"))

    @builtins.property
    @jsii.member(jsii_name="machineSpecInput")
    def machine_spec_input(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec], jsii.get(self, "machineSpecInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a0575e530580aeac9bbf07846d87b66327af19ee5f31b740764541e2ff329d8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxReplicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minReplicaCount")
    def min_replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReplicaCount"))

    @min_replica_count.setter
    def min_replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e7862a231e57b2a6496202ae050bbd59601edaa0398014395ade32447fb641d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minReplicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requiredReplicaCount")
    def required_replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "requiredReplicaCount"))

    @required_replica_count.setter
    def required_replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaedb0c3700459f844282e8fc8da1ec8651e8e1856e679ab228aced1c2e4fe08)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6704c153404dad80e4c65f10810256be8aeb7e27b01fa728c1f726e4b7e2ddf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6bce349bc382e23d6bca8126b32866295cff4e4a18ec7faa1b820b8b6f866b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointWithModelGardenDeploymentDeployConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentDeployConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc57a4478653c0cad7aec3ab02ade017ebc4f452149d144ba790eb1569c8f29f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDedicatedResources")
    def put_dedicated_resources(
        self,
        *,
        machine_spec: typing.Union[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec, typing.Dict[builtins.str, typing.Any]],
        min_replica_count: jsii.Number,
        autoscaling_metric_specs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs, typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_replica_count: typing.Optional[jsii.Number] = None,
        required_replica_count: typing.Optional[jsii.Number] = None,
        spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param machine_spec: machine_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#machine_spec VertexAiEndpointWithModelGardenDeployment#machine_spec}
        :param min_replica_count: The minimum number of machine replicas that will be always deployed on. This value must be greater than or equal to 1. If traffic increases, it may dynamically be deployed onto more replicas, and as traffic decreases, some of these extra replicas may be freed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#min_replica_count VertexAiEndpointWithModelGardenDeployment#min_replica_count}
        :param autoscaling_metric_specs: autoscaling_metric_specs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#autoscaling_metric_specs VertexAiEndpointWithModelGardenDeployment#autoscaling_metric_specs}
        :param max_replica_count: The maximum number of replicas that may be deployed on when the traffic against it increases. If the requested value is too large, the deployment will error, but if deployment succeeds then the ability to scale to that many replicas is guaranteed (barring service outages). If traffic increases beyond what its replicas at maximum may handle, a portion of the traffic will be dropped. If this value is not provided, will use min_replica_count as the default value. The value of this field impacts the charge against Vertex CPU and GPU quotas. Specifically, you will be charged for (max_replica_count * number of cores in the selected machine type) and (max_replica_count * number of GPUs per replica in the selected machine type). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#max_replica_count VertexAiEndpointWithModelGardenDeployment#max_replica_count}
        :param required_replica_count: Number of required available replicas for the deployment to succeed. This field is only needed when partial deployment/mutation is desired. If set, the deploy/mutate operation will succeed once available_replica_count reaches required_replica_count, and the rest of the replicas will be retried. If not set, the default required_replica_count will be min_replica_count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#required_replica_count VertexAiEndpointWithModelGardenDeployment#required_replica_count}
        :param spot: If true, schedule the deployment workload on `spot VMs <https://cloud.google.com/kubernetes-engine/docs/concepts/spot-vms>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#spot VertexAiEndpointWithModelGardenDeployment#spot}
        '''
        value = VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources(
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
    ) -> VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesOutputReference:
        return typing.cast(VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesOutputReference, jsii.get(self, "dedicatedResources"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedResourcesInput")
    def dedicated_resources_input(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources], jsii.get(self, "dedicatedResourcesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__295c0465e30e1b66f715f62be8fd23351c3364ce34fb06da4cb9afeb6680cc50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fastTryoutEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemLabels")
    def system_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "systemLabels"))

    @system_labels.setter
    def system_labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0f4fbbc90c3d91b98489143e3515c55a4a7a7fb56b45d1dc435c4ab4fe99e98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentDeployConfig]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentDeployConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentDeployConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ae99b3ccac870e9cf03ca659a16de3036206c62a453e422e7dbb6a194c621cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentEndpointConfig",
    jsii_struct_bases=[],
    name_mapping={
        "dedicated_endpoint_enabled": "dedicatedEndpointEnabled",
        "endpoint_display_name": "endpointDisplayName",
    },
)
class VertexAiEndpointWithModelGardenDeploymentEndpointConfig:
    def __init__(
        self,
        *,
        dedicated_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        endpoint_display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dedicated_endpoint_enabled: If true, the endpoint will be exposed through a dedicated DNS [Endpoint.dedicated_endpoint_dns]. Your request to the dedicated DNS will be isolated from other users' traffic and will have better performance and reliability. Note: Once you enabled dedicated endpoint, you won't be able to send request to the shared DNS {region}-aiplatform.googleapis.com. The limitations will be removed soon. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#dedicated_endpoint_enabled VertexAiEndpointWithModelGardenDeployment#dedicated_endpoint_enabled}
        :param endpoint_display_name: The user-specified display name of the endpoint. If not set, a default name will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#endpoint_display_name VertexAiEndpointWithModelGardenDeployment#endpoint_display_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__043914b0dcaff6ce69418fe4af0edcd6ecfc17137be31a05845ad4c3a8eec0d0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#dedicated_endpoint_enabled VertexAiEndpointWithModelGardenDeployment#dedicated_endpoint_enabled}
        '''
        result = self._values.get("dedicated_endpoint_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def endpoint_display_name(self) -> typing.Optional[builtins.str]:
        '''The user-specified display name of the endpoint. If not set, a default name will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#endpoint_display_name VertexAiEndpointWithModelGardenDeployment#endpoint_display_name}
        '''
        result = self._values.get("endpoint_display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentEndpointConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointWithModelGardenDeploymentEndpointConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentEndpointConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39d8edfb9a1cb35f769e7ecad862a8682613276d021e020b028397e418d522fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3141278eb2a9ff4bcdbeefaf880fbcbd839b858b2d828a59d1ba96d5e90b82f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dedicatedEndpointEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpointDisplayName")
    def endpoint_display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointDisplayName"))

    @endpoint_display_name.setter
    def endpoint_display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c74a891b23aa42223602f85b0ab2b6bd429082ae2d78456290c0f868a8117e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointDisplayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentEndpointConfig]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentEndpointConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentEndpointConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d83999933d5bd417b29509d4b53d3ce69a77ac999329ce6e725512c8697ff1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfig",
    jsii_struct_bases=[],
    name_mapping={
        "accept_eula": "acceptEula",
        "container_spec": "containerSpec",
        "hugging_face_access_token": "huggingFaceAccessToken",
        "hugging_face_cache_enabled": "huggingFaceCacheEnabled",
        "model_display_name": "modelDisplayName",
    },
)
class VertexAiEndpointWithModelGardenDeploymentModelConfig:
    def __init__(
        self,
        *,
        accept_eula: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        container_spec: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        hugging_face_access_token: typing.Optional[builtins.str] = None,
        hugging_face_cache_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        model_display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accept_eula: Whether the user accepts the End User License Agreement (EULA) for the model. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#accept_eula VertexAiEndpointWithModelGardenDeployment#accept_eula}
        :param container_spec: container_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#container_spec VertexAiEndpointWithModelGardenDeployment#container_spec}
        :param hugging_face_access_token: The Hugging Face read access token used to access the model artifacts of gated models. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#hugging_face_access_token VertexAiEndpointWithModelGardenDeployment#hugging_face_access_token}
        :param hugging_face_cache_enabled: If true, the model will deploy with a cached version instead of directly downloading the model artifacts from Hugging Face. This is suitable for VPC-SC users with limited internet access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#hugging_face_cache_enabled VertexAiEndpointWithModelGardenDeployment#hugging_face_cache_enabled}
        :param model_display_name: The user-specified display name of the uploaded model. If not set, a default name will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#model_display_name VertexAiEndpointWithModelGardenDeployment#model_display_name}
        '''
        if isinstance(container_spec, dict):
            container_spec = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec(**container_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__203f85dcb75ecb19fd8f65f6fa1a6bde4750c795b7b90c18ee1f92bc05b359d5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#accept_eula VertexAiEndpointWithModelGardenDeployment#accept_eula}
        '''
        result = self._values.get("accept_eula")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def container_spec(
        self,
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec"]:
        '''container_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#container_spec VertexAiEndpointWithModelGardenDeployment#container_spec}
        '''
        result = self._values.get("container_spec")
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec"], result)

    @builtins.property
    def hugging_face_access_token(self) -> typing.Optional[builtins.str]:
        '''The Hugging Face read access token used to access the model artifacts of gated models.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#hugging_face_access_token VertexAiEndpointWithModelGardenDeployment#hugging_face_access_token}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#hugging_face_cache_enabled VertexAiEndpointWithModelGardenDeployment#hugging_face_cache_enabled}
        '''
        result = self._values.get("hugging_face_cache_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def model_display_name(self) -> typing.Optional[builtins.str]:
        '''The user-specified display name of the uploaded model. If not set, a default name will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#model_display_name VertexAiEndpointWithModelGardenDeployment#model_display_name}
        '''
        result = self._values.get("model_display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec",
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
class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec:
    def __init__(
        self,
        *,
        image_uri: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        deployment_timeout: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv", typing.Dict[builtins.str, typing.Any]]]]] = None,
        grpc_ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        health_probe: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe", typing.Dict[builtins.str, typing.Any]]] = None,
        health_route: typing.Optional[builtins.str] = None,
        liveness_probe: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe", typing.Dict[builtins.str, typing.Any]]] = None,
        ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        predict_route: typing.Optional[builtins.str] = None,
        shared_memory_size_mb: typing.Optional[builtins.str] = None,
        startup_probe: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param image_uri: URI of the Docker image to be used as the custom container for serving predictions. This URI must identify an image in Artifact Registry or Container Registry. Learn more about the `container publishing requirements <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#publishing>`_, including permissions requirements for the Vertex AI Service Agent. The container image is ingested upon ModelService.UploadModel, stored internally, and this original path is afterwards not used. To learn about the requirements for the Docker image itself, see `Custom container requirements <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#>`_. You can use the URI to one of Vertex AI's `pre-built container images for prediction <https://cloud.google.com/vertex-ai/docs/predictions/pre-built-containers>`_ in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#image_uri VertexAiEndpointWithModelGardenDeployment#image_uri}
        :param args: Specifies arguments for the command that runs when the container starts. This overrides the container's `'CMD' <https://docs.docker.com/engine/reference/builder/#cmd>`_. Specify this field as an array of executable and arguments, similar to a Docker 'CMD''s "default parameters" form. If you don't specify this field but do specify the command field, then the command from the 'command' field runs without any additional arguments. See the `Kubernetes documentation about how the 'command' and 'args' fields interact with a container's 'ENTRYPOINT' and 'CMD' <https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#notes>`_. If you don't specify this field and don't specify the 'command' field, then the container's `'ENTRYPOINT' <https://docs.docker.com/engine/reference/builder/#cmd>`_ and 'CMD' determine what runs based on their default behavior. See the Docker documentation about `how 'CMD' and 'ENTRYPOINT' interact <https://docs.docker.com/engine/reference/builder/#understand-how-cmd-and-entrypoint-interact>`_. In this field, you can reference `environment variables set by Vertex AI <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_ and environment variables set in the env field. You cannot reference environment variables set in the Docker image. In order for environment variables to be expanded, reference them by using the following syntax:$(VARIABLE_NAME) Note that this differs from Bash variable expansion, which does not use parentheses. If a variable cannot be resolved, the reference in the input string is used unchanged. To avoid variable expansion, you can escape this syntax with '$$'; for example:$$(VARIABLE_NAME) This field corresponds to the 'args' field of the Kubernetes Containers `v1 core API <https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.23/#container-v1-core>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#args VertexAiEndpointWithModelGardenDeployment#args}
        :param command: Specifies the command that runs when the container starts. This overrides the container's `ENTRYPOINT <https://docs.docker.com/engine/reference/builder/#entrypoint>`_. Specify this field as an array of executable and arguments, similar to a Docker 'ENTRYPOINT''s "exec" form, not its "shell" form. If you do not specify this field, then the container's 'ENTRYPOINT' runs, in conjunction with the args field or the container's `'CMD' <https://docs.docker.com/engine/reference/builder/#cmd>`_, if either exists. If this field is not specified and the container does not have an 'ENTRYPOINT', then refer to the Docker documentation about `how 'CMD' and 'ENTRYPOINT' interact <https://docs.docker.com/engine/reference/builder/#understand-how-cmd-and-entrypoint-interact>`_. If you specify this field, then you can also specify the 'args' field to provide additional arguments for this command. However, if you specify this field, then the container's 'CMD' is ignored. See the `Kubernetes documentation about how the 'command' and 'args' fields interact with a container's 'ENTRYPOINT' and 'CMD' <https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#notes>`_. In this field, you can reference `environment variables set by Vertex AI <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_ and environment variables set in the env field. You cannot reference environment variables set in the Docker image. In order for environment variables to be expanded, reference them by using the following syntax:$(VARIABLE_NAME) Note that this differs from Bash variable expansion, which does not use parentheses. If a variable cannot be resolved, the reference in the input string is used unchanged. To avoid variable expansion, you can escape this syntax with '$$'; for example:$$(VARIABLE_NAME) This field corresponds to the 'command' field of the Kubernetes Containers `v1 core API <https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.23/#container-v1-core>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#command VertexAiEndpointWithModelGardenDeployment#command}
        :param deployment_timeout: Deployment timeout. Limit for deployment timeout is 2 hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#deployment_timeout VertexAiEndpointWithModelGardenDeployment#deployment_timeout}
        :param env: env block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#env VertexAiEndpointWithModelGardenDeployment#env}
        :param grpc_ports: grpc_ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#grpc_ports VertexAiEndpointWithModelGardenDeployment#grpc_ports}
        :param health_probe: health_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#health_probe VertexAiEndpointWithModelGardenDeployment#health_probe}
        :param health_route: HTTP path on the container to send health checks to. Vertex AI intermittently sends GET requests to this path on the container's IP address and port to check that the container is healthy. Read more about `health checks <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#health>`_. For example, if you set this field to '/bar', then Vertex AI intermittently sends a GET request to the '/bar' path on the port of your container specified by the first value of this 'ModelContainerSpec''s ports field. If you don't specify this field, it defaults to the following value when you deploy this Model to an Endpoint:/v1/endpoints/ENDPOINT/deployedModels/DEPLOYED_MODEL:predict The placeholders in this value are replaced as follows: - ENDPOINT: The last segment (following 'endpoints/')of the Endpoint.name][] field of the Endpoint where this Model has been deployed. (Vertex AI makes this value available to your container code as the `'AIP_ENDPOINT_ID' environment variable <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_.) - DEPLOYED_MODEL: DeployedModel.id of the 'DeployedModel'. (Vertex AI makes this value available to your container code as the `'AIP_DEPLOYED_MODEL_ID' environment variable <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_.) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#health_route VertexAiEndpointWithModelGardenDeployment#health_route}
        :param liveness_probe: liveness_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#liveness_probe VertexAiEndpointWithModelGardenDeployment#liveness_probe}
        :param ports: ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#ports VertexAiEndpointWithModelGardenDeployment#ports}
        :param predict_route: HTTP path on the container to send prediction requests to. Vertex AI forwards requests sent using projects.locations.endpoints.predict to this path on the container's IP address and port. Vertex AI then returns the container's response in the API response. For example, if you set this field to '/foo', then when Vertex AI receives a prediction request, it forwards the request body in a POST request to the '/foo' path on the port of your container specified by the first value of this 'ModelContainerSpec''s ports field. If you don't specify this field, it defaults to the following value when you deploy this Model to an Endpoint:/v1/endpoints/ENDPOINT/deployedModels/DEPLOYED_MODEL:predict The placeholders in this value are replaced as follows: - ENDPOINT: The last segment (following 'endpoints/')of the Endpoint.name][] field of the Endpoint where this Model has been deployed. (Vertex AI makes this value available to your container code as the `'AIP_ENDPOINT_ID' environment variable <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_.) - DEPLOYED_MODEL: DeployedModel.id of the 'DeployedModel'. (Vertex AI makes this value available to your container code as the `'AIP_DEPLOYED_MODEL_ID' environment variable <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_.) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#predict_route VertexAiEndpointWithModelGardenDeployment#predict_route}
        :param shared_memory_size_mb: The amount of the VM memory to reserve as the shared memory for the model in megabytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#shared_memory_size_mb VertexAiEndpointWithModelGardenDeployment#shared_memory_size_mb}
        :param startup_probe: startup_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#startup_probe VertexAiEndpointWithModelGardenDeployment#startup_probe}
        '''
        if isinstance(health_probe, dict):
            health_probe = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe(**health_probe)
        if isinstance(liveness_probe, dict):
            liveness_probe = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe(**liveness_probe)
        if isinstance(startup_probe, dict):
            startup_probe = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe(**startup_probe)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__607ce6f922c84e3557c78b5636819968898033902c3dd84431a631fcf813f0d2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#image_uri VertexAiEndpointWithModelGardenDeployment#image_uri}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#args VertexAiEndpointWithModelGardenDeployment#args}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#command VertexAiEndpointWithModelGardenDeployment#command}
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deployment_timeout(self) -> typing.Optional[builtins.str]:
        '''Deployment timeout. Limit for deployment timeout is 2 hours.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#deployment_timeout VertexAiEndpointWithModelGardenDeployment#deployment_timeout}
        '''
        result = self._values.get("deployment_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv"]]]:
        '''env block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#env VertexAiEndpointWithModelGardenDeployment#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv"]]], result)

    @builtins.property
    def grpc_ports(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts"]]]:
        '''grpc_ports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#grpc_ports VertexAiEndpointWithModelGardenDeployment#grpc_ports}
        '''
        result = self._values.get("grpc_ports")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts"]]], result)

    @builtins.property
    def health_probe(
        self,
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe"]:
        '''health_probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#health_probe VertexAiEndpointWithModelGardenDeployment#health_probe}
        '''
        result = self._values.get("health_probe")
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe"], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#health_route VertexAiEndpointWithModelGardenDeployment#health_route}
        '''
        result = self._values.get("health_route")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def liveness_probe(
        self,
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe"]:
        '''liveness_probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#liveness_probe VertexAiEndpointWithModelGardenDeployment#liveness_probe}
        '''
        result = self._values.get("liveness_probe")
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe"], result)

    @builtins.property
    def ports(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts"]]]:
        '''ports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#ports VertexAiEndpointWithModelGardenDeployment#ports}
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts"]]], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#predict_route VertexAiEndpointWithModelGardenDeployment#predict_route}
        '''
        result = self._values.get("predict_route")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shared_memory_size_mb(self) -> typing.Optional[builtins.str]:
        '''The amount of the VM memory to reserve as the shared memory for the model in megabytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#shared_memory_size_mb VertexAiEndpointWithModelGardenDeployment#shared_memory_size_mb}
        '''
        result = self._values.get("shared_memory_size_mb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def startup_probe(
        self,
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe"]:
        '''startup_probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#startup_probe VertexAiEndpointWithModelGardenDeployment#startup_probe}
        '''
        result = self._values.get("startup_probe")
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Name of the environment variable. Must be a valid C identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#name VertexAiEndpointWithModelGardenDeployment#name}
        :param value: Variables that reference a $(VAR_NAME) are expanded using the previous defined environment variables in the container and any service environment variables. If a variable cannot be resolved, the reference in the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, regardless of whether the variable exists or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#value VertexAiEndpointWithModelGardenDeployment#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bf0c91b90f579945096c2f9eda1d3d20a1ebb133fa60e595621d62072561e93)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the environment variable. Must be a valid C identifier.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#name VertexAiEndpointWithModelGardenDeployment#name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#value VertexAiEndpointWithModelGardenDeployment#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnvList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnvList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42baac13605807e174823cd86b99493838f4895fe966b61e9fdc81d3910663b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnvOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd10b1d076ac6a9e73ec634c541253f081cdc1b1c73da28b1b8e94a5c55146c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnvOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa696957bcf3c0775cf359d8706e03862578b2dd6fe43eb15e266b44dd10883d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f66c0a05bc29b933a1e891af50140a09cee1fb50edbc0c2f02c880e56bf6616b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e65b6db9991b105195137ab81784accdd8c59196aa72589d49acb4b8d192521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9fa6b7d3d5728b65c52cff627b32a9cffb9ff87ec888427d21a0f9b7a61cf7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnvOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnvOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab5c6c0adad0361f35c55d08af9e83d750452268bbb8740be8409fa637e7daca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54d08e9bbbc9ec4885be6aa148047f604330c6743cdcdfd2c60a9ffe067485a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c8dc61ff21c9ef92d2965f7e6187ce44eebba89a588a59e32812faa4ca99c87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c873bc6c88f783e1190a152bcc64858e8839a209665d65f0115e0f722aec81a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts",
    jsii_struct_bases=[],
    name_mapping={"container_port": "containerPort"},
)
class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts:
    def __init__(self, *, container_port: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param container_port: The number of the port to expose on the pod's IP address. Must be a valid port number, between 1 and 65535 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#container_port VertexAiEndpointWithModelGardenDeployment#container_port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d61e6e0cbc5edd3d7fa6fedf6870d4ab6a911b9fb675714d88258fa88088efe0)
            check_type(argname="argument container_port", value=container_port, expected_type=type_hints["container_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_port is not None:
            self._values["container_port"] = container_port

    @builtins.property
    def container_port(self) -> typing.Optional[jsii.Number]:
        '''The number of the port to expose on the pod's IP address.

        Must be a valid port number, between 1 and 65535 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#container_port VertexAiEndpointWithModelGardenDeployment#container_port}
        '''
        result = self._values.get("container_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPortsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPortsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03e52929d74656579057026f3dc7f169e680a7ce5d192643dfed53d217b64e22)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPortsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2832967345ac5e173e3101690a73a4af6942f6e1826037c3b2de8ac3a8da6b6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPortsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f26f7afcf2ec378f385960c0e7b7e01917f0dc1e6b529c2168ef30562b11e806)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63f0554200630bc18c03bea5fafd573db30da7e764c5bfa4d29cbe4055e4301e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7044a1a781c50072e7162ab0018a534b46d75faed38db717e46236c812b070a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf8b0efbd7be6426f89490d2afbd75404667b06976bd7f970ba64360535b985d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPortsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPortsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fc73dc000f5a5512b5cb38f50d79317333a8aa1f29ea4914ea521d62966aac6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b164667b14bc0439622a180a7dab00f2149b04239137643450ac65b7ce9f4a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7763bfedb66c3e33f651ee4334ef6428a2e58911529c205077aa1f28b45471a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe",
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
class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe:
    def __init__(
        self,
        *,
        exec: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec", typing.Dict[builtins.str, typing.Any]]] = None,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        success_threshold: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param exec: exec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#exec VertexAiEndpointWithModelGardenDeployment#exec}
        :param failure_threshold: Number of consecutive failures before the probe is considered failed. Defaults to 3. Minimum value is 1. Maps to Kubernetes probe argument 'failureThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#failure_threshold VertexAiEndpointWithModelGardenDeployment#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#grpc VertexAiEndpointWithModelGardenDeployment#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#http_get VertexAiEndpointWithModelGardenDeployment#http_get}
        :param initial_delay_seconds: Number of seconds to wait before starting the probe. Defaults to 0. Minimum value is 0. Maps to Kubernetes probe argument 'initialDelaySeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#initial_delay_seconds VertexAiEndpointWithModelGardenDeployment#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Must be less than timeout_seconds. Maps to Kubernetes probe argument 'periodSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#period_seconds VertexAiEndpointWithModelGardenDeployment#period_seconds}
        :param success_threshold: Number of consecutive successes before the probe is considered successful. Defaults to 1. Minimum value is 1. Maps to Kubernetes probe argument 'successThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#success_threshold VertexAiEndpointWithModelGardenDeployment#success_threshold}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#tcp_socket VertexAiEndpointWithModelGardenDeployment#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Must be greater or equal to period_seconds. Maps to Kubernetes probe argument 'timeoutSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#timeout_seconds VertexAiEndpointWithModelGardenDeployment#timeout_seconds}
        '''
        if isinstance(exec, dict):
            exec = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec(**exec)
        if isinstance(grpc, dict):
            grpc = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc(**grpc)
        if isinstance(http_get, dict):
            http_get = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet(**http_get)
        if isinstance(tcp_socket, dict):
            tcp_socket = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket(**tcp_socket)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__095710d75e6c2d6b1cdbc3daec87d29c4104864789067ff370067290fc851baf)
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
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec"]:
        '''exec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#exec VertexAiEndpointWithModelGardenDeployment#exec}
        '''
        result = self._values.get("exec")
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec"], result)

    @builtins.property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        '''Number of consecutive failures before the probe is considered failed. Defaults to 3. Minimum value is 1.

        Maps to Kubernetes probe argument 'failureThreshold'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#failure_threshold VertexAiEndpointWithModelGardenDeployment#failure_threshold}
        '''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def grpc(
        self,
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc"]:
        '''grpc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#grpc VertexAiEndpointWithModelGardenDeployment#grpc}
        '''
        result = self._values.get("grpc")
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc"], result)

    @builtins.property
    def http_get(
        self,
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet"]:
        '''http_get block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#http_get VertexAiEndpointWithModelGardenDeployment#http_get}
        '''
        result = self._values.get("http_get")
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet"], result)

    @builtins.property
    def initial_delay_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds to wait before starting the probe. Defaults to 0. Minimum value is 0.

        Maps to Kubernetes probe argument 'initialDelaySeconds'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#initial_delay_seconds VertexAiEndpointWithModelGardenDeployment#initial_delay_seconds}
        '''
        result = self._values.get("initial_delay_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period_seconds(self) -> typing.Optional[jsii.Number]:
        '''How often (in seconds) to perform the probe.

        Default to 10 seconds.
        Minimum value is 1. Must be less than timeout_seconds.

        Maps to Kubernetes probe argument 'periodSeconds'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#period_seconds VertexAiEndpointWithModelGardenDeployment#period_seconds}
        '''
        result = self._values.get("period_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def success_threshold(self) -> typing.Optional[jsii.Number]:
        '''Number of consecutive successes before the probe is considered successful. Defaults to 1. Minimum value is 1.

        Maps to Kubernetes probe argument 'successThreshold'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#success_threshold VertexAiEndpointWithModelGardenDeployment#success_threshold}
        '''
        result = self._values.get("success_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tcp_socket(
        self,
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket"]:
        '''tcp_socket block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#tcp_socket VertexAiEndpointWithModelGardenDeployment#tcp_socket}
        '''
        result = self._values.get("tcp_socket")
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket"], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after which the probe times out.

        Defaults to 1 second.
        Minimum value is 1. Must be greater or equal to period_seconds.

        Maps to Kubernetes probe argument 'timeoutSeconds'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#timeout_seconds VertexAiEndpointWithModelGardenDeployment#timeout_seconds}
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec",
    jsii_struct_bases=[],
    name_mapping={"command": "command"},
)
class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec:
    def __init__(
        self,
        *,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param command: Command is the command line to execute inside the container, the working directory for the command is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#command VertexAiEndpointWithModelGardenDeployment#command}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b08a8a80aed5084f11a3d9a4d2dd42653d2dd5599a40fdca08cd0287bd88af79)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#command VertexAiEndpointWithModelGardenDeployment#command}
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96213e179f4f24d44957d9990169bd8b9087d7316d47bcf790c6fc3e95859768)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbbf03a17a06586a6e42170141ed8d05829c50c420f51326e660ef05520403ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb0376d459577f82ddd6fabb9bb2cf4e04df7e8fdfaa55182aa0ae47f2b78713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "service": "service"},
)
class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc:
    def __init__(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number of the gRPC service. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        :param service: Service is the name of the service to place in the gRPC HealthCheckRequest. See https://github.com/grpc/grpc/blob/master/doc/health-checking.md. If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#service VertexAiEndpointWithModelGardenDeployment#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e85b4fb40ab9c0abc36357f4161c0982f858c23925050aab77b8133bd441ab6f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''Service is the name of the service to place in the gRPC HealthCheckRequest. See https://github.com/grpc/grpc/blob/master/doc/health-checking.md.

        If this is not specified, the default behavior is defined by gRPC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#service VertexAiEndpointWithModelGardenDeployment#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5a6d27a1809179c1a088a490ae41f75beaa032f1a63cd250bebe0d35429262c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc9c48023496c50e69f7daff646e54ad76abd5e7e7740e85084c3b08178a47e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edb3c75bc835ee3bd578460f38de8da54f860b43d9f1abc93191b4e86dc03a93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67e917d4dc9f4be95af283c3c6c06e8d627cb3794500b639f85024eca67b0f46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "http_headers": "httpHeaders",
        "path": "path",
        "port": "port",
        "scheme": "scheme",
    },
)
class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        scheme: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: Host name to connect to, defaults to the model serving container's IP. You probably want to set "Host" in httpHeaders instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#host VertexAiEndpointWithModelGardenDeployment#host}
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#http_headers VertexAiEndpointWithModelGardenDeployment#http_headers}
        :param path: Path to access on the HTTP server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#path VertexAiEndpointWithModelGardenDeployment#path}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        :param scheme: Scheme to use for connecting to the host. Defaults to HTTP. Acceptable values are "HTTP" or "HTTPS". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#scheme VertexAiEndpointWithModelGardenDeployment#scheme}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__229aef6951090a938696b3de4f8e5d1c92acc46b3666c8d1feeae171374480d4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#host VertexAiEndpointWithModelGardenDeployment#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders"]]]:
        '''http_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#http_headers VertexAiEndpointWithModelGardenDeployment#http_headers}
        '''
        result = self._values.get("http_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders"]]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to access on the HTTP server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#path VertexAiEndpointWithModelGardenDeployment#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Number of the port to access on the container. Number must be in the range 1 to 65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scheme(self) -> typing.Optional[builtins.str]:
        '''Scheme to use for connecting to the host. Defaults to HTTP. Acceptable values are "HTTP" or "HTTPS".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#scheme VertexAiEndpointWithModelGardenDeployment#scheme}
        '''
        result = self._values.get("scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The header field name. This will be canonicalized upon output, so case-variant names will be understood as the same header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#name VertexAiEndpointWithModelGardenDeployment#name}
        :param value: The header field value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#value VertexAiEndpointWithModelGardenDeployment#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eba02b42b8e9784e47c37975481f51313ea8fcc96d004e583620a4dd09466f92)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#name VertexAiEndpointWithModelGardenDeployment#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The header field value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#value VertexAiEndpointWithModelGardenDeployment#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c539b3ef3acb678895f320bda429309564eb443717bdae935a376508021b76e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5158ef6829fd35d88c087778aba53b7b39102b9a0fd907c5e701c09b5b160633)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93dcdd18f651d83a2ef452bf2b65127f8beed7785a15885e9f872847cd003e1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3366161c0b428e9d90658792082c5d24eb7a6d5e9283005cc739d519aea2cd6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea9e20b177e2c6976cadcfb5993ace4d13bd5ee52c73280f2fe071485e5334cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ab646f6471927ec79590595f4eb3e4d29bf3a5925804b43f87ab332dda48623)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b82b4f6a9f4d89a63b0eefb5c30d5a09c3d327090ab6318d5fcdbea35500b682)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33000b77219ee1193d45b9a4c3ed405f0a4d9e39af1307511064bcc5352ad972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1285d21c88cb5939694046c35231b2a41461dbace352b7e181403be4a6726f0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e81513844c4f793e49c35aff13490f1d1177d49afe169f4416dbb6dc4c9a0f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfcaa2c1be9590c76471bd57e0b1ff102025a3194d24d5e9f0bc6bb344fc5a7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpHeaders")
    def put_http_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd92bd1993f0b0866cff1b6519f3ef5f7ac760acb86ddbb922a1ee367b5687cb)
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
    ) -> VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeadersList:
        return typing.cast(VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeadersList, jsii.get(self, "httpHeaders"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="httpHeadersInput")
    def http_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders]]], jsii.get(self, "httpHeadersInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__bac49ca58e149df6917495fa1b835fb6a543ea109ca1545f625dc3f6994a6643)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a84d2b84b7ac610b2e895cb4d6b2decb2089b6cd6eab4a25da34ae804e3ad984)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__367ea48602964f7fd82cc43e48ddd8f053ec5bfb31eb69d942fbf5fa2154e662)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheme")
    def scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheme"))

    @scheme.setter
    def scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__098407e19af0a19b1291e98198f2dd7fb9818fd75bc8306315899723c89d8d12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aed48db93091e4dac7d15a8a5e614ee438f1811342182b29cf30bdd2fd6a3b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e529c2159d0a7657076dbab2ba772e6565c459254a35b375ae317bab28c2259e)
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
        :param command: Command is the command line to execute inside the container, the working directory for the command is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#command VertexAiEndpointWithModelGardenDeployment#command}
        '''
        value = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec(
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
        :param port: Port number of the gRPC service. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        :param service: Service is the name of the service to place in the gRPC HealthCheckRequest. See https://github.com/grpc/grpc/blob/master/doc/health-checking.md. If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#service VertexAiEndpointWithModelGardenDeployment#service}
        '''
        value = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc(
            port=port, service=service
        )

        return typing.cast(None, jsii.invoke(self, "putGrpc", [value]))

    @jsii.member(jsii_name="putHttpGet")
    def put_http_get(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        scheme: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: Host name to connect to, defaults to the model serving container's IP. You probably want to set "Host" in httpHeaders instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#host VertexAiEndpointWithModelGardenDeployment#host}
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#http_headers VertexAiEndpointWithModelGardenDeployment#http_headers}
        :param path: Path to access on the HTTP server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#path VertexAiEndpointWithModelGardenDeployment#path}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        :param scheme: Scheme to use for connecting to the host. Defaults to HTTP. Acceptable values are "HTTP" or "HTTPS". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#scheme VertexAiEndpointWithModelGardenDeployment#scheme}
        '''
        value = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet(
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
        :param host: Optional: Host name to connect to, defaults to the model serving container's IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#host VertexAiEndpointWithModelGardenDeployment#host}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        '''
        value = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket(
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
    ) -> VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExecOutputReference:
        return typing.cast(VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExecOutputReference, jsii.get(self, "exec"))

    @builtins.property
    @jsii.member(jsii_name="grpc")
    def grpc(
        self,
    ) -> VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpcOutputReference:
        return typing.cast(VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpcOutputReference, jsii.get(self, "grpc"))

    @builtins.property
    @jsii.member(jsii_name="httpGet")
    def http_get(
        self,
    ) -> VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetOutputReference:
        return typing.cast(VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetOutputReference, jsii.get(self, "httpGet"))

    @builtins.property
    @jsii.member(jsii_name="tcpSocket")
    def tcp_socket(
        self,
    ) -> "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocketOutputReference":
        return typing.cast("VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocketOutputReference", jsii.get(self, "tcpSocket"))

    @builtins.property
    @jsii.member(jsii_name="execInput")
    def exec_input(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec], jsii.get(self, "execInput"))

    @builtins.property
    @jsii.member(jsii_name="failureThresholdInput")
    def failure_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcInput")
    def grpc_input(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc], jsii.get(self, "grpcInput"))

    @builtins.property
    @jsii.member(jsii_name="httpGetInput")
    def http_get_input(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet], jsii.get(self, "httpGetInput"))

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
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket"]:
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket"], jsii.get(self, "tcpSocketInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ad5e62859fcec675cf6e116156298a81ff31d03b0e1e4624e9450adf23578d2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelaySeconds")
    def initial_delay_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelaySeconds"))

    @initial_delay_seconds.setter
    def initial_delay_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__470e5865aef70fc536d5d94cae44c2eecfe78095d26fc01feeacbf82e80cbba5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelaySeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodSeconds")
    def period_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodSeconds"))

    @period_seconds.setter
    def period_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18ef52c0a49f7ec17f936ddbabcb6fa298f5ff8a7759afaaaa343344cec652be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successThreshold")
    def success_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successThreshold"))

    @success_threshold.setter
    def success_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1587f6de0367edd3643237345a8db726e1ec5a611dc680a0bd0b9350be8cb41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f36eabe6316717480b3435cdecb1e19d24cd7cea84953251fca0c3120913d1fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b011c4001c64c1c21b1d9fb339126e61594654f1da64b7211705dd4960b5a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket",
    jsii_struct_bases=[],
    name_mapping={"host": "host", "port": "port"},
)
class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param host: Optional: Host name to connect to, defaults to the model serving container's IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#host VertexAiEndpointWithModelGardenDeployment#host}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__253d1dca32393cf9dc66799bab9c451b912fcb93eef1449058d29e83e043ad16)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#host VertexAiEndpointWithModelGardenDeployment#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Number of the port to access on the container. Number must be in the range 1 to 65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocketOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocketOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2194f50c09eb951ad88310f154399cb29781bf387db562c77a0d8822607ac7ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1734309bf4ded49e45491fa5634496caed997f3845943b4ab51d388be8d02a96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a5d8331d4f46c5021f9cd7e035062c59ce7afabac963f1c6cf61cf027124211)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86219665b21b30df9374d92581096e1aaa6b655b7eaee04d0026676a5889080d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe",
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
class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe:
    def __init__(
        self,
        *,
        exec: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec", typing.Dict[builtins.str, typing.Any]]] = None,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        success_threshold: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param exec: exec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#exec VertexAiEndpointWithModelGardenDeployment#exec}
        :param failure_threshold: Number of consecutive failures before the probe is considered failed. Defaults to 3. Minimum value is 1. Maps to Kubernetes probe argument 'failureThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#failure_threshold VertexAiEndpointWithModelGardenDeployment#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#grpc VertexAiEndpointWithModelGardenDeployment#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#http_get VertexAiEndpointWithModelGardenDeployment#http_get}
        :param initial_delay_seconds: Number of seconds to wait before starting the probe. Defaults to 0. Minimum value is 0. Maps to Kubernetes probe argument 'initialDelaySeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#initial_delay_seconds VertexAiEndpointWithModelGardenDeployment#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Must be less than timeout_seconds. Maps to Kubernetes probe argument 'periodSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#period_seconds VertexAiEndpointWithModelGardenDeployment#period_seconds}
        :param success_threshold: Number of consecutive successes before the probe is considered successful. Defaults to 1. Minimum value is 1. Maps to Kubernetes probe argument 'successThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#success_threshold VertexAiEndpointWithModelGardenDeployment#success_threshold}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#tcp_socket VertexAiEndpointWithModelGardenDeployment#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Must be greater or equal to period_seconds. Maps to Kubernetes probe argument 'timeoutSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#timeout_seconds VertexAiEndpointWithModelGardenDeployment#timeout_seconds}
        '''
        if isinstance(exec, dict):
            exec = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec(**exec)
        if isinstance(grpc, dict):
            grpc = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc(**grpc)
        if isinstance(http_get, dict):
            http_get = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet(**http_get)
        if isinstance(tcp_socket, dict):
            tcp_socket = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket(**tcp_socket)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa0672bd51a65fc8c6d48993d05d498b287d7ae1df8a608fe1330ac040adc262)
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
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec"]:
        '''exec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#exec VertexAiEndpointWithModelGardenDeployment#exec}
        '''
        result = self._values.get("exec")
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec"], result)

    @builtins.property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        '''Number of consecutive failures before the probe is considered failed. Defaults to 3. Minimum value is 1.

        Maps to Kubernetes probe argument 'failureThreshold'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#failure_threshold VertexAiEndpointWithModelGardenDeployment#failure_threshold}
        '''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def grpc(
        self,
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc"]:
        '''grpc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#grpc VertexAiEndpointWithModelGardenDeployment#grpc}
        '''
        result = self._values.get("grpc")
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc"], result)

    @builtins.property
    def http_get(
        self,
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet"]:
        '''http_get block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#http_get VertexAiEndpointWithModelGardenDeployment#http_get}
        '''
        result = self._values.get("http_get")
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet"], result)

    @builtins.property
    def initial_delay_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds to wait before starting the probe. Defaults to 0. Minimum value is 0.

        Maps to Kubernetes probe argument 'initialDelaySeconds'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#initial_delay_seconds VertexAiEndpointWithModelGardenDeployment#initial_delay_seconds}
        '''
        result = self._values.get("initial_delay_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period_seconds(self) -> typing.Optional[jsii.Number]:
        '''How often (in seconds) to perform the probe.

        Default to 10 seconds.
        Minimum value is 1. Must be less than timeout_seconds.

        Maps to Kubernetes probe argument 'periodSeconds'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#period_seconds VertexAiEndpointWithModelGardenDeployment#period_seconds}
        '''
        result = self._values.get("period_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def success_threshold(self) -> typing.Optional[jsii.Number]:
        '''Number of consecutive successes before the probe is considered successful. Defaults to 1. Minimum value is 1.

        Maps to Kubernetes probe argument 'successThreshold'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#success_threshold VertexAiEndpointWithModelGardenDeployment#success_threshold}
        '''
        result = self._values.get("success_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tcp_socket(
        self,
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket"]:
        '''tcp_socket block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#tcp_socket VertexAiEndpointWithModelGardenDeployment#tcp_socket}
        '''
        result = self._values.get("tcp_socket")
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket"], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after which the probe times out.

        Defaults to 1 second.
        Minimum value is 1. Must be greater or equal to period_seconds.

        Maps to Kubernetes probe argument 'timeoutSeconds'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#timeout_seconds VertexAiEndpointWithModelGardenDeployment#timeout_seconds}
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec",
    jsii_struct_bases=[],
    name_mapping={"command": "command"},
)
class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec:
    def __init__(
        self,
        *,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param command: Command is the command line to execute inside the container, the working directory for the command is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#command VertexAiEndpointWithModelGardenDeployment#command}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16039a4d1af1bcbee10c6c5da5d3f4615f4b7f7b29fbed3acacf9f160e37a8ff)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#command VertexAiEndpointWithModelGardenDeployment#command}
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__394b6aadfccc10b0c1fc851c6bb127206460dfa32ef0c98c07e308ffb0488dee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57902bc7116e8964c49ddfea9bcf9ad85a56ed09991d97cd202dd74bdbc91ea6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5dc0c5a3803d7ab67e9aa99c807b691fbbc89012a11e08c4fb8505cec22be56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "service": "service"},
)
class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc:
    def __init__(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number of the gRPC service. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        :param service: Service is the name of the service to place in the gRPC HealthCheckRequest. See https://github.com/grpc/grpc/blob/master/doc/health-checking.md. If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#service VertexAiEndpointWithModelGardenDeployment#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__921d4cda2ef983e9f30b4c11bb1b50bf4ee84555ac83a3db9ed0b028a7dba4c0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''Service is the name of the service to place in the gRPC HealthCheckRequest. See https://github.com/grpc/grpc/blob/master/doc/health-checking.md.

        If this is not specified, the default behavior is defined by gRPC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#service VertexAiEndpointWithModelGardenDeployment#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fc234d1341e1934bfc260ee0a75af10c2ff599d459ec4056ba044c2a3f384a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed9fcfa9ee76295549b1cded221549b17283a709149f564ba370e2fa3aac3997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d7211d50e4a150c5675837bcc4b489f7c881b6d027d867540a559a810d5a0a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e803a0874b19be90eb606a5dc0ed8dc5a3378c4697d6efe9af5e6988e7a58f45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "http_headers": "httpHeaders",
        "path": "path",
        "port": "port",
        "scheme": "scheme",
    },
)
class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        scheme: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: Host name to connect to, defaults to the model serving container's IP. You probably want to set "Host" in httpHeaders instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#host VertexAiEndpointWithModelGardenDeployment#host}
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#http_headers VertexAiEndpointWithModelGardenDeployment#http_headers}
        :param path: Path to access on the HTTP server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#path VertexAiEndpointWithModelGardenDeployment#path}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        :param scheme: Scheme to use for connecting to the host. Defaults to HTTP. Acceptable values are "HTTP" or "HTTPS". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#scheme VertexAiEndpointWithModelGardenDeployment#scheme}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bd598309c5c570bc1248955ec412fe75a849227a8ecd824031f47f3a60d2171)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#host VertexAiEndpointWithModelGardenDeployment#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders"]]]:
        '''http_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#http_headers VertexAiEndpointWithModelGardenDeployment#http_headers}
        '''
        result = self._values.get("http_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders"]]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to access on the HTTP server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#path VertexAiEndpointWithModelGardenDeployment#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Number of the port to access on the container. Number must be in the range 1 to 65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scheme(self) -> typing.Optional[builtins.str]:
        '''Scheme to use for connecting to the host. Defaults to HTTP. Acceptable values are "HTTP" or "HTTPS".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#scheme VertexAiEndpointWithModelGardenDeployment#scheme}
        '''
        result = self._values.get("scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The header field name. This will be canonicalized upon output, so case-variant names will be understood as the same header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#name VertexAiEndpointWithModelGardenDeployment#name}
        :param value: The header field value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#value VertexAiEndpointWithModelGardenDeployment#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__215a26de43f911e643623c6621db3258f3564dd3a61b3a5c6833ccdcb2540474)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#name VertexAiEndpointWithModelGardenDeployment#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The header field value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#value VertexAiEndpointWithModelGardenDeployment#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22a2d1efe27062cdc530f0013ae3c7720d589a5103f2e3edf0653a1ef963c7da)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aa4be1d8f6d8ef9487f1b9a5fe9274e281cb8e275e22dca2d724a7fe85ffa66)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b1d3af6a6ded3bbf8cbf13b40864feabd5f2407b8996edf23e86141d6414409)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1826f58163c92168e9af8fa378c2fceb020de4f40c290af5a04f7d84f4d0164)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9378df92f9a820041b45cd95c9799f10bd191f76f1c877023528179f567357a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98ce5cfec9043b4eefc781126313be8a043ea5ecbf267a0264f944c8975fbe79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa6372c41b67558153d58a0197cfa8f5e4635081baf790e81b2b11be90fe28f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f1cca7c14d0d57acabaa24d4a0d6eff50b562c706eff55bc07290c4c094166a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a785424d21dd4b3166ce863cf30b32cffbef77587d98dedf8c67795d015f213)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a829725fb0710c41abb55f7500b614aa8a9014d34e71e4bb9105fc09120e6dc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__58996a1be088c0545c27dffda11e57919846c552efb62d928e981991473af42d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpHeaders")
    def put_http_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08cf8b1046e8d2dca545e95256a944c9a05ca4ee09cae8a264a009a8575d3d7b)
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
    ) -> VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeadersList:
        return typing.cast(VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeadersList, jsii.get(self, "httpHeaders"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="httpHeadersInput")
    def http_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders]]], jsii.get(self, "httpHeadersInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9692caa0f5e41631821d2ba30db23c9e35fe550ff006fc245be48a33ba3f7675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76ebc33b7242caa9749d05d563573d9dd066ab0fe379f382eb4c092b1fe7dde1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0450ecf912e03b4b2781733729bcff912f56f1b410e5fb608c6534bdb28628f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheme")
    def scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheme"))

    @scheme.setter
    def scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c74d5e5df0dd423d3936d6c0384271a844cc4d35fdf46e9ff7604509f751d1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dc393f665e2062b8379f19d53fddcca8639afdf8edceec76017d5e58f39b901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cff813df31e2670269884be2ee591f17563927455f5404ce81070e923a3ff442)
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
        :param command: Command is the command line to execute inside the container, the working directory for the command is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#command VertexAiEndpointWithModelGardenDeployment#command}
        '''
        value = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec(
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
        :param port: Port number of the gRPC service. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        :param service: Service is the name of the service to place in the gRPC HealthCheckRequest. See https://github.com/grpc/grpc/blob/master/doc/health-checking.md. If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#service VertexAiEndpointWithModelGardenDeployment#service}
        '''
        value = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc(
            port=port, service=service
        )

        return typing.cast(None, jsii.invoke(self, "putGrpc", [value]))

    @jsii.member(jsii_name="putHttpGet")
    def put_http_get(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        scheme: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: Host name to connect to, defaults to the model serving container's IP. You probably want to set "Host" in httpHeaders instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#host VertexAiEndpointWithModelGardenDeployment#host}
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#http_headers VertexAiEndpointWithModelGardenDeployment#http_headers}
        :param path: Path to access on the HTTP server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#path VertexAiEndpointWithModelGardenDeployment#path}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        :param scheme: Scheme to use for connecting to the host. Defaults to HTTP. Acceptable values are "HTTP" or "HTTPS". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#scheme VertexAiEndpointWithModelGardenDeployment#scheme}
        '''
        value = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet(
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
        :param host: Optional: Host name to connect to, defaults to the model serving container's IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#host VertexAiEndpointWithModelGardenDeployment#host}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        '''
        value = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket(
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
    ) -> VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExecOutputReference:
        return typing.cast(VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExecOutputReference, jsii.get(self, "exec"))

    @builtins.property
    @jsii.member(jsii_name="grpc")
    def grpc(
        self,
    ) -> VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpcOutputReference:
        return typing.cast(VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpcOutputReference, jsii.get(self, "grpc"))

    @builtins.property
    @jsii.member(jsii_name="httpGet")
    def http_get(
        self,
    ) -> VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetOutputReference:
        return typing.cast(VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetOutputReference, jsii.get(self, "httpGet"))

    @builtins.property
    @jsii.member(jsii_name="tcpSocket")
    def tcp_socket(
        self,
    ) -> "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocketOutputReference":
        return typing.cast("VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocketOutputReference", jsii.get(self, "tcpSocket"))

    @builtins.property
    @jsii.member(jsii_name="execInput")
    def exec_input(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec], jsii.get(self, "execInput"))

    @builtins.property
    @jsii.member(jsii_name="failureThresholdInput")
    def failure_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcInput")
    def grpc_input(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc], jsii.get(self, "grpcInput"))

    @builtins.property
    @jsii.member(jsii_name="httpGetInput")
    def http_get_input(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet], jsii.get(self, "httpGetInput"))

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
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket"]:
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket"], jsii.get(self, "tcpSocketInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d3807f2af08e1b0ee70c0516feebc4fd75332c41c85ca38f6f318030c44b743c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelaySeconds")
    def initial_delay_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelaySeconds"))

    @initial_delay_seconds.setter
    def initial_delay_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e962249e6874b7c7a44155dfe265a69f8594ba01a26c370c917aae452e8523f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelaySeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodSeconds")
    def period_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodSeconds"))

    @period_seconds.setter
    def period_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62118daea7b345016aa2bcebcca408b9f82f07b01553b4ff7f5582964371c44e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successThreshold")
    def success_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successThreshold"))

    @success_threshold.setter
    def success_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2520bd2795afe6deb07f81c4eca583cd62f19866b7bd6a3ab05d04b81d39676)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__981dcbb8d5f6f944943859afb16a7348ecd8c429b825467db82af142410cad49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2b0e286ab228fb5f9e938ff1543cf5f3695569f6bbc688fa17bc6a02fc8d309)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket",
    jsii_struct_bases=[],
    name_mapping={"host": "host", "port": "port"},
)
class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param host: Optional: Host name to connect to, defaults to the model serving container's IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#host VertexAiEndpointWithModelGardenDeployment#host}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b0973de20f14d90d36c3145ab60a9173b9b44a43bf32d4ef91c96bca9e35e6b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#host VertexAiEndpointWithModelGardenDeployment#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Number of the port to access on the container. Number must be in the range 1 to 65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocketOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocketOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11005f3511ad32b4428f61cd2fbdb3ac3fed535cbe4157c476d9ca9de1acb7e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2263362774772b5f0e92efcaca82ed3e4c24bd3507fac95b1aa7eae5581b1f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47968a2062a157fb736daca900beb53c9f7d44782dd959d33ded51e80818ce5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a12a99f2f2475e4edddbc52e70dbfd12c59ebd7e7dc3cacd969f7cb40e2386f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f244885973e2db911bddced4d1cef4eb3abcdf36beb06086181f6828f81bad45)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEnv")
    def put_env(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04bcf0a419e56d8ad1c67124135cd25c2c118ff3b82bf3271981a000b6f87d79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnv", [value]))

    @jsii.member(jsii_name="putGrpcPorts")
    def put_grpc_ports(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__259f672ee4dacd7a78e49b04205fbce9f3dee52cd073e56fb1802591168ca8ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGrpcPorts", [value]))

    @jsii.member(jsii_name="putHealthProbe")
    def put_health_probe(
        self,
        *,
        exec: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec, typing.Dict[builtins.str, typing.Any]]] = None,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        success_threshold: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param exec: exec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#exec VertexAiEndpointWithModelGardenDeployment#exec}
        :param failure_threshold: Number of consecutive failures before the probe is considered failed. Defaults to 3. Minimum value is 1. Maps to Kubernetes probe argument 'failureThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#failure_threshold VertexAiEndpointWithModelGardenDeployment#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#grpc VertexAiEndpointWithModelGardenDeployment#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#http_get VertexAiEndpointWithModelGardenDeployment#http_get}
        :param initial_delay_seconds: Number of seconds to wait before starting the probe. Defaults to 0. Minimum value is 0. Maps to Kubernetes probe argument 'initialDelaySeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#initial_delay_seconds VertexAiEndpointWithModelGardenDeployment#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Must be less than timeout_seconds. Maps to Kubernetes probe argument 'periodSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#period_seconds VertexAiEndpointWithModelGardenDeployment#period_seconds}
        :param success_threshold: Number of consecutive successes before the probe is considered successful. Defaults to 1. Minimum value is 1. Maps to Kubernetes probe argument 'successThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#success_threshold VertexAiEndpointWithModelGardenDeployment#success_threshold}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#tcp_socket VertexAiEndpointWithModelGardenDeployment#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Must be greater or equal to period_seconds. Maps to Kubernetes probe argument 'timeoutSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#timeout_seconds VertexAiEndpointWithModelGardenDeployment#timeout_seconds}
        '''
        value = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe(
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
        exec: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec, typing.Dict[builtins.str, typing.Any]]] = None,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        success_threshold: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param exec: exec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#exec VertexAiEndpointWithModelGardenDeployment#exec}
        :param failure_threshold: Number of consecutive failures before the probe is considered failed. Defaults to 3. Minimum value is 1. Maps to Kubernetes probe argument 'failureThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#failure_threshold VertexAiEndpointWithModelGardenDeployment#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#grpc VertexAiEndpointWithModelGardenDeployment#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#http_get VertexAiEndpointWithModelGardenDeployment#http_get}
        :param initial_delay_seconds: Number of seconds to wait before starting the probe. Defaults to 0. Minimum value is 0. Maps to Kubernetes probe argument 'initialDelaySeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#initial_delay_seconds VertexAiEndpointWithModelGardenDeployment#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Must be less than timeout_seconds. Maps to Kubernetes probe argument 'periodSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#period_seconds VertexAiEndpointWithModelGardenDeployment#period_seconds}
        :param success_threshold: Number of consecutive successes before the probe is considered successful. Defaults to 1. Minimum value is 1. Maps to Kubernetes probe argument 'successThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#success_threshold VertexAiEndpointWithModelGardenDeployment#success_threshold}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#tcp_socket VertexAiEndpointWithModelGardenDeployment#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Must be greater or equal to period_seconds. Maps to Kubernetes probe argument 'timeoutSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#timeout_seconds VertexAiEndpointWithModelGardenDeployment#timeout_seconds}
        '''
        value = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f10814f06bc318361e9d7cf24a6df1de1a6a2b13d922956e8dc6a0f6e8f4fd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPorts", [value]))

    @jsii.member(jsii_name="putStartupProbe")
    def put_startup_probe(
        self,
        *,
        exec: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec", typing.Dict[builtins.str, typing.Any]]] = None,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        success_threshold: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param exec: exec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#exec VertexAiEndpointWithModelGardenDeployment#exec}
        :param failure_threshold: Number of consecutive failures before the probe is considered failed. Defaults to 3. Minimum value is 1. Maps to Kubernetes probe argument 'failureThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#failure_threshold VertexAiEndpointWithModelGardenDeployment#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#grpc VertexAiEndpointWithModelGardenDeployment#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#http_get VertexAiEndpointWithModelGardenDeployment#http_get}
        :param initial_delay_seconds: Number of seconds to wait before starting the probe. Defaults to 0. Minimum value is 0. Maps to Kubernetes probe argument 'initialDelaySeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#initial_delay_seconds VertexAiEndpointWithModelGardenDeployment#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Must be less than timeout_seconds. Maps to Kubernetes probe argument 'periodSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#period_seconds VertexAiEndpointWithModelGardenDeployment#period_seconds}
        :param success_threshold: Number of consecutive successes before the probe is considered successful. Defaults to 1. Minimum value is 1. Maps to Kubernetes probe argument 'successThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#success_threshold VertexAiEndpointWithModelGardenDeployment#success_threshold}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#tcp_socket VertexAiEndpointWithModelGardenDeployment#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Must be greater or equal to period_seconds. Maps to Kubernetes probe argument 'timeoutSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#timeout_seconds VertexAiEndpointWithModelGardenDeployment#timeout_seconds}
        '''
        value = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe(
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
    ) -> VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnvList:
        return typing.cast(VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnvList, jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="grpcPorts")
    def grpc_ports(
        self,
    ) -> VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPortsList:
        return typing.cast(VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPortsList, jsii.get(self, "grpcPorts"))

    @builtins.property
    @jsii.member(jsii_name="healthProbe")
    def health_probe(
        self,
    ) -> VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeOutputReference:
        return typing.cast(VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeOutputReference, jsii.get(self, "healthProbe"))

    @builtins.property
    @jsii.member(jsii_name="livenessProbe")
    def liveness_probe(
        self,
    ) -> VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeOutputReference:
        return typing.cast(VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeOutputReference, jsii.get(self, "livenessProbe"))

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(
        self,
    ) -> "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPortsList":
        return typing.cast("VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPortsList", jsii.get(self, "ports"))

    @builtins.property
    @jsii.member(jsii_name="startupProbe")
    def startup_probe(
        self,
    ) -> "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeOutputReference":
        return typing.cast("VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeOutputReference", jsii.get(self, "startupProbe"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv]]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcPortsInput")
    def grpc_ports_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts]]], jsii.get(self, "grpcPortsInput"))

    @builtins.property
    @jsii.member(jsii_name="healthProbeInput")
    def health_probe_input(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe], jsii.get(self, "healthProbeInput"))

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
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe], jsii.get(self, "livenessProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts"]]], jsii.get(self, "portsInput"))

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
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe"]:
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe"], jsii.get(self, "startupProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59a58fe3759bf7af0f0bd274b0919caa833e073eb07a28554823987566006217)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3457ce077fa04cacb8035d4ee5d24ae02ad8f98e91649255fb4bb3f4edd67ee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deploymentTimeout")
    def deployment_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentTimeout"))

    @deployment_timeout.setter
    def deployment_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb60c4c975dd63335876b8d76b7acdc67c96c7a6596dd7a76c3dfc993d0e5b3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthRoute")
    def health_route(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthRoute"))

    @health_route.setter
    def health_route(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c96222a75417b4be8ebd4bc4dc8d0d25f32ee9950db858da6044fd073cffa407)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthRoute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageUri")
    def image_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageUri"))

    @image_uri.setter
    def image_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e65f31416d0358fc8cbeaf67b41c1f1987089736e3a9208f822b4b1314c62497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="predictRoute")
    def predict_route(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "predictRoute"))

    @predict_route.setter
    def predict_route(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ced18594d446b10678bc7e2c1df8348ebe35017851b7abda11e449b7d726567c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predictRoute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sharedMemorySizeMb")
    def shared_memory_size_mb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sharedMemorySizeMb"))

    @shared_memory_size_mb.setter
    def shared_memory_size_mb(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__188d0201644ab9d5a31e95eed7fb62330756d5a8a4473977cf9e464ff4856769)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedMemorySizeMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e6c67ca86da7c186a9715377876339b39b9c264809d2c9a391435312019d711)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts",
    jsii_struct_bases=[],
    name_mapping={"container_port": "containerPort"},
)
class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts:
    def __init__(self, *, container_port: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param container_port: The number of the port to expose on the pod's IP address. Must be a valid port number, between 1 and 65535 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#container_port VertexAiEndpointWithModelGardenDeployment#container_port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c674d93fd60fdd87b212c1e3b33671442606c684a0a14095b0b0d8cf5c0018c0)
            check_type(argname="argument container_port", value=container_port, expected_type=type_hints["container_port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_port is not None:
            self._values["container_port"] = container_port

    @builtins.property
    def container_port(self) -> typing.Optional[jsii.Number]:
        '''The number of the port to expose on the pod's IP address.

        Must be a valid port number, between 1 and 65535 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#container_port VertexAiEndpointWithModelGardenDeployment#container_port}
        '''
        result = self._values.get("container_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPortsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPortsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f9a3b7a1f427050c87dc6218b5d96b61bcffc6e71b27a07986f3199a863f259)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPortsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03bde5818b28845842816b9577fb82c22cb24a4ba34f584b2164b7bc6d926a89)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPortsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee1aa37a8d6dc67787ab33ae3c0a455773ce5a13ff81a5a10e690c0de0d3c445)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83bb131e54b9d0b7d04e77efa579f5e92903d0c1c10fa9793c92f318cbce8abc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30565a852c0b1067f6c4cfdfd41e53658a7b52d90362798f397cbc6b3a348a8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a713f637d271554def982e54ee4eb2a122b0342036b5b35feb35a18dd5cd3046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPortsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPortsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25e67db759a40ad771c11e83259f1034e48a896419e658e44f1d4593ae57c928)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5762e93dadba44af3e87d0b5a5f10a44c98bbb4176a9e0281dd53537a7ef82f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38412be91a48ef078536d08e2c2b0d9eace0b1a3e5d76fb7e1678bfbc3ba22e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe",
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
class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe:
    def __init__(
        self,
        *,
        exec: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec", typing.Dict[builtins.str, typing.Any]]] = None,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        success_threshold: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param exec: exec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#exec VertexAiEndpointWithModelGardenDeployment#exec}
        :param failure_threshold: Number of consecutive failures before the probe is considered failed. Defaults to 3. Minimum value is 1. Maps to Kubernetes probe argument 'failureThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#failure_threshold VertexAiEndpointWithModelGardenDeployment#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#grpc VertexAiEndpointWithModelGardenDeployment#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#http_get VertexAiEndpointWithModelGardenDeployment#http_get}
        :param initial_delay_seconds: Number of seconds to wait before starting the probe. Defaults to 0. Minimum value is 0. Maps to Kubernetes probe argument 'initialDelaySeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#initial_delay_seconds VertexAiEndpointWithModelGardenDeployment#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Must be less than timeout_seconds. Maps to Kubernetes probe argument 'periodSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#period_seconds VertexAiEndpointWithModelGardenDeployment#period_seconds}
        :param success_threshold: Number of consecutive successes before the probe is considered successful. Defaults to 1. Minimum value is 1. Maps to Kubernetes probe argument 'successThreshold'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#success_threshold VertexAiEndpointWithModelGardenDeployment#success_threshold}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#tcp_socket VertexAiEndpointWithModelGardenDeployment#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Must be greater or equal to period_seconds. Maps to Kubernetes probe argument 'timeoutSeconds'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#timeout_seconds VertexAiEndpointWithModelGardenDeployment#timeout_seconds}
        '''
        if isinstance(exec, dict):
            exec = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec(**exec)
        if isinstance(grpc, dict):
            grpc = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc(**grpc)
        if isinstance(http_get, dict):
            http_get = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet(**http_get)
        if isinstance(tcp_socket, dict):
            tcp_socket = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket(**tcp_socket)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c864151a1132dd01495331e0c5a5d5266ea2f555a2fca5a9f273914064af297)
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
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec"]:
        '''exec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#exec VertexAiEndpointWithModelGardenDeployment#exec}
        '''
        result = self._values.get("exec")
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec"], result)

    @builtins.property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        '''Number of consecutive failures before the probe is considered failed. Defaults to 3. Minimum value is 1.

        Maps to Kubernetes probe argument 'failureThreshold'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#failure_threshold VertexAiEndpointWithModelGardenDeployment#failure_threshold}
        '''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def grpc(
        self,
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc"]:
        '''grpc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#grpc VertexAiEndpointWithModelGardenDeployment#grpc}
        '''
        result = self._values.get("grpc")
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc"], result)

    @builtins.property
    def http_get(
        self,
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet"]:
        '''http_get block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#http_get VertexAiEndpointWithModelGardenDeployment#http_get}
        '''
        result = self._values.get("http_get")
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet"], result)

    @builtins.property
    def initial_delay_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds to wait before starting the probe. Defaults to 0. Minimum value is 0.

        Maps to Kubernetes probe argument 'initialDelaySeconds'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#initial_delay_seconds VertexAiEndpointWithModelGardenDeployment#initial_delay_seconds}
        '''
        result = self._values.get("initial_delay_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period_seconds(self) -> typing.Optional[jsii.Number]:
        '''How often (in seconds) to perform the probe.

        Default to 10 seconds.
        Minimum value is 1. Must be less than timeout_seconds.

        Maps to Kubernetes probe argument 'periodSeconds'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#period_seconds VertexAiEndpointWithModelGardenDeployment#period_seconds}
        '''
        result = self._values.get("period_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def success_threshold(self) -> typing.Optional[jsii.Number]:
        '''Number of consecutive successes before the probe is considered successful. Defaults to 1. Minimum value is 1.

        Maps to Kubernetes probe argument 'successThreshold'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#success_threshold VertexAiEndpointWithModelGardenDeployment#success_threshold}
        '''
        result = self._values.get("success_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tcp_socket(
        self,
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket"]:
        '''tcp_socket block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#tcp_socket VertexAiEndpointWithModelGardenDeployment#tcp_socket}
        '''
        result = self._values.get("tcp_socket")
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket"], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after which the probe times out.

        Defaults to 1 second.
        Minimum value is 1. Must be greater or equal to period_seconds.

        Maps to Kubernetes probe argument 'timeoutSeconds'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#timeout_seconds VertexAiEndpointWithModelGardenDeployment#timeout_seconds}
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec",
    jsii_struct_bases=[],
    name_mapping={"command": "command"},
)
class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec:
    def __init__(
        self,
        *,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param command: Command is the command line to execute inside the container, the working directory for the command is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#command VertexAiEndpointWithModelGardenDeployment#command}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37eab2fa8d200ee8b91bd9853f64ca59febdb755366c6e34b98585d2dda39ee5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#command VertexAiEndpointWithModelGardenDeployment#command}
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a9ef8352bdf02bc09569f0f6d1ccaff29780b98e90f0638e1bc6fa0507306a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a244dc9413af6843a9cfdd7ebf66dbe72bf196fdd2fcdb2dbc42fadf91adea39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c45bf65c20bc7c3e8dd19a934f676f8e72df227eb4257bd725725f0d07c56947)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "service": "service"},
)
class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc:
    def __init__(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number of the gRPC service. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        :param service: Service is the name of the service to place in the gRPC HealthCheckRequest. See https://github.com/grpc/grpc/blob/master/doc/health-checking.md. If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#service VertexAiEndpointWithModelGardenDeployment#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df0362256ce602963133edd92c09a7dba6cd466ca2daad3f9bdea846c73f2664)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''Service is the name of the service to place in the gRPC HealthCheckRequest. See https://github.com/grpc/grpc/blob/master/doc/health-checking.md.

        If this is not specified, the default behavior is defined by gRPC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#service VertexAiEndpointWithModelGardenDeployment#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8da0d57cf90c5901bb20f001430cf61fe058e1c25f51c2752dcd41a8914748e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9aefebfb310c5d8a35c6192a775d26e743f032951a5adf4c052514c975cab4ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3bf1cfb786f8fd14283187546fab48f34ebd020c2e740f27687208a6501ae9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b941d3de84e43d7ad189c95a2e8297261e5cfff21d1d3198530f8e153b19751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "http_headers": "httpHeaders",
        "path": "path",
        "port": "port",
        "scheme": "scheme",
    },
)
class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        scheme: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: Host name to connect to, defaults to the model serving container's IP. You probably want to set "Host" in httpHeaders instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#host VertexAiEndpointWithModelGardenDeployment#host}
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#http_headers VertexAiEndpointWithModelGardenDeployment#http_headers}
        :param path: Path to access on the HTTP server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#path VertexAiEndpointWithModelGardenDeployment#path}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        :param scheme: Scheme to use for connecting to the host. Defaults to HTTP. Acceptable values are "HTTP" or "HTTPS". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#scheme VertexAiEndpointWithModelGardenDeployment#scheme}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fa9a3047f73d82af7f4971db4f874132dbbd32dc2b98db2d503d7f838220674)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#host VertexAiEndpointWithModelGardenDeployment#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders"]]]:
        '''http_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#http_headers VertexAiEndpointWithModelGardenDeployment#http_headers}
        '''
        result = self._values.get("http_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders"]]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to access on the HTTP server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#path VertexAiEndpointWithModelGardenDeployment#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Number of the port to access on the container. Number must be in the range 1 to 65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scheme(self) -> typing.Optional[builtins.str]:
        '''Scheme to use for connecting to the host. Defaults to HTTP. Acceptable values are "HTTP" or "HTTPS".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#scheme VertexAiEndpointWithModelGardenDeployment#scheme}
        '''
        result = self._values.get("scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The header field name. This will be canonicalized upon output, so case-variant names will be understood as the same header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#name VertexAiEndpointWithModelGardenDeployment#name}
        :param value: The header field value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#value VertexAiEndpointWithModelGardenDeployment#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf75512372bb28ce035dc026e2f8af657401b9605aa7935fa7d833d556ee61d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#name VertexAiEndpointWithModelGardenDeployment#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The header field value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#value VertexAiEndpointWithModelGardenDeployment#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae0fe1aa2e19ae3d95d0a267012dd1a0334fe1044e013788e91a68fbaaaa075b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e5c42d69982a58ce4afd3b7c6aa37af1727bf40e52d7d85211a3cf5f5c0d851)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e95f518e9aa42354dcd34d67091a6f5e1178b926cde1947163888627444672c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8712c7f988b5867bc742c0a78a4c838bf14b9e856e266828872ea9342942c113)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73c80d795a2821e071e6d268ae6e2b2f5fff233e35625e5b71081995cdd34ed4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572911429ec1b292a3b46bd7dc650203952fadfcc2aac38cea97f4f0555ce412)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbc269ed3ca9e94b0e470e6cd58d165b1b40317d87c174266e268e27812a815e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df3507df041a7a7b1dc999a9252880deffd4697c0dd385ff131a3e8a4232363b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48c006b973b4eed46804053a358dfe744bd782856eb1606c6e44a9ccb31e1373)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__223daf2d1a022b46d6c3f087820ed5a4c28164030d94922f8b5e013af4f846dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03d104108a9bc521507d2dee8935cc2a34fbc36914e85167bac28fb413e8fa35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpHeaders")
    def put_http_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b21a9de8aebf516d52f2863a52ba80da3de15668220876d03f02d7126e85b242)
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
    ) -> VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeadersList:
        return typing.cast(VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeadersList, jsii.get(self, "httpHeaders"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="httpHeadersInput")
    def http_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders]]], jsii.get(self, "httpHeadersInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__28a29c61f159b6109c78e6791e0d45bcdee6e88629c6f12df5d4e7c1a4fe15f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4f8f8c6c051e8eb52591e25dbf64b380d354d0a0819bbb0e4daddec5966b087)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f31e50414528a4b5f385c874e623f4bd0a29e27419b23be5ea5f6ae949dd6461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheme")
    def scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheme"))

    @scheme.setter
    def scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97cf7c42c2286a3180a09b8c5a9206a1c49d6ab440fbda99c9d25d2d49ecf0ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea981630d424ef6049027ae17638dcc9605c7a4bce710d1b68c737a93d5847d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__152374bb07ddcc764658647f831a4325b8ac85c1af405d3a39d6f65fd0148708)
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
        :param command: Command is the command line to execute inside the container, the working directory for the command is root ('/') in the container's filesystem. The command is simply exec'd, it is not run inside a shell, so traditional shell instructions ('|', etc) won't work. To use a shell, you need to explicitly call out to that shell. Exit status of 0 is treated as live/healthy and non-zero is unhealthy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#command VertexAiEndpointWithModelGardenDeployment#command}
        '''
        value = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec(
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
        :param port: Port number of the gRPC service. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        :param service: Service is the name of the service to place in the gRPC HealthCheckRequest. See https://github.com/grpc/grpc/blob/master/doc/health-checking.md. If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#service VertexAiEndpointWithModelGardenDeployment#service}
        '''
        value = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc(
            port=port, service=service
        )

        return typing.cast(None, jsii.invoke(self, "putGrpc", [value]))

    @jsii.member(jsii_name="putHttpGet")
    def put_http_get(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        scheme: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: Host name to connect to, defaults to the model serving container's IP. You probably want to set "Host" in httpHeaders instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#host VertexAiEndpointWithModelGardenDeployment#host}
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#http_headers VertexAiEndpointWithModelGardenDeployment#http_headers}
        :param path: Path to access on the HTTP server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#path VertexAiEndpointWithModelGardenDeployment#path}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        :param scheme: Scheme to use for connecting to the host. Defaults to HTTP. Acceptable values are "HTTP" or "HTTPS". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#scheme VertexAiEndpointWithModelGardenDeployment#scheme}
        '''
        value = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet(
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
        :param host: Optional: Host name to connect to, defaults to the model serving container's IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#host VertexAiEndpointWithModelGardenDeployment#host}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        '''
        value = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket(
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
    ) -> VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExecOutputReference:
        return typing.cast(VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExecOutputReference, jsii.get(self, "exec"))

    @builtins.property
    @jsii.member(jsii_name="grpc")
    def grpc(
        self,
    ) -> VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpcOutputReference:
        return typing.cast(VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpcOutputReference, jsii.get(self, "grpc"))

    @builtins.property
    @jsii.member(jsii_name="httpGet")
    def http_get(
        self,
    ) -> VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetOutputReference:
        return typing.cast(VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetOutputReference, jsii.get(self, "httpGet"))

    @builtins.property
    @jsii.member(jsii_name="tcpSocket")
    def tcp_socket(
        self,
    ) -> "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocketOutputReference":
        return typing.cast("VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocketOutputReference", jsii.get(self, "tcpSocket"))

    @builtins.property
    @jsii.member(jsii_name="execInput")
    def exec_input(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec], jsii.get(self, "execInput"))

    @builtins.property
    @jsii.member(jsii_name="failureThresholdInput")
    def failure_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcInput")
    def grpc_input(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc], jsii.get(self, "grpcInput"))

    @builtins.property
    @jsii.member(jsii_name="httpGetInput")
    def http_get_input(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet], jsii.get(self, "httpGetInput"))

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
    ) -> typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket"]:
        return typing.cast(typing.Optional["VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket"], jsii.get(self, "tcpSocketInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4a8f2c3e154b987cf0bc567fdc8151ca2538f4408ebd4cbd57ab5803391d6f58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelaySeconds")
    def initial_delay_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelaySeconds"))

    @initial_delay_seconds.setter
    def initial_delay_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20a6c0e6bdbb0e87ebf7582dc69737dcebd608ef42a71fbf5041a47a992f5a0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelaySeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodSeconds")
    def period_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodSeconds"))

    @period_seconds.setter
    def period_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f88e7d59833b0e84ad0a6ee1f2588b574150e82484cd195b81f474d7c9f70c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="successThreshold")
    def success_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "successThreshold"))

    @success_threshold.setter
    def success_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b5b7fa51794406b72e79a223126fec9f293fa0bf1fddc700321e8c52b2a013b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "successThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79c2769b64c683fe9bb24340c9e0194e8997ac3ccc36b5148dab9efdefe44430)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dd2707a36afb077957fc2e311c78fea8be6331147cd90dda40dc0b96ed9704d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket",
    jsii_struct_bases=[],
    name_mapping={"host": "host", "port": "port"},
)
class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param host: Optional: Host name to connect to, defaults to the model serving container's IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#host VertexAiEndpointWithModelGardenDeployment#host}
        :param port: Number of the port to access on the container. Number must be in the range 1 to 65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c145f6a8a3ec7736ff1d0cbaaec1d7ca56324c2666a4c16eb771a416e5a12ac)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#host VertexAiEndpointWithModelGardenDeployment#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Number of the port to access on the container. Number must be in the range 1 to 65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#port VertexAiEndpointWithModelGardenDeployment#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocketOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocketOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4daaee9c5363932b8e580817149d10f64ccb8efa902f9bcf31839a45b603d09e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffb5a6cb3bd0c9ad6afb8409b66b8eff68d84a83591c4b3f69ea75cf40551ebe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__500c39ab55e9e8f21b9e0126675bec6524e3d71809d2e59da754d21633adc5ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38597d1fa1ef34c517fa5c9e5da119977b3fc3713e7465883ac004400a304804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointWithModelGardenDeploymentModelConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentModelConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41979b55d1205da09e2ea5c0cc39c1a82bb1b0c9058529a6a2d6f8cee2d51254)
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
        env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv, typing.Dict[builtins.str, typing.Any]]]]] = None,
        grpc_ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts, typing.Dict[builtins.str, typing.Any]]]]] = None,
        health_probe: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe, typing.Dict[builtins.str, typing.Any]]] = None,
        health_route: typing.Optional[builtins.str] = None,
        liveness_probe: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe, typing.Dict[builtins.str, typing.Any]]] = None,
        ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts, typing.Dict[builtins.str, typing.Any]]]]] = None,
        predict_route: typing.Optional[builtins.str] = None,
        shared_memory_size_mb: typing.Optional[builtins.str] = None,
        startup_probe: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param image_uri: URI of the Docker image to be used as the custom container for serving predictions. This URI must identify an image in Artifact Registry or Container Registry. Learn more about the `container publishing requirements <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#publishing>`_, including permissions requirements for the Vertex AI Service Agent. The container image is ingested upon ModelService.UploadModel, stored internally, and this original path is afterwards not used. To learn about the requirements for the Docker image itself, see `Custom container requirements <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#>`_. You can use the URI to one of Vertex AI's `pre-built container images for prediction <https://cloud.google.com/vertex-ai/docs/predictions/pre-built-containers>`_ in this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#image_uri VertexAiEndpointWithModelGardenDeployment#image_uri}
        :param args: Specifies arguments for the command that runs when the container starts. This overrides the container's `'CMD' <https://docs.docker.com/engine/reference/builder/#cmd>`_. Specify this field as an array of executable and arguments, similar to a Docker 'CMD''s "default parameters" form. If you don't specify this field but do specify the command field, then the command from the 'command' field runs without any additional arguments. See the `Kubernetes documentation about how the 'command' and 'args' fields interact with a container's 'ENTRYPOINT' and 'CMD' <https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#notes>`_. If you don't specify this field and don't specify the 'command' field, then the container's `'ENTRYPOINT' <https://docs.docker.com/engine/reference/builder/#cmd>`_ and 'CMD' determine what runs based on their default behavior. See the Docker documentation about `how 'CMD' and 'ENTRYPOINT' interact <https://docs.docker.com/engine/reference/builder/#understand-how-cmd-and-entrypoint-interact>`_. In this field, you can reference `environment variables set by Vertex AI <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_ and environment variables set in the env field. You cannot reference environment variables set in the Docker image. In order for environment variables to be expanded, reference them by using the following syntax:$(VARIABLE_NAME) Note that this differs from Bash variable expansion, which does not use parentheses. If a variable cannot be resolved, the reference in the input string is used unchanged. To avoid variable expansion, you can escape this syntax with '$$'; for example:$$(VARIABLE_NAME) This field corresponds to the 'args' field of the Kubernetes Containers `v1 core API <https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.23/#container-v1-core>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#args VertexAiEndpointWithModelGardenDeployment#args}
        :param command: Specifies the command that runs when the container starts. This overrides the container's `ENTRYPOINT <https://docs.docker.com/engine/reference/builder/#entrypoint>`_. Specify this field as an array of executable and arguments, similar to a Docker 'ENTRYPOINT''s "exec" form, not its "shell" form. If you do not specify this field, then the container's 'ENTRYPOINT' runs, in conjunction with the args field or the container's `'CMD' <https://docs.docker.com/engine/reference/builder/#cmd>`_, if either exists. If this field is not specified and the container does not have an 'ENTRYPOINT', then refer to the Docker documentation about `how 'CMD' and 'ENTRYPOINT' interact <https://docs.docker.com/engine/reference/builder/#understand-how-cmd-and-entrypoint-interact>`_. If you specify this field, then you can also specify the 'args' field to provide additional arguments for this command. However, if you specify this field, then the container's 'CMD' is ignored. See the `Kubernetes documentation about how the 'command' and 'args' fields interact with a container's 'ENTRYPOINT' and 'CMD' <https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#notes>`_. In this field, you can reference `environment variables set by Vertex AI <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_ and environment variables set in the env field. You cannot reference environment variables set in the Docker image. In order for environment variables to be expanded, reference them by using the following syntax:$(VARIABLE_NAME) Note that this differs from Bash variable expansion, which does not use parentheses. If a variable cannot be resolved, the reference in the input string is used unchanged. To avoid variable expansion, you can escape this syntax with '$$'; for example:$$(VARIABLE_NAME) This field corresponds to the 'command' field of the Kubernetes Containers `v1 core API <https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.23/#container-v1-core>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#command VertexAiEndpointWithModelGardenDeployment#command}
        :param deployment_timeout: Deployment timeout. Limit for deployment timeout is 2 hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#deployment_timeout VertexAiEndpointWithModelGardenDeployment#deployment_timeout}
        :param env: env block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#env VertexAiEndpointWithModelGardenDeployment#env}
        :param grpc_ports: grpc_ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#grpc_ports VertexAiEndpointWithModelGardenDeployment#grpc_ports}
        :param health_probe: health_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#health_probe VertexAiEndpointWithModelGardenDeployment#health_probe}
        :param health_route: HTTP path on the container to send health checks to. Vertex AI intermittently sends GET requests to this path on the container's IP address and port to check that the container is healthy. Read more about `health checks <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#health>`_. For example, if you set this field to '/bar', then Vertex AI intermittently sends a GET request to the '/bar' path on the port of your container specified by the first value of this 'ModelContainerSpec''s ports field. If you don't specify this field, it defaults to the following value when you deploy this Model to an Endpoint:/v1/endpoints/ENDPOINT/deployedModels/DEPLOYED_MODEL:predict The placeholders in this value are replaced as follows: - ENDPOINT: The last segment (following 'endpoints/')of the Endpoint.name][] field of the Endpoint where this Model has been deployed. (Vertex AI makes this value available to your container code as the `'AIP_ENDPOINT_ID' environment variable <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_.) - DEPLOYED_MODEL: DeployedModel.id of the 'DeployedModel'. (Vertex AI makes this value available to your container code as the `'AIP_DEPLOYED_MODEL_ID' environment variable <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_.) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#health_route VertexAiEndpointWithModelGardenDeployment#health_route}
        :param liveness_probe: liveness_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#liveness_probe VertexAiEndpointWithModelGardenDeployment#liveness_probe}
        :param ports: ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#ports VertexAiEndpointWithModelGardenDeployment#ports}
        :param predict_route: HTTP path on the container to send prediction requests to. Vertex AI forwards requests sent using projects.locations.endpoints.predict to this path on the container's IP address and port. Vertex AI then returns the container's response in the API response. For example, if you set this field to '/foo', then when Vertex AI receives a prediction request, it forwards the request body in a POST request to the '/foo' path on the port of your container specified by the first value of this 'ModelContainerSpec''s ports field. If you don't specify this field, it defaults to the following value when you deploy this Model to an Endpoint:/v1/endpoints/ENDPOINT/deployedModels/DEPLOYED_MODEL:predict The placeholders in this value are replaced as follows: - ENDPOINT: The last segment (following 'endpoints/')of the Endpoint.name][] field of the Endpoint where this Model has been deployed. (Vertex AI makes this value available to your container code as the `'AIP_ENDPOINT_ID' environment variable <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_.) - DEPLOYED_MODEL: DeployedModel.id of the 'DeployedModel'. (Vertex AI makes this value available to your container code as the `'AIP_DEPLOYED_MODEL_ID' environment variable <https://cloud.google.com/vertex-ai/docs/predictions/custom-container-requirements#aip-variables>`_.) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#predict_route VertexAiEndpointWithModelGardenDeployment#predict_route}
        :param shared_memory_size_mb: The amount of the VM memory to reserve as the shared memory for the model in megabytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#shared_memory_size_mb VertexAiEndpointWithModelGardenDeployment#shared_memory_size_mb}
        :param startup_probe: startup_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#startup_probe VertexAiEndpointWithModelGardenDeployment#startup_probe}
        '''
        value = VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec(
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
    ) -> VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecOutputReference:
        return typing.cast(VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecOutputReference, jsii.get(self, "containerSpec"))

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
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec], jsii.get(self, "containerSpecInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e889498768977c35c1363af0ef829d9aa6ae1b2db3c3af59b2bf08f9ff825405)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceptEula", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="huggingFaceAccessToken")
    def hugging_face_access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "huggingFaceAccessToken"))

    @hugging_face_access_token.setter
    def hugging_face_access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a85c7646ed6f50c390223d474b7e6b31abb114b2e8e942075bca17528f50619)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd91eacaac6ce507522d13acd13b387a1640ff67ca1eb728ba395e1a8ca23055)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "huggingFaceCacheEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelDisplayName")
    def model_display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelDisplayName"))

    @model_display_name.setter
    def model_display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66d12c8e408617d5aaef4f032b604506c59d054b2b102ad550c9410580aef811)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelDisplayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfig]:
        return typing.cast(typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05838c2d8423cc32020212536ad085ba0d1292e53d8e6b496463be536493a121)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class VertexAiEndpointWithModelGardenDeploymentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#create VertexAiEndpointWithModelGardenDeployment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#delete VertexAiEndpointWithModelGardenDeployment#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fef62f77816edc18865030ac2ead253b05c924479d74d94023bd036034a8de7b)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#create VertexAiEndpointWithModelGardenDeployment#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint_with_model_garden_deployment#delete VertexAiEndpointWithModelGardenDeployment#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointWithModelGardenDeploymentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointWithModelGardenDeploymentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpointWithModelGardenDeployment.VertexAiEndpointWithModelGardenDeploymentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9c77ab4f5d3a24c29e8c6d6a89d62fe846c4f3c1aed59b08aeb2a251f8fbf6d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18c02149a80a5161ee64b3c0c9a171c4eefbaba7e4b5b6daf985255385a1bbaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d04eee4d6736e6643d0e52a03477129ef81520351e1bbe898d4968acc7bad3ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe9f9d2552fa89ea51c16a743ac0503190f688b8d5b70b511d189d2e14986f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VertexAiEndpointWithModelGardenDeployment",
    "VertexAiEndpointWithModelGardenDeploymentConfig",
    "VertexAiEndpointWithModelGardenDeploymentDeployConfig",
    "VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources",
    "VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs",
    "VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecsList",
    "VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecsOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec",
    "VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity",
    "VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinityOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentDeployConfigOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentEndpointConfig",
    "VertexAiEndpointWithModelGardenDeploymentEndpointConfigOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfig",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnvList",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnvOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPortsList",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPortsOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExecOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpcOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeadersList",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeadersOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocketOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExecOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpcOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeadersList",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeadersOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocketOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPortsList",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPortsOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExecOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpcOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeadersList",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeadersOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocketOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentModelConfigOutputReference",
    "VertexAiEndpointWithModelGardenDeploymentTimeouts",
    "VertexAiEndpointWithModelGardenDeploymentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c48ae63f271b6332a6896a67086dce4a13f91c775933b89a6516f21e916bedda(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    deploy_config: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentDeployConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoint_config: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentEndpointConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    hugging_face_model_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    model_config: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    publisher_model_name: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b3be9181eeaf51cdee0b9dab6cfb3486a290688223b0a2b9a43cf3e0ea13f1c5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb7416b80b46e12b794497361b8967966e4a34d448a486406ac88df2128c5773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c1cf2b533cb8a3c18ce7057b739665079a9485dbf4973dae012b9966b12f112(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52abc607155069c26b2a9342dfbe4ae4c29ab9fa1a3af3dd0dec427b520ebf9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85f48f599e12cae43489669f9dded6300d1713ab6701f9f9002130f7e81b4f16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5d4c5d46b156509493c2cc8c75d8861fe14b644ed08435fd9fe616e450e448(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36960e4dcb3c5d974fc4c7eeb506376c1b85011bee5698a4dfbd7bbf2214ce4c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    deploy_config: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentDeployConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoint_config: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentEndpointConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    hugging_face_model_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    model_config: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    publisher_model_name: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7113ecf351197087fb0c2b08300d9d1a9cce330beafce577d5a99f214511a0fa(
    *,
    dedicated_resources: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources, typing.Dict[builtins.str, typing.Any]]] = None,
    fast_tryout_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    system_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e85343fe99c4717ad67cbbf474893174f9bc4c88a7a16da3ae0b0f37816090(
    *,
    machine_spec: typing.Union[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec, typing.Dict[builtins.str, typing.Any]],
    min_replica_count: jsii.Number,
    autoscaling_metric_specs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max_replica_count: typing.Optional[jsii.Number] = None,
    required_replica_count: typing.Optional[jsii.Number] = None,
    spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20b8184ff8044b80f84cf0bfaa1032599512882a095867c7a6093d7a84fd6684(
    *,
    metric_name: builtins.str,
    target: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758f468b9368bd06a9983e7db386408f501dcd356b2b9b8e3444db7c1148103a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee14b09294fecdc9233927e3173e3872e00ef207ddfa7a528a9a84c91fef7806(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a54ee4fe1094acc4680df296376180800fd38e148b857756b722b2ce9820fd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8578aeb7ddf3aad6720b80c84f53df8b3121e8598eb66e9bcea9cc5ceeff5c3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bebd4ce710d3facf803ff0d08abbc273c54417e715243751a44dbf8dafe419b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f50d05e951e1c8d116b2fc8dcde3db707daaebac50be90c4537635e9a419c0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9778f0800b6db1650b6350b43be15d2cf9df580b59169466ef6e1fb7ccb91f51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e9ef6a63f9b9e29a436901547ba4bbfac5306286e9b0c63ff3d897d6ae04e6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__022a1f5e4ac51ef4bcca777b954066c1109ac5eb3f0507700b801c57f8b047f3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c316e51e67488c7fb657bb9be1d5a8dc751473ac264b7ebb07c1163849a7a529(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1c42768ccfea6927f131cffb250a1a640a390cf4f083630c2ef8abd728fbde(
    *,
    accelerator_count: typing.Optional[jsii.Number] = None,
    accelerator_type: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    multihost_gpu_node_count: typing.Optional[jsii.Number] = None,
    reservation_affinity: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
    tpu_topology: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b42a40888bb1608ed634c4a0bb1c27ad5a7f75bcfb14bd357ff0b6cd39e961(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ef697940600037754b8aec9885efc57466ec2743701f0cdefde85ed152f42ab(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__748e6ebf74d0be33136f1deb69d14d6aa8f8ff1e586b2191724fe55201fa98d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d2e10ad82fa9a3f7d6d00a18ab77953152019923036049c80d287d84aa8c0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a6e95760f8b2831e01576057fafa29e8dc267689aac81c636ed03cda44d55df(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a82726dd91be6517f06c07657a257eee205da2942bd0ad8b951f547df49af94b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4324e7a16c3f1c25fc6ae790504bc0cd16c93dad663d9d3007ca4ff938db28(
    value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7801dcc3ea0e34735644b00c4d807eb91fe7f1b482c17664d9f34023688184b3(
    *,
    reservation_affinity_type: builtins.str,
    key: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ded6a31cdbf5c3b4a15b6b2f7b9499824e63087fb5157f6cd1f89fa54736187(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32bcbb37106487628a25e29f0019e5f580b98da5a23d36a4447bcb64d2da7e33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c816c27b332b1823e6f5dd8830bc4066e0ca9599d01fce11a9f67de18b9cee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b4839e43afebd2714e3b2b7f56b5d1fa015cd16e36e1ca4ba455f34f2c734b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c54fcacff6bd731dda9c9313a402701887fa3c28bf9007b646a032b3689ba0b(
    value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesMachineSpecReservationAffinity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ce78a1468e7b20f80c65b1d6a5f4ecb14cee7a15f4339ff5f8212b5c81928e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39ab58fda269e42b43f579056ff51479489ab9ad93013e3181f5c1fa188477e6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResourcesAutoscalingMetricSpecs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0575e530580aeac9bbf07846d87b66327af19ee5f31b740764541e2ff329d8d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e7862a231e57b2a6496202ae050bbd59601edaa0398014395ade32447fb641d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaedb0c3700459f844282e8fc8da1ec8651e8e1856e679ab228aced1c2e4fe08(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6704c153404dad80e4c65f10810256be8aeb7e27b01fa728c1f726e4b7e2ddf6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6bce349bc382e23d6bca8126b32866295cff4e4a18ec7faa1b820b8b6f866b9(
    value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentDeployConfigDedicatedResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc57a4478653c0cad7aec3ab02ade017ebc4f452149d144ba790eb1569c8f29f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__295c0465e30e1b66f715f62be8fd23351c3364ce34fb06da4cb9afeb6680cc50(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0f4fbbc90c3d91b98489143e3515c55a4a7a7fb56b45d1dc435c4ab4fe99e98(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae99b3ccac870e9cf03ca659a16de3036206c62a453e422e7dbb6a194c621cb(
    value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentDeployConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__043914b0dcaff6ce69418fe4af0edcd6ecfc17137be31a05845ad4c3a8eec0d0(
    *,
    dedicated_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    endpoint_display_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d8edfb9a1cb35f769e7ecad862a8682613276d021e020b028397e418d522fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3141278eb2a9ff4bcdbeefaf880fbcbd839b858b2d828a59d1ba96d5e90b82f8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c74a891b23aa42223602f85b0ab2b6bd429082ae2d78456290c0f868a8117e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d83999933d5bd417b29509d4b53d3ce69a77ac999329ce6e725512c8697ff1a(
    value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentEndpointConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__203f85dcb75ecb19fd8f65f6fa1a6bde4750c795b7b90c18ee1f92bc05b359d5(
    *,
    accept_eula: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    container_spec: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    hugging_face_access_token: typing.Optional[builtins.str] = None,
    hugging_face_cache_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    model_display_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607ce6f922c84e3557c78b5636819968898033902c3dd84431a631fcf813f0d2(
    *,
    image_uri: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    deployment_timeout: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv, typing.Dict[builtins.str, typing.Any]]]]] = None,
    grpc_ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    health_probe: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe, typing.Dict[builtins.str, typing.Any]]] = None,
    health_route: typing.Optional[builtins.str] = None,
    liveness_probe: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe, typing.Dict[builtins.str, typing.Any]]] = None,
    ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    predict_route: typing.Optional[builtins.str] = None,
    shared_memory_size_mb: typing.Optional[builtins.str] = None,
    startup_probe: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf0c91b90f579945096c2f9eda1d3d20a1ebb133fa60e595621d62072561e93(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42baac13605807e174823cd86b99493838f4895fe966b61e9fdc81d3910663b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd10b1d076ac6a9e73ec634c541253f081cdc1b1c73da28b1b8e94a5c55146c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa696957bcf3c0775cf359d8706e03862578b2dd6fe43eb15e266b44dd10883d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f66c0a05bc29b933a1e891af50140a09cee1fb50edbc0c2f02c880e56bf6616b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e65b6db9991b105195137ab81784accdd8c59196aa72589d49acb4b8d192521(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9fa6b7d3d5728b65c52cff627b32a9cffb9ff87ec888427d21a0f9b7a61cf7b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5c6c0adad0361f35c55d08af9e83d750452268bbb8740be8409fa637e7daca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d08e9bbbc9ec4885be6aa148047f604330c6743cdcdfd2c60a9ffe067485a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c8dc61ff21c9ef92d2965f7e6187ce44eebba89a588a59e32812faa4ca99c87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c873bc6c88f783e1190a152bcc64858e8839a209665d65f0115e0f722aec81a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d61e6e0cbc5edd3d7fa6fedf6870d4ab6a911b9fb675714d88258fa88088efe0(
    *,
    container_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03e52929d74656579057026f3dc7f169e680a7ce5d192643dfed53d217b64e22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2832967345ac5e173e3101690a73a4af6942f6e1826037c3b2de8ac3a8da6b6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f26f7afcf2ec378f385960c0e7b7e01917f0dc1e6b529c2168ef30562b11e806(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63f0554200630bc18c03bea5fafd573db30da7e764c5bfa4d29cbe4055e4301e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7044a1a781c50072e7162ab0018a534b46d75faed38db717e46236c812b070a0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf8b0efbd7be6426f89490d2afbd75404667b06976bd7f970ba64360535b985d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc73dc000f5a5512b5cb38f50d79317333a8aa1f29ea4914ea521d62966aac6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b164667b14bc0439622a180a7dab00f2149b04239137643450ac65b7ce9f4a4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7763bfedb66c3e33f651ee4334ef6428a2e58911529c205077aa1f28b45471a2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__095710d75e6c2d6b1cdbc3daec87d29c4104864789067ff370067290fc851baf(
    *,
    exec: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec, typing.Dict[builtins.str, typing.Any]]] = None,
    failure_threshold: typing.Optional[jsii.Number] = None,
    grpc: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
    http_get: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
    initial_delay_seconds: typing.Optional[jsii.Number] = None,
    period_seconds: typing.Optional[jsii.Number] = None,
    success_threshold: typing.Optional[jsii.Number] = None,
    tcp_socket: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b08a8a80aed5084f11a3d9a4d2dd42653d2dd5599a40fdca08cd0287bd88af79(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96213e179f4f24d44957d9990169bd8b9087d7316d47bcf790c6fc3e95859768(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbbf03a17a06586a6e42170141ed8d05829c50c420f51326e660ef05520403ba(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb0376d459577f82ddd6fabb9bb2cf4e04df7e8fdfaa55182aa0ae47f2b78713(
    value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeExec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e85b4fb40ab9c0abc36357f4161c0982f858c23925050aab77b8133bd441ab6f(
    *,
    port: typing.Optional[jsii.Number] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5a6d27a1809179c1a088a490ae41f75beaa032f1a63cd250bebe0d35429262c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc9c48023496c50e69f7daff646e54ad76abd5e7e7740e85084c3b08178a47e2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb3c75bc835ee3bd578460f38de8da54f860b43d9f1abc93191b4e86dc03a93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67e917d4dc9f4be95af283c3c6c06e8d627cb3794500b639f85024eca67b0f46(
    value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeGrpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__229aef6951090a938696b3de4f8e5d1c92acc46b3666c8d1feeae171374480d4(
    *,
    host: typing.Optional[builtins.str] = None,
    http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    scheme: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba02b42b8e9784e47c37975481f51313ea8fcc96d004e583620a4dd09466f92(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c539b3ef3acb678895f320bda429309564eb443717bdae935a376508021b76e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5158ef6829fd35d88c087778aba53b7b39102b9a0fd907c5e701c09b5b160633(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93dcdd18f651d83a2ef452bf2b65127f8beed7785a15885e9f872847cd003e1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3366161c0b428e9d90658792082c5d24eb7a6d5e9283005cc739d519aea2cd6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea9e20b177e2c6976cadcfb5993ace4d13bd5ee52c73280f2fe071485e5334cd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab646f6471927ec79590595f4eb3e4d29bf3a5925804b43f87ab332dda48623(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b82b4f6a9f4d89a63b0eefb5c30d5a09c3d327090ab6318d5fcdbea35500b682(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33000b77219ee1193d45b9a4c3ed405f0a4d9e39af1307511064bcc5352ad972(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1285d21c88cb5939694046c35231b2a41461dbace352b7e181403be4a6726f0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e81513844c4f793e49c35aff13490f1d1177d49afe169f4416dbb6dc4c9a0f6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfcaa2c1be9590c76471bd57e0b1ff102025a3194d24d5e9f0bc6bb344fc5a7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd92bd1993f0b0866cff1b6519f3ef5f7ac760acb86ddbb922a1ee367b5687cb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac49ca58e149df6917495fa1b835fb6a543ea109ca1545f625dc3f6994a6643(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a84d2b84b7ac610b2e895cb4d6b2decb2089b6cd6eab4a25da34ae804e3ad984(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__367ea48602964f7fd82cc43e48ddd8f053ec5bfb31eb69d942fbf5fa2154e662(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__098407e19af0a19b1291e98198f2dd7fb9818fd75bc8306315899723c89d8d12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aed48db93091e4dac7d15a8a5e614ee438f1811342182b29cf30bdd2fd6a3b9(
    value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeHttpGet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e529c2159d0a7657076dbab2ba772e6565c459254a35b375ae317bab28c2259e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad5e62859fcec675cf6e116156298a81ff31d03b0e1e4624e9450adf23578d2a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__470e5865aef70fc536d5d94cae44c2eecfe78095d26fc01feeacbf82e80cbba5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18ef52c0a49f7ec17f936ddbabcb6fa298f5ff8a7759afaaaa343344cec652be(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1587f6de0367edd3643237345a8db726e1ec5a611dc680a0bd0b9350be8cb41(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f36eabe6316717480b3435cdecb1e19d24cd7cea84953251fca0c3120913d1fa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b011c4001c64c1c21b1d9fb339126e61594654f1da64b7211705dd4960b5a2(
    value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbe],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__253d1dca32393cf9dc66799bab9c451b912fcb93eef1449058d29e83e043ad16(
    *,
    host: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2194f50c09eb951ad88310f154399cb29781bf387db562c77a0d8822607ac7ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1734309bf4ded49e45491fa5634496caed997f3845943b4ab51d388be8d02a96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a5d8331d4f46c5021f9cd7e035062c59ce7afabac963f1c6cf61cf027124211(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86219665b21b30df9374d92581096e1aaa6b655b7eaee04d0026676a5889080d(
    value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecHealthProbeTcpSocket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0672bd51a65fc8c6d48993d05d498b287d7ae1df8a608fe1330ac040adc262(
    *,
    exec: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec, typing.Dict[builtins.str, typing.Any]]] = None,
    failure_threshold: typing.Optional[jsii.Number] = None,
    grpc: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
    http_get: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
    initial_delay_seconds: typing.Optional[jsii.Number] = None,
    period_seconds: typing.Optional[jsii.Number] = None,
    success_threshold: typing.Optional[jsii.Number] = None,
    tcp_socket: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16039a4d1af1bcbee10c6c5da5d3f4615f4b7f7b29fbed3acacf9f160e37a8ff(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394b6aadfccc10b0c1fc851c6bb127206460dfa32ef0c98c07e308ffb0488dee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57902bc7116e8964c49ddfea9bcf9ad85a56ed09991d97cd202dd74bdbc91ea6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5dc0c5a3803d7ab67e9aa99c807b691fbbc89012a11e08c4fb8505cec22be56(
    value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeExec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__921d4cda2ef983e9f30b4c11bb1b50bf4ee84555ac83a3db9ed0b028a7dba4c0(
    *,
    port: typing.Optional[jsii.Number] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc234d1341e1934bfc260ee0a75af10c2ff599d459ec4056ba044c2a3f384a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed9fcfa9ee76295549b1cded221549b17283a709149f564ba370e2fa3aac3997(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d7211d50e4a150c5675837bcc4b489f7c881b6d027d867540a559a810d5a0a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e803a0874b19be90eb606a5dc0ed8dc5a3378c4697d6efe9af5e6988e7a58f45(
    value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeGrpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bd598309c5c570bc1248955ec412fe75a849227a8ecd824031f47f3a60d2171(
    *,
    host: typing.Optional[builtins.str] = None,
    http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    scheme: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__215a26de43f911e643623c6621db3258f3564dd3a61b3a5c6833ccdcb2540474(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a2d1efe27062cdc530f0013ae3c7720d589a5103f2e3edf0653a1ef963c7da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aa4be1d8f6d8ef9487f1b9a5fe9274e281cb8e275e22dca2d724a7fe85ffa66(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b1d3af6a6ded3bbf8cbf13b40864feabd5f2407b8996edf23e86141d6414409(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1826f58163c92168e9af8fa378c2fceb020de4f40c290af5a04f7d84f4d0164(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9378df92f9a820041b45cd95c9799f10bd191f76f1c877023528179f567357a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ce5cfec9043b4eefc781126313be8a043ea5ecbf267a0264f944c8975fbe79(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6372c41b67558153d58a0197cfa8f5e4635081baf790e81b2b11be90fe28f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1cca7c14d0d57acabaa24d4a0d6eff50b562c706eff55bc07290c4c094166a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a785424d21dd4b3166ce863cf30b32cffbef77587d98dedf8c67795d015f213(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a829725fb0710c41abb55f7500b614aa8a9014d34e71e4bb9105fc09120e6dc4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58996a1be088c0545c27dffda11e57919846c552efb62d928e981991473af42d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08cf8b1046e8d2dca545e95256a944c9a05ca4ee09cae8a264a009a8575d3d7b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9692caa0f5e41631821d2ba30db23c9e35fe550ff006fc245be48a33ba3f7675(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76ebc33b7242caa9749d05d563573d9dd066ab0fe379f382eb4c092b1fe7dde1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0450ecf912e03b4b2781733729bcff912f56f1b410e5fb608c6534bdb28628f1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c74d5e5df0dd423d3936d6c0384271a844cc4d35fdf46e9ff7604509f751d1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dc393f665e2062b8379f19d53fddcca8639afdf8edceec76017d5e58f39b901(
    value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeHttpGet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cff813df31e2670269884be2ee591f17563927455f5404ce81070e923a3ff442(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3807f2af08e1b0ee70c0516feebc4fd75332c41c85ca38f6f318030c44b743c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e962249e6874b7c7a44155dfe265a69f8594ba01a26c370c917aae452e8523f3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62118daea7b345016aa2bcebcca408b9f82f07b01553b4ff7f5582964371c44e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2520bd2795afe6deb07f81c4eca583cd62f19866b7bd6a3ab05d04b81d39676(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__981dcbb8d5f6f944943859afb16a7348ecd8c429b825467db82af142410cad49(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b0e286ab228fb5f9e938ff1543cf5f3695569f6bbc688fa17bc6a02fc8d309(
    value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbe],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b0973de20f14d90d36c3145ab60a9173b9b44a43bf32d4ef91c96bca9e35e6b(
    *,
    host: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11005f3511ad32b4428f61cd2fbdb3ac3fed535cbe4157c476d9ca9de1acb7e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2263362774772b5f0e92efcaca82ed3e4c24bd3507fac95b1aa7eae5581b1f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47968a2062a157fb736daca900beb53c9f7d44782dd959d33ded51e80818ce5c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a12a99f2f2475e4edddbc52e70dbfd12c59ebd7e7dc3cacd969f7cb40e2386f4(
    value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecLivenessProbeTcpSocket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f244885973e2db911bddced4d1cef4eb3abcdf36beb06086181f6828f81bad45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04bcf0a419e56d8ad1c67124135cd25c2c118ff3b82bf3271981a000b6f87d79(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecEnv, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__259f672ee4dacd7a78e49b04205fbce9f3dee52cd073e56fb1802591168ca8ff(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecGrpcPorts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f10814f06bc318361e9d7cf24a6df1de1a6a2b13d922956e8dc6a0f6e8f4fd7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a58fe3759bf7af0f0bd274b0919caa833e073eb07a28554823987566006217(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3457ce077fa04cacb8035d4ee5d24ae02ad8f98e91649255fb4bb3f4edd67ee9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb60c4c975dd63335876b8d76b7acdc67c96c7a6596dd7a76c3dfc993d0e5b3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96222a75417b4be8ebd4bc4dc8d0d25f32ee9950db858da6044fd073cffa407(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e65f31416d0358fc8cbeaf67b41c1f1987089736e3a9208f822b4b1314c62497(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced18594d446b10678bc7e2c1df8348ebe35017851b7abda11e449b7d726567c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__188d0201644ab9d5a31e95eed7fb62330756d5a8a4473977cf9e464ff4856769(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e6c67ca86da7c186a9715377876339b39b9c264809d2c9a391435312019d711(
    value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c674d93fd60fdd87b212c1e3b33671442606c684a0a14095b0b0d8cf5c0018c0(
    *,
    container_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f9a3b7a1f427050c87dc6218b5d96b61bcffc6e71b27a07986f3199a863f259(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03bde5818b28845842816b9577fb82c22cb24a4ba34f584b2164b7bc6d926a89(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee1aa37a8d6dc67787ab33ae3c0a455773ce5a13ff81a5a10e690c0de0d3c445(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83bb131e54b9d0b7d04e77efa579f5e92903d0c1c10fa9793c92f318cbce8abc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30565a852c0b1067f6c4cfdfd41e53658a7b52d90362798f397cbc6b3a348a8a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a713f637d271554def982e54ee4eb2a122b0342036b5b35feb35a18dd5cd3046(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25e67db759a40ad771c11e83259f1034e48a896419e658e44f1d4593ae57c928(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5762e93dadba44af3e87d0b5a5f10a44c98bbb4176a9e0281dd53537a7ef82f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38412be91a48ef078536d08e2c2b0d9eace0b1a3e5d76fb7e1678bfbc3ba22e7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecPorts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c864151a1132dd01495331e0c5a5d5266ea2f555a2fca5a9f273914064af297(
    *,
    exec: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec, typing.Dict[builtins.str, typing.Any]]] = None,
    failure_threshold: typing.Optional[jsii.Number] = None,
    grpc: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
    http_get: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
    initial_delay_seconds: typing.Optional[jsii.Number] = None,
    period_seconds: typing.Optional[jsii.Number] = None,
    success_threshold: typing.Optional[jsii.Number] = None,
    tcp_socket: typing.Optional[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37eab2fa8d200ee8b91bd9853f64ca59febdb755366c6e34b98585d2dda39ee5(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9ef8352bdf02bc09569f0f6d1ccaff29780b98e90f0638e1bc6fa0507306a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a244dc9413af6843a9cfdd7ebf66dbe72bf196fdd2fcdb2dbc42fadf91adea39(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45bf65c20bc7c3e8dd19a934f676f8e72df227eb4257bd725725f0d07c56947(
    value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeExec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df0362256ce602963133edd92c09a7dba6cd466ca2daad3f9bdea846c73f2664(
    *,
    port: typing.Optional[jsii.Number] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8da0d57cf90c5901bb20f001430cf61fe058e1c25f51c2752dcd41a8914748e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aefebfb310c5d8a35c6192a775d26e743f032951a5adf4c052514c975cab4ae(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3bf1cfb786f8fd14283187546fab48f34ebd020c2e740f27687208a6501ae9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b941d3de84e43d7ad189c95a2e8297261e5cfff21d1d3198530f8e153b19751(
    value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeGrpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa9a3047f73d82af7f4971db4f874132dbbd32dc2b98db2d503d7f838220674(
    *,
    host: typing.Optional[builtins.str] = None,
    http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    scheme: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf75512372bb28ce035dc026e2f8af657401b9605aa7935fa7d833d556ee61d(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae0fe1aa2e19ae3d95d0a267012dd1a0334fe1044e013788e91a68fbaaaa075b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e5c42d69982a58ce4afd3b7c6aa37af1727bf40e52d7d85211a3cf5f5c0d851(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e95f518e9aa42354dcd34d67091a6f5e1178b926cde1947163888627444672c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8712c7f988b5867bc742c0a78a4c838bf14b9e856e266828872ea9342942c113(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c80d795a2821e071e6d268ae6e2b2f5fff233e35625e5b71081995cdd34ed4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572911429ec1b292a3b46bd7dc650203952fadfcc2aac38cea97f4f0555ce412(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbc269ed3ca9e94b0e470e6cd58d165b1b40317d87c174266e268e27812a815e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df3507df041a7a7b1dc999a9252880deffd4697c0dd385ff131a3e8a4232363b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c006b973b4eed46804053a358dfe744bd782856eb1606c6e44a9ccb31e1373(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__223daf2d1a022b46d6c3f087820ed5a4c28164030d94922f8b5e013af4f846dd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03d104108a9bc521507d2dee8935cc2a34fbc36914e85167bac28fb413e8fa35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21a9de8aebf516d52f2863a52ba80da3de15668220876d03f02d7126e85b242(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28a29c61f159b6109c78e6791e0d45bcdee6e88629c6f12df5d4e7c1a4fe15f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f8f8c6c051e8eb52591e25dbf64b380d354d0a0819bbb0e4daddec5966b087(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31e50414528a4b5f385c874e623f4bd0a29e27419b23be5ea5f6ae949dd6461(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97cf7c42c2286a3180a09b8c5a9206a1c49d6ab440fbda99c9d25d2d49ecf0ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea981630d424ef6049027ae17638dcc9605c7a4bce710d1b68c737a93d5847d6(
    value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeHttpGet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__152374bb07ddcc764658647f831a4325b8ac85c1af405d3a39d6f65fd0148708(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a8f2c3e154b987cf0bc567fdc8151ca2538f4408ebd4cbd57ab5803391d6f58(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a6c0e6bdbb0e87ebf7582dc69737dcebd608ef42a71fbf5041a47a992f5a0a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f88e7d59833b0e84ad0a6ee1f2588b574150e82484cd195b81f474d7c9f70c0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b5b7fa51794406b72e79a223126fec9f293fa0bf1fddc700321e8c52b2a013b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79c2769b64c683fe9bb24340c9e0194e8997ac3ccc36b5148dab9efdefe44430(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dd2707a36afb077957fc2e311c78fea8be6331147cd90dda40dc0b96ed9704d(
    value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbe],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c145f6a8a3ec7736ff1d0cbaaec1d7ca56324c2666a4c16eb771a416e5a12ac(
    *,
    host: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4daaee9c5363932b8e580817149d10f64ccb8efa902f9bcf31839a45b603d09e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffb5a6cb3bd0c9ad6afb8409b66b8eff68d84a83591c4b3f69ea75cf40551ebe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__500c39ab55e9e8f21b9e0126675bec6524e3d71809d2e59da754d21633adc5ac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38597d1fa1ef34c517fa5c9e5da119977b3fc3713e7465883ac004400a304804(
    value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfigContainerSpecStartupProbeTcpSocket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41979b55d1205da09e2ea5c0cc39c1a82bb1b0c9058529a6a2d6f8cee2d51254(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e889498768977c35c1363af0ef829d9aa6ae1b2db3c3af59b2bf08f9ff825405(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a85c7646ed6f50c390223d474b7e6b31abb114b2e8e942075bca17528f50619(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd91eacaac6ce507522d13acd13b387a1640ff67ca1eb728ba395e1a8ca23055(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66d12c8e408617d5aaef4f032b604506c59d054b2b102ad550c9410580aef811(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05838c2d8423cc32020212536ad085ba0d1292e53d8e6b496463be536493a121(
    value: typing.Optional[VertexAiEndpointWithModelGardenDeploymentModelConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fef62f77816edc18865030ac2ead253b05c924479d74d94023bd036034a8de7b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c77ab4f5d3a24c29e8c6d6a89d62fe846c4f3c1aed59b08aeb2a251f8fbf6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c02149a80a5161ee64b3c0c9a171c4eefbaba7e4b5b6daf985255385a1bbaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04eee4d6736e6643d0e52a03477129ef81520351e1bbe898d4968acc7bad3ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe9f9d2552fa89ea51c16a743ac0503190f688b8d5b70b511d189d2e14986f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointWithModelGardenDeploymentTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
