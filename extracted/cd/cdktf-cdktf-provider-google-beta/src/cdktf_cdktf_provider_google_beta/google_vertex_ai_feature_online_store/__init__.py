r'''
# `google_vertex_ai_feature_online_store`

Refer to the Terraform Registry for docs: [`google_vertex_ai_feature_online_store`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store).
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


class GoogleVertexAiFeatureOnlineStore(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStore.GoogleVertexAiFeatureOnlineStore",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store google_vertex_ai_feature_online_store}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        bigtable: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreBigtable", typing.Dict[builtins.str, typing.Any]]] = None,
        dedicated_serving_endpoint: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        embedding_management: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreEmbeddingManagement", typing.Dict[builtins.str, typing.Any]]] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        optimized: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreOptimized", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store google_vertex_ai_feature_online_store} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The resource name of the Feature Online Store. This value may be up to 60 characters, and valid characters are [a-z0-9_]. The first character cannot be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#name GoogleVertexAiFeatureOnlineStore#name}
        :param bigtable: bigtable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#bigtable GoogleVertexAiFeatureOnlineStore#bigtable}
        :param dedicated_serving_endpoint: dedicated_serving_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#dedicated_serving_endpoint GoogleVertexAiFeatureOnlineStore#dedicated_serving_endpoint}
        :param embedding_management: embedding_management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#embedding_management GoogleVertexAiFeatureOnlineStore#embedding_management}
        :param force_destroy: If set to true, any FeatureViews and Features for this FeatureOnlineStore will also be deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#force_destroy GoogleVertexAiFeatureOnlineStore#force_destroy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#id GoogleVertexAiFeatureOnlineStore#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels with user-defined metadata to organize your feature online stores. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#labels GoogleVertexAiFeatureOnlineStore#labels}
        :param optimized: optimized block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#optimized GoogleVertexAiFeatureOnlineStore#optimized}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#project GoogleVertexAiFeatureOnlineStore#project}.
        :param region: The region of feature online store. eg us-central1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#region GoogleVertexAiFeatureOnlineStore#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#timeouts GoogleVertexAiFeatureOnlineStore#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9cb8c07117ae66ea4f976534ee61374bc8ab214581191288fe6801fc6a84d6a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleVertexAiFeatureOnlineStoreConfig(
            name=name,
            bigtable=bigtable,
            dedicated_serving_endpoint=dedicated_serving_endpoint,
            embedding_management=embedding_management,
            force_destroy=force_destroy,
            id=id,
            labels=labels,
            optimized=optimized,
            project=project,
            region=region,
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
        '''Generates CDKTF code for importing a GoogleVertexAiFeatureOnlineStore resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleVertexAiFeatureOnlineStore to import.
        :param import_from_id: The id of the existing GoogleVertexAiFeatureOnlineStore that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleVertexAiFeatureOnlineStore to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d64077d894894b8d23dda0648675f32462371fc8912521dd9458f4752b94b4a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBigtable")
    def put_bigtable(
        self,
        *,
        auto_scaling: typing.Union["GoogleVertexAiFeatureOnlineStoreBigtableAutoScaling", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param auto_scaling: auto_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#auto_scaling GoogleVertexAiFeatureOnlineStore#auto_scaling}
        '''
        value = GoogleVertexAiFeatureOnlineStoreBigtable(auto_scaling=auto_scaling)

        return typing.cast(None, jsii.invoke(self, "putBigtable", [value]))

    @jsii.member(jsii_name="putDedicatedServingEndpoint")
    def put_dedicated_serving_endpoint(
        self,
        *,
        private_service_connect_config: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param private_service_connect_config: private_service_connect_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#private_service_connect_config GoogleVertexAiFeatureOnlineStore#private_service_connect_config}
        '''
        value = GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpoint(
            private_service_connect_config=private_service_connect_config
        )

        return typing.cast(None, jsii.invoke(self, "putDedicatedServingEndpoint", [value]))

    @jsii.member(jsii_name="putEmbeddingManagement")
    def put_embedding_management(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Enable embedding management. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#enabled GoogleVertexAiFeatureOnlineStore#enabled}
        '''
        value = GoogleVertexAiFeatureOnlineStoreEmbeddingManagement(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putEmbeddingManagement", [value]))

    @jsii.member(jsii_name="putOptimized")
    def put_optimized(self) -> None:
        value = GoogleVertexAiFeatureOnlineStoreOptimized()

        return typing.cast(None, jsii.invoke(self, "putOptimized", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#create GoogleVertexAiFeatureOnlineStore#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#delete GoogleVertexAiFeatureOnlineStore#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#update GoogleVertexAiFeatureOnlineStore#update}.
        '''
        value = GoogleVertexAiFeatureOnlineStoreTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBigtable")
    def reset_bigtable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigtable", []))

    @jsii.member(jsii_name="resetDedicatedServingEndpoint")
    def reset_dedicated_serving_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDedicatedServingEndpoint", []))

    @jsii.member(jsii_name="resetEmbeddingManagement")
    def reset_embedding_management(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmbeddingManagement", []))

    @jsii.member(jsii_name="resetForceDestroy")
    def reset_force_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceDestroy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetOptimized")
    def reset_optimized(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptimized", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    @jsii.member(jsii_name="bigtable")
    def bigtable(self) -> "GoogleVertexAiFeatureOnlineStoreBigtableOutputReference":
        return typing.cast("GoogleVertexAiFeatureOnlineStoreBigtableOutputReference", jsii.get(self, "bigtable"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedServingEndpoint")
    def dedicated_serving_endpoint(
        self,
    ) -> "GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointOutputReference":
        return typing.cast("GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointOutputReference", jsii.get(self, "dedicatedServingEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="embeddingManagement")
    def embedding_management(
        self,
    ) -> "GoogleVertexAiFeatureOnlineStoreEmbeddingManagementOutputReference":
        return typing.cast("GoogleVertexAiFeatureOnlineStoreEmbeddingManagementOutputReference", jsii.get(self, "embeddingManagement"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="optimized")
    def optimized(self) -> "GoogleVertexAiFeatureOnlineStoreOptimizedOutputReference":
        return typing.cast("GoogleVertexAiFeatureOnlineStoreOptimizedOutputReference", jsii.get(self, "optimized"))

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
    def timeouts(self) -> "GoogleVertexAiFeatureOnlineStoreTimeoutsOutputReference":
        return typing.cast("GoogleVertexAiFeatureOnlineStoreTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="bigtableInput")
    def bigtable_input(
        self,
    ) -> typing.Optional["GoogleVertexAiFeatureOnlineStoreBigtable"]:
        return typing.cast(typing.Optional["GoogleVertexAiFeatureOnlineStoreBigtable"], jsii.get(self, "bigtableInput"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedServingEndpointInput")
    def dedicated_serving_endpoint_input(
        self,
    ) -> typing.Optional["GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpoint"]:
        return typing.cast(typing.Optional["GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpoint"], jsii.get(self, "dedicatedServingEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="embeddingManagementInput")
    def embedding_management_input(
        self,
    ) -> typing.Optional["GoogleVertexAiFeatureOnlineStoreEmbeddingManagement"]:
        return typing.cast(typing.Optional["GoogleVertexAiFeatureOnlineStoreEmbeddingManagement"], jsii.get(self, "embeddingManagementInput"))

    @builtins.property
    @jsii.member(jsii_name="forceDestroyInput")
    def force_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="optimizedInput")
    def optimized_input(
        self,
    ) -> typing.Optional["GoogleVertexAiFeatureOnlineStoreOptimized"]:
        return typing.cast(typing.Optional["GoogleVertexAiFeatureOnlineStoreOptimized"], jsii.get(self, "optimizedInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleVertexAiFeatureOnlineStoreTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleVertexAiFeatureOnlineStoreTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="forceDestroy")
    def force_destroy(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceDestroy"))

    @force_destroy.setter
    def force_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1146465c1019537ac1b07e068e4be54970b29a291aab5d800a2ce1e1d023a4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18820187d8ee08e473ce519d0bb522fa61748abb148fb4d7e33fe125d5b4e598)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a54604b722d6858f8e2c4c6200d34bc12fcbd4e288ad236e79243bc3131ad239)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c186b4857159387ac4ef8c492aa468dafd515829e5ac76124c2789ba71099e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b4775ea50a299e2d441ccde4a2e356a6b83b3f5fb6fe912c985d862711f9c50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b57dceeb601f954f87d1c7a749f4d54e4e33732bac4d77ec399ab31762e227a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStore.GoogleVertexAiFeatureOnlineStoreBigtable",
    jsii_struct_bases=[],
    name_mapping={"auto_scaling": "autoScaling"},
)
class GoogleVertexAiFeatureOnlineStoreBigtable:
    def __init__(
        self,
        *,
        auto_scaling: typing.Union["GoogleVertexAiFeatureOnlineStoreBigtableAutoScaling", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param auto_scaling: auto_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#auto_scaling GoogleVertexAiFeatureOnlineStore#auto_scaling}
        '''
        if isinstance(auto_scaling, dict):
            auto_scaling = GoogleVertexAiFeatureOnlineStoreBigtableAutoScaling(**auto_scaling)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__349994520e9f8b2db27dcd5edeae165c04a1c91f1080cc04e6724de272228fba)
            check_type(argname="argument auto_scaling", value=auto_scaling, expected_type=type_hints["auto_scaling"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auto_scaling": auto_scaling,
        }

    @builtins.property
    def auto_scaling(self) -> "GoogleVertexAiFeatureOnlineStoreBigtableAutoScaling":
        '''auto_scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#auto_scaling GoogleVertexAiFeatureOnlineStore#auto_scaling}
        '''
        result = self._values.get("auto_scaling")
        assert result is not None, "Required property 'auto_scaling' is missing"
        return typing.cast("GoogleVertexAiFeatureOnlineStoreBigtableAutoScaling", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeatureOnlineStoreBigtable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStore.GoogleVertexAiFeatureOnlineStoreBigtableAutoScaling",
    jsii_struct_bases=[],
    name_mapping={
        "max_node_count": "maxNodeCount",
        "min_node_count": "minNodeCount",
        "cpu_utilization_target": "cpuUtilizationTarget",
    },
)
class GoogleVertexAiFeatureOnlineStoreBigtableAutoScaling:
    def __init__(
        self,
        *,
        max_node_count: jsii.Number,
        min_node_count: jsii.Number,
        cpu_utilization_target: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_node_count: The maximum number of nodes to scale up to. Must be greater than or equal to minNodeCount, and less than or equal to 10 times of 'minNodeCount'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#max_node_count GoogleVertexAiFeatureOnlineStore#max_node_count}
        :param min_node_count: The minimum number of nodes to scale down to. Must be greater than or equal to 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#min_node_count GoogleVertexAiFeatureOnlineStore#min_node_count}
        :param cpu_utilization_target: A percentage of the cluster's CPU capacity. Can be from 10% to 80%. When a cluster's CPU utilization exceeds the target that you have set, Bigtable immediately adds nodes to the cluster. When CPU utilization is substantially lower than the target, Bigtable removes nodes. If not set will default to 50%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#cpu_utilization_target GoogleVertexAiFeatureOnlineStore#cpu_utilization_target}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35fedbaf461a1dda3d7bfe04e89230fe4c33846dc0ed045d3745e7c9422a4d93)
            check_type(argname="argument max_node_count", value=max_node_count, expected_type=type_hints["max_node_count"])
            check_type(argname="argument min_node_count", value=min_node_count, expected_type=type_hints["min_node_count"])
            check_type(argname="argument cpu_utilization_target", value=cpu_utilization_target, expected_type=type_hints["cpu_utilization_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_node_count": max_node_count,
            "min_node_count": min_node_count,
        }
        if cpu_utilization_target is not None:
            self._values["cpu_utilization_target"] = cpu_utilization_target

    @builtins.property
    def max_node_count(self) -> jsii.Number:
        '''The maximum number of nodes to scale up to.

        Must be greater than or equal to minNodeCount, and less than or equal to 10 times of 'minNodeCount'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#max_node_count GoogleVertexAiFeatureOnlineStore#max_node_count}
        '''
        result = self._values.get("max_node_count")
        assert result is not None, "Required property 'max_node_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_node_count(self) -> jsii.Number:
        '''The minimum number of nodes to scale down to. Must be greater than or equal to 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#min_node_count GoogleVertexAiFeatureOnlineStore#min_node_count}
        '''
        result = self._values.get("min_node_count")
        assert result is not None, "Required property 'min_node_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def cpu_utilization_target(self) -> typing.Optional[jsii.Number]:
        '''A percentage of the cluster's CPU capacity.

        Can be from 10% to 80%. When a cluster's CPU utilization exceeds the target that you have set, Bigtable immediately adds nodes to the cluster. When CPU utilization is substantially lower than the target, Bigtable removes nodes. If not set will default to 50%.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#cpu_utilization_target GoogleVertexAiFeatureOnlineStore#cpu_utilization_target}
        '''
        result = self._values.get("cpu_utilization_target")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeatureOnlineStoreBigtableAutoScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiFeatureOnlineStoreBigtableAutoScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStore.GoogleVertexAiFeatureOnlineStoreBigtableAutoScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c812c964774d880609fbf60744897e67dc0dd36d7c16da491a89cad71b290a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCpuUtilizationTarget")
    def reset_cpu_utilization_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuUtilizationTarget", []))

    @builtins.property
    @jsii.member(jsii_name="cpuUtilizationTargetInput")
    def cpu_utilization_target_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuUtilizationTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="maxNodeCountInput")
    def max_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minNodeCountInput")
    def min_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuUtilizationTarget")
    def cpu_utilization_target(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuUtilizationTarget"))

    @cpu_utilization_target.setter
    def cpu_utilization_target(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0459fa4511f522e82b422a7a11968446032ec5defdff3081001d598079b5617f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuUtilizationTarget", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxNodeCount")
    def max_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxNodeCount"))

    @max_node_count.setter
    def max_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__999726ea57ad61a222c8474ba85cfe815e380ffe3be82279e9e77246fb955998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodeCount")
    def min_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNodeCount"))

    @min_node_count.setter
    def min_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6d40a58045cab68707445fbc086d2e514b16bba7bd53c4b2cc919f29946b232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiFeatureOnlineStoreBigtableAutoScaling]:
        return typing.cast(typing.Optional[GoogleVertexAiFeatureOnlineStoreBigtableAutoScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiFeatureOnlineStoreBigtableAutoScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf23c12e0ac0c1db7c026b11c57a006dee14db7fee2774d1dc82de0d04f128a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiFeatureOnlineStoreBigtableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStore.GoogleVertexAiFeatureOnlineStoreBigtableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b506d8f6f38ab51337c0058571afe58dbda7132865efdd71a85718f5b4148f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoScaling")
    def put_auto_scaling(
        self,
        *,
        max_node_count: jsii.Number,
        min_node_count: jsii.Number,
        cpu_utilization_target: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_node_count: The maximum number of nodes to scale up to. Must be greater than or equal to minNodeCount, and less than or equal to 10 times of 'minNodeCount'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#max_node_count GoogleVertexAiFeatureOnlineStore#max_node_count}
        :param min_node_count: The minimum number of nodes to scale down to. Must be greater than or equal to 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#min_node_count GoogleVertexAiFeatureOnlineStore#min_node_count}
        :param cpu_utilization_target: A percentage of the cluster's CPU capacity. Can be from 10% to 80%. When a cluster's CPU utilization exceeds the target that you have set, Bigtable immediately adds nodes to the cluster. When CPU utilization is substantially lower than the target, Bigtable removes nodes. If not set will default to 50%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#cpu_utilization_target GoogleVertexAiFeatureOnlineStore#cpu_utilization_target}
        '''
        value = GoogleVertexAiFeatureOnlineStoreBigtableAutoScaling(
            max_node_count=max_node_count,
            min_node_count=min_node_count,
            cpu_utilization_target=cpu_utilization_target,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoScaling", [value]))

    @builtins.property
    @jsii.member(jsii_name="autoScaling")
    def auto_scaling(
        self,
    ) -> GoogleVertexAiFeatureOnlineStoreBigtableAutoScalingOutputReference:
        return typing.cast(GoogleVertexAiFeatureOnlineStoreBigtableAutoScalingOutputReference, jsii.get(self, "autoScaling"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingInput")
    def auto_scaling_input(
        self,
    ) -> typing.Optional[GoogleVertexAiFeatureOnlineStoreBigtableAutoScaling]:
        return typing.cast(typing.Optional[GoogleVertexAiFeatureOnlineStoreBigtableAutoScaling], jsii.get(self, "autoScalingInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiFeatureOnlineStoreBigtable]:
        return typing.cast(typing.Optional[GoogleVertexAiFeatureOnlineStoreBigtable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiFeatureOnlineStoreBigtable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c778dfe68b297c3cb16f4b2a13c6bb24c6da5ecabc702bf51062ecd963f246c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStore.GoogleVertexAiFeatureOnlineStoreConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "bigtable": "bigtable",
        "dedicated_serving_endpoint": "dedicatedServingEndpoint",
        "embedding_management": "embeddingManagement",
        "force_destroy": "forceDestroy",
        "id": "id",
        "labels": "labels",
        "optimized": "optimized",
        "project": "project",
        "region": "region",
        "timeouts": "timeouts",
    },
)
class GoogleVertexAiFeatureOnlineStoreConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        bigtable: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreBigtable, typing.Dict[builtins.str, typing.Any]]] = None,
        dedicated_serving_endpoint: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        embedding_management: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreEmbeddingManagement", typing.Dict[builtins.str, typing.Any]]] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        optimized: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreOptimized", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The resource name of the Feature Online Store. This value may be up to 60 characters, and valid characters are [a-z0-9_]. The first character cannot be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#name GoogleVertexAiFeatureOnlineStore#name}
        :param bigtable: bigtable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#bigtable GoogleVertexAiFeatureOnlineStore#bigtable}
        :param dedicated_serving_endpoint: dedicated_serving_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#dedicated_serving_endpoint GoogleVertexAiFeatureOnlineStore#dedicated_serving_endpoint}
        :param embedding_management: embedding_management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#embedding_management GoogleVertexAiFeatureOnlineStore#embedding_management}
        :param force_destroy: If set to true, any FeatureViews and Features for this FeatureOnlineStore will also be deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#force_destroy GoogleVertexAiFeatureOnlineStore#force_destroy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#id GoogleVertexAiFeatureOnlineStore#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels with user-defined metadata to organize your feature online stores. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#labels GoogleVertexAiFeatureOnlineStore#labels}
        :param optimized: optimized block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#optimized GoogleVertexAiFeatureOnlineStore#optimized}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#project GoogleVertexAiFeatureOnlineStore#project}.
        :param region: The region of feature online store. eg us-central1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#region GoogleVertexAiFeatureOnlineStore#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#timeouts GoogleVertexAiFeatureOnlineStore#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bigtable, dict):
            bigtable = GoogleVertexAiFeatureOnlineStoreBigtable(**bigtable)
        if isinstance(dedicated_serving_endpoint, dict):
            dedicated_serving_endpoint = GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpoint(**dedicated_serving_endpoint)
        if isinstance(embedding_management, dict):
            embedding_management = GoogleVertexAiFeatureOnlineStoreEmbeddingManagement(**embedding_management)
        if isinstance(optimized, dict):
            optimized = GoogleVertexAiFeatureOnlineStoreOptimized(**optimized)
        if isinstance(timeouts, dict):
            timeouts = GoogleVertexAiFeatureOnlineStoreTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6614077e66ff9fd057c37e56bc045095c0e1752afe8b94662ad13aca0622175)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument bigtable", value=bigtable, expected_type=type_hints["bigtable"])
            check_type(argname="argument dedicated_serving_endpoint", value=dedicated_serving_endpoint, expected_type=type_hints["dedicated_serving_endpoint"])
            check_type(argname="argument embedding_management", value=embedding_management, expected_type=type_hints["embedding_management"])
            check_type(argname="argument force_destroy", value=force_destroy, expected_type=type_hints["force_destroy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument optimized", value=optimized, expected_type=type_hints["optimized"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
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
        if bigtable is not None:
            self._values["bigtable"] = bigtable
        if dedicated_serving_endpoint is not None:
            self._values["dedicated_serving_endpoint"] = dedicated_serving_endpoint
        if embedding_management is not None:
            self._values["embedding_management"] = embedding_management
        if force_destroy is not None:
            self._values["force_destroy"] = force_destroy
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if optimized is not None:
            self._values["optimized"] = optimized
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
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
    def name(self) -> builtins.str:
        '''The resource name of the Feature Online Store.

        This value may be up to 60 characters, and valid characters are [a-z0-9_]. The first character cannot be a number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#name GoogleVertexAiFeatureOnlineStore#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bigtable(self) -> typing.Optional[GoogleVertexAiFeatureOnlineStoreBigtable]:
        '''bigtable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#bigtable GoogleVertexAiFeatureOnlineStore#bigtable}
        '''
        result = self._values.get("bigtable")
        return typing.cast(typing.Optional[GoogleVertexAiFeatureOnlineStoreBigtable], result)

    @builtins.property
    def dedicated_serving_endpoint(
        self,
    ) -> typing.Optional["GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpoint"]:
        '''dedicated_serving_endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#dedicated_serving_endpoint GoogleVertexAiFeatureOnlineStore#dedicated_serving_endpoint}
        '''
        result = self._values.get("dedicated_serving_endpoint")
        return typing.cast(typing.Optional["GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpoint"], result)

    @builtins.property
    def embedding_management(
        self,
    ) -> typing.Optional["GoogleVertexAiFeatureOnlineStoreEmbeddingManagement"]:
        '''embedding_management block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#embedding_management GoogleVertexAiFeatureOnlineStore#embedding_management}
        '''
        result = self._values.get("embedding_management")
        return typing.cast(typing.Optional["GoogleVertexAiFeatureOnlineStoreEmbeddingManagement"], result)

    @builtins.property
    def force_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, any FeatureViews and Features for this FeatureOnlineStore will also be deleted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#force_destroy GoogleVertexAiFeatureOnlineStore#force_destroy}
        '''
        result = self._values.get("force_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#id GoogleVertexAiFeatureOnlineStore#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The labels with user-defined metadata to organize your feature online stores.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#labels GoogleVertexAiFeatureOnlineStore#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def optimized(self) -> typing.Optional["GoogleVertexAiFeatureOnlineStoreOptimized"]:
        '''optimized block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#optimized GoogleVertexAiFeatureOnlineStore#optimized}
        '''
        result = self._values.get("optimized")
        return typing.cast(typing.Optional["GoogleVertexAiFeatureOnlineStoreOptimized"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#project GoogleVertexAiFeatureOnlineStore#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of feature online store. eg us-central1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#region GoogleVertexAiFeatureOnlineStore#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleVertexAiFeatureOnlineStoreTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#timeouts GoogleVertexAiFeatureOnlineStore#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleVertexAiFeatureOnlineStoreTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeatureOnlineStoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStore.GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpoint",
    jsii_struct_bases=[],
    name_mapping={"private_service_connect_config": "privateServiceConnectConfig"},
)
class GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpoint:
    def __init__(
        self,
        *,
        private_service_connect_config: typing.Optional[typing.Union["GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param private_service_connect_config: private_service_connect_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#private_service_connect_config GoogleVertexAiFeatureOnlineStore#private_service_connect_config}
        '''
        if isinstance(private_service_connect_config, dict):
            private_service_connect_config = GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig(**private_service_connect_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39f343c0d1611481a41437239d4e4c115f4d0949f564aa1c7a2e9d092831984b)
            check_type(argname="argument private_service_connect_config", value=private_service_connect_config, expected_type=type_hints["private_service_connect_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if private_service_connect_config is not None:
            self._values["private_service_connect_config"] = private_service_connect_config

    @builtins.property
    def private_service_connect_config(
        self,
    ) -> typing.Optional["GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig"]:
        '''private_service_connect_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#private_service_connect_config GoogleVertexAiFeatureOnlineStore#private_service_connect_config}
        '''
        result = self._values.get("private_service_connect_config")
        return typing.cast(typing.Optional["GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStore.GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f39a078126000e601eda38e2683aec3fed1c96a4cd36c801270a23736e30251f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPrivateServiceConnectConfig")
    def put_private_service_connect_config(
        self,
        *,
        enable_private_service_connect: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        project_allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enable_private_service_connect: If set to true, customers will use private service connection to send request. Otherwise, the connection will set to public endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#enable_private_service_connect GoogleVertexAiFeatureOnlineStore#enable_private_service_connect}
        :param project_allowlist: A list of Projects from which the forwarding rule will target the service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#project_allowlist GoogleVertexAiFeatureOnlineStore#project_allowlist}
        '''
        value = GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig(
            enable_private_service_connect=enable_private_service_connect,
            project_allowlist=project_allowlist,
        )

        return typing.cast(None, jsii.invoke(self, "putPrivateServiceConnectConfig", [value]))

    @jsii.member(jsii_name="resetPrivateServiceConnectConfig")
    def reset_private_service_connect_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateServiceConnectConfig", []))

    @builtins.property
    @jsii.member(jsii_name="privateServiceConnectConfig")
    def private_service_connect_config(
        self,
    ) -> "GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfigOutputReference":
        return typing.cast("GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfigOutputReference", jsii.get(self, "privateServiceConnectConfig"))

    @builtins.property
    @jsii.member(jsii_name="publicEndpointDomainName")
    def public_endpoint_domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicEndpointDomainName"))

    @builtins.property
    @jsii.member(jsii_name="serviceAttachment")
    def service_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAttachment"))

    @builtins.property
    @jsii.member(jsii_name="privateServiceConnectConfigInput")
    def private_service_connect_config_input(
        self,
    ) -> typing.Optional["GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig"]:
        return typing.cast(typing.Optional["GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig"], jsii.get(self, "privateServiceConnectConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpoint]:
        return typing.cast(typing.Optional[GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__515efeb57025bc646d72ce82aff95219eea112284fc4a99cc4fd4e314b62d0a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStore.GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_private_service_connect": "enablePrivateServiceConnect",
        "project_allowlist": "projectAllowlist",
    },
)
class GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig:
    def __init__(
        self,
        *,
        enable_private_service_connect: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        project_allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enable_private_service_connect: If set to true, customers will use private service connection to send request. Otherwise, the connection will set to public endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#enable_private_service_connect GoogleVertexAiFeatureOnlineStore#enable_private_service_connect}
        :param project_allowlist: A list of Projects from which the forwarding rule will target the service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#project_allowlist GoogleVertexAiFeatureOnlineStore#project_allowlist}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a66ed49bdb0fa78ab52280a866cfd7e3adac296b2080bfb75e8ce222f54cfb8)
            check_type(argname="argument enable_private_service_connect", value=enable_private_service_connect, expected_type=type_hints["enable_private_service_connect"])
            check_type(argname="argument project_allowlist", value=project_allowlist, expected_type=type_hints["project_allowlist"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable_private_service_connect": enable_private_service_connect,
        }
        if project_allowlist is not None:
            self._values["project_allowlist"] = project_allowlist

    @builtins.property
    def enable_private_service_connect(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If set to true, customers will use private service connection to send request.

        Otherwise, the connection will set to public endpoint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#enable_private_service_connect GoogleVertexAiFeatureOnlineStore#enable_private_service_connect}
        '''
        result = self._values.get("enable_private_service_connect")
        assert result is not None, "Required property 'enable_private_service_connect' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def project_allowlist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Projects from which the forwarding rule will target the service attachment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#project_allowlist GoogleVertexAiFeatureOnlineStore#project_allowlist}
        '''
        result = self._values.get("project_allowlist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStore.GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d42e4880ea0cb93f7a39ff1737f8175b01b36a2b65ab9092a25ab42643d781aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetProjectAllowlist")
    def reset_project_allowlist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectAllowlist", []))

    @builtins.property
    @jsii.member(jsii_name="enablePrivateServiceConnectInput")
    def enable_private_service_connect_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePrivateServiceConnectInput"))

    @builtins.property
    @jsii.member(jsii_name="projectAllowlistInput")
    def project_allowlist_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "projectAllowlistInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePrivateServiceConnect")
    def enable_private_service_connect(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enablePrivateServiceConnect"))

    @enable_private_service_connect.setter
    def enable_private_service_connect(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9314689b64540bc89f83c41c00c9e333f18edcf2b4616791dc6b1f5f80783dd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePrivateServiceConnect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectAllowlist")
    def project_allowlist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "projectAllowlist"))

    @project_allowlist.setter
    def project_allowlist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6501808f5d03fd2b96a6e8bde74d7f23e97a39e4a9056bd8b1fe03fd28a1d90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectAllowlist", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76d722e529666279c56afe6a92bfa6d1f013bd510dd056d4546a502fc7941a84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStore.GoogleVertexAiFeatureOnlineStoreEmbeddingManagement",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleVertexAiFeatureOnlineStoreEmbeddingManagement:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Enable embedding management. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#enabled GoogleVertexAiFeatureOnlineStore#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0636064c829ef9c91665087f95e3de5548d59724f3fddc6df0d701383e7ab13f)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable embedding management.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#enabled GoogleVertexAiFeatureOnlineStore#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeatureOnlineStoreEmbeddingManagement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiFeatureOnlineStoreEmbeddingManagementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStore.GoogleVertexAiFeatureOnlineStoreEmbeddingManagementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6f8c0526f7ba459696809b2bae2c5fa392df4c1fa9c62ec5e399e5140840060)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a836bd450c6c57cb77c8745cbe72259a464fc103fc3ad76090377c2c69671b41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiFeatureOnlineStoreEmbeddingManagement]:
        return typing.cast(typing.Optional[GoogleVertexAiFeatureOnlineStoreEmbeddingManagement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiFeatureOnlineStoreEmbeddingManagement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b54afb349fc40df53b999c8d15cd8a64800585e8ad9689e50e5be6a9721c712f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStore.GoogleVertexAiFeatureOnlineStoreOptimized",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleVertexAiFeatureOnlineStoreOptimized:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeatureOnlineStoreOptimized(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiFeatureOnlineStoreOptimizedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStore.GoogleVertexAiFeatureOnlineStoreOptimizedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__155a364a0bb2689b1e5aaab21caf8c0756dcbf704ea6bcf74b579c9744d15842)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiFeatureOnlineStoreOptimized]:
        return typing.cast(typing.Optional[GoogleVertexAiFeatureOnlineStoreOptimized], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiFeatureOnlineStoreOptimized],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27074fd9e93c0fae3d1aab9aecdbf88b385d0578718ab7b4e483152f63d6dba8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStore.GoogleVertexAiFeatureOnlineStoreTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleVertexAiFeatureOnlineStoreTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#create GoogleVertexAiFeatureOnlineStore#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#delete GoogleVertexAiFeatureOnlineStore#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#update GoogleVertexAiFeatureOnlineStore#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88ed595768e4a6f75d9dba683b2da767651d45de8ddb5dac56290b984aa50af5)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#create GoogleVertexAiFeatureOnlineStore#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#delete GoogleVertexAiFeatureOnlineStore#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_feature_online_store#update GoogleVertexAiFeatureOnlineStore#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeatureOnlineStoreTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiFeatureOnlineStoreTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeatureOnlineStore.GoogleVertexAiFeatureOnlineStoreTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74356dfb69b0b96b6e6f4717c25b7ac9dbf8d192af2fc2c8b32b4728d070b493)
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
            type_hints = typing.get_type_hints(_typecheckingstub__711e753dce975f3e75aea63f7f92ac300a4c2b6fb20a6f3a72429131e38a4031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__293c204da31da6836bba4555d969983198ddfb6395e0e1184ef04186ba525a1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c773880d4e027dd209999ca405f6572431b9a8c99442deede659c531c4fb5dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiFeatureOnlineStoreTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiFeatureOnlineStoreTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiFeatureOnlineStoreTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3a7e6a7f2725f13bee54e44ebd32ce8186c23f9425e7c55cd37f9ef0586930b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleVertexAiFeatureOnlineStore",
    "GoogleVertexAiFeatureOnlineStoreBigtable",
    "GoogleVertexAiFeatureOnlineStoreBigtableAutoScaling",
    "GoogleVertexAiFeatureOnlineStoreBigtableAutoScalingOutputReference",
    "GoogleVertexAiFeatureOnlineStoreBigtableOutputReference",
    "GoogleVertexAiFeatureOnlineStoreConfig",
    "GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpoint",
    "GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointOutputReference",
    "GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig",
    "GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfigOutputReference",
    "GoogleVertexAiFeatureOnlineStoreEmbeddingManagement",
    "GoogleVertexAiFeatureOnlineStoreEmbeddingManagementOutputReference",
    "GoogleVertexAiFeatureOnlineStoreOptimized",
    "GoogleVertexAiFeatureOnlineStoreOptimizedOutputReference",
    "GoogleVertexAiFeatureOnlineStoreTimeouts",
    "GoogleVertexAiFeatureOnlineStoreTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a9cb8c07117ae66ea4f976534ee61374bc8ab214581191288fe6801fc6a84d6a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    bigtable: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreBigtable, typing.Dict[builtins.str, typing.Any]]] = None,
    dedicated_serving_endpoint: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
    embedding_management: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreEmbeddingManagement, typing.Dict[builtins.str, typing.Any]]] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    optimized: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreOptimized, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6d64077d894894b8d23dda0648675f32462371fc8912521dd9458f4752b94b4a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1146465c1019537ac1b07e068e4be54970b29a291aab5d800a2ce1e1d023a4a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18820187d8ee08e473ce519d0bb522fa61748abb148fb4d7e33fe125d5b4e598(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54604b722d6858f8e2c4c6200d34bc12fcbd4e288ad236e79243bc3131ad239(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c186b4857159387ac4ef8c492aa468dafd515829e5ac76124c2789ba71099e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b4775ea50a299e2d441ccde4a2e356a6b83b3f5fb6fe912c985d862711f9c50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b57dceeb601f954f87d1c7a749f4d54e4e33732bac4d77ec399ab31762e227a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__349994520e9f8b2db27dcd5edeae165c04a1c91f1080cc04e6724de272228fba(
    *,
    auto_scaling: typing.Union[GoogleVertexAiFeatureOnlineStoreBigtableAutoScaling, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35fedbaf461a1dda3d7bfe04e89230fe4c33846dc0ed045d3745e7c9422a4d93(
    *,
    max_node_count: jsii.Number,
    min_node_count: jsii.Number,
    cpu_utilization_target: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c812c964774d880609fbf60744897e67dc0dd36d7c16da491a89cad71b290a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0459fa4511f522e82b422a7a11968446032ec5defdff3081001d598079b5617f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__999726ea57ad61a222c8474ba85cfe815e380ffe3be82279e9e77246fb955998(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d40a58045cab68707445fbc086d2e514b16bba7bd53c4b2cc919f29946b232(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf23c12e0ac0c1db7c026b11c57a006dee14db7fee2774d1dc82de0d04f128a7(
    value: typing.Optional[GoogleVertexAiFeatureOnlineStoreBigtableAutoScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b506d8f6f38ab51337c0058571afe58dbda7132865efdd71a85718f5b4148f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c778dfe68b297c3cb16f4b2a13c6bb24c6da5ecabc702bf51062ecd963f246c(
    value: typing.Optional[GoogleVertexAiFeatureOnlineStoreBigtable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6614077e66ff9fd057c37e56bc045095c0e1752afe8b94662ad13aca0622175(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    bigtable: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreBigtable, typing.Dict[builtins.str, typing.Any]]] = None,
    dedicated_serving_endpoint: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
    embedding_management: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreEmbeddingManagement, typing.Dict[builtins.str, typing.Any]]] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    optimized: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreOptimized, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39f343c0d1611481a41437239d4e4c115f4d0949f564aa1c7a2e9d092831984b(
    *,
    private_service_connect_config: typing.Optional[typing.Union[GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f39a078126000e601eda38e2683aec3fed1c96a4cd36c801270a23736e30251f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515efeb57025bc646d72ce82aff95219eea112284fc4a99cc4fd4e314b62d0a2(
    value: typing.Optional[GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a66ed49bdb0fa78ab52280a866cfd7e3adac296b2080bfb75e8ce222f54cfb8(
    *,
    enable_private_service_connect: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    project_allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d42e4880ea0cb93f7a39ff1737f8175b01b36a2b65ab9092a25ab42643d781aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9314689b64540bc89f83c41c00c9e333f18edcf2b4616791dc6b1f5f80783dd4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6501808f5d03fd2b96a6e8bde74d7f23e97a39e4a9056bd8b1fe03fd28a1d90(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d722e529666279c56afe6a92bfa6d1f013bd510dd056d4546a502fc7941a84(
    value: typing.Optional[GoogleVertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0636064c829ef9c91665087f95e3de5548d59724f3fddc6df0d701383e7ab13f(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6f8c0526f7ba459696809b2bae2c5fa392df4c1fa9c62ec5e399e5140840060(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a836bd450c6c57cb77c8745cbe72259a464fc103fc3ad76090377c2c69671b41(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b54afb349fc40df53b999c8d15cd8a64800585e8ad9689e50e5be6a9721c712f(
    value: typing.Optional[GoogleVertexAiFeatureOnlineStoreEmbeddingManagement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__155a364a0bb2689b1e5aaab21caf8c0756dcbf704ea6bcf74b579c9744d15842(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27074fd9e93c0fae3d1aab9aecdbf88b385d0578718ab7b4e483152f63d6dba8(
    value: typing.Optional[GoogleVertexAiFeatureOnlineStoreOptimized],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88ed595768e4a6f75d9dba683b2da767651d45de8ddb5dac56290b984aa50af5(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74356dfb69b0b96b6e6f4717c25b7ac9dbf8d192af2fc2c8b32b4728d070b493(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__711e753dce975f3e75aea63f7f92ac300a4c2b6fb20a6f3a72429131e38a4031(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__293c204da31da6836bba4555d969983198ddfb6395e0e1184ef04186ba525a1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c773880d4e027dd209999ca405f6572431b9a8c99442deede659c531c4fb5dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3a7e6a7f2725f13bee54e44ebd32ce8186c23f9425e7c55cd37f9ef0586930b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiFeatureOnlineStoreTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
