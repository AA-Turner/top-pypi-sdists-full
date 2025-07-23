r'''
# `google_firestore_index`

Refer to the Terraform Registry for docs: [`google_firestore_index`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index).
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


class FirestoreIndex(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firestoreIndex.FirestoreIndex",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index google_firestore_index}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        collection: builtins.str,
        fields: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FirestoreIndexFields", typing.Dict[builtins.str, typing.Any]]]],
        api_scope: typing.Optional[builtins.str] = None,
        database: typing.Optional[builtins.str] = None,
        density: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        multikey: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        query_scope: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["FirestoreIndexTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index google_firestore_index} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param collection: The collection being indexed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#collection FirestoreIndex#collection}
        :param fields: fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#fields FirestoreIndex#fields}
        :param api_scope: The API scope at which a query is run. Default value: "ANY_API" Possible values: ["ANY_API", "DATASTORE_MODE_API", "MONGODB_COMPATIBLE_API"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#api_scope FirestoreIndex#api_scope}
        :param database: The Firestore database id. Defaults to '"(default)"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#database FirestoreIndex#database}
        :param density: The density configuration for this index. Possible values: ["SPARSE_ALL", "SPARSE_ANY", "DENSE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#density FirestoreIndex#density}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#id FirestoreIndex#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param multikey: Optional. Whether the index is multikey. By default, the index is not multikey. For non-multikey indexes, none of the paths in the index definition reach or traverse an array, except via an explicit array index. For multikey indexes, at most one of the paths in the index definition reach or traverse an array, except via an explicit array index. Violations will result in errors. Note this field only applies to indexes with MONGODB_COMPATIBLE_API ApiScope. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#multikey FirestoreIndex#multikey}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#project FirestoreIndex#project}.
        :param query_scope: The scope at which a query is run. Default value: "COLLECTION" Possible values: ["COLLECTION", "COLLECTION_GROUP", "COLLECTION_RECURSIVE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#query_scope FirestoreIndex#query_scope}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#timeouts FirestoreIndex#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d6dbf2ebb92aa71f9ee8915462235f1ba87257636bce872875b708f0ad6092f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FirestoreIndexConfig(
            collection=collection,
            fields=fields,
            api_scope=api_scope,
            database=database,
            density=density,
            id=id,
            multikey=multikey,
            project=project,
            query_scope=query_scope,
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
        '''Generates CDKTF code for importing a FirestoreIndex resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the FirestoreIndex to import.
        :param import_from_id: The id of the existing FirestoreIndex that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the FirestoreIndex to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ad62271976141c94bc62e035cf0aed5e71d9c0d1cde65832059bf9c835a0109)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFields")
    def put_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FirestoreIndexFields", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__398772710b5223e9b4a5174a1df337d15722c673e9dbcbe143d97e614bc819c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFields", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#create FirestoreIndex#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#delete FirestoreIndex#delete}.
        '''
        value = FirestoreIndexTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetApiScope")
    def reset_api_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiScope", []))

    @jsii.member(jsii_name="resetDatabase")
    def reset_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabase", []))

    @jsii.member(jsii_name="resetDensity")
    def reset_density(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDensity", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMultikey")
    def reset_multikey(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultikey", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetQueryScope")
    def reset_query_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryScope", []))

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
    @jsii.member(jsii_name="fields")
    def fields(self) -> "FirestoreIndexFieldsList":
        return typing.cast("FirestoreIndexFieldsList", jsii.get(self, "fields"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "FirestoreIndexTimeoutsOutputReference":
        return typing.cast("FirestoreIndexTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="apiScopeInput")
    def api_scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="collectionInput")
    def collection_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collectionInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="densityInput")
    def density_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "densityInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldsInput")
    def fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FirestoreIndexFields"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FirestoreIndexFields"]]], jsii.get(self, "fieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="multikeyInput")
    def multikey_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "multikeyInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="queryScopeInput")
    def query_scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FirestoreIndexTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FirestoreIndexTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="apiScope")
    def api_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiScope"))

    @api_scope.setter
    def api_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6431a562778b4de66cb197b528d68a5e26e2e35a5da8b3bafc72acf245f65d78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiScope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="collection")
    def collection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collection"))

    @collection.setter
    def collection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e93473b67d14df63cab6ca27fc191ac9c5c7829e5df61b0264799498bbb46481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f14c267d4306fb080f1c4cc68273958631f9eda63a788dbbc058f44567f7cc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="density")
    def density(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "density"))

    @density.setter
    def density(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d531a8a8f7a32773fd334b7099e17f4c37b702f7728bc00697da4361e06fe03d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "density", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bacd8d3b21a143d096ee64db2f8efe085722bbce6af8aa7424ee1cb3b1628525)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multikey")
    def multikey(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "multikey"))

    @multikey.setter
    def multikey(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb0c0ce7072246282ac67af41be8ed1d2b945ea605063756c59aee7a18ebc105)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multikey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba2f2f613abbcb86314decf0606c2e600fa2b5dfe4f879f4e0d20706859de56f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryScope")
    def query_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryScope"))

    @query_scope.setter
    def query_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5b1904b9345ba29c3753a0d8a73b14e28aab79cef8c8075b465f0e2eac534b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryScope", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firestoreIndex.FirestoreIndexConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "collection": "collection",
        "fields": "fields",
        "api_scope": "apiScope",
        "database": "database",
        "density": "density",
        "id": "id",
        "multikey": "multikey",
        "project": "project",
        "query_scope": "queryScope",
        "timeouts": "timeouts",
    },
)
class FirestoreIndexConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        collection: builtins.str,
        fields: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FirestoreIndexFields", typing.Dict[builtins.str, typing.Any]]]],
        api_scope: typing.Optional[builtins.str] = None,
        database: typing.Optional[builtins.str] = None,
        density: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        multikey: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        query_scope: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["FirestoreIndexTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param collection: The collection being indexed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#collection FirestoreIndex#collection}
        :param fields: fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#fields FirestoreIndex#fields}
        :param api_scope: The API scope at which a query is run. Default value: "ANY_API" Possible values: ["ANY_API", "DATASTORE_MODE_API", "MONGODB_COMPATIBLE_API"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#api_scope FirestoreIndex#api_scope}
        :param database: The Firestore database id. Defaults to '"(default)"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#database FirestoreIndex#database}
        :param density: The density configuration for this index. Possible values: ["SPARSE_ALL", "SPARSE_ANY", "DENSE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#density FirestoreIndex#density}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#id FirestoreIndex#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param multikey: Optional. Whether the index is multikey. By default, the index is not multikey. For non-multikey indexes, none of the paths in the index definition reach or traverse an array, except via an explicit array index. For multikey indexes, at most one of the paths in the index definition reach or traverse an array, except via an explicit array index. Violations will result in errors. Note this field only applies to indexes with MONGODB_COMPATIBLE_API ApiScope. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#multikey FirestoreIndex#multikey}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#project FirestoreIndex#project}.
        :param query_scope: The scope at which a query is run. Default value: "COLLECTION" Possible values: ["COLLECTION", "COLLECTION_GROUP", "COLLECTION_RECURSIVE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#query_scope FirestoreIndex#query_scope}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#timeouts FirestoreIndex#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = FirestoreIndexTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe2877e5cb699770e1e21c9d0a268c5042d40361fcbb1aee66c621f1b3142aaa)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument collection", value=collection, expected_type=type_hints["collection"])
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
            check_type(argname="argument api_scope", value=api_scope, expected_type=type_hints["api_scope"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument density", value=density, expected_type=type_hints["density"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument multikey", value=multikey, expected_type=type_hints["multikey"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument query_scope", value=query_scope, expected_type=type_hints["query_scope"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "collection": collection,
            "fields": fields,
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
        if api_scope is not None:
            self._values["api_scope"] = api_scope
        if database is not None:
            self._values["database"] = database
        if density is not None:
            self._values["density"] = density
        if id is not None:
            self._values["id"] = id
        if multikey is not None:
            self._values["multikey"] = multikey
        if project is not None:
            self._values["project"] = project
        if query_scope is not None:
            self._values["query_scope"] = query_scope
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
    def collection(self) -> builtins.str:
        '''The collection being indexed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#collection FirestoreIndex#collection}
        '''
        result = self._values.get("collection")
        assert result is not None, "Required property 'collection' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fields(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FirestoreIndexFields"]]:
        '''fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#fields FirestoreIndex#fields}
        '''
        result = self._values.get("fields")
        assert result is not None, "Required property 'fields' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FirestoreIndexFields"]], result)

    @builtins.property
    def api_scope(self) -> typing.Optional[builtins.str]:
        '''The API scope at which a query is run. Default value: "ANY_API" Possible values: ["ANY_API", "DATASTORE_MODE_API", "MONGODB_COMPATIBLE_API"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#api_scope FirestoreIndex#api_scope}
        '''
        result = self._values.get("api_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database(self) -> typing.Optional[builtins.str]:
        '''The Firestore database id. Defaults to '"(default)"'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#database FirestoreIndex#database}
        '''
        result = self._values.get("database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def density(self) -> typing.Optional[builtins.str]:
        '''The density configuration for this index. Possible values: ["SPARSE_ALL", "SPARSE_ANY", "DENSE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#density FirestoreIndex#density}
        '''
        result = self._values.get("density")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#id FirestoreIndex#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multikey(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Whether the index is multikey. By default, the index is not multikey. For non-multikey indexes, none of the paths in the index definition reach or traverse an array, except via an explicit array index. For multikey indexes, at most one of the paths in the index definition reach or traverse an array, except via an explicit array index. Violations will result in errors. Note this field only applies to indexes with MONGODB_COMPATIBLE_API ApiScope.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#multikey FirestoreIndex#multikey}
        '''
        result = self._values.get("multikey")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#project FirestoreIndex#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_scope(self) -> typing.Optional[builtins.str]:
        '''The scope at which a query is run. Default value: "COLLECTION" Possible values: ["COLLECTION", "COLLECTION_GROUP", "COLLECTION_RECURSIVE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#query_scope FirestoreIndex#query_scope}
        '''
        result = self._values.get("query_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["FirestoreIndexTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#timeouts FirestoreIndex#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["FirestoreIndexTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirestoreIndexConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firestoreIndex.FirestoreIndexFields",
    jsii_struct_bases=[],
    name_mapping={
        "array_config": "arrayConfig",
        "field_path": "fieldPath",
        "order": "order",
        "vector_config": "vectorConfig",
    },
)
class FirestoreIndexFields:
    def __init__(
        self,
        *,
        array_config: typing.Optional[builtins.str] = None,
        field_path: typing.Optional[builtins.str] = None,
        order: typing.Optional[builtins.str] = None,
        vector_config: typing.Optional[typing.Union["FirestoreIndexFieldsVectorConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param array_config: Indicates that this field supports operations on arrayValues. Only one of 'order', 'arrayConfig', and 'vectorConfig' can be specified. Possible values: ["CONTAINS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#array_config FirestoreIndex#array_config}
        :param field_path: Name of the field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#field_path FirestoreIndex#field_path}
        :param order: Indicates that this field supports ordering by the specified order or comparing using =, <, <=, >, >=. Only one of 'order', 'arrayConfig', and 'vectorConfig' can be specified. Possible values: ["ASCENDING", "DESCENDING"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#order FirestoreIndex#order}
        :param vector_config: vector_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#vector_config FirestoreIndex#vector_config}
        '''
        if isinstance(vector_config, dict):
            vector_config = FirestoreIndexFieldsVectorConfig(**vector_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b3456b73d58d6079ff30fb14b2d454c491db1abd58c2439576f86955f09cc1b)
            check_type(argname="argument array_config", value=array_config, expected_type=type_hints["array_config"])
            check_type(argname="argument field_path", value=field_path, expected_type=type_hints["field_path"])
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
            check_type(argname="argument vector_config", value=vector_config, expected_type=type_hints["vector_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if array_config is not None:
            self._values["array_config"] = array_config
        if field_path is not None:
            self._values["field_path"] = field_path
        if order is not None:
            self._values["order"] = order
        if vector_config is not None:
            self._values["vector_config"] = vector_config

    @builtins.property
    def array_config(self) -> typing.Optional[builtins.str]:
        '''Indicates that this field supports operations on arrayValues.

        Only one of 'order', 'arrayConfig', and
        'vectorConfig' can be specified. Possible values: ["CONTAINS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#array_config FirestoreIndex#array_config}
        '''
        result = self._values.get("array_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def field_path(self) -> typing.Optional[builtins.str]:
        '''Name of the field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#field_path FirestoreIndex#field_path}
        '''
        result = self._values.get("field_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def order(self) -> typing.Optional[builtins.str]:
        '''Indicates that this field supports ordering by the specified order or comparing using =, <, <=, >, >=.

        Only one of 'order', 'arrayConfig', and 'vectorConfig' can be specified. Possible values: ["ASCENDING", "DESCENDING"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#order FirestoreIndex#order}
        '''
        result = self._values.get("order")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vector_config(self) -> typing.Optional["FirestoreIndexFieldsVectorConfig"]:
        '''vector_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#vector_config FirestoreIndex#vector_config}
        '''
        result = self._values.get("vector_config")
        return typing.cast(typing.Optional["FirestoreIndexFieldsVectorConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirestoreIndexFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirestoreIndexFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firestoreIndex.FirestoreIndexFieldsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__536fe2bc78b288a9ac15e8f48bd6731727992530f36ada796073893fcc323f3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FirestoreIndexFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3acc0658839a34edcad5d85b44aff5e329efc6b46601c7f36df954bd052fe81)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FirestoreIndexFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64bf90f225e7efbc3d23cadcb3eaf31a5d2ce007fc022d13098cb89d4a347c4d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cbebd8306f4f9843139294cce9325ee79e843018e1520cc2727b03f1f0f960f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e71c28f30e5e42f8e570889b4bc98608318af9955abc33ab2e8c93c1de4f7e76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirestoreIndexFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirestoreIndexFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirestoreIndexFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b09b18b72e559407e2870ac38ca0ac2144d05a90738d00976f1128b5578ae60d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FirestoreIndexFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firestoreIndex.FirestoreIndexFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60980568ffc4ead3dbf2b9c15347c5e0721c1db7222ce9130d0ec45e311c7725)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putVectorConfig")
    def put_vector_config(
        self,
        *,
        dimension: typing.Optional[jsii.Number] = None,
        flat: typing.Optional[typing.Union["FirestoreIndexFieldsVectorConfigFlat", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dimension: The resulting index will only include vectors of this dimension, and can be used for vector search with the same dimension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#dimension FirestoreIndex#dimension}
        :param flat: flat block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#flat FirestoreIndex#flat}
        '''
        value = FirestoreIndexFieldsVectorConfig(dimension=dimension, flat=flat)

        return typing.cast(None, jsii.invoke(self, "putVectorConfig", [value]))

    @jsii.member(jsii_name="resetArrayConfig")
    def reset_array_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArrayConfig", []))

    @jsii.member(jsii_name="resetFieldPath")
    def reset_field_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldPath", []))

    @jsii.member(jsii_name="resetOrder")
    def reset_order(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrder", []))

    @jsii.member(jsii_name="resetVectorConfig")
    def reset_vector_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVectorConfig", []))

    @builtins.property
    @jsii.member(jsii_name="vectorConfig")
    def vector_config(self) -> "FirestoreIndexFieldsVectorConfigOutputReference":
        return typing.cast("FirestoreIndexFieldsVectorConfigOutputReference", jsii.get(self, "vectorConfig"))

    @builtins.property
    @jsii.member(jsii_name="arrayConfigInput")
    def array_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arrayConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldPathInput")
    def field_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldPathInput"))

    @builtins.property
    @jsii.member(jsii_name="orderInput")
    def order_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orderInput"))

    @builtins.property
    @jsii.member(jsii_name="vectorConfigInput")
    def vector_config_input(
        self,
    ) -> typing.Optional["FirestoreIndexFieldsVectorConfig"]:
        return typing.cast(typing.Optional["FirestoreIndexFieldsVectorConfig"], jsii.get(self, "vectorConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="arrayConfig")
    def array_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arrayConfig"))

    @array_config.setter
    def array_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__847ef72e105872030da7cb454a4e4d675cacfc3577c590ac5f9f1c8ef7fe072e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arrayConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fieldPath")
    def field_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldPath"))

    @field_path.setter
    def field_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c5b188557145d2d30f8be30a589eb5cbe82a51d9c157a327d6a7e2a770f153a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "order"))

    @order.setter
    def order(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__778c8e004619ceda41380085ca0b90f0daef63f0adde61355ae667f75b4e5f03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "order", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirestoreIndexFields]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirestoreIndexFields]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirestoreIndexFields]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f880787c0942a7a0c16fa5be77fd631feac72ec365978cd355cd26c331c6a21f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firestoreIndex.FirestoreIndexFieldsVectorConfig",
    jsii_struct_bases=[],
    name_mapping={"dimension": "dimension", "flat": "flat"},
)
class FirestoreIndexFieldsVectorConfig:
    def __init__(
        self,
        *,
        dimension: typing.Optional[jsii.Number] = None,
        flat: typing.Optional[typing.Union["FirestoreIndexFieldsVectorConfigFlat", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dimension: The resulting index will only include vectors of this dimension, and can be used for vector search with the same dimension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#dimension FirestoreIndex#dimension}
        :param flat: flat block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#flat FirestoreIndex#flat}
        '''
        if isinstance(flat, dict):
            flat = FirestoreIndexFieldsVectorConfigFlat(**flat)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6cc6249d8c5df3011a48fb364f062c4ac45331888164b24d3392f0d03432c48)
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
            check_type(argname="argument flat", value=flat, expected_type=type_hints["flat"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dimension is not None:
            self._values["dimension"] = dimension
        if flat is not None:
            self._values["flat"] = flat

    @builtins.property
    def dimension(self) -> typing.Optional[jsii.Number]:
        '''The resulting index will only include vectors of this dimension, and can be used for vector search with the same dimension.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#dimension FirestoreIndex#dimension}
        '''
        result = self._values.get("dimension")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def flat(self) -> typing.Optional["FirestoreIndexFieldsVectorConfigFlat"]:
        '''flat block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#flat FirestoreIndex#flat}
        '''
        result = self._values.get("flat")
        return typing.cast(typing.Optional["FirestoreIndexFieldsVectorConfigFlat"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirestoreIndexFieldsVectorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firestoreIndex.FirestoreIndexFieldsVectorConfigFlat",
    jsii_struct_bases=[],
    name_mapping={},
)
class FirestoreIndexFieldsVectorConfigFlat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirestoreIndexFieldsVectorConfigFlat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirestoreIndexFieldsVectorConfigFlatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firestoreIndex.FirestoreIndexFieldsVectorConfigFlatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2116fa86961368e427c5adcb6056afca09f71641f7583d4ade56181bf3e10917)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FirestoreIndexFieldsVectorConfigFlat]:
        return typing.cast(typing.Optional[FirestoreIndexFieldsVectorConfigFlat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FirestoreIndexFieldsVectorConfigFlat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b185ef3493c48fde65e6b9270cffb13a9ec34969ca1478c6e896bf23d611de21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FirestoreIndexFieldsVectorConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firestoreIndex.FirestoreIndexFieldsVectorConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35a48e8b156be0120249ee76afb3ff53cc40909c288d3ceebb33cedfea887808)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFlat")
    def put_flat(self) -> None:
        value = FirestoreIndexFieldsVectorConfigFlat()

        return typing.cast(None, jsii.invoke(self, "putFlat", [value]))

    @jsii.member(jsii_name="resetDimension")
    def reset_dimension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDimension", []))

    @jsii.member(jsii_name="resetFlat")
    def reset_flat(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlat", []))

    @builtins.property
    @jsii.member(jsii_name="flat")
    def flat(self) -> FirestoreIndexFieldsVectorConfigFlatOutputReference:
        return typing.cast(FirestoreIndexFieldsVectorConfigFlatOutputReference, jsii.get(self, "flat"))

    @builtins.property
    @jsii.member(jsii_name="dimensionInput")
    def dimension_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dimensionInput"))

    @builtins.property
    @jsii.member(jsii_name="flatInput")
    def flat_input(self) -> typing.Optional[FirestoreIndexFieldsVectorConfigFlat]:
        return typing.cast(typing.Optional[FirestoreIndexFieldsVectorConfigFlat], jsii.get(self, "flatInput"))

    @builtins.property
    @jsii.member(jsii_name="dimension")
    def dimension(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dimension"))

    @dimension.setter
    def dimension(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f87497d7f95d8c1c2d0acef38c504a82578c0e0ffb551210cfba91f660277dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dimension", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FirestoreIndexFieldsVectorConfig]:
        return typing.cast(typing.Optional[FirestoreIndexFieldsVectorConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FirestoreIndexFieldsVectorConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb1311eea1ea81cde2e76039d339f10f91dd5c098e1b752efdabbadb7c7b490)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.firestoreIndex.FirestoreIndexTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class FirestoreIndexTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#create FirestoreIndex#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#delete FirestoreIndex#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4419a46a3be27be4a22b7825e4e5be08ddeb5ac284cf86687262e18c1f60af3)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#create FirestoreIndex#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/firestore_index#delete FirestoreIndex#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirestoreIndexTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirestoreIndexTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.firestoreIndex.FirestoreIndexTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__124ab46af3e032dec2ef7ea287ef5190085938f893240567923ad8a2d417d397)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a1a9e6859e05b3459a1cb2696f0196637ed12438e3ec32c301f6e9f921e5cfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2455c5f2e79f09163c441b429732a8dbc094f13cf5192dcea5c8b6bbbba788bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirestoreIndexTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirestoreIndexTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirestoreIndexTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e56dd0e4b471f5baccaa8374a46abad45c88cfed35d994c7b504809c46d40582)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "FirestoreIndex",
    "FirestoreIndexConfig",
    "FirestoreIndexFields",
    "FirestoreIndexFieldsList",
    "FirestoreIndexFieldsOutputReference",
    "FirestoreIndexFieldsVectorConfig",
    "FirestoreIndexFieldsVectorConfigFlat",
    "FirestoreIndexFieldsVectorConfigFlatOutputReference",
    "FirestoreIndexFieldsVectorConfigOutputReference",
    "FirestoreIndexTimeouts",
    "FirestoreIndexTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__2d6dbf2ebb92aa71f9ee8915462235f1ba87257636bce872875b708f0ad6092f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    collection: builtins.str,
    fields: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FirestoreIndexFields, typing.Dict[builtins.str, typing.Any]]]],
    api_scope: typing.Optional[builtins.str] = None,
    database: typing.Optional[builtins.str] = None,
    density: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    multikey: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    query_scope: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[FirestoreIndexTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__1ad62271976141c94bc62e035cf0aed5e71d9c0d1cde65832059bf9c835a0109(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398772710b5223e9b4a5174a1df337d15722c673e9dbcbe143d97e614bc819c6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FirestoreIndexFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6431a562778b4de66cb197b528d68a5e26e2e35a5da8b3bafc72acf245f65d78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e93473b67d14df63cab6ca27fc191ac9c5c7829e5df61b0264799498bbb46481(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f14c267d4306fb080f1c4cc68273958631f9eda63a788dbbc058f44567f7cc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d531a8a8f7a32773fd334b7099e17f4c37b702f7728bc00697da4361e06fe03d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bacd8d3b21a143d096ee64db2f8efe085722bbce6af8aa7424ee1cb3b1628525(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0c0ce7072246282ac67af41be8ed1d2b945ea605063756c59aee7a18ebc105(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2f2f613abbcb86314decf0606c2e600fa2b5dfe4f879f4e0d20706859de56f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5b1904b9345ba29c3753a0d8a73b14e28aab79cef8c8075b465f0e2eac534b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe2877e5cb699770e1e21c9d0a268c5042d40361fcbb1aee66c621f1b3142aaa(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    collection: builtins.str,
    fields: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FirestoreIndexFields, typing.Dict[builtins.str, typing.Any]]]],
    api_scope: typing.Optional[builtins.str] = None,
    database: typing.Optional[builtins.str] = None,
    density: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    multikey: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    query_scope: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[FirestoreIndexTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b3456b73d58d6079ff30fb14b2d454c491db1abd58c2439576f86955f09cc1b(
    *,
    array_config: typing.Optional[builtins.str] = None,
    field_path: typing.Optional[builtins.str] = None,
    order: typing.Optional[builtins.str] = None,
    vector_config: typing.Optional[typing.Union[FirestoreIndexFieldsVectorConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__536fe2bc78b288a9ac15e8f48bd6731727992530f36ada796073893fcc323f3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3acc0658839a34edcad5d85b44aff5e329efc6b46601c7f36df954bd052fe81(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64bf90f225e7efbc3d23cadcb3eaf31a5d2ce007fc022d13098cb89d4a347c4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cbebd8306f4f9843139294cce9325ee79e843018e1520cc2727b03f1f0f960f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e71c28f30e5e42f8e570889b4bc98608318af9955abc33ab2e8c93c1de4f7e76(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b09b18b72e559407e2870ac38ca0ac2144d05a90738d00976f1128b5578ae60d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FirestoreIndexFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60980568ffc4ead3dbf2b9c15347c5e0721c1db7222ce9130d0ec45e311c7725(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__847ef72e105872030da7cb454a4e4d675cacfc3577c590ac5f9f1c8ef7fe072e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c5b188557145d2d30f8be30a589eb5cbe82a51d9c157a327d6a7e2a770f153a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__778c8e004619ceda41380085ca0b90f0daef63f0adde61355ae667f75b4e5f03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f880787c0942a7a0c16fa5be77fd631feac72ec365978cd355cd26c331c6a21f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirestoreIndexFields]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6cc6249d8c5df3011a48fb364f062c4ac45331888164b24d3392f0d03432c48(
    *,
    dimension: typing.Optional[jsii.Number] = None,
    flat: typing.Optional[typing.Union[FirestoreIndexFieldsVectorConfigFlat, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2116fa86961368e427c5adcb6056afca09f71641f7583d4ade56181bf3e10917(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b185ef3493c48fde65e6b9270cffb13a9ec34969ca1478c6e896bf23d611de21(
    value: typing.Optional[FirestoreIndexFieldsVectorConfigFlat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35a48e8b156be0120249ee76afb3ff53cc40909c288d3ceebb33cedfea887808(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f87497d7f95d8c1c2d0acef38c504a82578c0e0ffb551210cfba91f660277dc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb1311eea1ea81cde2e76039d339f10f91dd5c098e1b752efdabbadb7c7b490(
    value: typing.Optional[FirestoreIndexFieldsVectorConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4419a46a3be27be4a22b7825e4e5be08ddeb5ac284cf86687262e18c1f60af3(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__124ab46af3e032dec2ef7ea287ef5190085938f893240567923ad8a2d417d397(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a1a9e6859e05b3459a1cb2696f0196637ed12438e3ec32c301f6e9f921e5cfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2455c5f2e79f09163c441b429732a8dbc094f13cf5192dcea5c8b6bbbba788bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e56dd0e4b471f5baccaa8374a46abad45c88cfed35d994c7b504809c46d40582(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FirestoreIndexTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
