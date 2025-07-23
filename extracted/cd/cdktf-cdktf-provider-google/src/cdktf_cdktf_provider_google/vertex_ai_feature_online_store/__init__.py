r'''
# `google_vertex_ai_feature_online_store`

Refer to the Terraform Registry for docs: [`google_vertex_ai_feature_online_store`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store).
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


class VertexAiFeatureOnlineStore(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStore.VertexAiFeatureOnlineStore",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store google_vertex_ai_feature_online_store}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        bigtable: typing.Optional[typing.Union["VertexAiFeatureOnlineStoreBigtable", typing.Dict[builtins.str, typing.Any]]] = None,
        dedicated_serving_endpoint: typing.Optional[typing.Union["VertexAiFeatureOnlineStoreDedicatedServingEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        optimized: typing.Optional[typing.Union["VertexAiFeatureOnlineStoreOptimized", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VertexAiFeatureOnlineStoreTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store google_vertex_ai_feature_online_store} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The resource name of the Feature Online Store. This value may be up to 60 characters, and valid characters are [a-z0-9_]. The first character cannot be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#name VertexAiFeatureOnlineStore#name}
        :param bigtable: bigtable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#bigtable VertexAiFeatureOnlineStore#bigtable}
        :param dedicated_serving_endpoint: dedicated_serving_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#dedicated_serving_endpoint VertexAiFeatureOnlineStore#dedicated_serving_endpoint}
        :param force_destroy: If set to true, any FeatureViews and Features for this FeatureOnlineStore will also be deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#force_destroy VertexAiFeatureOnlineStore#force_destroy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#id VertexAiFeatureOnlineStore#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels with user-defined metadata to organize your feature online stores. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#labels VertexAiFeatureOnlineStore#labels}
        :param optimized: optimized block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#optimized VertexAiFeatureOnlineStore#optimized}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#project VertexAiFeatureOnlineStore#project}.
        :param region: The region of feature online store. eg us-central1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#region VertexAiFeatureOnlineStore#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#timeouts VertexAiFeatureOnlineStore#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcef1ae517a7f9f10bd3f937cecc085854a30b325a37a203ce70226dcbdcf915)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VertexAiFeatureOnlineStoreConfig(
            name=name,
            bigtable=bigtable,
            dedicated_serving_endpoint=dedicated_serving_endpoint,
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
        '''Generates CDKTF code for importing a VertexAiFeatureOnlineStore resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VertexAiFeatureOnlineStore to import.
        :param import_from_id: The id of the existing VertexAiFeatureOnlineStore that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VertexAiFeatureOnlineStore to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b98fa78c8cae748a26198ce70fda99eb9845b31bc1af247ca3798d7aa147396)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBigtable")
    def put_bigtable(
        self,
        *,
        auto_scaling: typing.Union["VertexAiFeatureOnlineStoreBigtableAutoScaling", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param auto_scaling: auto_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#auto_scaling VertexAiFeatureOnlineStore#auto_scaling}
        '''
        value = VertexAiFeatureOnlineStoreBigtable(auto_scaling=auto_scaling)

        return typing.cast(None, jsii.invoke(self, "putBigtable", [value]))

    @jsii.member(jsii_name="putDedicatedServingEndpoint")
    def put_dedicated_serving_endpoint(
        self,
        *,
        private_service_connect_config: typing.Optional[typing.Union["VertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param private_service_connect_config: private_service_connect_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#private_service_connect_config VertexAiFeatureOnlineStore#private_service_connect_config}
        '''
        value = VertexAiFeatureOnlineStoreDedicatedServingEndpoint(
            private_service_connect_config=private_service_connect_config
        )

        return typing.cast(None, jsii.invoke(self, "putDedicatedServingEndpoint", [value]))

    @jsii.member(jsii_name="putOptimized")
    def put_optimized(self) -> None:
        value = VertexAiFeatureOnlineStoreOptimized()

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#create VertexAiFeatureOnlineStore#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#delete VertexAiFeatureOnlineStore#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#update VertexAiFeatureOnlineStore#update}.
        '''
        value = VertexAiFeatureOnlineStoreTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBigtable")
    def reset_bigtable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigtable", []))

    @jsii.member(jsii_name="resetDedicatedServingEndpoint")
    def reset_dedicated_serving_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDedicatedServingEndpoint", []))

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
    def bigtable(self) -> "VertexAiFeatureOnlineStoreBigtableOutputReference":
        return typing.cast("VertexAiFeatureOnlineStoreBigtableOutputReference", jsii.get(self, "bigtable"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedServingEndpoint")
    def dedicated_serving_endpoint(
        self,
    ) -> "VertexAiFeatureOnlineStoreDedicatedServingEndpointOutputReference":
        return typing.cast("VertexAiFeatureOnlineStoreDedicatedServingEndpointOutputReference", jsii.get(self, "dedicatedServingEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="optimized")
    def optimized(self) -> "VertexAiFeatureOnlineStoreOptimizedOutputReference":
        return typing.cast("VertexAiFeatureOnlineStoreOptimizedOutputReference", jsii.get(self, "optimized"))

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
    def timeouts(self) -> "VertexAiFeatureOnlineStoreTimeoutsOutputReference":
        return typing.cast("VertexAiFeatureOnlineStoreTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="bigtableInput")
    def bigtable_input(self) -> typing.Optional["VertexAiFeatureOnlineStoreBigtable"]:
        return typing.cast(typing.Optional["VertexAiFeatureOnlineStoreBigtable"], jsii.get(self, "bigtableInput"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedServingEndpointInput")
    def dedicated_serving_endpoint_input(
        self,
    ) -> typing.Optional["VertexAiFeatureOnlineStoreDedicatedServingEndpoint"]:
        return typing.cast(typing.Optional["VertexAiFeatureOnlineStoreDedicatedServingEndpoint"], jsii.get(self, "dedicatedServingEndpointInput"))

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
    def optimized_input(self) -> typing.Optional["VertexAiFeatureOnlineStoreOptimized"]:
        return typing.cast(typing.Optional["VertexAiFeatureOnlineStoreOptimized"], jsii.get(self, "optimizedInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VertexAiFeatureOnlineStoreTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VertexAiFeatureOnlineStoreTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__522336b7d6133a48ac125385e75b37a5a60f520c44312436957aa9123cf63665)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f03c5306c5efbd9f5127d79784dfcd80c059ea16559e4fb587f76ec8e7820ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a340a5873eab0cc0ca6643294bac4fa31b3e90e04385d5a6df97d40cbc87913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0ede84ffc72288c12169d84a71b29fefc06207bdac88710db9d807c9341c933)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97214193846f38f35b2fe658012704cccbae677d2650a949800857e68d9045d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eef5030e0fda7665e6ba1659564575fdfce697620f6a853203146114b5a5d51a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStore.VertexAiFeatureOnlineStoreBigtable",
    jsii_struct_bases=[],
    name_mapping={"auto_scaling": "autoScaling"},
)
class VertexAiFeatureOnlineStoreBigtable:
    def __init__(
        self,
        *,
        auto_scaling: typing.Union["VertexAiFeatureOnlineStoreBigtableAutoScaling", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param auto_scaling: auto_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#auto_scaling VertexAiFeatureOnlineStore#auto_scaling}
        '''
        if isinstance(auto_scaling, dict):
            auto_scaling = VertexAiFeatureOnlineStoreBigtableAutoScaling(**auto_scaling)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b98e609ff13742864217a94cd3d82e00591e443932a3923c04bb7600b191625f)
            check_type(argname="argument auto_scaling", value=auto_scaling, expected_type=type_hints["auto_scaling"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auto_scaling": auto_scaling,
        }

    @builtins.property
    def auto_scaling(self) -> "VertexAiFeatureOnlineStoreBigtableAutoScaling":
        '''auto_scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#auto_scaling VertexAiFeatureOnlineStore#auto_scaling}
        '''
        result = self._values.get("auto_scaling")
        assert result is not None, "Required property 'auto_scaling' is missing"
        return typing.cast("VertexAiFeatureOnlineStoreBigtableAutoScaling", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiFeatureOnlineStoreBigtable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStore.VertexAiFeatureOnlineStoreBigtableAutoScaling",
    jsii_struct_bases=[],
    name_mapping={
        "max_node_count": "maxNodeCount",
        "min_node_count": "minNodeCount",
        "cpu_utilization_target": "cpuUtilizationTarget",
    },
)
class VertexAiFeatureOnlineStoreBigtableAutoScaling:
    def __init__(
        self,
        *,
        max_node_count: jsii.Number,
        min_node_count: jsii.Number,
        cpu_utilization_target: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_node_count: The maximum number of nodes to scale up to. Must be greater than or equal to minNodeCount, and less than or equal to 10 times of 'minNodeCount'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#max_node_count VertexAiFeatureOnlineStore#max_node_count}
        :param min_node_count: The minimum number of nodes to scale down to. Must be greater than or equal to 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#min_node_count VertexAiFeatureOnlineStore#min_node_count}
        :param cpu_utilization_target: A percentage of the cluster's CPU capacity. Can be from 10% to 80%. When a cluster's CPU utilization exceeds the target that you have set, Bigtable immediately adds nodes to the cluster. When CPU utilization is substantially lower than the target, Bigtable removes nodes. If not set will default to 50%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#cpu_utilization_target VertexAiFeatureOnlineStore#cpu_utilization_target}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__455e47ddbe6cd295ef35ee2e1af62e91f5a3003ba46c9f97fe66775bf0a92fd5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#max_node_count VertexAiFeatureOnlineStore#max_node_count}
        '''
        result = self._values.get("max_node_count")
        assert result is not None, "Required property 'max_node_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_node_count(self) -> jsii.Number:
        '''The minimum number of nodes to scale down to. Must be greater than or equal to 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#min_node_count VertexAiFeatureOnlineStore#min_node_count}
        '''
        result = self._values.get("min_node_count")
        assert result is not None, "Required property 'min_node_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def cpu_utilization_target(self) -> typing.Optional[jsii.Number]:
        '''A percentage of the cluster's CPU capacity.

        Can be from 10% to 80%. When a cluster's CPU utilization exceeds the target that you have set, Bigtable immediately adds nodes to the cluster. When CPU utilization is substantially lower than the target, Bigtable removes nodes. If not set will default to 50%.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#cpu_utilization_target VertexAiFeatureOnlineStore#cpu_utilization_target}
        '''
        result = self._values.get("cpu_utilization_target")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiFeatureOnlineStoreBigtableAutoScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiFeatureOnlineStoreBigtableAutoScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStore.VertexAiFeatureOnlineStoreBigtableAutoScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d10e99b100e6182103955d8609daed10d62e1710426a879f970bbb3c71f7a59)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6cd71072352700b1b67bc59deeee7bd8547b3a4dcb08c5900558756d6e0b2eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuUtilizationTarget", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxNodeCount")
    def max_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxNodeCount"))

    @max_node_count.setter
    def max_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff8aa31dd10b0e5629fd231830c1d0a7887c8228406aa786fbe6bbd89446f0cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodeCount")
    def min_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNodeCount"))

    @min_node_count.setter
    def min_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c2a9005174539790433d9b27bcd2a7a3d06361843c2667122ee841ed0aec527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiFeatureOnlineStoreBigtableAutoScaling]:
        return typing.cast(typing.Optional[VertexAiFeatureOnlineStoreBigtableAutoScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiFeatureOnlineStoreBigtableAutoScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14a3034203953f0aaf8b121bf10676c5da5a52a1cbc9fde16e2fd8871473bf39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiFeatureOnlineStoreBigtableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStore.VertexAiFeatureOnlineStoreBigtableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2219935b15f66e0e9d95225409782a10db5a54d822c2de4f8ba4c3736422950f)
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
        :param max_node_count: The maximum number of nodes to scale up to. Must be greater than or equal to minNodeCount, and less than or equal to 10 times of 'minNodeCount'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#max_node_count VertexAiFeatureOnlineStore#max_node_count}
        :param min_node_count: The minimum number of nodes to scale down to. Must be greater than or equal to 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#min_node_count VertexAiFeatureOnlineStore#min_node_count}
        :param cpu_utilization_target: A percentage of the cluster's CPU capacity. Can be from 10% to 80%. When a cluster's CPU utilization exceeds the target that you have set, Bigtable immediately adds nodes to the cluster. When CPU utilization is substantially lower than the target, Bigtable removes nodes. If not set will default to 50%. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#cpu_utilization_target VertexAiFeatureOnlineStore#cpu_utilization_target}
        '''
        value = VertexAiFeatureOnlineStoreBigtableAutoScaling(
            max_node_count=max_node_count,
            min_node_count=min_node_count,
            cpu_utilization_target=cpu_utilization_target,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoScaling", [value]))

    @builtins.property
    @jsii.member(jsii_name="autoScaling")
    def auto_scaling(
        self,
    ) -> VertexAiFeatureOnlineStoreBigtableAutoScalingOutputReference:
        return typing.cast(VertexAiFeatureOnlineStoreBigtableAutoScalingOutputReference, jsii.get(self, "autoScaling"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingInput")
    def auto_scaling_input(
        self,
    ) -> typing.Optional[VertexAiFeatureOnlineStoreBigtableAutoScaling]:
        return typing.cast(typing.Optional[VertexAiFeatureOnlineStoreBigtableAutoScaling], jsii.get(self, "autoScalingInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VertexAiFeatureOnlineStoreBigtable]:
        return typing.cast(typing.Optional[VertexAiFeatureOnlineStoreBigtable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiFeatureOnlineStoreBigtable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e7482bd48cbd6540fec2857c8855dd280d48631f584624c1d21a33d015a92bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStore.VertexAiFeatureOnlineStoreConfig",
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
        "force_destroy": "forceDestroy",
        "id": "id",
        "labels": "labels",
        "optimized": "optimized",
        "project": "project",
        "region": "region",
        "timeouts": "timeouts",
    },
)
class VertexAiFeatureOnlineStoreConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bigtable: typing.Optional[typing.Union[VertexAiFeatureOnlineStoreBigtable, typing.Dict[builtins.str, typing.Any]]] = None,
        dedicated_serving_endpoint: typing.Optional[typing.Union["VertexAiFeatureOnlineStoreDedicatedServingEndpoint", typing.Dict[builtins.str, typing.Any]]] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        optimized: typing.Optional[typing.Union["VertexAiFeatureOnlineStoreOptimized", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VertexAiFeatureOnlineStoreTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The resource name of the Feature Online Store. This value may be up to 60 characters, and valid characters are [a-z0-9_]. The first character cannot be a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#name VertexAiFeatureOnlineStore#name}
        :param bigtable: bigtable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#bigtable VertexAiFeatureOnlineStore#bigtable}
        :param dedicated_serving_endpoint: dedicated_serving_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#dedicated_serving_endpoint VertexAiFeatureOnlineStore#dedicated_serving_endpoint}
        :param force_destroy: If set to true, any FeatureViews and Features for this FeatureOnlineStore will also be deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#force_destroy VertexAiFeatureOnlineStore#force_destroy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#id VertexAiFeatureOnlineStore#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels with user-defined metadata to organize your feature online stores. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#labels VertexAiFeatureOnlineStore#labels}
        :param optimized: optimized block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#optimized VertexAiFeatureOnlineStore#optimized}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#project VertexAiFeatureOnlineStore#project}.
        :param region: The region of feature online store. eg us-central1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#region VertexAiFeatureOnlineStore#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#timeouts VertexAiFeatureOnlineStore#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bigtable, dict):
            bigtable = VertexAiFeatureOnlineStoreBigtable(**bigtable)
        if isinstance(dedicated_serving_endpoint, dict):
            dedicated_serving_endpoint = VertexAiFeatureOnlineStoreDedicatedServingEndpoint(**dedicated_serving_endpoint)
        if isinstance(optimized, dict):
            optimized = VertexAiFeatureOnlineStoreOptimized(**optimized)
        if isinstance(timeouts, dict):
            timeouts = VertexAiFeatureOnlineStoreTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c05c4422be25e11d1234269fa90fc459406d40a84ff4975ba55deaab220544f6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#name VertexAiFeatureOnlineStore#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bigtable(self) -> typing.Optional[VertexAiFeatureOnlineStoreBigtable]:
        '''bigtable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#bigtable VertexAiFeatureOnlineStore#bigtable}
        '''
        result = self._values.get("bigtable")
        return typing.cast(typing.Optional[VertexAiFeatureOnlineStoreBigtable], result)

    @builtins.property
    def dedicated_serving_endpoint(
        self,
    ) -> typing.Optional["VertexAiFeatureOnlineStoreDedicatedServingEndpoint"]:
        '''dedicated_serving_endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#dedicated_serving_endpoint VertexAiFeatureOnlineStore#dedicated_serving_endpoint}
        '''
        result = self._values.get("dedicated_serving_endpoint")
        return typing.cast(typing.Optional["VertexAiFeatureOnlineStoreDedicatedServingEndpoint"], result)

    @builtins.property
    def force_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, any FeatureViews and Features for this FeatureOnlineStore will also be deleted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#force_destroy VertexAiFeatureOnlineStore#force_destroy}
        '''
        result = self._values.get("force_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#id VertexAiFeatureOnlineStore#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#labels VertexAiFeatureOnlineStore#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def optimized(self) -> typing.Optional["VertexAiFeatureOnlineStoreOptimized"]:
        '''optimized block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#optimized VertexAiFeatureOnlineStore#optimized}
        '''
        result = self._values.get("optimized")
        return typing.cast(typing.Optional["VertexAiFeatureOnlineStoreOptimized"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#project VertexAiFeatureOnlineStore#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of feature online store. eg us-central1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#region VertexAiFeatureOnlineStore#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VertexAiFeatureOnlineStoreTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#timeouts VertexAiFeatureOnlineStore#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VertexAiFeatureOnlineStoreTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiFeatureOnlineStoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStore.VertexAiFeatureOnlineStoreDedicatedServingEndpoint",
    jsii_struct_bases=[],
    name_mapping={"private_service_connect_config": "privateServiceConnectConfig"},
)
class VertexAiFeatureOnlineStoreDedicatedServingEndpoint:
    def __init__(
        self,
        *,
        private_service_connect_config: typing.Optional[typing.Union["VertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param private_service_connect_config: private_service_connect_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#private_service_connect_config VertexAiFeatureOnlineStore#private_service_connect_config}
        '''
        if isinstance(private_service_connect_config, dict):
            private_service_connect_config = VertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig(**private_service_connect_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__134cc915f6415794078c2f258ccfe25a7074b9e31880aa78e5e9d76f81ba2920)
            check_type(argname="argument private_service_connect_config", value=private_service_connect_config, expected_type=type_hints["private_service_connect_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if private_service_connect_config is not None:
            self._values["private_service_connect_config"] = private_service_connect_config

    @builtins.property
    def private_service_connect_config(
        self,
    ) -> typing.Optional["VertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig"]:
        '''private_service_connect_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#private_service_connect_config VertexAiFeatureOnlineStore#private_service_connect_config}
        '''
        result = self._values.get("private_service_connect_config")
        return typing.cast(typing.Optional["VertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiFeatureOnlineStoreDedicatedServingEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiFeatureOnlineStoreDedicatedServingEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStore.VertexAiFeatureOnlineStoreDedicatedServingEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59a8712aa5e36f5231d430720fdc4c987cb6caf7b41a7603bc3799950eda4980)
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
        :param enable_private_service_connect: If set to true, customers will use private service connection to send request. Otherwise, the connection will set to public endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#enable_private_service_connect VertexAiFeatureOnlineStore#enable_private_service_connect}
        :param project_allowlist: A list of Projects from which the forwarding rule will target the service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#project_allowlist VertexAiFeatureOnlineStore#project_allowlist}
        '''
        value = VertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig(
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
    ) -> "VertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfigOutputReference":
        return typing.cast("VertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfigOutputReference", jsii.get(self, "privateServiceConnectConfig"))

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
    ) -> typing.Optional["VertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig"]:
        return typing.cast(typing.Optional["VertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig"], jsii.get(self, "privateServiceConnectConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiFeatureOnlineStoreDedicatedServingEndpoint]:
        return typing.cast(typing.Optional[VertexAiFeatureOnlineStoreDedicatedServingEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiFeatureOnlineStoreDedicatedServingEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad6cb35c8d4ee2e464f822026fdbc36ae545e7ba66cf8776c19d55cbc5964c9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStore.VertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_private_service_connect": "enablePrivateServiceConnect",
        "project_allowlist": "projectAllowlist",
    },
)
class VertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig:
    def __init__(
        self,
        *,
        enable_private_service_connect: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        project_allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enable_private_service_connect: If set to true, customers will use private service connection to send request. Otherwise, the connection will set to public endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#enable_private_service_connect VertexAiFeatureOnlineStore#enable_private_service_connect}
        :param project_allowlist: A list of Projects from which the forwarding rule will target the service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#project_allowlist VertexAiFeatureOnlineStore#project_allowlist}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09edb7664d89362d80f94643fa098df80e94394308dd5109f49771cccc5dbce1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#enable_private_service_connect VertexAiFeatureOnlineStore#enable_private_service_connect}
        '''
        result = self._values.get("enable_private_service_connect")
        assert result is not None, "Required property 'enable_private_service_connect' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def project_allowlist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Projects from which the forwarding rule will target the service attachment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#project_allowlist VertexAiFeatureOnlineStore#project_allowlist}
        '''
        result = self._values.get("project_allowlist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStore.VertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c74d611b70d75393d208436415b3f04e02394cdf713512f0a7127052af3c143)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6300af5a7e8e79989aec0b151e0ac53e0321024c9ad77917d062382694a58ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePrivateServiceConnect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectAllowlist")
    def project_allowlist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "projectAllowlist"))

    @project_allowlist.setter
    def project_allowlist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c14554e02803c5fd8ca92ea42aa065e0b4b7de247216de163ea28630f98e55bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectAllowlist", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig]:
        return typing.cast(typing.Optional[VertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ec26208ecc53b6f69f5aa1cfea089492cd0314ede906aba1129192ca94bb0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStore.VertexAiFeatureOnlineStoreOptimized",
    jsii_struct_bases=[],
    name_mapping={},
)
class VertexAiFeatureOnlineStoreOptimized:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiFeatureOnlineStoreOptimized(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiFeatureOnlineStoreOptimizedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStore.VertexAiFeatureOnlineStoreOptimizedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0646ffe8fcfb954d6af36dbc9059e7895cf422ac8f1f434e5016dc442ca5578)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VertexAiFeatureOnlineStoreOptimized]:
        return typing.cast(typing.Optional[VertexAiFeatureOnlineStoreOptimized], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiFeatureOnlineStoreOptimized],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__168c2e634515eb4f54e02f82059d8fefb807c391743bd01e3d8fd5ff8704f25c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStore.VertexAiFeatureOnlineStoreTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class VertexAiFeatureOnlineStoreTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#create VertexAiFeatureOnlineStore#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#delete VertexAiFeatureOnlineStore#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#update VertexAiFeatureOnlineStore#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1133b5d44a7a063ac4744f575ad2d2e749120b5acdf11e55d9cb57c1b0bce341)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#create VertexAiFeatureOnlineStore#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#delete VertexAiFeatureOnlineStore#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_feature_online_store#update VertexAiFeatureOnlineStore#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiFeatureOnlineStoreTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiFeatureOnlineStoreTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiFeatureOnlineStore.VertexAiFeatureOnlineStoreTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39c24f184abc3a46c24887cdd7c170b5005b14a3ac1b73d35cee6e2452c65b45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c17a998d46648da7aedd9dd96b47579eb30da7d15c03ff4e4418bf0f1835ce15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0467e589a7f9759f8d5bb6b7a8b4f611d904ef5161ef0b50115251dba4118b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c8920b1298d78d6026a36bc77362b2b24fe5a5d8228b5fe0b3c4b656068d09a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiFeatureOnlineStoreTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiFeatureOnlineStoreTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiFeatureOnlineStoreTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17bf9aad156db2569c31318120cef4dc74fd5ff9c6a75a77987d0156ed67aa37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VertexAiFeatureOnlineStore",
    "VertexAiFeatureOnlineStoreBigtable",
    "VertexAiFeatureOnlineStoreBigtableAutoScaling",
    "VertexAiFeatureOnlineStoreBigtableAutoScalingOutputReference",
    "VertexAiFeatureOnlineStoreBigtableOutputReference",
    "VertexAiFeatureOnlineStoreConfig",
    "VertexAiFeatureOnlineStoreDedicatedServingEndpoint",
    "VertexAiFeatureOnlineStoreDedicatedServingEndpointOutputReference",
    "VertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig",
    "VertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfigOutputReference",
    "VertexAiFeatureOnlineStoreOptimized",
    "VertexAiFeatureOnlineStoreOptimizedOutputReference",
    "VertexAiFeatureOnlineStoreTimeouts",
    "VertexAiFeatureOnlineStoreTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__dcef1ae517a7f9f10bd3f937cecc085854a30b325a37a203ce70226dcbdcf915(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    bigtable: typing.Optional[typing.Union[VertexAiFeatureOnlineStoreBigtable, typing.Dict[builtins.str, typing.Any]]] = None,
    dedicated_serving_endpoint: typing.Optional[typing.Union[VertexAiFeatureOnlineStoreDedicatedServingEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    optimized: typing.Optional[typing.Union[VertexAiFeatureOnlineStoreOptimized, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VertexAiFeatureOnlineStoreTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3b98fa78c8cae748a26198ce70fda99eb9845b31bc1af247ca3798d7aa147396(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__522336b7d6133a48ac125385e75b37a5a60f520c44312436957aa9123cf63665(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f03c5306c5efbd9f5127d79784dfcd80c059ea16559e4fb587f76ec8e7820ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a340a5873eab0cc0ca6643294bac4fa31b3e90e04385d5a6df97d40cbc87913(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0ede84ffc72288c12169d84a71b29fefc06207bdac88710db9d807c9341c933(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97214193846f38f35b2fe658012704cccbae677d2650a949800857e68d9045d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eef5030e0fda7665e6ba1659564575fdfce697620f6a853203146114b5a5d51a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98e609ff13742864217a94cd3d82e00591e443932a3923c04bb7600b191625f(
    *,
    auto_scaling: typing.Union[VertexAiFeatureOnlineStoreBigtableAutoScaling, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__455e47ddbe6cd295ef35ee2e1af62e91f5a3003ba46c9f97fe66775bf0a92fd5(
    *,
    max_node_count: jsii.Number,
    min_node_count: jsii.Number,
    cpu_utilization_target: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d10e99b100e6182103955d8609daed10d62e1710426a879f970bbb3c71f7a59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6cd71072352700b1b67bc59deeee7bd8547b3a4dcb08c5900558756d6e0b2eb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff8aa31dd10b0e5629fd231830c1d0a7887c8228406aa786fbe6bbd89446f0cc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2a9005174539790433d9b27bcd2a7a3d06361843c2667122ee841ed0aec527(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14a3034203953f0aaf8b121bf10676c5da5a52a1cbc9fde16e2fd8871473bf39(
    value: typing.Optional[VertexAiFeatureOnlineStoreBigtableAutoScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2219935b15f66e0e9d95225409782a10db5a54d822c2de4f8ba4c3736422950f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e7482bd48cbd6540fec2857c8855dd280d48631f584624c1d21a33d015a92bb(
    value: typing.Optional[VertexAiFeatureOnlineStoreBigtable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05c4422be25e11d1234269fa90fc459406d40a84ff4975ba55deaab220544f6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    bigtable: typing.Optional[typing.Union[VertexAiFeatureOnlineStoreBigtable, typing.Dict[builtins.str, typing.Any]]] = None,
    dedicated_serving_endpoint: typing.Optional[typing.Union[VertexAiFeatureOnlineStoreDedicatedServingEndpoint, typing.Dict[builtins.str, typing.Any]]] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    optimized: typing.Optional[typing.Union[VertexAiFeatureOnlineStoreOptimized, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VertexAiFeatureOnlineStoreTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134cc915f6415794078c2f258ccfe25a7074b9e31880aa78e5e9d76f81ba2920(
    *,
    private_service_connect_config: typing.Optional[typing.Union[VertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a8712aa5e36f5231d430720fdc4c987cb6caf7b41a7603bc3799950eda4980(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6cb35c8d4ee2e464f822026fdbc36ae545e7ba66cf8776c19d55cbc5964c9f(
    value: typing.Optional[VertexAiFeatureOnlineStoreDedicatedServingEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09edb7664d89362d80f94643fa098df80e94394308dd5109f49771cccc5dbce1(
    *,
    enable_private_service_connect: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    project_allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c74d611b70d75393d208436415b3f04e02394cdf713512f0a7127052af3c143(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6300af5a7e8e79989aec0b151e0ac53e0321024c9ad77917d062382694a58ae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c14554e02803c5fd8ca92ea42aa065e0b4b7de247216de163ea28630f98e55bd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ec26208ecc53b6f69f5aa1cfea089492cd0314ede906aba1129192ca94bb0e(
    value: typing.Optional[VertexAiFeatureOnlineStoreDedicatedServingEndpointPrivateServiceConnectConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0646ffe8fcfb954d6af36dbc9059e7895cf422ac8f1f434e5016dc442ca5578(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__168c2e634515eb4f54e02f82059d8fefb807c391743bd01e3d8fd5ff8704f25c(
    value: typing.Optional[VertexAiFeatureOnlineStoreOptimized],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1133b5d44a7a063ac4744f575ad2d2e749120b5acdf11e55d9cb57c1b0bce341(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c24f184abc3a46c24887cdd7c170b5005b14a3ac1b73d35cee6e2452c65b45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c17a998d46648da7aedd9dd96b47579eb30da7d15c03ff4e4418bf0f1835ce15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0467e589a7f9759f8d5bb6b7a8b4f611d904ef5161ef0b50115251dba4118b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8920b1298d78d6026a36bc77362b2b24fe5a5d8228b5fe0b3c4b656068d09a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17bf9aad156db2569c31318120cef4dc74fd5ff9c6a75a77987d0156ed67aa37(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiFeatureOnlineStoreTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
