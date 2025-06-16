r'''
# `google_vertex_ai_index`

Refer to the Terraform Registry for docs: [`google_vertex_ai_index`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index).
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


class GoogleVertexAiIndex(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndex.GoogleVertexAiIndex",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index google_vertex_ai_index}.'''

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
        metadata: typing.Optional[typing.Union["GoogleVertexAiIndexMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleVertexAiIndexTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index google_vertex_ai_index} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: The display name of the Index. The name can be up to 128 characters long and can consist of any UTF-8 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#display_name GoogleVertexAiIndex#display_name}
        :param description: The description of the Index. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#description GoogleVertexAiIndex#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#id GoogleVertexAiIndex#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param index_update_method: The update method to use with this Index. The value must be the followings. If not set, BATCH_UPDATE will be used by default. - BATCH_UPDATE: user can call indexes.patch with files on Cloud Storage of datapoints to update. - STREAM_UPDATE: user can call indexes.upsertDatapoints/DeleteDatapoints to update the Index and the updates will be applied in corresponding DeployedIndexes in nearly real-time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#index_update_method GoogleVertexAiIndex#index_update_method}
        :param labels: The labels with user-defined metadata to organize your Indexes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#labels GoogleVertexAiIndex#labels}
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#metadata GoogleVertexAiIndex#metadata}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#project GoogleVertexAiIndex#project}.
        :param region: The region of the index. eg us-central1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#region GoogleVertexAiIndex#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#timeouts GoogleVertexAiIndex#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab867be7ef557318c31359acdf6f1e528d47eaa000f825953925c48272a77377)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleVertexAiIndexConfig(
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
        '''Generates CDKTF code for importing a GoogleVertexAiIndex resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleVertexAiIndex to import.
        :param import_from_id: The id of the existing GoogleVertexAiIndex that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleVertexAiIndex to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fc49a2f1e0b8086ab5f4699035d070a045f0d12c9267241a680e0e6143d2811)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMetadata")
    def put_metadata(
        self,
        *,
        config: typing.Optional[typing.Union["GoogleVertexAiIndexMetadataConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        contents_delta_uri: typing.Optional[builtins.str] = None,
        is_complete_overwrite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#config GoogleVertexAiIndex#config}
        :param contents_delta_uri: Allows inserting, updating or deleting the contents of the Matching Engine Index. The string must be a valid Cloud Storage directory path. If this field is set when calling IndexService.UpdateIndex, then no other Index field can be also updated as part of the same call. The expected structure and format of the files this URI points to is described at https://cloud.google.com/vertex-ai/docs/matching-engine/using-matching-engine#input-data-format Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#contents_delta_uri GoogleVertexAiIndex#contents_delta_uri}
        :param is_complete_overwrite: If this field is set together with contentsDeltaUri when calling IndexService.UpdateIndex, then existing content of the Index will be replaced by the data from the contentsDeltaUri. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#is_complete_overwrite GoogleVertexAiIndex#is_complete_overwrite}
        '''
        value = GoogleVertexAiIndexMetadata(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#create GoogleVertexAiIndex#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#delete GoogleVertexAiIndex#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#update GoogleVertexAiIndex#update}.
        '''
        value = GoogleVertexAiIndexTimeouts(
            create=create, delete=delete, update=update
        )

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
    def deployed_indexes(self) -> "GoogleVertexAiIndexDeployedIndexesList":
        return typing.cast("GoogleVertexAiIndexDeployedIndexesList", jsii.get(self, "deployedIndexes"))

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
    def index_stats(self) -> "GoogleVertexAiIndexIndexStatsList":
        return typing.cast("GoogleVertexAiIndexIndexStatsList", jsii.get(self, "indexStats"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> "GoogleVertexAiIndexMetadataOutputReference":
        return typing.cast("GoogleVertexAiIndexMetadataOutputReference", jsii.get(self, "metadata"))

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
    def timeouts(self) -> "GoogleVertexAiIndexTimeoutsOutputReference":
        return typing.cast("GoogleVertexAiIndexTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    def metadata_input(self) -> typing.Optional["GoogleVertexAiIndexMetadata"]:
        return typing.cast(typing.Optional["GoogleVertexAiIndexMetadata"], jsii.get(self, "metadataInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleVertexAiIndexTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleVertexAiIndexTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af09f185d284da6539a444b26c07add8442dd879c5be14980562a06219af7450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b66046b9d7527e5addd82359b0d9a53e11ea246813a91aa359d4ef68e20ef06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a5c28055b8df795fc252b9a746e8da8ec14d118ff7497bb9ebfe555b56f8858)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indexUpdateMethod")
    def index_update_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "indexUpdateMethod"))

    @index_update_method.setter
    def index_update_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0df84d776198911bdbbf63c8719d44c49b54a46a34f4b0946b6a115155034e09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indexUpdateMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__422b56ae5b859b8496a1427e3597746e8994617a95c869cc5c3da99e232ff006)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a768790250b5d52803a80c6e7edbab882b8a7f92e7979d3dd9a149027d09744)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30207f3d72c6573205f2421ac582b4ebb71b1bc93c8e8517ad8205ce51c44441)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndex.GoogleVertexAiIndexConfig",
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
class GoogleVertexAiIndexConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        metadata: typing.Optional[typing.Union["GoogleVertexAiIndexMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleVertexAiIndexTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: The display name of the Index. The name can be up to 128 characters long and can consist of any UTF-8 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#display_name GoogleVertexAiIndex#display_name}
        :param description: The description of the Index. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#description GoogleVertexAiIndex#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#id GoogleVertexAiIndex#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param index_update_method: The update method to use with this Index. The value must be the followings. If not set, BATCH_UPDATE will be used by default. - BATCH_UPDATE: user can call indexes.patch with files on Cloud Storage of datapoints to update. - STREAM_UPDATE: user can call indexes.upsertDatapoints/DeleteDatapoints to update the Index and the updates will be applied in corresponding DeployedIndexes in nearly real-time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#index_update_method GoogleVertexAiIndex#index_update_method}
        :param labels: The labels with user-defined metadata to organize your Indexes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#labels GoogleVertexAiIndex#labels}
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#metadata GoogleVertexAiIndex#metadata}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#project GoogleVertexAiIndex#project}.
        :param region: The region of the index. eg us-central1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#region GoogleVertexAiIndex#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#timeouts GoogleVertexAiIndex#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(metadata, dict):
            metadata = GoogleVertexAiIndexMetadata(**metadata)
        if isinstance(timeouts, dict):
            timeouts = GoogleVertexAiIndexTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a544d5e28a7d60d789e8e616c369e5cb49c12cf76ffb11f8e41a6aa1e1dd083)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#display_name GoogleVertexAiIndex#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the Index.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#description GoogleVertexAiIndex#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#id GoogleVertexAiIndex#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#index_update_method GoogleVertexAiIndex#index_update_method}
        '''
        result = self._values.get("index_update_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The labels with user-defined metadata to organize your Indexes.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#labels GoogleVertexAiIndex#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata(self) -> typing.Optional["GoogleVertexAiIndexMetadata"]:
        '''metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#metadata GoogleVertexAiIndex#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional["GoogleVertexAiIndexMetadata"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#project GoogleVertexAiIndex#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of the index. eg us-central1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#region GoogleVertexAiIndex#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleVertexAiIndexTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#timeouts GoogleVertexAiIndex#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleVertexAiIndexTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiIndexConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndex.GoogleVertexAiIndexDeployedIndexes",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleVertexAiIndexDeployedIndexes:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiIndexDeployedIndexes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiIndexDeployedIndexesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndex.GoogleVertexAiIndexDeployedIndexesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0f5bab26230f5323108ea6877b6600573216328f241f56e722186fad5ad01b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleVertexAiIndexDeployedIndexesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c65d15d02c37a15f8f3ff0627b221448c386171d741e9b30fc4ab9319f41093f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleVertexAiIndexDeployedIndexesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5edaa04d942c93a74cecb9e42b89c3fedaf70881e395e3c8277028463b6a953a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d19e30789be5645694e0fb7eda26ffd997888dddb476c40c111a7ec569f12d73)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef3ef65e08c45c14ff8a689ff06d86d4b053cbd1f36e648fe24b84de14df270d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiIndexDeployedIndexesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndex.GoogleVertexAiIndexDeployedIndexesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0782fcac5fbecb10e52dd9a5fdc97143fb7938b51e6c961d42d698d04d164c0)
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
    def internal_value(self) -> typing.Optional[GoogleVertexAiIndexDeployedIndexes]:
        return typing.cast(typing.Optional[GoogleVertexAiIndexDeployedIndexes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiIndexDeployedIndexes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e8e6eba89f84225c0de3c219c7d3dabcf53b4127644d31db4d63ac5a73e86cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndex.GoogleVertexAiIndexIndexStats",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleVertexAiIndexIndexStats:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiIndexIndexStats(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiIndexIndexStatsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndex.GoogleVertexAiIndexIndexStatsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9caaa0f26ac1b147d436922b3ad5b9d1129fedb411a793a8989ffb53c7c81468)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GoogleVertexAiIndexIndexStatsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbf4b002efad17335949f2063e622f979bad103f35545f79ade34da1d1a237cc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleVertexAiIndexIndexStatsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff81bf318766459934e04508d0cdc5bf2d00e835edbb4783853fa4c5ebe2fd7e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__088816b89cdf3654bb3142e814273d99562811033a9e5693fe05b690b1b525d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30ee98f8d5107e298dd8f2bbdf7be33b9566136c11231f9c77c158c7b15da775)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiIndexIndexStatsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndex.GoogleVertexAiIndexIndexStatsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dc10c0afa7a8d3ffbd0fd3002a8159190473afbb2ae9a424cfcc2d9a8ee9a99)
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
    def internal_value(self) -> typing.Optional[GoogleVertexAiIndexIndexStats]:
        return typing.cast(typing.Optional[GoogleVertexAiIndexIndexStats], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiIndexIndexStats],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57adda4af2c5065fb059992b926d03237836236fd5365371807cdb81b2f21ff7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndex.GoogleVertexAiIndexMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "config": "config",
        "contents_delta_uri": "contentsDeltaUri",
        "is_complete_overwrite": "isCompleteOverwrite",
    },
)
class GoogleVertexAiIndexMetadata:
    def __init__(
        self,
        *,
        config: typing.Optional[typing.Union["GoogleVertexAiIndexMetadataConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        contents_delta_uri: typing.Optional[builtins.str] = None,
        is_complete_overwrite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#config GoogleVertexAiIndex#config}
        :param contents_delta_uri: Allows inserting, updating or deleting the contents of the Matching Engine Index. The string must be a valid Cloud Storage directory path. If this field is set when calling IndexService.UpdateIndex, then no other Index field can be also updated as part of the same call. The expected structure and format of the files this URI points to is described at https://cloud.google.com/vertex-ai/docs/matching-engine/using-matching-engine#input-data-format Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#contents_delta_uri GoogleVertexAiIndex#contents_delta_uri}
        :param is_complete_overwrite: If this field is set together with contentsDeltaUri when calling IndexService.UpdateIndex, then existing content of the Index will be replaced by the data from the contentsDeltaUri. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#is_complete_overwrite GoogleVertexAiIndex#is_complete_overwrite}
        '''
        if isinstance(config, dict):
            config = GoogleVertexAiIndexMetadataConfig(**config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7af80fb3abd9040e766079d9f9ff9fe3f556a7981bfe7493de4144a733d2243)
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
    def config(self) -> typing.Optional["GoogleVertexAiIndexMetadataConfig"]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#config GoogleVertexAiIndex#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["GoogleVertexAiIndexMetadataConfig"], result)

    @builtins.property
    def contents_delta_uri(self) -> typing.Optional[builtins.str]:
        '''Allows inserting, updating  or deleting the contents of the Matching Engine Index.

        The string must be a valid Cloud Storage directory path. If this
        field is set when calling IndexService.UpdateIndex, then no other
        Index field can be also updated as part of the same call.
        The expected structure and format of the files this URI points to is
        described at https://cloud.google.com/vertex-ai/docs/matching-engine/using-matching-engine#input-data-format

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#contents_delta_uri GoogleVertexAiIndex#contents_delta_uri}
        '''
        result = self._values.get("contents_delta_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_complete_overwrite(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If this field is set together with contentsDeltaUri when calling IndexService.UpdateIndex, then existing content of the Index will be replaced by the data from the contentsDeltaUri.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#is_complete_overwrite GoogleVertexAiIndex#is_complete_overwrite}
        '''
        result = self._values.get("is_complete_overwrite")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiIndexMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndex.GoogleVertexAiIndexMetadataConfig",
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
class GoogleVertexAiIndexMetadataConfig:
    def __init__(
        self,
        *,
        dimensions: jsii.Number,
        algorithm_config: typing.Optional[typing.Union["GoogleVertexAiIndexMetadataConfigAlgorithmConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        approximate_neighbors_count: typing.Optional[jsii.Number] = None,
        distance_measure_type: typing.Optional[builtins.str] = None,
        feature_norm_type: typing.Optional[builtins.str] = None,
        shard_size: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dimensions: The number of dimensions of the input vectors. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#dimensions GoogleVertexAiIndex#dimensions}
        :param algorithm_config: algorithm_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#algorithm_config GoogleVertexAiIndex#algorithm_config}
        :param approximate_neighbors_count: The default number of neighbors to find via approximate search before exact reordering is performed. Exact reordering is a procedure where results returned by an approximate search algorithm are reordered via a more expensive distance computation. Required if tree-AH algorithm is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#approximate_neighbors_count GoogleVertexAiIndex#approximate_neighbors_count}
        :param distance_measure_type: The distance measure used in nearest neighbor search. The value must be one of the followings: - SQUARED_L2_DISTANCE: Euclidean (L_2) Distance - L1_DISTANCE: Manhattan (L_1) Distance - COSINE_DISTANCE: Cosine Distance. Defined as 1 - cosine similarity. - DOT_PRODUCT_DISTANCE: Dot Product Distance. Defined as a negative of the dot product Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#distance_measure_type GoogleVertexAiIndex#distance_measure_type}
        :param feature_norm_type: Type of normalization to be carried out on each vector. The value must be one of the followings: - UNIT_L2_NORM: Unit L2 normalization type - NONE: No normalization type is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#feature_norm_type GoogleVertexAiIndex#feature_norm_type}
        :param shard_size: Index data is split into equal parts to be processed. These are called "shards". The shard size must be specified when creating an index. The value must be one of the followings: - SHARD_SIZE_SMALL: Small (2GB) - SHARD_SIZE_MEDIUM: Medium (20GB) - SHARD_SIZE_LARGE: Large (50GB) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#shard_size GoogleVertexAiIndex#shard_size}
        '''
        if isinstance(algorithm_config, dict):
            algorithm_config = GoogleVertexAiIndexMetadataConfigAlgorithmConfig(**algorithm_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b58f4a960ccf9444e5ffc55471a03da141356dee4530ef590ee35e1c7cfadcf0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#dimensions GoogleVertexAiIndex#dimensions}
        '''
        result = self._values.get("dimensions")
        assert result is not None, "Required property 'dimensions' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def algorithm_config(
        self,
    ) -> typing.Optional["GoogleVertexAiIndexMetadataConfigAlgorithmConfig"]:
        '''algorithm_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#algorithm_config GoogleVertexAiIndex#algorithm_config}
        '''
        result = self._values.get("algorithm_config")
        return typing.cast(typing.Optional["GoogleVertexAiIndexMetadataConfigAlgorithmConfig"], result)

    @builtins.property
    def approximate_neighbors_count(self) -> typing.Optional[jsii.Number]:
        '''The default number of neighbors to find via approximate search before exact reordering is performed.

        Exact reordering is a procedure where results returned by an
        approximate search algorithm are reordered via a more expensive distance computation.
        Required if tree-AH algorithm is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#approximate_neighbors_count GoogleVertexAiIndex#approximate_neighbors_count}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#distance_measure_type GoogleVertexAiIndex#distance_measure_type}
        '''
        result = self._values.get("distance_measure_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def feature_norm_type(self) -> typing.Optional[builtins.str]:
        '''Type of normalization to be carried out on each vector.

        The value must be one of the followings:

        - UNIT_L2_NORM: Unit L2 normalization type
        - NONE: No normalization type is specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#feature_norm_type GoogleVertexAiIndex#feature_norm_type}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#shard_size GoogleVertexAiIndex#shard_size}
        '''
        result = self._values.get("shard_size")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiIndexMetadataConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndex.GoogleVertexAiIndexMetadataConfigAlgorithmConfig",
    jsii_struct_bases=[],
    name_mapping={
        "brute_force_config": "bruteForceConfig",
        "tree_ah_config": "treeAhConfig",
    },
)
class GoogleVertexAiIndexMetadataConfigAlgorithmConfig:
    def __init__(
        self,
        *,
        brute_force_config: typing.Optional[typing.Union["GoogleVertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tree_ah_config: typing.Optional[typing.Union["GoogleVertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param brute_force_config: brute_force_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#brute_force_config GoogleVertexAiIndex#brute_force_config}
        :param tree_ah_config: tree_ah_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#tree_ah_config GoogleVertexAiIndex#tree_ah_config}
        '''
        if isinstance(brute_force_config, dict):
            brute_force_config = GoogleVertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig(**brute_force_config)
        if isinstance(tree_ah_config, dict):
            tree_ah_config = GoogleVertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig(**tree_ah_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12d281e3ea9ff14b696480cd191fcda0ae5fe962e85d4acd2e200f7125032de7)
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
    ) -> typing.Optional["GoogleVertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig"]:
        '''brute_force_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#brute_force_config GoogleVertexAiIndex#brute_force_config}
        '''
        result = self._values.get("brute_force_config")
        return typing.cast(typing.Optional["GoogleVertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig"], result)

    @builtins.property
    def tree_ah_config(
        self,
    ) -> typing.Optional["GoogleVertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig"]:
        '''tree_ah_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#tree_ah_config GoogleVertexAiIndex#tree_ah_config}
        '''
        result = self._values.get("tree_ah_config")
        return typing.cast(typing.Optional["GoogleVertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiIndexMetadataConfigAlgorithmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndex.GoogleVertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleVertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndex.GoogleVertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7a9e61fa46ecc486d713c4b976c9be68213c3d788a60c76db1f3f4a5bbfd156)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__436a33039ca970bba3e5c3e6893af83944a9fb354ba00056947e07bddebd935e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiIndexMetadataConfigAlgorithmConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndex.GoogleVertexAiIndexMetadataConfigAlgorithmConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6afb879b784dec329df01469f7f45eaec3838e21c7154ec480c655f67906ec4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBruteForceConfig")
    def put_brute_force_config(self) -> None:
        value = GoogleVertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig()

        return typing.cast(None, jsii.invoke(self, "putBruteForceConfig", [value]))

    @jsii.member(jsii_name="putTreeAhConfig")
    def put_tree_ah_config(
        self,
        *,
        leaf_node_embedding_count: typing.Optional[jsii.Number] = None,
        leaf_nodes_to_search_percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param leaf_node_embedding_count: Number of embeddings on each leaf node. The default value is 1000 if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#leaf_node_embedding_count GoogleVertexAiIndex#leaf_node_embedding_count}
        :param leaf_nodes_to_search_percent: The default percentage of leaf nodes that any query may be searched. Must be in range 1-100, inclusive. The default value is 10 (means 10%) if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#leaf_nodes_to_search_percent GoogleVertexAiIndex#leaf_nodes_to_search_percent}
        '''
        value = GoogleVertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig(
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
    ) -> GoogleVertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfigOutputReference:
        return typing.cast(GoogleVertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfigOutputReference, jsii.get(self, "bruteForceConfig"))

    @builtins.property
    @jsii.member(jsii_name="treeAhConfig")
    def tree_ah_config(
        self,
    ) -> "GoogleVertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfigOutputReference":
        return typing.cast("GoogleVertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfigOutputReference", jsii.get(self, "treeAhConfig"))

    @builtins.property
    @jsii.member(jsii_name="bruteForceConfigInput")
    def brute_force_config_input(
        self,
    ) -> typing.Optional[GoogleVertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig], jsii.get(self, "bruteForceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="treeAhConfigInput")
    def tree_ah_config_input(
        self,
    ) -> typing.Optional["GoogleVertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig"]:
        return typing.cast(typing.Optional["GoogleVertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig"], jsii.get(self, "treeAhConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiIndexMetadataConfigAlgorithmConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiIndexMetadataConfigAlgorithmConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiIndexMetadataConfigAlgorithmConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6d7e15b582a10d63ce74e45375419f54b77496c79be387442fe2a9600073719)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndex.GoogleVertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig",
    jsii_struct_bases=[],
    name_mapping={
        "leaf_node_embedding_count": "leafNodeEmbeddingCount",
        "leaf_nodes_to_search_percent": "leafNodesToSearchPercent",
    },
)
class GoogleVertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig:
    def __init__(
        self,
        *,
        leaf_node_embedding_count: typing.Optional[jsii.Number] = None,
        leaf_nodes_to_search_percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param leaf_node_embedding_count: Number of embeddings on each leaf node. The default value is 1000 if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#leaf_node_embedding_count GoogleVertexAiIndex#leaf_node_embedding_count}
        :param leaf_nodes_to_search_percent: The default percentage of leaf nodes that any query may be searched. Must be in range 1-100, inclusive. The default value is 10 (means 10%) if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#leaf_nodes_to_search_percent GoogleVertexAiIndex#leaf_nodes_to_search_percent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b480accf43cdc44b7541f4a53df3e0c89b2cd48e7e71d7b879e58807d498ddc)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#leaf_node_embedding_count GoogleVertexAiIndex#leaf_node_embedding_count}
        '''
        result = self._values.get("leaf_node_embedding_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def leaf_nodes_to_search_percent(self) -> typing.Optional[jsii.Number]:
        '''The default percentage of leaf nodes that any query may be searched.

        Must be in
        range 1-100, inclusive. The default value is 10 (means 10%) if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#leaf_nodes_to_search_percent GoogleVertexAiIndex#leaf_nodes_to_search_percent}
        '''
        result = self._values.get("leaf_nodes_to_search_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndex.GoogleVertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a217b259bc27642e853c27918a7e3e615984b1cc03dab06d5c074dac8f02cca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7e015b9c33c8aba8781f525ca58260735c839bb834703b90950b62a08db1397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "leafNodeEmbeddingCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="leafNodesToSearchPercent")
    def leaf_nodes_to_search_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "leafNodesToSearchPercent"))

    @leaf_nodes_to_search_percent.setter
    def leaf_nodes_to_search_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf33dfbe0f570c188cb8148b8afc341844d9be164a661da07727e990e7ab9580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "leafNodesToSearchPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1486ffae10010b50aa46716cd20a27a825dbf12674a324a4c0744e46005e8b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiIndexMetadataConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndex.GoogleVertexAiIndexMetadataConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a025d8d6940ceb4736455c06ffc4ac19f673880d129d7676058e7be9ce01daf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAlgorithmConfig")
    def put_algorithm_config(
        self,
        *,
        brute_force_config: typing.Optional[typing.Union[GoogleVertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        tree_ah_config: typing.Optional[typing.Union[GoogleVertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param brute_force_config: brute_force_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#brute_force_config GoogleVertexAiIndex#brute_force_config}
        :param tree_ah_config: tree_ah_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#tree_ah_config GoogleVertexAiIndex#tree_ah_config}
        '''
        value = GoogleVertexAiIndexMetadataConfigAlgorithmConfig(
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
    ) -> GoogleVertexAiIndexMetadataConfigAlgorithmConfigOutputReference:
        return typing.cast(GoogleVertexAiIndexMetadataConfigAlgorithmConfigOutputReference, jsii.get(self, "algorithmConfig"))

    @builtins.property
    @jsii.member(jsii_name="algorithmConfigInput")
    def algorithm_config_input(
        self,
    ) -> typing.Optional[GoogleVertexAiIndexMetadataConfigAlgorithmConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiIndexMetadataConfigAlgorithmConfig], jsii.get(self, "algorithmConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__066b86eb1062d78a36503645c24ea75c45191be89b41efae681b8325f4debf37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "approximateNeighborsCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dimensions")
    def dimensions(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dimensions"))

    @dimensions.setter
    def dimensions(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d521da6c11361ea75655ec7f255953fb8df3fc9f2b23f958ced48f3ba35bc8e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dimensions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="distanceMeasureType")
    def distance_measure_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "distanceMeasureType"))

    @distance_measure_type.setter
    def distance_measure_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fb2a7e8f075272da6b2fc4d40d36325656103a0d3352ccf1f9d327b221385f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distanceMeasureType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="featureNormType")
    def feature_norm_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "featureNormType"))

    @feature_norm_type.setter
    def feature_norm_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66012a951ace924585fba5ace4d52ceacf81f3d1b636c40ba15e811513b1f76f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "featureNormType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shardSize")
    def shard_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shardSize"))

    @shard_size.setter
    def shard_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c90f9c421ef0310773a9f116da7941a734d55915766c575b0b5ed28394af37db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shardSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleVertexAiIndexMetadataConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiIndexMetadataConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiIndexMetadataConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e334edd923c2f133eb3534d0bd1631a99b2913bad6592e77065d38e4c1e02e4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiIndexMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndex.GoogleVertexAiIndexMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0706a73605016f39168003b58d24256d452922a5bee4067f35273eaccbc35d7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        dimensions: jsii.Number,
        algorithm_config: typing.Optional[typing.Union[GoogleVertexAiIndexMetadataConfigAlgorithmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        approximate_neighbors_count: typing.Optional[jsii.Number] = None,
        distance_measure_type: typing.Optional[builtins.str] = None,
        feature_norm_type: typing.Optional[builtins.str] = None,
        shard_size: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dimensions: The number of dimensions of the input vectors. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#dimensions GoogleVertexAiIndex#dimensions}
        :param algorithm_config: algorithm_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#algorithm_config GoogleVertexAiIndex#algorithm_config}
        :param approximate_neighbors_count: The default number of neighbors to find via approximate search before exact reordering is performed. Exact reordering is a procedure where results returned by an approximate search algorithm are reordered via a more expensive distance computation. Required if tree-AH algorithm is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#approximate_neighbors_count GoogleVertexAiIndex#approximate_neighbors_count}
        :param distance_measure_type: The distance measure used in nearest neighbor search. The value must be one of the followings: - SQUARED_L2_DISTANCE: Euclidean (L_2) Distance - L1_DISTANCE: Manhattan (L_1) Distance - COSINE_DISTANCE: Cosine Distance. Defined as 1 - cosine similarity. - DOT_PRODUCT_DISTANCE: Dot Product Distance. Defined as a negative of the dot product Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#distance_measure_type GoogleVertexAiIndex#distance_measure_type}
        :param feature_norm_type: Type of normalization to be carried out on each vector. The value must be one of the followings: - UNIT_L2_NORM: Unit L2 normalization type - NONE: No normalization type is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#feature_norm_type GoogleVertexAiIndex#feature_norm_type}
        :param shard_size: Index data is split into equal parts to be processed. These are called "shards". The shard size must be specified when creating an index. The value must be one of the followings: - SHARD_SIZE_SMALL: Small (2GB) - SHARD_SIZE_MEDIUM: Medium (20GB) - SHARD_SIZE_LARGE: Large (50GB) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#shard_size GoogleVertexAiIndex#shard_size}
        '''
        value = GoogleVertexAiIndexMetadataConfig(
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
    def config(self) -> GoogleVertexAiIndexMetadataConfigOutputReference:
        return typing.cast(GoogleVertexAiIndexMetadataConfigOutputReference, jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional[GoogleVertexAiIndexMetadataConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiIndexMetadataConfig], jsii.get(self, "configInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__26c771ef499845d421fdab861bef9fc7100ca60fab43f40272c8884923d3ef1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdd6c1384a3247c743370719dd4c6dfc31ea79e1bea63945b72061a5ec27c0c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isCompleteOverwrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleVertexAiIndexMetadata]:
        return typing.cast(typing.Optional[GoogleVertexAiIndexMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiIndexMetadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f50e9802d0fbbc3661ae94903a221e76bddc68337e4abc846fe39402d99bcff1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndex.GoogleVertexAiIndexTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleVertexAiIndexTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#create GoogleVertexAiIndex#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#delete GoogleVertexAiIndex#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#update GoogleVertexAiIndex#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcd4d846783a281e5f20d042fbfee7643151e93d36ae6fc993cdbb74aaf070f2)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#create GoogleVertexAiIndex#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#delete GoogleVertexAiIndex#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index#update GoogleVertexAiIndex#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiIndexTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiIndexTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndex.GoogleVertexAiIndexTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a3b83bbd9db5248789c23c59c5131643ac49ba649d5484d0e9350c9ced2e411)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79daf2e30f287c1ea9bde7bcc5e340f06763d41cadfa3edbb0d0cc75a0c3c56b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb7fa72a9f9779e1cc71d3fb6033c151c69de4012153b280fd3cba16d8ce1fa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c939de874c50a6b0f6d2c3db2d6e46f9a7b3b3b53df133239207642ac8ab8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiIndexTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiIndexTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiIndexTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eb7e8e2a4dff274bbea1fc8bde32c8ef961116356f0659f1cf5561ad0549744)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleVertexAiIndex",
    "GoogleVertexAiIndexConfig",
    "GoogleVertexAiIndexDeployedIndexes",
    "GoogleVertexAiIndexDeployedIndexesList",
    "GoogleVertexAiIndexDeployedIndexesOutputReference",
    "GoogleVertexAiIndexIndexStats",
    "GoogleVertexAiIndexIndexStatsList",
    "GoogleVertexAiIndexIndexStatsOutputReference",
    "GoogleVertexAiIndexMetadata",
    "GoogleVertexAiIndexMetadataConfig",
    "GoogleVertexAiIndexMetadataConfigAlgorithmConfig",
    "GoogleVertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig",
    "GoogleVertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfigOutputReference",
    "GoogleVertexAiIndexMetadataConfigAlgorithmConfigOutputReference",
    "GoogleVertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig",
    "GoogleVertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfigOutputReference",
    "GoogleVertexAiIndexMetadataConfigOutputReference",
    "GoogleVertexAiIndexMetadataOutputReference",
    "GoogleVertexAiIndexTimeouts",
    "GoogleVertexAiIndexTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ab867be7ef557318c31359acdf6f1e528d47eaa000f825953925c48272a77377(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    index_update_method: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata: typing.Optional[typing.Union[GoogleVertexAiIndexMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleVertexAiIndexTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4fc49a2f1e0b8086ab5f4699035d070a045f0d12c9267241a680e0e6143d2811(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af09f185d284da6539a444b26c07add8442dd879c5be14980562a06219af7450(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b66046b9d7527e5addd82359b0d9a53e11ea246813a91aa359d4ef68e20ef06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a5c28055b8df795fc252b9a746e8da8ec14d118ff7497bb9ebfe555b56f8858(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0df84d776198911bdbbf63c8719d44c49b54a46a34f4b0946b6a115155034e09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__422b56ae5b859b8496a1427e3597746e8994617a95c869cc5c3da99e232ff006(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a768790250b5d52803a80c6e7edbab882b8a7f92e7979d3dd9a149027d09744(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30207f3d72c6573205f2421ac582b4ebb71b1bc93c8e8517ad8205ce51c44441(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a544d5e28a7d60d789e8e616c369e5cb49c12cf76ffb11f8e41a6aa1e1dd083(
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
    metadata: typing.Optional[typing.Union[GoogleVertexAiIndexMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleVertexAiIndexTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0f5bab26230f5323108ea6877b6600573216328f241f56e722186fad5ad01b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c65d15d02c37a15f8f3ff0627b221448c386171d741e9b30fc4ab9319f41093f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5edaa04d942c93a74cecb9e42b89c3fedaf70881e395e3c8277028463b6a953a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19e30789be5645694e0fb7eda26ffd997888dddb476c40c111a7ec569f12d73(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef3ef65e08c45c14ff8a689ff06d86d4b053cbd1f36e648fe24b84de14df270d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0782fcac5fbecb10e52dd9a5fdc97143fb7938b51e6c961d42d698d04d164c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e8e6eba89f84225c0de3c219c7d3dabcf53b4127644d31db4d63ac5a73e86cb(
    value: typing.Optional[GoogleVertexAiIndexDeployedIndexes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9caaa0f26ac1b147d436922b3ad5b9d1129fedb411a793a8989ffb53c7c81468(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbf4b002efad17335949f2063e622f979bad103f35545f79ade34da1d1a237cc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff81bf318766459934e04508d0cdc5bf2d00e835edbb4783853fa4c5ebe2fd7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088816b89cdf3654bb3142e814273d99562811033a9e5693fe05b690b1b525d3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ee98f8d5107e298dd8f2bbdf7be33b9566136c11231f9c77c158c7b15da775(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc10c0afa7a8d3ffbd0fd3002a8159190473afbb2ae9a424cfcc2d9a8ee9a99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57adda4af2c5065fb059992b926d03237836236fd5365371807cdb81b2f21ff7(
    value: typing.Optional[GoogleVertexAiIndexIndexStats],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7af80fb3abd9040e766079d9f9ff9fe3f556a7981bfe7493de4144a733d2243(
    *,
    config: typing.Optional[typing.Union[GoogleVertexAiIndexMetadataConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    contents_delta_uri: typing.Optional[builtins.str] = None,
    is_complete_overwrite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b58f4a960ccf9444e5ffc55471a03da141356dee4530ef590ee35e1c7cfadcf0(
    *,
    dimensions: jsii.Number,
    algorithm_config: typing.Optional[typing.Union[GoogleVertexAiIndexMetadataConfigAlgorithmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    approximate_neighbors_count: typing.Optional[jsii.Number] = None,
    distance_measure_type: typing.Optional[builtins.str] = None,
    feature_norm_type: typing.Optional[builtins.str] = None,
    shard_size: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d281e3ea9ff14b696480cd191fcda0ae5fe962e85d4acd2e200f7125032de7(
    *,
    brute_force_config: typing.Optional[typing.Union[GoogleVertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tree_ah_config: typing.Optional[typing.Union[GoogleVertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a9e61fa46ecc486d713c4b976c9be68213c3d788a60c76db1f3f4a5bbfd156(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__436a33039ca970bba3e5c3e6893af83944a9fb354ba00056947e07bddebd935e(
    value: typing.Optional[GoogleVertexAiIndexMetadataConfigAlgorithmConfigBruteForceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6afb879b784dec329df01469f7f45eaec3838e21c7154ec480c655f67906ec4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d7e15b582a10d63ce74e45375419f54b77496c79be387442fe2a9600073719(
    value: typing.Optional[GoogleVertexAiIndexMetadataConfigAlgorithmConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b480accf43cdc44b7541f4a53df3e0c89b2cd48e7e71d7b879e58807d498ddc(
    *,
    leaf_node_embedding_count: typing.Optional[jsii.Number] = None,
    leaf_nodes_to_search_percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a217b259bc27642e853c27918a7e3e615984b1cc03dab06d5c074dac8f02cca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7e015b9c33c8aba8781f525ca58260735c839bb834703b90950b62a08db1397(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf33dfbe0f570c188cb8148b8afc341844d9be164a661da07727e990e7ab9580(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1486ffae10010b50aa46716cd20a27a825dbf12674a324a4c0744e46005e8b3(
    value: typing.Optional[GoogleVertexAiIndexMetadataConfigAlgorithmConfigTreeAhConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a025d8d6940ceb4736455c06ffc4ac19f673880d129d7676058e7be9ce01daf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__066b86eb1062d78a36503645c24ea75c45191be89b41efae681b8325f4debf37(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d521da6c11361ea75655ec7f255953fb8df3fc9f2b23f958ced48f3ba35bc8e7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb2a7e8f075272da6b2fc4d40d36325656103a0d3352ccf1f9d327b221385f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66012a951ace924585fba5ace4d52ceacf81f3d1b636c40ba15e811513b1f76f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c90f9c421ef0310773a9f116da7941a734d55915766c575b0b5ed28394af37db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e334edd923c2f133eb3534d0bd1631a99b2913bad6592e77065d38e4c1e02e4a(
    value: typing.Optional[GoogleVertexAiIndexMetadataConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0706a73605016f39168003b58d24256d452922a5bee4067f35273eaccbc35d7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26c771ef499845d421fdab861bef9fc7100ca60fab43f40272c8884923d3ef1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd6c1384a3247c743370719dd4c6dfc31ea79e1bea63945b72061a5ec27c0c0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f50e9802d0fbbc3661ae94903a221e76bddc68337e4abc846fe39402d99bcff1(
    value: typing.Optional[GoogleVertexAiIndexMetadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd4d846783a281e5f20d042fbfee7643151e93d36ae6fc993cdbb74aaf070f2(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3b83bbd9db5248789c23c59c5131643ac49ba649d5484d0e9350c9ced2e411(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79daf2e30f287c1ea9bde7bcc5e340f06763d41cadfa3edbb0d0cc75a0c3c56b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb7fa72a9f9779e1cc71d3fb6033c151c69de4012153b280fd3cba16d8ce1fa4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c939de874c50a6b0f6d2c3db2d6e46f9a7b3b3b53df133239207642ac8ab8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb7e8e2a4dff274bbea1fc8bde32c8ef961116356f0659f1cf5561ad0549744(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiIndexTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
