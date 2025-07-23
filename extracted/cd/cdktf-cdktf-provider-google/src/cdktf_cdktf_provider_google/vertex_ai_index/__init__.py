r'''
# `google_vertex_ai_index`

Refer to the Terraform Registry for docs: [`google_vertex_ai_index`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index).
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


class VertexAiIndex(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiIndex.VertexAiIndex",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index google_vertex_ai_index}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        index_update_method: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata: typing.Optional[typing.Union["VertexAiIndexMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VertexAiIndexTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index google_vertex_ai_index} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: The display name of the Index. The name can be up to 128 characters long and can consist of any UTF-8 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#display_name VertexAiIndex#display_name}
        :param description: The description of the Index. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#description VertexAiIndex#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#id VertexAiIndex#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param index_update_method: The update method to use with this Index. The value must be the followings. If not set, BATCH_UPDATE will be used by default. - BATCH_UPDATE: user can call indexes.patch with files on Cloud Storage of datapoints to update. - STREAM_UPDATE: user can call indexes.upsertDatapoints/DeleteDatapoints to update the Index and the updates will be applied in corresponding DeployedIndexes in nearly real-time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#index_update_method VertexAiIndex#index_update_method}
        :param labels: The labels with user-defined metadata to organize your Indexes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#labels VertexAiIndex#labels}
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#metadata VertexAiIndex#metadata}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#project VertexAiIndex#project}.
        :param region: The region of the index. eg us-central1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#region VertexAiIndex#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#timeouts VertexAiIndex#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b7076b26580b2f525ea3e36739fd080577bc3926fa6f7a6480fd3f5b955f1a8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VertexAiIndexConfig(
            display_name=display_name,
            description=description,
            id=id,
            index_update_method=index_update_method,
            labels=labels,
            metadata=metadata,
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
        '''Generates CDKTF code for importing a VertexAiIndex resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VertexAiIndex to import.
        :param import_from_id: The id of the existing VertexAiIndex that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VertexAiIndex to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5e757214fd8abd3798b360c361084430dc43d29bbf0f412ea5fa6a718e34e29)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMetadata")
    def put_metadata(
        self,
        *,
        config: typing.Optional[typing.Union["VertexAiIndexMetadataConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        contents_delta_uri: typing.Optional[builtins.str] = None,
        is_complete_overwrite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#config VertexAiIndex#config}
        :param contents_delta_uri: Allows inserting, updating or deleting the contents of the Matching Engine Index. The string must be a valid Cloud Storage directory path. If this field is set when calling IndexService.UpdateIndex, then no other Index field can be also updated as part of the same call. The expected structure and format of the files this URI points to is described at https://cloud.google.com/vertex-ai/docs/matching-engine/using-matching-engine#input-data-format Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#contents_delta_uri VertexAiIndex#contents_delta_uri}
        :param is_complete_overwrite: If this field is set together with contentsDeltaUri when calling IndexService.UpdateIndex, then existing content of the Index will be replaced by the data from the contentsDeltaUri. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#is_complete_overwrite VertexAiIndex#is_complete_overwrite}
        '''
        value = VertexAiIndexMetadata(
            config=config,
            contents_delta_uri=contents_delta_uri,
            is_complete_overwrite=is_complete_overwrite,
        )

        return typing.cast(None, jsii.invoke(self, "putMetadata", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#create VertexAiIndex#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#delete VertexAiIndex#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#update VertexAiIndex#update}.
        '''
        value = VertexAiIndexTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIndexUpdateMethod")
    def reset_index_update_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIndexUpdateMethod", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="deployedIndexes")
    def deployed_indexes(self) -> "VertexAiIndexDeployedIndexesList":
        return typing.cast("VertexAiIndexDeployedIndexesList", jsii.get(self, "deployedIndexes"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="indexStats")
    def index_stats(self) -> "VertexAiIndexIndexStatsList":
        return typing.cast("VertexAiIndexIndexStatsList", jsii.get(self, "indexStats"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> "VertexAiIndexMetadataOutputReference":
        return typing.cast("VertexAiIndexMetadataOutputReference", jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="metadataSchemaUri")
    def metadata_schema_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataSchemaUri"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VertexAiIndexTimeoutsOutputReference":
        return typing.cast("VertexAiIndexTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="indexUpdateMethodInput")
    def index_update_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexUpdateMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional["VertexAiIndexMetadata"]:
        return typing.cast(typing.Optional["VertexAiIndexMetadata"], jsii.get(self, "metadataInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VertexAiIndexTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VertexAiIndexTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7563902c2a93f33c4baaa026cac9f6c84d1ba958a049af49db40ddb13e00cc3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f86db3723738b2a9a83fbf2b786b2d03a85319b492a85bef2e4322557ca1351)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65712878d2466377ffeb5befe76c4a1a2dc099818f5299b7539a9bfc818ec1fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indexUpdateMethod")
    def index_update_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "indexUpdateMethod"))

    @index_update_method.setter
    def index_update_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e490edf3138e6c96191c8ae627eb3bec6394a01b3f3c1f9d1e9f06eae6f2ff68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indexUpdateMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1711fbca13dfd773731181d6dcb4f64d9d779f60a664d61c105840f1f5e69cb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d302d07c93e89418a38747df9f393c44688109eb23e7227db8492d0c2b9080e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9868f10e3782437a430767133705fdf16c686469f9469d310e34a7aa8a725349)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiIndex.VertexAiIndexConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "display_name": "displayName",
        "description": "description",
        "id": "id",
        "index_update_method": "indexUpdateMethod",
        "labels": "labels",
        "metadata": "metadata",
        "project": "project",
        "region": "region",
        "timeouts": "timeouts",
    },
)
class VertexAiIndexConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        display_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        index_update_method: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata: typing.Optional[typing.Union["VertexAiIndexMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VertexAiIndexTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: The display name of the Index. The name can be up to 128 characters long and can consist of any UTF-8 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#display_name VertexAiIndex#display_name}
        :param description: The description of the Index. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#description VertexAiIndex#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#id VertexAiIndex#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param index_update_method: The update method to use with this Index. The value must be the followings. If not set, BATCH_UPDATE will be used by default. - BATCH_UPDATE: user can call indexes.patch with files on Cloud Storage of datapoints to update. - STREAM_UPDATE: user can call indexes.upsertDatapoints/DeleteDatapoints to update the Index and the updates will be applied in corresponding DeployedIndexes in nearly real-time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#index_update_method VertexAiIndex#index_update_method}
        :param labels: The labels with user-defined metadata to organize your Indexes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#labels VertexAiIndex#labels}
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#metadata VertexAiIndex#metadata}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#project VertexAiIndex#project}.
        :param region: The region of the index. eg us-central1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#region VertexAiIndex#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#timeouts VertexAiIndex#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(metadata, dict):
            metadata = VertexAiIndexMetadata(**metadata)
        if isinstance(timeouts, dict):
            timeouts = VertexAiIndexTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0126877dbafd6883709f6ec67439a1762436c7d6a7ab3b81fd0ee1df9f65337c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument index_update_method", value=index_update_method, expected_type=type_hints["index_update_method"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if index_update_method is not None:
            self._values["index_update_method"] = index_update_method
        if labels is not None:
            self._values["labels"] = labels
        if metadata is not None:
            self._values["metadata"] = metadata
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
    def display_name(self) -> builtins.str:
        '''The display name of the Index.

        The name can be up to 128 characters long and can consist of any UTF-8 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#display_name VertexAiIndex#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the Index.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#description VertexAiIndex#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#id VertexAiIndex#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def index_update_method(self) -> typing.Optional[builtins.str]:
        '''The update method to use with this Index.

        The value must be the followings. If not set, BATCH_UPDATE will be used by default.

        - BATCH_UPDATE: user can call indexes.patch with files on Cloud Storage of datapoints to update.
        - STREAM_UPDATE: user can call indexes.upsertDatapoints/DeleteDatapoints to update the Index and the updates will be applied in corresponding DeployedIndexes in nearly real-time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#index_update_method VertexAiIndex#index_update_method}
        '''
        result = self._values.get("index_update_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The labels with user-defined metadata to organize your Indexes.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#labels VertexAiIndex#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata(self) -> typing.Optional["VertexAiIndexMetadata"]:
        '''metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#metadata VertexAiIndex#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional["VertexAiIndexMetadata"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#project VertexAiIndex#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of the index. eg us-central1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#region VertexAiIndex#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VertexAiIndexTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#timeouts VertexAiIndex#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VertexAiIndexTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiIndexConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiIndex.VertexAiIndexDeployedIndexes",
    jsii_struct_bases=[],
    name_mapping={},
)
class VertexAiIndexDeployedIndexes:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiIndexDeployedIndexes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiIndexDeployedIndexesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiIndex.VertexAiIndexDeployedIndexesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e92746e71dea095ede5f2d80aa54ec4c59e6ba9d800f527c852001411f06e3e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VertexAiIndexDeployedIndexesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cde63c1d221e9ea78e4f21bed913be572428ba28845b0567ecd266f9f80bbda7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VertexAiIndexDeployedIndexesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2973accc9879ba24a2d40dec660a8e1c3ca91e811ab36ab4fb27cf0f7d335ad9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__004234377cb06f6eb67e78ba2969bc0a48990463cd15937308c4c903ff063d61)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb9837de2d85ce51d8a8a6c313c224184a0a5f00609c7fb954c29cc41df053af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class VertexAiIndexDeployedIndexesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiIndex.VertexAiIndexDeployedIndexesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad24836040cb8a10b66b8d4a6945bb2de99aa62315d48823870a5be586e18ebb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="deployedIndexId")
    def deployed_index_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deployedIndexId"))

    @builtins.property
    @jsii.member(jsii_name="indexEndpoint")
    def index_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "indexEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VertexAiIndexDeployedIndexes]:
        return typing.cast(typing.Optional[VertexAiIndexDeployedIndexes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiIndexDeployedIndexes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__608707c4dc41d2d5221d161ee57cd4875a3e20186c4acfa8d9bb814400c5c0eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiIndex.VertexAiIndexIndexStats",
    jsii_struct_bases=[],
    name_mapping={},
)
class VertexAiIndexIndexStats:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiIndexIndexStats(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiIndexIndexStatsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiIndex.VertexAiIndexIndexStatsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83c87cc697b50850c45620e382b2f30404fd589af2d5c56b20571a24aa2d8122)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VertexAiIndexIndexStatsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9058e41ef51f9cacd3cd22b7076b2281104d77fb08749713c694ba9004b83662)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VertexAiIndexIndexStatsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3154f280509c6c7d5a5a9819427252653de8d39fe69b2f406e968df64273fd27)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecc956efbc9d1987ab820ec816bb7d597f67ef9738c4b0237f85d19bddf97003)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa530a8f473a9d8d3eadac0d1fca205dfdca0bdf63a6f8fafff4b3b6abf58417)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class VertexAiIndexIndexStatsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiIndex.VertexAiIndexIndexStatsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc385f7aed9543f76bc65891e7358219fa3434c4b77a47aaa211b7afb871025e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="shardsCount")
    def shards_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "shardsCount"))

    @builtins.property
    @jsii.member(jsii_name="vectorsCount")
    def vectors_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vectorsCount"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VertexAiIndexIndexStats]:
        return typing.cast(typing.Optional[VertexAiIndexIndexStats], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VertexAiIndexIndexStats]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ef11e5d00d02825b5e6b828e11f4c6b695f3bf538fd569ca5eabb2516729e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiIndex.VertexAiIndexMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "config": "config",
        "contents_delta_uri": "contentsDeltaUri",
        "is_complete_overwrite": "isCompleteOverwrite",
    },
)
class VertexAiIndexMetadata:
    def __init__(
        self,
        *,
        config: typing.Optional[typing.Union["VertexAiIndexMetadataConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        contents_delta_uri: typing.Optional[builtins.str] = None,
        is_complete_overwrite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#config VertexAiIndex#config}
        :param contents_delta_uri: Allows inserting, updating or deleting the contents of the Matching Engine Index. The string must be a valid Cloud Storage directory path. If this field is set when calling IndexService.UpdateIndex, then no other Index field can be also updated as part of the same call. The expected structure and format of the files this URI points to is described at https://cloud.google.com/vertex-ai/docs/matching-engine/using-matching-engine#input-data-format Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#contents_delta_uri VertexAiIndex#contents_delta_uri}
        :param is_complete_overwrite: If this field is set together with contentsDeltaUri when calling IndexService.UpdateIndex, then existing content of the Index will be replaced by the data from the contentsDeltaUri. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#is_complete_overwrite VertexAiIndex#is_complete_overwrite}
        '''
        if isinstance(config, dict):
            config = VertexAiIndexMetadataConfig(**config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7d0caeb99ed92a048aa59a2e7440c4b724861f8c17e6dd056c384dc5b6d1b4c)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument contents_delta_uri", value=contents_delta_uri, expected_type=type_hints["contents_delta_uri"])
            check_type(argname="argument is_complete_overwrite", value=is_complete_overwrite, expected_type=type_hints["is_complete_overwrite"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config is not None:
            self._values["config"] = config
        if contents_delta_uri is not None:
            self._values["contents_delta_uri"] = contents_delta_uri
        if is_complete_overwrite is not None:
            self._values["is_complete_overwrite"] = is_complete_overwrite

    @builtins.property
    def config(self) -> typing.Optional["VertexAiIndexMetadataConfig"]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#config VertexAiIndex#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["VertexAiIndexMetadataConfig"], result)

    @builtins.property
    def contents_delta_uri(self) -> typing.Optional[builtins.str]:
        '''Allows inserting, updating  or deleting the contents of the Matching Engine Index.

        The string must be a valid Cloud Storage directory path. If this
        field is set when calling IndexService.UpdateIndex, then no other
        Index field can be also updated as part of the same call.
        The expected structure and format of the files this URI points to is
        described at https://cloud.google.com/vertex-ai/docs/matching-engine/using-matching-engine#input-data-format

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#contents_delta_uri VertexAiIndex#contents_delta_uri}
        '''
        result = self._values.get("contents_delta_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_complete_overwrite(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If this field is set together with contentsDeltaUri when calling IndexService.UpdateIndex, then existing content of the Index will be replaced by the data from the contentsDeltaUri.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#is_complete_overwrite VertexAiIndex#is_complete_overwrite}
        '''
        result = self._values.get("is_complete_overwrite")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiIndexMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiIndex.VertexAiIndexMetadataConfig",
    jsii_struct_bases=[],
    name_mapping={
        "dimensions": "dimensions",
        "algorithm_config": "algorithmConfig",
        "approximate_neighbors_count": "approximateNeighborsCount",
        "distance_measure_type": "distanceMeasureType",
        "feature_norm_type": "featureNormType",
        "shard_size": "shardSize",
    },
)
class VertexAiIndexMetadataConfig:
    def __init__(
        self,
        *,
        dimensions: jsii.Number,
        algorithm_config: typing.Optional[typing.Union["VertexAiIndexMetadataConfigAlgorithmConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        approximate_neighbors_count: typing.Optional[jsii.Number] = None,
        distance_measure_type: typing.Optional[builtins.str] = None,
        feature_norm_type: typing.Optional[builtins.str] = None,
        shard_size: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dimensions: The number of dimensions of the input vectors. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#dimensions VertexAiIndex#dimensions}
        :param algorithm_config: algorithm_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#algorithm_config VertexAiIndex#algorithm_config}
        :param approximate_neighbors_count: The default number of neighbors to find via approximate search before exact reordering is performed. Exact reordering is a procedure where results returned by an approximate search algorithm are reordered via a more expensive distance computation. Required if tree-AH algorithm is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#approximate_neighbors_count VertexAiIndex#approximate_neighbors_count}
        :param distance_measure_type: The distance measure used in nearest neighbor search. The value must be one of the followings: - SQUARED_L2_DISTANCE: Euclidean (L_2) Distance - L1_DISTANCE: Manhattan (L_1) Distance - COSINE_DISTANCE: Cosine Distance. Defined as 1 - cosine similarity. - DOT_PRODUCT_DISTANCE: Dot Product Distance. Defined as a negative of the dot product Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#distance_measure_type VertexAiIndex#distance_measure_type}
        :param feature_norm_type: Type of normalization to be carried out on each vector. The value must be one of the followings: - UNIT_L2_NORM: Unit L2 normalization type - NONE: No normalization type is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#feature_norm_type VertexAiIndex#feature_norm_type}
        :param shard_size: Index data is split into equal parts to be processed. These are called "shards". The shard size must be specified when creating an index. The value must be one of the followings: - SHARD_SIZE_SMALL: Small (2GB) - SHARD_SIZE_MEDIUM: Medium (20GB) - SHARD_SIZE_LARGE: Large (50GB) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#shard_size VertexAiIndex#shard_size}
        '''
        if isinstance(algorithm_config, dict):
            algorithm_config = VertexAiIndexMetadataConfigAlgorithmConfig(**algorithm_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c65b98db650b9656406d5a3874f903ac0bea58541cb19846b06a26d524049aa4)
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            check_type(argname="argument algorithm_config", value=algorithm_config, expected_type=type_hints["algorithm_config"])
            check_type(argname="argument approximate_neighbors_count", value=approximate_neighbors_count, expected_type=type_hints["approximate_neighbors_count"])
            check_type(argname="argument distance_measure_type", value=distance_measure_type, expected_type=type_hints["distance_measure_type"])
            check_type(argname="argument feature_norm_type", value=feature_norm_type, expected_type=type_hints["feature_norm_type"])
            check_type(argname="argument shard_size", value=shard_size, expected_type=type_hints["shard_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dimensions": dimensions,
        }
        if algorithm_config is not None:
            self._values["algorithm_config"] = algorithm_config
        if approximate_neighbors_count is not None:
            self._values["approximate_neighbors_count"] = approximate_neighbors_count
        if distance_measure_type is not None:
            self._values["distance_measure_type"] = distance_measure_type
        if feature_norm_type is not None:
            self._values["feature_norm_type"] = feature_norm_type
        if shard_size is not None:
            self._values["shard_size"] = shard_size

    @builtins.property
    def dimensions(self) -> jsii.Number:
        '''The number of dimensions of the input vectors.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#dimensions VertexAiIndex#dimensions}
        '''
        result = self._values.get("dimensions")
        assert result is not None, "Required property 'dimensions' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def algorithm_config(
        self,
    ) -> typing.Optional["VertexAiIndexMetadataConfigAlgorithmConfig"]:
        '''algorithm_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#algorithm_config VertexAiIndex#algorithm_config}
        '''
        result = self._values.get("algorithm_config")
        return typing.cast(typing.Optional["VertexAiIndexMetadataConfigAlgorithmConfig"], result)

    @builtins.property
    def approximate_neighbors_count(self) -> typing.Optional[jsii.Number]:
        '''The default number of neighbors to find via approximate search before exact reordering is performed.

        Exact reordering is a procedure where results returned by an
        approximate search algorithm are reordered via a more expensive distance computation.
        Required if tree-AH algorithm is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#approximate_neighbors_count VertexAiIndex#approximate_neighbors_count}
        '''
        result = self._values.get("approximate_neighbors_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def distance_measure_type(self) -> typing.Optional[builtins.str]:
        '''The distance measure used in nearest neighbor search.

        The value must be one of the followings:

        - SQUARED_L2_DISTANCE: Euclidean (L_2) Distance
        - L1_DISTANCE: Manhattan (L_1) Distance
        - COSINE_DISTANCE: Cosine Distance. Defined as 1 - cosine similarity.
        - DOT_PRODUCT_DISTANCE: Dot Product Distance. Defined as a negative of the dot product

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#distance_measure_type VertexAiIndex#distance_measure_type}
        '''
        result = self._values.get("distance_measure_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def feature_norm_type(self) -> typing.Optional[builtins.str]:
        '''Type of normalization to be carried out on each vector.

        The value must be one of the followings:

        - UNIT_L2_NORM: Unit L2 normalization type
        - NONE: No normalization type is specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#feature_norm_type VertexAiIndex#feature_norm_type}
        '''
        result = self._values.get("feature_norm_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shard_size(self) -> typing.Optional[builtins.str]:
        '''Index data is split into equal parts to be processed.

        These are called "shards".
        The shard size must be specified when creating an index. The value must be one of the followings:

        - SHARD_SIZE_SMALL: Small (2GB)
        - SHARD_SIZE_MEDIUM: Medium (20GB)
        - SHARD_SIZE_LARGE: Large (50GB)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#shard_size VertexAiIndex#shard_size}
        '''
        result = self._values.get("shard_size")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiIndexMetadataConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiIndex.VertexAiIndexMetadataConfigAlgorithmConfig",
    jsii_struct_bases=[],
    name_mapping={
        "brute_force_config": "bruteForceConfig",
        "tree_ah_config": "treeAhConfig",
    },
)
class VertexAiIndexMetadataConfigAlgorithmConfig:
    def __init__(
        self,
        *,
        brute_force_config: typing.Optional[typing.Union["VertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tree_ah_config: typing.Optional[typing.Union["VertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param brute_force_config: brute_force_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#brute_force_config VertexAiIndex#brute_force_config}
        :param tree_ah_config: tree_ah_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#tree_ah_config VertexAiIndex#tree_ah_config}
        '''
        if isinstance(brute_force_config, dict):
            brute_force_config = VertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig(**brute_force_config)
        if isinstance(tree_ah_config, dict):
            tree_ah_config = VertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig(**tree_ah_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1dfaee87e3155ed4eb2a6cf272aec1a576be8077027590c1bba0eae5ac8d05e)
            check_type(argname="argument brute_force_config", value=brute_force_config, expected_type=type_hints["brute_force_config"])
            check_type(argname="argument tree_ah_config", value=tree_ah_config, expected_type=type_hints["tree_ah_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if brute_force_config is not None:
            self._values["brute_force_config"] = brute_force_config
        if tree_ah_config is not None:
            self._values["tree_ah_config"] = tree_ah_config

    @builtins.property
    def brute_force_config(
        self,
    ) -> typing.Optional["VertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig"]:
        '''brute_force_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#brute_force_config VertexAiIndex#brute_force_config}
        '''
        result = self._values.get("brute_force_config")
        return typing.cast(typing.Optional["VertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig"], result)

    @builtins.property
    def tree_ah_config(
        self,
    ) -> typing.Optional["VertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig"]:
        '''tree_ah_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#tree_ah_config VertexAiIndex#tree_ah_config}
        '''
        result = self._values.get("tree_ah_config")
        return typing.cast(typing.Optional["VertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiIndexMetadataConfigAlgorithmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiIndex.VertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class VertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiIndex.VertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62852922e44ffbcf600144bb06159f30b28cc5234ba0440c08aec8d946209f4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig]:
        return typing.cast(typing.Optional[VertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__066054f1f2ce42107ef85f203cce7b07d773346553ac146fe4b5ce0146e44264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiIndexMetadataConfigAlgorithmConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiIndex.VertexAiIndexMetadataConfigAlgorithmConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__325151a502e54a33776c4fac1beae0bff03cce0d7e0775cf8a95121352b3075d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBruteForceConfig")
    def put_brute_force_config(self) -> None:
        value = VertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig()

        return typing.cast(None, jsii.invoke(self, "putBruteForceConfig", [value]))

    @jsii.member(jsii_name="putTreeAhConfig")
    def put_tree_ah_config(
        self,
        *,
        leaf_node_embedding_count: typing.Optional[jsii.Number] = None,
        leaf_nodes_to_search_percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param leaf_node_embedding_count: Number of embeddings on each leaf node. The default value is 1000 if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#leaf_node_embedding_count VertexAiIndex#leaf_node_embedding_count}
        :param leaf_nodes_to_search_percent: The default percentage of leaf nodes that any query may be searched. Must be in range 1-100, inclusive. The default value is 10 (means 10%) if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#leaf_nodes_to_search_percent VertexAiIndex#leaf_nodes_to_search_percent}
        '''
        value = VertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig(
            leaf_node_embedding_count=leaf_node_embedding_count,
            leaf_nodes_to_search_percent=leaf_nodes_to_search_percent,
        )

        return typing.cast(None, jsii.invoke(self, "putTreeAhConfig", [value]))

    @jsii.member(jsii_name="resetBruteForceConfig")
    def reset_brute_force_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBruteForceConfig", []))

    @jsii.member(jsii_name="resetTreeAhConfig")
    def reset_tree_ah_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTreeAhConfig", []))

    @builtins.property
    @jsii.member(jsii_name="bruteForceConfig")
    def brute_force_config(
        self,
    ) -> VertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfigOutputReference:
        return typing.cast(VertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfigOutputReference, jsii.get(self, "bruteForceConfig"))

    @builtins.property
    @jsii.member(jsii_name="treeAhConfig")
    def tree_ah_config(
        self,
    ) -> "VertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfigOutputReference":
        return typing.cast("VertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfigOutputReference", jsii.get(self, "treeAhConfig"))

    @builtins.property
    @jsii.member(jsii_name="bruteForceConfigInput")
    def brute_force_config_input(
        self,
    ) -> typing.Optional[VertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig]:
        return typing.cast(typing.Optional[VertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig], jsii.get(self, "bruteForceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="treeAhConfigInput")
    def tree_ah_config_input(
        self,
    ) -> typing.Optional["VertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig"]:
        return typing.cast(typing.Optional["VertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig"], jsii.get(self, "treeAhConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiIndexMetadataConfigAlgorithmConfig]:
        return typing.cast(typing.Optional[VertexAiIndexMetadataConfigAlgorithmConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiIndexMetadataConfigAlgorithmConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b368ef0bf68796d9ae73c415fe3af3496bfc0626ce29c5314018de55920a15c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiIndex.VertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig",
    jsii_struct_bases=[],
    name_mapping={
        "leaf_node_embedding_count": "leafNodeEmbeddingCount",
        "leaf_nodes_to_search_percent": "leafNodesToSearchPercent",
    },
)
class VertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig:
    def __init__(
        self,
        *,
        leaf_node_embedding_count: typing.Optional[jsii.Number] = None,
        leaf_nodes_to_search_percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param leaf_node_embedding_count: Number of embeddings on each leaf node. The default value is 1000 if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#leaf_node_embedding_count VertexAiIndex#leaf_node_embedding_count}
        :param leaf_nodes_to_search_percent: The default percentage of leaf nodes that any query may be searched. Must be in range 1-100, inclusive. The default value is 10 (means 10%) if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#leaf_nodes_to_search_percent VertexAiIndex#leaf_nodes_to_search_percent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9800582b6ed7f8f6095b3c1f88a2f6445c8e6eb4133ac5131f2c37db4686318)
            check_type(argname="argument leaf_node_embedding_count", value=leaf_node_embedding_count, expected_type=type_hints["leaf_node_embedding_count"])
            check_type(argname="argument leaf_nodes_to_search_percent", value=leaf_nodes_to_search_percent, expected_type=type_hints["leaf_nodes_to_search_percent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if leaf_node_embedding_count is not None:
            self._values["leaf_node_embedding_count"] = leaf_node_embedding_count
        if leaf_nodes_to_search_percent is not None:
            self._values["leaf_nodes_to_search_percent"] = leaf_nodes_to_search_percent

    @builtins.property
    def leaf_node_embedding_count(self) -> typing.Optional[jsii.Number]:
        '''Number of embeddings on each leaf node. The default value is 1000 if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#leaf_node_embedding_count VertexAiIndex#leaf_node_embedding_count}
        '''
        result = self._values.get("leaf_node_embedding_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def leaf_nodes_to_search_percent(self) -> typing.Optional[jsii.Number]:
        '''The default percentage of leaf nodes that any query may be searched.

        Must be in
        range 1-100, inclusive. The default value is 10 (means 10%) if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#leaf_nodes_to_search_percent VertexAiIndex#leaf_nodes_to_search_percent}
        '''
        result = self._values.get("leaf_nodes_to_search_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiIndex.VertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de9d7e2a1e81aa0bee256db991410632176c799ae7f04feb11b262c06065b478)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLeafNodeEmbeddingCount")
    def reset_leaf_node_embedding_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLeafNodeEmbeddingCount", []))

    @jsii.member(jsii_name="resetLeafNodesToSearchPercent")
    def reset_leaf_nodes_to_search_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLeafNodesToSearchPercent", []))

    @builtins.property
    @jsii.member(jsii_name="leafNodeEmbeddingCountInput")
    def leaf_node_embedding_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "leafNodeEmbeddingCountInput"))

    @builtins.property
    @jsii.member(jsii_name="leafNodesToSearchPercentInput")
    def leaf_nodes_to_search_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "leafNodesToSearchPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="leafNodeEmbeddingCount")
    def leaf_node_embedding_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "leafNodeEmbeddingCount"))

    @leaf_node_embedding_count.setter
    def leaf_node_embedding_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c056ce3f3fd47f822745184c4577305e5fa97ea595169feef8712d04c7a3b5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "leafNodeEmbeddingCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="leafNodesToSearchPercent")
    def leaf_nodes_to_search_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "leafNodesToSearchPercent"))

    @leaf_nodes_to_search_percent.setter
    def leaf_nodes_to_search_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0c015648da2849e19fc1ad4313060459567734a7ce5489615511d1063cdd772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "leafNodesToSearchPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig]:
        return typing.cast(typing.Optional[VertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afe57b20fd77bba1ac4879636a754fde9208bae940062b3d6b523456b204cca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiIndexMetadataConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiIndex.VertexAiIndexMetadataConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c47b8ad3fc423b4ff20f04716453d8d3fce06039801def4b26d98acadda7eb1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAlgorithmConfig")
    def put_algorithm_config(
        self,
        *,
        brute_force_config: typing.Optional[typing.Union[VertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        tree_ah_config: typing.Optional[typing.Union[VertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param brute_force_config: brute_force_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#brute_force_config VertexAiIndex#brute_force_config}
        :param tree_ah_config: tree_ah_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#tree_ah_config VertexAiIndex#tree_ah_config}
        '''
        value = VertexAiIndexMetadataConfigAlgorithmConfig(
            brute_force_config=brute_force_config, tree_ah_config=tree_ah_config
        )

        return typing.cast(None, jsii.invoke(self, "putAlgorithmConfig", [value]))

    @jsii.member(jsii_name="resetAlgorithmConfig")
    def reset_algorithm_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlgorithmConfig", []))

    @jsii.member(jsii_name="resetApproximateNeighborsCount")
    def reset_approximate_neighbors_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApproximateNeighborsCount", []))

    @jsii.member(jsii_name="resetDistanceMeasureType")
    def reset_distance_measure_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDistanceMeasureType", []))

    @jsii.member(jsii_name="resetFeatureNormType")
    def reset_feature_norm_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFeatureNormType", []))

    @jsii.member(jsii_name="resetShardSize")
    def reset_shard_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShardSize", []))

    @builtins.property
    @jsii.member(jsii_name="algorithmConfig")
    def algorithm_config(
        self,
    ) -> VertexAiIndexMetadataConfigAlgorithmConfigOutputReference:
        return typing.cast(VertexAiIndexMetadataConfigAlgorithmConfigOutputReference, jsii.get(self, "algorithmConfig"))

    @builtins.property
    @jsii.member(jsii_name="algorithmConfigInput")
    def algorithm_config_input(
        self,
    ) -> typing.Optional[VertexAiIndexMetadataConfigAlgorithmConfig]:
        return typing.cast(typing.Optional[VertexAiIndexMetadataConfigAlgorithmConfig], jsii.get(self, "algorithmConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="approximateNeighborsCountInput")
    def approximate_neighbors_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "approximateNeighborsCountInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionsInput")
    def dimensions_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dimensionsInput"))

    @builtins.property
    @jsii.member(jsii_name="distanceMeasureTypeInput")
    def distance_measure_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "distanceMeasureTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="featureNormTypeInput")
    def feature_norm_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "featureNormTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="shardSizeInput")
    def shard_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shardSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="approximateNeighborsCount")
    def approximate_neighbors_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "approximateNeighborsCount"))

    @approximate_neighbors_count.setter
    def approximate_neighbors_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c246190a136c80ec322cbe5298015854e6b4f96c86376328b798dff2bd62be51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "approximateNeighborsCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dimensions")
    def dimensions(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dimensions"))

    @dimensions.setter
    def dimensions(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be907e8afb7e1ab291e83e3f31b0426dc83630f04c4d7d5b3ab3aadd28b91057)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dimensions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="distanceMeasureType")
    def distance_measure_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "distanceMeasureType"))

    @distance_measure_type.setter
    def distance_measure_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c2baa0048e337800654e0ac9b8634e35fb5ff0545a9bbf4c3002649e9e0437)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distanceMeasureType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="featureNormType")
    def feature_norm_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "featureNormType"))

    @feature_norm_type.setter
    def feature_norm_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5a92da137146867d4d5628a39f594d1363a7f51dd65a395490a5434440ca815)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "featureNormType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shardSize")
    def shard_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shardSize"))

    @shard_size.setter
    def shard_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fb1c75b00d3ce9ca5419012f71fe65ff7bfb0c272ec359f50756bf6a95c6674)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shardSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VertexAiIndexMetadataConfig]:
        return typing.cast(typing.Optional[VertexAiIndexMetadataConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiIndexMetadataConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54490ecc4e7242c72bf8247f29e4a8d6687c881486451e9fc8a08be9cc013ee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiIndexMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiIndex.VertexAiIndexMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__842252725a906d4ff1158448e6c50bb0cfba21f2332053c12ae4bdbf93bf7788)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        dimensions: jsii.Number,
        algorithm_config: typing.Optional[typing.Union[VertexAiIndexMetadataConfigAlgorithmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        approximate_neighbors_count: typing.Optional[jsii.Number] = None,
        distance_measure_type: typing.Optional[builtins.str] = None,
        feature_norm_type: typing.Optional[builtins.str] = None,
        shard_size: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dimensions: The number of dimensions of the input vectors. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#dimensions VertexAiIndex#dimensions}
        :param algorithm_config: algorithm_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#algorithm_config VertexAiIndex#algorithm_config}
        :param approximate_neighbors_count: The default number of neighbors to find via approximate search before exact reordering is performed. Exact reordering is a procedure where results returned by an approximate search algorithm are reordered via a more expensive distance computation. Required if tree-AH algorithm is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#approximate_neighbors_count VertexAiIndex#approximate_neighbors_count}
        :param distance_measure_type: The distance measure used in nearest neighbor search. The value must be one of the followings: - SQUARED_L2_DISTANCE: Euclidean (L_2) Distance - L1_DISTANCE: Manhattan (L_1) Distance - COSINE_DISTANCE: Cosine Distance. Defined as 1 - cosine similarity. - DOT_PRODUCT_DISTANCE: Dot Product Distance. Defined as a negative of the dot product Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#distance_measure_type VertexAiIndex#distance_measure_type}
        :param feature_norm_type: Type of normalization to be carried out on each vector. The value must be one of the followings: - UNIT_L2_NORM: Unit L2 normalization type - NONE: No normalization type is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#feature_norm_type VertexAiIndex#feature_norm_type}
        :param shard_size: Index data is split into equal parts to be processed. These are called "shards". The shard size must be specified when creating an index. The value must be one of the followings: - SHARD_SIZE_SMALL: Small (2GB) - SHARD_SIZE_MEDIUM: Medium (20GB) - SHARD_SIZE_LARGE: Large (50GB) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#shard_size VertexAiIndex#shard_size}
        '''
        value = VertexAiIndexMetadataConfig(
            dimensions=dimensions,
            algorithm_config=algorithm_config,
            approximate_neighbors_count=approximate_neighbors_count,
            distance_measure_type=distance_measure_type,
            feature_norm_type=feature_norm_type,
            shard_size=shard_size,
        )

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="resetConfig")
    def reset_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfig", []))

    @jsii.member(jsii_name="resetContentsDeltaUri")
    def reset_contents_delta_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentsDeltaUri", []))

    @jsii.member(jsii_name="resetIsCompleteOverwrite")
    def reset_is_complete_overwrite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsCompleteOverwrite", []))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> VertexAiIndexMetadataConfigOutputReference:
        return typing.cast(VertexAiIndexMetadataConfigOutputReference, jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional[VertexAiIndexMetadataConfig]:
        return typing.cast(typing.Optional[VertexAiIndexMetadataConfig], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="contentsDeltaUriInput")
    def contents_delta_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentsDeltaUriInput"))

    @builtins.property
    @jsii.member(jsii_name="isCompleteOverwriteInput")
    def is_complete_overwrite_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isCompleteOverwriteInput"))

    @builtins.property
    @jsii.member(jsii_name="contentsDeltaUri")
    def contents_delta_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentsDeltaUri"))

    @contents_delta_uri.setter
    def contents_delta_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10a50635e8e8425ee12f6de7b6503dc4451caa649d1d331b2b38d08c5c23915e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentsDeltaUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isCompleteOverwrite")
    def is_complete_overwrite(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isCompleteOverwrite"))

    @is_complete_overwrite.setter
    def is_complete_overwrite(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__938d3ce0f6e2b9a47cf64f006be0dd6d455e0a94d1a7625ff078fb2fcd1a4bce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isCompleteOverwrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VertexAiIndexMetadata]:
        return typing.cast(typing.Optional[VertexAiIndexMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VertexAiIndexMetadata]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__130af001eff5dd83fcd71b7b4e688de93f2d5df76f343f6498d6785b07260a60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiIndex.VertexAiIndexTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class VertexAiIndexTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#create VertexAiIndex#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#delete VertexAiIndex#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#update VertexAiIndex#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__573540121c5308a4424a29f792f7c14587f34518ec87151d590b5550fbcdf00c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#create VertexAiIndex#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#delete VertexAiIndex#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index#update VertexAiIndex#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiIndexTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiIndexTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiIndex.VertexAiIndexTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e17486a6d33e5f891c2af6764a9b31bad27c20008c5774f6f7896aec91cfa3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a092c2b7f21256c0c2085cf5097ef2e89f0064e73e86214aec449ec2e38cc29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7727065b1cd82db057dca9222ebf3ffb033c6ebbd3dcb38ce3e7cfed641fa0b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ef5e7f0c0a7e2dbc85b8099b31491930a7a59a79f762402462c87151dd434e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiIndexTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiIndexTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiIndexTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a22119e95d931b2b854a4250e266c56e013e78e0acf3c8c15e9f78ac4f8ae60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VertexAiIndex",
    "VertexAiIndexConfig",
    "VertexAiIndexDeployedIndexes",
    "VertexAiIndexDeployedIndexesList",
    "VertexAiIndexDeployedIndexesOutputReference",
    "VertexAiIndexIndexStats",
    "VertexAiIndexIndexStatsList",
    "VertexAiIndexIndexStatsOutputReference",
    "VertexAiIndexMetadata",
    "VertexAiIndexMetadataConfig",
    "VertexAiIndexMetadataConfigAlgorithmConfig",
    "VertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig",
    "VertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfigOutputReference",
    "VertexAiIndexMetadataConfigAlgorithmConfigOutputReference",
    "VertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig",
    "VertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfigOutputReference",
    "VertexAiIndexMetadataConfigOutputReference",
    "VertexAiIndexMetadataOutputReference",
    "VertexAiIndexTimeouts",
    "VertexAiIndexTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__4b7076b26580b2f525ea3e36739fd080577bc3926fa6f7a6480fd3f5b955f1a8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    index_update_method: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata: typing.Optional[typing.Union[VertexAiIndexMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VertexAiIndexTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__a5e757214fd8abd3798b360c361084430dc43d29bbf0f412ea5fa6a718e34e29(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7563902c2a93f33c4baaa026cac9f6c84d1ba958a049af49db40ddb13e00cc3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f86db3723738b2a9a83fbf2b786b2d03a85319b492a85bef2e4322557ca1351(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65712878d2466377ffeb5befe76c4a1a2dc099818f5299b7539a9bfc818ec1fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e490edf3138e6c96191c8ae627eb3bec6394a01b3f3c1f9d1e9f06eae6f2ff68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1711fbca13dfd773731181d6dcb4f64d9d779f60a664d61c105840f1f5e69cb4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d302d07c93e89418a38747df9f393c44688109eb23e7227db8492d0c2b9080e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9868f10e3782437a430767133705fdf16c686469f9469d310e34a7aa8a725349(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0126877dbafd6883709f6ec67439a1762436c7d6a7ab3b81fd0ee1df9f65337c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    index_update_method: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata: typing.Optional[typing.Union[VertexAiIndexMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VertexAiIndexTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e92746e71dea095ede5f2d80aa54ec4c59e6ba9d800f527c852001411f06e3e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde63c1d221e9ea78e4f21bed913be572428ba28845b0567ecd266f9f80bbda7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2973accc9879ba24a2d40dec660a8e1c3ca91e811ab36ab4fb27cf0f7d335ad9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__004234377cb06f6eb67e78ba2969bc0a48990463cd15937308c4c903ff063d61(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb9837de2d85ce51d8a8a6c313c224184a0a5f00609c7fb954c29cc41df053af(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad24836040cb8a10b66b8d4a6945bb2de99aa62315d48823870a5be586e18ebb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__608707c4dc41d2d5221d161ee57cd4875a3e20186c4acfa8d9bb814400c5c0eb(
    value: typing.Optional[VertexAiIndexDeployedIndexes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c87cc697b50850c45620e382b2f30404fd589af2d5c56b20571a24aa2d8122(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9058e41ef51f9cacd3cd22b7076b2281104d77fb08749713c694ba9004b83662(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3154f280509c6c7d5a5a9819427252653de8d39fe69b2f406e968df64273fd27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecc956efbc9d1987ab820ec816bb7d597f67ef9738c4b0237f85d19bddf97003(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa530a8f473a9d8d3eadac0d1fca205dfdca0bdf63a6f8fafff4b3b6abf58417(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc385f7aed9543f76bc65891e7358219fa3434c4b77a47aaa211b7afb871025e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ef11e5d00d02825b5e6b828e11f4c6b695f3bf538fd569ca5eabb2516729e4(
    value: typing.Optional[VertexAiIndexIndexStats],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7d0caeb99ed92a048aa59a2e7440c4b724861f8c17e6dd056c384dc5b6d1b4c(
    *,
    config: typing.Optional[typing.Union[VertexAiIndexMetadataConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    contents_delta_uri: typing.Optional[builtins.str] = None,
    is_complete_overwrite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c65b98db650b9656406d5a3874f903ac0bea58541cb19846b06a26d524049aa4(
    *,
    dimensions: jsii.Number,
    algorithm_config: typing.Optional[typing.Union[VertexAiIndexMetadataConfigAlgorithmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    approximate_neighbors_count: typing.Optional[jsii.Number] = None,
    distance_measure_type: typing.Optional[builtins.str] = None,
    feature_norm_type: typing.Optional[builtins.str] = None,
    shard_size: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1dfaee87e3155ed4eb2a6cf272aec1a576be8077027590c1bba0eae5ac8d05e(
    *,
    brute_force_config: typing.Optional[typing.Union[VertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tree_ah_config: typing.Optional[typing.Union[VertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62852922e44ffbcf600144bb06159f30b28cc5234ba0440c08aec8d946209f4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__066054f1f2ce42107ef85f203cce7b07d773346553ac146fe4b5ce0146e44264(
    value: typing.Optional[VertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325151a502e54a33776c4fac1beae0bff03cce0d7e0775cf8a95121352b3075d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b368ef0bf68796d9ae73c415fe3af3496bfc0626ce29c5314018de55920a15c(
    value: typing.Optional[VertexAiIndexMetadataConfigAlgorithmConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9800582b6ed7f8f6095b3c1f88a2f6445c8e6eb4133ac5131f2c37db4686318(
    *,
    leaf_node_embedding_count: typing.Optional[jsii.Number] = None,
    leaf_nodes_to_search_percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de9d7e2a1e81aa0bee256db991410632176c799ae7f04feb11b262c06065b478(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c056ce3f3fd47f822745184c4577305e5fa97ea595169feef8712d04c7a3b5a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0c015648da2849e19fc1ad4313060459567734a7ce5489615511d1063cdd772(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afe57b20fd77bba1ac4879636a754fde9208bae940062b3d6b523456b204cca9(
    value: typing.Optional[VertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c47b8ad3fc423b4ff20f04716453d8d3fce06039801def4b26d98acadda7eb1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c246190a136c80ec322cbe5298015854e6b4f96c86376328b798dff2bd62be51(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be907e8afb7e1ab291e83e3f31b0426dc83630f04c4d7d5b3ab3aadd28b91057(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c2baa0048e337800654e0ac9b8634e35fb5ff0545a9bbf4c3002649e9e0437(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5a92da137146867d4d5628a39f594d1363a7f51dd65a395490a5434440ca815(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fb1c75b00d3ce9ca5419012f71fe65ff7bfb0c272ec359f50756bf6a95c6674(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54490ecc4e7242c72bf8247f29e4a8d6687c881486451e9fc8a08be9cc013ee5(
    value: typing.Optional[VertexAiIndexMetadataConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__842252725a906d4ff1158448e6c50bb0cfba21f2332053c12ae4bdbf93bf7788(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a50635e8e8425ee12f6de7b6503dc4451caa649d1d331b2b38d08c5c23915e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938d3ce0f6e2b9a47cf64f006be0dd6d455e0a94d1a7625ff078fb2fcd1a4bce(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__130af001eff5dd83fcd71b7b4e688de93f2d5df76f343f6498d6785b07260a60(
    value: typing.Optional[VertexAiIndexMetadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__573540121c5308a4424a29f792f7c14587f34518ec87151d590b5550fbcdf00c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e17486a6d33e5f891c2af6764a9b31bad27c20008c5774f6f7896aec91cfa3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a092c2b7f21256c0c2085cf5097ef2e89f0064e73e86214aec449ec2e38cc29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7727065b1cd82db057dca9222ebf3ffb033c6ebbd3dcb38ce3e7cfed641fa0b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef5e7f0c0a7e2dbc85b8099b31491930a7a59a79f762402462c87151dd434e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a22119e95d931b2b854a4250e266c56e013e78e0acf3c8c15e9f78ac4f8ae60(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiIndexTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
